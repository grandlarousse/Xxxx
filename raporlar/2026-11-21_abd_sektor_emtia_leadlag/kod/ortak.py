"""Ortak veri ve test kütüphanesi. Bütün backtest betikleri bunu kullanır (yöntem tek yerde dursun).

Profil: karar ABD kapanışında (16:00 ET), giriş aynı kapanış, çıkış t+1 / t+2 / t+3 kapanışı.

Temel kurallar (ayrıntı: ../YONTEM.md):
- Getiri: temettü ve bölünmeye göre düzeltilmiş (adjclose). Açılış/yüksek/düşük aynı katsayıyla düzeltilir.
- Takvim: NYSE işlem günleri (SPY'ın veri olan günleri).
- "Kapanışta bilinen" kuralı: bir öncü serinin t günü değeri ancak 16:00 ET'den önce kesinleşiyorsa t sinyalinde
  kullanılır. Aksi halde 1 gün geciktirilir (bkz. GECIKME ve bilinen_getiri()).
- Her test hem ham hem "sürüklenme düzeltilmiş" (hedefin aynı dönemdeki koşulsuz ortalaması çıkarılmış) raporlanır.
- Dönemler: IS <= 2018-12-31, OOS >= 2019-01-01, SON >= 2024-01-01 (SON, OOS'un alt kümesidir).
  2015'ten sonra başlayan araçta IS = geçerli günlerin ilk %55'i (donem_sinirlari).

Sürüm 2 (21.11.2026, yöntem eleştirmeni denetiminden sonra; ayrıntı YONTEM.md bölüm 10):
  hac_t (düz ağırlıklı HAC), maliyet_serisi (işlem günündeki likiditeye göre), islem_testi(hedge=...),
  plasebo_dairesel, havuz_testi (çok hedefli testlerde gün bazlı portföy t'si), tarama (White t, arındırılmış),
  siniflandir (yeni A/B eşikleri ve OOS üzerinde BH), gecikmeli serilerde "sonraki ilk NYSE günü" eşlemesi.
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
    """1 = çubuk 16:00 ET'den sonra kapanır (ya da zamanlaması doğrulanamadı): kendinden SONRAKİ ilk NYSE gününe eşlenir."""
    m = meta().loc[sembol]
    tur = m["tur"]
    if tur == "CRYPTOCURRENCY" or sembol in ("DX-Y.NYB", "^MOVE"):
        return 1
    return 0


def kaldiracli(sembol):
    """Kaldıraçlı/ters ETF mi? Bunlar keşif hedefi değil, uygulama aracıdır."""
    try:
        g = str(meta().loc[sembol, "gruplar"]).split(";")
    except KeyError:
        return False
    return ("kaldiracli" in g) or ("ek_kaldiracli" in g)


@functools.lru_cache(maxsize=1)
def bayat_hedefler():
    """Kapanış fiyatı bayat olan ETF'ler (ek/dogrulama/bayat_kapanis_taramasi.csv: t_x >= 3 ya da hacim < 1 mn $) + CPER."""
    yol = os.path.join(KOK, "ek", "dogrulama", "bayat_kapanis_taramasi.csv")
    out = {"CPER", "CANE", "WEAT", "CRAK"}
    if os.path.exists(yol):
        d = pd.read_csv(yol)
        out |= set(d.loc[(d["t_x"] >= 3) | (d["hacim_mn"] < 1), "etf"])
    return out


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
    # Eşleme, 2005 öncesini de içeren TAM NYSE takvimiyle yapılır. Yalnız takvim() (>= ALT_SINIR_TARIH) kullanılırsa
    # 2000-2004 getirilerinin tamamı ilk güne (2005-01-03) yığılır: o gün dev bir sahte getiri oluşur, 60 günlük
    # z-skoru ve 250 günlük beta pencereleri bozulur (yöntem sınaması G1/S1, 21.11.2026).
    tam = oku("SPY").index
    # Gecikmeli seriler (kripto spot, DX-Y.NYB, ^MOVE): çubuk kendinden SONRAKİ ilk NYSE gününe eşlenir. Böylece
    # hafta sonu kripto hareketi pazartesi sinyaline girer; cuma çubuğu (ABD kapanışından sonra biter) da pazartesiye.
    gec = bool(bilinen and gecikme(sembol))
    pos = tam.searchsorted(r.index, side="right" if gec else "left")
    gecerli = pos < len(tam)
    s = pd.Series(r.values[gecerli], index=tam[pos[gecerli]]).groupby(level=0).sum()
    s = s.reindex(tk)
    ilk = r.index.min()
    s[s.index < ilk] = np.nan
    s = s.where(s.notna() | (s.index < ilk), 0.0)  # yerel tatil: yeni bilgi yok
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


