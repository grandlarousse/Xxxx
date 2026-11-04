import warnings; warnings.filterwarnings('ignore')
import numpy as np, pandas as pd, lb, common as C
V = pd.read_pickle('V_sa.pkl'); P = pd.read_pickle('P_sa.pkl')
print('== spot vekili, Kural A, brut ve net, donemler')
Ts, ds = C.run(P, exit_=1.5, spot=True)
Ts0, ds0 = C.run(P, exit_=1.5, spot=True, cA=0, cB=0, tick=False)
for a, b in [('2005-01-01', '2013-12-31'), ('2014-01-01', '2020-12-31'), ('2021-01-01', '2026-12-31')]:
    x = Ts[(Ts.d0 >= a) & (Ts.d0 <= b)]; x0 = Ts0[(Ts0.d0 >= a) & (Ts0.d0 <= b)]
    print(f'  {a[:4]}-{b[:4]}: n={len(x)} brut {x0.net.mean():.1f} (t {x0.net.mean()/x0.net.std()*np.sqrt(len(x0)):.2f}) net {x.net.mean():.1f} (t {x.net.mean()/x.net.std()*np.sqrt(len(x)):.2f}) ort maliyet {x.cost.mean():.1f}')
for nm, ex in [('C', 1.0), ('B', 0.5)]:
    T1, _ = C.run(P, exit_=ex, spot=True); T0, _ = C.run(P, exit_=ex, spot=True, cA=0, cB=0, tick=False)
    for a, b in [('2005-01-01', '2013-12-31')]:
        x = T1[(T1.d0 >= a) & (T1.d0 <= b)]; x0 = T0[(T0.d0 >= a) & (T0.d0 <= b)]
        print(f'  {nm} {a[:4]}-{b[:4]}: n={len(x)} brut {x0.net.mean():.1f} (t {x0.net.mean()/x0.net.std()*np.sqrt(len(x0)):.2f}) net {x.net.mean():.1f} (t {x.net.mean()/x.net.std()*np.sqrt(len(x)):.2f})')
print('== maksimum tutma (VIOP 2021-26 / 2023-26)')
for nm, ex in [('A', 1.5), ('C', 1.0), ('B', 0.5)]:
    for mh in [None, 3, 5, 10, 20]:
        T, d = C.run(V, exit_=ex, maxhold=mh); T = T[~T.bad]
        print(f'  {nm} maks {str(mh):4s}:', C.line(T, d, '2021-01-01', '2026-12-31'), '| 23-26 t', round(lb.summ(T, d, pd.Timestamp('2023-01-01'), pd.Timestamp('2026-12-31'))['t'], 2))
print('== yalniz kisa (z>+1,5) / yalniz uzun')
for side in ['short', 'long']:
    T, d = C.run(V, exit_=1.5, side=side); T = T[~T.bad]
    print(f'  A {side}:', C.line(T, d, '2021-01-01', '2026-12-31'))
# 2023 subat deprem kapanisi: acik islem var mi
T, d = C.run(V, exit_=1.5); T = T[~T.bad]
print('deprem donemi islemleri:', T[(T.d0 <= '2023-02-15') & (T.d1 >= '2023-02-07')][['d0', 'd1', 'sgn', 'net']].to_string())
print('bad (eksik veri) islemler:', C.run(V, exit_=1.5)[0].query('bad')[['d0', 'd1']].values.tolist())
