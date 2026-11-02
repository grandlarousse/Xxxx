"""Yayın günü (Perşembe 11:30 UTC sonrası) tepkisi gerçek mi? Plasebo: aynı haftanın diğer günlerinde 11:30->kapanış. XU030/XBANK saatlik (2023-11+)."""
import numpy as np, pandas as pd, alib
from alib import ll
W = pd.read_csv('res_flow_weekly.csv', parse_dates=['fri', 'D']).set_index('fri')
cal = ll.bist_cal()
for sym in ['XU030.IS', 'XBANK.IS', 'XU100.IS']:
    p1130 = ll.snap_daily(sym, '11:30'); p1500 = ll.snap_daily(sym, '15:15'); p0700 = ll.snap_daily(sym, '07:30')
    rA = np.log(p1500 / p1130); rB = np.log(p1130 / p0700)
    out = {}
    for off in [-3, -2, -1, 0, 1, 2]:
        dd = []
        for fri, w in W.dropna(subset=['D']).iterrows():
            i = cal.searchsorted(w.D) + off
            if 0 <= i < len(cal): dd.append((fri, cal[i]))
        m = pd.DataFrame(dd, columns=['fri', 'day']).set_index('fri')
        m['rA'] = rA.reindex(m.day).values; m['rB'] = rB.reindex(m.day).values; m['fz'] = W.fz
        m = m.dropna()
        out[off] = dict(n=len(m), corr_after1130=round(m[['fz', 'rA']].corr().iloc[0, 1], 3), corr_morning=round(m[['fz', 'rB']].corr().iloc[0, 1], 3))
    print(sym, pd.DataFrame(out).T.to_string())
