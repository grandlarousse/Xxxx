"""Ek: temettü günleri çevresi pnl, 2024-25 (2026 hariç), ızgara medyan bps, yanlış eşik duyarlılığı (limit günleri S'den çıkarılırsa)."""
import vb, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
P = vb.pair_inputs('SAHOL', 'AKBNK'); A, B, beta = P['A'], P['B'], P['beta']; z = vb.zscore(P['S'], 60); pos = vb.positions(z, 1.5)
df = vb.pnl_open(pos, A['gap'], A['intra'], B['gap'], B['intra'], beta, 8)
ex = pd.Series(False, index=df.index)
for s in ['SAHOL', 'AKBNK']:
    d = vb.load(s).reindex(df.index); rc = np.log(d['c'] / d['c'].ffill().shift()); dd = (d['cc'] - rc).abs() > 0.005
    for t in d.index[dd & (d.index >= '2014')]:
        i = df.index.get_loc(t); ex.iloc[max(0, i - 2): i + 6] = True
d2 = df.copy(); d2.loc[ex, 'net'] = 0
print('temettü günleri [-2,+5] penceresi sıfırlanınca:', vb.table(d2).loc[['IS', 'OOS'], ['bps', 't']].round(2).to_dict(), ' pencere gün sayısı', int(ex.sum()))
print('2024-25:', {k: round(v, 2) for k, v in vb.summ(df, '2024-01-01', '2026-01-01').items()}, ' 2026:', {k: round(v, 2) for k, v in vb.summ(df, '2026-01-01', '2027-01-01').items()})
g = pd.read_csv('res_grid_sahol.csv'); print('105 spes. OOS bps medyan', g.OOS_bps.median().round(1), ' IS bps medyan', g.IS_bps.median().round(1), ' OOS bps çeyrekler', g.OOS_bps.quantile([.25, .75]).round(1).to_dict())
# Yıllık t (8 bps)
rows = {}
for y in range(2014, 2027):
    s = vb.summ(df, f'{y}-01-01', f'{y + 1}-01-01'); rows[y] = (round(s['bps'], 1), round(s['t'], 2))
print('yıl (bps, t):', rows)
