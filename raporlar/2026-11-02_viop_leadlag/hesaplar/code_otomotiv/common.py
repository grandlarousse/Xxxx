"""otomotiv ajanı ortak yardımcıları (ll.py'nin ÜZERİNE kurulu; ll.py değiştirilmez).
Zamanlama (ll.py konvansiyonu): BIST günü t için sürücü getirisi r_d(t) = (t_önceki, t] (sürücü yerel tarih <= t son kapanış).
  - ABD / FX / kripto / vadeli: kapanış BIST kapanışından SONRA -> işlenebilir öncülük = sürücü_{t-1} -> BIST intra_t.
  - Avrupa: kapanış 15:30/16:30 UTC (BIST 15:00 UTC'den 0,5-1,5 saat sonra) -> işlenebilir = lag1 -> intra.
  - Kore/Japonya/Tayvan: kapanış 05:30-06:30 UTC, BIST açılışı ~07:00 UTC -> sürücü lag0 BIST t açılışından ÖNCE bilinir:
    işlenebilir = sürücü_t (lag0) -> BIST intra_t.  HK (08:00 UTC) ve Hindistan (10:00 UTC) BIST seansıyla çakışır -> lag0 işlenebilir DEĞİL.
"""
import sys, os
sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/code')
import numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
import ll

OUT = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out'
CODE = os.path.join(OUT, 'code_otomotiv')
RES = os.path.join(CODE, 'res'); os.makedirs(RES, exist_ok=True)
STOCKS = ['FROTO', 'TOASO', 'DOAS', 'ARCLK', 'VESTL', 'ASTOR']
SPLIT = '2021-01-01'

ASIA_PRE = ('.KS', '.KQ', '.T', '.TW')       # BIST açılışından önce kapanan borsalar
ASIA_OVERLAP = ('.HK', '.NS', '.BO', '.SS', '.SZ', '.SI', '.JK', '.KL', '.BK')  # seansla çakışır

def timing(sym):
    s = sym.upper()
    if s.endswith('.IS'): return 'bist'
    if s.endswith(ASIA_PRE) or s in ('^N225', '^KS11', '^TWII', 'KRW=X'): return 'asia_pre'
    if s.endswith(ASIA_OVERLAP) or s in ('^HSI', '^HSCE', '^NSEI', '^BSESN'): return 'asia_overlap'
    return 'post'  # ABD, Avrupa, FX, vadeli, kripto: BIST kapanışından sonra kapanır (lag1 işlenebilir)

def lead_lag(sym):
    """işlenebilir öncülük testinde kullanılacak gecikme: asia_pre -> 0, diğer -> 1"""
    return 0 if timing(sym) == 'asia_pre' else 1

_rc = {}
def R(sym, mask_zero=True):
    """BIST takvimli log getiri. BIST dışı sürücüde tam 0 (tatil ffill) -> NaN."""
    k = (sym, mask_zero)
    if k in _rc: return _rc[k]
    r = ll.ret(sym)
    if mask_zero and not ll.is_bist(ll.T(sym)): r = r.where(r != 0)
    r.name = sym; _rc[k] = r; return r

_dc = {}
def D(stock):
    if stock not in _dc: _dc[stock] = ll.decomp(stock)
    return _dc[stock]

def M(): return R('XU100')
def USDTRY(): return R('TRY=X')

def corr_t(a, b, start=None, end=None):
    df = pd.concat([a.rename('a'), b.rename('b')], axis=1).dropna()
    if start: df = df[df.index >= pd.Timestamp(start)]
    if end: df = df[df.index < pd.Timestamp(end)]
    if len(df) < 40: return np.nan, np.nan, len(df)
    c = df['a'].corr(df['b'])
    za = (df['a'] - df['a'].mean()) / df['a'].std(); zb = (df['b'] - df['b'].mean()) / df['b'].std()
    _, t, n = ll.nw_t(za, zb)
    return c, t, n

def pcorr(a, b, controls, start=None, end=None):
    df = pd.concat([a.rename('a'), b.rename('b')] + [c.rename(f'c{i}') for i, c in enumerate(controls)], axis=1).dropna()
    if start: df = df[df.index >= pd.Timestamp(start)]
    if end: df = df[df.index < pd.Timestamp(end)]
    if len(df) < 40: return np.nan, np.nan, len(df)
    C = np.column_stack([np.ones(len(df))] + [df[f'c{i}'].values for i in range(len(controls))])
    ra = df['a'].values - C @ np.linalg.lstsq(C, df['a'].values, rcond=None)[0]
    rb = df['b'].values - C @ np.linalg.lstsq(C, df['b'].values, rcond=None)[0]
    ra = pd.Series(ra, index=df.index); rb = pd.Series(rb, index=df.index)
    c = float(np.corrcoef(ra, rb)[0, 1])
    _, t, n = ll.nw_t((ra - ra.mean()) / ra.std(), (rb - rb.mean()) / rb.std())
    return c, t, n

def beta(a, b, start=None):
    df = pd.concat([a.rename('a'), b.rename('b')], axis=1).dropna()
    if start: df = df[df.index >= pd.Timestamp(start)]
    if len(df) < 40: return np.nan
    return float(np.cov(df['a'], df['b'])[0, 1] / df['b'].var())

def year_sign_share(a, b, ref_sign, min_n=60):
    df = pd.concat([a.rename('a'), b.rename('b')], axis=1).dropna()
    g = df.groupby(df.index.year).apply(lambda x: x['a'].corr(x['b']) if len(x) >= min_n else np.nan).dropna()
    if len(g) == 0: return np.nan, 0, g
    return float((np.sign(g) == ref_sign).mean()), len(g), g

