import numpy as np, pandas as pd, warnings, sys
from scipy.optimize import nnls, brentq
warnings.filterwarnings('ignore')
V = '/tmp/claude-0/-home-user-Xxxx/b52fa442-3316-551a-bdd2-9e9f754166e0/scratchpad/veri/panel/'
OUT = '/home/user/Xxxx/raporlar/2026-11-10_viop_leadlag_islem/ek/'
TS = pd.Timestamp
rd = lambda n: pd.read_parquet(V + n + '.parquet')

# ---------------- vadeli paneller (ana takvim) ----------------
fr = rd('fut_ret'); cal = fr.index; ncal = len(cal)
fl = rd('fut_limit'); ft = rd('fut_trades'); fv = rd('fut_value_tl'); fc = rd('fut_code'); fs = rd('fut_settle')
lik = pd.read_csv('/home/user/Xxxx/raporlar/2026-11-02_viop_leadlag/veri_ozet/y_viop_likidite.csv', usecols=['und', 'rt_cost_retail_bps']).drop_duplicates('und').set_index('und').rt_cost_retail_bps
vg = rd('viop_gunluk')[['date', 'code', 'close', 'settle']]
A = {}
for u in ['KCHOL', 'SAHOL', 'AKBNK', 'XU030']:
    cl = pd.DataFrame({'date': cal, 'code': fc[u].values}).merge(vg, on=['date', 'code'], how='left')
    A[u] = dict(r=fr[u].values.astype(float), lim=(fl[u].values == 1), liq=((ft[u] >= 20) & (fv[u] >= 1e6)).values,
                code=fc[u].fillna('').values.astype(object), settle=fs[u].values, close1=cl.close.values.astype(float),
                cost=float(lik.get(u, 22)) if u != 'XU030' else 6.0)
cK = A['KCHOL']['cost']

# ---------------- spot ----------------
sp = rd('spot_gunluk'); sp = sp[sp.date >= '2014-01-01']
D = pd.DatetimeIndex(sorted(sp[sp.sym == 'XU030.IS'].date.unique()))
pv = lambda col: sp.pivot_table(index='date', columns='sym', values=col, aggfunc='last').reindex(D)
ADJ, C, H, L, VO = pv('adj'), pv('c'), pv('h'), pv('l'), pv('v')
R0 = np.log(ADJ).diff(); RC0 = np.log(C).diff()
EX = ((RC0 - R0).abs() > 0.005) & R0.notna()
spl = pd.read_csv(V + 'bolunme_gunleri.csv'); spl['date'] = pd.to_datetime(spl.date)
SPL = pd.DataFrame(False, index=D, columns=ADJ.columns)
for s, d in zip(spl.sym, spl.date):
    if s in SPL.columns and d in D: SPL.loc[d, s] = True
R = R0.copy(); R[(VO == 0) & (H == L)] = np.nan; R[SPL] = np.nan
mg = pd.Series(np.where(D < TS('2020-03-13'), np.log(1.205), np.log(1.105)), index=D)
for c in R.columns:
    if c in ('XU030.IS', 'XBANK.IS'): R.loc[R[c].abs() > 0.5, c] = np.nan
    else: R[c] = R[c].mask(R[c].abs() > mg)
BADI = (EX | SPL)  # saatlik/5dk icin gecersiz gunler
comps = ['TUPRS.IS', 'FROTO.IS', 'TOASO.IS', 'ARCLK.IS', 'YKBNK.IS', 'OTKAR.IS', 'TTRAK.IS', 'AYGAZ.IS']
sade5 = ['TUPRS.IS', 'FROTO.IS', 'YKBNK.IS', 'TOASO.IS', 'ARCLK.IS']
need = comps + ['KCHOL.IS', 'SAHOL.IS', 'AKBNK.IS', 'XU030.IS']


def rbeta(x, m):
    ok = x.notna() & m.notna(); xx = x.where(ok); mm = m.where(ok)
    return (xx.rolling(250, min_periods=125).cov(mm) / mm.rolling(250, min_periods=125).var()).shift(1)


