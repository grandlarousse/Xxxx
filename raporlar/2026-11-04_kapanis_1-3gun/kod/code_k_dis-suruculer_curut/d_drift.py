"""Rejim-drift kontrolü: işlem getirisinden aynı takvim yılının (ya da geçmiş 250 günün) koşulsuz t->t+h ortalaması (x yön) çıkarılır.
Sinyalin yönü uzun süre tek tarafa kayıyorsa (USDTRY carry, altın rallisi) kazancın ne kadarı 'trend'den geliyor?"""
import numpy as np, pandas as pd, cl, ev, json
import importlib
def drift_adj(z, und, h, lg, thr=1.0, start="2017-03-06"):
    Y = ev.ydict(und, start); y = Y[(h, lg)]
    tr = cl.trades(z, y, h, thr)
    extra = 3 if lg == "hedged" else 0
    ym = y.groupby(y.index.year).transform("mean")
    ytr = y.rolling(250, min_periods=100).mean().shift(h)  # yalnız geçmişte gerçekleşmiş getiriler
    g = tr["gross"] * 1e4; d = tr["dir"]
    adj_year = g - d * ym.reindex(tr.index) * 1e4; adj_trail = g - d * ytr.reindex(tr.index) * 1e4
    o = dict(und=und, h=h, leg=lg, n=len(tr), net8=round((g - 8 - extra).mean(), 1), t=round(cl.tstat(g - 8 - extra), 2),
             net8_yeardrift_adj=round((adj_year - 8 - extra).mean(), 1), t_year=round(cl.tstat(adj_year - 8 - extra), 2),
             net8_trail_adj=round((adj_trail - 8 - extra).mean(), 1), t_trail=round(cl.tstat(adj_trail - 8 - extra), 2))
    a = adj_year - 8 - extra
    o["year_adj_2024_26"] = round(a[a.index >= "2024-01-01"].mean(), 1); o["t_2024_26"] = round(cl.tstat(a[a.index >= "2024-01-01"]), 2)
    o["year_adj_IS"] = round(a[a.index < "2022-01-01"].mean(), 1); o["year_adj_OOS"] = round(a[a.index >= "2022-01-01"].mean(), 1)
    return o
rows = []
# 1 rafineri
import c1sig
z1 = c1sig.z_ref(); rows += [dict(cand="REF->TUPRS", **drift_adj(z1, "TUPRS", h, lg)) for h, lg in ((2, "raw"), (3, "raw"), (2, "hedged"))]
z2 = c1sig.z_asx(); rows += [dict(cand="ASX->EREGL", **drift_adj(z2, "EREGL", h, lg)) for h, lg in ((3, "hedged"), (2, "hedged"), (3, "raw"))]
g = ev.R("XAUUSD"); z3 = cl.zscale(g, 250, 100)
rows += [dict(cand="GOLD->TRALT", **drift_adj(z3, "TRALT", h, lg, start="2018-12-17")) for h, lg in ((2, "hedged"), (1, "hedged"), (2, "raw"))]
rows += [dict(cand="GOLD->TRMET", **drift_adj(z3, "TRMET", 2, "hedged", start="2018-12-17"))]
u = ev.R("USDTRY"); z4 = cl.zscale(sum(u.shift(i) for i in range(5)), 250, 100); z4d = cl.zscale(sum(u.shift(i) for i in range(5)), 250, 100, demean=True)
rows += [dict(cand="USD5->THYAO", **drift_adj(z4, "THYAO", h, lg)) for h, lg in ((3, "raw"), (3, "hedged"), (2, "raw"))]
rows += [dict(cand="USD5(demeaned)->THYAO", **drift_adj(z4d, "THYAO", h, lg)) for h, lg in ((3, "raw"), (3, "hedged"))]
D = pd.DataFrame(rows); pd.set_option("display.width", 250); print(D.to_string()); D.to_csv(cl.OUT + "/d_drift.csv", index=False)
