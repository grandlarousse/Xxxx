"""1b) Endeks devre kesici (EBDKS) günleri ve 3) 2026 fon krizi.
EBDKS adayları VERİDEN: XU100 gün-içi dip / önceki kapanış <= -5% (2020-02 sonrası; 5/7 eşikli sistem, sonra tek eşik %6 (tarih doğrulanamadı)).
Fon krizi: 'tasfiye hisseleri' (borsaningundemi: fonların fiili dolaşımdaki payı en yüksek 10 hisse) vs 47 VİOP vs diğer BIST.
Kriz takvimi (Gedik 05.10.2026 Tablo 3 + olay ajanı): 11.09 fiili dolaşım yöntemi; 15.09 Pusula temerrüdü; 16.09 -%5,5 + EBDKS; 17.09 SPK 131 fon tasfiye;
21.09 tasfiye süresi 6 ay; 22.09 BIST50 yukarı adım; 30.09 ara ödeme kararı; 02.10 kredili %20 esnekliğin sonu (uzatıldı mı belirsiz); 27.10 7596 sayılı Kanun.
"""
import numpy as np, pandas as pd, alib
from alib import ll
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 40)
d = ll.raw('XU100.IS').copy(); d.index = pd.DatetimeIndex(d['ldate'].values); d = d[~d.index.duplicated(keep='last')]
pc = d.c.shift(1); low = d.l / pc - 1; cc = np.log(d.adj).diff(); intra = np.log(d.c / d.o); gap = cc - intra
cb = d[(low <= -0.05) & (d.index >= '2020-02-01')].index
print('EBDKS aday günleri (XU100 gün-içi dip <= -%5):')
rows = []
for t in cb:
    i = d.index.get_loc(t)
    r = dict(date=t.date(), low_pct=round(100 * low.iloc[i], 2), close_pct=round(100 * (np.exp(cc.iloc[i]) - 1), 2), gap0=round(1e4 * gap.iloc[i]),
             gap1=round(1e4 * gap.iloc[i + 1]) if i + 1 < len(d) else np.nan, intra1=round(1e4 * intra.iloc[i + 1]) if i + 1 < len(d) else np.nan,
             cc1=round(1e4 * cc.iloc[i + 1]) if i + 1 < len(d) else np.nan, cc2_5=round(1e4 * cc.iloc[i + 2:i + 6].sum()) if i + 6 < len(d) else np.nan,
             cc1_20=round(1e4 * cc.iloc[i + 1:i + 21].sum()) if i + 21 < len(d) else np.nan, rebound_close_vs_low=round(1e4 * np.log(d.c.iloc[i] / d.l.iloc[i])))
    rows.append(r)
C = pd.DataFrame(rows); print(C.to_string())
C.to_csv('res_circuit_breaker.csv', index=False)
for v in ['gap1', 'intra1', 'cc1', 'cc2_5', 'cc1_20']:
    x = C[v].dropna(); print(v, 'ort %.0f bps, medyan %.0f, t %.2f, n %d, pozitif %d' % (x.mean(), x.median(), alib.tstat(x)[0], len(x), (x > 0).sum()))
# Kontrol: XU100 kapanış <= -%4 olan ama dip > -%5 olan günler (devre kesici çalışmayan büyük düşüşler)
ctrl = d[(np.exp(cc) - 1 <= -0.04) & (low > -0.05) & (d.index >= '2020-02-01')].index
cc1c = [cc.iloc[d.index.get_loc(t) + 1] for t in ctrl if d.index.get_loc(t) + 1 < len(d)]
print('Kontrol (kapanış<=-4%, dip>-5%) n', len(cc1c), 'ertesi gün cc ort %.0f bps' % (1e4 * np.mean(cc1c)))
# ---------------- Fon krizi kesiti
P = alib.panel()
TAS = ['TEHOL', 'ANELE', 'TRHOL', 'OZATD', 'PEKGY', 'IEYHO', 'DSTKF', 'ISKPL', 'SELEC', 'BIGEN']
def rr(s):
    x = ll.raw(s + '.IS').copy(); x.index = pd.DatetimeIndex(x['ldate'].values); x = x[~x.index.duplicated(keep='last')]; x = x[x.v.fillna(0) > 0]
    return np.log(x.adj).diff(), (x.c * x.v)
