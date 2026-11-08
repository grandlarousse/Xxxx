import sys; sys.path.insert(0, ".")
from adv_common import *
pc, q = lowmom_spot(5); pv = asof_to_viop(pc)
act = (pv != 0)
spell = (act != act.shift()).cumsum().where(act)
for h in [1, 5]:
    net = bt(pv, r_v, h, 5, demean=True)
    # pnl'i başlatan pozisyon günü spell'ine ata: net_t+1 ~ pos_t; h>1'de kaba: pnl günü t'nin spell'i (t-1 aktif)
    lab = spell.shift(1).reindex(net.index)
    if h > 1: lab = spell.ffill(limit=h).shift(1).reindex(net.index)
    g = net.groupby(lab).agg(["sum", "size"])
    g["start"] = [spell[spell == k].index.min() for k in g.index]; g["len"] = [int((spell == k).sum()) for k in g.index]
    big = g[g.len >= 5]
    for per in ["IS", "OOS"]:
        a, b = PER[per]; gg = big[(big.start >= a) & (big.start <= b)]
        print(f"h{h} {per}: >=5 günlük aktif dönem sayısı {len(gg)}, pozitif {int((gg['sum'] > 0).sum())}, toplam bps {gg['sum'].sum()*1e4:.0f}, en büyük 3'ün payı {gg['sum'].nlargest(3).sum()/gg['sum'].sum():.2f}")
    print("   OOS dönemleri:", [(str(r.start.date()), r.len, round(r['sum']*1e4)) for _, r in big[big.start > IS_END].iterrows()])
# Blok bootstrap (aylık bloklar) — OOS h5 ve FULL h1 Sharpe için %95 aralık
rng = np.random.default_rng(1)
for h, per in [(1, "FULL"), (1, "OOS"), (5, "FULL"), (5, "OOS")]:
    a, b = PER[per]; m = (r_v.index >= a) & (r_v.index <= b)
    net = bt(pv[m], r_v[m], h, 5, demean=True)
    mo = net.index.to_period("M"); blocks = [net.values[mo == p] for p in mo.unique()]
    B = []
    for _ in range(3000):
        idx = rng.integers(0, len(blocks), len(blocks)); x = np.concatenate([blocks[i] for i in idx])
        B.append(x.mean() / x.std() * np.sqrt(252))
    B = np.array(B)
    print(f"h{h} {per}: Sharpe {sh(net):.2f}, aylık blok bootstrap %95 [{np.quantile(B,0.025):.2f}, {np.quantile(B,0.975):.2f}], P(<=0) {(B<=0).mean():.3f}")
