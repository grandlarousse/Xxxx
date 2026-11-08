"""Hakem (adv) ortak: panel, takvim maskeleri, NW t, backtest."""
import numpy as np, pandas as pd, statsmodels.api as sm, warnings
warnings.filterwarnings("ignore")
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
O = f"{S}/out/e1_etf_zaman_takvim_adv"
d = pd.read_parquet(f"{S}/panel/panel_etf.parquet"); d.index = pd.to_datetime(d.index); idx = d.index
IS_END = pd.Timestamp("2017-12-31")

def yahoo(t):
    y = pd.read_parquet(f"{S}/panel/yahoo/{t}.parquet"); y.index = pd.to_datetime(y.index); return y

UNSCHED = pd.DatetimeIndex(["1985-09-27", "1994-04-27", "2001-09-11", "2001-09-12", "2001-09-13", "2001-09-14", "2004-06-11",
                            "2007-01-02", "2012-10-29", "2012-10-30", "2018-12-05", "2025-01-09"])

def cal_masks(IDX):
    ix = pd.Series(IDX, index=IDX)
    ym = ix.dt.to_period("M"); first = ym != ym.shift(1); last = ym != ym.shift(-1)
    bd = pd.bdate_range(IDX.min(), IDX.max()); hol = bd.difference(IDX).difference(UNSCHED)
    nxt = ix.shift(-1)
    hv = hol.values
    pre = []
    for a, b in zip(IDX.values, nxt.values):
        if pd.isna(b): pre.append(False); continue
        j = np.searchsorted(hv, a, side="right"); pre.append(bool(j < len(hv) and hv[j] < b))
    pre = pd.Series(pre, index=IDX)
    pos_in_m = ix.groupby(ym).cumcount() + 1; pos_end = ix.groupby(ym).cumcount(ascending=False) + 1
    return dict(first=first, last=last, pre=pre, pos_in_m=pos_in_m, pos_end=pos_end)

def nwt(y, x, L=5):
    dd = pd.concat([pd.Series(y, name="y"), pd.Series(x, name="x")], axis=1).dropna()
    if len(dd) < 30 or dd.x.std() == 0: return np.nan, np.nan, len(dd)
    m = sm.OLS(dd.y, sm.add_constant(dd.x)).fit(cov_type="HAC", cov_kwds={"maxlags": L})
    return float(m.params["x"]), float(m.tvalues["x"]), len(dd)

def ev(mask_day, r, start=None, end=None, L=5):
    """mask_day: getiri günü (D) maskesi. r: log getiri (D-1 kapanış -> D kapanış). Dönüş: olay ort bps, diğer bps, t, n."""
    x = mask_day.reindex(r.index).fillna(False).astype(float)
    dd = pd.concat([r.rename("y"), x.rename("x")], axis=1).dropna()
    if start is not None: dd = dd[dd.index >= pd.Timestamp(start)]
    if end is not None: dd = dd[dd.index <= pd.Timestamp(end)]
    b, t, n = nwt(dd.y, dd.x, L)
    on = dd.y[dd.x == 1]; off = dd.y[dd.x == 0]
    return dict(n_ev=int(len(on)), ev_bps=round(on.mean() * 1e4, 1), oth_bps=round(off.mean() * 1e4, 1), t=round(t, 2), hit=round((on > 0).mean(), 3),
                med_bps=round(on.median() * 1e4, 1))

def bt_day(mask_day, r_log, cost_rt_bps):
    """getiri günü maskesinde (önceki kapanışta al, D kapanışında sat) uzun; basit getiri, maliyet her gidiş-dönüş tam RT (ardışık günlerde birleşik)."""
    m = mask_day.reindex(r_log.index).fillna(False).astype(float)
    rs = np.expm1(r_log)
    turn = (m - m.shift(1).fillna(0)).abs()     # pozisyon değişimi (D-1 kapanışındaki giriş D'nin m'sine yansır)
    net = m * rs - turn * cost_rt_bps / 2e4
    return net.dropna()

def perf(p):
    p = p.dropna()
    if len(p) < 50: return dict(sh=np.nan, ann=np.nan)
    a = p.mean() * 252; v = p.std() * np.sqrt(252)
    return dict(sh=round(a / v, 2), ann=round(a * 100, 2))
