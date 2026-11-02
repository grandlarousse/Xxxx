"""v_M4_a BAĞIMSIZ yardımcı modül. ll.py / mh.py IMPORT EDİLMEZ; her şey ham parquet'ten.
Zamanlama: BIST günü t için sürücü fiyatı = sürücünün yerel tarihi (ldate) <= t olan son kapanışı.
Tokyo (.T) kapanışı 06:00 UTC (2024-11-05'ten itibaren 06:30 UTC), ASX (.AX) kapanış müzayedesi ~05:10 UTC (Avust. yaz saati) / ~06:10 UTC,
Kore (.KS) 06:30 UTC. BIST açılış müzayedesi eşleşmesi ~06:55-07:00 UTC (2016+; 2016 öncesi TR kışında 1 saat geç).
"""
import os, numpy as np, pandas as pd
SCR = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
DATA = os.path.join(SCR, "data")
OUT = os.path.join(SCR, "out", "code_v_M4_a")
UP, DN = np.log(1.105), np.log(0.895)
SPLIT = pd.Timestamp("2021-01-01")
_c = {}

def raw(sym, kind="daily"):
    k = (sym, kind)
    if k not in _c:
        _c[k] = pd.read_parquet(os.path.join(DATA, kind, sym + ".parquet"))
    return _c[k]

def is_bist(sym): return sym.endswith(".IS")

def px(sym, field="adj"):
    d = raw(sym)
    s = pd.Series(d[field].values, index=pd.DatetimeIndex(d["ldate"].values), dtype=float)
    keep = ~s.index.duplicated(keep="last")
    s = s[keep]
    if is_bist(sym):
        v = pd.Series(d["v"].values, index=pd.DatetimeIndex(d["ldate"].values))[keep]
        if (v.fillna(0) > 0).mean() > 0.5:
            s = s[v.fillna(0).values > 0]
    s = s[(s > 0) & s.notna()]
    return s

_cal = None
def cal():
    global _cal
    if _cal is None:
        d = raw("XU100.IS"); idx = pd.DatetimeIndex(d["ldate"].values)
        v = d["v"].fillna(0).values
        if (v > 0).mean() > 0.5: idx = idx[v > 0]
        _cal = idx.unique().sort_values()
    return _cal

def on_cal(s):
    c = cal(); c = c[c >= s.index[0]]
    return s.reindex(s.index.union(c)).ffill().reindex(c)

def ret(sym, sigma_clip=12.0, zero_nan=True):
    """BIST takviminde log getiri. BIST dışı: geçmiş 250g sd'nin sigma_clip katı üstü sıçramalar NaN (None=temizlik yok).
    zero_nan: tatil ffill sıfırları NaN."""
    s = on_cal(px(sym)); r = np.log(s).diff()
    if is_bist(sym):
        r[(r > UP) | (r < DN)] = np.nan
    elif sigma_clip:
        sd = r.rolling(250, min_periods=60).std().shift(1)
        r[(r.abs() > sigma_clip * sd) & sd.notna()] = np.nan
    if zero_nan: r = r.where(r != 0)
    return r

def decomp(sym, start="2014-01-01"):
    """cc = log adj farkı (hissenin kendi işlem günleri), intra = log(c/o), gap = cc - intra."""
    d = raw(sym).copy(); d.index = pd.DatetimeIndex(d["ldate"].values); d = d[~d.index.duplicated(keep="last")]
    if (d["v"].fillna(0) > 0).mean() > 0.5: d = d[d["v"].fillna(0) > 0]
    cc = np.log(d["adj"]).diff(); intra = np.log(d["c"] / d["o"])
    bad_o = (d["o"] <= 0) | d["o"].isna() | ((d["h"] == d["l"]) & (d["o"] == d["c"].shift(1)))
    intra[bad_o] = np.nan
    gap = cc - intra
    o = pd.DataFrame({"cc": cc, "gap": gap, "intra": intra, "o": d["o"], "c": d["c"], "pc": d["c"].shift(1)})
    bad = (o["cc"] > UP) | (o["cc"] < DN)
    o.loc[bad, ["cc", "gap", "intra"]] = np.nan
    badg = (o["gap"] > UP) | (o["gap"] < DN)
    o.loc[badg, ["gap", "intra"]] = np.nan
    o.loc[o.index < pd.Timestamp(start), ["gap", "intra"]] = np.nan
    return o

def zpast(r, w=250, mp=60):
    mu = r.rolling(w, min_periods=mp).mean().shift(1); sd = r.rolling(w, min_periods=mp).std().shift(1)
    return (r - mu) / sd

