"""(h) Bu ajanın kayıt defteri üzerinde yerel BH-FDR (birincil testler, h=1/3/5 alt kümesi) ve özet."""
import sys
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
sys.path.insert(0, f"{S}/code")
import pandas as pd, numpy as np
from lib_altin import bh_fdr
r = pd.read_csv(f"{S}/out/registry/a6_akis_konum_cin.csv")
print("toplam kayıt:", len(r)); print(r.family.value_counts().to_string())
prim = r[~r.family.str.contains("robust|early|sameday|rule")].copy()
prim["q"] = bh_fdr(prim.p.fillna(1))
p135 = prim[prim.h.isin([1, 3, 5])].copy(); p135["q135"] = bh_fdr(p135.p.fillna(1))
print("birincil test:", len(prim), "| h∈{1,3,5}:", len(p135))
print(prim.sort_values("p").head(15)[["family", "test_id", "h", "ic", "t", "t_is", "t_oos", "yrs_same_sign", "yrs", "p", "q"]].round(4).to_string(index=False))
print(p135.sort_values("p").head(8)[["test_id", "h", "t", "p", "q135"]].round(4).to_string(index=False))
print("birincil |t|>=2:", int((prim.t.abs() >= 2).sum()), "| %5 düzeyde şans beklentisi ≈", round(0.0455 * len(prim), 1))
r["q_all"] = bh_fdr(r.p.fillna(1))
r.sort_values("p").to_csv(f"{S}/out/a6_akis_konum_cin/registry_with_q.csv", index=False)
prim.sort_values("p").to_csv(f"{S}/out/a6_akis_konum_cin/registry_primary_q.csv", index=False)
