"""v_YR1_a bağımsız doğrulama kütüphanesi (ll.py KULLANILMAZ).
Temizlik kuralları (görev metni):
- index = ldate (yerel tarih), tekrarlar atılır, son gün 2026-10-30.
- bayat gün: hacim<=0 VE h==l -> satır atılır (hacim serisi anlamlıysa).
- kurumsal işlem/veri hatası: 2020-03-13 öncesi cc log getirisi > ln1,205 veya < ln0,795; sonrası > ln1,105 veya < ln0,895 -> NaN.
- açılış: 2014 öncesi gap/intra NaN; o<=0 veya (h==l ve o==önceki c) -> NaN.
- cc = log(adj_t/adj_{t-1}) (temettü dahil); intra = log(c/o); gap = cc - intra.
"""
import numpy as np, pandas as pd, os, warnings
warnings.filterwarnings('ignore')
SCR = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad'
DATA = SCR + '/data'; OUT = SCR + '/out'; HERE = OUT + '/code_v_YR1_a'
LAST = pd.Timestamp('2026-10-30'); SPLIT = pd.Timestamp('2021-01-01'); RS = pd.Timestamp('2020-03-13')
_c = {}

def raw(sym):
    s = sym if sym.endswith('.IS') else sym + '.IS'
    if s not in _c:
        d = pd.read_parquet(f'{DATA}/daily/{s}.parquet')
        d.index = pd.DatetimeIndex(pd.to_datetime(d['ldate']).values)
        d = d[~d.index.duplicated(keep='last')].sort_index()
        d = d[d.index <= LAST]
        if (d['v'].fillna(0) > 0).mean() > 0.5:
            d = d[~((d['v'].fillna(0) <= 0) & (d['h'] == d['l']))]
        _c[s] = d
    return _c[s]

def bad(r):
    pre = r.index < RS
    up = np.where(pre, np.log(1.205), np.log(1.105)); dn = np.where(pre, np.log(0.795), np.log(0.895))
    return (r > up) | (r < dn)

def dec(sym):
    d = raw(sym)
    cc = np.log(d['adj']).diff()
    intra = np.log(d['c'] / d['o'])
    bo = (d['o'] <= 0) | d['o'].isna() | ((d['h'] == d['l']) & (d['o'] == d['c'].shift(1)))
    intra[bo] = np.nan
    gap = cc - intra
    out = pd.DataFrame({'cc': cc, 'gap': gap, 'intra': intra, 'px': d['c']})
    b = bad(out['cc']); out.loc[b, ['cc', 'gap', 'intra']] = np.nan
    out.loc[out.index < pd.Timestamp('2014-01-01'), ['gap', 'intra']] = np.nan
    bg = bad(out['gap'].fillna(0)); out.loc[bg, ['gap', 'intra']] = np.nan
    return out

def h1_px(sym, hhmm_end='07:30'):
    """Saatlik barlardan, bar BİTİŞ anı hhmm_end (UTC) olan barın kapanışı. 06:30 barı 07:30 UTC = 10:30 TSİ'de biter."""
    s = sym if sym.endswith('.IS') else sym + '.IS'
    h = pd.read_parquet(f'{DATA}/h1/{s}.parquet')
    h = h[~h.index.duplicated(keep='last')]
    start = pd.Timedelta(hours=int(hhmm_end[:2]), minutes=int(hhmm_end[3:])) - pd.Timedelta(hours=1)
    tod = h.index - h.index.normalize()
    x = h[tod == start]
    out = pd.Series(x['c'].values, index=pd.DatetimeIndex(x.index.tz_convert(None).normalize()))
    out = out[out.index <= LAST]
    return out[~out.index.duplicated(keep='last')]

def roll_beta(a, b, w=250, mp=120):
    df = pd.concat([a, b], axis=1)
    return (df.iloc[:, 0].rolling(w, min_periods=mp).cov(df.iloc[:, 1]) / df.iloc[:, 1].rolling(w, min_periods=mp).var()).shift(1)

def zscore(S, w, mp=None):
    mp = mp or w // 2
    return (S - S.rolling(w, min_periods=mp).mean()) / S.rolling(w, min_periods=mp).std()

def nwt(x, lags=5):
    x = pd.Series(x).dropna().values; n = len(x)
    if n < 20: return np.nan, np.nan, n
    m = x.mean(); e = x - m
    g0 = (e @ e) / n; s = g0
    for L in range(1, lags + 1):
        g = (e[L:] @ e[:-L]) / n; s += 2 * (1 - L / (lags + 1)) * g
    se = np.sqrt(s / n)
    return m, m / se if se > 0 else np.nan, n

