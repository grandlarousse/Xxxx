"""(e) VİOP baz anomalisi -> uzlaşma_t -> uzlaşma_{t+h} (kapanıştan kapanışa).
Girdi: out/code_y_viop/results/basis_panel.parquet (b_L = ln(F_uzlaşma/S_kapanış), b_L_close = ln(F_kapanış/S_kapanış), b* = r·τ − temettü,
anom_dev = (b − b*) − kendi 60g medyanı (t−1'e kadar)). Ek sinyaller: Δb = b_t − b_{t−1}; b − medyan5(b) (taşıma gürültüsüne dayanıklı).
Hipotez: pahalı vadeli (pozitif sapma) ertesi gün ucuzlar (yön −sign).
Uygulama: (i) 47 pay vadelisi kesitsel L/S (üst %20 sat, alt %20 al), (ii) hisse bazında zaman serisi |z|>thr, (iii) XU030 vadelisi zaman serisi.
Giriş: E0 uzlaşma_t; E1 vadeli son işlem_t (XU030'da 18:15, spot kapanışından sonra -> sinyal tam bilinir); E2 uzlaşma_{t+1}.
Not: pay vadelisinde 23.09.2022'den beri seans 18:10'da, spot müzayedesiyle aynı anda bitiyor -> E0/E1 sinyali o an tam bilinmez (sınırda)."""
from klib import *
C = ctx(); vcal = C['vcal']
B = pd.read_parquet(S + '/out/code_y_viop/results/basis_panel.parquet')
B['date'] = pd.to_datetime(B['date'])
B = B[B.und.isin(VIOP47 + ['XU030'])].sort_values(['und', 'date'])
g = B.groupby('und')
# DÜZELTME: Δb yalnız aynı sözleşmede (L sözleşmesi değişince takvim yayılımı kadar sıçrar); dev5 taşıma-düzeltilmiş baz (b − b*) üzerinde
same = g['L_code'].shift(1) == B['L_code']
B['db'] = g['b_L'].diff().where(same)
B['db_c'] = g['b_L_close'].diff().where(same)
B['a_s'] = B['b_L'] - B['b_star']; B['a_c'] = B['b_L_close'] - B['b_star']
B['dev5'] = B['a_s'] - B.groupby('und')['a_s'].transform(lambda x: x.rolling(5, min_periods=3).median().shift(1))
B['dev5_c'] = B['a_c'] - B.groupby('und')['a_c'].transform(lambda x: x.rolling(5, min_periods=3).median().shift(1))
bad = (B['L_trades'] < 5) | (B['L_dte'] <= 1)
for c in ['db', 'db_c', 'dev5', 'dev5_c']: B.loc[bad | (B[c].abs() > 0.08), c] = np.nan
SIG = {'anom_dev': 'E0', 'dev5': 'E0', 'db': 'E0', 'anom_close_dev': 'E1', 'dev5_c': 'E1', 'db_c': 'E1'}
out = []
# (i) kesitsel L/S
def ls_series(sig, h, entry):
    d = B[B.und.isin(VIOP47)][['date', 'und', sig]].dropna().copy()
    d['n'] = d.groupby('date')[sig].transform('count'); d = d[d.n >= 15]
    d['r'] = d.groupby('date')[sig].rank(pct=True)
    d = d[(d.r >= 0.8) | (d.r <= 0.2)].copy()
    d['side'] = np.where(d.r >= 0.8, -1.0, 1.0)
    if entry == 'E2': d['date'] = shift_date(d['date'], 1, vcal); ent = 'E0'
    else: ent = entry
    d = d.dropna(subset=['date'])
    d['ret'] = vectorized_fut(d, h, ent)
    d = d.dropna(subset=['ret'])
    # günlük L/S: uzun ort − kısa ort (her bacak eşit ağırlık) -> tek "işlem" = bir gün
    L = d[d.side > 0].groupby('date')['ret'].mean(); Sx = d[d.side < 0].groupby('date')['ret'].mean()
    ls = (L + Sx).dropna() / 2  # ret yön uygulanmış: (uzun getirisi + kısa getirisi)/2 = sermaye başına (iki bacak toplam 1 birim)
    return pd.DataFrame({'date': ls.index, 'ret': ls.values})
for sig, e_nat in SIG.items():
    for h in [1, 2, 3, 5]:
        for entry in sorted({e_nat, 'E2'}):
            tr = ls_series(sig, h, entry)
            st = trade_stats(tr, 'ret', h=h, legs=1, is_end=V_IS_END)  # ret sermaye başına; maliyet bacak başına RT -> legs=1 (iki bacak/2 birim)
            reg('e_baz', f'L/S kesit {sig}', 'VIOP47_LS', entry, h, st, dict(sig=sig))
            out.append(f'L/S kesit {sig:15s} {entry} h{h} {fmt(st)}')
