"""e3_etf_akis_prim ortak yardımcılar (ETF akışları, prim/iskonto, kaldıraçlı ETF dengelemesi).
Bu cephede IS = 2008..2017, OOS = 2018..2026-11; ayrıca 2022+ alt dönemi.
Hedef: ABD kapanışından kapanışına (16:00 ET) log getiri toplamı, h NYSE günü.
"""
import os, sys, json, numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
sys.path.insert(0, f"{S}/code")
import lib_altin
from lib_altin import fwd, ic, split_stats, nw_ols, register, placebo_lead
lib_altin.IS_END = pd.Timestamp("2017-12-31")
IS_END = lib_altin.IS_END
SUB_START = pd.Timestamp("2022-01-01")
P = f"{S}/panel"; OUT = f"{S}/out/e3_etf_akis_prim"
AGENT = "e3_etf_akis_prim"
HS = (1, 3, 5)
# Midas maliyetleri (gidiş-dönüş, bps): (temel, stres)
COST = {"plain": (10.0, 20.0), "lev": (20.0, 40.0)}
LEV = {"GLL": 2.0, "DUST": 2.0, "JDST": 2.0, "ZSL": 2.0}   # ters ETF kaldıraçları (DUST/JDST 2020 öncesi -3x; gerçekleşen kaldıraç ayrıca ölçülür)
INV_OF = {"GLD": "GLL", "IAU": "GLL", "GDX": "DUST", "GDXJ": "JDST", "SLV": "ZSL", "PHYS": "GLL"}
EXTREMES = {"2008": ("2008-01-01", "2008-12-31"), "2013-04": ("2013-04-01", "2013-04-30"),
            "2020-03": ("2020-03-01", "2020-03-31"), "2026-01/02": ("2026-01-01", "2026-02-28")}


def load_etf():
    d = pd.read_parquet(f"{P}/panel_etf.parquet"); d.index = pd.to_datetime(d.index); return d


def lr(px):
    return np.log(px).diff()


def sub_ic(x, y, h, start=SUB_START, method="spearman"):
    m = x.index >= start
    return ic(x[m], y[m], max(h, 5), method)


def test(family, test_id, predictor, x, y, h, note="", reg=True, method="spearman"):
    """split_stats + 2022+ IC; kayda geçir. y = ileri getiri (fwd(r,h))."""
    st = split_stats(x, y, h, method)
    s22 = sub_ic(x, y, h, method=method)
    st["ic_22"] = s22["ic"]; st["t_22"] = s22["t"]
    if reg:
        register(AGENT, family, test_id, predictor, h, st, note)
    st.update(family=family, test_id=test_id, predictor=predictor, h=h, note=note)
    return st


def mean_diff_test(family, test_id, predictor, ev, y, h, note="", reg=True):
    """Olay günleri (ev==1) sonrası ortalama ileri getiri − koşulsuz ortalama; NW t (lag>=h). 'ic' alanı bps cinsinden fark."""
    d = pd.concat([ev.rename("e"), y.rename("y")], axis=1).dropna()
    out = {}
    for nm, msk in [("full", slice(None)), ("is", d.index <= IS_END), ("oos", d.index > IS_END), ("22", d.index >= SUB_START)]:
        dd = d.loc[msk] if not isinstance(msk, slice) else d
        if dd.e.sum() < 5 or len(dd) < 50:
            out[nm] = (np.nan, np.nan, int(dd.e.sum())); continue
        r = nw_ols(dd.y, dd.e.astype(float), lags=max(h, 5))
        out[nm] = (r["b"] * 1e4, r["t"], int(dd.e.sum()))
    yr = d[d.e == 1].groupby(d[d.e == 1].index.year).y.mean() - d.groupby(d.index.year).y.mean()
    yr = yr.dropna()
    sgn = np.sign(out["full"][0])
    st = dict(ic=out["full"][0], t=out["full"][1], n=out["full"][2], t_is=out["is"][1], ic_is=out["is"][0], t_oos=out["oos"][1], ic_oos=out["oos"][0],
              ic_22=out["22"][0], t_22=out["22"][1], n_22=out["22"][2],
              yrs_same_sign=int((np.sign(yr) == sgn).sum()), yrs=int(len(yr)), by_year=yr.mul(1e4).round(1).to_dict())
    if reg:
        register(AGENT, family, test_id, predictor, h, st, note + "; ic=olay sonrası ortalama fark (bps)")
    st.update(family=family, test_id=test_id, predictor=predictor, h=h, note=note)
    return st


