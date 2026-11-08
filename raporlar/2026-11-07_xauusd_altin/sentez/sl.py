"""Sentez kütüphanesi: ayakta kalan sinyallerin pozisyon serileri (analist tanımlarıyla birebir), kademeli backtest, dönem özetleri.
VİOP: giriş gün t uzlaşması, hedef v_ret (aktif kontrat, aynı kontrat içi), maliyet 5 bps gidiş-dönüş (stres 10).
ETF : giriş gün t ABD kapanışı, hedef log(c_t+1/c_t) (adjclose), maliyet 10 bps gidiş-dönüş (stres 20), yalnız uzun.
"""
import sys, numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
sys.path.insert(0, f"{S}/code"); sys.path.insert(0, f"{S}/out/e2_etf_leadlag")
P = f"{S}/panel"
V_IS_END = pd.Timestamp("2021-12-31"); E_IS_END = pd.Timestamp("2017-12-31")

V = pd.read_parquet(f"{P}/panel_viop.parquet"); V.index = pd.to_datetime(V.index)
SP = pd.read_parquet(f"{P}/panel_spot.parquet"); SP.index = pd.to_datetime(SP.index)
E = pd.read_parquet(f"{P}/panel_etf.parquet"); E.index = pd.to_datetime(E.index)
HALF_TR = pd.to_datetime(pd.read_csv(f"{S}/out/a1_zaman_serisi_rep/half_days.csv", header=None)[0].iloc[1:].values)
RV = V.v_ret.astype(float)


def us_half_days():
    import exchange_calendars as xc
    c = xc.get_calendar("XNYS", start="2008-01-01", end="2026-12-31")
    sch = c.schedule
    cl = sch["close"].dt.tz_convert("America/New_York")
    return pd.DatetimeIndex(sch.index[cl.dt.hour < 16]).tz_localize(None)


def nyse_sessions(end="2026-12-31"):
    import exchange_calendars as xc
    c = xc.get_calendar("XNYS", start="2008-01-01", end=end)
    return pd.DatetimeIndex(c.sessions).tz_localize(None)


HALF_US = us_half_days()


def eff_of(pos, h):
    pos = pos.fillna(0).clip(-1, 1)
    return sum(pos.shift(k).fillna(0) for k in range(h)) / h


def bt_eff(eff, r, cost_bps, demean=False, simple=True):
    """eff: gün t kapanışından sonra taşınan netleştirilmiş pozisyon; kazanç = eff_{t-1} * r_t; maliyet |Δeff| * cost/2.
    r log getiri olarak verilir; simple=True ise sabit nominalli pozisyonun gerçek P&L'i için basit getiriye (e^r − 1) çevrilir."""
    r = r.astype(float).copy()
    if simple: r = np.expm1(r)
    if demean: r = r - r.mean()
    eff = eff.reindex(r.index).fillna(0)
    gross = eff.shift(1) * r
    turn = (eff - eff.shift(1).fillna(0)).abs()
    cost = turn.shift(1).fillna(0) * cost_bps / 2 / 1e4
    net = (gross - cost).dropna()
    return net, turn.reindex(net.index)


def per_stats(net, turn=None):
    if len(net) < 30 or net.std() == 0: return dict(sharpe=np.nan, ann=np.nan, t=np.nan, n=len(net))
    ann = net.mean() * 252; vol = net.std() * np.sqrt(252)
    return dict(sharpe=round(ann / vol, 2), ann_pct=round(ann * 100, 2), vol_pct=round(vol * 100, 2), t=round(net.mean() / net.std() * np.sqrt(len(net)), 2),
                n=len(net), turn_yr=None if turn is None else round(turn.sum() / len(net) * 252, 1))


def periods(front):
    if front == "VIOP":
        return [("tam", None, None), ("IS", None, V_IS_END), ("OOS", V_IS_END + pd.Timedelta(days=1), None), ("2022+", pd.Timestamp("2022-01-01"), None), ("2026", pd.Timestamp("2026-01-01"), None)]
    return [("tam", None, None), ("IS", None, E_IS_END), ("OOS", E_IS_END + pd.Timedelta(days=1), None), ("2022+", pd.Timestamp("2022-01-01"), None), ("2026", pd.Timestamp("2026-01-01"), None)]


