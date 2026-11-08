import sys; sys.path.insert(0, ".")
from adv_common import *
P = s.s_p15.astype(float); ma20 = P.rolling(20).mean(); sd20 = P.rolling(20).std(); bbz = (P - ma20) / sd20
bb = asof_to_viop(pd.Series(np.where(bbz < -2, 1.0, np.where(bbz > 2, -1.0, 0.0)), index=P.index).where(bbz.notna()))
rv1 = asof_to_viop(-np.sign(r_s))
for nm, pv in [("BB_REV", bb), ("REV_1", rv1)]:
    for c in [0, 5]:
        net = bt(pv, r_v, 1, c, demean=True)
        g = net.groupby(net.index.year).mean()
        print(nm, f"{c}bps FULL {sh(net):.2f} (t {tstat(net):.2f}); yıllık pozitif {int((g>0).sum())}/{len(g)}", g.mul(1e4*252).round(0).to_dict() if c == 5 else "")
# TAILMOM long/short ve pre/post akşam seansı
tm = -bb
pre = d.index < "2020-09-18"
for nm, m in [("pre", pre), ("post", ~pre)]:
    net = bt(tm[m], r_v[m], 1, 5, demean=True); print("TAILMOM", nm, round(sh(net), 2), round(tstat(net), 2))