Rm = R['XU030.IS']
B = pd.DataFrame({c: rbeta(R[c], Rm) for c in need})
E = R[need] - B.mul(Rm, axis=0)


def basket(Ef, W):
    ok = Ef.notna() & W.notna()
    num = (W.where(ok) * Ef.where(ok)).sum(axis=1, min_count=1); mass = W.where(ok).sum(axis=1)
    EL = num / mass; EL[mass < 0.5] = np.nan
    return EL


def reg_weights(tgt, cs):
    W = pd.DataFrame(np.nan, index=D, columns=cs); Y = R[tgt].values; X = R[cs].values
    for i in range(250, len(D)):
        y = Y[i - 250:i]; x = X[i - 250:i]
        cols = np.isnan(x).mean(0) < 0.2
        if cols.sum() == 0: continue
        rows = ~np.isnan(y) & ~np.isnan(x[:, cols]).any(1)
        if rows.sum() < 100: continue
        w, _ = nnls(x[rows][:, cols], y[rows]); s = w.sum()
        if s > 0:
            ww = np.full(len(cs), np.nan); ww[cols] = w / s; W.iloc[i] = np.where(np.isnan(ww), 0, ww)
    return W


def mkvar(tgt, cs, W):
    EL = basket(E[cs], W); SL = EL.rolling(120, min_periods=60).std().shift(1)
    ET = E[tgt]; ST = ET.rolling(120, min_periods=60).std().shift(1)
    return dict(tgt=tgt, cs=cs, W=W, SL=SL, ST=ST, zL=EL / SL, zT=ET / ST)


def zalt(v, Rx):
    EL = basket(Rx[v['cs']] - B[v['cs']].mul(Rx['XU030.IS'], axis=0), v['W']) / v['SL']
    ET = (Rx[v['tgt']] - B[v['tgt']] * Rx['XU030.IS']) / v['ST']
    return EL, ET


Wreg = reg_weights('KCHOL.IS', comps)
Wew = pd.DataFrame(1 / 8, index=D, columns=comps)
def Wone(c): return pd.DataFrame({c: 1.0}, index=D)
VAR = {'REG': mkvar('KCHOL.IS', comps, Wreg), 'EW': mkvar('KCHOL.IS', comps, Wew),
       'YKBNK': mkvar('KCHOL.IS', ['YKBNK.IS'], Wone('YKBNK.IS')), 'TUPRS': mkvar('KCHOL.IS', ['TUPRS.IS'], Wone('TUPRS.IS')),
       'SAH_AKB': mkvar('SAHOL.IS', ['AKBNK.IS'], Wone('AKBNK.IS'))}

# ---------------- saatlik 17:30 ve dk5 14:50 fiyatlari ----------------
def hourly_p1730():
    h = rd('saatlik'); h = h[h.sym.isin(need)].copy()
    h['d'] = h.ts_utc.dt.tz_localize(None).dt.normalize(); h['hm'] = h.ts_utc.dt.strftime('%H:%M')
    has = h[h.hm == '14:30'].assign(x=1).pivot_table(index='d', columns='sym', values='x', aggfunc='last').reindex(D).fillna(0) > 0
    c13 = h[h.hm == '13:30'].pivot_table(index='d', columns='sym', values='c', aggfunc='last').reindex(D)
    c12 = h[h.hm == '12:30'].pivot_table(index='d', columns='sym', values='c', aggfunc='last').reindex(D)
    has = has.reindex(columns=c13.columns, fill_value=False)
    P = c12.where(~has, c13)
    return P
P30 = hourly_p1730()
d5 = rd('dk5'); d5 = d5[d5.sym.isin(need) & (d5.ts_utc.dt.strftime('%H:%M') == '14:45')].copy()
d5['d'] = d5.ts_utc.dt.tz_localize(None).dt.normalize()
P50 = d5.pivot_table(index='d', columns='sym', values='c', aggfunc='last').reindex(D)
Cprev = C.shift(1)
def intra_ret(P):
    Rk = np.log(P / Cprev[P.columns]); Rk = Rk.mask(BADI[P.columns]); return Rk
