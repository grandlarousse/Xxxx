"""Bağımsız yeniden üretim yardımcıları (lib_altin KULLANILMADI). NW-HAC, kukla/koşullu testler, kademeli backtest."""
import numpy as np, pandas as pd

IS_END = pd.Timestamp("2021-12-31")


def nw_ols(y, X, L, correction=False):
    """y ~ X (X sabit içermeli). Bartlett çekirdekli Newey-West. Döndür (beta, se, t)."""
    y = np.asarray(y, float); X = np.asarray(X, float)
    n, k = X.shape
    XtX_inv = np.linalg.inv(X.T @ X)
    b = XtX_inv @ X.T @ y
    u = y - X @ b
    Xu = X * u[:, None]
    Sm = Xu.T @ Xu
    for l in range(1, L + 1):
        w = 1 - l / (L + 1)
        G = Xu[l:].T @ Xu[:-l]
        Sm += w * (G + G.T)
    if correction: Sm *= n / (n - k)
    V = XtX_inv @ Sm @ XtX_inv
    se = np.sqrt(np.diag(V))
    return b, se, b / se


def reg_t(x, y, L):
    """y ~ a + b x, NW t'si (x ve y Series, ortak gözlemler)."""
    d = pd.concat([pd.Series(x, name="x"), pd.Series(y, name="y")], axis=1).dropna()
    if len(d) < 10 or d.x.std() == 0: return np.nan, np.nan, len(d)
    X = np.column_stack([np.ones(len(d)), d.x.values])
    b, se, t = nw_ols(d.y.values, X, L)
    return t[1], d.x.corr(d.y), len(d)


def mean_t(z, L):
    """ortalamanın NW t'si (z Series)."""
    z = pd.Series(z).dropna()
    if len(z) < 5: return np.nan
    b, se, t = nw_ols(z.values, np.ones((len(z), 1)), L)
    return t[0]


def split(idx):
    return idx <= IS_END, idx > IS_END


def dummy_test(D, y, h, label=""):
    """D: 0/1 Series (gün endeksli), y: fwd_h. Fark ve NW t (lag=max(h,5)) tam/IS/OOS + yıllık işaret."""
    L = max(h, 5)
    d = pd.concat([D.rename("D"), y.rename("y")], axis=1).dropna()
    isn, oos = split(d.index)
    out = dict(label=label, h=h, n=len(d), n_ev=int(d.D.sum()))
    for nm, m in [("full", slice(None)), ("is", isn), ("oos", oos)]:
        dd = d[m] if not isinstance(m, slice) else d
        e = dd.y[dd.D == 1]; ne = dd.y[dd.D == 0]
        t, ic, n = reg_t(dd.D, dd.y, L)
        out[f"diff_{nm}"] = (e.mean() - ne.mean()) * 1e4
        out[f"ev_mean_{nm}"] = e.mean() * 1e4
        out[f"non_mean_{nm}"] = ne.mean() * 1e4
        out[f"t_{nm}"] = t; out[f"ic_{nm}"] = ic; out[f"nev_{nm}"] = int(len(e))
    out["hit"] = float((d.y[d.D == 1] > 0).mean())
    yr = {}
    for yy, g in d.groupby(d.index.year):
        if (g.D == 1).sum() >= 1 and (g.D == 0).sum() >= 5:
            yr[int(yy)] = round((g.y[g.D == 1].mean() - g.y[g.D == 0].mean()) * 1e4, 1)
    sg = np.sign(out["diff_full"])
    out["yrs_same"] = f"{sum(np.sign(v) == sg for v in yr.values())}/{len(yr)}"
    out["by_year"] = yr
    return out


