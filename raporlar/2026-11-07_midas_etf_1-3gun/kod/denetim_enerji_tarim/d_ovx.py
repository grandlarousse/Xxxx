"""Denetim: OVX >= 1,25 x SMA20 iken USO'nun sonraki 3 günlük |hareketi| (EN07 boyut kuralı). OVX 16:15 ET -> t+1'den ölçülür.
Çalıştırma: python3 -I kod/denetim_enerji_tarim/d_ovx.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from scipy import stats as sst
import dsim as D, lib
u = lib.load("USO")["c"]; ovx = lib.vol_index("OVX").reindex(u.index).ffill()
flag = (ovx >= 1.25 * ovx.rolling(20).mean())
a3 = (u.shift(-4) / u.shift(-1) - 1).abs()   # t+1 kapanış -> t+4 kapanış (OVX 16:15 bilgisi temiz)
a3b = (u.shift(-3) / u - 1).abs()
for nm, x in (("t+1->t+4", a3), ("t->t+3", a3b)):
    d = pd.DataFrame({"f": flag, "a": x}).dropna()
    m1, m0 = d.a[d.f].mean(), d.a[~d.f].mean(); t, p = sst.ttest_ind(d.a[d.f], d.a[~d.f], equal_var=False)
    di = d[d.index > lib.IS_END]; r_oos = di.a[di.f].mean() / di.a[~di.f].mean()
    di = d[d.index <= lib.IS_END]; r_is = di.a[di.f].mean() / di.a[~di.f].mean()
    print(f"{nm}: bayraklı gün {int(d.f.sum())}, |3g| {m1*1e4:.0f} vs {m0*1e4:.0f} bp, oran {m1/m0:.2f} (t {t:.2f}); IS oran {r_is:.2f}, OOS oran {r_oos:.2f}")
