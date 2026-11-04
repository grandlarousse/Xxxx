import warnings; warnings.filterwarnings('ignore')
import numpy as np, pandas as pd, lb, common as C
pairs = [('SAHOL', 'AKBNK', True), ('SAHOL', 'YKBNK', True), ('SAHOL', 'XBANK', 'XLBNK'), ('KCHOL', 'YKBNK', True), ('AGHOL', 'AEFES', False),
         ('SAHOL', 'GARAN', True), ('SAHOL', 'ISCTR', True), ('KCHOL', 'AKBNK', True), ('AKBNK', 'YKBNK', True), ('KCHOL', 'SAHOL', True)]
rows = []
for a, b, hv in pairs:
    o = C.setup(a, b, fb=(hv if isinstance(hv, str) else None), viop=bool(hv))
    sig = o['sig']; P = o['P']
    print(f'=== {a}/{b}  beta(son)={sig.beta.iloc[-1]:.2f}  z(son)={sig.z.iloc[-1]:.2f}  corr(r) 2021+={sig.loc["2021":,["ra","rb"]].corr().iloc[0,1]:.2f}')
    for nm, ex in [('A', 1.5), ('C', 1.0), ('B', 0.5)]:
        Ts, ds = C.run(P, exit_=ex, spot=True)
        l1 = C.line(Ts, ds, '2014-01-01', '2020-12-31'); l2 = C.line(Ts, ds, '2021-01-01', '2026-12-31')
        r = dict(pair=f'{a}/{b}', rule=nm)
        s1 = lb.summ(Ts, ds, pd.Timestamp('2014-01-01'), pd.Timestamp('2020-12-31')); s2 = lb.summ(Ts, ds, pd.Timestamp('2021-01-01'), pd.Timestamp('2026-12-31'))
        r.update(is_n=s1['n'], is_net=s1['mean_net'], is_t=s1['t'], spot_oos_net=s2['mean_net'], spot_oos_t=s2['t'])
        print(f'  {nm} SPOT14-20: {l1}\n    SPOT21-26: {l2}')
        if hv:
            V = o['V']
            T, d = C.run(V, exit_=ex); T = T[~T.bad]
            s3 = lb.summ(T, d, pd.Timestamp('2021-01-01'), pd.Timestamp('2026-12-31'))
            if s3['n'] == 0:
                print('    VIOP: islem yok; F0B dolu gun', V.F0B.notna().sum(), 'dFB dolu', V.dFB.notna().sum(), 'bad', len(T)); rows.append(r); continue
            vv = V.loc['2025':, ['valA', 'valB']].median() / 1e6
            r.update(viop_n=s3['n'], viop_net=s3['mean_net'], viop_t=s3['t'], viop_tnw=s3.get('t_nw'), adv_mn=f"{vv.valA:.0f}/{vv.valB:.0f}")
            print(f'    VIOP21-26: {C.line(T, d, "2021-01-01", "2026-12-31")}  (2025+ medyan islem degeri mn TL {vv.valA:.0f}/{vv.valB:.0f})')
        rows.append(r)
R = pd.DataFrame(rows); R.to_csv('res_pairs.csv', index=False)
print(R.round(2).to_string(index=False))
