"""Bağımsız yeniden üretim — ortak yardımcılar (lib_altin KULLANILMADI).
IS = <=2017-12-31, OOS = 2018+. Hedef: log(adjclose_{t+h}/adjclose_t) (ABD kapanışı 16:00 ET).
"""
import os, glob, lzma, json, numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
P = f"{S}/panel"; OUT = f"{S}/out/e3_etf_akis_prim_rep"
IS_END = pd.Timestamp("2017-12-31")
NY = "America/New_York"

def yh(t, col="adjclose"):
    x = pd.read_parquet(f"{P}/yahoo/{t}.parquet"); x.index = pd.to_datetime(x.index).normalize()
    x = x[~x.index.duplicated(keep="last")]
    return x[col] if col else x

def nyse_days(start="2008-01-01"):
    g = yh("GLD", None); return pd.DatetimeIndex(g.index[g.index >= start])

def xau_hourly(with_2026_min=True):
    """Dukascopy BID saatlik; fiyat anı = bar başlangıcı + 1 saat (barın son tikinin üst sınırı)."""
    d = pd.read_parquet(f"{P}/duka/XAUUSD.parquet")
    s = d["c"].copy(); s.index = d.index + pd.Timedelta(hours=1)
    if with_2026_min:
        last = s.index.max(); add = []
        for f in sorted(glob.glob(f"{S}/data/duka_m/XAUUSD/2026*.bi5")):
            b = open(f, "rb").read()
            if not b: continue
            day = pd.Timestamp(os.path.basename(f)[:8], tz="UTC")
            raw = lzma.decompress(b); a = np.frombuffer(raw, dtype=">i4").reshape(-1, 6).astype(np.int64)
            vol = np.frombuffer(raw, dtype=">f4").reshape(-1, 6)[:, 5].astype(np.float64)
            m = pd.DataFrame({"t": day + pd.to_timedelta(a[:, 0], unit="s"), "c": a[:, 2] / 1e3, "v": vol})
            m = m[m.v > 0]
            # dakika mumu: fiyat anı = dakika başı + 1 dk; saatlik son değer
            m["t"] = m["t"] + pd.Timedelta(minutes=1)
            add.append(m)
        if add:
            m = pd.concat(add).set_index("t").sort_index()
            m = m[m.index > last]
            # saat sınırına yuvarlanmış anlık değerler: her tam saatte, o saate kadar son dakika kapanışı
            hr = m["c"].resample("1h", label="right", closed="right").last().dropna()
            s = pd.concat([s, hr]).sort_index()
    s = s[~s.index.duplicated(keep="first")]
    return s

def snap(series, targets, max_stale_min=60):
    """targets (UTC DatetimeIndex) anında ya da öncesindeki son değer; en fazla max_stale_min dakika bayat."""
    idx = series.index.searchsorted(targets, side="right") - 1
    ok = idx >= 0
    vals = np.where(ok, series.values[np.clip(idx, 0, None)], np.nan)
    ts = series.index.values[np.clip(idx, 0, None)]
    stale = (targets.values - ts) / np.timedelta64(1, "m")
    return pd.Series(np.where(ok & (stale <= max_stale_min), vals, np.nan), index=targets), pd.Series(ts, index=targets)

def et_times(days, hh, mm=0):
    return pd.DatetimeIndex([pd.Timestamp(d) + pd.Timedelta(hours=hh, minutes=mm) for d in days]).tz_localize(NY).tz_convert("UTC")

# ---------------- istatistik
def nw_t(y, x, L):
    """y = a + b x OLS; Newey-West (Bartlett, L gecikme) t(b). Küçük örnek düzeltmesi yok."""
    y = np.asarray(y, float); x = np.asarray(x, float); n = len(y)
    X = np.column_stack([np.ones(n), x])
    XtXi = np.linalg.inv(X.T @ X); b = XtXi @ X.T @ y; e = y - X @ b
    u = X * e[:, None]; Sm = u.T @ u
    for l in range(1, L + 1):
        w = 1 - l / (L + 1); G = u[l:].T @ u[:-l]; Sm += w * (G + G.T)
    V = XtXi @ Sm @ XtXi
    return b[1], b[1] / np.sqrt(V[1, 1])

