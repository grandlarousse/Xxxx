"""v_K1_b: bağımsız yükleyici/araçlar. ll.py ve v_K1_a/vk.py IMPORT EDİLMEZ.
Tanımlar:
  cc_t   = log(adj_t / adj_{t-1})           (temettü+bölünme düzeltmeli kapanış-kapanış)
  intra_t= log(c_t / o_t)                   (aynı gün ham fiyat; açılış müzayedesi -> kapanış müzayedesi)
  gap_t  = cc_t - intra_t                   (temettü düzeltmeli gece getirisi)
Temizlik: fiyat bazında exp(cc)-1 veya exp(gap)-1 ∉ [-%10,5, +%10,5] -> gün atılır (simetrik).
          v<=0, o∉[l,h], o<=0 -> atılır. 2023-02-08 (deprem, BIST işlemleri iptal) satırı silinir, 15.02 getirisi 07.02'ye göre hesaplanır.
"""
import os, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
S = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
DD, H1D, M5D = S + "/data/daily", S + "/data/h1", S + "/data/m5"
OUT = S + "/out/code_v_K1_b"
VIOP = "AEFES AKBNK AKSEN ALARK ARCLK ASELS ASTOR BIMAS BRSAN CIMSA DOAS DOHOL EKGYO ENJSA ENKAI EREGL FROTO GARAN GUBRF HALKB HEKTS ISCTR KCHOL KRDMD MGROS ODAS OYAKC PETKM PGSUS SAHOL SASA SISE SOKM TAVHL TCELL THYAO TKFEN TOASO TRALT TRMET TSKB TTKOM TUPRS ULKER VAKBN VESTL YKBNK".split()
LIM = 0.105
DROP_DAYS = [pd.Timestamp("2023-02-08")]
IS_END = pd.Timestamp("2020-12-31")

def _f(d, sym):
    s = sym if sym.endswith(".IS") or sym.startswith("^") or "=" in sym else sym + ".IS"
    return f"{d}/{s}.parquet"

def raw_daily(sym):
    d = pd.read_parquet(_f(DD, sym))
    d.index = pd.DatetimeIndex(d.pop("ldate").values)
    d = d[~d.index.duplicated(keep="last")].sort_index()
    d = d.drop(index=[x for x in DROP_DAYS if x in d.index])
    return d

def daily(sym, start="2014-01-01", is_index=False):
    d = raw_daily(sym)
    d = d[(d.c > 0) & (d.adj > 0)]
    if not is_index:
        d = d[d.v.fillna(0) > 0]
    cc = np.log(d.adj).diff()
    ok_o = (d.o > 0) & (d.o >= d.l * 0.9999) & (d.o <= d.h * 1.0001)
    intra = np.log(d.c / d.o).where(ok_o)
    gap = cc - intra
    out = pd.DataFrame({"o": d.o, "h": d.h, "l": d.l, "c": d.c, "adj": d.adj, "v": d.v,
                        "cc": cc, "gap": gap, "intra": intra})
    out["tlv"] = d.v * d.c * (d.adj / d.c)  # yaklaşık TL hacim (bölünme düzeltmesi oranlarıyla ölçek önemsiz; rank için)
    out["tlv_raw"] = d.v * d.c
    bad = (np.expm1(out.cc) > LIM) | (np.expm1(out.cc) < -LIM)
    badg = (np.expm1(out.gap) > LIM) | (np.expm1(out.gap) < -LIM)
    out.loc[bad | badg, ["cc", "gap", "intra"]] = np.nan
    return out[out.index >= start]

def h1(sym):
    p = _f(H1D, sym)
    if not os.path.exists(p): return None
    d = pd.read_parquet(p); d = d[~d.index.duplicated(keep="last")].sort_index()
    d["day"] = pd.DatetimeIndex(d.ldate.values); d["hm"] = d.index.hour * 100 + d.index.minute
    return d

def m5(sym):
    p = _f(M5D, sym)
    if not os.path.exists(p): return None
    d = pd.read_parquet(p); d = d[~d.index.duplicated(keep="last")].sort_index()
    d["day"] = pd.DatetimeIndex(d.ldate.values); d["hm"] = d.index.hour * 100 + d.index.minute
    return d

def nwt(x, L=5):
    x = np.asarray(x, float); x = x[np.isfinite(x)]; n = len(x)
    if n < 8: return np.nan, np.nan, n
    m = x.mean(); e = x - m; s = e @ e / n
    for k in range(1, min(L, n - 1) + 1):
        s += 2 * (1 - k / (L + 1)) * (e[k:] @ e[:-k]) / n
    return m, m / np.sqrt(s / n), n

def ols_nw(y, X, L=5):
    y = np.asarray(y, float); X = np.column_stack([np.ones(len(y))] + [np.asarray(c, float) for c in X])
    ok = np.isfinite(y) & np.isfinite(X).all(1); y, X = y[ok], X[ok]
    Q = np.linalg.inv(X.T @ X); b = Q @ X.T @ y; u = y - X @ b; Xu = X * u[:, None]; Sm = Xu.T @ Xu
    for k in range(1, L + 1):
        G = Xu[k:].T @ Xu[:-k]; Sm += (1 - k / (L + 1)) * (G + G.T)
    se = np.sqrt(np.diag(Q @ Sm @ Q)); return b, b / se, len(y)

def bh(p, q=0.05):
    p = np.asarray(p, float); n = len(p); o = np.argsort(p)
    thr = p[o] <= q * np.arange(1, n + 1) / n
    k = (np.where(thr)[0].max() + 1) if thr.any() else 0
    r = np.zeros(n, bool); r[o[:k]] = True; return r

def fade(g, it, thr=0.01, cost=10.0):
    """|gap|>thr günlerinde -sign(gap)*intra (bps) - maliyet"""
    m = (g.abs() > thr) & it.notna() & g.notna()
    return (-np.sign(g[m]) * it[m] * 1e4 - cost)

def summ(x, label=""):
    x = pd.Series(x).dropna()
    m, t, n = nwt(x.values)
    return dict(label=label, n=n, mean=round(m, 1) if n else np.nan, t=round(t, 2) if n else np.nan,
                med=round(x.median(), 1) if n else np.nan, hit=round((x > 0).mean(), 3) if n else np.nan)
