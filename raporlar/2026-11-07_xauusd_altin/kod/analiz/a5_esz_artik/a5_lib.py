"""a5_esz_artik — ortak yardımcılar: yuvarlanan (yalnız geçmiş) regresyon artığı, sinyal kurma, bacak ayrımlı backtest.
Bilgi zamanı: tüm dk_<SYM>_p15 / xau_p15 değerleri Dukascopy BID saatlik mumunun 14:00 barının kapanışı (=14:59:59 UTC,
'fiyat anı = index+1h'), yani gün t 15:00 UTC'de bilinir; uzlaşma VWAP'ı 15:05-15:15 UTC. Beta yalnız t-W..t-1 satırlarıyla tahmin edilir.
"""
import sys, os, numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
sys.path.insert(0, f"{S}/code")
from lib_altin import *  # noqa
OUT = f"{S}/out/a5_esz_artik"
AGENT = "a5_esz_artik"


def roll_resid(y, X, W, minp=None):
    """y_t = a + b'X_t + e_t; (a,b) yalnız [t-W, t-1] satırlarından (tam veri olanlar, en az minp). Döndür DataFrame(e, fit, sig)."""
    minp = minp or int(0.8 * W)
    X = pd.DataFrame(X)
    Y = np.asarray(y, float); Xv = X.values.astype(float)
    n, p = Xv.shape
    ok = np.isfinite(Y) & np.all(np.isfinite(Xv), 1)
    e = np.full(n, np.nan); fit = np.full(n, np.nan); sig = np.full(n, np.nan); B = np.full((n, p), np.nan)
    for t in range(n):
        if not ok[t]:
            continue
        lo = max(0, t - W)
        m = ok[lo:t]
        if m.sum() < minp:
            continue
        idx = np.arange(lo, t)[m]
        A = np.column_stack([np.ones(len(idx)), Xv[idx]])
        coef, *_ = np.linalg.lstsq(A, Y[idx], rcond=None)
        r = Y[idx] - A @ coef
        sig[t] = r.std(ddof=p + 1)
        fit[t] = Xv[t] @ coef[1:]
        e[t] = Y[t] - coef[0] - fit[t]
        B[t] = coef[1:]
    out = pd.DataFrame(dict(e=e, fit=fit, sig=sig), index=pd.Index(y.index))
    for j, c in enumerate(X.columns):
        out[f"b_{c}"] = B[:, j]
    return out


def cum_z(e, sig, k):
    """k günlük kümülatif artık, t'deki (geçmişe dayalı) artık sigmasıyla standartlaştırılmış."""
    return e.rolling(k, min_periods=k).sum() / (sig * np.sqrt(k))


def legs_bt(pos, ret, h, cost=COST_BPS):
    """IS/OOS/full için: net Sharpe (5 bps), stres (10 bps), demeaned, uzun bacak, kısa bacak, buy&hold; yıllık devir."""
    res = {}
    for nm, msk in [("full", np.ones(len(ret), bool)), ("is", ret.index <= IS_END), ("oos", ret.index > IS_END)]:
        rr = ret[msk]; pp = pos.reindex(rr.index).fillna(0)
        a = backtest(pp, rr, h, cost); a10 = backtest(pp, rr, h, 2 * cost); dm = backtest(pp, rr, h, cost, demean=True)
        lg = backtest(pp.clip(lower=0), rr, h, cost); sh = backtest(pp.clip(upper=0), rr, h, cost)
        lgd = backtest(pp.clip(lower=0), rr, h, cost, demean=True); shd = backtest(pp.clip(upper=0), rr, h, cost, demean=True)
        bh = backtest(pd.Series(1.0, index=rr.index), rr, 1, 0)
        f = lambda z, k="sharpe": (round(z[k], 2) if z else np.nan)
        res[nm] = dict(sh=f(a), sh10=f(a10), sh_dm=f(dm), ann=(round(a["ann_ret"] * 100, 2) if a else np.nan), t=f(a, "t_daily"),
                       long_sh=f(lg), long_dm=f(lgd), short_sh=f(sh), short_dm=f(shd), bh=f(bh), turn=f(a, "turnover_per_yr"),
                       expo=f(a, "exposure"), long_frac=round(float((pp > 0).mean()), 2), short_frac=round(float((pp < 0).mean()), 2))
    return res


def flat_bt(res, prefix=""):
    return {f"{prefix}{k}_{nm}": v for nm, d in res.items() for k, v in d.items()}


def yearly_ic(x, y):
    d = pd.concat([x.rename("x"), y.rename("y")], axis=1).dropna()
    return d.groupby(d.index.year).apply(lambda g: g.x.corr(g.y, method="spearman") if len(g) > 20 else np.nan)
