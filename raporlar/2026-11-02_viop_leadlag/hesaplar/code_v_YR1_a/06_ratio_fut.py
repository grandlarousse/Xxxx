"""YR1-A VİOP vadeli fiyatlarıyla (2017-03+) backtest: sinyal spot kapanıştan; giriş uzlaşma t (iyimser), uzlaşma t+1 (muhafazakâr), vadeli ilk işlem t+1."""
import sys; sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_YR1_a')
from vlib import *; from fut import cont
exec(open(HERE + '/03_ratio_alt.py').read().split("if __name__ == '__main__':")[0])
P = pair('SAHOL', 'AKBNK')
fa, fb = cont('SAHOL'), cont('AKBNK')
print('vadeli kapsamı', fa.index.min().date(), fa.index.max().date(), len(fa), len(fb))
idx = P['idx']; beta = P['beta']
FA, FB = fa.reindex(idx), fb.reindex(idx)
# vadeli-spot getiri korelasyonu (kontrol)
print('corr(vadeli r, spot cc): SAHOL', FA['r'].corr(P['da']['cc']).round(3), ' AKBNK', FB['r'].corr(P['db']['cc']).round(3))
c_f = FA['r'] - beta * FB['r']; g_f = FA['ro_gap'] - beta * FB['ro_gap']; i_f = FA['ro_in'] - beta * FB['ro_in']
z = zscore(P['S'], 60); pos = positions(z, 1.5)
# vadeli fiyatlardan kendi sinyali
Sf = c_f.fillna(0).cumsum(); zf = zscore(Sf, 60); posf = positions(zf, 1.5)
rows = []
lo0 = '2017-06-01'
for lab, ps, entry, g, i, c in [('spot sinyal, uzlaşma t girişi (iyimser)', pos, 'close0', g_f, i_f, c_f),
                                ('spot sinyal, uzlaşma t+1 girişi', pos, 'close1', g_f, i_f, c_f),
                                ('spot sinyal, vadeli ilk işlem t+1', pos, 'open', g_f, i_f, c_f),
                                ('vadeli sinyal, uzlaşma t+1 girişi', posf, 'close1', g_f, i_f, c_f),
                                ('KARŞILAŞTIRMA spot, açılış t+1', pos, 'open', P['g'], P['i'], P['c'])]:
    for cost in [8, 15, 30]:
        sim = simulate(ps, g, i, c, P['lw'], entry, cost)
        o = dict(lab=lab, cost=cost)
        for per, l, h in [('2017-20', lo0, SPLIT), ('2021-26', SPLIT, '2027-01-01'), ('2023-26', '2023-01-01', '2027-01-01')]:
            st = summarize(sim, l, h); o[f'{per}_m'] = st['mean_bps']; o[f'{per}_t'] = st['t_all']; o[f'{per}_n'] = st['n_act']
        yb = by_year(sim[sim.index >= lo0]); o['yrs'] = f'{int((yb > 0).sum())}/{len(yb)}'
        if cost == 8: o['by_year'] = yb.to_dict()
        rows.append(o)
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 150)
D = pd.DataFrame(rows); print(D.drop(columns=['by_year']).round(2).to_string())
for r in rows:
    if r['cost'] == 8: print(r['lab'], r['by_year'])
# likidite: sinyal günlerinde seçilen kontratın günlük TL hacmi
for nm, F in [('SAHOL', FA), ('AKBNK', FB)]:
    v = F['value_tl'] / 1e6
    print(nm, 'medyan günlük vadeli hacim (mn TL, seçilen kontrat) yıl:', v.groupby(v.index.year).median().round(1).to_dict())
