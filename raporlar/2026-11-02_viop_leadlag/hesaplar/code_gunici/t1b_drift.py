"""Gece/gün-içi ortalama getiri ayrışması (uzun örneklem, günlük panel 2014+): ortalama gap ve gün-içi (açılış->kapanış) yıllara göre.
'Açılışta sat, kapanışta kapat' (short_open_cover_close) kuralının yıllık kırılımı. Çıktı: results/t1b_drift.csv"""
import pandas as pd, numpy as np, g_common as g
P = pd.read_parquet(g.SCR + "/data/panel_decomp_bist.parquet")
rows = []
syms = [s for s in g.IDX + g.VIOP]
for s in syms:
    try: dd = g.ll.decomp(s)
    except Exception: continue
    dd = dd[dd.index >= "2014-01-01"]
    for y, x in dd.groupby(dd.index.year):
        rows.append(dict(stock=s, year=y, n=x["intra"].notna().sum(), gap_bps=1e4 * x["gap"].mean(), intra_bps=1e4 * x["intra"].mean(),
                         t_intra=g.ll.nw_t(x["intra"])[1]))
R = pd.DataFrame(rows); R.to_csv(g.RES + "/t1b_drift.csv", index=False)
stk = R[R.stock.isin(g.VIOP)]
print(R[R.stock == "XU030"].round(2).to_string(index=False))
print(stk.groupby("year")[["gap_bps", "intra_bps"]].median().round(1).T.to_string())
print("frac stocks intra<0 by year", stk.assign(neg=stk.intra_bps < 0).groupby("year")["neg"].mean().round(2).to_dict())
