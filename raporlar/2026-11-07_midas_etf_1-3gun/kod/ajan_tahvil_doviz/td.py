"""tahvil_doviz ailesi: ortak yardımcılar (kod/lib.py ve kod/strategies.py DEĞİŞTİRİLMEDEN genişletme).

ZAMANLAMA: lib.py sözleşmesine birebir uyar. Sinyal t kapanışına kadarki bilgiyle hesaplanır; olay takvimleri
(FOMC, CPI, NFP, Hazine ihaleleri, ay sonu) önceden bilinir ve kullanılabilir.
Hazine sabit vadeli getirileri (lib.fred('DGS10') vb.) ~15:30 ET kotasyonlarıdır -> t kapanışında bilinir
(TradingView TVC:US10Y anlık izlenir).
MALİYET: lib.cost_bp ile aynı formül (2 x 1,5 USD komisyon + likidite kademesine göre makas);
pozisyon 1.000 / 2.500 / 10.000 USD için ayrı hesaplanır.
"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
KOD = os.path.dirname(HERE)
sys.path.insert(0, KOD)
import numpy as np, pandas as pd
import lib

ROOT = lib.ROOT
OUT = os.path.join(ROOT, "sonuclar", "aile_tahvil_doviz")
os.makedirs(OUT, exist_ok=True)

TAHVIL = "TLT TMF TMV TBT UBT IEF SHY BIL SGOV AGG BND LQD HYG JNK TIP EMB MUB ZROZ EDV GOVT VCIT IEI TLH SCHP USHY BKLN STIP".split()
DOVIZ = "UUP UDN FXE FXY FXB FXA FXC FXF CEW YCS YCL EUO ULE".split()
FAM = TAHVIL + DOVIZ

# Kopya / aynı dayanak grupları (getiri korelasyonu ile doğrulandı: 01_islenebilirlik.py -> kopya_gruplari.csv)
GROUPS = {
    "uzun_hazine":      ["TLT", "TLH", "EDV", "ZROZ"],      # 10-20 / 20+ / 25+ yıl; TLT temsilci
    "uzun_hazine_kald": ["TMF", "UBT"],                     # 3x / 2x TLT dayanağı
    "uzun_hazine_ters": ["TMV", "TBT"],                     # -3x / -2x
    "orta_hazine":      ["IEF", "IEI", "GOVT"],
    "kisa_hazine":      ["SHY"],
    "hazine_bono":      ["BIL", "SGOV"],                    # nakit benzeri
    "toplam_tahvil":    ["AGG", "BND"],
    "yatirim_kredi":    ["LQD", "VCIT"],
    "yuksek_getiri":    ["HYG", "JNK", "USHY"],
    "kredi_kredisi":    ["BKLN"],
    "tufe_endeksli":    ["TIP", "SCHP"],
    "kisa_tufe":        ["STIP"],
    "gelisen_tahvil":   ["EMB"],
    "belediye":         ["MUB"],
    "usd":              ["UUP", "UDN"],                     # UDN = -UUP
    "eur":              ["FXE", "ULE", "EUO"],              # ULE 2x, EUO -2x
    "jpy":              ["FXY", "YCL", "YCS"],              # YCL 2x, YCS -2x
    "chf":              ["FXF"], "gbp": ["FXB"], "aud": ["FXA"], "cad": ["FXC"], "gelisen_doviz": ["CEW"],
}
SYM2GRP = {s: g for g, ss in GROUPS.items() for s in ss}
# Aile içi tutarlılık temsilcileri (kaldıraçsız, farklı dayanak). Hepsi aynı faiz faktörüne bağlıdır:
# tahvil temsilcileri birbirinin bağımsız kanıtı değil, "farklı vade/kredi kesitleri"dir.
REPS_TAHVIL = ["TLT", "IEF", "SHY", "AGG", "LQD", "HYG", "BKLN", "TIP", "STIP", "EMB", "MUB"]
REPS_FAIZ = ["TLT", "IEF", "AGG", "LQD", "TIP", "MUB", "EMB"]       # faiz (süre) duyarlı çekirdek
REPS_DOVIZ = ["UUP", "FXE", "FXY", "FXF", "FXB", "FXA", "FXC", "CEW"]
REPS = REPS_TAHVIL + REPS_DOVIZ
# Kaldıraçlı/ters araçlar: dayanak -> [(araç, kaldıraç)]
LEV = {"TLT": [("UBT", 2), ("TMF", 3), ("TBT", -2), ("TMV", -3)],
       "FXY": [("YCL", 2), ("YCS", -2)], "FXE": [("ULE", 2), ("EUO", -2)], "UUP": [("UDN", -1)]}

POS = (1000.0, 2500.0, 10000.0)

def cost_at(df, pos=2500.0):
    return 2 * lib.COMM_USD / pos * 1e4 + lib.spread_bp_tier(df)

def events(name, kinds=None):
    e = pd.read_csv(os.path.join(ROOT, "data", "events", name + ".csv"), parse_dates=["date"])
    if kinds is not None:
        e = e[e["event"].isin(kinds)]
    return pd.DatetimeIndex(sorted(e["date"].unique()))

def ev_on_idx(dates, idx, shift=0):
    """Olay tarihlerini işlem günü indeksine oturtur (işlem günü değilse sonraki işlem günü) ve 'shift' işlem günü kaydırır.
    shift=-1: olaydan bir önceki işlem günü. Dönüş: bool Seri (idx)."""
    pos = np.searchsorted(idx.values, pd.DatetimeIndex(dates).values)
    pos = pos[(pos < len(idx))] + shift
    pos = pos[(pos >= 0) & (pos < len(idx))]
    m = np.zeros(len(idx), bool); m[pos] = True
    return pd.Series(m, index=idx)

def _t(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]; n = len(x)
    if n < 3: return np.nan
    sd = x.std(ddof=1)
    return x.mean() / (sd / math.sqrt(n)) if sd > 0 else np.nan

def full_eval(df, sig, h=1, mode="C0", exit_sig=None, label="", sym="", warm=200, cost=None):
    """Standart istatistik paketi: 2.500 USD net + 1.000/10.000 USD duyarlılık. sig df.index'e hizalanır."""
    sig = sig.reindex(df.index).fillna(False).astype(bool).copy()
    if warm: sig.iloc[:warm] = False
    c25 = cost_at(df, 2500.0) if cost is None else cost
    s, tr = lib.evaluate(df, sig, h, mode, c25, exit_sig=exit_sig, label=label)
    s["sym"] = sym; s["n_sig_days"] = int(sig.sum())
    if len(tr):
        g = tr["gross"].values
        for p in (1000.0, 10000.0):
            s[f"net_bp_{int(p)}"] = (g.mean() - (cost_at(df, p) if cost is None else cost) / 1e4) * 1e4
        s["worst_gross_bp"] = float(g.min() * 1e4)
        s["p"] = lib.t_to_p(s.get("t", np.nan), s["n"])
        s["p_edge"] = lib.t_to_p(s.get("t_edge", np.nan), s["n"])
        s["t_gross"] = _t(g)
    return s, tr

