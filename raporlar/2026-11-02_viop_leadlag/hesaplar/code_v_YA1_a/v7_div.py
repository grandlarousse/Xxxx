"""v_YA1_a — temettü ex-günü (bağımsız). Olay: f=adj/c sıçraması f_t/f_{t-1}-1 in (0,003, 0,35), önceki satır ardışık işlem günü; dy=1-f_{t-1}/f_t, %0,3<dy<%25.
 gap0 = log(o_t / (c_{t-1}(1-dy)))  (açılış vs teorik ex fiyat) ; intra0 = log(c_t/o_t)
 Yahoo ex-tarih doğruluğu: ham kapanış değişimi log(c_t/c_{t-1}) ~ log(1-dy) regresyonu t-1,t,t+1 için (eğim ~1 olan gün gerçek ex günü).
 BT: ex-gün açılışta SAT, kapanışta KAPAT (VİOP47 / tümü), 8/15/30 bps + tik; IS 2014-2020 (2014 öncesi Yahoo açılışı bozuk) / OOS 2021-2026; yıllar.
 Gerçekçi giriş: 10:30 TSİ (h1, 2023-11-30+) ; VİOP vadeli açılış->kapanış (bülten) ; vadeli fiyat düzeltmesi var mı (prev_settle vs önceki uzlaşma).
"""
import numpy as np, pandas as pd, os, sys, glob
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from v0_panel import SCR, index_ret
from v1_events import VIOP
from v2_bt import nw_t
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 40)

def st(x, dates, cost=0, tik=None):
    x = pd.Series(np.asarray(x, float)); d = pd.Series(np.asarray(dates))
    if tik is not None: x = x - np.asarray(tik, float)
    x = x - cost / 1e4
    ok = x.notna().values; x = x[ok]; d = d[ok]
    if len(x) < 8: return dict(n=len(x))
    gm = x.groupby(d.values).mean()
    return dict(n=len(x), trade=round(1e4 * x.mean(), 1), med=round(1e4 * x.median(), 1), t_cl=round(gm.mean() / (gm.std() / np.sqrt(len(gm))), 2), t_nw=round(nw_t(gm), 2), hit=round((x > 0).mean(), 3))

P = pd.read_parquet(HERE + '/_panel.parquet').sort_values(['stock', 'date']).reset_index(drop=True)
cnt = P.groupby('date').size(); nst = P.groupby(P.date.dt.year).stock.nunique()
cal = cnt[cnt >= 0.4 * nst.reindex(cnt.index.year).values].index; cpos = pd.Series(np.arange(len(cal)), index=cal)
P['cp'] = cpos.reindex(P.date).values
g = P.groupby('stock')
P['contig'] = (P.cp - g.cp.shift(1)) == 1
P['f'] = P.adj / P.c
P['jump'] = P.f / g.f.shift(1) - 1
P['dy'] = 1 - g.f.shift(1) / P.f
P['rawcc'] = np.log(P.c / g.c.shift(1))
P['b'] = g.c.shift(1) * (1 - P.dy)
P['gap0'] = np.log(P.o / P.b); P['intra0'] = np.log(P.c / P.o)
P['rawcc_m1'] = g.rawcc.shift(1); P['rawcc_p1'] = g.rawcc.shift(-1)
P['cc'] = np.log(P.adj / g.adj.shift(1))
X = index_ret('XU100'); P['xintra'] = X.intra.reindex(P.date).values
mu = P[(P.date >= '2014-01-01')].groupby('stock').intra0.mean() if False else None
D = P[(P.jump > 0.003) & (P.jump < 0.35) & P.contig & (P.dy > 0.003) & (P.dy < 0.25) & (P.date >= '2010-01-01')].copy()
D['viop'] = D.stock.isin(VIOP); D['yr'] = D.date.dt.year
print('Temettü olayı n', len(D), 'hisse', D.stock.nunique(), '| VİOP47', D.viop.sum(), '| 2014+', (D.date >= '2014').sum())
# Yahoo ex-tarih doğruluğu
for lab, s in [('2014+', D[D.date >= '2014']), ('2021+', D[D.date >= '2021'])]:
    y = np.log(1 - s.dy)
    out = {}
    for c in ['rawcc_m1', 'rawcc', 'rawcc_p1']:
        z = s[[c]].assign(y=y).dropna()
        b = np.polyfit(z.y, z[c], 1)[0]; out[c] = round(b, 2)
    big = s[s.dy >= 0.03]
    hitex = (abs(big.rawcc - np.log(1 - big.dy)) < abs(big.rawcc)).mean()
    print(f'  {lab}: ham getiri ~ log(1-dy) eğimi  t-1:{out["rawcc_m1"]}  t:{out["rawcc"]}  t+1:{out["rawcc_p1"]} | dy>=%3 olaylarda t günü düşüş temettüye daha yakın: {hitex:.3f} (n={len(big)})')
