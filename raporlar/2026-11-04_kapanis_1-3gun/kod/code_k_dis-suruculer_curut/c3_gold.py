"""Aday 3: VİOP XAUUSD bugünkü uzlaşma değişimi -> F_TRALT (hedge'li), TRMET ikincil. Zamanlama: 15:00 UTC altın ile kıyas."""
import numpy as np, pandas as pd, cl, ev, json, hsnap
out = {}
g = ev.R("XAUUSD"); z = cl.zscale(g, 250, 100)
res, G, tr = ev.evaluate("GOLD_V->TRALT h2 hedged", z, "TRALT", main=(2, 1.0, "hedged"), start="2018-12-17", nsim=300)
out["TRALT_h2_hedged"] = res; G.to_csv(cl.OUT + "/c3_grid_tralt.csv", index=False); tr.to_csv(cl.OUT + "/c3_trades_tralt.csv")
r2, G2, _ = ev.evaluate("GOLD_V->TRMET h2 hedged", z, "TRMET", main=(2, 1.0, "hedged"), start="2018-12-17", nsim=200)
out["TRMET_h2_hedged"] = r2
r3, _, _ = ev.evaluate("GOLD_V->TRALT h2 raw", z, "TRALT", main=(2, 1.0, "raw"), start="2018-12-17", nsim=0, placebo=False, verbose=False)
out["TRALT_h2_raw"] = r3; print("raw", json.dumps(r3, ensure_ascii=False, default=str))
# zamanlama: 15:00 UTC altın (GC=F saatlik) ile sinyal 2024-07+
gh = hsnap.r_snap("GC=F", 15, 0)
both = pd.concat([g.rename("settle"), gh.rename("h15")], axis=1).dropna(); both = both[both.index >= "2024-07-01"]
print("corr settle vs 15:00", both.corr().iloc[0, 1].round(3), len(both))
zh = cl.zscale(gh, 120, 60)
zs_ = z.copy()
for lab, zz in (("settle-z", zs_), ("15:00-z", zh)):
    for h in (1, 2, 3):
        Y = ev.ydict("TRALT", "2024-07-01")
        t = cl.trades(zz, Y[(h, "hedged")], h, 1.0); s = cl.summ(t, 11, split="2025-07-01")
        print(lab, "h", h, "n", s["n"], "net", round(s["net"], 1), "t", round(s["t"], 2), "1.yarı", round(s["IS"], 1), "2.yarı", round(s["OOS"], 1))
agree = (np.sign(z) == np.sign(zh))[(z.abs() > 1) & zh.notna() & (z.index >= "2024-07-01")].mean()
print("|z_settle|>1 günlerinde 15:00 sinyaliyle işaret uyumu", round(agree, 3), "; |z_15|>1 de olan oran", round(((zh.abs() > 1) & (z.abs() > 1)).sum() / (z.abs() > 1)[(z.index >= "2024-07-01") & zh.notna()].sum(), 3))
# 'bir gün eski' sinyal ve TRALT kendi artığı kontrolü
rows = []
def quick(lab, zz, h=2, lg="hedged", und="TRALT", start="2018-12-17"):
    Y = ev.ydict(und, start); t = cl.trades(zz, Y[(h, lg)], h, 1.0); s = cl.summ(t, 8 + (3 if lg == "hedged" else 0))
    rows.append(dict(var=lab, und=und, h=h, leg=lg, n=s["n"], net8=round(s["net"], 1), t=round(s["t"], 2), IS=round(s["IS"], 1), OOS=round(s["OOS"], 1)))
for h in (1, 2, 3):
    quick("lag1 (dünkü altın)", z.shift(1), h); quick("demeaned", cl.zscale(g, 250, 100, demean=True), h)
    quick("XAUTRY VİOP", cl.zscale(ev.R("XAUTRY") if False else cl.fut_ret("XAUTRY"), 250, 100), h)
    quick("COMEX GC=F t-1 (günlük)", cl.zscale(cl.to_bist(cl.lret("GC=F", "c"), "after"), 250, 100), h)
Q = pd.DataFrame(rows); print(Q.to_string()); Q.to_csv(cl.OUT + "/c3_robust.csv", index=False)
L = ev.legs("TRALT")
for h in (1, 2):
    y = cl.fwd(L["hedged"], h); y = y[y.index >= "2018-12-17"]
    X = pd.concat([z.rename("z"), cl.zscale(L["hedged"], 250, 100).rename("own_resid")], axis=1)
    o = cl.nw_reg(y * 1e4, X, h + 1); print("reg h", h, o[1]); print(o[0].round(3)); out[f"reg_h{h}"] = o[0].round(3).to_dict()
    # rejim: yıllara göre regresyon katsayısı
    for a, b in (("2019", "2020"), ("2021", "2022"), ("2023", "2024"), ("2025", "2026")):
        yy = y[(y.index >= a) & (y.index < str(int(b) + 1))]
        o = cl.nw_reg(yy * 1e4, X, h + 1)
        if o: print("  ", a, b, "z b", round(o[0].loc["z", "b"], 1), "t", round(o[0].loc["z", "t"], 2), "n", o[1])
print(cl.liq("TRALT").to_string())
json.dump(out, open(cl.OUT + "/c3_gold.json", "w"), ensure_ascii=False, default=str, indent=1)
