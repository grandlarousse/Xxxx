"""holding ajanı yardımcıları (ll.py üzerine; ll.py'yi değiştirmez).
Zamanlama: ll.py konvansiyonu. b_{t-1} -> intra_t = işlenebilir öncülük; b_{t-1} -> gap_t = eşzamansız kapanış (işlenemez).
"""
import sys, os, numpy as np, pandas as pd
SCR = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad'
sys.path.insert(0, SCR + '/code')
import ll  # noqa
OUT = SCR + '/out'
CODE = OUT + '/code_holding'
SPLIT = pd.Timestamp('2021-01-01')
IS0 = pd.Timestamp('2014-01-01')
START = pd.Timestamp('2010-01-01')
RATES = {'^TNX', '^FVX', '^IRX', '^TYX'}  # seviye farkı (bps) kullanılır

_P = None
def panel():
    global _P
    if _P is None:
        _P = pd.read_parquet(SCR + '/data/panel_ret_bistcal.parquet')
    return _P

_CAT = None
def is_fx(sym):
    """Yahoo günlük FX (=X) barı: ldate D 'c' = D-1 sonu (~00:00 UTC D) anlık fiyatı (o≈c). h1 ile doğrulandı."""
    global _CAT
    if _CAT is None:
        _CAT = pd.read_csv(SCR + '/data/catalog.csv').set_index('sym')
    return sym.endswith('=X') or (sym in _CAT.index and str(_CAT.loc[sym, 'type']) == 'CURRENCY')

def fxret(sym, sync=True):
    """FX getirisi. sync=True: UTC günü t (00:00 t -> 00:00 t+1) = düzeltilmiş ll.ret(sym).
    sync=False: UTC günü t-1 = BIST t açılışından ÖNCE bilinir."""
    r = ll.ret(sym)  # ll.FX_FIX=True (koordinatör düzeltmesi) zaten 1 gün kaydırıyor -> burada ek kaydırma YOK
    assert ll.FX_FIX, 'll.FX_FIX kapalı: zaman düzeltmesi gerekli'
    return r if sync else r.shift(1)

def dret(sym, fx_sync=True):
    """sürücü getirisi BIST takviminde. Faizler: seviye farkı (yüzde puan*100 = bps). FX: zaman düzeltmeli (shift -1)."""
    if is_fx(sym): return fxret(sym, fx_sync)
    if sym in RATES:
        s = ll.daily(sym, 'c'); r = s.diff() * 100.0
        sd = r.rolling(250, min_periods=60).std().shift(1); r[(r.abs() > 12 * sd) & sd.notna()] = np.nan
        return r
    if sym == 'CRACK':  # ULSD (HO=F, $/gal*42) - Brent ($/bbl) dizel crack değişimi ($/bbl), BIST takvimi
        ho = ll.daily('HO=F', 'c') * 42; bz = ll.daily('BZ=F', 'c')
        c = (ho - bz); r = c.diff()
        sd = r.rolling(250, min_periods=60).std().shift(1); r[(r.abs() > 12 * sd) & sd.notna()] = np.nan
        return r
    return ll.ret(sym)

def sret(stock, usd=False):
    r = ll.ret(stock)
    if usd: r = r - fxret('TRY=X', True)  # ll.FX_FIX ile hizalı (= ll.bist_usd)
    return r

def mkt(usd=False):
    return sret('XU100', usd)

def _nwt(y, x):
    b, t, n = ll.nw_t(y, x)
    return b, t, n

def zs(s):
    return (s - s.mean()) / s.std()

def corr_t(a, b, start=None, end=None):
    df = pd.concat([a.rename('a'), b.rename('b')], axis=1).dropna()
    if start is not None: df = df[df.index >= pd.Timestamp(start)]
    if end is not None: df = df[df.index < pd.Timestamp(end)]
    if len(df) < 60: return np.nan, np.nan, len(df)
    c = df['a'].corr(df['b']); _, t, n = ll.nw_t(zs(df['a']), zs(df['b']))
    return c, t, n

def pcorr_t(a, b, ctrl, start=None, end=None):
    """kısmi korelasyon (ctrl listesi kontrol) + NW t (artıklar üzerinden)."""
    cs = [c.rename(f'c{i}') for i, c in enumerate(ctrl)]
    df = pd.concat([a.rename('a'), b.rename('b')] + cs, axis=1).dropna()
    if start is not None: df = df[df.index >= pd.Timestamp(start)]
    if end is not None: df = df[df.index < pd.Timestamp(end)]
    if len(df) < 60: return np.nan, np.nan, len(df)
    C = np.column_stack([np.ones(len(df))] + [df[c.name].values for c in cs])
    ra = df['a'].values - C @ np.linalg.lstsq(C, df['a'].values, rcond=None)[0]
    rb = df['b'].values - C @ np.linalg.lstsq(C, df['b'].values, rcond=None)[0]
    pc = float(np.corrcoef(ra, rb)[0, 1])
    _, t, n = ll.nw_t(pd.Series(zs(pd.Series(ra))).values, pd.Series(zs(pd.Series(rb))).values)
    return pc, t, len(df)

