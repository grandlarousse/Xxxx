"""v_E3_a bağımsız doğrulama kütüphanesi. ll.py / elib.py IMPORT EDİLMEZ; ham parquet'ten kendi hizalama ve temizlik.
Zaman: parquet index = UTC bar başlangıcı; 'ldate' = yerel işlem tarihi.
"""
import os, numpy as np, pandas as pd
import statsmodels.api as sm

SCR = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
DATA = SCR + "/data"
OUT = SCR + "/out/code_v_E3_a"
RES = OUT + "/res"
os.makedirs(RES, exist_ok=True)
UP, DN = 0.105, -0.105  # BIST fiyat bazında simetrik eşik

_c = {}
def raw(sym, kind="daily"):
    k = (sym, kind)
    if k not in _c:
        _c[k] = pd.read_parquet(f"{DATA}/{kind}/{sym}.parquet")
    return _c[k]

def by_ldate(sym, kind="daily"):
    d = raw(sym, kind).copy()
    d.index = pd.DatetimeIndex(d["ldate"].values)
    d = d[~d.index.duplicated(keep="last")].sort_index()
    return d

def bist_cal():
    d = by_ldate("XU100.IS")
    if d["v"].fillna(0).gt(0).mean() > 0.5:
        d = d[d["v"].fillna(0) > 0]
    return d.index

def bist_decomp(sym, start="2014-01-01", vol_filter=True):
    """BIST günlük: cc(adj), gap, intra=log(c/o). Simetrik ±%10,5 fiyat bazlı temizlik (cc ve gap üzerinde).
    Bozuk açılış: o<=0/NaN veya (h==l ve o==önceki c)."""
    d = by_ldate(sym)
    if vol_filter and d["v"].fillna(0).gt(0).mean() > 0.5:
        d = d[d["v"].fillna(0) > 0]
    d = d[(d["c"] > 0) & (d["adj"] > 0)]
    cc = np.log(d["adj"]).diff()
    intra = np.log(d["c"] / d["o"])
    bad_open = (d["o"] <= 0) | d["o"].isna() | ((d["h"] == d["l"]) & (d["o"] == d["c"].shift(1)))
    intra[bad_open] = np.nan
    gap = cc - intra
    out = pd.DataFrame({"cc": cc, "gap": gap, "intra": intra, "o": d["o"], "c": d["c"], "prev_c": d["c"].shift(1),
                        "v": d["v"]})
    pc = np.expm1(out["cc"]); bad = (pc > UP) | (pc < DN)
    out.loc[bad, ["cc", "gap", "intra"]] = np.nan
    pg = np.expm1(out["gap"]); badg = (pg > UP) | (pg < DN)
    out.loc[badg, ["gap", "intra"]] = np.nan
    out.loc[out.index < pd.Timestamp(start), ["gap", "intra"]] = np.nan
    out["stale_open"] = (out["o"] == out["prev_c"])
    return out

def us_close(sym, field="adj", clean_sigma=12):
    """ABD/vadeli günlük kapanış serisi (yerel tarih) ve kendi takviminde log getiri (12σ temizliği opsiyonel)."""
    d = by_ldate(sym)
    p = d[field].astype(float); p = p[p > 0].dropna()
    r = np.log(p).diff()
    nbad = 0
    if clean_sigma:
        sd = r.rolling(250, min_periods=60).std().shift(1)
        bad = (r.abs() > clean_sigma * sd) & sd.notna(); nbad = int(bad.sum())
        r[bad] = np.nan
    return p, r, nbad

def map_A(sym, cal, **kw):
    """ll-konvansiyonunun BAĞIMSIZ yeniden yazımı: BIST günü t fiyatı = yerel tarihi <= t olan son kapanış;
    r_A(t) = log P(t) - log P(t_önceki). Temizlenmiş günlük getirilerin (t_önceki, t] toplamı olarak hesaplanır."""
    p, r, nb = us_close(sym, **kw)
    cum = r.fillna(0).cumsum()
    # P index'ine göre son kapanış <= t
    pos = cum.index.searchsorted(cal, side="right") - 1
    v = np.where(pos >= 0, cum.values[np.clip(pos, 0, None)], np.nan)
    s = pd.Series(v, index=cal)
    first = r.dropna().index.min()
    s[cal < first] = np.nan
    out = s.diff()
    # temizlenmiş (NaN) günü içeren aralık -> NaN
    nanr = r.isna().astype(int).cumsum()
    nv = np.where(pos >= 0, nanr.values[np.clip(pos, 0, None)], np.nan)
    nn = pd.Series(nv, index=cal).diff()
    out[nn > 0] = np.nan
    return out

