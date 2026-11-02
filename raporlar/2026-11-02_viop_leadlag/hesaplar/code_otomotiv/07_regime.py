"""Stabilite / rejim: yıllara göre corr ve pc|XU100, rejim pencereleri, 250g kayan korelasyon özeti,
olay öncesi/sonrası (TOASO-Stellantis Türkiye: red 24.10.2024, onay 18.04.2025; Beko Europe 02.04.2024), Fisher z farkı.
Çıktı: res/regime_year.csv, res/regime_windows.csv, res/rolling_summary.csv, res/rolling_series.parquet, res/events.csv"""
from common import *
from scipy import stats

def basket(syms): return pd.concat([R(s) for s in syms], axis=1).mean(axis=1)
GRID = basket(['SU.PA', 'ABBN.SW', 'ETN', '267260.KS', '298040.KS', 'SIE.DE'])
EXP = None
PAIRS = [('FROTO', 'EXV5.DE'), ('FROTO', 'VOW3.DE'), ('FROTO', 'F'), ('FROTO', 'TOASO.IS'), ('TOASO', 'EXV5.DE'), ('TOASO', 'STLAM.MI'),
         ('TOASO', 'RNO.PA'), ('DOAS', 'VOW3.DE'), ('ARCLK', 'WHR'), ('ARCLK', 'ELUX-B.ST'), ('VESTL', '034220.KS'), ('VESTL', 'ARCLK.IS'),
         ('ASTOR', 'GRID_BASKET'), ('ASTOR', 'EUPWR.IS'), ('FROTO', 'TRY=X'), ('TOASO', 'TRY=X'), ('DOAS', 'TRY=X'), ('ARCLK', 'TRY=X'),
         ('VESTL', 'TRY=X'), ('ARCLK', 'EURTRY=X'), ('FROTO', 'EURTRY=X')]
def drv(x): return GRID.rename('GRID_BASKET') if x == 'GRID_BASKET' else R(x)
m = M()
WIN = [('2010-01_2018-07', '2010-01-01', '2018-08-01'), ('2018-08_kur_krizi', '2018-08-01', '2019-01-01'), ('2019_2021-11', '2019-01-01', '2021-12-01'),
       ('2021-12_2022-01_kur_soku', '2021-12-01', '2022-02-01'), ('2022-02_2023-05', '2022-02-01', '2023-06-01'),
       ('2023-06_2025-03_ortodoks', '2023-06-01', '2025-03-19'), ('2025-03-19_imamoglu_sonrasi', '2025-03-19', '2025-09-01'),
       ('2025-09_2026-08', '2025-09-01', '2026-09-01'), ('2026-09_10_fon_krizi', '2026-09-01', '2026-11-01')]
yr, wn, rs, rser = [], [], [], {}
for st, x in PAIRS:
    a = R(st); b = drv(x)
    df = pd.concat([a.rename('a'), b.rename('b'), m.rename('m')], axis=1).dropna(); df = df[df.index >= '2010-01-01']
    for y, g in df.groupby(df.index.year):
        if len(g) < 60: continue
        pc, _, _ = pcorr(g['a'], g['b'], [g['m']])
        yr.append({'stock': st, 'driver': x, 'year': y, 'corr': g['a'].corr(g['b']), 'pc': pc, 'n': len(g)})
    for lab, s0, s1 in WIN:
        g = df[(df.index >= s0) & (df.index < s1)]
        if len(g) < 30: continue
        pc, _, _ = pcorr(g['a'], g['b'], [g['m']])
        wn.append({'stock': st, 'driver': x, 'window': lab, 'corr': g['a'].corr(g['b']), 'pc': pc, 'n': len(g)})
    rc = df['a'].rolling(250, min_periods=200).corr(df['b']).dropna()
    rser[f'{st}|{x}'] = rc
    if len(rc):
        rs.append({'stock': st, 'driver': x, 'roll_min': rc.min(), 'roll_p10': rc.quantile(.1), 'roll_med': rc.median(), 'roll_p90': rc.quantile(.9),
                   'roll_max': rc.max(), 'share_pos': (rc > 0).mean(), 'last': rc.iloc[-1], 'last_date': str(rc.index[-1].date())})
