"""Hakem (adversarial) ortak: analist kütüphanesinden BAĞIMSIZ sinyal/backtest yeniden kurulumu."""
import numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
IS_END = pd.Timestamp("2021-12-31")
d = pd.read_parquet(f"{S}/panel/panel_viop.parquet"); d.index = pd.to_datetime(d.index)
s = pd.read_parquet(f"{S}/panel/panel_spot.parquet"); s.index = pd.to_datetime(s.index)
r_v = d.v_ret.astype(float)
lp = np.log(s.s_p15.astype(float)); r_s = lp.diff()

def exp_pct(x, minp=250):
    v = x.values; out = np.full(len(v), np.nan); hist = []
    import bisect
    srt = []
    for i, xi in enumerate(v):
        if np.isfinite(xi):
            bisect.insort(srt, xi)
            if len(srt) >= minp:
                out[i] = bisect.bisect_right(srt, xi) / len(srt)
    return pd.Series(out, index=x.index)

def asof_to_viop(x, maxdays=4):
    """spot takvimli seriyi VİOP günlerine: aynı gün varsa o gün, yoksa son spot günü (<=maxdays takvim günü)."""
    x = x.sort_index()
    pos = x.index.searchsorted(d.index, side="right") - 1
    ok = pos >= 0
    vals = np.where(ok, x.values[np.clip(pos, 0, None)], np.nan)
    age = (d.index - x.index[np.clip(pos, 0, None)]).days
    vals = np.where(ok & (np.asarray(age) <= maxdays), vals, np.nan)
    return pd.Series(vals, index=d.index)

def lowmom_spot(k=5, rvwin=20, thr=1/3, qmin=250, mode="lo"):
    rv = r_s.rolling(rvwin).std()
    q = exp_pct(rv, qmin)
    sg = np.sign(lp - lp.shift(k))
    if mode == "lo":
        p = sg.where(q < thr, 0.0)
    elif mode == "hi_rev":
        p = (-sg).where(q > thr, 0.0)
    elif mode == "volreg":
        p = pd.Series(np.where(q < 1/3, sg, np.where(q > 2/3, -sg, 0.0)), index=sg.index)
    return p.where(q.notna() & sg.notna()), q

def bt(pos, ret, h=1, cost=5.0, demean=False, demean_mode="full"):
    """kademeli h alt portföy; maliyet |Δeff| * cost/2 (analistle aynı netleşmeli tanım)."""
    r = ret.astype(float).copy()
    if demean:
        if demean_mode == "full": r = r - r.mean()
        elif demean_mode == "year": r = r - r.groupby(r.index.year).transform("mean")
        elif demean_mode == "trail250": r = r - r.rolling(250, min_periods=120).mean().shift(1)
    p = pos.reindex(r.index).fillna(0).clip(-1, 1)
    eff = sum(p.shift(j).fillna(0) for j in range(h)) / h
    gross = eff.shift(1) * r
    turn = (eff - eff.shift(1).fillna(0)).abs()
    c = turn.shift(1).fillna(0) * cost / 2 / 1e4
    net = (gross - c).dropna()
    return net

def sh(net):
    net = net.dropna()
    if len(net) < 30 or net.std() == 0: return np.nan
    return net.mean() / net.std() * np.sqrt(252)

def tstat(net):
    net = net.dropna(); return net.mean() / (net.std() / np.sqrt(len(net)))

def nw_t(net, L=5):
    import statsmodels.api as sm
    y = net.dropna().values
    m = sm.OLS(y, np.ones(len(y))).fit(cov_type="HAC", cov_kwds={"maxlags": L})
    return float(m.tvalues[0])

PER = {"2017-19": ("2017-01-01", "2019-12-31"), "2020-21": ("2020-01-01", "2021-12-31"), "2022-23": ("2022-01-01", "2023-12-31"), "2024-26": ("2024-01-01", "2026-12-31"),
       "IS": ("2017-01-01", "2021-12-31"), "OOS": ("2022-01-01", "2026-12-31"), "FULL": ("2017-01-01", "2026-12-31")}
