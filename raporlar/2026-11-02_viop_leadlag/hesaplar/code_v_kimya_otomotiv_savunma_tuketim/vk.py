"""v_kimya_otomotiv_savunma_tuketim — BAĞIMSIZ doğrulama yardımcıları (ll.py import EDİLMEZ; ham parquet'ten).
Konvansiyon (kendi uygulamam):
 - Her sembol ham parquet'ten okunur, indeks = 'ldate' (yerel işlem tarihi), tekrarlar son kayıtla.
 - BIST hissesi (.IS, endeks değil): v<=0 günleri atılır (işlem yok). Getiri kendi işlem günleri arasında, sonra BIST takvimine
   reindex (eksik gün = NaN, ffill YOK). Temizlik: fiyat oranı >1,105 veya <0,895 olan günler NaN (adj bazında).
 - BIST endeksi (X...): v filtresi yok, aynı ±%10,5 temizliği.
 - BIST dışı sürücü: BIST takvimine 'yerel tarih <= t son kapanış' ile ffill; tatil sıfırları NaN; 8σ (geçmiş 250g) sıçramalar NaN (roll).
 - Yahoo '=X' FX: günlük c(t) = 00:00 UTC t fiyatı (fx_timing_check.py ile doğrulandı) -> değer bir önceki satırın tarihine kaydırılır
   (fixed r(t) = UTC günü t). fx_raw=True ile ham (kaydırılmamış) seri alınabilir.
 - Ayrıştırma: cc = ln(adj_t/adj_{t-1}), intra = ln(c/o), gap = cc - intra; 2014 öncesi gap/intra NaN; şüpheli açılış (o<=0 veya
   h==l & o==önceki c) NaN; gap oranı ±%10,5 dışı NaN.
"""
import os, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
D = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data'
OUT = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_kimya_otomotiv_savunma_tuketim'
UP, DN = np.log(1.105), np.log(0.895)
IS_ = ('2014-01-01', '2020-12-31'); OOS_ = ('2021-01-01', '2026-12-31'); FULL0 = '2010-01-01'

def ysym(s):
    if s.endswith('.IS') or '.' in s or '=' in s or s.startswith('^') or '-' in s: return s
    return s + '.IS' if os.path.exists(f'{D}/daily/{s}.IS.parquet') else s

def is_bist(s): return ysym(s).endswith('.IS')
def is_bist_index(s):
    s = ysym(s); return s.endswith('.IS') and s.startswith('X') and s[:-3] in BIST_IDX
BIST_IDX = set('XU030 XU050 XU100 XUTUM XYUZO XBANK XLBNK X10XB XHOLD XUSIN XUMAL XUHIZ XUTEK XULAS XELKT XGIDA XKMYA XMANA XMADN XTAST XTEKS XINSA XKAGT XBLSM XILTM XTCRT XGMYO XSGRT XYORT XFINK XAKUR XSPOR XTRZM XTMTU XHARZ XSD25 XUSRD XKURY XBANA XSIST XMESY XYLDZ XTUMY XKTUM XK030 XK100'.split())

_raw = {}
def raw(s):
    s = ysym(s)
    if s not in _raw:
        p = f'{D}/daily/{s}.parquet'
        if not os.path.exists(p):
            import subprocess
            subprocess.run(['python3', '-I', '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/code/ydl.py', 'daily', s], capture_output=True)
        d = pd.read_parquet(p).copy()
        d.index = pd.DatetimeIndex(d['ldate'].values); d = d[~d.index.duplicated(keep='last')].sort_index()
        _raw[s] = d
    return _raw[s]

_cal = None
def cal():
    global _cal
    if _cal is None:
        d = raw('XU100.IS'); d = d[d['c'].notna() & (d['c'] > 0)]
        _cal = pd.DatetimeIndex(d.index.unique()).sort_values()
    return _cal

