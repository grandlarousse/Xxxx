"""Bağımsız yardımcılar (lib_altin KULLANILMAZ): NW-HAC t (elle, Bartlett), Spearman/Pearson IC, IS/OOS ayrımı, kademeli backtest."""
import numpy as np, pandas as pd
IS_END = pd.Timestamp("2021-12-31")

def nw_t(y, x, L):
    """y = a + b x + e; Bartlett çekirdekli Newey-West HAC; küçük örneklem düzeltmesi YOK. Döndür (b, t, n)."""
    d = pd.concat([pd.Series(y), pd.Series(x)], axis=1).dropna().values
    if len(d) < 30: return np.nan, np.nan, len(d)
    Y = d[:, 0]; X = np.column_stack([np.ones(len(d)), d[:, 1]])
    XtX_inv = np.linalg.inv(X.T @ X)
    b = XtX_inv @ X.T @ Y
    e = Y - X @ b
    u = X * e[:, None]
    Sm = u.T @ u
    for j in range(1, L + 1):
        w = 1 - j / (L + 1)
        G = u[j:].T @ u[:-j]
        Sm += w * (G + G.T)
    V = XtX_inv @ Sm @ XtX_inv
    return float(b[1]), float(b[1] / np.sqrt(V[1, 1])), len(d)

def ic_t(x, y, L, method="spearman"):
    d = pd.concat([pd.Series(x, name="x"), pd.Series(y, name="y")], axis=1).dropna()
    if len(d) < 30: return dict(ic=np.nan, t=np.nan, n=len(d))
    if method == "spearman": d = d.rank()
    c = float(np.corrcoef(d.x, d.y)[0, 1])
    zx = (d.x - d.x.mean()) / d.x.std(); zy = (d.y - d.y.mean()) / d.y.std()
    _, t, n = nw_t(zy, zx, L)
    return dict(ic=c, t=t, n=n)

def split(x, y, h, method="spearman", is_end=IS_END):
    L = max(h, 5)
    x = pd.Series(x); y = pd.Series(y)
    f = ic_t(x, y, L, method)
    a = ic_t(x[x.index <= is_end], y[y.index <= is_end], L, method)
    o = ic_t(x[x.index > is_end], y[y.index > is_end], L, method)
    d = pd.concat([x.rename("x"), y.rename("y")], axis=1).dropna()
    yr = d.groupby(d.index.year).apply(lambda g: g.x.corr(g.y, method=method) if len(g) > 20 else np.nan)
    same = int((np.sign(yr) == np.sign(f["ic"])).sum())
    return dict(ic=f["ic"], t=f["t"], n=f["n"], ic_is=a["ic"], t_is=a["t"], ic_oos=o["ic"], t_oos=o["t"], yrs=f"{same}/{int(yr.notna().sum())}", by_year=yr.round(3).to_dict())

def bt(pos, ret, h, cost_bps=5.0, demean=False, netting=True, ann=252):
    """Kademeli: her gün t uzlaşmasında pos_t/h açılır, t+h uzlaşmasında kapanır. eff_t = ort(pos_t..pos_{t-h+1}), t→t+1 getirisinde tutulur.
    netting=True: maliyet |Δeff| × c/2 (tek yön). netting=False: her dilim açılış+kapanışta ayrı öder: (|pos_t|+|pos_{t-h}|)/h × c/2."""
    r = ret.astype(float).copy()
    if demean: r = r - r.mean()
    p = pos.reindex(r.index).fillna(0.0).clip(-1, 1)
    eff = p.rolling(h, min_periods=1).sum() / h          # p_t + ... + p_{t-h+1} (başta eksik → 0 sayılır)
    gross = eff.shift(1) * r
    if netting:
        c = (eff - eff.shift(1).fillna(0)).abs() * cost_bps / 2 / 1e4
    else:
        c = (p.abs() + p.shift(h).fillna(0).abs()) / h * cost_bps / 2 / 1e4
    net = (gross - c.shift(1).fillna(0)).iloc[1:]
    mu = net.mean() * ann; sd = net.std() * np.sqrt(ann)
    tt = net.mean() / (net.std() / np.sqrt(len(net)))
    return dict(sharpe=float(mu / sd), ann_ret=float(mu), t_sharpe=float(tt), n=len(net), exposure=float(eff.abs().mean()),
                turnover=float((eff - eff.shift(1).fillna(0)).abs().sum() / len(net) * ann), pnl=net)

def bt_explicit(pos, ret, h, cost_bps=5.0):
    """Açık dilim simülasyonu (çapraz kontrol): her dilim kendi giriş/çıkış uzlaşmasıyla; netleştirme yok."""
    r = ret.astype(float).values; p = pos.reindex(ret.index).fillna(0.0).clip(-1, 1).values; n = len(r)
    pnl = np.zeros(n)
    for t in range(n):
        if p[t] == 0: continue
        w = p[t] / h
        pnl[t] -= abs(w) * cost_bps / 2 / 1e4 if t + 1 < n else 0   # açılış (t uzlaşması) – t+1 pnl'ine yazmak yerine t'ye; Sharpe'ı etkilemez
        for k in range(1, h + 1):
            if t + k < n: pnl[t + k] += w * r[t + k]
        if t + h < n: pnl[t + h] -= abs(w) * cost_bps / 2 / 1e4
    s = pd.Series(pnl, index=ret.index).iloc[1:]
    return float(s.mean() / s.std() * np.sqrt(252))
