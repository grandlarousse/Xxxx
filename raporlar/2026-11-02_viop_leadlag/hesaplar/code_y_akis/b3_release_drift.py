"""Yayın günü: 11:30 (yayın) sonrası hangi pencerede fiyatlanıyor? 11:30->12:30 (ilk saat), 12:30->kapanış (işlenebilir sürüklenme), backtest."""
import numpy as np, pandas as pd, alib
from alib import ll
W = pd.read_csv('res_flow_weekly.csv', parse_dates=['fri', 'D']).set_index('fri').dropna(subset=['D', 'fz'])
for sym in ['XU030.IS', 'XBANK.IS']:
    s = {h: ll.snap_daily(sym, h) for h in ['11:30', '12:30', '13:30', '15:15']}
    m = pd.DataFrame(index=W.index); m['fz'] = W.fz
    m['r1'] = np.log(s['12:30'] / s['11:30']).reindex(W.D).values
    m['r2'] = np.log(s['15:15'] / s['12:30']).reindex(W.D).values
    m['r3'] = np.log(s['15:15'] / s['13:30']).reindex(W.D).values
    m = m.dropna()
    print(sym, 'n', len(m), 'corr fz~[11:30-12:30] %.3f  [12:30-kapanış] %.3f  [13:30-kapanış] %.3f' % tuple(m[['fz', c]].corr().iloc[0, 1] for c in ['r1', 'r2', 'r3']))
    for c in ['r2', 'r3']:
        for cost in [8, 15]:
            pos = np.sign(m.fz); pnl = pos * m[c] - cost / 1e4
            t = pnl.mean() / pnl.std() * np.sqrt(len(pnl))
            h1 = pnl[m.index < '2025-05-01']; h2 = pnl[m.index >= '2025-05-01']
            print('  BT', c, 'cost', cost, 'mean %.1f bps t %.2f hit %.2f | yarı1 %.1f yarı2 %.1f' % (1e4 * pnl.mean(), t, (pnl > 0).mean(), 1e4 * h1.mean(), 1e4 * h2.mean()))
    m2 = m[m.index < '2026-09-01']; print('  fon krizi hariç corr r2 %.3f n %d' % (m2[['fz', 'r2']].corr().iloc[0, 1], len(m2)))
