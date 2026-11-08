"""metal_madenci ailesi ortak yardımcıları (lib.py / strategies.py DEĞİŞTİRİLMEDEN genişletme).

Zamanlama: lib.py başındaki ZAMANLAMA SÖZLEŞMESİ aynen geçerli (sinyal t kapanışına kadarki bilgiyle;
C0 = t kapanışı, O1 = t+1 açılış, C1 = t+1 kapanış; çıkış girişten h işlem günü sonraki kapanış).
Maliyet: 2 x 1,5 USD komisyon / pozisyon + lib.spread_bp_tier (tam makas).
"""
import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__))
KOD = os.path.dirname(HERE)
if KOD not in sys.path:
    sys.path.insert(0, KOD)
import numpy as np, pandas as pd
import lib, strategies as S

ROOT = lib.ROOT
OUTD = os.path.join(ROOT, "sonuclar", "aile_metal_madenci")
os.makedirs(OUTD, exist_ok=True)

FAM = "GLD IAU GLDM SLV SIVR PPLT PALL CPER DBB UGL GLL AGQ ZSL GDX GDXJ NUGT DUST JNUG JDST SIL SILJ RING COPX XME URA URNM LIT REMX".split()
# Kopya / yakın kopya grupları (bağımsız kanıt DEĞİL)
CLUSTER = {
    "GLD": "altin", "IAU": "altin", "GLDM": "altin", "UGL": "altin", "GLL": "altin",
    "SLV": "gumus", "SIVR": "gumus", "AGQ": "gumus", "ZSL": "gumus",
    "PPLT": "platin", "PALL": "paladyum",
    "CPER": "bakir", "DBB": "baz_metal",
    "GDX": "altin_madenci", "GDXJ": "altin_madenci", "RING": "altin_madenci",
    "NUGT": "altin_madenci", "DUST": "altin_madenci", "JNUG": "altin_madenci", "JDST": "altin_madenci",
    "SIL": "gumus_madenci", "SILJ": "gumus_madenci",
    "COPX": "bakir_madenci", "XME": "metal_madencilik",
    "URA": "uranyum", "URNM": "uranyum", "LIT": "lityum", "REMX": "nadir_toprak",
}
# Her kümeden bir temsilci (kaldıraçsız, en likit): aile geneli "bağımsız" test bunlarla yapılır
REP12 = ["GLD", "SLV", "PPLT", "PALL", "CPER", "GDX", "SIL", "COPX", "XME", "URA", "LIT", "REMX"]
# Kaldıraçsız uzun ETF'lerin geniş listesi (kopyalar hariç)
REP17 = ["GLD", "SLV", "PPLT", "PALL", "CPER", "DBB", "GDX", "GDXJ", "SIL", "SILJ", "RING", "COPX", "XME", "URA", "URNM", "LIT", "REMX"]
MINERS = ["GDX", "GDXJ", "RING", "SIL", "SILJ"]
LEV = {"UGL": ("GLD", 2), "GLL": ("GLD", -2), "AGQ": ("SLV", 2), "ZSL": ("SLV", -2),
       "NUGT": ("GDX", 2), "DUST": ("GDX", -2), "JNUG": ("GDXJ", 2), "JDST": ("GDXJ", -2)}

# Ek veri düzeltmesi (lib'e dokunmadan): IAU 2021-03-08 tek günlük hatalı bar
# (IAU +%8,5 iken GLD/GLDM -%1; ertesi gün tam geri dönüş) -> satır atılır.
BAD = {"IAU": ["2021-03-08"]}
# 30 Ocak 2026 gümüş çöküşü (SLV -%28,5) ve ertesi iki haftalık çalkantı: duyarlılık penceresi
SHOCK_WIN = (pd.Timestamp("2026-01-26"), pd.Timestamp("2026-02-13"))

