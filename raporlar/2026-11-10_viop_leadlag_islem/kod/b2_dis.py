"""b2: F3_DIS ailesi backtest (PLAN v2). python3 -I b2_dis.py <VERI_DIR> <EK_DIR>"""
import sys, math, warnings, numpy as np, pandas as pd
from scipy import stats
warnings.filterwarnings('ignore'); np.seterr(all='ignore')
V, EK = sys.argv[1], sys.argv[2]; P = V + '/panel/'
rp = lambda n: pd.read_parquet(P + n)
fr = rp('fut_ret.parquet'); cal = fr.index; N = len(cal)
fl = rp('fut_limit.parquet').reindex(cal); ft = rp('fut_trades.parquet'); fv = rp('fut_value_tl.parquet'); fc = rp('fut_code.parquet'); fs = rp('fut_settle.parquet')
SG = {s: g.sort_values('date') for s, g in rp('spot_gunluk.parquet').groupby('sym')}
dg = pd.concat([rp('dis_gunluk.parquet'), rp('ek_b2_dis_gunluk.parquet')])
DG = {s: g.sort_values('date') for s, g in dg.groupby('sym')}
hh = pd.concat([rp('saatlik.parquet'), rp('ek_b2_saatlik.parquet')])
HG = {s: g.sort_values('ts_utc') for s, g in hh.groupby('sym')}
spl = pd.read_csv(P + 'bolunme_gunleri.csv', parse_dates=['date']); SPD = {s: set(g.date) for s, g in spl.groupby('sym')}
liq = pd.read_csv('/home/user/Xxxx/raporlar/2026-11-02_viop_leadlag/veri_ozet/y_viop_likidite.csv').set_index('und')['rt_cost_retail_bps']
def retail(u):
    if u in ('XU030', 'XLBNK'): return 6.0
    v = liq.get(u, np.nan); return 22.0 if pd.isna(v) else float(v)
pairs = pd.read_csv(EK + '/ciftler_onkayit.csv', sep=';'); pairs = pairs[pairs.aile == 'F3_DIS'].reset_index(drop=True)
# ---------- yardimcilar
def beta(r, m):
    return (r.rolling(250, min_periods=120).cov(m) / m.rolling(250, min_periods=120).var()).shift(1)
def sig(e): return e.rolling(120, min_periods=60).std().shift(1)
def exflag(s):
    src = SG if s in SG else DG
    a = np.zeros(N, bool)
    if s in src:
        d = src[s].set_index('date'); x = np.log(d.c / d.c.shift()) - np.log(d.adj / d.adj.shift())
        xs = set(d.index[x.abs() > 0.005]) | SPD.get(s, set())
        if xs:
            pos = cal.searchsorted(sorted(xs)); pos = pos[pos < N]; a[pos] = True
    return a
SPR = {}
def spot_ret(s):
    if s in SPR: return SPR[s]
    d = SG[s].set_index('date'); d = d[~d.index.duplicated(keep='last')]
    r = np.log(d['adj'] / d['adj'].shift(1))
    r[r.index.isin(SPD.get(s, set()))] = np.nan
    if s in ('XU030.IS', 'XBANK.IS'): bad = r.abs() > 0.5
    else:
        m = np.where(r.index < pd.Timestamp('2020-03-13'), 0.20, 0.10)
        bad = (r > np.log(1 + m + 0.005)) | (r < np.log(1 - m - 0.005))
    r[bad | ((d['v'] == 0) & (d['h'] == d['l']))] = np.nan
    SPR[s] = r.reindex(cal); return SPR[s]
def asof_p(s):
    d = DG[s].set_index('date'); p = d['adj'].copy()
    if s == 'HRC=F': p[d['v'].fillna(0) == 0] = np.nan
    p = p[~p.index.duplicated(keep='last')]
    return p.reindex(p.index.union(cal)).ffill().reindex(cal)
