"""GÖREV 3: Saatlik (h1) ve 5 dk (m5) öncülük: endeks barları -> hisse barları (lag 0..L, hisse kendi lag'leri kontrollü), ters yön,
hisse-hariç (ex) endeksle mekanik kısım ayrımı, endeks->endeks (büyük->küçük, sektörler arası).
Kaynak: 'isy' (İş Yatırım; bar etiketi = bar başlangıcı UTC, :00 ızgara; h1 2017+, m5 2024+) veya 'yh' (Yahoo; h1 2023-11+ :30 ızgara, m5 son 60 gün).
Kapanış müzayedesi barı (15:00 UTC etiketi) ve günün ilk barı (gece gap'i) regresyon dışı. Lag'ler gün sınırını geçmez.
Kullanım: python3 s4_intraday.py isy h1 | isy m5 | yh m5 | yh h1
"""
import sys
from ye_common import *
SRC, KIND = (sys.argv[1], sys.argv[2]) if len(sys.argv) > 2 else ("isy", "h1")
L = 3 if KIND == "h1" else 6
H1START = pd.Timestamp("2017-01-01")

def px(code):
    if SRC == "isy":
        p = f"{ISY}/{KIND}/{code}.parquet"
        if not os.path.exists(p): return None
        s = pd.read_parquet(p)["px"]
    else:
        p = f"{SCR}/data/{KIND}/{code}.IS.parquet"
        if not os.path.exists(p): return None
        s = pd.read_parquet(p)["c"]; s.index = s.index.tz_convert(None)
    s = s[(s > 0)].astype(float); s = s[~s.index.duplicated(keep="last")]
    return s[(s.index >= (H1START if KIND == "h1" else "2000")) & (s.index < END + pd.Timedelta(days=1))]

def bar_ret(s):
    date = (s.index + pd.Timedelta(hours=3)).normalize()
    r = np.log(s).diff(); r[date != np.roll(date, 1)] = np.nan
    auc = (s.index.hour == 15) & (s.index.minute == 0) if SRC == "isy" or KIND == "m5" else (s.index.hour == 15)
    r[auc] = np.nan
    r[(r.abs() > 0.09)] = np.nan
    return pd.DataFrame({"r": r.values, "date": date}, index=s.index)

def lagm(df, col, k):
    x = df[col].shift(k); x[df["date"].shift(k) != df["date"]] = np.nan; return x

def fit(y, X, lags_nw):
    b, t, n, r2 = ols_nw(y, X, lags=lags_nw); return b, t, n, r2

def sumtest(y, X, idx_cols):
    """Σβ (idx_cols) ve t'si (NW)."""
    yv = np.asarray(y, float); Xv = np.asarray(X, float); ok = np.isfinite(yv) & np.isfinite(Xv).all(1); yv = yv[ok]; Xv = np.column_stack([np.ones(ok.sum()), Xv[ok]])
    if len(yv) < 100: return np.nan, np.nan
    XtXi = np.linalg.pinv(Xv.T @ Xv); b = XtXi @ Xv.T @ yv; e = yv - Xv @ b; u = Xv * e[:, None]; S = u.T @ u
    for l in range(1, L + 2):
        w = 1 - l / (L + 2); G = u[l:].T @ u[:-l]; S += w * (G + G.T)
    V = XtXi @ S @ XtXi; c = np.zeros(len(b)); c[[i + 1 for i in idx_cols]] = 1
    return c @ b, (c @ b) / np.sqrt(c @ V @ c)

def leadlag(ys, xs, per=None, ctrl_own=True):
    """ys, xs: bar_ret DataFrame'leri (aynı ızgara). y_t = a + Σ_{k=0..L} β_k x_{t-k} + Σ_{k=1..L} γ_k y_{t-k}."""
    df = pd.concat([ys["r"].rename("y"), xs["r"].rename("x"), ys["date"]], axis=1, join="inner").dropna(subset=["date"])
    if per is not None: df = df[(df["date"] >= per[0]) & (df["date"] <= per[1])]
    cols = {f"x{k}": (df["x"] if k == 0 else lagm(df, "x", k)) for k in range(L + 1)}
    if ctrl_own: cols.update({f"y{k}": lagm(df, "y", k) for k in range(1, L + 1)})
    X = pd.DataFrame(cols)
    # gün sınırını aşan gecikmeler 0 kabul edilir (satır atılmaz): y ve x0 mevcutsa gözlem kullanılır
    lagc = [c for c in X.columns if c != "x0"]; X[lagc] = X[lagc].fillna(0.0)
    b, t, n, r2 = fit(df["y"].values, X.values, L + 1)
    out = {"n": n, "r2": r2}
    for k in range(L + 1): out[f"b{k}"] = b[1 + k]; out[f"t{k}"] = t[1 + k]
    sb, st = sumtest(df["y"].values, X.values, list(range(1, L + 1))); out["sum_lag"] = sb; out["t_sum_lag"] = st
    tot = sum(out[f"b{k}"] for k in range(L + 1)); out["lag_share"] = sb / tot if tot else np.nan
    return out

