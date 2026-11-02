"""v_A4_b — 2. aşama şeytanın avukatı. BAĞIMSIZ çekirdek: ll.py / h.py / v_A4_a.vcore IMPORT EDİLMEZ.
Ham parquet'ten kendi hizalama ve temizlik.

Hizalama (varsayılan, 'C' = sürücünün KENDİ takviminde hesap):
  - Her sürücü/sepet kendi işlem takviminde (AB sepeti: AB günleri, ABD sepeti: ABD günleri) getiri, artık (kayan beta),
    z-skor (geçmiş pencere, shift 1) hesaplanır.
  - BIST günü t için kullanılan değer: takvim tarihi D, t_prev <= D < t olan SON sürücü günü (t_prev = önceki BIST günü).
    AB/ABD kapanışları D akşamı (en geç 21:00 UTC) -> BIST açılışı t 07:00 UTC'den >= 10 saat önce. Pencerede gün yoksa NaN.
  - Böylece aynı sürücü günü iki BIST gününde kullanılmaz; BIST tatili sonrası en taze sürücü günü kullanılır.
Hizalama 'A' (kaynakla aynı mantık, kendi kodum): BIST takvimine ffill, log fark, 0 -> NaN, sonra shift(1).
"""
import numpy as np, pandas as pd, os, warnings
warnings.filterwarnings("ignore")
S = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
RES = S + "/out/code_v_A4_b/res"
os.makedirs(RES, exist_ok=True)
EU_AIR = ["LHA.DE", "AF.PA", "IAG.L", "RYA.IR", "EZJ.L", "WIZZ.L", "JET2.L"]
US_AIR = ["DAL", "UAL", "AAL", "LUV", "ALK", "JBLU"]
SPLIT = pd.Timestamp("2021-01-01")
LIM = 0.105

_cache = {}
def raw(sym, kind="daily"):
    k = (sym, kind)
    if k not in _cache:
        p = f"{S}/data/{kind}/{sym}.parquet"
        _cache[k] = pd.read_parquet(p) if os.path.exists(p) else None
    return _cache[k]

def close_own(sym, field="adj"):
    """Sürücü kapanışı kendi takviminde (index = yerel tarih)."""
    d = raw(sym)
    if d is None or len(d) < 300: return None
    s = pd.Series(d[field].values.astype(float), index=pd.DatetimeIndex(d.ldate).normalize())
    s = s[~s.index.duplicated(keep="last")].dropna(); s = s[s > 0]
    if "v" in d and sym[0] != "^" and not sym.endswith("=X") and not sym.endswith("=F"):
        v = pd.Series(d.v.values, index=pd.DatetimeIndex(d.ldate).normalize()); v = v[~v.index.duplicated(keep="last")]
        if (v.reindex(s.index).fillna(0) > 0).mean() > 0.8:
            s = s[v.reindex(s.index).fillna(0) > 0]
    if sym.endswith("=X"):
        # Yahoo FX: satır D'nin c'si ~ D 00:00 UTC fiyatı -> D gününün sonu = satır D+1
        s = pd.Series(s.values[1:], index=s.index[:-1])
    return s

def ret_own(sym, field="adj"):
    s = close_own(sym, field)
    if s is None: return None
    r = np.log(s).diff()
    r = r.where(r != 0)  # bayat (tatil ffill) -> NaN
    sd = r.rolling(250, min_periods=60).std().shift(1)
    r[(r.abs() > 12 * sd) & sd.notna()] = np.nan
    return r.dropna()

_cal = None
def bist_cal():
    global _cal
    if _cal is None:
        d = raw("XU100.IS"); d = d[d.v.fillna(0) > 0]
        _cal = pd.DatetimeIndex(sorted(set(pd.DatetimeIndex(d.ldate).normalize())))
    return _cal

def bist_day(sym):
    """BIST hisse/endeks: cc, gap, intra (kendi). Fiyat bazında ±%10,5 dışı gün -> NaN (simetrik).
    intra = log(c/o); 2014 öncesi intra/gap NaN."""
    d = raw(sym)
    if d is None: return None
    d = d.copy(); d.index = pd.DatetimeIndex(d.ldate).normalize(); d = d[~d.index.duplicated(keep="last")]
    isidx = sym.startswith("X") and sym.endswith(".IS") and len(sym) <= 9
    if not isidx and (d.v.fillna(0) > 0).mean() > 0.5: d = d[d.v.fillna(0) > 0]
    d = d[(d.c > 0) & (d.adj > 0)]
    cc = np.log(d.adj).diff()
    rawcc = np.log(d.c).diff()
    intra = np.log(d.c / d.o)
    gap_raw = np.log(d.o / d.c.shift(1))
    bad = (rawcc.abs() > np.log(1 + LIM)) | (cc.abs() > np.log(1 + LIM)) | (rawcc > np.log(1 + LIM)) | (rawcc < np.log(1 - LIM))
    bad_o = (d.o <= 0) | d.o.isna() | (gap_raw > np.log(1 + LIM)) | (gap_raw < np.log(1 - LIM))
    out = pd.DataFrame({"cc": cc, "intra": intra, "o": d.o, "c": d.c, "h": d.h, "l": d.l, "v": d.v})
    out["gap"] = out.cc - out.intra
    out.loc[bad, ["cc", "gap", "intra"]] = np.nan
    out.loc[bad_o, ["gap", "intra"]] = np.nan
    out.loc[out.index < "2014-01-01", ["gap", "intra"]] = np.nan
    return out

