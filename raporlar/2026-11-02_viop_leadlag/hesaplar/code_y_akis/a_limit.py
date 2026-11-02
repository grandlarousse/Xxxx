"""1) TAVAN/TABAN günleri -> ertesi gün gap / gün-içi / t+2..5 sürüklenme.
Fiyat limiti rejimleri VERİDEN tespit edildi (177 BIST hissesi, adj oranı R=adj_t/adj_{t-1}):
  - 2015-12 .. 2020-03-10: ±%20 (BISTECH; R=1,19–1,21 yığılması), 2020-03-13'ten beri ±%10 (R=1,095–1,105 yığılması; >1,11 neredeyse sıfır).
  - 2015-11 öncesi: baz fiyat = ağırlıklı ortalama fiyat -> kapanış-kapanış oranı limitle örtüşmüyor (kullanılmadı).
  NOT: ll._bad (±%10,5 dışı = NaN) 2015-12..2020-03 arasında GERÇEK %10,5–20 hareketlerini siliyor (yan bulgu, rapora yazıldı).
Sınıflar (P10 eşik: R>=1,0925 / <=0,9075 ; P20: >=1,185 / <=0,815; tik yuvarlaması toleransı):
  TC = tavan kapanış (R>=eşik & c>=0,999h) ; TCL = kilitli tavan (TC & l>=0,999h) ; TU = tavana dokunup altında kapanış (h-oranı>=eşik & R<eşik-0,01)
  BC/BCL/BU = taban simetriği ; UP6 = R in [1,06, eşik-0,01) & dokunmadı (kontrol) ; DN6 simetriği.
Çıktılar: res_limit_events.parquet (olay düzeyi), res_limit_summary.csv, log_a.txt
"""
import numpy as np, pandas as pd, alib
P = alib.panel(); END = pd.Timestamp('2026-10-30')
X = alib.xu('XU100')
rows = []
for k in P['c'].columns:
    d = pd.DataFrame({f: P[f][k] for f in P}).dropna(subset=['c', 'adj']); d = d[d.index <= END]
    if len(d) < 100: continue
    R = d.adj / d.adj.shift(1); f = d.c / d.adj  # adj->c dönüşümü
    Rh = R * d.h / d.c; Rl = R * d.l / d.c
    tv = (d.c * d.v).rolling(60, min_periods=20).median().shift(1)  # önceki 60g medyan TL hacim (look-ahead yok)
    cc = np.log(R); intra = np.log(d.c / d.o)
    bad_open = (d.o <= 0) | d.o.isna() | ((d.h == d.l) & (d.o == d.c.shift(1)) & (R.sub(1).abs() < 0.09))
    intra[bad_open] = np.nan; gap = cc - intra
    nxt = pd.DataFrame({'cc1': cc.shift(-1), 'gap1': gap.shift(-1), 'intra1': intra.shift(-1),
                        'cc2_5': cc.shift(-2).rolling(4).sum().shift(-3), 'cc2_10': cc.shift(-2).rolling(9).sum().shift(-8),
                        'd1': pd.Series(d.index, index=d.index).shift(-1)})
    age = np.arange(len(d))  # işlem günü yaşı (halka arz etkisi)
    e = pd.DataFrame({'stock': k, 'R': R, 'Rh': Rh, 'Rl': Rl, 'cc0': cc, 'gap0': gap, 'intra0': intra, 'c': d.c, 'h': d.h, 'l': d.l, 'tv': tv, 'age': age}, index=d.index)
    e = pd.concat([e, nxt], axis=1)
    rows.append(e)