def beta(a, b, start=None):
    df = pd.concat([a.rename('a'), b.rename('b')], axis=1).dropna()
    if start is not None: df = df[df.index >= pd.Timestamp(start)]
    if len(df) < 60: return np.nan
    return float(np.cov(df['a'], df['b'])[0, 1] / df['b'].var())

def yr_sign(a, b, k=0, ctrl=None, ref_sign=None):
    """yıllık korelasyon (veya kısmi), aynı işaret oranı."""
    x = b.shift(k)
    cols = [a.rename('a'), x.rename('b')] + ([ctrl.rename('m')] if ctrl is not None else [])
    df = pd.concat(cols, axis=1).dropna()
    out = {}
    for y, g in df.groupby(df.index.year):
        if len(g) < 60: continue
        if ctrl is None: out[y] = g['a'].corr(g['b'])
        else:
            C = np.column_stack([np.ones(len(g)), g['m'].values])
            ra = g['a'].values - C @ np.linalg.lstsq(C, g['a'].values, rcond=None)[0]
            rb = g['b'].values - C @ np.linalg.lstsq(C, g['b'].values, rcond=None)[0]
            out[y] = np.corrcoef(ra, rb)[0, 1]
    s = pd.Series(out)
    if len(s) == 0: return s, np.nan
    sg = ref_sign if ref_sign is not None else np.sign(s.mean())
    return s, float((np.sign(s) == sg).mean())

def decomp(stock):
    return ll.decomp(stock)

def pair(stock, drv, usd=False, start=START, b=None, drv_label=None):
    """Brif standardındaki tüm metrikler. b verilirse sürücü serisi olarak kullanılır."""
    a = sret(stock, usd); m = mkt(usd)
    if b is None: b = dret(drv)
    a = a[a.index >= start]; b = b[b.index >= start]
    last = a.dropna().index.max()
    o = {'stock': stock + ('_USD' if usd else ''), 'driver': drv_label or drv}
    o['corr_full'], o['t_sync'], o['n'] = corr_t(a, b)
    o['corr_3y'], _, _ = corr_t(a, b, start=last - pd.DateOffset(years=3))
    o['corr_1y'], _, _ = corr_t(a, b, start=last - pd.DateOffset(years=1))
    o['pc'], o['pc_t'], _ = pcorr_t(a, b, [m])
    o['pc_IS'], o['pc_IS_t'], _ = pcorr_t(a, b, [m], start=IS0, end=SPLIT)
    o['pc_OOS'], o['pc_OOS_t'], _ = pcorr_t(a, b, [m], start=SPLIT)
    o['c_IS'], _, _ = corr_t(a, b, start=IS0, end=SPLIT)
    o['c_OOS'], _, _ = corr_t(a, b, start=SPLIT)
    o['beta'] = beta(a, b)
    ys, o['yr_same_sign'] = yr_sign(a, b, 0, None, np.sign(o['corr_full']))
    _, o['yr_same_sign_pc'] = yr_sign(a, b, 0, m, np.sign(o['pc']))
    # lag1 cc
    o['c_lag1'], o['t_lag1'], _ = corr_t(a, b.shift(1))
    # ters yön: hisse_{t-1} -> sürücü_t
    o["c_rev"], o["t_rev"], _ = corr_t(b, a.shift(1))
    # gap / intra
    if not usd:
        d = decomp(stock); dm = decomp('XU100')
        d = d[d.index >= IS0]
        o['gap_c'], o['gap_t'], _ = corr_t(d['gap'], b.shift(1))
        o['intra_c'], o['intra_t'], o['n_intra'] = corr_t(d['intra'], b.shift(1))
        o['intra_IS_c'], o['intra_IS_t'], _ = corr_t(d['intra'], b.shift(1), IS0, SPLIT)
        o['intra_OOS_c'], o['intra_OOS_t'], _ = corr_t(d['intra'], b.shift(1), SPLIT)
        # XU100 gün içi kontrollü (hisseye özgü işlenebilir kısım)
        o['intra_pc'], o['intra_pc_t'], _ = pcorr_t(d['intra'], b.shift(1), [dm['intra']])
        # çok günlü sürüklenme: b_{t-1} -> cc_{t+1..t+4} (t gününden sonraki 4 gün)
        fwd = sum(a.shift(-j) for j in range(1, 5))
        o['drift_c'], o['drift_t'], _ = corr_t(fwd, b.shift(1))
    return o

def bt_summary(res):
    o = {}
    for k in ['IS', 'OOS', 'ALL']:
        r = res.get(k, {})
        for f in ['n', 'mean_bps', 't', 'hit', 'sharpe', 'ann_ret_pct', 'maxdd_pct']:
            o[f'{k}_{f}'] = r.get(f, np.nan)
    o['by_year'] = res.get('by_year_bps')
    return o

def fmt(x, d=3):
    try:
        if x is None or (isinstance(x, float) and np.isnan(x)): return ''
        return f'{x:.{d}f}'
    except Exception:
        return str(x)
