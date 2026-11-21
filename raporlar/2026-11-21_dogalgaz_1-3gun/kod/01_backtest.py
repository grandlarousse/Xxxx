#!/usr/bin/env python3
"""K1 backtest: ABD dogalgaz araclari, kapanista giris, 1-3 gun tasima.

Kullanim:  python -I 01_backtest.py <veri_klasoru> [<cikti_klasoru>]
Cikti: K1_tum_testler.csv, K1_L1.csv, K1_L2.csv, K1_L3.csv, K1_mevsimsellik.csv,
       K1_veri_kontrol.txt (cikti_klasoru; varsayilan ../ek)
Sartname: ek/backtest_sartname.md + ek/M1_yontem_denetimi.md (denetim onceliklidir).
Ileri bakis yok: sinyal t gunu 16:00 ET'ye kadarki veriyle; sigma ve beta t-1'e kadar.
"""
import sys, os, math
import numpy as np, pandas as pd
from scipy import stats

P = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ek')
os.makedirs(OUT, exist_ok=True)
np.seterr(all='ignore')

IS_END = pd.Timestamp('2021-12-31'); OOS_START = pd.Timestamp('2022-01-01')
S24 = pd.Timestamp('2024-01-01'); GAS_IS_START = pd.Timestamp('2011-10-06')
LOG = []
def log(*a):
    s = ' '.join(str(x) for x in a); LOG.append(s)

# ---------------------------------------------------------------- veri
def rd(t):
    f = f"{P}/d_{t}.csv"
    if not os.path.exists(f): return None
    x = pd.read_csv(f, parse_dates=['Date'], index_col='Date').sort_index()
    return x[~x.index.duplicated()]

UNG = rd('UNG'); D = UNG.index; nD = len(D); DI = {d: i for i, d in enumerate(D)}
EQ_COST = {'UNG': 10, 'BOIL': 15, 'KOLD': 15, 'EQT': 6, 'EXE': 6, 'LNG': 6, 'KMI': 6, 'WMB': 6, 'XOP': 6, 'FCG': 15}
def cost_of(t): return EQ_COST.get(t, 12)

RAW = {}
def load(t, kind='eq'):
    """Kapanis/acilis/hacim master takvime (UNG islem gunleri) hizalanir, ileri doldurma yok.
    Gecersiz gun (hacim 0 -> eksik) NaN. Getiriler ardisik gecerli gunler arasinda (vadeli: bosluga izin)."""
    x = rd(t)
    if x is None: return None
    x = x.reindex(D)
    c = x.Close.copy(); o = x.Open.copy(); v = x.Volume.copy()
    bad = c.isna() | (c <= 0)
    if kind in ('eq', 'unl', 'ttf'):
        bad |= (v == 0)
    if kind == 'unl':
        bad |= (c.diff() == 0)
    c[bad] = np.nan; o[bad] = np.nan
    o[(o == c) & (x.High == x.Low)] = np.nan  # acilisi bozuk bar
    if kind in ('fut', 'ttf'):
        prev = c.ffill().shift(1)   # yalniz onceki gecerli kapanisi bulmak icin; sinyal doldurulmaz
    else:
        prev = c.shift(1)
    rcc = c / prev - 1
    ron = o / prev - 1; rid = c / o - 1
    dv = (c * v).where(~bad)
    RAW[t] = dict(c=c, o=o, v=v, rcc=rcc, ron=ron, rid=rid, dv=dv)
    return RAW[t]

for t in ['UNG', 'BOIL', 'KOLD', 'FCG']: load(t, 'eq')
load('UNL', 'unl'); load('TTF_F', 'ttf'); load('NG_F', 'fut')
STK = ['EQT', 'AR', 'RRC', 'CNX', 'CRK', 'EXE', 'GPOR', 'LNG', 'NEXT', 'VG', 'XOP', 'SPY', 'USO', 'KMI', 'WMB']
for t in STK: load(t, 'eq')
# BOIL/KOLD hacmi 0 gunleri: fon fiyati (NAV'a yakin) var; eski donemde seyrek islem. Fiyat korunur (raporlanir).
for t in ['BOIL', 'KOLD']:
    x = rd(t).reindex(D); c = x.Close; RAW[t]['c'] = c; RAW[t]['rcc'] = c / c.shift(1) - 1
    o = x.Open.where(~((x.Open == x.Close) & (x.High == x.Low))); RAW[t]['o'] = o
    RAW[t]['ron'] = o / c.shift(1) - 1; RAW[t]['rid'] = c / o - 1

def lr(t, k='rcc'): return np.log1p(RAW[t][k])
def sig60(r): return r.rolling(60, min_periods=40).std().shift(1)
def zsc(r, cap=None):
    z = r / sig60(r)
    return z.clip(-cap, cap) if cap else z

r_ung = lr('UNG'); z_ung = zsc(r_ung)
ZUNG_ABS = z_ung.abs().values

# ---------------------------------------------------------------- hedefler (matris)
TG = {}; R_CC = []; R_ON = []; R_ID = []; COST = []
def add_target(name, rcc, ron, rid, cost):
    TG[name] = len(R_CC)
    R_CC.append(np.asarray(rcc, float)); R_ON.append(np.asarray(ron, float)); R_ID.append(np.asarray(rid, float))
    COST.append(np.broadcast_to(np.asarray(cost, float), (nD,)).copy())

for t in ['UNG', 'BOIL', 'KOLD'] + STK:
    add_target(t, RAW[t]['rcc'].values, RAW[t]['ron'].values, RAW[t]['rid'].values, cost_of(t))

def beta_lag(ry, rx, n=250):
    cov = ry.rolling(n, min_periods=120).cov(rx); var = rx.rolling(n, min_periods=120).var()
    return (cov / var).shift(1)

def liquid(t):
    med = RAW[t]['dv'].rolling(60, min_periods=40).median().shift(1)
    return (med >= 20e6) & RAW[t]['rcc'].notna()

def basket(members, name, clip=0.15):
    """Esit agirlikli, gunluk dengelenen sepet. Uyelik: onceki 60 gun medyan dolar hacmi >= 20 mn $.
    P&L ham; sinyal icin uye getirileri +-%15'te kirpilmis seri ayrica doner."""
    el = pd.DataFrame({t: liquid(t) for t in members})
    rc = pd.DataFrame({t: RAW[t]['rcc'] for t in members}).where(el)
    ro = pd.DataFrame({t: RAW[t]['ron'] for t in members}).where(el)
    ri = pd.DataFrame({t: RAW[t]['rid'] for t in members}).where(el)
    cst = pd.DataFrame({t: pd.Series(cost_of(t), index=D) for t in members}).where(el)
    n = el.sum(axis=1)
    rb = rc.mean(axis=1).where(n > 0); rbo = ro.mean(axis=1).where(n > 0); rbi = ri.mean(axis=1).where(n > 0)
    rclip = rc.clip(-clip, clip).mean(axis=1).where(n > 0)
    cb = cst.mean(axis=1).fillna(12)
    add_target(name, rb.values, rbo.values, rbi.values, cb.values)
    return dict(r=rb, ro=rbo, ri=rbi, rclip=rclip, cost=cb, n=n, el=el, rc=rc)

GAS = ['EQT', 'AR', 'RRC', 'CNX', 'CRK', 'EXE', 'GPOR']
BK = basket(GAS, 'SEPET'); BKx = basket([t for t in GAS if t != 'CRK'], 'SEPET_CRKsiz')
SM = basket(['CRK', 'AR', 'RRC', 'CNX'], 'KUCUK')
LB = basket(['LNG', 'NEXT', 'VG'], 'LNGSEP')
rx = RAW['XOP']; rs = RAW['SPY']
def hedged(name, b, hx, hname, hcost):
    be = beta_lag(b['r'], hx['rcc'])
    add_target(name, (b['r'] - be * hx['rcc']).values, (b['ro'] - be * hx['ron']).values,
               (b['ri'] - be * hx['rid']).values, (b['cost'] + be.abs().fillna(1) * hcost).values)
    return be
