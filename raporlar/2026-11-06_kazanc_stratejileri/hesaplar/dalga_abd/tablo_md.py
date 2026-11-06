"""8) Rapor icin markdown tablolari uretir (stdout)."""
import os, numpy as np, pandas as pd
from dalga_tanim import OUT
res = pd.read_pickle(os.path.join(OUT, "kurallar_grid.pkl"))
A = res[res.fam == "A"].copy()
A = A[A.rule.str.endswith("none")]
A["kural"] = A.rule.str.replace("A_", "").str.replace("_none", "")
t = A[["kural", "tr_per_yr", "avg_mo", "win_rel", "avg_rel", "med_rel", "false_start", "hit", "capture_med", "lag_med", "cagr", "cagr00", "cagr15", "maxdd"]].copy()
for c in ["win_rel", "avg_rel", "med_rel", "false_start", "hit", "capture_med", "lag_med", "cagr", "cagr00", "cagr15", "maxdd"]:
    t[c] = (t[c] * 100).round(1)
t["tr_per_yr"] = t.tr_per_yr.round(1); t["avg_mo"] = t.avg_mo.round(1)
print(t.to_markdown(index=False))
print()
B = res[res.fam != "A"].copy()
keep = ["B_L1s0_k3_plain","B_L1s0_k10_plain","B_L3s0_k3_plain","B_L3s0_k5_plain","B_L6s0_k3_plain","B_L6s0_k5_plain","B_L6s1_k3_plain","B_L12s0_k1_plain","B_L12s0_k3_plain","B_L12s0_k5_plain","B_L12s1_k3_plain","B_L12s1_k5_plain","C_L12s0_k3_abs","C_L6s0_k5_abs","C_L12s0_k3_mkt","C_L6s0_k5_mkt","D_L12s0_k3_buf","D_L6s1_k10_buf","D_L12s0_k3_trail15","D_L6s0_k5_trail15"]
b = B.set_index("rule").loc[keep, ["turn_yr", "hit", "capture_med", "lag_med", "cagr", "cagr_stress", "sharpe", "maxdd", "cagr00", "maxdd00", "cagr15", "maxdd15"]].reset_index()
for c in ["hit", "capture_med", "lag_med", "cagr", "cagr_stress", "maxdd", "cagr00", "maxdd00", "cagr15", "maxdd15"]:
    b[c] = (b[c] * 100).round(1)
b["turn_yr"] = b.turn_yr.round(1); b["sharpe"] = b.sharpe.round(2)
print(b.to_markdown(index=False))
print()
S = pd.read_pickle(os.path.join(OUT, "swing_grid.pkl"))
S = S[S.rule.str.endswith("none")]
s = S[["rule", "tr_yr", "hold_d", "win_rel", "avg_rel", "med_rel", "win_2015-26", "rel_2015-26", "cagr31", "cagr00", "cagr15", "dd31", "dd15"]].copy()
for c in ["win_rel", "avg_rel", "med_rel", "win_2015-26", "rel_2015-26", "cagr31", "cagr00", "cagr15", "dd31", "dd15"]:
    s[c] = (s[c] * 100).round(1)
s["tr_yr"] = s.tr_yr.round(1)
print(s.to_markdown(index=False))