def hac_t(z, lag=0):
    """Düz ağırlıklı (Hansen-Hodrick) HAC t. Örtüşen h günlük getirilerde Newey-West(h-1) kalıcı sinyallerde t'yi
    %10-13 şişiriyordu (yöntem sınaması S5). Varyans <= 0 çıkarsa Newey-West'e düşer."""
    z = np.asarray(z, dtype=float)
    z = z[~np.isnan(z)]
    n = len(z)
    if n < 10:
        return np.nan
    m = z.mean()
    e = z - m
    v = (e @ e) / n
    for k in range(1, min(lag, n - 1) + 1):
        v += 2 * (e[k:] @ e[:-k]) / n
    if v <= 0:
        return nw_t(z, lag)
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


def t_to_p(t, tek_yon=False):
    """Normal yaklaşım p değeri (iki yönlü; tek_yon=True ise P(Z >= t))."""
    from scipy.stats import norm

    t = np.asarray(t, dtype=float)
    return (1 - norm.cdf(t)) if tek_yon else 2 * (1 - norm.cdf(np.abs(t)))


# ----------------------------------------------------------------------------------------------------------------
# Maliyet, arındırma
# ----------------------------------------------------------------------------------------------------------------


@functools.lru_cache(maxsize=None)
def maliyet_serisi(hedef):
    """İşlem günündeki likiditeye göre gidiş-dönüş maliyet (bps). 60 günlük medyan dolar hacmi (1 gün gecikmeli):
    >= 100 mn $ -> 5; 20-100 mn $ -> 10; < 20 mn $ -> 20. Kaldıraçlı/ters ETF'te taban 10.
    Aracı kurum komisyonu DAHİL DEĞİL (raporda ayrı duyarlılık)."""
    c, v = panel("close", [hedef])[hedef], panel("volume", [hedef])[hedef]
    dv = (c * v).rolling(60, min_periods=20).median().shift(1) / 1e6
    m = pd.Series(20.0, index=c.index)
    m[dv >= 20] = 10.0
    m[dv >= 100] = 5.0
    if kaldiracli(hedef):
        m = m.clip(lower=10.0)
    return m


def artik_getiri(sembol, faktor="SPY", bilinen=True):
    """Öncü ya da hedef getirisinin faktörden (SPY) arındırılmış kısmı: x - beta*r_faktor (beta 250 gün, gecikmeli).
    Amaç: piyasanın kendi günlük dönüşünü 'öncülük' sanmamak (yöntem sınaması G4)."""
    x = hizali_getiri(sembol, bilinen=bilinen)
    f = hizali_getiri(faktor, bilinen=False)
    if sembol == faktor:
        return x
    return x - kayan_beta(x, f) * f


@functools.lru_cache(maxsize=8192)
def _ileri(hedef, h, giris, hedge=None):
    """Önbellekli ileri getiri serisi (çağıran yerinde değiştirmemeli)."""
    f = ileri_getiri([hedef], h, giris)[hedef]
    if hedge and hedge != hedef:
        fh = ileri_getiri([hedge], h, giris)[hedge]
        r = basit_getiri([hedef, hedge])
        f = f - kayan_beta(r[hedef], r[hedge]) * fh
    return f


