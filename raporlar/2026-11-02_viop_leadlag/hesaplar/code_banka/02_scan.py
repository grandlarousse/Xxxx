"""Veri güdümlü tarama: 7 banka + XBANK x panel_ret_bistcal'daki TÜM semboller (2014+).
Testler (her biri ayrı aile, BH-FDR q=0.05):
  sync      : corr(bank_t, d_t)
  sync_pc   : kısmi corr(bank_t, d_t | XU100_t)
  gap       : corr(gap_t, d_{t-1})
  gap_pc    : kısmi corr(gap_t, d_{t-1} | XU100 gap_t)  (piyasa ötesi açılış etkisi)
  intra     : corr(intra_t, d_{t-1})   (İŞLENEBİLİR aday)
  intra_x   : corr(intra_t - XU100 intra_t, d_{t-1})  (banka-özgü işlenebilir)
  rev       : kısmi corr(d_t, bank_{t-1} | XU100_{t-1})  (banka önde)
t: White HC0 (z-skorlu). FX(=X) serileri 1 gün geri kaydırıldı (bk.FIX_FX).
"""
import bk, ll, numpy as np, pandas as pd
from scipy import stats
START = pd.Timestamp("2014-01-01")
P = bk.P[bk.P.index >= START].copy()
cat = pd.read_csv(bk.SCR + "/data/catalog.csv").set_index("sym")
# FX (=X) hizalaması artık panelin kendisinde (ll.FX_FIX=True); burada ek kaydırma yok.
keep = [c for c in P.columns if P[c].notna().sum() >= 750 and cat.loc[c, "zero_frac"] < 0.30] if True else list(P.columns)
P = P[keep]
xu = P["XU100.IS"]; xg = bk.dec("XU100", "gap"); xi = bk.dec("XU100", "intra")

def _ht(a, b):
    m = ~(np.isnan(a) | np.isnan(b)); n = m.sum()
    if n < 250: return np.nan, np.nan, n
    a = a[m]; b = b[m]; a = (a - a.mean()) / a.std(); b = (b - b.mean()) / b.std()
    be = (a * b).sum() / (b * b).sum(); e = a - be * b
    se = np.sqrt(((b * e) ** 2).sum()) / (b * b).sum()
    return float(np.dot(a, b) / (n - 1) / 1.0) if False else float(np.corrcoef(a, b)[0, 1]), float(be / se), int(n)

def _res(a, c):
    m = ~(np.isnan(a) | np.isnan(c)); out = np.full(len(a), np.nan)
    if m.sum() < 250: return out
    X = np.c_[np.ones(m.sum()), c[m]]; out[m] = a[m] - X @ np.linalg.lstsq(X, a[m], rcond=None)[0]; return out

def _pct(a, b, c):
    m = ~(np.isnan(a) | np.isnan(b) | np.isnan(c)); aa = np.where(m, a, np.nan); bb = np.where(m, b, np.nan)
    return _ht(_res(aa, c), _res(bb, c))

rows = []
idx = P.index
for st in bk.ALL:
    y = P[ll.T(st)].values
    g = bk.dec(st, "gap").reindex(idx).values; it = bk.dec(st, "intra").reindex(idx).values
    itx = it - xi.reindex(idx).values
    xuv = xu.values; xgv = xg.reindex(idx).values; xuL = xu.shift(1).values
    isis = (idx < bk.SPLIT)
    for d in P.columns:
        if d == ll.T(st): continue
        x = P[d].values; xL = P[d].shift(1).values; yL = P[ll.T(st)].shift(1).values
        tests = {
            "sync": (y, x, None), "sync_pc": (y, x, xuv), "gap": (g, xL, None), "gap_pc": (g, xL, xgv),
            "intra": (it, xL, None), "intra_x": (itx, xL, None), "rev": (x, yL, xuL)}
        for tn, (a, b, c) in tests.items():
            r_, t_, n_ = _pct(a, b, c) if c is not None else _ht(a, b)
            # IS / OOS
            ri, ti, _ = (_pct(np.where(isis, a, np.nan), b, c) if c is not None else _ht(np.where(isis, a, np.nan), b))
            ro, to, _ = (_pct(np.where(~isis, a, np.nan), b, c) if c is not None else _ht(np.where(~isis, a, np.nan), b))
            rows.append((st, d, tn, r_, t_, n_, ri, ti, ro, to))
df = pd.DataFrame(rows, columns=["stock", "driver", "test", "corr", "t", "n", "is_corr", "is_t", "oos_corr", "oos_t"])
df["p"] = 2 * (1 - stats.norm.cdf(df["t"].abs()))
df["fdr_pass"] = False; df["p_adj"] = np.nan
for tn, gdf in df.groupby("test"):
    rej, padj = ll.fdr(gdf["p"].values, 0.05); df.loc[gdf.index, "fdr_pass"] = rej; df.loc[gdf.index, "p_adj"] = padj
df["group"] = df["driver"].map(cat["group"]); df["name"] = df["driver"].map(cat["name"])
df["stable"] = (np.sign(df["is_corr"]) == np.sign(df["oos_corr"])) & (df["is_t"].abs() >= 2) & (df["oos_t"].abs() >= 2)
df.to_parquet(bk.RES + "/scan.parquet")
s = df.groupby("test").agg(n_tests=("p", "size"), n_fdr=("fdr_pass", "sum"), n_stable=("stable", "sum"))
print(s.to_string()); s.to_csv(bk.RES + "/scan_summary.csv")
