"""Ortak kütüphane: veri yükleme, getiri tanımları, takvim hizalama, olay testi, BH-FDR.

KULLANIM ÖRNEĞİ (B1-B3 aynen kopyalar; getiriler bps, takvim TK() = SPY günleri)
    import sys; sys.path.insert(0, "kod"); import ortak as o
    C = o.evren("Ç")                                    # "T", "Ç", "YENİ", "ARAÇ"
    Cl, H, L = (o._mat(a, C) for a in ("AClose", "AHigh", "ALow"))
    # 1) olay testi: F1a, IBS < 0,2 -> al, h=1 (filtreler madde 2.1-2.2 islemler() içinde)
    isl = o.islemler((Cl - L) / (H - L) < 0.2, h=1, getiri="ham", bilanco_at=True, test_id="F1a_C_h1")
    sat = [o.test(isl, test_id="F1a_C_h1", ajan="B1", aile="F1", varyant="a", birincil=1, kaynak="lit",
                  evren="C", h=1, cikis="kapanis", getiri_turu="ham", yon=+1)]   # yon=-1: "uzak dur"
    rj, ek = o.rejim(isl), o.ekonomi(isl, "havuz", t_stat=sat[0]["t_kume"])
    # 2) eğim testi (madde 4.7): öncülün 60 günlük z'si; kontroller varsayılan (hedef ve SMH t getirisi)
    z = o.zskor(o.hizala("2330.TW"))                     # t'de bilinen seri (hizala zaman kuralı)
    X = pd.DataFrame({k: z for k in ["TSM", "NVDA", "SMH"]})
    eg = o.egim_testi(X, getiri="ham", h=1)              # egim_bps, t_egim, p_egim, p_perm
    isl2 = o.islemler(X >= 1, h=1, test_id="LL1a_h1")    # z >= +1 olay testi; net alfa > 0 olmalı
    sat.append(o.test(isl2, egim=eg, test_id="LL1a_h1", ajan="B2", aile="LL1", varyant="a",
                      birincil=1, kaynak="lit", evren="karma", yon=+1))   # p_birincil = p_egim
    o.kaydet("B1", sat); o.kaydet("B1", isl, "islemler"); o.kaydet("B1", rj, "rejim")
    o.kaydet("B1", ek, "ekonomi")     # sonra (tek kez, en son): b, ll6, ozet = o.birlestir()
    # Notlar: 'not' Python anahtar sözcüğü -> test(..., notu="..."). LL6 satırlarına asama="kesif"/"dogrulama".
    # bilanco(kod), fomc(), maliyet(kod), ileri(kod,h,cikis), artik(kod,h) doğrudan da çağrılabilir.

ZAMAN KURALI (geleceğe bakışı önlemek için temel sözleşme)
-----------------------------------------------------------
* Sinyal D günü ABD kapanışında (16:00 ET) hesaplanır ve yalnızca o ana kadar KESİN bilinen
  veriyi kullanabilir.
* ileri_getiri(h): D kapanışından D+h kapanışına (ABD işlem günü). D gününün kendi getirisi
  İÇERMEZ. Sinyal D'de, işlem D kapanışında açılır, D+h kapanışında kapanır.
* gece_getiri: D kapanışı -> D+1 açılışı.  gun_ici_getiri: D açılışı -> D kapanışı (aynı gün).
* Tüm fiyatlar düzeltilmiş (AdjClose/Close çarpanıyla) kullanılır: AOpen, AHigh, ALow, AClose.

YABANCI PİYASALAR (hizala)
* Tayvan (.TW, ^TWII), Kore (.KS, ^KS11), Japonya (.T, ^N225), Hong Kong (.HK): yerel D günü
  seansı ET ile D günü sabahı (en geç ~04:00 ET) biter -> ABD D seansı başlamadan bilinir.
  D kapanışında sinyal olarak gecikmesiz kullanılabilir ("once").
* Avrupa (.AS, .DE, .PA, ^STOXX50E): yerel D seansı 17:30 CET = 11:30 ET'de biter -> ABD D
  kapanışından önce bilinir ("once"). Ancak ABD D gün içi getirisinin bir kısmıyla eşzamanlıdır.
* ABD kapanışından SONRA kapanan seriler ("sonra"): BTC-USD/ETH-USD (Yahoo günlük mumu UTC 24:00
  = 19:00/20:00 ET'de kapanır), vadeli işlemler CL=F GC=F HG=F NQ=F ES=F (Yahoo günlük barı
  ~17:00 ET'de kapanır), döviz JPY=X KRW=X TWD=X DX-Y.NYB (Yahoo FX günü ABD kapanışından sonra
  biter). Bunlar D kapanışı sinyali için 1 gün gecikmeli (D-1 değeri) kullanılmalıdır.
  ^VIX/^VIX9D/^VIX3M/^VVIX 16:15 ET'de kapanır: 15 dk sonra. Kesinlik için gecikme=1 ya da
  "yaklaşık eşzamanlı" diye etiketle (varsayılan: sonra).
* Tatil uyumsuzluğu: yerel piyasa D günü kapalıysa D için değer NaN olur; getiri UYDURULMAZ,
  ileri doldurma yapılmaz. ABD kapalıyken yabancı piyasanın işlem gördüğü günün getirisi
  varsayılan olarak düşer (birikimli=True ile bir sonraki ABD gününe eklenebilir).
* ^VIX 2026-05-25 ve 2026-09-07 gibi ABD tatillerinde de değer veriyor; ABD takvimi SPY'den alınır.
"""
from __future__ import annotations
import re
from pathlib import Path
import numpy as np
import pandas as pd

KOK = Path(__file__).resolve().parents[1]
VERI = KOK / "veri"

SONRA_KAPANAN = {"BTC-USD", "ETH-USD", "CL=F", "GC=F", "HG=F", "NQ=F", "ES=F", "JPY=X", "KRW=X",
                 "TWD=X", "DX-Y.NYB", "^VIX", "^VIX9D", "^VIX3M", "^VVIX"}
YABANCI_EKLER = (".TW", ".KS", ".T", ".HK", ".AS", ".DE", ".PA")
YABANCI_ENDEKS = {"^KS11", "^TWII", "^N225", "^STOXX50E"}


def dosya_adi(kod):
    return kod.replace("^", "_").replace("=", "_").replace("/", "_")


def yabanci_mi(kod):
    return kod.endswith(YABANCI_EKLER) or kod in YABANCI_ENDEKS


# ---------------------------------------------------------------- yükleme
_onbellek: dict = {}


def yukle(kod, saatlik=False):
    """Günlük: index=Date, sütunlar Open..Close, AdjClose, Volume, carpan, AOpen, AHigh, ALow, AClose.
    Saatlik: index=Datetime (America/New_York), bar başlangıcı."""
    anahtar = (kod, saatlik)
    if anahtar not in _onbellek:
        alt = "saatlik" if saatlik else "gunluk"
        yol = VERI / alt / f"{dosya_adi(kod)}.csv"
        if saatlik:
            df = pd.read_csv(yol, index_col=0)
            df.index = pd.to_datetime(df.index, utc=True).tz_convert("America/New_York")
        else:
            df = pd.read_csv(yol, index_col=0, parse_dates=True)
        _onbellek[anahtar] = df.sort_index()
    return _onbellek[anahtar].copy()


def abd_takvimi(bas=None):
    t = yukle("SPY").index
    return t[t >= pd.Timestamp(bas)] if bas else t


def panel(alan="AClose", kodlar=None, takvim=True):
    """Geniş tablo (satır=ABD işlem günü, sütun=kod). Yabancı kodlar ham yerel tarihleriyle
    eşlenir (hizalama için hizala() kullan). Eksik değer NaN kalır."""
    if kodlar is None:
        k = pd.read_csv(VERI / "kapsam_gunluk.csv", index_col=0)
        kodlar = [i for i in k.index if k.loc[i, "n"] and k.loc[i, "n"] > 0]
    s = {}
    for k in kodlar:
        try:
            s[k] = yukle(k)[alan]
        except FileNotFoundError:
            print(f"panel: {k} yok")
    p = pd.DataFrame(s)
    if takvim:
        p = p.reindex(abd_takvimi())
    return p


# ---------------------------------------------------------------- getiriler
def gunluk_getiri(c):
    """D-1 kapanışı -> D kapanışı (D'de bilinir)."""
    return c / c.shift(1) - 1


def ileri_getiri(c, h=1):
    """D kapanışı -> D+h kapanışı. D'deki sinyalin hedefi. D'nin kendi getirisini içermez."""
    return c.shift(-h) / c - 1


def gece_getiri(o, c):
    """D kapanışı -> D+1 açılışı; D satırına yazılır (ileriye dönük)."""
    return o.shift(-1) / c - 1


def gece_getiri_gecmis(o, c):
    """D-1 kapanışı -> D açılışı; D satırına yazılır (betimleyici, D açılışında bilinir)."""
    return o / c.shift(1) - 1


def gun_ici_getiri(o, c):
    """D açılışı -> D kapanışı; D satırına yazılır."""
    return c / o - 1