be_bk = hedged('SEPET_h', BK, rx, 'XOP', 6); hedged('SEPET_CRKsiz_h', BKx, rx, 'XOP', 6)
be_sm = hedged('KUCUK_h', SM, rx, 'XOP', 6); hedged('LNGSEP_h', LB, rs, 'SPY', 6)
# E5 icin hisse - (diger uyeler sepeti) hedefleri
for t in GAS:
    others = [o for o in GAS if o != t]
    oth = BK['rc'][others].mean(axis=1)
    add_target(f'{t}_h', (RAW[t]['rcc'] - oth).values, (RAW[t]['ron'] - BK['rc'][others].mean(axis=1) * np.nan).values,
               np.full(nD, np.nan), cost_of(t) + 11)
R_CC = np.vstack(R_CC); R_ON = np.vstack(R_ON); R_ID = np.vstack(R_ID); COST = np.vstack(COST)
YEAR = D.year.values; MON = D.month.values; WINTER = np.isin(MON, [11, 12, 1, 2, 3])

# ---------------------------------------------------------------- motor
def nw_t(x, L):
    x = np.asarray(x, float); T = len(x)
    if T < 10: return np.nan
    m = x.mean(); e = x - m; g0 = e @ e / T; s = g0
    for l in range(1, L + 1):
        s += 2 * (1 - l / (L + 1)) * (e[l:] @ e[:-l]) / T
    return m / math.sqrt(s / T) if s > 0 else np.nan

def trades(tg, ti, d, h, kind='cc'):
    """Islem getirileri (basit): kapanis t -> kapanis t+h. kind on/id: yalniz h=1, sonraki gece/gun ici."""
    tg = np.asarray(tg); ti = np.asarray(ti); d = np.asarray(d, float)
    ok = ti + h < nD; tg, ti, d = tg[ok], ti[ok], d[ok]
    if kind == 'cc':
        F = np.ones(len(ti)); Fo = np.ones(len(ti))
        for k in range(1, h + 1):
            F *= 1 + R_CC[tg, ti + k]
            Fo *= (1 + R_ID[tg, ti + 1]) if k == 1 else (1 + R_CC[tg, ti + k])
        F -= 1; Fo -= 1
    else:
        M = R_ON if kind == 'on' else R_ID
        F = M[tg, ti + 1].copy(); Fo = np.full(len(ti), np.nan)
    ok = np.isfinite(F); return tg[ok], ti[ok], d[ok], F[ok], Fo[ok]

def pstats(tg, ti, d, F, h, kind, cmult=None):
    """Bir donem icin olculer. t: gunluk strateji P&L serisi (cakisan lotlar toplanir), NW gecikme h."""
    o = {}
    n = len(F); o['n'] = n
    if n < 5:
        return o
    g = d * F; c = COST[tg, ti] / 1e4
    net = g - c
    o['ort'] = g.mean() * 1e4; o['med'] = np.median(g) * 1e4; o['net'] = net.mean() * 1e4
    o['isabet'] = (net > 0).mean()
    o['net2x'] = (g - 2 * c).mean() * 1e4
    o['netz'] = (g - c * np.where(ZUNG_ABS[ti] > 2, 2, 1)).mean() * 1e4
    a, b = ti.min(), min(ti.max() + h, nD - 1)
    pnl = np.zeros(nD)
    if kind == 'cc':
        for k in range(1, h + 1):
            np.add.at(pnl, ti + k, d * R_CC[tg, ti + k])
    else:
        M = R_ON if kind == 'on' else R_ID
        np.add.at(pnl, ti + 1, d * M[tg, ti + 1])
    seg = np.nan_to_num(pnl[a + 1:b + 1])
    o['t'] = nw_t(seg, h)
    # ortusmeyen alt kume (giris gunu bazinda ortalama, acgozlu)
    s = pd.Series(g).groupby(ti).mean(); days = s.index.values; vals = s.values
    sel = []; last = -10**9
    for j, dd in enumerate(days):
        if dd >= last + h: sel.append(j); last = dd
    v = vals[sel]; o['n_ind'] = len(v)
    o['t_ind'] = v.mean() / (v.std(ddof=1) / math.sqrt(len(v))) if len(v) > 2 and v.std() > 0 else np.nan
    o['sd_ind'] = v.std(ddof=1) * 1e4 if len(v) > 2 else np.nan
    return o

ROWS = []
def period_mask(ti, lo, hi):
    dt = D[ti]; return (dt >= lo) & (dt <= hi)

def evaluate(cell, tg, ti, d, h, kind='cc', role='sinyal', is_start=None, extra=None, kesif=False):
    tg, ti, d, F, Fo = trades(tg, ti, d, h, kind)
    first = D[0] if is_start is None else is_start
    r = dict(cell); r.update(rol=role, h=h, hedef_tur=kind)
    if extra: r.update(extra)
    allm = D[ti] >= first
    r['n_tum'] = int(allm.sum())
    f0 = max(first, D[ti[allm].min()]) if allm.any() else first
    yrs = max((D[-1] - f0).days / 365.25, 0.25); r['yilda'] = r['n_tum'] / yrs
    for nm, lo, hi in [('IS', first, IS_END), ('OOS', OOS_START, D[-1]), ('s24', S24, D[-1]),
                       ('tum', first, D[-1]), ('pre', D[0], GAS_IS_START - pd.Timedelta(days=1))]:
        if nm == 'pre' and is_start != GAS_IS_START: continue
        m = period_mask(ti, lo, hi)
        st = pstats(tg[m], ti[m], d[m], F[m], h, kind)
        for k, v in st.items(): r[f'{nm}_{k}'] = v
    m = allm
    g = d[m] * F[m]; net = g - COST[tg[m], ti[m]] / 1e4
    if len(g) >= 5:
        r['kis_net'] = net[WINTER[ti[m]]].mean() * 1e4 if WINTER[ti[m]].any() else np.nan
        r['yaz_net'] = net[~WINTER[ti[m]]].mean() * 1e4 if (~WINTER[ti[m]]).any() else np.nan
        go = d[m] * Fo[m]; ok = np.isfinite(go)
        r['acilis_ort'] = go[ok].mean() * 1e4 if ok.sum() > 5 else np.nan
        ys = pd.Series(net).groupby(YEAR[ti[m]]).agg(['mean', 'count']); ys = ys[ys['count'] >= 10]
        r['yil_n'] = len(ys); r['yil_poz'] = (ys['mean'] > 0).mean() if len(ys) else np.nan
        k = int(math.ceil(0.05 * len(net))); r['top5_net'] = np.sort(net)[:-k].mean() * 1e4 if len(net) > k else np.nan
        if h == 1 and kind == 'cc':
            ok2 = ti[m] + 1 < nD
            r['h1_gece'] = np.nanmean(d[m] * R_ON[tg[m], ti[m] + 1]) * 1e4
            r['h1_gun'] = np.nanmean(d[m] * R_ID[tg[m], ti[m] + 1]) * 1e4
    sdi, ni = r.get('OOS_sd_ind', np.nan), r.get('OOS_n_ind', np.nan)
    r['MDE'] = 1.65 * sdi / math.sqrt(ni) if isinstance(ni, (int, float)) and ni and ni > 2 and np.isfinite(sdi) else np.nan
    r['kesif'] = kesif
    ROWS.append(r); return r

# ---------------------------------------------------------------- hucre ureticileri
def ev_from(cond, dirv=None):
    """cond: bool Series (t gunu), dirv: +1/-1 Series. Doner: (ti, d)."""
    c = cond.reindex(D).fillna(False).values.astype(bool)
    ti = np.where(c)[0]
    d = np.ones(len(ti)) if dirv is None else np.sign(dirv.reindex(D).values[ti])
    ok = np.isfinite(d) & (d != 0); return ti[ok], d[ok]

