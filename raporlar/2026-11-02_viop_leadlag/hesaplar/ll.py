"""ORTAK LEAD-LAG KÜTÜPHANESİ (tüm ajanlar bunu kullanır; bağımsız doğrulama ajanları kendi kodunu yazar).
import sys; sys.path.insert(0, '<SCRATCH>/code'); import ll

ZAMANLAMA KONVANSİYONU (KRİTİK):
- BIST pay piyasası: sürekli işlem ~10:00-18:00 TSİ, kapanış seansı 18:00-18:10 TSİ (= 15:00-15:10 UTC; Türkiye 2016'dan beri UTC+3 sabit).
- Günlük seriler 'BIST takvimine' oturtulur: BIST günü t için sürücü fiyatı = sürücünün yerel tarihi <= t olan son kapanışı.
  Böylece sürücü getirisi r_d(t) = (t_önceki, t] aralığı.
- lag k > 0  ==> corr(hisse_t, sürücü_{t-k}): sürücü ÖNDE.  lag k < 0 ==> hisse önde.
- ABD/vadeli/FX kapanışı (~20-22 UTC) BIST kapanışından SONRA. Yani ABD sürücüsünün lag0 getirisi, BIST kapanışından sonraki 5-7 saati de içerir.
  ABD lag1 -> BIST t etkisi büyük ölçüde 'eşzamansız kapanış' (non-synchronous close) mekanizmasıdır ve açılış gap'inde fiyatlanır.
  Gerçek 'işlenebilir' öncülük için: sürücü_{t-1} -> BIST gün-içi (açılış->kapanış) t getirisini test et (ll.decomp).
- Asya kapanışları (Tokyo/Seul ~06:00-06:30, Şanghay 07:00, HK 08:00 UTC) BIST t seansından ÖNCE/başında: Asya lag0 = BIST'e göre zaten 'önde'.
- Avrupa kapanışı 15:30 UTC (yaz) / 16:30 UTC (kış): BIST'ten 0,5-1,5 saat sonra -> lag0 neredeyse senkron, küçük bir 'sonra' kısmı var.
- Saatlik verilerle kesin hizalama: ll.snap_daily(sym, '15:00') = her gün 15:00 UTC'deki (BIST kapanışı) fiyat.

GETİRİLER: log getiri. BIST hisseleri TL. USD bazlı istenirse ll.bist_usd().
FX ZAMANLAMA DÜZELTMESİ (01.11.2026): Yahoo '=X' kur serilerinin günlük kapanışı t günü 00:00 UTC'dir; ll.daily/ret bunu otomatik
  düzeltir (FX_FIX=True): düzeltilmiş r_FX(t) ≈ UTC günü t (BIST seansı t + ABD seansı t dahil) -> ABD varlıkları gibi BIST kapanışından SONRA biter.
  Diğer kapanışlar (saatlikle doğrulandı): BZ=F ~19:00 UTC, GC=F ~18:00, ZN=F ~19:00, ES=F/^VIX/^TNX/TKC/TUR ~20–21, BTC-USD 24:00 UTC, ^N225 ~06:30, 000001.SS ~07:00.
TEMİZLİK (v4, 02.11): fiyat marjı 2020-03-13 öncesi ±%20, sonrası ±%10 -> rejime bağlı eşik (ll._bad); bayat gün = hacim 0 VE h==l (ll._stale). Eski not: BIST'te günlük fiyat marjı ±%10 -> fiyat bazında +%10,5 üstü / -%10,5 altı (log: >ln1,105 veya <ln0,895) BIST günleri kurumsal işlem/veri hatası sayılıp NaN yapılır (01.11 simetri düzeltmesi: taban günleri artık KORUNUR).
  gap = r_cc(adj) - r_intraday (temettü etkisi gap'e değil düzeltmeye gider). Açılış verisi şüpheli günler (o==önceki c ve h==l) NaN.
"""
import os, json, numpy as np, pandas as pd, warnings
from scipy import stats
warnings.filterwarnings("ignore")
BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
LIM = np.log(1.105)  # geriye uyumluluk; kullanmayın
LIM_UP, LIM_DN = np.log(1.105), np.log(0.895)  # DÜZELTME 01.11.2026 (olay ajanı): fiyat bazında simetrik ±%10,5. Eski |r|>ln(1,105) kuralı -%10 taban günlerini (ln0,9=-0,105) siliyordu.
REGIME_SWITCH = pd.Timestamp("2020-03-13")  # DÜZELTME 02.11.2026 (akış ajanı): BIST fiyat marjı 2020-03-13 öncesi ±%20, sonrası ±%10
LIM_UP20, LIM_DN20 = np.log(1.205), np.log(0.795)
def _bad(r):
    """Kurumsal işlem/veri hatası bayrağı (fiyat bazında simetrik, rejime bağlı). 2020-03-13 öncesi ±%20,5, sonrası ±%10,5.
    Not: 2020 öncesi %10,5–20,5 aralığındaki küçük bedelsizler (ör. %20 bedelsiz = −%16,7) yakalanmaz — kalıntı risk."""
    idx = r.index
    pre = pd.Series(np.asarray(idx < REGIME_SWITCH), index=idx)
    up = pd.Series(np.where(pre, LIM_UP20, LIM_UP), index=idx); dn = pd.Series(np.where(pre, LIM_DN20, LIM_DN), index=idx)
    return (r > up) | (r < dn)
