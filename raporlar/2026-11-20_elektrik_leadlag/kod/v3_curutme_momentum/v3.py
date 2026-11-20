"""v3.py — V3 çürütme: sektör momentumu sepet kuralları S1 (A5_zirve20_sepet_h3) ve S2 (A2_xelkt_z1_tum_h3).
Kullanım: python3 -I v3.py <panel_full> <cikti.csv> <a7_kapanis_hacim.csv>
Bütün rakamlar bps, maliyet öncesi (aksi yazılmadıkça). 'per' = sinyal günleri − dönemin bütün günleri (sepet düzeyinde).
"""
import os
import sys
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'ortak'))
import elib  # noqa: E402

PANEL, OUT, HACIM = sys.argv[1], sys.argv[2], sys.argv[3]
P = elib.load(PANEL)
sc = elib.sector_cols(P)
idx = P['ret_cc'].index
T0 = pd.Timestamp
PER = {'IS': (None, elib.IS_END), 'OOS1': (elib.OOS1_START, elib.OOS1_END), 'KASA': (elib.KASA_START, None),
       'HAVUZ': (elib.OOS1_START, None)}
ROWS = []


def pm(name):
    a, b = PER[name] if isinstance(name, str) else name
    m = np.ones(len(idx), dtype=bool)
    if a is not None:
        m &= idx >= a
    if b is not None:
        m &= idx <= b
    return m


def st(x, d, h, per):
    m = pm(per)
    xx = x[m]
    dd = (d[m].astype(bool)) & xx.notna()
    xv = xx.where(dd, 0.0).fillna(0.0).values
    dv = dd.values.astype(float)
    mu, t = elib._hac_mean(xv, dv, max(h - 1, 0))
    pos = np.where(dv > 0)[0]
    return int(dv.sum()), elib._indep(pos, h), (1e4 * mu if mu == mu else np.nan), t


def add(sal, kural, tanim, B, d, h, demean=True, pers=('IS', 'OOS1', 'KASA', 'HAVUZ'), note='', show=True):
    out = []
    for p in pers:
        x = B - B[pm(p)].mean() if demean else B
        n, ni, bps, t = st(x, d, h, p)
        ROWS.append(dict(saldiri=sal, kural=kural, tanim=tanim, donem=p, h=h, n_gun=n, n_bagimsiz=ni, bps=bps, t=t, aciklama=note))
        out.append(f'{p} {bps:+.0f} (t {t:.1f}; {n}/{ni})')
    if show:
        print(f'  [{sal}] {kural} | {tanim}: ' + ' | '.join(out))


def rec(sal, kural, tanim, donem, bps, t=np.nan, n=np.nan, ni=np.nan, h=3, note=''):
    ROWS.append(dict(saldiri=sal, kural=kural, tanim=tanim, donem=donem, h=h, n_gun=n, n_bagimsiz=ni, bps=bps, t=t, aciklama=note))


# ---------------------------------------------------------------- sinyaller
L = P['idx'].reindex(idx)
r = P['idx_ret'].reindex(idx)


def zs(x):
    return x / x.rolling(60, min_periods=40).std().shift(1)


def hi(x, w):
    return (x >= x.rolling(w, min_periods=w).max()).fillna(False)


def lo(x, w):
    return (x <= x.rolling(w, min_periods=w).min()).fillna(False)


zE = zs(r['XELKT'])
SIG = {'S1': hi(L['XELKT'], 20), 'S2': (zE >= 1).fillna(False)}
_FX = {}


def fx(h):
    if h not in _FX:
        _FX[h] = elib.fwd_exec(P, h, 'long', sc)
    return _FX[h]


def basket(h, mask=None, min_n=5, F=None):
    f, fl, _ = fx(h)
    if F is not None:
        f = F
    X = f.where(fl if mask is None else (fl & mask))
    n = X.notna().sum(axis=1)
    return X.mean(axis=1).where(n >= min_n)


B = {h: basket(h) for h in (1, 2, 3, 5)}
B3 = B[3]

# ---------------------------------------------------------------- 0. yeniden üretim
print('== 0. yeniden üretim (elib.evaluate, per) ve bağımsız hesap')
for k in ('S1', 'S2'):
    sigm = pd.DataFrame(np.repeat(SIG[k].values[:, None], len(sc), axis=1), index=idx, columns=sc)
    if k == 'S2':
        sigm = sigm & P['tradable'][sc]
    for mode in ('uc_parca', 'havuz'):
        elib.PERIOD_MODE = mode
        P['_cache'] = {}
        row = elib.evaluate(sigm, P, h=3, measure='per', min_n=5, name=k)
        print('  elib', k, mode, {q: round(v, 2) for q, v in row.items() if q.startswith(('ort_fazla', 't_', 'n_gun', 'n_bagimsiz', 'basabas', 'net_temel', 'net_muh'))})
        if mode == 'havuz':
            rec('0_yeniden', k, 'elib per (hisse düzeyi dönem-nötr), havuz 2023+', 'HAVUZ', row['ort_fazla_OOS_bps'], row['t_OOS'], row['n_gun_OOS'], row['n_bagimsiz_OOS'])
            rec('5_maliyet', k, 'işlem başına başabaş (per)', 'HAVUZ', row['basabas_OOS_bps'])
            rec('5_maliyet', k, 'net temel (per − maliyet)', 'HAVUZ', row['net_temel_bps_OOS'])
            rec('5_maliyet', k, 'net muhafazakâr (per − maliyet)', 'HAVUZ', row['net_muhafazakar_bps_OOS'])
    add('0_yeniden', k, 'sepet düzeyi per (kendi kodum, elib.fwd_exec)', B3, SIG[k], 3)
    add('0_yeniden', k, 'ham getiri (kıyassız)', B3, SIG[k], 3, demean=False)
