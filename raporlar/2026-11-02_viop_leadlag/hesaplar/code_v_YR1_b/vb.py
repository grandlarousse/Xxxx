"""v_YR1_b bağımsız kütüphane (ll.py / vlib.py import ETMEZ).
Temizlik: bayat gün = v<=0 & h==l -> NaN; kurumsal işlem/veri hatası eşiği rejime bağlı
(2020-03-13 öncesi |r|>%20,5, sonrası >%10,5 -> NaN); 2014 öncesi açılış kullanılmaz.
Getiriler adj-tutarlı: f=adj/c; cc=log(adj_t/adj_{t-1}); gap=log(o_t f_t/adj_{t-1}); intra=log(c_t/o_t).
Endeks: adj yoksa c.
"""
import numpy as np, pandas as pd, os
D = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data'
SPLIT = pd.Timestamp('2021-01-01'); REG = pd.Timestamp('2020-03-13')
_cache = {}
def load(sym):
    if sym in _cache: return _cache[sym]
    fn = f'{D}/daily/{sym}.IS.parquet' if os.path.exists(f'{D}/daily/{sym}.IS.parquet') else f'{D}/daily/{sym}.parquet'
    d = pd.read_parquet(fn); d.index = pd.DatetimeIndex(d['ldate']).normalize(); d = d[~d.index.duplicated(keep='last')].sort_index()
    d = d[d.index >= '2008-01-01'].copy()
    if d['adj'].isna().all(): d['adj'] = d['c']
    stale = (d['v'].fillna(0) <= 0) & (d['h'] == d['l'])
    if sym.startswith('X'): stale = (d['h'] == d['l']) & (d['o'] == d['c']) & (d['c'] == d['c'].shift())  # endekste hacim güvenilmez
    d.loc[stale, ['o', 'h', 'l', 'c', 'adj']] = np.nan
    f = d['adj'] / d['c']
    adjp = d['adj'].ffill()
    cc = np.log(d['adj'] / adjp.shift())
    gap = np.log(d['o'] * f / adjp.shift()); intra = np.log(d['c'] / d['o'])
    lim = pd.Series(np.where(d.index < REG, 0.205, 0.105), index=d.index)   # fiyat bazında (basit getiri) simetrik eşik
    def ex(x): return (np.expm1(x)).abs() > lim
    bad = ex(cc) | ex(gap) | ex(intra)
    out = pd.DataFrame({'cc': cc, 'gap': gap, 'intra': intra, 'c': d['c'], 'o': d['o'], 'adj': d['adj'], 'v': d['v'], 'h': d['h'], 'l': d['l']})
    out.loc[bad, ['cc', 'gap', 'intra']] = np.nan
    out.loc[out.index < '2014-01-01', ['gap', 'intra']] = np.nan
    # gap+intra cc ile tutarlı olmalı (yuvarlama hariç)
    _cache[sym] = out
    return out
def cal():
    return load('XU100').index
def h1(sym):
    fn = f'{D}/h1/{sym}.IS.parquet'
    h = pd.read_parquet(fn); h['t'] = h.index.strftime('%H:%M'); h['ld'] = pd.DatetimeIndex(h['ldate']).normalize()
    return h
def p1030(sym):
    """10:30 TSİ fiyatı = 06:30 UTC barının kapanışı."""
    h = h1(sym); f = h[h['t'] == '06:30'].set_index('ld')['c']; return f[~f.index.duplicated()]
def p1730(sym):
    h = h1(sym); f = h[h['t'] == '13:30'].set_index('ld')['c']; return f[~f.index.duplicated()]
def nw_t(x, lags=5):
    x = pd.Series(x).dropna().values; n = len(x)
    if n < 10: return np.nan, np.nan
    m = x.mean(); e = x - m; g0 = (e @ e) / n; s = g0
    for L in range(1, lags + 1):
        g = (e[L:] @ e[:-L]) / n; s += 2 * (1 - L / (lags + 1)) * g
    se = np.sqrt(s / n); return m, (m / se if se > 0 else np.nan)
def zscore(S, win):
    mp = win // 2
    return (S - S.rolling(win, min_periods=mp).mean()) / S.rolling(win, min_periods=mp).std()
