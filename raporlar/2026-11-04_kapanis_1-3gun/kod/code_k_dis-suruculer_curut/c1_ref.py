"""Aday 1: ABD rafineri sepeti (VLO, MPC, PSX, PBF) dünkü artığı -> F_TUPRS. Bağımsız yeniden hesap."""
import numpy as np, pandas as pd, cl, ev, json
MEM = ["VLO", "MPC", "PSX", "PBF"]
rm = cl.lret("^GSPC", "adj")
def resid(m):
    r = cl.lret(m, "adj"); b = cl.roll_beta(r, rm.reindex(r.index), 250, 100)
    return r - b * rm.reindex(r.index)
RS = {m: resid(m) for m in MEM}
def basket(members, beta1=False, minm=None):
    if beta1:
        df = pd.concat([cl.lret(m, "adj") for m in members], axis=1).sub(rm, axis=0)
    else:
        df = pd.concat([RS[m] for m in members], axis=1)
    minm = minm or max(1, len(members) - 1)
    P = df.mean(axis=1).where(df.notna().sum(axis=1) >= minm)
    return P
def zsig(P, c=None, lag=0):
    Pb = cl.to_bist(P, "after", c)
    if lag: Pb = Pb.shift(lag)
    return cl.zscale(Pb, 250, 100)
out = {}
P = basket(MEM)
z = zsig(P)
res, G, tr = ev.evaluate("REF_US->TUPRS", z, "TUPRS", main=(2, 1.0, "raw"), nsim=300)
out["main_h2_raw"] = res
G.to_csv(cl.OUT + "/c1_grid.csv", index=False); tr.to_csv(cl.OUT + "/c1_trades_h2raw.csv")
r3, _, tr3 = ev.evaluate("REF_US->TUPRS h3", z, "TUPRS", main=(3, 1.0, "raw"), nsim=0, placebo=True, verbose=False)
out["main_h3_raw"] = r3; print("h3", json.dumps(r3, ensure_ascii=False, default=str))
r3h, _, _ = ev.evaluate("REF_US->TUPRS h2 hedged", z, "TUPRS", main=(2, 1.0, "hedged"), nsim=0, placebo=False, verbose=False)
out["main_h2_hedged"] = r3h; print("h2 hedged", json.dumps(r3h, ensure_ascii=False, default=str))
# sağlamlık: beta=1, LOO, tek üye, bir gün eski, demeaned z, 120g pencere
rows = []
def quick(lab, zz, h=2, lg="raw"):
    Y = ev.ydict("TUPRS", "2017-03-06"); t = cl.trades(zz, Y[(h, lg)], h, 1.0)
    s = cl.summ(t, 8 + (3 if lg == "hedged" else 0))
    rows.append(dict(var=lab, h=h, leg=lg, n=s["n"], net8=round(s["net"], 1), t=round(s["t"], 2), IS=round(s["IS"], 1), OOS=round(s["OOS"], 1)))
for h in (2, 3):
    quick("beta1", zsig(basket(MEM, beta1=True)), h)
    for m in MEM: quick(f"LOO-{m}", zsig(basket([x for x in MEM if x != m])), h)
    for m in MEM: quick(f"only-{m}", zsig(basket([m], minm=1)), h)
    quick("lag1 (t-2 ABD günü)", zsig(P, lag=1), h)
    quick("120g std", cl.zscale(cl.to_bist(P, "after"), 120, 60), h)
    quick("demeaned z", cl.zscale(cl.to_bist(P, "after"), 250, 100, demean=True), h)
    # 'look-ahead' kontrolü: ABD t günü (BIST kapanışından SONRA kapanır) — kullanılamaz, yalnız mekanizma için
    Pb_same = cl.to_bist(P, "before"); quick("YASAK: ABD aynı gün t", cl.zscale(Pb_same, 250, 100), h)
Q = pd.DataFrame(rows); print(Q.to_string()); Q.to_csv(cl.OUT + "/c1_robust.csv", index=False)
# regresyon: y_h ~ z + TUPRS bugünkü hedged artığı + XU030 bugün
L = ev.legs("TUPRS"); m = ev.R("XU030")
for h in (2, 3):
    y = cl.fwd(L["raw"], h); y = y[y.index >= "2017-03-06"]
    X = pd.concat([z.rename("z"), cl.zscale(L["hedged"], 250, 100).rename("own_resid"), cl.zscale(m, 250, 100).rename("xu030")], axis=1)
    o = cl.nw_reg(y * 1e4, X, h + 1); print("reg h", h, o[1]); print(o[0].round(3))
    out[f"reg_h{h}"] = o[0].round(3).to_dict()
# spot 2014+
c = ev.scal()
zs = cl.zscale(cl.to_bist(P, "after", c), 250, 100)
for h in (2, 3):
    o, _ = ev.evaluate_spot("REF_US->TUPRS spot", zs, "TUPRS.IS", main=(h, 1.0, "raw")); out[f"spot_h{h}"] = o
json.dump(out, open(cl.OUT + "/c1_ref.json", "w"), ensure_ascii=False, default=str, indent=1)
