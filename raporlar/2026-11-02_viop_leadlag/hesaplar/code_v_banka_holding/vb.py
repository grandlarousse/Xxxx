# -*- coding: utf-8 -*-
"""
v_banka_holding — BAGIMSIZ dogrulama kutuphanesi (ll.py IMPORT EDILMEZ).
Ham parquet -> kendi hizalama / temizlik / istatistik.

Konvansiyonlar (kendi kararlarim, BRIEF ile uyumlu):
- BIST takvimi: XU100.IS satirlari (ldate) — hisse satirlari tatil gunlerinde v=0 bayat satir icerebilir; takvime reindex ile atilir.
- BIST hisse: cc = log(adj_t/adj_{t-1}); fiyat bazinda |c_t/c_{t-1}-1|>%10,5 (veya adj bazinda) -> o gunun cc/gap/intra NaN (simetrik).
  Endekslere temizlik UYGULANMAZ (fiyat limiti yok; 2013-06-03 XBANK -%11 gercek).
  gap = log(o_t * (adj_t/c_t) / adj_{t-1}), intra = log(c_t/o_t); 2014 oncesi gap/intra NaN (acilis verisi bozuk).
- BIST disi: her BIST gunu t icin "t gunu veya oncesindeki son gozlem" (ffill, max 7 takvim gunu bayatlik) -> log getiri.
  Yahoo '=X' FX: ldate=d satirinin kapanisi ~d gunu 00:00 UTC (= d-1 sonu) -> satir bazinda 1 geri kaydirma
  (i+1. satirin fiyati i. satirin tarihine atanir). (Saatlikle dogrulandi: gunluk c(d) ~ saatlik 23:00 UTC(d-1), medyan 2,8 bp.)
- Kismi korelasyon: y ve x, [1, Z] uzerine OLS ile artiklastirilir; pc = corr(e_y, e_x). t: y ~ x + Z regresyonunda x katsayisinin
  Newey-West(5) t'si.
"""
import numpy as np, pandas as pd, os, warnings
warnings.filterwarnings('ignore')
D = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data'
_cache = {}

def load_daily(sym):
    if sym in _cache: return _cache[sym]
    x = pd.read_parquet(f'{D}/daily/{sym}.parquet')
    x.index = pd.to_datetime(x['ldate']).dt.normalize()
    x.index = x.index.tz_localize(None) if x.index.tz is not None else x.index
    x = x[~x.index.duplicated(keep='last')].sort_index()
    _cache[sym] = x
    return x

def bist_cal(start='2005-01-01'):
    x = load_daily('XU100.IS')
    x = x[(x['c'] > 0) & x['c'].notna()]
    return x.index[x.index >= start]

CAL = bist_cal()

def _is_index(sym):
    return sym.startswith('X') and sym.endswith('.IS') and sym[:-3].isalpha() and sym[:-3] in INDEXES

INDEXES = set('XU030 XU050 XU100 XUTUM XYUZO XTUMY XKTUM XK030 XK100 XBANK XLBNK X10XB XHOLD XUSIN XUMAL XUHIZ XUTEK XULAS XELKT XGIDA XKMYA XMANA XMADN XTAST XTEKS XINSA XKAGT XBLSM XILTM XTCRT XGMYO XSGRT XYORT XFINK XAKUR XSPOR XTRZM XTMTU XHARZ XSD25 XUSRD XKURY XBANA XSIST XMESY XYLDZ'.split())

def bist_rets(sym, cal=CAL, clean=None):
    """DataFrame cc, gap, intra (log) on BIST calendar."""
    x = load_daily(sym)
    if clean is None: clean = not _is_index(sym)
    c = x['c'].reindex(cal); a = x['adj'].reindex(cal); o = x['o'].reindex(cal)
    h = x['h'].reindex(cal); l = x['l'].reindex(cal)
    for s in (c, a, o):
        s[s <= 0] = np.nan
    cc = np.log(a / a.shift(1))
    gap = np.log(o * (a / c) / a.shift(1))
    intra = np.log(c / o)
    if clean:
        pr = c / c.shift(1) - 1; pa = a / a.shift(1) - 1
        bad = (pr.abs() > 0.105) | (pa.abs() > 0.105)
        cc[bad] = np.nan; gap[bad] = np.nan; intra[bad] = np.nan
    # acilis sanity: o [l,h] disinda ise NaN
    badopen = (o > h * 1.0001) | (o < l * 0.9999)
    gap[badopen] = np.nan; intra[badopen] = np.nan
    pre = cal < pd.Timestamp('2014-01-01')
    gap[pre] = np.nan; intra[pre] = np.nan
    return pd.DataFrame({'cc': cc, 'gap': gap, 'intra': intra}, index=cal)

FX_SWITCH = pd.Timestamp('2010-08-04')
FXMODE = os.environ.get('VB_FXMODE', 'fix2')

