"""A2 — İddiaya özgü ek kontroller: başlangıç tarihi duyarlılığı (2005+ vs 2010+), yıllık pc, yarı örneklem (ASTOR),
15:00 UTC hizalı (h1) senkron, haftalık + STOXX kontrolü, ASELS–EU savunma rejim bölümü, ULKER–kakao lag/aylık, çimento ex-çift sepet."""
import sys; sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_kimya_otomotiv_savunma_tuketim')
from vk import *
M = ret('XU100'); U = ret('TRY=X'); E = ret('EEM'); STX = ret('^STOXX'); SPX = ret('^GSPC')
CF3 = [M, U, E, E.shift(1)]
EU_DEF = ['RHM.DE', 'BA.L', 'LDO.MI', 'HO.PA', 'SAAB-B.ST', 'KOG.OL', 'HAG.DE', 'R3NK.DE']
EUD = basket(EU_DEF, 3)
f = lambda x: f'{x:.3f}' if isinstance(x, (float, np.floating)) and not np.isnan(x) else str(x)
def P(*a): print(*[f(x) for x in a])

print('=== 1) Başlangıç duyarlılığı: pc|XU100 2005+ vs 2010+ vs 2014+ ===')
for a, b in [('GUBRF', 'BAGFS'), ('TKFEN', 'ENKAI'), ('CIMSA', 'AKCNS'), ('CIMSA', 'OYAKC'), ('SISE', 'XBANK'), ('AEFES', 'CCOLA'), ('TCELL', 'TKC')]:
    out = []
    for s in ['2005-01-01', '2010-01-01', '2014-01-01']:
        pc, t, n = pcorr(ret(a), ret(b), [M], s, None); out.append(f'{s[:4]}+: pc {pc:.3f} (t {t:.1f}, n {n})')
    pc, t, n = pcorr(ret(a), ret(b), [M], '2005-01-01', '2009-12-31'); out.append(f'2005-09: {pc:.3f}')
    print(a, b, ' | '.join(out))

print('\n=== 2) Yıllık pc|XU100 ===')
yrs = {}
for a, b in [('GUBRF', 'BAGFS'), ('TKFEN', 'ENKAI'), ('SISE', 'XBANK'), ('CIMSA', 'OYAKC'), ('CIMSA', 'AKCNS'), ('TOASO', 'EXV5.DE'), ('TOASO', 'STLAM.MI'), ('AEFES', 'CCOLA'), ('AEFES', 'CARL-B.CO'), ('AEFES', 'CCH.L'), ('ASTOR', 'EUPWR'), ('ASTOR', 'GESAN')]:
    _, _, v = years_sign(ret(a), ret(b), [M], y0=2010)
    yrs[f'{a}-{b}'] = v
Y = pd.DataFrame(yrs).T.round(2); print(Y.to_string())
_, _, v = years_sign(ret('ASELS'), EUD, [M], y0=2010); _, _, v2 = years_sign(ret('ASELS'), EUD, [M, STX], y0=2010)
print('ASELS-EU_DEF pc|XU100:', {k: round(x, 2) for k, x in v.items()}); print('ASELS-EU_DEF pc|XU100+STOXX:', {k: round(x, 2) for k, x in v2.items()})
Y.to_csv(f'{OUT}/res/a2_yearly.csv')

