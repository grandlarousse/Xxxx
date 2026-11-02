"""BC sürüklenmesi: t+1 kapanışında açığa satış/VİOP short DOLUMU mümkün mü? t+1 de taban kapanış ise (satıcı kuyruğu) giriş yok sayılır;
ilk 'taban olmayan' kapanışta gir, 4 gün tut (XU100'e göre fazla). Ayrıca kilitli tavan ertesi gap'inin 'alınabilirliği' (TC kilitli ise kapanıştan alım dolmaz)."""
import numpy as np, pandas as pd, alib
E = pd.read_parquet('res_limit_events.parquet'); E = E[E.reg == 'P10'].sort_values(['stock', 'date']).copy()
X = alib.xu('XU100')
g = E.groupby('stock')
E['BC_next'] = g.BC.shift(-1); E['BC_next2'] = g.BC.shift(-2)
E['cc_x'] = E.cc0 - X['cc'].reindex(E.date).values
# t+1 taban değilse: t+1 kapanışında gir, t+2..t+5 (mevcut cc2_5x). t+1 taban ise: t+2 taban değilse t+2 kapanışında gir, t+3..t+6
E['x_lead'] = {k: v for k, v in []} if False else np.nan
for k in [3, 4, 5, 6]: E[f'ccx_f{k}'] = g.cc_x.shift(-k)
E['alt_entry2'] = E[['ccx_f3', 'ccx_f4', 'ccx_f5', 'ccx_f6']].sum(axis=1, min_count=4)
def dayavg(sub, col, sg=-1, cost=15):
    gg = (sg * sub[col] - cost / 1e4).groupby(sub.date).mean().dropna(); m, t, n = alib.nw(gg, 5); return round(1e4 * gg.mean(), 1), round(t, 2), n
for uni, m in [('viop47', E.viop), ('all', E.stock.notna()), ('liqH', E.liq == 'H')]:
    s = E[m & E.BC]
    a = s[s.BC_next == False]; b = s[(s.BC_next == True) & (s.BC_next2 == False)]
    print(uni, 'BC olay', len(s), '| t+1 taban DEĞİL -> t+1 kapanış girişi:', dayavg(a, 'cc2_5x'), 'n', len(a), '| t+1 taban, t+2 değil -> t+2 girişi:', dayavg(b, 'alt_entry2'), 'n', len(b),
          '| IS(<2023)', dayavg(a[a.date < '2023'], 'cc2_5x'), 'OOS', dayavg(a[a.date >= '2023'], 'cc2_5x'))