Y = pd.DataFrame(yr); W = pd.DataFrame(wn); RS = pd.DataFrame(rs)
Y.to_csv(os.path.join(RES, 'regime_year.csv'), index=False); W.to_csv(os.path.join(RES, 'regime_windows.csv'), index=False)
RS.to_csv(os.path.join(RES, 'rolling_summary.csv'), index=False); pd.DataFrame(rser).to_parquet(os.path.join(RES, 'rolling_series.parquet'))
pv = Y.pivot_table(index=['stock', 'driver'], columns='year', values='pc').round(2)
print('pc|XU100 yıllara göre (seçme):'); print(pv[[c for c in pv.columns if c >= 2014]].to_string())
print(W.pivot_table(index=['stock', 'driver'], columns='window', values='pc').round(2).to_string())
print(RS.round(2).to_string(index=False))

# ---- olaylar: öncesi/sonrası korelasyon farkı (Fisher z) ----
def fz(r1, n1, r2, n2):
    z = (np.arctanh(r2) - np.arctanh(r1)) / np.sqrt(1 / (n1 - 3) + 1 / (n2 - 3)); return z, 2 * stats.norm.sf(abs(z))
ev = []
EVTS = [('TOASO', ['STLAM.MI', 'EXV5.DE', 'DOAS.IS', 'TRY=X', 'EURTRY=X', 'FROTO.IS'], '2023-01-01', '2025-04-18', '2026-11-01', 'Stellantis Türkiye devri (RK onayı 18.04.2025)'),
        ('ARCLK', ['WHR', 'ELUX-B.ST', 'EURUSD=X', 'EURTRY=X', 'TRY=X', 'EXV5.DE', '^STOXX'], '2022-04-01', '2024-04-02', '2026-11-01', 'Beko Europe kapanışı 02.04.2024'),
        ('ASTOR', ['GRID_BASKET', 'SU.PA', 'ETN', '298040.KS', 'EUPWR.IS'], '2023-01-01', '2025-01-01', '2026-11-01', 'ASTOR ABD sözleşmeleri/küresel tema (2025+)')]
for st, xs, s0, e, s1, lab in EVTS:
    for x in xs:
        a = R(st); b = drv(x)
        for kind in ['corr', 'pc']:
            res = []
            for (lo, hi) in [(s0, e), (e, s1)]:
                if kind == 'corr': c, _, n = corr_t(a, b, start=lo, end=hi)
                else: c, _, n = pcorr(a, b, [m], start=lo, end=hi)
                res.append((c, n))
            z, p = fz(res[0][0], res[0][1], res[1][0], res[1][1])
            ev.append({'event': lab, 'stock': st, 'driver': x, 'kind': kind, 'pre': res[0][0], 'n_pre': res[0][1], 'post': res[1][0], 'n_post': res[1][1], 'z': z, 'p': p})
E = pd.DataFrame(ev); E.to_csv(os.path.join(RES, 'events.csv'), index=False)
print(E.round(3).to_string(index=False))
# olay günleri anormal getiri (piyasa modeli, 250g tahmin penceresi)
ar = []
for st, day in [('TOASO', '2024-10-24'), ('TOASO', '2024-10-25'), ('TOASO', '2025-04-18'), ('TOASO', '2025-04-21'), ('ARCLK', '2024-04-02'), ('ARCLK', '2024-04-03'),
                ('ARCLK', '2023-01-17'), ('ARCLK', '2023-01-18')]:
    a = R(st); df = pd.concat([a.rename('a'), m.rename('m')], axis=1).dropna()
    t0 = pd.Timestamp(day)
    if t0 not in df.index: ar.append({'stock': st, 'day': day, 'AR_pct': np.nan}); continue
    est = df[df.index < t0].tail(250); b = np.polyfit(est['m'], est['a'], 1)
    resid = est['a'] - np.polyval(b, est['m']); arv = df.loc[t0, 'a'] - np.polyval(b, df.loc[t0, 'm'])
    ar.append({'stock': st, 'day': day, 'AR_pct': 100 * arv, 'AR_z': arv / resid.std(), 'r_stock_pct': 100 * df.loc[t0, 'a'], 'r_xu100_pct': 100 * df.loc[t0, 'm']})
AR = pd.DataFrame(ar); AR.to_csv(os.path.join(RES, 'event_ar.csv'), index=False); print(AR.round(2).to_string(index=False))
