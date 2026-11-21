"""Ortak veri ve test kütüphanesi. Bütün backtest betikleri bunu kullanır (yöntem tek yerde dursun).

Profil: karar ABD kapanışında (16:00 ET), giriş aynı kapanış, çıkış t+1 / t+2 / t+3 kapanışı.

Temel kurallar (ayrıntı: ../YONTEM.md):
- Getiri: temettü ve bölünmeye göre düzeltilmiş (adjclose). Açılış/yüksek/düşük aynı katsayıyla düzeltilir.
- Takvim: NYSE işlem günleri (SPY'ın veri olan günleri).
- "Kapanışta bilinen" kuralı: bir öncü serinin t günü değeri ancak 16:00 ET'den önce kesinleşiyorsa t sinyalinde
  kullanılır. Aksi halde 1 gün geciktirilir (bkz. GECIKME ve bilinen_getiri()).
- Her test hem ham hem "sürüklenme düzeltilmiş" (hedefin aynı dönemdeki koşulsuz ortalaması çıkarılmış) raporlanır.
- Dönemler: IS <= 2018-12-31, OOS >= 2019-01-01, SON >= 2024-01-01 (SON, OOS'un alt kümesidir).
"""
import os
import functools

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERI = os.path.join(KOK, "veri")
IS_BITIS = "2018-12-31"
OOS_BAS = "2019-01-01"
SON_BAS = "2024-01-01"
ALT_SINIR_TARIH = "2005-01-01"  # testler bundan önceye gitmez

# ----------------------------------------------------------------------------------------------------------------
# Veri
# ----------------------------------------------------------------------------------------------------------------


def dosya_adi(sembol):
    return sembol.replace("^", "_idx_").replace("=", "_eq_").replace("/", "_")


@functools.lru_cache(maxsize=1)
def meta():
    m = pd.read_csv(os.path.join(VERI, "meta.csv"))
    m = m[m["n"] >= 60].set_index("sembol")  # 1 satırlık bozuk seriler dışarıda
    return m


@functools.lru_cache(maxsize=None)
def oku(sembol):
    """Tek sembol: tarih indeksli open/high/low/close/adjclose/volume + düzeltilmiş o/h/l (ao, ah, al)."""
    yol = os.path.join(VERI, "ham", dosya_adi(sembol) + ".csv")
    d = pd.read_csv(yol, parse_dates=["date"]).set_index("date").sort_index()
    d = d[~d.index.duplicated(keep="last")]
    for c in ["open", "high", "low", "close", "adjclose", "volume"]:
        d[c] = pd.to_numeric(d[c], errors="coerce")
    d = d[d["close"] > 0]
    k = d["adjclose"] / d["close"]
    d["ao"], d["ah"], d["al"] = d["open"] * k, d["high"] * k, d["low"] * k
    return d


@functools.lru_cache(maxsize=1)
def takvim():
    """NYSE işlem günleri."""
    idx = oku("SPY").index
    return idx[idx >= ALT_SINIR_TARIH]


# Öncü olarak kullanılacak serilerde, t günlük çubuğun ABD hisse kapanışında (16:00 ET) bilinip bilinmediği.
# 0 = bilinir (aynı gün kullanılabilir); 1 = çubuk 16:00 ET'den sonra kapanır, 1 gün geciktir.
# Ampirik sınama (kod/hizalama_testi.py, YONTEM.md bölüm 3):
# - Vadeliler (=F): tarih düzeltmesinden sonra ETF karşılıklarıyla aynı gün korelasyonu 0,8-0,99; "vadeli eksi ETF"
#   farkı ETF'in ertesi gece getirisini öngörmüyor (CL, GC, SI, NG, ES, NQ, ZN için |corr| < 0,06). Yani ölçülebilir
#   ileri bakış yok -> 0. Yine de birincil öncü ETF'tir; vadeli sinyali 1 gün gecikmeyle de raporlanır (SUPHELI_VADELI).
# - Kripto spot (BTC-USD vb.): çubuk 00:00 UTC'de kapanır, fark ertesi geceyi öngörüyor (corr ~0,3) -> 1.
# - Kur (=X): Yahoo'nun t tarihli çubuğu ABD'nin t-1 gününe denk gelir (FXE ile corr: t-1 günü 0,93, aynı gün 0,04).
#   Yani t çubuğu t kapanışında bilinir ama bayat bilgidir -> 0. Kur sinyali için kur ETF'lerini (UUP, FXE, FXY...) kullan.
# - DX-Y.NYB: UUP ile aynı gün 0,96; fark ertesi geceyi hafif öngörüyor (0,11) -> 1 (temkinli).
SUPHELI_VADELI = {"CL=F", "BZ=F", "NG=F", "RB=F", "HO=F", "GC=F", "SI=F", "PL=F", "PA=F", "HG=F", "ALI=F", "HRC=F",
                  "TIO=F", "ES=F", "NQ=F", "RTY=F", "YM=F", "ZN=F", "ZB=F", "ZT=F", "ZF=F", "6E=F", "6J=F", "BTC=F"}
