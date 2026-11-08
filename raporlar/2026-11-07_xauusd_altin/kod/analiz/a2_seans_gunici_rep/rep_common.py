"""Bağımsız yeniden üretim — ortak araçlar (lib_altin KULLANILMAZ).
Kurallar:
  - Dukascopy saatlik bar index = bar başlangıcı (UTC); fiyat anı T = bar(T-1h) kapanışı.
  - Ekim-Kasım 2026: saatlik dosya 2026-10-30 20:00 barında bitiyor -> dakikalık bi5'ten kendi kod çözücümle saatlik bar.
  - VİOP aktif kontrat: viop_long'dan F_XAUUSD satırları; aktif = ÖNCEKİ gün OI'si en büyük kontrat (ileriye bakmasız).
  - v_ret = log(settle/prev_settle) aktif kontrat içinde. fwd_h(t) = sum_{k=1..h} v_ret(t+k).
  - NW: kendi Bartlett-kernel HAC kodum (numpy).
"""
import os, glob, lzma, struct
import numpy as np, pandas as pd

S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
P = f"{S}/panel"
OUT = f"{S}/out/a2_seans_gunici_rep"
IS_END = pd.Timestamp("2021-12-31")


# ---------------------------------------------------------------- spot fiyatları
def decode_bi5(path, day):
    b = open(path, "rb").read()
    if not b:
        return None
    raw = lzma.decompress(b)
    n = len(raw) // 24
    rec = np.frombuffer(raw[: n * 24], dtype=np.dtype([("t", ">i4"), ("o", ">i4"), ("c", ">i4"), ("l", ">i4"), ("h", ">i4"), ("v", ">f4")]))
    t = day + pd.to_timedelta(rec["t"].astype(np.int64), unit="s")
    df = pd.DataFrame({"o": rec["o"] / 1e3, "c": rec["c"] / 1e3, "l": rec["l"] / 1e3, "h": rec["h"] / 1e3, "v": rec["v"].astype(float)}, index=t)
    return df


def minute_all(sym="XAUUSD"):
    out = []
    for f in sorted(glob.glob(f"{S}/data/duka_m/{sym}/*.bi5")):
        day = pd.Timestamp(os.path.basename(f)[:8], tz="UTC")
        d = decode_bi5(f, day)
        if d is not None and len(d):
            out.append(d)
    m = pd.concat(out).sort_index()
    return m


_H = None
def hourly_bars():
    """Saatlik bar (index = bar başlangıcı). Saatlik dosyanın bittiği yerden sonrası dakikadan."""
    global _H
    if _H is not None:
        return _H
    h = pd.read_parquet(f"{P}/duka/XAUUSD.parquet")
    last = h.index.max()
    m = minute_all()
    m = m[(m.index > last + pd.Timedelta(minutes=59)) & (m.v > 0)]
    if len(m):
        hm = m.resample("1h").agg({"o": "first", "c": "last", "l": "min", "h": "max", "v": "sum"}).dropna()
        h = pd.concat([h, hm]).sort_index()
    _H = h
    return h


def price_at(times):
    """Tam olarak T anındaki fiyat = T-1h başlangıçlı barın kapanışı; bar yoksa NaN (as-of YOK)."""
    h = hourly_bars()
    c = h["c"]
    key = pd.DatetimeIndex(times) - pd.Timedelta(hours=1)
    return pd.Series(c.reindex(key).values, index=times)


def price_asof(times, max_stale_h=1.0):
    """T anında bilinen son fiyat (fiyat anı <= T), en fazla max_stale_h saat bayat."""
    h = hourly_bars()
    pt = h.index + pd.Timedelta(hours=1)
    c = h["c"].values
    times = pd.DatetimeIndex(times)
    i = pt.searchsorted(times, side="right") - 1
    ok = i >= 0
    ii = np.clip(i, 0, None)
    stale = (times - pt[ii]) / pd.Timedelta(hours=1)
    val = np.where(ok & (stale <= max_stale_h), c[ii], np.nan)
    return pd.Series(val, index=times)


def day_times(days, hour, day_offset=0):
    days = pd.DatetimeIndex(days)
    return pd.DatetimeIndex([pd.Timestamp(d.date()).tz_localize("UTC") + pd.Timedelta(days=day_offset, hours=hour) for d in days])


# ---------------------------------------------------------------- VİOP aktif kontrat
def viop_active():
    L = pd.read_parquet(f"{P}/viop_long.parquet")
    L = L[L.code.astype(str).str.startswith("F_XAUUSD")].copy()
    L["date"] = pd.to_datetime(L["date"])
    days = np.sort(L.date.unique())
    # her gün OI en büyük kontrat (gün sonu); aktif(t) = argmax OI (t-1)
    idx = L.groupby("date").oi.idxmax()
    top = L.loc[idx, ["date", "code"]].set_index("date").code
    top = top.reindex(pd.DatetimeIndex(days))
    act = top.shift(1)
    act.iloc[0] = top.iloc[0]
    Li = L.set_index(["date", "code"])
    rows = []
    for d, c in act.items():
        if (d, c) in Li.index:
            r = Li.loc[(d, c)]
            if isinstance(r, pd.DataFrame):
                r = r.iloc[0]
            rows.append(dict(date=d, code=c, settle=r.settle, prev_settle=r.prev_settle, expiry=r.expiry, oi=r.oi, volume=r.volume, open=r.open, close=r.close, os_price=r.os_price))
        else:
            rows.append(dict(date=d, code=c))
    A = pd.DataFrame(rows).set_index("date")
    A["ret"] = np.log(A.settle / A.prev_settle)
    return A


