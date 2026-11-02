"""olay ajanı yardımcıları (ll.py'yi kullanır, değiştirmez)."""
import sys, numpy as np, pandas as pd
SC = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad'
sys.path.insert(0, SC + '/code'); import ll
from universe import VIOP
OUT = SC + '/out'
EV = pd.read_csv(OUT + '/olay_tarihleri.csv', parse_dates=['date', 'react_date'])
_P = None
UP, DN = np.log(1.105), np.log(0.895)   # SİMETRİK fiyat eşiği (ll.py'deki |r|>ln1.105 kuralı -%10 limit-down günlerini atıyor)
IDX = ['XU100', 'XU030', 'XBANK', 'XUSIN', 'XHOLD', 'XLBNK']
def decomp2(sym):
    d = ll.raw(ll.T(sym)).copy(); d.index = pd.DatetimeIndex(d['ldate'].values); d = d[~d.index.duplicated(keep='last')]
    if d['v'].fillna(0).gt(0).mean() > 0.5: d = d[d['v'].fillna(0) > 0]
    cc = np.log(d['adj']).diff(); intra = np.log(d['c'] / d['o'])
    bad = (d['o'] <= 0) | d['o'].isna() | ((d['h'] == d['l']) & (d['o'] == d['c'].shift(1)))
    intra[bad] = np.nan; gap = cc - intra
    o = pd.DataFrame({'cc': cc, 'gap': gap, 'intra': intra})
    if sym not in IDX:
        o.loc[(o.cc > UP) | (o.cc < DN), :] = np.nan
        o.loc[(o.gap > UP) | (o.gap < DN), ['gap', 'intra']] = np.nan
    o.loc[o.index < pd.Timestamp('2014-01-01'), ['gap', 'intra']] = np.nan
    return o
def panel():
    global _P
    if _P is None:
        import os
        f = SC + '/out/code_olay/_panel_decomp_sym.parquet'
        if os.path.exists(f): _P = pd.read_parquet(f)
        else:
            _P = pd.concat({s: decomp2(s) for s in VIOP + IDX}, axis=1); _P = _P[_P.index >= '2014-01-01']; _P.to_parquet(f)
    return _P
def comp(field):  # DataFrame hisseler x tarih
    p = panel(); return p.xs(field, axis=1, level=1)
CAL = ll.bist_cal()
def tstat(x):
    x = pd.Series(x).dropna(); n = len(x)
    return (x.mean() / (x.std(ddof=1) / np.sqrt(n)) if n > 2 and x.std() > 0 else np.nan), n
def fwd_cc(cc, k1, k2):
    """t+k1..t+k2 kümülatif cc (t'ye hizalı)."""
    s = sum(cc.shift(-k) for k in range(k1, k2 + 1)); return s
def event_table(dates, cols=('XU100','XBANK','XU030'), extra=None):
    """dates: react_date listesi. Her olay için gap/intra/cc ve t+1..t+5 kümülatif."""
    cc, gp, it = comp('cc'), comp('gap'), comp('intra')
    f15 = fwd_cc(cc, 1, 5)
    rows = []
    for d in dates:
        if d not in cc.index: continue
        r = {'react_date': d}
        for c in cols:
            r[f'{c}_gap'] = gp.at[d, c]; r[f'{c}_intra'] = it.at[d, c]; r[f'{c}_cc'] = cc.at[d, c]; r[f'{c}_f1_5'] = f15.at[d, c]
        rows.append(r)
    return pd.DataFrame(rows)
def xsec(dates, sign=None, field='cc', bench='XU100'):
    """Hisse bazında olay günü aşırı getiri (hisse - XU100) ortalaması, işaret ile çarpılmış (sign: dict date->±1)."""
    X = comp(field); ex = X[VIOP].sub(X[bench], axis=0)
    ds = [d for d in dates if d in ex.index]
    E = ex.loc[ds]
    if sign is not None: E = E.mul(pd.Series([sign[d] for d in ds], index=ds), axis=0)
    out = pd.DataFrame({'mean_bps': 1e4 * E.mean(), 't': E.mean() / (E.std() / np.sqrt(E.notna().sum())), 'n': E.notna().sum()})
    return out.sort_values('mean_bps')
def abs_ratio(dates, field='gap', cols=None):
    """Olay günlerinde |getiri| / normal günler |getiri| oranı (hisse bazında)."""
    X = comp(field); cols = cols or (VIOP + ['XU100', 'XBANK'])
    ds = pd.DatetimeIndex([d for d in dates if d in X.index])
    m = X.index.isin(ds)
    a = X.loc[m, cols].abs().mean(); b = X.loc[~m, cols].abs().mean()
    return (a / b).sort_values()
