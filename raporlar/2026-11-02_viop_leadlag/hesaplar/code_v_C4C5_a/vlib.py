"""v_C4C5_a - BAGIMSIZ dogrulama kutuphanesi (ll.py IMPORT EDILMEZ).
Kendi hizalama/temizlik kurallarim:
 * BIST: data/daily parquet; sifir hacimli gunler atilir; cc = dlog(adj); intra = log(c/o); gap = cc - intra.
   Temizlik: fiyat bazinda +%10,5 ustu / -%10,5 alti cc gunleri NaN (simetrik); acilis supheli (o<=0, o disinda [l,h], h==l ve o==onceki c) -> intra/gap NaN;
   2014 oncesi gap/intra NaN; |gap| > ln(1.105) -> NaN.
 * Surucu (HK/SS/Yahoo): adj kapanis; BIST gunu t icin fiyat = yerel tarihi <= t olan son kapanis (yerel tarih = UTC tarihi, Asya seansi ayni UTC gununde).
   Sinyal_t = logP(<=t) - logP(<=t_onceki_BIST). Surucu t gununde islem gormediyse 'fresh=False' (sinyal 0 veya NaN secenegi).
 * FX '=X': Yahoo gunluk 'kapanis' ldate gunu 00:00 UTC -> 1 gun geri kaydir (kendim).
 * SHFE (Sina): tekil kontratlardan onceki gun max-OI kuraliyla (sadece ileri) roll-duzeltilmis getiri. Kendi uygulamam.
"""
import os, re, json, glob, numpy as np, pandas as pd
SCR = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
DAILY = SCR + "/data/daily"; H1 = SCR + "/data/h1"; M5 = SCR + "/data/m5"
SINA = SCR + "/data_cin/sina"; SINA60 = SCR + "/dl_v_C4C5a/sina60"
UP, DN = np.log(1.105), np.log(0.895)
_c = {}

def rawd(sym, kind="daily"):
    k = (sym, kind)
    if k not in _c:
        base = {"daily": DAILY, "h1": H1, "m5": M5}[kind]
        _c[k] = pd.read_parquet(os.path.join(base, sym.replace("/", "_") + ".parquet"))
    return _c[k]

def bist_daily(sym):
    """BIST hissesi/endeksi: DataFrame(o,h,l,c,adj,v, cc, intra, gap), index = yerel tarih."""
    d = rawd(sym).copy(); d.index = pd.DatetimeIndex(d["ldate"].values); d = d[~d.index.duplicated(keep="last")].sort_index()
    if d["v"].fillna(0).gt(0).mean() > 0.5: d = d[d["v"].fillna(0) > 0]
    cc = np.log(d["adj"]).diff()
    intra = np.log(d["c"] / d["o"])
    bad_o = (d["o"] <= 0) | d["o"].isna() | (d["o"] > d["h"] * 1.0001) | (d["o"] < d["l"] * 0.9999) | ((d["h"] == d["l"]) & (d["o"] == d["c"].shift(1)))
    intra[bad_o] = np.nan
    gap = cc - intra
    out = d[["o", "h", "l", "c", "adj", "v"]].copy(); out["cc"] = cc; out["intra"] = intra; out["gap"] = gap
    bad = (cc > UP) | (cc < DN)
    out.loc[bad, ["cc", "intra", "gap"]] = np.nan
    out.loc[out.index < "2014-01-01", ["intra", "gap"]] = np.nan
    out.loc[(out["gap"] > UP) | (out["gap"] < DN), ["intra", "gap"]] = np.nan
    return out

def cal():
    return bist_daily("XU100.IS").index

def local_px(sym, field="adj"):
    d = rawd(sym); s = pd.Series(d[field].values, index=pd.DatetimeIndex(d["ldate"].values)).astype(float)
    s = s[~s.index.duplicated(keep="last")].dropna(); s = s[s > 0].sort_index()
    if sym.endswith("=X"): s = s.shift(-1).dropna()  # FX: ldate gunu 00:00 UTC -> gun sonu = sonraki bar
    return s

def on_cal(s, C=None):
    """Seviye serisini BIST takvimine: t icin yerel tarihi <= t olan son deger. Ayrica fresh (t gunu gozlem var mi)."""
    C = cal() if C is None else C
    C = C[C >= s.index[0]]
    v = s.reindex(s.index.union(C)).ffill().reindex(C)
    fresh = pd.Series(C.isin(s.index), index=C)
    return v, fresh

def sig_close(sym, C=None, clean=True):
    """BIST takviminde surucu kapanis-kapanis log getiri (ll konvansiyonunun bagimsiz esdegeri)."""
    s = local_px(sym); v, fresh = on_cal(s, C); r = np.log(v).diff()
    if clean:
        rl = np.log(s).diff(); sd = rl.rolling(250, min_periods=60).std().shift(1)
        bad_days = rl.index[(rl.abs() > 12 * sd) & sd.notna()]
        r[r.index.isin(bad_days)] = np.nan
    return r, fresh

def nw(y, X, lags=5):
    """OLS y ~ const + X, HAC (Bartlett) t-istatistikleri. X: DataFrame. Donus: (params, tvals, n)."""
    import statsmodels.api as sm
    df = pd.concat([y.rename("_y"), X], axis=1).dropna()
    if len(df) < 30: return None, None, len(df)
    m = sm.OLS(df["_y"].values, sm.add_constant(df.drop(columns="_y").values, has_constant="add")).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    names = ["const"] + list(df.drop(columns="_y").columns)
    return pd.Series(m.params, index=names), pd.Series(m.tvalues, index=names), len(df)

