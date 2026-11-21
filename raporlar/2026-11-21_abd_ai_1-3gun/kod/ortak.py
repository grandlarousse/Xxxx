"""Ortak kütüphane: veri yükleme, getiri tanımları, takvim hizalama, olay testi, BH-FDR.

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
