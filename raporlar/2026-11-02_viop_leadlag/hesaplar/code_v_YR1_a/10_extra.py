"""Ek kontroller: NAV ağırlık karıştırma (düzeltilmiş), bacak-özel maliyet, KCHOL-XU030 vadeli backtest, SAHOL/AKBNK yoğunlaşma ve 2026 hariç."""
import sys; HERE = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_YR1_a'; sys.path.insert(0, HERE)
exec(open(HERE + '/07_nav.py').read().split("if __name__ == '__main__':")[0])
from fut import cont
pd.set_option('display.width', 260)
def st2(sim, pers=(('IS', '2014-01-01', SPLIT), ('OOS', SPLIT, '2027-01-01'))):
    o = {}
    for p, lo, hi in pers:
        s = summarize(sim, lo, hi); o[f'{p}_m'] = s['mean_bps']; o[f'{p}_t'] = s['t_all']; o[f'{p}_n'] = s['n_act']
    return o
navr = nav_ret(W0); pos, z = signal(navr)
# 1) ağırlık karıştırma
R = []
for s in range(30):
    rg = np.random.default_rng(100 + s); mult = rg.uniform(.7, 1.3, len(W0))
    W = {k: v * m for (k, v), m in zip(W0.items(), mult)}
    p_, _ = signal(nav_ret(W)); R.append(st2(simulate(p_, tg, ti, tc, lw, 'open', 8)))
R = pd.DataFrame(R); print('NAV ağırlıkları ±%30 rastgele (30 çekiliş): IS t ort/min/maks', R.IS_t.mean().round(2), R.IS_t.min().round(2), R.IS_t.max().round(2), '| OOS t', R.OOS_t.mean().round(2), R.OOS_t.min().round(2), R.OOS_t.max().round(2))
# 2) bacak-özel maliyet: KCHOL c bps, XU030 vadeli 3 bps (gidiş-dönüş) -> nominal ağırlıklı ortalama
for c in [8, 15, 30]:
    eff = (c * 1 + 3 * bm.abs()) / (1 + bm.abs())
    sims = []
    sim = simulate(pos, tg, ti, tc, lw, 'open', 0); per_side = (eff / 1e4) / 2 * lw
    sim['pnl'] = sim['gross'] - sim['trade'] * per_side.reindex(sim.index).ffill()
    print(f'KCHOL {c} bps + XU030 3 bps:', {k: round(v, 2) for k, v in st2(sim).items()})
# 3) vadeli: KCHOL ve XU030 sürekli vadeli
fk, fx = cont('KCHOL'), cont('XU030')
FK, FX = fk.reindex(cal), fx.reindex(cal)
print('vadeli kapsam', fk.index.min().date(), ' corr(vadeli,spot) KCHOL', FK['r'].corr(K['cc']).round(3), ' XU030', FX['r'].corr(X['cc']).round(3))
cf = FK['r'] - bm * FX['r']; gf = FK['ro_gap'] - bm * FX['ro_gap']; inf_ = FK['ro_in'] - bm * FX['ro_in']
pers = (('2017-20', '2017-06-01', SPLIT), ('2021-26', SPLIT, '2027-01-01'), ('2023-26', '2023-01-01', '2027-01-01'))
for lab, entry, g_, i_, c_ in [('vadeli uzlaşma t (iyimser)', 'close0', gf, inf_, cf), ('vadeli uzlaşma t+1', 'close1', gf, inf_, cf), ('vadeli ilk işlem t+1', 'open', gf, inf_, cf), ('spot açılış t+1 (karş.)', 'open', tg, ti, tc)]:
    for c in [8, 15, 30]:
        print(f'{lab:28s} {c:2d}bps', {k: round(v, 2) for k, v in st2(simulate(pos, g_, i_, c_, lw, entry, c), pers).items()})
v = FK['value_tl'] / 1e6; print('KCHOL vadeli medyan günlük hacim (mn TL):', v.groupby(v.index.year).median().dropna().round(1).to_dict())
# 4) SAHOL/AKBNK: yoğunlaşma ve 2026 hariç
exec(open(HERE + '/03_ratio_alt.py').read().split("if __name__ == '__main__':")[0])
P = pair('SAHOL', 'AKBNK'); o, sim, pos2 = run(P, 60, 1.5)
print('SAHOL/AKBNK 2021-2025 (2026 hariç):', {k: round(v, 2) for k, v in st2(sim, (('2021-25', SPLIT, '2026-01-01'), ('2026', '2026-01-01', '2027-01-01'), ('2014-17', '2014-01-01', '2018-01-01'), ('2018-20', '2018-01-01', SPLIT))).items()})
# işlem bazında pnl
p1 = sim['p1']; tid = ((p1 != 0) & (p1 != p1.shift(1).fillna(0))).cumsum()
# çıkış günü gap'ini son işleme ata
tid = tid.where(sim['expo'], np.nan); tid = tid.where(p1 != 0, tid.shift(1))
tr = sim[sim.expo].groupby(tid[sim.expo])['pnl'].sum()
tr.index = [sim[sim.expo].index[(tid[sim.expo] == i).values][0] for i in tr.index]
for per, lo, hi in [('IS', '2014-01-01', SPLIT), ('OOS', SPLIT, '2027-01-01')]:
    t = tr[(tr.index >= lo) & (tr.index < hi)]
    top5 = t.sort_values(ascending=False).head(5).sum()
    print(per, f'işlem sayısı {len(t)}, işlem başı ort {1e4*t.mean():.1f} bps, isabet {(t>0).mean():.2f}, toplam {1e4*t.sum():.0f} bps, en iyi 5 işlem payı {100*top5/t.sum():.0f}%, en iyi 5 hariç işlem başı {1e4*t.sort_values(ascending=False).iloc[5:].mean():.1f} bps, medyan {1e4*t.median():.1f}')
# NAV yıllık (temel, açılış, 8 bps) ve SAHOL/AKBNK yıllık (temel)
print('NAV yıllık bps/aktif gün:', by_year(simulate(pos, tg, ti, tc, lw, 'open', 8)).loc[2014:].to_dict())
print('SAHOL/AKBNK yıllık bps/aktif gün:', by_year(sim).loc[2014:].to_dict())