def gas_cell(base, z, k, h, side, extra=None, is_start=GAS_IS_START, kesif=False, kind='cc', rawsig=None):
    """Gaz hedefli hucre: sinyal satiri UNG (birlesik: d=sign(z), momentum konvansiyonu; tek yon: UNG uzun kosullu).
    Tek yonlu hucrede IS isaretine gore islem satirlari: yukari -> BOIL uzun + UNG uzun, asagi -> KOLD uzun."""
    s = z if rawsig is None else rawsig
    if side == 'birlesik': cond = (z.abs() > k) & (s != 0); ti, d = ev_from(cond, s)
    elif side == 'yukari': ti, d = ev_from((z > k) & (s > 0))
    else: ti, d = ev_from((z < -k) & (s < 0))
    cell = dict(base); cell.update(esik=k, yon_kosul=side)
    if extra: cell.update(extra)
    tgu = np.full(len(ti), TG['UNG'])
    r = evaluate(cell, tgu, ti, d, h, kind, 'sinyal', is_start, kesif=kesif)
    if side == 'birlesik':
        r['etiket_rol'] = 'teshis'; return
    m = r.get('IS_ort', np.nan) if not kesif else r.get('tum_ort', np.nan)
    if not np.isfinite(m): return
    prods = ['BOIL', 'UNG'] if m > 0 else ['KOLD']
    for p in prods:
        c2 = dict(cell); c2['urun'] = p; c2['islem_yon'] = 'uzun'
        evaluate(c2, np.full(len(ti), TG[p]), ti, np.ones(len(ti)), h, kind, 'islem', is_start, kesif=kesif)

def stock_cell(base, cond, h, target, tradable, is_start=None, extra=None, dirv=None, extra_targets=()):
    ti, d = ev_from(cond, dirv)
    cell = dict(base); cell.update(hedef=target)
    if extra: cell.update(extra)
    r = evaluate(cell, np.full(len(ti), TG[target]), ti, d, h, 'cc', 'sinyal', is_start)
    for et in extra_targets:  # CRK'siz vb. teshis kolonlari
        tg_, ti_, d_, F, _ = trades(np.full(len(ti), TG[et]), ti, d, h)
        if len(F) > 5: r[f'{et}_ort'] = (d_ * F).mean() * 1e4; r[f'{et}_tum_t'] = pstats(tg_, ti_, d_, F, h, 'cc').get('t')
    if not tradable or dirv is not None:
        r['etiket_rol'] = 'teshis'; return
    c2 = dict(cell); c2['urun'] = tradable; c2['islem_yon'] = 'uzun'
    evaluate(c2, np.full(len(ti), TG[tradable]), ti, np.ones(len(ti)), h, 'cc', 'islem', is_start)

SIDES = ['birlesik', 'yukari', 'asagi']
# G1
for k in [0, 1, 2]:
    for h in [1, 2, 3]:
        for sd in SIDES:
            gas_cell(dict(test='G1', grup=f'G1|{sd}', kural=f'r_UNG z {">" if sd!="asagi" else "<-"}{k} ({sd})', ki=k, hi=h), z_ung, k, h, sd, rawsig=r_ung)
# G2
for w in [3, 5]:
    cum = r_ung.rolling(w).sum(); zc = cum / (sig60(r_ung) * math.sqrt(w))
    for k in [1, 2]:
        for h in [1, 2, 3]:
            for sd in SIDES:
                gas_cell(dict(test='G2', grup=f'G2|{w}|{sd}', kural=f'{w}g birikimli z {sd} |z|>{k}', ki=k, hi=h), zc, k, h, sd)
# G3
ron_u = lr('UNG', 'ron'); rid_u = lr('UNG', 'rid')
for nm, ser in [('gece', ron_u), ('guniçi', rid_u)]:
    zz = zsc(ser)
    for k in [0, 1]:
        for h in [1, 2, 3]:
            for sd in SIDES:
                gas_cell(dict(test='G3', grup=f'G3|{nm}|{sd}', kural=f'r_{nm} z {sd} |z|>{k}', ki=k, hi=h), zz, k, h, sd, rawsig=ser)
# G4 (saatlik, kesif)
H = pd.read_csv(f"{P}/h_UNG.csv"); H['dt'] = pd.to_datetime(H.Datetime.str[:19])
H['dte'] = H.dt.dt.normalize(); H['hm'] = H.dt.dt.strftime('%H:%M')
o1430 = H[H.hm == '14:30'].set_index('dte').Open; c1530 = H[H.hm == '15:30'].set_index('dte').Close
r_set = np.log(c1530 / o1430).reindex(D)
z_set = zsc(r_set)
for k in [0, 1]:
    for kind, hlab in [('on', 'sonraki gece'), ('id', 'sonraki gun ici'), ('cc', 'h=1')]:
        for sd in SIDES:
            gas_cell(dict(test='G4', grup=f'G4|{kind}|{sd}', kural=f'UNG 14:30-16:00 z {sd} |z|>{k} -> {hlab}', ki=k, hi={'on': 0, 'id': 1, 'cc': 2}[kind]),
                     z_set, k, 1, sd, is_start=D[0], kesif=True, kind=kind, rawsig=r_set)
# G5 (EIA: Persembe varsayimi; Persembe tatilse ayni haftanin Carsambasi)
wk = pd.Series(D.isocalendar().week.values * 1 + D.isocalendar().year.values * 100, index=D)
dow = pd.Series(D.dayofweek, index=D)
rel = pd.Series(False, index=D)
for w_, grp in dow.groupby(wk):
    if (grp == 3).any(): rel[grp.index[grp == 3][0]] = True
    elif (grp == 2).any(): rel[grp.index[grp == 2][0]] = True
for k in [0, 1]:
    for h in [1, 2, 3]:
        for sd in SIDES:
            zr = z_ung.where(rel); gas_cell(dict(test='G5', grup=f'G5|{sd}', kural=f'EIA gunu (Per) r_UNG z {sd} |z|>{k}', ki=k, hi=h), zr, k, h, sd, rawsig=r_ung.where(rel))
            # karsilastirma: EIA disi gunler (teshis kolonu)
            zn = z_ung.where(~rel)
            cond = (zn.abs() > k) if sd == 'birlesik' else ((zn > k) & (r_ung > 0) if sd == 'yukari' else (zn < -k) & (r_ung < 0))
            ti, d = ev_from(cond, np.sign(r_ung) if sd == 'birlesik' else None)
            _, ti2, d2, F, _ = trades(np.full(len(ti), TG['UNG']), ti, d, h)
            mm = D[ti2] >= GAS_IS_START
            for rr in ROWS[::-1]:
                if rr.get('test') == 'G5' and rr.get('yon_kosul') == sd and rr.get('esik') == k and rr['h'] == h and rr['rol'] == 'sinyal':
                    rr['karsilastirma_bps'] = (d2[mm] * F[mm]).mean() * 1e4; break
# G6 haftanin gunu
nxt_dow = pd.Series(np.r_[D.dayofweek[1:], -1], index=D)
names = ['Pzt', 'Sal', 'Car', 'Per', 'Cum']
for i, nm in enumerate(names):
    gas_cell(dict(test='G6', grup=f'G6|{nm}', kural=f'bitis gunu {nm} (UNG uzun kosullu)', ki=0, hi=0), (nxt_dow == i).astype(float) * 1, 0.5, 1, 'yukari', rawsig=pd.Series(1.0, index=D))
for nm, msk in [('kis', WINTER), ('yaz', ~WINTER)]:
    cond = ((dow == 4) & pd.Series(msk, index=D)).astype(float)
    gas_cell(dict(test='G6', grup=f'G6|hs_{nm}', kural=f'hafta sonu tasima Cum->Pzt ({nm})', ki=0, hi=0), cond, 0.5, 1, 'yukari', rawsig=pd.Series(1.0, index=D))