def donem_sinirlari(hedef):
    """(is_bitis, oos_bas). Araç 2015'ten sonra başladıysa IS = geçerli günlerin ilk %55'i."""
    c = panel("adjclose", [hedef])[hedef].dropna()
    if len(c) and c.index[0] > pd.Timestamp("2015-01-01"):
        kes = c.index[int(len(c) * 0.55)]
        return str(kes.date()), str((kes + pd.Timedelta(days=1)).date())
    return IS_BITIS, OOS_BAS


# ----------------------------------------------------------------------------------------------------------------
# Olay / işlem testi
# ----------------------------------------------------------------------------------------------------------------


def islem_testi(sinyal, hedef, h=1, maliyet_bps=None, giris="kapanis", bas=None, bit=None, ust_at=10, hedge=None):
    """Tek hedef için sinyal testi.

    sinyal: NYSE takviminde Series; +1 = al, -1 = sat (ters ETF ya da açığa), 0/NaN = işlem yok.
            t günü değeri yalnız t günü 16:00 ET'de bilinen bilgiyle üretilmiş olmalı.
    hedef : sembol (ABD'de işlem gören).
    maliyet_bps: sayı, Series ya da None (None -> maliyet_serisi(hedef): işlem günündeki likidite sınıfı).
    hedge : verilirse (ör. "SPY") ileri getiri hedef - beta*hedge olarak hesaplanır (piyasadan arındırılmış test).
    Dönen dict: n, yıllık işlem, brüt/net ortalama (bps), isabet, t (düz ağırlıklı HAC, gecikme h-1; işlem olmayan
                günler 0 sayılarak), sürüklenme düzeltilmiş ortalama ve t, AL / SAT bacakları ayrı (ham net, anormal, t),
                en iyi `ust_at` işlem çıkınca net ortalama ve t.
    """
    f = _ileri(hedef, h, giris, hedge)
    s = sinyal.reindex(f.index).fillna(0.0)
    if maliyet_bps is None:
        c = maliyet_serisi(hedef).reindex(f.index) / 1e4
    elif isinstance(maliyet_bps, pd.Series):
        c = maliyet_bps.reindex(f.index) / 1e4
    else:
        c = pd.Series(float(maliyet_bps) / 1e4, index=f.index)
    if bas is not None:
        f, s, c = f[f.index >= bas], s[s.index >= bas], c[c.index >= bas]
    if bit is not None:
        f, s, c = f[f.index <= bit], s[s.index <= bit], c[c.index <= bit]
    gecerli = f.notna()
    f, s, c = f[gecerli], s[gecerli], c[gecerli].fillna(20 / 1e4)
    if len(f) < 60:
        return {"n": 0}
    drift = f.mean()
    akt = s != 0
    n = int(akt.sum())
    if n == 0:
        return {"n": 0}
    brut = (s * f)[akt]
    net = brut - c[akt]
    anormal = (s * (f - drift))[akt] - c[akt]
    z_net = pd.Series(0.0, index=f.index)
    z_net[akt] = net
    z_abn = pd.Series(0.0, index=f.index)
    z_abn[akt] = anormal
    yil = (f.index[-1] - f.index[0]).days / 365.25
    out = {
        "n": n,
        "yillik_islem": round(n / max(yil, 0.1), 1),
        "brut_bps": round(float(brut.mean()) * 1e4, 1),
        "net_bps": round(float(net.mean()) * 1e4, 1),
        "isabet": round(float((brut > 0).mean()), 3),
        "t_net": round(float(hac_t(z_net.values, lag=h - 1)), 2),
        "anormal_net_bps": round(float(anormal.mean()) * 1e4, 1),
        "t_anormal": round(float(hac_t(z_abn.values, lag=h - 1)), 2),
        "hedef_drift_bps": round(float(drift) * 1e4, 1),
        "std_bps": round(float(brut.std()) * 1e4, 1),
        "maliyet_ort_bps": round(float(c[akt].mean()) * 1e4, 1),
    }
    for ad, maske in (("al", s > 0), ("sat", s < 0)):
        k = int(maske.sum())
        out[f"n_{ad}"] = k
        if k >= 10:
            out[f"net_bps_{ad}"] = round(float(((s * f)[maske] - c[maske]).mean()) * 1e4, 1)
            ab = (s * (f - drift))[maske] - c[maske]
            out[f"anormal_bps_{ad}"] = round(float(ab.mean()) * 1e4, 1)
            zz = pd.Series(0.0, index=f.index)
            zz[maske] = ab
            out[f"t_anormal_{ad}"] = round(float(hac_t(zz.values, lag=h - 1)), 2)
    if n > 3 * ust_at:
        kalan = net.sort_values(ascending=False).iloc[ust_at:]
        z2 = pd.Series(0.0, index=f.index)
        z2[kalan.index] = kalan
        out[f"net_bps_ust{ust_at}_haric"] = round(float(kalan.mean()) * 1e4, 1)
        out[f"t_ust{ust_at}_haric"] = round(float(hac_t(z2.values, lag=h - 1)), 2)
    return out


