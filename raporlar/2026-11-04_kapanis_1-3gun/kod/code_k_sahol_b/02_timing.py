import warnings; warnings.filterwarnings('ignore')
import numpy as np, pandas as pd, lb, common as C
V = pd.read_pickle('V_sa.pkl'); sig = pd.read_pickle('sig_sa.pkl')
hA = lb.hourly('SAHOL'); hB = lb.hourly('AKBNK')
def bar(h, t):
    return h[h.t == t].groupby('ldate').c.last()
out = {}
for lab, tt in [('1730', ['13:30']), ('1800', ['14:30', '13:30'])]:
    pa = None; pb = None
    for t in tt:  # 14:30 yoksa 13:30 kullan
        xa = bar(hA, t); xb = bar(hB, t)
        pa = xa if pa is None else pa.combine_first(xa)
        pb = xb if pb is None else pb.combine_first(xb)
    za = lb.z_intraday(sig, pa.reindex(sig.index), pb.reindex(sig.index))
    out[lab] = za
Z = pd.DataFrame({'close': sig.z, 'z1730': out['1730'], 'z1800': out['1800']})
Zv = Z.reindex(V.index)
a, b = '2023-12-01', '2026-11-03'
m = Zv.loc[a:b].dropna()
print('z korelasyonu (2023-12+):', m.corr().round(3).to_dict())
print('|z|>1.5 isaret uyumu: close vs 1730', ((m.close.abs() > 1.5) == (m.z1730.abs() > 1.5)).mean().round(3))
for ex_nm, ex in [('A', 1.5), ('C', 1.0), ('B', 0.5)]:
    print('== Kural', ex_nm, 'pencere', a, b)
    for col in ['close', 'z1730', 'z1800']:
        X = V.copy(); X['z'] = Zv[col]
        X.loc[X.index < a, 'z'] = np.nan
        T, d = C.run(X, exit_=ex)
        T = T[~T.bad]
        print(f'  sinyal={col:6s}', C.line(T, d, a, b))
# ertesi gun uzlasmasi: sinyali 1 gun kaydir (karar t kapanisi, islem t+1 uzlasmasi)
print('== Ertesi gun uzlasmasi (z 1 gun gecikmeli), VIOP')
for ex_nm, ex in [('A', 1.5), ('C', 1.0), ('B', 0.5)]:
    X = V.copy(); X['z'] = V.z.shift(1)
    T, d = C.run(X, exit_=ex); T = T[~T.bad]
    X0 = V.copy(); T0, d0 = C.run(X0, exit_=ex); T0 = T0[~T0.bad]
    for (pa_, pb_) in [('2021-01-01', '2026-12-31'), ('2023-12-01', '2026-12-31')]:
        print(f'  {ex_nm} {pa_[:7]}+ ayni gun:', C.line(T0, d0, pa_, pb_))
        print(f'  {ex_nm} {pa_[:7]}+ ertesi :', C.line(T, d, pa_, pb_))
# sadece giris gecikmeli, cikis ayni (gercekci olmayan ama ayristirici)
print('== olay profili: ayni gun uzlasma girisi, kumulatif brut (VIOP 2021-26, A girisleri)')
TA = pd.read_csv('tr_viop_A.csv', parse_dates=['d0', 'd1'])
TA = TA[(TA.d0 >= '2021-01-01')]
idx = V.index; pos = {d: i for i, d in enumerate(idx)}
for h in [1, 2, 3, 5, 10]:
    r = []
    for _, t in TA.iterrows():
        i0 = pos[t.d0]; i1 = min(i0 + h, len(idx) - 1)
        sa = V.dFA.values[i0:i1].sum() / V.F0A.values[i0]; sb = V.dFB.values[i0:i1].sum() / V.F0B.values[i0]
        r.append(t.sgn * (sa - t.beta * sb) * 1e4)
    r = np.array(r); print(f'  h={h:2d}: ort {r.mean():6.1f} t {r.mean()/r.std(ddof=1)*np.sqrt(len(r)):5.2f}')
Z.to_pickle('Z_intraday.pkl')
