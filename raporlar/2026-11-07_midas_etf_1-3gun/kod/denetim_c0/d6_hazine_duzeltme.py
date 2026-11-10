"""Görev 2 ek: Hazine (ve OVX/GVZ) z-skorlarındaki tatil-NaN kaybı düzeltilirse medyan-t sıralaması değişir mi?
Düzeltme: L_UP/L_DN için z, serinin KENDİ takviminde (NaN'ler atılarak) hesaplanır, sonra hedef takvimine taşınır.
GERIDE/ONDE için rolling pencereler NaN'siz alt-örneklemde (öncü ve hedefin ikisinin de geçerli olduğu günler) hesaplanır."""
import os, sys, warnings
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from ortak import *
warnings.filterwarnings("ignore")
spy = px("SPY").index
X = leaders(spy)
Ls = ["DGS10_d", "DGS2_d", "DGS30_d", "DFII10_d", "T10YIE_d", "OVX_dlog", "GVZ_dlog"]
res = []
for T in targets():
    df = px(T); c = df["c"].values.astype(float); cost = my_cost(df) / 1e4
    rT = np.log(df["c"]).diff()
    for L in Ls:
        if L == T: continue
        x = X[L].reindex(df.index)
        if x.notna().sum() < 400: continue
        xv = x.dropna(); zL = (xv / xv.rolling(60).std().shift(1)).reindex(df.index)
        D = pd.DataFrame({"t": rT, "l": x}).dropna()
        beta = (D.t.rolling(60).cov(D.l) / D.l.rolling(60).var()).shift(1)
        e = D.t - beta * D.l; zr = (e / e.rolling(60).std().shift(1)).reindex(df.index)
        for k, s in (("L_UP", zL >= 2), ("L_DN", zL <= -2), ("GERIDE", zr <= -2), ("ONDE", zr >= 2)):
            sig = s.fillna(False).values.copy(); sig[:80] = False
            if sig.sum() < 30: continue
            for h in (1, 2, 3):
                ent, g = sim_greedy(sig, c, h)
                if len(ent) < 30: continue
                res.append((T, L, k, h, len(ent), tstat(g - cost)))
r = pd.DataFrame(res, columns=["target", "leader", "kind", "h", "n", "t"])
g = r.groupby(["leader", "kind", "h"]).agg(med_t=("t", "median"), n_tg=("t", "size"), pos=("t", lambda v: (v > 0).mean())).reset_index()
orig = pd.read_csv(os.path.join(ROOT, "sonuclar", "c0_leadlag.csv"))
go = orig[orig.leader.isin(Ls)].groupby(["leader", "kind", "h"]).agg(med_t_tarama=("t", "median"), n_tg_tarama=("t", "size")).reset_index()
m = g.merge(go, on=["leader", "kind", "h"], how="outer").sort_values("med_t", ascending=False)
print(m.round(3).head(15).to_string(index=False))
print("düzeltilmiş en yüksek medyan t:", round(m.med_t.max(), 3), "(TLT L_UP h3 = 1,379)")
m.to_csv(os.path.join(HERE, "d6_hazine_duzeltme.csv"), index=False)
