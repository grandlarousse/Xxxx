"""Görev 4: taramanın kapsamadığı, literatürde bilinen seviye tabanlı VIX öncüleri (C0, yalnız long, maliyetli).
 (i)  VIX/VIX3M >= 1 (vade yapısı ters dönmüş; tarama yalnız ORANIN GÜNLÜK DEĞİŞİMİNİ kullandı)
 (ii) Connors 'VIX stretch': VIX >= 1,10 x SMA10(VIX)  (seviyenin kısa ortalamaya göre gerilmesi)
 (iii) 5 günlük öncü getirisi: SPY 5g z <= -2 (tarama yalnız 1 günlük z kullandı)
Not: VIX 16:15 ET kapanır -> C0'da hafif ileriye bakış."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from ortak import *
pd.set_option("display.width", 250)
spy = px("SPY").index
vix = pd.read_parquet(os.path.join(DATA, "vol", "VIX.parquet"))["close"].reindex(spy)
v3 = pd.read_parquet(os.path.join(DATA, "vol", "VIX3M.parquet"))["close"].reindex(spy)
spyc = px("SPY")["c"]
z5 = np.log(spyc).diff(5) / (np.log(spyc).diff().rolling(60).std().shift(1) * np.sqrt(5))
sigs = {"VIX/VIX3M>=1": vix / v3 >= 1.0, "VIX>=1.10*SMA10": vix >= 1.10 * vix.rolling(10).mean(),
        "SPY 5g z<=-2": z5 <= -2}
IS_END = pd.Timestamp("2021-12-31")
rows = []
for nm, s in sigs.items():
    for T in ("SPY", "QQQ"):
        df = px(T); c = df["c"].values; sig = s.reindex(df.index).fillna(False).values.copy(); sig[:80] = False
        cost = my_cost(df) / 1e4
        for h in (1, 2, 3):
            ent, g = sim_greedy(sig, c, h); net = g - cost; d = df.index[ent]
            u = (c[h:] / c[:-h] - 1)[80:].mean()
            i, o = net[d <= IS_END], net[d > IS_END]
            rows.append({"sinyal": nm, "hedef": T, "h": h, "n": len(net), "net_bp": net.mean() * 1e4, "t": tstat(net),
                         "kenar_bp(brüt-koşulsuz)": (g.mean() - u) * 1e4, "IS_t": tstat(i), "OOS_t": tstat(o),
                         "t_en_iyi5_haric": tstat(np.sort(net)[:-5]), "2020_haric_t": tstat(net[d.year != 2020])})
o = pd.DataFrame(rows); print(o.round(2).to_string(index=False)); o.to_csv(os.path.join(HERE, "d5_kacirilan.csv"), index=False)
