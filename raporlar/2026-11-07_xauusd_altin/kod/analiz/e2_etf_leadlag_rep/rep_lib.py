"""Bagimsiz yeniden uretim yardimcilari (lib_altin ve e2_common KULLANILMAZ).
Ham tablolar: panel/yahoo/*.parquet (gunluk OHLC, index = yerel tarih, ts_utc = seans acilisi),
panel/duka/XAUUSD.parquet (saatlik BID, index = bar baslangici UTC, fiyat ani = index + 1 saat),
panel/duka_min_XAUUSD.parquet (dakikalik; yalniz 2026-10-30 sonrasi yamasi icin).
"""
import numpy as np, pandas as pd

S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
P = f"{S}/panel"
OUT = f"{S}/out/e2_etf_leadlag_rep"
IS_END = pd.Timestamp("2017-12-31")
NY = "America/New_York"


def yahoo(tk, col="adjclose"):
    d = pd.read_parquet(f"{P}/yahoo/{tk}.parquet")
    d.index = pd.to_datetime(d.index).normalize()
    return d[col].astype(float)


def nyse_calendar():
    g = yahoo("GLD")
    idx = g.index[(g.index >= "2008-01-02") & (g.index <= "2026-11-06")]
    return pd.DatetimeIndex(idx)


def at_local(dates, hh, mm, tz):
    """yerel tarih + saat -> UTC Timestamp dizisi"""
    s = pd.Series(pd.DatetimeIndex(dates) + pd.Timedelta(hours=hh, minutes=mm))
    return pd.DatetimeIndex(s.dt.tz_localize(tz).dt.tz_convert("UTC"))


# ---------- spot altin: fiyat ani T (UTC) ----------
def gold_price_series():
    """T (UTC, tam saat) -> o anki fiyat = baslangici T-1h olan saatlik barin kapanisi.
    2026-10-30 21:00 UTC sonrasi icin dakikalik veri: T anindaki fiyat = baslangici T-1dk olan dakika barinin kapanisi."""
    h = pd.read_parquet(f"{P}/duka/XAUUSD.parquet")
    ph = pd.Series(h["c"].values, index=h.index + pd.Timedelta(hours=1))   # fiyat ani
    m = pd.read_parquet(f"{P}/duka_min_XAUUSD.parquet")
    mi = pd.DatetimeIndex(m.index).tz_localize("UTC") + pd.Timedelta(minutes=1)
    pm = pd.Series(m["c"].values, index=mi)
    pm = pm[pm.index > ph.index.max()]
    return ph.sort_index(), pm.sort_index()


def price_at(ph, pm, T, max_stale_h=3):
    """T anindaki (ya da en fazla max_stale_h saat onceki) son fiyat; yalniz T ve oncesi."""
    T = pd.DatetimeIndex(T)
    allp = pd.concat([ph, pm]).sort_index()
    allp = allp[~allp.index.duplicated(keep="last")]
    pos = allp.index.searchsorted(T, side="right") - 1
    out = np.full(len(T), np.nan); stamp = [pd.NaT] * len(T)
    for i, p_ in enumerate(pos):
        if p_ < 0: continue
        ts = allp.index[p_]
        if (T[i] - ts) <= pd.Timedelta(hours=max_stale_h):
            out[i] = allp.values[p_]; stamp[i] = ts
    return pd.Series(out, index=T), pd.DatetimeIndex(stamp)


# ---------- istatistik ----------
def nw_slope_t(y, x, L):
    """y = a + b x + u; Bartlett cekirdekli Newey-West t (kucuk orneklem duzeltmesi yok)."""
    x = np.asarray(x, float); y = np.asarray(y, float); n = len(x)
    xc = x - x.mean(); yc = y - y.mean()
    b = (xc @ yc) / (xc @ xc)
    u = yc - b * xc
    g = xc * u
    S = g @ g
    for l in range(1, L + 1):
        w = 1 - l / (L + 1)
        S += 2 * w * (g[l:] @ g[:-l])
    se = np.sqrt(S) / (xc @ xc)
    return b, b / se


