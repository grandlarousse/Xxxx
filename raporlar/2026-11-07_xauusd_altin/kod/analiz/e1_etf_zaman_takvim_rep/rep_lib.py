"""Bağımsız yeniden üretim — e1_etf_zaman_takvim (ETF/Midas cephesi).
lib_altin / e1_common KULLANILMAZ. Ham Yahoo günlük OHLC + exchange_calendars XNYS takvimi.
Zaman: giriş = gün t ABD kapanışı; çıkış = t+h kapanışı. Karar anı = gün t 15:00 ET.
IS = ilk veri..2017-12-31, OOS = 2018-01-01.., ayrıca 2022+.
"""
import json, numpy as np, pandas as pd
import exchange_calendars as xc

S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
OUT = f"{S}/out/e1_etf_zaman_takvim_rep"
IS_END = pd.Timestamp("2017-12-31")
OOS_START = pd.Timestamp("2018-01-01")
P22 = pd.Timestamp("2022-01-01")
START, END = "2008-01-02", "2026-11-06"

# ---------------- takvim (bağımsız kaynak: exchange_calendars XNYS) ----------------
CAL = xc.get_calendar("XNYS", start="2006-01-01", end="2027-12-31")
SESS = CAL.sessions_in_range(START, END)
SESS = pd.DatetimeIndex(SESS.tz_localize(None) if SESS.tz is not None else SESS)


def regular_holidays():
    """XNYS düzenli tatilleri (hafta içi, gözlemlenen tarih) + adları."""
    rows = []
    for rule in CAL.regular_holidays.rules:
        for d in rule.dates(pd.Timestamp("2007-12-01"), pd.Timestamp("2027-01-31")):
            if d.dayofweek < 5:
                rows.append((pd.Timestamp(d), rule.name))
    h = pd.DataFrame(rows, columns=["date", "name"]).drop_duplicates("date").sort_values("date").set_index("date")
    # takvim tatili olarak işaretli ama aslında seans olan günleri at (güvenlik)
    h = h[~h.index.isin(SESS)]
    return h


def adhoc_closures():
    return pd.DatetimeIndex([pd.Timestamp(x).tz_localize(None) if getattr(pd.Timestamp(x), "tz", None) else pd.Timestamp(x)
                             for x in CAL.adhoc_holidays])


def early_closes():
    e = CAL.early_closes
    e = pd.DatetimeIndex(e.tz_localize(None) if getattr(e, "tz", None) is not None else e)
    return e[(e >= START) & (e <= END)]


# ---------------- fiyat verisi (ham Yahoo) ----------------
def yahoo(t):
    y = pd.read_parquet(f"{S}/panel/yahoo/{t}.parquet")
    y.index = pd.to_datetime(y.index)
    return y


def adj_on_sessions(t):
    """adjclose, XNYS seanslarına reindex. Eksik gün NaN kalır (getiri ardışık seans dışında hesaplanmaz)."""
    y = yahoo(t)
    return y["adjclose"].reindex(SESS)


def logret(t):
    a = adj_on_sessions(t)
    return np.log(a).diff()          # gün t-1 kapanış -> gün t kapanış; önceki seans eksikse NaN


def fwd_log(r, h):
    """t kapanışından t+h kapanışına log getiri (r_{t+1}+...+r_{t+h})."""
    return sum(r.shift(-k) for k in range(1, h + 1))


# ---------------- Newey-West (kendi uygulaması, Bartlett) ----------------
def nw_ols(y, X, L, add_const=True, small=True):
    """y ~ X (+sabit). Bartlett çekirdekli HAC kovaryans, lag L. small=True: n/(n-k) düzeltmesi.
    Döndür: (beta, t) — beta/t vektörleri (sabit varsa ilk eleman sabit)."""
    y = np.asarray(y, float)
    X = np.asarray(X, float)
    if X.ndim == 1: X = X[:, None]
    if add_const: X = np.column_stack([np.ones(len(y)), X])
    n, k = X.shape
    XtX_inv = np.linalg.inv(X.T @ X)
    b = XtX_inv @ X.T @ y
    u = y - X @ b
    g = X * u[:, None]
    Sm = g.T @ g
    for l in range(1, L + 1):
        w = 1 - l / (L + 1)
        G = g[l:].T @ g[:-l]
        Sm += w * (G + G.T)
    V = XtX_inv @ Sm @ XtX_inv
    if small: V *= n / (n - k)
    se = np.sqrt(np.diag(V))
    return b, b / se


