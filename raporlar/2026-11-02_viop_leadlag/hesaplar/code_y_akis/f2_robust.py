"""Sağlamlık: (1) BC t+2..5 sürüklenmesi kriz kümelerinden mi? (2) Temettü ex-günü açılış verisi güvenilir mi (h1 ilk bar vs günlük açılış)? (3) TC fade: kriz hariç / yıl kırılımı"""
import numpy as np, pandas as pd, alib, json
from alib import ll
E = pd.read_parquet('res_limit_events.parquet'); E = E[E.reg == 'P10']
crisis = [('2020-03-01', '2020-04-30'), ('2021-12-01', '2021-12-31'), ('2023-02-06', '2023-02-28'), ('2025-03-18', '2025-04-15'), ('2026-09-01', '2026-10-31')]
cm = pd.Series(False, index=E.index)
for a, b in crisis: cm |= (E.date >= a) & (E.date <= b)
E['crisis'] = cm
def dayavg(sub, col, sg):
    g = (sg * sub[col]).groupby(sub.date).mean().dropna(); m, t, n = alib.nw(g, 5); return round(1e4 * g.mean(), 1), round(t, 2), n
for nm, cls, col, sg in [('BC_short_t2_5x', 'BC', 'cc2_5x', -1), ('TC_fade_intra', 'TC', 'intra1', -1), ('TU_fade_intra', 'TU', 'intra1', -1), ('BCL_long_intra', 'BCL', 'intra1', 1)]:
    for uni, m in [('viop47', E.viop), ('all', E.stock.notna())]:
        s = E[m & E[cls]]
        print(nm, uni, 'tümü', dayavg(s, col, sg), '| kriz hariç', dayavg(s[~s.crisis], col, sg), '| sadece kriz', dayavg(s[s.crisis], col, sg),
              '| yıllar', (1e4 * (sg * s[col]).groupby(s.date.dt.year).mean()).round(0).to_dict())
# kalabalık günler (aynı gün >=10 olay) hariç
for cls, col, sg in [('BC', 'cc2_5x', -1), ('TC', 'intra1', -1)]:
    s = E[E[cls]]; cnt = s.groupby('date').stock.transform('count')
    print(cls, 'aynı gün <5 olay olan günler:', dayavg(s[cnt < 5], col, sg), 'n_olay', int((cnt < 5).sum()))
# (2) Temettü ex-günü: h1 ilk barın açılışı vs Yahoo günlük açılış (VİOP hisseleri, 2023-11+)
T = pd.read_csv('res_div_events.csv', parse_dates=['date']); T = T[(T.dy > 0.003) & (T.dy < 0.25) & (T.date >= '2023-11-15') & T.viop]
P = alib.panel(); rows = []
for _, e in T.iterrows():
    try: h = ll.raw(e.stock + '.IS', 'h1')
    except Exception: continue
    hd = h[h.index.tz_convert(None).normalize() == e.date]
    if not len(hd): continue
    o_d = P['o'][e.stock].get(e.date); c_prev = P['c'][e.stock].shift(1).get(e.date); c_d = P['c'][e.stock].get(e.date)
    rows.append(dict(stock=e.stock, date=e.date.date(), dy=round(100 * e.dy, 2), o_daily=o_d, o_h1=hd.o.iloc[0], c_prev=c_prev, c=c_d, intra0_bps=round(1e4 * e.intra0),
                     h1_first_bar_ret_bps=round(1e4 * np.log(hd.c.iloc[0] / hd.o.iloc[0])), rest_of_day_bps=round(1e4 * np.log(c_d / hd.c.iloc[0]))))
R = pd.DataFrame(rows); pd.set_option('display.width', 250)
print(R.to_string()); print('o_daily==o_h1 oranı', (np.isclose(R.o_daily, R.o_h1, rtol=1e-3)).mean(), 'ort intra0', R.intra0_bps.mean(), 'ilk saat', R.h1_first_bar_ret_bps.mean(), 'gün kalanı', R.rest_of_day_bps.mean())
# açılış == önceki kapanış (düzeltilmemiş açılış şüphesi) oranı tüm temettü olaylarında
T2 = pd.read_csv('res_div_events.csv', parse_dates=['date']); T2 = T2[(T2.dy > 0.003) & (T2.dy < 0.25)]
susp = []
for _, e in T2.iterrows():
    o = P['o'][e.stock].get(e.date); cp = P['c'][e.stock].shift(1).get(e.date); susp.append(abs(o / cp - 1) < 0.001 if (o and cp) else np.nan)
T2['open_eq_prevclose'] = susp
print('açılış≈önceki kapanış (düzeltilmemiş) olay oranı', T2.open_eq_prevclose.mean(), 'bu olaylarda intra0 ort', 1e4 * T2[T2.open_eq_prevclose == True].intra0.mean(), 'diğerleri', 1e4 * T2[T2.open_eq_prevclose == False].intra0.mean(), 'n diğer', int((T2.open_eq_prevclose == False).sum()))
print('diğerleri IS/OOS intra0:', 1e4 * T2[(T2.open_eq_prevclose == False) & (T2.date < '2021')].intra0.mean(), 1e4 * T2[(T2.open_eq_prevclose == False) & (T2.date >= '2021')].intra0.mean())
