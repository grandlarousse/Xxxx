import warnings; warnings.filterwarnings('ignore')
import numpy as np, pandas as pd, lb, common as C
V0 = pd.read_pickle('V_sa.pkl'); P0 = pd.read_pickle('P_sa.pkl')
df = lb.pair_frame('SAHOL', 'AKBNK')
print('== beta penceresi duyarliligi (zw=60, giris 1,5), VIOP 2021-26 t / 2023-26 t / SPOT 2014-20 t')
for bw in [60, 120, 250, 500, 750, 'sabit1']:
    if bw == 'sabit1':
        sig = lb.zsig(df, bw=250); 
        e = (df.ra.fillna(0) - df.rb.fillna(0)); Sx = e.cumsum(); z = (Sx - Sx.rolling(60).mean()) / Sx.rolling(60).std()
        sig['z'] = z; sig['beta'] = 1.0
    else:
        sig = lb.zsig(df, bw=bw, bmin=min(125, bw))
    V = V0.copy(); V['z'] = sig.z.reindex(V.index); V['beta'] = sig.beta.reindex(V.index).ffill()
    P = P0.copy(); P['z'] = sig.z; P['beta'] = sig.beta
    s = []
    for nm, ex in [('A', 1.5), ('C', 1.0), ('B', 0.5)]:
        T, d = C.run(V, exit_=ex); T = T[~T.bad]; Ts, ds = C.run(P, exit_=ex, spot=True)
        o1 = lb.summ(T, d, pd.Timestamp('2021-01-01'), pd.Timestamp('2026-12-31')); o2 = lb.summ(T, d, pd.Timestamp('2023-01-01'), pd.Timestamp('2026-12-31'))
        o3 = lb.summ(Ts, ds, pd.Timestamp('2014-01-01'), pd.Timestamp('2020-12-31')); o4 = lb.summ(T, d, pd.Timestamp('2017-03-01'), pd.Timestamp('2022-12-31'))
        s.append(f"{nm}: {o1['mean_net']:5.0f}({o1['t']:4.2f}) 23-26 {o2['t']:4.2f} 17-22 {o4['t']:4.2f} IS {o3['mean_net']:4.0f}({o3['t']:4.2f})")
    print(f'  bw={bw}:', ' | '.join(s))
print('== yillara gore Kural A (VIOP 2017-26, 8 bps+tik) ve spot (2014-20)')
T, d = C.run(V0, exit_=1.5); T = T[~T.bad]
Ts, ds = C.run(P0, exit_=1.5, spot=True)
for nm, X in [('VIOP', T), ('SPOT', Ts)]:
    X = X.copy(); X['y'] = X.d0.dt.year
    g = X.groupby('y').net.agg(['size', 'mean', 'sum']).round(0)
    g['t'] = X.groupby('y').net.apply(lambda q: q.mean() / q.std(ddof=1) * np.sqrt(len(q))).round(2)
    print(nm); print(g.T.to_string())
o = lb.summ(T, d, pd.Timestamp('2017-03-01'), pd.Timestamp('2022-12-31')); print('VIOP 2017-22 A:', C.line(T, d, '2017-03-01', '2022-12-31'))
print('VIOP 2023-26 A:', C.line(T, d, '2023-01-01', '2026-12-31'))
# dusus donemi
eq = d.loc['2021':].cumsum(); dd = eq - eq.cummax(); t1 = dd.idxmin(); t0 = eq.loc[:t1].idxmax()
print('A VIOP 2021+ maks dusus', round(dd.min()), t0.date(), '->', t1.date(), '; toparlanma', (eq.loc[t1:] >= eq.loc[t0]).idxmax().date() if (eq.loc[t1:] >= eq.loc[t0]).any() else 'yok')
TT = T[T.d0 >= '2021-01-01']
print('A tutma dagilimi: %75', TT.hold.quantile(.75), '%90', TT.hold.quantile(.9), 'maks', TT.hold.max(), '; 3 gun ve alti oran', (TT.hold <= 3).mean().round(2))
print('A long/short:', TT.groupby('sgn').net.agg(['size', 'mean']).round(1).to_dict())
print('A tutma <=3 gun islemleri ort', TT[TT.hold <= 3].net.mean().round(1), '; >3 gun', TT[TT.hold > 3].net.mean().round(1), '; >10 gun', TT[TT.hold > 10].net.mean().round(1), (TT.hold > 10).sum())