# G7 takvim
months = pd.period_range(D[0], D[-1] + pd.offsets.MonthBegin(2), freq='M')
EXP = []
for mth in months:
    j = D.searchsorted(mth.start_time) - 3
    if 0 <= j < nD and D.searchsorted(mth.start_time) < nD: EXP.append(j)
EXP = np.array(sorted(set(EXP)))
def idx_cond(idx):
    s = pd.Series(0.0, index=D); idx = idx[(idx >= 0) & (idx < nD)]; s.iloc[idx] = 1.0; return s
lastd = np.where(np.r_[D.month[1:] != D.month[:-1], True])[0]
for nm, idx, h, des in [('vade_once5', EXP - 6, 5, 'son islem gununden onceki 5 gun (giris E-6, cikis E-1)'),
                         ('vade_sonra5', EXP, 5, 'son islem gununden sonraki 5 gun (giris E, cikis E+5)'),
                         ('UNG_roll', EXP - 11, 4, 'UNG roll yaklasigi: vadeden onceki 10.-7. is gunleri'),
                         ('ay_donumu', lastd - 1, 4, 'ay donumu: son 1 + ilk 3 gun')]:
    gas_cell(dict(test='G7', grup=f'G7|{nm}', kural=des, ki=0, hi=0), idx_cond(idx), 0.5, h, 'yukari', rawsig=pd.Series(1.0, index=D))
# G8 egri vekili
unl = lr('UNL'); dif = (r_ung - unl)
cnt = dif.notna().rolling(20).sum(); s20 = dif.rolling(20, min_periods=15).sum() * 20 / cnt
s20 = s20.where(cnt >= 15); z8 = s20 / (sig60(dif) * math.sqrt(20))
for k, ser in [(0, s20), (1, z8)]:
    for h in [1, 2, 3]:
        for sd in SIDES:
            gas_cell(dict(test='G8', grup=f'G8|{sd}', kural=f'20g (UNG-UNL) {"isaret" if k==0 else "z"} {sd} (neg=contango)', ki=k, hi=h), ser if k else ser, k, h, sd, rawsig=s20)
# T1 trend/kirilim
c_u = RAW['UNG']['c']
for nm, sig in [('MA10', np.sign(c_u - c_u.rolling(10).mean())), ('MA20', np.sign(c_u - c_u.rolling(20).mean())),
                ('kirilim20', np.where(c_u > c_u.rolling(20).max().shift(1), 1, np.where(c_u < c_u.rolling(20).min().shift(1), -1, 0)))]:
    sig = pd.Series(np.asarray(sig, float), index=D)
    for h in [1, 2, 3]:
        for sd in SIDES:
            gas_cell(dict(test='T1', grup=f'T1|{nm}|{sd}', kural=f'{nm} {sd}', ki=0, hi=h), sig, 0, h, sd)
# T2 G1 x oynaklik rejimi (sigma60 kayan 756g yuzdelik)
s60 = sig60(r_ung); pr = s60.rolling(756, min_periods=250).apply(lambda a: (a[:-1] < a[-1]).mean(), raw=True)
reg = pd.cut(pr, [-0.01, 1 / 3, 2 / 3, 1.01], labels=['dusuk', 'orta', 'yuksek'])
for rg in ['dusuk', 'orta', 'yuksek']:
    zr = z_ung.where(reg == rg)
    for k in [0, 1, 2]:
        for sd in SIDES:
            gas_cell(dict(test='T2', grup=f'T2|{rg}|{sd}', kural=f'G1 oyn.{rg} r_UNG z {sd} |z|>{k}', ki=k, hi=0), zr, k, 1, sd, rawsig=r_ung.where(reg == rg))

# E testleri
def eside(z, k, sd):
    if sd == 'birlesik': return (z.abs() > k), np.sign(z)
    if sd == 'yukari': return (z > k), None
    return (z < -k), None
for k in [0, 1, 2]:
    for h in [1, 2, 3]:
        for sd in SIDES:
            cond, dv = eside(z_ung, k, sd)
            if k == 0: cond = cond & (r_ung != 0)
            stock_cell(dict(test='E1', grup=f'E1|ham|{sd}', kural=f'r_UNG z {sd} |z|>{k} -> sepet', ki=k, hi=h, esik=k, yon_kosul=sd), cond, h, 'SEPET', 'SEPET', dirv=dv, extra_targets=('SEPET_CRKsiz',))
            stock_cell(dict(test='E1', grup=f'E1|kor|{sd}', kural=f'r_UNG z {sd} |z|>{k} -> sepet-bXOP', ki=k, hi=h, esik=k, yon_kosul=sd), cond, h, 'SEPET_h', None, dirv=dv)
for w in [3, 5]:
    zc = r_ung.rolling(w).sum() / (sig60(r_ung) * math.sqrt(w))
    for h in [1, 2, 3]:
        for sd in SIDES:
            cond, dv = eside(zc, 1, sd)
            stock_cell(dict(test='E2', grup=f'E2|{w}|ham|{sd}', kural=f'UNG {w}g z {sd} |z|>1 -> sepet', ki=w, hi=h, esik=1, yon_kosul=sd), cond, h, 'SEPET', 'SEPET', dirv=dv, extra_targets=('SEPET_CRKsiz',))
            stock_cell(dict(test='E2', grup=f'E2|{w}|kor|{sd}', kural=f'UNG {w}g z {sd} |z|>1 -> sepet-bXOP', ki=w, hi=h, esik=1, yon_kosul=sd), cond, h, 'SEPET_h', None, dirv=dv)
lx = lr('XOP')
ex_bk = np.log1p(BK['rclip']) - be_bk * lx; z_exbk = zsc(ex_bk)
for k in [0, 1]:
    for h in [1, 2, 3]:
        for sd in SIDES:
            gas_cell(dict(test='E3', grup=f'E3|{sd}', kural=f'sepet fazla getiri z {sd} |z|>{k} -> UNG', ki=k, hi=h), z_exbk, k, h, sd, is_start=GAS_IS_START, rawsig=ex_bk)
eq = np.log1p(RAW['EQT']['rcc'].clip(-.15, .15)); be_eq = beta_lag(eq, lx); z_eq = zsc(eq - be_eq * lx)
for k in [0, 1]:
    for h in [1, 2]:
        for sd in SIDES:
            cond, dv = eside(z_eq, k, sd)
            # sinyal satiri: kucukler fazla getirisi; islem satiri: kucukler sepeti uzun (ham)
            ti, d = ev_from(cond, dv)
            cell = dict(test='E4', grup=f'E4|{sd}', kural=f'EQT fazla getiri z {sd} |z|>{k} -> kucukler', ki=k, hi=h, esik=k, yon_kosul=sd, hedef='KUCUK_h')
            r = evaluate(cell, np.full(len(ti), TG['KUCUK_h']), ti, d, h)
            if sd == 'birlesik': r['etiket_rol'] = 'teshis'; continue
            c2 = dict(cell); c2.update(urun='KUCUK', islem_yon='uzun')
            evaluate(c2, np.full(len(ti), TG['KUCUK']), ti, np.ones(len(ti)), h, 'cc', 'islem')
# E5 sepet ici artik donusu (havuzlanmis)
EV5 = {('al'): [], ('ayna'): []}
for t in GAS:
    others = [o for o in GAS if o != t]
    oth = BK['rc'][others].clip(-.15, .15).mean(axis=1)
    rr = RAW[t]['rcc'].clip(-.15, .15) - oth
    z5 = zsc(rr); el = BK['el'][t].fillna(False)
    for side, cond in [('al', z5 < -1.5), ('ayna', z5 > 1.5)]:
        ti = np.where((cond & el).fillna(False).values)[0]
        EV5[side].append((t, ti))
