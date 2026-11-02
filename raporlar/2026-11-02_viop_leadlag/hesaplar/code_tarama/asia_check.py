"""Asya lag1 -> BIST gün-içi (intra_t) etkisinin incelenmesi: dış sürücü mü, yoksa BIST'in kendi gecikmeli gap'inin vekili mi?
Çıktı: cache/asia_check.csv, cache/asia_bt.csv"""
import os, sys, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tlib import *
import ll, statsmodels.api as sm
P, DP = load_panels(); idx = P.index
D = DP.reindex(idx)
rows = []
def ols_t(y, X):
    d = pd.concat([y.rename("y"), X], axis=1).dropna()
    m = sm.OLS(d["y"], sm.add_constant(d.drop(columns="y"))).fit(cov_type="HC0")
    return m.params, m.tvalues, len(d)
for tgt in ["XU030", "XU100", "THYAO", "GARAN", "KCHOL", "SISE"]:
    y = D[(tgt, "intra")]; g = D[(tgt, "gap")]; c = P[tgt + ".IS"]
    own = {"gap_{t-1}": g.shift(1), "intra_{t-1}": y.shift(1), "cc_{t-1}": c.shift(1), "gap_t": g}
    for k, v in own.items():
        for w in ["full", "is", "oos"]:
            m = (idx >= WIN[w][0]) & (idx <= WIN[w][1]); rows.append({"target": tgt, "x": k, "win": w, "corr": y[m].corr(v[m])})
    for drv in ["^KS11", "^N225", "^TWII", "^AXJO", "EWY", "^GSPC", "ES=F", "EEM"]:
        x1 = P[drv].shift(1)
        for w in ["full", "is", "oos", "1y"]:
            m = (idx >= WIN[w][0]) & (idx <= WIN[w][1])
            r = {"target": tgt, "x": drv + "_{t-1}", "win": w, "corr": y[m].corr(x1[m])}
            # kontrollü: BIST'in kendi gap_{t-1}, intra_{t-1}, gap_t ve ABD lag1/lag2
            X = pd.DataFrame({"x": x1, "gap_l1": g.shift(1), "intra_l1": y.shift(1), "gap_t": g, "spx_l1": P["^GSPC"].shift(1), "spx_l2": P["^GSPC"].shift(2)})[m]
            b, t, n = ols_t(y[m], X); r.update({"t_raw": ols_t(y[m], X[["x"]])[1]["x"], "b_ctrl": b["x"], "t_ctrl": t["x"], "t_gap_l1": t["gap_l1"], "t_gap_t": t["gap_t"], "n": n})
            rows.append(r)
A = pd.DataFrame(rows); A.round(4).to_csv(CACHE + "/asia_check.csv", index=False)
print(A[(A.target.isin(["XU030", "THYAO"])) & (A.win == "full")][["target", "x", "corr", "t_raw", "t_ctrl", "t_gap_l1", "t_gap_t"]].round(3).to_string(index=False))
print(A[(A.target == "XU030") & A.x.isin(["^KS11_{t-1}", "gap_{t-1}", "^N225_{t-1}"])][["x", "win", "corr", "t_raw", "t_ctrl"]].round(3).to_string(index=False))
# yıllara göre
y = D[("XU030", "intra")]
yr = pd.DataFrame({"KS11_l1": y.groupby(idx.year).apply(lambda s: s.corr(P["^KS11"].shift(1).reindex(s.index))),
                   "N225_l1": y.groupby(idx.year).apply(lambda s: s.corr(P["^N225"].shift(1).reindex(s.index))),
                   "own_gap_l1": y.groupby(idx.year).apply(lambda s: s.corr(D[("XU030", "gap")].shift(1).reindex(s.index))),
                   "own_gap_t": y.groupby(idx.year).apply(lambda s: s.corr(D[("XU030", "gap")].reindex(s.index)))}).round(3)
yr.to_csv(CACHE + "/asia_check_years.csv"); print(yr.T.to_string())
BT = []
for drv in ["^KS11", "^N225", "^TWII"]:
    for tgt in ["XU030", "XU100"]:
        for cost in [4, 8, 15]:
            for mode, thr in [("sign", 0.0), ("z", 1.0)]:
                res, _ = ll.backtest(P[drv].shift(1), D[(tgt, "intra")], cost_bps=cost, mode=mode, thr=thr)
                BT.append({"driver": drv, "target": tgt, "cost": cost, "mode": f"{mode}{thr:g}", **{f"{s}_{k}": res[s].get(k) for s in ["IS", "OOS"] for k in ["sharpe", "mean_bps", "t", "n"]},
                           "by_year": str(res["by_year_bps"]) if (cost == 8 and mode == "sign") else ""})
for tgt in ["XU030"]:
    for cost in [4, 8, 15]:
        res, _ = ll.backtest(D[(tgt, "gap")].shift(1), D[(tgt, "intra")], cost_bps=cost)
        BT.append({"driver": "OWN_gap_l1", "target": tgt, "cost": cost, "mode": "sign0", **{f"{s}_{k}": res[s].get(k) for s in ["IS", "OOS"] for k in ["sharpe", "mean_bps", "t", "n"]}, "by_year": str(res["by_year_bps"]) if cost == 8 else ""})
B = pd.DataFrame(BT); B.round(3).to_csv(CACHE + "/asia_bt.csv", index=False)
print(B[B.target == "XU030"][["driver", "cost", "mode", "IS_sharpe", "IS_mean_bps", "IS_t", "OOS_sharpe", "OOS_mean_bps", "OOS_t", "OOS_n"]].round(2).to_string(index=False))
print(B[(B.target == "XU030") & (B.by_year != "")][["driver", "by_year"]].to_string(index=False))
