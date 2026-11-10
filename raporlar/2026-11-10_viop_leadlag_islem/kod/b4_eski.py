#!/usr/bin/env python3
"""b4: ESKI ailesi (PLAN.md 8. bolum) - 7 kuralin yeniden hesabi, 10.11.2026'ya kadar.
Calistir: python3 -I b4_eski.py   (cikti: ek/eski_b4.csv, durum_b4.csv, esik_b4.csv, islemler_b4.csv, b4_kalibrasyon.txt)"""
import numpy as np, pandas as pd, math, sys, json
try:
    from scipy import stats as sst
except Exception:
    sst = None

V = '/tmp/claude-0/-home-user-Xxxx/b52fa442-3316-551a-bdd2-9e9f754166e0/scratchpad/veri/panel/'
EK = '/home/user/Xxxx/raporlar/2026-11-10_viop_leadlag_islem/ek/'
LIK = '/home/user/Xxxx/raporlar/2026-11-02_viop_leadlag/veri_ozet/y_viop_likidite.csv'
rd = lambda f: pd.read_parquet(V + f + '.parquet')
FR = rd('fut_ret'); cal = pd.DatetimeIndex(FR.index).normalize(); N = len(cal)
def wide(f):
    x = rd(f); x.index = pd.DatetimeIndex(x.index).normalize(); return x.reindex(cal)
FR.index = cal
FL, FT, FV, FC, FS = wide('fut_limit'), wide('fut_trades'), wide('fut_value_tl'), wide('fut_code'), wide('fut_settle')
SPD = rd('spot_gunluk'); DIS = rd('dis_gunluk'); HR = rd('saatlik')
BOL = pd.read_csv(V + 'bolunme_gunleri.csv'); BOL['date'] = pd.to_datetime(BOL['date'])
LK = pd.read_csv(LIK).set_index('und')['rt_cost_retail_bps']
LAST = cal[-1]; iL = N - 1
REG = pd.Timestamp('2020-03-13')

def pv(df, col):
    return df.pivot_table(index='date', columns='sym', values=col, aggfunc='last')
SP = {k: pv(SPD, k).reindex(cal) for k in ['adj', 'c', 'v', 'h', 'l']}

def sret(sym):
    adj = SP['adj'][sym]; stale = (SP['v'][sym] == 0) & (SP['h'][sym] == SP['l'][sym])
    r = np.log(adj.where(~stale) / adj.where(~stale).shift(1))
    sd = BOL.loc[BOL.sym == sym, 'date']; r[r.index.isin(sd)] = np.nan
    lim = np.where(cal < REG, math.log(1.205), math.log(1.105))
    r[(r.abs() > lim)] = np.nan
    if sym in ('XU030.IS', 'XBANK.IS'):
        r[(r.index == pd.Timestamp('2020-07-27'))] = np.nan
    return r

def ownret(df, sym):
    s = df[df.sym == sym].drop_duplicates('date', keep='last').set_index('date')['adj'].dropna().sort_index()
    return np.log(s).diff()

def rbeta(y, x, w=250, mp=125, shift=1):
    m = y.notna() & x.notna(); yy = y.where(m); xx = x.where(m)
    cov = (yy * xx).rolling(w, min_periods=mp).mean() - yy.rolling(w, min_periods=mp).mean() * xx.rolling(w, min_periods=mp).mean()
    var = (xx * xx).rolling(w, min_periods=mp).mean() - xx.rolling(w, min_periods=mp).mean() ** 2
    return (cov / var).shift(shift)

def to_cal(s, side):  # side 'right': t_prev<=d<t ; 'left': t_prev<d<=t
    s = s.dropna(); s = s[s.index >= cal[0]]
    k = np.searchsorted(cal.values, s.index.values, side=side); ok = k < N
    out = pd.Series(s.values[ok], index=cal[k[ok]])
    return out.groupby(level=0).sum().reindex(cal)

# ------------------------------------------------------------------ yardimcilar
def arr(und, wd):
    return wd[und].to_numpy(dtype=float) if wd is FR or True else None

def cost_of(und):
    if und in ('XU030', 'XLBNK'): return (3., 3., 6.)
    if und in ('USDTRY', 'XAUUSD', 'XAGUSD', 'XAUTRY'): return (3., 3., 8.)
    return (8., 15., float(LK.get(und, 22.)))

class Leg:
    def __init__(s, und):
        s.und = und; s.ret = FR[und].to_numpy(float); s.lim = FL[und].to_numpy(float)
        s.trd = FT[und].to_numpy(float); s.val = FV[und].to_numpy(float)
        c = FC[und].astype(object).to_numpy(); s.chg = np.r_[False, c[1:] != c[:-1]]
        s.cs = np.nancumsum(s.ret); s.nn = np.cumsum(np.isnan(s.ret)); s.cost = cost_of(und)
        yr = pd.Series(s.ret, index=cal); ym = yr.groupby(cal.year).transform('mean').fillna(0).to_numpy()
        s.dcs = np.cumsum(ym); s.chgc = np.cumsum(s.chg)
