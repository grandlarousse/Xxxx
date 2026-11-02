"""kimya ajanı ortak yardımcıları (ll.py'yi DEĞİŞTİRMEZ, sadece kullanır).
Zamanlama: ll.py konvansiyonu. Sürücü getirisi r_d(t) = (BIST günü t-1, t] aralığında sürücünün son kapanışları arası.
lag1 = sürücü_{t-1}. ABD/vadeli kapanışlı sürücüde lag1->gap = eşzamansız kapanış (işlenemez); lag1->intra = işlenebilir.
"""
import sys, os, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
SCR = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
sys.path.insert(0, SCR + "/code")
import ll

OUT = SCR + "/out"
STOCKS = ["GUBRF", "HEKTS", "TKFEN", "SISE", "CIMSA", "OYAKC"]
SPLIT = pd.Timestamp("2021-01-01")
_rc = {}


def R(sym):
    if sym not in _rc:
        _rc[sym] = ll.ret(sym)
    return _rc[sym]


_dc = {}


def DEC(stock):
    if stock not in _dc:
        _dc[stock] = ll.decomp(stock)
    return _dc[stock]


def usd(stock):
    return R(stock) - R("TRY=X")


def _corr(a, b, start=None, end=None, min_n=60):
    df = pd.concat([a.rename("a"), b.rename("b")], axis=1).dropna()
    if start is not None: df = df[df.index >= pd.Timestamp(start)]
    if end is not None: df = df[df.index < pd.Timestamp(end)]
    if len(df) < min_n: return np.nan, len(df)
    return df["a"].corr(df["b"]), len(df)


def resid(y, X):
    """y'nin X (liste) üzerine OLS artığı (ortak örneklem)."""
    df = pd.concat([y.rename("y")] + [x.rename(f"x{i}") for i, x in enumerate(X)], axis=1).dropna()
    C = np.column_stack([np.ones(len(df))] + [df[f"x{i}"].values for i in range(len(X))])
    b = np.linalg.lstsq(C, df["y"].values, rcond=None)[0]
    return pd.Series(df["y"].values - C @ b, index=df.index)


def pc(a, b, controls, start=None, end=None, min_n=60):
    df = pd.concat([a.rename("a"), b.rename("b")] + [c.rename(f"c{i}") for i, c in enumerate(controls)], axis=1).dropna()
    if start is not None: df = df[df.index >= pd.Timestamp(start)]
    if end is not None: df = df[df.index < pd.Timestamp(end)]
    if len(df) < min_n: return np.nan, len(df)
    C = np.column_stack([np.ones(len(df))] + [df[f"c{i}"].values for i in range(len(controls))])
    ra = df["a"].values - C @ np.linalg.lstsq(C, df["a"].values, rcond=None)[0]
    rb = df["b"].values - C @ np.linalg.lstsq(C, df["b"].values, rcond=None)[0]
    return float(np.corrcoef(ra, rb)[0, 1]), len(df)


def nwt_corr(a, b, start=None, end=None):
    df = pd.concat([a.rename("a"), b.rename("b")], axis=1).dropna()
    if start is not None: df = df[df.index >= pd.Timestamp(start)]
    if end is not None: df = df[df.index < pd.Timestamp(end)]
    if len(df) < 60: return np.nan
    za = (df.a - df.a.mean()) / df.a.std(); zb = (df.b - df.b.mean()) / df.b.std()
    return ll.nw_t(za, zb)[1]


def by_year(a, b, controls=None):
    df = pd.concat([a.rename("a"), b.rename("b")] + ([c.rename(f"c{i}") for i, c in enumerate(controls)] if controls else []), axis=1).dropna()
    out = {}
    for y, g in df.groupby(df.index.year):
        if len(g) < 60: continue
        if controls:
            C = np.column_stack([np.ones(len(g))] + [g[f"c{i}"].values for i in range(len(controls))])
            ra = g.a.values - C @ np.linalg.lstsq(C, g.a.values, rcond=None)[0]
            rb = g.b.values - C @ np.linalg.lstsq(C, g.b.values, rcond=None)[0]
            out[y] = float(np.corrcoef(ra, rb)[0, 1])
        else:
            out[y] = g.a.corr(g.b)
    return pd.Series(out)


