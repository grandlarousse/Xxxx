"""Yüksek çözünürlüklü veri-madenciliği null'u: 24 varyantlık ızgarada max-t, dairesel kaydırma (2000 tekrar)."""
import numpy as np, pandas as pd, cl, ev, c1sig, json, sys, time
def run(lab, z, und, start, nsim=2000):
    Y = ev.ydict(und, start); grid = [(h, thr, lg, 8 + (3 if lg == "hedged" else 0)) for h in ev.HS for thr in ev.THR for lg in ev.LEGS]
    obs = []
    for g in grid:
        tr = cl.trades(z, Y[(g[0], g[2])], g[0], g[1]); obs.append(cl.tstat(tr["gross"].values * 1e4 - g[3]))
    t0 = time.time(); mx, per = cl.circ_null(z, Y, grid, nsim=nsim, seed=11)
    o = dict(cand=lab, obs_max_t=round(np.nanmax(obs), 2), p_maxgrid=float(np.mean(mx >= np.nanmax(obs))), null_q95=round(float(np.quantile(mx, 0.95)), 2),
             null_q99=round(float(np.quantile(mx, 0.99)), 2), secs=round(time.time() - t0))
    print(json.dumps(o, ensure_ascii=False)); return o
u = ev.R("USDTRY"); g = ev.R("XAUUSD")
out = [run("REF->TUPRS", c1sig.z_ref(), "TUPRS", "2017-03-06"), run("ASX->EREGL", c1sig.z_asx(), "EREGL", "2017-03-06"),
       run("GOLD->TRALT", cl.zscale(g, 250, 100), "TRALT", "2018-12-17"), run("USD5->THYAO", cl.zscale(sum(u.shift(i) for i in range(5)), 250, 100), "THYAO", "2017-03-06")]
pd.DataFrame(out).to_csv(cl.OUT + "/n_null.csv", index=False)
