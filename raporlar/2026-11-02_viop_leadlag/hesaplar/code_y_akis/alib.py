"""akis ajanı ortak yardımcıları (ll.py'ye dokunmaz). Panel önbelleği: out/code_y_akis/_panel_ohlc.parquet"""
import os, sys, numpy as np, pandas as pd
SCR = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad'
sys.path.insert(0, SCR + '/code'); import ll  # noqa
HERE = os.path.dirname(os.path.abspath(__file__))
VIOP = ll.VIOP
# Fiyat limiti rejimleri (veriden tespit: bkz. a_limit.py başlığı)
P20_START, P20_END = pd.Timestamp('2015-12-01'), pd.Timestamp('2020-03-10')
P10_START = pd.Timestamp('2020-03-13')
SPLIT = pd.Timestamp('2021-01-01')  # IS/OOS (P10 rejiminde IS=2020-03..2022-12 kullanılır, bkz. rapor)

def bist_stocks():
    c = pd.read_csv(SCR + '/data/catalog.csv')
    b = c[c.group.isin(['VIOP', 'BIST_other'])].sym.tolist()
    return [s for s in b if not s.startswith('X')]

def panel(force=False):
    """dict of wide DataFrames o,h,l,c,adj,v (index=BIST tarih, columns=kısa kod). Sıfır hacimli günler NaN."""
    p = HERE + '/_panel_ohlc.parquet'
    if os.path.exists(p) and not force:
        P = pd.read_parquet(p); return {k: P[k] for k in ['o', 'h', 'l', 'c', 'adj', 'v']}
    out = {k: {} for k in ['o', 'h', 'l', 'c', 'adj', 'v']}
    for s in bist_stocks():
        d = ll.raw(s).copy(); d.index = pd.DatetimeIndex(d['ldate'].values); d = d[~d.index.duplicated(keep='last')]
        d = d[d['v'].fillna(0) > 0]
        k = s.replace('.IS', '')
        for f in out: out[f][k] = d[f]
    P = pd.concat({f: pd.DataFrame(v).sort_index() for f, v in out.items()}, axis=1)
    P = P[P.index >= '2005-01-01']
    P.to_parquet(p)
    return {k: P[k] for k in ['o', 'h', 'l', 'c', 'adj', 'v']}

def xu(sym='XU100'):
    d = ll.raw(sym + '.IS').copy(); d.index = pd.DatetimeIndex(d['ldate'].values); d = d[~d.index.duplicated(keep='last')]
    cc = np.log(d['adj']).diff(); it = np.log(d['c'] / d['o']); gp = cc - it
    return pd.DataFrame({'cc': cc, 'gap': gp, 'intra': it})

def tstat(x):
    x = pd.Series(x).dropna()
    if len(x) < 3: return np.nan, len(x)
    return x.mean() / (x.std(ddof=1) / np.sqrt(len(x))), len(x)

def cluster_t(df, val, cl='date'):
    """Tarih kümelenmiş t (aynı gün çok olay -> ortalamaların t'si)."""
    g = df.groupby(cl)[val].mean().dropna()
    return tstat(g)

def nw(y, lags=5):
    b, t, n = ll.nw_t(pd.Series(y).dropna(), lags=lags); return b, t, n
