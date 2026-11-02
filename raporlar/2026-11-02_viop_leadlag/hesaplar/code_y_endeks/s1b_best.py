"""GÖREV 1b: en iyi açıklayan endeks (son 3 yıl ortak örneklem; ham ve hisse-hariç)."""
from ye_common import *
S = pd.read_csv(RES + "/sync.csv")
best = []
for s, g in S.groupby("stock"):
    g = g.copy(); g["r2_3y"] = g["corr_3y"] ** 2; g["r2ex_3y"] = g["corr_ex_3y"].fillna(g["corr_3y"]) ** 2
    g3 = g[g["start"].astype(str) <= "2023-06-01"]
    b_raw = g3.sort_values("r2_3y", ascending=False).iloc[0]; b_ex = g3.sort_values("r2ex_3y", ascending=False).iloc[0]
    nat = g3[g3.idx.isin(NATIONAL)]; b_nat = nat.sort_values("r2ex_3y", ascending=False).iloc[0]
    sec = [x for x in SECT[s] if x in set(g.idx)]
    gs = g[g.idx.isin(sec)].sort_values("r2_3y", ascending=False)
    b2f = g3[g3.idx != "XU100"].sort_values("r2_2f", ascending=False).iloc[0]
    r100 = g[g.idx == "XU100"].iloc[0]; ryz = g[g.idx == "XYUZO"]
    best.append({"stock": s, "best_raw_3y": b_raw.idx, "r2_raw_3y": b_raw.r2_3y, "best_ex_3y": b_ex.idx, "r2_ex_3y": b_ex.r2ex_3y,
                 "best_national_ex": b_nat.idx, "r2_nat_ex": b_nat.r2ex_3y,
                 "r2_xu100_3y": r100.r2_3y, "r2_xu100ex_3y": r100.r2ex_3y, "corr_xu100": r100.corr_full, "beta_xu100": r100.beta, "w_xu100": r100.w_last,
                 "own_sector": gs.iloc[0].idx if len(gs) else None, "r2_own_3y": gs.iloc[0].r2_3y if len(gs) else np.nan,
                 "r2_own_ex_3y": gs.iloc[0].r2ex_3y if len(gs) else np.nan, "w_own": gs.iloc[0].w_last if len(gs) else np.nan,
                 "pc_own": gs.iloc[0].pcorr_xu100 if len(gs) else np.nan,
                 "best_2f_idx": b2f.idx, "r2_2f": b2f.r2_2f, "dR2_2f": b2f.r2_2f - r100.r2, "pc_best2f": b2f.pcorr_xu100,
                 "r2_xyuzo_3y": ryz.r2_3y.iloc[0] if len(ryz) else np.nan, "corr_xyuzo": ryz.corr_full.iloc[0] if len(ryz) else np.nan})
Bst = pd.DataFrame(best); Bst.to_csv(RES + "/sync_best.csv", index=False)
pd.set_option("display.width", 250); print(Bst.round(3).to_string())