elib.PERIOD_MODE = 'havuz'
P['_cache'] = {}
# bağımsız: px.parquet düzeltilmiş kapanışından
px = P['px'].copy()
px['date'] = pd.to_datetime(px['date'])
C = px.pivot_table(index='date', columns='sym', values='c', aggfunc='last').reindex(index=idx, columns=sc)
f3i = C.shift(-3) / C - 1
B3i = f3i.where(P['fill_long'][sc]).mean(axis=1).where(f3i.where(P['fill_long'][sc]).notna().sum(axis=1) >= 5)
for k in ('S1', 'S2'):
    add('0_yeniden', k, 'bağımsız (px.c düzeyinden, kilit kaydırmasız) per', B3i, SIG[k], 3)

# ---------------------------------------------------------------- 1. kıyas
print('== 1. kıyas')
ym = pd.Series(idx.to_period('M'), index=idx)
ewd = elib.ew_basket(P)
for k in ('S1', 'S2'):
    d = SIG[k]
    c60 = B3.rolling(121, center=True, min_periods=60).mean()
    add('1_kiyas', k, '(i) ±60 gün merkezli ortalama (bütün günler)', B3 - c60, d, 3, demean=False)
    Bn = B3.where(~d)
    c60x = Bn.rolling(121, center=True, min_periods=20).mean()
    add('1_kiyas', k, '(i-b) ±60 gün merkezli, yalnız sinyalsiz günler', B3 - c60x, d, 3, demean=False)
    c20x = Bn.rolling(41, center=True, min_periods=8).mean()
    add('1_kiyas', k, '(i-c) ±20 gün merkezli, yalnız sinyalsiz günler', B3 - c20x, d, 3, demean=False)
    mb = Bn.groupby(ym).transform('mean').where(Bn.groupby(ym).transform('count') >= 3)
    add('1_kiyas', k, '(ii) aynı ayın sinyalsiz günleri', B3 - mb, d, 3, demean=False)
    for mk in ('XU100', 'XU030'):
        beta = (ewd.rolling(250, min_periods=60).cov(r[mk]) / r[mk].rolling(250, min_periods=60).var()).shift(1).fillna(1.0)
        fm = elib.fwd_simple(r[[mk]], 3)[mk]
        add('1_kiyas', k, f'(iii) β·{mk} korumalı, per', B3 - beta * fm, d, 3)
        if k == 'S1':
            add('1_kiyas', k, f'    aynı günlerde {mk} kendisi f3 (per)', fm, d, 3)
# genel momentum mu: aynı kural endekslerin kendisine
for X in ['XELKT', 'XU030', 'XU100', 'XUTUM', 'XUSIN', 'XUHIZ']:   # XBANK: IS'te seri kırığı var, alınmadı
    fX = elib.fwd_simple(r[[X]], 3)[X]
    add('1_genel', 'S1-tipi', f'{X} 20g zirve → {X} f3 (per)', fX, hi(L[X], 20), 3, pers=('IS', 'HAVUZ'))
    add('1_genel', 'S2-tipi', f'{X} z≥1 → {X} f3 (per)', fX, (zs(r[X]) >= 1).fillna(False), 3, pers=('IS', 'HAVUZ'))
hM = hi(L['XU100'], 20)
zM = zs(r['XU100'])
add('1_ozgu', 'S1', 'XELKT zirve & XU100 zirve DEĞİL → sepet', B3, SIG['S1'] & ~hM, 3)
add('1_ozgu', 'S1', 'XELKT zirve & XU100 zirve → sepet', B3, SIG['S1'] & hM, 3)
add('1_ozgu', 'S1', 'XU100 zirve & XELKT zirve DEĞİL → sepet', B3, hM & ~SIG['S1'], 3)
add('1_ozgu', 'S2', 'XELKT z≥1 & XU100 z<1 → sepet', B3, SIG['S2'] & ~(zM >= 1), 3)
add('1_ozgu', 'S2', 'XELKT z≥1 & XU100 z≥1 → sepet', B3, SIG['S2'] & (zM >= 1), 3)
add('1_ozgu', 'S2', 'XU100 z≥1 & XELKT z<1 → sepet', B3, (zM >= 1) & ~SIG['S2'], 3)
add('1_ortusme', 'S1∩S2', 'ikisi birden', B3, SIG['S1'] & SIG['S2'], 3)
add('1_ortusme', 'S1\\S2', 'yalnız zirve (z<1)', B3, SIG['S1'] & ~SIG['S2'], 3)
add('1_ortusme', 'S2\\S1', 'yalnız z≥1 (zirve değil)', B3, SIG['S2'] & ~SIG['S1'], 3)


# ---- 1b. rejim denetimi: t anında bilinen rejim değişkenleriyle
LE = L['XELKT']
r20 = LE / LE.shift(20) - 1
r60 = LE / LE.shift(60) - 1
near = (LE >= 0.98 * LE.rolling(20, min_periods=20).max()) & ~SIG['S1']
up60 = LE > LE.rolling(60, min_periods=60).mean()


def within(sal, k, tanim, d, ctrl, h=3):
    out = []
    for p in ('IS', 'OOS1', 'KASA', 'HAVUZ'):
        mm = pd.Series(pm(p), index=idx) & ctrl
        x = B[h] - B[h][mm].mean()
        n, ni, bps, t = st(x, d & ctrl, h, p)
        rec(sal, k, tanim, p, bps, t, n, ni, h)
        out.append(f'{p} {bps:+.0f} (t {t:.1f}; {n}/{ni}; rejim günü {int(mm.sum())})')
    print(f'  [{sal}] {k} | {tanim}: ' + ' | '.join(out))


add('1_rejim', 'S1', 'XELKT zirveye ≤%2 yakın ama zirve DEĞİL → sepet (per)', B3, near, 3)
add('1_rejim', 'S1', 'XELKT 60g ortalamasının üstünde (bütün günler) → sepet (per)', B3, up60, 3)
add('1_rejim', 'S1', 'XELKT 20g getirisi > 0 (bütün günler) → sepet (per)', B3, (r20 > 0), 3)
for k in ('S1', 'S2'):
    within('1_rejim', k, 'rejim içi fark: yalnız "XELKT 60g ort. üstünde" günleri içinde sinyal − sinyalsiz', SIG[k], up60)
    within('1_rejim', k, 'rejim içi fark: yalnız "20g getiri > 0" günleri içinde', SIG[k], (r20 > 0))
    within('1_rejim', k, 'rejim içi fark: yalnız "zirveye ≤%2 yakın ya da zirve" günleri içinde', SIG[k], near | SIG['S1'])