BAYAT_KUR = True  # =X serileri bir önceki ABD gününü temsil eder


def gecikme(sembol):
    m = meta().loc[sembol]
    tur = m["tur"]
    if tur == "CRYPTOCURRENCY" or sembol == "DX-Y.NYB":
        return 1
    return 0


def log_getiri(sembol):
    """Kendi takviminde kapanıştan kapanışa log getiri."""
    d = oku(sembol)
    return np.log(d["adjclose"]).diff().dropna()


def hizali_getiri(sembol, bilinen=True):
    """NYSE takvimine hizalı log getiri.

    Sembolün kendi takvimindeki günlük log getirileri, o tarihe eşit ya da sonraki ilk NYSE gününe toplanır
    (hafta sonu/tatil birikir). bilinen=True ise gecikme(sembol) kadar gün kaydırılır: dönen serinin t değeri,
    t günü 16:00 ET'de kesin bilinen bilgidir.
    """
    r = log_getiri(sembol)
    tk = takvim()
    pos = tk.searchsorted(r.index, side="left")
    gecerli = pos < len(tk)
    s = pd.Series(r.values[gecerli], index=tk[pos[gecerli]]).groupby(level=0).sum()
    s = s.reindex(tk)
    ilk = r.index.min()
    s[s.index < ilk] = np.nan
    s = s.where(s.notna() | (s.index < ilk), 0.0)  # yerel tatil: yeni bilgi yok
    if bilinen and gecikme(sembol):
        s = s.shift(gecikme(sembol))
    return s


@functools.lru_cache(maxsize=None)
def _panel(alan):
    yol = os.path.join(VERI, f"panel_{alan}.parquet")
    if os.path.exists(yol):
        return pd.read_parquet(yol)
    tk = takvim()
    cols = {}
    for s in meta().index:
        try:
            cols[s] = oku(s)[alan].reindex(tk)
        except Exception:  # noqa: BLE001
            continue
    p = pd.DataFrame(cols, index=tk)
    p.to_parquet(yol)
    return p


def panel(alan="adjclose", semboller=None):
    """NYSE takviminde geniş tablo (yalnız aynı tarihli satırlar; ileri doldurma yok).
    alan: adjclose, close, ao, ah, al, open, high, low, volume."""
    p = _panel(alan)
    return p if semboller is None else p[[s for s in semboller if s in p.columns]]


def abd_semboller(tur=None):
    m = meta()
    m = m[m["saat_dilimi"] == "America/New_York"]
    if tur:
        m = m[m["tur"].isin([tur] if isinstance(tur, str) else tur)]
    return list(m.index)


def grup(ad):
    """evren.py'deki bir grubun, verisi olan sembolleri."""
    m = meta()
    return [s for s in m.index if ad in str(m.loc[s, "gruplar"]).split(";")]


# ----------------------------------------------------------------------------------------------------------------
# Getiri yardımcıları (hedef tarafı: ABD'de işlem gören araçlar)
# ----------------------------------------------------------------------------------------------------------------


def basit_getiri(semboller=None):
    """Kapanıştan kapanışa basit getiri paneli (t-1 -> t)."""
    return panel("adjclose", semboller).pct_change(fill_method=None)


def gece_gunici(semboller=None):
    """(gece, gunici): gece = açılış(t)/kapanış(t-1)-1, gunici = kapanış(t)/açılış(t)-1."""
    c, o = panel("adjclose", semboller), panel("ao", semboller)
    return o / c.shift(1) - 1, c / o - 1


