import numpy as np, pandas as pd, cl, ev, json
g = ev.R("XAUUSD"); z = cl.zscale(g, 250, 100)
rows = []
def quick(lab, zz, h=2, lg="hedged", und="TRALT", start="2018-12-17"):
    Y = ev.ydict(und, start); t = cl.trades(zz, Y[(h, lg)], h, 1.0); s = cl.summ(t, 8 + (3 if lg == "hedged" else 0))
    rows.append(dict(var=lab, und=und, h=h, leg=lg, n=s["n"], net8=round(s["net"], 1), t=round(s["t"], 2), IS=round(s["IS"], 1), OOS=round(s["OOS"], 1), drop10=round(cl.drop_top(t, 8 + (3 if lg == "hedged" else 0), 10)[1], 2)))
for h in (1, 2, 3):
    quick("ana (settle)", z, h)
    quick("lag1 (dünkü altın)", z.shift(1), h); quick("demeaned", cl.zscale(g, 250, 100, demean=True), h)
    quick("COMEX GC=F t-1 (günlük)", cl.zscale(cl.to_bist(cl.lret("GC=F", "c"), "after"), 250, 100), h)
    quick("ana, XU030 yerine 250g beta yok (raw)", z, h, lg="raw")
Q = pd.DataFrame(rows); print(Q.to_string()); Q.to_csv(cl.OUT + "/c3_robust.csv", index=False)
L = ev.legs("TRALT")
for h in (1, 2):
    y = cl.fwd(L["hedged"], h); y = y[y.index >= "2018-12-17"]
    X = pd.concat([z.rename("z"), cl.zscale(L["hedged"], 250, 100).rename("own_resid")], axis=1)
    o = cl.nw_reg(y * 1e4, X, h + 1); print("reg h", h, o[1]); print(o[0].round(3))
    for a, b in (("2019", "2020"), ("2021", "2022"), ("2023", "2024"), ("2025", "2026")):
        yy = y[(y.index >= a) & (y.index < str(int(b) + 1))]
        o = cl.nw_reg(yy * 1e4, X, h + 1)
        if o: print("  ", a, b, "z b", round(o[0].loc["z", "b"], 1), "t", round(o[0].loc["z", "t"], 2), "n", o[1])
print(cl.liq("TRALT").to_string()); print(cl.liq("TRMET").to_string())