def ols_hac(y, X, lag=5):
    df = pd.concat([y.rename('y'), X], axis=1).dropna()
    A = np.column_stack([np.ones(len(df)), df.drop(columns='y').values])
    b = np.linalg.lstsq(A, df['y'].values, rcond=None)[0]
    u = df['y'].values - A @ b
    Z = A * u[:, None]
    S_ = Z.T @ Z
    for j in range(1, lag + 1):
        G = Z[j:].T @ Z[:-j]
        S_ += (1 - j / (lag + 1)) * (G + G.T)
    Ai = np.linalg.inv(A.T @ A)
    V = Ai @ S_ @ Ai
    return b[1:], b[1:] / np.sqrt(np.diag(V)[1:]), len(df)


for k in ('S1', 'S2'):
    for p in ('IS', 'HAVUZ', 'KASA'):
        mm = pm(p)
        Xr = pd.DataFrame({'sig': SIG[k].astype(float), 'r20': r20, 'r60': r60, 'xu100_r20': L['XU100'] / L['XU100'].shift(20) - 1})[mm]
        b, t, n = ols_hac(B3[mm], Xr)
        print(f'  [1_rejim] {k} {p} regresyon B3 ~ sinyal + XELKT r20 + r60 + XU100 r20 (HAC 5): sinyal {1e4 * b[0]:+.0f} bps (t {t[0]:.1f}); r20 katsayı {b[1]:+.3f} (t {t[1]:.1f}); r60 {b[2]:+.3f} (t {t[2]:.1f}); n {n}')
        rec('1_rejim', k, 'regresyon: sinyal katsayısı (kontrol: XELKT r20, r60, XU100 r20)', p, 1e4 * b[0], t[0], n)

# ---- 1c. yerel kıyasların mekanik yanlılığı: günleri karıştırılmış (öngörülebilirlik yok) dünyada aynı ölçüler
def loc_meas(rI, rB, k, mm):
    LI = (1 + rI).cumprod()
    LB = (1 + rB).cumprod()
    f = LB.shift(-3) / LB - 1
    d = hi(LI, 20) if k == 'S1' else ((rI / rI.rolling(60, min_periods=40).std().shift(1)) >= 1).fillna(False)
    d = d & f.notna() & pd.Series(mm, index=rI.index)
    fn = f.where(~d)
    o = {'per': (f - f[mm].mean())[d].mean(),
         'c60': (f - f.rolling(121, center=True, min_periods=60).mean())[d].mean(),
         'c60x': (f - fn.rolling(121, center=True, min_periods=20).mean())[d].mean(),
         'c20x': (f - fn.rolling(41, center=True, min_periods=8).mean())[d].mean(),
         'ay': (f - fn.groupby(ym).transform('mean').where(fn.groupby(ym).transform('count') >= 3))[d].mean()}
    return {q: 1e4 * v for q, v in o.items()}


rI0, rB0 = r['XELKT'].fillna(0.0), ewd.fillna(0.0)
rng = np.random.default_rng(11)
for k in ('S1', 'S2'):
    for p in ('IS', 'HAVUZ'):
        mm = pm(p)
        act = loc_meas(rI0, rB0, k, mm)
        pos_ = np.where(mm)[0]
        nul = []
        for _ in range(300):
            perm = rng.permutation(pos_)
            a, b_ = rI0.values.copy(), rB0.values.copy()
            a[pos_], b_[pos_] = a[perm], b_[perm]
            nul.append(loc_meas(pd.Series(a, index=idx), pd.Series(b_, index=idx), k, mm))
        nul = pd.DataFrame(nul)
        txt = []
        for q in ('per', 'c60', 'c60x', 'c20x', 'ay'):
            pv = float((nul[q] >= act[q]).mean())
            txt.append(f'{q}: gerçek {act[q]:+.0f}, sıfır dünyası ort {nul[q].mean():+.0f} → düzeltilmiş {act[q] - nul[q].mean():+.0f} (p {pv:.3f})')
            rec('1_yanlilik', k, f'{q}: düzeltilmiş (gerçek − karıştırılmış dünya ortalaması); basit EW sepet', p, act[q] - nul[q].mean(), note=f'gerçek {act[q]:+.0f}; sıfır ort {nul[q].mean():+.0f}; karıştırma p {pv:.3f}')
        print(f'  [1_yanlilik] {k} {p} ' + ' | '.join(txt))

# ---------------------------------------------------------------- 2. kümelenme
print('== 2. kümelenme')


def waves(d, gap):
    pos = np.where(d.values)[0]
    lab = pd.Series(-1, index=idx)
    w, last = -1, -10 ** 9
    for i in pos:
        if i - last > gap:
            w += 1
        lab.iloc[i] = w
        last = i
    return lab


def boot(Bx, d, per, block=10, n=4000, seed=7):
    m = pm(per)
    x = Bx[m].values
    dd = (d[m].values.astype(bool)) & np.isfinite(x)
    Tn = len(x)
    nb = int(np.ceil(Tn / block))
    rng = np.random.default_rng(seed)
    out = np.empty(n)
    ar = np.arange(block)
    for i in range(n):
        s = rng.integers(0, Tn, nb)
        ind = ((s[:, None] + ar) % Tn).ravel()[:Tn]
        xs, ds = x[ind], dd[ind]
        out[i] = np.nanmean(xs[ds]) - np.nanmean(xs) if ds.sum() > 2 else np.nan
    return 1e4 * np.nanpercentile(out, [5, 50, 95]), float(np.nanmean(out <= 0)), out


