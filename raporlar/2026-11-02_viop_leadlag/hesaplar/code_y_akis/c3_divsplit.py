"""Temettü ex-günü (Yahoo adj/c oranındaki sıçrama) ve bedelsiz (Yahoo split olayları) -> fiyat yolu.
Temettü: f=adj/c; ex günü t: f_t/f_{t-1}-1 > 0,3% ; brüt verim d = 1 - f_{t-1}/f_t.
  ex-günü 'düzeltilmiş' getiri r_adj (= fiyat düşüşü - temettü) > 0 ise fiyat temettüden AZ düşüyor (stopaj / vergi etkisi; Elton-Gruber).
  Ayrıca t-5..t-1 (temettü öncesi) ve t+1..t+5 (sonrası) XU100'e göre fazla getiri.
Bedelsiz: ex günü (Yahoo split tarihi). Pencereler: [-20,-1], [0], [+1,+5], [+1,+20] fazla getiri (adj bazlı, split düzeltmeli).
"""
import numpy as np, pandas as pd, json, glob, os, alib
from alib import ll
P = alib.panel(); X = alib.xu('XU100'); xcc = X['cc']
END = pd.Timestamp('2026-10-30')
rows = []
for k in P['c'].columns:
    d = pd.DataFrame({f: P[f][k] for f in P}).dropna(subset=['c', 'adj']); d = d[(d.index <= END) & (d.index >= '2010-01-01')]
    if len(d) < 300: continue
    f = d.adj / d.c; jump = f / f.shift(1) - 1
    cc = np.log(d.adj).diff(); intra = np.log(d.c / d.o); gap = cc - intra
    ex = cc - xcc.reindex(d.index)
    for t in d.index[(jump > 0.003) & (jump < 0.35)]:
        i = d.index.get_loc(t)
        if i < 25 or i + 21 >= len(d): continue
        dy = 1 - f.iloc[i - 1] / f.iloc[i]
        rows.append(dict(stock=k, date=t, dy=dy, r_adj=cc.iloc[i], ex0=ex.iloc[i], gap0=gap.iloc[i], intra0=intra.iloc[i],
                         pre5=ex.iloc[i - 5:i].sum(), post5=ex.iloc[i + 1:i + 6].sum(), post20=ex.iloc[i + 1:i + 21].sum(),
                         pre1=ex.iloc[i - 1], viop=k in alib.VIOP))
T = pd.DataFrame(rows); T.to_csv('res_div_events.csv', index=False)
T = T[(T.dy > 0.003) & (T.dy < 0.25)]
print('Temettü olayı n', len(T), 'hisse', T.stock.nunique())
def sm(sub, lab):
    o = dict(set=lab, n=len(sub), dy_med_pct=round(100 * sub.dy.median(), 2))
    for v in ['r_adj', 'ex0', 'gap0', 'intra0', 'pre1', 'pre5', 'post5', 'post20']:
        o[v + '_bps'] = round(1e4 * sub[v].mean(), 1); o[v + '_t'] = round(alib.cluster_t(sub, v)[0], 2)
    # fiyat düşüş oranı (ex-gün kapanış-kapanış fiyat düşüşü / temettü): PDR = 1 - r_adj/dy yaklaşık
    o['PDR_med'] = round(float(np.median(1 - sub.r_adj / sub.dy)), 2)
    return o
out = [sm(T, 'all'), sm(T[T.viop], 'viop47'), sm(T[T.date < '2021'], 'IS_2010_20'), sm(T[T.date >= '2021'], 'OOS_2021_26'),
       sm(T[T.dy >= 0.03], 'dy>=3%'), sm(T[(T.dy >= 0.03) & T.viop], 'viop47_dy>=3%')]
S = pd.DataFrame(out); pd.set_option('display.width', 250); pd.set_option('display.max_columns', 40)
print(S.to_string()); S.to_csv('res_div_summary.csv', index=False)
# yıllara göre ex-gün düzeltilmiş getiri
print((1e4 * T.groupby(T.date.dt.year).r_adj.mean()).round(1).to_dict())
# ---- Bedelsiz
sp = []
for fpath in glob.glob(alib.SCR + '/data/meta/*.IS.json'):
    m = json.load(open(fpath)); k = os.path.basename(fpath)[:-8]
    for dt, ratio in (m.get('splits') or {}).items():
        try: a, b = ratio.split(':'); rr = float(a) / float(b)
        except Exception: continue
        sp.append(dict(stock=k, date=pd.Timestamp(dt), ratio=rr))
SP = pd.DataFrame(sp); SP = SP[(SP.ratio > 1.05) & (SP.date >= '2010-01-01')]
rows = []
for _, e in SP.iterrows():
    if e.stock not in P['c'].columns: continue
    d = pd.DataFrame({f: P[f][e.stock] for f in P}).dropna(subset=['c', 'adj']); d = d[d.index <= END]
    cc = np.log(d.adj).diff(); ex = cc - xcc.reindex(d.index)
    pos = d.index.searchsorted(e.date)
    if pos < 25 or pos + 21 >= len(d) or abs((d.index[pos] - e.date).days) > 4: continue
    bad = (cc.iloc[pos - 20:pos + 21].abs() > 0.25).any()  # ayarlanmamış split sıçraması
    rows.append(dict(stock=e.stock, date=d.index[pos], ratio=e.ratio, bad=bad, pre20=ex.iloc[pos - 20:pos].sum(), pre5=ex.iloc[pos - 5:pos].sum(), ex0=ex.iloc[pos],
                     post5=ex.iloc[pos + 1:pos + 6].sum(), post20=ex.iloc[pos + 1:pos + 21].sum(), viop=e.stock in alib.VIOP))
B = pd.DataFrame(rows); B.to_csv('res_bedelsiz_events.csv', index=False)
B = B[~B.bad]
o = []
for lab, sub in [('all', B), ('viop47', B[B.viop]), ('IS_2010_20', B[B.date < '2021']), ('OOS_2021_26', B[B.date >= '2021'])]:
    r = dict(set=lab, n=len(sub))
    for v in ['pre20', 'pre5', 'ex0', 'post5', 'post20']:
        r[v + '_bps'] = round(1e4 * sub[v].mean(), 1); r[v + '_t'] = round(alib.tstat(sub[v])[0], 2); r[v + '_med'] = round(1e4 * sub[v].median(), 1)
    o.append(r)
print(pd.DataFrame(o).to_string()); pd.DataFrame(o).to_csv('res_bedelsiz_summary.csv', index=False)