# ---------------------------------------------------------------- backtest (basit getirilerle, iki enstrümanlı)
def _stagger(pos, h):
    pos = pos.fillna(0).clip(-1, 1)
    return sum(pos.shift(k).fillna(0) for k in range(h)) / h


def bt(pos, r_long, h, cost_long, r_inv=None, L_inv=2.0, cost_inv=20.0, demean=False, mode="long_only"):
    """pos_t ∈ [-1,1], gün t kapanışında (16:00 ET) alınır; kademeli h-gün tutuş.
    mode='long_only': kısa sinyaller nakit (pos<0 -> 0).
    mode='inverse'  : kısa sinyaller ters ETF ile (nominal = |pos|/L_inv, böylece −1 hedef pozisyona yaklaşır).
    r_long, r_inv: GÜNLÜK log getiri serileri (t-1 kapanış -> t kapanış); basit getiriye çevrilir.
    Maliyet: her bacakta |Δnominal| × (gidiş-dönüş/2)."""
    idx = r_long.index
    p = pos.reindex(idx)
    if mode == "long_only":
        p = p.clip(lower=0)
    eff = _stagger(p, h)
    wl = eff.clip(lower=0)
    ws = (-eff).clip(lower=0) / L_inv if mode == "inverse" else eff * 0
    R = np.expm1(r_long)
    if demean: R = R - R.mean()
    pnl = wl.shift(1) * R
    cost = (wl - wl.shift(1).fillna(0)).abs().shift(1).fillna(0) * cost_long / 2e4
    if mode == "inverse":
        Ri = np.expm1(r_inv.reindex(idx))
        if demean: Ri = Ri - Ri.mean()
        pnl = pnl + ws.shift(1) * Ri.fillna(0)
        cost = cost + (ws - ws.shift(1).fillna(0)).abs().shift(1).fillna(0) * cost_inv / 2e4
    net = (pnl - cost)
    net = net[R.notna()].dropna()
    return net, wl, ws


def perf(net):
    net = net.dropna()
    if len(net) < 50 or net.std() == 0:
        return dict(sharpe=np.nan, ann=np.nan, vol=np.nan, t=np.nan, n=len(net))
    ann = net.mean() * 252; vol = net.std() * np.sqrt(252)
    return dict(sharpe=round(ann / vol, 3), ann=round(ann * 100, 2), vol=round(vol * 100, 2),
                t=round(net.mean() / (net.std() / np.sqrt(len(net))), 2), n=len(net))


def segs(net):
    out = {}
    for nm, m in [("full", slice(None)), ("is", net.index <= IS_END), ("oos", net.index > IS_END), ("22", net.index >= SUB_START)]:
        out[nm] = perf(net[m] if not isinstance(m, slice) else net)
    return out


