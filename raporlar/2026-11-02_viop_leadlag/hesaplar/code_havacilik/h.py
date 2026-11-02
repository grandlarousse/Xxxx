"""havacilik ajanı yardımcı modülü (ll.py'yi DEĞİŞTİRMEZ, sadece kullanır).
Zamanlama: ll.py konvansiyonu. lag k>0 => sürücü önde. ABD/ICE/CME kapanışı BIST kapanışından sonra.
"""
import os, sys, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
S = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
sys.path.insert(0, S + "/code")
import ll  # noqa
OUT = S + "/out"
CODE = OUT + "/code_havacilik"
RES = CODE + "/res"
os.makedirs(RES, exist_ok=True)
STOCKS = ["THYAO", "PGSUS", "TAVHL"]
SPLIT = pd.Timestamp("2021-01-01")
LAST = pd.Timestamp("2026-10-30")

_rc = {}
def R(sym):
    """BIST takvimli log getiri (cache)."""
    if sym not in _rc:
        _rc[sym] = ll.ret(sym)
    return _rc[sym]

_dc = {}
def D(sym):
    if sym not in _dc:
        _dc[sym] = ll.decomp(sym)
    return _dc[sym]

def jet_crack():
    """Jet crack proxy: HO($/gal)*42 - Brent($/bbl). Getiri yerine: d(crack)/Brent_{t-1} (Brent fiyatına göre normalize değişim)."""
    ho = ll.daily("HO=F", "c"); bz = ll.daily("BZ=F", "c")
    df = pd.concat([ho.rename("ho"), bz.rename("bz")], axis=1).dropna()
    cr = df["ho"] * 42 - df["bz"]
    x = cr.diff() / df["bz"].shift(1)
    sd = x.rolling(250, min_periods=60).std().shift(1)
    x[(x.abs() > 12 * sd) & sd.notna()] = np.nan
    # ffill zero days -> 0 already; return
    return x.rename("JETCRACK")

def tstat_corr(r, n):
    return r * np.sqrt(max(n - 2, 1)) / np.sqrt(max(1 - r * r, 1e-12))

def _corr(a, b, start=None, end=None):
    df = pd.concat([a.rename("a"), b.rename("b")], axis=1).dropna()
    if start is not None: df = df[df.index >= pd.Timestamp(start)]
    if end is not None: df = df[df.index < pd.Timestamp(end)]
    if len(df) < 60: return np.nan, len(df)
    return df["a"].corr(df["b"]), len(df)

def _nwcorr(a, b, start=None, end=None, lags=5):
    """standardize edilmiş regresyon katsayısı (=corr) + Newey-West t"""
    df = pd.concat([a.rename("a"), b.rename("b")], axis=1).dropna()
    if start is not None: df = df[df.index >= pd.Timestamp(start)]
    if end is not None: df = df[df.index < pd.Timestamp(end)]
    if len(df) < 60: return np.nan, np.nan, len(df)
    za = (df["a"] - df["a"].mean()) / df["a"].std(); zb = (df["b"] - df["b"].mean()) / df["b"].std()
    b_, t_, n_ = ll.nw_t(za, zb, lags=lags)
    return df["a"].corr(df["b"]), t_, n_

