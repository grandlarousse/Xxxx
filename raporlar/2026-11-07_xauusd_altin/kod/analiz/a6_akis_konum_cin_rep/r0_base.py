"""Bağımsız yeniden üretim — temel yapı taşları (lib_altin KULLANILMADI).
- VİOP hedef: viop_long'dan aktif kontrat (t-1 OI en büyük), aynı kontrat içinde log(settle/prev_settle); fwd_h = t+1..t+h toplamı.
- Spot altın: Dukascopy saatlik BID, fiyat anı = bar_start + 1h; Ekim-Kasım 2026 yaması dakikalık dosyadan.
- İstatistik: Spearman IC, NW (Bartlett) t (rank-z OLS), kendi kademeli backtest'im.
"""
import numpy as np, pandas as pd, os
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
P = f"{S}/panel"; OUT = f"{S}/out/a6_akis_konum_cin_rep"
IS_END = pd.Timestamp("2021-12-31")

# ---------------- VİOP hedef ----------------
def viop_target():
    L = pd.read_parquet(f"{P}/viop_long.parquet")
    x = L[L.root == "XAUUSD"].copy(); x["date"] = pd.to_datetime(x["date"]); x["expiry"] = pd.to_datetime(x["expiry"])
    days = np.sort(x.date.unique())
    st = x.pivot_table(index="date", columns="code", values="settle")
    ps = x.pivot_table(index="date", columns="code", values="prev_settle")
    oi = x.pivot_table(index="date", columns="code", values="oi")
    # aktif = önceki günün OI en büyük kontratı (ilk gün: aynı gün)
    oi_prev = oi.shift(1); oi_prev.iloc[0] = oi.iloc[0]
    oi_prev = oi_prev.where(st.notna())          # o gün de işlem gören kontratlar arasından
    act = oi_prev.idxmax(axis=1)
    r = pd.Series([np.log(st.loc[d, c] / ps.loc[d, c]) for d, c in act.items()], index=st.index)
    # prev_settle tutarlılık: bir önceki günkü settle ile aynı mı?
    chk = pd.Series([ (st.shift(1).loc[d, c], ps.loc[d, c]) for d, c in act.items()], index=st.index)
    T = pd.DataFrame({"code": act, "ret": r})
    T["settle"] = [st.loc[d, c] for d, c in act.items()]
    T["prev_settle_bulletin"] = [ps.loc[d, c] for d, c in act.items()]
    T["prev_settle_own"] = [st.shift(1).loc[d, c] for d, c in act.items()]
    for h in (1, 3, 5, 10):
        T[f"fwd{h}"] = sum(T["ret"].shift(-k) for k in range(1, h + 1))
    return T

# ---------------- spot altın ----------------
_G = None
def gold_series():
    global _G
    if _G is None:
        h = pd.read_parquet(f"{P}/duka/XAUUSD.parquet")
        s = h["c"].copy(); s.index = s.index.tz_convert("UTC").tz_localize(None) + pd.Timedelta(hours=1)
        m = pd.read_parquet(f"{P}/duka_min_XAUUSD.parquet")["c"]
        m.index = pd.to_datetime(m.index) + pd.Timedelta(minutes=1)   # dakika bar kapanışı
        m = m[m.index > s.index.max()]
        # dakikadan saat başı fiyatları (saat başı anında son bilinen)
        _G = pd.concat([s, m]).sort_index()
        _G = _G[~_G.index.duplicated(keep="first")]
    return _G

def gold_at(ts, max_stale_h=2.0):
    G = gold_series(); ts = pd.DatetimeIndex(ts)
    out = np.full(len(ts), np.nan); ok = ~ts.isna()
    i = G.index.searchsorted(ts[ok], side="right") - 1
    ii = np.clip(i, 0, None)
    stale = (ts[ok] - G.index[ii]) / pd.Timedelta(hours=1)
    out[ok] = np.where((i >= 0) & (stale <= max_stale_h), G.values[ii], np.nan)
    return out

# ---------------- istatistik ----------------
def nw_t(y, X, L):
    """OLS y~X (X sabit içerir), Bartlett NW kovaryans, katsayı t'leri (küçük örneklem düzeltmesi yok)."""
    y = np.asarray(y, float); X = np.asarray(X, float); n, k = X.shape
    XtX_inv = np.linalg.inv(X.T @ X); b = XtX_inv @ X.T @ y; e = y - X @ b
    u = X * e[:, None]; Sm = u.T @ u
    for l in range(1, L + 1):
        w = 1 - l / (L + 1); G_ = u[l:].T @ u[:-l]; Sm += w * (G_ + G_.T)
    V = XtX_inv @ Sm @ XtX_inv
    return b, b / np.sqrt(np.diag(V)), n