LEG = {}
def leg(u):
    if u not in LEG: LEG[u] = Leg(u)
    return LEG[u]

def evaluate(trs, legs, wts, shift=0, light=False, ea=None):
    """trs: (e,x,d,z) listesi. legs: Leg listesi; wts: ilk bacak icin 1, digerleri icin sinyal gunu agirlik dizisi."""
    out = []
    for (e, x, d, z) in trs:
        E, X = e + shift, x + shift
        if X >= N or x is None: continue
        g = 0.; dr = 0.; c8 = c15 = cr = 0.; roll = 0; bad = False
        for L, w in zip(legs, wts):
            wi = 1.0 if np.isscalar(w) else w[e]
            if not np.isfinite(wi): bad = True; break
            if L.nn[X] - L.nn[E] > 0: bad = True; break
            if not light:
                if L.lim[E] == 1 or L.lim[X] == 1: bad = True; break
                if not (L.trd[E] >= 20 and L.val[E] >= 1e6 and L.trd[X] >= 20 and L.val[X] >= 1e6): bad = True; break
                if (L.chgc[X] - L.chgc[E]) > 0: roll = 1
            g += wi * (L.cs[X] - L.cs[E]); dr += wi * (L.dcs[X] - L.dcs[E])
            c8 += abs(wi) * L.cost[0]; c15 += abs(wi) * L.cost[1]; cr += abs(wi) * L.cost[2]
        if bad: continue
        gb = 1e4 * d * g
        if ea is not None:
            v = ea[e]
            if not np.isfinite(v): continue
            gb += 1e4 * d * v
        out.append(dict(ei=e, e=cal[e], x=cal[min(X, N - 1)], xi=X, d=d, z=z, hold=X - E, brut=gb, c8=c8 * (1 + roll), c15=c15 * (1 + roll),
                        cr=cr * (1 + roll), roll=roll, drift=1e4 * d * dr, long=int(d > 0)))
    return pd.DataFrame(out)

def greedy(dirs, zs, h, valid=None):
    trs = []; nxt = 0
    for i in range(N):
        d = dirs[i]
        if d == 0 or not np.isfinite(d) or i < nxt: continue
        trs.append((i, i + h, int(d), zs[i])); nxt = i + h
    return trs

def simulate(z, beta, thr=1.5, maxN=None):
    zz = z; n = len(zz); ep = np.where(np.abs(zz) > thr, np.sign(zz), 0.0); ep[np.isnan(zz)] = 0
    side = 0; last_ep = 0; k = 0; held = 0; T = []
    for i in range(n):
        if ep[i] != 0 and (i == 0 or ep[i] != ep[i - 1]): k += 1
        eid = k if ep[i] != 0 else 0
        if side != 0:
            held += 1
            if (not np.isnan(zz[i]) and side * zz[i] >= -thr) or (maxN and held >= maxN):
                T[-1][1] = i; side = 0
        if side == 0 and ep[i] != 0 and eid != last_ep and not np.isnan(beta[i]):
            side = int(-ep[i]); last_ep = eid; held = 0
            T.append([i, None, side, zz[i]])
    return [(a, b, c, d) for a, b, c, d in T]

