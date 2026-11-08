"""Hakem (adversarial) ortak yardımcılar. a2_common'dan yalnız yamalı saatlik seriyi alır; geri kalanı bağımsız."""
import os, sys, numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
sys.path.insert(0, f"{S}/code"); sys.path.insert(0, f"{S}/out/a2_seans_gunici")
from lib_altin import load_viop, load_spot, ic, nw_ols, fwd, backtest, bt_summary, IS_END, bh_fdr  # noqa
import a2_common as A2  # noqa  (yalnız price_series / segments için)
OUT = f"{S}/out/a2_seans_gunici_adv"
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40); pd.set_option("display.max_rows", 300)

SUBP = {"2010-16": ("2010-01-01", "2016-12-31"), "2017-19": ("2017-01-01", "2019-12-31"), "2020-21": ("2020-01-01", "2021-12-31"),
        "2022-23": ("2022-01-01", "2023-12-31"), "2024-26": ("2024-01-01", "2026-12-31")}

def mean_t(x, lags=5):
    import statsmodels.api as sm
    x = pd.Series(x).dropna()
    if len(x) < 30: return (np.nan, np.nan, len(x))
    m = sm.OLS(x.values, np.ones(len(x))).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    return (float(x.mean()), float(m.tvalues[0]), len(x))

def sub_ic(x, y, h, periods=SUBP, method="spearman"):
    out = {}
    for k, (a, b) in periods.items():
        m = (x.index >= a) & (x.index <= b)
        r = ic(x[m], y[m], max(h, 5), method)
        out[k] = (round(r["ic"], 4) if np.isfinite(r["ic"]) else np.nan, round(r["t"], 2) if np.isfinite(r["t"]) else np.nan, r["n"])
    return out

def snap(px, ts, tol_h=1.0):
    """px: fiyat serisi (index = fiyat anı). ts anında ya da önce son fiyat; tol_h saatten eskiyse NaN."""
    ts = pd.DatetimeIndex(ts)
    i = px.index.searchsorted(ts, side="right") - 1
    ok = i >= 0; ii = np.clip(i, 0, None)
    val = np.where(ok, px.values[ii], np.nan)
    age = (ts - px.index[ii]) / pd.Timedelta(hours=1)
    return np.where(ok & (age <= tol_h), val, np.nan)
