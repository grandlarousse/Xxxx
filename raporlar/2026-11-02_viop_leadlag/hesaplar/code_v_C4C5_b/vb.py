"""v_C4C5_b — bağımsız doğrulama kütüphanesi (ll.py / vlib.py IMPORT EDİLMEZ).
Kendi hizalama + temizlik:
- BIST günlük: index = ldate (yerel tarih). cc = log(adj) farkı, intra = log(c/o), gap = cc - intra.
  Temizlik: bayat gün (v==0 ve h==l) atılır; fiyat bazında simetrik ±%10,5 (cc ve gap) -> NaN (opsiyonel rejim: 2020-03-13 öncesi ±%20,5);
  açılış şüpheli (o<=0 veya (h==l ve o==önceki c)) -> intra/gap NaN; 2014 öncesi intra/gap NaN.
- Yabancı (Asya) günlük: yerel tarih ldate; BIST günü t'ye (önceki BIST günü, t] aralığındaki yerel getirilerin toplamı.
  Yabancı işlem görmediyse: 'zero' modunda 0, 'nan' modunda NaN.
- NW t: standartlaştırılmış y ~ x regresyonu, Newey-West (Bartlett) lag=5.
"""
import os, json, glob, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
S = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
D = S + "/data"
UP, DN = np.log(1.105), np.log(0.895)
UP20, DN20 = np.log(1.205), np.log(0.795)
_c = {}

def raw(sym, kind="daily"):
    k = (sym, kind)
    if k not in _c:
        _c[k] = pd.read_parquet(f"{D}/{kind}/{sym}.parquet")
    return _c[k]

def daily_local(sym):
    d = raw(sym).copy()
    d.index = pd.DatetimeIndex(pd.to_datetime(d["ldate"].values))
    d = d[~d.index.duplicated(keep="last")].sort_index()
    return d

def bist_cal():
    if "cal" not in _c:
        x = daily_local("XU100.IS"); _c["cal"] = x.index[x["c"].notna()]
    return _c["cal"]

def _badmask(r, regime=False):
    if not regime:
        return (r > UP) | (r < DN)
    pre = r.index < pd.Timestamp("2020-03-13")
    up = np.where(pre, UP20, UP); dn = np.where(pre, DN20, DN)
    return (r > up) | (r < dn)

def bist_dec(sym, regime=False):
    k = ("dec", sym, regime)
    if k in _c: return _c[k]
    d = daily_local(sym)
    if (d["v"].fillna(0) > 0).mean() > 0.5:
        d = d[~((d["v"].fillna(0) <= 0) & (d["h"] == d["l"]))]
    cc = np.log(d["adj"]).diff()
    intra = np.log(d["c"] / d["o"])
    badopen = (d["o"] <= 0) | d["o"].isna() | ((d["h"] == d["l"]) & (d["o"] == d["c"].shift(1)))
    intra[badopen] = np.nan
    gap = cc - intra
    o = pd.DataFrame({"cc": cc, "gap": gap, "intra": intra})
    o.loc[_badmask(o["cc"], regime), :] = np.nan
    o.loc[o.index < "2014-01-01", ["gap", "intra"]] = np.nan
    o.loc[_badmask(o["gap"], regime), ["gap", "intra"]] = np.nan
    _c[k] = o
    return o

def to_bist(r_local, mode="zero"):
    """yerel tarihli getiri serisini BIST takvimine topla."""
    cal = bist_cal()
    r_local = r_local.dropna()
    r_local = r_local[(r_local.index > cal[0]) & (r_local.index <= cal[-1])]
    pos = cal.searchsorted(r_local.index, side="left")
    g = pd.Series(r_local.values, index=cal[pos])
    agg = g.groupby(level=0).sum()
    out = pd.Series(0.0 if mode == "zero" else np.nan, index=cal)
    out.loc[agg.index] = agg.values
    out[out.index <= r_local.index[0]] = np.nan
    return out

def loc_ret(sym, field="c"):
    d = daily_local(sym)
    p = d["adj"] if field == "adj" else d[field]
    return np.log(p).diff()

def nw_t(y, x=None, lags=5):
    """x verilirse: standartlaştırılmış regresyon eğimi (=corr) ve NW t. Yoksa ortalama ve NW t."""
    if x is None:
        e = np.asarray(y, float); e = e[~np.isnan(e)]; n = len(e); m = e.mean(); u = e - m
        v = u @ u / n
        for L in range(1, lags + 1):
            w = 1 - L / (lags + 1); v += 2 * w * (u[L:] @ u[:-L]) / n
        return m, m / np.sqrt(v / n), n
    df = pd.concat([pd.Series(y).rename("y"), pd.Series(x).rename("x")], axis=1).dropna()
    n = len(df)
    if n < 30: return np.nan, np.nan, n
    yy = (df.y - df.y.mean()) / df.y.std(); xx = (df.x - df.x.mean()) / df.x.std()
    b = (xx @ yy) / (xx @ xx); u = (yy - b * xx).values * xx.values
    v = u @ u / n
    for L in range(1, lags + 1):
        w = 1 - L / (lags + 1); v += 2 * w * (u[L:] @ u[:-L]) / n
    se = np.sqrt(v / n) / ((xx @ xx) / n)
    return b, b / se, n

