"""Genel çürütme değerlendiricisi (bağımsız)."""
import numpy as np, pandas as pd, cl, json
VIOP = ["AEFES","AKBNK","AKSEN","ALARK","ARCLK","ASELS","ASTOR","BIMAS","BRSAN","CIMSA","DOAS","DOHOL","EKGYO","ENJSA","ENKAI","EREGL","FROTO","GARAN","GUBRF","HALKB","HEKTS","ISCTR","KCHOL","KRDMD","MGROS","ODAS","OYAKC","PETKM","PGSUS","SAHOL","SASA","SISE","SOKM","TAVHL","TCELL","THYAO","TKFEN","TOASO","TRALT","TRMET","TSKB","TTKOM","TUPRS","ULKER","VAKBN","VESTL","YKBNK"]
_R = {}
def R(und):
    if und not in _R:
        _R[und] = cl.fut_ret(und, None if und in ("XU030", "USDTRY", "XAUUSD", "XLBNK") else und + ".IS")
    return _R[und]
def legs(und):
    r = R(und); m = R("XU030"); b = cl.roll_beta(r, m, 250, 100)
    return {"raw": r, "hedged": r - b * m}
HS = [1, 2, 3, 5]; THR = [0.5, 1.0, 1.5]; LEGS = ["raw", "hedged"]
def ydict(und, start, end=None):
    L = legs(und); out = {}
    for h in HS:
        for lg in LEGS:
            y = cl.fwd(L[lg], h); y = y[y.index >= start]
            if end: y = y[y.index <= end]
            out[(h, lg)] = y
    return out
def evaluate(name, z, und, main=(2, 1.0, "raw"), start="2017-03-06", split="2022-01-01", nsim=300, placebo=True, verbose=True, end=None):
    co = cl.costs(); cs = float(co.loc[und, "rt_cost_small_bps"]); c1m = float(co.loc[und, "rt_cost_1m_bps"])
    Y = ydict(und, start, end); rollf = cl.front(und)["roll"]
    grid = []; rows = []
    for h in HS:
        for thr in THR:
            for lg in LEGS:
                extra = 3 if lg == "hedged" else 0
                tr = cl.trades(z, Y[(h, lg)], h, thr, rollf)
                s8 = cl.summ(tr, 8 + extra, split=split); s15 = cl.summ(tr, 15 + extra, split=split)
                rows.append(dict(h=h, thr=thr, leg=lg, n=s8.get("n"), per_yr=s8.get("per_yr"), gross=s8.get("gross"), net8=s8.get("net"), t8=s8.get("t"),
                                 net15=s15.get("net"), t15=s15.get("t"), IS=s8.get("IS"), IS_t=s8.get("IS_t"), OOS=s8.get("OOS"), OOS_t=s8.get("OOS_t"), long=s8.get("long_frac")))
                grid.append((h, thr, lg, 8 + extra))
    G = pd.DataFrame(rows)
    h, thr, lg = main; extra = 3 if lg == "hedged" else 0
    tr = cl.trades(z, Y[(h, lg)], h, thr, rollf)
    res = dict(name=name, und=und, main=f"h{h} thr{thr} {lg}")
    s8 = cl.summ(tr, 8 + extra, split=split); s15 = cl.summ(tr, 15 + extra, split=split)
    sc = cl.summ(tr, cs + extra, roll_cost=cs, split=split); s1m = cl.summ(tr, c1m + extra, roll_cost=c1m, split=split)
    res.update(n=s8["n"], per_yr=round(s8["per_yr"], 1), gross=round(s8["gross"], 1), net8=round(s8["net"], 1), t8=round(s8["t"], 2),
               net15=round(s15["net"], 1), t15=round(s15["t"], 2), net_small_roll=round(sc["net"], 1), t_small_roll=round(sc["t"], 2),
               net_1m_roll=round(s1m["net"], 1), t_1m_roll=round(s1m["t"], 2), hit=round(s8["hit"], 3), long_frac=round(s8["long_frac"], 2),
               IS=round(s8["IS"], 1), IS_t=round(s8["IS_t"], 2), IS_n=s8["IS_n"], OOS=round(s8["OOS"], 1), OOS_t=round(s8["OOS_t"], 2), OOS_n=s8["OOS_n"],
               rolls_frac=round((tr["rolls"] > 0).mean(), 2))
    res["periods"] = cl.periods(tr, 8 + extra); res["by_year"] = cl.by_year(tr, 8 + extra)
    m10, t10 = cl.drop_top(tr, 8 + extra, 10); res["drop_top10"] = (round(m10, 1), round(t10, 2))
    m5, t5 = cl.drop_top(tr, 8 + extra, 5); res["drop_top5"] = (round(m5, 1), round(t5, 2))
    net = tr["gross"] * 1e4 - 8 - extra
    res["long_net"] = round(net[tr["dir"] > 0].mean(), 1); res["short_net"] = round(net[tr["dir"] < 0].mean(), 1)
    res["n_long"] = int((tr["dir"] > 0).sum()); res["n_short"] = int((tr["dir"] < 0).sum())
    # bacak drifti: tüm günlerde t->t+h ortalaması (uzun eğilim kontrolü)
    yall = Y[(h, lg)].dropna() * 1e4; res["uncond_fwd_bps"] = round(yall.mean(), 1)
    res["drift_explained_bps"] = round((res["n_long"] - res["n_short"]) / max(res["n"], 1) * yall.mean(), 1)
    # dairesel kaydırma null
    if nsim:
        mx, per = cl.circ_null(z, Y, grid, nsim=nsim)
        g0 = (h, thr, lg, 8 + extra); t_obs = res["t8"]
        res["p_circ_single"] = round(float(np.mean(per[g0][np.isfinite(per[g0])] >= t_obs)), 3)
        res["null_mean_t_single"] = round(float(np.nanmean(per[g0])), 2)
        tmax_obs = np.nanmax(G["t8"].values)
        res["grid_best"] = G.loc[G["t8"].idxmax(), ["h", "thr", "leg", "net8", "t8"]].to_dict()
        res["p_circ_maxgrid_obs_main"] = round(float(np.mean(mx >= t_obs)), 3)
        res["p_circ_maxgrid_obs_best"] = round(float(np.mean(mx >= tmax_obs)), 3)
        res["grid_n_variants"] = len(grid)
    res["grid_pos_frac"] = round(float((G["net8"] > 0).mean()), 2)
    # plasebo: aynı sinyal diğer 46 hisse
    if placebo:
        ts = {}
        for s in VIOP:
            try:
                L = legs(s); y = cl.fwd(L[lg], h); y = y[y.index >= start]
                if end: y = y[y.index <= end]
                trs = cl.trades(z, y, h, thr)
                ts[s] = cl.tstat(trs["gross"].values * 1e4 - 8 - extra) if len(trs) >= 20 else np.nan
            except Exception as e:
                ts[s] = np.nan
        ts = pd.Series(ts).dropna().sort_values(ascending=False)
        res["placebo_rank"] = f"{int(list(ts.index).index(und)) + 1}/{len(ts)}" if und in ts.index else "na"
        oth = ts.drop(und, errors="ignore")
        res["placebo_others_mean_t"] = round(float(oth.mean()), 2); res["placebo_others_frac_t>2"] = round(float((oth > 2).mean()), 3)
        res["placebo_top3"] = {k: round(v, 2) for k, v in ts.head(3).items()}
    if verbose:
        print(json.dumps(res, ensure_ascii=False, default=str, indent=None))
        print(G.round(2).to_string())
    return res, G, tr