IDX = ["XU030", "XBANK", "XUSIN", "XHOLD", "XLBNK"]
if __name__ == "__main__":
    tag = f"{SRC}_{KIND}"
    PR = {k: bar_ret(px(k)) for k in IDX + ["XU100", "XTUMY", "XYUZO", "X10XB", "XUMAL", "XKMYA", "XMANA", "XULAS", "XELKT", "XGIDA", "XTAST", "XILTM", "XUHIZ", "XUTEK", "XTCRT"]
          if px(k) is not None}
    first = min(v.index[0] for v in PR.values()); last = max(v.index[-1] for v in PR.values())
    PERS = {"full": (pd.Timestamp("2000-01-01"), END)}
    if KIND == "h1" and SRC == "isy": PERS.update({"IS": (H1START, SPLIT - pd.Timedelta(days=1)), "OOS": (SPLIT, END)})
    if SRC == "isy": PERS.update({k: (pd.Timestamp(a), pd.Timestamp(b)) for k, (a, b) in REGIMES.items()})
    else: PERS.update({"pre_crisis": (pd.Timestamp("2000-01-01"), pd.Timestamp("2026-09-15")), "fon_krizi_16Eyl+": (pd.Timestamp("2026-09-16"), END)})
    rows = []
    liqd = pd.read_csv(RES + "/viop_liquidity.csv", index_col=0) if os.path.exists(RES + "/viop_liquidity.csv") else None
    for s in VIOP:
        p = px(s)
        if p is None: continue
        S_ = bar_ret(p)
        for I in IDX:
            if I not in PR: continue
            XI = PR[I]
            # hisse-hariç endeks (günlük NNLS ağırlığı)
            df = pd.concat([XI["r"].rename("i"), S_["r"].rename("s"), XI["date"]], axis=1, join="inner")
            w = weight_series(I, s, pd.DatetimeIndex(df["date"].unique())).reindex(df["date"]).values
            ex = np.log1p((np.expm1(df["i"]) - w * np.expm1(df["s"]).fillna(0)) / (1 - w))
            XE = pd.DataFrame({"r": ex.values, "date": df["date"].values}, index=df.index)
            for var, X_ in [("raw", XI), ("ex", XE)]:
                for pn, pr in PERS.items():
                    o = leadlag(S_, X_, pr); o.update(stock=s, idx=I, var=var, dir="idx->stk", per=pn, w=float(np.nanmean(w))); rows.append(o)
                    if pn in ("full", "OOS", "fon_krizi_16Eyl+", "2026_EylEki_fon_krizi"):
                        o = leadlag(X_, S_, pr); o.update(stock=s, idx=I, var=var, dir="stk->idx", per=pn, w=float(np.nanmean(w))); rows.append(o)
        print(s, flush=True)
    R_ = pd.DataFrame(rows); R_.to_csv(RES + f"/intraday_{tag}.csv", index=False)
    # endeks -> endeks
    pairs = [("XU030", "XTUMY"), ("XTUMY", "XU030"), ("XU030", "XYUZO"), ("XYUZO", "XU030"), ("XBANK", "XUSIN"), ("XUSIN", "XBANK"), ("XLBNK", "X10XB"), ("X10XB", "XLBNK"),
             ("XUMAL", "XHOLD"), ("XHOLD", "XUMAL"), ("XBANK", "XHOLD"), ("XHOLD", "XBANK"), ("XU030", "XU100"), ("XU100", "XU030"), ("XBANK", "XUHIZ"), ("XUSIN", "XUHIZ"),
             ("XBANK", "XKMYA"), ("XBANK", "XMANA"), ("XBANK", "XULAS"), ("XU030", "XKMYA"), ("XU030", "XMANA"), ("XU030", "XULAS"), ("XU030", "XELKT"), ("XU030", "XGIDA"),
             ("XU030", "XTAST"), ("XU030", "XILTM"), ("XU030", "XTCRT"), ("XU030", "XUTEK"), ("XU030", "XHOLD"), ("XU030", "XBANK"), ("XBANK", "XU030")]
    rr = []
    for a, b in pairs:
        if a not in PR or b not in PR: continue
        for pn, pr in PERS.items():
            o = leadlag(PR[b], PR[a], pr); o.update(leader=a, follower=b, per=pn); rr.append(o)
    RR = pd.DataFrame(rr); RR.to_csv(RES + f"/intraday_idx_{tag}.csv", index=False)
    pd.set_option("display.width", 250)
    print(RR[RR.per == "full"][["leader", "follower", "n", "b0", "b1", "t1", "b2", "t2", "sum_lag", "t_sum_lag", "lag_share"]].round(3).to_string())
    f = R_[(R_.per == "full")]
    print(f.groupby(["dir", "idx", "var"])[["b0", "b1", "t1", "sum_lag", "t_sum_lag", "lag_share"]].median().round(3).to_string())
    print(f.groupby(["dir", "idx", "var"]).apply(lambda g: pd.Series({"n_t_sum>3": (g.t_sum_lag > 3).sum(), "n_t_sum<-3": (g.t_sum_lag < -3).sum(), "n": len(g)})).to_string())