def last_date():
    return R('XU100').dropna().index.max()

def split_for(a, b):
    """IS/OOS ayrımı: standart 2014-2020 / 2021+. Ortak örneklem 2019 sonrası başlıyorsa (ör. ASTOR, GEV) örneklem ortası."""
    df = pd.concat([a, b], axis=1).dropna()
    if len(df) == 0: return pd.Timestamp(SPLIT), '2014-01-01'
    if df.index[0] > pd.Timestamp('2019-01-01'):
        return df.index[len(df) // 2], str(df.index[0].date())
    return pd.Timestamp(SPLIT), '2014-01-01'

def pair_stats(stock, driver, start='2010-01-01'):
    """Bir hisse-sürücü çifti için standart istatistikler (senkron + öncülük + ters)."""
    a = R(stock); b = R(driver)
    a = a[a.index >= pd.Timestamp(start)]
    m = M(); u = USDTRY()
    ld = last_date(); s3 = ld - pd.DateOffset(years=3); s1 = ld - pd.DateOffset(years=1)
    o = {'stock': stock, 'driver': driver, 'timing': timing(driver)}
    o['c_full'], o['t_full'], o['n'] = corr_t(a, b)
    o['c_3y'], _, o['n_3y'] = corr_t(a, b, start=s3)
    o['c_1y'], _, o['n_1y'] = corr_t(a, b, start=s1)
    o['c_lag1'], o['t_lag1'], _ = corr_t(a, b.shift(1))     # ABD vb.: senkron ilişkinin eşzamansız kısmı
    o['pc_xu100'], o['pc_t'], _ = pcorr(a, b, [m])
    o['pc_xu100_3y'], _, _ = pcorr(a, b, [m], start=s3)
    o['pc_xu100_usd'], _, _ = pcorr(a, b, [m, u])           # XU100 + USDTRY kontrollü
    o['c_usd'], _, _ = corr_t(a - u, b)                      # USD bazlı hisse getirisi
    o['beta'] = beta(a, b)
    sp, is0 = split_for(a, b)
    o['split'] = str(sp.date())
    o['c_IS'], o['t_IS'], _ = corr_t(a, b, start=is0, end=sp)
    o['c_OOS'], o['t_OOS'], _ = corr_t(a, b, start=sp)
    o['pc_IS'], o['pc_t_IS'], _ = pcorr(a, b, [m], start=is0, end=sp)
    o['pc_OOS'], o['pc_t_OOS'], _ = pcorr(a, b, [m], start=sp)
    sh, ny, _ = year_sign_share(a, b, np.sign(o['c_full']) if pd.notna(o['c_full']) else 1)
    o['yr_same_sign'], o['n_years'] = sh, ny
    # ters yön: hisse_{t-1} -> sürücü_t   (Asya için: hisse_t -> Asya_{t+1})
    if timing(driver) == 'asia_pre':
        o['rev_c'], o['rev_t'], _ = corr_t(b.shift(-1), a)
    else:
        o['rev_c'], o['rev_t'], _ = corr_t(b, a.shift(1))
    # öncülük: gap / intra
    d = D(stock); L = lead_lag(driver)
    bl = b.shift(L)
    o['lead_lag'] = L
    o['gap_c'], o['gap_t'], _ = corr_t(d['gap'], bl)
    o['intra_c'], o['intra_t'], o['intra_n'] = corr_t(d['intra'], bl)
    o['intra_c_IS'], o['intra_t_IS'], _ = corr_t(d['intra'], bl, end=sp)
    o['intra_c_OOS'], o['intra_t_OOS'], _ = corr_t(d['intra'], bl, start=sp)
    # piyasa kontrollü gün-içi öncülük (XU100 gap_t biliniyor; ABD lag1'i de kontrol)
    xg = D('XU100')['gap']
    o['intra_pc_ctrl'], o['intra_pc_t'], _ = pcorr(d['intra'], bl, [xg, R('^GSPC').shift(1)])
    # çok günlük sürüklenme: sürücü_{t-L} -> hisse cc t+1..t+4 toplamı (bilindikten sonraki günler)
    fwd = sum(a.shift(-k) for k in range(1, 5))
    o['drift_c'], o['drift_t'], _ = corr_t(fwd, bl)
    return o

# ---------- backtest yardımcıları ----------
def bt(signal, target, costs=(8, 15), mode='sign', thr=0.0, split=SPLIT, start='2014-01-01'):
    signal = signal[signal.index >= pd.Timestamp(start)]
    out = {}
    for c in costs:
        r, pnl = ll.backtest(signal, target, cost_bps=c, mode=mode, thr=thr, split=split)
        out[c] = (r, pnl)
    return out

def bt_row(name, res, cost):
    r = res[cost][0]
    row = {'test': name, 'cost_bps': cost}
    for k in ['IS', 'OOS', 'ALL']:
        for f in ['n', 'mean_bps', 't', 'hit', 'sharpe', 'ann_ret_pct', 'maxdd_pct']:
            row[f'{k}_{f}'] = r[k].get(f, np.nan)
    row['by_year_bps'] = str(r['by_year_bps'])
    return row

def fmt(x, d=3):
    try:
        if pd.isna(x): return 'nan'
    except Exception: pass
    return f'{x:.{d}f}' if isinstance(x, (float, np.floating)) else str(x)
