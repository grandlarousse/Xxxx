"""v_K1_a bağımsız doğrulama: KENDİ veri yükleyici (ll.py import edilmez)."""
import os, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
S = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
DD = S + "/data/daily"; H1 = S + "/data/h1"; M5 = S + "/data/m5"
OUT = S + "/out/code_v_K1_a"
VIOP = ["AEFES","AKBNK","AKSEN","ALARK","ARCLK","ASELS","ASTOR","BIMAS","BRSAN","CIMSA","DOAS","DOHOL","EKGYO","ENJSA","ENKAI","EREGL","FROTO","GARAN","GUBRF","HALKB","HEKTS","ISCTR","KCHOL","KRDMD","MGROS","ODAS","OYAKC","PETKM","PGSUS","SAHOL","SASA","SISE","SOKM","TAVHL","TCELL","THYAO","TKFEN","TOASO","TRALT","TRMET","TSKB","TTKOM","TUPRS","ULKER","VAKBN","VESTL","YKBNK"]
UP, DN = np.log(1.105), np.log(0.895)
SPLIT = pd.Timestamp("2021-01-01")

def load_daily(sym):
    f = f"{DD}/{sym}.IS.parquet" if not sym.endswith(".IS") else f"{DD}/{sym}.parquet"
    d = pd.read_parquet(f)
    d = d.set_index(pd.DatetimeIndex(d["ldate"].values)).drop(columns="ldate")
    d = d[~d.index.duplicated(keep="last")].sort_index()
    if d["v"].fillna(0).gt(0).mean() > 0.5:  # hisse: hacimsiz günleri at (endeksler hacimsiz olabilir)
        d = d[d["v"].fillna(0) > 0]
    d = d[(d["c"] > 0) & (d["adj"] > 0)]
    return d

def decomp(sym, start="2014-01-01"):
    """cc(adj)=gap+intra. intra=log(c/o) ham fiyat (aynı gün). gap = cc - intra (temettü düzeltmeli gece getirisi).
    Temizlik: cc veya gap fiyat bazında +%10,5 / -%10,5 dışı -> NaN; |intra|>ln(1,25) -> NaN; o<=0 / NaN -> NaN;
    o==önceki c ve h==l (işlem yok gibi) -> NaN."""
    d = load_daily(sym)
    cc = np.log(d["adj"]).diff()
    raw_gap = np.log(d["o"] / d["c"].shift(1))
    intra = np.log(d["c"] / d["o"])
    bad_o = (d["o"] <= 0) | d["o"].isna() | ((d["h"] == d["l"]) & (d["o"] == d["c"].shift(1)))
    intra[bad_o] = np.nan
    gap = cc - intra
    out = pd.DataFrame({"cc": cc, "gap": gap, "intra": intra, "raw_gap": raw_gap, "o": d["o"], "c": d["c"], "h": d["h"], "l": d["l"], "v": d["v"], "tlv": d["v"] * d["c"]})
    badcc = (out.cc > UP) | (out.cc < DN)
    out.loc[badcc, ["cc", "gap", "intra"]] = np.nan
    badg = (out.gap > UP) | (out.gap < DN) | (out.intra.abs() > np.log(1.25))
    out.loc[badg, ["gap", "intra"]] = np.nan
    return out[out.index >= start]

def nw_mean_t(x, lags=5):
    x = np.asarray(x, float); x = x[~np.isnan(x)]; n = len(x)
    if n < 10: return np.nan, np.nan, n
    m = x.mean(); e = x - m
    g0 = (e @ e) / n; s = g0
    for L in range(1, lags + 1):
        w = 1 - L / (lags + 1); s += 2 * w * (e[L:] @ e[:-L]) / n
    return m, m / np.sqrt(s / n), n

def nw_ols(y, X, lags=5):
    """y = X b ; NW standart hatalar. X sabit içermeli."""
    y = np.asarray(y, float); X = np.asarray(X, float)
    ok = ~np.isnan(y) & ~np.isnan(X).any(1); y = y[ok]; X = X[ok]; n = len(y)
    XtX_inv = np.linalg.inv(X.T @ X); b = XtX_inv @ X.T @ y; u = y - X @ b
    Xu = X * u[:, None]; Sm = Xu.T @ Xu
    for L in range(1, lags + 1):
        w = 1 - L / (lags + 1); G = Xu[L:].T @ Xu[:-L]; Sm += w * (G + G.T)
    V = XtX_inv @ Sm @ XtX_inv
    return b, b / np.sqrt(np.diag(V)), n

def bh(p, q=0.05):
    p = np.asarray(p, float); n = len(p); o = np.argsort(p); r = np.empty(n); r[o] = np.arange(1, n + 1)
    thr = p[o] <= q * np.arange(1, n + 1) / n
    k = np.max(np.where(thr)[0]) + 1 if thr.any() else 0
    rej = np.zeros(n, bool); rej[o[:k]] = True
    return rej

def h1(sym):
    f = f"{H1}/{sym}.IS.parquet" if not sym.endswith(".IS") else f"{H1}/{sym}.parquet"
    if not os.path.exists(f): return None
    d = pd.read_parquet(f); d = d[~d.index.duplicated(keep="last")].sort_index()
    d["day"] = pd.DatetimeIndex(d["ldate"].values)
    d["hm"] = d.index.hour * 100 + d.index.minute
    return d

def m5(sym):
    f = f"{M5}/{sym}.IS.parquet" if not sym.endswith(".IS") else f"{M5}/{sym}.parquet"
    if not os.path.exists(f): return None
    d = pd.read_parquet(f); d = d[~d.index.duplicated(keep="last")].sort_index()
    d["day"] = pd.DatetimeIndex(d["ldate"].values)
    d["hm"] = d.index.hour * 100 + d.index.minute
    return d
