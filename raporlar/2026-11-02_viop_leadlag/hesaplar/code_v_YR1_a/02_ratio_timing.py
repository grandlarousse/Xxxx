"""YR1-A zamanlama: giriş anı alternatifleri, işlem günü ayrıştırması, 10:30 girişi (h1, 2023-12+), tik maliyeti."""
import sys; sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_YR1_a')
from vlib import *
A, B = 'SAHOL', 'AKBNK'
da, db = dec(A), dec(B)
idx = da.index.union(db.index); idx = idx[idx >= pd.Timestamp('2010-01-01')]
da, db = da.reindex(idx), db.reindex(idx)
beta = roll_beta(da['cc'], db['cc'])
S = (da['cc'] - beta * db['cc']).fillna(0).cumsum()
g = da['gap'] - beta * db['gap']; i = da['intra'] - beta * db['intra']; c = da['cc'] - beta * db['cc']
lw = 1 + beta.abs()
tick = 1e4 * (0.01 / da['px'] + beta.abs() * 0.01 / db['px'])  # 1 tik gidiş-dönüş, iki bacak
rows = []
def rec(lab, sim, lo='2014-01-01'):
    r = dict(lab=lab)
    for per, l, h in [('IS', lo, SPLIT), ('OOS', SPLIT, '2027-01-01'), ('H1win', '2023-12-01', '2027-01-01')]:
        st = summarize(sim, l, h)
        r[f'{per}_mean'] = st['mean_bps']; r[f'{per}_t'] = st['t_all']; r[f'{per}_n'] = st['n_act']; r[f'{per}_sh'] = st['sharpe']; r[f'{per}_ann%'] = st['ann_pct']
    yb = by_year(sim[sim.index >= lo]); r['yrs_pos'] = f'{int((yb > 0).sum())}/{len(yb)}'; r['by_year'] = yb.to_dict(); rows.append(r)
print('ortalama tik maliyeti (bps, gidiş-dönüş iki bacak) yıllara göre:', tick.groupby(tick.index.year).mean().loc[2014:].round(1).to_dict())
for thr, w in [(1.5, 60)]:
    z = zscore(S, w); pos = positions(z, thr)
    for entry in ['close0', 'open', 'close1']:
        for cost in [8, 15, 30]:
            rec(f'{entry} {cost}bps', simulate(pos, g, i, c, lw, entry, cost))
        rec(f'{entry} 8bps+tik', simulate(pos, g, i, c, lw, entry, 8, tick))
        rec(f'{entry} 15bps+tik', simulate(pos, g, i, c, lw, entry, 15, tick))
    # 2 gün gecikme (t+2 kapanışı)
    rec('close2 (t+2 kapanış) 8bps', simulate(pos.shift(1), g, i, c, lw, 'close1', 8))
    # 10:30 girişi: gap' = log(p1030_t / c_{t-1}), intra' = log(c_t / p1030_t), yalnız h1 dönemi
    pa, pb = h1_px(A), h1_px(B)
    ia = np.log(raw(A)['c'] / pa.reindex(raw(A).index)).reindex(idx); ib = np.log(raw(B)['c'] / pb.reindex(raw(B).index)).reindex(idx)
    i2 = ia - beta * ib; g2 = c - i2
    m = i2.notna()
    for cost in [0, 8, 15]:
        s1030 = simulate(pos, g2.where(m), i2.where(m), c, lw, 'open', cost); s1030 = s1030[s1030.index >= '2023-12-01']
        sop = simulate(pos, g.where(m), i.where(m), c, lw, 'open', cost); sop = sop[sop.index >= '2023-12-01']
        for lab, ss in [('10:30 girişi', s1030), ('açılış (aynı günler)', sop)]:
            st = summarize(ss, '2023-12-01', '2027-01-01'); rows.append(dict(lab=f'{lab} {cost}bps [2023-12..2026-10]', H1win_mean=st['mean_bps'], H1win_t=st['t_all'], H1win_n=st['n_act'], H1win_sh=st['sharpe']))
    # işlem gününe göre ayrıştırma (açılış girişi, brüt)
    sim = simulate(pos, g, i, c, lw, 'open', 0)
    p1 = sim['p1']; newtr = (p1 != 0) & (p1 != p1.shift(1).fillna(0))
    k = np.zeros(len(p1)); cnt = 0
    for j, (nt, v) in enumerate(zip(newtr.values, p1.values)):
        cnt = 1 if nt else (cnt + 1 if v != 0 else 0); k[j] = cnt
    sim['k'] = k
    # çıkış günü (p1==0, p2!=0) -> sadece gap
    exitd = (p1 == 0) & (pos.reindex(sim.index).shift(2).fillna(0) != 0)
    sim.loc[exitd, 'k'] = -1
    for per, lo, hi in [('IS', '2014-01-01', SPLIT), ('OOS', SPLIT, '2027-01-01')]:
        ss = sim[(sim.index >= lo) & (sim.index < hi)]
        t = ss[ss.expo].groupby(np.clip(ss.loc[ss.expo, 'k'], -1, 6))['gross'].agg(['count', 'mean', 'sum'])
        t['mean'] *= 1e4; t['sum'] *= 1e4; t['pay_%'] = 100 * t['sum'] / t['sum'].sum()
        # giriş gününün gün-içi parçası vs sonraki gap
        print(per, 'brüt pnl işlem gününe göre (k=1: giriş günü gün-içi [açılış->kapanış], k>=2: gap+gün-içi, -1: çıkış günü gap):'); print(t.round(1).to_string())
pd.set_option('display.width', 250)
D = pd.DataFrame(rows); D.to_csv(HERE + '/res_ratio_timing.csv', index=False)
print(D.drop(columns=['by_year']).round(2).to_string())
for r in rows:
    if 'by_year' in r and isinstance(r['by_year'], dict) and r['lab'].endswith(' 8bps'): print(r['lab'], r['by_year'])
