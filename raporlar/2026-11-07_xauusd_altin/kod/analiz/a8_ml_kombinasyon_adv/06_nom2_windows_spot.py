"""Hakem: -Δk nom2 (k=3..20) spot panelde 2010-16 (bağımsız) ve 2017-26; h=1. Ayrıca VİOP'ta 2024-26 hariç."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/code")
from lib_altin import load_viop, load_spot, ic, backtest, fwd
d = load_viop(); s = load_spot()
asof = lambda x: x.reindex(x.index.union(d.index)).ffill(limit=2).reindex(d.index)
for k in (3, 5, 7, 10, 15, 20):
    x = -s.ust_nom2.diff(k); y = s.sfwd1
    xv = asof(x); yv = fwd(d.v_ret, 1)
    pre = (yv.index < "2024-01-01")
    print(f"k={k:2d} spot2010-16 t {ic(x.loc['2010':'2016'], y.loc['2010':'2016'], 5)['t']:.2f}  spot2017-26 t {ic(x.loc['2017':], y.loc['2017':], 5)['t']:.2f}  "
          f"VİOP 2017-23 t {ic(xv[pre].loc['2017-03':], yv[pre].loc['2017-03':], 5)['t']:.2f}  VİOP Pearson 2017+ t {ic(xv.loc['2017-03':], yv.loc['2017-03':], 5, method='pearson')['t']:.2f}  "
          f"spot2010-16 Sharpe {backtest(np.sign(x).loc['2010':'2016'], s.s_ret.loc['2010':'2016'].dropna(), 1)['sharpe']:.2f}")
x = (s.ust_nom10 - s.ust_nom2).diff(5); xv = asof(x); yv = fwd(d.v_ret, 1); pre = (yv.index < "2024-01-01")
print("curve_d5 VİOP 2017-23 t", round(ic(xv[pre].loc["2017-03":], yv[pre].loc["2017-03":], 5)["t"], 2))
x = np.log(s.xau_p15 / s.xau_p14); xv = asof(x); yv = fwd(d.v_ret, 5); pre = (yv.index < "2024-01-01")
print("seg_last1h h5 VİOP 2017-23 t", round(ic(xv[pre].loc["2017-03":], yv[pre].loc["2017-03":], 5)["t"], 2))
