"""Açığa satış yasağı rejimi (yaklaşık; haber kaynaklı): 2025-03-24..2025-08-29 ve 2026-03-02..2026-06-26. BC sürüklenmesi ve TC/TU fade yasak döneminde farklı mı?"""
import numpy as np, pandas as pd, alib
E = pd.read_parquet('res_limit_events.parquet'); E = E[E.reg == 'P10'].sort_values(['stock', 'date']).copy()
E['BC_next'] = E.groupby('stock').BC.shift(-1)
ban = ((E.date >= '2025-03-24') & (E.date <= '2025-08-29')) | ((E.date >= '2026-03-02') & (E.date <= '2026-06-26'))
E['ban'] = ban
def da(sub, col, sg):
    g = (sg * sub[col]).groupby(sub.date).mean().dropna(); return round(1e4 * g.mean(), 1), round(alib.nw(g, 5)[1], 2), len(g)
for nm, m, col, sg in [('BC t+1 kapanış girişli short t2_5x (dolum mümkün)', E.BC & (E.BC_next == False), 'cc2_5x', -1), ('TC fade intra1', E.TC, 'intra1', -1), ('TU fade intra1', E.TU, 'intra1', -1)]:
    s = E[m & (E.date >= '2023-01-01')]
    print(nm, '| yasak', da(s[s.ban], col, sg), '| yasak dışı (2023+)', da(s[~s.ban], col, sg))