HC = {}; HSRC = {}
def hp(s, T, bist):
    k = (s, T, bist)
    if k in HC: return HC[k]
    if s not in HG:
        HC[k] = pd.Series(np.nan, index=cal); HSRC[k] = pd.Series('', index=cal); return HC[k]
    d = HG[s]; ts = pd.to_datetime(d['ts_utc'], utc=True)
    df = pd.DataFrame({'day': ts.dt.tz_localize(None).dt.normalize().values, 'tm': (ts.dt.hour * 60 + ts.dt.minute).values, 'o': d['o'].values, 'c': d['c'].values})
    nxt = df.groupby('day')['tm'].shift(-1); end = np.minimum(df.tm + 60, nxt.fillna(1e9))
    if bist: end = np.minimum(end, 900)
    df['end'] = end
    a = df[df.end <= T].groupby('day').tail(1)
    b = df[(df.tm <= T) & (~df.day.isin(a.day))].groupby('day').tail(1)
    p = pd.Series(np.r_[a.c.values, b.o.values], index=np.r_[a.day.values, b.day.values])
    age = pd.Series(np.r_[(T - a.end).values, (T - b.tm).values], index=p.index)
    src = pd.Series(['c'] * len(a) + ['o'] * len(b), index=p.index)
    p[age > 60] = np.nan
    HC[k] = p.reindex(cal); HSRC[k] = src.reindex(cal); return HC[k]
RAWS = {'TUR', 'EEM', 'CRACK321'}
israw = lambda s: '=F' in s or s in RAWS
def region(s, mode):
    if mode in ('SAAT', 'K1730'): return 'EXW1.DE' if '.' in s else 'SPY'
    if s.endswith('.AX'): return '^AXJO'
    if s.endswith('.T'): return '^N225'
    if s.endswith('.KS'): return '^KS11'
    return '^STOXX50E' if '.' in s else '^GSPC'
RC = {}
def Rcomp(s, mode):
    k = (s, mode)
    if k in RC: return RC[k]
    T = 890 if mode == 'SAAT' else 870
    if s == 'CRACK321':
        if mode == 'T1':
            a, b, z = asof_p('RB=F'), asof_p('HO=F'), asof_p('BZ=F'); cr = (2 * a + b) * 14 - z
            R = (cr.shift(1) - cr.shift(2)) / z.shift(2)
        else:
            a, b, z = [hp(x, T, False) for x in ('RB=F', 'HO=F', 'BZ=F')]; cr = (2 * a + b) * 14 - z
            R = (cr - cr.shift(1)) / z.shift(1)
    elif mode in ('SAAT', 'K1730'):
        lp = np.log(hp(s, T, s.endswith('.IS'))); R = lp - lp.shift(1); R[exflag(s)] = np.nan
    else:
        lp = np.log(asof_p(s)); R = lp.shift(1) - lp.shift(2) if mode == 'T1' else lp - lp.shift(1)
    RC[k] = R; return R
def leader(comps, mode):
    Rs, Es = [], []
    for s in comps:
        R = Rcomp(s, mode)
        if israw(s): E = R
        else:
            ix = Rcomp(region(s, mode), mode); E = R - beta(R, ix) * ix
        Rs.append(R); Es.append(E)
    Rd = pd.concat(Rs, axis=1); Ed = pd.concat(Es, axis=1); ok = Ed.notna().sum(axis=1) >= len(comps) / 2
    return Ed.mean(axis=1).where(ok), Rd.mean(axis=1).where(ok)
TG = {}
def target(u):
    if u in TG: return TG[u]
    sy = {'XU030': 'XU030.IS', 'XLBNK': 'XBANK.IS'}.get(u, u + '.IS')
    rT = spot_ret(sy); mkt = spot_ret('XU030.IS')
    bT = beta(rT, mkt) if u != 'XU030' else pd.Series(0.0, index=cal)
    eT = rT - bT * mkt; db = fr[u] - rT
    TG[u] = dict(sy=sy, rT=rT, mkt=mkt, bT=bT, eT=eT, sT=sig(eT), sR=sig(rT), zdb=(db / db.rolling(120, min_periods=60).std().shift(1)).values); return TG[u]
def tzs(u, kind):
    t = target(u); e, r, sT, sR = t['eT'], t['rT'], t['sT'], t['sR']
    if kind == 'T1': return ((e.shift(1) + e) / (math.sqrt(2) * sT)).values, ((r.shift(1) + r) / (math.sqrt(2) * sR)).values
    if kind == 'K1730':
        s = t['sy']; c = SG[s].set_index('date')['c']; c = c[~c.index.duplicated()].reindex(cal)
        def rk(sym):
            cc = SG[sym].set_index('date')['c']; cc = cc[~cc.index.duplicated()].reindex(cal)
            x = np.log(hp(sym, 870, True) / cc.shift(1)); x[exflag(sym)] = np.nan; return x
        Rk = rk(s); Rm = rk('XU030.IS') if u != 'XU030' else 0 * Rk
        ek = Rk - t['bT'] * Rm
        return (ek / sT).values, (Rk / sR).values
    return (e / sT).values, (r / sR).values
