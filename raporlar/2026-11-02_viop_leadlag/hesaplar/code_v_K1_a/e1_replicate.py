"""(a) K1 yeniden üretim: CIMSA/OYAKC |gap|>%1 fade -> intra; maliyet 10 bps; IS 2014-2020 / OOS 2021+; yıllara göre."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_K1_a")
from vk import *
rows = []
def stats(pnl):
    m, t, n = nw_mean_t(pnl.values)
    return 1e4 * m, t, n
for s in ["CIMSA", "OYAKC", "XU100"]:
    d = decomp(s).dropna(subset=["gap", "intra"])
    for thr in [0.0, 0.005, 0.01, 0.015, 0.02, 0.03]:
        x = d[d.gap.abs() > thr]
        g = -np.sign(x.gap) * x.intra
        for cost in [0, 10]:
            p = g - cost / 1e4
            a = stats(p); i = stats(p[p.index < SPLIT]); o = stats(p[p.index >= SPLIT])
            yr = (1e4 * p.groupby(p.index.year).mean())
            rows.append(dict(sym=s, thr=thr, cost=cost, n=a[2], all_bps=a[0], all_t=a[1], IS_bps=i[0], IS_t=i[1], IS_n=i[2], OOS_bps=o[0], OOS_t=o[1], OOS_n=o[2],
                             yrs_pos=int((yr > 0).sum()), n_yrs=len(yr), hit=float((p > 0).mean())))
            if thr == 0.01 and cost == 10:
                print(s, "yıllık net bps:", yr.round(0).to_dict())
                print(s, "yıllık n:", p.groupby(p.index.year).size().to_dict())
    # korelasyonlar
    for per, msk in [("2014-20", d.index < SPLIT), ("2021+", d.index >= SPLIT), ("all", d.index >= "2014")]:
        print(s, per, "corr(gap,intra)=%.3f" % d[msk].gap.corr(d[msk].intra), "n", msk.sum())
    print(s, "yıllık corr(gap,intra):", d.groupby(d.index.year).apply(lambda g: round(g.gap.corr(g.intra), 2)).to_dict())
R = pd.DataFrame(rows); R.to_csv(OUT + "/res_e1_replicate.csv", index=False)
pd.set_option("display.width", 250)
print(R.round(2).to_string(index=False))
