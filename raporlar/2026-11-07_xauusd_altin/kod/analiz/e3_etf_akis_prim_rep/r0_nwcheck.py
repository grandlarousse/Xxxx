import numpy as np, pandas as pd, statsmodels.api as sm
from rc import nw_t
rng = np.random.default_rng(1); n = 3000
x = rng.standard_normal(n); e = np.convolve(rng.standard_normal(n + 4), np.ones(5) / 5, "valid")[:n]
y = 0.05 * x + e
b, t = nw_t(y, x, 5)
m = sm.OLS(y, sm.add_constant(x)).fit(cov_type="HAC", cov_kwds={"maxlags": 5, "use_correction": False})
m2 = sm.OLS(y, sm.add_constant(x)).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
print("own", round(b, 5), round(t, 4), "| sm no-corr", round(m.params[1], 5), round(m.tvalues[1], 4), "| sm default", round(m2.tvalues[1], 4))
