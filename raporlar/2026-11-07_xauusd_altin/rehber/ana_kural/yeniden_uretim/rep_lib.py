"""Bagimsiz yeniden uretim kutuphanesi (net_rep). Ana ajanin kodu CALISTIRILMAZ / import edilmez.
Her sey ham Yahoo (GDX, GLD, SPY) + ham VIOP bulteni (viop_long) + ham Dukascopy saatlikten kurulur."""
import numpy as np, pandas as pd
import statsmodels.api as sm

S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
OUT = f"{S}/out/net_rep"


# ---------------------------------------------------------------- Yahoo -> artik
def load_yahoo(tk, col="adjclose"):
    d = pd.read_parquet(f"{S}/panel/yahoo/{tk}.parquet")
    d.index = pd.to_datetime(d.index).astype("datetime64[ns]")
    return d[col].astype(float)


def us_returns(col="adjclose", tickers=("GDX", "GLD", "SPY")):
    px = pd.concat({k: load_yahoo(k, col) for k in tickers}, axis=1, join="inner").sort_index()
    assert px.notna().all().all()
    return np.log(px).diff().iloc[1:]


def rolling_resid(R, win=250, minobs=250, y="GDX", xs=("GLD", "SPY"), sub_const=False):
    """e_d = r_y,d - sum_j b_j,d r_j,d ; b_d = sabitli OLS, satirlar [d-win, d-1] (d haric).
    minobs: en az gozlem (kural 250 diyor; ana ajan 60 ile basliyor)."""
    Y = R[y].values
    X = R[list(xs)].values
    n = len(R)
    e = np.full(n, np.nan)
    B = np.full((n, len(xs) + 1), np.nan)
    for i in range(minobs, n):
        lo = max(0, i - win)
        A = np.column_stack([np.ones(i - lo), X[lo:i]])
        b = np.linalg.lstsq(A, Y[lo:i], rcond=None)[0]
        B[i] = b
        e[i] = Y[i] - X[i] @ b[1:] - (b[0] if sub_const else 0.0)
    e = pd.Series(e, index=R.index, name="e")
    B = pd.DataFrame(B, index=R.index, columns=["const"] + list(xs))
    return e, B


# ---------------------------------------------------------------- VIOP ham bultenden
def viop_active_from_raw(root="XAUUSD"):
    """Aktif kontrat = bir onceki VIOP gununde acik pozisyonu en buyuk vade (esitlikte en yakin vade).
    ret_t = log(settle_t / prev_settle_t), ayni kontrat. Kendi kurulum; panel_viop ile ayrica karsilastirilir."""
    vl = pd.read_parquet(f"{S}/panel/viop_long.parquet")
    x = vl[vl.root == root].copy()
    x["date"] = pd.to_datetime(x["date"]).astype("datetime64[ns]")
    x["expiry"] = pd.to_datetime(x["expiry"]).astype("datetime64[ns]")
    x = x.sort_values(["date", "expiry"])
    days = pd.DatetimeIndex(sorted(x.date.unique()))
    byd = {d: g.set_index("code") for d, g in x.groupby("date")}
    rows = []
    prev = None
    for d in days:
        g = byd[d]
        if prev is None:
            cand = g[g.expiry >= d]
            code = cand.sort_values(["oi", "expiry"], ascending=[False, True]).index[0]
        else:
            gp = byd[prev]
            cand = gp[(gp.expiry >= d) & gp.index.isin(g.index)]  # bugun hala islem goren vadeler
            code = cand.sort_values(["oi", "expiry"], ascending=[False, True]).index[0]
        r = g.loc[code]
        rows.append(dict(date=d, code=code, expiry=r.expiry, settle=r.settle, prev_settle=r.prev_settle,
                         ret=np.log(r.settle / r.prev_settle), volume=r.volume, oi=r.oi, close=r.close, open=r.open))
        prev = d
    out = pd.DataFrame(rows).set_index("date")
    return out, x


# ---------------------------------------------------------------- eslestirme
def map_last_us_before(target_days, us_series):
    """Her hedef gun t icin: tarihi KESINLIKLE < t olan son ABD kapanisinin degeri ve tarihi."""
    s = us_series.dropna()
    ud = s.index.values.astype("datetime64[ns]")
    td = pd.DatetimeIndex(target_days).values.astype("datetime64[ns]")
    idx = np.searchsorted(ud, td, side="left") - 1
    val = np.where(idx >= 0, s.values[np.clip(idx, 0, None)], np.nan)
    dts = np.where(idx >= 0, ud[np.clip(idx, 0, None)], np.datetime64("NaT"))
    return pd.Series(val, index=target_days), pd.Series(pd.DatetimeIndex(dts), index=target_days)


