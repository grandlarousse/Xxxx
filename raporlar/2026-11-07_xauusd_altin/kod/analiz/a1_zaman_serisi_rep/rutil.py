"""Bağımsız yeniden üretim yardımcıları (lib_altin'den bağımsız, sıfırdan)."""
import bisect, numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"; OUT = f"{S}/out/a1_zaman_serisi_rep"
IS_END = pd.Timestamp("2021-12-31")


def load():
    B = pd.read_parquet(f"{OUT}/base.parquet"); SP = pd.read_parquet(f"{OUT}/spot.parquet")
    SP = SP[SP.index >= "2010-01-04"]  # 1 Ocak 2010 tatil kotasyonu dışarıda
    SP["lp"] = np.log(SP.p15); SP["r"] = SP.lp.diff()
    return B, SP


def exp_pct(x, minp=250):
    """genişleyen yüzdelik: bugün dahil geçmişteki değerlerin x_t'ye eşit/küçük oranı; en az minp gözlem."""
    srt, out = [], np.full(len(x), np.nan)
    for i, v in enumerate(np.asarray(x, float)):
        if np.isfinite(v):
            bisect.insort(srt, v)
            if len(srt) >= minp: out[i] = bisect.bisect_right(srt, v) / len(srt)
    return pd.Series(out, index=x.index)


def asof_to(F, idx, maxdays=4):
    """spot-takvimli seriyi hedef günlere taşı: aynı gün varsa o (NaN dahil), yoksa ≤maxdays önceki son spot günü."""
    F = pd.DataFrame(F)
    out = F.reindex(idx)
    miss = ~idx.isin(F.index)
    p = F.index.searchsorted(idx[miss], side="right") - 1
    ok = (p >= 0) & ((idx[miss] - F.index[np.clip(p, 0, None)]).days <= maxdays)
    out.loc[idx[miss][ok]] = F.iloc[p[ok]].values
    return out


def nw_se_slope(y, x, L):
    """y = a + b x + u; Bartlett NW kovaryansı (küçük örnek düzeltmesiz). Döndür b, se."""
    y = np.asarray(y, float); x = np.asarray(x, float); n = len(y)
    X = np.column_stack([np.ones(n), x]); XtXi = np.linalg.inv(X.T @ X); b = XtXi @ X.T @ y; u = y - X @ b
    g = X * u[:, None]; Sm = g.T @ g
    for l in range(1, L + 1):
        w = 1 - l / (L + 1); G = g[l:].T @ g[:-l]; Sm += w * (G + G.T)
    V = XtXi @ Sm @ XtXi
    return b[1], np.sqrt(V[1, 1])


def ic_nw(x, y, L):
    d = pd.concat([pd.Series(x, name="x"), pd.Series(y, name="y")], axis=1).dropna()
    if len(d) < 30: return dict(ic=np.nan, t=np.nan, n=len(d))
    rx, ry = d.x.rank(), d.y.rank()
    ic = np.corrcoef(rx, ry)[0, 1]
    zx = (rx - rx.mean()) / rx.std(); zy = (ry - ry.mean()) / ry.std()
    b, se = nw_se_slope(zy.values, zx.values, L)
    return dict(ic=ic, t=b / se, n=len(d))


def ic_split(x, y, h):
    L = max(h, 5)
    f = ic_nw(x, y, L); a = ic_nw(x[x.index <= IS_END], y[y.index <= IS_END], L); b = ic_nw(x[x.index > IS_END], y[y.index > IS_END], L)
    d = pd.concat([pd.Series(x, name="x"), pd.Series(y, name="y")], axis=1).dropna()
    yr = {}
    for yy, g in d.groupby(d.index.year):
        if len(g) > 20: yr[yy] = g.x.rank().corr(g.y.rank())
    yr = pd.Series(yr); same = int((np.sign(yr) == np.sign(f["ic"])).sum())
    return dict(ic=f["ic"], t=f["t"], n=f["n"], ic_is=a["ic"], t_is=a["t"], ic_oos=b["ic"], t_oos=b["t"], yrs=f"{same}/{len(yr)}", by_year=yr.round(3).to_dict())


