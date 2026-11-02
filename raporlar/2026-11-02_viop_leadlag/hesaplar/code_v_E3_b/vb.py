"""v_E3_b bağımsız kütüphane (ll.py / elib.py / vlib.py IMPORT EDİLMEZ). Ham parquet -> kendi hizalama ve temizlik.
Kurallar:
- BIST günü t: TUPRS.IS ve XU100.IS ldate'leri (v>0). gün-içi = ln(c/o) (aynı gün, ölçek düzeltmesinden bağımsız).
  cc = ln(adj_t/adj_{t-1}); gap = cc - intra. Temizlik: fiyat bazlı c_t/c_{t-1} [0,895;1,105] dışı -> cc/gap/intra NaN (simetrik);
  o, [l,h] dışında ise (%0,1 tolerans) intra/gap NaN; |intra|>0,2 NaN.
- ABD/vadeli sürücü: ldate = yerel işlem tarihi; kapanış 20-21 UTC (BIST t-1 kapanışından sonra, BIST t açılışından önce).
  sigA(t)  = ln P(ldate<=t_{-1}) - ln P(ldate<=t_{-2})   (ll tarzı lag1; BIST tatilinden sonra bayat kalabilir)
  sigC(t)  = ln P(ldate< t)      - ln P(ldate< t_{-1})   (BIST t-1 açılışı ile t açılışı arasında biten TÜM ABD kapanışları; taze)
- FX '=X': ldate L 'c' = L günü 00:00 UTC fiyatı. sigFX(t) = ln P_fx(ldate<=t) - ln P_fx(ldate<=t_{-1}) => t günü 00:00 UTC'ye kadar
  bilinen değişim (BIST açılışından önce bilinir).
"""
import os, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
S = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
D = S + "/data"; RES = S + "/out/code_v_E3_b/res"
SPLIT = pd.Timestamp("2021-01-01")
_c = {}
def raw(sym, kind="daily"):
    k = (sym, kind)
    if k not in _c:
        p = f"{D}/{kind}/{sym.replace('/', '_')}.parquet"
        d = pd.read_parquet(p)
        if kind == "daily":
            d = d.copy(); d.index = pd.DatetimeIndex(pd.to_datetime(d["ldate"]).values).normalize()
            d = d[~d.index.duplicated(keep="last")].sort_index()
        _c[k] = d
    return _c[k]

def bist_cal(start="2013-06-01"):
    a = raw("TUPRS.IS"); b = raw("XU100.IS")
    ia = a.index[(a["v"].fillna(0) > 0)]; ib = b.index[(b["v"].fillna(0) > 0)]
    cal = ia.intersection(ib)
    return cal[cal >= pd.Timestamp(start)]

def bist_dec(sym, cal=None):
    d = raw(sym).copy()
    for c in "ohlc": d[c] = d[c].astype(float)
    d = d[(d.c > 0) & (d.o > 0)]
    pr = d.c / d.c.shift(1)
    bad = (pr > 1.105) | (pr < 0.895)
    cc = np.log(d.adj / d.adj.shift(1))
    intra = np.log(d.c / d.o)
    badopen = (d.o > d.h * 1.001) | (d.o < d.l * 0.999) | (intra.abs() > 0.2)
    out = pd.DataFrame({"cc": cc, "intra": intra}, index=d.index)
    out.loc[bad, ["cc", "intra"]] = np.nan
    out.loc[badopen, "intra"] = np.nan
    out["gap"] = out.cc - out.intra
    out["o_eq_pc"] = (d.o == d.c.shift(1)).astype(float)
    out["o"] = d.o; out["c"] = d.c; out["h"] = d.h; out["l"] = d.l; out["v"] = d.v; out["pc"] = d.c.shift(1)
    if cal is not None: out = out.reindex(cal)
    return out

def px(sym, field="adj"):
    d = raw(sym)
    s = d[field].astype(float) if field in d else d["c"].astype(float)
    s = s[(s > 0)].dropna()
    return s

def _asof(s, dates, strict):
    """s: fiyat (index yerel tarih). dates'teki her t için ldate<=t (strict=False) veya < t (strict=True) olan son fiyat."""
    idx = s.index.values
    pos = np.searchsorted(idx, dates.values, side=("left" if strict else "right")) - 1
    v = np.where(pos >= 0, s.values[np.clip(pos, 0, None)], np.nan)
    return pd.Series(v, index=dates)