def ic_t(x, y, L):
    d = pd.concat([pd.Series(x, name="x"), pd.Series(y, name="y")], axis=1).dropna()
    if len(d) < 30: return dict(ic=np.nan, t=np.nan, n=len(d))
    rk = d.rank(); c = rk.x.corr(rk.y)
    zx = (rk.x - rk.x.mean()) / rk.x.std(); zy = (rk.y - rk.y.mean()) / rk.y.std()
    b, t, n = nw_t(zy.values, np.column_stack([np.ones(len(zx)), zx.values]), L)
    return dict(ic=float(c), t=float(t[1]), n=int(n))

def split(x, y, h, is_end=IS_END):
    L = max(h, 5)
    x = x.reindex(y.index)
    f = ic_t(x, y, L); i = ic_t(x[x.index <= is_end], y[y.index <= is_end], L); o = ic_t(x[x.index > is_end], y[y.index > is_end], L)
    d = pd.concat([x.rename("x"), y.rename("y")], axis=1).dropna()
    yr = d.groupby(d.index.year).apply(lambda g: g.x.corr(g.y, method="spearman") if len(g) > 20 else np.nan)
    same = int((np.sign(yr) == np.sign(f["ic"])).sum())
    return dict(ic=f["ic"], t=f["t"], n=f["n"], ic_is=i["ic"], t_is=i["t"], ic_oos=o["ic"], t_oos=o["t"], yrs=f"{same}/{int(yr.notna().sum())}",
                by_year=yr.round(3).to_dict())

def stagger(pos, r, h, cost_bps=5.0, demean=False, netted=True):
    """pos_t gün t uzlaşmasında açılır, t+1..t+h getirilerini taşır, her gün sermayenin 1/h'i.
    Gün s portföy getirisi = (1/h) Σ_{j=1..h} pos_{s-j} r_s. Maliyet gidiş-dönüş cost_bps:
    netted: |eff_t - eff_{t-1}| × cost/2 ;  non-netted: (|pos_t|+|pos_{t-h}|)/h × cost/2 (her alt portföy ayrı işlem)."""
    r = r.dropna().copy()
    if demean: r = r - r.mean()
    p = pos.reindex(r.index).fillna(0.0).clip(-1, 1)
    eff = sum(p.shift(j).fillna(0) for j in range(h)) / h        # gün t kapanışından sonra tutulan
    gross = eff.shift(1).fillna(0) * r
    if netted:
        turn = (eff - eff.shift(1).fillna(0)).abs()
    else:
        turn = (p.abs() + p.shift(h).fillna(0).abs()) / h
    cost = turn.shift(1).fillna(0) * cost_bps / 2 / 1e4
    net = gross - cost
    sh = net.mean() / net.std() * np.sqrt(252) if net.std() > 0 else np.nan
    return dict(sharpe=float(sh), ann=float(net.mean() * 252), turn_yr=float(turn.sum() / len(net) * 252), pnl=net)

def periods(pos, r, h, cost_bps=5.0, netted=True):
    out = {}
    for nm, m in [("full", r.index == r.index), ("is", r.index <= IS_END), ("oos", r.index > IS_END)]:
        rr = r[m]
        out[nm] = dict(LS=stagger(pos, rr, h, cost_bps, netted=netted)["sharpe"],
                       LS_dm=stagger(pos, rr, h, cost_bps, demean=True, netted=netted)["sharpe"],
                       long=stagger(pos.clip(lower=0), rr, h, cost_bps, netted=netted)["sharpe"],
                       long_dm=stagger(pos.clip(lower=0), rr, h, cost_bps, demean=True, netted=netted)["sharpe"],
                       short=stagger(pos.clip(upper=0), rr, h, cost_bps, netted=netted)["sharpe"],
                       short_dm=stagger(pos.clip(upper=0), rr, h, cost_bps, demean=True, netted=netted)["sharpe"],
                       bh=float(rr.dropna().mean() / rr.dropna().std() * np.sqrt(252)))
    return out