print('\n=== 3) ASTOR yarı örneklem + kayan ham corr ===')
for b in ['EUPWR', 'GESAN']:
    df = pd.concat([ret('ASTOR'), ret(b), M], axis=1).dropna(); mid = df.index[len(df) // 2]
    p1 = pcorr(ret('ASTOR'), ret(b), [M], None, mid); p2 = pcorr(ret('ASTOR'), ret(b), [M], mid, None)
    rc = df.iloc[:, 0].rolling(250, min_periods=200).corr(df.iloc[:, 1]).dropna()
    print(f'ASTOR-{b}: yarı1 (<{mid.date()}) pc {p1[0]:.3f} t {p1[1]:.1f} | yarı2 pc {p2[0]:.3f} t {p2[1]:.1f} | 250g ham corr min {rc.min():.3f} son {rc.iloc[-1]:.3f}')
    # Fisher z farkı
    z = (np.arctanh(p1[0]) - np.arctanh(p2[0])) / np.sqrt(1 / (p1[2] - 4) + 1 / (p2[2] - 4)); print('   Fisher z (yarı1-yarı2)', round(z, 2))
    # likidite: son 250 gün TL hacim medyanı
for s in ['ASTOR', 'EUPWR', 'GESAN']:
    d = raw(s); tl = (d['c'] * d['v']).loc['2025-11-01':]; print(s, 'son 1y medyan günlük TL hacim (mn TL):', round(tl.median() / 1e6, 1))

print('\n=== 4) 15:00 UTC hizalı h1 senkron (2023-12+): BIST cc_t ~ sürücü r[15:00 t-1 -> 15:00 t] ===')
for a, b in [('TOASO', 'STLAM.MI'), ('TOASO', 'RNO.PA'), ('TOASO', 'EXV5.DE'), ('FROTO', 'EXV5.DE'), ('ASELS', 'RHM.DE'), ('ASELS', 'LDO.MI'), ('ASELS', 'SAAB-B.ST'), ('ASELS', 'BA.L'), ('CIMSA', 'HEI.DE'), ('SISE', 'SGO.PA')]:
    rb = snap_ret(b, 15, 0); stx = snap_ret('^STOXX', 15, 0)
    if rb is None: print(a, b, 'h1 yok'); continue
    ra = ret(a)
    c0 = pcorr(ra, rb, [], '2023-12-01', None); p0 = pcorr(ra, rb, [M], '2023-12-01', None)
    p1 = pcorr(ra, rb, [M, stx], '2023-12-01', None) if stx is not None else (np.nan, np.nan, 0)
    d0 = pcorr(ra, ret(b), [M], '2023-12-01', None)
    print(f'{a}-{b}: 15UTC corr {c0[0]:.3f} | pc|XU100 {p0[0]:.3f} (t {p0[1]:.1f}, n {p0[2]}) | pc|XU100+STOXX15 {p1[0]:.3f} (t {p1[1]:.1f}) || günlük kapanış pc|XU100 aynı dönem {d0[0]:.3f}')

print('\n=== 5) Haftalık pc: XU100 vs XU100+STOXX+EEM ===')
W = {k: weekly(ret(k)) for k in ['XU100', '^STOXX', 'EEM', 'TRY=X']}
for a, b in [('TOASO', 'EXV5.DE'), ('TOASO', 'RNO.PA'), ('TOASO', 'STLAM.MI'), ('AEFES', 'CARL-B.CO'), ('AEFES', 'HEIA.AS'), ('AEFES', 'ABI.BR'), ('AEFES', 'CCH.L'), ('AEFES', 'BUD')]:
    wa, wb = weekly(ret(a)), weekly(ret(b))
    r = []
    for s, e in [(FULL0, None), IS_, OOS_]:
        p0 = pcorr(wa, wb, [W['XU100']], s, e, min_n=40); p1 = pcorr(wa, wb, [W['XU100'], W['^STOXX'], W['EEM'], W['TRY=X']], s, e, min_n=40)
        r.append(f'{s[:4]}-{(e or "2026")[:4]}: {p0[0]:.3f}/{p1[0]:.3f} (t {p1[1]:.1f})')
    print(f'{a}-{b} haftalık pc|XU100 / pc|XU100+STOXX+EEM+USDTRY: ' + ' | '.join(r))
wE = weekly(EUD); wa = weekly(ret('ASELS'))
for s, e in [('2014-01-01', '2021-12-31'), ('2022-01-01', None)]:
    p0 = pcorr(wa, wE, [W['XU100']], s, e, min_n=40); p1 = pcorr(wa, wE, [W['XU100'], W['^STOXX'], W['EEM'], W['TRY=X']], s, e, min_n=40)
    print(f'ASELS-EU_DEF haftalık {s[:4]}-{(e or "2026")[:4]}: {p0[0]:.3f} / {p1[0]:.3f} (t {p1[1]:.1f}, n {p1[2]})')

print('\n=== 6) S3 ASELS–EU savunma sepeti rejim (günlük) ===')
A = ret('ASELS')
for s, e in [('2014-01-01', '2021-12-31'), ('2022-01-01', None), ('2010-01-01', '2021-12-31'), ('2022-02-24', None), ('2025-01-01', None)]:
    a0 = pcorr(A, EUD, [M], s, e); a1 = pcorr(A, EUD, [M, STX], s, e); a2 = pcorr(A, EUD, CF3 + [STX], s, e)
    l1 = pcorr(A, EUD.shift(1), [M, M.shift(1), A.shift(1)], s, e)
    print(f'{s}..{e}: pc|XU100 {a0[0]:.3f} (t {a0[1]:.1f}, n {a0[2]}) | +STOXX {a1[0]:.3f} (t {a1[1]:.1f}) | +USDTRY+EEM {a2[0]:.3f} (t {a2[1]:.1f}) | lag1 {l1[0]:.3f} (t {l1[1]:.1f})')
p1 = pcorr(A, EUD, [M, STX], '2014-01-01', '2021-12-31'); p2 = pcorr(A, EUD, [M, STX], '2022-01-01', None)
z = (np.arctanh(p2[0]) - np.arctanh(p1[0])) / np.sqrt(1 / (p1[2] - 5) + 1 / (p2[2] - 5)); print('Fisher z (2022-26 vs 2014-21, +STOXX):', round(z, 2))
# tek isim katkısı
for s_ in EU_DEF:
    a1 = pcorr(A, ret(s_), [M, STX], '2022-01-01', None); a0 = pcorr(A, ret(s_), [M, STX], '2014-01-01', '2021-12-31')
    print(f'  {s_}: 2014-21 {a0[0]:.3f} (n {a0[2]}) -> 2022-26 {a1[0]:.3f} (t {a1[1]:.1f}, n {a1[2]})')
# 'savunma şoku' dışında: büyük EU_DEF günlerini çıkar
ab = pd.concat([A, EUD, M, STX], axis=1, keys=['a', 'e', 'm', 's']).dropna(); ab = ab[ab.index >= '2022-01-01']
mask = ab.e.abs() < ab.e.abs().quantile(0.95)
p = pcorr(ab.a[mask], ab.e[mask], [ab.m[mask], ab.s[mask]]); print('2022-26, |EU_DEF| üst %5 günler hariç pc|XU100+STOXX:', round(p[0], 3), 't', round(p[1], 1))

print('\n=== 7) T3 ULKER – kakao ===')
CC = ret('CC=F'); U_ = ret('ULKER'); dU = decomp('ULKER')
for s, e in [(FULL0, None), IS_, OOS_]:
    a = pcorr(U_, CC, [M], s, e); b = pcorr(dU['intra'], CC.shift(1), [M.shift(1), U_.shift(1)], max(s, '2014-01-01'), e)
    c = pcorr(dU['gap'], CC.shift(1), [M.shift(1)], max(s, '2014-01-01'), e)
    print(f'{s[:4]}-{(e or "2026")[:4]}: sync pc {a[0]:.3f} (t {a[1]:.1f}) | CC_(t-1)->intra pc {b[0]:.3f} (t {b[1]:.1f}) | CC_(t-1)->gap {c[0]:.3f} (t {c[1]:.1f})')
mU = U_.groupby(pd.Grouper(freq='ME')).sum(min_count=10); mC = CC.groupby(pd.Grouper(freq='ME')).sum(min_count=10); mM = M.groupby(pd.Grouper(freq='ME')).sum(min_count=10)
for L in range(0, 7):
    p = pcorr(mU, mC.shift(L), [mM], FULL0, None, min_n=40); print(f'  aylık ULKER ~ kakao lag{L}: pc|XU100 {p[0]:.3f} (t {p[1]:.1f}, n {p[2]})')
print('  ULKER göreli (vs XU100) sinyal BT: sign(CC_{t-1}) * -(ULKER intra) [maliyet hipotezi: kakao↑ -> ULKER↓], 8 bps')
rel = dU['intra'] - decomp('XU100')['intra']
for s, e in [IS_, OOS_]:
    print('   ', s[:4], bt_sign(-CC.shift(1), dU['intra'], 8, 0, s, e), ' göreli:', bt_sign(-CC.shift(1), rel, 8, 0, s, e))

print('\n=== 8) Çimento: ex-çift çimento sepeti kontrolü (küme faktörü mü, çift mi?) ===')
CEM = ['CIMSA', 'OYAKC', 'AKCNS', 'NUHCM', 'AFYON', 'BUCIM', 'KONYA']
for a, b in [('CIMSA', 'OYAKC'), ('CIMSA', 'AKCNS'), ('OYAKC', 'AFYON')]:
    rest = basket([x for x in CEM if x not in (a, b)], 3)
    p0 = pcorr(ret(a), ret(b), [M]); p1 = pcorr(ret(a), ret(b), [M, rest]); p2 = pcorr(ret(a), rest, [M]); p3 = pcorr(ret(b), rest, [M])
    print(f'{a}-{b}: pc|XU100 {p0[0]:.3f} -> +ex-çift sepet {p1[0]:.3f} (t {p1[1]:.1f}); {a}~sepet {p2[0]:.3f}, {b}~sepet {p3[0]:.3f}')
# illikit bacak: bayat fiyat lead-lag var mı? (küçük -> büyük)
for a, b in [('CIMSA', 'KONYA'), ('CIMSA', 'BUCIM'), ('OYAKC', 'BUCIM')]:
    l = pcorr(ret(a), ret(b).shift(1), [M, M.shift(1), ret(a).shift(1)]); r_ = pcorr(ret(b), ret(a).shift(1), [M, M.shift(1), ret(b).shift(1)])
    print(f'  {b}_(t-1)->{a}_t pc {l[0]:.3f} (t {l[1]:.1f}) | {a}_(t-1)->{b}_t pc {r_[0]:.3f} (t {r_[1]:.1f})')
