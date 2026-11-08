"""Bağımsız yeniden üretim kütüphanesi (a5_esz_artik iddiaları). lib_altin.py / a5_lib.py KULLANILMAZ.
Ham kaynaklar: panel/viop_long.parquet (VİOP bülten satırları), panel/duka/<SYM>.parquet (Dukascopy BID saatlik, index = bar başlangıcı UTC).
Fiyat anı HH:00 UTC = başlangıcı (HH-1):00 olan barın kapanışı (yani HH-1:59:59 UTC).
"""
import numpy as np, pandas as pd

S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
P = f"{S}/panel"
OUT = f"{S}/out/a5_esz_artik_rep"
IS_END = pd.Timestamp("2021-12-31")


# ---------------- VİOP hedefi (ham bültenden) ----------------
def viop_active(root="XAUUSD"):
    v = pd.read_parquet(f"{P}/viop_long.parquet")
    v = v[v.root.astype(str) == root].copy()
    v["date"] = pd.to_datetime(v.date)
    st = v.pivot_table(index="date", columns="code", values="settle", aggfunc="last")
    ps = v.pivot_table(index="date", columns="code", values="prev_settle", aggfunc="last")
    oi = v.pivot_table(index="date", columns="code", values="oi", aggfunc="last")
    vol = v.pivot_table(index="date", columns="code", values="volume", aggfunc="last")
    dates = st.index
    act = []
    for i, d in enumerate(dates):
        present = st.loc[d].dropna().index
        if i == 0:
            o = oi.loc[d, present]
        else:
            o = oi.loc[dates[i - 1]].reindex(present).fillna(-1)  # önceki günün OI'si (ileriye bakmasız)
        act.append(o.idxmax())
    act = pd.Series(act, index=dates, name="code")
    s = np.array([st.at[d, c] for d, c in act.items()])
    p = np.array([ps.at[d, c] for d, c in act.items()])
    # tutarlılık: prev_settle == aynı kontratın bir önceki gün uzlaşması mı?
    prev_own = np.array([st[c].shift(1).at[d] for d, c in act.items()])
    out = pd.DataFrame(dict(code=act, settle=s, prev_settle=p, prev_own=prev_own,
                            volume=[vol.at[d, c] for d, c in act.items()]), index=dates)
    out["ret"] = np.log(out.settle / out.prev_settle)
    return out


def fwd_sum(r, h):
    """t+1..t+h toplamı (t satırında)."""
    a = np.column_stack([r.shift(-k).values for k in range(1, h + 1)])
    return pd.Series(a.sum(1), index=r.index).where(np.isfinite(a).all(1))


# ---------------- Dukascopy saatlik görüntüler ----------------
_HCACHE = {}


def hourly(sym):
    if sym not in _HCACHE:
        h = pd.read_parquet(f"{P}/duka/{sym}.parquet")
        h.index = h.index.tz_convert("UTC").tz_localize(None)
        _HCACHE[sym] = h
    return _HCACHE[sym]


def snap(sym, HH):
    """Gün d için HH:00 UTC fiyatı = başlangıcı d+(HH-1)h olan barın kapanışı; tam bar yoksa NaN (ffill YOK)."""
    h = hourly(sym)
    c = h["c"][h.index.hour == HH - 1]
    c.index = c.index.normalize()
    return c[~c.index.duplicated()]


# ---------------- İstatistik ----------------
def nw_t(y, x, L, correction=True):
    """y = a + b x OLS, Newey-West (Bartlett, maxlag L) t(b). Kendi uygulamam."""
    y = np.asarray(y, float); x = np.asarray(x, float); n = len(y)
    X = np.column_stack([np.ones(n), x])
    XtX_inv = np.linalg.inv(X.T @ X)
    b = XtX_inv @ X.T @ y
    u = y - X @ b
    Z = X * u[:, None]
    Sm = Z.T @ Z
    for j in range(1, L + 1):
        w = 1 - j / (L + 1)
        G = Z[j:].T @ Z[:-j]
        Sm += w * (G + G.T)
    V = XtX_inv @ Sm @ XtX_inv
    if correction:
        V *= n / (n - 2)
    return b[1] / np.sqrt(V[1, 1])


def ic_t(x, y, L, method="spearman"):
    d = pd.concat([pd.Series(x, name="x"), pd.Series(y, name="y")], axis=1).dropna()
    n = len(d)
    if n < 30:
        return dict(ic=np.nan, t=np.nan, n=n)
    if method == "spearman":
        d = d.rank()
    c = np.corrcoef(d.x, d.y)[0, 1]
    zx = (d.x - d.x.mean()) / d.x.std(); zy = (d.y - d.y.mean()) / d.y.std()
    return dict(ic=c, t=nw_t(zy.values, zx.values, L), n=n)


