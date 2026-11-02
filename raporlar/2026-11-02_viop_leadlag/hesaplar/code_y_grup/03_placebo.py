"""Plasebo null: grup bağı OLMAYAN rastgele BIST hisse çiftlerinde aynı lead-lag testleri.
Soru: grup çiftlerindeki öncülük, genel 'büyük/likit -> küçük/illikit' gecikmesinden (Lo-MacKinlay) fazla mı?"""
from gx import *
import importlib.util
spec = importlib.util.spec_from_file_location('p2', HERE + '/02_pairs.py'); p2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(p2)
cat = pd.read_csv(SCR + '/data/catalog.csv')
U = [s.replace('.IS', '') for s in cat[cat.group.isin(['VIOP', 'BIST_other'])].sym if not s.startswith('X')]
grp_of = {}
for a, b, g, t in PAIRS: grp_of.setdefault(a, set()).add(g); grp_of.setdefault(b, set()).add(g)
liqd = {}
for s in U:
    try:
        tl, z = liq(s, '2021-01-01'); liqd[s] = tl
    except Exception: pass
U = [s for s in U if s in liqd and R(s).dropna().index.min() < pd.Timestamp('2019-01-01')]
rows = []
import random as rnd; rnd.seed(7)
pairs = set()
while len(pairs) < 500:
    a, b = rnd.sample(U, 2)
    if grp_of.get(a, set()) & grp_of.get(b, set()): continue
    pairs.add((a, b))
for i, (x, y) in enumerate(sorted(pairs)):
    try:
        o = p2.lead_stats(x, y, '')
        o.update(dict(x=x, y=y, liq_x=liqd[x], liq_y=liqd[y]))
        A, B = R(x), R(y); df = pd.concat([A, B, R('XU100')], axis=1).dropna(); df = df[df.index >= '2010-01-01']
        o['pc'] = ll.partial_corr(df.iloc[:, 0], df.iloc[:, 1], [df.iloc[:, 2]])[0]
        rows.append(o)
    except Exception as e: print('ERR', x, y, e)
    if i % 50 == 0: print(i, flush=True)
P = pd.DataFrame(rows); P.to_csv(HERE + '/res_placebo.csv', index=False)
for c in ['l1_cc_t', 'l1_gap_t', 'l1_intra_t', 'g2i_t']:
    v = P[c].dropna(); print(c, 'n', len(v), 'mean', round(v.mean(), 2), 'sd', round(v.std(), 2), '%|t|>2', round((v.abs() > 2).mean(), 3), '%t>2', round((v > 2).mean(), 3), 'q95', round(v.quantile(.95), 2), 'q99', round(v.quantile(.99), 2))