def fwd(r, h):
    return sum(r.shift(-k) for k in range(1, h + 1))


# ---------------------------------------------------------------- istatistik
def nw_t_ols(y, x, L):
    """y = a + b x + u; Bartlett NW HAC, maxlag L, küçük örneklem düzeltmesi n/(n-k). b'nin t'si."""
    y = np.asarray(y, float); x = np.asarray(x, float)
    n = len(y)
    X = np.column_stack([np.ones(n), x])
    XtXi = np.linalg.inv(X.T @ X)
    b = XtXi @ X.T @ y
    u = y - X @ b
    g = X * u[:, None]
    Sm = g.T @ g
    for l in range(1, L + 1):
        w = 1 - l / (L + 1)
        G = g[l:].T @ g[:-l]
        Sm += w * (G + G.T)
    Sm *= n / (n - 2)
    V = XtXi @ Sm @ XtXi
    return b[1], b[1] / np.sqrt(V[1, 1])


def nw_t_mean(x, L=5):
    x = np.asarray(pd.Series(x).dropna(), float)
    n = len(x)
    u = x - x.mean()
    s = (u @ u)
    for l in range(1, L + 1):
        s += 2 * (1 - l / (L + 1)) * (u[l:] @ u[:-l])
    s *= n / (n - 1)
    se = np.sqrt(s) / n
    return x.mean(), x.mean() / se, n


def ic_nw(x, y, L):
    d = pd.concat([pd.Series(x, name="x"), pd.Series(y, name="y")], axis=1).dropna()
    if len(d) < 30:
        return np.nan, np.nan, len(d)
    rx = d.x.rank().values; ry = d.y.rank().values
    c = np.corrcoef(rx, ry)[0, 1]
    zx = (rx - rx.mean()) / rx.std(ddof=1); zy = (ry - ry.mean()) / ry.std(ddof=1)
    _, t = nw_t_ols(zy, zx, L)
    return c, t, len(d)


def split_ic(x, y, h, min_year=20):
    L = max(h, 5)
    x = pd.Series(x); y = pd.Series(y)
    full = ic_nw(x, y, L)
    isx = ic_nw(x[x.index <= IS_END], y[y.index <= IS_END], L)
    oos = ic_nw(x[x.index > IS_END], y[y.index > IS_END], L)
    d = pd.concat([x.rename("x"), y.rename("y")], axis=1).dropna()
    yr = d.groupby(d.index.year).apply(lambda g: g.x.rank().corr(g.y.rank()) if len(g) > min_year else np.nan)
    same = int((np.sign(yr.dropna()) == np.sign(full[0])).sum())
    return dict(ic=full[0], t=full[1], n=full[2], ic_is=isx[0], t_is=isx[1], ic_oos=oos[0], t_oos=oos[1], yrs=f"{same}/{int(yr.notna().sum())}")


def stagger_pnl(pos, ret, h, cost_bps):
    """Kademeli: her gün 1/h sermaye ile pos_t açılır, t uzlaşmasında girilir, h gün tutulur.
    eff_t = ortalama(pos_t..pos_{t-h+1}); getiri(t+1) = eff_t * ret_{t+1} - |eff_t - eff_{t-1}| * cost/2 (tek yön)."""
    ret = ret.copy()
    pos = pos.reindex(ret.index).fillna(0.0).clip(-1, 1)
    eff = pos.rolling(h, min_periods=1).sum() / h
    # ilk h-1 gün: rolling(min_periods=1).sum()/h -> doğru (eksikler 0)
    turn = (eff - eff.shift(1).fillna(0)).abs()
    pnl = eff.shift(1) * ret - turn.shift(1) * cost_bps / 2 / 1e4
    return pnl.dropna(), eff, turn


def sharpe(x):
    x = pd.Series(x).dropna()
    return x.mean() / x.std() * np.sqrt(252) if x.std() > 0 else np.nan


def bt(pos, ret, h, cost_bps, period=None):
    """period: None tam, 'is', 'oos' — dönem içinde ayrı backtest (ret o döneme kısıtlanır)."""
    if period == "is":
        r = ret[ret.index <= IS_END]
    elif period == "oos":
        r = ret[ret.index > IS_END]
    else:
        r = ret
    r = r.dropna()
    pnl, eff, turn = stagger_pnl(pos, r, h, cost_bps)
    pnl_dm, _, _ = stagger_pnl(pos, r - r.mean(), h, cost_bps)
    return dict(sharpe=sharpe(pnl), sharpe_dm=sharpe(pnl_dm), ann=pnl.mean() * 252 * 100, turn=turn.sum() / len(pnl) * 252, expo=eff.abs().mean(), n=len(pnl),
                bh=sharpe(r))