# ---------------------------------------------------------------- hizalama
def hizala(kod_ya_da_seri, alan="AClose", getiri=True, gecikme=None, birikimli=False, takvim=None):
    """Bir serinin değerini ABD işlem günü D'ye, D kapanışında BİLİNEN haliyle eşler.

    getiri=True: önce yerel takvimde ardışık kapanışlar arası getiri hesaplanır (tatil boşlukları
    yerel takvimde kalır), sonra ABD günlerine eşlenir. Yerel piyasa D'de kapalıysa NaN.
    gecikme: None ise koddan otomatik (SONRA_KAPANAN için 1, diğerleri 0). gecikme=1, D satırına
    yerel D-1 (son ABD gününden önceki) değeri koyar: ABD takviminde 1 satır kaydırma.
    birikimli=True: ABD'nin kapalı olduğu yerel işlem günlerinin getirisi sonraki ABD gününe
    bileşik olarak eklenir (yalnızca getiri=True ile).
    """
    if isinstance(kod_ya_da_seri, str):
        kod = kod_ya_da_seri
        s = yukle(kod)[alan]
    else:
        kod, s = getattr(kod_ya_da_seri, "name", None), kod_ya_da_seri
    s = s.dropna()
    s.index = pd.to_datetime(s.index).normalize()
    takvim = abd_takvimi() if takvim is None else takvim
    if gecikme is None:
        gecikme = 1 if kod in SONRA_KAPANAN else 0
    if getiri:
        r = s / s.shift(1) - 1
        if birikimli:
            # her yerel günü, kendisinden sonraki ilk (ya da aynı) ABD gününe ata ve bileşikle
            hedef = takvim[np.searchsorted(takvim.values, r.index.values, side="left").clip(max=len(takvim) - 1)]
            ok = hedef >= r.index
            g = (1 + r[ok]).groupby(hedef[ok]).prod() - 1
            out = g.reindex(takvim)
            # ABD günü D'de yerel piyasa kapalıysa ve öncesinde birikmiş getiri yoksa NaN kalır
        else:
            out = r.reindex(takvim)
    else:
        out = s.reindex(takvim)
    if gecikme:
        out = out.shift(gecikme)
    out.name = kod
    return out


def sonraki_yerel_seans(kod, alan="AClose", takvim=None):
    """ABD D kapanışından SONRA gelen ilk yerel seansın getirisi (ABD -> Asya yönü, takipçi).
    D satırına yazılır; D'de BİLİNMEZ, hedef değişken olarak kullanılır."""
    s = yukle(kod)[alan].dropna()
    r = s / s.shift(1) - 1
    takvim = abd_takvimi() if takvim is None else takvim
    pos = np.searchsorted(r.index.values, takvim.values, side="right")  # ilk yerel gün > D
    vals = np.where(pos < len(r), r.values[pos.clip(max=len(r) - 1)], np.nan)
    return pd.Series(vals, index=takvim, name=kod)


# ---------------------------------------------------------------- olay testi
def _nw_t(x, lags):
    """Ortalamanın Newey-West (Bartlett) t istatistiği."""
    x = np.asarray(x, float)
    x = x[~np.isnan(x)]
    n = len(x)
    if n < 3:
        return np.nan
    e = x - x.mean()
    s = e @ e / n
    for L in range(1, min(lags, n - 1) + 1):
        w = 1 - L / (lags + 1)
        s += 2 * w * (e[L:] @ e[:-L]) / n
    return x.mean() / np.sqrt(s / n) if s > 0 else np.nan


def _hac_fark_t(y, d, lags):
    """y = a + b*d regresyonunda b'nin HAC t'si (statsmodels)."""
    import statsmodels.api as sm
    X = sm.add_constant(d.astype(float))
    m = sm.OLS(y.astype(float), X).fit(cov_type="HAC", cov_kwds={"maxlags": max(lags, 1)})
    return float(m.params.iloc[1]), float(m.tvalues.iloc[1])


VARSAYILAN_DONEMLER = {"2010-2014": ("2010", "2014"), "2015-2019": ("2015", "2019"),
                       "2020-2022": ("2020", "2022"), "2023-2025": ("2023", "2025"),
                       "2026": ("2026", "2026")}


def bindirmeyi_ele(sinyal, h):
    """Bir işlem açıldıktan sonra h gün boyunca yeni sinyali yok sayar (tek pozisyon)."""
    s = sinyal.fillna(False).astype(bool).values
    out = np.zeros(len(s), bool)
    bekle = -1
    for i, v in enumerate(s):
        if v and i > bekle:
            out[i] = True
            bekle = i + h - 1
    return pd.Series(out, index=sinyal.index)


def olay_testi(sinyal, ileri, h=1, maliyet_bps=0.0, bindirme_yok=False, n_boot=2000,
               donemler=None, seed=0, en_iyi_cikar=10):
    """sinyal: D günü kapanışında bilinen bool seri. ileri: aynı aracın D->D+h getirisi
    (ileri_getiri(c, h)). maliyet_bps: gidiş-dönüş toplam işlem maliyeti (baz puan).

    Dönüş: dict (n, ortalama, medyan, isabet, nw_t, kosulsuz_ort, fazla, fazla_hac_t, boot_p,
    en_iyi10_cikinca_ort, donemler{ad: (n, ort)}). Getiriler oran (0.01 = %1).
    Boot p: aynı sayıda rastgele giriş günü (ileri'si dolu günlerden, iadesiz) ile ortalamanın
    gözlenen işlem ortalamasından büyük ya da eşit olma oranı (tek yönlü, uzun pozisyon)."""
    df = pd.concat({"s": sinyal.astype("boolean"), "r": ileri}, axis=1).dropna()
    df["s"] = df["s"].astype(bool)
    if bindirme_yok:
        df["s"] = bindirmeyi_ele(df["s"], h)
    m = maliyet_bps / 1e4
    tr = df.loc[df["s"], "r"] - m
    n = len(tr)
    out = dict(n=n, h=h, maliyet_bps=maliyet_bps, bindirme_yok=bindirme_yok)
    if n == 0:
        return out
    kos = df["r"].mean()
    lags = max(h - 1, 0) if bindirme_yok else h  # örtüşen getiride h-1 gecikme yeter; pay bırakıldı
    out.update(ortalama=tr.mean(), medyan=tr.median(), isabet=(tr > 0).mean(),
               nw_t=_nw_t(tr.values, lags), kosulsuz_ort=kos, fazla=tr.mean() + m - kos)
    if 3 <= n < len(df):
        b, t = _hac_fark_t(df["r"], df["s"], h)
        out["fark_sinyal_disi"] = b
        out["fazla_hac_t"] = t
    rng = np.random.default_rng(seed)
    pool = df["r"].values - m
    if n < len(pool):
        idx = np.argsort(rng.random((n_boot, len(pool))), axis=1)[:, :n] if len(pool) * n_boot < 4e7 \
            else np.stack([rng.choice(len(pool), n, replace=False) for _ in range(n_boot)])
        bm = pool[idx].mean(axis=1)
        out["boot_p"] = (np.sum(bm >= tr.mean()) + 1) / (n_boot + 1)
    if n > en_iyi_cikar:
        out[f"en_iyi{en_iyi_cikar}_cikinca_ort"] = tr.sort_values().iloc[:-en_iyi_cikar].mean()
    don = {}
    for ad, (a, b) in (donemler or VARSAYILAN_DONEMLER).items():
        x = tr.loc[a:b]
        don[ad] = (len(x), x.mean() if len(x) else np.nan)
    out["donemler"] = don
    return out


def olay_tablosu(sonuclar: dict) -> pd.DataFrame:
    """{ad: olay_testi çıktısı} -> düz tablo (dönemler ayrı sütunlar)."""
    satir = {}
    for ad, r in sonuclar.items():
        r = dict(r)
        for d, (k, v) in r.pop("donemler", {}).items():
            r[f"n_{d}"], r[f"ort_{d}"] = k, v
        satir[ad] = r
    return pd.DataFrame(satir).T


# ---------------------------------------------------------------- çoklu test
def bh_fdr(p, q=0.10):
    """Benjamini-Hochberg. Dönüş: (düzeltilmiş p dizisi, q düzeyinde red maskesi). NaN korunur."""
    p = np.asarray(p, float)
    ok = ~np.isnan(p)
    pv = p[ok]
    m = len(pv)
    adj = np.full_like(p, np.nan)
    rej = np.zeros(len(p), bool)
    if m == 0:
        return adj, rej
    o = np.argsort(pv)
    ranked = pv[o] * m / np.arange(1, m + 1)
    ranked = np.minimum.accumulate(ranked[::-1])[::-1].clip(max=1)
    a = np.empty(m)
    a[o] = ranked
    adj[ok] = a
    rej[ok] = a <= q
    return adj, rej


# ---------------------------------------------------------------- saatlik
def saatlik_gunluk_ozet(kod):
    """Saatlik barlardan gün başına: n_bar, son_bar saati, p1530 (15:30 barının açılışı =
    15:30 fiyatı), c_saat (son bar kapanışı), tam_gun (7 bar ve son bar 15:30).
    Yarım günler (Yahoo'da son bar 11:30, eksik) ve eksik barlı günler (ör. 2026-01-30,
    çoğu kodda 3 bar) tam_gun=False olur; p1530 yalnızca tam günlerde doludur (NaN, uydurma yok)."""
    h = yukle(kod, saatlik=True)
    g = h.groupby(h.index.normalize().tz_localize(None))
    o_ = pd.DataFrame({"n_bar": g.size(),
                       "son_bar": g.apply(lambda x: x.index[-1].strftime("%H:%M")),
                       "p1530": g["Open"].last(), "c_saat": g["Close"].last()})
    o_["tam_gun"] = (o_["n_bar"] == 7) & (o_["son_bar"] == "15:30")
    o_.loc[~o_["tam_gun"], "p1530"] = np.nan
    return o_