_rc = {}
def ret(s, fx_raw=False, field='adj'):
    """BIST takviminde günlük log getiri."""
    s = ysym(s); k = (s, fx_raw, field)
    if k in _rc: return _rc[k]
    d = raw(s); p = d[field] if field in d else d['c']
    p = p.astype(float); p = p[(p > 0) & p.notna()]
    C = cal()
    if s.endswith('.IS'):
        if not is_bist_index(s) and d['v'].fillna(0).gt(0).mean() > 0.5:
            p = p[d['v'].reindex(p.index).fillna(0) > 0]
        r = np.log(p).diff()
        r[(r > UP) | (r < DN)] = np.nan
        r = r.reindex(C)
    else:
        if s.endswith('=X') and not fx_raw:
            p = pd.Series(p.shift(-1).values, index=p.index).dropna()
        C2 = C[C >= p.index[0]]
        pp = p.reindex(p.index.union(C2)).ffill().reindex(C2)
        r = np.log(pp).diff()
        r[r == 0] = np.nan
        sd = r.rolling(250, min_periods=60).std().shift(1)
        r[(r.abs() > 8 * sd) & sd.notna()] = np.nan
        r = r.reindex(C)
    r.name = s; _rc[k] = r; return r

_dc = {}
def decomp(s):
    s = ysym(s)
    if s in _dc: return _dc[s]
    d = raw(s).copy()
    if not is_bist_index(s) and d['v'].fillna(0).gt(0).mean() > 0.5: d = d[d['v'].fillna(0) > 0]
    d = d[(d['adj'] > 0) & (d['c'] > 0)]
    cc = np.log(d['adj']).diff(); intra = np.log(d['c'] / d['o'])
    bad = (d['o'] <= 0) | d['o'].isna() | ((d['h'] == d['l']) & (d['o'] == d['c'].shift(1)))
    intra[bad] = np.nan
    gap = cc - intra
    o = pd.DataFrame({'cc': cc, 'gap': gap, 'intra': intra})
    badcc = (o.cc > UP) | (o.cc < DN); o.loc[badcc, :] = np.nan
    badg = (o.gap > UP) | (o.gap < DN); o.loc[badg, ['gap', 'intra']] = np.nan
    o.loc[o.index < '2014-01-01', ['gap', 'intra']] = np.nan
    o = o.reindex(cal()); _dc[s] = o; return o

def basket(syms, min_n=2, lag=0):
    X = pd.concat([ret(x).shift(lag) for x in syms], axis=1)
    b = X.mean(axis=1); b[X.notna().sum(axis=1) < min_n] = np.nan
    return b

# ---------------- istatistik ----------------
def nw_se_slope(y, x, lags=5):
    """OLS y=a+bx; Newey-West(Bartlett) t of b."""
    y = np.asarray(y, float); x = np.asarray(x, float); n = len(y)
    X = np.column_stack([np.ones(n), x]); XtX_inv = np.linalg.inv(X.T @ X)
    b = XtX_inv @ X.T @ y; u = y - X @ b
    g = X * u[:, None]; S = g.T @ g
    for L in range(1, lags + 1):
        w = 1 - L / (lags + 1); G = g[L:].T @ g[:-L]; S += w * (G + G.T)
    V = XtX_inv @ S @ XtX_inv
    return b[1], b[1] / np.sqrt(V[1, 1])

def _frame(a, b, controls, start=None, end=None):
    cols = [a.rename('a'), b.rename('b')] + [c.rename(f'c{i}') for i, c in enumerate(controls)]
    df = pd.concat(cols, axis=1).dropna()
    if start is not None: df = df[df.index >= pd.Timestamp(start)]
    if end is not None: df = df[df.index <= pd.Timestamp(end)]
    return df

def pcorr(a, b, controls=(), start=None, end=None, min_n=60):
    """Kısmi korelasyon (kontroller + sabit üzerinde artık). Dönüş: (pc, NW t, n)."""
    df = _frame(a, b, controls, start, end); n = len(df)
    if n < min_n: return np.nan, np.nan, n
    ya, yb = df['a'].values, df['b'].values
    if controls:
        C = np.column_stack([np.ones(n)] + [df[f'c{i}'].values for i in range(len(controls))])
        ya = ya - C @ np.linalg.lstsq(C, ya, rcond=None)[0]
        yb = yb - C @ np.linalg.lstsq(C, yb, rcond=None)[0]
    pc = float(np.corrcoef(ya, yb)[0, 1])
    za = (ya - ya.mean()) / ya.std(); zb = (yb - yb.mean()) / yb.std()
    _, t = nw_se_slope(za, zb)
    return pc, t, n

