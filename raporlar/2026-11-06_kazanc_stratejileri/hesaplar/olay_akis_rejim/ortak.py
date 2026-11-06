"""Ortak yardimcilar: fiyat paneli, endeksler, olay calismasi (BHAR + piyasa modeli CAR), kumelenmis t, tavan kilidi.
Fiyat kaynagi: kardes ajanin (bist_test) Is Yatirim HisseTekil onbellegi (adj = temettu+bedelsiz duzeltmeli kapanis; hi/lo duzeltmeli)
  -> scratchpad/data/bist_test/hisse/<KOD>.parquet (SADECE bugun islem goren hisseler: hayatta kalma yanliligi notu raporda).
  Eksik hisseler icin kendi onbellegim: scratchpad/data/akis_rejim/hisse/<KOD>.parquet (ayni uc, varsayilan basliklar, 0.7 sn).
Endeksler: bist_test/endeks/<KOD>.csv (ChartData IndexHistoricalAll). XBANK 2010-07-02..2010-12-31 araliginda 1/100 olcek hatasi var -> x100 duzeltilir."""
import os, time, json, numpy as np, pandas as pd, requests
SP = "/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad"
DATA = SP + "/data"; MY = DATA + "/akis_rejim"
HISSE = DATA + "/bist_test/hisse"; MYH = MY + "/hisse"; END = DATA + "/bist_test/endeks"
OUTD = "/home/user/Xxxx/raporlar/2026-11-06_kazanc_stratejileri/hesaplar/olay_akis_rejim/cikti"
os.makedirs(MYH, exist_ok=True); os.makedirs(OUTD, exist_ok=True)
VIOP = set("AEFES AKBNK AKSEN ALARK ARCLK ASELS ASTOR BIMAS BRSAN CIMSA DOAS DOHOL EKGYO ENJSA ENKAI EREGL FROTO GARAN GUBRF HALKB HEKTS ISCTR KCHOL KRDMD MGROS ODAS OYAKC PETKM PGSUS SAHOL SASA SISE SOKM TAVHL TCELL THYAO TKFEN TOASO TRALT TRMET TSKB TTKOM TUPRS ULKER VAKBN VESTL YKBNK KOZAL KOZAA".split())
_U = "https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/HisseTekil"
_C = {"HGDG_KAPANIS": "adj", "HG_KAPANIS": "raw", "HGDG_MAX": "hi", "HGDG_MIN": "lo", "HGDG_HACIM": "vol_tl", "PD": "mcap"}
_S = requests.Session()
def endeks(kod):
    e = pd.read_csv(f"{END}/{kod}.csv", parse_dates=["ldate"]).set_index("ldate")["px"].astype(float)
    e = e[~e.index.duplicated(keep="last")].sort_index()
    if kod == "XBANK": e.loc["2010-07-02":"2010-12-31"] *= 100.0
    return e
def _fetch(kod):
    for k in range(3):
        try:
            r = _S.get(_U, params={"hisse": kod, "startdate": "01-01-2009", "enddate": "06-11-2026"}, timeout=120)
            if r.status_code == 200:
                v = r.json().get("value") or []
                if not v: return None
                df = pd.DataFrame(v); df["d"] = pd.to_datetime(df["HGDG_TARIH"], format="%d-%m-%Y")
                df = df.drop_duplicates("d").set_index("d").sort_index()
                return pd.DataFrame({n: pd.to_numeric(df[c], errors="coerce") for c, n in _C.items() if c in df})
        except Exception as ex: print("err", kod, ex)
        time.sleep(3)
    return None
_cache = {}
def hisse(kod, fetch=True):
    if kod in _cache: return _cache[kod]
    p1 = f"{HISSE}/{kod}.parquet"; p2 = f"{MYH}/{kod}.parquet"; d = None
    if os.path.exists(p1): d = pd.read_parquet(p1)
    elif os.path.exists(p2): d = pd.read_parquet(p2)
    elif os.path.exists(p2 + ".empty"): d = None
    elif fetch:
        d = _fetch(kod); time.sleep(0.7)
        if d is None or len(d) == 0: open(p2 + ".empty", "w").write("")
        else: d.to_parquet(p2)
    if d is not None:
        d = d[~d.index.duplicated(keep="last")].sort_index(); d = d[d.adj > 0]
        d["r"] = d.adj.pct_change()
    _cache[kod] = d; return d
def islem_gunleri():
    return endeks("XU100").index
