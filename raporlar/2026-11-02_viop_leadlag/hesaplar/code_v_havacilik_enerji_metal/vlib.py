"""BAĞIMSIZ doğrulama kütüphanesi (v_havacilik_enerji_metal). ll.py KULLANILMAZ; ham parquet'ten okunur.
Hizalama: BIST günü t için sürücü fiyatı = sürücünün yerel tarihi <= t olan son kapanışı (ffill).
FX '=X': günlük barın kapanışı ldate günü ~00:00 UTC (EURUSD h1 ile doğrulandı: medyan fark 2,3 bp @00 UTC, 21 bp @15 UTC)
 -> değer bir sonraki barın kapanışına kaydırılır (= UTC günü t sonu).
BIST temizlik: log getiri > ln(1,105) veya < ln(0,895) -> NaN (fiyat bazında simetrik ±%10,5).
Sürücü temizlik: |r| > 12 * önceki 250g std -> NaN (vadeli roll / veri hatası).
Gap/gün-içi: gap = ln(o_t / c_{t-1}) (ham fiyat), intra = ln(c_t / o_t); kurumsal işlem günleri (adj/c oranı değişimi > 1 bp)
 ve açılışı şüpheli günler (o == c_{t-1} ve h == l) NaN; 2014 öncesi NaN; |gap| veya cc temizlik sınırını aşarsa NaN."""
import os, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
BASE = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data"
UP, DN = np.log(1.105), np.log(0.895)
_c = {}
def raw(sym, kind="daily"):
    k = (sym, kind)
    if k not in _c:
        d = pd.read_parquet(f"{BASE}/{kind}/{sym}.parquet")
        if kind == "daily":
            d.index = pd.DatetimeIndex(d["ldate"].values).normalize()
            d = d[~d.index.duplicated(keep="last")].sort_index()
        _c[k] = d
    return _c[k]
def isb(sym): return sym.endswith(".IS")
_cal = None
def cal():
    global _cal
    if _cal is None:
        d = raw("XU100.IS"); d = d[(d["v"].fillna(0) > 0) & d["c"].notna()]
        _cal = d.index
    return _cal
def px(sym, field="adj", on_cal=True):
    d = raw(sym)
    s = d[field].astype(float) if field in d else d["c"].astype(float)
    if isb(sym) and d["v"].fillna(0).gt(0).mean() > 0.5:
        s = s[d["v"].fillna(0) > 0]
    s = s[s > 0].dropna()
    if sym.endswith("=X"):
        s = s.shift(-1).dropna()
    if on_cal:
        c = cal(); c = c[c >= s.index[0]]
        s = s.reindex(s.index.union(c)).ffill().reindex(c)
    return s
def ret(sym, on_cal=True, clean=True):
    r = np.log(px(sym, on_cal=on_cal)).diff()
    if clean:
        if isb(sym): r[(r > UP) | (r < DN)] = np.nan
        else:
            sd = r.rolling(250, min_periods=60).std().shift(1); r[(r.abs() > 12 * sd) & sd.notna()] = np.nan
    return r
def dec(sym):
    d = raw(sym).copy()
    if d["v"].fillna(0).gt(0).mean() > 0.5: d = d[d["v"].fillna(0) > 0]
    pc = d["c"].shift(1)
    gap = np.log(d["o"] / pc); intra = np.log(d["c"] / d["o"]); cc = np.log(d["adj"]).diff()
    f = np.log(d["adj"] / d["c"]); ca = (f.diff().abs() > 1e-4)
    badopen = (d["o"] <= 0) | d["o"].isna() | ((d["o"] == pc) & (d["h"] == d["l"]))
    out = pd.DataFrame({"cc": cc, "gap": gap, "intra": intra})
    out.loc[ca, ["gap"]] = np.nan
    out.loc[badopen, ["gap", "intra"]] = np.nan
    bad = (out.cc > UP) | (out.cc < DN) | (out.gap > UP) | (out.gap < DN)
    out.loc[bad, :] = np.nan
    out.loc[out.index < "2014-01-01", ["gap", "intra"]] = np.nan
    return out.reindex(cal())
# --------- istatistik ---------
def resid(y, X):
    X = np.column_stack([np.ones(len(y)), X]); b = np.linalg.lstsq(X, y, rcond=None)[0]; return y - X @ b
