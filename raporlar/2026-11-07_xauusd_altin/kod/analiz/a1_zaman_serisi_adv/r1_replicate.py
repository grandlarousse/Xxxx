import sys; sys.path.insert(0, ".")
from adv_common import *
pc, q = lowmom_spot(5)
pv = asof_to_viop(pc)
print("aktif gün payı VİOP:", (pv.abs() > 0).mean().round(3), " long payı aktifte:", (pv[pv != 0] > 0).mean().round(3))
for h in [1, 3, 5]:
    out = {}
    for nm, (a, b) in PER.items():
        m = (r_v.index >= a) & (r_v.index <= b)
        net = bt(pv[m], r_v[m], h, 5, demean=True); raw = bt(pv[m], r_v[m], h, 5)
        out[nm] = (round(sh(net), 2), round(tstat(net), 2), round(sh(raw), 2))
    print("h", h, out)
# IC (spearman) ret5 on low vol days vs fwd1
from scipy.stats import spearmanr
x = asof_to_viop((lp - lp.shift(5)).where(q < 1/3))
for h in [1, 5]:
    y = d[f"fwd{h}"]; dd = pd.concat([x, y], axis=1).dropna()
    print("IC h", h, spearmanr(dd.iloc[:, 0], dd.iloc[:, 1])[0].round(3), len(dd))
# rejim payı yıllık
print(pd.DataFrame({"act": (pv != 0), "long": (pv > 0)}).groupby(pv.index.year).mean().round(2).T.to_string())