def ic_t(x, y, L):
    d = pd.concat([pd.Series(x, name="x"), pd.Series(y, name="y")], axis=1).dropna()
    if len(d) < 30: return np.nan, np.nan, len(d)
    rx = d.x.rank().values; ry = d.y.rank().values
    zx = (rx - rx.mean()) / rx.std(ddof=1); zy = (ry - ry.mean()) / ry.std(ddof=1)
    ic = np.corrcoef(rx, ry)[0, 1]
    _, t = nw_slope_t(zy, zx, L)
    return float(ic), float(t), len(d)


def fwd_ret(logp, h):
    """log(c_{t+h}/c_t) dogrudan fiyattan"""
    return logp.shift(-h) - logp


def stats_block(x, y, h, extra_periods=True):
    L = max(h, 5)
    o = {}
    o["ic"], o["t"], o["n"] = ic_t(x, y, L)
    o["ic_is"], o["t_is"], o["n_is"] = ic_t(x[x.index <= IS_END], y[y.index <= IS_END], L)
    o["ic_oos"], o["t_oos"], o["n_oos"] = ic_t(x[x.index > IS_END], y[y.index > IS_END], L)
    if extra_periods:
        o["ic_22"], o["t_22"], _ = ic_t(x[x.index >= "2022-01-01"], y[y.index >= "2022-01-01"], L)
    d = pd.concat([pd.Series(x, name="x"), pd.Series(y, name="y")], axis=1).dropna()
    yr = d.groupby(d.index.year).apply(lambda g: g.x.rank().corr(g.y.rank()) if len(g) > 20 else np.nan)
    o["yrs_same"] = int((np.sign(yr) == np.sign(o["ic"])).sum()); o["yrs"] = int(yr.notna().sum())
    o["by_year"] = yr
    return o


def sub_ic(x, y, h, a, b):
    m = (x.index >= a) & (x.index <= b)
    return ic_t(x[m], y.reindex(x.index)[m], max(h, 5))


# ---------- yuvarlanan regresyon ----------
def roll_ols(y, X, win, minp):
    """y_t ~ 1 + X_t, pencere [t-win+1, t] (t dahil). Donus: katsayilar (sabit haric), index = y.index."""
    Yv = y.values.astype(float); Xv = X.values.astype(float); n, k = Xv.shape
    B = np.full((n, k), np.nan)
    for i in range(n):
        lo = max(0, i - win + 1)
        yy = Yv[lo:i + 1]; xx = Xv[lo:i + 1]
        m = np.isfinite(yy) & np.isfinite(xx).all(1)
        if m.sum() < minp: continue
        A = np.column_stack([np.ones(m.sum()), xx[m]])
        B[i] = np.linalg.lstsq(A, yy[m], rcond=None)[0][1:]
    return pd.DataFrame(B, index=y.index, columns=X.columns)


# ---------- strateji ----------
def positions(x, sign, q):
    xi = x[x.index <= IS_END].dropna()
    hi, lo = xi.quantile(q), xi.quantile(1 - q)
    p = pd.Series(0.0, index=x.index)
    p[x > hi] = sign; p[x < lo] = -sign
    return p, hi, lo


def bt(pos, r, h, cost_bps):
    """Kademeli: eff_t = (1/h) sum_{j<h} pos_{t-j}; pnl_{t+1} = eff_t r_{t+1} - |eff_t - eff_{t-1}| c/2.
    Tum ornek uzerinde calisir (donem sinirinda pozisyon tasinir); donem dilimi sonra alinir."""
    pos = pos.reindex(r.index).fillna(0.0)
    eff = pos.rolling(h, min_periods=1).sum() / h
    eff = eff.where(np.arange(len(eff)) >= 0)
    turn = (eff - eff.shift(1).fillna(0)).abs()
    pnl = eff.shift(1) * r - turn.shift(1).fillna(0) * cost_bps / 2 / 1e4
    return pnl, eff, turn


def sharpe(p):
    p = p.dropna()
    return float(p.mean() / p.std() * np.sqrt(252)) if len(p) > 50 and p.std() > 0 else np.nan


def maxdd(p):
    c = p.fillna(0).cumsum(); return float((c - c.cummax()).min())