def sig(sym, cal, kind="A", field="adj", clean_sd=12.0):
    s = px(sym, field)
    # sürücüde aşırı değer temizliği: 12 sigma (yerel getiri bazında)
    r = np.log(s).diff(); sd = r.std()
    bad = r.abs() > clean_sd * sd
    if sym.endswith("=X"):
        p = _asof(s, cal, strict=False)  # t günü 00:00 UTC
        out = np.log(p).diff()
    elif kind == "A":
        p = _asof(s, cal, strict=False); out = np.log(p).diff().shift(1)
    elif kind == "C":
        p = _asof(s, cal, strict=True); out = np.log(p).diff()
    else:
        raise ValueError(kind)
    # kirli yerel getirileri içeren günleri NaN
    if bad.any():
        bd = r.index[bad]
        if sym.endswith("=X"):
            m = pd.Series(cal.isin(bd), index=cal)
        elif kind == "A":
            nxt = pd.Series(_asof(pd.Series(np.arange(len(s)), index=s.index).astype(float), cal, False).values, index=cal)
            m = pd.Series(False, index=cal)
            for b in bd:
                k = s.index.get_loc(b)
                m |= (nxt.shift(1) >= k) & (nxt.shift(2) < k)
        else:
            nxt = pd.Series(_asof(pd.Series(np.arange(len(s)), index=s.index).astype(float), cal, True).values, index=cal)
            m = pd.Series(False, index=cal)
            for b in bd:
                k = s.index.get_loc(b)
                m |= (nxt >= k) & (nxt.shift(1) < k)
        out[m.values] = np.nan
    return out

def nw(y, X=None, lags=5, add_const=True):
    """OLS + Newey-West HAC t. y: Series; X: DataFrame/Series. dönüş: (params, tvalues, n)"""
    import statsmodels.api as sm
    if X is None:
        df = pd.DataFrame({"y": y}).dropna(); Xm = np.ones((len(df), 1))
        m = sm.OLS(df["y"].values, Xm).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
        return pd.Series(m.params, ["const"]), pd.Series(m.tvalues, ["const"]), len(df)
    X = X.to_frame() if isinstance(X, pd.Series) else X
    df = pd.concat([y.rename("__y"), X], axis=1).dropna()
    Xm = df.drop(columns="__y")
    if add_const: Xm = sm.add_constant(Xm, has_constant="add")
    m = sm.OLS(df["__y"].values, Xm.values).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    return pd.Series(m.params, Xm.columns), pd.Series(m.tvalues, Xm.columns), len(df)

def zsig(s, win=250, minp=60):
    mu = s.rolling(win, min_periods=minp).mean().shift(1); sd = s.rolling(win, min_periods=minp).std().shift(1)
    return (s - mu) / sd

def bt(signal, target, thr=1.0, mode="z", cost=0.0, win=250):
    df = pd.concat([signal.rename("s"), target.rename("y")], axis=1).dropna()
    if mode == "z":
        z = zsig(df.s, win); pos = np.sign(z).where(z.abs() > thr, 0.0).fillna(0.0)
    else:
        pos = np.sign(df.s).where(df.s.abs() > thr, 0.0)
    pnl = pos * df.y - cost / 1e4 * pos.abs()
    return pnl, pos

def tstat(x, lags=5):
    x = pd.Series(x).dropna()
    if len(x) < 10: return np.nan
    _, t, _ = nw(x, None, lags); return float(t.iloc[0])

def stats(pnl, pos, label=""):
    a = pos != 0; p = pnl[a]
    if a.sum() < 10: return dict(n=int(a.sum()))
    ann = p.mean() * 252 * a.mean(); vol = pnl.std() * np.sqrt(252)
    return dict(n=int(a.sum()), bps=1e4 * p.mean(), t=tstat(p), hit=float((p > 0).mean()), sharpe=ann / vol if vol > 0 else np.nan)

def split_stats(pnl, pos):
    out = {}
    for k, m in [("ALL", pnl.index >= "1900"), ("IS", pnl.index < SPLIT), ("OOS", pnl.index >= SPLIT)]:
        out[k] = stats(pnl[m], pos[m])
    return out

def isy_close(code, cal):
    """İş Yatırım günlük endeks kapanışı (data/isy/d). Sadece kapanış (px)."""
    d = pd.read_parquet(f"{D}/isy/d/{code}.parquet")
    s = pd.Series(d["px"].astype(float).values, index=pd.DatetimeIndex(pd.to_datetime(d["ldate"]).values).normalize())
    s = s[~s.index.duplicated(keep="last")].sort_index()
    return s.reindex(cal)