def row(s, extra=None):
    keys = ["label", "sym", "mode", "h", "n", "mean_gross_bp", "mean_net_bp", "net_bp_1000", "net_bp_10000", "win", "pf", "t",
            "t_gross", "p", "is_n", "is_net_bp", "is_t", "oos_n", "oos_net_bp", "oos_t", "years_pos_frac", "maxdd", "worst_bp",
            "edge_bp", "t_edge", "cost_bp", "n_sig_days"]
    r = {k: s.get(k, np.nan) for k in keys}
    if extra: r.update(extra)
    return r

def passes(s, min_n=40):
    """Kabul eşiği (mod sağlamlığı ayrıca kontrol edilir)."""
    try:
        return bool(s["n"] >= min_n and s["mean_net_bp"] > 0 and s["t"] >= 2 and s["is_net_bp"] > 0 and s["oos_net_bp"] > 0
                    and s["years_pos_frac"] >= 0.6)
    except Exception:
        return False

def basket(trs, key="entry_date"):
    """Aynı tarihte birden fazla ETF'te açılan işlemleri ortalayıp t hesaplar (bağımlılığı azaltır)."""
    if not trs: return np.nan, 0, np.nan
    a = pd.concat(trs)
    if len(a) == 0: return np.nan, 0, np.nan
    b = a.groupby(key)["net"].mean()
    return _t(b.values), len(b), b.mean() * 1e4