def bt(pos, ret, h, cost_bps=5.0, demean=False, strict=False):
    """Kademeli h alt portföy. pos_t gün t uzlaşmasında açılır, t+h uzlaşmasında kapanır. eff_t = ort(pos_t..pos_{t-h+1}).
    PnL_{t+1} = eff_t·r_{t+1} − maliyet. Netleşmeli maliyet: |eff_t − eff_{t-1}|·cost/2 (tek yön). Katı: her alt portföy açılış+kapanış
    = |pos_t|/h·cost/2 + |pos_{t-h}|/h·cost/2 (netleşme yok). demean: r − ort(r) (değerlendirilen örneklemde)."""
    r = ret.astype(float)
    if demean: r = r - r.mean()
    p = pos.reindex(r.index).astype(float).fillna(0.0).clip(-1, 1)
    eff = sum(p.shift(k).fillna(0.0) for k in range(h)) / h
    if strict:
        tr = (p.abs() + p.shift(h).fillna(0.0).abs()) / h
    else:
        tr = (eff - eff.shift(1).fillna(0.0)).abs()
    pnl = eff.shift(1) * r - tr.shift(1).fillna(0.0) * cost_bps / 2 / 1e4
    pnl = pnl.dropna()
    m, s = pnl.mean(), pnl.std()
    # NW t (lag 5) günlük PnL için
    L = 5; u = (pnl - m).values; n = len(u); g0 = (u @ u) / n; lr = g0 + 2 * sum((1 - l / (L + 1)) * (u[l:] @ u[:-l]) / n for l in range(1, L + 1))
    return dict(sharpe=m / s * np.sqrt(252), t=m / (s / np.sqrt(n)), t_nw=m / np.sqrt(lr / n), ann=m * 252, n=n, expo=float(eff.reindex(pnl.index).abs().mean()),
                turn=float(tr.reindex(pnl.index).sum() / n * 252), pnl=pnl, eff=eff)


def bt_split(pos, ret, h, cost=5.0):
    ism = ret.index <= IS_END
    o = {}
    for nm, m in [("full", np.ones(len(ret), bool)), ("is", ism), ("oos", ~ism)]:
        rr = ret[m]; pp = pos.reindex(rr.index)
        o[nm + "_raw"] = bt(pp, rr, h, cost); o[nm + "_dm"] = bt(pp, rr, h, cost, demean=True)
    rr = ret[~ism]; pp = pos.reindex(rr.index)
    o["oos_dm10"] = bt(pp, rr, h, 10, demean=True); o["oos_dm_strict"] = bt(pp, rr, h, cost, demean=True, strict=True)
    o["full_dm_strict"] = bt(pos, ret, h, cost, demean=True, strict=True)
    o["oos_long_dm"] = bt(pp.clip(lower=0), rr, h, cost, demean=True); o["oos_short_dm"] = bt(pp.clip(upper=0), rr, h, cost, demean=True)
    o["full_long_dm"] = bt(pos.clip(lower=0), ret, h, cost, demean=True); o["full_short_dm"] = bt(pos.clip(upper=0), ret, h, cost, demean=True)
    f = o["full_dm"]; act = f["eff"].reindex(ret.index).abs().groupby(ret.index.year).mean()
    g = f["pnl"].groupby(f["pnl"].index.year); ys = g.mean() / g.std() * np.sqrt(252)
    ya = [y for y in ys.index if act.get(y, 0) > 0.05]
    o["by_year"] = {int(y): round(float(ys[y]), 2) for y in ya}; o["yrs"] = f"{sum(ys[y] > 0 for y in ya)}/{len(ya)}"
    return o


def row(nm, h, o):
    R = lambda k, f="sharpe": round(float(o[k][f]), 2)
    return dict(sig=nm, h=h, sh_full=R("full_raw"), shdm_full=R("full_dm"), t_full=R("full_dm", "t"), tnw_full=R("full_dm", "t_nw"),
                shdm_is=R("is_dm"), t_is=R("is_dm", "t"), shdm_oos=R("oos_dm"), t_oos=R("oos_dm", "t"), sh_oos_net=R("oos_raw"),
                shdm_oos_10=R("oos_dm10"), shdm_oos_strict=R("oos_dm_strict"), long_oos=R("oos_long_dm"), short_oos=R("oos_short_dm"),
                long_full=R("full_long_dm"), short_full=R("full_short_dm"), expo=round(o["full_dm"]["expo"], 2), turn=round(o["full_dm"]["turn"], 1),
                trades_yr=round(o["full_dm"]["turn"] / 2, 1), yrs=o["yrs"], by_year=o["by_year"])
