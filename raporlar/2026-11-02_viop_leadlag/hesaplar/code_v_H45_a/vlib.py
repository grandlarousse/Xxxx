"""v_H45_a — BAĞIMSIZ doğrulama kütüphanesi (ll.py import EDİLMEZ; hizalama/temizlik burada sıfırdan yazıldı).

Zamanlama (UTC):
- BIST açılış müzayedesi ~06:55-07:00 UTC (Yahoo günlük 'o' = m5 06:55 barı = müzayede fiyatı; 01_audit.py ile doğrulandı).
  Sürekli işlem 07:00 UTC'de başlar; kapanış seansı 15:00-15:10 UTC (Yahoo 'c').
- TUR (ABD ETF) kapanışı 20:00/21:00 UTC. BIST günü t için 'TUR_{t-1}' = BIST t açılışından ÖNCEKİ son ABD kapanışı
  ile BIST t_prev açılışından önceki son ABD kapanışı arası log getiri (ABD tarihi < t ve < t_prev).
- Yahoo '=X' FX günlük barı: 2011+ için ldate D 'c' ≈ 00:00 UTC D fiyatı (h1 ve FXE/TUR korelasyonuyla doğrulandı);
  2005-2010'da ldate D 'c' ≈ D günü SONU. (Bu yüzden FX'i yalnızca 2011+ kullanıyoruz.)
  BIST t için USDTRY_{t-1} = ln(P00(t)/P00(t_prev)), P00(D) = ldate<=D olan son barın 'c'si (=00:00 UTC D) -> açılıştan önce bilinir.
"""
import os, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
SCR = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad'
DATA = SCR + '/data'
CODE = SCR + '/out/code_v_H45_a'
IS0, SPLIT = pd.Timestamp('2014-01-01'), pd.Timestamp('2021-01-01')
LUP, LDN = np.log(1.105), np.log(0.895)
_c = {}


def raw(sym, kind='daily'):
    k = (sym, kind)
    if k not in _c:
        p = f'{DATA}/{kind}/{sym}.parquet'
        d = pd.read_parquet(p)
        if kind == 'daily':
            d.index = pd.DatetimeIndex(d['ldate'].values)
            d = d[~d.index.duplicated(keep='last')].sort_index()
        _c[k] = d
    return _c[k]


def bist_cal():
    if 'cal' not in _c:
        d = raw('XU100.IS')
        _c['cal'] = d.index[d['v'].fillna(0) > 0]
    return _c['cal']


def decomp(code, strict=False):
    """BIST hissesi/endeksi: cc (adj), gap, intra (=ln c/o), bayraklar. Index = BIST takvimi.
    Temizlik: fiyat bazında cc ∉ [ln .895, ln 1.105] -> tüm satır NaN; gap aynı aralık dışı -> gap/intra NaN.
    Şüpheli açılış: (o==önceki c & h==l) her zaman NaN; strict=True ise ayrıca o==c (aynı gün) ve o==önceki c günleri NaN.
    Önceki satır takvimde bir önceki gün değilse (askı/eksik veri) gap/intra NaN."""
    sym = code if code.endswith('.IS') else code + '.IS'
    d = raw(sym).copy()
    isidx = d['v'].fillna(0).gt(0).mean() < 0.5 or code.startswith('X')
    if not isidx:
        d = d[d['v'].fillna(0) > 0]
    cal = bist_cal()
    d = d[d.index.isin(cal)]
    pos = cal.get_indexer(d.index)
    contiguous = pd.Series(np.r_[False, np.diff(pos) == 1], index=d.index)
    pc = d['c'].shift(1)
    cc = np.log(d['adj'] / d['adj'].shift(1))
    intra = np.log(d['c'] / d['o'])
    gap = cc - intra
    f_ll = (d['h'] == d['l']) & np.isclose(d['o'], pc, rtol=1e-6)
    f_oc = np.isclose(d['o'], d['c'], rtol=1e-6)
    f_opc = np.isclose(d['o'], pc, rtol=1e-6)
    bad_open = f_ll | (d['o'] <= 0) | d['o'].isna()
    if strict:
        bad_open = bad_open | f_oc | f_opc
    out = pd.DataFrame({'cc': cc, 'gap': gap, 'intra': intra, 'o': d['o'], 'c': d['c'], 'v': d['v'],
                        'f_oc': f_oc, 'f_opc': f_opc})
    badcc = (cc > LUP) | (cc < LDN)
    out.loc[badcc, ['cc', 'gap', 'intra']] = np.nan
    out.loc[bad_open | ~contiguous, ['gap', 'intra']] = np.nan
    out.loc[(gap > LUP) | (gap < LDN), ['gap', 'intra']] = np.nan
    out.loc[~contiguous, 'cc'] = np.nan
    out.loc[out.index < IS0, ['gap', 'intra']] = np.nan
    return out.reindex(cal)


def us_prev(sym, field='adj'):
    """ABD kapanışlı sembol: BIST günü t için sinyal = ln(P(son ABD tarihi < t) / P(son ABD tarihi < t_prev)).
    Ayrıca TUR_{t} (aynı gün; BIST kapanışından SONRA biter) = ln(P(<=t)/P(<=t_prev))."""
    d = raw(sym)
    p = d[field].astype(float); p = p[p > 0].dropna()
    cal = bist_cal()
    i_lt = p.index.searchsorted(cal, side='left') - 1  # son tarih < t
    P_lt = pd.Series(np.where(i_lt >= 0, p.values[np.clip(i_lt, 0, None)], np.nan), index=cal)
    D_lt = pd.Series(np.where(i_lt >= 0, p.index.values[np.clip(i_lt, 0, None)], np.datetime64('NaT')), index=cal)
    i_le = p.index.searchsorted(cal, side='right') - 1
    P_le = pd.Series(np.where(i_le >= 0, p.values[np.clip(i_le, 0, None)], np.nan), index=cal)
    prev = np.log(P_lt / P_lt.shift(1))
    # bayat: son ABD kapanışı t'den 6 günden eski ise NaN
    prev[(cal - pd.DatetimeIndex(D_lt.values)) > pd.Timedelta(days=6)] = np.nan
    same = np.log(P_le / P_le.shift(1))
    r = prev.copy()
    sd = r.rolling(250, min_periods=60).std().shift(1)
    prev[(r.abs() > 12 * sd) & sd.notna()] = np.nan
    return prev, same


