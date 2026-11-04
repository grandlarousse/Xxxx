import warnings; warnings.filterwarnings('ignore')
import numpy as np, pandas as pd, lb, common as C
V = pd.read_pickle('V_sa.pkl'); sig = pd.read_pickle('sig_sa.pkl'); P = pd.read_pickle('P_sa.pkl')
idx = V.index
# ---- (2a) temettu gunleri
print('== (2a) temettu gunleri: vadeli getirisi vs spot ham / adj')
for leg, cc, pp, F0, dF in [('SAHOL', 'ca', 'pa', 'F0A', 'dFA'), ('AKBNK', 'cb', 'pb', 'F0B', 'dFB')]:
    f = sig[pp] / sig[cc]; jump = f / f.shift(1) - 1
    ex = jump[jump > 0.003].index; ex = ex[ex >= '2017-03-10']
    rf = (V[dF] / V[F0]).shift(1)  # t-1 -> t vadeli getirisi (t-1'de tutulan sozlesme)
    rraw = np.log(sig[cc]).diff(); radj = np.log(sig[pp]).diff()
    rows = []
    for d in ex:
        if d in rf.index:
            rows.append((d.date(), round(jump[d] * 100, 2), round(np.log1p(rf[d]) * 100, 2), round(rraw[d] * 100, 2), round(radj[d] * 100, 2)))
    R = pd.DataFrame(rows, columns=['exdate', 'temettu%', 'vadeli%', 'spot_ham%', 'spot_adj%'])
    R['vad-adj'] = R['vadeli%'] - R['spot_adj%']; R['vad-ham'] = R['vadeli%'] - R['spot_ham%']
    print(leg); print(R.to_string(index=False))
# ---- (2b) gunluk vadeli - spot farki; devir gunu ve normal gun
print('== (2b) |vadeli - spot adj| gunluk fark dagilimi (2021+), devir gunu ayri')
for leg, pp, F0, dF, roll in [('SAHOL', 'pa', 'F0A', 'dFA', 'rollA'), ('AKBNK', 'pb', 'F0B', 'dFB', 'rollB')]:
    rf = np.log1p(V[dF] / V[F0])  # d -> d+1, c(d)
    rs = np.log(sig[pp]).diff().shift(-1).reindex(idx)  # d -> d+1 spot
    D = pd.DataFrame({'rf': rf, 'rs': rs, 'roll': V[roll]}).loc['2021':].dropna()
    D['diff'] = (D.rf - D.rs) * 1e4
    print(leg, 'normal gun: ort %.1f sd %.1f | devir gunu (yeni sozlesmenin ilk gunu): ort %.1f sd %.1f n=%d | |fark|>200bps: %d' % (
        D[~D.roll]['diff'].mean(), D[~D.roll]['diff'].std(), D[D.roll]['diff'].mean(), D[D.roll]['diff'].std(), D.roll.sum(), (D['diff'].abs() > 200).sum()))
    print('   en buyuk farklar:', D['diff'].abs().sort_values().tail(4).round(0).to_dict())
# ---- (2c) islem bazinda VIOP - spot farki (ayni tarihler), long/short; devirli islemler
TA = pd.read_csv('tr_viop_A.csv', parse_dates=['d0', 'd1']); TA = TA[(TA.d0 >= '2021-01-01') & ~TA.bad]
ps = {d: i for i, d in enumerate(P.index)}
sp = []
for _, t in TA.iterrows():
    i0, i1 = ps[t.d0], ps[t.d1]
    sa = P.dFA.values[i0:i1].sum() / P.F0A.values[i0]; sb = P.dFB.values[i0:i1].sum() / P.F0B.values[i0]
    sp.append(t.sgn * (sa - t.beta * sb) * 1e4)
TA['spot_gross'] = sp; TA['vmins'] = TA.gross - TA.spot_gross
print('== (2c) A 2021-26 islem bazinda VIOP brut - spot brut (ayni giris/cikis gunleri):')
print(TA.groupby('sgn').agg(n=('net', 'size'), vadeli_brut=('gross', 'mean'), spot_brut=('spot_gross', 'mean'), fark=('vmins', 'mean'), hold=('hold', 'mean')).round(1))
print(' devirli islemler:', TA.groupby(TA.nroll > 0).agg(n=('net', 'size'), net=('net', 'mean'), fark=('vmins', 'mean')).round(1).to_dict())
# temettu donemi iceren islemler
exd = []
for pp, cc in [('pa', 'ca'), ('pb', 'cb')]:
    f = sig[pp] / sig[cc]; j = f / f.shift(1) - 1; exd += list(j[j > 0.003].index)
TA['div'] = [any((d > t.d0) and (d <= t.d1) for d in exd) for _, t in TA.iterrows()]
print(' temettu gunu iceren islemler:', TA[TA['div']][['d0', 'd1', 'sgn', 'gross', 'spot_gross', 'vmins']].round(0).to_string())
# ---- (4) alt donemler
print('== (4) alt donemler, VIOP, 8bps+tik')
for nm, ex in [('A', 1.5), ('C', 1.0), ('B', 0.5)]:
    T, d = C.run(V, exit_=ex); T = T[~T.bad]
    for a, b in [('2021-01-01', '2022-12-31'), ('2023-01-01', '2023-12-31'), ('2024-01-01', '2024-12-31'), ('2025-01-01', '2025-12-31'),
                 ('2026-01-01', '2026-12-31'), ('2026-09-16', '2026-11-03'), ('2025-03-19', '2025-05-31'), ('2025-11-01', '2026-11-03')]:
        print(f'  {nm} {a}..{b}:', C.line(T, d, a, b))
    # fon krizi islemleri
    F = T[(T.d1 >= '2026-09-01')]
    print('   son islemler:', F[['d0', 'd1', 'sgn', 'hold', 'net']].round(0).to_string(index=False).replace('\n', '\n   '))
# ---- (5) en iyi 5/10 islem cikinca
print('== (5) en iyi islemler cikarilinca (VIOP 2021-26)')
for nm, ex in [('A', 1.5), ('C', 1.0), ('B', 0.5)]:
    T, d = C.run(V, exit_=ex); T = T[~T.bad & (T.d0 >= '2021-01-01')]
    for k in [0, 5, 10]:
        x = T.net.sort_values().iloc[:len(T) - k] if k else T.net
        print(f'  {nm} -{k:2d}: n={len(x)} ort={x.mean():6.1f} t={x.mean()/x.std(ddof=1)*np.sqrt(len(x)):5.2f} medyan={x.median():6.1f}')
    # en iyi ve en kotu islemler
    print('   en iyi 5:', T.nlargest(5, 'net')[['d0', 'net']].assign(d0=lambda q: q.d0.dt.date).values.tolist())
    print('   en kotu 5:', T.nsmallest(5, 'net')[['d0', 'net']].assign(d0=lambda q: q.d0.dt.date).values.tolist())