for side in ['al', 'ayna']:
    for h in [1, 2, 3]:
        for var in ['ham', 'kor']:
            tg = np.concatenate([np.full(len(ti), TG[t if var == 'ham' else f'{t}_h']) for t, ti in EV5[side]])
            ti = np.concatenate([ti for t, ti in EV5[side]]); d = np.ones(len(ti))
            cell = dict(test='E5', grup=f'E5|{side}|{var}', kural=f'hisse-sepet artik z {"<-1.5 AL" if side=="al" else ">+1.5 ayna"} ({var})', ki=0, hi=h, esik=1.5, yon_kosul=side, hedef=f'hisse_{var}')
            r = evaluate(cell, tg, ti, d, h)
            if side == 'ayna' or var == 'kor': r['etiket_rol'] = 'teshis'; continue
            c2 = dict(cell); c2.update(urun='hisse', islem_yon='uzun'); evaluate(c2, tg, ti, d, h, 'cc', 'islem')
# E6 yetisme
ex5 = (np.log1p(BK['rclip']) - be_bk * lx).rolling(5).sum()
gap6 = r_ung.rolling(5).sum() - ex5; z6 = gap6 / (sig60(r_ung - (np.log1p(BK['rclip']) - be_bk * lx)) * math.sqrt(5))
for nm, cond in [('gaz_onde', z6 > 1), ('ayna', z6 < -1)]:
    for h in [1, 2, 3]:
        stock_cell(dict(test='E6', grup=f'E6|{nm}|ham', kural=f'5g UNG - 5g sepet fazla z {">1" if nm=="gaz_onde" else "<-1"} -> sepet', ki=0, hi=h, esik=1, yon_kosul=nm), cond, h, 'SEPET', 'SEPET', extra_targets=('SEPET_CRKsiz',))
        stock_cell(dict(test='E6', grup=f'E6|{nm}|kor', kural=f'5g UNG - 5g sepet fazla z {">1" if nm=="gaz_onde" else "<-1"} -> sepet-bXOP', ki=0, hi=h, esik=1, yon_kosul=nm), cond, h, 'SEPET_h', None)
# X1 TTF
ttf_r = lr('TTF_F'); vpos = (RAW['TTF_F']['v'] > 0).astype(float).rolling(60).mean()
TTF_START = vpos[vpos > 0.9].index[0]
ttf_r = ttf_r.where(D >= TTF_START); z_ttf = zsc(ttf_r, cap=4)
z_ttf_l1 = z_ttf.shift(1)
dpos = pd.Series(np.arange(nD), index=D); firstd = np.where(np.r_[True, D.month[1:] != D.month[:-1]])[0]
turn = np.zeros(nD, bool)
for j in lastd: turn[max(j - 1, 0):j + 1] = True
for j in firstd: turn[j:j + 2] = True
TURN = pd.Series(turn, index=D)
def sens_cols(r, z, k, h, sd):
    out = {}
    for nm, zz in [('ttf_gecikme1', z_ttf_l1), ('ttf_aydonumu_haric', z_ttf.where(~TURN))]:
        if sd == 'birlesik': ti, d = ev_from(zz.abs() > k, np.sign(zz))
        elif sd == 'yukari': ti, d = ev_from(zz > k)
        else: ti, d = ev_from(zz < -k)
        _, ti2, d2, F, _ = trades(np.full(len(ti), TG['UNG']), ti, d, h); mm = D[ti2] >= GAS_IS_START
        r[f'{nm}_ort'] = (d2[mm] * F[mm]).mean() * 1e4 if mm.sum() > 5 else np.nan
for k in [0, 1, 2]:
    for h in [1, 2, 3]:
        for sd in SIDES:
            n0 = len(ROWS)
            gas_cell(dict(test='X1', grup=f'X1|{sd}', kural=f'TTF r z {sd} |z|>{k} -> UNG', ki=k, hi=h), z_ttf, k, h, sd, rawsig=ttf_r)
            sens_cols(ROWS[n0], z_ttf, k, h, sd)
# X2 TTF -> LNG sepeti
for h in [1, 2, 3]:
    for sd in SIDES:
        cond, dv = eside(z_ttf, 1, sd)
        stock_cell(dict(test='X2', grup=f'X2|ham|{sd}', kural=f'TTF z {sd} |z|>1 -> LNG sepeti', ki=1, hi=h, esik=1, yon_kosul=sd), cond, h, 'LNGSEP', 'LNGSEP', dirv=dv)
        stock_cell(dict(test='X2', grup=f'X2|kor|{sd}', kural=f'TTF z {sd} |z|>1 -> LNG sepeti-bSPY', ki=1, hi=h, esik=1, yon_kosul=sd), cond, h, 'LNGSEP_h', None, dirv=dv)
# X3
z_uso = zsc(lr('USO')); z_xop = zsc(lx)
for h in [1, 2]:
    for sd in SIDES:
        gas_cell(dict(test='X3', grup=f'X3|USO|{sd}', kural=f'USO z {sd} |z|>1 -> UNG', ki=1, hi=h), z_uso, 1, h, sd)
for sd in SIDES:
    cond, dv = eside(z_xop, 1, sd)
    stock_cell(dict(test='X3', grup=f'X3|XOP|{sd}', kural=f'XOP z {sd} |z|>1 -> gaz sepeti', ki=1, hi=1, esik=1, yon_kosul=sd), cond, 1, 'SEPET', 'SEPET', dirv=dv)

# ---------------------------------------------------------------- secim kurali ve etiket
df = pd.DataFrame(ROWS)
df['cell_id'] = df['grup'].astype(str) + '|k' + df['ki'].astype(str) + '|h' + df['hi'].astype(str)
sig = df[df.rol == 'sinyal'].copy()
# BH: tum IS testleri (kesif disi), iki yonlu normal p
bh = sig[~sig.kesif & sig.IS_t.notna()].copy()
bh['p'] = 2 * stats.norm.sf(bh.IS_t.abs())
p = bh.p.values; o = np.argsort(p); m = len(p)
q = np.empty(m); q[o] = np.minimum.accumulate((p[o] * m / np.arange(1, m + 1))[::-1])[::-1]
bh['q'] = np.minimum(q, 1)
df.loc[bh.index, 'p_IS'] = bh.p; df.loc[bh.index, 'q_IS'] = bh.q
N_BH = m
sigi = df[df.rol == 'sinyal'].set_index('cell_id')
def neighbors_ok(row):
    g = row.grup; ki = row.ki; hi = row.hi
    same = sigi[(sigi.grup == g)]
    nb = same[((same.ki - ki).abs() + (same.hi - hi).abs()) == 1] if np.issubdtype(type(ki), np.number) else same.iloc[0:0]
    try:
        nb = same[((same.ki.astype(float) - float(ki)).abs() + (same.hi.astype(float) - float(hi)).abs()) == 1]
    except Exception:
        nb = same.iloc[0:0]
    me = sigi.loc[row.cell_id, 'tum_ort']
    if len(nb) == 0: return True, 0
    return bool((np.sign(nb.tum_ort) == np.sign(me)).all()), len(nb)

