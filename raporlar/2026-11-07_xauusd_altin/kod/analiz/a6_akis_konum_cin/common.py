"""a6_akis_konum_cin ortak yardımcılar.
Aile: konumlanma (CFTC COT), akış (VİOP OI/hacim, Çin altın ETF hacmi), Asya/Çin (SHFE primi, Asya endeksleri, Çin altın hisseleri), GPR.
Tüm öngörücüler gün t 15:00 UTC'den önce bilinir (her betikte bilgi zamanı yazılı). Hedef: VİOP fwd{h} (t uzlaşması -> t+h uzlaşması).
"""
import os, sys, json, warnings
warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
sys.path.insert(0, f"{S}/code")
from lib_altin import *  # noqa
from lib_altin import IS_END, COST_BPS

AG = "a6_akis_konum_cin"
OUT = f"{S}/out/{AG}"
os.makedirs(OUT, exist_ok=True)
HS = (1, 3, 5, 10)

D = load_viop()
R = D["v_ret"]                       # VİOP aktif kontrat uzlaşma getirisi (aynı kontrat içinde)
SP = load_spot()                     # 2010+ spot paneli (15:00->15:00 UTC)

# --- sağlamlık maskeleri
ROLL = (D["v_code"] != D["v_code"].shift(1))                       # aktif kontrat değişim günü
ROLL_NEAR = ROLL | ROLL.shift(-1, fill_value=False) | ROLL.shift(1, fill_value=False)
EXTREME = ((D.index >= "2020-03-01") & (D.index <= "2020-04-30")) | ((D.index >= "2026-01-01") & (D.index <= "2026-02-28"))
EXTREME = pd.Series(EXTREME, index=D.index)


def zroll(x, w, minp=None):
    m = x.rolling(w, min_periods=minp or int(w * 0.8)).mean(); s = x.rolling(w, min_periods=minp or int(w * 0.8)).std()
    return (x - m) / s


def T(x, fam, tid, desc, hs=HS, note="", y_mask=None, reg=True):
    """IC testi (Spearman, NW lag>=max(h,5)) + kayıt. y_mask: True olan günleri (sinyal günü t) dışla."""
    rows = []
    for h in hs:
        y = D[f"fwd{h}"].copy()
        xx = x.reindex(D.index).copy()
        if y_mask is not None:
            xx[y_mask.reindex(D.index).fillna(False).values] = np.nan
        st = split_stats(xx, y, h)
        if reg:
            register(AG, fam, tid, desc, h, st, note)
        rows.append(dict(family=fam, test_id=tid, predictor=desc, h=h, n=st["n"], ic=st["ic"], t=st["t"], ic_is=st["ic_is"], t_is=st["t_is"],
                         ic_oos=st["ic_oos"], t_oos=st["t_oos"], yrs_same=f'{st["yrs_same_sign"]}/{st["yrs"]}', by_year=st["by_year"], note=note))
    return rows


def T_early(x_spot, fam, tid, desc, hs=(1, 3, 5, 10), note="", start="2010-01-01", end="2016-12-31", reg=True):
    """Spot panelde 2010-2016 erken dönem tekrar: hedef sfwd{h} (15:00->15:00 UTC spot)."""
    rows = []
    for h in hs:
        y = SP[f"sfwd{h}"]
        msk = (SP.index >= start) & (SP.index <= end)
        st = ic(x_spot[msk], y[msk], max(h, 5))
        d = pd.concat([x_spot[msk].rename("x"), y[msk].rename("y")], axis=1).dropna()
        yr = d.groupby(d.index.year).apply(lambda g: g.x.corr(g.y, method="spearman") if len(g) > 20 else np.nan)
        st2 = dict(ic=st["ic"], t=st["t"], n=st["n"], yrs_same_sign=int((np.sign(yr) == np.sign(st["ic"])).sum()), yrs=int(yr.notna().sum()))
        if reg:
            register(AG, fam + "_early", tid + "_early", desc + " [spot 2010-2016]", h, st2, note)
        rows.append(dict(family=fam + "_early", test_id=tid, predictor=desc, h=h, n=st["n"], ic=st["ic"], t=st["t"], yrs_same=f'{st2["yrs_same_sign"]}/{st2["yrs"]}'))
    return rows