RK30 = intra_ret(P30); RK50 = intra_ret(P50)
KATI0 = D[D >= '2023-12-11'][0]

# ---------------- islem uretici ----------------
def sigd(zL, zT, zthr=1.0, tthr=0.25, kind='KUL'):
    zl = zL.reindex(cal); zt = zT.reindex(cal); d = np.sign(zl)
    if kind == 'KUL': c = (zl.abs() >= zthr) & (d * zt <= tthr)
    elif kind == 'ONCU': c = (zl.abs() >= zthr)
    else: c = (zl.abs() >= zthr) & (d * zt > tthr)
    return d.where(c, 0).fillna(0).values


def gen(und, d, h, mode='E0', hedge=False, xfun=None, bad=None, e1=False, bk=None):
    a = A[und]; r = a['r']; rows = []; busy = -1; cst = a['cost']
    for t in np.flatnonzero(d != 0):
        e = t + 1 if mode == 'E2' else t
        if e < busy or e >= ncal: continue
        x = e + h if xfun is None else xfun(t, e, d[t])
        if x is None or x >= ncal: continue
        if a['lim'][e] or a['lim'][x] or (not a['liq'][e]) or (not a['liq'][x]): continue
        seg = r[e + 1:x + 1]
        if len(seg) == 0 or np.isnan(seg).any(): continue
        if bad is not None and bad[t:x + 1].any(): continue
        g = d[t] * seg.sum()
        if hedge:
            sx = A['XU030']['r'][e + 1:x + 1]; b = bk[t]
            if np.isnan(sx).any() or np.isnan(b): continue
            g -= d[t] * b * sx.sum()
        if e1:
            c1 = a['close1'][e]; s0 = a['settle'][e]
            if not (c1 > 0) or not (s0 > 0): continue
            g += d[t] * np.log(s0 / c1)
        roll = int((a['code'][e:x + 1] != a['code'][e]).any())
        rows.append((cal[t], cal[e], cal[x], int(d[t]), g * 1e4, x - e, roll, cst * (1 + roll) + (6.0 if hedge else 0.0)))
        busy = x
    return pd.DataFrame(rows, columns=['t', 'e', 'x', 'd', 'g', 'hold', 'roll', 'cost'])


PM = {'TAM': lambda e: e >= TS('2017-03-01'), 'IS': lambda e: e < TS('2022-01-01'), 'OOS': lambda e: e >= TS('2022-01-01'),
      'SON2Y': lambda e: e >= TS('2024-11-10'), 'KATIDON': lambda e: e >= KATI0, 'EX2020_22': lambda e: ~e.dt.year.isin([2020, 2021, 2022])}


def stats(df, per):
    if len(df) == 0: return dict(n=0)
    s = df[PM[per](df.e)]; n = len(s)
    if n < 3: return dict(n=n, brut=s.g.mean() if n else np.nan)
    g = s.g; m = g.mean(); t = m / (g.std(ddof=1) / np.sqrt(n)); top = g.sort_values(ascending=False).iloc[10:]
    t10 = top.mean() / (top.std(ddof=1) / np.sqrt(len(top))) if len(top) > 2 else np.nan
    return dict(n=n, brut=m, t=t, med=g.median(), hit=(g > 0).mean(), net=m - s.cost.mean(), ex10=top.mean() if len(top) else np.nan, t10=t10,
                bps_gun=g.sum() / s.hold.sum(), hold=s.hold.mean())


ROWS = []
def rec(kural, surum, giris, cikis, df, pers=('TAM', 'IS', 'OOS', 'SON2Y')):
    for p in pers: ROWS.append(dict(kural=kural, surum=surum, giris=giris, cikis=cikis, donem=p, **stats(df, p)))


def fmt(df, per='TAM'):
    s = stats(df, per); return ' '.join(f'{k}={v:.1f}' if isinstance(v, float) else f'{k}={v}' for k, v in s.items())