E = pd.concat(rows); E.index.name = 'date'; E = E.reset_index()
E['reg'] = np.where(E.date >= alib.P10_START, 'P10', np.where((E.date >= alib.P20_START) & (E.date <= alib.P20_END), 'P20', 'old'))
E = E[E.reg != 'old'].copy()
up = np.where(E.reg == 'P10', 1.0925, 1.185); dn = np.where(E.reg == 'P10', 0.9075, 0.815)
lim_up = E.R <= np.where(E.reg == 'P10', 1.106, 1.206); lim_dn = E.R >= np.where(E.reg == 'P10', 0.894, 0.794)  # bariz kurumsal işlem/veri hatası dışı
E['TC'] = (E.R >= up) & (E.c >= 0.999 * E.h) & lim_up
E['TCL'] = E.TC & (E.l >= 0.999 * E.h)
E['TU'] = (E.Rh >= up) & (E.R < up - 0.01) & (E.Rh <= np.where(E.reg == 'P10', 1.106, 1.206))
E['BC'] = (E.R <= dn) & (E.c <= 1.001 * E.l) & lim_dn
E['BCL'] = E.BC & (E.h <= 1.001 * E.l)
E['BU'] = (E.Rl <= dn) & (E.R > dn + 0.01) & (E.Rl >= np.where(E.reg == 'P10', 0.894, 0.794))
mid = np.where(E.reg == 'P10', 0.06, 0.12)
E['UP6'] = (E.R - 1 >= mid) & (E.Rh < up) & (E.R < up - 0.01)
E['DN6'] = (1 - E.R >= mid) & (E.Rl > dn) & (E.R > dn + 0.01)
E['viop'] = E.stock.isin(alib.VIOP)
E['ipo'] = E.age < 40
# piyasa düzeltmesi
E['gap1x'] = E.gap1 - X['gap'].reindex(E.d1).values; E['intra1x'] = E.intra1 - X['intra'].reindex(E.d1).values; E['cc1x'] = E.cc1 - X['cc'].reindex(E.d1).values
xc = X['cc']; xsum = xc.shift(-2).rolling(4).sum().shift(-3)
E['cc2_5x'] = E.cc2_5 - xsum.reindex(E.date).values
# likidite tercili (yıllık kesitsel)
E['yr'] = E.date.dt.year
E['liq'] = E.groupby('yr').tv.transform(lambda s: pd.qcut(s.rank(method='first'), 3, labels=['L', 'M', 'H']) if s.notna().sum() > 30 else np.nan)
E.to_parquet('res_limit_events.parquet')
cls = ['TC', 'TCL', 'TU', 'UP6', 'BC', 'BCL', 'BU', 'DN6']
out = []
def summ(sub, lab):
    r = {'grp': lab, 'n': len(sub), 'n_days': sub.date.nunique()}
    for v in ['gap1', 'intra1', 'cc1', 'gap1x', 'intra1x', 'cc2_5', 'cc2_5x']:
        m = 1e4 * sub[v].mean(); t, _ = alib.cluster_t(sub, v)
        r[v + '_bps'] = round(m, 1); r[v + '_t'] = round(t, 2)
    r['p_pos_gap1'] = round((sub.gap1 > 0).mean(), 3)
    return r
for reg in ['P10', 'P20']:
    for c_ in cls:
        s = E[(E.reg == reg) & E[c_]]
        out.append(dict(reg=reg, cls=c_, **summ(s, 'all')))
        out.append(dict(reg=reg, cls=c_, **summ(s[~s.ipo], 'no_ipo')))
        out.append(dict(reg=reg, cls=c_, **summ(s[s.viop], 'viop47')))
        for lq in ['L', 'M', 'H']: out.append(dict(reg=reg, cls=c_, **summ(s[s.liq == lq], 'liq_' + lq)))
        if reg == 'P10':
            out.append(dict(reg=reg, cls=c_, **summ(s[s.date < '2023-01-01'], 'IS_2020_22')))
            out.append(dict(reg=reg, cls=c_, **summ(s[s.date >= '2023-01-01'], 'OOS_2023_26')))
S = pd.DataFrame(out); S.to_csv('res_limit_summary.csv', index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 30)
print(S[S.grp.isin(['all', 'no_ipo', 'viop47', 'IS_2020_22', 'OOS_2023_26'])][['reg', 'cls', 'grp', 'n', 'n_days', 'gap1_bps', 'gap1_t', 'intra1_bps', 'intra1_t', 'gap1x_bps', 'intra1x_bps', 'intra1x_t', 'cc2_5x_bps', 'cc2_5x_t', 'p_pos_gap1']].to_string())
# ardışık tavan olasılığı
for reg in ['P10', 'P20']:
    s = E[E.reg == reg]
    nxt_tc = s.groupby('stock').TC.shift(-1); nxt_bc = s.groupby('stock').BC.shift(-1)
    print(reg, 'P(TC)=%.4f P(TC_t+1|TC_t)=%.3f P(TC_t+1|TCL_t)=%.3f P(TC_t+1|TU_t)=%.3f | P(BC)=%.4f P(BC_t+1|BC_t)=%.3f P(BC_t+1|BCL_t)=%.3f' % (
        s.TC.mean(), nxt_tc[s.TC].mean(), nxt_tc[s.TCL].mean(), nxt_tc[s.TU].mean(), s.BC.mean(), nxt_bc[s.BC].mean(), nxt_bc[s.BCL].mean()))
