"""Hakem (adversarial) ortak yardımcılar — a4_abd_capraz iddialarını çürütme denemesi.
Analistin lib_altin fonksiyonlarını (ic, split_stats, backtest) kullanır; sinyalleri ham Yahoo dosyalarından ve paneldeki
as-of sütunlardan ayrı ayrı kurar."""
import sys, numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
sys.path.insert(0, f"{S}/code")
from lib_altin import ic, split_stats, backtest, nw_ols, fwd, IS_END, bh_fdr, load_viop, load_spot, hourly  # noqa
OUT = f"{S}/out/a4_abd_capraz_adv"

SUBP = [("2017-19", "2017-01-01", "2019-12-31"), ("2020-21", "2020-01-01", "2021-12-31"),
        ("2022-23", "2022-01-01", "2023-12-31"), ("2024-26", "2024-01-01", "2026-12-31")]


def zscale(r, win=120, minp=60):
    return r / r.rolling(win, min_periods=minp).std().shift(1)


def beta(a, b, win=60, minp=40):
    return (a.rolling(win, min_periods=minp).cov(b) / b.rolling(win, min_periods=minp).var()).shift(1)


def miner_resid(df, m, bw=60, zw=120, bench="y_GLD"):
    rm = np.log(df[m]).diff(); rg = np.log(df[bench]).diff()
    return zscale(rm - beta(rm, rg, bw, max(10, int(bw * 0.67))) * rg, zw, max(30, zw // 2))


def tercile(x, thr=0.43):
    return np.sign(x).where(x.abs() > thr, 0.0).where(x.notna(), 0.0)


def bt_stats(pos, ret, h, cost=5.0, demean=False):
    r = backtest(pos, ret, h, cost_bps=cost, demean=demean)
    if r is None: return dict(sh=np.nan, t=np.nan, ann=np.nan)
    return dict(sh=round(r["sharpe"], 2), t=round(r["t_daily"], 2), ann=round(r["ann_ret"] * 100, 2), turn=round(r["turnover_per_yr"], 1))


def per_mask(idx, a, b):
    return (idx >= pd.Timestamp(a)) & (idx <= pd.Timestamp(b))
