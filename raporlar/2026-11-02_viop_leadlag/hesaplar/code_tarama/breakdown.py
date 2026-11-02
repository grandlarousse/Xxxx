"""Aile x kapanış kovası kırılımı (FDR q=0.05 tam dönem, 47 VİOP) -> cache/fdr_by_bucket.csv"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tlib import *
M = pd.read_parquet(OUT + '/tarama_matrix.parquet'); V = M[~M.is_index_row]
rows = []
for f in ["sync", "pc_xt", "gap_l1", "intra_l1", "intra_l0", "cum25", "rev"]:
    for b, g in V.groupby("bucket"):
        p = g[f"p_{f}_full"].values; ok = ~np.isnan(p)
        r, _ = bh(p, 0.05)  # kova içi FDR
        rows.append({"fam": f, "bucket": b, "n": int(ok.sum()), "p05_frac": round(float((p[ok] < .05).mean()), 3),
                     "bh05_global": int((g[f"q_{f}_full"] < .05).sum()), "bh05_within_bucket": int(r.sum()),
                     "med_abs_corr": round(float(g[f"{f}_full"].abs().median()), 3), "mean_corr": round(float(g[f"{f}_full"].mean()), 3)})
B = pd.DataFrame(rows); B.to_csv(CACHE + '/fdr_by_bucket.csv', index=False); print(B.to_string(index=False))