def donemli_test(sinyal, hedef, h=1, maliyet_bps=None, giris="kapanis", hedge=None):
    """IS / OOS / SON dönemleri ve tamamı için islem_testi; düz dict döner (önekli anahtarlar)."""
    is_bit, oos_bas = donem_sinirlari(hedef)
    out = {"hedef": hedef, "h": h, "giris": giris, "is_bitis": is_bit}
    for ad, b, e in (("tum", None, None), ("is", None, is_bit), ("oos", oos_bas, None), ("son", SON_BAS, None)):
        r = islem_testi(sinyal, hedef, h, maliyet_bps, giris, b, e, hedge=hedge)
        for k, v in r.items():
            out[f"{ad}_{k}"] = v
    return out


def yillik_tablo(sinyal, hedef, h=1, maliyet_bps=None, giris="kapanis"):
    """Yıl yıl: işlem sayısı, net ortalama (bps), yılın toplam net getirisi (%)."""
    f = ileri_getiri([hedef], h, giris)[hedef]
    s = sinyal.reindex(f.index).fillna(0.0)
    c = (maliyet_serisi(hedef).reindex(f.index) if maliyet_bps is None else
         (maliyet_bps.reindex(f.index) if isinstance(maliyet_bps, pd.Series) else pd.Series(float(maliyet_bps), index=f.index))) / 1e4
    ok = f.notna() & (s != 0)
    net = (s * f)[ok] - c[ok]
    g = net.groupby(net.index.year)
    return pd.DataFrame({"n": g.size(), "net_bps": (g.mean() * 1e4).round(1), "toplam_yuzde": (g.sum() * 100).round(1)})


def plasebo(sinyal, hedef, h=1, kaydirma=(5, 10, 20, 40)):
    """ESKİ plasebo: sinyali sabit gün kaydırır (maliyetsiz, sürüklenme düzeltilmiş t). Takvim sinyallerinde kaydırılmış
    sinyal aynı güne düşebildiği için güvenilmez; H koşulu için plasebo_dairesel kullan."""
    return {k: islem_testi(sinyal.shift(k), hedef, h, 0).get("t_anormal") for k in kaydirma}


