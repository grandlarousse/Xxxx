"""Bağımsız yeniden üretim kütüphanesi (lib_altin KULLANILMAZ).
Ham tablolar: viop_long.parquet (bülten), duka/*.parquet (saatlik BID, index=bar başlangıcı UTC; fiyat anı=index+1h)."""
import numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
P = f"{S}/panel"
OUT = f"{S}/out/a7_turkiye_rep"
IS_END = pd.Timestamp("2021-12-31")

_V = None
def viop_long():
    global _V
    if _V is None:
        _V = pd.read_parquet(f"{P}/viop_long.parquet")
        _V["date"] = pd.to_datetime(_V["date"]); _V["expiry"] = pd.to_datetime(_V["expiry"])
    return _V

def continuous(root):
    """Aktif kontrat_t = (t-1 günü OI'si en büyük) VE t günü bültende olan kontrat. ret_t = ln(settle_t/settle_{t-1}) aynı kontratta
    (önceki gün settle'ı kendi tablomdan; bülten prev_settle ile ayrıca karşılaştırılır)."""
    d = viop_long(); d = d[d.root == root]
    st = d.pivot_table(index="date", columns="code", values="settle", aggfunc="first")
    ps = d.pivot_table(index="date", columns="code", values="prev_settle", aggfunc="first")
    oi = d.pivot_table(index="date", columns="code", values="oi", aggfunc="first")
    vol = d.pivot_table(index="date", columns="code", values="volume", aggfunc="first")
    exp = d.groupby("code").expiry.first()
    dates = st.index
    rows = []
    for i, t in enumerate(dates):
        today = st.loc[t].dropna().index
        if i == 0:
            act = vol.loc[t, today].idxmax()
        else:
            o = oi.iloc[i - 1][today].dropna()
            act = o.idxmax() if len(o) and o.max() > 0 else vol.loc[t, today].idxmax()
        s_t = st.loc[t, act]
        s_prev = st.iloc[i - 1][act] if i > 0 else np.nan
        rows.append(dict(date=t, code=act, expiry=exp[act], settle=s_t, settle_prev_own=s_prev, prev_settle_bull=ps.loc[t, act],
                         ret=np.log(s_t / s_prev) if (i > 0 and s_prev > 0 and s_t > 0) else np.nan,
                         oi=oi.loc[t, act], volume=vol.loc[t, act], dte=(exp[act] - t).days))
    return pd.DataFrame(rows).set_index("date")

def duka_at(sym, days, hour, max_stale_h=1):
    """Gün d için d hour:00 UTC'de bilinen son bar kapanışı (bar_start+1h <= d hour:00, en fazla max_stale_h eski)."""
    h = pd.read_parquet(f"{P}/duka/{sym}.parquet")
    t_px = (h.index + pd.Timedelta(hours=1)).tz_convert(None)
    s = pd.Series(h["c"].values, index=t_px).sort_index()
    targ = pd.DatetimeIndex(days) + pd.Timedelta(hours=hour)
    pos = s.index.searchsorted(targ, side="right") - 1
    vals = np.where(pos >= 0, s.values[np.clip(pos, 0, None)], np.nan)
    ts = s.index.values[np.clip(pos, 0, None)]
    stale = (targ.values - ts) / np.timedelta64(1, "h")
    out = pd.Series(np.where((pos >= 0) & (stale <= max_stale_h), vals, np.nan), index=pd.DatetimeIndex(days))
    stamp = pd.Series(np.where(pos >= 0, ts, np.datetime64("NaT")), index=pd.DatetimeIndex(days))
    return out, stamp

def fwdsum(r, h):
    a = np.column_stack([r.shift(-k).values for k in range(1, h + 1)])
    return pd.Series(a.sum(axis=1), index=r.index)  # herhangi biri NaN ise NaN

