"""K1 hazirlik: VIOP on vade zincirleri, ABD seansi eslemesi, saatlik anlik fiyatlar, ham ongorucu ve hedef sutunlari.
Cikti: SCR/k1_panel.pkl ve hesap/K1/prep.log. Bagimsiz kod."""
import numpy as np, pandas as pd, re, sys
SCR = '/tmp/claude-0/-home-user-Xxxx/e31e33e0-f360-5bc6-a008-2cee330297de/scratchpad'
V = SCR + '/veri'
OUT = '/home/user/Xxxx/raporlar/2026-11-10_altin_panel_denetimi/hesap/K1'
log = open(OUT + '/prep.log', 'w')
def L(*a):
    s = ' '.join(str(x) for x in a); print(s); log.write(s + '\n')

d = pd.read_csv(V + '/viop_filtre.csv', dtype=str)
d = d.rename(columns={'SOZLESME KODU': 'code', 'VADE TARIHI': 'mat', 'UZLASMA FIYATI': 'S', 'ONCEKI UZLASMA FIYATI': 'P',
                      'ISLEM HACMI': 'vol', 'ISLEM MIKTARI': 'qty', 'ACIK POZISYON': 'oi', 'TARIH': 'date'})
for c in ['S', 'P', 'vol', 'qty', 'oi']:
    d[c] = pd.to_numeric(d[c], errors='coerce')
d['date'] = pd.to_datetime(d['date']); d['mat'] = pd.to_datetime(d['mat'])
dates = pd.DatetimeIndex(sorted(d['date'].unique()))
N = len(dates); last = dates[-1]
L('VIOP gun', N, dates[0].date(), last.date())

def build(rx):
    s = d[d.code.str.match(rx)].copy()   # N1 ve benzeri ozel kodlar rx ile elenir
    s = s.sort_values('qty').drop_duplicates(['date', 'mat'], keep='last')
    pos = dates.get_indexer(s['date'])
    pm = np.searchsorted(dates.values, s['mat'].values, side='right') - 1
    extra = np.where(s['mat'] > last, [max(0, np.busday_count((last + pd.Timedelta(days=1)).date(), (m + pd.Timedelta(days=1)).date())) if m > last else 0 for m in s['mat']], 0)
    s['rem'] = pm - pos + extra
    s['r'] = np.log(s['S'] / s['P'])
    s.loc[~np.isfinite(s['r']), 'r'] = np.nan
    s['di'] = pos
    mats = sorted(s['mat'].unique()); mi = {m: i for i, m in enumerate(mats)}
    s['mi'] = s['mat'].map(mi)
    R = np.full((N, len(mats)), np.nan); Q = np.full((N, len(mats)), np.nan)
    R[s['di'].values, s['mi'].values] = s['r'].values
    Q[s['di'].values, s['mi'].values] = s['qty'].values
    e = s[s['rem'] >= 4].sort_values(['di', 'mat']).drop_duplicates('di', keep='first')
    front = np.full(N, -1); front[e['di'].values] = e['mi'].values
    rf = np.full(N, np.nan); qf = np.full(N, np.nan)
    ok = front >= 0
    rf[ok] = R[np.where(ok)[0], front[ok]]; qf[ok] = Q[np.where(ok)[0], front[ok]]
    # ek: hacim TL, aciK pozisyon on vade
    vol = np.full(N, np.nan); oi = np.full(N, np.nan)
    vv = s.set_index(['di', 'mi'])
    for i in np.where(ok)[0]:
        try:
            row = vv.loc[(i, front[i])]; vol[i] = row['vol']; oi[i] = row['oi']
        except KeyError:
            pass
    return dict(R=R, front=front, rf=rf, qf=qf, vol=vol, oi=oi)

