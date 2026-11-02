"""Veri/zamanlama denetimi: (1) Yahoo günlük açılış = açılış müzayedesi mi? (2) açılış kalitesi yıllara göre
(3) Yahoo FX günlük kapanış saati yıllara göre (FXE / TUR ile korelasyon) ve geçiş tarihi."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vlib as V, numpy as np, pandas as pd
pd.set_option('display.width', 250)

print('=== (1) Günlük açılış vs m5/h1 ===')
for s in ['KCHOL', 'ENKAI', 'TUPRS', 'FROTO', 'YKBNK', 'ARCLK', 'TOASO', 'AYGAZ', 'OTKAR', 'TTRAK', 'XU100', 'XU030']:
    d = V.raw(s + '.IS'); m = V.raw(s + '.IS', 'm5').copy(); h = V.raw(s + '.IS', 'h1').copy()
    m['d'] = m.index.tz_convert(None).normalize(); h['d'] = h.index.tz_convert(None).normalize()
    m655 = m[(m.index.hour == 6) & (m.index.minute == 55)].set_index('d')['c']
    m700 = m[(m.index.hour == 7) & (m.index.minute == 0)].set_index('d')['o']
    h1o = h.groupby('d')['o'].first()
    j = pd.concat([d['o'].rename('Do'), m655.rename('m655'), m700.rename('m700o'), h1o.rename('h1o')], axis=1)
    a = j.dropna(subset=['m655']); b = j.dropna(subset=['h1o', 'Do'])
    print(f"{s:6s} Do==m5 06:55 müzayede: {np.isclose(a.Do, a.m655, rtol=1e-4).mean():.2f} (n={len(a)}); "
          f"Do==m5 07:00 açılış: {np.isclose(a.Do, a.m700o, rtol=1e-4).mean():.2f}; Do==h1 ilk bar o: {np.isclose(b.Do, b.h1o, rtol=1e-4).mean():.2f} (n={len(b)})")

print('\n=== (2) Açılış kalitesi: o==c (aynı gün) ve o==önceki c oranı, yıllara göre ===')
R = {}
for s in ['KCHOL', 'ENKAI', 'TUPRS', 'FROTO', 'YKBNK', 'ARCLK', 'TOASO', 'AYGAZ', 'OTKAR', 'TTRAK']:
    D = V.decomp(s)
    D = D[D['cc'].notna()]
    R[s + ' o=c'] = D['f_oc'].astype(float).groupby(D.index.year).mean()
    R[s + ' o=pc'] = D['f_opc'].astype(float).groupby(D.index.year).mean()
print(pd.DataFrame(R).loc[2012:].round(2).T.to_string())

print('\n=== (3) Yahoo FX günlük kapanış zamanı: corr(ref_t, FXraw[ldate t]) (k=0) vs FXraw[ldate t+1] (k=1) ===')
def fxchk(fxsym, ref, field='adj'):
    fx = V.raw(fxsym)['c']; r = V.raw(ref); rr = np.log(r[field]).diff(); cal = r.index
    out = {}
    for k in [0, 1]:
        idx = np.clip(fx.index.searchsorted(cal + pd.Timedelta(days=k), side='left'), 0, len(fx) - 1)
        f = np.log(pd.Series(fx.values[idx], index=cal)).diff()
        df = pd.concat([rr.rename('x'), f.rename('f')], axis=1).dropna()
        out[k] = df.groupby(df.index.year).apply(lambda g: g.x.corr(g.f))
        out[f'roll{k}'] = df['x'].rolling(60).corr(df['f'])
    return out
o = fxchk('EURUSD=X', 'FXE')
print('EURUSD=X vs FXE'); print(pd.DataFrame({0: o[0], 1: o[1]}).round(2).T.to_string())
r0, r1 = o['roll0'], o['roll1']
sw = (r1 > r0).loc['2009':'2012']
print('60g kayan korelasyonda k=1 > k=0 ilk kalıcı geçiş:', sw[sw.rolling(40).mean() > 0.95].index.min())
o = fxchk('TRY=X', 'TUR')
print('TRY=X vs TUR'); print(pd.DataFrame({0: o[0], 1: o[1]}).round(2).T.to_string())
o = fxchk('TRY=X', 'XU100.IS')
print('TRY=X vs XU100'); print(pd.DataFrame({0: o[0], 1: o[1]}).round(2).T.to_string())

print('\n=== (4) h1 ile TRY=X günlük c saati (2024+): |ln(c_daily/h1 fiyatı)| medyan, bps ===')
d = V.raw('TRY=X'); h = V.raw('TRY=X', 'h1')
hc = pd.Series(h['c'].values, index=h.index + pd.Timedelta(hours=1))
for off in [-9, -6, -3, -1, 0, 1, 3, 6, 9, 15, 21, 24]:
    t = pd.DatetimeIndex(d.index).tz_localize('UTC') + pd.Timedelta(hours=off)
    pos = hc.index.searchsorted(t, side='right') - 1; ok = pos >= 0
    v = hc.values[np.clip(pos, 0, None)]
    age = (t - hc.index[np.clip(pos, 0, None)])
    x = pd.Series(np.abs(np.log(d['c'].values / v)), index=d.index)[ok & (age < pd.Timedelta(hours=2))]
    x = x[x.index >= '2024-02-01']
    print(f'  ldate 00:00 {off:+d}h: medyan {1e4 * x.median():.2f} bps, ortalama {1e4 * x.mean():.2f} (n={len(x)})')

print('\n=== (5) TUR hizası: TUR_{t-1} (ABD tarihi < t) örnek ===')
p, s = V.us_prev('TUR')
print(pd.concat([p.rename('TUR_prev'), s.rename('TUR_same')], axis=1).dropna().tail(5))