def last_n(a, n=250):
    s = a.dropna(); return s.index[-n] if len(s) >= n else s.index[0]

def years_sign(a, b, controls=(), y0=2010, ref=None, min_n=60):
    vals = {}
    for y in range(y0, 2027):
        pc, t, n = pcorr(a, b, controls, f'{y}-01-01', f'{y}-12-31', min_n=min_n)
        if n >= min_n and not np.isnan(pc): vals[y] = pc
    if not vals: return 0, 0, vals
    if ref is None: ref = np.sign(np.nanmean(list(vals.values())))
    same = sum(1 for v in vals.values() if np.sign(v) == np.sign(ref))
    return same, len(vals), vals

def weekly(r):
    w = r.groupby(pd.Grouper(freq='W-FRI')).agg(['sum', 'count'])
    out = w['sum'].where(w['count'] >= 3); return out

def p_from_t(t):
    from scipy import stats
    return 2 * stats.norm.sf(abs(t))

def bh(p):
    p = np.asarray(p, float); n = np.sum(~np.isnan(p)); o = np.argsort(np.where(np.isnan(p), 9, p))
    q = np.full(len(p), np.nan); prev = 1.0
    ranks = np.arange(1, len(p) + 1)
    pv = np.where(np.isnan(p), np.nan, p)[o]
    qs = pv * n / ranks
    qs = np.minimum.accumulate(qs[::-1])[::-1]
    q[o] = np.minimum(qs, 1)
    return q

# ---------- saatlik 15:00 UTC kesitleri ----------
def snap(s, hh=15, mm=0):
    """Her UTC günü için hh:mm UTC'ye kadar kapanmış son 60m barın kapanışı (bar damgası = başlangıç). 3 saatten eski -> NaN."""
    s = ysym(s); p = f'{D}/h1/{s}.parquet'
    if not os.path.exists(p): return None
    h = pd.read_parquet(p)
    st = h.index.tz_convert(None)
    end = st + pd.Timedelta(minutes=60)
    if s.endswith('.IS'):
        end = pd.DatetimeIndex(np.where((st.hour == 14) & (st.minute == 30), st + pd.Timedelta(minutes=30), end))
        end = pd.DatetimeIndex(np.where((st.hour == 15) & (st.minute == 0), st + pd.Timedelta(minutes=10), end))
    ser = pd.Series(h['c'].values, index=end).sort_index(); ser = ser[~ser.index.duplicated(keep='last')]
    days = pd.DatetimeIndex(ser.index.normalize().unique())
    tg = days + pd.Timedelta(hours=hh, minutes=mm)
    pos = ser.index.searchsorted(tg, side='right') - 1
    ok = pos >= 0
    v = np.where(ok, ser.values[np.clip(pos, 0, None)], np.nan)
    age = tg.values - ser.index.values[np.clip(pos, 0, None)]
    v[age > np.timedelta64(3, 'h')] = np.nan
    return pd.Series(v, index=days)

def snap_ret(s, hh=15, mm=0):
    x = snap(s, hh, mm)
    if x is None: return None
    C = cal(); C2 = C[C >= x.dropna().index[0]] if x.notna().any() else C
    x = x.dropna(); x = x.reindex(x.index.union(C2)).ffill().reindex(C2)
    r = np.log(x).diff(); r[r == 0] = np.nan
    return r.reindex(C)

def bt_sign(sig, tgt, cost_bps=8, thr=0.0, start=None, end=None):
    """sign(sig) * tgt - cost (|sig|>thr günleri). Dönüş: n, ort bps, t, Sharpe(yıllık)."""
    df = pd.concat([sig.rename('s'), tgt.rename('y')], axis=1).dropna()
    if start: df = df[df.index >= pd.Timestamp(start)]
    if end: df = df[df.index <= pd.Timestamp(end)]
    df = df[df.s.abs() > thr]
    if len(df) < 20: return len(df), np.nan, np.nan, np.nan
    pnl = np.sign(df.s) * df.y - cost_bps / 1e4
    m = pnl.mean(); sd = pnl.std()
    t = m / (sd / np.sqrt(len(pnl)))
    return len(df), m * 1e4, t, m / sd * np.sqrt(252)