def fx_align(p):
    """Yahoo '=X' gunluk zaman damgasi konvansiyonu 2010-08-04'te DEGISIYOR (FXE/EURUSD, EWZ/BRL, EZA/ZAR, XU100/USDTRY ile dogrulandi):
    ldate < 2010-08-04: satir = AYNI gunun kapanisi (kaydirma YOK);
    ldate >= 2010-08-04: satir = ~00:00 UTC (= onceki gun sonu) -> bir satir geri kaydir. 2010-08-03/04 satirlari ayni fiyat (gecis tekrari).
    FXMODE='fix1' -> tum tarihi kaydir (ll.FX_FIX benzeri), 'raw' -> hic kaydirma."""
    if FXMODE == 'raw':
        return p
    if FXMODE == 'fix1':
        return pd.Series(p.values[1:], index=p.index[:-1])
    idx = p.index; v = p.values
    pre = pd.Series(v[idx < FX_SWITCH], index=idx[idx < FX_SWITCH])
    pos = np.where(idx >= FX_SWITCH)[0]
    pos = pos[pos >= 1]
    post = pd.Series(v[pos], index=idx[pos - 1])
    out = pd.concat([pre, post])
    out = out[~out.index.duplicated(keep='last')].sort_index()
    return out

def ext_ret(sym, cal=CAL, field='adj', maxstale=7):
    """BIST disi sembolun BIST takvimine oturtulmus log getirisi (t gunu dahil son gozlem)."""
    x = load_daily(sym)
    p = x[field].astype(float)
    p = p[(p > 0) & p.notna()]
    if sym.endswith('=X'):
        p = fx_align(p)
    lastd = pd.Series(p.index, index=p.index)
    u = p.index.union(cal)
    pon = p.reindex(u).ffill().reindex(cal)
    ld = lastd.reindex(u).ffill().reindex(cal)
    stale = (pd.Series(cal, index=cal) - ld).dt.days > maxstale
    pon[stale] = np.nan
    pon[cal > p.index.max()] = np.nan
    pon[cal < p.index.min()] = np.nan
    return np.log(pon / pon.shift(1))

def ret(sym, cal=CAL):
    if sym.endswith('.IS'):
        return bist_rets(sym, cal)['cc']
    return ext_ret(sym, cal)

# ---------------- istatistik ----------------
def _nw_se(X, e, lags=5):
    n, k = X.shape
    XtX_inv = np.linalg.pinv(X.T @ X)
    u = X * e[:, None]
    S = u.T @ u
    for L in range(1, lags + 1):
        w = 1 - L / (lags + 1)
        G = u[L:].T @ u[:-L]
        S += w * (G + G.T)
    V = XtX_inv @ S @ XtX_inv
    return np.sqrt(np.maximum(np.diag(V), 0))

def ols(y, X, lags=5):
    X1 = np.column_stack([np.ones(len(y)), X])
    b, *_ = np.linalg.lstsq(X1, y, rcond=None)
    e = y - X1 @ b
    se = _nw_se(X1, e, lags)
    return b[1:], se[1:], e

def pc(y, x, Z=None, lags=5):
    """y,x: Series; Z: DataFrame or None. Returns dict(n, corr, pc, beta, t)."""
    df = pd.concat([y.rename('y'), x.rename('x')] + ([Z] if Z is not None else []), axis=1).dropna()
    n = len(df)
    if n < 30: return dict(n=n, corr=np.nan, pc=np.nan, beta=np.nan, t=np.nan)
    yy = df['y'].values; xx = df['x'].values
    r = np.corrcoef(yy, xx)[0, 1]
    if Z is not None and Z.shape[1] > 0:
        zz = df[list(Z.columns)].values
        Z1 = np.column_stack([np.ones(n), zz])
        ey = yy - Z1 @ np.linalg.lstsq(Z1, yy, rcond=None)[0]
        ex = xx - Z1 @ np.linalg.lstsq(Z1, xx, rcond=None)[0]
        p = np.corrcoef(ey, ex)[0, 1]
        b, se, _ = ols(yy, np.column_stack([xx, zz]), lags)
    else:
        p = r
        b, se, _ = ols(yy, xx[:, None], lags)
    return dict(n=n, corr=r, pc=p, beta=b[0], t=b[0] / se[0] if se[0] > 0 else np.nan)

LAST = pd.Timestamp('2026-10-30')
PERIODS = {
    'full2005': ('2005-01-01', '2026-12-31'),
    'full2010': ('2010-01-01', '2026-12-31'),
    'IS14_20': ('2014-01-01', '2020-12-31'),
    'OOS21_26': ('2021-01-01', '2026-12-31'),
    'last3y': ('2023-10-31', '2026-12-31'),
    'last1y': ('2025-10-31', '2026-12-31'),
}

def per(s, a, b):
    return s[(s.index >= a) & (s.index <= b)]

def summarize(y, x, Z=None, periods=PERIODS):
    out = {}
    for k, (a, b) in periods.items():
        yy = per(y, a, b); xx = per(x, a, b); ZZ = per(Z, a, b) if Z is not None else None
        out[k] = pc(yy, xx, ZZ)
    return out

def yearly(y, x, Z=None, start=2010, end=2026, minn=100):
    rows = []
    for yr in range(start, end + 1):
        a, b = f'{yr}-01-01', f'{yr}-12-31'
        d = pc(per(y, a, b), per(x, a, b), per(Z, a, b) if Z is not None else None)
        if d['n'] >= minn:
            rows.append(dict(year=yr, **d))
    return pd.DataFrame(rows)

def same_sign_frac(yr_df, col, ref):
    if len(yr_df) == 0 or col not in yr_df: return np.nan, 0
    v = yr_df[col].dropna()
    if len(v) == 0: return np.nan, 0
    return float((np.sign(v) == np.sign(ref)).mean()), len(v)

def fmt(d, keys=('n', 'corr', 'pc', 't')):
    return ' '.join(f"{k}={d[k]:.3f}" if k != 'n' else f"n={d[k]}" for k in keys)