def ileri_getiri(semboller=None, h=1, giris="kapanis"):
    """Sinyal günü t için ileri getiri.
    giris='kapanis': kapanış(t) -> kapanış(t+h)   (ana senaryo)
    giris='acilis' : açılış(t+1) -> kapanış(t+h)  (gecikmeli giriş; gece hareketi kaçırılır)
    giris='ertesi' : kapanış(t+1) -> kapanış(t+1+h) (1 gün geç giriş)
    giris='gece'   : kapanış(t) -> açılış(t+1)    (yalnız gece)
    """
    c = panel("adjclose", semboller)
    if giris == "kapanis":
        return c.shift(-h) / c - 1
    if giris == "acilis":
        o = panel("ao", semboller)
        return c.shift(-h) / o.shift(-1) - 1
    if giris == "ertesi":
        return c.shift(-h - 1) / c.shift(-1) - 1
    if giris == "gece":
        o = panel("ao", semboller)
        return o.shift(-1) / c - 1
    raise ValueError(giris)


def zskor(x, pencere=60, min_n=40):
    """Gecikmesiz ama yalnız geçmişi kullanan z: x_t / std(x_{t-pencere..t-1})."""
    sd = x.rolling(pencere, min_periods=min_n).std().shift(1)
    return x / sd


def kayan_beta(y, x, pencere=250, min_n=120):
    """y'nin x'e kayan betası; t değeri yalnız t-1'e kadar veriyi kullanır."""
    cov = y.rolling(pencere, min_periods=min_n).cov(x)
    var = x.rolling(pencere, min_periods=min_n).var()
    return (cov / var).shift(1)


# ----------------------------------------------------------------------------------------------------------------
# İstatistik
# ----------------------------------------------------------------------------------------------------------------


def nw_t(z, lag=0):
    """Ortalama için Newey-West t istatistiği. z: gözlem dizisi (NaN'lar atılır, zaman sırası korunur)."""
    z = np.asarray(z, dtype=float)
    z = z[~np.isnan(z)]
    n = len(z)
    if n < 10:
        return np.nan
    m = z.mean()
    e = z - m
    v = (e @ e) / n
    for k in range(1, min(lag, n - 1) + 1):
        w = 1 - k / (lag + 1)
        v += 2 * w * (e[k:] @ e[:-k]) / n
    if v <= 0:
        return np.nan
    return m / np.sqrt(v / n)


def bh_fdr(p, q=0.10):
    """Benjamini-Hochberg: geçenler için True dizisi."""
    p = np.asarray(p, dtype=float)
    ok = ~np.isnan(p)
    out = np.zeros(len(p), dtype=bool)
    idx = np.where(ok)[0]
    if len(idx) == 0:
        return out
    sirali = idx[np.argsort(p[idx])]
    m = len(sirali)
    esik = q * (np.arange(1, m + 1)) / m
    gecen = p[sirali] <= esik
    if gecen.any():
        k = np.max(np.where(gecen)[0])
        out[sirali[: k + 1]] = True
    return out


def t_to_p(t):
    """İki yönlü normal yaklaşım p değeri."""
    from scipy.stats import norm

    return 2 * (1 - norm.cdf(np.abs(t)))


# ----------------------------------------------------------------------------------------------------------------
# Olay / işlem testi
# ----------------------------------------------------------------------------------------------------------------

MALIYET_BPS = {"etf_likit": 5, "hisse_buyuk": 5, "orta": 10, "kaldiracli": 10, "dusuk_likidite": 20}