def plasebo_dairesel(sinyal, hedef, h=1, n=1000, min_kaydirma=60, tohum=0, hedge=None, bas=None, bit=None):
    """H koşulu: sinyal dairesel olarak rastgele kaydırılır (>= min_kaydirma gün, n tekrar). Gerçek sinyalin
    sürüklenme düzeltilmiş ortalaması bu dağılımın üst %2,5'inde olmalı. Dönen: {'plasebo_p', 'plasebo_ort_bps'}.
    Sinyalin kümelenme yapısı korunur; yalnız zamanlaması bozulur."""
    f = _ileri(hedef, h, "kapanis", hedge)
    s = sinyal.reindex(f.index).fillna(0.0)
    if bas is not None:
        f, s = f[f.index >= bas], s[s.index >= bas]
    if bit is not None:
        f, s = f[f.index <= bit], s[s.index <= bit]
    ok = f.notna()
    a = (f[ok] - f[ok].mean()).values
    sv = s[ok].values
    nact = int((sv != 0).sum())
    if nact < 20 or len(a) < 2 * min_kaydirma + 10:
        return {"plasebo_p": np.nan, "plasebo_ort_bps": np.nan}
    gercek = float((sv * a).sum() / nact)
    rng = np.random.default_rng(tohum)
    ks = rng.integers(min_kaydirma, len(a) - min_kaydirma, n)
    st = np.array([(np.roll(sv, int(k)) * a).sum() / nact for k in ks])
    return {"plasebo_p": round(float((np.sum(st >= gercek) + 1) / (n + 1)), 4), "plasebo_ort_bps": round(float(st.mean()) * 1e4, 2)}


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
# Çok hedefli (havuz) test: aynı gün birden çok hedefte işlem varsa gözlemler bağımsız değildir.
# ----------------------------------------------------------------------------------------------------------------


def havuz_testi(sinyaller, h=1, maliyet_bps=None, giris="kapanis", bas=None, bit=None, hedge=None):
    """Çok hedefli sinyal testi. sinyaller: DataFrame (sütun = hedef sembol; değer +1/-1/0).

    Her sinyal günü için o gün işlem açılan hedeflerin EŞİT AĞIRLIKLI ortalaması alınır; t istatistiği bu günlük
    portföy serisinden hesaplanır (işlem olmayan gün 0). Düz havuz t'si 50 bağlantılı hedefte ~5 kat şişer (sınama S10).
    Sürüklenme düzeltmesi hedef bazındadır (her hedefin aynı dönemdeki koşulsuz ortalaması).
    """
    cols = [c for c in sinyaller.columns if c in panel("adjclose").columns]
    F = ileri_getiri(cols, h, giris)
    if hedge:
        fh = ileri_getiri([hedge], h, giris)[hedge]
        r = basit_getiri(cols + ([hedge] if hedge not in cols else []))
        B = pd.DataFrame({c: kayan_beta(r[c], r[hedge]) for c in cols})
        F = F - B.mul(fh, axis=0)
    S = sinyaller[cols].reindex(F.index).fillna(0.0)
    if maliyet_bps is None:
        C = pd.DataFrame({c: maliyet_serisi(c) for c in cols}).reindex(F.index).fillna(20.0) / 1e4
    else:
        C = pd.DataFrame(float(maliyet_bps) / 1e4, index=F.index, columns=cols)
    if bas is not None:
        F, S, C = F[F.index >= bas], S[S.index >= bas], C[C.index >= bas]
    if bit is not None:
        F, S, C = F[F.index <= bit], S[S.index <= bit], C[C.index <= bit]
    akt = (S != 0) & F.notna()
    n_islem = int(akt.values.sum())
    if n_islem == 0 or len(F) < 60:
        return {"n_islem": 0}
    drift = F.mean()
    net = (S * F - C).where(akt)
    abn = (S * (F - drift) - C).where(akt)
    gun_n = akt.sum(axis=1)
    var = gun_n > 0
    p_net = (net.sum(axis=1) / gun_n).where(var)
    p_abn = (abn.sum(axis=1) / gun_n).where(var)
    out = {
        "n_islem": n_islem,
        "n_gun": int(var.sum()),
        "ort_islem_gun": round(float(gun_n[var].mean()), 1),
        "net_bps": round(float(p_net.mean()) * 1e4, 1),
        "anormal_net_bps": round(float(p_abn.mean()) * 1e4, 1),
        "t_net": round(float(hac_t(p_net.fillna(0.0).values, lag=h - 1)), 2),
        "t_anormal": round(float(hac_t(p_abn.fillna(0.0).values, lag=h - 1)), 2),
        "isabet_gun": round(float((p_net[var] > 0).mean()), 3),
        "islem_net_bps": round(float(np.nanmean(net.values)) * 1e4, 1),
    }
    for ad, maske in (("al", (S > 0) & F.notna()), ("sat", (S < 0) & F.notna())):
        k = maske.sum(axis=1)
        if int(k.sum()) >= 20:
            pa = (abn.where(maske).sum(axis=1) / k).where(k > 0)
            pn = (net.where(maske).sum(axis=1) / k).where(k > 0)
            out[f"n_{ad}"] = int(k.sum())
            out[f"net_bps_{ad}"] = round(float(pn.mean()) * 1e4, 1)
            out[f"anormal_bps_{ad}"] = round(float(pa.mean()) * 1e4, 1)
            out[f"t_anormal_{ad}"] = round(float(hac_t(pa.fillna(0.0).values, lag=h - 1)), 2)
    return out