def positions(z, thr, mode='band', exit_thr=None):
    """Kapanış t'de bilinen z_t -> pozisyon kararı pos_t. band: |z|>thr iken -sign(z), aksi 0 (kaynak tanımı).
    hyst: |z|>thr'de gir, z işaret değiştirene/|z|<exit_thr olana kadar tut."""
    z = z.copy()
    if mode == 'band':
        return (-np.sign(z)).where(z.abs() > thr, 0.0).fillna(0.0)
    p = np.zeros(len(z)); cur = 0.0; zv = z.values
    ex = 0.0 if exit_thr is None else exit_thr
    for i, v in enumerate(zv):
        if np.isnan(v): p[i] = cur; continue
        if cur == 0 and abs(v) > thr: cur = -np.sign(v)
        elif cur != 0 and ((cur < 0 and v < ex) or (cur > 0 and v > -ex)): cur = 0.0
        if cur == 0 and abs(v) > thr: cur = -np.sign(v)
        p[i] = cur
    return pd.Series(p, index=z.index)

def simulate(pos, gap, intra, cc, legw, entry='open', cost_rt=8.0, tick_rt=None):
    """pos_t: kapanış t'de karar. legw: toplam nominal (1+|beta|) – maliyet ölçeği.
    entry: 'open' (t+1 açılış), 'close0' (aynı gün kapanış ~ VİOP 18:10-18:15; iyimser), 'close1' (t+1 kapanış; muhafazakâr).
    gap/intra burada '10:30 girişi' için yeniden tanımlanmış seriler de olabilir.
    cost_rt: bacak başına gidiş-dönüş bps (nominal ağırlıklı). tick_rt: ek tik maliyeti (bps, gidiş-dönüş, toplam nominal ağırlıklı seri).
    Dönüş: DataFrame(pnl, gross, cost, expo) – expo: o gün pozisyon riski var mı."""
    idx = gap.index
    p = pos.reindex(idx).fillna(0.0)
    p1, p2 = p.shift(1).fillna(0), p.shift(2).fillna(0)
    lw = legw.reindex(idx).ffill().fillna(2.0)
    tk = (tick_rt.reindex(idx).ffill().fillna(0) if tick_rt is not None else 0.0)
    per_side = (cost_rt / 1e4) / 2 * lw + (tk / 1e4) / 2
    if entry == 'open':
        gross = p2 * gap.fillna(0) + p1 * intra.fillna(0); trade = (p1 - p2).abs(); expo = (p1 != 0) | (p2 != 0)
    elif entry == 'close0':
        gross = p1 * cc.fillna(0); trade = (p - p1).abs(); expo = (p1 != 0)
    elif entry == 'close1':
        gross = p2 * cc.fillna(0); trade = (p1 - p2).abs(); expo = (p2 != 0)
    else:
        raise ValueError(entry)
    cost = trade * per_side
    return pd.DataFrame({'pnl': gross - cost, 'gross': gross, 'cost': cost, 'expo': expo, 'trade': trade, 'p1': p1, 'act_p1': (p1 != 0) if entry != 'close1' else (p2 != 0)})

def summarize(sim, lo='2014-01-01', hi='2027-01-01', active='expo'):
    s = sim[(sim.index >= pd.Timestamp(lo)) & (sim.index < pd.Timestamp(hi))]
    a = s[s[active]] if active else s
    m, t, n = nwt(a['pnl'])
    mall, tall, nall = nwt(s['pnl'])
    sd = s['pnl'].std()
    entries = int(((s['p1'] != 0) & (s['p1'].shift(1).fillna(0) != s['p1'])).sum())
    return dict(n_act=int(n), mean_bps=1e4 * m if n else np.nan, t_act=t, t_all=tall, gross_bps=1e4 * a['gross'].mean() if n else np.nan,
                cost_bps=1e4 * a['cost'].mean() if n else np.nan, sharpe=(s['pnl'].mean() / sd * np.sqrt(252)) if sd > 0 else np.nan,
                ann_pct=100 * s['pnl'].mean() * 252, pct_in=float(s[active].mean()) if active else 1.0, entries=entries,
                hold_d=(n / entries) if entries else np.nan, hit=float((a['pnl'] > 0).mean()) if n else np.nan)

def by_year(sim, active='expo'):
    a = sim[sim[active]] if active else sim
    return (1e4 * a['pnl'].groupby(a.index.year).mean()).round(1)