labels = []
for i, r in df.iterrows():
    sg = sigi.loc[r.cell_id]
    if r.rol == 'sinyal':
        df.loc[i, 'etiket'] = 'teshis (sinyal satiri)'; continue
    a1 = (not r.kesif) and abs(sg.IS_t) >= 2.0 and sg.get('q_IS', 1) <= 0.10 if np.isfinite(sg.IS_t) else False
    if r.kesif:
        a2 = (r.get('tum_t', np.nan) >= 2.0) and (r.get('tum_net', np.nan) > 0)
    else:
        a2 = (r.get('OOS_ort', np.nan) > 0) and (r.get('OOS_t', np.nan) >= 1.65) and (r.get('OOS_net', np.nan) > 0)
    nok, nnb = neighbors_ok(r)
    c_year = (r.get('yil_poz', np.nan) >= 0.6)
    c_top = (r.get('top5_net', np.nan) > 0)
    c_24 = (r.get('s24_net', np.nan) >= 0) if np.isfinite(r.get('s24_net', np.nan)) else False
    gap = (r.get('acilis_ort', np.nan) < 0.5 * r.get('tum_ort', np.nan)) if np.isfinite(r.get('acilis_ort', np.nan)) else False
    a3 = c_year and c_top and nok and c_24
    fails = [n for n, c in [('yil', c_year), ('top5', c_top), ('komsu', nok), ('2024-26', c_24)] if not c]
    df.loc[i, ['adim1', 'adim2', 'adim3']] = [bool(a1), bool(a2), bool(a3)]
    df.loc[i, 'komsu_ok'] = nok; df.loc[i, 'gap_etkisi'] = bool(gap); df.loc[i, 'adim3_eksik'] = ','.join(fails)
    if r.kesif:
        lab = 'IZLE (kesif)' if a2 and c_24 else 'KULLANILAMAZ'
    elif a1 and a2 and a3: lab = 'KULLANILABILIR'
    elif a1 and a2: lab = 'IZLE'
    elif (r.get('OOS_t', np.nan) >= 2.0) and r.get('OOS_net', np.nan) > 0 and c_24: lab = 'IZLE (yalniz OOS)'
    elif a1 and not a2 and np.isfinite(r.get('MDE', np.nan)) and r.MDE > 2 * abs(r.get('IS_ort', np.nan)): lab = 'GUCU YETERSIZ'
    else: lab = 'KULLANILAMAZ'
    if gap and lab != 'KULLANILAMAZ': lab += ' +gap'
    df.loc[i, 'etiket'] = lab
df.loc[df.rol == 'sinyal', 'q_IS'] = df.loc[df.rol == 'sinyal', 'q_IS']
for c in ['p_IS', 'q_IS']:
    df[c] = df.groupby('cell_id')[c].transform('first')
lead = ['test', 'kural', 'rol', 'urun', 'hedef', 'yon_kosul', 'esik', 'h', 'hedef_tur', 'n_tum', 'yilda', 'IS_n', 'IS_ort', 'IS_t', 'IS_t_ind',
        'OOS_n', 'OOS_ort', 'OOS_t', 'OOS_t_ind', 'OOS_med', 'OOS_isabet', 'OOS_net', 'OOS_net2x', 'OOS_netz', 's24_n', 's24_ort', 's24_t', 's24_net',
        'pre_n', 'pre_ort', 'pre_t', 'tum_ort', 'tum_t', 'tum_net', 'kis_net', 'yaz_net', 'acilis_ort', 'yil_n', 'yil_poz', 'top5_net', 'komsu_ok',
        'MDE', 'p_IS', 'q_IS', 'adim1', 'adim2', 'adim3', 'adim3_eksik', 'gap_etkisi', 'etiket']
rest = [c for c in df.columns if c not in lead]
df = df[lead + rest]
num = df.select_dtypes(float).columns; df[num] = df[num].round(3)
df.to_csv(f'{OUT}/K1_tum_testler.csv', index=False)

# ---------------------------------------------------------------- L1, L2, L3
U = RAW['UNG']['rcc']; Bo = RAW['BOIL']['rcc']; Ko = RAW['KOLD']['rcc']
st = np.where(D >= GAS_IS_START)[0][0] + 1
s60g = sig60(r_ung); prl = s60g.rolling(756, min_periods=250).apply(lambda a: (a[:-1] < a[-1]).mean(), raw=True)
L1 = []
for h in [1, 2, 3, 5, 10, 21]:
    starts = np.arange(st, nD - h, h)
    rec = []
    for a in starts:
        u = U.values[a + 1:a + h + 1]; b = Bo.values[a + 1:a + h + 1]; k_ = Ko.values[a + 1:a + h + 1]
        if not (np.isfinite(u).all() and np.isfinite(b).all() and np.isfinite(k_).all()): continue
        Uc = np.prod(1 + u) - 1; Bc = np.prod(1 + b) - 1; Kc = np.prod(1 + k_) - 1
        iB = np.prod(1 + 2 * u) - 1; iK = np.prod(1 - 2 * u) - 1
        rec.append(dict(rej=prl.values[a], sum_u2=(u ** 2).sum(), B_gap=Bc - 2 * Uc, K_gap=Kc + 2 * Uc,
                        B_vol=iB - 2 * Uc, K_vol=iK + 2 * Uc, B_res=Bc - iB + 0.0095 * h / 252, K_res=Kc - iK + 0.0095 * h / 252,
                        ikisi=(Bc < 0) & (Kc < 0)))
    R = pd.DataFrame(rec)
    R['rejim'] = pd.cut(R.rej, [-0.01, 1 / 3, 2 / 3, 1.01], labels=['dusuk', 'orta', 'yuksek'])
    for rg, G in [('tum', R)] + [(x, R[R.rejim == x]) for x in ['dusuk', 'orta', 'yuksek']]:
        L1.append(dict(h=h, rejim=rg, n=len(G), BOIL_fark_bps=G.B_gap.mean() * 1e4, BOIL_oynaklik_bps=G.B_vol.mean() * 1e4,
                       BOIL_s2_yaklasik_bps=-G.sum_u2.mean() * 1e4, ucret_bps=-0.0095 * h / 252 * 1e4, BOIL_artik_bps=G.B_res.mean() * 1e4,
                       KOLD_fark_bps=G.K_gap.mean() * 1e4, KOLD_oynaklik_bps=G.K_vol.mean() * 1e4, KOLD_3s2_yaklasik_bps=-3 * G.sum_u2.mean() * 1e4,
                       KOLD_artik_bps=G.K_res.mean() * 1e4, ikisi_kaybetti=G.ikisi.mean()))
L1 = pd.DataFrame(L1).round(2); L1.to_csv(f'{OUT}/K1_L1.csv', index=False)
L2 = []
for nm, s in [('UNG', U), ('BOIL', Bo), ('KOLD', Ko)]:
    for per, lo, hi in [('2012-2021', '2012-01-01', '2021-12-31'), ('2022-2026', '2022-01-01', '2026-12-31')]:
        for sez, msk in [('tum', np.ones(nD, bool)), ('kis', WINTER), ('yaz', ~WINTER)]:
            x = s[(D >= lo) & (D <= hi) & msk].dropna()
            L2.append(dict(arac=nm, donem=per, sezon=sez, n=len(x), ort_bps=x.mean() * 1e4, t=x.mean() / x.std() * math.sqrt(len(x)), yillik_bilesik=(np.prod(1 + x) ** (252 / len(x)) - 1)))
L2 = pd.DataFrame(L2).round(3); L2.to_csv(f'{OUT}/K1_L2.csv', index=False)
L3 = []
allt = sorted([f[2:-4] for f in os.listdir(P) if f.startswith('d_')])
for t in allt:
    x = rd(t).reindex(D); c = x.Close.where(x.Volume.fillna(1) > 0) if t not in ('NG_F', 'CL_F', 'BZ_F', 'HO_F', 'VIX') else x.Close
    r = c.pct_change(fill_method=None); r3 = c.pct_change(3, fill_method=None)
    rec = dict(arac=t)
    for nm, msk in [('son250', D >= D[-250]), ('2022+', D >= OOS_START)]:
        y = r[msk]; xx = U[msk]; ok = y.notna() & xx.notna()
        if ok.sum() > 50:
            b, a, rv, _, _ = stats.linregress(xx[ok], y[ok]); rec[f'beta_{nm}'] = b; rec[f'R2_{nm}'] = rv ** 2
    rr = r[D >= D[-250]].dropna()
    rec['yillik_oyn'] = rr.std() * math.sqrt(252) if len(rr) > 50 else np.nan
    rec['ort_abs1g_%'] = rr.abs().mean() * 100; rec['ort_abs3g_%'] = r3[D >= D[-250]].abs().mean() * 100
    rec['dolar_hacim_60g_mn'] = (x.Close * x.Volume)[-60:].mean() / 1e6 if t not in ('NG_F', 'TTF_F', 'CL_F', 'BZ_F', 'HO_F', 'VIX') else np.nan
    L3.append(rec)
