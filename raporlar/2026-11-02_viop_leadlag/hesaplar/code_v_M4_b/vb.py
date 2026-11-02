"""v_M4_b BAGIMSIZ yardimci modul (ll.py / mh.py / v.py IMPORT EDILMEZ). Ham parquet'ten.
Farkli kurgu (bilincli): surucu getirisi surucunun KENDI takviminde hesaplanir ve yalniz surucunun yerel tarihi (ldate)
== BIST gunu t ise o gune atanir (ffill yok). Tokyo/ASX/Kore t kapanisi BIST t acilis muzayedesinden once.
"""
import os, numpy as np, pandas as pd
import statsmodels.api as sm
SCR = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
DATA = os.path.join(SCR, "data"); OUT = os.path.join(SCR, "out", "code_v_M4_b")
UP, DN = np.log(1.105), np.log(0.895)
SPLIT = pd.Timestamp("2021-01-01")
_c = {}

def raw(sym, kind="daily"):
    k = (sym, kind)
    if k not in _c:
        p = os.path.join(DATA, kind, sym + ".parquet")
        _c[k] = pd.read_parquet(p)
    return _c[k]

def by_ldate(sym, kind="daily"):
    d = raw(sym, kind).copy(); d.index = pd.DatetimeIndex(d["ldate"].values); d = d[~d.index.duplicated(keep="last")]
    return d.sort_index()

def cal():
    d = by_ldate("XU100.IS"); return d.index[(d["v"].fillna(0) > 0) & d["c"].notna()]

def dret(sym, clip=0.25, field="adj"):
    """Surucunun kendi takviminde log getiri; |r|>clip NaN; sifir hacimli & h==l bayat gunler atilir."""
    d = by_ldate(sym); s = d[field].astype(float)
    st = (d["v"].fillna(0) <= 0) & (d["h"] == d["l"])
    if (d["v"].fillna(0) > 0).mean() > 0.5: s = s[~st]
    s = s[s > 0].dropna(); r = np.log(s).diff()
    r[r.abs() > clip] = np.nan
    return r

def zpast(r, w=250, mp=60):
    mu = r.rolling(w, min_periods=mp).mean().shift(1); sd = r.rolling(w, min_periods=mp).std().shift(1)
    return (r - mu) / sd

def comp(syms, w=250, minc=1, lag=0):
    """Bilesen z (kendi takviminde, gecmis pencere) -> BIST gunune ldate eslesmesiyle ata -> ortalama.
    lag=k: BIST takviminde k gun bayatlatilmis sinyal."""
    c = cal(); Z = {}
    for s in syms:
        z = zpast(dret(s), w)
        Z[s] = z.reindex(c)
    Z = pd.DataFrame(Z)
    cnt = Z.notna().sum(axis=1)
    m = Z.mean(axis=1).where(cnt >= minc)
    if lag: m = m.shift(lag)
    return m, Z

def bist(sym, lim="sym"):
    """BIST gun ayristirmasi. lim='sym': fiyat bazinda +-%10,5 ; 'regime': 2020-03-13 oncesi +-%20,5."""
    d = by_ldate(sym)
    if (d["v"].fillna(0) > 0).mean() > 0.5: d = d[~((d["v"].fillna(0) <= 0) & (d["h"] == d["l"]))]
    d = d[(d["c"] > 0) & (d["o"] > 0)]
    cc = np.log(d["adj"]).diff()
    intra = np.log(d["c"] / d["o"])
    bad_o = (d["o"] > d["h"] * 1.0001) | (d["o"] < d["l"] * 0.9999) | ((d["h"] == d["l"]) & (d["o"] == d["c"].shift(1)))
    intra[bad_o] = np.nan
    gap = cc - intra
    o = pd.DataFrame({"cc": cc, "gap": gap, "intra": intra, "o": d["o"], "h": d["h"], "l": d["l"], "c": d["c"], "v": d["v"]})
    if lim == "sym":
        up = pd.Series(UP, index=o.index); dn = pd.Series(DN, index=o.index)
    else:
        pre = o.index < pd.Timestamp("2020-03-13")
        up = pd.Series(np.where(pre, np.log(1.205), UP), index=o.index); dn = pd.Series(np.where(pre, np.log(0.795), DN), index=o.index)
    bad = (o["cc"] > up) | (o["cc"] < dn)
    o.loc[bad, ["cc", "gap", "intra"]] = np.nan
    badg = (o["gap"] > up) | (o["gap"] < dn) | (o["intra"] > up) | (o["intra"] < dn)
    o.loc[badg, ["gap", "intra"]] = np.nan
    o.loc[o.index < pd.Timestamp("2014-01-01"), ["gap", "intra"]] = np.nan
    return o