def _stale(d):
    """Bayat BIST günü: hacim 0 VE fiyat aralığı yok (h==l). (DÜZELTME 02.11: SASA'da Yahoo hacmi 2025-06'dan beri günlerin %42'sinde 0 ama fiyat işliyor.)"""
    return (d["v"].fillna(0) <= 0) & (d["h"] == d["l"])
FX_FIX = True  # '=X' serileri 1 gün geri kaydırılır (bkz. daily()). Eski davranış için ll.FX_FIX=False
_cache = {}
def _p(kind, sym): return os.path.join(BASE, kind, sym.replace("/", "_") + ".parquet")
def raw(sym, kind="daily"):
    k = (sym, kind)
    if k not in _cache:
        p = _p(kind, sym)
        if not os.path.exists(p):
            import ydl; r = ydl.fetch(sym, kind)
            if not os.path.exists(p): raise FileNotFoundError(f"{sym} {kind}: {r}")
        _cache[k] = pd.read_parquet(p)
    return _cache[k]
def meta(sym):
    p = os.path.join(BASE, "meta", sym.replace("/", "_") + ".json")
    return json.load(open(p)) if os.path.exists(p) else {}
def is_bist(sym): return sym.endswith(".IS")
def T(sym):  # kısa ad -> Yahoo
    return sym if ("." in sym or "=" in sym or sym.startswith("^") or "-" in sym) else (sym + ".IS" if sym.isupper() and len(sym) <= 6 and sym in _BIST_SET else sym)
from universe import VIOP, BIST_EXTRA, G
_BIST_SET = set(VIOP + BIST_EXTRA)

def bist_cal():
    d = raw("XU100.IS"); d = d[d["v"].fillna(0) > 0] if d["v"].fillna(0).gt(0).mean() > 0.5 else d
    return pd.DatetimeIndex(d["ldate"].values).unique().sort_values()

def daily(sym, field="adj", on_bist_cal=True):
    """Fiyat serisi, index = yerel tarih. on_bist_cal=True ise BIST takvimine ffill ile oturtulur (son bilinen kapanış)."""
    sym = T(sym); d = raw(sym)
    s = pd.Series(d[field].values if field in d else d["c"].values, index=pd.DatetimeIndex(d["ldate"].values)).astype(float)
    s = s[~s.index.duplicated(keep="last")].dropna(); s = s[s > 0]
    if FX_FIX and sym.endswith("=X"):
        # DÜZELTME (01.11.2026, banka ajanı bulgusu, koordinatör doğruladı): Yahoo '=X' FX günlük barında ldate=t 'kapanışı'
        # aslında t günü ~00:00 UTC fiyatıdır (EURUSD medyan fark 2 bp; 15:00 UTC'de 21 bp). Gerçek 'UTC günü t sonu' fiyatı = bir sonraki barın değeri.
        s = s.shift(-1).dropna()
    if is_bist(sym):  # sıfır hacimli bayat günleri at (endeksler hariç)
        dd = d.copy(); dd.index = pd.DatetimeIndex(dd["ldate"].values); dd = dd[~dd.index.duplicated(keep="last")]
        st = _stale(dd)
        if dd["v"].fillna(0).gt(0).mean() > 0.5: s = s[~st.reindex(s.index).fillna(False).astype(bool)]
    if on_bist_cal:
        cal = bist_cal(); cal = cal[cal >= s.index[0]]
        s = s.reindex(s.index.union(cal)).ffill().reindex(cal)
    return s

