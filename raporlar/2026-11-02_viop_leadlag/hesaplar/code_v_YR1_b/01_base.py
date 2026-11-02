"""Temel tekrar + alt dönemler + yıllık + işlem profili + uç değer bağımlılığı (SAHOL/AKBNK z60>1,5, β250)."""
import vb, numpy as np, pandas as pd
pd.set_option('display.width', 250)
P = vb.pair_inputs('SAHOL', 'AKBNK')
z = vb.zscore(P['S'], 60); pos = vb.positions(z, 1.5)
A, B, beta = P['A'], P['B'], P['beta']
res = {}
for c in [0, 8, 15, 30]:
    df = vb.pnl_open(pos, A['gap'], A['intra'], B['gap'], B['intra'], beta, c)
    res[c] = df
    print(f'--- maliyet {c} bps (bacak başına gidiş-dönüş; nominal ağırlıklı) ---'); print(vb.table(df).round(3).to_string())
df = res[8]
# kaynağın muhasebesi (p1!=0 günleri) karşılaştırma
for lab, lo, hi in [('IS', '2014', '2021'), ('OOS', '2021', '2027')]:
    x = df[(df.index >= lo) & (df.index < hi)]; m = x[x.Pi != 0]['net'].mean() * 1e4
    print(lab, 'kaynak muhasebesi (Pi!=0 ort.):', round(m, 1), '| doğru (maruz gün):', round(x[x.exp]['net'].mean() * 1e4, 1))
# yıllık
e = df[df.exp & (df.index >= '2014')]
yr = (e['net'].groupby(e.index.year).agg(['mean', 'count'])); yr['mean'] *= 1e4
print('yıllık bps/maruz gün:', yr['mean'].round(1).to_dict()); print('pozitif yıl', (yr['mean'] > 0).sum(), '/', len(yr))
# işlem profili
T = vb.trades(df[df.index >= '2014-01-01'])
T['yr'] = pd.DatetimeIndex(T.entry).year
for lab, m in [('IS', T.yr < 2021), ('OOS', T.yr >= 2021)]:
    t = T[m]; print(lab, 'işlem', len(t), 'ort net bps', round(1e4 * t.net.mean(), 1), 'medyan', round(1e4 * t.net.median(), 1), 'isabet', round((t.net > 0).mean(), 3), 'ort gün', round(t.ndays.mean(), 2),
                    'trade-t', round(t.net.mean() / t.net.std() * np.sqrt(len(t)), 2))
# uç değer: en iyi k işlemi çıkar
for lab, lo, hi in [('IS', 2014, 2021), ('OOS', 2021, 2027)]:
    t = T[(T.yr >= lo) & (T.yr < hi)].sort_values('net', ascending=False)
    tot = t.net.sum()
    for k in [0, 1, 3, 5, 10]:
        r = t.iloc[k:]; print(lab, f'en iyi {k} işlem hariç: toplam pay {r.net.sum() / tot:.2f}, ort {1e4 * r.net.mean():.1f} bps, trade-t {r.net.mean() / r.net.std() * np.sqrt(len(r)):.2f}')
    print(lab, 'en iyi 5 işlem:', [(str(a.date()), round(1e4 * b)) for a, b in zip(t.entry[:5], t.net[:5])])
    print(lab, 'en kötü 5 işlem:', [(str(a.date()), round(1e4 * b)) for a, b in zip(t.entry[-5:], t.net[-5:])])
# günlük winsorize
for q in [0.01, 0.025]:
    d2 = df.copy(); x = d2.loc[d2.exp & (d2.index >= '2014'), 'net']; lo, hi = x.quantile(q), x.quantile(1 - q)
    d2['net'] = d2['net'].clip(lo, hi).where(d2.exp, d2['net'])
    print(f'winsor {q}:'); print(vb.table(d2).loc[['IS', 'OOS', '2021-23', '2024-26'], ['bps', 't']].round(2).to_string())
# kriz pencerelerini çıkar
CR = [('2018-08-01', '2018-09-30'), ('2020-03-01', '2020-04-30'), ('2021-11-15', '2022-01-31'), ('2023-02-06', '2023-03-15'), ('2023-05-01', '2023-06-30'), ('2025-03-17', '2025-04-30'), ('2026-09-01', '2026-10-31')]
d3 = df.copy(); m = pd.Series(False, index=d3.index)
for a, b in CR: m |= (d3.index >= a) & (d3.index <= b)
d3.loc[m, ['net', 'gross', 'cost']] = 0; d3.loc[m, 'exp'] = False; d3.loc[m, 'valid'] = False
print('kriz pencereleri hariç:'); print(vb.table(d3).round(2).to_string())
d4 = df[df.index < '2026-01-01']; print('2026 hariç OOS:', vb.summ(d4, '2021', '2026'))
pd.concat({c: res[c]['net'] for c in res}, axis=1).to_parquet('res_base_pnl.parquet')
df.to_parquet('res_base_df8.parquet')
T.to_csv('res_base_trades.csv', index=False)