def giris_gunu(ts, takvim, kesim="17:00"):
    """KAP yayin zamani ts -> ilk islem gunu kapanisi (yayin o gun kesim saatinden once ise o gun, degilse sonraki islem gunu)."""
    d = ts.normalize(); i = takvim.searchsorted(d)
    if i < len(takvim) and takvim[i] == d and ts.strftime("%H:%M") < kesim: return takvim[i]
    j = takvim.searchsorted(d, side="right")
    return takvim[j] if j < len(takvim) else None
HZ = (5, 20, 60)
def olay_getiri(kod, t0, xu, xr, hz=HZ, pre=20):
    """t0 = giris gunu (kapanista alis). Cikti: BH ham, BH endeks, BHAR, piyasa modeli CAR (beta [-250,-21]), on-donem, gun0, tavan kilidi, likidite."""
    d = hisse(kod)
    if d is None or t0 not in d.index: return None
    i = d.index.get_loc(t0)
    if i < pre + 1: return None
    a = d.adj.values; out = {"kod": kod, "t0": t0}
    r0 = a[i] / a[i - 1] - 1; out["gun0"] = r0
    out["tavan"] = bool(r0 >= 0.095 and d.hi.iloc[i] > 0 and a[i] >= 0.999 * d.hi.iloc[i] * (a[i] / d.adj.iloc[i]))
    out["taban"] = bool(r0 <= -0.095 and d.lo.iloc[i] > 0 and a[i] <= 1.001 * d.lo.iloc[i])
    m = xu.reindex(d.index).ffill().values
    out["on"] = a[i - 1] / a[i - 1 - pre] - 1 - (m[i - 1] / m[i - 1 - pre] - 1)
    out["vol20"] = float(np.nanmedian(d.vol_tl.values[max(0, i - 20):i])) if "vol_tl" in d else np.nan
    # beta: [-250,-21]
    rs = d.r.values; rm = pd.Series(m).pct_change().values
    lo_ = max(1, i - 250); hi_ = i - 20
    x, y = rm[lo_:hi_], rs[lo_:hi_]; ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() >= 100:
        b = np.cov(x[ok], y[ok])[0, 1] / np.var(x[ok]); al = np.mean(y[ok]) - b * np.mean(x[ok])
    else: b, al = np.nan, np.nan
    out["beta"] = b
    for h in hz:
        if i + h >= len(a): out[f"bh{h}"] = out[f"bhm{h}"] = out[f"ar{h}"] = out[f"mm{h}"] = np.nan; continue
        # takvim bosluklarina karsi: h islem gunu sonrasi tarih endeks takvimine gore ~ ayni
        out[f"bh{h}"] = a[i + h] / a[i] - 1; out[f"bhm{h}"] = m[i + h] / m[i] - 1
        out[f"ar{h}"] = out[f"bh{h}"] - out[f"bhm{h}"]
        seg = slice(i + 1, i + h + 1)
        out[f"mm{h}"] = np.nansum(rs[seg] - (al + b * rm[seg])) if np.isfinite(b) else np.nan
    return out
def kume_t(x, g):
    """Ortalama ve tarih kumelerine gore (g) saglam t."""
    x = pd.Series(x).astype(float); g = pd.Series(g).reindex(x.index)
    ok = x.notna(); x, g = x[ok], g[ok]; n = len(x)
    if n < 3: return np.nan, np.nan, n
    mu = x.mean(); e = (x - mu).groupby(g.values).sum()
    G = len(e); se = np.sqrt((e ** 2).sum() * G / max(G - 1, 1)) / n
    return mu, mu / se if se > 0 else np.nan, n
def ozet(df, col, g="hafta"):
    x = df[col].dropna()
    if len(x) < 3: return {"n": len(x)}
    mu, t, n = kume_t(df[col], df[g])
    return {"n": n, "ort%": 100 * mu, "t_kume": t, "medyan%": 100 * x.median(), "isabet%": 100 * (x > 0).mean(),
            "p5%": 100 * x.quantile(.05), "p95%": 100 * x.quantile(.95), "kume": df.loc[x.index, g].nunique()}
def tablo(df, cols, g="hafta"):
    return pd.DataFrame({c: ozet(df, c, g) for c in cols}).T
def md(df, fl=2):
    if df is None or len(df) == 0: return "(bos)\n"
    d = df.copy()
    for c in d.columns:
        if d[c].dtype.kind == "f": d[c] = d[c].map(lambda v: "" if pd.isna(v) else (f"{v:.{fl}f}" if abs(v) < 1e5 else f"{v:.0f}"))
    cols = [str(c) for c in d.columns]; idx = d.index.name or ""
    s = "| " + " | ".join([idx] + cols) + " |\n|" + "---|" * (len(cols) + 1) + "\n"
    for k, row in d.iterrows(): s += "| " + " | ".join([str(k)] + [str(v) for v in row.values]) + " |\n"
    return s