def signals(eL, rL, zT, zTh, zT1, zdb, rho):
    zL = (eL / sig(eL)).values; zh = (rL / sig(rL)).values
    d = np.sign(zL) * rho; dh = np.sign(zh) * rho; a = np.abs(zL) >= 1; x = d * zT
    S = {'S_KUL': (a & (x <= .25), d), 'S_KUL_YATAY': (a & (x >= -.5) & (x <= .25), d), 'S_KUL_TERS': (a & (x < -.5), d), 'S_ONCU': (a, d), 'S_IKISI': (a & (x > .25), d)}
    S['S_KUL_BAZSIZ'] = (S['S_KUL'][0] & (np.abs(zdb) < 1), d)
    S['S_HAM'] = ((np.abs(zh) >= 1) & (dh * zTh <= .25), dh)
    S['S_KENDI'] = (np.abs(zT1) >= 1, -np.sign(zT1)); return S, zL
SUM = {}; ROLL = {}; OKD = {}; YM = {}
def prep(u, h):
    if (u, h) not in SUM:
        SUM[(u, h)] = fr[u].rolling(h, min_periods=h).sum().shift(-h).values
        cc = (fc[u] != fc[u].shift(1)).astype(float); ROLL[(u, h)] = cc.rolling(h, min_periods=h).sum().shift(-h).values > 0
    if u not in OKD:
        OKD[u] = ((fl[u].fillna(0) == 0) & (ft[u] >= 20) & (fv[u] >= 1e6)).values
        YM[u] = fr[u].groupby(fr.index.year).mean() * 1e4
def select(u, mask, d, h, entry):
    prep(u, h); S = SUM[(u, h)]; ok = OKD[u]; sh = 1 if entry == 'E2' else 0
    I, E, R, RL = [], [], [], []; last = -1
    for i in np.where(mask & ~np.isnan(d))[0]:
        e = i + sh; x = e + h
        if x >= N: break
        if e < last or not (ok[e] and ok[x]) or np.isnan(S[e]): continue
        I.append(i); E.append(e); R.append(1e4 * d[i] * S[e]); RL.append(ROLL[(u, h)][e]); last = x
    return dict(i=np.array(I, int), e=np.array(E, int), ret=np.array(R), roll=np.array(RL, bool), d=d[np.array(I, int)] if I else np.array([]))
PER = [('TAM', '2017-03-01', '2027-01-01'), ('IS', '2017-01-01', '2022-01-01'), ('OOS', '2022-01-01', '2027-01-01'), ('SON2Y', '2024-11-10', '2027-01-01'), ('2020+', '2020-01-01', '2027-01-01'), ('SAAT_DON', '2023-11-09', '2027-01-01')]
def tt(x):
    n = len(x)
    if n < 3 or np.std(x, ddof=1) == 0: return np.nan
    return x.mean() / (np.std(x, ddof=1) / math.sqrt(n))
def pstat(tr, u, h, per):
    nm, a, b = per; dts = cal[tr['e']]; m = (dts >= a) & (dts < b); n = int(m.sum())
    base = dict(n=n)
    if n == 0: return base
    r = tr['ret'][m]; ro = tr['roll'][m]; d = tr['d'][m]; yr = dts[m].year.values
    c = retail(u); y0 = max(pd.Timestamp(a), cal[0]); y1 = min(pd.Timestamp(b), cal[-1]); yrs = max((y1 - y0).days / 365.25, 1e-9)
    sd = r - d * h * YM[u].reindex(yr).values
    top = np.sort(r)[::-1][10:] if n > 10 else np.array([])
    ym = pd.Series(r).groupby(yr).mean()
    base.update(yillik_n=n / yrs, brut=r.mean(), net8=(r - 8 * (1 + ro)).mean(), net15=(r - 15 * (1 + ro)).mean(), net_bireysel=(r - c * (1 + ro)).mean(), t=tt(r), isabet=(r > 0).mean(), medyan=np.median(r),
                brut_ilk10haric=top.mean() if len(top) else np.nan, t_ilk10haric=tt(top) if len(top) else np.nan, poz_yil=int((ym > 0).sum()), yil_say=len(ym), brut_suruklenme_duz=np.nanmean(sd), uzun_pay=(d > 0).mean(), n_roll=int(ro.sum()))
    return base
