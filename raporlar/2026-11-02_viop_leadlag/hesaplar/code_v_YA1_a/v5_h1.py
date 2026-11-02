"""v_YA1_a — gerçekçi giriş vekilleri (spot): saatlik ilk bar kapanışı (10:30 TSİ, 2023-11-30+) ve 5dk ilk 30 dk VWAP (10:00-10:30 TSİ, son ~60 gün).
Açılış seansı fiyatı (günlük o) ile ayrıştırma: fade = [o -> 10:30] + [10:30 -> kapanış]. Koşulsuz tabanlar da hesaplanır.
"""
import numpy as np, pandas as pd, os, sys, glob
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from v0_panel import SCR
from v2_bt import nw_t
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 40)

def st(x, dates, cost=0):
    x = pd.Series(np.asarray(x, float)) - cost / 1e4; d = pd.Series(np.asarray(dates))
    ok = x.notna().values; x = x[ok]; d = d[ok]
    if len(x) < 8: return dict(n=len(x), trade=round(1e4 * x.mean(), 1) if len(x) else np.nan)
    gm = x.groupby(d.values).mean()
    return dict(n=len(x), trade=round(1e4 * x.mean(), 1), t_cl=round(gm.mean() / (gm.std() / np.sqrt(len(gm))), 2) if len(gm) > 2 else np.nan, day=round(1e4 * gm.mean(), 1), t_nw=round(nw_t(gm), 2))

rows = []
for fp in glob.glob(SCR + '/data/h1/*.IS.parquet'):
    s = os.path.basename(fp)[:-11]
    if s.startswith('X'): continue
    h = pd.read_parquet(fp); h = h[h.index.strftime('%H:%M') == '06:30']
    if len(h) == 0: continue
    rows.append(pd.DataFrame({'stock': s, 'date': pd.to_datetime(h.ldate).dt.normalize().values, 'h_o': h.o.values, 'p1030': h.c.values, 'h_hi': h.h.values, 'h_lo': h.l.values}))
H = pd.concat(rows)
m5r = []
for fp in glob.glob(SCR + '/data/m5/*.IS.parquet'):
    s = os.path.basename(fp)[:-11]
    if s.startswith('X'): continue
    m = pd.read_parquet(fp); t = m.index.strftime('%H:%M')
    m = m[(t >= '07:00') & (t <= '07:25')]
    if len(m) == 0: continue
    m['d'] = pd.to_datetime(m.ldate).dt.normalize(); m['tp'] = (m.h + m.l + m.c) / 3; m['w'] = m.v.fillna(0) * m.tp
    g = m.groupby('d').agg(w=('w', 'sum'), v=('v', 'sum'), tp=('tp', 'mean'))
    vw = np.where(g.v > 0, g.w / g.v.where(g.v > 0), g.tp)
    m5r.append(pd.DataFrame({'stock': s, 'date': g.index, 'vwap30': vw}))
M5 = pd.concat(m5r)
print('h1 hisse:', H.stock.nunique(), 'gün', H.date.min().date(), H.date.max().date(), '| m5 hisse', M5.stock.nunique(), M5.date.min().date(), M5.date.max().date())
E = pd.read_parquet(HERE + '/_ev.parquet'); E = E[E.reg == 'P10'].copy()
E = E.merge(H.rename(columns={'date': 'date_1'}), on=['stock', 'date_1'], how='left').merge(M5.rename(columns={'date': 'date_1'}), on=['stock', 'date_1'], how='left')
E['c1'] = E.o * 0  # yer tutucu
# t+1 günlük o ve c: o_1 = b_1*Ro_1 ; c_1 = ... -> intra_1 ve gap_1 mevcut; 10:30 bileşenleri için t+1 o/c gerekiyor -> paneli kullan
P = pd.read_parquet(HERE + '/_panel.parquet', columns=['stock', 'date', 'o', 'c'])
E = E.merge(P.rename(columns={'date': 'date_1', 'o': 'o1', 'c': 'cl1'}), on=['stock', 'date_1'], how='left')
E['open_match'] = (E.h_o / E.o1 - 1).abs() < 0.002
E['o_to_1030'] = np.log(E.p1030 / E.o1); E['f1030'] = np.log(E.cl1 / E.p1030)
E['v_to_c'] = np.log(E.cl1 / E.vwap30); E['o_to_v'] = np.log(E.vwap30 / E.o1)
E.to_parquet(HERE + '/_ev_h1.parquet')
# koşulsuz taban (h1 hisseleri, 2023-11+)
PU = P.rename(columns={'o': 'o1', 'c': 'cl1'}).merge(H, on=['stock', 'date'], how='inner')
PU['f1030'] = np.log(PU.cl1 / PU.p1030); PU['o_to_1030'] = np.log(PU.p1030 / PU.o1); PU['intra'] = np.log(PU.cl1 / PU.o1)
PU = PU[PU.intra.abs() < 0.11]
VI = set(E[E.viop].stock)
print('\nKOŞULSUZ (h1 hisseleri, tüm günler) SAT->kapanış brüt: açılıştan', st(-PU.intra, PU.date), '| 10:30dan', st(-PU.f1030, PU.date), '| VİOP47 10:30dan', st(-PU[PU.stock.isin(VI)].f1030, PU[PU.stock.isin(VI)].date))
for nm, m in [('TC', E.TC), ('TU', E.TU), ('BC_long?', E.BC), ('TCL', E.TCL), ('UP6', E.UP6)]:
    for lab, um in [('viop47', E.viop), ('h1_tümü', E.stock.notna())]:
        s = E[m & um & E.p1030.notna() & E.open_match]
        if len(s) < 8: continue
        print(f'\n{nm} {lab}: n={len(s)}  açılış eşleşmesi ok. SAT (fade) brüt bileşenler:')
        print('   açılış->kapanış (günlük o):', st(-s.intra_1, s.date), '\n   açılış->10:30:', st(-s.o_to_1030, s.date), '\n   10:30->kapanış:', st(-s.f1030, s.date),
              '\n   10:30->kapanış @15:', st(-s.f1030, s.date, 15), '| @15+tik:', st(-s.f1030 - np.minimum(0.01 / s.c_unadj_1, 0.02), s.date, 15))
        q = s[s.vwap30.notna()]
        if len(q) >= 5: print('   [m5] ilk30dk VWAP->kapanış brüt:', st(-q.v_to_c, q.date), ' açılış->VWAP30:', st(-q.o_to_v, q.date), ' açılış->kapanış aynı olaylar:', st(-q.intra_1, q.date))