LOG = []
def P_(*a): print(*a); LOG.append(' '.join(str(x) for x in a))

# ---------------- A: tum surumler ----------------
SG = {}   # (isim,kind,giris)-> d dizisi
for nm in ['REG', 'EW', 'YKBNK', 'TUPRS', 'SAH_AKB']:
    v = VAR[nm]
    zLk, zTk = zalt(v, RK30)
    for kind in ['KUL', 'ONCU']:
        SG[(nm, kind, 'C')] = sigd(v['zL'], v['zT'], 1.0, 0.25, kind)
        SG[(nm, kind, 'K')] = sigd(zLk, zTk, 1.0, 0.25, kind)
    tg = 'KCHOL' if nm != 'SAH_AKB' else 'SAHOL'
    for kind in ['KUL', 'ONCU']:
        for h in (1, 2, 3):
            dfE0 = gen(tg, SG[(nm, kind, 'C')], h); dfE2 = gen(tg, SG[(nm, kind, 'C')], h, 'E2'); dfK = gen(tg, SG[(nm, kind, 'K')], h)
            rec(nm, 'S_' + kind, 'E0', f'h{h}', dfE0); rec(nm, 'S_' + kind, 'E2', f'h{h}', dfE2)
            rec(nm, 'S_' + kind, 'KATI', f'h{h}', dfK, ('KATIDON', 'SON2Y'))
            rec(nm, 'S_' + kind, 'E0', f'h{h}', dfE0, ('KATIDON',))
            if nm == 'REG' and kind == 'KUL' and h == 2: dfREG = dfE0
# yardimci: ham getiri, sade kural
pct = np.exp(R) - 1
def lead_tgt(pc):
    ld = pc[sade5].mean(axis=1).where(pc[sade5].notna().sum(axis=1) >= 3) - pc['XU030.IS']
    tg = pc['KCHOL.IS'] - pc['XU030.IS']; return ld, tg
ldS, tgS = lead_tgt(pct)
sL = ldS.rolling(120, min_periods=60).std().shift(1); sT = tgS.rolling(120, min_periods=60).std().shift(1)
pK30 = np.exp(RK30) - 1; ldK, tgK = lead_tgt(pK30)
SG[('SADE', 'KUL', 'C')] = sigd(ldS / sL, tgS / sT); SG[('SADE', 'KUL', 'K')] = sigd(ldK / sL, tgK / sT)
def sigfix(ld, tg, x, tt=0.003):
    l = ld.reindex(cal); t_ = tg.reindex(cal); d = np.sign(l); return d.where((l.abs() >= x) & (d * t_ <= tt), 0).fillna(0).values
for x in (0.01, 0.015):
    SG[(f'FIX{x*100:.1f}', 'KUL', 'C')] = sigfix(ldS, tgS, x); SG[(f'FIX{x*100:.1f}', 'KUL', 'K')] = sigfix(ldK, tgK, x)
for nm in ['SADE', 'FIX1.0', 'FIX1.5']:
    lab = nm + ('_KESIF' if nm.startswith('FIX') else '')
    for h in (1, 2, 3):
        dfE0 = gen('KCHOL', SG[(nm, 'KUL', 'C')], h); dfE2 = gen('KCHOL', SG[(nm, 'KUL', 'C')], h, 'E2'); dfK = gen('KCHOL', SG[(nm, 'KUL', 'K')], h)
        rec(lab, 'S_KUL', 'E0', f'h{h}', dfE0); rec(lab, 'S_KUL', 'E2', f'h{h}', dfE2)
        rec(lab, 'S_KUL', 'KATI', f'h{h}', dfK, ('KATIDON', 'SON2Y')); rec(lab, 'S_KUL', 'E0', f'h{h}', dfE0, ('KATIDON',))
        if nm == 'SADE' and h == 2: dfSADE = dfE0

