import sys; sys.path.insert(0, ".")
from adv_common import *
pc, q = lowmom_spot(5); pv = asof_to_viop(pc)
def per_stats(pos, ret, h, cost=5, mode="full"):
    o = {}
    for per in ["IS", "OOS", "FULL", "2017-19", "2020-21", "2022-23", "2024-26"]:
        a, b = PER[per]; m = (ret.index >= a) & (ret.index <= b)
        net = bt(pos[m], ret[m], h, cost, demean=True, demean_mode=mode)
        o[per] = f"{sh(net):.2f}({tstat(net):.2f})"
    return o
for h in [1, 5]:
    for mode in ["full", "year", "trail250"]:
        print(f"h{h} demean={mode:8s}", per_stats(pv, r_v, h, 5, mode))
    print(f"h{h} LONG bacak (yıl-demean)", per_stats(pv.clip(lower=0), r_v, h, 5, "year"))
    print(f"h{h} SHORT bacak (yıl-demean)", per_stats(pv.clip(upper=0), r_v, h, 5, "year"))
    print(f"h{h} LONG bacak (full-demean)", per_stats(pv.clip(lower=0), r_v, h, 5, "full"))
    print(f"h{h} SHORT bacak (full-demean)", per_stats(pv.clip(upper=0), r_v, h, 5, "full"))
    print(f"h{h} 10bps full-demean", per_stats(pv, r_v, h, 10, "full"))
    print(f"h{h} 25bps (perakende) full-demean", per_stats(pv, r_v, h, 25, "full"))
# yıl yıl: aktif gün, long payı, yıl-demean Sharpe, ham pnl (bps/yıl)
for h in [1, 5]:
    net_y = bt(pv, r_v, h, 5, demean=True, demean_mode="year"); net_f = bt(pv, r_v, h, 5, demean=True); raw = bt(pv, r_v, h, 5)
    Y = pd.DataFrame({"act": (pv != 0).groupby(pv.index.year).mean(), "long_share_act": (pv[pv != 0] > 0).groupby(pv[pv != 0].index.year).mean(),
                      "ret_yr%": r_v.groupby(r_v.index.year).sum() * 100,
                      "sh_full_dm": net_f.groupby(net_f.index.year).apply(sh), "sh_year_dm": net_y.groupby(net_y.index.year).apply(sh),
                      "pnl_raw_bps": raw.groupby(raw.index.year).sum() * 1e4, "pnl_yrdm_bps": net_y.groupby(net_y.index.year).sum() * 1e4})
    print(f"\nh={h} yıllık"); print(Y.round(2).to_string())
# Dairesel kaydırma (circular shift) null: pozisyon serisini getiriye göre rastgele kaydır
rng = np.random.default_rng(0)
for h in [1, 5]:
    obs = sh(bt(pv, r_v, h, 5, demean=True))
    P = pv.reindex(r_v.index).fillna(0).values; n = len(P); null = []
    for _ in range(2000):
        sft = rng.integers(60, n - 60)
        null.append(sh(bt(pd.Series(np.roll(P, sft), index=r_v.index), r_v, h, 5, demean=True)))
    null = np.array(null)
    print(f"h{h} circular-shift null: obs {obs:.2f}, null mean {null.mean():.2f} sd {null.std():.2f}, p(one-sided) {(null >= obs).mean():.4f}")
