import warnings; warnings.filterwarnings('ignore')
import numpy as np, pandas as pd, lb, common as C
V0 = pd.read_pickle('V_sa.pkl'); P0 = pd.read_pickle('P_sa.pkl')
df = lb.pair_frame('SAHOL', 'AKBNK')
rows = []
for bw in [250, 120]:
    for zw in [20, 40, 60, 120]:
        sig = lb.zsig(df, bw=bw, zw=zw, bmin=min(125, bw))
        V = V0.copy(); V['z'] = sig.z.reindex(V.index); V['beta'] = sig.beta.reindex(V.index).ffill()
        P = P0.copy(); P['z'] = sig.z; P['beta'] = sig.beta
        for en in [1.0, 1.5, 2.0]:
            for ex in [en, 1.0, 0.5, 0.0]:
                if ex > en or (ex == 1.0 and en == 1.0 and ex != en): continue
                lab = 'A' if ex == en else f'{ex}'
                T, d = C.run(V, entry=en, exit_=ex); T = T[~T.bad]
                Ts, ds = C.run(P, entry=en, exit_=ex, spot=True)
                o = lb.summ(T, d, pd.Timestamp('2021-01-01'), pd.Timestamp('2026-12-31'))
                o2 = lb.summ(Ts, ds, pd.Timestamp('2014-01-01'), pd.Timestamp('2020-12-31'))
                o3 = lb.summ(T, d, pd.Timestamp('2023-01-01'), pd.Timestamp('2026-12-31'))
                o4 = lb.summ(T, d, pd.Timestamp('2021-01-01'), pd.Timestamp('2022-12-31'))
                rows.append(dict(bw=bw, zw=zw, entry=en, exit=lab, n_oos=o['n'], net_oos=o['mean_net'], t_oos=o['t'], tnw_oos=o['t_nw'],
                                 hold=o['hold_mean'], n_is=o2['n'], net_is=o2['mean_net'], t_is=o2['t'], t_2122=o4['t'], t_2326=o3['t']))
G = pd.DataFrame(rows)
G.to_csv('res_grid.csv', index=False)
pd.set_option('display.width', 200)
print(G.round(2).to_string(index=False))
for bw in [250, 120]:
    g = G[G.bw == bw]
    print(f'bw={bw}: kombinasyon {len(g)}; OOS t>2: {(g.t_oos>2).sum()}, t>1.65: {(g.t_oos>1.65).sum()}, net>0: {(g.net_oos>0).sum()}; IS t>2: {(g.t_is>2).sum()}; ikisi de >2: {((g.t_is>2)&(g.t_oos>2)).sum()}; OOS t medyan {g.t_oos.median():.2f}, NW medyan {g.tnw_oos.median():.2f}')
    for zw in [20, 40, 60, 120]:
        h = g[g.zw == zw]; print(f'   zw={zw}: OOS t medyan {h.t_oos.median():.2f} min {h.t_oos.min():.2f}; IS t medyan {h.t_is.median():.2f}')
    a = g[g.exit == 'A']; print(f'   yalniz A cikisi: OOS t {a.t_oos.round(2).tolist()}')