_c = {}
def load(sym):
    if sym in _c:
        return _c[sym].copy()
    df = lib.load(sym)
    for d in BAD.get(sym, []):
        df = df.drop(pd.Timestamp(d), errors="ignore")
    _c[sym] = df
    return df.copy()

def cost(df, pos=2500.0):
    return 2 * lib.COMM_USD / pos * 1e4 + lib.spread_bp_tier(df)

def tv_map():
    t = pd.read_csv(os.path.join(ROOT, "sonuclar", "tv_etf.csv"))
    t = t[t["durum"].astype(str).str.startswith("dogrulandi")]
    return dict(zip(t["sym"], t["tv"]))

def tv_valid():
    t = pd.read_csv(os.path.join(ROOT, "sonuclar", "tv_dogrulama.csv"))
    return set(t[t["durum"].isin(["dogrulandi", "dogrulandi_kanonik"])]["ticker"])

def events(name, kind=None):
    e = pd.read_csv(os.path.join(ROOT, "data", "events", name + ".csv"))
    if kind is not None:
        e = e[e["event"].isin(kind if isinstance(kind, (list, tuple)) else [kind])]
    return pd.DatetimeIndex(pd.to_datetime(e["date"]))

def date_sig(df, dates):
    return pd.Series(df.index.isin(pd.DatetimeIndex(dates)), index=df.index)

def nw_tstat(x, lags):
    """Ortalamanın Newey-West t'si."""
    x = np.asarray(x, float); x = x[np.isfinite(x)]; n = len(x)
    if n < 3: return np.nan
    e = x - x.mean(); s = (e @ e) / n
    for l in range(1, lags + 1):
        if l >= n: break
        s += 2 * (1 - l / (lags + 1)) * (e[l:] @ e[:-l]) / n
    return x.mean() / math.sqrt(s / n) if s > 0 else np.nan

def p_from_t(t, n):
    return lib.t_to_p(t, n)

# ------------------------------------------------------------------ değerlendirme
def full(sym, sig, h, mode, df=None, exit_sig=None, label="", warm=200):
    """Tek ETF x sinyal x h x mod için standart istatistikler + maliyet duyarlılığı + şok penceresi hariç."""
    if df is None: df = load(sym)
    sig = sig.reindex(df.index).fillna(False).astype(bool).copy()
    if warm: sig.iloc[:warm] = False
    c25 = cost(df, 2500)
    s, tr = lib.evaluate(df, sig, h, mode, c25, exit_sig=exit_sig, label=label)
    s["sym"] = sym
    if s.get("n", 0) == 0:
        return s, tr
    s["p"] = p_from_t(s["t"], s["n"])
    s["net_1000_bp"] = s["mean_gross_bp"] - cost(df, 1000)
    s["net_10000_bp"] = s["mean_gross_bp"] - cost(df, 10000)
    m = (tr["sig_date"] >= SHOCK_WIN[0]) & (tr["sig_date"] <= SHOCK_WIN[1])
    x = tr.loc[~m, "net"].values
    s["net_ex2026sok_bp"] = x.mean() * 1e4 if len(x) else np.nan
    s["t_ex2026sok"] = x.mean() / (x.std(ddof=1) / math.sqrt(len(x))) if len(x) > 2 and x.std(ddof=1) > 0 else np.nan
    # en iyi tek işlem çıkarılınca
    if len(tr) > 3:
        y = np.sort(tr["net"].values)[:-1]
        s["net_ex_best_bp"] = y.mean() * 1e4
    return s, tr

def modes(sym, sig, h, df=None, exit_sig=None, warm=200):
    """C0/O1/C1 brüt ve net ortalamaları (mod sağlamlığı)."""
    out = {}
    for md in ("C0", "O1", "C1"):
        s, _ = full(sym, sig, h, md, df=df, exit_sig=exit_sig, warm=warm)
        out[md] = (s.get("n", 0), s.get("mean_gross_bp", np.nan), s.get("mean_net_bp", np.nan), s.get("t", np.nan))
    return out