def islem_testi(sinyal, hedef, h=1, maliyet_bps=5, giris="kapanis", bas=None, bit=None, ust_at=10):
    """Tek hedef için sinyal testi.

    sinyal: NYSE takviminde Series; +1 = al, -1 = sat (ters ETF ya da açığa), 0/NaN = işlem yok.
            t günü değeri yalnız t günü 16:00 ET'de bilinen bilgiyle üretilmiş olmalı.
    hedef : sembol (ABD'de işlem gören).
    Dönen dict: n, yıllık işlem, brüt/net ortalama (bps), isabet, t (NW, gecikme h-1; işlem olmayan günler 0 sayılarak),
                sürüklenme düzeltilmiş ortalama ve t, yalnız-al / yalnız-sat ayrımı, en iyi `ust_at` işlem çıkınca net ort. ve t.
    Not: h>1'de işlemler örtüşür; t istatistiği günlük seri üzerinden HAC ile hesaplanır.
    """
    f = ileri_getiri([hedef], h, giris)[hedef]
    s = sinyal.reindex(f.index).fillna(0.0)
    if bas is not None:
        f, s = f[f.index >= bas], s[s.index >= bas]
    if bit is not None:
        f, s = f[f.index <= bit], s[s.index <= bit]
    gecerli = f.notna()
    f, s = f[gecerli], s[gecerli]
    if len(f) < 60:
        return {"n": 0}
    c = maliyet_bps / 1e4
    drift = f.mean()
    akt = s != 0
    n = int(akt.sum())
    if n == 0:
        return {"n": 0}
    brut = (s * f)[akt]
    net = brut - c
    anormal = (s * (f - drift))[akt]
    z_net = pd.Series(0.0, index=f.index)
    z_net[akt] = net
    z_abn = pd.Series(0.0, index=f.index)
    z_abn[akt] = anormal - c
    yil = (f.index[-1] - f.index[0]).days / 365.25
    out = {
        "n": n,
        "yillik_islem": round(n / max(yil, 0.1), 1),
        "brut_bps": round(float(brut.mean()) * 1e4, 1),
        "net_bps": round(float(net.mean()) * 1e4, 1),
        "isabet": round(float((brut > 0).mean()), 3),
        "t_net": round(float(nw_t(z_net.values, lag=h - 1)), 2),
        "anormal_net_bps": round(float(anormal.mean() - c) * 1e4, 1),
        "t_anormal": round(float(nw_t(z_abn.values, lag=h - 1)), 2),
        "hedef_drift_bps": round(float(drift) * 1e4, 1),
        "std_bps": round(float(brut.std()) * 1e4, 1),
    }
    for ad, maske in (("al", s > 0), ("sat", s < 0)):
        k = int(maske.sum())
        out[f"n_{ad}"] = k
        if k >= 10:
            out[f"net_bps_{ad}"] = round(float(((s * f)[maske] - c).mean()) * 1e4, 1)
            out[f"anormal_bps_{ad}"] = round(float(((s * (f - drift))[maske] - c).mean()) * 1e4, 1)
    if n > 3 * ust_at:
        kalan = net.sort_values(ascending=False).iloc[ust_at:]
        z2 = pd.Series(0.0, index=f.index)
        z2[kalan.index] = kalan
        out[f"net_bps_ust{ust_at}_haric"] = round(float(kalan.mean()) * 1e4, 1)
        out[f"t_ust{ust_at}_haric"] = round(float(nw_t(z2.values, lag=h - 1)), 2)
    return out


def donemli_test(sinyal, hedef, h=1, maliyet_bps=5, giris="kapanis"):
    """IS / OOS / SON dönemleri ve tamamı için islem_testi; düz dict döner (önekli anahtarlar)."""
    out = {"hedef": hedef, "h": h, "giris": giris, "maliyet_bps": maliyet_bps}
    for ad, b, e in (("tum", None, None), ("is", None, IS_BITIS), ("oos", OOS_BAS, None), ("son", SON_BAS, None)):
        r = islem_testi(sinyal, hedef, h, maliyet_bps, giris, b, e)
        for k, v in r.items():
            out[f"{ad}_{k}"] = v
    return out


def yillik_tablo(sinyal, hedef, h=1, maliyet_bps=5, giris="kapanis"):
    """Yıl yıl: işlem sayısı, net ortalama (bps), yılın toplam net getirisi (%)."""
    f = ileri_getiri([hedef], h, giris)[hedef]
    s = sinyal.reindex(f.index).fillna(0.0)
    ok = f.notna() & (s != 0)
    net = (s * f)[ok] - maliyet_bps / 1e4
    g = net.groupby(net.index.year)
    return pd.DataFrame({"n": g.size(), "net_bps": (g.mean() * 1e4).round(1), "toplam_yuzde": (g.sum() * 100).round(1)})


def plasebo(sinyal, hedef, h=1, kaydirma=(5, 10, 20, 40)):
    """Sinyali ileri kaydırıp (eski sinyal) aynı testi maliyetsiz yapar; gerçek etki varsa kaydırılmış sinyalde
    kaybolmalıdır. Dönen: kaydırma -> sürüklenme düzeltilmiş t. |t| > 2 çıkan plasebo, etkinin sinyale değil
    döneme/rejime bağlı olduğunu düşündürür."""
    return {k: islem_testi(sinyal.shift(k), hedef, h, 0).get("t_anormal") for k in kaydirma}


