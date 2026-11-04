"""Aday 4: VİOP USDTRY 5 günlük kümülatif değişim -> F_THYAO. Uzun-eğilim (carry) ve zamanlama kontrolleri."""
import numpy as np, pandas as pd, cl, ev, json
out = {}
u = ev.R("USDTRY")
P5 = sum(u.shift(i) for i in range(5))
z = cl.zscale(P5, 250, 100)
zz = z[z.index >= "2017-03-06"]
act = zz[zz.abs() > 1]
print("aktif gün oranı ve uzun payı (yıllara göre):")
print(pd.DataFrame({"active": (zz.abs() > 1).groupby(zz.index.year).mean().round(2), "long_share": (act > 0).groupby(act.index.year).mean().round(2)}).T.to_string())
res, G, tr = ev.evaluate("USD5->THYAO h3 raw", z, "THYAO", main=(3, 1.0, "raw"), nsim=300)
out["main_h3_raw"] = res; G.to_csv(cl.OUT + "/c4_grid.csv", index=False); tr.to_csv(cl.OUT + "/c4_trades.csv")
r2, _, _ = ev.evaluate("USD5->THYAO h3 hedged", z, "THYAO", main=(3, 1.0, "hedged"), nsim=200, placebo=True, verbose=False); out["h3_hedged"] = r2
print("hedged", json.dumps(r2, ensure_ascii=False, default=str))
rows = []
def quick(lab, zz, h=3, lg="raw", und="THYAO"):
    Y = ev.ydict(und, "2017-03-06"); t = cl.trades(zz, Y[(h, lg)], h, 1.0); s = cl.summ(t, 8 + (3 if lg == "hedged" else 0))
    rows.append(dict(var=lab, und=und, h=h, leg=lg, n=s["n"], long=round(s["long_frac"], 2), net8=round(s["net"], 1), t=round(s["t"], 2), IS=round(s["IS"], 1), OOS=round(s["OOS"], 1),
                     drop10_t=round(cl.drop_top(t, 8 + (3 if lg == "hedged" else 0), 10)[1], 2), p2426=cl.periods(t, 8)["2024-26"]))
# carry'den arındırılmış: 5g değişim - geçmiş 250g ortalama (demeaned) ; ve vadeli-spot ayrımı yerine lag1 (t-1 uzlaşmasına kadar)
zd = cl.zscale(P5, 250, 100, demean=True)
zl = cl.zscale(sum(u.shift(i) for i in range(1, 6)), 250, 100)
always_long = pd.Series(2.0, index=z.index)
for h in (2, 3):
    for lg in ("raw", "hedged"):
        quick("ana", z, h, lg); quick("demeaned (carry çıkarılmış)", zd, h, lg); quick("lag1 (t-1'e kadar)", zl, h, lg)
        quick("HEP UZUN (kıyas)", always_long, h, lg)
        quick("yalnız uzun sinyaller", z.where(z > 1), h, lg); quick("yalnız kısa sinyaller", z.where(z < -1), h, lg)
for s in ("XU030", "VESTL", "FROTO", "TOASO", "PGSUS", "AKBNK"):
    quick("ana", z, 3, "raw", s)
Q = pd.DataFrame(rows); pd.set_option("display.width", 250); print(Q.to_string()); Q.to_csv(cl.OUT + "/c4_robust.csv", index=False)
json.dump(out, open(cl.OUT + "/c4_usd.json", "w"), ensure_ascii=False, default=str, indent=1)