def cut(x, a, b):
    if a is not None: x = x[x.index >= a]
    if b is not None: x = x[x.index <= b]
    return x


def summarize(pos, r, h, cost, front, simple=True):
    """Analist yöntemi: dönem başına pozisyon ve getiri dilimlenip kademeli backtest; ham, drift çıkarılmış, stres maliyet; B&H."""
    out = {}
    for nm, a, b in periods(front):
        rr = cut(r.dropna(), a, b); pp = pos.reindex(rr.index)
        net, turn = bt_eff(eff_of(pp, h), rr, cost, simple=simple)
        dm, _ = bt_eff(eff_of(pp, h), rr, cost, demean=True, simple=simple)
        st, _ = bt_eff(eff_of(pp, h), rr, cost * 2, simple=simple)
        bh, _ = bt_eff(pd.Series(1.0, index=rr.index), rr, 0, simple=simple)
        s = per_stats(net, turn)
        out[nm] = dict(sharpe=s["sharpe"], ann_pct=s.get("ann_pct"), t=s["t"], sharpe_dm=per_stats(dm)["sharpe"], sharpe_stres=per_stats(st)["sharpe"],
                       bh_sharpe=per_stats(bh)["sharpe"], bh_ann_pct=per_stats(bh).get("ann_pct"), turn_yr=s.get("turn_yr"),
                       expo=round(float(eff_of(pp, h).abs().mean()), 3))
    return out


# ------------------------------------------------------------------ VİOP sinyalleri
def sig_lowmom(k=5, rvwin=20, lo=1 / 3):
    """A1-LOWMOM: q = rv20'nin 2010'dan beri genişleyen yüzdeliği (bugün dahil, min 250); q<1/3 iken sign(ln P_t/P_{t-k}). Spot takviminde."""
    lp = np.log(SP.s_p15); r = lp.diff(); rv = r.rolling(rvwin).std()
    v = rv.values; q = np.full(len(v), np.nan); hist = []
    for i, xi in enumerate(v):
        if np.isfinite(xi):
            hist.append(xi)
            if len(hist) >= 250: q[i] = (np.asarray(hist) <= xi).mean()
    q = pd.Series(q, index=SP.index)
    sg = np.sign(lp - lp.shift(k))
    p = pd.Series(np.where(q < lo, sg, 0.0), index=SP.index).where(q.notna() & sg.notna())
    return p, q, rv * np.sqrt(252)


def to_viop(x):
    out = x.reindex(V.index)
    miss = ~V.index.isin(x.index)
    if miss.any():
        pos = x.index.searchsorted(V.index[miss], side="right") - 1
        out[miss] = np.where(pos >= 0, x.values[np.clip(pos, 0, None)], np.nan)
    return out


def sig_qend():
    """A3_QEND: Mar/Haz/Eyl/Ara'nın sondan 2. VİOP işlem günü uzun, h=3."""
    idx = V.index; ym = idx.to_period("M")
    s = pd.Series(idx, index=idx)
    p = pd.Series(0.0, index=idx)
    for m, g in s.groupby(ym):
        if m.month in (3, 6, 9, 12) and len(g) >= 2:
            # ay tamamlanmış olmalı (son ay eksikse atla)
            if g.index[-1] == idx[-1] and m == idx[-1].to_period("M"): continue
            p[g.index[-2]] = 1.0
    return p


def sig_gdxj_res_viop():
    """A4-C1: e = r_GDXJ − β60·r_GLD (y_* = cutoff'tan önce bilinen son ABD kapanışı, VİOP satırlarında diff), z = e/std120 (geçmiş), |z|>0,43."""
    rm = np.log(V.y_GDXJ).diff(); rg = np.log(V.y_GLD).diff()
    b = rm.rolling(60, min_periods=40).cov(rg).shift(1) / rg.rolling(60, min_periods=40).var().shift(1)
    e = rm - b * rg
    z = e / e.rolling(120, min_periods=60).std().shift(1)
    p = np.sign(z).where(z.abs() > 0.43, 0.0).where(z.notna(), 0.0)
    return p, z