def fwd(ch, k, lock=None):
    """Girişte secilen AYNI kontratin t+1..t+k gunluk r toplami. lock: cikis gunu kilitliyse +1 gun kaydir (en cok +2)."""
    R, front = ch['R'], ch['front']
    out = np.full(N, np.nan)
    for i in range(N):
        f = front[i]
        if f < 0: continue
        e = k
        if lock is not None:
            while i + e < N and lock[i + e] and e < k + 3: e += 1
        if i + e >= N: continue
        seg = R[i + 1:i + e + 1, f]
        if np.isnan(seg).any(): continue
        out[i] = seg.sum()
    return out

chs = {}
chs['XAU'] = build(r'^F_XAUUSD\d{4}$')
chs['TRALT'] = build(r'^F_(TRALT|KOZAL)\d{4}$')
chs['TRMET'] = build(r'^F_(TRMET|KOZAA)\d{4}$')
chs['XU030'] = build(r'^F_XU030\d{4}$')
chs['USDTRY'] = build(r'^F_USDTRY\d{4}$')
P = pd.DataFrame(index=dates)
for k, c in chs.items():
    P['r_' + k] = c['rf']; P['q_' + k] = c['qf']; P['vol_' + k] = c['vol']; P['oi_' + k] = c['oi']
    L(k, 'on vade r dolu gun', int(np.isfinite(c['rf']).sum()))
P['pd'] = dates.to_series().shift(1).values
# bosluk gunu d: onceki VIOP gunune hafta ici gun sayisi
dd = [np.nan if pd.isna(p) else np.busday_count(p.date(), t.date()) for p, t in zip(P['pd'], dates)]
P['dgap'] = np.maximum(np.array(dd, dtype=float), 1)

# ---- kilit ve arife
arife = pd.to_datetime(['2019-06-03', '2019-10-28', '2020-07-30', '2020-10-28', '2021-05-12', '2021-07-19', '2021-10-28', '2022-07-08', '2022-10-28', '2023-04-20', '2023-06-27', '2024-04-09', '2024-10-28', '2025-06-05', '2025-10-28', '2026-03-19', '2026-05-26', '2026-10-28'])
P['arife'] = dates.isin(arife)
thr = np.where(dates < pd.Timestamp('2020-03-13'), 0.195, 0.095)
P['lock'] = (P['r_TRALT'].abs() >= thr).fillna(False).values
lockarr = P['lock'].values
for k in (1, 2, 3):
    P[f'yT{k}'] = fwd(chs['TRALT'], k, lockarr) * 1e4
    P[f'yX{k}'] = fwd(chs['XAU'], k) * 1e4
    P[f'yU{k}'] = fwd(chs['XU030'], k, lockarr) * 1e4
    # kilit kaydirmasi XAU bacagi icin de ayni cikis gunu: A3 icin ayri hesap
    P[f'yXa{k}'] = np.nan
# A3 icin XAU bacagi TRALT ile ayni cikis gunu olmali: efektif k'yi yeniden hesapla
def eff_k(k):
    ek = np.full(N, k)
    for i in range(N):
        e = k
        while i + e < N and lockarr[i + e] and e < k + 3: e += 1
        ek[i] = e
    return ek
for k in (1, 2, 3):
    ek = eff_k(k); out = np.full(N, np.nan); R = chs['XAU']['R']; fr = chs['XAU']['front']
    # XAU bacagi TRALT'in girisi ile ayni gun, kendi on vadesi
    for i in range(N):
        f = fr[i]
        if f < 0 or i + ek[i] >= N: continue
        seg = R[i + 1:i + ek[i] + 1, f]
        if not np.isnan(seg).any(): out[i] = seg.sum()
    P[f'yXa{k}'] = out * 1e4

# ---- ABD gunluk
def rd(path):
    x = pd.read_csv(path)
    x['d'] = pd.to_datetime(x['ldate'])
    return x.groupby('d').last()
