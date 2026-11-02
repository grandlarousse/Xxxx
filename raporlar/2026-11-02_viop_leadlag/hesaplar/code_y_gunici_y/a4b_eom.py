"""GÖREV 4 ek: ay sonu (VİOP vade sonu = ayın son iş günü) ve ayın ilk iş günü etkisi, günlük 2014+ (gap/gün-içi ayrışmış).
y ∈ {cc, gap, intra}; X = [eom dummy, first-day dummy]; NW(5) t. XU030 + 47 hisse havuzu (gün kümelenmiş). Yıllara göre.
Strateji: XU030 eom kapanışında al -> ilk gün kapanışında sat (takvim bilinir, look-ahead yok); ve eom açılışta sat -> eom kapanışta kapat.
Çıktı: res/a4b_eom.csv, res/a4b_eom_years.csv"""
import numpy as np, pandas as pd, c_common as c
ll = c.ll
cal = ll.bist_cal(); cal = cal[cal >= "2013-12-01"]
s = pd.Series(cal, index=cal); eom = pd.DatetimeIndex(s.groupby([cal.year, cal.month]).max().values)
first = pd.DatetimeIndex(s.groupby([cal.year, cal.month]).min().values)
rows = []; yrs = {}
def reg(y, X, groups=None):
    df = pd.concat([y.rename("y"), X], axis=1).dropna()
    if groups is None:
        import statsmodels.api as sm
        m = sm.OLS(df["y"].values, sm.add_constant(df.drop(columns="y").values)).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
        return m.params, m.tvalues, len(df)
for sym in ["XU030", "XU100"]:
    d = ll.decomp(sym); d = d[d.index >= "2014-01-01"]
    X = pd.DataFrame({"eom": d.index.isin(eom).astype(float), "first": d.index.isin(first).astype(float)}, index=d.index)
    for y in ["cc", "gap", "intra"]:
        for per, m in [("all", d.index >= "2014"), ("IS2014-20", d.index < "2021"), ("OOS2021-26", d.index >= "2021")]:
            p, t, n = reg(d[y][m], X[m])
            rows.append(dict(sym=sym, y=y, period=per, const_bps=1e4 * p[0], eom_bps=1e4 * p[1], t_eom=t[1], first_bps=1e4 * p[2], t_first=t[2], n=n))
    if sym == "XU030":
        e = d[d.index.isin(eom)]; f = d[d.index.isin(first)]
        yrs["XU030_eom_intra"] = (1e4 * e["intra"].groupby(e.index.year).mean()).round(1)
        yrs["XU030_first_gap"] = (1e4 * f["gap"].groupby(f.index.year).mean()).round(1)
        yrs["XU030_first_cc"] = (1e4 * f["cc"].groupby(f.index.year).mean()).round(1)
        yrs["XU030_other_cc"] = (1e4 * d["cc"][~d.index.isin(eom) & ~d.index.isin(first)].groupby(d.index[~d.index.isin(eom) & ~d.index.isin(first)].year).mean()).round(1)
# 47 hisse havuzu
pool = []
for sym in c.VIOP:
    d = ll.decomp(sym); d = d[d.index >= "2014-01-01"].copy(); d["date"] = d.index; pool.append(d)
P = pd.concat(pool); P["eom"] = P["date"].isin(eom).astype(float); P["first"] = P["date"].isin(first).astype(float)
for y in ["cc", "gap", "intra"]:
    for per, m in [("all", P.index >= "2014"), ("IS2014-20", P.index < "2021"), ("OOS2021-26", P.index >= "2021")]:
        df = P[m][[y, "eom", "first", "date"]].dropna()
        b, se, cov, r2, n = c.ols_cl(df[y].values, df[["eom", "first"]].values, df["date"].values)
        rows.append(dict(sym="47_havuz", y=y, period=per, const_bps=1e4 * b[0], eom_bps=1e4 * b[1], t_eom=b[1] / se[1], first_bps=1e4 * b[2], t_first=b[2] / se[2], n=n))
R = pd.DataFrame(rows); R.to_csv(c.RES + "/a4b_eom.csv", index=False)
Y = pd.DataFrame(yrs); Y.to_csv(c.RES + "/a4b_eom_years.csv")
pd.set_option("display.width", 200); print(R.round(2).to_string()); print(Y.to_string())
