"""v_YG1_b ortak modül — bağımsız temizlik/hizalama (ll.py ve v_YG1_a/vc.py import EDİLMEZ).
Kurallar:
 - bayat gün: v==0 ve h==l -> satır atılır
 - kurumsal işlem / bozuk veri eşiği rejime bağlı: 2020-03-13 öncesi |oran-1|>%20,5, sonrası >%10,5
   (adj cc, adj gap ve ham o/c_{-1} için ayrı ayrı); gün-içi |ln(c/o)| > ln((1+L)/(1-L)) bozuk
 - önceki geçerli satır bir önceki BIST günü değilse gap NaN
 - gap = ln(o*adj/c / adj_{-1}); intra = ln(c/o)
"""
import numpy as np, pandas as pd, os
D = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data'
S47 = 'AEFES AKBNK AKSEN ALARK ARCLK ASELS ASTOR BIMAS BRSAN CIMSA DOAS DOHOL EKGYO ENJSA ENKAI EREGL FROTO GARAN GUBRF HALKB HEKTS ISCTR KCHOL KRDMD MGROS ODAS OYAKC PETKM PGSUS SAHOL SASA SISE SOKM TAVHL TCELL THYAO TKFEN TOASO TRALT TRMET TSKB TTKOM TUPRS ULKER VAKBN VESTL YKBNK'.split()
REG = pd.Timestamp('2020-03-13')

def load_daily(sym):
    d = pd.read_parquet(f'{D}/daily/{sym}.IS.parquet')
    d = d.copy(); d['date'] = pd.to_datetime(d['ldate']).dt.normalize()
    d = d.set_index('date').sort_index()
    d = d[~d.index.duplicated(keep='last')]
    return d

def calendar():
    x = load_daily('XU100'); x = x[x.index >= '2013-06-01']
    return x.index

CAL = None
def clean(sym, start='2013-06-01'):
    global CAL
    if CAL is None: CAL = calendar()
    d = load_daily(sym); d = d[d.index >= start]
    d = d[(d.o > 0) & (d.c > 0) & (d.adj > 0)]
    stale = (d.v.fillna(0) == 0) & (d.h == d.l)
    d = d[~stale].copy()
    d = d[d.index.isin(CAL)]
    pos = pd.Series(np.arange(len(CAL)), index=CAL)
    p = pos.reindex(d.index).values
    consec = np.r_[False, np.diff(p) == 1]
    L = np.where(d.index < REG, 0.205, 0.105)
    lo, hi = np.log(1 - L), np.log(1 + L)
    f = d.adj / d.c
    ao = d.o * f
    cc = np.log(d.adj / d.adj.shift())
    gap = np.log(ao / d.adj.shift())
    rawgap = np.log(d.o / d.c.shift())
    intra = np.log(d.c / d.o)
    bad = (cc < lo) | (cc > hi) | (gap < lo) | (gap > hi)
    # ham açılış oranı limit dışı ve adj gap de şüpheliyse
    bad |= ((rawgap < lo) | (rawgap > hi)) & ((gap < lo) | (gap > hi))
    bad_i = (intra.abs() > np.log((1 + L) / (1 - L)))
    out = pd.DataFrame({'o': d.o, 'h': d.h, 'l': d.l, 'c': d.c, 'adj': d.adj, 'v': d.v,
                        'gap': gap.where(consec & ~bad), 'intra': intra.where(~bad_i),
                        'cc': cc.where(consec & ~bad), 'rawgap': rawgap.where(consec & ~bad),
                        'tv': d.c * d.v, 'f': f})
    out['divday'] = (np.abs(np.log(f / f.shift())) > 1e-4) & consec
    out['sym'] = sym
    return out

def panel(syms=S47, add_index=True):
    fr = {s: clean(s) for s in syms}
    if add_index:
        fr['XU030'] = clean('XU030')
    return fr

def wide(fr, col):
    return pd.DataFrame({s: v[col] for s, v in fr.items()})

def tstat(x):
    x = np.asarray(x, float); x = x[~np.isnan(x)]
    if len(x) < 3: return np.nan
    return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))

def nw_t(x, lags=5):
    x = pd.Series(x).dropna().values
    n = len(x)
    if n < 10: return np.nan
    e = x - x.mean(); g0 = (e @ e) / n; s = g0
    for k in range(1, lags + 1):
        s += 2 * (1 - k / (lags + 1)) * (e[k:] @ e[:-k]) / n
    return x.mean() / np.sqrt(s / n)

def clus_t(vals, days):
    """işlem bazında ortalama, gün kümelenmiş t"""
    df = pd.DataFrame({'v': vals, 'd': days}).dropna()
    n = len(df)
    if n < 10: return np.nan, np.nan, 0
    m = df.v.mean()
    g = (df.v - m).groupby(df.d).sum()
    se = np.sqrt((g ** 2).sum()) / n
    return m, m / se, n

def bh(p, q=0.05):
    p = np.asarray(p, float); n = np.sum(~np.isnan(p))
    o = np.argsort(np.where(np.isnan(p), np.inf, p))
    r = np.empty(len(p)); r[o] = np.arange(1, len(p) + 1)
    thr = np.where(np.isnan(p), np.inf, p) <= q * r / n
    k = np.max(r[thr]) if thr.any() else 0
    return (r <= k) & ~np.isnan(p)

PERIODS = {'14-17': ('2014-01-01', '2017-12-31'), '18-20': ('2018-01-01', '2020-12-31'),
           '21-23': ('2021-01-01', '2023-12-31'), '24-26': ('2024-01-01', '2026-12-31'),
           'IS': ('2014-01-01', '2020-12-31'), 'OOS': ('2021-01-01', '2026-12-31'),
           'IS16': ('2016-01-01', '2020-12-31'), 'ALL': ('2014-01-01', '2026-12-31')}