# =====================================================================================
# ADIM 0 EKLERİ (PROTOKOL 13.2 imzaları). Yukarıdaki işlevler değişmedi; aşağısı ektir.
# Birimler: getiriler bps (1 bps = 0,01 %). Takvim: SPY işlem günleri (ABD), 2010-01-04 -> 2026-11-20.
# =====================================================================================
import math
from scipy import stats as _st

T_EVREN = ["SMH", "SOXX", "QQQ", "XLK", "SPY", "IWM"]
KALDIRAC = {"SOXL": 3, "SOXS": -3, "TQQQ": 3, "SQQQ": -3, "USD": 2, "TECL": 3, "TECS": -3,
            "NVDL": 2, "NVDX": 2, "NVDD": -1, "NVDQ": -2, "AMDL": 2, "MUU": 2, "TSLL": 2,
            "PLTU": 2, "SMCX": 2}
TEK_HISSE_KALDIRAC = {"NVDL", "NVDX", "NVDD", "NVDQ", "AMDL", "MUU", "TSLL", "PLTU", "SMCX"}
M1_KODLAR = set("NVDA AMD AVGO TSM MU MSFT GOOGL META AMZN AAPL TSLA SOXL SOXS TQQQ SQQQ".split()) | set(T_EVREN)
YENI_EK = ["DRAM"]          # hedef ETF (bellek), YENİ evrenine eklendi (kaldıraçsız, 2026 başlangıçlı)
DONEMLER = {"P1": ("2010-01-01", "2019-12-31"), "P2": ("2020-01-01", "2022-12-31"),
            "P3": ("2023-01-01", "2026-11-20")}
SON_GUN = pd.Timestamp("2026-11-20")
SON12_BAS = pd.Timestamp("2025-11-21")
SONUC = VERI / "sonuc"
SONUC_SUTUN = ("test_id ajan aile varyant birincil kaynak evren h cikis getiri_turu n_islem n_gun n_arac "
               "ilk_tarih son_tarih ort_bps kosulsuz_bps alfa_bps se_bps t_kume p_kume egim_bps t_egim "
               "p_birincil t_takvim p_perm mde_bps maliyet_bps alfa_net_bps alfa_net_2x_bps mutlak_net_bps "
               "medyan_bps isabet alfa_ust1suz_bps alfa_5gunsuz_bps alfa_h2_bps alfa_h3_bps alfa_acilis_bps "
               "alfa_P1 t_P1 n_P1 alfa_P2 t_P2 n_P2 alfa_P3 t_P3 n_P3 alfa_son12 n_son12 alfa_temiz q_bh "
               "etiket not").split()


def TK():
    t = abd_takvimi()
    return t[t <= SON_GUN]


def _donem_no(idx):
    """0=P1, 1=P2, 2=P3 (tarih dizisi için)."""
    y = pd.DatetimeIndex(idx)
    return np.where(y < "2020-01-01", 0, np.where(y < "2023-01-01", 1, 2))


# ---------------------------------------------------------------- fiyat / evren / maliyet
_bol = None


def _bolunmeler():
    global _bol
    if _bol is None:
        yol = VERI / "bolunme.csv"
        _bol = pd.read_csv(yol, parse_dates=["tarih"]) if yol.exists() else pd.DataFrame(columns=["kod", "tarih", "oran"])
    return _bol


def fiyat(kod):
    """Günlük fiyat tablosu (kendi takvimi): AOpen AHigh ALow AClose (düzeltilmiş), Open High Low Close
    (Yahoo: bölünmeye göre düzeltilmiş, temettüye göre düzeltilmemiş), Volume, ciro (= Close*Volume, $;
    bölünmeden bağımsız), gercek_fiyat (o günkü bölünmemiş fiyat = Close * sonraki bölünme oranları
    çarpımı; madde 2.2'deki 3 $ eşiği için), bozuk (madde 2.1)."""
    k = ("fiyat", kod)
    if k not in _onbellek:
        d = yukle(kod)
        b = _bolunmeler()
        b = b[b.kod == kod]
        kat = pd.Series(1.0, index=d.index)
        for t, r in zip(b.tarih, b.oran):
            kat[d.index < t] *= r
        d["ciro"] = d["Close"] * d["Volume"]
        d["gercek_fiyat"] = d["Close"] * kat
        d["bozuk"] = ((d["High"] < d[["Open", "Close"]].max(axis=1)) | (d["Low"] > d[["Open", "Close"]].min(axis=1))
                      | (d["High"] == d["Low"]))
        _onbellek[k] = d
    return _onbellek[k].copy()


def evren(ad):
    """T, Ç (ya da C), YENİ (ya da YENI), ARAÇ (ya da ARAC). Madde 2.5. Ç: indir.HEDEF içinde ilk verisi
    <= 2016-01-01 olan; YENİ: kalan hedefler + DRAM; ARAÇ: kaldıraçlı/ters ETF'ler."""
    import sys as _s
    _s.path.insert(0, str(Path(__file__).parent))
    from indir import HEDEF
    ad = ad.upper().replace("Ç", "C").replace("İ", "I").replace("Ç", "C")
    if ad == "T":
        return list(T_EVREN)
    if ad in ("ARAC", "ARAÇ"):
        return list(KALDIRAC)
    k = pd.read_csv(VERI / "kapsam_gunluk.csv", index_col=0)
    ilk = pd.to_datetime(k["ilk"], errors="coerce")
    c = [h for h in HEDEF if h in ilk.index and pd.notna(ilk[h]) and ilk[h] <= pd.Timestamp("2016-01-01")]
    if ad == "C":
        return c
    if ad == "YENI":
        return [h for h in HEDEF if h not in c and h in ilk.index and pd.notna(ilk[h])] + YENI_EK
    raise ValueError(ad)


def maliyet(kod):
    """Gidiş-dönüş bps (madde 8.2): M1=10, M2=20 (son 250 gün medyan ciro >= 300 mn $), M3=40."""
    if kod in M1_KODLAR:
        return 10.0
    if kod in TEK_HISSE_KALDIRAC:
        return 40.0
    c = fiyat(kod)["ciro"].loc[:SON_GUN].tail(250).median()
    return 20.0 if c >= 300e6 else 40.0


# ---------------------------------------------------------------- matrisler (önbellekli)
def _mat(alan, kodlar):
    k = ("mat", alan, tuple(kodlar))
    if k not in _onbellek:
        t = TK()
        _onbellek[k] = pd.DataFrame({c: fiyat(c)[alan] for c in kodlar}).reindex(t)
    return _onbellek[k]


def _ileri_ham(kodlar, h, cikis):
    """D kapanışı -> D+h kapanışı (cikis='kapanis') ya da D+h açılışı ('acilis'), bps; kendi takviminde
    hesaplanıp ABD takvimine eşlenir."""
    k = ("ileri", tuple(kodlar), h, cikis)
    if k not in _onbellek:
        t = TK()
        s = {}
        for c in kodlar:
            d = fiyat(c).dropna(subset=["AClose"])
            son = d["AOpen"] if cikis == "acilis" else d["AClose"]
            s[c] = (son.shift(-h) / d["AClose"] - 1) * 1e4
        _onbellek[k] = pd.DataFrame(s).reindex(t)
    return _onbellek[k]


def _gunluk_ham(kodlar):
    k = ("gunluk", tuple(kodlar))
    if k not in _onbellek:
        t = TK()
        _onbellek[k] = pd.DataFrame({c: gunluk_getiri(fiyat(c)["AClose"].dropna()) * 1e4 for c in kodlar}).reindex(t)
    return _onbellek[k]


def _beta(kodlar):
    """beta_t: t dahil son 250 gün (en az 120) günlük getirilerle SMH'ye göre."""
    k = ("beta", tuple(kodlar))
    if k not in _onbellek:
        r = _gunluk_ham(kodlar)
        m = _gunluk_ham(["SMH"])["SMH"]
        b = {}
        for c in kodlar:
            ok = r[c].notna() & m.notna()
            x, y = m.where(ok), r[c].where(ok)
            cov = x.rolling(250, min_periods=120).cov(y)
            var = x.rolling(250, min_periods=120).var()
            b[c] = cov / var
        _onbellek[k] = pd.DataFrame(b)
    return _onbellek[k]


def _ileri_tur(kodlar, h, cikis, tur):
    f = _ileri_ham(kodlar, h, cikis)
    if tur == "ham":
        return f
    k = ("ileri_art", tuple(kodlar), h, cikis)
    if k not in _onbellek:
        fs = _ileri_ham(["SMH"], h, cikis)["SMH"]
        _onbellek[k] = f - _beta(kodlar).mul(fs, axis=0)
    return _onbellek[k]


def _gunluk_tur(kodlar, tur):
    r = _gunluk_ham(kodlar)
    if tur == "ham":
        return r
    k = ("gunluk_art", tuple(kodlar))
    if k not in _onbellek:
        m = _gunluk_ham(["SMH"])["SMH"]
        _onbellek[k] = r - _beta(kodlar).shift(1).mul(m, axis=0)
    return _onbellek[k]


def _donem_ort(X):
    """Her sütun için dönem (P1/P2/P3) ortalaması, satırlara yayılmış (T x N)."""
    d = _donem_no(X.index)
    out = np.full(X.shape, np.nan)
    v = X.values
    for p in range(3):
        m = d == p
        if m.any():
            with np.errstate(all="ignore"):
                out[m] = np.nanmean(v[m], axis=0)
    return out