def pair(stock, drv, start="2005-01-01"):
    """Bir hisse-sürücü çifti için standart metrikler (brief formatına uygun)."""
    a = R(stock); b = R(drv); m = R("XU100")
    a = a[a.index >= start]
    last = a.dropna().index.max()
    d3 = last - pd.DateOffset(years=3); d1 = last - pd.DateOffset(years=1)
    o = {"stock": stock, "driver": drv}
    o["corr_full"], o["n"] = _corr(a, b)
    o["corr_3y"], _ = _corr(a, b, d3)
    o["corr_1y"], _ = _corr(a, b, d1, min_n=40)
    o["pc_full"], _ = pc(a, b, [m])
    o["pc_3y"], _ = pc(a, b, [m], d3)
    o["pc_1y"], _ = pc(a, b, [m], d1, min_n=40)
    o["pc_IS"], _ = pc(a, b, [m], "2014-01-01", SPLIT)
    o["pc_OOS"], _ = pc(a, b, [m], SPLIT)
    o["c_IS"], _ = _corr(a, b, "2014-01-01", SPLIT)
    o["c_OOS"], _ = _corr(a, b, SPLIT)
    # ek kontrol: XU100 + USDTRY + ACWI(lag0,lag1) -> küresel risk dışı sektörel maruziyet
    o["pc_ext"], _ = pc(a, b, [m, R("TRY=X"), R("ACWI"), R("ACWI").shift(1)], "2009-01-01")
    df = pd.concat([a.rename("a"), b.rename("b")], axis=1).dropna()
    o["beta"] = np.polyfit(df.b, df.a, 1)[0] if len(df) > 60 else np.nan
    o["t_sync"] = nwt_corr(resid(a, [m]), resid(b, [m])) if len(df) > 60 else np.nan
    by = by_year(a, b, [m]); sgn = np.sign(o["pc_full"])
    o["yrs_same_sign"] = float((np.sign(by) == sgn).mean()) if len(by) else np.nan
    o["n_years"] = len(by)
    # USD bazlı senkron
    o["corr_usd"], _ = _corr(usd(stock), b, "2009-01-01")
    # lag yapıları (2014+ decomp)
    dd = DEC(stock)
    bl = b.shift(1)
    for col in ["gap", "intra", "cc"]:
        o[f"{col}_l1"], _ = _corr(dd[col], bl, "2014-01-01")
        o[f"{col}_l1_t"] = nwt_corr(dd[col], bl, "2014-01-01")
    o["intra_l1_IS"], _ = _corr(dd["intra"], bl, "2014-01-01", SPLIT)
    o["intra_l1_OOS"], _ = _corr(dd["intra"], bl, SPLIT)
    # XU100 intra kontrollü işlenebilir öncülük (hisseye özgü mü?)
    xi = DEC("XU100")["intra"]
    o["intra_l1_pc"], _ = pc(dd["intra"], bl, [xi], "2014-01-01")
    # t+2..t+5 sürüklenme (cc)
    # sürüklenme: sürücü_t (ABD kapanışı t gecesi bilinir) -> t+1 kapanışında gir, t+5 kapanışında çık = a_{t+2..t+5}
    fwd = sum(a.shift(-k) for k in range(2, 6))
    o["drift_2_5"], _ = _corr(fwd, b, "2014-01-01")
    o["drift_2_5_t"] = nwt_corr(fwd, b, "2014-01-01")
    # ters yön: hisse_{t-1} -> sürücü_t (ve hisse_t -> sürücü_{t+1}); Asya için hisse_{t-1}->sürücü_t anlamlı
    o["rev_l1"], _ = _corr(b, a.shift(1), "2014-01-01")
    o["rev_l1_t"] = nwt_corr(b, a.shift(1), "2014-01-01")
    return o


def bt_stats(pnl, pos):
    act = pos != 0; n = int(act.sum())
    if n < 20: return {"n": n}
    pa = pnl[act]; m, t, _ = ll.nw_t(pa)
    ann = pa.mean() * 252 * act.mean(); vol = pnl.std() * np.sqrt(252)
    eq = pnl.cumsum(); dd = (eq - eq.cummax()).min()
    return {"n": n, "mean_bps": 1e4 * pa.mean(), "t": t, "hit": float((pa > 0).mean()), "sharpe": ann / vol if vol > 0 else np.nan,
            "ann_pct": 100 * ann, "maxdd_pct": 100 * dd}


def run_bt(sig, tgt, cost_bps, thr=0.0, mode="sign", z_window=250, split=SPLIT, start="2014-01-01"):
    """sig_t pozisyondan ÖNCE bilinir (çağıran hizalar). tgt_t = pozisyonun kazandığı getiri. Maliyet gidiş-dönüş cost_bps."""
    df = pd.concat([sig.rename("s"), tgt.rename("y")], axis=1).dropna()
    df = df[df.index >= pd.Timestamp(start)]
    if mode == "z":
        mu = df.s.rolling(z_window, min_periods=60).mean().shift(1); sd = df.s.rolling(z_window, min_periods=60).std().shift(1)
        z = (df.s - mu) / sd; pos = np.sign(z).where(z.abs() > thr, 0.0)
    else:
        pos = np.sign(df.s).where(df.s.abs() > thr, 0.0)
    pos = pos.fillna(0.0)
    pnl = pos * df.y - cost_bps / 1e4 * pos.abs()
    res = {"ALL": bt_stats(pnl, pos), "IS": bt_stats(pnl[pnl.index < split], pos[pos.index < split]),
           "OOS": bt_stats(pnl[pnl.index >= split], pos[pos.index >= split])}
    res["by_year_bps"] = (1e4 * pnl[pos != 0].groupby(pnl[pos != 0].index.year).mean()).round(1).to_dict()
    res["gross_by_year_bps"] = (1e4 * (pos * df.y)[pos != 0].groupby(pnl[pos != 0].index.year).mean()).round(1).to_dict()
    return res, pnl, pos