# ---------------- ayrintilar: yon, E1, hedge, esik, ex-temettu, roll, donem ----------------
bk = B['KCHOL.IS'].reindex(cal).values
exd = pd.Series(False, index=D)
for c in ['KCHOL.IS'] + comps: exd |= EX[c].fillna(False)
exd_pos = np.flatnonzero(exd.values); badD = np.zeros(len(D), bool)
for p in exd_pos: badD[max(0, p - 1):p + 2] = True
bad = pd.Series(badD, index=D).reindex(cal).fillna(False).values
sTr = R['KCHOL.IS'].rolling(120, min_periods=60).std().shift(1).reindex(cal).values
for nm, key in [('REG', ('REG', 'KUL', 'C')), ('SADE', ('SADE', 'KUL', 'C'))]:
    d_ = SG[key]; base = gen('KCHOL', d_, 2)
    for y, sub in [('AL', base[base.d > 0]), ('SAT', base[base.d < 0])]: rec(nm, 'S_KUL', 'E0', 'h2_' + y, sub)
    rec(nm, 'S_KUL', 'E1', 'h2', gen('KCHOL', d_, 2, e1=True))
    rec(nm, 'S_KUL', 'E0_hedge', 'h2', gen('KCHOL', d_, 2, hedge=True, bk=bk))
    rec(nm, 'S_KUL', 'E2_hedge', 'h2', gen('KCHOL', d_, 2, 'E2', hedge=True, bk=bk))
    rec(nm, 'S_KUL', 'E0_EXDIV', 'h2', gen('KCHOL', d_, 2, bad=bad))
    rec(nm, 'S_KUL', 'E0_rollsuz', 'h2', base[base.roll == 0]); rec(nm, 'S_KUL', 'E0_rollu', 'h2', base[base.roll == 1])
    rec(nm, 'S_KUL', 'E0_ex2020_22', 'h2', base, ('EX2020_22',))
    base.to_csv(OUT + f'd1_islemler_{nm}_h2.csv', index=False)
    yl = base.assign(y=base.e.dt.year).groupby('y').g.agg(['count', 'mean']).round(1)
    yl2 = gen('KCHOL', d_, 2, 'E2'); yl2 = yl2.assign(y=yl2.e.dt.year).groupby('y').g.agg(['count', 'mean']).round(1)
    P_(nm, 'yil yil E0 h2 (n, ort):', yl.to_dict('index')); P_(nm, 'yil yil E2 h2:', yl2.to_dict('index'))
    top = base.sort_values('g', ascending=False)
    P_(nm, 'en iyi 10 islemin toplami / tum toplam:', round(top.g.iloc[:10].sum() / base.g.sum(), 2), 'en buyuk islem bps', round(top.g.iloc[0], 0), 'ilk 3 yil payi:', base.groupby(base.e.dt.year).g.sum().div(base.g.sum()).round(2).to_dict())
    # DOYGUN
    v = VAR['REG'] if nm == 'REG' else None
    zl = (VAR['REG']['zL'] if nm == 'REG' else ldS / sL).reindex(cal).values; zt = (VAR['REG']['zT'] if nm == 'REG' else tgS / sT).reindex(cal).values
    rK = A['KCHOL']['r']; n_ = ncal
    def xK1(t, e, dd):
        f = max(0, abs(zl[t]) - dd * zt[t]) * sTr[t]
        if np.isnan(f): return None
        cum = 0.0
        for k in (e + 1, e + 2):
            if k >= n_ or np.isnan(rK[k]): return None
            cum += dd * rK[k]
            if cum >= 0.5 * f: return k + 1
        return e + 3
    P30c = P30['KCHOL.IS'].reindex(cal).values; Cc = C['KCHOL.IS'].reindex(cal).values; BAD30 = BADI['KCHOL.IS'].reindex(cal).fillna(False).values
    def x30(t, e, dd):
        if cal[e] < KATI0: return None
        f = max(0, abs(zl[t]) - dd * zt[t]) * sTr[t]
        if np.isnan(f): return None
        for k in (e + 1, e + 2):
            if k >= n_: return None
            p = P30c[k]; c0 = Cc[e]
            if np.isnan(p) or np.isnan(c0) or BAD30[k]: continue
            if dd * np.log(p / c0) >= 0.5 * f: return k
        return e + 3
    dK1 = gen('KCHOL', d_, 0, xfun=xK1); d30 = gen('KCHOL', d_, 0, xfun=x30)
    rec(nm, 'S_KUL', 'E0', 'DOYGUN_K1', dK1); rec(nm, 'S_KUL', 'E0', 'DOYGUN_1730', d30, ('KATIDON', 'SON2Y'))
    for hh in (1, 2, 3): rec(nm, 'S_KUL', 'E0', f'h{hh}_karsilastir', gen('KCHOL', d_, hh), ('KATIDON', 'SON2Y'))
    P_(nm, 'DOYGUN_K1 TAM', fmt(dK1), '| DOYGUN_1730 KATIDON', fmt(d30, 'KATIDON'))