def _beklenen(kodlar, L, cikis, tur):
    """Araç x dönem sabit etkisi: kapanış çıkışında günlük ortalama x L (madde 4.1); açılış çıkışında
    aynı ileri serinin araç x dönem ortalaması."""
    k = ("bek", tuple(kodlar), L, cikis, tur)
    if k not in _onbellek:
        if cikis == "kapanis":
            _onbellek[k] = _donem_ort(_gunluk_tur(kodlar, tur)) * L
        else:
            _onbellek[k] = _donem_ort(_ileri_tur(kodlar, L, cikis, tur))
    return _onbellek[k]


def ileri(kod, h=1, cikis="kapanis"):
    """Ham ileri getiri, bps, ABD takviminde. kod str ya da liste (liste -> DataFrame)."""
    if isinstance(kod, str):
        return _ileri_ham([kod], h, cikis)[kod].copy()
    return _ileri_ham(list(kod), h, cikis).copy()


def artik(kod, h=1, cikis="kapanis"):
    """İleri getiri - beta_t x SMH ileri getirisi (madde 1.4), bps."""
    if isinstance(kod, str):
        return _ileri_tur([kod], h, cikis, "artik")[kod].copy()
    return _ileri_tur(list(kod), h, cikis, "artik").copy()


def uygun(kodlar):
    """Madde 2.1-2.2: bozuk satır değil, gerçek fiyat >= 3 $, 20 gün medyan ciro >= 20 mn $,
    t'den önce >= 250 geçerli kapanış. T x N bool."""
    k = ("uygun", tuple(kodlar))
    if k not in _onbellek:
        t = TK()
        s = {}
        for c in kodlar:
            d = fiyat(c)
            gec = d["AClose"].notna().cumsum().shift(1).fillna(0) >= 250
            s[c] = (~d["bozuk"]) & (d["gercek_fiyat"] >= 3) & (d["ciro"].rolling(20, min_periods=20).median() >= 20e6) & gec
        _onbellek[k] = pd.DataFrame(s).reindex(t).fillna(False).astype(bool)
    return _onbellek[k]


# ---------------------------------------------------------------- bilanço / FOMC
def bilanco(kod):
    """Bilanço duyuruları ve tepki günleri (madde 2.4). Sütunlar: duyuru, saat, zaman, tepki, A
    (duyurudan önceki son kapanış günü = tepki - 1 işlem günü), yontem ('saat' ya da 'hacim'),
    tepki_hacim (hacim kuralıyla seçilecek gün; tanı). Yalnız 2010-01-04 -> SON_GUN arası, işlem
    günü bulunanlar. Saat yoksa iki adaydan (duyuru günü / ertesi işlem günü) göreli hacmi
    (hacim / önceki 20 gün medyanı) büyük olan."""
    k = ("bilanco", kod)
    if k in _onbellek:
        return _onbellek[k].copy()
    yol = VERI / "bilanco" / f"{dosya_adi(kod)}.csv"
    bos = pd.DataFrame(columns=["duyuru", "saat", "zaman", "tepki", "A", "yontem", "tepki_hacim"])
    if not yol.exists():
        _onbellek[k] = bos
        return bos.copy()
    b = pd.read_csv(yol, parse_dates=["tarih"])
    t = TK()
    d = fiyat(kod)
    gv = (d["Volume"] / d["Volume"].rolling(20, min_periods=10).median().shift(1)).reindex(t)
    rows = []
    for _, r in b.iterrows():
        if r.tarih < t[0] or r.tarih > SON_GUN:
            continue
        i0 = t.searchsorted(r.tarih)          # duyuru günü ya da sonraki ilk işlem günü
        if i0 >= len(t):
            continue
        islem_gunu = t[i0] == r.tarih
        i1 = min(i0 + 1, len(t) - 1)
        # hacim kuralı
        if islem_gunu:
            a0, a1 = gv.iloc[i0], gv.iloc[i1]
            ih = i1 if (pd.notna(a1) and (pd.isna(a0) or a1 > a0)) else i0
        else:
            ih = i0
        if r.zaman == "sonra":
            it, yon = (i1 if islem_gunu else i0), "saat"
        elif r.zaman in ("once", "seans"):
            it, yon = i0, "saat"
        else:
            it, yon = ih, "hacim"
        rows.append(dict(duyuru=r.tarih, saat=r.saat, zaman=r.zaman, tepki=t[it],
                         A=t[it - 1] if it > 0 else pd.NaT, yontem=yon, tepki_hacim=t[ih]))
    out = pd.DataFrame(rows) if rows else bos
    _onbellek[k] = out
    return out.copy()


def _bilanco_maske(kodlar, h):
    """T x N: [t, t+h] aralığında bilanço tepki günü var mı."""
    k = ("bmaske", tuple(kodlar), h)
    if k not in _onbellek:
        t = TK()
        m = np.zeros((len(t), len(kodlar)), bool)
        for j, c in enumerate(kodlar):
            p = t.get_indexer(pd.DatetimeIndex(bilanco(c)["tepki"]))
            p = p[p >= 0]
            for off in range(h + 1):
                q = p - off
                m[q[q >= 0], j] = True
        _onbellek[k] = m
    return _onbellek[k]


def fomc():
    """Planlı FOMC karar günleri (DatetimeIndex), veri/fomc.csv; olağanüstü toplantılar hariç."""
    return pd.DatetimeIndex(pd.read_csv(VERI / "fomc.csv", parse_dates=["karar_gunu"])["karar_gunu"])


# ---------------------------------------------------------------- işlemler
def _tek_poz(S, h, cikis_off):
    """S: T x N bool (filtrelenmiş sinyal). cikis_off: None ya da T x N int (girişten çıkışa gün).
    Dönüş: giriş maskesi ve tutma süresi (T x N int). Açık pozisyon varken gelen sinyal atlanır."""
    if cikis_off is None and h == 1:
        return S, np.where(S, 1, 0)
    G = np.zeros_like(S)
    L = np.zeros(S.shape, int)
    for j in range(S.shape[1]):
        bekle = -1
        for i in np.flatnonzero(S[:, j]):
            if i > bekle:
                g = h if cikis_off is None else int(cikis_off[i, j])
                G[i, j] = True
                L[i, j] = g
                bekle = i + g - 1
    return G, L


def _cikis_offset(cikis_sinyal, h, T):
    """cikis_sinyal (T x N bool, kapanışta çıkış koşulu): girişten sonraki ilk j in 1..h; yoksa h."""
    c = cikis_sinyal.values.astype(bool)
    off = np.full(c.shape, h)
    for j in range(h, 0, -1):
        sh = np.zeros_like(c)
        sh[:-j] = c[j:]
        off = np.where(sh, j, off)
    return off


def islemler(sinyal, h=1, cikis="kapanis", getiri="ham", bilanco_at=False, cikis_sinyal=None,
             guc=None, test_id=None, filtre=True, yon=1):
    """sinyal: DataFrame (tarih x kod, bool; t kapanışında BİLİNEN) ya da adı kod olan bool Series.
    h: tutma (gün); cikis_sinyal verilirse h üst sınırdır (F2). getiri: 'ham' | 'artik'.
    bilanco_at: tepki günü [t, t+h] içindeyse sinyal atılır (madde 2.4). filtre: madde 2.1-2.2.
    guc: aynı biçimde sinyal gücü (ekonomi() havuzunda 'en uç 3' seçimi için).
    Araç başına tek pozisyon (madde 1.3). Dönüş: DataFrame test_id, kod, giris, cikis, gun, getiri_bps
    (seçilen türde), ham_bps, alfa_bps, alfa_ham_bps, maliyet_bps, guc; attrs içinde permütasyon ve
    ikincil sütunlar için gerekenler."""
    if isinstance(sinyal, pd.Series):
        sinyal = sinyal.to_frame(sinyal.name)
    kodlar = list(sinyal.columns)
    t = TK()
    S0 = sinyal.reindex(t).fillna(False).astype(bool).values
    hmax = h
    E = uygun(kodlar).values if filtre else np.ones(S0.shape, bool)
    if bilanco_at:
        E = E & ~_bilanco_maske(kodlar, hmax)
    off = None if cikis_sinyal is None else _cikis_offset(cikis_sinyal.reindex(t)[kodlar].fillna(False), h, len(t))
    F = {L: _ileri_tur(kodlar, L, cikis, getiri).values for L in range(1, hmax + 1)}
    Fh = {L: _ileri_ham(kodlar, L, cikis).values for L in range(1, hmax + 1)}
    B = {L: _beklenen(kodlar, L, cikis, getiri) for L in range(1, hmax + 1)}
    Bh = {L: _beklenen(kodlar, L, cikis, "ham") for L in range(1, hmax + 1)}
    gecerli = np.isfinite(F[hmax]) & np.isfinite(B[hmax])
    S = S0 & E & gecerli
    G, Lm = _tek_poz(S, h, off)
    ii, jj = np.nonzero(G)
    ll = Lm[ii, jj]
    def pick(D):
        v = np.full(len(ii), np.nan)
        for l in np.unique(ll):
            m = ll == l
            v[m] = D[l][ii[m], jj[m]]
        return v
    g, gh = pick(F), pick(Fh)
    bek, bekh = pick(B), pick(Bh)
    mk = ("maliyetler", tuple(kodlar))
    if mk not in _onbellek:
        _onbellek[mk] = np.array([maliyet(c) for c in kodlar])
    mal = _onbellek[mk]
    out = pd.DataFrame({"test_id": test_id, "kod": np.array(kodlar, object)[jj], "giris": t[ii],
                        "cikis": t[np.minimum(ii + ll, len(t) - 1)], "gun": ll, "getiri_bps": g,
                        "ham_bps": gh, "alfa_bps": g - bek, "alfa_ham_bps": gh - bekh,
                        "maliyet_bps": mal[jj]})
    if guc is not None:
        gv = guc.reindex(t)[kodlar].values
        out["guc"] = gv[ii, jj]
    out = out.sort_values(["giris", "kod"]).reset_index(drop=True)
    anahtar = f"ctx{len(_BAGLAM)}"
    out.attrs = {"ctx": anahtar}
    _BAGLAM[anahtar] = dict(sinyal=sinyal, S0=S0, E=E, h=h, cikis=cikis, getiri=getiri, bilanco_at=bilanco_at,
                     cikis_sinyal=cikis_sinyal, off=off, kodlar=kodlar, filtre=filtre, yon=yon, test_id=test_id)
    return out