def stats(x, y, h, method="spearman", L=None):
    L = L if L is not None else max(h, 5)
    x = pd.Series(x); y = pd.Series(y)
    f = ic_t(x, y, L, method)
    i = ic_t(x[x.index <= IS_END], y[y.index <= IS_END], L, method)
    o = ic_t(x[x.index > IS_END], y[y.index > IS_END], L, method)
    d = pd.concat([x.rename("x"), y.rename("y")], axis=1).dropna()
    yr = d.groupby(d.index.year).apply(lambda g: g.x.corr(g.y, method=method) if len(g) > 20 else np.nan)
    same = int((np.sign(yr.dropna()) == np.sign(f["ic"])).sum())
    return dict(ic=f["ic"], t=f["t"], n=f["n"], ic_is=i["ic"], t_is=i["t"], n_is=i["n"], ic_oos=o["ic"], t_oos=o["t"], n_oos=o["n"],
                yrs=f"{same}/{int(yr.notna().sum())}", by_year=yr.round(3).to_dict())


# ---------------- Backtest (kendi uygulamam) ----------------
def bt(pos, ret, h, cost_bps=5.0, demean=False):
    """Kademeli h alt portföy: gün t uzlaşmasında sermayenin 1/h'i ile pos_t açılır, t+h uzlaşmasında kapanır.
    Gün t+1 portföy getirisi = (1/h) Σ_{k=0..h-1} pos_{t-k} · r_{t+1}. Maliyet: alt portföy j'de pozisyon değişimi |pos_t - pos_{t-h}|/h × (cost/2),
    gün t kapanışında ödenir (t+1 getirisinden düşülür). Gidiş-dönüş = cost_bps."""
    r = ret.astype(float).copy()
    if demean:
        r = r - r.mean()
    p = pos.reindex(r.index).fillna(0.0).clip(-1, 1)
    eff = sum(p.shift(k).fillna(0.0) for k in range(h)) / h
    dpos = (eff - eff.shift(1).fillna(0.0)).abs()
    net = eff.shift(1).fillna(0.0) * r - dpos.shift(1).fillna(0.0) * cost_bps / 2e4
    net = net.iloc[1:]
    mu = net.mean(); sd = net.std()
    return dict(sr=mu / sd * np.sqrt(252) if sd > 0 else np.nan, ann=mu * 252, t=mu / (sd / np.sqrt(len(net))), n=len(net),
                expo=eff.abs().mean(), turn=dpos.sum() / len(net) * 252, pnl=net)


def bt_split(pos, ret, h, cost_bps=5.0):
    out = {}
    for nm, m in [("full", slice(None)), ("is", ret.index <= IS_END), ("oos", ret.index > IS_END)]:
        rr = ret[m]; pp = pos.reindex(rr.index)
        a = bt(pp, rr, h, cost_bps); a10 = bt(pp, rr, h, 2 * cost_bps); dm = bt(pp, rr, h, cost_bps, demean=True)
        lg = bt(pp.clip(lower=0), rr, h, cost_bps); sh = bt(pp.clip(upper=0), rr, h, cost_bps)
        lgd = bt(pp.clip(lower=0), rr, h, cost_bps, demean=True); shd = bt(pp.clip(upper=0), rr, h, cost_bps, demean=True)
        bh = bt(pd.Series(1.0, index=rr.index), rr, 1, 0.0)
        out[nm] = dict(sr=a["sr"], sr10=a10["sr"], sr_dm=dm["sr"], ann=a["ann"], t_pnl=a["t"], long=lg["sr"], long_dm=lgd["sr"],
                       short=sh["sr"], short_dm=shd["sr"], bh=bh["sr"], turn=a["turn"], expo=a["expo"])
    return out


def rolling_ols(y, X, W, minp=None):
    """y_t = a + b'X_t + e_t; (a,b) yalnız [t-W, t-1] satırlarından (tam gözlem, en az minp). σ_e ddof = p+1."""
    minp = minp or int(0.8 * W)
    X = pd.DataFrame(X)
    Y = y.values.astype(float); Xv = X.values.astype(float)
    n, p = Xv.shape
    ok = np.isfinite(Y) & np.isfinite(Xv).all(1)
    e = np.full(n, np.nan); fit = np.full(n, np.nan); sig = np.full(n, np.nan)
    for t in range(n):
        if not ok[t]:
            continue
        lo = max(0, t - W)
        idx = np.arange(lo, t)[ok[lo:t]]
        if len(idx) < minp:
            continue
        A = np.column_stack([np.ones(len(idx)), Xv[idx]])
        coef = np.linalg.lstsq(A, Y[idx], rcond=None)[0]
        res = Y[idx] - A @ coef
        sig[t] = np.sqrt((res ** 2).sum() / (len(idx) - (p + 1)))
        fit[t] = Xv[t] @ coef[1:]
        e[t] = Y[t] - coef[0] - fit[t]
    return pd.DataFrame(dict(e=e, fit=fit, sig=sig), index=y.index)
