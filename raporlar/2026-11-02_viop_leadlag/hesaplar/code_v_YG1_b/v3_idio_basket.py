"""v3: hisseye özgü fade — XU030 (Yahoo açılışı) yerine kendi-hariç ciro ağırlıklı 25'lik sepetle (aynı Yahoo açılış verisi) yeniden.
Ayrıca: endeks açılışının iyi olduğu yıllarla kötü olduğu yıllar ayrı."""
import numpy as np, pandas as pd, vb
fr = pd.read_pickle('res/panel.pkl'); S = vb.S47
G = vb.wide(fr, 'gap')['2014':]; I = vb.wide(fr, 'intra')['2014':]; TV = vb.wide(fr, 'tv')['2014':]
gx, ix = G.pop('XU030'), I.pop('XU030'); G, I = G[S], I[S]
W = TV[S].rolling(250, min_periods=120).median().shift(1)
rk = W.rank(axis=1, ascending=False)
Wt = W.where(rk <= 25).where(G.notna() & I.notna())
sw = Wt.sum(axis=1)
sg = (G * Wt).sum(axis=1); si = (I * Wt).sum(axis=1)
w0 = Wt.fillna(0)
# kendi hariç sepet
gbl = (-(G.fillna(0) * w0)).add(sg, axis=0).div((-w0).add(sw, axis=0), axis=0)
ibl = (-(I.fillna(0) * w0)).add(si, axis=0).div((-w0).add(sw, axis=0), axis=0)
ok = Wt.notna().sum(axis=1) >= 15
gbl = gbl[ok]; ibl = ibl[ok]
def tr(gs, ret, leg='both', thr=0.01):
    s = -np.sign(gs).where(gs.abs() > thr)
    if leg == 'up': s = s.where(gs > 0)
    if leg == 'down': s = s.where(gs < 0)
    return s * ret * 1e4
def summ(r, a, b):
    r = r.loc[a:b]; dw = r.mean(axis=1).dropna(); st = r.stack().dropna()
    m, t, n = vb.clus_t(st.values, st.index.get_level_values(0))
    return dict(DW=round(dw.mean(), 1), tDW=round(vb.tstat(dw), 2), TW=round(m, 1), tTW=round(t, 2), n=n)
specs = {
  'idio_XU030': tr(G.sub(gx, axis=0), I.sub(ix, axis=0)),
  'idio_basket': tr(G - gbl, I - ibl),
  'idio_XU030_up': tr(G.sub(gx, axis=0), I.sub(ix, axis=0), 'up'),
  'idio_basket_up': tr(G - gbl, I - ibl, 'up'),
  'idio_XU030_dn': tr(G.sub(gx, axis=0), I.sub(ix, axis=0), 'down'),
  'idio_basket_dn': tr(G - gbl, I - ibl, 'down'),
  'raw_HX030': tr(G, I.sub(ix, axis=0)),
  'raw_Hbasket': tr(G, I - ibl),
  'raw_unhedged': tr(G, I),
}
bad_years = [2014, 2015, 2021, 2022]
rows = []
for k, r in specs.items():
    for p in ['14-17', '18-20', '21-23', '24-26', 'IS', 'OOS']:
        a, b = vb.PERIODS[p]; rows.append(dict(spec=k, per=p, **summ(r, a, b)))
    good = r[~r.index.year.isin(bad_years)]; bad = r[r.index.year.isin(bad_years)]
    rows.append(dict(spec=k, per='goodXUopen', **summ(good, '2014', '2026')))
    rows.append(dict(spec=k, per='badXUopen', **summ(bad, '2014', '2026')))
R = pd.DataFrame(rows); R.to_csv('res/v3_idio_basket.csv', index=False)
pd.set_option('display.width', 250)
for v in ['DW', 'tDW', 'TW', 'tTW']:
    print(v); print(R.pivot(index='spec', columns='per', values=v)[['14-17','18-20','21-23','24-26','IS','OOS','goodXUopen','badXUopen']])
# yıllık idio XU030 vs sepet DW
yr = pd.DataFrame({k: specs[k].mean(axis=1).groupby(specs[k].index.year).mean() for k in ['idio_XU030', 'idio_basket', 'raw_HX030', 'raw_Hbasket', 'raw_unhedged']}).round(1)
print(yr)
pd.to_pickle({'gbl': gbl, 'ibl': ibl}, 'res/basket.pkl')
