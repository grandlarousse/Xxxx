"""v_H45_b — 2. aşama ÇÜRÜTME doğrulayıcısının bağımsız kütüphanesi.
ll.py ve 1. aşamanın vlib.py'si IMPORT EDİLMEZ; hizalama/temizlik burada ayrıca yazıldı.

Zamanlama (UTC) varsayımları:
- BIST: açılış müzayedesi ~06:55 (Yahoo günlük 'o' = müzayede fiyatı), sürekli işlem 07:00-15:00, kapanış seansı 15:00-15:10 ('c').
- ABD ETF (TUR, EWZ...): kapanış 20:00/21:00 UTC. BIST günü t için X_{t-1} = ln(P[son ABD tarihi < t] / P[son ABD tarihi < t_prev]).
  Aynı tarihli ABD kapanışı (tarih == t) BIST t kapanışından sonra olduğu için kullanılmaz.
- Yahoo '=X' günlük: 2011+ ldate D 'c' ~ 00:00 UTC D (1. aşama ve koordinatör doğruladı; ben ayrıca 00_audit'te h1 ile kontrol ettim).
  BIST t için FX_{t-1} = ln(P00(t)/P00(t_prev)), P00(D) = ldate == D satırı (yoksa ldate<=D son satır). 2011 öncesi atılır.
  FX_t (aynı gün, seans t'yi kapsar; işlenemez, yalnızca ayrıştırma için) = ln(P00(t_next)/P00(t)).
- Temizlik (BIST): fiyat-marjı rejimine göre: 2020-03-13 öncesi cc ∉ [ln .795, ln 1.205], sonrası cc ∉ [ln .895, ln 1.105] -> NaN.
  Ek 'LEGACY' modu: tüm dönem ±%10,5 (iddia/1. aşama ile karşılaştırma için).
  gap = ln(adj_t/adj_{t-1}) - ln(c_t/o_t) ; aynı sınırlar gap için de. Açılış şüpheli (o==c_prev ve h==l) -> gap/intra NaN.
  2014 öncesi gap/intra kullanılmaz.
"""
import numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
SCR = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad'
DATA = SCR + '/data'
OUT = SCR + '/out/code_v_H45_b'
T0, SPLIT = pd.Timestamp('2014-01-01'), pd.Timestamp('2021-01-01')
SWITCH = pd.Timestamp('2020-03-13')
_C = {}


def load(sym, kind='daily'):
    k = (sym, kind)
    if k not in _C:
        d = pd.read_parquet(f'{DATA}/{kind}/{sym}.parquet')
        if kind == 'daily':
            d.index = pd.DatetimeIndex(d['ldate'].values)
            d = d[~d.index.duplicated(keep='last')].sort_index()
        _C[k] = d
    return _C[k]


def cal():
    if 'cal' not in _C:
        d = load('XU100.IS')
        d = d[(d['c'] > 0)]
        _C['cal'] = d.index[d.index >= pd.Timestamp('2005-01-01')]
    return _C['cal']


def _lims(idx, legacy=False):
    if legacy:
        return pd.Series(np.log(1.105), idx), pd.Series(np.log(0.895), idx)
    pre = idx < SWITCH
    up = pd.Series(np.where(pre, np.log(1.205), np.log(1.105)), idx)
    dn = pd.Series(np.where(pre, np.log(0.795), np.log(0.895)), idx)
    return up, dn


def bist(code, legacy=False, strict=False):
    """DataFrame (BIST takvimi): cc, gap, intra, o, c, adj, h, l, v."""
    sym = code if code.endswith('.IS') else code + '.IS'
    key = ('bist', sym, legacy, strict)
    if key in _C:
        return _C[key]
    d = load(sym).copy()
    C = cal()
    is_idx = code.startswith('X') and len(code) <= 6 and d['v'].fillna(0).eq(0).mean() > 0.3
    if not is_idx:
        d = d[~((d['v'].fillna(0) <= 0) & (d['h'] == d['l']))]  # bayat gün
    d = d[d.index.isin(C)]
    pos = C.get_indexer(d.index)
    contig = pd.Series(np.r_[False, np.diff(pos) == 1], d.index)
    cpv = d['c'].shift(1)
    cc = np.log(d['adj'] / d['adj'].shift(1))
    intra = np.log(d['c'] / d['o'])
    gap = cc - intra
    up, dn = _lims(d.index, legacy)
    bad = (cc > up) | (cc < dn)
    badg = (gap > up) | (gap < dn) | (intra > up) | (intra < dn)
    badopen = ((d['h'] == d['l']) & np.isclose(d['o'], cpv)) | (d['o'] <= 0)
    if strict:
        badopen = badopen | np.isclose(d['o'], d['c']) | np.isclose(d['o'], cpv)
    out = pd.DataFrame({'cc': cc, 'gap': gap, 'intra': intra, 'o': d['o'], 'c': d['c'], 'adj': d['adj'],
                        'h': d['h'], 'l': d['l'], 'v': d['v']})
    out.loc[bad | ~contig, ['cc', 'gap', 'intra']] = np.nan
    out.loc[badg | badopen, ['gap', 'intra']] = np.nan
    out.loc[out.index < T0, ['gap', 'intra']] = np.nan
    out = out.reindex(C)
    _C[key] = out
    return out