print('\nEx-gün ölçüleri (bps; tarih kümelemeli t):')
for lab, s in [('tümü 2014+', D[D.date >= '2014']), ('VİOP47 2014+', D[(D.date >= '2014') & D.viop]), ('2010-2013 (açılış bozuk?)', D[D.date < '2014']),
               ('IS 2014-2020', D[(D.date >= '2014') & (D.date < '2021')]), ('OOS 2021-2026', D[D.date >= '2021']), ('dy>=%3 2014+', D[(D.date >= '2014') & (D.dy >= 0.03)])]:
    print(f'  {lab:28s} n={len(s):4d} dy_med={100 * s.dy.median():.2f}%  gap0', st(s.gap0, s.date), ' intra0', st(s.intra0, s.date),
          ' intra0=0 oranı', round((s.intra0.abs() < 1e-9).mean(), 3))
# PDR
s = D[D.date >= '2014']; print('  PDR medyan (1-(cc_adj)/dy ... ) =', round(float(np.median(1 - s.cc / s.dy)), 2))
print('\nBT: ex-gün açılışta SAT -> kapanış (işlem başı; tarih kümelemeli t)')
D['tik'] = np.minimum(0.01 / D.c_unadj, 0.02)
rows = []
for uni, um in [('viop47', D.viop), ('tümü', D.stock.notna())]:
    for pn, a, b in [('ALL_2014_26', '2014', '2027'), ('IS_2014_20', '2014', '2021'), ('OOS_2021_26', '2021', '2027'), ('src_IS_2010_20', '2010', '2021'), ('2010_2013', '2010', '2014')]:
        s = D[um & (D.date >= a) & (D.date < b)]
        r = {'uni': uni, 'per': pn}
        for cst in [0, 8, 15, 30]:
            q = st(-s.intra0, s.date, cst); r[f'c{cst}'] = q.get('trade'); r[f't{cst}'] = q.get('t_cl')
        q = st(-s.intra0, s.date, 15, s.tik); r['c15tik'] = q.get('trade'); r['t15tik'] = q.get('t_cl'); r['n'] = q.get('n')
        q = st(-(s.intra0 - s.xintra), s.date, 19); r['xu_neutral19'] = q.get('trade'); r['t_xu19'] = q.get('t_cl')
        rows.append(r)
print(pd.DataFrame(rows).to_string())
for uni, um in [('viop47', D.viop), ('tümü', D.stock.notna())]:
    s = D[um & (D.date >= '2014')]
    print(uni, 'yıllar @15 (işlem başı):', {int(y): st(-q.intra0, q.date, 15).get('trade') for y, q in s.groupby('yr')}, ' n:', s.groupby('yr').size().to_dict())
# koşulsuz gün-içi tabanı aynı hisse-yıl
P['yr'] = P.date.dt.year
base = P[(P.date >= '2014') & P.contig].groupby(['stock', 'yr']).intra0.mean()
D['base'] = base.reindex(pd.MultiIndex.from_arrays([D.stock, D.yr])).values
for uni, um in [('viop47', D.viop), ('tümü', D.stock.notna())]:
    s = D[um & (D.date >= '2014')]
    print(uni, 'aynı hisse-yıl koşulsuz gün-içi düşülmüş fade @15:', st(-(s.intra0 - s.base), s.date, 15), '| OOS:', st(-(s[s.date >= '2021'].intra0 - s[s.date >= '2021'].base), s[s.date >= '2021'].date, 15))