# esik duyarlilik (REG)
v = VAR['REG']
for zt_ in (0.75, 1.0, 1.5, 2.0):
    for tt in (0.0, 0.25, 0.5):
        dd = sigd(v['zL'], v['zT'], zt_, tt); rec('REG', f'S_KUL z>={zt_} t<={tt}', 'E0', 'h2', gen('KCHOL', dd, 2), ('TAM', 'OOS', 'SON2Y'))
# sade esik bugun
tomorrow_sL = ldS.rolling(120, min_periods=60).std().iloc[-1]; tomorrow_sT = tgS.rolling(120, min_periods=60).std().iloc[-1]
P_('SADE esik bugun (dun itibariyle sigma) oncu %', round(sL.iloc[-1] * 100, 2), 'hedef %', round(0.25 * sT.iloc[-1] * 100, 2), '| yarin icin', round(tomorrow_sL * 100, 2), round(0.25 * tomorrow_sT * 100, 2))

# ---------------- B: SAHOL/AKBNK ----------------
rs, ra = R['SAHOL.IS'], R['AKBNK.IS']
bb = rbeta(rs, ra); spr = rs - bb * ra
S = spr.where(bb.notna()).fillna(0).cumsum(); S[:bb.first_valid_index()] = np.nan
zD = (S - S.rolling(60).mean()) / S.rolling(60).std()
zB = zD.reindex(cal).values; bbc = bb.reindex(cal).values
cS, cA = A['SAHOL']['cost'], A['AKBNK']['cost']
def zalt_B(rs_, ra_):
    out = pd.Series(np.nan, index=D); Sv = S.values; bv = bb.values; a_ = rs_.values; b_ = ra_.values
    for j in range(60, len(D)):
        if np.isnan(a_[j]) or np.isnan(b_[j]) or np.isnan(bv[j]) or np.isnan(Sv[j - 1]): continue
        win = Sv[j - 59:j]
        if np.isnan(win).any(): continue
        x = Sv[j - 1] + a_[j] - bv[j] * b_[j]; w = np.append(win, x); out.iat[j] = (x - w.mean()) / w.std(ddof=1)
    return out
zBK = zalt_B(RK30['SAHOL.IS'], RK30['AKBNK.IS']).reindex(cal).values
def genB(z, mode='E0', cap=None, thr=1.5):
    rows = []; inz = np.nan_to_num(np.abs(z), nan=0) > thr; rS = A['SAHOL']['r']; rA = A['AKBNK']['r']
    for t in range(1, ncal):
        if not (inz[t] and not inz[t - 1]): continue
        e = t if mode == 'E0' else t + 1
        if e >= ncal - 1: continue
        k = e + 1
        while k < ncal and inz[k]: k += 1
        if k >= ncal: continue   # acik pozisyon
        x = k if cap is None else min(k, e + cap)
        if x <= e: continue
        ok = all((not A[u]['lim'][i]) and A[u]['liq'][i] for u in ('SAHOL', 'AKBNK') for i in (e, x))
        if not ok: continue
        sS = rS[e + 1:x + 1]; sA = rA[e + 1:x + 1]
        if np.isnan(sS).any() or np.isnan(sA).any() or np.isnan(bbc[t]): continue
        dd = -np.sign(z[t]); g = dd * (sS.sum() - bbc[t] * sA.sum())
        rl = int((A['SAHOL']['code'][e:x + 1] != A['SAHOL']['code'][e]).any()); ra_ = int((A['AKBNK']['code'][e:x + 1] != A['AKBNK']['code'][e]).any())
        rows.append((cal[t], cal[e], cal[x], int(dd), g * 1e4, x - e, rl + ra_, cS * (1 + rl) + cA * (1 + ra_)))
    return pd.DataFrame(rows, columns=['t', 'e', 'x', 'd', 'g', 'hold', 'roll', 'cost'])