def map_B(sym, cal, **kw):
    """'Taze' bilgi: BIST açılışı t'de bilinen en son ABD kapanışı = yerel tarihi < t olan son kapanış.
    sig_B(t) = log P(<t) - log P(<t_önceki). BIST tatillerinde (ör. Pazartesi kapalı) atlanan ABD günlerini de içerir.
    Zaten t için hizalanmış (ek shift YOK)."""
    p, r, nb = us_close(sym, **kw)
    cum = r.fillna(0).cumsum()
    pos = cum.index.searchsorted(cal, side="left") - 1  # tarih < t
    v = np.where(pos >= 0, cum.values[np.clip(pos, 0, None)], np.nan)
    s = pd.Series(v, index=cal)
    first = r.dropna().index.min(); s[cal <= first] = np.nan
    out = s.diff()
    nanr = r.isna().astype(int).cumsum()
    nv = np.where(pos >= 0, nanr.values[np.clip(pos, 0, None)], np.nan)
    out[pd.Series(nv, index=cal).diff() > 0] = np.nan
    return out

def hac(y, X, lags=5):
    df = pd.concat([y.rename("y"), X], axis=1).dropna()
    m = sm.OLS(df["y"], sm.add_constant(df.drop(columns="y"))).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    return m

def nw_mean(x, lags=5):
    x = pd.Series(x).dropna()
    if len(x) < 20: return np.nan, np.nan, len(x)
    m = sm.OLS(x.values, np.ones(len(x))).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    return m.params[0], m.tvalues[0], len(x)

def corr_t(a, b):
    df = pd.concat([a, b], axis=1).dropna()
    if len(df) < 40: return np.nan, np.nan, np.nan, len(df)
    r = df.iloc[:, 0].corr(df.iloc[:, 1]); n = len(df)
    t_iid = r * np.sqrt(n - 2) / np.sqrt(1 - r * r)
    z = (df - df.mean()) / df.std()
    m = sm.OLS(z.iloc[:, 0].values, sm.add_constant(z.iloc[:, 1].values)).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
    return r, t_iid, m.tvalues[1], n

def positions(sig, y, mode="z", thr=1.0, zw=250, minp=60):
    df = pd.concat([sig.rename("s"), y.rename("y")], axis=1).dropna()
    if mode == "z":
        mu = df.s.rolling(zw, min_periods=minp).mean().shift(1)
        sd = df.s.rolling(zw, min_periods=minp).std().shift(1)
        z = (df.s - mu) / sd
        pos = np.sign(z).where(z.abs() > thr, 0.0).fillna(0.0)
    else:
        pos = np.sign(df.s).where(df.s.abs() > thr, 0.0).fillna(0.0)
    return df, pos

def bt_stats(pnl, pos):
    act = pos != 0; n = int(act.sum())
    if n < 20: return {"n": n}
    pa = pnl[act]; m, t, _ = nw_mean(pa)
    ann = pa.mean() * 252 * act.mean(); vol = pnl.std() * np.sqrt(252)
    eq = pnl.cumsum(); dd = (eq - eq.cummax()).min()
    return {"n": n, "mean_bps": 1e4 * pa.mean(), "t": t, "hit": float((pa > 0).mean()), "sharpe": ann / vol if vol > 0 else np.nan,
            "ann_pct": 100 * ann, "maxdd_pct": 100 * dd, "n_long": int((pos > 0).sum()), "n_short": int((pos < 0).sum())}

def backtest(sig, y, cost_bps=0.0, mode="z", thr=1.0, split="2021-01-01", legs=1, **kw):
    df, pos = positions(sig, y, mode, thr, **kw)
    pnl = pos * df.y - legs * cost_bps / 1e4 * pos.abs()
    sp = pd.Timestamp(split)
    res = {"ALL": bt_stats(pnl, pos), "IS": bt_stats(pnl[pnl.index < sp], pos[pos.index < sp]),
           "OOS": bt_stats(pnl[pnl.index >= sp], pos[pos.index >= sp])}
    a = pos != 0
    res["by_year_bps"] = (1e4 * pnl[a].groupby(pnl[a].index.year).mean()).round(1).to_dict()
    res["by_year_n"] = pnl[a].groupby(pnl[a].index.year).size().to_dict()
    return res, pnl, pos, df
