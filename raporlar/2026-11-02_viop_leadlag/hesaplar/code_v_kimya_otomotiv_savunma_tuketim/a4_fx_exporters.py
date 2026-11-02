"""A4 — O4: USDTRY_{t-1} -> ihracatçı (FROTO, TOASO, ARCLK, VESTL) gün-içi. Ham (kaydırılmamış) vs düzeltilmiş Yahoo FX.
fx_timing_check.py: Yahoo c(t) = 00:00 UTC t fiyatı => ham r_raw(t) = UTC günü t-1 ; düzeltilmiş r_fix(t) = UTC günü t (BIST seansı t'yi İÇERİR).
Dolayısıyla: r_fix(t-1) ≈ r_raw(t) [UTC günü t-1, BIST t açılışından ÖNCE biter -> işlenebilir]; r_fix(t) = look-ahead (aynı gün)."""
import sys; sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_kimya_otomotiv_savunma_tuketim')
from vk import *
EXP = ['FROTO', 'TOASO', 'ARCLK', 'VESTL']
IB = pd.concat([decomp(s)['intra'] for s in EXP], axis=1).mean(axis=1)
GB = pd.concat([decomp(s)['gap'] for s in EXP], axis=1).mean(axis=1)
MI = decomp('XU100')['intra']; MG = decomp('XU100')['gap']
Uf = ret('TRY=X'); Ur = ret('TRY=X', fx_raw=True)
print('kontrol: corr(r_fix(t-1), r_raw(t)) =', round(pd.concat([Uf.shift(1), Ur], axis=1).dropna().corr().iloc[0, 1], 4))
cases = {'FIX lag0 (UTC t; LOOK-AHEAD)': Uf, 'FIX lag1 (UTC t-1; işlenebilir)': Uf.shift(1), 'FIX lag2 (UTC t-2)': Uf.shift(2),
         'RAW lag0 (=UTC t-1)': Ur, 'RAW lag1 (=UTC t-2)': Ur.shift(1), 'RAW lead -1 (=UTC t)': Ur.shift(-1)}
for lab, x in cases.items():
    out = []
    for nm, (s, e) in {'2014+': ('2014-01-01', None), 'IS': IS_, 'OOS': OOS_}.items():
        b, t = np.nan, np.nan
        df = pd.concat([IB.rename('y'), x.rename('x')], axis=1).dropna(); df = df[df.index >= pd.Timestamp(s)]
        if e: df = df[df.index <= pd.Timestamp(e)]
        b, t = nw_se_slope(df.y.values, df.x.values)
        pc = pcorr(IB, x, [MI], s, e)
        out.append(f'{nm}: b {b:.3f} t {t:.1f} | pc|XU100intra {pc[0]:.3f} (t {pc[1]:.1f})')
    g = pcorr(GB, x, [], '2014-01-01', None)
    print(f'{lab:34s} -> ihracatçı intra: ' + ' || '.join(out) + f' || gap corr {g[0]:.3f} (t {g[1]:.1f})')
print('\nBacktest sign(USDTRY sinyali) * ihracatçı intra, 8 bps:')
for lab in ['FIX lag1 (UTC t-1; işlenebilir)', 'RAW lag1 (=UTC t-2)', 'FIX lag0 (UTC t; LOOK-AHEAD)']:
    x = cases[lab]
    for s, e in [IS_, OOS_]:
        n, m, t, sh = bt_sign(x, IB, 8, 0, s, e); print(f'  {lab:34s} {s[:4]}-{e[:4]}: n {n} ort {m:.1f} bps t {t:.2f} Sh {sh:.2f}')
print('\nTekil hisseler, FIX lag1 vs RAW lag1 vs FIX lag0 -> intra (2014+, NW t):')
for s in EXP + ['DOAS', 'XU100']:
    y = decomp(s)['intra']; r = []
    for lab in ['FIX lag1 (UTC t-1; işlenebilir)', 'RAW lag1 (=UTC t-2)', 'FIX lag0 (UTC t; LOOK-AHEAD)']:
        df = pd.concat([y.rename('y'), cases[lab].rename('x')], axis=1).dropna(); df = df[df.index >= '2014-01-01']
        b, t = nw_se_slope(df.y.values, df.x.values); r.append(f'{lab.split(" (")[0]}: t {t:.1f}')
    print(' ', s, ' | '.join(r))

print('\nEk: FIX lag2 (UTC t-2) -> ihracatçı - XU100 göreli gün-içi (eski "ham lag1" ile aynı bilgi) ve yıllık işaret:')
REL = IB - MI
for s, e in [IS_, OOS_]:
    for c in (0, 16):
        n, m, t, sh = bt_sign(Uf.shift(2), REL, c, 0, s, e); print(f'  {s[:4]}-{e[:4]} maliyet {c} (iki bacak): n {n} ort {m:.2f} bps t {t:.2f} Sh {sh:.2f}')
yy = []
for y in range(2014, 2027):
    pc = pcorr(IB, Uf.shift(2), [MI], f'{y}-01-01', f'{y}-12-31'); yy.append(f'{y}:{pc[0]:+.2f}')
print('  yıllık pc|XU100intra:', ' '.join(yy))
