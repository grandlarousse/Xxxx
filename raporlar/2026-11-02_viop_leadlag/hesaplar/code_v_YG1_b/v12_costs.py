"""v12: maliyet sonrası net (gidiş-dönüş): taban 8 / 15 / kademeli (likit 8, illikit 20) + 1 tik (0,01 TL / 30.10.2026 fiyatı) + hedge 3 bps (hedge'li stratejilerde)."""
import numpy as np, pandas as pd, vb
fr = pd.read_pickle('res/panel.pkl'); S = vb.S47
G = vb.wide(fr, 'gap')['2014':][S]; I = vb.wide(fr, 'intra')['2014':][S]
B = pd.read_pickle('res/basket.pkl'); gbl, ibl = B['gbl'].reindex(G.index), B['ibl'].reindex(G.index)
liq = pd.read_csv('res/liq.csv', index_col=0).iloc[:, 0]
last = pd.Series({s: fr[s].c.iloc[-1] for s in S}); tick = 0.01 / last * 1e4
h1 = pd.read_pickle('res/h1.pkl'); L = h1['legs']; Hd = h1['Hd']
def costmat(cols, base, hedge):
    if base == 'tier': b = pd.Series({s: (8 if liq[s] == 'LIQ' else 20) for s in cols})
    else: b = pd.Series(float(base), index=cols)
    return b + tick[cols] + (3 if hedge else 0)
def net(sig, ret, base, hedge, a, b):
    r = (sig * ret * 1e4).loc[a:b]
    c = costmat(r.columns, base, hedge)
    n = r - sig.loc[a:b].abs() * c
    d = n.mean(axis=1).dropna(); st = n.stack().dropna(); m, t, _ = vb.clus_t(st.values, st.index.get_level_values(0))
    return f'{d.mean():6.1f} ({vb.tstat(d):4.1f}) / {m:6.1f} ({t:4.1f})'
cases = [
 ('47 ham both, E0->C, OOS 21-26', -np.sign(G).where(G.abs() > 0.01), I, False, '2021', '2026'),
 ('47 idio-UP sepet-hedge, E0->C, OOS 21-26', -np.sign(G - gbl).where((G - gbl) > 0.01), I - ibl, True, '2021', '2026'),
 ('47 idio-UP sepet-hedge, E0->C, 24-26', -np.sign(G - gbl).where((G - gbl) > 0.01), I - ibl, True, '2024', '2026'),
]
g0 = h1['G']; i0 = h1['IDG0']; g1 = h1['IDG1']
for k, nm in [('O_C', 'E0'), ('TP0_C', 'VWAP30 vekili'), ('1030_C', '10:30')]:
    cases.append((f'h1 47 ham both, {nm}->C', -np.sign(g0).where(g0.abs() > 0.01), L[k], False, '2023-11-30', '2026'))
for k, nm in [('O_C', 'E0'), ('TP0_C', 'VWAP30 vekili'), ('1030_C', '10:30')]:
    cases.append((f'h1 idio-UP sepet-hedge, {nm}->C', -np.sign(i0).where(i0 > 0.01), Hd[k], True, '2023-11-30', '2026'))
cases.append(('h1 idio-UP, sinyal@10:30, 10:30->C', -np.sign(g1).where(g1 > 0.01), Hd['1030_C'], True, '2023-11-30', '2026'))
for s in ['CIMSA', 'OYAKC']:
    cases.append((f'{s} E0->C OOS', -np.sign(G[[s]]).where(G[[s]].abs() > 0.01), I[[s]], False, '2021', '2026'))
    cases.append((f'{s} h1 VWAP30->C', -np.sign(g0[[s]]).where(g0[[s]].abs() > 0.01), L['TP0_C'][[s]], False, '2023-11-30', '2026'))
    cases.append((f'{s} h1 VWAP30->C 2025-05+', -np.sign(g0[[s]]).where(g0[[s]].abs() > 0.01), L['TP0_C'][[s]], False, '2025-05-01', '2026'))
print('DW (t) / TW (t)   | brüt | 8+tik | 15+tik | kademeli 8/20+tik')
for nm, sg, r, hed, a, b in cases:
    gross = (sg * r * 1e4).loc[a:b]; d = gross.mean(axis=1).dropna(); st = gross.stack().dropna(); m, t, _ = vb.clus_t(st.values, st.index.get_level_values(0))
    print(f'{nm:45s} | {d.mean():6.1f} ({vb.tstat(d):4.1f}) / {m:6.1f} ({t:4.1f}) | {net(sg, r, 0, hed, a, b) if False else net(sg, r, 8, hed, a, b)} | {net(sg, r, 15, hed, a, b)} | {net(sg, r, "tier", hed, a, b)}')
print('tik bps:', tick.sort_values(ascending=False).head(6).round(1).to_dict(), 'CIMSA', round(tick['CIMSA'], 1), 'OYAKC', round(tick['OYAKC'], 1))
