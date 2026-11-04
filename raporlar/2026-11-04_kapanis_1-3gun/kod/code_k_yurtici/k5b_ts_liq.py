"""(e) ek: hisse bazında zaman serisi baz sapması (tek bacak) — likidite ve dönem filtreleriyle (bayat kapanış/teorik uzlaşma riskine karşı)."""
from klib import *
C = ctx(); vcal = C['vcal']
B = pd.read_parquet(S + '/out/code_y_viop/results/basis_panel.parquet'); B['date'] = pd.to_datetime(B['date'])
B = B[B.und.isin(VIOP47)].sort_values(['und', 'date'])
TR = C['c1_trades'].stack().reset_index(); TR.columns = ['date', 'und', 'tr']
L = pd.read_csv(S + '/out/y_viop_likidite.csv')[['und', 'liq_class']]
B = B.merge(TR, on=['date', 'und'], how='left').merge(L, on='und', how='left')
out = []
for sig, entry in [('anom_close_dev', 'E1'), ('anom_dev', 'E0')]:
    d = B[['date', 'und', sig, 'tr', 'liq_class']].dropna(subset=[sig]).copy()
    d['z'] = d[sig] / d.groupby('und')[sig].transform(lambda x: x.rolling(120, min_periods=60).std().shift(1))
    for thr in [1.5, 2.5]:
        for lab, m in [('tümü', lambda e: e.tr >= 0), ('işlem>=1000', lambda e: e.tr >= 1000), ('A sınıfı', lambda e: e.liq_class == 'A'),
                       ('A sınıfı + 2022-09-23 sonrası', lambda e: (e.liq_class == 'A') & (e.date >= '2022-09-23')), ('işlem>=3000 + 2022-09-23 sonrası', lambda e: (e.tr >= 3000) & (e.date >= '2022-09-23'))]:
            e = d[(d.z.abs() > thr)].copy(); e = e[m(e)]; e['side'] = -np.sign(e.z)
            for h in [1, 3]:
                for ent in [entry, 'E2']:
                    ee = e.copy()
                    if ent == 'E2': ee['date'] = shift_date(ee['date'], 1, vcal); en = 'E0'
                    else: en = ent
                    ee = ee.dropna(subset=['date']); ee['ret'] = vectorized_fut(ee, h, en)
                    st = trade_stats(ee, 'ret', h=h, is_end=V_IS_END)
                    reg('e3_ts_liq', f'TS hisse {sig} |z|>{thr} [{lab}]', 'VIOP', ent, h, st, dict(sig=sig, thr=thr))
                    out.append(f'TS {sig:14s} |z|>{thr} [{lab:32s}] {ent} h{h} {fmt(st)}')
for o in out: print(o)
D = save_registry('e3_ts_liq'); print('test sayısı', len(D))
