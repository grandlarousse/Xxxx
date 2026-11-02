import sys; sys.path.insert(0, sys.argv[1]); import ll, pandas as pd, numpy as np
P = pd.read_parquet(ll.BASE + "/panel_ret_bistcal.parquet"); D = pd.read_parquet(ll.BASE + "/panel_decomp_bist.parquet")
P = P[P.index >= "2021-01-01"]; D = D[D.index >= "2021-01-01"]
m = P["XU100.IS"]; fx = P["TRY=X"]; es = P["ES=F"]; eem = P["EEM"]
rows = []
for s in ll.VIOP:
    r = P[s + ".IS"]; df = pd.concat([r, m], axis=1).dropna()
    b = np.cov(df.iloc[:, 0], df.iloc[:, 1])[0, 1] / df.iloc[:, 1].var()
    g = D[(s, "gap")]; it = D[(s, "intra")]
    rows.append({"stock": s, "corr_xu100": r.corr(m), "beta_xu100": b, "corr_usdtry": r.corr(fx), "pc_usdtry|xu100": ll.partial_corr(r, fx, [m])[0],
                 "es_sync": r.corr(es), "es_lag1_gap": g.corr(es.shift(1)), "es_lag1_intra": it.corr(es.shift(1)), "eem_lag1_gap": g.corr(eem.shift(1)),
                 "own_gap->intra": it.corr(g)})
T = pd.DataFrame(rows).set_index("stock").round(3)
print(T.sort_values("es_lag1_gap", ascending=False).to_string())
x = D[("XU100", "gap")]; print("XU100 gap~ES lag1 corr", round(x.corr(es.shift(1)), 3), " intra~ES lag1", round(D[("XU100", "intra")].corr(es.shift(1)), 3))
