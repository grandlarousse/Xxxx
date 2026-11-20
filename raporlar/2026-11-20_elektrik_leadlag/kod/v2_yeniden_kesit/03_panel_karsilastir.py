"""V2 (yalniz SONDA karsilastirma): kendi panelimiz ile panel_full'un getirisi ve bayraklari ne kadar ayni?
Kullanim: python3 -I 03_panel_karsilastir.py <WORK_DIR> <PANEL_FULL>"""
import os
import sys
import numpy as np
import pandas as pd

WORK, PF = sys.argv[1], sys.argv[2]
P = pd.read_pickle(os.path.join(WORK, 'v2_panel.pkl'))
rd = lambda n: pd.read_parquet(os.path.join(PF, n + '.parquet'))
cols = list(P['ret'].columns)
ix = P['ret'].index


def al(n, fill=None):
    d = rd(n)
    d.index = pd.to_datetime(d.index)
    d = d.reindex(index=ix, columns=cols)
    return d if fill is None else d.fillna(fill).astype(bool)


R = al('ret_cc')
print('takvim ayni mi:', len(rd('ret_cc')) == len(ix), '| sutun eksigi:', [c for c in cols if c not in rd('ret_cc').columns])
d = (P['ret'] - R).abs()
both = P['ret'].notna() & R.notna()
print('getiri: ortak hucre', int(both.sum().sum()), '| yalniz v2', int((P['ret'].notna() & R.isna()).sum().sum()), '| yalniz panel',
      int((P['ret'].isna() & R.notna()).sum().sum()), '| maks fark bps', round(1e4 * d.max().max(), 3), '| > 1 bps hucre', int((d > 1e-4).sum().sum()),
      '| > 0,01 bps hucre', int((d > 1e-6).sum().sum()))
big = d.stack()
big = big[big > 1e-4].sort_values(ascending=False).head(8)
print('en buyuk getiri farklari:', [(str(i[0].date()), i[1], round(1e4 * v, 1)) for i, v in big.items()])
post = ix >= '2015-12-01'
for a, b in (('lu', 'lim_up'), ('ld', 'lim_dn'), ('tu', 'lim_up_touch'), ('td', 'lim_dn_touch')):
    X, Y = P[a], al(b, False)
    for nm, m in (('tum', np.ones(len(ix), bool)), ('2015-12+', post), ('2023+', ix >= '2023-01-02')):
        print(f'{b:13s} {nm:8s} v2 {int(X[m].sum().sum()):5d} panel {int(Y[m].sum().sum()):5d} | yalniz v2 {int((X & ~Y)[m].sum().sum()):4d} | yalniz panel {int((~X & Y)[m].sum().sum()):4d}')
T0 = al('tradable', False)
ipo = rd('ipo_n'); ipo.index = pd.to_datetime(ipo.index); ipo = ipo.reindex(index=ix, columns=cols)
lu = al('lim_up', False)
Tp = T0 & R.notna() & (ipo > 20) & (((~lu) & R.notna()).cumsum() > 0)
print('tradable (E4 tanimi): v2', int(P['tr'].sum().sum()), 'panel', int(Tp.sum().sum()), '| yalniz v2', int((P['tr'] & ~Tp).sum().sum()),
      '| yalniz panel', int((~P['tr'] & Tp).sum().sum()))
x = (~P['tr'] & Tp).stack(); x = x[x]
print('yalniz panelde tradable ornekler:', [(str(i[0].date()), i[1]) for i in x.index[:12]], '... hisse dagilimi', x.reset_index().iloc[:, 1].value_counts().to_dict())
x = (P['tr'] & ~Tp).stack(); x = x[x]
print('yalniz v2 tradable:', [(str(i[0].date()), i[1]) for i in x.index[:12]])
x = (P['ld'] ^ al('lim_dn', False))[ix >= '2023-01-02'].stack(); x = x[x]
print('2023+ taban kapanis farklari:', [(str(i[0].date()), i[1]) for i in x.index[:12]])
x = (P['lu'] ^ lu)[ix >= '2023-01-02'].stack(); x = x[x]
print('2023+ tavan kapanis farklari:', [(str(i[0].date()), i[1]) for i in x.index[:12]])