_BAGLAM: dict = {}


def _ctx(isl):
    """islemler() çıktısının bağlamı (sinyal matrisi, filtreler...). CSV'den okunan işlemlerde yoktur."""
    return _BAGLAM.get(isl.attrs.get("ctx"), {})


def _perm_alfa(attrs, kayd):
    """Sinyal matrisini bütün araçlarda aynı k gün dairesel kaydırıp alfa ortalamasını yeniden hesaplar."""
    kodlar, h, cikis, getiri, off = attrs["kodlar"], attrs["h"], attrs["cikis"], attrs["getiri"], attrs["off"]
    A = {L: _ileri_tur(kodlar, L, cikis, getiri).values - _beklenen(kodlar, L, cikis, getiri) for L in range(1, h + 1)}
    gec = np.isfinite(A[h])
    A0 = {L: np.nan_to_num(A[L]) for L in A}
    E = attrs["E"] & gec
    out = np.full(len(kayd), np.nan)
    for n, k in enumerate(kayd):
        S = np.roll(attrs["S0"], int(k), axis=0) & E
        if off is None and h == 1:
            c = S.sum()
            out[n] = (A0[1] * S).sum() / c if c else np.nan
        else:
            G, L = _tek_poz(S, h, off)
            if not G.any():
                continue
            ii, jj = np.nonzero(G)
            ll = L[ii, jj]
            s = 0.0
            for l in np.unique(ll):
                m = ll == l
                s += A0[l][ii[m], jj[m]].sum()
            out[n] = s / len(ii)
    return out


def _kaydirmalar(n, T, seed=0, en_az=60):
    rng = np.random.default_rng(seed)
    return rng.integers(en_az, T - en_az, size=n)


# ---------------------------------------------------------------- istatistik
def _kume_t(x, g):
    """Ortalama, kümeli se, t, p (iki yönlü, sd = G-1). g: küme etiketleri."""
    x = np.asarray(x, float)
    n = len(x)
    if n < 2:
        return (x.mean() if n else np.nan), np.nan, np.nan, np.nan
    kod, inv = np.unique(np.asarray(g), return_inverse=True)
    G = len(kod)
    e = x - x.mean()
    sg = np.bincount(inv, weights=e)
    if G < 2:
        return x.mean(), np.nan, np.nan, np.nan
    se = math.sqrt(G / (G - 1) * (sg @ sg)) / n
    tt = x.mean() / se if se > 0 else np.nan
    p = 2 * _st.t.sf(abs(tt), G - 1) if np.isfinite(tt) else np.nan
    return x.mean(), se, tt, p


def _kume_etiket(giris, h):
    giris = pd.DatetimeIndex(giris)
    return giris.values if h == 1 else giris.to_period("W-FRI").astype(str).values


def _takvim_serisi(isl):
    """Açık pozisyonların günlük fazla getirilerinin eşit ağırlıklı serisi (madde 4.3)."""
    a = _ctx(isl)
    kodlar, getiri = a["kodlar"], a["getiri"]
    t = TK()
    R = _gunluk_tur(kodlar, getiri).values - _beklenen(kodlar, 1, "kapanis", getiri)
    jmap = {c: j for j, c in enumerate(kodlar)}
    ii = t.get_indexer(pd.DatetimeIndex(isl["giris"]))
    jj = isl["kod"].map(jmap).values
    ll = isl["gun"].values
    top = np.zeros(len(t))
    say = np.zeros(len(t))
    for L in range(1, int(ll.max()) + 1 if len(ll) else 1):
        m = ll >= L
        d = ii[m] + L
        ok = d < len(t)
        v = R[d[ok], jj[m][ok]]
        f = np.isfinite(v)
        np.add.at(top, d[ok][f], v[f])
        np.add.at(say, d[ok][f], 1)
    s = pd.Series(np.where(say > 0, top / np.maximum(say, 1), np.nan), index=t)
    return s.dropna()


def _alt_ozet(isl, h, maske=None):
    x = isl if maske is None else isl[maske]
    if len(x) == 0:
        return np.nan, np.nan, 0
    m, se, tt, p = _kume_t(x["alfa_bps"].values, _kume_etiket(x["giris"], h))
    return m, tt, len(x)


def _ikincil(isl, h, cikis):
    a = _ctx(isl)
    try:
        y = islemler(a["sinyal"], h=h, cikis=cikis, getiri=a["getiri"], bilanco_at=a["bilanco_at"],
                     filtre=a["filtre"])
        return y["alfa_bps"].mean() if len(y) else np.nan
    except Exception as e:  # ikincil sütun birincil sonucu bozmasın
        print("ikincil hata:", e)
        return np.nan


def test(islemler_, egim=None, perm=500, alfa_temiz=np.nan, seed=0, ikincil=True, **kimlik):
    """Madde 4 ve 13.4. islemler_: islemler() çıktısı. egim: egim_testi() çıktısı (eğim testlerinde;
    p_birincil ve p_perm eğimden alınır). kimlik: test_id, ajan, aile, varyant, birincil (1/0),
    kaynak (lit/turev), evren, h, cikis, getiri_turu, yon (+1 al, -1 uzak dur), not ...
    Dönüş: _sonuc.csv satırı (dict)."""
    isl = islemler_
    a = _ctx(isl)
    h = int(kimlik.get("h", a.get("h", 1)))
    yon = int(kimlik.get("yon", a.get("yon", 1)))
    r = {c: np.nan for c in SONUC_SUTUN}
    r.update(dict(h=h, cikis=a.get("cikis", "kapanis"), getiri_turu=a.get("getiri", "ham"), yon=yon,
                  birincil=1, not_=""))
    r.update(kimlik)
    n = len(isl)
    r["n_islem"] = n
    if n == 0:
        r["etiket"] = None
        return r
    x = isl["alfa_bps"].values
    g = _kume_etiket(isl["giris"], h)
    m, se, tt, p = _kume_t(x, g)
    r.update(n_gun=isl["giris"].nunique(), n_arac=isl["kod"].nunique(),
             ilk_tarih=str(isl["giris"].min().date()), son_tarih=str(isl["giris"].max().date()),
             ort_bps=isl["getiri_bps"].mean(), kosulsuz_bps=(isl["getiri_bps"] - isl["alfa_bps"]).mean(),
             alfa_bps=m, se_bps=se, t_kume=tt, p_kume=p, mde_bps=2.84 * se if np.isfinite(se) else np.nan,
             alfa_ham_bps=isl["alfa_ham_bps"].mean(), medyan_bps=isl["getiri_bps"].median(),
             isabet=(isl["getiri_bps"] > 0).mean())
    ts = _takvim_serisi(isl)
    r["t_takvim"] = _nw_t(ts.values, 5)
    r["n_takvim_gun"] = len(ts)
    mal = isl["maliyet_bps"].mean()
    r.update(maliyet_bps=mal, alfa_net_bps=m - mal, alfa_net_2x_bps=m - 2 * mal,
             mutlak_net_bps=r["ort_bps"] - mal)
    # en iyi %1 (en az 10) işlem ve en iyi 5 giriş günü çıkarılmış alfa (yon'a göre "en iyi")
    k = max(10, math.ceil(0.01 * n))
    srt = np.sort(yon * x)
    r["alfa_ust1suz_bps"] = yon * srt[:-k].mean() if n > k else np.nan
    gun = isl.groupby("giris")["alfa_bps"].sum() * yon
    at = set(gun.nlargest(5).index)
    kalan = isl[~isl["giris"].isin(at)]
    r["alfa_5gunsuz_bps"] = kalan["alfa_bps"].mean() if len(kalan) else np.nan
    # dönemler
    dn = _donem_no(isl["giris"])
    for p_, ad in enumerate(["P1", "P2", "P3"]):
        mm, t_, nn = _alt_ozet(isl, h, dn == p_)
        r[f"alfa_{ad}"], r[f"t_{ad}"], r[f"n_{ad}"] = mm, t_, nn
    mm, t_, nn = _alt_ozet(isl, h, isl["giris"] >= SON12_BAS)
    r["alfa_son12"], r["t_son12"], r["n_son12"] = mm, t_, nn
    # permütasyon
    if perm:
        kay = _kaydirmalar(perm, len(TK()), seed)
        pa = _perm_alfa(a, kay)
        pa = pa[np.isfinite(pa)]
        r["p_perm"] = (np.sum(np.abs(pa) >= abs(m)) + 1) / (len(pa) + 1)
        r["perm_ort_bps"], r["perm_sd_bps"] = pa.mean(), pa.std()
    # ikincil
    if ikincil:
        r["alfa_h2_bps"] = _ikincil(isl, 2, "kapanis")
        r["alfa_h3_bps"] = _ikincil(isl, 3, "kapanis")
        r["alfa_acilis_bps"] = _ikincil(isl, 1, "acilis")
    r["alfa_temiz"] = alfa_temiz
    if egim is not None:
        r["p_perm_olay"] = r.get("p_perm")
        r.update(egim_bps=egim["egim_bps"], t_egim=egim["t_egim"], p_birincil=egim["p_egim"],
                 p_perm=egim.get("p_perm", np.nan), se_egim_bps=egim["se_egim_bps"], n_gozlem=egim["n_gozlem"])
    else:
        r["p_birincil"] = p
    r["not"] = kimlik.get("not", kimlik.get("notu", ""))
    # fazla iyi sonuç bayrağı (görev kuralı): |t| > 5 ya da |alfa| > 100 bps -> geleceğe bakış / veri hatası ara
    tb = r["t_egim"] if egim is not None else tt
    r["supheli"] = bool((np.isfinite(tb) and abs(tb) > 5) or abs(m) > 100)
    if r["supheli"]:
        r["not"] = (str(r["not"]) + "; ŞÜPHELİ: |t|>5 ya da |alfa|>100 bps, geleceğe bakış/veri hatası ara").strip("; ")
    r.pop("notu", None)
    r.pop("not_", None)
    return r


