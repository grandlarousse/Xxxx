"""Aday 2: ASX FMG/BHP bugünkü artığı -> F_EREGL. Bağımsız yeniden hesap."""
import numpy as np, pandas as pd, cl, ev, json
MEM = ["FMG.AX", "BHP.AX"]
rm = cl.lret("^AXJO", "adj")
def resid(m, beta1=False):
    r = cl.lret(m, "adj")
    if beta1: return r - rm.reindex(r.index)
    b = cl.roll_beta(r, rm.reindex(r.index), 250, 100); return r - b * rm.reindex(r.index)
def basket(mem, beta1=False):
    df = pd.concat([resid(m, beta1) for m in mem], axis=1); return df.mean(axis=1).where(df.notna().sum(axis=1) >= len(mem))
def zsig(P, c=None, lag=0):
    Pb = cl.to_bist(P, "before", c)
    if lag: Pb = Pb.shift(lag)
    return cl.zscale(Pb, 250, 100)
out = {}
P = basket(MEM); z = zsig(P)
res, G, tr = ev.evaluate("MINERS_AU->EREGL h3 hedged", z, "EREGL", main=(3, 1.0, "hedged"), nsim=300)
out["main_h3_hedged"] = res; G.to_csv(cl.OUT + "/c2_grid.csv", index=False); tr.to_csv(cl.OUT + "/c2_trades.csv")
zb1 = zsig(basket(MEM, beta1=True))
r2, _, _ = ev.evaluate("MINERS_AU beta1 -> EREGL h3 raw", zb1, "EREGL", main=(3, 1.0, "raw"), nsim=200, verbose=True)
out["beta1_h3_raw"] = r2
r3, _, _ = ev.evaluate("MINERS_AU -> EREGL h2 hedged", z, "EREGL", main=(2, 1.0, "hedged"), nsim=0, placebo=False, verbose=False); out["h2_hedged"] = r3
print("h2 hedged", json.dumps(r3, ensure_ascii=False, default=str))
rows = []
def quick(lab, zz, h=3, lg="hedged", und="EREGL"):
    Y = ev.ydict(und, "2017-03-06"); t = cl.trades(zz, Y[(h, lg)], h, 1.0)
    s = cl.summ(t, 8 + (3 if lg == "hedged" else 0))
    rows.append(dict(var=lab, und=und, h=h, leg=lg, n=s["n"], net8=round(s["net"], 1), t=round(s["t"], 2), IS=round(s["IS"], 1), OOS=round(s["OOS"], 1)))
for h in (2, 3):
    quick("only-FMG", zsig(basket(["FMG.AX"])), h); quick("only-BHP", zsig(basket(["BHP.AX"])), h)
    quick("lag1 (dünkü ASX)", zsig(P, lag=1), h); quick("demeaned", cl.zscale(cl.to_bist(P, "before"), 250, 100, demean=True), h)
    quick("ham FMG getirisi (artık değil)", cl.zscale(cl.to_bist(cl.lret("FMG.AX"), "before"), 250, 100), h)
    quick("ASX200 kendisi", cl.zscale(cl.to_bist(rm, "before"), 250, 100), h)
    quick("KRDMD", z, h, und="KRDMD")
Q = pd.DataFrame(rows); print(Q.to_string()); Q.to_csv(cl.OUT + "/c2_robust.csv", index=False)
L = ev.legs("EREGL"); m = ev.R("XU030")
for h in (2, 3):
    y = cl.fwd(L["hedged"], h); y = y[y.index >= "2017-03-06"]
    X = pd.concat([z.rename("z"), cl.zscale(L["hedged"], 250, 100).rename("own_resid"), cl.zscale(m, 250, 100).rename("xu030")], axis=1)
    o = cl.nw_reg(y * 1e4, X, h + 1); print("reg h", h, o[1]); print(o[0].round(3)); out[f"reg_h{h}"] = o[0].round(3).to_dict()
c = ev.scal(); zs = cl.zscale(cl.to_bist(P, "before", c), 250, 100)
for h, lg in ((2, "hedged"), (3, "hedged"), (3, "raw")):
    o, _ = ev.evaluate_spot("MINERS_AU->EREGL spot", zs, "EREGL.IS", main=(h, 1.0, lg)); out[f"spot_h{h}_{lg}"] = o
json.dump(out, open(cl.OUT + "/c2_asx.json", "w"), ensure_ascii=False, default=str, indent=1)
