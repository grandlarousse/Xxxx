"""Aday 5: Avrupa savunma 15:00 UTC artığı -> F_ASELS (saatlik, 2023-12+). Günlük t-1 vekili ile uzun dönem."""
import numpy as np, pandas as pd, cl, ev, json, hsnap
MEM = ["RHM.DE", "BA.L", "LDO.MI", "SAAB-B.ST"]
c = cl.cal()
rm = hsnap.r_snap("^STOXX", 15, 0)
res_ = []
for m in MEM:
    r = hsnap.r_snap(m, 15, 0); b = cl.roll_beta(r, rm, 120, 40); res_.append((r - b * rm).rename(m))
D = pd.concat(res_, axis=1); P = D.mean(axis=1).where(D.notna().sum(axis=1) >= 3)
z = cl.zscale(P, 120, 40)
st = z.first_valid_index(); print("başlangıç", st)
out = {}
res, G, tr = ev.evaluate("DEF_EU(15:00)->ASELS h2 raw", z, "ASELS", main=(2, 1.0, "raw"), start=str(st.date()), split="2025-05-01", nsim=300)
out["h2_raw"] = res; G.to_csv(cl.OUT + "/c5_grid.csv", index=False); tr.to_csv(cl.OUT + "/c5_trades.csv")
r2, _, _ = ev.evaluate("DEF_EU(15:00)->ASELS h3 raw", z, "ASELS", main=(3, 1.0, "raw"), start=str(st.date()), split="2025-05-01", nsim=0, placebo=False, verbose=False)
print("h3", json.dumps(r2, ensure_ascii=False, default=str)); out["h3_raw"] = r2
r3, _, _ = ev.evaluate("DEF_EU(15:00)->ASELS h2 hedged", z, "ASELS", main=(2, 1.0, "hedged"), start=str(st.date()), split="2025-05-01", nsim=0, placebo=False, verbose=False)
print("h2 hedged", json.dumps(r3, ensure_ascii=False, default=str)); out["h2_hedged"] = r3
# zamanlama: 14:00 UTC snap (1 saat erken) ve LOO
rows = []
def quick(lab, zz, h=2, lg="raw"):
    Y = ev.ydict("ASELS", str(st.date())); t = cl.trades(zz, Y[(h, lg)], h, 1.0); s = cl.summ(t, 8 + (3 if lg == "hedged" else 0), split="2025-05-01")
    rows.append(dict(var=lab, h=h, leg=lg, n=s["n"], long=round(s["long_frac"], 2), net8=round(s["net"], 1), t=round(s["t"], 2), H1=round(s["IS"], 1), H2=round(s["OOS"], 1),
                     drop10_t=round(cl.drop_top(t, 8, 10)[1], 2)))
for h in (2, 3):
    for m in MEM: quick(f"LOO-{m}", cl.zscale(D.drop(columns=m).mean(axis=1), 120, 40), h)
    quick("14:00 UTC snap", cl.zscale(pd.concat([(hsnap.r_snap(m, 14, 0) - cl.roll_beta(hsnap.r_snap(m, 14, 0), hsnap.r_snap("^STOXX", 14, 0), 120, 40) * hsnap.r_snap("^STOXX", 14, 0)) for m in MEM], axis=1).mean(axis=1), 120, 40), h)
    quick("ham sepet (beta yok)", cl.zscale(pd.concat([hsnap.r_snap(m, 15, 0) for m in MEM], axis=1).mean(axis=1), 120, 40), h)
    quick("demeaned", cl.zscale(P, 120, 40, demean=True), h)
    quick("lag1", z.shift(1), h)
Q = pd.DataFrame(rows); print(Q.to_string()); Q.to_csv(cl.OUT + "/c5_robust.csv", index=False)
# günlük vekil t-1 (Avrupa kapanışı) 2018-12+ VİOP
rmd = cl.lret("^STOXX", "adj"); rr = []
for m in MEM:
    r = cl.lret(m, "adj"); b = cl.roll_beta(r, rmd.reindex(r.index), 250, 100); rr.append(r - b * rmd.reindex(r.index))
Pd = pd.concat(rr, axis=1); Pd = Pd.mean(axis=1).where(Pd.notna().sum(axis=1) >= 3)
zd = cl.zscale(cl.to_bist(Pd, "after"), 250, 100)
for h in (2, 3):
    Y = ev.ydict("ASELS", "2018-12-17"); t = cl.trades(zd, Y[(h, "raw")], h, 1.0); s = cl.summ(t, 8)
    print("günlük t-1 vekil h", h, "n", s["n"], "net", round(s["net"], 1), "t", round(s["t"], 2), "IS(2019-21)", round(s["IS"], 1), "OOS", round(s["OOS"], 1), cl.by_year(t, 8), cl.periods(t, 8))
print(cl.liq("ASELS").to_string())
json.dump(out, open(cl.OUT + "/c5_def.json", "w"), ensure_ascii=False, default=str, indent=1)
