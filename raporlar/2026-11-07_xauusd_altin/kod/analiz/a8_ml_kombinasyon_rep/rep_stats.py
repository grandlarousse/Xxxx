"""Bağımsız istatistik araçları (lib_altin'den bağımsız yazıldı).
 - nw_se_mean: Bartlett çekirdekli Newey-West ortalama standart hatası (küçük örnek düzeltmesi yok).
 - ic_test: Spearman IC; t = rank-z(y) ~ rank-z(x) OLS eğimi, NW (Bartlett, lag L) HAC.
 - bt: kademeli (h alt portföy) geri test, tek yön maliyet = cost/2 × |Δ etkin pozisyon|.
"""
import numpy as np, pandas as pd

IS_END = pd.Timestamp("2021-12-31")


def nw_var_sum(u, L):
    """sum_t u_t için NW varyansı (Bartlett), u ortalaması sıfır varsayılır (skor)."""
    u = np.asarray(u, float); n = len(u)
    g0 = u @ u
    s = g0
    for k in range(1, L + 1):
        w = 1 - k / (L + 1)
        s += 2 * w * (u[k:] @ u[:-k])
    return s


def nw_t_mean(x, L):
    x = pd.Series(x).dropna().values
    if len(x) < 30: return np.nan
    m = x.mean(); u = x - m
    v = nw_var_sum(u, L) / len(x) ** 2
    return m / np.sqrt(v)


def ols_nw_t(y, x, L):
    """y = a + b x; NW HAC t(b)."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    xc = x - x.mean(); b = (xc @ (y - y.mean())) / (xc @ xc)
    a = y.mean() - b * x.mean(); e = y - a - b * x
    sc = xc * e
    vb = nw_var_sum(sc, L) / (xc @ xc) ** 2
    return b, b / np.sqrt(vb)


def ic_test(x, y, L=5):
    d = pd.concat([pd.Series(x, name="x"), pd.Series(y, name="y")], axis=1).dropna()
    if len(d) < 30: return dict(ic=np.nan, t=np.nan, n=len(d))
    r = d.rank()
    ic = float(np.corrcoef(r.x, r.y)[0, 1])
    _, t = ols_nw_t(r.y.values, r.x.values, L)
    return dict(ic=ic, t=float(t), n=len(d))


def split_ic(x, y, h, is_end=IS_END):
    L = max(h, 5)
    x = pd.Series(x); y = pd.Series(y)
    f = ic_test(x, y, L)
    i = ic_test(x[x.index <= is_end], y[y.index <= is_end], L)
    o = ic_test(x[x.index > is_end], y[y.index > is_end], L)
    d = pd.concat([x.rename("x"), y.rename("y")], axis=1).dropna()
    yr = d.groupby(d.index.year).apply(lambda g: g.x.rank().corr(g.y.rank()) if len(g) > 20 else np.nan)
    same = int((np.sign(yr) == np.sign(f["ic"])).sum())
    return dict(ic=f["ic"], t=f["t"], n=f["n"], ic_is=i["ic"], t_is=i["t"], ic_oos=o["ic"], t_oos=o["t"], yrs=f"{same}/{int(yr.notna().sum())}", by_year=yr.round(3).to_dict())


def bt(pos, ret, h, cost_bps=5.0, demean=False):
    """pos_t: gün t uzlaşmasında açılan pozisyon (−1..1), h gün tutulur; her gün sermayenin 1/h'i.
    pnl_{t+1} = eff_t · r_{t+1} − |eff_t − eff_{t−1}| · cost/2 (eff_t = ortalama pos_{t..t−h+1})."""
    r = pd.Series(ret).dropna().astype(float)
    if demean: r = r - r.mean()
    p = pd.Series(pos).reindex(r.index).fillna(0.0).clip(-1, 1)
    eff = p.rolling(h, min_periods=1).sum() / h  # ilk h-1 günde eksik alt portföy = 0
    gross = eff.shift(1) * r
    tc = (eff - eff.shift(1).fillna(0.0)).abs().shift(1).fillna(0.0) * cost_bps / 2 / 1e4
    net = (gross - tc).iloc[1:]
    if len(net) < 50: return None
    mu, sd = net.mean(), net.std()
    turn = (eff - eff.shift(1).fillna(0.0)).abs()
    return dict(sharpe=float(mu / sd * np.sqrt(252)) if sd > 0 else np.nan, ann=float(mu * 252), vol=float(sd * np.sqrt(252)),
                turnover=float(turn.iloc[1:].sum() / len(net) * 252), exposure=float(eff.abs().mean()), n=len(net), pnl=net,
                flips_per_yr=float((p.diff().abs() > 0).sum() / len(net) * 252))


def bt_full(pos, ret, h, cost=5.0):
    a = bt(pos, ret, h, cost); b = bt(pos, ret, h, cost, demean=True)
    lo = bt(pd.Series(pos).clip(lower=0), ret, h, cost); sh = bt(pd.Series(pos).clip(upper=0), ret, h, cost)
    bh = bt(pd.Series(1.0, index=pd.Series(ret).dropna().index), ret, 1, 0.0)
    c10 = bt(pos, ret, h, 10.0)
    g = lambda z: round(z["sharpe"], 3) if z else np.nan
    return dict(sh=g(a), sh_dm=g(b), long=g(lo), short=g(sh), bh=g(bh), sh10=g(c10), turn=round(a["turnover"], 1) if a else np.nan,
                ann=round(a["ann"], 4) if a else np.nan)