def ic(x, y, L=5, method="spearman"):
    d = pd.concat([pd.Series(x, name="x"), pd.Series(y, name="y")], axis=1).dropna()
    if len(d) < 30: return dict(ic=np.nan, t=np.nan, n=len(d))
    if method == "spearman": d = d.rank()
    c = d.x.corr(d.y)
    zx = (d.x - d.x.mean()) / d.x.std(); zy = (d.y - d.y.mean()) / d.y.std()
    _, t = nw_t(zy.values, zx.values, L)
    return dict(ic=float(c), t=float(t), n=len(d))

def stats(x, y, h, method="spearman", is_end=IS_END, extra_splits=True):
    L = max(h, 5)
    d = pd.concat([pd.Series(x, name="x"), pd.Series(y, name="y")], axis=1).dropna()
    f = ic(d.x, d.y, L, method); a = ic(d.x[d.index <= is_end], d.y[d.index <= is_end], L, method)
    o = ic(d.x[d.index > is_end], d.y[d.index > is_end], L, method)
    yr = d.groupby(d.index.year).apply(lambda g: g.x.corr(g.y, method=method) if len(g) > 20 else np.nan).dropna()
    out = dict(n=f["n"], ic=round(f["ic"], 4), t=round(f["t"], 2), ic_is=round(a["ic"], 4), t_is=round(a["t"], 2),
               ic_oos=round(o["ic"], 4), t_oos=round(o["t"], 2), yrs=f"{int((np.sign(yr) == np.sign(f['ic'])).sum())}/{len(yr)}")
    if extra_splits:
        s22 = ic(d.x[d.index >= "2022-01-01"], d.y[d.index >= "2022-01-01"], L, method); out["t_22"] = round(s22["t"], 2)
    return out

def fwd(r, h):
    return sum(r.shift(-k) for k in range(1, h + 1))

# ---------------- backtest (bağımsız yazım)
def run_bt(pos, R, h, cost_rt_bps, inv=None):
    """pos_t (karar t kapanışında) -> t+1 getirisinde. R: basit günlük getiri (t-1 kapanış -> t kapanış).
    h>1: kademeli; her gün sermayenin 1/h'i h gün tutulur (ağırlık = son h sinyalin ortalaması).
    Maliyet: |Δağırlık| × (gidiş-dönüş/2), ağırlık değiştiği gün (t kapanışında) ödenir, t+1 PnL'inden düşülür.
    inv: dict(R=ters ETF basit getiri, L=Series kaldıraç, cost=gidiş-dönüş bps) -> pos<0 için |pos|/L nominal ters ETF.
    """
    idx = R.index; p = pos.reindex(idx).fillna(0.0)
    if inv is None: p = p.clip(lower=0)
    w = p.rolling(h, min_periods=1).sum() / h if h > 1 else p
    if h > 1:  # ilk h-1 günde eksik terimleri 0 say
        w = sum(p.shift(k).fillna(0) for k in range(h)) / h
    wl = w.clip(lower=0)
    pnl = wl.shift(1) * R
    cost = wl.diff().abs().fillna(wl.abs()).shift(1) * cost_rt_bps / 2e4
    if inv is not None:
        Ri = inv["R"].reindex(idx); Lv = inv["L"].reindex(idx)
        ws = (-w).clip(lower=0) / Lv
        pnl = pnl + (ws.shift(1) * Ri).fillna(0)
        cost = cost + ws.diff().abs().fillna(ws.abs()).shift(1).fillna(0) * inv["cost"] / 2e4
    net = (pnl - cost.fillna(0))[R.notna()].iloc[1:]
    return net, wl, (ws if inv is not None else wl * 0)

def sharpe(x):
    x = pd.Series(x).dropna()
    return np.nan if len(x) < 50 or x.std() == 0 else round(x.mean() / x.std() * np.sqrt(252), 3)

def seg_sh(x):
    x = x.dropna()
    return dict(full=sharpe(x), IS=sharpe(x[x.index <= IS_END]), OOS=sharpe(x[x.index > IS_END]), s22=sharpe(x[x.index >= "2022-01-01"]))