# ---------------------------------------------------------------- eğim testi (madde 4.7)
def zskor(X, pencere=60):
    """t değerinin t-1'e kadarki 'pencere' günlük ortalama ve std'ye göre z-skoru (t'de bilinir)."""
    mu = X.rolling(pencere, min_periods=pencere).mean().shift(1)
    sd = X.rolling(pencere, min_periods=pencere).std().shift(1)
    return (X - mu) / sd


def _icten(V, grp, ngrp):
    """Grup içi ortalamadan arındırma (araç x dönem sabit etkisi). V: n x k."""
    cnt = np.bincount(grp, minlength=ngrp).astype(float)
    out = np.empty_like(V)
    for c in range(V.shape[1]):
        s = np.bincount(grp, weights=V[:, c], minlength=ngrp)
        out[:, c] = V[:, c] - (s / np.maximum(cnt, 1))[grp]
    return out


def _ols_kume(y, X, kume):
    XtX = X.T @ X
    try:
        inv = np.linalg.inv(XtX)
    except np.linalg.LinAlgError:
        inv = np.linalg.pinv(XtX)
    b = inv @ (X.T @ y)
    e = y - X @ b
    _, ki = np.unique(kume, return_inverse=True)
    G = ki.max() + 1
    S = np.zeros((G, X.shape[1]))
    np.add.at(S, ki, X * e[:, None])
    n, k = X.shape
    V = inv @ (S.T @ S) @ inv * (G / (G - 1)) * ((n - 1) / (n - k))
    return b, np.sqrt(np.diag(V)), G


def egim_testi(x, getiri="ham", h=1, cikis="kapanis", kontroller=None, filtre=True, bilanco_at=False,
               perm=500, seed=0, y=None):
    """Panel eğimi: y(t->t+h, bps) = b * x_t + c * kontroller + araç x dönem sabit etkisi.
    x: DataFrame tarih x kod (hedef araçlar), öncül değeri (genelde zskor(...)); t'de bilinmeli.
    kontroller: None -> protokol varsayılanı {hedefin t getirisi, SMH'nin t getirisi} (bps);
    ya da {ad: DataFrame (tarih x kod) ya da Series (tarihe göre, bütün kodlara yayılır)}.
    SE tarihe (h=1) ya da haftaya (h>=2) göre kümeli; p_perm: x bütün araçlarda aynı k ile kaydırılır.
    Dönüş: dict egim_bps (x'in 1 birimi başına bps), se_egim_bps, t_egim, p_egim, p_perm, n_gozlem, n_tarih."""
    t = TK()
    kodlar = list(x.columns)
    X0 = x.reindex(t)[kodlar].values.astype(float)
    Y = (y.reindex(t)[kodlar].values if y is not None else _ileri_tur(kodlar, h, cikis, getiri).values)
    if kontroller is None:
        kontroller = {"r_hedef": _gunluk_ham(kodlar), "r_smh": _gunluk_ham(["SMH"])["SMH"]}
    C = []
    for ad, v in kontroller.items():
        if isinstance(v, pd.Series):
            v = pd.DataFrame(np.repeat(v.reindex(t).values[:, None], len(kodlar), 1), index=t, columns=kodlar)
        C.append(v.reindex(t)[kodlar].values.astype(float))
    ok0 = np.isfinite(Y)
    for c in C:
        ok0 &= np.isfinite(c)
    if filtre:
        ok0 &= uygun(kodlar).values
    if bilanco_at:
        ok0 &= ~_bilanco_maske(kodlar, h)
    dn = _donem_no(t)
    grp_m = dn[:, None] * len(kodlar) + np.arange(len(kodlar))[None, :]
    kume_m = np.broadcast_to(_kume_etiket(t, h)[:, None], X0.shape)

    def tahmin(Xm, se_ister=True):
        ok = ok0 & np.isfinite(Xm)
        if ok.sum() < 30:
            return np.nan, np.nan, np.nan, 0, 0
        V = np.column_stack([Xm[ok]] + [c[ok] for c in C] + [Y[ok]])
        _, grp = np.unique(grp_m[ok], return_inverse=True)
        W = _icten(V, grp, grp.max() + 1)
        Xd, yd = W[:, :-1], W[:, -1]
        # eşdoğrusal kontrolleri at (ör. hedef = SMH)
        keep = [0]
        for c in range(1, Xd.shape[1]):
            if np.linalg.matrix_rank(Xd[:, keep + [c]]) == len(keep) + 1:
                keep.append(c)
        Xd = Xd[:, keep]
        if not se_ister:
            b = np.linalg.lstsq(Xd, yd, rcond=None)[0]
            return b[0], np.nan, np.nan, ok.sum(), 0
        b, se, G = _ols_kume(yd, Xd, kume_m[ok])
        return b[0], se[0], G, ok.sum(), len(np.unique(np.broadcast_to(t.values[:, None], X0.shape)[ok]))

    b, se, G, nobs, ntar = tahmin(X0)
    tt = b / se if se and np.isfinite(se) and se > 0 else np.nan
    p = 2 * _st.t.sf(abs(tt), G - 1) if np.isfinite(tt) else np.nan
    out = dict(egim_bps=b, se_egim_bps=se, t_egim=tt, p_egim=p, n_gozlem=nobs, n_tarih=ntar, p_perm=np.nan)
    if perm:
        kay = _kaydirmalar(perm, len(t), seed)
        pb = np.array([tahmin(np.roll(X0, int(k), axis=0), se_ister=False)[0] for k in kay])
        pb = pb[np.isfinite(pb)]
        out["p_perm"] = (np.sum(np.abs(pb) >= abs(b)) + 1) / (len(pb) + 1)
    return out


# ---------------------------------------------------------------- rejim (madde 10)
def _rejim_gunleri():
    k = ("rejim_gun",)
    if k not in _onbellek:
        t = TK()
        vix = yukle("^VIX")["Close"].reindex(t)          # VIX t barı (madde 2.3: VIX ailesi t barıyla)
        q = fiyat("QQQ")["AClose"].reindex(t)
        smh = fiyat("SMH")["AClose"].reindex(t)
        d = pd.DataFrame(index=t)
        d["qqq_ust"] = q > q.rolling(200, min_periods=200).mean()
        d["vix"] = vix
        d["vix_kova"] = pd.cut(vix, [-np.inf, 15, 20, 30, np.inf], right=False,
                               labels=["VIX<15", "VIX15-20", "VIX20-30", "VIX>=30"])
        d["STRES"] = vix >= 30
        d["BUGUN"] = (vix >= 30) & (smh <= 0.75 * smh.rolling(250, min_periods=250).max())
        _onbellek[k] = d
    return _onbellek[k]


def _epizot(tarihler, ara=10):
    t = TK()
    p = np.sort(t.get_indexer(pd.DatetimeIndex(tarihler).unique()))
    if len(p) == 0:
        return {}
    ep = np.concatenate([[0], np.cumsum(np.diff(p) >= ara)])
    return dict(zip(t[p], ep))


def rejim(islemler_, n_boot=2000, seed=0):
    """Hücreler (marjinal): QQQ>200g ort, QQQ<200g ort, VIX<15, 15-20, 20-30, >=30; STRES; BUGÜN.
    t ve p yok. Büzülmüş = w*hücre + (1-w)*genel alfa, w = n_epizot/(n_epizot+20). Dönüş: DataFrame."""
    isl = islemler_
    d = _rejim_gunleri().reindex(pd.DatetimeIndex(isl["giris"]))
    genel = isl["alfa_bps"].mean()
    hucre = {"QQQ_ust200": d["qqq_ust"].values == True, "QQQ_alt200": d["qqq_ust"].values == False}
    for kv in ["VIX<15", "VIX15-20", "VIX20-30", "VIX>=30"]:
        hucre[kv] = (d["vix_kova"] == kv).values
    hucre["STRES"] = d["STRES"].values == True
    hucre["BUGUN"] = d["BUGUN"].values == True
    rng = np.random.default_rng(seed)
    rows = []
    for ad, m in hucre.items():
        x = isl[m]
        r = dict(test_id=_ctx(isl).get("test_id") or (isl["test_id"].iloc[0] if len(isl) else None),
                 hucre=ad, n_islem=len(x), n_gun=x["giris"].nunique() if len(x) else 0)
        if len(x):
            ep = x["giris"].map(_epizot(x["giris"]))
            ne = ep.nunique()
            grp = [x["alfa_bps"].values[ep.values == e] for e in np.unique(ep)]
            bs = []
            for _ in range(n_boot):
                s = rng.integers(0, ne, ne)
                v = np.concatenate([grp[i] for i in s])
                bs.append(v.mean())
            w = ne / (ne + 20)
            r.update(n_epizot=ne, ortalama_bps=x["alfa_bps"].mean(), medyan_bps=x["alfa_bps"].median(),
                     isabet=(x["getiri_bps"] > 0).mean(), en_kotu_bps=x["getiri_bps"].min(),
                     ar05_bps=np.percentile(bs, 5), ar95_bps=np.percentile(bs, 95),
                     buzulmus_bps=w * x["alfa_bps"].mean() + (1 - w) * genel,
                     not_="yalnız betimsel" if ne < 8 else "")
        else:
            r.update(n_epizot=0, not_="boş")
        rows.append(r)
    return pd.DataFrame(rows).rename(columns={"not_": "not"})