win = {'pre_Aug28_Sep11': ('2026-08-28', '2026-09-11'), 'Sep11_Sep16': ('2026-09-11', '2026-09-16'), 'Sep16_Sep17': ('2026-09-16', '2026-09-17'),
       'Sep17_Sep30': ('2026-09-17', '2026-09-30'), 'Sep30_Oct30': ('2026-09-30', '2026-10-30'), 'crisis_Sep11_Oct30': ('2026-09-11', '2026-10-30')}
allsyms = list(dict.fromkeys(TAS + list(P['c'].columns)))
rows = []
for s in allsyms:
    try: r, tv = rr(s)
    except Exception: continue
    o = dict(stock=s, grp='tasfiye10' if s in TAS else ('viop47' if s in alib.VIOP else 'other_bist'))
    for k, (a, b) in win.items():
        x = r[(r.index > a) & (r.index <= b)]; o[k] = np.exp(x.sum()) - 1 if len(x) else np.nan
    pre = r[(r.index > '2025-09-01') & (r.index <= '2026-08-28')]
    o['ret_12m_pre'] = np.exp(pre.sum()) - 1; o['vol_pre'] = pre.std() * np.sqrt(252)
    o['tv_pre_mn'] = tv[(tv.index > '2026-06-01') & (tv.index <= '2026-08-28')].median() / 1e6
    rows.append(o)
K = pd.DataFrame(rows); K.to_csv('res_fundcrisis_xsec.csv', index=False)
print(K.groupby('grp')[list(win) + ['ret_12m_pre']].median().mul(100).round(1).to_string())
print(K.groupby('grp').size())
# Ön-kriz özellikleri kriz getirisini açıklıyor mu? (büyük artış/yüksek oynaklık/küçük hacim = 'fon hisseleri' özellikleri)
import statsmodels.api as sm
Z = K.dropna(subset=['crisis_Sep11_Oct30', 'ret_12m_pre', 'vol_pre', 'tv_pre_mn']).copy()
Z['l_tv'] = np.log(Z.tv_pre_mn); Z['tas'] = (Z.grp == 'tasfiye10').astype(float); Z['y'] = np.log1p(Z.crisis_Sep11_Oct30)
m = sm.OLS(Z.y, sm.add_constant(Z[['ret_12m_pre', 'vol_pre', 'l_tv', 'tas']].assign(ret_12m_pre=np.log1p(Z.ret_12m_pre)))).fit(cov_type='HC1')
print(m.summary().tables[1])
# Günlük öncülük: tasfiye sepeti (eşit ağırlık) ve 'küçük-büyük' (XUTUM-XU030?) -> ertesi gün XU030 / 47 hisse; kriz dönemi vs önceki 2 yıl
bask = pd.concat([rr(s)[0].rename(s) for s in TAS], axis=1)
bask = bask[bask.index >= '2024-01-01'].mean(axis=1)
x30 = ll.ret('XU030.IS'); sml = (ll.ret('XYUZO.IS') - x30)
for lab, a, b in [('2024-01..2026-08', '2024-01-01', '2026-08-31'), ('kriz 2026-09-01..10-30', '2026-09-01', '2026-10-30')]:
    df = pd.concat([bask.rename('b'), x30.rename('x30'), sml.rename('sml')], axis=1).loc[a:b]
    print(lab, 'n', len(df), 'corr(sepet_t, XU030_t)=%.2f  corr(sepet_{t-1}, XU030_t)=%.2f  corr(XU030_{t-1}, sepet_t)=%.2f  corr(XYUZO-XU030_{t-1}, XU030_t)=%.2f' % (
        df.b.corr(df.x30), df.b.shift(1).corr(df.x30), df.x30.shift(1).corr(df.b), df.sml.shift(1).corr(df.x30)))
