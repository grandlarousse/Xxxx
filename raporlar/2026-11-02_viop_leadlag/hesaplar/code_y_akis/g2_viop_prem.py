"""Taban/tavan günü VİOP vadeli-spot prim sinyalinin kantilleri ve işlenebilir test (spot kapanış fiyatından işlem seansında giriş, ertesi açılışta çıkış)."""
import numpy as np, pandas as pd, alib
V = pd.read_csv('res_viop_limit.csv', parse_dates=['date']); V['prem'] = np.log(V.fut_settle_chg) - np.log(V.spot_R)
for cls in ['BC', 'TC']:
    s = V[(V.cls == cls)].dropna(subset=['prem', 'gap1']).copy()
    s['q'] = pd.qcut(s.prem.rank(method='first'), 5, labels=False)
    t = s.groupby('q').agg(n=('gap1', 'size'), prem_bps=('prem', lambda x: 1e4 * x.mean()), gap1_bps=('gap1', lambda x: 1e4 * x.mean()), intra1_bps=('intra1', lambda x: 1e4 * x.mean()),
                           cc1_bps=('cc1', lambda x: 1e4 * x.mean()), locked=('locked', 'mean')).round(1)
    print(cls); print(t.to_string())
    for per, a, b in [('IS<2023', '2020', '2022-12-31'), ('OOS>=2023', '2023', '2027')]:
        z = s[(s.date >= a) & (s.date <= b)]; print('  ', per, 'n', len(z), 'corr(prem,gap1)=%.2f' % z.prem.corr(z.gap1), 'corr(prem,cc1)=%.2f' % z.prem.corr(z.cc1))
    # rank IC tarih kümelenmiş
    ic = s.groupby('date').apply(lambda g: g.prem.corr(g.gap1, method='spearman') if len(g) >= 3 else np.nan).dropna()
    print('   tarih içi Spearman IC ort %.2f (n gün %d, t %.2f)' % (ic.mean(), len(ic), alib.tstat(ic)[0]))