def strat_eval(name, pos, tgt, h, d, inv=None, cost_kind="plain", restrict=None, extra=None):
    """Bir pozisyon serisini dört biçimde değerlendirir: yalnız uzun (temel/stres maliyet), ters ETF'li (temel/stres), demeaned.
    tgt: hedef ETF adı (c_<tgt>). inv: ters ETF adı (c_<inv>)."""
    r = lr(d[f"c_{tgt}"])
    if restrict is not None:
        r = r[r.index >= restrict]
    inv = inv or INV_OF.get(tgt)
    ri = lr(d[f"c_{inv}"]) if inv else None
    cb, cs = COST[cost_kind]; ib, is_ = COST["lev"]
    L = LEV.get(inv, 2.0)
    rows = []
    for mode in ["long_only", "inverse"]:
        if mode == "inverse" and ri is None: continue
        rr = r if mode == "long_only" else r[ri.reindex(r.index).notna()]
        for cname, cl, ci in [("base", cb, ib), ("stress", cs, is_)]:
            net, wl, ws = bt(pos, rr, h, cl, ri, L, ci, mode=mode)
            sg = segs(net)
            dm, _, _ = bt(pos, rr, h, cl, ri, L, ci, demean=True, mode=mode)
            sgd = segs(dm)
            bh = segs(np.expm1(rr).dropna())
            # bacak ayrımı (maliyetsiz)
            nl, _, _ = bt(pos.clip(lower=0), rr, h, 0.0, mode="long_only")
            if mode == "inverse":
                ns, _, _ = bt(pos.clip(upper=0), rr, h, 0.0, ri, L, 0.0, mode="inverse")
            row = dict(strategy=name, target=tgt, h=h, mode=mode, cost=cname, cost_bps=cl if mode == "long_only" else f"{cl}/{ci}",
                       exposure_long=round(wl.mean(), 3), exposure_short=round(ws.mean() * L, 3),
                       turnover_yr=round(((wl.diff().abs() + ws.diff().abs()).sum() / len(rr)) * 252, 1))
            for sgn, v in sg.items():
                row[f"sh_{sgn}"] = v["sharpe"]; row[f"ann_{sgn}"] = v["ann"]; row[f"t_{sgn}"] = v["t"]
            for sgn, v in sgd.items():
                row[f"shdm_{sgn}"] = v["sharpe"]
            for sgn, v in bh.items():
                row[f"bh_{sgn}"] = v["sharpe"]
            row["leg_long_ann_full"] = perf(nl)["ann"]; row["leg_long_sh_oos"] = perf(nl[nl.index > IS_END])["sharpe"]
            if mode == "inverse":
                row["leg_short_ann_full"] = perf(ns)["ann"]; row["leg_short_sh_oos"] = perf(ns[ns.index > IS_END])["sharpe"]
            # uç dönemler
            for k, (a, b) in EXTREMES.items():
                row[f"x_{k}"] = round(net[a:b].sum() * 100, 2) if len(net[a:b]) else np.nan
            msk = pd.Series(True, index=net.index)
            for a, b in EXTREMES.values():
                msk[a:b] = False
            row["sh_full_ex_extremes"] = perf(net[msk])["sharpe"]
            yr = net.groupby(net.index.year).sum()
            row["yrs_pos"] = f"{int((yr > 0).sum())}/{len(yr)}"
            if extra: row.update(extra)
            rows.append(row)
    return rows


def lbma_pm_spot():
    """Spot XAUUSD LBMA PM anında (15:00 Londra). Dukascopy saatlik (index=bar başlangıcı; fiyat anı=index+1h).
    15:00 Londra = 14:00 UTC (BST) / 15:00 UTC (GMT). Dukascopy kapsamı dışında (2026-10-30 sonrası) panel_spot xau_p14/xau_p15."""
    x = pd.read_parquet(f"{P}/duka/XAUUSD.parquet")
    px = x["c"].copy(); px.index = px.index + pd.Timedelta(hours=1)  # fiyat anı
    px = px[~px.index.duplicated()]
    days = pd.date_range("2004-11-01", "2026-11-30", freq="B")
    lon = pd.DatetimeIndex([pd.Timestamp(f"{d.date()} 15:00", tz="Europe/London").tz_convert("UTC") for d in days])
    v = px.reindex(lon).values
    out = pd.Series(v, index=days, name="spot_lbma")
    hh = pd.Series(lon.hour, index=days)
    sp = pd.read_parquet(f"{P}/panel_spot.parquet"); sp.index = pd.to_datetime(sp.index)
    alt = pd.Series(np.where(hh.reindex(sp.index) == 14, sp["xau_p14"], sp["xau_p15"]), index=sp.index)
    out = out.fillna(alt.reindex(out.index))
    return out, hh