def ret(sym, field="adj", on_bist_cal=True, clean=True):
    s = daily(sym, field, on_bist_cal); r = np.log(s).diff()
    if is_bist(T(sym)) and clean: r[_bad(r)] = np.nan
    if not is_bist(T(sym)) and clean:  # vadeli roll / veri hatası: 12 sigmalık sıçramaları at
        sd = r.rolling(250, min_periods=60).std().shift(1); r[(r.abs() > 12 * sd) & sd.notna()] = np.nan
    # BIST takviminde sürücü verisi yoksa (ör. tatil/eksik) getiri 0 olur -> eksik veri kontrolü:
    return r

def decomp(sym):
    """BIST hissesi için gün ayrıştırması: cc = gap + intra. DataFrame(cc, gap, intra), index BIST tarihleri."""
    sym = T(sym); d = raw(sym).copy(); d.index = pd.DatetimeIndex(d["ldate"].values); d = d[~d.index.duplicated(keep="last")]
    if d["v"].fillna(0).gt(0).mean() > 0.5: d = d[~_stale(d)]
    cc = np.log(d["adj"]).diff(); intra = np.log(d["c"] / d["o"])
    bad_open = (d["o"] <= 0) | d["o"].isna() | ((d["h"] == d["l"]) & (d["o"] == d["c"].shift(1)))
    intra[bad_open] = np.nan
    gap = cc - intra
    out = pd.DataFrame({"cc": cc, "gap": gap, "intra": intra})
    out.loc[_bad(out["cc"]), :] = np.nan
    out.loc[out.index < pd.Timestamp("2014-01-01"), ["gap", "intra"]] = np.nan  # Yahoo BIST açılış verisi 2013 öncesi güvenilmez (o==c)
    out.loc[_bad(out["gap"]), ["gap", "intra"]] = np.nan
    return out

def bist_usd(sym):
    """USD bazlı BIST getirisi (yaklaşık): r_TL - r_USDTRY (USDTRY Yahoo kapanışı ~22-23 UTC -> zaman uyumsuz; saatlik için snap kullan)."""
    return ret(sym) - ret("TRY=X")

# ---------- saatlik / gün-içi ----------
def intraday(sym, kind="h1"):
    d = raw(T(sym), kind); return d
def snap_daily(sym, hhmm="15:00", kind="h1", field="c"):
    """Her UTC günü için hhmm (UTC) anına kadar kapanmış son barın fiyatı. Bar zaman damgası = bar başlangıcı.
    60m barda bar [t, t+60dk) -> kapanış anı t+60dk. hhmm'e kadar kapanmış son bar seçilir."""
    d = raw(T(sym), kind)
    step = pd.Timedelta(minutes=60 if kind == "h1" else (5 if kind == "m5" else 15))
    end = d.index + step
    # BIST barları :30'da başlar (06:30..14:30 UTC) + 15:00 kapanış seansı barı. 14:30 barı 15:00'te, 15:00 barı ~15:10'da biter.
    if is_bist(T(sym)):
        st_ = d.index
        e = st_ + step
        e = e.where(~((st_.hour == 14) & (st_.minute == 30)), st_ + pd.Timedelta(minutes=30))
        e = e.where(~((st_.hour == 15) & (st_.minute == 0)), st_ + pd.Timedelta(minutes=10))
        end = e
    s = pd.Series(d[field].values, index=end)
    h, m = map(int, hhmm.split(":"))
    days = pd.DatetimeIndex(s.index.tz_convert(None).normalize().unique())
    targets = pd.DatetimeIndex(days + pd.Timedelta(hours=h, minutes=m)).tz_localize("UTC")
    s = s.sort_index(); pos = s.index.searchsorted(targets, side="right") - 1
    vals = np.where(pos >= 0, s.values[np.clip(pos, 0, None)], np.nan)
    ts = np.where(pos >= 0, s.index.values[np.clip(pos, 0, None)], np.datetime64("NaT"))
    out = pd.DataFrame({"px": vals, "bar_end": ts}, index=days)
    # bayat: hedef andan 6 saatten eskiyse NaN
    age = (targets.tz_convert(None).values - pd.DatetimeIndex(out["bar_end"]).values)
    out.loc[age > np.timedelta64(6, "h"), "px"] = np.nan
    return out["px"]

