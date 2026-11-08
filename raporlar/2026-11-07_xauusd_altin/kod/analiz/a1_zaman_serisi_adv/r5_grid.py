import sys; sys.path.insert(0, ".")
from adv_common import *
for H in ["14", "15", "16"]:
    sp = np.log(d[f"xau_p{H}"].astype(float)).diff(); same = d.v_code == d.v_code.shift(1)
    print("std(v_ret - spot", H, ") bps:", ((r_v - sp)[same].std() * 1e4).round(1))
rows = []
cache_q = {}
for rvwin in [10, 20, 40, 60]:
    rv = r_s.rolling(rvwin).std(); cache_q[rvwin] = exp_pct(rv)
for rvwin in [10, 20, 40, 60]:
    q = cache_q[rvwin]
    for thr in [0.2, 0.25, 0.3, 1/3, 0.4, 0.5, 0.6]:
        for k in [2, 3, 4, 5, 6, 7, 8, 10, 15, 20]:
            pc = np.sign(lp - lp.shift(k)).where(q < thr, 0.0).where(q.notna())
            pv = asof_to_viop(pc)
            for h in [1, 5]:
                o = dict(rvwin=rvwin, thr=round(thr, 3), k=k, h=h)
                for per in ["IS", "OOS", "FULL"]:
                    a, b = PER[per]; m = (r_v.index >= a) & (r_v.index <= b)
                    o[per] = round(sh(bt(pv[m], r_v[m], h, 5, demean=True)), 2)
                # erken spot 2010-16
                me = (s.index >= "2010-01-01") & (s.index <= "2016-12-31")
                o["E"] = round(sh(bt(pc[me], r_s[me], h, 5, demean=True)), 2)
                rows.append(o)
G = pd.DataFrame(rows); G.to_csv("grid_lowmom.csv", index=False)
for h in [1, 5]:
    g = G[(G.h == h) & (G.rvwin == 20)]
    print(f"\nh={h} rvwin=20, FULL demeaned Sharpe (satır thr, sütun k)"); print(g.pivot(index="thr", columns="k", values="FULL").to_string())
    print(f"h={h} rvwin=20, IS"); print(g.pivot(index="thr", columns="k", values="IS").to_string())
    print(f"h={h} rvwin=20, Erken 2010-16"); print(g.pivot(index="thr", columns="k", values="E").to_string())
    for rw in [10, 40, 60]:
        g2 = G[(G.h == h) & (G.rvwin == rw)]
        print(f"h={h} rvwin={rw} FULL"); print(g2.pivot(index="thr", columns="k", values="FULL").to_string())
for h in [1, 5]:
    g = G[G.h == h]
    print(h, "grid median FULL", g.FULL.median(), "IS", g.IS.median(), "OOS", g.OOS.median(), "E", g.E.median(), " pay(FULL>0)", (g.FULL > 0).mean().round(2), " base rank pct", (g.FULL < g[(g.rvwin==20)&(g.k==5)&(g.thr==0.333)].FULL.iloc[0]).mean().round(2))