L3 = pd.DataFrame(L3).round(3); L3.to_csv(f'{OUT}/K1_L3.csv', index=False)
ms = pd.DataFrame(dict(r=U, ay=D.month, yil=D.year))[D >= GAS_IS_START].dropna()
mm = ms.groupby(['yil', 'ay']).r.apply(lambda v: np.prod(1 + v) - 1).reset_index()
SEAS = mm.groupby('ay').r.agg(ort='mean', medyan='median', pozitif_oran=lambda v: (v > 0).mean(), n='count').round(4)
SEAS.to_csv(f'{OUT}/K1_mevsimsellik.csv')

# ---------------------------------------------------------------- veri kontrol ozeti
rn = np.log(rd('NG_F').Close).diff().reindex(D); ddv = (rn - r_ung).abs(); mk = ddv > 0.06
log('NG=F-UNG |fark|>%6 gun:', int(mk.sum()), '; ayin 27-30u:', int((mk & (D.day >= 27)).sum()), '-> NG=F sinyal olarak kullanilmadi')
bs = Bo; us = U; dev = (bs - 2 * us).dropna()
log('BOIL |r|>%60:', int((Bo.abs() > 0.6).sum()), 'KOLD |r|>%60:', int((Ko.abs() > 0.6).sum()), '-> atilan gun 0')
log('BOIL-2xUNG basit |sapma|>%5 gun:', int((dev.abs() > 0.05).sum()), 'KOLD+2xUNG:', int(((Ko + 2 * us).abs() > 0.05).sum()), '(atilmadi; denetim m.6)')
log('BOIL hacim 0 gun:', int((rd('BOIL').Volume == 0).sum()), 'KOLD:', int((rd('KOLD').Volume == 0).sum()), '(fiyat korundu)')
log('UNG acilis=kapanis & H=L (acilis gecersiz) gun:', int(RAW['UNG']['o'].isna().sum()))
log('TTF hacim 0 gun:', int((rd('TTF_F').Volume == 0).sum()), '; X1 baslangic:', TTF_START.date())
log('UNL gecersiz gun (kapanis degismedi ya da hacim 0):', int(RAW['UNL']['c'][D >= '2010-01-05'].isna().sum()))
log('NEXT hacim 0 gun:', int((rd('NEXT').Volume == 0).sum()), '; CRK |r|>%25:', int((RAW['CRK']['rcc'].abs() > 0.25).sum()))
log('G4 saatlik gun (14:30 ve 15:30 bari var):', int(r_set.notna().sum()), 'ilk', r_set.dropna().index[0].date())
log('EIA gunu: Persembe varsayimi (Persembe tatilse ayni haftanin Carsambasi); gercek EIA takvimi kullanilmadi. EIA gun sayisi:', int(rel.sum()))
log('Sepet uye-gun sayisi ort.:', round(BK['n'][D >= '2012'].mean(), 2), '; gaz sepeti ilk gun:', BK['r'].dropna().index[0].date())
log('Toplam sinyal hucresi:', int((df.rol == 'sinyal').sum()), '; BH sayimina giren IS testi:', N_BH, '; kesif (G4):', int(((df.rol == 'sinyal') & df.kesif).sum()))
open(f'{OUT}/K1_veri_kontrol.txt', 'w').write('\n'.join(LOG) + '\n')
print('\n'.join(LOG))
isl = df[df.rol == 'islem']
print(isl.etiket.value_counts().to_string())

# ---------------------------------------------------------------- K1_sonuc.md
def f(x, nd=1):
    try:
        return '' if x is None or not np.isfinite(float(x)) else f"{float(x):.{nd}f}"
    except Exception: return str(x)
isl = df[df.rol == 'islem'].copy(); isl['csv_satir'] = isl.index + 2
good = isl[~isl.etiket.str.startswith('KULLANILAMAZ')]
nulls = isl[isl.etiket.str.startswith('KULLANILAMAZ')].copy()
nulls = nulls.loc[nulls.groupby('test').tum_t.idxmax().dropna()]
def trow(r):
    if r.kesif:
        return (f"| {r.csv_satir} | {r.test} | {r.kural} | {r.urun} h={r.h} | {int(r.n_tum)} / {f(r.yilda,0)} | kesif | tum {f(r.tum_ort)} ({f(r.tum_t,2)}) | "
                f"{f(r.s24_ort)} ({f(r.s24_t,2)}) | {f(r.tum_net)} | {f(r.tum_isabet,2) if 'tum_isabet' in r else ''} | {r.etiket} |")
    return (f"| {r.csv_satir} | {r.test} | {r.kural} | {r.urun} h={r.h} | {int(r.n_tum)} / {f(r.yilda,0)} | {f(r.IS_ort)} ({f(r.IS_t,2)}) | {f(r.OOS_ort)} ({f(r.OOS_t,2)}) | "
            f"{f(r.s24_ort)} ({f(r.s24_t,2)}) | {f(r.OOS_net)} | {f(r.OOS_isabet,2)} | {r.etiket} |")
TAB = ["| CSV satir | test | kural | urun | n / yilda | IS ort bps (t) | OOS ort bps (t) | 2024-26 ort bps (t) | OOS net bps | OOS isabet | etiket |",
       "|---|---|---|---|---|---|---|---|---|---|---|"]
TAB += [trow(r) for _, r in good.iterrows()]
TAB += ['| | | **her testten en guclu bos sonuc (tum donem t en yuksek)** | | | | | | | | |']
TAB += [trow(r) for _, r in nulls.iterrows()]
lc = isl.etiket.value_counts()
md = []
md += ['# K1 — Backtest sonucu (dogalgaz araclari, kapanista giris, 1-3 gun)', '',
       f'Betik: `kod/01_backtest.py <veri>` (tek komut, ~10 sn). Tum satirlar: `ek/K1_tum_testler.csv` ({len(df)} satir). Tarih: {D[-1].date()} son veri.', '',
       '## 1. Veri kontrolu', *[f'- {x}' for x in LOG],
       '- NG=F gunluk ve saatlik seri karistirilmadi; G4 yalniz UNG saatlik barlarla (14:30 bar acilisi -> 15:30 bar kapanisi).',
       '- Bolunme: ham (duzeltilmemis) fiyat yok; duzeltilmis veride |r|>%60 gun 0, atilan gun 0. BOIL-2xUNG sapmalari endeks vade takvimi farkindan; atilmadi.',
       '- Hayatta kalma yanliligi: SWN, eski CHK, CTRA/COG yok; 2021 oncesi sepet yalniz hayatta kalanlar (E testleri iyimser).',
       '- EIA: gercek yayin takvimi yerine Persembe varsayimi. UNG roll penceresi: vade bitiminden onceki 10.-7. is gunu yaklasigi (USCF takvimi kullanilmadi). Is gunu = NYSE islem gunu.',
       '', '## 2. Test sayisi ve etiketler',
       f'- Sinyal hucresi: {int((df.rol=="sinyal").sum())} (BH sayimina giren IS testi {N_BH}; G4 kesif {int(((df.rol=="sinyal") & df.kesif).sum())}, BH disi). Islem satiri: {len(isl)}.',
       f'- En kucuk BH q: {f(df.q_IS.min(),3)}; IS |t|>=2 hucre: {int((df[df.rol=="sinyal"].IS_t.abs()>=2).sum())}. Adim 1 (|t|>=2 ve q<=0,10) gecen hucre: 0.',
       '- Etiketler (islem satiri): ' + '; '.join(f'{k}: {v}' for k, v in lc.items()),
       f'- Sans beklentisi: {len(isl)} islem satirinda OOS t>=2 ile ~%2,5 rastlantisal isabet ~{len(isl)*0.025:.0f} satir; "IZLE (yalniz OOS)" satirlari bu duzeyde.',
       '- Kurallar: IS gaz hucrelerinde 2011-10-06 - 2021-12-31 (UNG 2007-2011 yalniz `pre_*` kolonlari); OOS 2022-01-03+. t: gunluk strateji P&L serisi, cakisan lotlar toplanir, Newey-West gecikme h; `*_t_ind` ortusmeyen alt kume.',
       '- Adim 2-3 islem goren urunle (yukari: BOIL ve UNG uzun; asagi: KOLD uzun; hisse: sepet uzun). Birlesik yon ve korumali satirlar BH\'ye girer, etiket almaz (teshis).',
       '- GUCU YETERSIZ: denetim m.4, adim 1\'i gecip OOS\'de gecemeyen hucrelere uygulanir (MDE > 2x|IS ort|); adim 1 gecen olmadigindan 0. MDE her satirda `MDE` kolonunda.',
       '- Maliyet: taban (UNG 10, BOIL/KOLD 15, hisse 6-12 bps); `OOS_net2x` 2 kat, `OOS_netz` |z_UNG|>2 gunlerinde 2 kat.',
       '', '## 3. Etiketli ozet tablo (KULLANILABILIR + IZLE + her testten en guclu bos sonuc)', *TAB,
       '', '## 4. L1 — kaldirac erimesi (ortusmeyen pencereler, 2011-10+; bps)',
       'fark = gerceklesen - (+-2 x birikimli UNG); oynaklik = ideal gunluk 2x bilesik - 2x birikimli (kesin); s2 yaklasik = -c*Sum(u^2) (log bazli, basit farki abartir); artik = gercek - ideal + ucret (vade takvimi/endeks farki).',
       '', '| h | BOIL fark | BOIL oynaklik | BOIL artik | KOLD fark | KOLD oynaklik | KOLD artik | ucret | ikisi kaybetti |', '|---|---|---|---|---|---|---|---|---|']
