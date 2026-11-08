"""Görev 1-2: işlenebilirlik eleği + genel_tum.csv aile içi tutarlılık analizi.
Çalıştır: python3 -I kod/ajan_uluslararasi/a1_islenebilirlik_genel.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import ortak, lib

scr = ortak.screen()
# ---- 1) işlenebilirlik ----
rows = []
for s in ortak.FAM:
    r = scr.loc[s]
    rows.append({"sym": s, "grup": ortak.SYM2GRP[s], "bolge": ortak.REGION.get(s, ""), "lev": r["lev"],
                 "med_dv_m": r["med_dollar_vol_m"], "spread_bp": r["spread_bp"], "cost_rt_bp": r["cost_rt_bp"],
                 "vol_1d_bp": r["vol_1d_bp"], "cost_over_vol": r["cost_over_1d_vol"], "gap_share": r["gap_share"],
                 "worst_1d_1y": r["worst_1d_1y"], "ret_1y": r["ret_1y"], "tv": ortak.tv(s),
                 "cost_1000_bp": 30 + r["spread_bp"], "cost_10000_bp": 3 + r["spread_bp"]})
T = pd.DataFrame(rows)
T["elek"] = np.where(T["med_dv_m"] >= 20, "likit(>=20mn)", np.where(T["med_dv_m"] >= 10, "sinirda(10-20mn)", "ince(<10mn)"))
T = T.sort_values("med_dv_m", ascending=False)
T.to_csv(os.path.join(ortak.OUT, "islenebilirlik.csv"), index=False)
print(T["elek"].value_counts().to_string())

# ---- 2) genel_tum aile içi ----
g = pd.read_csv(os.path.join(ortak.ROOT, "sonuclar", "genel_tum.csv"))
g = g[g["sym"].isin(ortak.FAM)].copy()
print("aile satırı (test sayısı genel_tum):", len(g))
g["fdr_aile"] = lib.bh_fdr(g["p"].values, 0.10) & (g["mean_net_bp"] > 0)
print("aile içi BH-FDR q=0.10 (net>0) geçen:", int(g["fdr_aile"].sum()))
print(g[g["fdr_aile"]][["sym","sig","mode","h","exit","n","mean_net_bp","t","is_net_bp","oos_net_bp","years_pos_frac"]].to_string())

ind = ortak.independent(10)
gi = g[g["sym"].isin(ind)]
def agg(x):
    k = len(x)
    return pd.Series({"k": k, "pos_net": (x["mean_net_bp"] > 0).mean(), "pos_gross_edge": (x["edge_bp"] > 0).mean(),
                      "mean_net_bp": x["mean_net_bp"].mean(), "mean_gross_bp": x["mean_gross_bp"].mean(),
                      "med_t": x["t"].median(), "t_ge2": (x["t"] >= 2).mean(),
                      "is_oos_pos": ((x["is_net_bp"] > 0) & (x["oos_net_bp"] > 0)).mean(),
                      "stouffer": x["t"].sum() / np.sqrt(k), "mean_n": x["n"].mean()})
A = gi.groupby(["sig", "mode", "h", "exit"]).apply(agg).reset_index()
A = A.sort_values("stouffer", ascending=False)
A.to_csv(os.path.join(ortak.OUT, "genel_aile_tutarlilik.csv"), index=False)
pd.set_option("display.width", 250)
print("\n--- bağımsız likit (>=10mn) 1x temsilciler:", len(ind), ind)
print(A.head(30).to_string())
print(A[(A["pos_net"] >= 0.7)].to_string())