def kaydir(zL, zT, rho, u, kind, rng, B=500):
    S2 = SUM[(u, 2)]; valid = ~np.isnan(S2)
    def st(z):
        d = np.sign(z) * rho; m = (np.abs(z) >= 1) & valid
        if kind == 'KUL': m = m & (d * zT <= .25)
        return np.nan if m.sum() == 0 else (d[m] * S2[m]).mean() * 1e4
    real = st(zL); ks = rng.integers(250, N - 250 + 1, B); sh = np.array([st(np.roll(zL, k)) for k in ks])
    return real, float((sh >= real).mean()) if not np.isnan(real) else np.nan
def nw_t(x, L):
    x = x[~np.isnan(x)]; n = len(x)
    if n < L + 10: return np.nan
    u = x - x.mean(); v = u @ u / n
    for l in range(1, L + 1): v += 2 * (1 - l / (L + 1)) * (u[l:] @ u[:-l]) / n
    return x.mean() / math.sqrt(v / n)
# ---------- ABD yaz/kis
nyoff = pd.Series(pd.DatetimeIndex(cal + pd.Timedelta(hours=12)).tz_localize('America/New_York', nonexistent='shift_forward', ambiguous=True).map(lambda x: x.utcoffset().total_seconds()), index=cal)
US_DST = (nyoff == -14400).values
# ---------- kalibrasyon
R = {}; TR = {}; rows = []; rng = np.random.default_rng(20261110)
def calib():
    e = spot_ret('AKBNK.IS'); mk = spot_ret('XU030.IS'); e = e - beta(e, mk) * mk
    zL = (e / sig(e)).values; t = target('SAHOL'); zT = (t['eT'] / t['sT']).values
    d = np.sign(zL); m = (np.abs(zL) >= 1) & (d * zT <= .25)
    tr = select('SAHOL', m, d, 2, 'E0'); prep('SAHOL', 2); r = tr['ret']; return len(r), r.mean(), tt(r)
print('KALIBRASYON SAHOL<-AKBNK.IS S_KUL E0 h2 TAM: n=%d brut=%.2f t=%.2f' % calib())
# ---------- sahte oncu
def fake():
    us = sorted(pairs.hedef.unique()); out = {'ertesi': [], 'gurultu': []}; rg = np.random.default_rng(7)
    for u in us:
        zT, _ = tzs(u, 'T1'); t = target(u); zn = (t['eT'].shift(-1) / t['sT'].shift(-1)).values
        for nm, zs in (('ertesi', [zn]), ('gurultu', [rg.standard_normal(N) for _ in range(5)])):
            for z in zs:
                d = np.sign(z); tr = select(u, (np.abs(z) >= 1) & (d * zT <= .25), d, 2, 'E0')
                if len(tr['ret']) > 5: out[nm].append((u, len(tr['ret']), tr['ret'].mean(), tt(tr['ret']), tr['ret']))
    res = []
    for nm, L in out.items():
        allr = np.concatenate([x[4] for x in L]); mt = np.array([x[3] for x in L])
        res.append('%s: hedef-seri sayisi=%d, havuz n=%d, havuz ort=%.1f bps, havuz t=%.2f, ort(seri ort)=%.1f, |t|>=2 payi=%.2f' % (nm, len(L), len(allr), allr.mean(), tt(allr), np.mean([x[2] for x in L]), np.mean(np.abs(mt) >= 2)))
    return res
FAKE = fake(); print('SAHTE ONCU:'); [print(' ', x) for x in FAKE]
# ---------- konfigurasyonlar
cfgs = []
for _, p in pairs.iterrows():
    comps = p.oncu.split('+'); z = p.zaman
    if z == 'DIS': cfgs += [(p, comps, 'GUNLUK_T1', 'T1', ['E0', 'E2']), (p, comps, 'SAAT_1450', 'SAAT', ['E0', 'E2'])]
    elif z == 'ASYA_T': cfgs.append((p, comps, 'ASYA_T', 'ASYA', ['E0', 'E2']))
    else: cfgs += [(p, comps, 'VIOP_T_GUNLUK', 'VIOPD', ['E0', 'E2']), (p, ['GC=F'], 'VIOP_T_KATI1730', 'K1730', ['KATI'])]