# (ii) hisse bazında zaman serisi (z = sinyal / kendi 120g std, t-1'e kadar)
for sig, e_nat in SIG.items():
    d = B[B.und.isin(VIOP47)][['date', 'und', sig]].dropna().copy()
    d['z'] = d[sig] / d.groupby('und')[sig].transform(lambda x: x.rolling(120, min_periods=60).std().shift(1))
    for thr in [1.5, 2.5]:
        e = d[d.z.abs() > thr].copy(); e['side'] = -np.sign(e.z)
        for h in [1, 2, 3]:
            for entry in sorted({e_nat, 'E2'}):
                ee = e.copy()
                if entry == 'E2': ee['date'] = shift_date(ee['date'], 1, vcal); ent = 'E0'
                else: ent = entry
                ee = ee.dropna(subset=['date']); ee['ret'] = vectorized_fut(ee, h, ent)
                st = trade_stats(ee, 'ret', h=h, is_end=V_IS_END)
                reg('e_baz', f'TS hisse {sig} |z|>{thr}', 'VIOP', entry, h, st, dict(sig=sig, thr=thr))
                out.append(f'TS hisse {sig:15s} |z|>{thr} {entry} h{h} {fmt(st)}')
# (iii) XU030 vadelisi
X = B[B.und == 'XU030'].copy()
for sig, e_nat in SIG.items():
    X['z'] = X[sig] / X[sig].rolling(120, min_periods=60).std().shift(1)
    for thr in [1.0, 1.5, 2.0]:
        e = X[X.z.abs() > thr][['date', 'und', 'z']].copy(); e['side'] = -np.sign(e.z)
        for h in [1, 2, 3]:
            for entry in sorted({e_nat, 'E2'}):
                ee = e.copy()
                if entry == 'E2': ee['date'] = shift_date(ee['date'], 1, vcal); ent = 'E0'
                else: ent = entry
                ee = ee.dropna(subset=['date']); ee['ret'] = vectorized_fut(ee, h, ent)
                st = trade_stats(ee, 'ret', h=h, is_end=V_IS_END, costs=[3, 8])
                st['net8'] = st['gross'] - 3; st['net15'] = st['gross'] - 8  # endeks vadelisi: 3 / 8 bps
                reg('e_baz', f'XU030 TS {sig} |z|>{thr}', 'XU030F', entry, h, st, dict(sig=sig, thr=thr))
                out.append(f'XU030 TS {sig:15s} |z|>{thr} {entry} h{h} [net=3/8bps] {fmt(st)}')
for o in out: print(o)
D = save_registry('e_baz'); print('test sayısı', len(D))

# ---- likidite / dönem sağlamlığı (bayat kapanış ve teorik uzlaşma riskine karşı) ----
out.clear()
TR = C['c1_trades']; TVv = C['tot_value']
TRl = TR.stack().rename('tr').reset_index().rename(columns={'level_0': 'date'}); TRl.columns = ['date', 'und', 'tr']
TVl = TVv.stack().rename('val').reset_index(); TVl.columns = ['date', 'und', 'val']
def ls_filtered(sig, h, entry, min_trades=0, after=None, top_value=None):
    d = B[B.und.isin(VIOP47)][['date', 'und', sig]].dropna().copy()
    d = d.merge(TRl, on=['date', 'und'], how='left').merge(TVl, on=['date', 'und'], how='left')
    d = d[d.tr >= min_trades]
    if top_value: d = d[d.groupby('date')['val'].rank(ascending=False) <= top_value]
    if after: d = d[d.date >= after]
    d['n'] = d.groupby('date')[sig].transform('count'); d = d[d.n >= (8 if top_value else 15)]
    d['r'] = d.groupby('date')[sig].rank(pct=True)
    d = d[(d.r >= 0.8) | (d.r <= 0.2)].copy(); d['side'] = np.where(d.r >= 0.8, -1.0, 1.0)
    if entry == 'E2': d['date'] = shift_date(d['date'], 1, vcal); ent = 'E0'
    else: ent = entry
    d = d.dropna(subset=['date']); d['ret'] = vectorized_fut(d, h, ent); d = d.dropna(subset=['ret'])
    L = d[d.side > 0].groupby('date')['ret'].mean(); Sx = d[d.side < 0].groupby('date')['ret'].mean()
    ls = (L + Sx).dropna() / 2
    return pd.DataFrame({'date': ls.index, 'ret': ls.values})
for lab, kw in [('işlem>=300', dict(min_trades=300)), ('işlem>=1000', dict(min_trades=1000)), ('hacimce ilk 15', dict(top_value=15)),
                ('2022-09-23 sonrası (18:10 seans sonu)', dict(after='2022-09-23')), ('2022-09-23 sonrası + ilk 15', dict(after='2022-09-23', top_value=15))]:
    for sig, entry in [('anom_close_dev', 'E1'), ('anom_dev', 'E0')]:
        for h in [1, 3]:
            tr = ls_filtered(sig, h, entry, **kw)
            st = trade_stats(tr, 'ret', h=h, is_end=V_IS_END)
            reg('e_baz', f'L/S kesit {sig} [{lab}]', 'VIOP47_LS', entry, h, st, dict(sig=sig))
            out.append(f'L/S {sig:15s} [{lab:36s}] {entry} h{h} {fmt(st)}')
for o in out: print(o)
D = save_registry('e_baz'); print('test sayısı', len(D))