# ---------------- spot (uzun geçmiş kontrolü; spot kapanış dolumu kullanıcı için GEÇERSİZ, yalnız sinyalin varlığı için) ----------------
_SC = None
def scal():
    global _SC
    if _SC is None:
        d = cl.dly("XU100.IS"); d = d[(d["v"].fillna(0) > 0) | (d["h"] != d["l"])]
        _SC = pd.DatetimeIndex(d.index[d.index >= "2012-01-01"])
    return _SC
def sret(sym):
    r = cl.lret(sym, bist=True).reindex(scal())
    lim = np.where(r.index < cl.REGIME, np.log(1.205), np.log(1.105)); r[r.abs() > lim] = np.nan
    return r
def evaluate_spot(name, z, sym, main=(2, 1.0, "raw"), start="2014-01-01", split="2021-01-01"):
    r = sret(sym); m = sret("XU100.IS"); b = cl.roll_beta(r, m, 250, 100)
    L = {"raw": r, "hedged": r - b * m}
    h, thr, lg = main; extra = 3 if lg == "hedged" else 0
    y = cl.fwd(L[lg], h); y = y[y.index >= start]
    tr = cl.trades(z.reindex(scal()), y, h, thr)
    s = cl.summ(tr, 8 + extra, split=split)
    out = dict(name=name, sym=sym, main=f"h{h} thr{thr} {lg}", n=s["n"], net8=round(s["net"], 1), t8=round(s["t"], 2), IS=round(s["IS"], 1), IS_t=round(s["IS_t"], 2),
               OOS=round(s["OOS"], 1), OOS_t=round(s["OOS_t"], 2), by_year=cl.by_year(tr, 8 + extra), drop_top10=tuple(round(v, 2) for v in cl.drop_top(tr, 8 + extra, 10)))
    print(json.dumps(out, ensure_ascii=False, default=str))
    return out, tr