SIGS = ['S_KUL', 'S_KUL_YATAY', 'S_KUL_TERS', 'S_KUL_BAZSIZ', 'S_ONCU', 'S_IKISI', 'S_HAM', 'S_KENDI']
KAY = {}; META = {}; SKIP = []
for p, comps, zam, mode, girs in cfgs:
    u = p.hedef; key = (u, p.oncu, zam); rho = float(p.isaret)
    if any(s in ('HRC=F',) for s in comps) and False: continue
    if mode == 'VIOPD': eL = fr['XAUUSD'].copy(); rL = eL.copy()
    else: eL, rL = leader(comps, mode)
    if eL.notna().sum() < 50: SKIP.append((key, 'oncu verisi yok')); continue
    tk = {'T1': 'T1', 'SAAT': 'SAAT', 'ASYA': 'D', 'VIOPD': 'D', 'K1730': 'K1730'}[mode]
    zT, zTh = tzs(u, tk); _, _ = None, None; t0 = target(u); zT1 = (t0['eT'] / t0['sT']).values
    S, zL = signals(eL, rL, zT, zTh, zT1, t0['zdb'], rho); META[key] = dict(zL=zL, zT=zT, mode=mode)
    for sg in SIGS:
        m, d = S[sg]
        for g in girs:
            for h in (1, 2, 3):
                tr = select(u, m, d, h, 'E2' if g == 'E2' else 'E0'); TR[(key, sg, g, h)] = tr
                for per in PER:
                    if mode in ('SAAT', 'K1730') and per[0] not in ('TAM', 'SAAT_DON'): continue
                    st = pstat(tr, u, h, per)
                    R[(key, sg, g, h, per[0])] = st
                    rows.append(dict(aile='F3_DIS', hedef=u, oncu=p.oncu, isaret=int(rho), zamanlama=zam, agirlik='ES', sinyal=sg, giris=g, tutma=h, donem=per[0], **st))
    if mode in ('T1', 'ASYA', 'VIOPD'):
        for sg, kd in (('S_KUL', 'KUL'), ('S_ONCU', 'ONCU')): KAY[(key, sg)] = kaydir(zL, zT, rho, u, kd, rng)