def nwt(x, lags=5):
    x = pd.Series(x).dropna()
    if len(x) < 20: return np.nan
    m = sm.OLS(x.values, np.ones(len(x))).fit(cov_type="HAC", cov_kwds={"maxlags": lags}); return float(m.tvalues[0])

def nwreg(y, X, lags=5):
    df = pd.concat([y.rename("y"), X], axis=1).dropna()
    m = sm.OLS(df["y"].values, sm.add_constant(df.drop(columns="y").values)).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    return pd.DataFrame({"b": m.params[1:], "t": m.tvalues[1:]}, index=df.drop(columns="y").columns), len(df)

def positions(sig, target_index, thr=1.0, w=250, rez=True):
    s = sig.reindex(target_index)
    if rez:
        s2 = s.dropna(); z = zpast(s2, w).reindex(target_index)
    else:
        z = s
    pos = np.sign(z).where(z.abs() > thr, 0.0).fillna(0.0)
    return pos, z

def bt(sig, y, cost=15.0, thr=1.0, w=250, rez=True, start=None, end=None):
    """sig_t bilinen; y_t pozisyon getirisi. Hedefle hizalanmis gunlerde re-z (gecmis pencere)."""
    df = pd.concat([sig.rename("s"), y.rename("y")], axis=1).dropna()
    pos, z = positions(df["s"], df.index, thr, w, rez)
    pnl = pos * df["y"] - cost / 1e4 * pos.abs()
    out = pd.DataFrame({"pos": pos, "pnl": pnl, "y": df["y"], "z": z})
    if start is not None: out = out[out.index >= pd.Timestamp(start)]
    if end is not None: out = out[out.index < pd.Timestamp(end)]
    return out

def stats(o):
    a = o[o.pos != 0]
    if len(a) < 10: return dict(n=len(a), bps=np.nan, t=np.nan, sh=np.nan)
    sh = a.pnl.mean() * 252 * (o.pos != 0).mean() / (o.pnl.std() * np.sqrt(252)) if o.pnl.std() > 0 else np.nan
    return dict(n=len(a), bps=1e4 * a.pnl.mean(), t=nwt(a.pnl), sh=sh, hit=(a.pnl > 0).mean())

def isoos(o):
    r = {}
    for k, m in [("IS", o.index < SPLIT), ("OOS", o.index >= SPLIT), ("ALL", o.index == o.index)]:
        s = stats(o[m]); r.update({f"{k}_{kk}": v for kk, v in s.items()})
    return r

def corr_t(a, b):
    df = pd.concat([a.rename("a"), b.rename("b")], axis=1).dropna()
    if len(df) < 60: return np.nan, np.nan, len(df)
    za = (df.a - df.a.mean()) / df.a.std(); zb = (df.b - df.b.mean()) / df.b.std()
    t = nwreg(za, zb.rename("b"))[0].loc["b", "t"]
    return df.a.corr(df.b), t, len(df)

JP_AU = ["5411.T", "5401.T", "6301.T", "FMG.AX", "BHP.AX"]

def dret_ffill(sym):
    """Orijinal kurguya benzer: BIST takvimine ffill, log fark, 0 -> NaN, 12 sigma sicrama NaN."""
    d = by_ldate(sym); s = d["adj"].astype(float); s = s[s > 0].dropna()
    c = cal(); c = c[c >= s.index[0]]
    s = s.reindex(s.index.union(c)).ffill().reindex(c)
    r = np.log(s).diff()
    sd = r.rolling(250, min_periods=60).std().shift(1); r[(r.abs() > 12 * sd) & sd.notna()] = np.nan
    return r.where(r != 0)

def comp_ffill(syms, w=250):
    Z = pd.DataFrame({s: zpast(dret_ffill(s), w) for s in syms})
    return Z.mean(axis=1), Z
