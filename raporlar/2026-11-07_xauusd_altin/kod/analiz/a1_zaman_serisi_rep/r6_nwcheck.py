#!/usr/bin/env python3
"""Adım 6: NW t'nin gecikme seçimine duyarlılığı ve statsmodels ile çapraz kontrol (kendi NW uygulamam doğru mu)."""
import sys, numpy as np, pandas as pd, statsmodels.api as sm, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a1_zaman_serisi_rep")
from rutil import *
B, SP = load(); lp = SP.lp; r = SP.r; q = exp_pct(r.rolling(20).std())
x = asof_to(pd.DataFrame({"x": (lp - lp.shift(5)).where(q < 1/3)}), B.index).x
for h in [1, 3, 5]:
    y = B[f"fwd{h}"]; d = pd.concat([x.rename("x"), y.rename("y")], axis=1).dropna(); rx, ry = d.x.rank(), d.y.rank()
    zx = (rx - rx.mean()) / rx.std(); zy = (ry - ry.mean()) / ry.std()
    mine = {L: round(nw_se_slope(zy.values, zx.values, L)[0] / nw_se_slope(zy.values, zx.values, L)[1], 2) for L in [5, 10, 20]}
    smt = {L: round(float(sm.OLS(zy, sm.add_constant(zx)).fit(cov_type="HAC", cov_kwds={"maxlags": L}).tvalues.iloc[1]), 2) for L in [5, 10, 20]}
    # takvim boşluklarını koruyarak (rejim dışı günleri 0 katkı olarak tut): tam VİOP gün endeksinde skor serisi
    print(f"h{h} IC={np.corrcoef(rx, ry)[0,1]:.3f} n={len(d)} | NW t benim: {mine} | statsmodels: {smt}")
