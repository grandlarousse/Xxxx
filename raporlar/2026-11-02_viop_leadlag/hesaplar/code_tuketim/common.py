"""tuketim ajanı ortak yardımcıları (ll.py'yi DEĞİŞTİRMEZ, sadece kullanır).
Zamanlama: ll.py konvansiyonu. Sürücü lag0 = BIST takviminde (t_önceki, t] yerel tarihli kapanış.
ABD/vadeli kapanışı BIST kapanışından sonra -> lag1 cc etkisi çoğunlukla gap'te (işlenemez); işlenebilir = lag1 -> intra.
"""
import sys, os, numpy as np, pandas as pd
SCR = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
sys.path.insert(0, SCR + "/code")
import ll  # noqa
OUT = SCR + "/out"
CODE = OUT + "/code_tuketim"
STOCKS = ["BIMAS", "MGROS", "SOKM", "ULKER", "AEFES"]
START = "2014-01-01"; SPLIT = "2021-01-01"
_P = None; _D = None
def panel():
    global _P
    if _P is None: _P = pd.read_parquet(SCR + "/data/panel_ret_bistcal.parquet")
    return _P
def dpanel():
    global _D
    if _D is None: _D = pd.read_parquet(SCR + "/data/panel_decomp_bist.parquet")
    return _D
def R(sym):
    """BIST takvimli log getiri (panelde varsa panelden; yoksa ll.ret)."""
    y = ll.T(sym); P = panel()
    if y in P.columns: return P[y].copy()
    return ll.ret(y)
def DEC(stock):
    D = dpanel()
    if stock in D.columns.get_level_values(0): return D[stock].copy()
    return ll.decomp(stock)
def zero_mask(r):
    """BIST dışı sürücüde tatil-ffill sıfırlarını NaN yap (korelasyonu sulandırmasın)."""
    r = r.copy(); r[r == 0] = np.nan; return r
def nwcorr(a, b, lags=5):
    df = pd.concat([a.rename("a"), b.rename("b")], axis=1).dropna()
    if len(df) < 60: return np.nan, np.nan, len(df)
    c = df["a"].corr(df["b"])
    za = (df["a"] - df["a"].mean()) / df["a"].std(); zb = (df["b"] - df["b"].mean()) / df["b"].std()
    _, t, n = ll.nw_t(za, zb, lags)
    return c, t, n
def resid(y, X):
    """y'yi X'e (DataFrame/Series) göre artık; ortak indeks."""
    X = pd.DataFrame(X)
    df = pd.concat([y.rename("y"), X], axis=1).dropna()
    C = np.column_stack([np.ones(len(df)), df.drop(columns="y").values])
    b = np.linalg.lstsq(C, df["y"].values, rcond=None)[0]
    return pd.Series(df["y"].values - C @ b, index=df.index), b
def beta(y, x, controls=None):
    X = pd.concat([x.rename("x")] + ([c.rename(f"c{i}") for i, c in enumerate(controls)] if controls else []), axis=1)
    import statsmodels.api as sm
    df = pd.concat([y.rename("y"), X], axis=1).dropna()
    if len(df) < 60: return np.nan, np.nan
    m = sm.OLS(df["y"].values, sm.add_constant(df.drop(columns="y").values)).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
    return m.params[1], m.tvalues[1]
def win(s, start=None, end=None):
    if start is not None: s = s[s.index >= pd.Timestamp(start)]
    if end is not None: s = s[s.index < pd.Timestamp(end)]
    return s
LAST = pd.Timestamp("2026-10-30")
def pair_stats(stock, drv, start=START, zero_nan=True, usd=False):
    """Standart çift istatistikleri (BRIEF 2a-c, 3)."""
    a = R(stock); b = R(drv)
    if zero_nan and not ll.is_bist(ll.T(drv)): b = zero_mask(b)
    m = R("XU100"); fx = R("TRY=X")
    if usd: a = a - fx
    a, b, m = win(a, start), win(b, start), win(m, start)
    o = {"stock": stock, "driver_yahoo": drv}
    o["corr_full"], o["t_sync"], o["n"] = nwcorr(a, b)
    o["corr_3y"] = nwcorr(win(a, LAST - pd.DateOffset(years=3)), b)[0]
    o["corr_1y"] = nwcorr(win(a, LAST - pd.DateOffset(years=1)), b)[0]
    o["pcorr_xu100"], _ = ll.partial_corr(a, b, [m])
    o["pcorr_xu100_try"], _ = ll.partial_corr(a, b, [m, fx])
    o["pc_IS"], _ = ll.partial_corr(win(a, None, SPLIT), b, [m])
    o["pc_OOS"], _ = ll.partial_corr(win(a, SPLIT), b, [m])
    o["c_IS"] = nwcorr(win(a, None, SPLIT), b)[0]; o["c_OOS"] = nwcorr(win(a, SPLIT), b)[0]
    o["beta"], o["beta_t"] = beta(a, b)
    o["beta_xu100ctl"], o["beta_xu100ctl_t"] = beta(a, b, [m])
    # yıllık işaret tutarlılığı (kısmi)
    yrs = []
    for y in range(pd.Timestamp(start).year, 2027):
        aa = a[a.index.year == y]
        if aa.notna().sum() < 100: continue
        pc, n = ll.partial_corr(aa, b, [m])
        yrs.append(pc)
    yrs = np.array(yrs); sgn = np.sign(o["pcorr_xu100"])
    o["yrs_same_sign_pc"] = float((np.sign(yrs) == sgn).mean()) if len(yrs) else np.nan
    o["n_years"] = len(yrs)
    # öncülük
    o["lag1_cc"], o["lag1_cc_t"], _ = nwcorr(a, b.shift(1))
    dd = DEC(stock); dd = win(dd, max(pd.Timestamp(start), pd.Timestamp("2014-01-01")))
    if usd:
        pass
    o["gap_corr"], o["gap_t"], _ = nwcorr(dd["gap"], b.shift(1))
    o["intra_corr"], o["intra_t"], o["n_intra"] = nwcorr(dd["intra"], b.shift(1))
    o["intra_IS"], o["intra_IS_t"], _ = nwcorr(win(dd["intra"], None, SPLIT), b.shift(1))
    o["intra_OOS"], o["intra_OOS_t"], _ = nwcorr(win(dd["intra"], SPLIT), b.shift(1))
    # hisseye özgü gün-içi (XU100 gün-içi artığı)
    xi = DEC("XU100")["intra"] if "XU100" in dpanel().columns.get_level_values(0) else None
    if xi is not None:
        ri, _ = resid(dd["intra"], xi)
        o["intra_resid_corr"], o["intra_resid_t"], _ = nwcorr(ri, b.shift(1))
    # çok günlük sürüklenme: d_{t-1} -> r_{t+1..t+4}
    fwd = sum(a.shift(-k) for k in range(1, 5))
    o["drift_corr"], o["drift_t"], _ = nwcorr(fwd, b.shift(1), lags=8)
    # ters yön: hisse_{t-1} -> sürücü_t
    o["rev_corr"], o["rev_t"], _ = nwcorr(b, a.shift(1))
    return o
