"""v1: taban yeniden üretim + ortak faktör kontrolleri + alt dönemler (2014-17, 18-20, 21-23, 24-26)."""
import numpy as np, pandas as pd, vb
fr = pd.read_pickle('res/panel.pkl')
S = vb.S47
G = vb.wide(fr, 'gap')['2014':]; I = vb.wide(fr, 'intra')['2014':]; TV = vb.wide(fr, 'tv')['2014':]
gx, ix = G.pop('XU030'), I.pop('XU030'); TV = TV[S]
G, I = G[S], I[S]
# likidite: son 250 gün medyan TL ciro
liq = TV.iloc[-250:].median().sort_values()
ILL = list(liq.index[:24]); LIQ = list(liq.index[24:])
pd.Series({s: ('ILL' if s in ILL else 'LIQ') for s in S}).to_csv('res/liq.csv')
XS = I.sub(I.mean(axis=1), axis=0)        # aynı gün kesitsel ortalamadan arındırılmış gün-içi
HX = I.sub(ix, axis=0)                    # XU030 gün-içiyle hedge'li
IDG = G.sub(gx, axis=0)                   # hisseye özgü gap
def trades(gsig, ret, thr=0.01, leg='both', cols=None):
    s = -np.sign(gsig).where(gsig.abs() > thr)
    if leg == 'up': s = s.where(gsig > 0)
    if leg == 'down': s = s.where(gsig < 0)
    r = (s * ret) * 1e4
    if cols is not None: r = r[cols]
    return r
def summ(r, a, b):
    r = r.loc[a:b]
    dw = r.mean(axis=1).dropna()
    st = r.stack().dropna()
    m, t, n = vb.clus_t(st.values, st.index.get_level_values(0))
    return dict(DW=dw.mean(), tDW=vb.tstat(dw), TW=m, tTW=t, n=n, ndays=len(dw))
rows = []
specs = {
 'raw_both': trades(G, I), 'raw_up': trades(G, I, leg='up'), 'raw_down': trades(G, I, leg='down'),
 'raw_both_ILL': trades(G, I, cols=ILL), 'raw_both_LIQ': trades(G, I, cols=LIQ),
 'XS_both': trades(G, XS), 'XS_up': trades(G, XS, leg='up'), 'XS_down': trades(G, XS, leg='down'),
 'HX_both': trades(G, HX), 'HX_up': trades(G, HX, leg='up'), 'HX_down': trades(G, HX, leg='down'),
 'idio_HX_both': trades(IDG, HX), 'idio_HX_up': trades(IDG, HX, leg='up'), 'idio_HX_down': trades(IDG, HX, leg='down'),
 'idio_XS_both': trades(IDG, XS), 'idio_HX_both_ILL': trades(IDG, HX, cols=ILL), 'idio_HX_both_LIQ': trades(IDG, HX, cols=LIQ),
 # kıyas: |gap|>%1 günlerinde her zaman short gün-içi
 'alwaysshort': (-1 * I.where(G.abs() > 0.01)) * 1e4,
}
for k, r in specs.items():
    for p in ['14-17', '18-20', '21-23', '24-26', 'IS', 'IS16', 'OOS', 'ALL']:
        a, b = vb.PERIODS[p]
        rows.append(dict(spec=k, per=p, **summ(r, a, b)))
R = pd.DataFrame(rows); R.to_csv('res/v1_specs.csv', index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 300)
print(R.pivot(index='spec', columns='per', values='DW').round(1)[['14-17','18-20','21-23','24-26','IS','OOS']])
print(R.pivot(index='spec', columns='per', values='tDW').round(2)[['14-17','18-20','21-23','24-26','IS','OOS']])
print(R.pivot(index='spec', columns='per', values='TW').round(1)[['14-17','18-20','21-23','24-26','IS','OOS']])
print(R.pivot(index='spec', columns='per', values='tTW').round(2)[['14-17','18-20','21-23','24-26','IS','OOS']])
# Ortak faktör: DW fade günlük serisini aynı gün XU030 gün-içine regres et
for k in ['raw_both', 'raw_up', 'raw_down']:
    dw = specs[k].mean(axis=1).dropna()
    for p in ['IS', 'OOS', '24-26']:
        a, b = vb.PERIODS[p]
        y = dw.loc[a:b]; x = ix.reindex(y.index) * 1e4
        ok = x.notna(); y, x = y[ok], x[ok]
        X = np.c_[np.ones(len(x)), x]; bet = np.linalg.lstsq(X, y.values, rcond=None)[0]
        e = y.values - X @ bet; s2 = e @ e / (len(y) - 2); cov = s2 * np.linalg.inv(X.T @ X)
        print(f'{k} {p}: alpha {bet[0]:.1f} (t {bet[0]/np.sqrt(cov[0,0]):.2f}) beta_XU030intra {bet[1]:.3f} (t {bet[1]/np.sqrt(cov[1,1]):.1f}) n {len(y)}')
# net short oranı
s = -np.sign(G).where(G.abs() > 0.01)
print('short oranı IS/OOS', (s.loc[:'2020'] < 0).sum().sum() / s.loc[:'2020'].notna().sum().sum(), (s.loc['2021':] < 0).sum().sum() / s.loc['2021':].notna().sum().sum())
print('XU030 intra ort bps IS/OOS', ix.loc[:'2020'].mean() * 1e4, ix.loc['2021':].mean() * 1e4, 'hisse ort intra', I.loc[:'2020'].stack().mean() * 1e4, I.loc['2021':].stack().mean() * 1e4)
# Hisse bazında (OOS): medyan, pozitif oran
st = specs['raw_both']
po = st.loc['2021':]; pi = st.loc[:'2020']
ps = pd.DataFrame({'IS': pi.mean(), 'tIS': pi.apply(vb.tstat), 'OOS': po.mean(), 'tOOS': po.apply(vb.tstat), 'nOOS': po.notna().sum()})
from scipy import stats
ps['pOOS'] = 2 * stats.t.sf(ps.tOOS.abs(), ps.nOOS - 1)
ps['pALL'] = [2 * stats.t.sf(abs(vb.tstat(st[c])), st[c].notna().sum() - 1) for c in ps.index]
print('hisse medyan OOS', ps.OOS.median(), 'pozitif', (ps.OOS > 0).mean(), 'FDR ALL', vb.bh(ps.pALL.values).sum(), 'FDR OOS', vb.bh(ps.pOOS.values).sum())
print('IS medyan', ps.IS.median(), 'IS pozitif', (ps.IS > 0).mean(), 'corr(IS,OOS) hisse', ps[['IS', 'OOS']].corr().iloc[0, 1], 'spearman', ps[['IS','OOS']].corr('spearman').iloc[0,1])
ps.sort_values('OOS').to_csv('res/v1_stock.csv')
print(ps.sort_values('IS', ascending=False).head(10).round(2))