def havuz_donemli(sinyaller, h=1, maliyet_bps=None, giris="kapanis", hedge=None):
    """havuz_testi'nin tüm / IS / OOS / SON dökümü (sabit takvim sınırlarıyla)."""
    out = {"h": h, "giris": giris, "n_hedef": sinyaller.shape[1]}
    for ad, b, e in (("tum", None, None), ("is", None, IS_BITIS), ("oos", OOS_BAS, None), ("son", SON_BAS, None)):
        for k, v in havuz_testi(sinyaller, h, maliyet_bps, giris, b, e, hedge).items():
            out[f"{ad}_{k}"] = v
    return out


def havuz_gunluk(sinyaller, h=1, maliyet_bps=None, giris="kapanis"):
    """Gün bazlı eşit ağırlıklı portföy serisi (sürüklenme düzeltilmiş net); yıllık tablo ve plasebo için."""
    cols = [c for c in sinyaller.columns if c in panel("adjclose").columns]
    F = ileri_getiri(cols, h, giris)
    S = sinyaller[cols].reindex(F.index).fillna(0.0)
    C = (pd.DataFrame({c: maliyet_serisi(c) for c in cols}).reindex(F.index).fillna(20.0) if maliyet_bps is None
         else pd.DataFrame(float(maliyet_bps), index=F.index, columns=cols)) / 1e4
    akt = (S != 0) & F.notna()
    abn = (S * (F - F.mean()) - C).where(akt)
    k = akt.sum(axis=1)
    return (abn.sum(axis=1) / k).where(k > 0)


# ----------------------------------------------------------------------------------------------------------------
# Hızlı çift taraması (öncü x hedef) - yalnız h=1, White t, piyasadan arındırılmış
# ----------------------------------------------------------------------------------------------------------------