def tt(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    if len(x) < 3 or x.std(ddof=1) == 0: return np.nan
    return x.mean() / (x.std(ddof=1) / math.sqrt(len(x)))
def pval(t, n):
    if not np.isfinite(t): return np.nan
    if sst is not None: return float(2 * sst.t.sf(abs(t), max(n - 1, 1)))
    return math.erfc(abs(t) / math.sqrt(2))

PER = {
    'TAM': (pd.Timestamp('2017-03-06'), pd.Timestamp('2099-01-01')),
    'IS_2017_2021': (pd.Timestamp('2017-03-06'), pd.Timestamp('2021-12-31')),
    'OOS_2022_2026': (pd.Timestamp('2022-01-01'), pd.Timestamp('2099-01-01')),
    'SON2Y': (pd.Timestamp('2024-11-10'), pd.Timestamp('2099-01-01')),
    'Y2026': (pd.Timestamp('2026-01-01'), pd.Timestamp('2099-01-01')),
    'Y2020P': (pd.Timestamp('2020-01-01'), pd.Timestamp('2099-01-01')),
    'SAAT_DONEMI': (pd.Timestamp('2023-11-09'), pd.Timestamp('2099-01-01')),
}
def pstats(df, per, e2=None):
    a, b = PER[per]
    if df is None or len(df) == 0: return dict(n=0)
    m = df[(df.e >= a) & (df.e <= b)]
    if len(m) == 0: return dict(n=0)
    yrs = max((min(b, LAST) - max(a, cal[0])).days / 365.25, 1e-9)
    br = m.brut.to_numpy(); n = len(m)
    top = np.sort(br)[:-10] if n > 10 else np.array([np.nan])
    r = dict(n=n, yillik_n=n / yrs, brut=br.mean(), net8=(br - m.c8).mean(), net15=(br - m.c15).mean(), net_bireysel=(br - m.cr).mean(),
             t=tt(br), isabet=(br > 0).mean(), medyan=np.median(br), brut_ilk10haric=top.mean(), t_ilk10haric=tt(top),
             brut_suruklenme_duz=(m.brut - m.drift).mean(), uzun_pay=m.long.mean(), roll_sayisi=int(m.roll.sum()))
    if e2 is not None and len(e2):
        m2 = e2[(e2.e >= a) & (e2.e <= b)]; r['e2_brut'] = m2.brut.mean() if len(m2) else np.nan
        r['e2_n'] = len(m2)
    if per == 'TAM':
        r['yil_yil'] = ';'.join(f'{y}:{v:.0f}({len(g)})' for y, g in m.groupby(m.e.dt.year) for v in [g.brut.mean()])
    return r

# ------------------------------------------------------------------ KATI_1730 fiyat yardimcilari
def k1730(sym, hm_late=810, hm_early=750, hm_has=870):
    s = HR[HR.sym == sym].copy(); s['d'] = s.ts_utc.dt.tz_convert('UTC').dt.tz_localize(None).dt.normalize()
    s['hm'] = s.ts_utc.dt.hour * 60 + s.ts_utc.dt.minute
    p = s.pivot_table(index='d', columns='hm', values='c', aggfunc='last')
    for c in (hm_late, hm_early, hm_has):
        if c not in p.columns: p[c] = np.nan
    has = p[hm_has].notna()
    px = np.where(has, p[hm_late], p[hm_early])
    return pd.Series(px, index=p.index).reindex(cal)
def kret(sym):
    P = k1730(sym); cprev = SP['c'][sym].shift(1)
    r = np.log(P / cprev); sd = BOL.loc[BOL.sym == sym, 'date']; r[r.index.isin(sd)] = np.nan
    r[(r.abs() > math.log(1.105))] = np.nan
    return r

ROWS = []; TRL = []; DURUM = []; ESIK = []; REFROWS = {}
def emit(kural, surum, trsE0, legs, wts, giris_extra=None, ref=None, light_p=None, ea=None, extra_giris=None):
    e0 = evaluate(trsE0, legs, wts, 0, ea=ea); e2 = evaluate(trsE0, legs, wts, 1)
    sets = [('E0', e0)]
    if ea is not None: pass
    sets.append(('E2', e2))
    if giris_extra: sets += giris_extra
    for g, df in sets:
        for per in PER:
            s = pstats(df, per, e2 if g == 'E0' else None)
            if s['n'] == 0: continue
            row = dict(kural=kural, surum=surum, giris=g, donem=per); row.update(s)
            if g == 'E0' and per == 'TAM':
                row['p_birincil'] = pval(s['t'], s['n']); row['q_fdr'] = ''
                if light_p is not None: row['p_kaydir'] = light_p
                if ref: row['ref_deger'], row['ref_tur'] = ref
            ROWS.append(row)
        if len(df):
            d2 = df.copy(); d2['kural'] = kural; d2['surum'] = surum; d2['giris'] = g; TRL.append(d2)
    return e0, e2

def kaydir(make_trs, legs, wts_fn, actual_trs, reps=300, seed=20261110):
    """dairesel kaydirma: sinyal tarafi (d, z, agirlik) en az 250 gun kaydirilir; istatistik = filtresiz brut ortalama (E0)."""
    rng = np.random.default_rng(seed)
    a = evaluate(actual_trs, legs, wts_fn(0), 0, light=True)
    if len(a) == 0: return np.nan
    act = a.brut.mean(); cnt = 0; tot = 0
    for _ in range(reps):
        k = int(rng.integers(250, N - 250))
        df = evaluate(make_trs(k), legs, wts_fn(k), 0, light=True)
        if len(df) == 0: continue
        tot += 1; cnt += (df.brut.mean() >= act)
    return cnt / tot if tot else np.nan

def mk_fixed(dirs, zs, h):
    return lambda k: greedy(np.roll(dirs, k), np.roll(zs, k), h)

INFO = {}
# ================================================================== KALIBRASYON: SAHOL <- AKBNK.IS (S_KUL)
rX = sret('XU030.IS')
def resid(sym):
    r = sret(sym); b = rbeta(r, rX, 250, 125, 1); e = r - b * rX
    return e, e / e.rolling(120, min_periods=60).std().shift(1)
_, zL = resid('AKBNK.IS'); _, zT = resid('SAHOL.IS')
dK = np.sign(zL.to_numpy()); okk = (np.abs(zL.to_numpy()) >= 1) & (dK * zT.to_numpy() <= 0.25)
dsig = np.where(okk, dK, 0.0)
trK = greedy(dsig, zL.to_numpy(), 2)
kal = evaluate(trK, [leg('SAHOL')], [1.0], 0)
KAL = dict(n=len(kal), brut=kal.brut.mean(), t=tt(kal.brut))
open(EK + 'b4_kalibrasyon.txt', 'w').write(json.dumps(KAL))
print('KALIBRASYON SAHOL<-AKBNK.IS S_KUL E0 h2 tek bacak TAM:', KAL, flush=True)

# ================================================================== SAHTE ONCU SINAMASI (motor testi; ayni kalibrasyon cifti hedefi SAHOL)
def motor(zl_arr):
    d = np.sign(zl_arr); ok = (np.abs(zl_arr) >= 1) & (d * zT.to_numpy() <= 0.25)
    tr = greedy(np.where(ok, d, 0.0), zl_arr, 2)
    df = evaluate(tr, [leg('SAHOL')], [1.0], 0, light=True)
    return len(df), df.brut.mean(), tt(df.brut)
sahte = {}
# (1) hedefin ERTESI gun getirisinin z'si (hedef getirisi artigi: e_T t+1 / sigma_T)
eT, _z = resid('SAHOL.IS'); sigT = eT.rolling(120, min_periods=60).std().shift(1)
z_next = (eT.shift(-1) / sigT.shift(-1)).to_numpy()
# yon: d=sign(zl) ; hedef koşulu d*zT<=0.25 ayni
sahte['ertesi_gun_z'] = motor(z_next)
rng = np.random.default_rng(20261110); noise = rng.standard_normal(N)
sahte['rastgele_gurultu'] = motor(noise)
print('SAHTE ONCU:', sahte, flush=True)
json.dump({k: [float(x) for x in v] for k, v in sahte.items()}, open(EK + 'b4_sahte_oncu.json', 'w'))

# ================================================================== KURAL 1: XU030 baz sicramasi
vg = rd('viop_gunluk'); vg = vg[vg.und == 'XU030'][['date', 'code', 'close', 'settle']]; vg['date'] = pd.to_datetime(vg['date']).dt.normalize()
vg = vg.set_index(['date', 'code'])
cl = vg['close'].where(vg['close'] > 0)
codes = FC['XU030'].to_numpy(); spc = SP['c']['XU030.IS'].to_numpy()
b = np.full(N, np.nan); bprev = np.full(N, np.nan); clo = np.full(N, np.nan)
for i in range(N):
    c = codes[i]
    if isinstance(c, str):
        try: clo[i] = cl.get((cal[i], c), np.nan)
        except Exception: pass
        b[i] = math.log(clo[i] / spc[i]) if np.isfinite(clo[i]) and np.isfinite(spc[i]) else np.nan
        if i > 0:
            try: cp = cl.get((cal[i - 1], c), np.nan)
            except Exception: cp = np.nan
            bprev[i] = math.log(cp / spc[i - 1]) if np.isfinite(cp) and np.isfinite(spc[i - 1]) else np.nan
db = pd.Series(b - bprev, index=cal); db[(db.abs() > 0.5)] = np.nan
sd1 = db.rolling(120, min_periods=60).std().shift(1); z1 = (db / sd1)
d1 = np.where(z1.abs() > 1, -np.sign(z1), 0.0); d1[np.isnan(z1.to_numpy())] = 0
tr1 = greedy(d1, z1.to_numpy(), 1)
leg1 = [leg('XU030')]
settle_arr = FS['XU030'].to_numpy(float)
ea1 = np.log(settle_arr / clo)  # E1: giris son islem fiyati
p1 = kaydir(mk_fixed(d1, z1.to_numpy(), 1), leg1, lambda k: [1.0], tr1)
e0, e2 = emit('K1_XU030_BAZ', 'h1', tr1, leg1, [1.0], ref=('brut_E0_beklenti', 19.0), light_p=p1)
e1 = evaluate(tr1, leg1, [1.0], 0, ea=ea1)
for per in PER:
    s = pstats(e1, per)
    if s['n']: ROWS.append(dict(kural='K1_XU030_BAZ', surum='h1', giris='E1', donem=per, **s, **({'ref_deger': 25.0, 'ref_tur': 'brut_E1_onceki'} if per == 'TAM' else {})))
INFO[1] = dict(z=z1, thr=1.0, d=d1, db=db, sd=sd1)

# ================================================================== KURAL 2: SAHOL/AKBNK z60
rA, rB = sret('SAHOL.IS'), sret('AKBNK.IS')
braw = rA.rolling(250, min_periods=125).cov(rB) / rB.rolling(250, min_periods=125).var(); beta2 = braw.shift(1)
S = (rA - beta2 * rB).fillna(0).cumsum()
z2 = (S - S.rolling(60, min_periods=30).mean()) / S.rolling(60, min_periods=30).std()
bb2 = beta2.to_numpy()
legs2 = [leg('SAHOL'), leg('AKBNK')]
wts2 = lambda k=0: [1.0, -np.roll(bb2, k)]
for ver, mx in (('A_ESIK1.5', None), ('A_3GUN', 3)):
    trs = simulate(z2.to_numpy(), bb2, 1.5, mx)
    closed = [t for t in trs if t[1] is not None]; openp = [t for t in trs if t[1] is None]
    def mk(k, mx=mx): return [t for t in simulate(np.roll(z2.to_numpy(), k), np.roll(bb2, k), 1.5, mx) if t[1] is not None]
    p2 = kaydir(mk, legs2, wts2, closed)
    emit('K2_SAHOL_AKBNK', ver, closed, legs2, wts2(), ref=('net_onceki_rapor', 67.0), light_p=p2)
    INFO[('2', ver)] = dict(open=openp)
INFO[2] = dict(z=z2, beta=beta2, S=S)

# KATI_1730 kural 2
rAk, rBk = kret('SAHOL.IS'), kret('AKBNK.IS')
Sv = S.to_numpy(); zK2 = np.full(N, np.nan)
rAkv, rBkv = rAk.to_numpy(), rBk.to_numpy()
for t in range(60, N):
    if not (np.isfinite(rAkv[t]) and np.isfinite(rBkv[t]) and np.isfinite(bb2[t])): continue
    win = np.r_[Sv[t - 59:t], Sv[t - 1] + rAkv[t] - bb2[t] * rBkv[t]]
    zK2[t] = (win[-1] - win.mean()) / win.std(ddof=1)
for ver, mx in (('A_ESIK1.5', None), ('A_3GUN', 3)):
    trsK = [t for t in simulate(zK2, bb2, 1.5, mx) if t[1] is not None]
    trs0 = [t for t in simulate(z2.to_numpy(), bb2, 1.5, mx) if t[1] is not None]
    eK = evaluate(trsK, legs2, wts2(), 0)
    for per in ('SAAT_DONEMI', 'Y2026'):
        s = pstats(eK, per)
        if s['n']: ROWS.append(dict(kural='K2_SAHOL_AKBNK', surum=ver, giris='KATI_1730', donem=per, **s))
    if len(eK):
        d2 = eK.copy(); d2['kural'] = 'K2_SAHOL_AKBNK'; d2['surum'] = ver; d2['giris'] = 'KATI_1730'; TRL.append(d2)

# ================================================================== KURAL 3: Koza z3
rM, rTa, rEn = sret('TRMET.IS'), sret('TRALT.IS'), sret('TRENJ.IS')
grp = pd.concat([rTa, rEn], axis=1).mean(axis=1, skipna=False)
def cbeta(y, x, lo, hi):
    return (y.rolling(250, min_periods=120).cov(x) / x.rolling(250, min_periods=120).var()).shift(1).clip(lo, hi)
bg = cbeta(rM, grp, 0.2, 2.0); u = rM - bg * grp; sd60 = u.rolling(60, min_periods=40).std()
z3 = u.rolling(3, min_periods=3).sum() / (sd60 * math.sqrt(3)); bH = cbeta(rM, rTa, 0.3, 2.0)
d3 = np.where(z3.abs() > 1.5, np.sign(z3), 0.0); d3[np.isnan(z3.to_numpy())] = 0
tr3 = greedy(d3, z3.to_numpy(), 2)
bHv = bH.to_numpy()
legs3h = [leg('TRMET'), leg('TRALT')]; legs3t = [leg('TRMET')]
p3h = kaydir(mk_fixed(d3, z3.to_numpy(), 2), legs3h, lambda k: [1.0, -np.roll(bHv, k)], tr3)
p3t = kaydir(mk_fixed(d3, z3.to_numpy(), 2), legs3t, lambda k: [1.0], tr3)
# KATI
uK = rMk = kret('TRMET.IS'); grpK = pd.concat([kret('TRALT.IS'), kret('TRENJ.IS')], axis=1).mean(axis=1, skipna=False)
uKv = (kret('TRMET.IS') - bg * grpK)
z3K = (uKv + u.shift(1) + u.shift(2)) / (sd60.shift(1) * math.sqrt(3))
d3K = np.where(z3K.abs() > 1.5, np.sign(z3K), 0.0); d3K[np.isnan(z3K.to_numpy())] = 0
tr3K = greedy(d3K, z3K.to_numpy(), 2)
ekH = evaluate(tr3K, legs3h, [1.0, -bHv], 0); ekT = evaluate(tr3K, legs3t, [1.0], 0)
emit('K3_KOZA_Z3', 'HEDGELI_h2', tr3, legs3h, [1.0, -bHv], ref=('brut_E0_onceki', 45.0), light_p=p3h, giris_extra=[('KATI_1730', ekH)])
emit('K3_KOZA_Z3', 'TEK_TRMET_h2', tr3, legs3t, [1.0], ref=None, light_p=p3t, giris_extra=[('KATI_1730', ekT)])
f3 = np.where((d3 != 0) & (d3 != np.r_[0, d3[:-1]]), d3, 0.0)   # onceki raporun "ilk sinyal gunu" girisi
trf = greedy(f3, z3.to_numpy(), 2)
emit('K3_KOZA_Z3', 'HEDGELI_ILKGUN_h2', trf, legs3h, [1.0, -bHv], ref=('brut_E0_onceki', 45.0))
emit('K3_KOZA_Z3', 'TEK_TRMET_ILKGUN_h2', trf, legs3t, [1.0])
INFO[3] = dict(z=z3, sd60=sd60, d=d3)

# ================================================================== KURAL 4: ABD rafinerileri -> TUPRS
MKT = ownret(DIS, '^GSPC'); RS = {}
for m in ['VLO', 'MPC', 'PSX', 'PBF']:
    r = ownret(DIS, m); rm = MKT.reindex(r.index); bt = rbeta(r, rm, 250, 100, 1); RS[m] = r - bt * rm
dfR = pd.DataFrame(RS); P4 = dfR.mean(axis=1).where(dfR.notna().sum(axis=1) >= 3)
Pb = to_cal(P4, 'right'); sdP = Pb.rolling(250, min_periods=100).std().shift(1); z4 = Pb / sdP
d4 = np.where(z4.abs() > 1, np.sign(z4), 0.0); d4[np.isnan(z4.to_numpy())] = 0
tr4 = greedy(d4, z4.to_numpy(), 2); legs4 = [leg('TUPRS')]
p4 = kaydir(mk_fixed(d4, z4.to_numpy(), 2), legs4, lambda k: [1.0], tr4)
emit('K4_ABD_RAFINERI_TUPRS', 'h2', tr4, legs4, [1.0], ref=('net8_onceki', 42.0), light_p=p4)
INFO[4] = dict(z=z4, Pb=Pb, sdP=sdP)

# ================================================================== KURAL 5: VIOP altin -> TRALT
g5 = FR['XAUUSD']; sg5 = g5.rolling(250, min_periods=100).std().shift(1); z5 = g5 / sg5
d5 = np.where(z5.abs() > 1, np.sign(z5), 0.0); d5[np.isnan(z5.to_numpy())] = 0
rTr = sret('TRALT.IS'); b5 = rbeta(rTr, rX, 250, 125, 1).to_numpy()
tr5 = greedy(d5, z5.to_numpy(), 2)
legs5h = [leg('TRALT'), leg('XU030')]; legs5t = [leg('TRALT')]
p5h = kaydir(mk_fixed(d5, z5.to_numpy(), 2), legs5h, lambda k: [1.0, -np.roll(b5, k)], tr5)
p5t = kaydir(mk_fixed(d5, z5.to_numpy(), 2), legs5t, lambda k: [1.0], tr5)
# KATI: GC=F 14:00 UTC (bar baslangic 13:00 kapanisi) / onceki BIST gunu ayni an
g = HR[HR.sym == 'GC=F'].copy(); g['d'] = g.ts_utc.dt.tz_convert('UTC').dt.tz_localize(None).dt.normalize()
g['h'] = g.ts_utc.dt.hour; gp = g[g.h == 13].drop_duplicates('d', keep='last').set_index('d')['c'].reindex(cal)
gK = np.log(gp / gp.shift(1)); gdiff = (gK - FR['XAUUSD']).abs()
n_roll_drop = int((gdiff > 0.015).sum()); gK[gdiff > 0.015] = np.nan
sgK = gK.rolling(250, min_periods=100).std().shift(1); z5K = gK / sgK
d5K = np.where(z5K.abs() > 1, np.sign(z5K), 0.0); d5K[np.isnan(z5K.to_numpy())] = 0
tr5K = greedy(d5K, z5K.to_numpy(), 2)
e5kH = evaluate(tr5K, legs5h, [1.0, -b5], 0); e5kT = evaluate(tr5K, legs5t, [1.0], 0)
emit('K5_ALTIN_TRALT', 'HEDGELI_h2', tr5, legs5h, [1.0, -b5], ref=('net8_onceki_hedgeli', 51.8), light_p=p5h, giris_extra=[('KATI_1730', e5kH)])
emit('K5_ALTIN_TRALT', 'TEK_TRALT_h2', tr5, legs5t, [1.0], ref=('net8_onceki_ham_h2', 41.6), light_p=p5t, giris_extra=[('KATI_1730', e5kT)])
INFO[5] = dict(z=z5, sd=sg5, K_rolldrop=n_roll_drop)

# ================================================================== KURAL 6: FMG.AX + BHP.AX -> EREGL
IDX = ownret(DIS, '^AXJO'); RS6 = {}
for m in ['FMG.AX', 'BHP.AX']:
    r = ownret(DIS, m); rm = IDX.reindex(r.index); bt = rbeta(r, rm, 250, 100, 1); RS6[m] = r - bt * rm
d6df = pd.DataFrame(RS6); P6 = d6df.mean(axis=1).where(d6df.notna().sum(axis=1) >= 1)
Pb6 = to_cal(P6, 'left'); sdP6 = Pb6.rolling(250, min_periods=100).std().shift(1); z6 = Pb6 / sdP6
d6 = np.where(z6.abs() > 1, np.sign(z6), 0.0); d6[np.isnan(z6.to_numpy())] = 0
tr6 = greedy(d6, z6.to_numpy(), 3); b6 = rbeta(sret('EREGL.IS'), rX, 250, 125, 1).to_numpy()
legs6h = [leg('EREGL'), leg('XU030')]; legs6t = [leg('EREGL')]
p6h = kaydir(mk_fixed(d6, z6.to_numpy(), 3), legs6h, lambda k: [1.0, -np.roll(b6, k)], tr6)
p6t = kaydir(mk_fixed(d6, z6.to_numpy(), 3), legs6t, lambda k: [1.0], tr6)
emit('K6_FMG_BHP_EREGL', 'HEDGELI_h3', tr6, legs6h, [1.0, -b6], ref=('net8_onceki_hedgeli', 46.9), light_p=p6h)
emit('K6_FMG_BHP_EREGL', 'TEK_EREGL_h3', tr6, legs6t, [1.0], ref=('net8_onceki_ham', 51.7), light_p=p6t)
INFO[6] = dict(z=z6, Pb=Pb6, sdP=sdP6)

# ================================================================== KURAL 7: VIOP USDTRY 5g -> THYAO
r7 = FR['USDTRY']; legs7 = [leg('THYAO')]
Z7 = {}
for ver, rr in (('HAM_h3', r7), ('DRIFT_DUZ_h3', r7 - r7.shift(1).rolling(20, min_periods=15).mean())):
    x5 = rr.rolling(5, min_periods=5).sum(); s5 = x5.rolling(250, min_periods=100).std().shift(1); zz = x5 / s5
    dd = np.where(zz.abs() > 1, np.sign(zz), 0.0); dd[np.isnan(zz.to_numpy())] = 0
    trs = greedy(dd, zz.to_numpy(), 3)
    p7 = kaydir(mk_fixed(dd, zz.to_numpy(), 3), legs7, lambda k: [1.0], trs)
    emit('K7_USDTRY5G_THYAO', ver, trs, legs7, [1.0], ref=('net8_onceki_ham', 96.3) if ver.startswith('HAM') else None, light_p=p7)
    Z7[ver] = (zz, s5, x5, dd)
INFO[7] = Z7

# ================================================================== CIKTILAR
pd.DataFrame(ROWS).to_csv(EK + 'eski_b4.csv', sep=';', index=False, float_format='%.4g')
TL = pd.concat(TRL, ignore_index=True)
TL = TL[['kural', 'surum', 'giris', 'e', 'd', 'z', 'x', 'hold', 'brut', 'c8', 'c15', 'cr', 'roll', 'drift']].rename(columns={'e': 'giris_tarihi', 'd': 'yon', 'z': 'z_oncu', 'x': 'cikis_tarihi', 'brut': 'brut_bps', 'cr': 'c_bireysel'})
TL.to_csv(EK + 'islemler_b4.csv', sep=';', index=False, float_format='%.5g')

# ---- durum (son 10 gun)
def durum_rows(kural, z, thr, dirfn, label=''):
    for i in range(N - 10, N):
        zz = z.iloc[i]
        t = int(np.isfinite(zz) and abs(zz) > thr)
        DURUM.append(dict(kural=kural, tarih=cal[i].date(), z=zz, esik=thr, tetik=t, yon=int(dirfn(zz)) if t else 0, not_=label))
durum_rows('K1_XU030_BAZ', z1, 1.0, lambda z: -np.sign(z), 'yon=hedef vadelide, +1 AL')
durum_rows('K2_SAHOL_AKBNK', z2, 1.5, lambda z: -np.sign(z), 'yon=SAHOL spread (+1 SAHOL AL/AKBNK SAT); ilk-gun girisi icin bkz acik_poz')
durum_rows('K3_KOZA_Z3', z3, 1.5, lambda z: np.sign(z), 'yon=TRMET')
durum_rows('K4_ABD_RAFINERI_TUPRS', z4, 1.0, lambda z: np.sign(z), 'yon=TUPRS')
durum_rows('K5_ALTIN_TRALT', z5, 1.0, lambda z: np.sign(z), 'yon=TRALT')
durum_rows('K6_FMG_BHP_EREGL', z6, 1.0, lambda z: np.sign(z), 'yon=EREGL')
durum_rows('K7_USDTRY5G_THYAO_HAM', Z7['HAM_h3'][0], 1.0, lambda z: np.sign(z), 'yon=THYAO')
durum_rows('K7_USDTRY5G_THYAO_DRIFTDUZ', Z7['DRIFT_DUZ_h3'][0], 1.0, lambda z: np.sign(z), 'yon=THYAO')
# acik pozisyon: islemler dosyasindan degil, x>N-1 olanlardan (evaluate X>=N atlar) -> yeniden hesap
def open_pos(kural, trs_all, h=None):
    res = []
    for (e, x, d, z) in trs_all:
        if x is None or x > iL:
            if e <= iL: res.append((cal[e].date(), d, z, 'beklenen_cikis_gun_sayisi' if x is None else x - iL))
    return res
OPEN = {}
OPEN['K1_XU030_BAZ'] = open_pos('', tr1); OPEN['K3_KOZA_Z3'] = open_pos('', tr3); OPEN['K4_ABD_RAFINERI_TUPRS'] = open_pos('', tr4)
OPEN['K5_ALTIN_TRALT'] = open_pos('', tr5); OPEN['K6_FMG_BHP_EREGL'] = open_pos('', tr6)
OPEN['K2_SAHOL_AKBNK_A'] = open_pos('', [t for t in simulate(z2.to_numpy(), bb2, 1.5, None) if t[1] is None])
OPEN['K2_SAHOL_AKBNK_3GUN'] = open_pos('', [t for t in simulate(z2.to_numpy(), bb2, 1.5, 3) if t[1] is None])
for k, (zz, s5, x5, dd) in Z7.items():
    OPEN['K7_' + k] = open_pos('', greedy(dd, zz.to_numpy(), 3))
for k, v in OPEN.items():
    DURUM.append(dict(kural=k, tarih='ACIK_POZ_10.11.2026_KAPANIS', z=np.nan, esik=np.nan, tetik=len(v), yon=(v[0][1] if v else 0), not_=json.dumps([(str(a), int(b), float(c) if np.isfinite(c) else None, str(dd_)) for a, b, c, dd_ in v])))
pd.DataFrame(DURUM).rename(columns={'not_': 'not'}).to_csv(EK + 'durum_b4.csv', sep=';', index=False, float_format='%.4g')

# ---- esik
def cnt(z, thr): zz = z.iloc[-250:]; return int((zz.abs() > thr).sum())
E = []
sdb = db.iloc[-120:].std()
E.append(dict(kural='K1_XU030_BAZ', esik_z=1.0, esik_sade=f'XU030 vadeli-spot (baz) farki bir gunde +-{sdb*1e4:.0f} bps (std son 120 gun); bugun {db.iloc[-1]*1e4:+.0f} bps', gun_250=cnt(z1, 1.0), bugun_z=z1.iloc[-1]))
s60 = S.iloc[-60:]
E.append(dict(kural='K2_SAHOL_AKBNK', esik_z=1.5, esik_sade=f'SAHOL/AKBNK (beta ayarli) orani son 60 gun ortalamasindan +-%{1.5*s60.std()*100:.1f}; bugun ortalamadan %{(S.iloc[-1]-s60.mean())*100:+.1f}', gun_250=cnt(z2, 1.5), bugun_z=z2.iloc[-1]))
E.append(dict(kural='K3_KOZA_Z3', esik_z=1.5, esik_sade=f'TRMET, TRALT/TRENJ ortalamasina gore 3 gunluk birikimli fark +-%{1.5*sd60.iloc[-1]*math.sqrt(3)*100:.1f} (gunluk sapma std %{sd60.iloc[-1]*100:.2f}); bugun 3g toplam %{u.iloc[-3:].sum()*100:+.1f}', gun_250=cnt(z3, 1.5), bugun_z=z3.iloc[-1]))
E.append(dict(kural='K4_ABD_RAFINERI_TUPRS', esik_z=1.0, esik_sade=f'rafineri sepeti (VLO,MPC,PSX,PBF) S&P 500e gore bir ABD gununde +-%{Pb.iloc[-250:].std()*100:.2f}; bugunku (t-1) deger %{Pb.iloc[-1]*100:+.2f}', gun_250=cnt(z4, 1.0), bugun_z=z4.iloc[-1]))
E.append(dict(kural='K5_ALTIN_TRALT', esik_z=1.0, esik_sade=f'VIOP altin (XAUUSD) uzlasma bir gunde +-%{g5.iloc[-250:].std()*100:.2f}; bugun %{g5.iloc[-1]*100:+.2f}', gun_250=cnt(z5, 1.0), bugun_z=z5.iloc[-1]))
E.append(dict(kural='K6_FMG_BHP_EREGL', esik_z=1.0, esik_sade=f'FMG+BHP ortalamasi ASX200e gore +-%{Pb6.iloc[-250:].std()*100:.2f}; bugun %{Pb6.iloc[-1]*100:+.2f}', gun_250=cnt(z6, 1.0), bugun_z=z6.iloc[-1]))
for k, (zz, s5, x5, dd) in Z7.items():
    E.append(dict(kural='K7_USDTRY5G_THYAO_' + k, esik_z=1.0, esik_sade=f'VIOP USDTRY 5 gunluk degisim +-%{x5.iloc[-250:].std()*100:.2f} ({k}); bugun %{x5.iloc[-1]*100:+.2f}', gun_250=cnt(zz, 1.0), bugun_z=zz.iloc[-1]))
pd.DataFrame(E).to_csv(EK + 'esik_b4.csv', sep=';', index=False, float_format='%.4g')
print('KATI rol dusen altin gun:', n_roll_drop, 'tamam', flush=True)
print(pd.DataFrame(E)[['kural', 'esik_sade', 'gun_250', 'bugun_z']].to_string(max_colwidth=130))
