"""YR1-A: SAHOL/AKBNK oran ortalamaya dönüş — bağımsız yeniden üretim."""
import sys; sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_YR1_a')
from vlib import *
A, B = 'SAHOL', 'AKBNK'
da, db = dec(A), dec(B)
idx = da.index.union(db.index); idx = idx[idx >= pd.Timestamp('2010-01-01')]
da, db = da.reindex(idx), db.reindex(idx)
beta = roll_beta(da['cc'], db['cc'])
s = da['cc'] - beta * db['cc']; S = s.fillna(0).cumsum()
g = da['gap'] - beta * db['gap']; i = da['intra'] - beta * db['intra']; c = da['cc'] - beta * db['cc']
lw = 1 + beta.abs()
rows = []
def rec(lab, sim, act='expo', **kw):
    r = dict(lab=lab, **kw)
    for per, lo, hi in [('IS', '2014-01-01', SPLIT), ('OOS', SPLIT, '2027-01-01')]:
        st = summarize(sim, lo, hi, active=act)
        for k, v in st.items(): r[f'{per}_{k}'] = v
    yb = by_year(sim[sim.index >= '2014-01-01'], active=act); r['yrs_pos'] = f'{int((yb > 0).sum())}/{len(yb)}'; r['by_year'] = yb.to_dict()
    rows.append(r); return r
z60 = zscore(S, 60)
pos = positions(z60, 1.5)
# (0) kaynak muhasebesi taklidi: legs=2 sabit, aktif = p1!=0
sim0 = simulate(pos, g, i, c, pd.Series(2.0, index=idx), 'open', 8)
rec('kaynak-taklit (aktif=p1, legs=2, 8bps)', sim0, act='act_p1')
for cost in [0, 8, 15, 30]:
    sim = simulate(pos, g, i, c, lw, 'open', cost)
    rec(f'açılış girişi, expo-muhasebe, {cost}bps', sim, cost=cost)
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 200)
D = pd.DataFrame(rows)
cols = ['lab'] + [f'{p}_{k}' for p in ['IS', 'OOS'] for k in ['n_act', 'mean_bps', 't_act', 't_all', 'gross_bps', 'cost_bps', 'sharpe', 'entries', 'hold_d', 'pct_in']] + ['yrs_pos']
print(D[cols].round(2).T.to_string())
for r in rows[:2]: print(r['lab'], r['by_year'])