for k in ('S1', 'S2'):
    d = SIG[k] & B3.notna()
    for per in ('KASA', 'HAVUZ'):
        m = pm(per)
        x = (B3 - B3[m].mean())
        dm = d & pd.Series(m, index=idx)
        for gap in (3, 10):
            lab = waves(dm, gap)
            ws = x[dm].groupby(lab[dm]).agg(['sum', 'count', 'mean'])
            ws = ws.sort_values('sum', ascending=False)
            tot = ws['sum'].sum()
            rest = (tot - ws['sum'].iloc[:3].sum()) / max(ws['count'].iloc[3:].sum(), 1)
            first_dates = [dm[lab == w].index[0].strftime('%Y-%m-%d') for w in ws.index[:3]]
            print(f'  [2] {k} {per} boşluk>{gap}: {len(ws)} dalga, {int(dm.sum())} gün; artı dalga {int((ws["sum"] > 0).sum())}; '
                  f'en iyi 3 dalganın payı {ws["sum"].iloc[:3].sum() / tot:.0%} ({first_dates}; gün {ws["count"].iloc[:3].tolist()}); '
                  f'en iyi 3 dalga hariç gün ort {1e4 * rest:+.0f}; dalga ortalamalarının ort {1e4 * ws["mean"].mean():+.0f}, medyan {1e4 * ws["mean"].median():+.0f}')
            rec('2_kume', k, f'dalga sayısı (boşluk>{gap} gün)', per, np.nan, n=len(ws), ni=int((ws['sum'] > 0).sum()))
            rec('2_kume', k, f'en iyi 3 dalga hariç gün ort (boşluk>{gap})', per, 1e4 * rest, note=f'en iyi 3 payı {ws["sum"].iloc[:3].sum() / tot:.0%}')
            rec('2_kume', k, f'dalga ortalamalarının medyanı (boşluk>{gap})', per, 1e4 * ws['mean'].median())
            # dalga düzeyinde t (her dalga bir gözlem)
            wm = ws['mean']
            rec('2_kume', k, f'dalga düzeyi ort (her dalga 1 gözlem; boşluk>{gap})', per, 1e4 * wm.mean(), t=wm.mean() / (wm.std() / np.sqrt(len(wm))), n=len(wm))
            print(f'       dalga düzeyi t = {wm.mean() / (wm.std() / np.sqrt(len(wm))):.2f}')
        (q5, q50, q95), p0, bo = boot(B3, d, per)
        print(f'  [2] {k} {per} blok önyükleme (10 gün): %90 aralık [{q5:+.0f}, {q95:+.0f}], medyan {q50:+.0f}, P(≤0) {p0:.3f}, P(<36 bps maliyet) {np.nanmean(bo < 0.0036):.2f}')
        rec('2_kume', k, 'blok önyükleme %5', per, q5)
        rec('2_kume', k, 'blok önyükleme %95', per, q95, note=f'P(<=0)={p0:.3f}; P(<36bps)={np.nanmean(bo < 0.0036):.2f}')
    for gap in (3, 10):
        lab = waves(SIG[k], gap)
        first = SIG[k] & (lab != lab.shift(1).where(SIG[k].shift(1, fill_value=False), -2)) & (lab.groupby(lab).cumcount() == 0)
        add('2_kume', k, f'yalnız dalganın ilk sinyal günü (boşluk>{gap}), 3 gün tut: per', B3, first, 3)
        add('2_kume', k, f'yalnız dalganın ilk sinyal günü (boşluk>{gap}): ham', B3, first, 3, demean=False)
        add('2_kume', k, f'dalganın sonraki günleri (boşluk>{gap}): per', B3, SIG[k] & ~first, 3)

# ---------------------------------------------------------------- 3. kimde
print('== 3. kimde')
f3, fl3, dl3 = fx(3)
M, _ = elib.excess_measures(P, 3, 'long', sc)   # havuz modunda hisse düzeyi per
adv = elib.adv60(P)[sc].where(fl3)
rk = adv.rank(axis=1, ascending=False, method='first')
nfl = fl3.sum(axis=1)
terc = {'likit üçte bir': rk.le(nfl / 3, axis=0), 'orta üçte bir': rk.gt(nfl / 3, axis=0) & rk.le(2 * nfl / 3, axis=0),
        'sığ üçte bir': rk.gt(2 * nfl / 3, axis=0), 'en likit 10': rk <= 10, 'en likit 5': rk <= 5, 'en likit 10 dışı': rk > 10}