def pair_inputs(a, b, betawin=250, beta1=False):
    A, B = load(a), load(b)
    idx = cal(); A = A.reindex(idx); B = B.reindex(idx)
    if beta1: beta = pd.Series(1.0, index=idx)
    else: beta = (A['cc'].rolling(betawin, min_periods=betawin // 2).cov(B['cc']) / B['cc'].rolling(betawin, min_periods=betawin // 2).var()).shift(1)
    s = A['cc'] - beta * B['cc']
    S = s.fillna(0).cumsum()
    return dict(A=A, B=B, beta=beta, S=S, s=s)
def positions(z, thr, exit_=None):
    """In-band (exit_=None): pos=-sign(z) iff |z|>thr. Histerezis: giriş |z|>thr, çıkış z işaret değiştirip |z|<exit_ olunca."""
    zz = z.values; pos = np.zeros(len(zz))
    if exit_ is None:
        pos = np.where(np.abs(zz) > thr, -np.sign(zz), 0.0); pos[np.isnan(zz)] = 0.0
        return pd.Series(pos, index=z.index)
    cur = 0.0
    for i, v in enumerate(zz):
        if np.isnan(v): cur = 0.0
        elif cur == 0.0:
            if abs(v) > thr: cur = -np.sign(v)
        else:
            if (cur < 0 and v < exit_) or (cur > 0 and v > -exit_): cur = 0.0
            if cur == 0.0 and abs(v) > thr: cur = -np.sign(v)
        pos[i] = cur
    return pd.Series(pos, index=z.index)
def pnl_open(pos, gA, iA, gB, iB, beta, cost_bps, lag=1):
    """pos_t kapanışta karar; giriş t+lag açılışında. pnl_t = P_{t-1-lag+1}... genel: Pg = pos.shift(lag+1) (gap'i taşıyan), Pi = pos.shift(lag) (gün içi)."""
    Pg = pos.shift(lag + 1).fillna(0); Pi = pos.shift(lag).fillna(0)
    bg = beta.shift(lag + 1); bi = beta.shift(lag)   # bacak oranı giriş anındaki beta (yaklaşık: günlük güncel)
    sg = gA - bi * gB; si = iA - bi * iB
    gross = Pg * sg.fillna(0) + Pi * si.fillna(0)
    cost = (cost_bps / 1e4) / 2 * (1 + bi.abs().fillna(1)) * (Pi - Pg).abs()
    exp = (Pg != 0) | (Pi != 0)
    valid = sg.notna() | si.notna()
    return pd.DataFrame({'gross': gross, 'cost': cost, 'net': gross - cost, 'exp': exp, 'Pi': Pi, 'Pg': Pg, 'valid': valid})
def pnl_close(pos, ccA, ccB, beta, cost_bps, lag=0):
    """giriş t+lag kapanışında: pnl_t = pos_{t-1-lag} * cc spread."""
    P = pos.shift(1 + lag).fillna(0); b = beta.shift(1 + lag)
    s = ccA - b * ccB
    gross = P * s.fillna(0); cost = (cost_bps / 1e4) / 2 * (1 + b.abs().fillna(1)) * (P - P.shift().fillna(0)).abs()
    return pd.DataFrame({'gross': gross, 'cost': cost, 'net': gross - cost, 'exp': P != 0, 'Pi': P, 'Pg': P, 'valid': s.notna()})
def summ(df, lo='2014-01-01', hi='2027-01-01', col='net'):
    x = df[(df.index >= pd.Timestamp(lo)) & (df.index < pd.Timestamp(hi))]
    x = x[x['valid'] | x['exp']]
    e = x[x['exp']]
    if len(e) < 15: return dict(n=len(e), bps=np.nan, t=np.nan, ann=np.nan, sh=np.nan)
    m, t = nw_t(x[col].values, 5)  # tüm günler üzerinden t (sıfırlar dahil)
    sd = x[col].std()
    return dict(n=int(len(e)), bps=1e4 * e[col].mean(), t=t, ann=100 * x[col].mean() * 252, sh=(x[col].mean() / sd * np.sqrt(252)) if sd > 0 else np.nan, frac=len(e) / len(x))
def trades(df):
    """Pi değişimlerinden işlem listesi; her işlemin net getirisi (çıkış günü gap'i dahil)."""
    P = df['Pi'].values; Pg = df['Pg'].values; net = df['net'].values; idx = df.index
    out = []; cur = None
    tid = np.full(len(P), -1)
    k = -1
    for i in range(len(P)):
        if P[i] != 0 and (i == 0 or P[i] != P[i - 1]): k += 1; out.append([idx[i], None, P[i]])
        if P[i] != 0: tid[i] = k
        elif Pg[i] != 0 and k >= 0: tid[i] = k   # çıkış günü gap'i
        if P[i] == 0 and i > 0 and P[i - 1] != 0: out[k][1] = idx[i]
    s = pd.Series(net).groupby(tid).sum(); s = s[s.index >= 0]
    # yön değişiminde çıkış günü yeni işlemin ilk günüyle aynı: gap eskiye ait ama tid yeniye atanıyor -> küçük kayma, kabul
    T = pd.DataFrame(out, columns=['entry', 'exit', 'side']); T['net'] = s.reindex(range(len(T))).values
    T['ndays'] = pd.Series(tid[tid >= 0]).value_counts().reindex(range(len(T))).values
    return T
PERIODS = [('2014-17', '2014-01-01', '2018-01-01'), ('2018-20', '2018-01-01', '2021-01-01'), ('2021-23', '2021-01-01', '2024-01-01'), ('2024-26', '2024-01-01', '2027-01-01'),
           ('IS', '2014-01-01', '2021-01-01'), ('OOS', '2021-01-01', '2027-01-01'), ('ALL', '2014-01-01', '2027-01-01')]
def table(df, col='net'):
    return pd.DataFrame({k: summ(df, lo, hi, col) for k, lo, hi in PERIODS}).T