def stat_block(stock, drv, drv_name=None, start="2010-01-01", usd=False, ctrl_extra=None):
    """Bir hisse-sürücü çifti için standart istatistik bloğu (BRIEF metodoloji 2a-2c, 3)."""
    a = R(stock) if not usd else (R(stock) - R("TRY=X"))
    b = R(drv) if isinstance(drv, str) else drv
    name = drv_name or (drv if isinstance(drv, str) else drv.name)
    a = a[a.index >= pd.Timestamp(start)]; b = b[b.index >= pd.Timestamp(start)]
    m = R("XU100")
    out = {"stock": stock + ("_USD" if usd else ""), "driver": name}
    df = pd.concat([a.rename("a"), b.rename("b"), m.rename("m")], axis=1).dropna()
    df = df[(df["b"] != 0)]  # tatil ffill sıfırlarını at (sürücü işlem görmedi)
    out["n"] = len(df)
    out["corr_full"] = df["a"].corr(df["b"])
    out["corr_3y"] = df[df.index >= LAST - pd.DateOffset(years=3)].pipe(lambda x: x["a"].corr(x["b"]))
    out["corr_1y"] = df[df.index >= LAST - pd.DateOffset(years=1)].pipe(lambda x: x["a"].corr(x["b"]))
    ctr = [df["m"]] + ([ctrl_extra.reindex(df.index)] if ctrl_extra is not None else [])
    out["pcorr_xu100"], _ = ll.partial_corr(df["a"], df["b"], ctr)
    out["pcorr_3y"], _ = ll.partial_corr(df["a"][df.index >= LAST - pd.DateOffset(years=3)], df["b"], [df["m"]])
    bb, tt, _ = ll.nw_t(df["a"], df["b"])
    out["beta"] = bb; out["t_sync"] = tt
    out["corr_IS"] = df[df.index < SPLIT].pipe(lambda x: x["a"].corr(x["b"]) if len(x) > 60 else np.nan)
    out["corr_OOS"] = df[df.index >= SPLIT].pipe(lambda x: x["a"].corr(x["b"]))
    out["pc_IS"], _ = ll.partial_corr(df["a"][df.index < SPLIT], df["b"], [df["m"]]) if (df.index < SPLIT).sum() > 60 else (np.nan, 0)
    out["pc_OOS"], _ = ll.partial_corr(df["a"][df.index >= SPLIT], df["b"], [df["m"]])
    yc = df.groupby(df.index.year).apply(lambda x: x["a"].corr(x["b"]) if len(x) > 60 else np.nan).dropna()
    out["yrs_same_sign"] = float((np.sign(yc) == np.sign(out["corr_full"])).mean()) if len(yc) else np.nan
    # partial by year
    def _pcy(x):
        if len(x) < 60: return np.nan
        return ll.partial_corr(x["a"], x["b"], [x["m"]])[0]
    pcy = df.groupby(df.index.year).apply(_pcy).dropna()
    out["yrs_pc_same_sign"] = float((np.sign(pcy) == np.sign(out["pcorr_xu100"])).mean()) if len(pcy) else np.nan
    # lag1 cc
    bz = b.where(b != 0)
    c1, t1, n1 = _nwcorr(a, bz.shift(1))
    out["corr_lag1"] = c1; out["t_lag1"] = t1
    # reverse: stock_{t-1} -> driver_t
    cr, trv, _ = _nwcorr(bz, a.shift(1))
    out["rev_corr"] = cr; out["rev_t"] = trv
    if ll.is_bist(ll.T(stock)):
        dd = D(stock); dd = dd[dd.index >= pd.Timestamp("2014-01-01")]
        if usd:
            pass
        g, tg, ng = _nwcorr(dd["gap"], bz.shift(1)); out["gap_corr"] = g; out["gap_t"] = tg
        i_, ti, ni = _nwcorr(dd["intra"], bz.shift(1)); out["intra_corr"] = i_; out["intra_t"] = ti; out["n_intra"] = ni
        out["intra_IS"], out["intra_IS_t"], _ = _nwcorr(dd["intra"], bz.shift(1), end=SPLIT)
        out["intra_OOS"], out["intra_OOS_t"], _ = _nwcorr(dd["intra"], bz.shift(1), start=SPLIT)
        # gun-ici: XU100 gun-ici'nden arındırılmış (hisseye özgü)
        mi = D("XU100")["intra"]
        x = pd.concat([dd["intra"].rename("y"), mi.rename("m")], axis=1).dropna()
        beta_m = np.polyfit(x["m"], x["y"], 1)[0]
        ex = (x["y"] - beta_m * x["m"])
        out["xintra_corr"], out["xintra_t"], _ = _nwcorr(ex, bz.shift(1))
        # çok günlü sürüklenme: sürücü_{t-1} -> intra_t + cc_{t+1..t+4}
        fw = dd["intra"] + sum(dd["cc"].shift(-k) for k in range(1, 5))
        out["drift5_corr"], out["drift5_t"], _ = _nwcorr(fw, bz.shift(1), lags=10)
        # lag2 cc (t+1 açılışı sonrası)
        out["corr_lag2"], out["t_lag2"], _ = _nwcorr(dd["cc"], bz.shift(2))
    return out

def fmt(df, nd=3):
    return df.round(nd).to_string()