# ---- h1: 10:30 girişi
rows = []
for fp in glob.glob(SCR + '/data/h1/*.IS.parquet'):
    k = os.path.basename(fp)[:-11]
    if k.startswith('X'): continue
    h = pd.read_parquet(fp); h = h[h.index.strftime('%H:%M') == '06:30']
    rows.append(pd.DataFrame({'stock': k, 'date': pd.to_datetime(h.ldate).dt.normalize().values, 'h_o': h.o.values, 'p1030': h.c.values}))
H = pd.concat(rows)
DH = D.merge(H, on=['stock', 'date'], how='inner')
DH = DH[(DH.h_o / DH.o - 1).abs() < 0.002]
print('\nh1 (2023-11-30+) ex-gün olayı n', len(DH), 'VİOP47', DH.viop.sum())
for uni, um in [('viop47', DH.viop), ('h1 tümü', DH.stock.notna())]:
    s = DH[um]
    print(f'  {uni}: açılış->kapanış SAT brüt', st(-s.intra0, s.date), '| açılış->10:30', st(-np.log(s.p1030 / s.o), s.date), '| 10:30->kapanış', st(-np.log(s.c / s.p1030), s.date),
          '| 10:30->kapanış @15+tik', st(-np.log(s.c / s.p1030), s.date, 15, s.tik))
# ---- VİOP vadeli ex-gün
V = pd.read_parquet(SCR + '/data/viop_panel.parquet'); V = V[V.segment == 'SSF'].copy()
for c in ['open', 'high', 'low', 'close']: V.loc[V.qty.fillna(0) <= 0, c] = np.nan
V = V.sort_values(['code', 'date']); V['settle_prev_row'] = V.groupby('code').settle.shift(1)
Dv = D[D.viop & (D.date >= '2017-03-06')][['stock', 'date', 'dy', 'intra0', 'gap0', 'c', 'tik']].copy()
m = Dv.reset_index().merge(V, left_on=['stock', 'date'], right_on=['root', 'date'], how='left')
m = m[m.expiry > m.date].sort_values('expiry').groupby('index').head(1).set_index('index')
Dv = Dv.join(m[['code', 'open', 'close', 'settle', 'prev_settle', 'settle_prev_row', 'qty']])
Dv['adj_ratio'] = Dv.prev_settle / Dv.settle_prev_row
print('\nVİOP vadeli ex-gün: n', len(Dv), 'eşleşen', Dv.code.notna().sum(), '| prev_settle/önceki uzlaşma medyan', round(Dv.adj_ratio.median(), 4), ' vs (1-dy) medyan', round((1 - Dv.dy).median(), 4),
      '| düzeltme yapılmış (|ratio-(1-dy)|<0,3*dy) oranı', round(((Dv.adj_ratio - (1 - Dv.dy)).abs() < 0.3 * Dv.dy).mean(), 3), '| düzeltme yok (|ratio-1|<0,3*dy):', round(((Dv.adj_ratio - 1).abs() < 0.3 * Dv.dy).mean(), 3))
ok = Dv[Dv.qty.fillna(0) > 0]
fint = np.log(ok.close / ok.open)
print('  vadeli açılış->kapanış SAT brüt', st(-fint, ok.date), '| 15+tik', st(-fint, ok.date, 15, 0.01 / ok.open), '| spot aynı olaylar brüt', st(-ok.intra0, ok.date))
for a, b in [('2017', '2021'), ('2021', '2027')]:
    q = ok[(ok.date >= a) & (ok.date < b)]; fq = np.log(q.close / q.open)
    print(f'  {a}-{b}: vadeli 15+tik', st(-fq, q.date, 15, 0.01 / q.open), ' spot 15', st(-q.intra0, q.date, 15))
D.to_parquet(HERE + '/_div.parquet')