# ---------- istatistik ----------
def nw_t(y, x=None, lags=5):
    """OLS y = a + b x (x None ise ortalama testi), Newey-West t. Dönüş: (b, t, n)."""
    import statsmodels.api as sm
    y = pd.Series(y)
    if x is None:
        df = y.dropna(); 
        if len(df) < 30: return (np.nan, np.nan, len(df))
        m = sm.OLS(df.values, np.ones(len(df))).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
        return (m.params[0], m.tvalues[0], len(df))
    X = pd.DataFrame(x) if not isinstance(x, pd.DataFrame) else x
    df = pd.concat([y.rename("y"), X], axis=1).dropna()
    if len(df) < 30: return (np.nan, np.nan, len(df))
    m = sm.OLS(df["y"].values, sm.add_constant(df.drop(columns="y").values)).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    return (m.params[1], m.tvalues[1], len(df))

def ccf(a, b, lags=range(-3, 6), method="pearson", start=None, end=None):
    """corr(a_t, b_{t-k}) k in lags. k>0: b önde. Dönüş DataFrame(lag, corr, t_nw, n)."""
    rows = []
    for k in lags:
        df = pd.concat([a.rename("a"), b.shift(k).rename("b")], axis=1).dropna()
        if start: df = df[df.index >= pd.Timestamp(start)]
        if end: df = df[df.index <= pd.Timestamp(end)]
        if len(df) < 30: rows.append((k, np.nan, np.nan, len(df))); continue
        c = df["a"].corr(df["b"], method=method)
        za = (df["a"] - df["a"].mean()) / df["a"].std(); zb = (df["b"] - df["b"].mean()) / df["b"].std()
        _, t, n = nw_t(za, zb)
        rows.append((k, c, t, n))
    return pd.DataFrame(rows, columns=["lag", "corr", "t_nw", "n"]).set_index("lag")

def partial_corr(a, b, controls):
    df = pd.concat([a.rename("a"), b.rename("b")] + [c.rename(f"c{i}") for i, c in enumerate(controls)], axis=1).dropna()
    if len(df) < 30: return np.nan, 0
    import statsmodels.api as sm
    C = sm.add_constant(df[[c for c in df if c.startswith("c")]].values)
    ra = df["a"] - C @ np.linalg.lstsq(C, df["a"].values, rcond=None)[0]
    rb = df["b"] - C @ np.linalg.lstsq(C, df["b"].values, rcond=None)[0]
    return float(np.corrcoef(ra, rb)[0, 1]), len(df)

def rolling_corr(a, b, w=250):
    df = pd.concat([a, b], axis=1).dropna(); return df.iloc[:, 0].rolling(w).corr(df.iloc[:, 1])

def by_year_corr(a, b, k=0):
    df = pd.concat([a.rename("a"), b.shift(k).rename("b")], axis=1).dropna()
    return df.groupby(df.index.year).apply(lambda x: x["a"].corr(x["b"]) if len(x) > 30 else np.nan)

def fdr(pvals, q=0.05):
    from statsmodels.stats.multitest import multipletests
    p = np.asarray(pvals, float); ok = ~np.isnan(p); rej = np.zeros(len(p), bool); padj = np.full(len(p), np.nan)
    if ok.sum():
        r, pa, _, _ = multipletests(p[ok], alpha=q, method="fdr_bh"); rej[ok] = r; padj[ok] = pa
    return rej, padj

def t_to_p(t): return 2 * (1 - stats.norm.cdf(np.abs(t)))