cr = P['close_raw'][sc]
grp = dict(terc)
grp['ham fiyat ≥ 5 TL'] = cr >= 5
grp['ham fiyat < 5 TL'] = cr < 5
luf = (P['lim_up'][sc].shift(-1, fill_value=False) | P['lim_up'][sc].shift(-2, fill_value=False) | P['lim_up'][sc].shift(-3, fill_value=False))
ldf = (P['lim_dn'][sc].shift(-1, fill_value=False) | P['lim_dn'][sc].shift(-2, fill_value=False) | P['lim_dn'][sc].shift(-3, fill_value=False))
grp['t+1..t+3 tavan kapanışı OLMAYAN (geriye dönük tanı)'] = ~luf
grp['t+1..t+3 tavan ya da taban kapanışı OLMAYAN (tanı)'] = ~luf & ~ldf
nearlim = P['ret_cc'][sc] >= 0.089
grp['t günü tavana ≤%1 yakın kapananlar hariç'] = ~nearlim
notspec = pd.DataFrame(True, index=idx, columns=sc)
notspec[[c for c in ('BIGEN', 'LYDYE', 'MAGEN') if c in sc]] = False
grp['BIGEN, LYDYE, MAGEN çıkarılınca (çöküş serisi hisseleri)'] = notspec
grp['t günü ≥ +%7 kapananlar hariç'] = ~(P['ret_cc'][sc] >= 0.07)
for k in ('S1', 'S2'):
    d = SIG[k]
    for g, mask in grp.items():
        mn = 2 if 'likit 5' in g else 3
        sal = '4_dolum' if 'kapananlar hariç' in g else '3_kimde'
        add(sal, k, g, basket(3, mask, min_n=mn), d, 3, pers=('IS', 'HAVUZ', 'KASA'))
    # işlem düzeyi
    m = pm('HAVUZ')
    S = fl3[m] & d[m].values[:, None] & (nfl[m].values[:, None] >= 5)
    raw = f3[m].where(S)
    per = M['per'][m].where(S)
    ntr = int(S.values.sum())
    fu, fd = (S & luf[m]).values.sum(), (S & ldf[m]).values.sum()
    tot = np.nansum(per.values)
    print(f'  [3] {k} HAVUZ işlem: {ntr}; gün başına dolabilir hisse {S.sum(axis=1)[d[m]].mean():.1f}; tavanda kapandığı için dışarıda kalan/gün '
          f'{(P["tradable"][sc][m] & P["lim_up"][sc][m]).sum(axis=1)[d[m]].mean():.2f}; t günü tavana ≤%1 yakın işlem payı {(S & nearlim[m]).values.sum() / ntr:.1%}')
    print(f'      sonraki 3 günde tavan kapanışı gören işlem {fu / ntr:.1%}: ort ham {1e4 * np.nanmean(raw.where(luf[m]).values):+.0f}; '
          f'toplam per kazancındaki payı {np.nansum(per.where(luf[m]).values) / tot:.0%}; taban kapanışı gören {fd / ntr:.1%}: ort ham {1e4 * np.nanmean(raw.where(ldf[m]).values):+.0f}, '
          f'paylaşımı {np.nansum(per.where(ldf[m]).values) / tot:.0%}; işlem medyanı ham {1e4 * np.nanmedian(raw.values):+.0f}, isabet {np.nanmean(raw.values[np.isfinite(raw.values)] > 0):.2f}')
    rec('3_kimde', k, 'sonraki 3 günde tavan kapanışı gören işlemlerin toplam per kazancındaki payı (%)', 'HAVUZ', 100 * np.nansum(per.where(luf[m]).values) / tot, n=int(fu), note=f'işlemlerin {fu / ntr:.1%}')
    rec('3_kimde', k, 'işlem medyanı ham', 'HAVUZ', 1e4 * np.nanmedian(raw.values), n=ntr)
    bs = pd.DataFrame({'n': per.notna().sum(), 'per': 1e4 * per.mean(), 'top': per.sum()})
    bs = bs[bs.n >= 10].sort_values('top', ascending=False)
    print(f'      hisse bazında (≥10 işlem): {len(bs)} hisse, artı {int((bs.per > 0).sum())}; en çok katkı: '
          + ', '.join(f'{s} {v.per:+.0f} ({v.top / tot:.0%})' for s, v in bs.head(6).iterrows())
          + ' | en kötü: ' + ', '.join(f'{s} {v.per:+.0f}' for s, v in bs.tail(4).iterrows())
          + f' | VİOP üçlüsü: ' + ', '.join(f'{s} {bs.per.get(s, np.nan):+.0f}' for s in elib.VIOP))
    rec('3_kimde', k, 'hisse bazında artı olan hisse sayısı (≥10 işlem)', 'HAVUZ', np.nan, n=len(bs), ni=int((bs.per > 0).sum()))
    # çıkışta kilit
    dlS = (dl3[m] & S).values.sum()
    exit_ld = (P['lim_dn'][sc].shift(-3, fill_value=False)[m] & S).values.sum()
    fs = elib.fwd_simple(P['ret_cc'][sc], 3)[m].where(S)
    print(f'  [4] {k} çıkış günü tabanda kilitli işlem {exit_ld} ({exit_ld / ntr:.2%}); çıkışı kaydırılan {dlS}; kaydırmanın ort etkisi '
          f'{1e4 * (np.nanmean(raw.values) - np.nanmean(fs.values)):+.1f} bps/işlem; kilitli işlemlerde ort ham {1e4 * np.nanmean(raw.where(dl3[m]).values):+.0f}')
    rec('4_dolum', k, 'çıkış günü tabanda kilitli işlem payı (%)', 'HAVUZ', 100 * exit_ld / ntr, n=int(exit_ld))
H = pd.read_csv(HACIM).set_index('sym')
cap = H['kapanisin_%10u_tl']
advnow = H['gunluk_tl_medyan_20g']
print(f'  [3] kapanış seansı kapasitesi (10% kuralı, {len(cap)} hisse): min {cap.min():,.0f} TL, %25 {cap.quantile(.25):,.0f}, medyan {cap.median():,.0f}; '
      f'eşit ağırlıklı sepet tavanı = N×min = {len(cap) * cap.min():,.0f} TL; en sığ 5 hisse hariç N×min = {(len(cap) - 5) * cap.sort_values().iloc[5]:,.0f} TL; '
      f'sığ üçte birin medyan kapasitesi {cap.sort_values().iloc[:len(cap) // 3].median():,.0f} TL')
rec('3_kimde', 'S1,S2', 'eşit ağırlıklı sepet kapasitesi N×min (TL; kapanış seansının %10u)', 'A7 dönemi', len(cap) * cap.min(), n=len(cap))
rec('3_kimde', 'S1,S2', 'en sığ 5 hisse hariç sepet kapasitesi (TL)', 'A7 dönemi', (len(cap) - 5) * cap.sort_values().iloc[5], n=len(cap) - 5)

# ---------------------------------------------------------------- 4. giriş
print('== 4. giriş gecikmesi')
g1 = P['ret_co'][sc].shift(-1)
f3o = (1 + f3) / (1 + g1) - 1
for k in ('S1', 'S2'):
    d = SIG[k]
    add('4_dolum', k, 't+1 AÇILIŞINDAN giriş, t+3 kapanış çıkış (per)', basket(3, F=f3o), d, 3)
    add('4_dolum', k, 'gece payı: t kapanış → t+1 açılış (per)', basket(3, F=g1), d, 1)
    d1 = d.shift(1, fill_value=False)
    add('4_dolum', k, 't+1 KAPANIŞINDAN giriş, t+3 çıkış (2 gün; per)', B[2], d1, 2)
    add('4_dolum', k, 't+1 KAPANIŞINDAN giriş, t+4 çıkış (3 gün; per)', B[3], d1, 3)
    add('4_dolum', k, 't+1 kapanışından giriş, t+1 sinyal günü DEĞİLSE (3 gün; per)', B[3], d1 & ~d, 3)

