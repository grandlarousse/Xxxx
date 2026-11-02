"""v_S2_a bağımsız doğrulama yardımcıları (ll.py IMPORT EDİLMEZ; ham parquet'ten)."""
import numpy as np, pandas as pd, warnings, os
warnings.filterwarnings("ignore")
SCR = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
DATA = SCR + "/data"
OUT = SCR + "/out/code_v_S2_a/res"
UP, DN = np.log(1.105), np.log(0.895)

def rawd(sym, kind="daily"):
    d = pd.read_parquet(f"{DATA}/{kind}/{sym}.parquet")
    return d

def dser(sym, field="c", drop_zero_vol=False):
    """Günlük seri, index = ldate (yerel tarih), tekrarlar son."""
    d = rawd(sym)
    if drop_zero_vol:
        d = d[d["v"].fillna(0) > 0]
    s = pd.Series(d[field].values.astype(float), index=pd.DatetimeIndex(d["ldate"].values))
    s = s[~s.index.duplicated(keep="last")]
    s = s[s > 0].dropna()
    return s

def bist_ohlc(sym):
    d = rawd(sym); d = d[d["v"].fillna(0) > 0].copy()
    d.index = pd.DatetimeIndex(d["ldate"].values); d = d[~d.index.duplicated(keep="last")]
    return d[["o", "h", "l", "c", "adj", "v"]].astype(float)

def bist_decomp(sym):
    """Kendi ayrıştırmam: cc (adj), intra = ln(c/o), gap = cc - intra. Simetrik ±%10,5 temizlik (cc ve gap'te).
    Şüpheli açılış (o<=0, h==l & o==önceki c) NaN. 2014 öncesi gap/intra NaN."""
    d = bist_ohlc(sym)
    cc = np.log(d.adj).diff()
    # cc'yi yalnızca ardışık işlem günlerinde say (index zaten işlem günleri)
    intra = np.log(d.c / d.o)
    bad_o = (d.o <= 0) | ((d.h == d.l) & (d.o == d.c.shift(1)))
    intra[bad_o] = np.nan
    gap = cc - intra
    out = pd.DataFrame({"cc": cc, "gap": gap, "intra": intra, "o": d.o, "c": d.c, "adj": d.adj, "v": d.v})
    bad = (out.cc > UP) | (out.cc < DN)
    out.loc[bad, ["cc", "gap", "intra"]] = np.nan
    badg = (out.gap > UP) | (out.gap < DN)
    out.loc[badg, ["gap", "intra"]] = np.nan
    out.loc[out.index < "2014-01-01", ["gap", "intra"]] = np.nan
    return out

def nw(y, X, lags=5):
    import statsmodels.api as sm
    df = pd.concat([y.rename("y"), X], axis=1).dropna()
    m = sm.OLS(df["y"], sm.add_constant(df.drop(columns="y"))).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    return m, len(df)

def nw_mean(x, lags=5):
    import statsmodels.api as sm
    x = pd.Series(x).dropna()
    if len(x) < 10: return np.nan, np.nan, len(x)
    m = sm.OLS(x.values, np.ones(len(x))).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    return m.params[0], m.tvalues[0], len(x)

def bt(sig, y, cost_bps=8.0, thr=0.0, start=None, end=None):
    """pos = sign(sig) if |sig|>thr. pnl = pos*y - cost*|pos|. Sharpe = yıllık (sıfır günler dahil, 252)."""
    df = pd.concat([sig.rename("s"), y.rename("y")], axis=1).dropna()
    if start: df = df[df.index >= start]
    if end: df = df[df.index <= end]
    pos = np.sign(df.s).where(df.s.abs() > thr, 0.0)
    pnl = pos * df.y - cost_bps / 1e4 * pos.abs()
    act = pos != 0
    n = int(act.sum())
    if n < 5: return dict(n=n)
    pa = pnl[act]
    m, t, _ = nw_mean(pa)
    sh = pnl.mean() / pnl.std() * np.sqrt(252) if pnl.std() > 0 else np.nan
    eq = pnl.cumsum(); dd = (eq - eq.cummax()).min()
    return dict(n=n, n_days=len(df), mean_bps=1e4 * pa.mean(), t=t, hit=float((pa > 0).mean()), sharpe=sh,
                long_frac=float((pos[act] > 0).mean()), maxdd_pct=100 * dd, ann_pct=100 * pnl.mean() * 252)