for lab, df in [('E0', genB(zB)), ('E2', genB(zB, 'E2')), ('E0_cap3', genB(zB, cap=3)), ('E0_cap5', genB(zB, cap=5)), ('E0_cap10', genB(zB, cap=10))]:
    rec('B_SAHOL_AKBNK', 'bant1.5', lab, 'bant_cikis', df)
    if lab == 'E0': dfB = df
dfBK = genB(zBK); rec('B_SAHOL_AKBNK', 'bant1.5', 'KATI', 'bant_cikis', dfBK, ('KATIDON', 'SON2Y')); rec('B_SAHOL_AKBNK', 'bant1.5', 'E0', 'bant_cikis', dfB, ('KATIDON',))
dfB.to_csv(OUT + 'd1_islemler_B.csv', index=False)
hd = dfB.hold; P_('B tutma gun: n', len(hd), 'medyan', hd.median(), 'p75', hd.quantile(.75), 'p90', hd.quantile(.9), 'ort', round(hd.mean(), 2))
s2 = dfB[dfB.e >= TS('2024-11-10')]
P_('B SON2Y n', len(s2), 'ort', round(s2.g.mean(), 1), 'hold>5 n', int((s2.hold > 5).sum()), 'ort', round(s2[s2.hold > 5].g.mean(), 1), 'hold<=5 ort', round(s2[s2.hold <= 5].g.mean(), 1),
    'toplam payi hold>5', round(s2[s2.hold > 5].g.sum() / s2.g.sum(), 2), 'en iyi 3 toplam payi', round(s2.g.nlargest(3).sum() / s2.g.sum(), 2))
P_('B yil yil E0:', dfB.assign(y=dfB.e.dt.year).groupby('y').g.agg(['count', 'mean']).round(1).to_dict('index'))
P_('B kalibrasyon z 2026-11-03 (beklenen ~ -0.33):', round(zD.loc['2026-11-03'], 2) if TS('2026-11-03') in zD.index else None)

# ---------------- bugunku durum ----------------
last = D[-10:]
rows = []
for dte in last:
    rows.append(dict(tarih=dte.date(), REG_zL=VAR['REG']['zL'].get(dte), REG_zT=VAR['REG']['zT'].get(dte), REG_d=int(np.sign(VAR['REG']['zL'].get(dte))) if abs(VAR['REG']['zL'].get(dte, 0)) >= 1 and np.sign(VAR['REG']['zL'].get(dte)) * VAR['REG']['zT'].get(dte) <= 0.25 else 0,
                     SADE_lead_pct=ldS.get(dte) * 100, SADE_hedef_pct=tgS.get(dte) * 100, SADE_lead_esik_pct=sL.get(dte) * 100, SADE_hedef_esik_pct=0.25 * sT.get(dte) * 100,
                     SADE_d=int(SG[('SADE', 'KUL', 'C')][cal.get_loc(dte)]) if dte in cal else None, B_z=zD.get(dte)))
