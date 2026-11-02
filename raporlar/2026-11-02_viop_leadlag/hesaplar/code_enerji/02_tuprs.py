"""TUPRS derin analiz: (1) Brent mi crack mı? frekans (günlük/haftalık/aylık/çeyreklik), USD bazlı; çoklu regresyon.
(2) Yıllara göre / 2022 dizel crack rejimi. (3) ABD/AB rafineri emsalleri lag1 -> TUPRS gün-içi (işlenebilir?) kontrollü regresyon."""
import pandas as pd, numpy as np, statsmodels.api as sm, elib
from elib import R, DEC, ll
out = []
def P(*a):
    s = " ".join(str(x) for x in a); out.append(s); print(s)

# ---- fiyat seviyeleri (USD) ----
tu = ll.daily("TUPRS"); usd = ll.daily("TRY=X"); xu = ll.daily("XU100")
cr = elib.cracks()
lv = pd.concat([(tu / usd).rename("TU_usd"), (xu / usd).rename("XU_usd"), tu.rename("TU_tl"), cr], axis=1).dropna()
lv = lv[lv.index >= "2008-01-01"]
def freq_tab(rule):
    x = lv.resample(rule).last()
    d = pd.DataFrame({"tu": np.log(x.TU_usd).diff(), "tu_tl": np.log(x.TU_tl).diff(), "xu": np.log(x.XU_usd).diff(), "bz": np.log(x.BZ).diff(),
                      "dho": x.ho_crack.diff() / x.BZ.shift(1), "drb": x.rb_crack.diff() / x.BZ.shift(1), "d321": x.c321.diff() / x.BZ.shift(1),
                      "dho_lvl": x.ho_crack.diff(), "d321_lvl": x.c321.diff()}).dropna()
    # tatil/ffill sorunu yok (resample last). roll gürültüsü: winsorize %1
    for c in ["dho", "drb", "d321"]:
        lo, hi = d[c].quantile([.01, .99]); d[c] = d[c].clip(lo, hi)
    return d
res = []
for rule, lab in [("W-FRI", "haftalık"), ("ME", "aylık"), ("QE", "çeyreklik")]:
    d = freq_tab(rule)
    for per, dd in [("tam", d), ("IS14-20", d[(d.index >= "2014") & (d.index < "2021")]), ("OOS21-26", d[d.index >= "2021"]), ("2022", d[(d.index >= "2022") & (d.index < "2023")])]:
        if len(dd) < 8: continue
        r = {"frek": lab, "dönem": per, "n": len(dd)}
        for c in ["bz", "dho", "drb", "d321"]:
            r["c_" + c] = dd.tu.corr(dd[c]); r["pc_" + c] = ll.partial_corr(dd.tu, dd[c], [dd.xu])[0]
        # çoklu: tu ~ xu + bz + d321
        X = sm.add_constant(dd[["xu", "bz", "d321"]]); m = sm.OLS(dd.tu, X).fit(cov_type="HAC", cov_kwds={"maxlags": 3})
        r.update({"b_bz": m.params.bz, "t_bz": m.tvalues.bz, "b_321": m.params.d321, "t_321": m.tvalues.d321, "r2": m.rsquared})
        X = sm.add_constant(dd[["xu", "bz", "dho"]]); m = sm.OLS(dd.tu, X).fit(cov_type="HAC", cov_kwds={"maxlags": 3})
        r.update({"t_bz_ho": m.tvalues.bz, "t_ho": m.tvalues.dho})
        res.append(r)
F = pd.DataFrame(res); F.to_csv(elib.RES + "/tuprs_brent_vs_crack_freq.csv", index=False)
P("== TUPRS(USD) ~ Brent vs crack, frekansa göre (c=corr, pc=XU100usd kontrollü; t_ = HAC t, çoklu reg tu~xu+bz+d321)")
P(F[["frek", "dönem", "n", "c_bz", "pc_bz", "c_dho", "pc_dho", "c_d321", "pc_d321", "t_bz", "t_321", "t_ho", "r2"]].round(2).to_string(index=False))

# yıllık: aylık pcorr yerine haftalık pcorr yıl bazında
d = freq_tab("W-FRI"); yr = []
for y, dd in d.groupby(d.index.year):
    if len(dd) < 30: continue
    yr.append({"yıl": y, "pc_bz": ll.partial_corr(dd.tu, dd.bz, [dd.xu])[0], "pc_dho": ll.partial_corr(dd.tu, dd.dho, [dd.xu])[0], "pc_d321": ll.partial_corr(dd.tu, dd.d321, [dd.xu])[0]})
Y = pd.DataFrame(yr); Y.to_csv(elib.RES + "/tuprs_weekly_pcorr_by_year.csv", index=False)
P("== Haftalık kısmi korelasyon yıl bazında"); P(Y.round(2).to_string(index=False))
# crack seviyesi (çeyreklik ortalama) bilgi
q = lv.resample("QE").mean()[["ho_crack", "rb_crack", "c321", "BZ"]]
P("== Çeyreklik ortalama crack ($/bbl) son 16 çeyrek"); P(q.tail(16).round(1).to_string())

# ---- (3) emsal lag1 -> TUPRS gün-içi, kontroller ----
dd = DEC("TUPRS"); xd = DEC("XU100")
bask_us = pd.concat([R(s) for s in ["VLO", "MPC", "PSX", "PBF"]], axis=1).mean(axis=1).rename("US_REF")
bask_eu = pd.concat([R(s) for s in ["PKN.WA", "MOL.BD", "MOH.AT", "ELPE.AT", "NESTE.HE", "GALP.LS", "REP.MC", "OMV.VI"]], axis=1).mean(axis=1).rename("EU_REF")
X = pd.concat([dd.intra.rename("y"), (dd.intra - xd.intra).rename("y_h"), dd.gap.rename("gap"), bask_us.shift(1), bask_eu.shift(1), R("CRAK").shift(1).rename("CRAK"),
               R("ES=F").shift(1).rename("ES"), R("BZ=F").shift(1).rename("BZ"), R("XLE").shift(1).rename("XLE"), R("^STOXX").shift(1).rename("STOXX"), xd.intra.rename("xu_intra")], axis=1).dropna()
X = X[X.index >= "2014-01-01"]
def reg(y, cols, sub=None, lab=""):
    Z = X if sub is None else sub
    m = sm.OLS(Z[y], sm.add_constant(Z[cols])).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
    return lab + " " + y + " ~ " + "+".join(cols) + " | t: " + ", ".join(f"{c}={m.tvalues[c]:.2f}" for c in cols) + f" | n={int(m.nobs)}"
P("== Emsal lag1 -> TUPRS gün-içi (y) ve XU100'e göre hedge gün-içi (y_h)")
for per, sub in [("ALL", X), ("IS", X[X.index < "2021"]), ("OOS", X[X.index >= "2021"])]:
    P(reg("y", ["US_REF", "ES", "BZ"], sub, per)); P(reg("y_h", ["US_REF", "ES", "BZ"], sub, per))
    P(reg("y", ["EU_REF", "STOXX", "BZ"], sub, per)); P(reg("y_h", ["EU_REF", "STOXX", "BZ"], sub, per))
    P(reg("y_h", ["CRAK", "XLE", "ES"], sub, per)); P(reg("gap", ["US_REF", "ES", "BZ"], sub, per))
open(elib.RES + "/02_tuprs.txt", "w").write("\n".join(out))
