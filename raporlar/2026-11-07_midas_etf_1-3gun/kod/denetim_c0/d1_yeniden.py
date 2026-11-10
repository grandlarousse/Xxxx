"""Görev 1: c0_leadlag.csv'den rastgele 15 satır + t'ye göre en iyi 10 satırı bağımsız simülasyonla yeniden üret."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from ortak import *

r = pd.read_csv(os.path.join(ROOT, "sonuclar", "c0_leadlag.csv"))
rng = np.random.default_rng(20261110)
samp = r.iloc[rng.choice(len(r), 15, replace=False)]
top = r.sort_values("t", ascending=False).head(10)
rows = pd.concat([samp.assign(set="rastgele"), top.assign(set="en_iyi_t")])
spy = px("SPY").index
X = leaders(spy)
print("öncü sayısı", X.shape[1])
out = []
for _, q in rows.iterrows():
    T, L, k, h = q.target, q.leader, q.kind, int(q.h)
    df = px(T); c = df["c"].values.astype(float); cost = my_cost(df)
    if k in ("OWN_DN", "OWN_UP"):
        rT = np.log(df["c"]).diff(); z = zsc(rT)
        sig = ((z <= -2) if k == "OWN_DN" else (z >= 2)).values.copy(); sig[:80] = False
    else:
        sg, _, _ = signals_for(T, X, kinds=(k,), leaders_list=[L]); sig = sg[(L, k)]
    ent, g = sim_greedy(sig, c, h)
    net = g - cost / 1e4
    out.append({"set": q.set, "target": T, "leader": L, "kind": k, "h": h, "n_csv": int(q.n), "n_ben": len(net),
                "net_csv": round(q.net_bp, 2), "net_ben": round(net.mean() * 1e4, 2), "t_csv": round(q.t, 3), "t_ben": round(tstat(net), 3),
                "cost_csv": round(q.cost_bp, 3), "cost_ben": round(cost, 3), "brut_eksi_net_csv": round(q.gross_bp - q.net_bp, 3)})
o = pd.DataFrame(out)
o["fark_net"] = (o.net_ben - o.net_csv).round(3); o["fark_t"] = (o.t_ben - o.t_csv).round(3)
pd.set_option("display.width", 250)
print(o.to_string(index=False))
o.to_csv(os.path.join(HERE, "d1_yeniden.csv"), index=False)
print("tam eşleşen (n eşit, |dnet|<0.01, |dt|<0.001):", int(((o.n_csv == o.n_ben) & (o.fark_net.abs() < 0.01) & (o.fark_t.abs() < 0.001)).sum()), "/", len(o))
# maliyet bir kez mi düşülmüş: brüt - net == maliyet tüm CSV'de
d = (r.gross_bp - r.net_bp - r.cost_bp).abs().max()
print("CSV: max |brüt-net-maliyet| =", d)
