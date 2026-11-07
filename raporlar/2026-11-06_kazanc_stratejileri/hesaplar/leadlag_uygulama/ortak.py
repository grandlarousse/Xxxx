# -*- coding: utf-8 -*-
"""ortak.py - leadlag_uygulama yardimcilari: veri yukleme (leadlag2), BIST takvimi, ABD tarihli serilerin
BIST gunune eslenmesi, OLS + Newey-West, BH-FDR."""
import io, os, zipfile
import numpy as np, pandas as pd

V = os.environ.get("LL2", "/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/data/leadlag2")
BAS = pd.Timestamp("2009-01-01")


def takvim():
    s = pd.read_csv(os.path.join(V, "isy", "XU100.csv"), index_col=0, parse_dates=True)["px"]
    return s.index[s.index >= BAS]


def _lim(idx):
    return pd.Series(np.where(idx < pd.Timestamp("2020-03-13"), 0.205, 0.105), index=idx)


def bist_getiri(kod, cal, ipo_atla=20):
    """Log getiri, BIST takvimi. Hisse: hacim<=0 gunu bayat (fiyat yok sayilir, hareket ertesi gune).
    |basit getiri| > limit (13.03.2020 oncesi %20,5, sonra %10,5) -> NaN (kurumsal islem/veri hatasi).
    Hissede ilk ipo_atla islem gunu atilir (halka arz tavan serisi)."""
    d = pd.read_csv(os.path.join(V, "isy", kod + ".csv"), index_col=0, parse_dates=True)
    if "adj" in d.columns:
        p = d["adj"].copy()
        if "vol_tl" in d.columns:
            bayat = d["vol_tl"].notna() & (d["vol_tl"] <= 0)
            p[bayat] = np.nan
        hisse = True
    else:
        p = d["px"].copy(); hisse = False
    p = p[p > 0]
    ilk = p.dropna().index[0]; sonv = p.dropna().index[-1]
    c = cal[(cal >= ilk) & (cal <= sonv)]  # son gecerli gunden sonra ileri tasima yok
    p = p.reindex(p.index.union(c)).ffill().reindex(c)
    r = np.log(p).diff()
    if hisse:
        r[np.expm1(r).abs() > _lim(r.index)] = np.nan
        r.iloc[:ipo_atla] = np.nan
    return r.reindex(cal)


def fred(sid):
    d = pd.read_csv(os.path.join(V, "fred", sid + ".csv"))
    d.columns = ["tarih", "v"]
    d["tarih"] = pd.to_datetime(d["tarih"]); d["v"] = pd.to_numeric(d["v"], errors="coerce")
    s = d.dropna().set_index("tarih")["v"]
    return s[s > 0]


def cboe_vix():
    d = pd.read_csv(os.path.join(V, "cboe", "VIX.csv"))
    d["DATE"] = pd.to_datetime(d["DATE"], format="%m/%d/%Y")
    return d.set_index("DATE")["CLOSE"].astype(float)


def french49():
    z = zipfile.ZipFile(os.path.join(V, "french", "49_daily.zip"))
    t = z.read(z.namelist()[0]).decode("latin1").splitlines()
    # ilk blok: Average Value Weighted Returns -- Daily
    i0 = next(i for i, l in enumerate(t) if l.strip().startswith(",Agric") or l.strip().startswith("Agric") or l.startswith(" ,Agric"))
    hdr = [h.strip() for h in t[i0].split(",")]
    rows = []
    for l in t[i0 + 1:]:
        x = l.split(",")
        if not x[0].strip().isdigit():
            break
        rows.append(x)
    df = pd.DataFrame(rows, columns=hdr)
    df.index = pd.to_datetime(df.iloc[:, 0].str.strip(), format="%Y%m%d"); df = df.iloc[:, 1:].astype(float)
    df[df <= -99] = np.nan
    return df / 100.0


def french_ff():
    z = zipfile.ZipFile(os.path.join(V, "french", "F-F_Research_Data_Factors_daily_CSV.zip"))
    t = z.read(z.namelist()[0]).decode("latin1").splitlines()
    i0 = next(i for i, l in enumerate(t) if "Mkt-RF" in l)
    rows = []
    for l in t[i0 + 1:]:
        x = l.split(",")
        if not x[0].strip().isdigit():
            break
        rows.append(x)
    df = pd.DataFrame(rows, columns=["d", "MktRF", "SMB", "HML", "RF"])
    df.index = pd.to_datetime(df["d"].str.strip(), format="%Y%m%d"); df = df.drop(columns="d").astype(float) / 100.0
    return df


def us_to_bist(s, cal):
    """ABD tarihli seri (ABD gunu d) -> d'den SONRAKI ilk BIST gunu t. Ayni t'ye dusen ABD gunleri toplanir.
    Boylece deger BIST t kapanisindan once (t gunu 00:00 TSI'de) kesin bilinir."""
    s = s.dropna()
    pos = cal.searchsorted(s.index, side="right")
    ok = pos < len(cal)
    t = cal[pos[ok]]
    out = pd.Series(s.values[ok], index=t).groupby(level=0).sum(min_count=1)
    return out.reindex(cal)


def rolling_beta(y, x, n=250, mn=100):
    b = y.rolling(n, min_periods=mn).cov(x) / x.rolling(n, min_periods=mn).var()
    return b.shift(1)


def ols_nw(y, X, lag=5):
    """y (n,), X (n,k) sabit dahil degil -> sabit eklenir. Doner: beta, NW-t, n."""
    m = np.isfinite(y) & np.all(np.isfinite(X), axis=1)
    y = y[m]; X = np.column_stack([np.ones(m.sum()), X[m]])
    n, k = X.shape
    if n < 60:
        return np.full(k, np.nan), np.full(k, np.nan), n
    XtX_inv = np.linalg.pinv(X.T @ X)
    b = XtX_inv @ X.T @ y
    e = y - X @ b
    u = X * e[:, None]
    S = u.T @ u
    for L in range(1, lag + 1):
        w = 1 - L / (lag + 1)
        G = u[L:].T @ u[:-L]
        S += w * (G + G.T)
    V = XtX_inv @ S @ XtX_inv
    se = np.sqrt(np.diag(V))
    return b, b / se, n


def partial_corr(a, b, c):
    """a ile b arasinda c (DataFrame/Series) kontrollu kismi korelasyon."""
    d = pd.concat([a, b, c], axis=1).dropna()
    if len(d) < 60:
        return np.nan, len(d)
    Z = np.column_stack([np.ones(len(d)), d.iloc[:, 2:].values])
    ra = d.iloc[:, 0].values - Z @ np.linalg.lstsq(Z, d.iloc[:, 0].values, rcond=None)[0]
    rb = d.iloc[:, 1].values - Z @ np.linalg.lstsq(Z, d.iloc[:, 1].values, rcond=None)[0]
    return float(np.corrcoef(ra, rb)[0, 1]), len(d)


def bh(p):
    p = np.asarray(p, float); n = np.isfinite(p).sum()
    q = np.full_like(p, np.nan)
    idx = np.where(np.isfinite(p))[0]
    o = idx[np.argsort(p[idx])]
    r = np.arange(1, n + 1)
    qq = np.minimum.accumulate((p[o] * n / r)[::-1])[::-1]
    q[o] = np.minimum(qq, 1.0)
    return q


def p_from_t(t):
    from math import erf, sqrt
    if not np.isfinite(t):
        return np.nan
    return 2 * (1 - 0.5 * (1 + erf(abs(t) / sqrt(2))))
