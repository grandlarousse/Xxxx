"""Hakem çoklu test: ajan içi (542 / 220 birincil) ve global (bütün ajan kayıtları) Bonferroni + BH."""
import sys, glob, numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
sys.path.insert(0, f"{S}/code"); from lib_altin import bh_fdr
r = pd.read_csv(f"{S}/out/registry/a6_akis_konum_cin.csv")
prim = r[~r.family.str.contains("robust|early|sameday|rule")].copy()
G = pd.concat([pd.read_csv(f) for f in glob.glob(f"{S}/out/registry/*.csv")], ignore_index=True)
G = G[G.p.notna()]
print("ajan kayıt:", len(r), "birincil:", len(prim), "global (p var):", len(G))
targets = [("asia_cn_gold_res_comp", 5), ("asia_res600547_SS", 5), ("asia_r_HSI", 3), ("vp_oi_d5_x_sgnret5", 5), ("gpr_z250", 5), ("cn_comp_sum5_sign", 1), ("cn_cn_comp_sum5", 1)]
for nm, sub in [("ajan birincil", prim), ("ajan tümü", r), ("global", G)]:
    sub = sub.copy(); sub["q"] = bh_fdr(sub.p.fillna(1)); sub["bonf"] = np.minimum(sub.p * len(sub), 1)
    print(f"\n[{nm}] n={len(sub)} | Bonferroni %5 eşik p<{0.05/len(sub):.2e} (|t|>~{abs(__import__('scipy').stats.norm.ppf(0.025/len(sub))):.2f}) | BH q<0.10 sayısı={int((sub.q<0.10).sum())}")
    for tid, h in targets:
        z = sub[(sub.test_id == tid) & (sub.h == h)]
        for _, row in z.iterrows():
            print(f"  {tid} h={h}: t={row.t:+.2f} p={row.p:.4f} BH q={row.q:.3f} Bonf={row.bonf:.2f}")
    # OOS t'sinin p'si (seçim tam örneklemle yapıldığı için iyimser)
from scipy import stats
for nm, t in [("comp OOS", 3.40), ("600547 OOS", 3.08), ("sum5 OOS", 3.64)]:
    p = 2 * (1 - stats.norm.cdf(t)); print(f"{nm}: p={p:.5f} -> 220 birincil Bonf={min(p*220,1):.3f}, 542 Bonf={min(p*542,1):.3f}")