# ---------------------------------------------------------------- 5. maliyet ve yıllık
print('== 5. maliyet ve yıllık')
# TL taşıma maliyeti: XU030 yakın vade vadelisinin bazından zımni yıllık basit faiz (temettü nedeniyle alt sınır)
vfx = P['viop_front'][P['viop_front']['und'] == 'XU030'].copy()
vfx['date'] = pd.to_datetime(vfx['date'])
vfx = vfx.set_index('date')
bas = (vfx['uzlasma'] * vfx['fiyat_carpani'] / L['XU030'].reindex(vfx.index) - 1) * 365.0 / vfx['vkg']
bas = bas[(vfx['vkg'] >= 20) & (vfx['vkg'] <= 70)]
RATE = {y: float(bas[bas.index.year == y].median()) for y in (2023, 2024, 2025, 2026)}
print('  [5] XU030 vadeli bazından zımni yıllık TL faizi (medyan; alt sınır):', {y: f'{v:.0%}' for y, v in RATE.items()},
      '→ 3 işlem günü taşıma ≈', {y: f'{1e4 * v * 3 / 250:.0f} bps' for y, v in RATE.items()})
for y, v in RATE.items():
    rec('5_tasima', 'S1,S2', 'XU030 vadeli bazından zımni yıllık TL faizi (%; medyan, alt sınır)', str(y), 100 * v, n=int((bas.index.year == y).sum()))
    rec('5_tasima', 'S1,S2', '3 işlem günlük taşıma maliyeti (bps)', str(y), 1e4 * v * 3 / 250)