def tarama(oncu_df, hedef_semboller, h=1, bas=None, bit=None, min_n=500, arindir="SPY", zskorla=True):
    """Vektörel öngörü taraması (yalnız eleme içindir; ayakta kalanlar islem_testi ile yeniden sınanır).

    oncu_df: NYSE takviminde, t günü kapanışta bilinen öncü serileri (tercihen artik_getiri çıktıları).
    İşlem: öncü z-skorlanır; hedefin ileri getirisi SPY'dan arındırılır (arindir) ve 60 günlük oynaklığa bölünür;
    White t = sum(x*f) / sqrt(sum(x^2 * f^2)). Eski sürümdeki corr tabanlı t ham getiride medyan 1,8 kat şişikti ve
    piyasanın kendi günlük dönüşünü 'öncülük' diye buluyordu (yöntem sınaması G3-G4). h > 1 desteklenmez.
    Dönen: uzun tablo [oncu, hedef, n, b (z başına bps), t].
    """
    if h != 1:
        raise ValueError("tarama yalnız h=1 için ayarlıdır; h=2-3 için islem_testi kullan")
    hedefler = [c for c in hedef_semboller if c in panel("adjclose").columns]
    r = basit_getiri(hedefler + ([arindir] if arindir and arindir not in hedefler else []))
    F = r[hedefler].shift(-1)
    if arindir:
        fa = r[arindir].shift(-1)
        B = pd.DataFrame({c: kayan_beta(r[c], r[arindir]) for c in hedefler})
        F = F - B.mul(fa, axis=0)
    vol = r[hedefler].rolling(60, min_periods=40).std().shift(1)
    Fz = F / vol
    X = oncu_df.reindex(Fz.index)
    if zskorla:
        X = X.apply(lambda c: zskor(c, 60))
    X = X.clip(-5, 5)
    if bas is not None:
        Fz, X = Fz[Fz.index >= bas], X[X.index >= bas]
    if bit is not None:
        Fz, X = Fz[Fz.index <= bit], X[X.index <= bit]
    Fz = Fz - Fz.mean()
    xm, fm = X.notna().values.astype(float), Fz.notna().values.astype(float)
    xv, fv = np.nan_to_num(X.values), np.nan_to_num(Fz.values)
    n = xm.T @ fm
    pay = xv.T @ fv
    payda = np.sqrt((xv**2).T @ (fv**2))
    with np.errstate(invalid="ignore", divide="ignore"):
        t = pay / payda
        b = pay / ((xv**2).T @ fm)
    satirlar = []
    for i, oc in enumerate(X.columns):
        for j, hs in enumerate(Fz.columns):
            if n[i, j] >= min_n and oc != hs:
                satirlar.append((oc, hs, int(n[i, j]), float(b[i, j]), float(t[i, j])))
    return pd.DataFrame(satirlar, columns=["oncu", "hedef", "n", "b", "t"])


# ----------------------------------------------------------------------------------------------------------------
# Sınıflandırma (YONTEM.md bölüm 6, sürüm 2)
# ----------------------------------------------------------------------------------------------------------------

P_SIFIR_SAGLAM = 3.9e-5   # P(t_IS >= 2,5) * P(t_OOS >= 2,5), bağımsız sıfır hipotezi altında
P_SIFIR_KOSULLU = 1.4e-4  # P(t_IS >= 2,5) * P(t_OOS >= 2,0)


def siniflandir(df, aile_sutunu="aile", onek="", tavan_kosullu=None):
    """Koşul sütunlarını (k_A..k_I) ve sınıfı ekler.

    Beklenen sütunlar (onek + ...): is_t_anormal, oos_t_anormal, is_anormal_net_bps, oos_anormal_net_bps, son_net_bps,
    tum_anormal_net_bps, tum_net_bps_ust10_haric, tum_t_ust10_haric, tum_n, oos_n ve (ön elemeyi geçenlerde)
    yil_pozitif_oran, plasebo_p, acilis_anormal_bps, acilis_net_bps. Eksik sütun = koşul sağlanmadı.
    tavan_kosullu: bool Series; True olan satırlar en çok KOŞULLU olabilir (ör. hisse düzeyi AL-dönüş sinyalleri).
    BH: aile içinde, IS'ten seçilen (k_A) satırların OOS tek yönlü p değerlerine q = %10.
    """
    def g(c):
        return pd.to_numeric(df[onek + c], errors="coerce") if (onek + c) in df.columns else pd.Series(np.nan, index=df.index)

    df["k_A"] = g("is_t_anormal") >= 2.5
    ayni = (g("is_anormal_net_bps") > 0) & (g("oos_anormal_net_bps") > 0)
    df["k_B"] = ayni & (g("oos_t_anormal") >= 2.5)
    df["k_B_zayif"] = ayni & (g("oos_t_anormal") >= 2.0)
    df["k_C"] = g("son_net_bps") > 0
    df["k_D"] = g("tum_anormal_net_bps") >= 10
    df["k_E"] = (g("tum_net_bps_ust10_haric") > 0) & (g("tum_t_ust10_haric") >= 1.5)
    df["k_F"] = g("yil_pozitif_oran") >= 0.6
    df["k_G"] = (g("tum_n") >= 100) & (g("oos_n") >= 40)
    df["k_H"] = g("plasebo_p") <= 0.025
    bayat = df["hedef"].isin(bayat_hedefler()) if "hedef" in df.columns else False
    df["k_I"] = np.where(bayat, g("acilis_net_bps") > 0, g("acilis_anormal_bps") > 0)
    df["p_oos"] = t_to_p(g("oos_t_anormal").fillna(-9).values, tek_yon=True)
    df["bh_oos"] = False
    aileler = df[aile_sutunu] if aile_sutunu in df.columns else pd.Series("tek", index=df.index)
    for a in aileler.unique():
        m = (aileler == a) & df["k_A"]
        if m.any():
            df.loc[m, "bh_oos"] = bh_fdr(df.loc[m, "p_oos"].values, 0.10)
    yan = ["k_C", "k_D", "k_E", "k_F", "k_G", "k_H", "k_I"]
    tam = df["k_A"] & df["k_B"] & df["bh_oos"] & df[yan].all(axis=1)
    kosullu = df["k_A"] & df["k_B_zayif"] & (df[yan].sum(axis=1) >= 6) & ~tam
    izle = (g("is_t_anormal") >= 2.0) & (g("oos_t_anormal") >= 1.5) & ayni & ~tam & ~kosullu
    if tavan_kosullu is not None:
        kosullu = kosullu | (tam & tavan_kosullu)
        tam = tam & ~tavan_kosullu
    df["sinif"] = np.where(tam, "SAGLAM", np.where(kosullu, "KOSULLU", np.where(izle, "IZLE", "ELENDI")))
    return df