def us_lag(sym, field='adj', clip_sd=None):
    """ABD kapanışlı seri: (X_{t-1}, X_t_same) BIST takviminde. Ayrıca US-seans içi (o->c) ve gece (c_prev->o) parçaları."""
    d = load(sym)
    p = d[field].astype(float).where(lambda x: x > 0).dropna()
    C = cal()
    il = p.index.searchsorted(C, side='left') - 1
    ok = il >= 0
    P = pd.Series(np.where(ok, p.values[np.clip(il, 0, None)], np.nan), C)
    D = pd.Series(np.where(ok, p.index.values[np.clip(il, 0, None)], np.datetime64('NaT')), C)
    r = np.log(P / P.shift(1))
    stale = (C - pd.DatetimeIndex(D.values)) > pd.Timedelta(days=6)
    r[stale] = np.nan
    # parçalar: yalnızca tek ABD günü kapsanıyorsa (ardışık)
    o = d['o'].astype(float).reindex(p.index)
    cpr = d['c'].astype(float).reindex(p.index)
    usintra = np.log(cpr / o)  # ABD seansı (13:30/14:30 -> 20/21 UTC)
    usnight = np.log(p / p.shift(1)) - usintra  # önceki ABD kapanışı -> ABD açılışı (BIST seansını içerir)
    UI = pd.Series(np.where(ok, usintra.values[np.clip(il, 0, None)], np.nan), C)
    UN = pd.Series(np.where(ok, usnight.values[np.clip(il, 0, None)], np.nan), C)
    # kaç ABD günü kapsandı?
    cnt = pd.Series(il, C).diff()
    UI[cnt != 1] = np.nan; UN[cnt != 1] = np.nan
    if clip_sd is not None:
        sd = r.rolling(250, min_periods=60).std().shift(1)
        r[(r.abs() > clip_sd * sd) & sd.notna()] = np.nan
    return r, UI, UN


def fx_lag(sym='TRY=X'):
    """FX_{t-1} = ln(P00(t)/P00(t_prev)) ; FX_t (seans t dahil, işlenemez) = ln(P00(t_next)/P00(t))."""
    d = load(sym)
    p = d['c'].astype(float).where(lambda x: x > 0).dropna()
    C = cal()
    i = p.index.searchsorted(C, side='right') - 1
    P = pd.Series(np.where(i >= 0, p.values[np.clip(i, 0, None)], np.nan), C)
    r_prev = np.log(P / P.shift(1))
    r_same = np.log(P.shift(-1) / P)
    m = C < pd.Timestamp('2011-01-01')
    r_prev[m] = np.nan; r_same[m] = np.nan
    return r_prev, r_same


# ---------------- istatistik (bağımsız NW) ----------------
def nw_ols(y, X, L=5):
    """y: (n,), X: (n,k) sabit dahil değil. Dönüş b, t (sabit ilk)."""
    X = np.column_stack([np.ones(len(y)), X])
    n, k = X.shape
    XtXi = np.linalg.pinv(X.T @ X)
    b = XtXi @ X.T @ y
    e = y - X @ b
    u = X * e[:, None]
    S = u.T @ u
    for l in range(1, L + 1):
        w = 1 - l / (L + 1)
        G = u[l:].T @ u[:-l]
        S += w * (G + G.T)
    V = XtXi @ S @ XtXi
    se = np.sqrt(np.maximum(np.diag(V), 1e-300))
    return b, b / se, n


def reg(y, Xd, start=None, end=None, L=5):
    """y Series, Xd dict ad->Series. Dönüş dict: b, t (ad), n."""
    df = pd.concat([y.rename('_y')] + [v.rename(k) for k, v in Xd.items()], axis=1).dropna()
    if start is not None: df = df[df.index >= pd.Timestamp(start)]
    if end is not None: df = df[df.index < pd.Timestamp(end)]
    if len(df) < 40:
        return None
    b, t, n = nw_ols(df['_y'].values, df[list(Xd)].values, L)
    return {'b': dict(zip(['c'] + list(Xd), b)), 't': dict(zip(['c'] + list(Xd), t)), 'n': n}


