"""v_V1_b ortak yardımcılar — BAĞIMSIZ (ll.py / olib.py import edilmez). Ham parquet'ten hizalama."""
import os, numpy as np, pandas as pd
S = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad'
D = S + '/data/daily'
HERE = os.path.dirname(os.path.abspath(__file__))

def load(sym, fx_fix=None):
    d = pd.read_parquet(f'{D}/{sym}.parquet')
    d = d.copy(); d.index = pd.DatetimeIndex(pd.to_datetime(d['ldate'].values)).normalize()
    d = d[~d.index.duplicated(keep='last')].sort_index()
    if fx_fix is None: fx_fix = sym.endswith('=X')
    if fx_fix:  # '=X' bar(t).c = t günü ~00:00 UTC fiyatı -> t günü sonu = bir sonraki barın c'si
        d['c'] = d['c'].shift(-1); d['adj'] = d['adj'].shift(-1); d = d.dropna(subset=['c'])
    return d

def bist_cal():
    x = load('XU100.IS'); x = x[x.c > 0]
    return x.index

def ev_load(kind=('rating',)):
    e = pd.read_csv(HERE + '/events_b.csv', parse_dates=['ann'])
    return e[e.kind.isin(kind)].reset_index(drop=True)

def react_idx(cal, ann, after_close):
    """İlk BIST seansı indeksi. after_close=1: ann'den kesin SONRA; -1 (saat bilinmiyor): muhafazakâr -> ann'den sonra."""
    return int(cal.searchsorted(ann, side='right'))

def tstat(v):
    v = pd.Series(v).dropna(); n = len(v)
    if n < 2 or v.std() == 0: return np.nan, n
    return v.mean() / (v.std(ddof=1) / np.sqrt(n)), n

def fmt(v, nm=''):
    v = pd.Series(v).dropna(); t, n = tstat(v)
    return f'{nm:34s} mean {1e4*v.mean():+7.1f} bps  med {1e4*v.median():+7.1f}  t {t:+5.2f}  hit {100*(v>0).mean():4.0f}%  n {n}'