for _, r in L1[L1.rejim == 'tum'].iterrows():
    md.append(f"| {r.h} | {r.BOIL_fark_bps} | {r.BOIL_oynaklik_bps} | {r.BOIL_artik_bps} | {r.KOLD_fark_bps} | {r.KOLD_oynaklik_bps} | {r.KOLD_artik_bps} | {r.ucret_bps} | {r.ikisi_kaybetti:.2f} |")
l1r = L1[(L1.h == 10)]
md.append('- h=10 rejime gore BOIL fark / oynaklik: ' + '; '.join(f"{r.rejim} {r.BOIL_fark_bps}/{r.BOIL_oynaklik_bps}" for _, r in l1r.iterrows()) + ' (tamami `ek/K1_L1.csv`).')
md += ['', '## 5. L2 — kosulsuz ortalama gunluk getiri (bps, t)', '| arac | 2012-21 | 2022-26 | kis 2012-21 | yaz 2012-21 | kis 2022-26 | yaz 2022-26 |', '|---|---|---|---|---|---|---|']
for a in ['UNG', 'BOIL', 'KOLD']:
    g = L2[L2.arac == a].set_index(['donem', 'sezon'])
    cell = lambda p, s: f"{g.loc[(p, s), 'ort_bps']:.1f} ({g.loc[(p, s), 't']:.2f})"
    md.append(f"| {a} | {cell('2012-2021','tum')} | {cell('2022-2026','tum')} | {cell('2012-2021','kis')} | {cell('2012-2021','yaz')} | {cell('2022-2026','kis')} | {cell('2022-2026','yaz')} |")
md += ['', '## 6. L3 — maruziyet (secili; tamami `ek/K1_L3.csv`)', '| arac | beta son250 | R2 | beta 2022+ | R2 | yillik oyn | ort abs 1g % | ort abs 3g % | 60g dolar hacmi mn |', '|---|---|---|---|---|---|---|---|---|']
for _, r in L3[L3.arac.isin(['UNG', 'BOIL', 'KOLD', 'FCG', 'EQT', 'EXE', 'AR', 'RRC', 'CNX', 'CRK', 'LNG', 'XOP', 'TTF_F'])].iterrows():
    md.append(f"| {r.arac} | {f(r.beta_son250,2)} | {f(r.R2_son250,2)} | {f(r['beta_2022+'],2)} | {f(r['R2_2022+'],2)} | {f(r.yillik_oyn,2)} | {f(r['ort_abs1g_%'],2)} | {f(r['ort_abs3g_%'],2)} | {f(r.dolar_hacim_60g_mn,0)} |")
g1 = df[(df.test == 'G1') & (df.rol == 'sinyal') & (df.yon_kosul == 'yukari') & (df.esik == 2) & (df.h == 1)].iloc[0]
g1b = df[(df.test == 'G1') & (df.rol == 'sinyal') & (df.yon_kosul == 'yukari') & (df.esik == 1) & (df.h == 1)].iloc[0]
l1a = L1[(L1.rejim == 'tum') & (L1.h == 1)].iloc[0]
md += ['', '## 7. On kayitsiz kesifler (en cok IZLE; hicbiri etiket almadi)',
       f"- BOIL, 2xUNG'yi tek gunde bile ortalama {l1a.BOIL_fark_bps} bps/gun geride izliyor (h=1'de oynaklik erimesi tanim geregi 0; fark ucret {l1a.ucret_bps} + artik {l1a.BOIL_artik_bps}). KOLD artigi {l1a.KOLD_artik_bps} bps/gun. Kaynak: BOIL/KOLD endeksinin (Bloomberg NG alt endeksi) UNG'den farkli vade gecis takvimi. Uzun BOIL tasimanin yapisal maliyeti.",
       f"- Isaret degisimi: UNG z>2 yukari gununden sonra h=1 UNG ort. IS {f(g1.IS_ort)} bps (t {f(g1.IS_t,2)}), OOS {f(g1.OOS_ort)} bps (t {f(g1.OOS_t,2)}), n_OOS {int(g1.OOS_n)}; z>1'de OOS {f(g1b.OOS_ort)} (t {f(g1b.OOS_t,2)}). IS secimi BOIL dedigi icin kural geregi KULLANILAMAZ; 2022+ buyuk yukselis sonrasi donus yalniz gozlem (CSV satir {g1.name + 2}, {g1b.name + 2}).",
       (lambda s_: f"- Isaret kaliciligi (UNG sinyal satirlari, n={len(s_)}): 2007-2011 ile IS ayni isaret %{100*(np.sign(s_.pre_ort)==np.sign(s_.IS_ort)).mean():.0f}, IS ile OOS ayni isaret %{100*(np.sign(s_.OOS_ort)==np.sign(s_.IS_ort)).mean():.0f}.")(df[(df.rol=='sinyal') & df.pre_ort.notna() & df.IS_ort.notna()]),
       '', '## 8. Yapilamayanlar ve sinirlar',
       '- G9 (NOAA HDD): yapilmadi (istege bagli; gorev veri indirmeyi yasakliyor). Test sayimina girmedi.',
       '- Gercek EIA yayin takvimi ve USCF roll takvimi kullanilamadi (yaklasik kurallar; bolum 1).',
       '- Ham fiyatla bolunme orani kontrolu yapilamadi (yalniz duzeltilmis veri); |r|>%60 kontrolu 0 gun.',
       '- Korumali E5 hedefi icin t+1 acilis duyarliligi yok (hisse bazli gece getirisi kurulmadi); teshis satiri.',
       '- Kesif (G4, 2023-12+) satirlarinda IS/OOS ayrimi yok; yon tum donemden secildi, en cok IZLE.',
       '- X1 TTF sinyali 2019-01-25den (hacim kurali); IS yalniz 3 yil. Duyarlilik kolonlari: `ttf_gecikme1_ort`, `ttf_aydonumu_haric_ort`.']
open(f'{OUT}/K1_sonuc.md', 'w').write('\n'.join(md) + '\n')
print('sonuc tablolar yazildi', len(md), 'satir')