def ct(y, x, start=None, end=None, L=5):
    """korelasyon + NW t (standartlaştırılmış regresyon)."""
    df = pd.concat([y.rename('y'), x.rename('x')], axis=1).dropna()
    if start is not None: df = df[df.index >= pd.Timestamp(start)]
    if end is not None: df = df[df.index < pd.Timestamp(end)]
    if len(df) < 40: return (np.nan, np.nan, len(df))
    z = (df - df.mean()) / df.std()
    b, t, n = nw_ols(z['y'].values, z[['x']].values, L)
    return (float(df['y'].corr(df['x'])), float(t[1]), n)


def ct3(y, x):
    a = ct(y, x, T0); i = ct(y, x, T0, SPLIT); o = ct(y, x, SPLIT)
    return f"corr {a[0]:+.3f} t {a[1]:+.2f} n {a[2]} | IS {i[0]:+.3f} t {i[1]:+.2f} | OOS {o[0]:+.3f} t {o[1]:+.2f}"


def yearly(y, x, minn=50):
    df = pd.concat([y.rename('y'), x.rename('x')], axis=1).dropna()
    return df.groupby(df.index.year).apply(lambda g: g['y'].corr(g['x']) if len(g) >= minn else np.nan)


def zsig(s, win=250, minp=60):
    x = s.dropna()
    mu = x.rolling(win, min_periods=minp).mean().shift(1)
    sd = x.rolling(win, min_periods=minp).std().shift(1)
    return ((x - mu) / sd).reindex(s.index)


def bt(pos, tgt, cost_bps, start=T0):
    df = pd.concat([pos.rename('p'), tgt.rename('y')], axis=1).dropna()
    df = df[(df.index >= start) & (df['p'] != 0)]
    pnl = df['p'] * df['y'] - cost_bps / 1e4 * df['p'].abs()
    res = {}
    for lab, m in [('IS', pnl.index < SPLIT), ('OOS', pnl.index >= SPLIT), ('ALL', np.ones(len(pnl), bool))]:
        x = pnl[m]
        if len(x) < 15:
            res[lab] = (len(x), np.nan, np.nan); continue
        b, t, n = nw_ols(x.values, np.zeros((len(x), 0)), 5)
        res[lab] = (len(x), 1e4 * x.mean(), float(t[0]))
    res['yr'] = (1e4 * pnl.groupby(pnl.index.year).mean()).round(1).to_dict()
    return res, pnl


def fbt(r):
    return ' | '.join(f"{k} n {r[k][0]} {r[k][1]:+.1f}bps t {r[k][2]:+.2f}" for k in ('IS', 'OOS', 'ALL'))


# ---------------- VİOP bülteni ----------------
def viop_panel(underlyings=('KCHOL', 'ENKAI'), refresh=False):
    """Her gün ve dayanak için en yüksek hacimli pay vadelisi (F_<KOD>MMYY) satırı."""
    import glob, os
    fn = f'{OUT}/viop_ssf.parquet'
    if os.path.exists(fn) and not refresh:
        return pd.read_parquet(fn)
    rows = []
    pref = tuple('F_' + u for u in underlyings)
    for f in sorted(glob.glob(f'{DATA}/viop/viop_*.csv')):
        with open(f, encoding='windows-1254', errors='replace') as fh:
            lines = fh.read().splitlines()
        hdr = [h.strip() for h in lines[0].split(';')]
        for ln in lines[2:]:
            if not ln.startswith('20'):
                continue
            parts = ln.split(';')
            if len(parts) < 22:
                continue
            code = parts[1]
            if not code.startswith(pref):
                continue
            rows.append(dict(zip(hdr, parts)))
    df = pd.DataFrame(rows)
    num = ['UZLASMA FIYATI', 'ONCEKI UZLASMA FIYATI', 'ACILIS FIYATI', 'EN DUSUK FIYAT', 'EN YUKSEK FIYAT', 'KAPANIS FIYATI',
           'AGIRLIKLI ORTALAMA FIYAT', 'ISLEM HACMI', 'ISLEM MIKTARI', 'ISLEM SAYISI', 'ACIK POZISYON']
    for c in num:
        if c in df:
            df[c] = pd.to_numeric(df[c].str.replace(',', '.'), errors='coerce')
    df['date'] = pd.to_datetime(df['TARIH'])
    df['und'] = df['SOZLESME KODU'].str.slice(2, 7)
    df['exp'] = pd.to_datetime(df['VADE TARIHI'], errors='coerce')
    df.columns = [c.strip() for c in df.columns]
    df.to_parquet(fn)
    return df