cols = 'aile hedef oncu isaret zamanlama agirlik sinyal giris tutma donem n yillik_n brut net8 net15 net_bireysel t isabet medyan brut_ilk10haric t_ilk10haric poz_yil yil_say brut_suruklenme_duz uzun_pay'.split()
sonuc = pd.DataFrame(rows); sonuc = sonuc.rename(columns={}); sonuc[cols + ['n_roll']].to_csv(EK + '/sonuc_b2.csv', sep=';', index=False, float_format='%.4f')
# ---------- ozet ve karar
G = lambda key, sg, g, h, per, f: R.get((key, sg, g, h, per), {}).get(f, np.nan)
oz = []
for p, comps, zam, mode, girs in cfgs:
    key = (p.hedef, p.oncu, zam)
    if key not in META or mode == 'K1730': continue
    for sg in ('S_KUL', 'S_ONCU'):
        g0 = lambda per, f, g='E0': G(key, sg, g, 2, per, f)
        n = g0('TAM', 'n'); t = g0('TAM', 't'); pb = np.nan
        if n >= 3 and not np.isnan(t): pb = 2 * (1 - stats.t.cdf(abs(t), n - 1))
        kr, pk = KAY.get((key, sg), (np.nan, np.nan))
        row = dict(aile='F3_DIS', hedef=p.hedef, oncu=p.oncu, isaret=int(p.isaret), zamanlama=zam, sinyal=sg, n=n, t=t, brut=g0('TAM', 'brut'), net_bireysel_TAM=g0('TAM', 'net_bireysel'), net_bireysel_SON2Y=g0('SON2Y', 'net_bireysel'),
                   oos_brut=g0('OOS', 'brut'), oos_t=g0('OOS', 't'), oos_suruk=g0('OOS', 'brut_suruklenme_duz'), e2_brut=g0('TAM', 'brut', 'E2'), e2_n=g0('TAM', 'n', 'E2'), ilk10_brut=g0('TAM', 'brut_ilk10haric'), p_kaydir=pk, p_birincil=pb, q_fdr='')
        kk = (p.hedef, p.oncu, 'VIOP_T_KATI1730') if zam == 'VIOP_T_GUNLUK' else None
        if kk: row.update(kati_n=G(kk, sg, 'KATI', 2, 'TAM', 'n'), kati_brut=G(kk, sg, 'KATI', 2, 'TAM', 'brut'), kati_e0_brut=g0('SAAT_DON', 'brut'))
        if mode == 'SAAT':
            row.update(karar='BETIMSEL (ikincil, kisa donem)', neden='n=%d; IS/OOS/SON2Y tanimsiz' % n); oz.append(row); continue
        f = []
        if not (n >= 40): f.append('n<40')
        if not (t >= 2.5): f.append('t<2.5')
        if not (row['net_bireysel_TAM'] > 0 and row['net_bireysel_SON2Y'] > 0): f.append('net_bireysel<=0')
        if not (row['oos_brut'] > 0 and row['oos_t'] >= 1.5): f.append('OOS')
        if not (row['oos_suruk'] > 0): f.append('suruk_OOS')
        if not (row['e2_brut'] > 0 and row['e2_brut'] >= row['brut'] / 3): f.append('E2')
        if not (row['ilk10_brut'] > 0): f.append('ilk10')
        if not (pk <= 0.05): f.append('p_kaydir')
        cap = False
        if kk:
            kn = row['kati_n']
            if not (row['kati_brut'] > 0 and row['kati_brut'] >= row['kati_e0_brut'] / 2): f.append('KATI')
            if not (kn >= 30): cap = True
        row['karar'] = 'ELENDI'
        if len(f) == 0: row['karar'] = 'IZLE' if cap else 'ADAY (FDR hariç)'
        elif len(f) <= 2 and t >= 2.0: row['karar'] = 'IZLE'
        row['neden'] = ','.join(f) + (' ;KATI n<30' if cap else ''); oz.append(row)
oz = pd.DataFrame(oz); oz.to_csv(EK + '/ozet_b2.csv', sep=';', index=False, float_format='%.4f')
# ---------- havuz
POOL = []
grp = {}
for (key, sg, g, h), tr in TR.items():
    if g != 'E0' or len(tr['e']) == 0: continue
    zam = key[2]; u = key[0]; fu = fr[u].values * 1e4
    for gl in (zam, 'TUMU_GUNLUK_ASYA_VIOP' if zam in ('GUNLUK_T1', 'ASYA_T', 'VIOP_T_GUNLUK') else None):
        if gl is None: continue
        a = grp.setdefault((gl, sg, h), [np.zeros(N), np.zeros(N), []])
        for e, d, r in zip(tr['e'], tr['d'], tr['ret']):
            a[0][e + 1:e + h + 1] += d * fu[e + 1:e + h + 1]; a[1][e + 1:e + h + 1] += 1
        a[2].extend(tr['ret'])
ser = {}
for (gl, sg, h), (num, cnt, rr) in grp.items():
    s = np.where(cnt > 0, num / np.maximum(cnt, 1), np.nan); ser[(gl, sg, h)] = s; rr = np.array(rr)
    POOL.append(dict(aile='F3_DIS', zamanlama=gl, sinyal=sg, tutma=h, n_islem=len(rr), ort_islem_bps=rr.mean(), n_gun=int((cnt > 0).sum()), ort_gun_bps=np.nanmean(s), t_NW=nw_t(s, h + 1)))
for (gl, sg, h), s in list(ser.items()):
    if sg == 'S_KUL' and (gl, 'S_IKISI', h) in ser:
        df_ = s - ser[(gl, 'S_IKISI', h)]; POOL.append(dict(aile='F3_DIS', zamanlama=gl, sinyal='S_KUL-S_IKISI', tutma=h, n_gun=int(np.isfinite(df_).sum()), ort_gun_bps=np.nanmean(df_), t_NW=nw_t(df_, h + 1)))