def ek_olcutler(sinyal, hedef, h=1, maliyet_bps=None, hedge=None):
    """Pahalı sağlamlık ölçütleri (F, H, I koşulları için); yalnız ön elemeyi geçen testlerde çağır."""
    yt = yillik_tablo(sinyal, hedef, h, maliyet_bps)
    yt = yt[yt["n"] >= 3]
    ac = islem_testi(sinyal, hedef, h, maliyet_bps, "acilis")
    er = islem_testi(sinyal, hedef, h, maliyet_bps, "ertesi")
    out = {
        "yil_pozitif_oran": round(float((yt["net_bps"] > 0).mean()), 2) if len(yt) else np.nan,
        "yil_sayisi": int(len(yt)),
        "acilis_anormal_bps": ac.get("anormal_net_bps"),
        "acilis_net_bps": ac.get("net_bps"),
        "acilis_t_anormal": ac.get("t_anormal"),
        "ertesi_anormal_bps": er.get("anormal_net_bps"),
        "ertesi_t_anormal": er.get("t_anormal"),
    }
    out.update(plasebo_dairesel(sinyal, hedef, h, hedge=hedge))
    return out


def son_sinyal(sinyal):
    """Son işlem günündeki sinyal değeri ve tarihi (rapordaki 'bugün açık mı' sütunu için)."""
    s = sinyal.dropna()
    return {"son_gun": str(s.index[-1].date()), "son_sinyal": float(s.iloc[-1])} if len(s) else {}


if __name__ == "__main__":
    # Kendi kendini sınama: bilinen bir etki (IBS) ve plasebo
    c, hi, lo = panel("adjclose", ["QQQ"])["QQQ"], panel("ah", ["QQQ"])["QQQ"], panel("al", ["QQQ"])["QQQ"]
    ibs = (c - lo) / (hi - lo)
    sin = (ibs < 0.2).astype(float)
    d = donemli_test(sin, "QQQ", 1)
    print("QQQ IBS<0.2, h=1:", {k: v for k, v in d.items() if k.endswith(("_n", "anormal_net_bps", "t_anormal", "maliyet_ort_bps"))})
    print("ek ölçütler:", ek_olcutler(sin, "QQQ", 1))
    print("SPY hedge'li:", {k: v for k, v in donemli_test(sin, "QQQ", 1, hedge="SPY").items() if k.endswith(("anormal_net_bps", "t_anormal"))})