def gunluk_pnl(sinyal, hedef, h=1, maliyet_bps=5):
    """Örtüşen işlemleri 1/h ağırlıkla taşıyan stratejinin günlük net getirisi (portföy birleştirme için)."""
    r = basit_getiri([hedef])[hedef]
    s = sinyal.reindex(r.index).fillna(0.0)
    poz = sum(s.shift(k) for k in range(h)) / h  # t kapanışındaki pozisyon
    pnl = poz.shift(1) * r
    devir = (s.abs() / h) * 2  # her işlem bir giriş bir çıkış
    return (pnl - devir * (maliyet_bps / 2) / 1e4).dropna()


def ozet_pnl(pnl):
    """Günlük getiri serisinden yıllık getiri, oynaklık, Sharpe, en büyük düşüş."""
    pnl = pnl.dropna()
    if len(pnl) < 60:
        return {}
    yg = pnl.mean() * 252
    yo = pnl.std() * np.sqrt(252)
    egri = (1 + pnl).cumprod()
    dd = (egri / egri.cummax() - 1).min()
    return {
        "yillik_getiri_%": round(yg * 100, 1),
        "yillik_oynaklik_%": round(yo * 100, 1),
        "sharpe": round(yg / yo, 2) if yo > 0 else np.nan,
        "en_buyuk_dusus_%": round(dd * 100, 1),
        "t": round(float(nw_t(pnl.values, lag=5)), 2),
    }


# ----------------------------------------------------------------------------------------------------------------
# Hızlı çift taraması (öncü x hedef)
# ----------------------------------------------------------------------------------------------------------------


def tarama(oncu_df, hedef_semboller, h=1, bas=None, bit=None, min_n=500):
    """Vektörel öngörü taraması: her (öncü, hedef) için corr(öncü_t, hedef ileri getirisi t->t+h) ve yaklaşık t.

    oncu_df: NYSE takviminde, t günü kapanışta bilinen sinyal sütunları (ör. hizali_getiri çıktıları, z-skorlar).
    Dönen: uzun tablo [oncu, hedef, n, corr, t]. t = corr*sqrt(n_etkin-2)/sqrt(1-corr^2), n_etkin = n/h (örtüşme düzeltmesi).
    Yalnız eleme içindir; ayakta kalanlar islem_testi ile yeniden sınanır.
    """
    f = ileri_getiri(hedef_semboller, h)
    x = oncu_df.reindex(f.index)
    if bas is not None:
        f, x = f[f.index >= bas], x[x.index >= bas]
    if bit is not None:
        f, x = f[f.index <= bit], x[x.index <= bit]
    satirlar = []
    fv = f.values
    for oc in x.columns:
        xv = x[oc].values
        ok = ~np.isnan(xv)[:, None] & ~np.isnan(fv)
        n = ok.sum(axis=0)
        xx = np.where(ok, xv[:, None], np.nan)
        ff = np.where(ok, fv, np.nan)
        xm, fm = np.nanmean(xx, axis=0), np.nanmean(ff, axis=0)
        cov = np.nanmean((xx - xm) * (ff - fm), axis=0)
        sx, sf = np.nanstd(xx, axis=0), np.nanstd(ff, axis=0)
        with np.errstate(invalid="ignore", divide="ignore"):
            c = cov / (sx * sf)
            ne = n / h
            t = c * np.sqrt(np.maximum(ne - 2, 1)) / np.sqrt(1 - c**2)
        for j, hs in enumerate(f.columns):
            if n[j] >= min_n and hs != oc:
                satirlar.append((oc, hs, int(n[j]), c[j], t[j]))
    return pd.DataFrame(satirlar, columns=["oncu", "hedef", "n", "corr", "t"])


if __name__ == "__main__":
    # Kendi kendini sınama: bilinen bir etki (IBS) ve bir plasebo
    c, hi, lo = panel("adjclose", ["QQQ"])["QQQ"], panel("ah", ["QQQ"])["QQQ"], panel("al", ["QQQ"])["QQQ"]
    ibs = (c - lo) / (hi - lo)
    sin = (ibs < 0.2).astype(float)
    print("QQQ IBS<0.2, h=1:", {k: v for k, v in donemli_test(sin, "QQQ", 1).items() if k.endswith(("_n", "net_bps", "t_net", "t_anormal"))})
    print("plasebo:", plasebo(sin, "QQQ", 1))