def sig_last1h():
    """A8-3: sign(ln p15/p14), h=5; Türkiye yarım günleri dışlandı."""
    x = np.log(V.xau_p15 / V.xau_p14)
    p = np.sign(x).fillna(0.0)
    p[p.index.isin(HALF_TR)] = 0.0
    return p, x


def sig_trend_pma50():
    lp = np.log(SP.s_p15); ma = SP.s_p15.rolling(50).mean()
    return pd.Series(np.where(SP.s_p15 > ma, 1.0, -1.0), index=SP.index).where(ma.notna())


# ------------------------------------------------------------------ ETF sinyalleri
def ret_of(t):
    c = E[f"c_{t}"].astype(float); r = np.log(c).diff(); r[c.isna() | c.shift(1).isna()] = np.nan
    return r


def roll_beta2(y, X, win=250, minp=60):
    Xv = X.values; yv = y.values; n, k = Xv.shape; B = np.full((n, k), np.nan)
    for i in range(n):
        lo = max(0, i - win + 1); xx = Xv[lo:i + 1]; yy = yv[lo:i + 1]
        m = np.isfinite(yy) & np.all(np.isfinite(xx), axis=1)
        if m.sum() < minp: continue
        A = np.column_stack([np.ones(m.sum()), xx[m]])
        B[i] = np.linalg.lstsq(A, yy[m], rcond=None)[0][1:]
    return pd.DataFrame(B, index=X.index, columns=X.columns)


_RES = {}


def miner_resid(y):
    """e2 s1: e_t = r_Y,t − β_{t-1}·[r_GLD, r_SPY], β 250 günlük yuvarlanan OLS (minp 60)."""
    if y in _RES: return _RES[y]
    R = {t: ret_of(t) for t in [y, "GLD", "SPY"]}
    X = pd.concat([R["GLD"], R["SPY"]], axis=1); X.columns = ["GLD", "SPY"]
    B = roll_beta2(R[y], X, 250, 60).shift(1)
    e = R[y] - B["GLD"] * R["GLD"] - B["SPY"] * R["SPY"]
    _RES[y] = e
    return e


def pos_tail(x, q, is_end=E_IS_END):
    xi = x[x.index <= is_end].dropna(); hi = xi.quantile(q); lo = xi.quantile(1 - q)
    p = pd.Series(0.0, index=x.index); p[x > hi] = 1.0; p[x < lo] = -1.0; p[x.isna()] = 0.0
    return p, hi, lo


def sig_e2(y, k, q):
    e = miner_resid(y); x = e.rolling(k, min_periods=k).sum().shift(1)
    p, hi, lo = pos_tail(x, q)
    return p, x, hi, lo


def sig_m():
    """E3-1: m_t = ln(xau_cut_t / xau_close_{t-1}); m<0 ise GDXJ uzun h=1. ABD yarım günleri dışlandı."""
    m = np.log(E.xau_cut) - np.log(E.xau_close.shift(1))
    p = (m < 0).astype(float).where(m.notna(), 0.0)
    p[p.index.isin(HALF_US)] = 0.0
    return p, m


def sig_gdx_tatil():
    """E1-C2: NYSE tatilinden önceki son işlem günü (olay günü) GDX'te; giriş bir önceki kapanış, h=1 (yalnız uzun)."""
    ses = nyse_sessions()
    import exchange_calendars as xc
    c = xc.get_calendar("XNYS", start="2008-01-01", end="2026-12-31")
    hol = pd.DatetimeIndex(c.regular_holidays.holidays(start="2008-01-01", end="2026-12-31"))
    adh = pd.DatetimeIndex([x for x in c.adhoc_holidays if pd.Timestamp("2008-01-01") <= x <= pd.Timestamp("2026-12-31")]) if c.adhoc_holidays else pd.DatetimeIndex([])
    # olay günü = tatilden (hafta içi düzenli tatil) önceki son seans
    ev = []
    for hd in hol:
        if hd.weekday() >= 5: continue
        prev = ses[ses < hd]
        if len(prev): ev.append(prev[-1])
    ev = pd.DatetimeIndex(sorted(set(ev)))
    p = pd.Series(0.0, index=ses)
    for d0 in ev:
        prev = ses[ses < d0]
        if len(prev): p[prev[-1]] = 1.0  # giriş günü
    return p, ev
