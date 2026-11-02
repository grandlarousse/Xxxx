"""v_YG2_a / 7: hisse bazında regresyon (y ~ CA + L30 + DAY), HAC yerine 3'lü blok kümeli SE; BH-FDR (kendi uygulamam)."""
import numpy as np, pandas as pd, vcommon as v
from scipy import stats
P = v.load(); S = P[~P.stock.isin(["XU030", "XU100"])]
def bh(p, q=0.10):
    p = np.asarray(p); n = len(p); o = np.argsort(p); th = q * np.arange(1, n + 1) / n
    ok = p[o] <= th; k = np.max(np.where(ok)[0]) + 1 if ok.any() else 0
    rej = np.zeros(n, bool); rej[o[:k]] = True; return rej
rows = []
for y in ["y_gap", "y_c730"]:
    for s, g in S.groupby("stock"):
        d = g[[y, "CA", "L30", "DAY"]].dropna()
        if len(d) < 80: continue
        b, se, n, G = v.ols_cl(d[y].values, d[["CA", "L30", "DAY"]].values, np.arange(len(d)) // 3)
        rows.append(dict(y=y, stock=s, n=n, b_CA=b[1], t_CA=b[1] / se[1]))
R = pd.DataFrame(rows)
for y, g in R.groupby("y"):
    p = 2 * stats.norm.sf(np.abs(g.t_CA.values))
    for q in [0.05, 0.10]:
        R.loc[g.index, f"fdr{int(q*100)}"] = bh(p, q)
    gg = R.loc[g.index]
    print(y, "negatif pay:", round((gg.b_CA < 0).mean(), 3), " FDR5:", int(gg.fdr5.sum()), list(gg[gg.fdr5 == True].stock), " FDR10:", int(gg.fdr10.sum()), " medyan b:", round(gg.b_CA.median(), 3))
R.to_csv(v.RES + "/v7_stock_fdr.csv", index=False)
