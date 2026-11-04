import numpy as np, pandas as pd, cl, ev, json, hsnap
rows = []
def quick(lab, zz, h=3, lg="raw", und="THYAO", start="2017-03-06"):
    Y = ev.ydict(und, start); t = cl.trades(zz, Y[(h, lg)], h, 1.0); s = cl.summ(t, 8 + (3 if lg == "hedged" else 0))
    rows.append(dict(var=lab, h=h, leg=lg, start=start, n=s["n"], long=round(s["long_frac"], 2), net8=round(s["net"], 1), t=round(s["t"], 2), IS=round(s["IS"], 1), OOS=round(s["OOS"], 1)))
u = ev.R("USDTRY")
ty = cl.to_bist(cl.lret("TRY=X", "c"), "after")          # Yahoo kapanışı ldate < t (güvenli)
ty_same = cl.to_bist(cl.lret("TRY=X", "c"), "before")    # ldate <= t (kısmen geleceği içerebilir)
th = hsnap.r_snap("TRY=X", 15, 0)                        # 15:00 UTC anlık
for nm, x in (("VİOP fut 5g", u), ("Yahoo TRY=X 5g (t-1'e kadar)", ty), ("Yahoo TRY=X 5g (ldate<=t)", ty_same), ("saatlik TRY=X 15:00 5g", th)):
    P5 = sum(x.shift(i) for i in range(5))
    for dm in (False, True):
        z = cl.zscale(P5, 250 if "saat" not in nm else 120, 100 if "saat" not in nm else 60, demean=dm)
        for st in ("2017-03-06", "2023-12-15"):
            quick(nm + (" demeaned" if dm else ""), z, 3, "raw", start=st)
# vadeli - spot ayrışması (carry/baz bileşeni) tek başına
basis = u - ty
P5b = sum(basis.shift(i) for i in range(5)); quick("VİOP - Yahoo (baz) 5g", cl.zscale(P5b, 250, 100), 3, "raw")
Q = pd.DataFrame(rows); pd.set_option("display.width", 250); print(Q.to_string())
# spot THYAO 2014+ Yahoo TRY=X t-1
c = ev.scal(); tys = cl.to_bist(cl.lret("TRY=X", "c"), "after", c); P5s = sum(tys.shift(i) for i in range(5))
for dm in (False, True):
    ev.evaluate_spot("TRY=X 5g (t-1) -> THYAO spot" + (" demeaned" if dm else ""), cl.zscale(P5s, 250, 100, demean=dm), "THYAO.IS", main=(3, 1.0, "raw"))