def nw_slope_t(y, x, L):
    """OLS y=a+bx, Newey-West (Bartlett, maxlag L) t of b, with n/(n-k) small-sample düzeltmesi."""
    y = np.asarray(y, float); x = np.asarray(x, float); n = len(y)
    X = np.column_stack([np.ones(n), x])
    XtX_inv = np.linalg.inv(X.T @ X)
    b = XtX_inv @ X.T @ y
    e = y - X @ b
    u = X * e[:, None]
    Sm = u.T @ u
    for l in range(1, L + 1):
        w = 1 - l / (L + 1)
        G = u[l:].T @ u[:-l]
        Sm += w * (G + G.T)
    V = XtX_inv @ Sm @ XtX_inv * n / (n - 2)
    return b[1], b[1] / np.sqrt(V[1, 1])

def ic(x, y, h, mask=None):
    d = pd.concat([pd.Series(x, name="x"), pd.Series(y, name="y")], axis=1)
    if mask is not None: d = d[mask]
    d = d.dropna()
    if len(d) < 30: return dict(ic=np.nan, t=np.nan, n=len(d))
    rk = d.rank()
    c = rk.x.corr(rk.y)
    zx = (rk.x - rk.x.mean()) / rk.x.std(); zy = (rk.y - rk.y.mean()) / rk.y.std()
    _, t = nw_slope_t(zy.values, zx.values, max(h, 5))
    return dict(ic=c, t=t, n=len(d))

def ic_split(x, y, h):
    idx = pd.Series(x).index
    full = ic(x, y, h); is_ = ic(x, y, h, idx <= IS_END); oos = ic(x, y, h, idx > IS_END)
    d = pd.concat([pd.Series(x, name="x"), pd.Series(y, name="y")], axis=1).dropna()
    yr = d.groupby(d.index.year).apply(lambda g: g.x.rank().corr(g.y.rank()) if len(g) > 20 else np.nan)
    same = int((np.sign(yr) == np.sign(full["ic"])).sum())
    return dict(ic=full["ic"], t=full["t"], n=full["n"], ic_is=is_["ic"], t_is=is_["t"], ic_oos=oos["ic"], t_oos=oos["t"], yrs=f"{same}/{int(yr.notna().sum())}", by_year=yr.round(3).to_dict())

def bt(pos, ret, h, cost_bps, demean=False):
    """Kademeli: her gün 1/h sermaye ile pos_t açılır (t uzlaşması), h gün tutulur. eff_t = ort(pos_t..pos_{t-h+1}).
    pnl_{t+1} = eff_t*ret_{t+1} - |eff_t - eff_{t-1}| * cost/2 (tek yön). Ayrıca netleştirmesiz maliyet: sum_k |pos_{t-k} değişimi| / h."""
    r = ret.astype(float).copy()
    if demean: r = r - r.mean()
    pos = pos.reindex(r.index).fillna(0.0).clip(-1, 1)
    eff = sum(pos.shift(k).fillna(0.0) for k in range(h)) / h
    gross = eff.shift(1) * r
    turn = (eff - eff.shift(1).fillna(0.0)).abs()
    net = (gross - turn.shift(1).fillna(0.0) * cost_bps / 2 / 1e4).dropna()
    # netleştirmesiz (her alt portföy kendi açılış+kapanışını öder): açılış |pos_t|, kapanış |pos_{t-h}| -> her gün (|pos_t|+|pos_{t-h}|)/h
    if h > 1:
        gross_turn = (pos.abs() + pos.shift(h).fillna(0).abs()) / h
    else:
        gross_turn = (pos - pos.shift(1).fillna(0)).abs()
    net_nn = (gross - gross_turn.shift(1).fillna(0.0) * cost_bps / 2 / 1e4).dropna()
    def sh(z): return z.mean() / z.std() * np.sqrt(252) if z.std() > 0 else np.nan
    return dict(sharpe=sh(net), sharpe_nonet=sh(net_nn), ann=net.mean() * 252, vol=net.std() * np.sqrt(252),
                t=net.mean() / net.std() * np.sqrt(len(net)), n=len(net), expo=float(eff.abs().mean()), pnl=net, gross_sharpe=sh(gross.dropna()))

def bt_seg(pos, ret, h, cost_bps, demean=False):
    o = {}
    for nm, m in [("full", np.ones(len(ret), bool)), ("is", ret.index <= IS_END), ("oos", ret.index > IS_END)]:
        o[nm] = bt(pos[m], ret[m], h, cost_bps, demean)
    return o