# ---------------------------------------------------------------- ekonomi (madde 11)
def _ybbo(r, gun):
    v = np.prod(1 + np.asarray(r)) if len(r) else 1.0
    return v ** (252 / max(gun, 1)) - 1 if v > 0 else -1.0


def ekonomi(islemler_, arac, t_stat=None, donemler=("tam", "P3"), n_boot=2000, n_rast=1000, seed=0):
    """arac: tek kod (sermayenin tamamı) ya da 'havuz' (en çok 3 eşzamanlı, 1/3'er; fazlaysa |guc| en
    büyük 3; guc yoksa kod sırası, 'not'ta yazılır). Getiriler ham, kapanış->kapanış günlük yol;
    maliyet çıkış günü düşülür. Dönüş: DataFrame (madde 11.2 sütunları), dönem başına bir satır."""
    isl = islemler_.copy()
    a = _ctx(islemler_)
    if t_stat is None:
        t_stat = np.nan
    tkv = TK()
    rng = np.random.default_rng(seed)
    if arac != "havuz":
        isl = isl[isl["kod"] == arac]
    kodlar = sorted(isl["kod"].unique()) if len(isl) else [arac]
    R = _gunluk_ham(a.get("kodlar", kodlar)) / 1e4
    havuz = arac == "havuz"
    w0 = 1 / 3 if havuz else 1.0
    lev = max([abs(KALDIRAC.get(k, 1)) for k in kodlar] or [1])
    tavan = 1.0 if lev == 1 else (0.5 if lev == 2 else 0.33)
    rows = []
    for dad in donemler:
        bas, bit = (tkv[0], SON_GUN) if dad == "tam" else tuple(map(pd.Timestamp, DONEMLER[dad]))
        x = isl[(isl["giris"] >= bas) & (isl["giris"] <= bit)].copy()
        gunler = tkv[(tkv >= bas) & (tkv <= bit)]
        not_ = ""
        if havuz and len(x):
            if "guc" in x:
                x["_s"] = -x["guc"].abs()
            else:
                x["_s"] = 0
                not_ = "guc yok: kod sırası"
            secili, acik = [], []
            for gtar, grp in x.sort_values(["giris", "_s", "kod"]).groupby("giris", sort=True):
                acik = [c for c in acik if c > gtar]
                bos = 3 - len(acik)
                al = grp.iloc[:max(bos, 0)]
                secili.append(al)
                acik += list(al["cikis"])
            x = pd.concat(secili) if secili else x.iloc[:0]
        Rall = R.reindex(columns=kodlar).values
        jm = {c: j for j, c in enumerate(kodlar)}
        g0 = tkv.get_loc(gunler[0]) if len(gunler) else 0
        pv_ = np.zeros(len(gunler))
        pv50 = np.zeros(len(gunler))
        if len(x):
            ii = tkv.get_indexer(pd.DatetimeIndex(x["giris"]))
            jj = x["kod"].map(jm).values
            gl = x["gun"].values.astype(int)
            ml = x["maliyet_bps"].values / 1e4
            for L in range(1, gl.max() + 1):
                m = gl >= L
                d = ii[m] + L
                ok = (d - g0 >= 0) & (d - g0 < len(gunler))
                v = np.nan_to_num(Rall[d[ok], jj[m][ok]])
                np.add.at(pv_, d[ok] - g0, w0 * v)
                np.add.at(pv50, d[ok] - g0, w0 * v)
            dc = ii + gl - g0
            ok = (dc >= 0) & (dc < len(gunler))
            np.add.at(pv_, dc[ok], -w0 * ml[ok])
            np.add.at(pv50, dc[ok], -w0 * (ml[ok] + 0.005))
        port = pd.Series(pv_, index=gunler)
        port50 = pd.Series(pv50, index=gunler)
        net = (x["ham_bps"] - x["maliyet_bps"]) / 1e4
        yil = len(gunler) / 252
        eq = (1 + port).cumprod()
        yillik = (1 + port).groupby(port.index.year).prod() - 1
        # 20 günlük blok yeniden örnekleme, 1 yıl = 13 blok
        pv = port.values
        nb = max(len(pv) - 20, 1)
        bl = rng.integers(0, nb, size=(n_boot, 13))
        yb = np.array([np.prod(1 + np.concatenate([pv[s:s + 20] for s in row])) - 1 for row in bl])
        # rastgele giriş: aynı işlem sayısı, aynı araçlar, aynı tutma
        Rv = R[kodlar].reindex(gunler).fillna(0).values if len(kodlar) else np.zeros((len(gunler), 1))
        ry = []
        if len(x):
            gl = x["gun"].values
            ml = x["maliyet_bps"].values / 1e4
            cum = np.vstack([np.zeros(Rv.shape[1]), np.cumsum(np.log1p(Rv), axis=0)])
            for _ in range(n_rast):
                ii = rng.integers(0, max(len(gunler) - 3, 1), len(x))
                jj = rng.integers(0, Rv.shape[1], len(x))
                tr = np.expm1(cum[np.minimum(ii + 1 + gl, len(gunler)), jj] - cum[ii + 1, jj]) - ml
                ry.append(np.exp(np.sum(np.log1p(w0 * tr))) ** (1 / max(yil, 1e-9)) - 1)
        al_tut = Rv.mean(axis=1)
        mu, sd = net.mean() if len(net) else np.nan, net.std() if len(net) > 1 else np.nan
        mub = mu * max(0.0, 1 - 1 / t_stat ** 2) if np.isfinite(t_stat) and t_stat != 0 else np.nan
        f = mub / sd ** 2 if sd and np.isfinite(sd) and sd > 0 else np.nan
        kaz, kay = net[net > 0].mean() if (net > 0).any() else np.nan, net[net < 0].mean() if (net < 0).any() else np.nan
        rows.append(dict(test_id=a.get("test_id"), arac=arac, donem=dad, yillik_islem=len(x) / yil,
                         piyasada_gun_orani=(port != 0).mean(), islem_net_bps=net.mean() * 1e4 if len(net) else np.nan,
                         isabet=(net > 0).mean() if len(net) else np.nan,
                         kazanc_kayip=kaz / abs(kay) if np.isfinite(kaz) and np.isfinite(kay) else np.nan,
                         ybbo_net=_ybbo(port.values, len(gunler)), oynaklik=port.std() * np.sqrt(252),
                         sharpe=port.mean() / port.std() * np.sqrt(252) if port.std() > 0 else np.nan,
                         en_buyuk_dusus=(eq / eq.cummax() - 1).min(),
                         en_kotu_islem=net.min() * 1e4 if len(net) else np.nan, en_kotu_yil=yillik.min(),
                         yil_p5=np.percentile(yb, 5), yil_p50=np.percentile(yb, 50), yil_p95=np.percentile(yb, 95),
                         p_zarar_yil=(yb < 0).mean(), kelly_tam=f,
                         kelly_ceyrek=min(f / 4, tavan) if np.isfinite(f) else np.nan,
                         al_tut_ybbo=_ybbo(al_tut, len(gunler)),
                         rastgele_p95_ybbo=np.percentile(ry, 95) if ry else np.nan,
                         ybbo_net_50bps=_ybbo(port50.values, len(gunler)),
                         not_=(not_ + ("; ekonomik olarak anlamsız" if np.isfinite(f) and f / 4 < 0.1 else "")).strip("; ")))
    return pd.DataFrame(rows).rename(columns={"not_": "not"})


# ---------------------------------------------------------------- kayıt ve birleştirme
def kaydet(ajan, satirlar, tur="sonuc"):
    """veri/sonuc/<AJAN>_<tur>.csv yazar (üzerine). tur: sonuc | islemler | rejim | ekonomi | tasima |
    ya da serbest ad (ör. '1530' -> B1_1530.csv). satirlar: dict listesi ya da DataFrame."""
    SONUC.mkdir(parents=True, exist_ok=True)
    df = satirlar if isinstance(satirlar, pd.DataFrame) else pd.DataFrame(list(satirlar))
    if tur == "sonuc":
        df["ajan"] = df.get("ajan", ajan) if "ajan" in df else ajan
        ek = [c for c in df.columns if c not in SONUC_SUTUN]
        df = df.reindex(columns=SONUC_SUTUN + ek)
    if tur == "islemler":
        df = df[[c for c in ["test_id", "kod", "giris", "cikis", "getiri_bps", "alfa_bps", "gun", "ham_bps",
                             "alfa_ham_bps", "maliyet_bps"] if c in df]]
    ad = f"{ajan}_{tur}.csv" if tur in ("sonuc", "islemler", "rejim", "ekonomi", "tasima") else f"{ajan}_{tur}.csv"
    yol = SONUC / ad
    df.to_csv(yol, index=False)
    return yol


