"""(c) Kapanış müzayedesi hareketi (CA = log(spot kapanış / 18:00 fiyatı)) -> VİOP uzlaşma_t -> uzlaşma_{t+h}.
Girdi paneli: out/code_v_YG2_b/res/panel.parquet (bağımsız doğrulayıcının h1 paneli; CA yalnız 14:30 barı olan 'yaz' günleri, yarım günler hariç;
LH = log(C/P14:30) kış dahil). Dönem 2023-11 → 2026-10 (yalnız h1 verisi var) -> IS/OOS: 2023-11..2024-12 / 2025-01..2026-10.
Hipotez (önceki doğrulama): vadeli uzlaşması müzayede hareketinin ~%41'ini izliyor; spot ertesi sabah %35 geri dönerken vadeli CA yönünde 'yetişiyor'.
Testler: DEVAM = +sign(CA)·vadeli getiri (DÖNÜŞ = tersi; aynı testin işaret değişimi). E0 uzlaşma, E1 vadeli son işlem fiyatı, E2 ertesi gün uzlaşma.
Ayrıca hisseye özgü CA_id = CA − CA_XU030 ve kış vekili LH_id. Spot kıyas: −sign(CA)·(C_t→C_{t+h}) (açığa satış gerekir)."""
from klib import *
C = ctx(); vcal = C['vcal']
A = pd.read_parquet(S + '/out/code_v_YG2_b/res/panel.parquet')
A['date'] = pd.to_datetime(A['date'])
X = A[A.sym == 'XU030'].set_index('date')[['CA', 'LH']].rename(columns={'CA': 'CA_x', 'LH': 'LH_x'})
A = A[A.sym != 'XU030'].merge(X, left_on='date', right_index=True, how='left')
A['CA_id'] = A['CA'] - A['CA_x']; A['LH_id'] = A['LH'] - A['LH_x']
A = A.rename(columns={'sym': 'und'})
# vadeli likidite (t-1'e kadar 60g medyan TL hacim) tercili
TV = C['tot_value']
liq = TV.shift(1).rolling(60, min_periods=20).median()
A['fliq'] = [liq.at[d, u] if (d in liq.index and u in liq.columns) else np.nan for d, u in zip(A.date, A.und)]
A['fliq_r'] = A.groupby('date')['fliq'].rank(pct=True)
IS_END = pd.Timestamp('2024-12-31')
print('gözlem', A.CA.notna().sum(), 'gün', A.loc[A.CA.notna(), 'date'].nunique(), A.date.min().date(), A.date.max().date())
# vadeli uzlaşmanın CA'yı izleme oranı: settle_t vs P15 -> raw_r'ın CA'ya eğimi (günlük)
RR = C['raw_r']
A['fr0'] = [RR.at[d, u] if (d in RR.index and u in RR.columns) else np.nan for d, u in zip(A.date, A.und)]
A['spot_cc'] = np.log(A['C'] / A.groupby('und')['C'].shift(1))
z = A[['fr0', 'spot_cc', 'CA', 'date']].dropna()
z['d'] = z.spot_cc - z.fr0
b = np.polyfit(z.CA, z.d, 1)[0]
print(f'(spot cc − vadeli uzlaşma getirisi) ~ CA eğimi {b:.3f} -> vadeli uzlaşma CA\'nın ~%{100*(1-b):.0f}\'ını içeriyor')
out = []
def run(name, d, sig, thr, h, entry, extra_mask=None, inst='VIOP', side_sign=+1):
    e = d[d[sig].abs() > thr / 1e4].copy()
    if extra_mask is not None: e = e[extra_mask(e)]
    e['side'] = side_sign * np.sign(e[sig])
    if entry == 'E2': e['date'] = shift_date(e['date'], 1, vcal); ent = 'E0'
    else: ent = entry
    e = e.dropna(subset=['date']).copy()
    if inst == 'VIOP': e['ret'] = vectorized_fut(e, h, ent)
    else: e['ret'] = vectorized_spot(e, h, excess=None)
    st = trade_stats(e, 'ret', h=h, is_end=IS_END)
    reg('c_muzayede', name, inst, entry, h, st, dict(thr=thr, sig=sig))
    out.append(f'{name:34s} {sig:6s} |x|>{thr:3d} {inst} {entry} h{h} {fmt(st)}')
    return st
for sig in ['CA', 'CA_id']:
    for thr in [25, 50, 100]:
        for h in H:
            for entry in ['E0', 'E1', 'E2']:
                run('DEVAM vadeli', A, sig, thr, h, entry)
        for h in [1, 3]:
            run('DEVAM vadeli likit üst 1/3', A, sig, thr, h, 'E0', lambda e: e.fliq_r > 2 / 3)
            run('DEVAM vadeli likit alt 2/3', A, sig, thr, h, 'E0', lambda e: e.fliq_r <= 2 / 3)
            run('DÖNÜŞ spot (açığa satış)', A, sig, thr, h, 'C', inst='SPOT', side_sign=-1)
# kış vekili (14:30 sonrası 30 dk sürekli işlem dahil)
for thr in [25, 50]:
    for h in [1, 3]:
        run('DEVAM vadeli kış vekili LH_id', A[A.CA.isna()], 'LH_id', thr, h, 'E0')
for o in out: print(o)
D = save_registry('c_muzayede'); print('test sayısı', len(D))
# ek: E1 (vadeli son işlem) likit alt kümede ve XU030 bileşeni
out.clear()
for thr in [25, 50]:
    for h in [1, 2, 3]:
        run('DEVAM vadeli likit üst 1/3', A, 'CA', thr, h, 'E1', lambda e: e.fliq_r > 2 / 3)
        run('DEVAM vadeli likit üst 1/3', A, 'CA', thr, h, 'E2', lambda e: e.fliq_r > 2 / 3)
# piyasa geneli müzayede (XU030 spot CA_x) -> XU030 vadelisi
Xd = A[['date', 'CA_x']].drop_duplicates('date').assign(und='XU030')
for thr in [10, 20, 30]:
    for h in [1, 2, 3]:
        for entry in ['E0', 'E1']:
            run('XU030 müzayede -> XU030 vadeli DEVAM', Xd, 'CA_x', thr, h, entry)
for o in out: print(o)
D = save_registry('c_muzayede'); print('test sayısı', len(D))