sy = ['GLD', 'GDX', 'GDXJ', 'PHYS', 'SLV', 'SPY', 'TIP', 'DX-Y.NYB', '_TNX', '_VIX', 'GC_F']
D = {s: rd(f'{V}/yahoo_daily/{s}.csv') for s in sy}
us_dates = D['GLD'].index
usd = pd.DatetimeIndex([x for x in us_dates if x <= pd.Timestamp('2026-11-09')])
j = np.searchsorted(us_dates.values, dates.values, side='left') - 1     # kesin onceki ABD gunu
dstar = pd.DatetimeIndex(us_dates[j])
dup = pd.Series(dstar).duplicated().values            # ayni d* ikinci BIST gunu -> NA
dstar_ok = dstar.where(~dup)
P['dstar'] = dstar_ok
L('d* NA (tekrar)', int(dup.sum()))
def usret(s):
    c = D[s]['c']
    return (c.diff() if s == '_TNX' else np.log(c / c.shift()))
RET = {s: usret(s) for s in sy}
for s in ['GLD', 'GDX', 'GDXJ', 'PHYS', 'SLV', 'SPY', 'TIP', 'DX-Y.NYB', '_TNX', '_VIX']:
    P['us_' + s] = RET[s].reindex(dstar_ok).values
P['close_GLD'] = D['GLD']['c'].reindex(dstar_ok).values
P['close_GDX'] = D['GDX']['c'].reindex(dstar_ok).values
P['close_GDXJ'] = D['GDXJ']['c'].reindex(dstar_ok).values
P['close_PHYS'] = D['PHYS']['c'].reindex(dstar_ok).values

# ---- saatlik anlik fiyatlar
def rh(s):
    x = pd.read_csv(f'{V}/yahoo_h1/{s}.csv'); x['utc'] = pd.to_datetime(x['utc'], utc=True)
    return x.groupby('utc')['o'].first()
H = {s: rh(s) for s in ['GLD', 'GDX', 'GDXJ', 'PHYS', 'GC_F']}
def snap(s, hh, mm, shift_days=0):
    idx = pd.DatetimeIndex([pd.Timestamp(t.date(), tz='UTC') + pd.Timedelta(hours=hh, minutes=mm) for t in dates])
    return H[s].reindex(idx).values
for s in ['GLD', 'GDX', 'GDXJ', 'PHYS']:
    P['o1430_' + s] = snap(s, 14, 30)
    P.loc[P['dstar'].isna(), 'o1430_' + s] = np.nan
P['gc14'] = snap('GC_F', 14, 0); P['gc07'] = snap('GC_F', 7, 0)
# onceki BIST gununun gc14'u
P['gc14_prev'] = pd.Series(P['gc14'].values, index=dates).shift(1).values
P['gc_prevclose'] = np.nan
gcc = D['GC_F']['c']
jj = np.searchsorted(gcc.index.values, dates.values, side='left') - 1
P['gc_prevclose'] = gcc.values[jj]
P['gc_prevdate'] = gcc.index[jj]
# DST (ABD yaz = EDT)
off = [pd.Timestamp(t.date(), tz='UTC').replace(hour=14, minute=30).tz_convert('America/New_York').utcoffset().total_seconds() for t in dates]
P['us_summer'] = np.array(off) == -4 * 3600
# gunluk GC_F ve GLD jump kontrolu icin kaydet
P.to_pickle(SCR + '/k1_panel.pkl')
gcgl = pd.concat([RET['GC_F'].rename('gc'), RET['GLD'].rename('gld')], axis=1).dropna()
gcgl.to_pickle(SCR + '/k1_gcgld.pkl')
for s in ['GLD', 'GDX', 'GDXJ', 'PHYS']:
    L('anlik', s, int(np.isfinite(P['o1430_' + s]).sum()))
L('gc14', int(np.isfinite(P['gc14']).sum()), 'gc07', int(np.isfinite(P['gc07']).sum()))
L('yT2 dolu', int(P['yT2'].notna().sum()), 'yX2', int(P['yX2'].notna().sum()), 'kilit', int(P['lock'].sum()))
L(P.loc['2018-12-17':, ['r_XAU', 'r_TRALT', 'r_TRMET', 'r_XU030', 'r_USDTRY']].describe().round(4).to_string())
