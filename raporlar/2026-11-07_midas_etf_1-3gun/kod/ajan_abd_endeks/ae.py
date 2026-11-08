"""abd_endeks ailesi: ortak yardımcılar (kod/lib.py ve kod/strategies.py DEĞİŞTİRİLMEDEN genişletme).

ZAMANLAMA: lib.py sözleşmesine birebir uyar. Sinyal t kapanışına kadarki bilgiyle; olay takvimleri önceden bilinir.
MALİYET: lib.cost_bp ile aynı formül; pozisyon büyüklüğü 1.000 / 2.500 / 10.000 USD için ayrı hesaplanır.
"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
KOD = os.path.dirname(HERE)
sys.path.insert(0, KOD)
import numpy as np, pandas as pd
import lib

ROOT = lib.ROOT
OUT = os.path.join(ROOT, "sonuclar", "aile_abd_endeks")
os.makedirs(OUT, exist_ok=True)

FAM = ("SPY VOO IVV QQQ QQQM DIA IWM MDY RSP VTI TQQQ SQQQ UPRO SPXU SPXL SPXS SSO SDS QLD QID UDOW SDOW TNA TZA "
       "SH PSQ URTY SRTY MTUM QUAL USMV VLUE IWF IWD IWO IWN SCHD JEPI JEPQ VUG VTV SPLV SPHB VIG DGRO DVY NOBL QYLD "
       "XYLD SPYD COWZ AVUV SCHG MGK VYM").split()

# Kopya / aynı dayanak grupları (getiri korelasyonu 2022-06..2026-11 ile doğrulandı; bkz. 01_islenebilirlik.py)
GROUPS = {
    "SP500":      ["SPY", "VOO", "IVV", "VTI"],
    "SP500_kaldirac": ["UPRO", "SPXL", "SSO"],
    "SP500_ters": ["SH", "SDS", "SPXU", "SPXS"],
    "NDX":        ["QQQ", "QQQM"],
    "NDX_kaldirac": ["TQQQ", "QLD"],
    "NDX_ters":   ["PSQ", "QID", "SQQQ"],
    "R2K":        ["IWM"],
    "R2K_kaldirac": ["TNA", "URTY"],
    "R2K_ters":   ["TZA", "SRTY"],
    "DOW":        ["DIA"],
    "DOW_kaldirac": ["UDOW"],
    "DOW_ters":   ["SDOW"],
    "RSP":        ["RSP"],
    "MDY":        ["MDY"],
    "buyume_buyuk": ["IWF", "VUG", "SCHG", "MGK"],
    "deger_buyuk": ["IWD", "VTV", "VYM"],
    "temettu":    ["SCHD", "DGRO", "VIG", "DVY", "NOBL", "SPYD"],
    "dusuk_vol":  ["SPLV", "USMV"],
    "yuksek_beta": ["SPHB"],
    "momentum":   ["MTUM"],
    "kalite":     ["QUAL"],
    "deger_faktor": ["VLUE"],
    "kucuk_buyume": ["IWO"],
    "kucuk_deger": ["IWN", "AVUV"],
    "nakit_akisi": ["COWZ"],
    "kapali_alim_SP": ["JEPI", "XYLD"],
    "kapali_alim_NDX": ["JEPQ", "QYLD"],
}
SYM2GRP = {s: g for g, ss in GROUPS.items() for s in ss}
# Aile içi tutarlılık için grup temsilcileri (kaldıraçsız; her biri farklı dayanak/faktör)
CORE = ["SPY", "QQQ", "IWM", "DIA", "RSP", "MDY"]
FACTOR = ["IWF", "IWD", "SCHD", "SPLV", "SPHB", "MTUM", "QUAL", "VLUE", "IWO", "IWN", "COWZ", "JEPI", "QYLD"]
REPS = CORE + FACTOR
# Kaldıraçlı uygulama araçları: dayanak -> (araç, kaldıraç)
LEV = {"SPY": [("SSO", 2), ("UPRO", 3), ("SPXL", 3)], "QQQ": [("QLD", 2), ("TQQQ", 3)],
       "IWM": [("TNA", 3), ("URTY", 3)], "DIA": [("UDOW", 3)]}
INV = {"SPY": [("SH", -1), ("SDS", -2), ("SPXU", -3), ("SPXS", -3)], "QQQ": [("PSQ", -1), ("QID", -2), ("SQQQ", -3)],
       "IWM": [("TZA", -3), ("SRTY", -3)], "DIA": [("SDOW", -3)]}

POS = (1000.0, 2500.0, 10000.0)

def cost_at(df, pos=2500.0):
    return 2 * lib.COMM_USD / pos * 1e4 + lib.spread_bp_tier(df)

_ctx = None
def ctx():
    global _ctx
    if _ctx is None:
        _ctx = {k: lib.vol_index(k) for k in ("VIX", "VIX3M", "VIX9D", "VVIX")}
    return _ctx

def events(name, kinds=None):
    e = pd.read_csv(os.path.join(ROOT, "data", "events", name + ".csv"), parse_dates=["date"])
    if kinds is not None:
        e = e[e["event"].isin(kinds)]
    return pd.DatetimeIndex(sorted(e["date"].unique()))

def to_series(mask_dates, idx):
    return pd.Series(idx.isin(mask_dates), index=idx)

def _t(x):
    x = np.asarray(x, float); n = len(x)
    if n < 3: return np.nan
    sd = x.std(ddof=1)
    return x.mean() / (sd / math.sqrt(n)) if sd > 0 else np.nan

def full_eval(df, sig, h=1, mode="C0", exit_sig=None, label="", sym="", warm=200):
    """Standart istatistik paketi: 2.500 USD net + 1.000/10.000 USD duyarlılık. sig df.index'e hizalanır."""
    sig = sig.reindex(df.index).fillna(False).astype(bool).copy()
    if warm: sig.iloc[:warm] = False
    c25 = cost_at(df, 2500.0)
    s, tr = lib.evaluate(df, sig, h, mode, c25, exit_sig=exit_sig, label=label)
    s["sym"] = sym; s["n_sig_days"] = int(sig.sum())
    if len(tr):
        g = tr["gross"].values
        for p in (1000.0, 10000.0):
            s[f"net_bp_{int(p)}"] = (g.mean() - cost_at(df, p) / 1e4) * 1e4
        s["worst_gross_bp"] = float(g.min() * 1e4)
        s["p"] = lib.t_to_p(s.get("t", np.nan), s["n"])
        s["p_edge"] = lib.t_to_p(s.get("t_edge", np.nan), s["n"])
    return s, tr

def mode_grid(df, sig, h, exit_sig=None, label="", sym=""):
    """C0/O1/C1 için brüt/net/t."""
    out = {}
    for m in ("C0", "O1", "C1"):
        s, _ = full_eval(df, sig, h, m, exit_sig, label, sym)
        out[m] = s
    return out

def basket_t(trs, key="entry_date"):
    """Aynı tarihte birden fazla ETF'te açılan işlemleri ortalayıp (bağımlılığı azaltır) t hesaplar."""
    if not trs: return np.nan, 0, np.nan
    a = pd.concat(trs)
    if len(a) == 0: return np.nan, 0, np.nan
    b = a.groupby(key)["net"].mean()
    return _t(b.values), len(b), b.mean() * 1e4

def row(s, extra=None):
    keys = ["label", "sym", "mode", "h", "n", "mean_gross_bp", "mean_net_bp", "net_bp_1000", "net_bp_10000", "win", "pf", "t",
            "p", "is_n", "is_net_bp", "is_t", "oos_n", "oos_net_bp", "oos_t", "years_pos_frac", "maxdd", "worst_bp",
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