def fx_prev(sym='TRY=X'):
    """Yahoo FX: ldate D 'c' = 00:00 UTC D (2011+). BIST t: ln(P00(t)/P00(t_prev)) = açılıştan önce bilinen son gün hareketi."""
    d = raw(sym)
    p = d['c'].astype(float); p = p[p > 0].dropna()
    cal = bist_cal()
    i = p.index.searchsorted(cal, side='right') - 1  # ldate <= t  -> 00:00 UTC t fiyatı
    P = pd.Series(np.where(i >= 0, p.values[np.clip(i, 0, None)], np.nan), index=cal)
    r = np.log(P / P.shift(1))
    r[cal < pd.Timestamp('2011-01-01')] = np.nan  # zaman konvansiyonu 2010'da değişti
    return r


# ---------------- istatistik ----------------
def ols(y, X, lags=5, names=None):
    """OLS + Newey-West. y Series, X DataFrame/list of Series. Dönüş: (params, tvalues, n, r2) Series'ler."""
    import statsmodels.api as sm
    if isinstance(X, (list, tuple)):
        X = pd.concat([x.rename(names[i] if names else f'x{i}') for i, x in enumerate(X)], axis=1)
    df = pd.concat([y.rename('_y'), X], axis=1).dropna()
    if len(df) < 40:
        return None
    m = sm.OLS(df['_y'].values, sm.add_constant(df.drop(columns='_y').values, has_constant='add')).fit(
        cov_type='HAC', cov_kwds={'maxlags': lags})
    cols = ['const'] + list(df.drop(columns='_y').columns)
    return {'b': pd.Series(m.params, index=cols), 't': pd.Series(m.tvalues, index=cols), 'n': len(df), 'r2': m.rsquared}


def corr_t(y, x, start=None, end=None, lags=5):
    df = pd.concat([y.rename('y'), x.rename('x')], axis=1).dropna()
    if start is not None: df = df[df.index >= pd.Timestamp(start)]
    if end is not None: df = df[df.index < pd.Timestamp(end)]
    if len(df) < 40: return np.nan, np.nan, len(df)
    z = (df - df.mean()) / df.std()
    r = ols(z['y'], [z['x']], lags)
    return float(df['y'].corr(df['x'])), float(r['t'].iloc[1]), len(df)


def by_year(y, x, minn=60):
    df = pd.concat([y.rename('y'), x.rename('x')], axis=1).dropna()
    return df.groupby(df.index.year).apply(lambda g: g['y'].corr(g['x']) if len(g) >= minn else np.nan)


def zpos(sig, thr, win=250, minp=60):
    s = sig.dropna()
    mu = s.rolling(win, min_periods=minp).mean().shift(1)
    sd = s.rolling(win, min_periods=minp).std().shift(1)
    z = (s - mu) / sd
    pos = np.sign(z).where(z.abs() > thr, 0.0).fillna(0.0)
    return pos.reindex(sig.index).fillna(0.0)


def bt(pos, tgt, cost_bps):
    """pos_t (karar anından önce bilinen) * tgt_t - maliyet. Dönüş: dict IS/OOS/ALL + by_year."""
    df = pd.concat([pos.rename('p'), tgt.rename('y')], axis=1).dropna()
    df = df[df.index >= IS0]
    pnl = df['p'] * df['y'] - cost_bps / 1e4 * df['p'].abs()
    act = df['p'] != 0
    out = {}
    for lab, m in [('IS', df.index < SPLIT), ('OOS', df.index >= SPLIT), ('ALL', np.ones(len(df), bool))]:
        a = act & m; pa = pnl[a]
        if a.sum() < 20:
            out[lab] = {'n': int(a.sum())}; continue
        import statsmodels.api as sm
        mm = sm.OLS(pa.values, np.ones(len(pa))).fit(cov_type='HAC', cov_kwds={'maxlags': 5})
        p_all = pnl[m]
        sh = p_all.mean() / p_all.std() * np.sqrt(252) if p_all.std() > 0 else np.nan
        out[lab] = {'n': int(a.sum()), 'mean_bps': 1e4 * pa.mean(), 't': float(mm.tvalues[0]), 'hit': float((pa > 0).mean()),
                    'sharpe': sh, 'tot_pct': 100 * pa.sum()}
    out['by_year'] = (1e4 * pnl[act].groupby(pnl[act].index.year).mean()).round(1).to_dict()
    out['n_by_year'] = pnl[act].groupby(pnl[act].index.year).size().to_dict()
    return out, pnl


def fmt_bt(o, keys=('IS', 'OOS', 'ALL')):
    s = []
    for k in keys:
        r = o.get(k, {})
        if 'mean_bps' in r:
            s.append(f"{k}: n={r['n']} {r['mean_bps']:+.1f}bps t={r['t']:.2f} hit={r['hit']:.2f} SR={r['sharpe']:.2f}")
        else:
            s.append(f"{k}: n={r.get('n', 0)}")
    return ' | '.join(s)