for k in ('S1', 'S2'):
    d = SIG[k] & (nfl >= 5)
    m = pm('HAVUZ')
    Sf = (fl3 & d.values[:, None])
    Sf2 = Sf.copy()
    Sf2[~m] = False
    ct, cm = elib.cost_bps(P, Sf2, 'temel'), elib.cost_bps(P, Sf2, 'muhafazakar')
    x, dd = B3[m], d[m] & B3[m].notna()
    rawm = 1e4 * x[dd].mean()
    print(f'  [5] {k} HAVUZ maliyet temel {ct:.0f}, muhafazakâr {cm:.0f} bps; ham gün ort {rawm:+.0f} → net temel {rawm - ct:+.0f}, net muh. {rawm - cm:+.0f}; '
          f'dönemin sıradan 3 günü (ham) {1e4 * x.mean():+.0f}')
    rec('5_maliyet', k, 'gidiş-dönüş maliyet temel', 'HAVUZ', ct)
    rec('5_maliyet', k, 'gidiş-dönüş maliyet muhafazakâr', 'HAVUZ', cm)
    rec('5_maliyet', k, 'ham gün ort − temel maliyet', 'HAVUZ', rawm - ct)
    rec('5_maliyet', k, 'ham gün ort − muhafazakâr maliyet', 'HAVUZ', rawm - cm)
    # gerçekçi benzetim: sinyal günü kapanışta gir; son sinyalden 3 gün sonra kapanışta çık (örtüşen sinyaller pozisyonu uzatır)
    pos = (d.shift(1, fill_value=False) | d.shift(2, fill_value=False) | d.shift(3, fill_value=False))
    Fh = P['fill_long'][sc].astype(float).copy()
    Fh[~d.values] = np.nan
    held = Fh.ffill().shift(1) == 1
    rd = P['ret_cc'][sc].where(held).mean(axis=1).fillna(0.0).where(pos, 0.0)
    start = pos & ~pos.shift(1, fill_value=False)
    bh = ewd.fillna(0.0)
    lab3 = waves(d, 3)
    for y in (2023, 2024, 2025, 2026):
        my = idx.year == y
        ns = int(start[my].sum())
        gross = (1 + rd[my]).prod() - 1
        nt = (1 + gross) * (1 - ct / 1e4) ** ns - 1
        nm = (1 + gross) * (1 - cm / 1e4) ** ns - 1
        bhy = (1 + bh[my]).prod() - 1
        xu = (1 + r['XU100'][my].fillna(0)).prod() - 1
        inpos, outpos = rd[my][pos[my]], bh[my][~pos[my]]
        xy = B3[my]
        dy = d[my] & xy.notna()
        _, _, bpy, ty = st(B3 - B3[my].mean(), d, 3, (T0(f'{y}-01-01'), T0(f'{y}-12-31')))
        print(f'  [5] {k} {y}: sinyal günü {int(dy.sum())}, dalga {lab3[my][lab3[my] >= 0].nunique()}, pozisyon dönemi {ns}, piyasada gün {int(pos[my].sum())}/{int(my.sum())}; '
              f'per(yıl içi) {bpy:+.0f} (t {ty:.1f}), ham {1e4 * xy[dy].mean():+.0f}; strateji brüt {gross:+.1%}, net temel {nt:+.1%}, net muh. {nm:+.1%}; '
              f'sepeti hep tut {bhy:+.1%}; XU100 {xu:+.1%}; pozisyondaki gün ort {1e4 * inpos.mean():+.0f} bps/gün, dışarıdaki günlerde sepet {1e4 * outpos.mean():+.0f} bps/gün')
        for nm_, v in [('sinyal günü per (yıl içi kıyas)', bpy), ('sinyal günü ham', 1e4 * xy[dy].mean()), ('strateji yıllık brüt (%)', 100 * gross),
                       ('strateji yıllık net temel (%)', 100 * nt), ('strateji yıllık net muhafazakâr (%)', 100 * nm), ('sepeti hep tut (%)', 100 * bhy)]:
            rec('5_yillik', k, nm_, str(y), v, t=ty if 'per' in nm_ else np.nan, n=int(dy.sum()), ni=ns)
    mh = pm('HAVUZ')
    a_in, a_out = rd[mh][pos[mh]], bh[mh][~pos[mh]]
    se = np.sqrt(a_in.var() / len(a_in) + a_out.var() / len(a_out))
    print(f'  [5] {k} HAVUZ pozisyondaki günler {1e4 * a_in.mean():+.1f} bps/gün ({len(a_in)} gün) vs dışarıdaki günler {1e4 * a_out.mean():+.1f} bps/gün; fark t ≈ {(a_in.mean() - a_out.mean()) / se:.2f}; '
          f'en kötü tek pozisyon dönemi ve en kötü 3 günlük sepet getirisi: {1e4 * B3[mh][d[mh]].min():+.0f} bps; sinyal günlerinin %10 en kötüsü {1e4 * B3[mh][d[mh]].quantile(.1):+.0f}')
    rec('5_yillik', k, 'sinyal günü 3 günlük ham sepet getirisi: en kötü', 'HAVUZ', 1e4 * B3[mh][d[mh]].min())
    # pozisyon dönemi (dalga = tek gidiş-dönüş) düzeyinde kâr dağılımı
    sid = start.cumsum().where(pos)
    sp = (1 + rd[mh]).groupby(sid[mh]).prod() - 1
    ln = pos[mh].groupby(sid[mh]).sum()
    sps = sp.sort_values(ascending=False)
    print(f'  [5] {k} HAVUZ pozisyon dönemleri: {len(sp)}; ort süre {ln.mean():.1f} gün; ort ham {1e4 * sp.mean():+.0f}, medyan {1e4 * sp.median():+.0f}, kazanan {np.mean(sp > 0):.0%}, '
          f'temel maliyet sonrası kazanan {np.mean(sp > ct / 1e4):.0%}; en iyi 3 dönemin toplam içindeki payı {sps.iloc[:3].sum() / sp.sum():.0%}; en iyi 3 hariç ort {1e4 * sps.iloc[3:].mean():+.0f}; '
          f'en kötü dönem {1e4 * sp.min():+.0f}; en kötü 3: {[int(1e4 * v) for v in sps.iloc[-3:]]}')
    rec('5_yillik', k, 'pozisyon dönemi (tek gidiş-dönüş) ham getirisi: ortalama', 'HAVUZ', 1e4 * sp.mean(), n=len(sp))
    rec('5_yillik', k, 'pozisyon dönemi ham getirisi: medyan', 'HAVUZ', 1e4 * sp.median(), n=len(sp), note=f'kazanan {np.mean(sp > 0):.0%}; maliyet sonrası kazanan {np.mean(sp > ct / 1e4):.0%}')
    rec('5_yillik', k, 'pozisyon dönemi: en iyi 3 hariç ortalama ham', 'HAVUZ', 1e4 * sps.iloc[3:].mean(), n=len(sp) - 3, note=f'en iyi 3 payı {sps.iloc[:3].sum() / sp.sum():.0%}')
    rec('5_yillik', k, 'pozisyon dönemi: en kötü', 'HAVUZ', 1e4 * sp.min())
    # örtüşmeyen 3 günlük işlemler (sinyalde gir, 3 gün tut, çıkıştan önce yeni giriş yok)
    pp = np.where((d & B3.notna() & pd.Series(mh, index=idx)).values)[0]
    keep, last_ = [], -10 ** 9
    for i in pp:
        if i - last_ >= 3:
            keep.append(i); last_ = i
    v = B3.iloc[keep]
    print(f'  [5] {k} HAVUZ örtüşmeyen 3 günlük işlemler: {len(v)}; ham ort {1e4 * v.mean():+.0f} (t {v.mean() / (v.std() / np.sqrt(len(v))):.1f}), medyan {1e4 * v.median():+.0f}, kazanan {np.mean(v > 0):.0%}, '
          f'temel maliyet sonrası kazanan {np.mean(v > ct / 1e4):.0%}; yılda {len(v) / (mh.sum() / 250):.0f} işlem')
    rec('5_yillik', k, 'örtüşmeyen 3 günlük işlem: ham ortalama', 'HAVUZ', 1e4 * v.mean(), t=v.mean() / (v.std() / np.sqrt(len(v))), n=len(v))
    rec('5_yillik', k, 'örtüşmeyen 3 günlük işlem: ham medyan', 'HAVUZ', 1e4 * v.median(), n=len(v), note=f'maliyet sonrası kazanan {np.mean(v > ct / 1e4):.0%}')
    for y in (2023, 2024, 2025, 2026):
        my = idx.year == y
        ns = int(start[my].sum())
        nt = (1 + (1 + rd[my]).prod() - 1) * (1 - ct / 1e4) ** ns - 1
        ann = nt / max(int(pos[my].sum()), 1) * 250
        print(f'  [5] {k} {y}: bağlanan sermayenin yıllıklandırılmış net (temel) getirisi {ann:+.0%} (piyasada {int(pos[my].sum())} gün); TL faizinin altındaysa para piyasası fonu daha iyi')
        rec('5_yillik', k, 'piyasadaki günlere düşen net temel getiri, yıllıklandırılmış basit (%)', str(y), 100 * ann, n=int(pos[my].sum()))
        carry = RATE[y] * int(pos[my].sum()) / 250
        tot_x = tot_x + (nt - carry) if y > 2023 else (nt - carry)
        print(f'        {y}: zımni faiz {RATE[y]:.0%} → pozisyon günlerinin faiz karşılığı {carry:.1%}; nakde (para piyasası) göre fazla = net temel {nt:+.1%} − {carry:.1%} = {nt - carry:+.1%}')
        rec('5_yillik', k, 'nakde göre fazla: strateji net temel − pozisyon günlerinin zımni faizi (% puan)', str(y), 100 * (nt - carry), n=int(pos[my].sum()))
    print(f'        {k} dört yılın nakde göre fazla toplamı {tot_x:+.1%}')
    rec('5_yillik', k, 'nakde göre fazla: dört yıl toplamı (% puan)', '2023-2026', 100 * tot_x)
    x3 = B3[mh][d[mh]]
    c3 = pd.Series(x3.index.year, index=x3.index).map(RATE) * 3 / 250
    print(f'        {k} HAVUZ sinyal günü ham − temel maliyet − 3 günlük zımni faiz = {1e4 * (x3 - c3).mean() - ct:+.0f} bps; muhafazakâr maliyetle {1e4 * (x3 - c3).mean() - cm:+.0f}; KASA: {1e4 * (x3 - c3)[x3.index >= elib.KASA_START].mean() - ct:+.0f}')
    rec('5_maliyet', k, 'ham − temel maliyet − 3 günlük zımni TL faizi', 'HAVUZ', 1e4 * (x3 - c3).mean() - ct)
    rec('5_maliyet', k, 'ham − muhafazakâr maliyet − 3 günlük zımni TL faizi', 'HAVUZ', 1e4 * (x3 - c3).mean() - cm)
    rec('5_maliyet', k, 'ham − temel maliyet − 3 günlük zımni TL faizi', 'KASA', 1e4 * (x3 - c3)[x3.index >= elib.KASA_START].mean() - ct)
    rec('5_yillik', k, 'sinyal günü 3 günlük ham sepet getirisi: %10 dilim', 'HAVUZ', 1e4 * B3[mh][d[mh]].quantile(.1))