# ---------------------------------------------------------------- istatistik
def fwd_sum(r, h):
    """fwd_h(t) = r_{t+1}+...+r_{t+h} (log)."""
    return sum(r.shift(-k) for k in range(1, h + 1))


def nw_diff(y, s, L):
    """y = a + b*s ; b = sinyal gunleri ort. - diger gunler ort. ; HAC (Bartlett) maxlags=L."""
    d = pd.concat([y.rename("y"), s.rename("s")], axis=1).dropna()
    if d.s.nunique() < 2 or len(d) < 30:
        return dict(b=np.nan, t=np.nan, n1=int(d.s.sum()) if len(d) else 0, N=len(d))
    m = sm.OLS(d.y.values, sm.add_constant(d.s.values)).fit(cov_type="HAC", cov_kwds={"maxlags": L})
    return dict(b=m.params[1], t=m.tvalues[1], n1=int(d.s.sum()), N=len(d))


def event_stats(r, sig, h, a=None, b=None, L=None):
    f = fwd_sum(r, h)
    d = pd.concat([f.rename("f"), sig.rename("s")], axis=1).dropna()
    d = d.loc[a:b]
    L = L if L is not None else max(h, 5)
    nw = nw_diff(d.f, d.s, L)
    on = d.f[d.s > 0]; off = d.f[d.s == 0]
    return dict(h=h, N=len(d), n_sig=len(on), mean_sig=on.mean() * 100, mean_all=d.f.mean() * 100, mean_off=off.mean() * 100,
                hit_sig=(on > 0).mean() * 100, hit_all=(d.f > 0).mean() * 100, diff=nw["b"] * 100, t_nw=nw["t"],
                diff_vs_all=(on.mean() - d.f.mean()) * 100)


def sharpe(p):
    p = p.dropna()
    return p.mean() / p.std() * np.sqrt(252) if p.std() > 0 else np.nan


def maxdd(p):
    eq = (1 + p.fillna(0)).cumprod()
    return (eq / eq.cummax() - 1).min()


def run_trades(r, sig, H, cost_bps):
    """Yalniz uzun. Sinyal gunu s uzlasmasinda AL; SON sinyal gununden H VIOP gunu sonra uzlasmada SAT.
    Tutarken yeni sinyal gelirse sure yeniden baslar. Donus: (islem listesi, gunluk net pnl, pozisyon).
    r: gunluk log uzlasma getirisi (aktif kontrat). Maliyet: gidis-donus cost_bps (yarisi giris, yarisi cikis)."""
    idx = r.index
    sv = sig.reindex(idx).fillna(0).values
    rv = r.values
    n = len(idx)
    pos = np.zeros(n)          # gun t uzlasmasindan t+1 uzlasmasina tasinan pozisyon
    left = 0
    for i in range(n):
        if sv[i] > 0:
            left = H
        pos[i] = 1.0 if left > 0 else 0.0
        if left > 0:
            left -= 1
    pos = pd.Series(pos, index=idx)
    simple = np.exp(r) - 1
    gross = pos.shift(1).fillna(0) * simple.fillna(0)
    chg = pos.diff().abs().fillna(pos.abs())
    net = gross - chg * cost_bps / 2e4          # maliyet: pozisyon degisim gununde
    # islem listesi
    trades = []
    i = 0
    pv = pos.values
    while i < n:
        if pv[i] > 0 and (i == 0 or pv[i - 1] == 0):
            j = i
            while j + 1 < n and pv[j + 1] > 0:
                j += 1
            ex = j + 1                               # cikis gunu indeksi (uzlasma)
            closed = ex < n
            lr = np.nansum(rv[i + 1: min(ex, n - 1) + 1])
            trades.append(dict(entry=idx[i], exit=idx[ex] if closed else pd.NaT, days=(min(ex, n - 1) - i), closed=closed,
                               n_sig=int(sv[i:j + 1].sum()), gross=np.exp(lr) - 1, net=np.exp(lr) - 1 - cost_bps / 1e4))
            i = j + 1
        else:
            i += 1
    return pd.DataFrame(trades), net, pos


def alpha_vs_bh(p, bh, L=5):
    d = pd.concat([p.rename("p"), bh.rename("b")], axis=1).dropna()
    m = sm.OLS(d.p.values, sm.add_constant(d.b.values)).fit(cov_type="HAC", cov_kwds={"maxlags": L})
    return dict(alpha_ann=m.params[0] * 252 * 100, t=m.tvalues[0], beta=m.params[1])