pool = pd.DataFrame(POOL); pool.to_csv(EK + '/havuz_b2.csv', sep=';', index=False, float_format='%.4f')
# ---------- islem listesi (ADAY/IZLE) ve yaz/kis
il = []
for _, r in oz[oz.karar.str.startswith(('ADAY', 'IZLE'))].iterrows():
    key = (r.hedef, r.oncu, r.zamanlama); tr = TR[(key, r.sinyal, 'E0', 2)]; zL = META[key]['zL']; zT = META[key]['zT']
    for i, e, d, rt, ro in zip(tr['i'], tr['e'], tr['d'], tr['ret'], tr['roll']):
        il.append(dict(cift=f'{r.hedef}<-{r.oncu}', zamanlama=r.zamanlama, sinyal=r.sinyal, giris_tarihi=cal[e].date(), yon=int(d), z_L=zL[i], z_T=zT[i], cikis_tarihi=cal[min(e + 2, N - 1)].date(), brut_bps=rt, roll=int(ro)))
pd.DataFrame(il).to_csv(EK + '/islemler_b2.csv', sep=';', index=False, float_format='%.3f')
yk = []
for (key, sg, g, h), tr in TR.items():
    if key[2] != 'SAAT_1450' or g != 'E0' or h != 2 or sg not in ('S_KUL', 'S_ONCU') or not all((not israw(s)) and '.' not in s for s in key[1].split('+')): continue
    dst = US_DST[tr['e']]
    for nm, mm in (('yaz', dst), ('kis', ~dst)):
        r = tr['ret'][mm]; yk.append(dict(hedef=key[0], oncu=key[1], sinyal=sg, mevsim=nm, n=len(r), brut=r.mean() if len(r) else np.nan, t=tt(r) if len(r) > 2 else np.nan))
pd.DataFrame(yk).to_csv(EK + '/saat_yazkis_b2.csv', sep=';', index=False, float_format='%.3f')
# ---------- ekrana ozet
print('SKIP', SKIP); print('cfg', len(cfgs), 'ozet satir', len(oz), 'sonuc satir', len(sonuc))
print(oz.groupby(['zamanlama', 'sinyal']).karar.value_counts().unstack(fill_value=0).to_string())
print(pool[(pool.tutma == 2)][['zamanlama', 'sinyal', 'n_islem', 'ort_islem_bps', 'ort_gun_bps', 't_NW']].round(2).to_string())
pd.to_pickle(dict(oz=oz), '/tmp/claude-0/-home-user-Xxxx/b52fa442-3316-551a-bdd2-9e9f754166e0/scratchpad/kod_b2/oz.pkl') if False else None
# ---------- GUNLUK_T1 ornegi
t = pd.Timestamp('2026-11-06'); i = cal.get_loc(t); lp = asof_p('VLO'); pv = DG['VLO'].set_index('date')['adj']
d1, d2 = cal[i - 1], cal[i - 2]; a1 = pv[pv.index <= d1]; a2 = pv[pv.index <= d2]
tT = target('TUPRS'); print('ORNEK t=%s: VLO P(t-1=%s son kapanis tarihi %s)=%.2f / P(t-2=%s son kapanis tarihi %s)=%.2f ; oran=%.4f%%' % (t.date(), d1.date(), a1.index[-1].date(), a1.iloc[-1], d2.date(), a2.index[-1].date(), a2.iloc[-1], 100 * (a1.iloc[-1] / a2.iloc[-1] - 1)))
print(' hedef TUPRS e_T(%s)=%.4f e_T(%s)=%.4f sigma=%.4f zT2=%.2f; giris TUPRS uzlasma %s=%.2f; h=2 cikis %s' % (d1.date(), tT['eT'].iloc[i - 1], t.date(), tT['eT'].iloc[i], tT['sT'].iloc[i], tzs('TUPRS', 'T1')[0][i], t.date(), fs['TUPRS'].iloc[i], cal[min(i + 2, N - 1)].date()))
k = ('TUPRS', 'VLO+MPC+PSX+PBF', 'GUNLUK_T1'); print(' sepet zL=%.2f' % META[k]['zL'][i])
# ---------- aday/izle ve ozet satirlari (kisa)
print(oz[oz.karar.str.startswith(('ADAY', 'IZLE'))][['hedef', 'oncu', 'zamanlama', 'sinyal', 'n', 't', 'brut', 'oos_t', 'p_kaydir', 'neden']].round(2).to_string())
print(oz[(oz.sinyal == 'S_KUL')][['hedef', 'oncu', 'zamanlama', 'n', 't', 'brut', 'oos_brut', 'e2_brut', 'p_kaydir', 'karar']].round(2).to_string())