def yearly(tr):
    if tr is None or len(tr) == 0: return pd.DataFrame()
    g = tr.groupby(tr["sig_date"].dt.year)
    return pd.DataFrame({"n": g.size(), "net_bp": g["net"].mean() * 1e4, "toplam_net_pct": g["net"].sum() * 100})

def pooled(syms, sigfun, h, mode, lags=None, warm=200, dfs=None):
    """Aile geneli havuzlanmış test: her ETF'de çakışmayan işlemler; aynı sinyal günündeki işlemler
    ortalanarak tek 'olay' yapılır (ETF'ler arası bağımlılık) ve olay serisinin Newey-West t'si (lag=h) hesaplanır."""
    rows = []
    for s in syms:
        df = load(s) if dfs is None else dfs[s]
        sig = sigfun(df, s).reindex(df.index).fillna(False).astype(bool)
        if warm: sig.iloc[:warm] = False
        tr = lib.trades(df, sig, h, mode, cost=cost(df))
        if len(tr):
            tr["sym"] = s; rows.append(tr)
    if not rows:
        return {"n_ev": 0}, pd.DataFrame()
    T = pd.concat(rows)
    E = T.groupby("sig_date").agg(gross=("gross", "mean"), net=("net", "mean"), k=("sym", "size")).sort_index()
    x = E["net"].values
    res = {"n_tr": len(T), "n_ev": len(E), "gross_bp": E["gross"].mean() * 1e4, "net_bp": x.mean() * 1e4,
           "t_nw": nw_tstat(x, lags if lags is not None else h),
           "win": float((x > 0).mean())}
    for nm, m in (("is", E.index <= lib.IS_END), ("oos", E.index > lib.IS_END)):
        y = E.loc[m, "net"].values
        res[f"{nm}_net_bp"] = y.mean() * 1e4 if len(y) else np.nan
        res[f"{nm}_t"] = nw_tstat(y, lags if lags is not None else h) if len(y) > 3 else np.nan
    yr = E.groupby(E.index.year)["net"].sum()
    res["yil_pozitif"] = float((yr > 0).mean())
    sm = (E.index >= SHOCK_WIN[0]) & (E.index <= SHOCK_WIN[1])
    res["net_ex2026sok_bp"] = E.loc[~sm, "net"].mean() * 1e4
    res["t_ex2026sok"] = nw_tstat(E.loc[~sm, "net"].values, lags if lags is not None else h)
    # ETF başına pozitif sayısı
    per = T.groupby("sym")["net"].mean()
    res["etf_pozitif"] = f"{int((per > 0).sum())}/{len(per)}"
    return res, E

class Registry:
    """Denenen her testin kaydı (BH-FDR için)."""
    def __init__(self, name):
        self.name = name; self.rows = []
    def add(self, test, sym, mode, h, n, t, net_bp=np.nan, extra=None):
        r = {"betik": self.name, "test": test, "sym": sym, "mode": mode, "h": h, "n": n, "t": t,
             "net_bp": net_bp, "p": p_from_t(t, n) if np.isfinite(t) else np.nan}
        if extra: r.update(extra)
        self.rows.append(r)
    def save(self):
        df = pd.DataFrame(self.rows)
        df.to_csv(os.path.join(OUTD, f"testler_{self.name}.csv"), index=False)
        return df

def fmt(s, keys=("n", "mean_gross_bp", "mean_net_bp", "t", "win", "pf", "is_net_bp", "is_t", "oos_net_bp", "oos_t",
                 "years_pos_frac", "maxdd", "worst_bp", "net_1000_bp", "net_10000_bp", "net_ex2026sok_bp")):
    out = []
    for k in keys:
        v = s.get(k, np.nan)
        if isinstance(v, float):
            out.append(f"{k}={v:.2f}" if abs(v) < 1e5 else f"{k}={v:.3g}")
        else:
            out.append(f"{k}={v}")
    return " ".join(out)