# ---------- backtest ----------
def backtest(signal, target, cost_bps=8.0, mode="sign", thr=0.0, split="2021-01-01", z_window=250, both_sides=True):
    """signal_t: işlem kararından ÖNCE bilinen bilgi (hizalamayı çağıran yapar!). target_t: pozisyonun kazandığı getiri.
    mode='sign': pos=sign(signal) |signal|>thr ise. mode='z': z-skor (geçmiş pencere, look-ahead yok) |z|>thr ise sign.
    Maliyet: her gün açılıp kapanan pozisyon için gidiş-dönüş cost_bps (both_sides=True -> 2 x cost_bps/2 = cost_bps toplam).
    Dönüş: dict(IS, OOS, ALL istatistikleri) + günlük pnl serisi."""
    df = pd.concat([signal.rename("s"), target.rename("y")], axis=1).dropna()
    if mode == "z":
        mu = df["s"].rolling(z_window, min_periods=60).mean().shift(1); sd = df["s"].rolling(z_window, min_periods=60).std().shift(1)
        z = (df["s"] - mu) / sd; pos = np.sign(z).where(z.abs() > thr, 0.0)
    else:
        pos = np.sign(df["s"]).where(df["s"].abs() > thr, 0.0)
    pos = pos.fillna(0.0)
    pnl = pos * df["y"] - (cost_bps / 1e4) * pos.abs()
    def st(p, ps):
        act = ps != 0; n = int(act.sum())
        if n < 20: return {"n": n}
        pa = p[act]; m, t, _ = nw_t(pa)
        ann = pa.mean() * 252 * act.mean(); vol = p.std() * np.sqrt(252)
        eq = p.cumsum(); dd = (eq - eq.cummax()).min()
        return {"n": n, "mean_bps": 1e4 * pa.mean(), "t": t, "hit": float((pa > 0).mean()), "sharpe": ann / vol if vol > 0 else np.nan, "ann_ret_pct": 100 * ann, "maxdd_pct": 100 * dd}
    sp = pd.Timestamp(split)
    res = {"ALL": st(pnl, pos), "IS": st(pnl[pnl.index < sp], pos[pos.index < sp]), "OOS": st(pnl[pnl.index >= sp], pos[pos.index >= sp])}
    res["by_year_bps"] = (1e4 * pnl[pos != 0].groupby(pnl[pos != 0].index.year).mean()).round(1).to_dict()
    return res, pnl

def summarize_pair(stock, driver, start="2010-01-01", lags=range(-2, 4)):
    """Hızlı özet: senkron korelasyon (tam/son3y/son1y), XU100 kontrollü kısmi korelasyon, ccf, gap/intra lag1 etkileri."""
    a = ret(stock); b = ret(driver)
    a = a[a.index >= pd.Timestamp(start)]; b = b[b.index >= pd.Timestamp(start)]
    out = {"stock": stock, "driver": driver}
    last = a.dropna().index.max()
    for lab, st_ in [("full", None), ("3y", last - pd.DateOffset(years=3)), ("1y", last - pd.DateOffset(years=1))]:
        df = pd.concat([a, b], axis=1).dropna()
        if st_ is not None: df = df[df.index >= st_]
        out[f"c0_{lab}"] = df.iloc[:, 0].corr(df.iloc[:, 1]) if len(df) > 30 else np.nan
    m = ret("XU100")
    if T(stock) != "XU100.IS":
        out["pc0_xu100"], _ = partial_corr(a, b, [m])
    c = ccf(a, b, lags); 
    for k in lags: out[f"c{k}"] = c.loc[k, "corr"]; out[f"t{k}"] = c.loc[k, "t_nw"]
    if is_bist(T(stock)):
        dd = decomp(stock); dd = dd[dd.index >= pd.Timestamp(start)]
        for col in ["gap", "intra"]:
            x = pd.concat([dd[col], b.shift(1).rename("b")], axis=1).dropna()
            if len(x) > 60:
                bb, tt, n = nw_t((x[col]-x[col].mean())/x[col].std(), (x["b"]-x["b"].mean())/x["b"].std())
                out[f"{col}_lag1_corr"] = bb; out[f"{col}_lag1_t"] = tt
    return out
