"""v_cin_gunici_olay_tarama — BAĞIMSIZ çekirdek (ll.py import EDİLMEZ).
Ham parquet -> kendi hizalama/temizlik.
Kurallar:
 - Günlük parquet: index = bar başlangıcı UTC, 'ldate' = yerel tarih. Seriyi ldate ile indeksliyoruz (tekrar -> son).
 - Yahoo '=X' FX: ldate=t 'c' değeri aslında t günü 00:00 UTC fiyatı (h1 ile doğrulandı, v0 log) -> shift(-1): t etiketi = UTC günü t sonu.
 - BIST hisse: hacmi 0 olan günler atılır; fiyat bazında basit getiri > +%10,5 veya < -%10,5 -> NaN (simetrik).
 - BIST gap/intra: 2014 öncesi NaN; o==önceki c ve h==l olan günler NaN (bozuk açılış).
 - BIST takvimi: XU100.IS ldate'leri.
 - Sürücü BIST takvimine: yerel tarihi <= t olan son kapanış (ffill) -> r_d(t) = (t_önceki, t].
"""
import os, numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
D = S + "/data"
OUT = S + "/out/code_v_cin_gunici_olay_tarama/res"
UP, DN = np.log(1.105), np.log(0.895)
_c = {}

def raw(sym, kind="daily"):
    k = (sym, kind)
    if k not in _c:
        _c[k] = pd.read_parquet(f"{D}/{kind}/{sym}.parquet")
    return _c[k]

def isb(sym): return sym.endswith(".IS")
def is_index_bist(sym): return isb(sym) and sym.startswith("X") and sym[:-3].upper() == sym[:-3] and len(sym[:-3]) in (4, 5) and sym[:-3] not in ("XXXX",)

def frame(sym):
    d = raw(sym).copy()
    d.index = pd.DatetimeIndex(pd.to_datetime(d["ldate"]).values)
    d = d[~d.index.duplicated(keep="last")].sort_index()
    if sym.endswith("=X"):
        d = d[["o", "h", "l", "c", "adj"]].shift(-1).dropna()  # FX düzeltmesi
    if isb(sym) and "v" in d and d["v"].fillna(0).gt(0).mean() > 0.5:
        d = d[d["v"].fillna(0) > 0]
    return d

def px(sym, field="adj"):
    d = frame(sym)
    s = d[field if field in d else "c"].astype(float)
    return s[s > 0].dropna()

_cal = None
def cal():
    global _cal
    if _cal is None:
        _cal = pd.DatetimeIndex(frame("XU100.IS").index.unique()).sort_values()
    return _cal

def on_cal(s, c=None):
    c = cal() if c is None else c
    c2 = c[c >= s.index[0]]
    return s.reindex(s.index.union(c2)).ffill().reindex(c2).reindex(c)

def ret(sym, field="adj", oncal=True):
    s = px(sym, field)
    if isb(sym):
        r = np.log(s).diff()
        r[(r > UP) | (r < DN)] = np.nan
        return r.reindex(cal()) if oncal else r
    if oncal:
        s = on_cal(s)
    r = np.log(s).diff()
    # vadeli roll / veri hatası: 12 sigma
    sd = r.rolling(250, min_periods=60).std().shift(1)
    r[(r.abs() > 12 * sd) & sd.notna()] = np.nan
    return r

def decomp(sym, start="2014-01-01"):
    d = frame(sym)
    cc = np.log(d["adj"]).diff()
    intra = np.log(d["c"] / d["o"])
    bad = (d["o"] <= 0) | d["o"].isna() | ((d["h"] == d["l"]) & (d["o"] == d["c"].shift(1)))
    intra[bad] = np.nan
    gap = cc - intra
    o = pd.DataFrame({"cc": cc, "gap": gap, "intra": intra})
    if not is_index_bist(sym):
        o.loc[(o.cc > UP) | (o.cc < DN), :] = np.nan
        o.loc[(o.gap > UP) | (o.gap < DN), ["gap", "intra"]] = np.nan
    o.loc[o.index < pd.Timestamp(start), ["gap", "intra"]] = np.nan
    return o.reindex(cal())

VIOP = "AEFES AKBNK AKSEN ALARK ARCLK ASELS ASTOR BIMAS BRSAN CIMSA DOAS DOHOL EKGYO ENJSA ENKAI EREGL FROTO GARAN GUBRF HALKB HEKTS ISCTR KCHOL KRDMD MGROS ODAS OYAKC PETKM PGSUS SAHOL SASA SISE SOKM TAVHL TCELL THYAO TKFEN TOASO TRALT TRMET TSKB TTKOM TUPRS ULKER VAKBN VESTL YKBNK".split()

WIN = {"tam": ("2014-01-01", "2026-12-31"), "IS": ("2014-01-01", "2020-12-31"), "OOS": ("2021-01-01", "2026-12-31"),
       "3y": ("2023-10-31", "2026-12-31"), "1y": ("2025-10-31", "2026-12-31")}