dur = pd.DataFrame(rows).round(2); dur.to_csv(OUT + 'd1_durum.csv', index=False); P_(dur.to_string())
# B yarin
Sv = S.values; z_now = zD.iloc[-1]; bnow = (rolling_b := (R['SAHOL.IS'].where(rs.notna() & ra.notna()).rolling(250, min_periods=125).cov(ra.where(rs.notna() & ra.notna())) / ra.where(rs.notna() & ra.notna()).rolling(250, min_periods=125).var())).iloc[-1]
win = Sv[-59:]
def zn(x): w = np.append(win, x); return (x - w.mean()) / w.std(ddof=1)
res = {}
for thr in (1.5, -1.5):
    xs = brentq(lambda x: zn(x) - thr, Sv[-1] - 1, Sv[-1] + 1); dS = xs - Sv[-1]   # gereken spread degisimi
    res[thr] = dS
c_S = C['SAHOL.IS'].iloc[-1]; c_A = C['AKBNK.IS'].iloc[-1]
P_('B bugun z', round(z_now, 2), 'beta', round(bnow, 3), 'SAHOL', c_S, 'AKBNK', c_A, 'son tarih', D[-1].date())
for thr, dS in res.items():
    # AKBNK sabit: ln(Ps'/Ps)=dS ; SAHOL sabit: -b*ln(Pa'/Pa)=dS
    P_(f'B yarin esik |z|={thr}: SAHOL sabit iken AKBNK kapanis', round(c_A * np.exp(-dS / bnow), 2), '| AKBNK sabit iken SAHOL kapanis', round(c_S * np.exp(dS), 2))

# ---------------- 17:50 uyumu ----------------
dd5 = [x for x in D if x in P50.dropna(how='all').index][-60:]
def agree(name, a, b):
    a = pd.Series(a); b = pd.Series(b); m = a.notna() & b.notna(); a = a[m].astype(int); b = b[m].astype(int)
    same = (a == b).sum(); sig_c = (a != 0).sum(); both = ((a != 0) & (a == b)).sum(); opp = ((a != 0) & (b != 0) & (a != b)).sum()
    r = dict(kural=name, gun=len(a), ayni_durum=int(same), kapanis_sinyal=int(sig_c), k1450_sinyal=int((b != 0).sum()), ikisinde_ayni_yon=int(both), ters_yon=int(opp), kapanis_sinyali_kacirilan=int(((a != 0) & (b == 0)).sum()), yeni_sinyal=int(((a == 0) & (b != 0)).sum()))
    return r
UY = []
idx5 = pd.DatetimeIndex(dd5)
v = VAR['REG']; zl5, zt5 = zalt(v, RK50)
def dser(zl, zt, kind='KUL'):
    zl = zl.reindex(idx5); zt = zt.reindex(idx5); d = np.sign(zl); c = (zl.abs() >= 1) & (d * zt <= 0.25); return d.where(c, 0).where(zl.notna() & zt.notna())
def dclose(zl, zt):
    zl = zl.reindex(idx5); zt = zt.reindex(idx5); d = np.sign(zl); c = (zl.abs() >= 1) & (d * zt <= 0.25); return d.where(c, 0).where(zl.notna() & zt.notna())
UY.append(agree('A_REG', dclose(v['zL'], v['zT']).values, dser(zl5, zt5).values))
ld5, tg5 = lead_tgt(np.exp(RK50) - 1)
UY.append(agree('A_SADE', dclose(ldS / sL, tgS / sT).values, dser(ld5 / sL, tg5 / sT).values))
z50 = zalt_B(RK50['SAHOL.IS'], RK50['AKBNK.IS']).reindex(idx5)
zc = zD.reindex(idx5)
sg = lambda z: np.where(z.isna(), np.nan, np.where(z.abs() > 1.5, np.sign(z), 0))
UY.append(agree('B_SAHOL_AKBNK', sg(zc), sg(z50)))
uy = pd.DataFrame(UY); uy.to_csv(OUT + 'd1_uyum.csv', index=False); P_(uy.to_string()); P_('dk5 gun araligi', idx5[0].date(), idx5[-1].date(), len(idx5))
ND = pd.DataFrame(ROWS); ND.to_csv(OUT + 'd1_sonuc.csv', index=False)
open(OUT + 'd1_log.txt', 'w').write('\n'.join(LOG))