_YDIV = None
_LCACHE = {}
DIV_LOG = []
def _ydiv():
    global _YDIV
    if _YDIV is None:
        fn = os.path.join(OUT, "temettu_yahoo.csv")
        _YDIV = pd.read_csv(fn, parse_dates=["date"]) if os.path.exists(fn) else pd.DataFrame(columns=["sym", "date", "amount", "kind"])
    return _YDIV

def load(sym):
    """lib.load + dağıtım düzeltmesi. Nasdaq verisinde dağıtımı olmayan ETF'ler (NYSE Arca/Cboe listeli) için
    Yahoo Finance dağıtım olayları (00_temettu_indir.py) ile toplam getiri yeniden kurulur. Nasdaq'ta dağıtımı olan
    ETF'ler (TLT, IEF, SHY, BND, EMB, VCIT, IEI) lib.load ile aynen kullanılır (Yahoo ile karşılaştırıldı: 119/120 eşleşme).
    2026-11-02 (Kasım) dağıtımı Yahoo'da henüz yok: aylık ödeyenlerde bir önceki ayın tutarı tahmini olarak eklenir."""
    if sym in _LCACHE: return _LCACHE[sym].copy()
    d = lib.load(sym)
    raw = pd.read_parquet(os.path.join(ROOT, "data", "etf", sym + ".parquet"))
    y = _ydiv(); y = y[(y.sym == sym) & (y.kind == "div")]
    if (raw["div"] > 0).sum() >= 6 or len(y) == 0:
        _LCACHE[sym] = d; return d.copy()
    idx = d.index
    div = pd.Series(0.0, index=idx)
    for dt, a in zip(y["date"], y["amount"]):
        p = idx.searchsorted(dt)
        if 0 < p < len(idx): div.iloc[p] += a
    last12 = y[y.date >= pd.Timestamp("2025-11-01")]
    if len(last12) >= 10 and y.date.max() >= pd.Timestamp("2026-10-01") and y.date.max().day <= 3 \
            and pd.Timestamp("2026-11-02") in idx and y.date.max() < pd.Timestamp("2026-11-02"):
        div.loc[pd.Timestamp("2026-11-02")] += float(y["amount"].iloc[-1]); DIV_LOG.append((sym, "2026-11-02", "tahmin"))
    rc = d["raw_c"]
    tr = (rc + div) / rc.shift(1); tr.iloc[0] = 1.0
    adjc = rc.iloc[-1] * tr.cumprod() / tr.cumprod().iloc[-1]
    f_old = d["c"] / rc; f_new = adjc / rc
    out = d.copy()
    for k in ("o", "h", "l"):
        out[k] = d[k] / f_old * f_new
    out["c"] = adjc; out["div"] = div
    _LCACHE[sym] = out
    return out.copy()

_R = None
def rets():
    """Aile + öncü ETF'lerin log getiri paneli (SPY takvimi)."""
    global _R
    if _R is None:
        idx = lib.load("SPY").index
        R = {}
        for s in FAM + ["SPY", "QQQ", "IWM", "GLD", "CPER", "USO", "EEM", "EWJ"]:
            try:
                R[s] = np.log(load(s)["c"]).diff().reindex(idx)
            except Exception:
                pass
        _R = pd.DataFrame(R)
    return _R.copy()

def yld(name):
    """Hazine getirisi (yüzde) SPY takvimine hizalı, ileri doldurmasız."""
    s = lib.fred(name)
    idx = lib.load("SPY").index
    return s.reindex(idx)