def resid(y, X):
    """y ve X (DataFrame) ortak örneklemde; X'e göre OLS artığı."""
    if X is None or X.shape[1] == 0:
        return y - y.mean()
    A = np.column_stack([np.ones(len(X)), X.values])
    b, *_ = np.linalg.lstsq(A, y.values, rcond=None)
    return pd.Series(y.values - A @ b, index=y.index)

def hc_t(y, x):
    """y ~ a + b x için HC0 t ve OLS t."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    xm = x - x.mean(); ym = y - y.mean()
    b = (xm @ ym) / (xm @ xm)
    e = ym - b * xm
    n = len(x)
    v_hc = (xm ** 2 @ e ** 2) / (xm @ xm) ** 2
    v_ols = (e @ e) / (n - 2) / (xm @ xm)
    return b, b / np.sqrt(v_hc), b / np.sqrt(v_ols)

def pc(y, x, ctrl=None, win=None):
    """kısmi korelasyon (listwise ortak örneklem), HC t, n, beta (y'nin x'e kısmi betası)."""
    df = pd.concat([y.rename("y"), x.rename("x")] + ([ctrl] if ctrl is not None else []), axis=1).dropna()
    if win is not None:
        df = df.loc[win[0]:win[1]]
    n = len(df)
    if n < 30:
        return dict(r=np.nan, t=np.nan, n=n, b=np.nan)
    C = df.drop(columns=["y", "x"]) if ctrl is not None else None
    ry = resid(df["y"], C); rx = resid(df["x"], C)
    r = np.corrcoef(ry, rx)[0, 1]
    b, th, to = hc_t(ry, rx)
    return dict(r=r, t=th, t_ols=to, n=n, b=b)

def by_year(y, x, ctrl=None, years=range(2014, 2027)):
    out = {}
    for yr in years:
        out[yr] = pc(y, x, ctrl, (f"{yr}-01-01", f"{yr}-12-31"))["r"]
    return pd.Series(out)

def full_report(y, x, ctrl=None, name=""):
    rows = {}
    for w, (a, b) in WIN.items():
        rows[w] = pc(y, x, ctrl, (a, b))
    yr = by_year(y, x, ctrl)
    sgn = np.sign(rows["tam"]["r"])
    same = int((np.sign(yr.dropna()) == sgn).sum()); tot = int(yr.notna().sum())
    return rows, yr, same, tot

def fmt(rows, yr=None, same=None, tot=None):
    s = " | ".join(f"{w}: r={v['r']:+.3f} t={v['t']:+.2f} n={v['n']}" for w, v in rows.items())
    if yr is not None:
        s += f" | yıllar aynı işaret {same}/{tot}"
    return s

def bh(p, q=0.05):
    p = np.asarray(p, float); m = np.isfinite(p).sum()
    order = np.argsort(np.where(np.isfinite(p), p, np.inf))
    ps = p[order]
    thr = q * (np.arange(1, len(p) + 1)) / m
    ok = np.where(ps <= thr)[0]
    res = np.zeros(len(p), bool)
    if len(ok):
        res[order[: ok.max() + 1]] = True
    res[~np.isfinite(p)] = False
    return res

# ----- saatlik / 5dk -----
def bars(sym, kind="h1"):
    d = raw(sym, kind).copy()
    d = d[~d.index.duplicated(keep="last")].sort_index()
    return d

def snap(sym, hhmm_list, kind="h1"):
    """Her UTC günü için verilen saat (UTC) itibarıyla KAPANMIŞ son barın 'c'si. Bar zaman damgası = başlangıç.
    BIST: 14:30 barı 15:00'te, 15:00 barı 15:10'da biter. Diğer: başlangıç+adım."""
    d = bars(sym, kind)
    step = pd.Timedelta(minutes=60 if kind == "h1" else 5)
    st = d.index
    end = st + step
    if isb(sym) and kind == "h1":
        end = end.where(~((st.hour == 14) & (st.minute == 30)), st + pd.Timedelta(minutes=30))
        end = end.where(~((st.hour == 15) & (st.minute == 0)), st + pd.Timedelta(minutes=10))
    s = pd.Series(d["c"].values, index=end).sort_index()
    s = s[~s.index.duplicated(keep="last")]
    days = pd.DatetimeIndex(s.index.tz_convert(None).normalize().unique())
    out = {}
    for hm in hhmm_list:
        h, m = map(int, hm.split(":"))
        tg = (days + pd.Timedelta(hours=h, minutes=m)).tz_localize("UTC")
        pos = s.index.searchsorted(tg, side="right") - 1
        val = np.where(pos >= 0, s.values[np.clip(pos, 0, None)], np.nan)
        ts = np.where(pos >= 0, s.index.values[np.clip(pos, 0, None)], np.datetime64("NaT"))
        o = pd.DataFrame({"p": val, "ts": pd.to_datetime(ts, utc=True)}, index=days)
        # bayat: hedef zamandan 6 saatten eski son bar -> NaN (hafta sonu/tatil)
        age = (tg - pd.DatetimeIndex(o["ts"])).total_seconds() / 3600
        o.loc[np.asarray(age) > 6, "p"] = np.nan
        out[hm] = o["p"]
    return pd.DataFrame(out)
