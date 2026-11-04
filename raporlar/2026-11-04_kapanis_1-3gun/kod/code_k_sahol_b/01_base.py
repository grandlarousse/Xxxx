import warnings; warnings.filterwarnings('ignore')
import numpy as np, pandas as pd, lb, common as C
o = C.setup()
sig, V, P = o['sig'], o['V'], o['P']
print('son z:'); print(sig[['ca','cb','beta','z']].tail(8).round(4))
V.to_pickle('V_sa.pkl'); P.to_pickle('P_sa.pkl'); sig.to_pickle('sig_sa.pkl')
print('VIOP veri kontrol: dF NaN gunleri', V[['dFA','dFB']].isna().sum().to_dict(), 'son', V.index[-1])
for nm, ex in [('A', 1.5), ('C', 1.0), ('B', 0.5), ('z0', 0.0)]:
    print('==', nm)
    T, d = C.run(V, exit_=ex)
    T.to_csv(f'tr_viop_{nm}.csv', index=False)
    print(' VIOP 2021-26 :', C.line(T, d, '2021-01-01', '2026-12-31'))
    print(' VIOP 2017-20 :', C.line(T, d, '2017-03-01', '2020-12-31'))
    Ts, ds = C.run(P, exit_=ex, spot=True)
    print(' SPOT 2014-20 :', C.line(Ts, ds, '2014-01-01', '2020-12-31'))
    print(' SPOT 2021-26 :', C.line(Ts, ds, '2021-01-01', '2026-12-31'))
    if nm == 'A': Ts.to_csv('tr_spot_A.csv', index=False)
print('== sabit tutma')
for h in [1, 2, 3, 5, 10]:
    T, d = C.run(V, fixed=h); Ts, ds = C.run(P, fixed=h, spot=True)
    print(f' h={h:2d} VIOP21-26:', C.line(T, d, '2021-01-01', '2026-12-31'), '| SPOT14-20:', C.line(Ts, ds, '2014-01-01', '2020-12-31')[:60])