def ols_nw(y, X, lags=5):
    """çoklu regresyon, NW t'ler. X: DataFrame. Sabit eklenir. Değişkenler standartlaştırılır."""
    df = pd.concat([y.rename("_y"), X], axis=1).dropna()
    Z = (df - df.mean()) / df.std()
    yv = Z["_y"].values; Xv = np.column_stack([np.ones(len(Z)), Z.drop(columns="_y").values])
    XtX = Xv.T @ Xv; b = np.linalg.solve(XtX, Xv.T @ yv); e = yv - Xv @ b
    n = len(yv); g = Xv * e[:, None]; Sm = g.T @ g / n
    for L in range(1, lags + 1):
        w = 1 - L / (lags + 1); G = g[L:].T @ g[:-L] / n; Sm += w * (G + G.T)
    Q = np.linalg.inv(XtX / n); V = Q @ Sm @ Q / n
    t = b / np.sqrt(np.diag(V))
    return pd.DataFrame({"b": b[1:], "t": t[1:]}, index=Z.drop(columns="_y").columns), n

def bt(sig, tgt, cost=10.0, split="2021-01-01", start=None, end=None):
    df = pd.concat([sig.rename("s"), tgt.rename("y")], axis=1).dropna()
    if start: df = df[df.index >= start]
    if end: df = df[df.index < end]
    pos = np.sign(df.s)
    pnl = pos * df.y - cost / 1e4 * pos.abs()
    def st(p, ps):
        a = ps != 0; n = int(a.sum())
        if n < 20: return dict(n=n)
        m, t, _ = nw_t(p[a].values)
        sh = p.mean() / p.std() * np.sqrt(252) if p.std() > 0 else np.nan
        return dict(n=n, bps=1e4 * m, t=t, sh=sh, hit=float((p[a] > 0).mean()))
    sp = pd.Timestamp(split)
    return {"ALL": st(pnl, pos), "IS": st(pnl[pnl.index < sp], pos[pos.index < sp]), "OOS": st(pnl[pnl.index >= sp], pos[pos.index >= sp])}, pnl, pos

def fmt(r):
    return " | ".join(f"{k}: n={v.get('n')} {v.get('bps', np.nan):+.1f}bps t={v.get('t', np.nan):.2f} Sh={v.get('sh', np.nan):.2f}" for k, v in r.items())

# ---------- Sina vadeli: kendi roll-düzeltmem ----------
def sina_contracts(prod):
    out = {}
    for f in sorted(glob.glob(f"{S}/data_cin/sina/{prod}[0-9][0-9][0-9][0-9].json")):
        code = os.path.basename(f)[:-5]
        try:
            j = json.load(open(f))
        except Exception:
            continue
        if not j: continue
        df = pd.DataFrame(j)
        df["d"] = pd.to_datetime(df["d"]); df = df.set_index("d").sort_index()
        for c in "ohlcvps":
            if c in df: df[c] = pd.to_numeric(df[c], errors="coerce")
        df = df[(df["c"] > 0) & (df["v"] > 0)]
        out[code] = df
    return out

def sina_roll(prod):
    """Gün t için kontrat = t-1'de en yüksek açık pozisyonlu kontrat (yalnız ileri vadeye geçiş).
    Getiriler aynı kontrattan: cc = log(c_t/c_{t-1}), gapD = log(o_t/c_{t-1}) (o = gece seansı açılışı), ocD = log(c_t/o_t)."""
    k = ("roll", prod)
    if k in _c: return _c[k]
    cs = sina_contracts(prod)
    names = sorted(cs, key=lambda s: int(s[len(prod):]))
    C = pd.concat({n: cs[n]["c"] for n in names}, axis=1)
    O = pd.concat({n: cs[n]["o"] for n in names}, axis=1)
    P = pd.concat({n: cs[n]["p"] for n in names}, axis=1)
    V = pd.concat({n: cs[n]["v"] for n in names}, axis=1)
    days = C.index
    cur = None; rows = []
    order = {n: i for i, n in enumerate(names)}
    for i in range(1, len(days)):
        t0, t1 = days[i - 1], days[i]
        oi = P.loc[t0].dropna()
        if len(oi) == 0: continue
        best = oi.idxmax()
        if cur is None or order[best] > order[cur]:
            cur = best
        c0, c1, o1 = C.at[t0, cur], C.at[t1, cur], O.at[t1, cur]
        if not (np.isfinite(c0) and np.isfinite(c1)):
            # mevcut kontrat bitti -> en yüksek OI'ye geç ve bu günü atla
            cur = best; continue
        rows.append((t1, cur, np.log(c1 / c0), np.log(o1 / c0) if np.isfinite(o1) and o1 > 0 else np.nan, np.log(c1 / o1) if np.isfinite(o1) and o1 > 0 else np.nan))
    r = pd.DataFrame(rows, columns=["d", "ctr", "cc", "gapD", "ocD"]).set_index("d")
    _c[k] = r
    return r
