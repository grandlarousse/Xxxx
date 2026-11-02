"""v9: dolum ve likidite — VİOP bülteni (2017-03..2026-10). Ön ay (en yüksek TL hacimli) SSF.
(a) Sinyal günlerinde SSF işlem sayısı / TL hacim; (b) SSF gün içinde spot açılış eşdeğeri fiyatı (O x baz) gördü mü?
(c) SSF'nin kendi uzlaşma fiyatından ölçülen gün içi: spot O eşdeğerinden SSF uzlaşmaya fade (baz gürültüsü dahil)."""
import numpy as np, pandas as pd, vb
fr = pd.read_pickle('res/panel.pkl'); S = vb.S47
p = pd.read_parquet(f'{vb.D}/viop_panel.parquet', columns=['date', 'root', 'segment', 'expiry', 'settle', 'prev_settle', 'open', 'low', 'high', 'close', 'vwap', 'value_tl', 'trades'])
p = p[(p.segment == 'SSF') & p.root.isin(S)].copy()
p['date'] = pd.to_datetime(p.date)
p = p.sort_values(['root', 'date', 'value_tl']).groupby(['root', 'date']).tail(1)   # ön ay ~ en hacimli
liq = pd.read_csv('res/liq.csv', index_col=0).iloc[:, 0]
B = pd.read_pickle('res/basket.pkl'); gbl = B['gbl']; ibl = B['ibl']
rows = []
for s in S:
    d = fr[s]; q = p[p.root == s].set_index('date')
    x = pd.DataFrame({'O': d.o, 'C': d.c, 'gap': d.gap, 'intra': d.intra}).join(q[['settle', 'open', 'low', 'high', 'vwap', 'value_tl', 'trades']], how='inner')
    x = x.loc['2017-03-06':]
    x['idio'] = x.gap - gbl[s].reindex(x.index); x['hb'] = x.intra - ibl[s].reindex(x.index)
    x['b'] = x.settle / x.C
    x['Oeq'] = x.O * x.b
    x['sym'] = s; x['cls'] = liq[s]
    rows.append(x)
X = pd.concat(rows)
X = X[(X.trades > 0) & X.b.between(0.9, 1.15)]
print('SSF gün-hisse gözlemi', len(X))
for nm, cond, side in [('idio UP', X.idio > 0.01, -1), ('idio DOWN', X.idio < -0.01, 1), ('raw |gap|>1%', X.gap.abs() > 0.01, None)]:
    Y = X[cond].copy()
    if side is None: Y['side'] = -np.sign(Y.gap)
    else: Y['side'] = side
    fill = np.where(Y.side < 0, Y.high >= Y.Oeq, Y.low <= Y.Oeq)
    Y['fill'] = fill
    # SSF ile: spot O-eşdeğerinden SSF uzlaşmaya (dolum varsayımı) vs spot O->C
    Y['ssf_ret'] = Y.side * np.log(Y.settle / Y.Oeq) * 1e4; Y['spot_ret'] = Y.side * Y.intra * 1e4
    for cls in ['ILL', 'LIQ']:
        Z = Y[Y.cls == cls]; Zo = Z[Z.index >= '2021-01-01']
        print(f'{nm} {cls}: n {len(Z)} (OOS {len(Zo)}) | SSF işlem sayısı medyan {Z.trades.median():.0f} (OOS {Zo.trades.median():.0f}), p10 {Z.trades.quantile(0.1):.0f} | TL hacim medyan {Z.value_tl.median()/1e6:.1f} mn (OOS {Zo.value_tl.median()/1e6:.1f}) | SSF gün içinde O-eşdeğerine ulaştı: %{100*Z.fill.mean():.0f} (OOS %{100*Zo.fill.mean():.0f})')
        print(f'      OOS spot O->C {Zo.spot_ret.mean():.1f}  | SSF O-eşd.->uzlaşma {Zo.ssf_ret.mean():.1f} | yalnız O-eşdeğerine ulaşılan günler spot {Zo[Zo.fill].spot_ret.mean():.1f}, ulaşılamayan {Zo[~Zo.fill].spot_ret.mean():.1f} (n {(~Zo.fill).sum()})')
# CIMSA / OYAKC
for s in ['CIMSA', 'OYAKC']:
    Z = X[(X.sym == s) & (X.gap.abs() > 0.01) & (X.index >= '2021-01-01')]
    side = -np.sign(Z.gap); fill = np.where(side < 0, Z.high >= Z.Oeq, Z.low <= Z.Oeq)
    print(s, 'OOS sinyal günü SSF işlem medyanı', Z.trades.median(), 'TL hacim medyan (mn)', round(Z.value_tl.median() / 1e6, 1), 'O-eşd. ulaşma %', round(100 * fill.mean()), 'n', len(Z))
    for y, g in Z.groupby(Z.index.year):
        print('   ', y, 'trades medyan', g.trades.median(), 'TL mn', round(g.value_tl.median() / 1e6, 1))

print('\n--- (d) baz gürültüsü ve en-iyi-durum SSF dolumu')
X = X.sort_values(['sym']).copy()
X['lb'] = np.log(X.b)
db = X.groupby('sym').lb.diff()
print('günlük baz değişimi sd (bps)', round(db.std() * 1e4, 1), 'MAD-sd', round(1.4826 * (db - db.median()).abs().median() * 1e4, 1))
for nm, cond, side in [('idio UP', X.idio > 0.01, -1), ('idio DOWN', X.idio < -0.01, 1), ('raw |gap|>1%', X.gap.abs() > 0.01, None)]:
    Y = X[cond & (X.index >= '2021-01-01')].copy()
    Y['side'] = -np.sign(Y.gap) if side is None else side
    sp = Y.side * Y.intra * 1e4
    best_entry = np.where(Y.side < 0, np.minimum(Y.Oeq, Y.high), np.maximum(Y.Oeq, Y.low))
    best = Y.side * np.log(Y.settle / best_entry) * 1e4
    far = np.where(Y.side < 0, Y.high < Y.Oeq * (1 - 0.005), Y.low > Y.Oeq * (1 + 0.005))
    oh = np.where(Y.side < 0, np.isclose(Y.O, Y.index.map(lambda t: 0) + 0) , False)
    for cls in ['ILL', 'LIQ', 'ALL']:
        m = (Y.cls == cls).values if cls != 'ALL' else np.ones(len(Y), bool)
        print(f'{nm} {cls} OOS: spot O->C {sp[m].mean():.1f} | en-iyi-durum SSF (min(Oeq,SSF tepe) -> uzlaşma) {best[m].mean():.1f} | SSF hiç O-eşd.\'nin %0,5 yakınına gelmedi: %{100*far[m].mean():.1f} (n {far[m].sum()}), bu günlerde spot {sp[m][far[m]].mean():.0f} bps; bu günler hariç spot {sp[m][~far[m]].mean():.1f}')
