"""K1 analiz 2: panel tablosu (2024-06+): ayni saatte olculen degisimlerin korelasyonu, tazelik, artik korelasyonu, vade sicramasi."""
import numpy as np, pandas as pd
SCR = '/tmp/claude-0/-home-user-Xxxx/e31e33e0-f360-5bc6-a008-2cee330297de/scratchpad'
OUT = '/home/user/Xxxx/raporlar/2026-11-10_altin_panel_denetimi/hesap/K1'
log = open(OUT + '/panel.log', 'w')
def L(*a):
    s = ' '.join(str(x) for x in a); print(s); log.write(s + '\n')
P = pd.read_pickle(SCR + '/k1_panel.pkl'); idx = P.index
S = P[(idx >= '2024-06-20') & (~P['arife']) & (~P['lock'])].copy()
C = pd.DataFrame(index=S.index)
C['g_F_XAUUSD'] = S['r_XAU']
C['GC_14:00 anlik'] = np.log(S['gc14'] / S['gc_prevclose'])
for s in ['GLD', 'PHYS', 'GDX', 'GDXJ']:
    C[s + '_14:30 anlik'] = np.log(S['o1430_' + s] / S['close_' + s])
C['r_F_TRALT'] = S['r_TRALT']; C['r_F_TRMET'] = S['r_TRMET']; C['r_F_USDTRY'] = S['r_USDTRY']
M = C.corr(min_periods=100)
L('A) ANLIK (ayni saat) degisimler, 2024-06+ korelasyon; n(g,GLD)=', int(C[['g_F_XAUUSD', 'GLD_14:30 anlik']].dropna().shape[0]))
L(M.round(2).to_string())
ev = np.linalg.eigvalsh(C[['g_F_XAUUSD', 'GC_14:00 anlik', 'GLD_14:30 anlik', 'PHYS_14:30 anlik', 'GDX_14:30 anlik', 'GDXJ_14:30 anlik']].dropna().corr().values)[::-1]
L('6 panel satirinin korelasyon ozdegerleri (toplam 6):', np.round(ev, 2), 'ilk ozdeger payi', round(ev[0] / 6, 3))
ev2 = np.linalg.eigvalsh(C[['g_F_XAUUSD', 'GC_14:00 anlik', 'GLD_14:30 anlik', 'PHYS_14:30 anlik']].dropna().corr().values)[::-1]
L('altin-kopyasi 4 satir (g, GC, GLD, PHYS) ilk ozdeger payi', round(ev2[0] / 4, 3))
L('B) EKRANDA GORUNEN (d* kapanistan kapanisa) vs g, korelasyon (2024-06+; tum 2018+ ayri):')
for s in ['GLD', 'PHYS', 'GDX', 'GDXJ']:
    a = S[['r_XAU', 'us_' + s]].dropna(); b = P.loc[idx >= '2018-12-17', ['r_XAU', 'us_' + s]].dropna()
    L(s, 'cc d* vs g: 2024-06+', round(a.corr().iloc[0, 1], 3), 'n', len(a), '| 2018+', round(b.corr().iloc[0, 1], 3), 'n', len(b))
L('C) Mevsim: g ile korelasyon (yaz: 14:55 UTC = ABD seansi 85 dk, kis: 25 dk)')
for sea, m in (('yaz', S['us_summer']), ('kis', ~S['us_summer'])):
    cc = C[m.values].corr(min_periods=30)['g_F_XAUUSD']
    L(sea, 'n', int(m.sum()), cc.round(2).to_dict())
    for s in ['GLD', 'GDX', 'GDXJ', 'PHYS']:
        a = S.loc[m.values, ['r_XAU', 'us_' + s]].dropna()
        L('   ', sea, 'cc d* vs g', s, round(a.corr().iloc[0, 1], 3), 'n', len(a))
L('D) GDX-GDXJ GLD-arindirilmis artik korelasyonu (beta: ornek ici OLS)')
def resid(y, x):
    a = pd.concat([y, x], axis=1).dropna(); b = np.polyfit(a.iloc[:, 1], a.iloc[:, 0], 1)[0]
    return y - b * x, b
for nm, sub in (('cc d* 2018+', P[idx >= '2018-12-17']), ('cc d* 2024-06+', S)):
    e1, b1 = resid(sub['us_GDX'], sub['us_GLD']); e2, b2 = resid(sub['us_GDXJ'], sub['us_GLD'])
    a = pd.concat([e1, e2], axis=1).dropna(); L(nm, 'corr(e_GDX,e_GDXJ)', round(a.corr().iloc[0, 1], 3), 'n', len(a), 'beta', round(b1, 2), round(b2, 2))
ig = {s: np.log(S['o1430_' + s] / S['close_' + s]) for s in ['GLD', 'GDX', 'GDXJ']}
e1, b1 = resid(ig['GDX'], ig['GLD']); e2, b2 = resid(ig['GDXJ'], ig['GLD'])
a = pd.concat([e1, e2], axis=1).dropna(); L('anlik 14:30 (2023-12+ ort. 2024-06+)', 'corr', round(a.corr().iloc[0, 1], 3), 'n', len(a))
ep, _ = resid(S['us_GDXJ'], S['us_GDX'])
L('E) GC_F gunluk surekli seri vade sicramasi |r_GC_F - r_GLD| > %0,5')
G = pd.read_pickle(SCR + '/k1_gcgld.pkl'); G['dif'] = (G.gc - G.gld).abs()
for nm, g_ in (('tum ortak ornek', G), ('2024-06+', G[G.index >= '2024-06-20']), ('2018-12+', G[G.index >= '2018-12-17'])):
    L(nm, 'n gun', len(g_), 'sicrama gunu', int((g_.dif > 0.005).sum()), 'oran', round((g_.dif > 0.005).mean(), 3), 'korelasyon(gc,gld)', round(g_.corr().iloc[0, 1], 3))
L('F) Dogrusal ozet: F_XAUUSD g ile GC/GLD/PHYS 2024-06+ R2 ~ korelasyon^2:', {k: round(M.loc['g_F_XAUUSD', k] ** 2, 2) for k in M.columns[1:6]})
M.round(3).to_csv(OUT + '/panel_korelasyon.csv')