def composite(syms, w=250, sigma_clip=12.0):
    Z = pd.concat([zpast(ret(s, sigma_clip=sigma_clip), w) for s in syms], axis=1)
    return Z.mean(axis=1, skipna=True)

# ---------- istatistik (kendi NW) ----------
def nw_mean_t(x, L=5):
    x = np.asarray(pd.Series(x).dropna(), float); n = len(x)
    if n < 20: return np.nan, np.nan, n
    m = x.mean(); e = x - m
    g0 = (e @ e) / n; s = g0
    for l in range(1, L + 1):
        g = (e[l:] @ e[:-l]) / n; s += 2 * (1 - l / (L + 1)) * g
    return m, m / np.sqrt(s / n), n

def nw_ols(y, X, L=5):
    """y: Series, X: DataFrame. sabit eklenir. HAC (Bartlett) t. Dönüş: (params, tvals, n)."""
    df = pd.concat([y.rename("_y"), X], axis=1).dropna()
    Y = df["_y"].values; Xm = np.column_stack([np.ones(len(df)), df.drop(columns="_y").values]); n, k = Xm.shape
    XtXi = np.linalg.inv(Xm.T @ Xm); b = XtXi @ Xm.T @ Y; u = Y - Xm @ b
    G = Xm * u[:, None]; S = G.T @ G
    for l in range(1, L + 1):
        w = 1 - l / (L + 1); M = G[l:].T @ G[:-l]; S += w * (M + M.T)
    V = XtXi @ S @ XtXi
    names = ["const"] + list(df.drop(columns="_y").columns)
    return pd.Series(b, names), pd.Series(b / np.sqrt(np.diag(V)), names), n

def corr_t(a, b, L=5):
    df = pd.concat([a.rename("a"), b.rename("b")], axis=1).dropna()
    if len(df) < 40: return np.nan, np.nan, len(df)
    za = (df.a - df.a.mean()) / df.a.std(); zb = (df.b - df.b.mean()) / df.b.std()
    p, t, n = nw_ols(za, zb.to_frame("b"), L)
    return df.a.corr(df.b), t["b"], n

def positions(sig, tgt, mode="z", thr=1.0, w=250, rez=True):
    df = pd.concat([sig.rename("s"), tgt.rename("y")], axis=1).dropna()
    if mode == "z":
        s = zpast(df["s"], w) if rez else df["s"]
        pos = np.sign(s).where(s.abs() > thr, 0.0)
    else:
        pos = np.sign(df["s"]).where(df["s"].abs() > thr, 0.0)
    return pos.fillna(0.0), df["y"]

def bt(sig, tgt, cost=15.0, mode="z", thr=1.0, w=250, rez=True, split=SPLIT, periods=None):
    pos, y = positions(sig, tgt, mode, thr, w, rez)
    pnl = pos * y - cost / 1e4 * pos.abs()
    act = pos != 0
    def st(mask):
        p = pnl[act & mask]; n = len(p)
        if n < 15: return {"n": n, "bps": np.nan, "t": np.nan, "hit": np.nan, "sh": np.nan}
        m, t, _ = nw_mean_t(p)
        days = mask.sum(); ann = p.sum() / days * 252; vol = pnl[mask].std() * np.sqrt(252)
        return {"n": n, "bps": 1e4 * m, "t": t, "hit": float((p > 0).mean()), "sh": ann / vol if vol > 0 else np.nan}
    idx = pnl.index
    out = {"ALL": st(pd.Series(True, idx)), "IS": st(pd.Series((idx < split) & (idx >= pd.Timestamp("2014-01-01")), idx)),
           "OOS": st(pd.Series(idx >= split, idx))}
    yb = (1e4 * pnl[act].groupby(pnl[act].index.year).mean()).round(1)
    yn = pnl[act].groupby(pnl[act].index.year).size()
    out["yr"] = yb.to_dict(); out["yr_n"] = yn.to_dict()
    return out, pnl, pos

def flat(res, prefix=""):
    r = {}
    for k in ("ALL", "IS", "OOS"):
        for f, v in res[k].items(): r[f"{prefix}{k}_{f}"] = v
    yb = res["yr"]; r[f"{prefix}yrs_pos"] = f"{sum(v > 0 for v in yb.values())}/{len(yb)}"
    r[f"{prefix}by_year"] = ";".join(f"{k}:{v}" for k, v in yb.items())
    return r