def rresid(y, x, w=250, mp=120):
    df = pd.concat([y.rename("y"), x.rename("x")], axis=1).dropna()
    b = (df.y.rolling(w, min_periods=mp).cov(df.x) / df.x.rolling(w, min_periods=mp).var()).shift(1)
    return (df.y - b * df.x).dropna()

def zs(x, w=250, mp=60):
    mu = x.rolling(w, min_periods=mp).mean().shift(1); sd = x.rolling(w, min_periods=mp).std().shift(1)
    return ((x - mu) / sd).dropna()

def basket_own(syms, min_n=2):
    X = pd.concat([r.rename(s) for s in syms if (r := ret_own(s)) is not None], axis=1)
    m = X.mean(axis=1, skipna=True).where(X.notna().sum(1) >= min_n)
    return m.dropna(), X

def to_bist(x, how="last"):
    """sürücü günlük serisi (kendi takvimi) -> BIST günü t: t_prev <= D < t olan son D (veya toplam)."""
    c = bist_cal(); x = x.dropna().sort_index()
    xi = x.index.values
    hi = np.searchsorted(xi, c.values, side="left")          # D < t
    lo = np.searchsorted(xi, np.r_[c.values[:1] - np.timedelta64(5, "D"), c.values[:-1]], side="left")  # D >= t_prev
    vals = x.values; out = np.full(len(c), np.nan)
    ok = hi > lo
    if how == "last":
        out[ok] = vals[hi[ok] - 1]
    else:
        cs = np.r_[0, np.cumsum(vals)]
        out[ok] = cs[hi[ok]] - cs[lo[ok]]
    return pd.Series(out, index=c)

def sector_signal(eu_syms, us_syms, idx_eu="^STOXX", idx_us="^GSPC", w=250, resid=True):
    """Sepet artık z: kendi takviminde, sonra BIST t'ye (önceden bilinen)."""
    parts = {}
    for nm, syms, ix in [("EU", eu_syms, idx_eu), ("US", us_syms, idx_us)]:
        if not syms: continue
        b, _ = basket_own(syms)
        x = rresid(b, ret_own(ix), w) if resid else b
        parts[nm] = to_bist(zs(x).clip(-3, 3))
    return parts

def nw_t_mean(x, lags=5):
    x = np.asarray(x, float); x = x[~np.isnan(x)]; n = len(x)
    if n < 20: return np.nan
    e = x - x.mean(); v = (e @ e) / n
    for L in range(1, lags + 1):
        v += 2 * (1 - L / (lags + 1)) * (e[L:] @ e[:-L]) / n
    return x.mean() / np.sqrt(v / n)

def bt(sig, y, cost=8.0, thr=1.0, start=None, end=None):
    """sig hizalı (t'de pozisyondan ÖNCE bilinir). |sig|>thr -> sign. Dönüş: dict(n,bps,t_iid,t_nw,gross)."""
    df = pd.concat([sig.rename("s"), y.rename("y")], axis=1).dropna()
    if start is not None: df = df[df.index >= pd.Timestamp(start)]
    if end is not None: df = df[df.index < pd.Timestamp(end)]
    pos = np.sign(df.s).where(df.s.abs() > thr, 0.0)
    a = pos != 0
    g = (pos * df.y)[a]
    n = int(a.sum())
    if n < 15: return {"n": n, "bps": np.nan, "t": np.nan, "t_nw": np.nan, "gross": np.nan}
    net = g - cost / 1e4
    return {"n": n, "bps": 1e4 * net.mean(), "t": net.mean() / net.std() * np.sqrt(n), "t_nw": nw_t_mean(net.values),
            "gross": 1e4 * g.mean(), "t_g": g.mean() / g.std() * np.sqrt(n), "hit": float((g > 0).mean())}

def pnl_series(sig, y, thr=1.0):
    df = pd.concat([sig.rename("s"), y.rename("y")], axis=1).dropna()
    pos = np.sign(df.s).where(df.s.abs() > thr, 0.0)
    return (pos * df.y)[pos != 0], pos

PER = {"IS": (None, "2021-01-01"), "OOS": ("2021-01-01", None), "ALL": (None, None),
       "14-17": ("2014-01-01", "2018-01-01"), "18-20": ("2018-01-01", "2021-01-01"),
       "21-23": ("2021-01-01", "2024-01-01"), "24-26": ("2024-01-01", None)}

def bt_periods(sig, y, cost=8.0, thr=1.0, pers=("IS", "OOS")):
    return {p: bt(sig, y, cost, thr, *PER[p]) for p in pers}

def ols_nw(y, X, lags=5):
    """standartlaştırılmış OLS, NW(HAC) t. numpy (statsmodels'siz)."""
    df = pd.concat([y.rename("y"), X], axis=1).dropna()
    Z = (df - df.mean()) / df.std()
    yv = Z.y.values; Xv = np.c_[np.ones(len(Z)), Z.drop(columns="y").values]
    XtX_inv = np.linalg.pinv(Xv.T @ Xv); b = XtX_inv @ Xv.T @ yv; e = yv - Xv @ b
    u = Xv * e[:, None]; S_ = u.T @ u
    for L in range(1, lags + 1):
        w = 1 - L / (lags + 1); G = u[L:].T @ u[:-L]; S_ += w * (G + G.T)
    V = XtX_inv @ S_ @ XtX_inv
    se = np.sqrt(np.diag(V))
    names = ["const"] + list(Z.drop(columns="y").columns)
    return pd.DataFrame({"coef": b, "t": b / se}, index=names), len(df)
