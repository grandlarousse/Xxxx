"""USDTRY k-günlük kümülatif -> THYAO/ihracatçılar: (i) saatlik 15:00 (H), (ii) spot 2014+ ile Yahoo TRY=X t-1 (gecikmeli, geçerli) ve h15."""
import numpy as np, pandas as pd, klib as K, ll
Sp = K.spot_panel(); F = K.fut_panel()
EXP = ["THYAO", "FROTO", "TOASO", "VESTL", "ARCLK", "EREGL", "SISE", "AEFES", "PGSUS", "TAVHL"]
d = pd.read_csv(K.RES + "/b_multiday_H.csv")
print(d[(d.driver == "USD") & (d.form == "raw") & d.stock.isin(["THYAO", "VESTL", "FROTO", "PGSUS", "XU030"])].pivot_table(index=["stock", "k"], columns="h", values="t").round(2))
usdL = ll.ret("TRY=X")  # FX_FIX: UTC günü t sonu -> BIST kapanışından sonra -> shift(1)
R = Sp; mk = Sp["XU100"]; betaS = K.roll_beta(R[K.STOCKS], mk, 250, 60)
rows = []
for k in (3, 5):
    z = K.sdscale(K.cum(usdL.reindex(R.index), k, 1), 250, 60)
    for s in ["THYAO", "VESTL", "FROTO", "PGSUS", "XU030", "BASKET"]:
        for h in (2, 3):
            if s == "BASKET": y = pd.concat([K.fwd(R[x], h) for x in EXP], axis=1).mean(axis=1)
            else: y = K.fwd(R[s], h)
            y = y[y.index >= "2014-01-01"]
            r = K.reg(y, z, h + 1); out = dict(k=k, stock=s, h=h, t=r["t"], b=r["b"] * 1e4)
            for a, b in (("2014", "2016-12-31"), ("2017", "2020-12-31"), ("2021", "2026-12-31")):
                yy = y[(y.index >= a) & (y.index <= b)]; out["t_" + a] = K.reg(yy, z, h + 1)["t"]
            tr = K.trades_nonoverlap(z, y, h, 1.0); st = K.trade_stats(tr, 8, "2021-01-01"); out.update(net8=st["net"], t8=st["t_net"], IS=st["IS_net"], OOS=st["OOS_net"], yrs=st["yrs_pos"])
            rows.append(out)
pd.set_option("display.width", 250); print(pd.DataFrame(rows).round(2).to_string())
