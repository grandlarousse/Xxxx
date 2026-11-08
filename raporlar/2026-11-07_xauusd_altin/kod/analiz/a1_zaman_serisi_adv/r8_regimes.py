import sys; sys.path.insert(0, ".")
from adv_common import *
pc, q = lowmom_spot(5)
qv = asof_to_viop(q)
sg = asof_to_viop(np.sign(lp - lp.shift(5)))
def st(pos, h=1, mode="full"):
    o = {}
    for per in ["IS", "OOS", "FULL"]:
        a, b = PER[per]; m = (r_v.index >= a) & (r_v.index <= b)
        net = bt(pos[m], r_v[m], h, 5, demean=True, demean_mode=mode); o[per] = f"{sh(net):.2f}({tstat(net):.2f})"
    return o
for h in [1, 5]:
    print(f"--- h={h}")
    print("TSMOM5 koşulsuz          ", st(sg, h))
    print("TSMOM5 q<1/3 (LOWMOM)    ", st(sg.where(qv < 1/3, 0), h))
    print("TSMOM5 1/3<=q<=2/3 (orta)", st(sg.where((qv >= 1/3) & (qv <= 2/3), 0), h))
    print("TSMOM5 q>2/3 (yüksek)    ", st(sg.where(qv > 2/3, 0), h))
    print("SAKİN-UZUN (q<1/3 → +1)  ", st(pd.Series(1.0, index=d.index).where(qv < 1/3, 0), h))
    print("SAKİN-UZUN yıl-demean    ", st(pd.Series(1.0, index=d.index).where(qv < 1/3, 0), h, "year"))
# aktif gün başına IC farkı: aktif günlerde corr(sign ret5, fwd1) düşük/orta/yüksek rejimde
from scipy.stats import spearmanr
x5 = asof_to_viop(lp - lp.shift(5))
for h in [1, 5]:
    y = d[f"fwd{h}"]
    for nm, m in [("lo", qv < 1/3), ("mid", (qv >= 1/3) & (qv <= 2/3)), ("hi", qv > 2/3)]:
        for per in ["IS", "OOS"]:
            a, b = PER[per]; mm = m & (d.index >= a) & (d.index <= b)
            dd = pd.concat([x5[mm], y[mm]], axis=1).dropna()
            print(h, nm, per, "IC", round(spearmanr(dd.iloc[:, 0], dd.iloc[:, 1])[0], 3), "n", len(dd))