def legs(pos, h, ret=None, cost=COST_BPS):
    """Strateji + uzun/kısa bacak + buy&hold, IS/OOS, ham ve demeaned net Sharpe."""
    ret = R if ret is None else ret
    out = {}
    for nm, p in [("LS", pos), ("long_leg", pos.clip(lower=0)), ("short_leg", pos.clip(upper=0))]:
        out[nm] = bt_summary(p, ret, h, cost)
    out["buyhold"] = {k: bt_summary(pd.Series(1.0, index=ret.index), ret, 1, 0)[k] for k in ("full", "is", "oos")}
    return out


def legs_table(pos, h, label, ret=None):
    rows = []
    for cost in (COST_BPS, 10.0):
        o = legs(pos, h, ret, cost)
        for leg in (("LS", "long_leg", "short_leg", "buyhold") if cost == COST_BPS else ("LS", "long_leg", "short_leg")):
            for per in ("full", "is", "oos"):
                r = o[leg][per]
                rows.append(dict(rule=label, h=h, cost_bps=cost if leg != "buyhold" else 0, leg=leg, period=per, sharpe=r["sharpe"], sharpe_dm=r["sharpe_demeaned"],
                                 ann_pct=r["ann"], hit=r["hit"], turnover=r["turnover"], exposure=r["exposure"]))
    return pd.DataFrame(rows)


def yearly_pnl(pos, h, ret=None, cost=COST_BPS):
    ret = R if ret is None else ret
    b = backtest(pos, ret, h, cost)
    if b is None: return None
    p = b["pnl"]
    return p.groupby(p.index.year).agg(lambda s: s.mean() / s.std() * np.sqrt(252) if s.std() > 0 else np.nan).round(2)


def save(rows, name):
    df = pd.DataFrame(rows)
    if "by_year" in df: df["by_year"] = df["by_year"].astype(str)
    df.to_csv(f"{OUT}/{name}.csv", index=False)
    return df


def show(df, cols=("test_id", "h", "n", "ic", "t", "t_is", "t_oos", "yrs_same")):
    c = [x for x in cols if x in df.columns]
    with pd.option_context("display.width", 250, "display.max_rows", 500):
        print(df[c].round(3).to_string(index=False))


def rule_stats(pos, h, y=None, demean=False):
    """Kural için: aktif günlerde pos_t × fwd_h ortalaması (bps) ve NW t (lag=max(h,5)) — tam/IS/OOS, yıllık işaret.
    demean=True: fwd_h'den tam örneklem ortalaması (drift) çıkarılır."""
    y = D[f"fwd{h}"] if y is None else y
    if demean: y = y - y.mean()
    z = (pos.reindex(y.index) * y).where(pos.reindex(y.index).fillna(0) != 0).dropna()
    def one(s):
        if len(s) < 20: return (np.nan, np.nan, len(s))
        r = nw_ols(s, pd.Series(1.0, index=s.index, name="c"), lags=max(h, 5), add_const=False)
        return (s.mean() * 1e4, r["t"], len(s))
    f = one(z); i = one(z[z.index <= IS_END]); o = one(z[z.index > IS_END])
    yr = z.groupby(z.index.year).mean()
    same = int((np.sign(yr) == np.sign(f[0])).sum())
    return dict(ic=f[0], t=f[1], n=f[2], ic_is=i[0], t_is=i[1], ic_oos=o[0], t_oos=o[1], yrs_same_sign=same, yrs=int(yr.notna().sum()),
                by_year=(yr * 1e4).round(1).to_dict())


def snap_h(sym, days, hour_utc, max_stale_h=2):
    """Dukascopy saatlik: gün D'nin hour_utc:00 fiyatı (bar kapanışı = bar_start+1h), en fazla max_stale_h saat bayat."""
    h = hourly(sym)
    s = h["c"].copy(); s.index = (pd.DatetimeIndex(h.index).tz_convert("UTC") if h.index.tz is not None else pd.DatetimeIndex(h.index).tz_localize("UTC")) + pd.Timedelta(hours=1)
    s = s.sort_index()
    days = pd.DatetimeIndex(days)
    targ = days.tz_localize("UTC") + pd.Timedelta(hours=hour_utc)
    idx = s.index.searchsorted(targ, side="right") - 1
    vals = np.where(idx >= 0, s.values[np.clip(idx, 0, None)], np.nan)
    ts = s.index[np.clip(idx, 0, None)]
    stale = (targ - ts) / pd.Timedelta(hours=1)
    vals = np.where((idx >= 0) & (stale <= max_stale_h), vals, np.nan)
    return pd.Series(vals, index=days)