# ---------------------------------------------------------------- 6. karar anı (17:50)
print('== 6. karar anı')
m5 = pd.read_parquet(os.path.join(PANEL, 'm5_isy', 'XELKT.parquet'))
m5['d'] = pd.to_datetime(m5['ts_tr']).dt.normalize()
m5['hm'] = pd.to_datetime(m5['ts_tr']).dt.strftime('%H:%M')
g = m5.groupby('d')
last, lasthm = g['c'].last(), g['hm'].last()
print('  son bar damgası dağılımı:', lasthm.value_counts().head(6).to_dict())
std60 = r['XELKT'].rolling(60, min_periods=40).std().shift(1)
prevmax = L['XELKT'].shift(1).rolling(19, min_periods=19).max()
for lab, cut in (('17:50', '17:45'), ('17:30', '17:25'), ('17:00', '16:55')):
    v = m5[m5.hm <= cut].groupby('d')['c'].last()
    ok = (lasthm >= '17:55')
    ratio = (v / last).where(ok).reindex(idx)
    Lp = L['XELKT'] * ratio
    rp = (1 + r['XELKT']) * ratio - 1
    PS = {'S1': (Lp >= prevmax) & ratio.notna(), 'S2': (rp / std60 >= 1) & ratio.notna()}
    for k in ('S1', 'S2'):
        for per in ((T0('2017-01-01'), elib.IS_END), 'HAVUZ'):
            m = pm(per) & ratio.notna().values
            c, p = SIG[k][m], PS[k][m]
            capt = (c & p).sum() / max(c.sum(), 1)
            fals = (p & ~c).sum() / max(p.sum(), 1)
            pn = per if isinstance(per, str) else '2017-22'
            x = B3 - B3[pm(per)].mean()
            res = []
            for nm_, dd in (('vekil sinyaliyle giren', PS[k]), ('yakalanan', PS[k] & SIG[k]), ('kaçan', SIG[k] & ~PS[k]), ('yanlış', PS[k] & ~SIG[k]), ('kapanış sinyali (aynı günler)', SIG[k])):
                dd2 = dd & ratio.notna()
                n, ni, bps, t = st(x, dd2, 3, per)
                res.append(f'{nm_} {bps:+.0f} (t {t:.1f}; {n})')
                rec('6_karar', k, f'{lab} vekili: {nm_} (per)', pn, bps, t, n, ni)
            rec('6_karar', k, f'{lab} vekili: yakalama (%)', pn, 100 * capt, n=int(c.sum()))
            rec('6_karar', k, f'{lab} vekili: yanlış sinyal (%)', pn, 100 * fals, n=int(p.sum()))
            print(f'  [6] {k} {lab} {pn}: yakalama {capt:.0%}, yanlış {fals:.0%} | ' + ' | '.join(res))

# ---------------------------------------------------------------- 7. parametre
print('== 7. parametre')
for w in (10, 15, 20, 30, 40, 60):
    out = []
    for h in (1, 2, 3, 5):
        d = hi(L['XELKT'], w)
        add('7_param', 'S1', f'zirve penceresi {w}, h={h}', B[h], d, h, pers=('IS', 'OOS1', 'KASA', 'HAVUZ'), show=False)
        a = [q for q in ROWS[-4:]]
        out.append(f'h{h}: ' + ' / '.join(f'{q["bps"]:+.0f}({q["t"]:.1f})' for q in a))
    print(f'  [7] S1 pencere {w} [IS/OOS1/KASA/HAVUZ] ' + ' | '.join(out))
for th in (0.5, 0.75, 1.0, 1.25, 1.5, 2.0):
    out = []
    for h in (1, 2, 3, 5):
        d = (zE >= th).fillna(False)
        add('7_param', 'S2', f'z eşiği {th}, h={h}', B[h], d, h, pers=('IS', 'OOS1', 'KASA', 'HAVUZ'), show=False)
        a = [q for q in ROWS[-4:]]
        out.append(f'h{h}: ' + ' / '.join(f'{q["bps"]:+.0f}({q["t"]:.1f})' for q in a))
    print(f'  [7] S2 eşik {th} [IS/OOS1/KASA/HAVUZ] ' + ' | '.join(out))
# 3 günün dağılımı: 1., 2., 3. gün ayrı
for k in ('S1', 'S2'):
    for j in (1, 2, 3):
        dj = SIG[k].shift(j - 1, fill_value=False)
        add('7_param', k, f'tutmanın {j}. günü tek başına (per, 1 günlük)', B[1], dj, 1, pers=('IS', 'HAVUZ', 'KASA'))

# ---------------------------------------------------------------- 8. aşağı yön
print('== 8. aşağı yön')
for nm_, d in (('XELKT 20g dip', lo(L['XELKT'], 20)), ('XELKT z≤−1', (zE <= -1).fillna(False)), ('XELKT z≤−1,5', (zE <= -1.5).fillna(False)),
               ('XELKT 20g dip & XU100 dip değil', lo(L['XELKT'], 20) & ~lo(L['XU100'], 20))):
    for h in (1, 3):
        add('8_asagi', 'kaçınma', f'{nm_} → sepet AL h={h} (per)', B[h], d, h)

df = pd.DataFrame(ROWS)
for c in ('bps', 't'):
    df[c] = df[c].astype(float).round(2)
df.to_csv(OUT, index=False)
print('satır:', len(df), '→', OUT)