def cond_test(x, y, h, label=""):
    """x: yalnız olay günlerinde değer (diğerleri NaN). Sürekli IC NW t, işaret kuralı ort ve t (iki türlü)."""
    L = max(h, 5)
    d = pd.concat([x.rename("x"), y.rename("y")], axis=1).dropna()
    d = d[d.x != 0]
    isn, oos = split(d.index)
    out = dict(label=label, h=h, n=len(d))
    for nm, m in [("full", slice(None)), ("is", isn), ("oos", oos)]:
        dd = d[m] if not isinstance(m, slice) else d
        t_ic, ic, n = reg_t(dd.x, dd.y, L)
        pnl = np.sign(dd.x) * dd.y
        out[f"ic_{nm}"] = ic; out[f"tIC_{nm}"] = t_ic
        out[f"sgn_mean_{nm}"] = pnl.mean() * 1e4
        out[f"t_sgnmean_{nm}"] = mean_t(pnl, L)          # ort(sign·y) = 0 testi
        out[f"t_sgnreg_{nm}"] = reg_t(np.sign(dd.x), dd.y, L)[0]   # y ~ a + b·sign(x)
        out[f"n_{nm}"] = len(dd)
        out[f"hit_{nm}"] = float((pnl > 0).mean())
    yr_ic, yr_m = {}, {}
    for yy, g in d.groupby(d.index.year):
        if len(g) >= 4:
            yr_ic[int(yy)] = round(g.x.corr(g.y), 3); yr_m[int(yy)] = round((np.sign(g.x) * g.y).mean() * 1e4, 1)
    out["yrs_same_ic"] = f"{sum(np.sign(v) == np.sign(out['ic_full']) for v in yr_ic.values())}/{len(yr_ic)}"
    out["yrs_same_sgnmean"] = f"{sum(v > 0 for v in yr_m.values())}/{len(yr_m)}"
    out["by_year_sgnmean"] = yr_m
    return out


def backtest(pos, r, h, cost_bps=5.0, demean=False):
    """Kademeli: eff_t = ort(pos_t..pos_{t-h+1}); pnl_{t+1} = eff_t·r_{t+1} − |Δeff_t|·cost/2. pos gün t uzlaşmasında."""
    r = r.copy()
    if demean: r = r - r.mean()
    p = pos.reindex(r.index).fillna(0.0)
    eff = sum(p.shift(k).fillna(0) for k in range(h)) / h
    turn = (eff - eff.shift(1).fillna(0)).abs()
    pnl = eff.shift(1) * r - turn.shift(1).fillna(0) * cost_bps / 2e4
    pnl = pnl.dropna()
    sd = pnl.std()
    return dict(sharpe=pnl.mean() / sd * np.sqrt(252) if sd > 0 else np.nan, ann=pnl.mean() * 252 * 100, n=len(pnl),
                exposure=float(eff.abs().mean()), pnl=pnl)


def bt_block(pos, r, h):
    out = {}
    isn, oos = split(r.index)
    for nm, m in [("full", np.ones(len(r), bool)), ("is", isn), ("oos", oos)]:
        rr = r[m]; pp = pos.reindex(rr.index).fillna(0)
        out[f"sh_{nm}"] = backtest(pp, rr, h)["sharpe"]
        out[f"sh_{nm}_dm"] = backtest(pp, rr, h, demean=True)["sharpe"]
        out[f"sh_{nm}_10"] = backtest(pp, rr, h, cost_bps=10)["sharpe"]
        out[f"sh_{nm}_0"] = backtest(pp, rr, h, cost_bps=0)["sharpe"]
        out[f"bh_{nm}"] = rr.mean() / rr.std() * np.sqrt(252)
        out[f"long_{nm}"] = backtest(pp.clip(lower=0), rr, h)["sharpe"] if (pp > 0).any() else np.nan
        out[f"short_{nm}"] = backtest(pp.clip(upper=0), rr, h)["sharpe"] if (pp < 0).any() else np.nan
        out[f"short_{nm}_dm"] = backtest(pp.clip(upper=0), rr, h, demean=True)["sharpe"] if (pp < 0).any() else np.nan
        out[f"long_{nm}_dm"] = backtest(pp.clip(lower=0), rr, h, demean=True)["sharpe"] if (pp > 0).any() else np.nan
    out["trades_per_year"] = float((pos != 0).sum() / (len(r) / 252))
    return out


def fmt(d, keys):
    return " ".join(f"{k}={d[k]:.2f}" if isinstance(d.get(k), (float, np.floating)) else f"{k}={d.get(k)}" for k in keys)