def zt(y, x, lags=5):
    """Standartlastirilmis tek degiskenli regresyon: (corr, NW t, n)."""
    df = pd.concat([y.rename("y"), x.rename("x")], axis=1).dropna()
    if len(df) < 30: return np.nan, np.nan, len(df)
    p, t, n = nw((df.y - df.y.mean()) / df.y.std(), ((df.x - df.x.mean()) / df.x.std()).to_frame("x"), lags)
    return float(p["x"]), float(t["x"]), n

def bt(sig, tgt, cost_bps=10.0, split="2021-01-01"):
    """pos = sign(sig) (sig==0 -> islem yok). Gunluk acilip kapanan pozisyon; maliyet gidis-donus cost_bps.
    Sharpe = (aktif gun ort * 252 * aktif oran) / (tum gun pnl std * sqrt252)."""
    df = pd.concat([sig.rename("s"), tgt.rename("y")], axis=1).dropna()
    pos = np.sign(df["s"]); pnl = pos * df["y"] - cost_bps / 1e4 * pos.abs()
    def st(p, ps):
        a = ps != 0; n = int(a.sum())
        if n < 20: return {"n": n}
        pa = p[a]; vol = p.std() * np.sqrt(252); ann = pa.mean() * 252 * a.mean()
        import statsmodels.api as sm
        t = sm.OLS(pa.values, np.ones(len(pa))).fit(cov_type="HAC", cov_kwds={"maxlags": 5}).tvalues[0]
        return {"n": n, "mean_bps": 1e4 * pa.mean(), "t": float(t), "hit": float((pa > 0).mean()), "sharpe": ann / vol if vol > 0 else np.nan}
    sp = pd.Timestamp(split)
    res = {"ALL": st(pnl, pos), "IS": st(pnl[pnl.index < sp], pos[pos.index < sp]), "OOS": st(pnl[pnl.index >= sp], pos[pos.index >= sp])}
    act = pos != 0
    res["yr"] = (1e4 * pnl[act].groupby(pnl[act].index.year).mean()).round(1).to_dict()
    return res, pnl

# ---------- SHFE (Sina) ----------
def _sina_daily(nm):
    p = os.path.join(SINA, nm + ".json")
    if not os.path.exists(p): return None
    d = json.load(open(p))
    if not d: return None
    df = pd.DataFrame(d); df.index = pd.to_datetime(df["d"]); df = df[~df.index.duplicated(keep="last")].sort_index()
    for k in "ohlcvps":
        if k in df: df[k] = pd.to_numeric(df[k], errors="coerce")
    return df

def shfe_contracts(code):
    files = sorted(glob.glob(os.path.join(SINA, f"{code}[0-9][0-9][0-9][0-9].json")))
    C, P, O = {}, {}, {}
    for f in files:
        nm = os.path.basename(f)[:-5]
        if not re.fullmatch(code + r"\d{4}", nm): continue
        df = _sina_daily(nm)
        if df is None or len(df) < 5: continue
        C[nm] = df["c"]; P[nm] = df["p"]; O[nm] = df["o"]
    cols = sorted(C, key=lambda x: int(x[len(code):]))
    C = pd.DataFrame(C)[cols]; P = pd.DataFrame(P)[cols].fillna(0); O = pd.DataFrame(O)[cols]
    C = C.where(C > 0); O = O.where(O > 0)
    return C, P, O, cols

def shfe_main(code, start_oi_share=0.6):
    """Ana kontrat (gun t'de kullanilan = t-1 gunu max OI, sadece ileri). Donus: DataFrame(main_name, r_cc, r_gap(c_{t-1}->o_t), r_oc(o_t->c_t))."""
    k = ("shfe", code)
    if k in _c: return _c[k]
    C, P, O, cols = shfe_contracts(code)
    mi = np.maximum.accumulate(P.values.argmax(axis=1))
    main = pd.Series(mi, index=P.index); prev = main.shift(1)
    lc = np.log(C); lo = np.log(O)
    rows = []
    for i in range(1, len(P)):
        j = int(prev.iloc[i])
        rows.append((P.index[i], cols[j], lc.iloc[i, j] - lc.iloc[i - 1, j], lo.iloc[i, j] - lc.iloc[i - 1, j], lc.iloc[i, j] - lo.iloc[i, j], P.iloc[i, j]))
    df = pd.DataFrame(rows, columns=["d", "main", "r_cc", "r_gap", "r_oc", "oi"]).set_index("d")
    # baslangic: secilen kontratin OI'si surekli serinin OI'sinin >=%60'i oldugu ilk 5 gun
    c0 = _sina_daily(code + "0")
    if c0 is not None:
        ratio = (df["oi"] / c0["p"].reindex(df.index)).rolling(5).min()
        good = ratio[ratio >= start_oi_share]
        if len(good): df = df[df.index > good.index[0]]
    _c[k] = df; return df

def sina60(nm):
    p = os.path.join(SINA60, nm + ".txt")
    if not os.path.exists(p): return None
    t = open(p).read(); m = re.search(r"\((\[.*\])\)", t, re.S)
    d = json.loads(m.group(1)) if m else []
    if not d: return None
    df = pd.DataFrame(d); df.index = pd.to_datetime(df["d"]); df = df[~df.index.duplicated(keep="last")].sort_index()
    for k in "ohlcvp": df[k] = pd.to_numeric(df[k], errors="coerce")
    return df  # index: Pekin yerel saati, bar BITIS etiketi