def dummy_test(x, y, L, start=None):
    """x (0/1 ya da sürekli) ~ y, NW t; tam/IS/OOS/2022+; yıllık korelasyon işareti; Pearson IC."""
    d = pd.concat([pd.Series(x, name="x"), pd.Series(y, name="y")], axis=1).dropna()
    if start is not None: d = d[d.index >= start]
    def tt(q):
        if len(q) < 40 or q.x.std() == 0: return np.nan, np.nan
        b, t = nw_ols(q.y.values, q.x.values, L)
        return b[1], t[1]
    b_f, t_f = tt(d); _, t_i = tt(d[d.index <= IS_END]); b_o, t_o = tt(d[d.index >= OOS_START]); _, t_2 = tt(d[d.index >= P22])
    ic = d.x.corr(d.y)
    yr = d.groupby(d.index.year).apply(lambda g: g.x.corr(g.y) if (len(g) > 20 and g.x.std() > 0) else np.nan)
    same = int((np.sign(yr.dropna()) == np.sign(ic)).sum())
    ev = d.y[d.x == 1]; ot = d.y[d.x == 0]
    return dict(n=len(d), n_ev=int((d.x == 1).sum()), ic=ic, b_bps=b_f * 1e4, t=t_f, t_is=t_i, t_oos=t_o, t_22=t_2,
                yrs=f"{same}/{int(yr.notna().sum())}", ev_bps=ev.mean() * 1e4, oth_bps=ot.mean() * 1e4,
                ev_oos_bps=ev[ev.index >= OOS_START].mean() * 1e4, hit=(ev > 0).mean())


# ---------------- backtest (kendi uygulaması) ----------------
def bt(pos, rs, h=1, cost_rt=10.0):
    """pos_t: gün t kapanışında alınan hedef ağırlık [0,1] (ya da ters ETF ağırlığı), h gün tutulur (1/h kademeli).
    rs: o ETF'in basit günlük getirisi (t-1 -> t). Getiri: eff_{t-1}*rs_t. Maliyet: |eff_{t-1}-eff_{t-2}|*cost/2 bps, gün t'de düşülür.
    Döndür: net günlük P&L (rs mevcut günlerde), devir (|Δeff|)."""
    pos = pos.reindex(SESS).fillna(0.0)
    eff = sum(pos.shift(k).fillna(0.0) for k in range(h)) / h
    turn = (eff - eff.shift(1).fillna(0.0)).abs()
    gross = eff.shift(1).fillna(0.0) * rs.fillna(0.0)
    cost = turn.shift(1).fillna(0.0) * cost_rt / 2e4
    valid = rs.notna()
    return (gross - cost)[valid], turn[valid]


def perf(p, turn=None):
    p = p.dropna()
    if len(p) < 50: return dict(sh=np.nan, ann=np.nan, vol=np.nan, mdd=np.nan, n=len(p), rt_yr=np.nan)
    ann = p.mean() * 252; vol = p.std() * np.sqrt(252)
    w = (1 + p).cumprod(); mdd = (w / w.cummax() - 1).min()
    o = dict(sh=ann / vol if vol > 0 else np.nan, ann=ann * 100, vol=vol * 100, mdd=mdd * 100, n=len(p))
    o["rt_yr"] = turn.reindex(p.index).sum() / len(p) * 252 / 2 if turn is not None else np.nan
    return o


def per(s, k):
    if k == "full": return s
    if k == "is": return s[s.index <= IS_END]
    if k == "oos": return s[s.index >= OOS_START]
    if k == "p22": return s[s.index >= P22]
    raise KeyError(k)


PERIODS = ["full", "is", "oos", "p22"]


def demeaned_sharpe(pos, rl, h, cost_rt, k, how="period_log"):
    """Drift çıkarılmış: hedef getiriden ortalama çıkarılır, yalnız uzun pozisyonla backtest.
    how='period_log': analistin yöntemi (dönem içi log getiri ortalaması, dönem dilimlendikten sonra);
    how='full_simple': tam örneklem basit getiri ortalaması."""
    if how == "period_log":
        r = per(rl.dropna(), k); r = r - r.mean()
        rr = pd.Series(np.nan, index=SESS); rr.loc[r.index] = r.values
        net, tr = bt(pos, rr, h, cost_rt)
        return perf(per(net, k), tr)["sh"]
    else:
        rs = np.expm1(rl); r = rs - rs.dropna().mean()
        net, tr = bt(pos, r, h, cost_rt)
        return perf(per(net, k), tr)["sh"]