def _aile_kok(aile):
    """Aile kökü: 'F11a' -> 'F11', 'F1d' -> 'F1', 'LL4_BTC' -> 'LL4'. (Düzeltme: önek karşılaştırması
    F11'i F1 sayıyordu; madde 12'nin 7. ve 8. ölçütleri yalnız F1–F5 ve F10 içindir.)"""
    m = re.match(r"(F\d+|LL\d+)", str(aile))
    return m.group(1) if m else str(aile)


def _etiket(r, kriter_8, kriter_9):
    """Madde 12. Dönüş: (etiket, kontrol dizgesi, not)."""
    yon = int(r.get("yon", 1) if pd.notna(r.get("yon", np.nan)) else 1)
    egimli = pd.notna(r.get("t_egim"))
    tb = r["t_egim"] if egimli else r["t_kume"]
    k = {}
    k[1] = (r["n_islem"] >= 100) and (r["n_gun"] >= 60)
    esik = 3.0 if r.get("kaynak") == "turev" else 2.5
    qok = (r["q_bh"] <= 0.10) if pd.notna(r.get("q_bh")) else True
    k[2] = bool(qok and pd.notna(tb) and yon * tb >= esik)
    k[3] = True if yon < 0 else bool(r["alfa_net_bps"] > 0)
    dog = [(r[f"n_{p}"] >= 50 and yon * r[f"alfa_{p}"] > 0) for p in ("P1", "P2", "P3")]
    k[4] = bool(dog[2] and sum(dog) >= 2)
    k[5] = bool(yon * r["alfa_ust1suz_bps"] > 0 and yon * r["alfa_5gunsuz_bps"] > 0)
    k[6] = bool(pd.notna(r["t_takvim"]) and yon * r["t_takvim"] >= 1.5 and pd.notna(r["p_perm"]) and r["p_perm"] <= 0.05)
    aile = str(r.get("aile", ""))
    if _aile_kok(aile) in ("F1", "F2", "F3", "F4", "F10"):
        k[7] = None if pd.isna(r.get("alfa_temiz")) else bool(yon * r["alfa_temiz"] > 0)
    else:
        k[7] = True
    k[8], k[9] = kriter_8, kriter_9
    k["4.6"] = True if r.get("getiri_turu") != "artik" else bool(np.sign(r["alfa_bps"]) == np.sign(r.get("alfa_ham_bps", np.nan)))
    bek = [str(i) for i, v in k.items() if v is None]
    bas = [str(i) for i, v in k.items() if v is False]
    kontrol = " ".join(f"{i}:{'+' if v else ('?' if v is None else '-')}" for i, v in k.items())
    notlar = []
    if pd.notna(r.get("alfa_son12")) and yon * r["alfa_son12"] < 0 and pd.notna(r.get("t_son12")) and yon * r["t_son12"] < -1:
        notlar.append("soluyor")
    if not k[1]:
        return "GÜÇSÜZ", kontrol, notlar
    if not bas and not bek:
        return "GEÇTİ", kontrol, notlar
    if not bas:
        return f"GEÇTİ-bekliyor({','.join(bek)})", kontrol, notlar
    if pd.notna(tb) and abs(tb) >= 2 and yon * tb > 0 and k[1] and k[3] and k[4]:
        return "ADAY", kontrol, notlar
    return "KULLANILAMAZ", kontrol, notlar


def birlestir(beklenen_birincil=61, yaz=True):
    """Bütün veri/sonuc/<AJAN>_sonuc.csv'leri okur; birincil (birincil==1, aile != LL6) testlerde tek havuz
    BH %10 (q_bh), madde 6.2 eşikleri ve madde 12 etiketleri. Ölçüt 8: B1_1530.csv (test_id, A_bps, B_bps,
    oran_B_A), ölçüt 9: veri/sonuc/yeniden_kodlama.csv (test_id, n_islem, alfa_bps); dosya ya da satır
    yoksa 'bekliyor'. LL6 ayrı havuz: satırlarda asama = 'kesif' | 'dogrulama', aynı varyant.
    Dönüş: (birlesik DataFrame, LL6 DataFrame, özet dict)."""
    dosyalar = [f for f in sorted(SONUC.glob("*_sonuc.csv")) if not f.name.startswith("BIRLESIK")]
    if not dosyalar:
        raise FileNotFoundError("veri/sonuc/*_sonuc.csv yok")
    df = pd.concat([pd.read_csv(f) for f in dosyalar], ignore_index=True)
    for c in ("yon", "alfa_ham_bps", "t_son12", "asama"):
        if c not in df:
            df[c] = np.nan
    df["q_bh"] = np.nan
    ll6 = df["aile"].astype(str).str.startswith("LL6")
    bir = (df["birincil"] == 1) & ~ll6
    adj, _ = bh_fdr(df.loc[bir, "p_birincil"].values, 0.10)
    df.loc[bir, "q_bh"] = adj
    # alfa_temiz: boşsa aynı test_id'nin T karşılığından (…_C_… -> …_T_…)
    al = df.set_index("test_id")["alfa_bps"].to_dict()
    for i in df.index[df["alfa_temiz"].isna()]:
        tid = str(df.at[i, "test_id"])
        if "_C_" in tid and tid.replace("_C_", "_T_") in al:
            df.at[i, "alfa_temiz"] = al[tid.replace("_C_", "_T_")]
    y1530 = SONUC / "B1_1530.csv"
    t1530 = pd.read_csv(y1530).set_index("test_id") if y1530.exists() else None
    yyk = SONUC / "yeniden_kodlama.csv"
    tyk = pd.read_csv(yyk).set_index("test_id") if yyk.exists() else None
    et, ko, no = [], [], []
    for _, r in df.iterrows():
        tid, yon = r["test_id"], (r["yon"] if pd.notna(r["yon"]) else 1)
        k8 = True
        if _aile_kok(r["aile"]) in ("F1", "F2", "F3", "F4", "F5", "F10"):
            if t1530 is None or tid not in t1530.index:
                k8 = None
            else:
                b, o_ = t1530.at[tid, "B_bps"], t1530.at[tid, "oran_B_A"]
                k8 = bool(yon * b > 0 and o_ >= 0.5)
        if tyk is None or tid not in tyk.index:
            k9 = None
        else:
            k9 = bool(abs(tyk.at[tid, "n_islem"] - r["n_islem"]) <= 0.01 * r["n_islem"]
                      and abs(tyk.at[tid, "alfa_bps"] - r["alfa_bps"]) <= 1)
        if ll6[_]:
            et.append(None); ko.append(""); no.append(""); continue
        e, k, n = _etiket(r, k8, k9)
        if r["birincil"] != 1:
            e = "tanı:" + e
        et.append(e); ko.append(k); no.append(";".join(n))
    df["etiket"], df["kontrol"] = et, ko
    df["not"] = [";".join([x for x in [str(a) if pd.notna(a) else "", b] if x]) for a, b in zip(df["not"], no)]
    # LL6
    L = df[ll6].copy()
    ozet = dict(n_birincil=int(bir.sum()), beklenen=beklenen_birincil, bh_red=int((df.loc[bir, "q_bh"] <= 0.10).sum()))
    if len(L):
        kes = L[L["asama"] == "kesif"].copy()
        a1, r1 = bh_fdr(kes["p_birincil"].values, 0.10)
        kes["q_bh"], kes["kesif_gecti"] = a1, r1
        dog = L[L["asama"] == "dogrulama"].set_index("varyant")
        sonuc = []
        for _, r in kes[kes["kesif_gecti"]].iterrows():
            if r["varyant"] not in dog.index:
                continue
            d = dog.loc[r["varyant"]]
            tb = d["t_egim"] if pd.notna(d.get("t_egim")) else d["t_kume"]
            tk = r["t_egim"] if pd.notna(r.get("t_egim")) else r["t_kume"]
            ayni = np.sign(tb) == np.sign(tk)
            p1 = _st.norm.sf(np.sign(tk) * tb)
            sonuc.append((r["varyant"], ayni, np.sign(tk) * tb, p1))
        if sonuc:
            v = pd.DataFrame(sonuc, columns=["varyant", "ayni_isaret", "t_tek", "p_tek"])
            v["q_dog"] = bh_fdr(v["p_tek"].values, 0.10)[0]
            v["dogrulandi"] = v["ayni_isaret"] & (v["t_tek"] >= 2) & (v["q_dog"] <= 0.10)
            L = L.merge(v, on="varyant", how="left")
        ozet.update(ll6_kesif=len(kes), ll6_kesif_gecen=int(r1.sum()), ll6_sansla_beklenen=0.10 * int(r1.sum()),
                    ll6_dogrulanan=int(v["dogrulandi"].sum()) if sonuc else 0)
    if ozet["n_birincil"] != beklenen_birincil:
        print(f"UYARI: birincil test sayısı {ozet['n_birincil']} (beklenen {beklenen_birincil})")
    if yaz:
        df[~ll6].to_csv(SONUC / "BIRLESIK_sonuc.csv", index=False)
        if len(L):
            L.to_csv(SONUC / "BIRLESIK_LL6.csv", index=False)
    return df[~ll6], L, ozet
