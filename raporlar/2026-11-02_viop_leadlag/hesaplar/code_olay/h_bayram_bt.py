"""Uzun kapanış (bayram) sonrası ilk gün: sign(ES kapanış süresince) -> XU030/XBANK gün-içi (açılışta gir, kapanışta çık)."""
from olib import *
B = pd.read_csv('res_bayram.csv', parse_dates=['react']).set_index('react'); it = comp('intra')
for c in ['XU030', 'XBANK', 'XU100']:
    for cost in [8, 15]:
        p = np.sign(B.es_closure) * it[c].reindex(B.index) - cost / 1e4; p = p.dropna()
        s = ' '.join(f"{lab}:{1e4*p[m].mean():.1f}bps(t{tstat(p[m])[0]:.2f},n{int(m.sum())})" for lab, m in [('IS', p.index < '2021-01-01'), ('OOS', p.index >= '2021-01-01'), ('ALL', p.index.notna())])
        print(c, cost, s)