def pcorr(a, b, ctrl=None, start=None, end=None, minn=30):
    """Kısmi korelasyon (kontroller aynı gün). Dönüş (pc, n, t_basit)."""
    L = [a.rename("a"), b.rename("b")] + ([c.rename(f"c{i}") for i, c in enumerate(ctrl)] if ctrl else [])
    df = pd.concat(L, axis=1, sort=True).dropna()
    if start: df = df[df.index >= pd.Timestamp(start)]
    if end: df = df[df.index <= pd.Timestamp(end)]
    n = len(df)
    if n < minn: return (np.nan, n, np.nan)
    if ctrl:
        C = df[[c for c in df if c.startswith("c")]].values
        ra = resid(df.a.values, C); rb = resid(df.b.values, C); k = C.shape[1]
    else:
        ra = df.a.values; rb = df.b.values; k = 0
    r = float(np.corrcoef(ra, rb)[0, 1]); t = r * np.sqrt((n - 2 - k) / max(1e-12, 1 - r * r))
    return (r, n, t)
def nw_reg(y, X, lags=5):
    import statsmodels.api as sm
    df = pd.concat([y.rename("y")] + [x.rename(f"x{i}") for i, x in enumerate(X)], axis=1, sort=True).dropna()
    m = sm.OLS(df.y.values, sm.add_constant(df.drop(columns="y").values)).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    return m.params[1:], m.tvalues[1:], len(df)
def pc_nwt(a, b, ctrl, start=None, end=None, lags=5):
    """b'nin a üzerindeki katsayısının NW-t'si (kontrollü regresyon) — kısmi korelasyonun HAC anlamlılığı."""
    df = pd.concat([a.rename("a"), b.rename("b")] + [c.rename(f"c{i}") for i, c in enumerate(ctrl or [])], axis=1, sort=True).dropna()
    if start: df = df[df.index >= pd.Timestamp(start)]
    if end: df = df[df.index <= pd.Timestamp(end)]
    if len(df) < 30: return np.nan
    X = [df.b] + [df[c] for c in df if c.startswith("c")]
    p, t, n = nw_reg(df.a, X, lags); return float(t[0])
def wk(r, rule="W-FRI", minc=3):
    return r.resample(rule).sum(min_count=minc)
def mo(r, minc=12):
    return r.resample("ME").sum(min_count=minc)
PER = {"tam": ("2010-01-01", None), "IS": ("2014-01-01", "2020-12-31"), "OOS": ("2021-01-01", None), "1y": ("2025-10-31", None)}
def periods(a, b, ctrl=None, minn=30):
    return {k: pcorr(a, b, ctrl, s, e, minn) for k, (s, e) in PER.items()}
def byyear(a, b, ctrl=None, minn=100, start="2010-01-01"):
    df = pd.concat([a.rename("a"), b.rename("b")] + [c.rename(f"c{i}") for i, c in enumerate(ctrl or [])], axis=1, sort=True).dropna()
    df = df[df.index >= start]; out = {}
    for y, g in df.groupby(df.index.year):
        if len(g) < minn: continue
        cc = [g[c] for c in g if c.startswith("c")]
        out[y] = pcorr(g.a, g.b, cc if cc else None, minn=minn)[0]
    return pd.Series(out)
# --------- saatlik ---------
def snap(sym, hhmm, kind="h1"):
    """Her UTC günü için hhmm (UTC) anına kadar KAPANMIŞ son barın kapanışı. Bar damgası = bar başlangıcı.
    BIST barları: :30 başlangıçlı 60 dk; 14:30 barı 15:00'te biter; 15:00 barı (kapanış seansı) 15:10'da biter. 6 saatten bayatsa NaN."""
    d = raw(sym, kind); st = d.index
    step = pd.Timedelta(minutes=60 if kind == "h1" else 5)
    end = st + step
    if isb(sym) and kind == "h1":
        m = (st.hour == 14) & (st.minute == 30); end = end.where(~m, st + pd.Timedelta(minutes=30))
        m = (st.hour == 15) & (st.minute == 0); end = end.where(~m, st + pd.Timedelta(minutes=10))
    s = pd.Series(d["c"].values, index=end).sort_index(); s = s[~s.index.duplicated(keep="last")]
    h, mi = map(int, hhmm.split(":"))
    days = pd.DatetimeIndex(st.tz_convert(None).normalize().unique())
    tg = (days + pd.Timedelta(hours=h, minutes=mi)).tz_localize("UTC")
    pos = s.index.searchsorted(tg, side="right") - 1
    ok = pos >= 0; pos = np.clip(pos, 0, None)
    val = np.where(ok, s.values[pos], np.nan); age = tg.values - s.index.values[pos]
    val = np.where(age > np.timedelta64(6, "h"), np.nan, val)
    return pd.Series(val, index=days)

def h1_daily_close(sym):
    """h1 verisinden günlük kapanış (BIST: günün son barı = kapanış seansı). Yahoo günlük verisi olmayan endeksler (XULAS, XMANA) için."""
    d = raw(sym, "h1"); s = pd.Series(d["c"].values, index=pd.DatetimeIndex(d["ldate"].values).normalize())
    s = s.groupby(level=0).last(); return s.reindex(cal()).dropna()
