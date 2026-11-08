"""E3-1 mekanizma tanıları (bağımsız): ayrıştırma, kaldıraçlı ürün öncesi/sonrası, 5 dk son 30 dk momentumu."""
from rc import *
import warnings; warnings.filterwarnings("ignore")
import statsmodels.api as sm
sig = pd.read_parquet(f"{OUT}/sig_m.parquet"); days = sig.index
for tgt in ["GDXJ", "GDX"]:
    r = np.log(yh(tgt).reindex(days)).diff()
    d = pd.concat([r.shift(-1).rename("y"), sig.m.rename("m"), r.rename("r")], axis=1).dropna()
    b = np.polyfit(d.m, d.r, 1)[0]; d["idio"] = d.r - b * d.m
    mm = sm.OLS(d.y, sm.add_constant(d[["m", "idio"]])).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
    print(tgt, "r_t+1 ~ m_t + idio_t:", {k: f"{mm.params[k]:.3f} (t {mm.tvalues[k]:.2f})" for k in ["m", "idio"]}, "| beta(r_t~m_t)", round(b, 2))
for tgt, launch in [("GDX", "2010-12-08"), ("GDXJ", "2013-10-03")]:
    y = fwd(np.log(yh(tgt).reindex(days)).diff(), 1)
    print(tgt, "öncesi:", ic(sig.zm[:launch], y[:launch], 5), "| sonrası:", ic(sig.zm[launch:], y[launch:], 5))
for t in ["GDXJ", "GDX", "GLD"]:
    g = pd.read_parquet(f"{P}/yahoo_5m/{t}.parquet"); g.index = g.index.tz_convert(NY); g = g.between_time("09:30", "15:55")
    c = g[g.index.strftime("%H:%M") == "15:25"]["close"]; c.index = pd.to_datetime(c.index.date)
    cl = yh(t, "close")
    a = np.log(c / cl.shift(1).reindex(c.index)); b_ = np.log(cl.reindex(c.index) / c)
    dd = pd.concat([a, b_], axis=1).dropna()
    print(t, "5 dk: t-1 kapanış->15:30 vs son 30 dk korelasyon", round(dd.iloc[:, 0].corr(dd.iloc[:, 1]), 3), "n", len(dd))
