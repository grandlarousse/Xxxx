"""06 ek: (a) BT1 brüt yıllık kırılım ve |z|>1 tek bacak; (b) gap kontrolü (açılışta eksik tepki mi?); (c) saatlik Brent(h-1)->TUPRS(h) brüt bps."""
import pandas as pd, numpy as np, statsmodels.api as sm, elib
from elib import R, DEC, ll
xud = DEC("XU100"); tu = DEC("TUPRS")
US_REF = pd.concat([R(s) for s in ["VLO", "MPC", "PSX", "PBF"]], axis=1).mean(axis=1)
sig = US_REF.shift(1); sig = sig[sig.index >= "2014-01-01"]
for lab, kw, tgt, c in [("BT1 işaret, tek bacak", dict(mode="sign"), tu.intra, 0), ("BT1zo |z|>1 tek bacak", dict(mode="z", thr=1.0), tu.intra, 0),
                        ("BT1zo |z|>1 tek bacak 8bps", dict(mode="z", thr=1.0), tu.intra, 8), ("BT1zo |z|>1 tek bacak 15bps", dict(mode="z", thr=1.0), tu.intra, 15)]:
    res, pnl = ll.backtest(sig, tgt, cost_bps=c, **kw)
    print(lab, "| IS:", {k: round(v, 2) for k, v in res["IS"].items() if k in ["n", "mean_bps", "t", "sharpe", "hit"]}, "| OOS:", {k: round(v, 2) for k, v in res["OOS"].items() if k in ["n", "mean_bps", "t", "sharpe", "hit", "maxdd_pct"]})
    print("   yıllık bps:", res["by_year_bps"])
# (b) gap kontrolü
X = pd.concat([tu.intra.rename("y"), tu.gap.rename("gap"), sig.rename("s"), xud.gap.rename("xg"), R("ES=F").shift(1).rename("es")], axis=1).dropna()
for per, x in [("ALL", X), ("IS", X[X.index < "2021"]), ("OOS", X[X.index >= "2021"])]:
    m = sm.OLS(x.y, sm.add_constant(x[["s", "gap", "xg", "es"]])).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
    print(per, "intra ~ US_REF_lag1 + TUPRS gap + XU100 gap + ES_lag1 | t:", {k: round(v, 2) for k, v in m.tvalues.items()})
# gap'in US_REF'e tepkisi (beta) vs sonraki gün-içi devam: underreaction oranı
m1 = sm.OLS(X.gap, sm.add_constant(X[["s"]])).fit(); m2 = sm.OLS(X.y, sm.add_constant(X[["s"]])).fit()
print(f"gap beta={m1.params.s:.3f}, intra beta={m2.params.s:.3f} -> toplam tepkinin gün-içi payı={m2.params.s/(m1.params.s+m2.params.s):.2f}")
# (c) saatlik
hs = ll.intraday("TUPRS")["c"]; hs = hs[~hs.index.duplicated()]
rs = np.log(hs).diff(); rs = rs[(rs.index.minute == 30) & (rs.index.hour >= 7) & (rs.index.hour <= 13)]
hd = ll.intraday("BZ=F")["c"]; hd = hd[~hd.index.duplicated()]
def at(ts):
    pos = hd.index.searchsorted(ts, side="right") - 1
    return pd.Series(np.where(pos >= 0, hd.values[np.clip(pos, 0, None)], np.nan), index=ts)
p0 = at(rs.index - pd.Timedelta(minutes=1)); pm1 = at(rs.index - pd.Timedelta(minutes=61))
lagr = pd.Series(np.log(p0.values / pm1.values), index=rs.index)
x = pd.concat([rs.rename("y"), lagr.rename("s")], axis=1).dropna(); x = x[x.s != 0]
for thr in [0, 0.003, 0.005]:
    xx = x[x.s.abs() > thr]; g = (np.sign(xx.s) * xx.y)
    print(f"saatlik Brent(h-1)->TUPRS(h) |s|>{thr}: n={len(xx)}, brüt ort={1e4*g.mean():.1f} bps, t={ll.nw_t(g)[1]:.2f} (maliyet 8-15 bps/işlem)")
