"""ll v4 temizlik değişikliği öncesi (results_pre_v4) ve sonrası (results) karşılaştırma."""
import pandas as pd, numpy as np
A, B = "results_pre_v4", "results"
def rd(f, d): return pd.read_csv(f"{d}/{f}")
a = rd("sync_best.csv", A).set_index("stock"); b = rd("sync_best.csv", B).set_index("stock")
for c in ["r2_xu100_3y", "r2_own_3y", "r2_own_ex_3y", "beta_xu100", "corr_xu100", "corr_xyuzo"]:
    d = (b[c] - a[c]).abs(); print(f"sync_best {c}: maks |fark| {d.max():.4f} ({d.idxmax()}), medyan {d.median():.4f}")
print("best_ex_3y değişen:", list(b.index[a.best_ex_3y != b.best_ex_3y]))
for f, key in [("lead_idx_to_stock.csv", ["stock", "idx", "var", "target"]), ("lead_stock_to_idx.csv", ["stock", "idx"]), ("lead_idx_to_idx.csv", ["leader", "follower"])]:
    x = rd(f, A).set_index(key); y = rd(f, B).set_index(key); j = x[["t_full"]].join(y[["t_full"]], rsuffix="_v4").dropna()
    d = (j.t_full_v4 - j.t_full).abs()
    print(f"{f}: n={len(j)}, |t| farkı medyan {d.median():.3f}, maks {d.max():.2f} {d.idxmax()}, |t|>3 sayısı {int((j.t_full.abs()>3).sum())} -> {int((j.t_full_v4.abs()>3).sum())}")
for f in ["A_cc_fdr.csv", "A_gap_fdr.csv", "A_intra_fdr.csv", "B_fdr.csv", "C_fdr.csv"]:
    print(f, "FDR geçen:", int(rd(f, A).fdr.sum()), "->", int(rd(f, B).fdr.sum()))
x = rd("lomac_tests.csv", A); y = rd("lomac_tests.csv", B); j = x.merge(y, on=["test", "target", "per"], suffixes=("", "_v4"))
j = j[j.per.isin(["full", "IS", "OOS"])]; j["d"] = (j.b_v4 - j.b).abs(); print("lomac maks |b| farkı", round(j.d.max(), 3), j.loc[j.d.idxmax(), ["test", "target", "per", "b", "b_v4"]].to_dict())
x = rd("backtests.csv", A); y = rd("backtests.csv", B); j = x.merge(y, on=["bt", "stock", "cost"], suffixes=("", "_v4")); j["d"] = (j.OOS_mean_bps_v4 - j.OOS_mean_bps).abs()
print("backtest OOS bps maks fark", round(j.d.max(), 2), j.loc[j.d.idxmax(), ["bt", "stock", "cost", "OOS_mean_bps", "OOS_mean_bps_v4"]].to_dict(), " medyan", round(j.d.median(), 2))
k = j[j.stock.isin(["XU030", "47 hisse L/S", "illikit16", "likit16"]) & (j.cost == 8)][["bt", "stock", "OOS_mean_bps", "OOS_mean_bps_v4", "OOS_t", "OOS_t_v4"]]; print(k.round(2).to_string())
x = rd("regimes.csv", A).set_index("regime"); y = rd("regimes.csv", B).set_index("regime")
for c in ["cum_Q1illik_%", "cum_Q5likit_%", "avg_pair_corr_VIOP", "lead_XU030->Q1_cc_b"]:
    print(c, (y[c] - x[c]).abs().max().round(3))
for f in ["thyao_robust.csv", "bt_thyao_lead.csv"]:
    x = rd(f, A); y = rd(f, B); print(f); print(pd.concat([x.iloc[:, :4], y.iloc[:, 1:4].add_suffix("_v4")], axis=1).head(8).round(3).to_string())
