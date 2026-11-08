#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gunluk_oneri.py - Her BIST is gunu aksami (VIOP bulteni sonrasi, ~21:05 TSI) TEK komutla gunluk oneri raporu.

NE YAPAR
  0. BUGUN NE YAPILIR: ertesi seans icin somut emirler (ya da "Islem yok" + neden) ve yarin tetiklenebilecekler
     (tetige <= %3 kalanlar, kesin tetik fiyatiyla).
  1. BIST rejimi (PLAN_BIST s2: T1-T3, M1-M5) ve KRIZ kesicisi (a-f); makro girdiler <cikti>/makro.json'dan.
  2. Plan kurallari (bist_sinyal.py mantigi): K1 ve K2 z, K4 kirilim ve bekleme listesi, kume 12 ay RS,
     VIOP resmi bulten ima oranlari, K6 kapisi.
  3. 1-3 gunluk PRATIK sinyaller (2026-11-04_kapanis_1-3gun): SAHOL/AKBNK artik z, Koza z3 (TRMET/TRALT/TRENJ),
     altin -> TRALT (VIOP F_XAUUSD uzlasma degisimi vekili), XU030 kapanis bazi sicramasi (bulten kapanis fiyati;
     karar canli 18:10-18:15 oldugu icin TradingView alarmiyla), TUPRS <- ABD rafinerileri (TradingView alarmiyla).
  4. Takvim bayraklari (PLAN_BIST s3.10, s7; PLAN_ABD s7) - statik tablo.
  5. ABD rejimi (PLAN_ABD s2.2-2.6): FRED SP500/NASDAQ100, CBOE VIX/VIX3M; kalici durum <cikti>/durum.json
     (ralli denemesi gun sayisi, FTD, SARI 3 kapanis sayaci, pilot freni). Her calismada okunur ve yazilir.
  6. Veri tazeligi tablosu.
  Cikti: <cikti>/oneri_<YYYYMMDD>.md, <cikti>/SON.md (ayni icerik), <cikti>/BILDIRIM.txt (<= ~600 karakter),
         <cikti>/durum.json (guncellenir), <cikti>/makro.json (yoksa 05.11 degerleriyle olusturulur).

KULLANIM
  python3 gunluk_oneri.py --cikti ../gunluk --veri /tmp/gunluk_veri
  python3 gunluk_oneri.py --cikti ../gunluk                 # --veri verilmezse gecici klasor
  python3 gunluk_oneri.py --cikti ../gunluk --veri V --cevrimdisi   # hic istek atmadan onbellekten (deneme)
  Secenekler: --bekle 0.4 (istekler arasi sn), --tarih YYYY-MM-DD (BIST kesim tarihi), --durum-yazmadan (durum.json'u
  degistirme; deneme icin), --butce 480 (sn; Is Yatirim indirmesi icin zaman butcesi).

NOTLAR
  * python3 + requests + pandas + numpy. Varsayilan istek basliklari (User-Agent degistirilmez), istekler arasi bekleme,
    429'da geri cekilme. Yahoo kullanilmaz. Bir kaynak duserse o bolum "veri yok" der, digerleri devam eder.
  * Kaynaklar: Is Yatirim ChartData (163 seri, duzeltilmis kapanis), Borsa Istanbul VIOP bulteni (son 2 gun) ve pay piyasasi
    bulteni (thbYYYYMMDD1.zip, son 60 gun -> 60g medyan TL hacim / likidite sirasi; HisseTekil ile ayni sonuc), KAP endeks
    listesi, FRED (SP500, NASDAQ100), CBOE (VIX, VIX3M). HisseTekil yalniz bulten alinamazsa yedektir.
  * Is Yatirim baglantisi koparsa (devre kesici) once onbellek kullanilir, pay bultenlerinden sonra eksikler bir kez daha
    denenir, sonra --isy-son (360 sn) dolana kadar ~60 sn'de bir TEK istekle yoklanir; yine yoksa BIST bolumleri "veri yok"
    olur ve son basarili calismanin tetikleri pay bulteninin kapanis fiyatlariyla kontrol edilir (yedek kip).
  * Is Yatirim bazen KISALTILMIS gecmis donduruyor (denetim 08.11: GARAN 1 yil): ilk tarihi istenenden > 30 gun sonra gelen
    seri bir kez daha istenir, uzun olani alinir.
  * Bos onbellekle sure ~3 dk (08.11 olcumu 178 sn: 163 + 60 + ~8 istek; denetimde Is Yatirim yarida kopunca 382 sn);
    dolu onbellekle ~30 sn; Is Yatirim hic acilmazsa yoklamayla ~7 dk (ust sinir ~8,5 dk).
  * Ham veri onbellegi --veri klasorundedir; depoya konmaz. durum.json ve makro.json kucuk durum dosyalaridir (ham veri degil).
  * Bilgi amaclidir; yatirim tavsiyesi degildir.
"""
import argparse, io, json, math, os, sys, tempfile, time, zipfile
from datetime import datetime, timedelta
import numpy as np, pandas as pd, requests

sys.dont_write_bytecode = True   # bulut calismasi depoya __pycache__ birakmasin
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bist_tarama as bt   # noqa: E402  (VIOP listesi, KAP endeks listesi, VIOP bulteni, TSI, oturum S)
import bist_sinyal as bs   # noqa: E402  (kumeler, dislama, makro varsayilani, fmt, z yardimcilari)

TSI = bt.TSI
S = bt.S  # requests.Session, varsayilan basliklar
CHART_URL = bt.URL
HT_URL = bs.HT_URL
FRED_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={}"
CBOE_URL = "https://cdn.cboe.com/api/global/us_indices/daily_prices/{}_History.csv"
THB_URL = "https://www.borsaistanbul.com/data/thb/{:%Y}/{:%m}/thb{:%Y%m%d}1.zip"
TCMB_URL = "https://www.tcmb.gov.tr/kurlar/{:%Y%m}/{:%d%m%Y}.xml"
f = bs.fmt
_kac = lambda c: str(c).replace("\\|", "|").replace("|", "\\|")  # hucre icindeki | tabloyu bozmasin
tablo = lambda bas, sat: bs.tablo([_kac(x) for x in bas], [[_kac(c) for c in r] for r in sat])
sma = lambda s, n: s.rolling(n).mean()
pc2 = lambda v: f"%{100 * v:.2f}".replace(".", ",")  # %0,25
f4 = lambda v: f"{v:.4f}".replace(".", ",") if v is not None and np.isfinite(v) else "—"

# ---------------------------------------------------------------------------------------------------------------
# Takvimler (BIST 2026 Kasim-Aralik kesin; 2027 bayramlari tahmini -> OTOMASYON.md: her yil basinda teyit edin)
TATIL_BIST = {pd.Timestamp(x) for x in [
    "2026-10-29", "2027-01-01", "2027-03-10", "2027-03-11", "2027-03-12", "2027-04-23", "2027-05-19",
    "2027-05-17", "2027-05-18", "2027-05-20", "2027-07-15", "2027-08-30", "2027-10-29"]}
TATIL_ABD = {pd.Timestamp(x) for x in [
    "2026-11-26", "2026-12-25", "2027-01-01", "2027-01-18", "2027-02-15", "2027-03-26", "2027-05-31",
    "2027-06-18", "2027-07-05", "2027-09-06", "2027-11-25", "2027-12-24"]}


def is_gunu(d, tatil):
    d = pd.Timestamp(d).normalize()
    return d.weekday() < 5 and d not in tatil


def sonraki(d, n=1, tatil=TATIL_BIST):
    d = pd.Timestamp(d).normalize()
    k = 0
    while k < n:
        d += pd.Timedelta(days=1)
        if is_gunu(d, tatil):
            k += 1
    return d


def onceki_veya_ayni(d, tatil=TATIL_BIST):
    d = pd.Timestamp(d).normalize()
    while not is_gunu(d, tatil):
        d -= pd.Timedelta(days=1)
    return d


def is_gunu_say(a, b, tatil=TATIL_BIST):
    """(a, b] arasindaki is gunu sayisi."""
    a, b = pd.Timestamp(a).normalize(), pd.Timestamp(b).normalize()
    return sum(1 for d in pd.date_range(a + pd.Timedelta(days=1), b) if is_gunu(d, tatil))


def tr_tarih(d):
    if d is None:
        return "—"
    d = pd.Timestamp(d)
    gun = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"][d.weekday()]
    return f"{gun} {d:%d.%m.%Y}"


# Statik takvim (PLAN_BIST s3.10 A1-A10, s7; PLAN_ABD s7). blok: yeni girisi engelledigi kollar ("TUM" = hepsi).
TAKVIM = [
    ("2026-11-09", "2026-11-09", "BIST", "3Ç konsolide bilançoların son günü (A1)",
     "Bilançosunu 9.11 18:00'den önce açıklamamış isimlerde 9.11 gecesi pozisyon taşınmaz, yeni giriş yok; ilk karar 10.11 kapanışı.",
     {"isim": "BILANCO"}),
    ("2026-11-10", "2026-11-10", "ABD", "16:30 TSİ Ekim CPI", "ABD'de 16:45'ten önce emir yok (veri günü kuralı). MDT yasağı başlar.", {}),
    ("2026-11-11", "2026-11-11", "BIST", "MSCI duyurusu öncesi kapanış (A2, A3)",
     "Hiçbir kolda yeni giriş yok (K1 ve 1–3 günlük sinyaller dahil).", {"kol": "TUM"}),
    ("2026-11-11", "2026-11-11", "ABD", "Gaziler Günü: tahvil kapalı, hisse açık", "En erken FTD kapanışı (06.11 1. gün olduysa); hacim şartına dikkat.", {}),
    ("2026-11-12", "2026-11-13", "BIST", "MSCI sonuçları (12.11 01:00), 14:30 rezerv, SPK kredili esneklik kararı (A2)",
     "Yeni K3/K4/K5/K9 girişi yok (1–3 günlük sinyaller K9 kanalıdır); K1 normal. 12.11 14:30 rezervi makro.json'a yaz: haftalık değişim ≤ −5 mlr $ ise KRİZ (d).",
     {"kol": ["K3", "K4", "K5", "K9"]}),
    ("2026-11-13", "2026-11-13", "BIST", "Kredili esneklik seans sonunda bitiyor (A4)",
     "Uzatılmazsa: K4 girişi 23.11'e, VİOP-47 dışı long 30.11'e kadar yok; zarardaki VİOP-47 dışı spot satılır. makro.json 'kredili_esneklik_uzatildi' alanını doldur.", {}),
    ("2026-11-13", "2026-11-13", "ABD", "16:30 PPI", "Veri günü kuralı. En erken SARI kapanışı.", {}),
    ("2026-11-17", "2026-11-17", "ABD", "NVDA sonuçları (kapanış sonrası)", "Bütün kümelerde yeni giriş yok.", {"abd": True}),
    ("2026-11-18", "2026-11-18", "ABD", "22:00 FOMC tutanakları", "Giriş emirleri GTD, 21:55 TSİ'de düşer.", {}),
    ("2026-11-19", "2026-11-19", "BIST", "Banka konsolide son günü; 14:30 rezerv (2. hafta)",
     "Bilançosu gelecek bacakta K1 girişi yok (AKBNK açıkladı mı KAP'tan bak). M1 2. hafta, KRİZ (d) kontrolü.", {}),
    ("2026-11-20", "2026-11-20", "ABD", "Aylık opsiyon vadesi", "Bilgi.", {}),
    ("2026-11-23", "2026-11-23", "BIST", "A4 uygulanıyorsa K4 girişleri bu kapanıştan serbest", "—", {}),
    ("2026-11-25", "2026-11-25", "BIST", "Kasım pay vadelisi son devir günü (A10)", "Açık Kasım bacakları kapanışta kapatılır ya da Aralık'a devredilir.", {}),
    ("2026-11-25", "2026-11-25", "ABD", "GSYH, PCE, Bej Kitap", "Yeni giriş yok.", {"abd": True}),
    ("2026-11-26", "2026-11-26", "BIST", "14:30 rezerv (3. hafta)", "M1 olası 1; GEÇİŞ 27.11'den geçerli olabilir.", {}),
    ("2026-11-26", "2026-11-26", "ABD", "Şükran Günü: piyasa kapalı", "—", {}),
    ("2026-11-27", "2026-11-27", "ABD", "Erken kapanış 21:00 TSİ", "Yeni giriş yok.", {"abd": True}),
    ("2026-11-30", "2026-11-30", "BIST", "VİOP Kasım vadesi; MSCI yürürlüğü; ay sonu",
     "Vade gününe pozisyon taşınmaz. T2 ve 12 ay küme RS sırası. MSCI'dan çıkarılan hisseler bu kapanışa kadar alınmaz.", {}),
    ("2026-12-03", "2026-12-03", "BIST", "10:00 Kasım TÜFE", "makro.json 'tufe_aylik' listesine ekle (M2).", {}),
    ("2026-12-08", "2026-12-08", "ABD", "Makro gap-ayarlı ısı kontrolü", "Aşan kısım 9.12 MOO.", {}),
    ("2026-12-09", "2026-12-09", "ABD", "FOMC 22:00", "Yeni giriş yok.", {"abd": True}),
    ("2026-12-10", "2026-12-10", "BIST", "TCMB PPK (anket %35)",
     "Sürprizsiz indirimde (±25 bp) 11.12'den ~15.03.2027'ye kadar BANKA kümesinde yeni K4/K9 yarım boy, en çok 1 (A7). makro.json 'ppk_10_12_surprizsiz_indirim'.", {}),
    ("2026-12-21", "2026-12-23", "BIST", "Aralık VİOP devir haftası (A10)", "Aralık bacakları en geç 23.12 kapanışında devredilir ya da kapanır.", {}),
    ("2026-12-31", "2026-12-31", "BIST", "Aralık vadesi (XU030, USDTRY, pay)", "Devredilmeyen her şey kapanmış olmalı.", {}),
    ("2027-01-29", "2027-02-05", "BIST", "BIST30 blok kilidi / fon uyumu (A9)", "K1'de yeni giriş yok.", {"kol": ["K1"]}),
    ("2027-02-01", "2027-02-01", "BIST", "K3b pilot başlangıcı", "Yarım boy, hedge'li.", {}),
]

# ---------------------------------------------------------------------------------------------------------------
KAYNAK = {}   # ad -> dict(durum, son, not)
ISY = {"down": False, "hata_ardisik": 0, "istek": 0, "basari": 0}
T0 = time.time()


def kaynak(ad, durum, son=None, notu=""):
    KAYNAK[ad] = dict(durum=durum, son=son, notu=notu)


def al(url, params=None, timeout=30, deneme=3, bekle=0.4):
    """Varsayilan baslikla GET; 429'da geri cekilir. Basarisizsa None."""
    for k in range(deneme):
        try:
            r = S.get(url, params=params, timeout=timeout)
            if r.status_code == 429:
                time.sleep(10 * (k + 1)); continue
            if r.status_code == 200:
                time.sleep(bekle)
                return r
            if r.status_code in (403, 404, 407):
                time.sleep(bekle)
                return None
        except requests.RequestException:
            pass
        time.sleep(2 * (k + 1))
    return None


# ---------------------------------------------------------------------------------------------------------------
# Is Yatirim (ChartData + HisseTekil), devre kesicili
def isy_istek(kod, bas, son, bekle):
    if ISY["down"]:
        return pd.Series(dtype=float, name=kod)
    p = {"period": 1440, "from": bas.strftime("%Y%m%d000000"), "to": son.strftime("%Y%m%d235959"), "endeks": kod}
    baglanti_hatasi = 0
    for k in range(3):
        try:
            ISY["istek"] += 1
            r = S.get(CHART_URL, params=p, timeout=30)
            if r.status_code == 429:
                time.sleep(10 * (k + 1)); continue
            if r.status_code == 200 and r.text.strip():
                d = r.json().get("data") or []
                if d:
                    ISY["hata_ardisik"] = 0; ISY["basari"] += 1
                    ts = pd.to_datetime([x[0] for x in d], unit="ms") + pd.Timedelta(hours=3)
                    time.sleep(bekle)
                    return pd.Series([float(x[1]) for x in d], index=ts.normalize(), name=kod)
        except (requests.ConnectionError, requests.Timeout):
            baglanti_hatasi += 1
            if ISY["basari"] == 0 and baglanti_hatasi >= 2:   # hic basari yokken 2 baglanti hatasi: kaynak kapali say
                ISY["down"] = True
                return pd.Series(dtype=float, name=kod)
        except (requests.RequestException, ValueError):
            pass
        time.sleep(1.5 * (k + 1))
        p["from"] = (bas - timedelta(days=k + 1)).strftime("%Y%m%d000000")
    if baglanti_hatasi == 3:
        ISY["hata_ardisik"] += 1
        if ISY["hata_ardisik"] >= 2:   # denetim 08.11: 3 -> 2 (her basarisiz seri ~35 sn yakiyor)
            ISY["down"] = True
    return pd.Series(dtype=float, name=kod)


def _supheli(s, bas):
    """Kesik bas ya da ortada > 20 takvim gunu delik (BIST'te en uzun tatil koprusu ~9-10 gun)."""
    return bool(s.index[0] > pd.Timestamp(bas) + pd.Timedelta(days=30) or (len(s) > 1 and s.index.to_series().diff().dt.days.max() > 20))


def isy_seri(kod, pxdir, bas, simdi, bekle, cevrimdisi):
    fn = os.path.join(pxdir, kod + ".csv")
    eski = None
    if os.path.exists(fn):
        try:
            eski = pd.read_csv(fn, index_col=0, parse_dates=True)["px"].astype(float)
        except Exception:
            eski = None
    if cevrimdisi or ISY["down"]:
        return eski if eski is not None else pd.Series(dtype=float)
    s = None
    if eski is not None and len(eski) and eski.index[0] <= pd.Timestamp(bas) + pd.Timedelta(days=10):
        yeni = isy_istek(kod, (eski.index[-1] - pd.Timedelta(days=15)).to_pydatetime(), simdi, bekle)
        if not len(yeni):
            s = eski
        else:
            ort = eski.index.intersection(yeni.index)
            fark = (yeni.reindex(ort) / eski.reindex(ort) - 1).abs().max() if len(ort) else np.inf
            # artimli guncelleme yalniz ortusen gunler tutuyorsa (duzeltme/bolunme yoksa) ve bosluk yoksa
            if len(ort) >= 3 and fark <= 0.002:
                s = pd.concat([eski[eski.index < yeni.index[0]], yeni])
    if s is None:
        s = isy_istek(kod, bas, simdi, bekle)
        # DENETIM 08.11: Is Yatirim aralikli olarak EKSIK gecmis donduruyor: bas tarafi kesik (GARAN yalniz son 1 yil;
        # MPARK/ULKER/ODAS/OTKAR 2024-03-29'dan) ya da ortada delik (BTCIM 2024-01-03..2024-03-28 yok). Ilk tarih istenenden
        # > 30 gun sonraysa ya da iki gun arasi > 20 takvim gunuyse bir kez daha iste; iki cevap ortusen gunlerde tutuyorsa
        # birlestir, tutmuyorsa uzun olani al (yeni halka arzlarda iki cevap ayni cikar).
        if len(s) and _supheli(s, bas) and not ISY["down"]:
            s2 = isy_istek(kod, bas - timedelta(days=3), simdi, bekle)
            ISY["kisa_tekrar"] = ISY.get("kisa_tekrar", 0) + 1
            if len(s2):
                ort = s.index.intersection(s2.index)
                if len(ort) >= 20 and (s2.reindex(ort) / s.reindex(ort) - 1).abs().max() <= 0.002:
                    s = s2.combine_first(s)
                elif len(s2) > len(s):
                    s = s2
            if _supheli(s, bas):
                ISY.setdefault("supheli", []).append(kod)
        if eski is not None and len(eski) and len(s) and len(eski.index.difference(s.index)):
            ort = eski.index.intersection(s.index)
            if len(ort) >= 20 and (s.reindex(ort) / eski.reindex(ort) - 1).abs().max() <= 0.002:
                s = s.combine_first(eski)   # onbellekteki daha uzun/deliksiz gecmisi koru (ortusen gunler tutuyorsa)
    s = s[~s.index.duplicated(keep="last")].sort_index()
    if len(s):
        s.rename("px").to_frame().to_csv(fn)
    return s


def isy_hacim(kod, veri, kesim, bekle, cevrimdisi):
    d = os.path.join(veri, "hacim"); os.makedirs(d, exist_ok=True)
    fn = os.path.join(d, kod + ".csv")
    eski = pd.read_csv(fn, index_col=0, parse_dates=True) if os.path.exists(fn) else None
    if cevrimdisi or ISY["down"]:
        return eski
    bas = (eski.index[-1] - pd.Timedelta(days=10)) if eski is not None and len(eski) else kesim - pd.Timedelta(days=120)
    p = {"hisse": kod, "startdate": bas.strftime("%d-%m-%Y"), "enddate": kesim.strftime("%d-%m-%Y")}
    yeni = None
    hata = 0
    for k in range(2):
        try:
            ISY["istek"] += 1
            r = S.get(HT_URL, params=p, timeout=30)
            if r.status_code == 200 and r.text.strip():
                v = r.json().get("value") or []
                if v:
                    ISY["hata_ardisik"] = 0
                    yeni = pd.DataFrame({"hacim": [x.get("HGDG_HACIM") for x in v], "ham": [x.get("HG_KAPANIS") for x in v]},
                                        index=pd.to_datetime([x["HGDG_TARIH"] for x in v], format="%d-%m-%Y"))
                break
            if r.status_code == 429:
                time.sleep(10 * (k + 1))
        except (requests.ConnectionError, requests.Timeout):
            hata += 1; time.sleep(2 * (k + 1))
        except (requests.RequestException, ValueError):
            time.sleep(2 * (k + 1))
    if hata == 2:
        ISY["hata_ardisik"] += 1
        if ISY["hata_ardisik"] >= 3:
            ISY["down"] = True
    time.sleep(bekle)
    if yeni is None:
        return eski
    s = yeni if eski is None else pd.concat([eski[eski.index < yeni.index[0]], yeni])
    s = s[~s.index.duplicated(keep="last")].sort_index().iloc[-260:]
    s.to_csv(fn)
    return s


# ---------------------------------------------------------------------------------------------------------------
# Borsa Istanbul bultenleri, FRED, CBOE, TCMB
def viop_iki_bulten(kesim, veri, bekle, cevrimdisi):
    """Son ve bir onceki VIOP bulteni (DataFrame, tarih). Cevrimdisi: yalniz onbellek."""
    if cevrimdisi:
        d = os.path.join(veri, "viop")
        fl = sorted(x for x in os.listdir(d) if x.startswith("viop_") and x <= f"viop_{kesim:%Y%m%d}.csv") if os.path.isdir(d) else []
        out = []
        for x in fl[-2:][::-1]:
            B, g = bt.viop_bulten(pd.Timestamp(x[5:13]), veri, geri=0)
            out.append((B, g))
        while len(out) < 2:
            out.append((None, None))
        return out[0], out[1]
    try:
        B1, g1 = bt.viop_bulten(kesim, veri, geri=5, bekle=bekle)
    except Exception:
        B1, g1 = None, None
    if B1 is None:
        return (None, None), (None, None)
    try:
        B0, g0 = bt.viop_bulten(g1 - pd.Timedelta(days=1), veri, geri=6, bekle=bekle)
    except Exception:
        B0, g0 = None, None
    return (B1, g1), (B0, g0)


def pay_bulteni_gun(g, veri, bekle, cevrimdisi=False):
    """Borsa Istanbul pay piyasasi gunluk bulteni (thbYYYYMMDD1.zip), tek gun: KOD -> kapanis, TL hacim. Yoksa None."""
    d = os.path.join(veri, "thb"); os.makedirs(d, exist_ok=True)
    g = pd.Timestamp(g).normalize()
    fn = os.path.join(d, f"thb{g:%Y%m%d}1.zip")
    icerik = open(fn, "rb").read() if os.path.exists(fn) else None
    if icerik is None and not cevrimdisi:
        r = al(THB_URL.format(g, g, g), timeout=40, deneme=2, bekle=bekle)
        if r is not None and r.content[:2] == b"PK":
            icerik = r.content
            open(fn, "wb").write(icerik)
    if not icerik:
        return None
    try:
        z = zipfile.ZipFile(io.BytesIO(icerik))
        ad = [n for n in z.namelist() if n.lower().endswith(".csv")][0]
        metin = z.read(ad).decode("utf-8", "replace").splitlines()
        bas = [x.strip() for x in metin[0].split(";")]
        i_kod, i_kap, i_hac = bas.index("ISLEM  KODU"), bas.index("KAPANIS FIYATI"), bas.index("TOPLAM ISLEM HACMI")
        sat = {}
        for x in metin[2:]:
            k = x.split(";")
            if len(k) > i_hac and k[i_kod].endswith(".E"):
                sat[k[i_kod][:-2]] = (pd.to_numeric(k[i_kap].replace(",", "."), errors="coerce"),
                                      pd.to_numeric(k[i_hac].replace(",", "."), errors="coerce"))
        return pd.DataFrame.from_dict(sat, orient="index", columns=["KAPANIS FIYATI", "TOPLAM ISLEM HACMI"])
    except Exception:
        return None


def pay_bulteni(tarih, veri, bekle, cevrimdisi=False):
    """tarih'ten geriye ilk bulunan pay bulteni (yedek kip)."""
    g = pd.Timestamp(tarih).normalize()
    for _ in range(5):
        while not is_gunu(g, TATIL_BIST):
            g -= pd.Timedelta(days=1)
        df = pay_bulteni_gun(g, veri, bekle, cevrimdisi)
        if df is not None:
            return df, g
        g -= pd.Timedelta(days=1)
    return None, None


def likidite_bulten(son, veri, bekle, cevrimdisi, n=60, butce=240):
    """Son n BIST gununun pay bultenlerinden 60g medyan TL hacim (PLAN_BIST s4.1 likidite sirasi).
    Doner: (medyan sozlugu, basarili gun sayisi, son bulten tarihi, son bulten DataFrame)."""
    gunler, g = [], pd.Timestamp(son).normalize()
    while len(gunler) < n:
        if is_gunu(g, TATIL_BIST):
            gunler.append(g)
        g -= pd.Timedelta(days=1)
    t0 = time.time(); V = {}; hata = 0; son_df = None; son_g = None
    for g in gunler:
        if time.time() - t0 > butce:
            break
        df = pay_bulteni_gun(g, veri, bekle, cevrimdisi)
        if df is None:
            hata += 1
            if not V and hata >= 3:
                break
            continue
        V[g] = df["TOPLAM ISLEM HACMI"]
        if son_df is None:
            son_df, son_g = df, g
    if not V:
        return {}, 0, None, None
    X = pd.DataFrame(V)
    X = X.where(X > 0)
    med = X.median(axis=1)[X.count(axis=1) >= min(20, max(len(V) // 2, 1))]
    return med.to_dict(), len(V), son_g, son_df


def fred(sid, veri, bekle, cevrimdisi):
    fn = os.path.join(veri, f"fred_{sid}.csv")
    metin = None
    if not cevrimdisi:
        r = al(FRED_URL.format(sid), timeout=40, bekle=bekle)
        if r is not None and r.text.lower().startswith("observation_date"):
            metin = r.text; open(fn, "w").write(metin)
    if metin is None and os.path.exists(fn):
        metin = open(fn).read()
    if not metin:
        return pd.Series(dtype=float)
    x = pd.read_csv(io.StringIO(metin))
    s = pd.to_numeric(x.iloc[:, 1], errors="coerce")
    s.index = pd.to_datetime(x.iloc[:, 0])
    return s.dropna()


def cboe(ad, veri, bekle, cevrimdisi):
    fn = os.path.join(veri, f"cboe_{ad}.csv")
    metin = None
    if not cevrimdisi:
        r = al(CBOE_URL.format(ad), timeout=40, bekle=bekle)
        if r is not None and r.text.startswith("DATE"):
            metin = r.text; open(fn, "w").write(metin)
    if metin is None and os.path.exists(fn):
        metin = open(fn).read()
    if not metin:
        return pd.Series(dtype=float)
    x = pd.read_csv(io.StringIO(metin))
    s = pd.to_numeric(x["CLOSE"], errors="coerce")
    s.index = pd.to_datetime(x["DATE"], format="%m/%d/%Y")
    return s.dropna()


def tcmb_usd(tarih, veri, bekle, cevrimdisi):
    """TCMB gosterge USD doviz satis kuru (15:30); tatilde geriye gider."""
    g = pd.Timestamp(tarih).normalize()
    d = os.path.join(veri, "tcmb"); os.makedirs(d, exist_ok=True)
    for _ in range(6):
        while g.weekday() >= 5:
            g -= pd.Timedelta(days=1)
        fn = os.path.join(d, f"{g:%Y%m%d}.xml")
        metin = open(fn, encoding="utf-8").read() if os.path.exists(fn) else None
        if metin is None and not cevrimdisi:
            r = al(TCMB_URL.format(g, g), timeout=30, deneme=2, bekle=bekle)
            if r is not None and "<Tarih_Date" in r.text:
                metin = r.text; open(fn, "w", encoding="utf-8").write(metin)
        if metin:
            i = metin.find('CurrencyCode="USD"')
            j = metin.find("<ForexSelling>", i); k = metin.find("</ForexSelling>", j)
            try:
                return float(metin[j + 14:k]), g
            except ValueError:
                pass
        g -= pd.Timedelta(days=1)
    return None, None


# ---------------------------------------------------------------------------------------------------------------
# Durum ve makro dosyalari
def makro_yukle(yol):
    yeni = not os.path.exists(yol)
    if yeni:
        M = {"aciklama": ("Elle girilen makro veriler (PLAN_BIST s2, s3 K6). Her Persembe 14:30 sonrasi TCMB rezervini ve ayin 3'unde "
                          "TUFE'yi guncelleyin, 'guncellendi' tarihini degistirin. Listeler eski -> yeni sirali; her hafta "
                          "net_rezerv_swap_haric listesine [etiket, mlr $] ekleyin. Ayrintilar: ../OTOMASYON.md"),
             "guncellendi": "2026-11-05",
             "kaynak": "PLAN_BIST.md ve BIST_GUNLUK_RUTIN.md 05.11.2026 degerleri"}
        M.update({k: v for k, v in bs.MAKRO_VARSAYILAN.items() if k != "kaynak"})
        M["net_rezerv_swap_haric"] = [["2026-10-29 yayini", 30.8], ["2026-11-05 yayini", 24.3]]
        M["tufe_aylik"] = [["2026-10", 2.58]]
        M.update({"kredili_esneklik_uzatildi": None, "ppk_10_12_surprizsiz_indirim": None, "msci_cikarilanlar": [],
                  "bilanco_aciklayanlar_9_11": []})
        json.dump(M, open(yol, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    M = dict(bs.MAKRO_VARSAYILAN)
    M.update(json.load(open(yol, encoding="utf-8")))
    return M, yeni


DURUM_BASLANGIC = {
    "aciklama": ("Kalici durum (gunluk_oneri.py her calismada okur ve yazar). 'ayarlar' ve 'acik_pozisyonlar' elle "
                 "duzenlenir; 'abd' blogu PLAN_ABD s2.2-2.6 sayaclaridir (elle duzeltme: OTOMASYON.md)."),
    "surum": 1,
    "son_calisma": None,
    "ayarlar": {"hesap_tl": 1000000, "pratik_sahol_akbnk": "kagit",
                "not": "pratik_sahol_akbnk: 'kagit' (PLAN_BIST K1 oncelikli, ayni ciftte iki sinyal calistirilmaz) ya da 'canli'"},
    "acik_pozisyonlar": [],
    "acik_pozisyon_ornegi": {"kol": "K4", "enstruman": "ENJSA", "yon": "AL", "giris_tarihi": "2026-11-10",
                             "giris_fiyati": 127.5, "adet": 100, "not": "kol: K1 | K4 | PRATIK_SAHOL | KOZA | ALTIN | TUPRS | XU030_BAZ"},
    "abd": {
        "son_tarih": "2026-11-06",
        "kaynak_notu": "Baslangic: tarama/abd_rejim_20261106.md (06.11 S&P kapanisi haber kaynagindan; FRED gelince teyit edilir)",
        "teyitsiz": {"2026-11-06": {"SPX": 7376.86}},
        "son_kapanis": {"SPX": 7376.86, "NDX": 26989.99},
        "ralli": {"SPX": {"dip": 7353.73, "dip_tarihi": "2026-11-05", "gun1": "2026-11-06", "gun": 1},
                  "NDX": {"dip": 26629.81, "dip_tarihi": "2026-11-05", "gun1": "2026-11-06", "gun": 1}},
        "ftd": None,
        "ftd_hacim_teyit": None,
        "sari_sayac": 0,
        "durum": "KIRMIZI",
        "pilot_freni": False,
        "manuel": {"s5fi": 62.5, "s5th": 66.1, "tarih": "2026-11-05",
                   "not": "INDEX:S5FI / INDEX:S5TH TradingView'dan elle; 3 gunden eskiyse kullanilmaz"},
        "gecmis": [{"tarih": "2026-11-05", "durum": "KIRMIZI", "neden": "a: VIX/VIX3M 1,10"},
                   {"tarih": "2026-11-06", "durum": "KIRMIZI", "neden": "a: VIX/VIX3M 1,04 (05.11: 1,10)"}],
    },
    "bist": {"son_tarih": None, "rejim": None, "kriz": None, "tetikler": []},
}


def durum_yukle(yol):
    if not os.path.exists(yol):
        D = json.loads(json.dumps(DURUM_BASLANGIC))
        return D, True
    D = json.load(open(yol, encoding="utf-8"))
    for k, v in DURUM_BASLANGIC.items():
        D.setdefault(k, json.loads(json.dumps(v)))
    return D, False


def _kok(fn, a, b, n=100):
    """fn(a) ve fn(b) zit isaretliyse kok (ikiye bolme); degilse nan."""
    fa, fb = fn(a), fn(b)
    if not (np.isfinite(fa) and np.isfinite(fb)) or fa * fb > 0:
        return np.nan
    for _ in range(n):
        m = (a + b) / 2; fm = fn(m)
        if (fm > 0) == (fa > 0):
            a, fa = m, fm
        else:
            b = m
    return (a + b) / 2


def k1_tetik_yarin(sah, akb, ps=None, pa=None, L=60):
    """K1 icin YARININ kapanisinda z=+-2 veren kesin fiyatlar (60 gunluk pencere bir gun kayar; obur bacak sabit).
    DENETIM 08.11: bist_sinyal.k1_tetikler bugunun degerini degistiriyordu (pencere kaymiyor; 06.11'de ~3-4 kurus fark)."""
    x = (np.log(sah) - np.log(akb)).dropna().values
    s0, a0 = float(ps if ps is not None else sah.iloc[-1]), float(pa if pa is not None else akb.iloc[-1])  # gercek son kapanis
    w0 = x[-(L - 1):]

    def z(xn):
        w = np.r_[w0, xn]; return (xn - w.mean()) / w.std(ddof=1)
    out = {}
    for tg in (2, -2):
        xn = _kok(lambda v: z(v) - tg, x[-1] - 1.0, x[-1] + 1.0)
        if np.isfinite(xn):
            d = xn - x[-1]
            out[f"SAHOL_z{tg:+d}"] = s0 * math.exp(d)
            out[f"AKBNK_z{tg:+d}"] = a0 * math.exp(-d)
    return out


# ---------------------------------------------------------------------------------------------------------------
# BIST hesaplari (bist_sinyal.py ile ayni tanimlar)
def bist_hesapla(D, HV, M, B, btar, b100, simdi, hesap):
    xu = D["XU100"]; son = xu.index[-1]
    tlref = D.get("TLREF"); usd = D.get("USDTRY")
    R = {"son": son}
    # 1. rejim
    xs50, xs200 = sma(xu, 50), sma(xu, 200)
    T1 = bool(xu.iloc[-1] > xs200.iloc[-1])
    T3 = bool((xu.iloc[-5:] > xs50.iloc[-5:]).all())
    xu12 = xu.iloc[-1] / xu.iloc[-253] - 1
    nakit12 = bs.nakit_getiri(tlref, xu.index[-253], son) if tlref is not None else np.nan
    T2 = bool(xu12 > max(nakit12 if np.isfinite(nakit12) else 0, 0.455))
    xb = D["XBANK"]; xb200 = sma(xb, 200)
    M5 = bool(xb.iloc[-1] > xb200.iloc[-1])
    nr = [v for _, v in M["net_rezerv_swap_haric"] if v is not None]
    nr_deg = list(np.diff(nr)) if len(nr) >= 2 else []
    M1 = bool(len(nr_deg) >= 3 and all(d > 0 for d in nr_deg[-3:]))
    tufe = [v for _, v in M["tufe_aylik"] if v is not None]
    M2 = bool(len(tufe) >= 2 and all(v < 2.0 for v in tufe[-2:]))
    cds, cds20, cds_ok = M.get("cds5y"), M.get("cds5y_20g_once"), bool(M.get("cds_teyitli"))
    M4 = bool(cds_ok and cds is not None and cds < 230 and cds20 is not None and cds < cds20)
    durum = "AÇIK" if T1 else ("GEÇİŞ" if (T3 and M1 and (M2 or M4 or M5)) else "KAPALI")
    R.update(T1=T1, T2=T2, T3=T3, M1=M1, M2=M2, M4=M4, M5=M5, durum=durum, acik=sum([T1, T2, T3, M1, M2, M4, M5]),
             xu=xu.iloc[-1], xs50=xs50.iloc[-1], xs200=xs200.iloc[-1], xu12=xu12, nakit12=nakit12,
             t2_esik=xu.iloc[-253] * (1 + max(nakit12 if np.isfinite(nakit12) else 0, 0.455)),
             xb=xb.iloc[-1], xb200=xb200.iloc[-1], nr=nr, nr_deg=nr_deg, tufe=M["tufe_aylik"], cds=cds, cds_ok=cds_ok)
    R["r0"] = {"AÇIK": 0.0075, "GEÇİŞ": 0.005, "KAPALI": 0.0025}[durum]
    R["k9_risk"] = 0.0025 if durum == "KAPALI" else 0.005
    # VIOP
    mev_net = M["mevduat_32g_brut"] * 0.825 / 100
    vsat, usd_on, hisse_vadeli = [], None, []
    if B is not None:
        def spot_at(k):
            s = D.get(k)
            return (s.loc[:btar].iloc[-1], s.loc[:btar].index[-1]) if s is not None and len(s.loc[:btar]) else (np.nan, None)
        S30, _ = spot_at("XU030")
        tl_b = tlref.loc[:btar].iloc[-1] / 100 if tlref is not None and len(tlref.loc[:btar]) else np.nan
        for _, x in B[B["SOZLESME KODU"].str.match(r"^F_XU030\d{4}$")].sort_values("VADE TARIHI").head(3).iterrows():
            T = (x["VADE TARIHI"] - btar).days
            if T <= 0 or not x["UZLASMA FIYATI"] > 0 or not np.isfinite(S30):
                continue
            basit = (x["UZLASMA FIYATI"] / S30 - 1) * 365 / T
            bil = (x["UZLASMA FIYATI"] / S30) ** (365 / T) - 1
            vsat.append(dict(kod=x["SOZLESME KODU"], vade=x["VADE TARIHI"].date(), T=T, F=x["UZLASMA FIYATI"], S=S30, basit=basit,
                             bil=bil, tlref=tl_b, esik=mev_net + 0.03, ac=basit >= mev_net + 0.03, hacim=x["ISLEM HACMI"],
                             ap=x["ACIK POZISYON"]))
        Su, _ = spot_at("USDTRY")
        ur = B[B["SOZLESME KODU"].str.match(r"^F_USDTRY\d{4}$")].sort_values("VADE TARIHI")
        ur = ur[(ur["VADE TARIHI"] - btar).dt.days > 5]
        if len(ur) and np.isfinite(Su):
            x = ur.iloc[0]; T = (x["VADE TARIHI"] - btar).days
            ima = ((x["UZLASMA FIYATI"] / Su) * (1 + M["usd_faiz"] * T / 360) - 1) * 365 / T
            usd_on = dict(kod=x["SOZLESME KODU"], F=x["UZLASMA FIYATI"], S=Su, T=T, ima=ima)
        for k in ["SAHOL", "AKBNK", "GARAN", "YKBNK", "KCHOL", "TUPRS", "THYAO", "TRALT", "TRMET"]:
            Sk, _ = spot_at(k)
            r = B[B["SOZLESME KODU"].str.match(rf"^F_{k}\d{{4}}$")].sort_values("VADE TARIHI")
            r = r[(r["VADE TARIHI"] - btar).dt.days > 3].head(2)
            for _, x in r.iterrows():
                T = (x["VADE TARIHI"] - btar).days
                if not (np.isfinite(Sk) and x["UZLASMA FIYATI"] > 0):
                    continue
                ima = (x["UZLASMA FIYATI"] / Sk - 1) * 365 / T
                hisse_vadeli.append([x["SOZLESME KODU"], T, f(x["UZLASMA FIYATI"]), f(Sk), f(ima, "%u"),
                                     f"{100 * (mev_net - ima):+.1f}".replace(".", ","), f(x["ISLEM HACMI"] / 1e6, "f0"),
                                     f(x["ACIK POZISYON"], "f0"),
                                     "E" if (mev_net - ima >= 0.03 and x["ACIK POZISYON"] >= 20000 and x["ISLEM HACMI"] >= 1e8 and T > 30) else "H"])
    R.update(vsat=vsat, usd_on=usd_on, hisse_vadeli=hisse_vadeli, mev_net=mev_net)
    # KRIZ
    kriz = {}
    r5 = xu.iloc[-1] / xu.iloc[-6] - 1
    kriz["a XU100 5 gün ≤ −%8"] = (f(r5, "%"), r5 <= -0.08)
    hiz = (usd.iloc[-1] / usd.iloc[-11]) ** (252 / 10) - 1 if usd is not None and len(usd) > 11 else np.nan
    kriz["b USDTRY 10g yıllık > %35"] = (f(hiz, "%"), bool(np.isfinite(hiz) and hiz > 0.35))
    kriz["c CDS > 300 (teyitli)"] = (f"{cds} (teyitli: {'E' if cds_ok else 'H'})", bool(cds_ok and cds is not None and cds > 300))
    nr_kriz = bool((len(nr_deg) >= 2 and all(d <= -5 for d in nr_deg[-2:])) or (nr and nr[-1] < 0))
    kriz["d net rezerv 2 hafta ≤ −5 mlr $ ya da < 0"] = (" / ".join(f(float(d), "f1") for d in nr_deg[-2:]) + " mlr $/hafta" if nr_deg else "—", nr_kriz)
    ekriz = bool(usd_on and usd_on["ima"] > M["politika_faizi"] / 100 + 0.05)
    kriz["e F_USDTRY ön ay ima > politika + 5"] = (f(usd_on["ima"], "%u") if usd_on else "bülten yok", ekriz)
    kriz["f MSCI danışma"] = ("evet" if M.get("msci_danisma") else "hayır", bool(M.get("msci_danisma")))
    R["kriz"] = kriz; R["kriz_var"] = any(v[1] for v in kriz.values()); R["hiz"] = hiz
    R["kriz_yakin"] = (len(nr_deg) >= 1 and nr_deg[-1] <= -5)
    # K6
    R["k6"] = {
        "1 net rezerv 2 hf ≥ −2 ve ≥ 20": bool(len(nr) >= 3 and nr[-1] - nr[-3] >= -2 and nr[-1] >= 20) if len(nr) >= 3
        else bool(len(nr) >= 2 and nr[-1] - nr[-2] >= -2 and nr[-1] >= 20),
        "2 yabancı DİBS ≥ −500 mn $": bool(M["yabanci_dibs_hafta_mn_usd"] is not None and M["yabanci_dibs_hafta_mn_usd"] >= -500),
        "3 F_USDTRY ima ≤ politika+5": bool(usd_on and not ekriz),
        "4 USDTRY 10g ≤ %30": bool(np.isfinite(hiz) and hiz <= 0.30),
        "5 brüt rezerv ≥ 160": bool(M["brut_rezerv"] is not None and M["brut_rezerv"] >= 160),
        "6 Kural 0": bool(M.get("kural0")),
    }
    # K4
    liq_tum = pd.Series(HV).dropna().sort_values(ascending=False)
    liq = liq_tum[liq_tum.index.isin(set(bt.VIOP) | set(b100))]
    lsira = pd.Series(np.arange(1, len(liq) + 1), index=liq.index)
    lsira_tum = pd.Series(np.arange(1, len(liq_tum) + 1), index=liq_tum.index)
    rows = []
    for k, c in D.items():
        if k in ("XU100", "XU030", "XBANK", "USDTRY", "TLREF") or len(c) < 260 or c.index[-1] < son:
            continue
        r = c.pct_change()
        s50, s150, s200 = sma(c, 50), sma(c, 150), sma(c, 200)
        z252 = c.iloc[-252:].max(); d252 = c.iloc[-252:].min()
        g = lambda n: c.iloc[-1] / c.iloc[-1 - n] - 1
        rows.append(dict(kod=k, kapanis=c.iloc[-1], b52=bool(c.iloc[-1] > c.iloc[-253:-1].max()), tetik=z252,
                         uzak=z252 / c.iloc[-1] - 1, tt_dizilim=bool(c.iloc[-1] > s50.iloc[-1] > s150.iloc[-1] > s200.iloc[-1]),
                         tt_egim=bool(s200.iloc[-1] > s200.iloc[-22]), tt_dip=bool(c.iloc[-1] >= 1.25 * d252),
                         tt_zirve=bool(c.iloc[-1] >= 0.75 * z252), sma50=s50.iloc[-1],
                         R=0.4 * g(63) + 0.2 * g(126) + 0.2 * g(189) + 0.2 * g(252), atr=r.abs().iloc[-14:].mean() * 1.25,
                         limit60=int((r.iloc[-60:].abs() >= 0.095).sum()), limit60_up=int((r.iloc[-60:] >= 0.095).sum()),
                         limit60_dn=int((r.iloc[-60:] <= -0.095).sum()), gecmis=len(c), viop=k in bt.VIOP))
    K = pd.DataFrame(rows).set_index("kod")
    K["lsira"] = lsira.reindex(K.index)
    rs_ev = [k for k in K.index if lsira_tum.get(k, 999) <= 150] if len(lsira_tum) >= 50 else list(K.index)
    K["rs"] = np.nan; K.loc[rs_ev, "rs"] = bs.yuzdelik(K.loc[rs_ev, "R"])
    K["tt_rs"] = K.rs >= 80
    stok_kume = {u: kk for kk, uu in bs.KUMELER.items() for u in uu}; stok_kume.update(bs.K4_KUME_OZEL)
    K["kume"] = [stok_kume.get(k, "—") for k in K.index]
    K["blok"] = [bs.BLOK.get(stok_kume.get(k, ""), "Diğer") for k in K.index]
    msci_cik = set(M.get("msci_cikarilanlar") or [])

    def dislama(k):
        n = []
        if k in bs.DISLAMA_KOD: n.append(bs.DISLAMA_KOD[k])
        if K.at[k, "limit60"] >= 3: n.append(f"60g'de {K.at[k, 'limit60']} limit kapanış")
        if K.at[k, "gecmis"] < 252: n.append("<252 gün")
        if k in msci_cik: n.append("MSCI'dan çıkarıldı (30.11'e kadar alınmaz)")
        return "; ".join(n)
    K["dislama"] = [dislama(k) for k in K.index]
    K["evren75"] = K.lsira <= 75
    K["tt_tam"] = K.tt_dizilim & K.tt_egim & K.tt_dip & K.tt_zirve & K.tt_rs
    K["nitelikli"] = K.b52 & K.tt_tam & K.evren75 & (K.dislama == "")
    K["stop"] = [0.25 if (k in bs.LIMIT_ISIM or K.at[k, "atr"] > 0.045) else 0.15 for k in K.index]
    K["nominal"] = R["r0"] * np.where(K.viop, 1.0, 0.75) / K.stop
    K["tl"] = [min(K.at[k, "nominal"] * hesap, 0.02 * HV.get(k, np.inf)) for k in K.index]
    R["K"] = K
    R["nit"] = K[K.nitelikli].sort_values("rs", ascending=False)
    R["izle"] = K[(~K.nitelikli) & (K.dislama == "") & (K.lsira <= 100) & (K.uzak <= 0.15) &
                  ((K.tt_dizilim.astype(int) + K.tt_egim + K.tt_dip + K.tt_zirve + K.tt_rs) >= 4)].sort_values("uzak")
    R["liq_n"] = len(liq)
    # kume RS
    ks = []
    nakit3 = bs.nakit_getiri(tlref, xu.index[-64], son) if tlref is not None else np.nan
    for kk, uu in bs.KUMELER.items():
        rr = []
        for u in uu:
            s = D.get(u)
            if s is None or len(s) < 150: continue
            r = s.pct_change(); r = r.mask(r.abs() > 0.35, 0.0); r.iloc[:21] = np.nan
            rr.append(r.rename(u))
        if len(rr) < 2: continue
        Rr = pd.concat(rr, axis=1, sort=True).reindex(xu.index)
        ew = (1 + Rr.mean(axis=1).fillna(0)).cumprod()
        rel = ew / xu
        if rel.notna().sum() < 260: continue
        h126 = rel.iloc[-126:]
        ks.append(dict(kume=kk, blok=bs.BLOK.get(kk, "Diğer"), rs12=rel.iloc[-1] / rel.iloc[-253] - 1,
                       rel3=rel.iloc[-1] / rel.iloc[-64] - 1, tl3=ew.iloc[-1] / ew.iloc[-64] - 1,
                       gun126=int(len(h126) - 1 - int(np.argmax(h126.values))),
                       gen50=np.mean([D[u].iloc[-1] > sma(D[u], 50).iloc[-1] for u in Rr.columns if len(D[u]) >= 50])))
    R["KS"] = pd.DataFrame(ks).sort_values("rs12", ascending=False).reset_index(drop=True) if ks else pd.DataFrame()
    R["nakit3"] = nakit3
    # K1 / K2 (60 gun, bugun dahil)
    sah, akb = bs.temiz_fiyat(D["SAHOL"]), bs.temiz_fiyat(D["AKBNK"])
    x1 = (np.log(sah) - np.log(akb)).dropna(); z1 = bs.z_seri(x1)
    R["z1"] = z1; R["k1_tet"] = k1_tetik_yarin(sah, akb, D["SAHOL"].iloc[-1], D["AKBNK"].iloc[-1]); R["kes1"] = bs.son_kesisim(z1)
    kc = bs.temiz_fiyat(D["KCHOL"])
    sep = pd.concat([bs.temiz_fiyat(D[u]) for u in bs.K2_SEPET if u in D], axis=1)
    bk = np.exp(np.log(sep).diff().mean(axis=1).fillna(0).cumsum())
    z2 = bs.z_seri((np.log(kc) - np.log(bk)).dropna())
    R["z2"] = z2; R["kes2"] = bs.son_kesisim(z2)
    # K1 model (t+1 giris, 20 is gunu tutma) - yalnizca bilgi
    zz = z1.dropna(); pos = None; son_islem = None
    idx = list(zz.index)
    for i, t in enumerate(idx):
        if pos is not None and i >= pos["cikis_i"]:
            son_islem = pos; pos = None
        if pos is None and abs(zz.iloc[i]) >= 2:
            pos = dict(sinyal=t, yon=-int(np.sign(zz.iloc[i])), giris_i=i + 1, cikis_i=i + 1 + 20, z=zz.iloc[i])
    R["k1_model"] = pos; R["k1_son"] = son_islem; R["k1_idx"] = idx
    return R


# ---------------------------------------------------------------------------------------------------------------
# PRATIK 1-3 gun sinyalleri
def pr_temiz_getiri(s, cal):
    """sinyal.py clean_ret: log getiri, BIST takvimi, |basit getiri| > %10,5 (13.03.2020 oncesi %20,5) -> NaN.
    Not: Is Yatirim'da hacim/yuksek/dusuk olmadigi icin 'bayat gun' filtresi uygulanamaz."""
    s = s[s > 0]
    cal = cal[cal >= s.index[0]]
    s = s.reindex(s.index.union(cal)).ffill().reindex(cal)
    r = np.log(s).diff()
    lim = pd.Series(np.where(r.index < pd.Timestamp("2020-03-13"), 0.205, 0.105), index=r.index)
    r[(np.expm1(r).abs() > lim)] = np.nan
    return r


def pr_sahol(D, hesap, risk=0.0025, Fs=None, Fa=None):
    cal = D["XU100"].index
    rA, rB = pr_temiz_getiri(D["SAHOL"], cal), pr_temiz_getiri(D["AKBNK"], cal)
    idx = rA.index.intersection(rB.index); rA, rB = rA.reindex(idx), rB.reindex(idx)
    braw = rA.rolling(250, min_periods=125).cov(rB) / rB.rolling(250, min_periods=125).var()
    beta = braw.shift(1)
    Sg = (rA - beta * rB).fillna(0).cumsum()
    z = (Sg - Sg.rolling(60, min_periods=30).mean()) / Sg.rolling(60, min_periods=30).std()
    # durum makinesi (sinyal.py simulate; giris |z|>1,5 bolumunun ilk gunu, cikis |z|<=1,5)
    zz = z.values; ep = np.where(np.abs(zz) > 1.5, np.sign(zz), 0.0); ep[np.isnan(zz)] = 0
    side = 0; last_ep = 0; k = 0; held = 0; T = []; act = "BEKLE"
    for i in range(len(zz)):
        if ep[i] != 0 and (i == 0 or ep[i] != ep[i - 1]): k += 1
        eid = k if ep[i] != 0 else 0; act = "BEKLE" if side == 0 else "TUT"
        if side != 0:
            held += 1
            if not np.isnan(zz[i]) and side * zz[i] >= -1.5:
                T[-1].update(cikis=z.index[i], gun=held); side = 0; act = "KAPAT"
        if side == 0 and ep[i] != 0 and eid != last_ep and not np.isnan(beta.values[i]):
            side = int(-ep[i]); last_ep = eid; held = 0
            T.append(dict(giris=z.index[i], yon=side, z=zz[i], beta=beta.values[i], cikis=None, gun=None))
            act = ("KAPAT + " if act == "KAPAT" else "") + ("AÇ LONG" if side > 0 else "AÇ SHORT")
    pa, pb = D["SAHOL"].iloc[-1], D["AKBNK"].iloc[-1]
    Sv = Sg.values

    def tetik(target):
        def zx(x):
            w = np.r_[Sv[-59:], Sv[-1] + x]; return (w[-1] - w.mean()) / w.std(ddof=1)
        lo, hi = (-0.6, 0.0) if target < 0 else (0.0, 0.6)
        if (zx(lo) - target) * (zx(hi) - target) > 0: return np.nan
        for _ in range(80):
            m = (lo + hi) / 2
            if (zx(m) - target) * (zx(lo) - target) <= 0: hi = m
            else: lo = m
        return (lo + hi) / 2
    bn = braw.iloc[-1]
    tet = {}
    for tg in (1.5, -1.5):
        x = tetik(tg)
        tet[tg] = (pa * np.exp(x), pb * np.exp(-x / bn)) if np.isfinite(x) else (np.nan, np.nan)
    b = beta.iloc[-1]
    fa, fb = (Fs or pa), (Fa or pb)
    na_ = max(int(np.floor(hesap * risk / (0.09 * fa * 100))), 1); nb_ = int(round(na_ * b * fa / fb)) if np.isfinite(b) else 0
    return dict(z=z, beta=b, beta_yarin=bn, side=side, held=held, act=act, T=T, tet=tet, pa=pa, pb=pb, n=(na_, nb_),
                tarih=z.index[-1], fa=fa, fb=fb)


def pr_koza(D, hesap, risk):
    syms = ["TRMET", "TRALT", "TRENJ", "XU030"]
    if any(s not in D for s in syms):
        return None
    R = {}
    for s in syms:
        a = D[s]
        r = np.log(a / a.shift(1))
        if s != "XU030":
            pre = r.index < pd.Timestamp("2020-03-13")
            up = np.where(pre, np.log(1.205), np.log(1.105)); dn = np.where(pre, np.log(0.795), np.log(0.895))
            r = r.mask((r > up) | (r < dn))
        R[s] = r
    R = pd.DataFrame(R).dropna(how="all")
    y, h = R.TRMET, R.TRALT
    grp = pd.concat([h, R.TRENJ], axis=1).mean(axis=1, skipna=False)
    beta = lambda yy, xx: (yy.rolling(250, min_periods=120).cov(xx) / xx.rolling(250, min_periods=120).var()).shift(1)
    b_g = beta(y, grp).clip(0.2, 2.0)
    u = y - b_g * grp
    sd60 = u.rolling(60, min_periods=40).std()
    z3 = u.rolling(3, min_periods=3).sum() / (sd60 * np.sqrt(3))
    bH = beta(y, h).clip(0.3, 2.0)
    Sg = pd.DataFrame({"z3": z3, "bH": bH, "u": u, "sd60": sd60, "b_g": b_g}).dropna(subset=["z3", "bH"], how="all")
    # pratik kural yeniden oynatma (sinyal_koza.py replay; kilit vekili spot |r| > %9,5)
    Sx = Sg.iloc[-400:]
    zv = Sx.z3.values; act = np.where(np.isfinite(zv) & (np.abs(zv) > 1.5), np.sign(zv), 0.0)
    rr = R.reindex(Sx.index)
    lock = ((rr.TRMET.abs() > np.log(1.095)) | (rr.TRALT.abs() > np.log(1.095))).values
    trades, pos, block = [], None, 0.0
    for i in range(len(Sx)):
        if pos is not None and i == pos["exit"]:
            if act[i] == pos["s"] and pos["exit"] - pos["i0"] + 2 <= 6:
                pos["exit"] += 2; pos["ext"] += 1
                continue
            pos["out"] = i; trades.append(pos); block = pos["s"] if act[i] == pos["s"] else 0.0; pos = None
        if pos is None:
            if block and act[i] != block: block = 0.0
            if act[i] != 0 and act[i] != block and not lock[i]:
                pos = dict(i0=i, s=act[i], exit=i + 2, ext=0, b=Sx.bH.values[i], z=zv[i])
    L = Sg.iloc[-1]
    PM, PH = D["TRMET"].iloc[-1], D["TRALT"].iloc[-1]
    s2 = Sg.u.iloc[-2:].sum()
    # DENETIM 08.11: yarinin sigma60'i yarinin artigini da icerir (sinyal_koza.py 'sigma60 sabit' yaklasimi tetigi
    # 06.11'de ~%0,15-0,35 dar veriyordu); TRALT ve TRENJ yatayken grp = 0 -> u_yarin = r_TRMET, kesin cozum:
    uw = Sg.u.values[-59:]

    def z3_yarin(un):
        w = np.r_[uw, un]; w = w[np.isfinite(w)]
        return (s2 + un) / (np.std(w, ddof=1) * np.sqrt(3)) if len(w) >= 40 else np.nan
    up = _kok(lambda v: z3_yarin(v) - 1.5, -0.2, 0.2); dn = _kok(lambda v: z3_yarin(v) + 1.5, -0.2, 0.2)
    if not np.isfinite(up): up = 1.5 * L.sd60 * np.sqrt(3) - s2
    if not np.isfinite(dn): dn = -1.5 * L.sd60 * np.sqrt(3) - s2
    G = min(hesap * risk / 0.0205, hesap)
    nM = max(int(round(G / (1 + L.bH) / (100 * PM))), 1); nH = int(round(L.bH * nM * PM / PH))
    return dict(z3=Sg.z3, L=L, tarih=Sg.index[-1], idx=Sx.index, trades=trades, pos=pos, kilit=bool(lock[-1]),
                tet_al=PM * np.exp(up), tet_sat=PM * np.exp(dn), PM=PM, PH=PH, G=G, n=(nM, nH))


def on_vade(B, dayanak, btar, min_gun=3, sonra=None):
    """Bultende dayanagin en yakin vadesi (vadeye > min_gun kalan; 'sonra' verilirse vade > sonra)."""
    if B is None:
        return None
    r = B[B["SOZLESME KODU"].str.match(rf"^F_{dayanak}\d{{4}}$")].sort_values("VADE TARIHI")
    r = r[(r["VADE TARIHI"] - btar).dt.days > min_gun]
    if sonra is not None:
        r = r[r["VADE TARIHI"] > pd.Timestamp(sonra)]
    return r.iloc[0] if len(r) else None


def pr_altin(B, btar, D, hesap):
    """VIOP ons altin on vade UZLASMA degisimi (arastirmanin asil sinyali; pratikte 17:55 TVC:GOLD)."""
    x = on_vade(B, "XAUUSD", btar, min_gun=3)
    if x is None:
        return None
    onceki = pd.to_numeric(str(x["ONCEKI UZLASMA FIYATI"]).replace(",", "."), errors="coerce")
    if not (onceki and onceki > 0 and x["UZLASMA FIYATI"] > 0):
        return None
    g = math.log(x["UZLASMA FIYATI"] / onceki)
    sig = 0.0170
    out = dict(kod=x["SOZLESME KODU"], F=x["UZLASMA FIYATI"], F0=onceki, g=g, sig=sig, z=g / sig)
    if "TRALT" in D and "XU030" in D:
        rT = np.log(D["TRALT"]).diff(); rX = np.log(D["XU030"]).diff()
        j = pd.concat([rT, rX], axis=1).dropna().iloc[-250:]
        bta = j.iloc[:, 0].cov(j.iloc[:, 1]) / j.iloc[:, 1].var()
        xt, tr = D["XU030"].iloc[-1], D["TRALT"].iloc[-1]
        out.update(beta=bta, N=int(round(10 * xt / (bta * 100 * tr))) if bta > 0 else None, xu030=xt, tralt=tr)
    return out


def pr_baz(B1, g1, B0, g0, D):
    """XU030 vadelisi kapanis bazi: b = ln(F_kapanis / S_kapanis); ayni sozlesmede gunluk degisim; sigma ~50 bps."""
    if B1 is None or B0 is None or "XU030" not in D:
        return None
    s = D["XU030"]
    if g1 not in s.index or g0 not in s.index:
        return None
    r1 = B1[B1["SOZLESME KODU"].str.match(r"^F_XU030\d{4}$")].sort_values("VADE TARIHI")
    r1 = r1[(r1["VADE TARIHI"] - g1).dt.days > 1]
    if not len(r1):
        return None
    x1 = r1.iloc[0]
    x0 = B0[B0["SOZLESME KODU"] == x1["SOZLESME KODU"]]
    if not len(x0) or not (x1["KAPANIS FIYATI"] > 0 and x0.iloc[0]["KAPANIS FIYATI"] > 0):
        return None
    b1 = math.log(x1["KAPANIS FIYATI"] / s.loc[g1]); b0 = math.log(x0.iloc[0]["KAPANIS FIYATI"] / s.loc[g0])
    sig = 0.0050
    return dict(kod=x1["SOZLESME KODU"], F=x1["KAPANIS FIYATI"], Fu=x1["UZLASMA FIYATI"], S=s.loc[g1], b=b1, b0=b0, db=b1 - b0,
                z=(b1 - b0) / sig, sig=sig, oran_ust=math.exp(b1 + sig), oran_alt=math.exp(b1 - sig),
                F_ust=s.loc[g1] * math.exp(b1 + sig), F_alt=s.loc[g1] * math.exp(b1 - sig))


# ---------------------------------------------------------------------------------------------------------------
# ABD rejimi (PLAN_ABD s2.2-2.6)
def abd_guncelle(A, spx_f, ndx_f, vix, vix3m):
    """durum['abd'] sozlugunu yeni FRED gunleriyle ileri sarar. Doner: (A, rapor sozlugu)."""
    notlar = []
    spx = spx_f.copy()
    for t, v in list(A.get("teyitsiz", {}).items()):
        t_ = pd.Timestamp(t)
        if t_ in spx.index:
            fark = spx.loc[t_] / v["SPX"] - 1
            if abs(fark) > 0.001:
                notlar.append(f"{t} S&P teyitsiz kapanış {f(v['SPX'])} ≠ FRED {f(spx.loc[t_])} (fark {f(fark, '%')}); sayaçlar elle kontrol edilmeli.")
            del A["teyitsiz"][t]
        else:
            spx.loc[t_] = v["SPX"]
    spx = spx.sort_index()
    ndx = ndx_f.sort_index()
    vr = (vix / vix3m).dropna()
    s10, s20, s50, s200 = sma(spx, 10), sma(spx, 20), sma(spx, 50), sma(spx, 200)
    n10, n20 = sma(ndx, 10), sma(ndx, 20)
    son_t = pd.Timestamp(A["son_tarih"])
    # DENETIM 08.11: bir gun ancak VIX/VIX3M (ve NDX) o gun icin yayimlanmissa islenir; yoksa sonraki calismaya kalir
    # (eskiden VIX'i gec gelen gun bir kez 'kosul yok' sayilip SARI sayaci sifirlaniyordu).
    yeni = []
    for t in spx_f.index:
        if t <= son_t:
            continue
        if t not in vr.index or (t not in ndx.index and (not len(ndx) or ndx.index[-1] < t)):
            notlar.append(f"{t.date()} ABD kapanışı henüz işlenmedi: " + ("VIX/VIX3M" if t not in vr.index else "Nasdaq-100") +
                          " verisi yok (sonraki çalışmada işlenir).")
            break
        yeni.append(t)

    def kosullar(t):
        i = spx.index.get_loc(t)
        tp = spx.index[i - 1]
        vs = vr.loc[:t]
        if len(vs) and vs.index[-1] == t:
            vr_t = vs.iloc[-1]; vr_p = vs.iloc[-2] if len(vs) >= 2 else np.nan
        else:
            vr_t = np.nan; vr_p = vs.iloc[-1] if len(vs) else np.nan
        ka = bool((np.isfinite(vr_t) and vr_t >= 1) or (np.isfinite(vr_p) and vr_p >= 1))
        kb = bool(spx.loc[t] < s200.loc[t] and spx.loc[tp] < s200.loc[tp])
        man = A.get("manuel") or {}
        kc = None
        if man.get("s5fi") is not None and man.get("tarih") and (t - pd.Timestamp(man["tarih"])).days <= 3:
            kc = bool(man["s5fi"] < 50 and man.get("s5th", 100) < 60)
        return dict(vr=vr_t, vr_onceki=vr_p, ka=ka, kb=kb, kc=kc, spx=spx.loc[t], s10=s10.loc[t], s20=s20.loc[t],
                    s50=s50.loc[t], s200=s200.loc[t])

    for t in yeni:
        i = spx.index.get_loc(t); tp = spx.index[i - 1]
        c, p = spx.loc[t], spx.loc[tp]
        gun_deg = {}
        for ad, ser, cc, pp in (("SPX", spx, c, p), ("NDX", ndx, ndx.get(t, np.nan), ndx.loc[:t].iloc[-2] if len(ndx.loc[:t]) >= 2 else np.nan)):
            Rl = A["ralli"][ad]
            if not np.isfinite(cc) or not np.isfinite(pp) or (ad == "NDX" and t not in ndx.index):
                continue
            if cc < Rl["dip"]:
                Rl.update(dip=float(cc), dip_tarihi=str(t.date()), gun1=None, gun=0)
                if A.get("ftd") and A["ftd"].get("endeks") == ad:
                    notlar.append(f"{t.date()}: {ad} ralli dibinin altında kapandı → FTD geçersiz, sayım sıfırlandı.")
                    A["ftd"] = None; A["ftd_hacim_teyit"] = None
            elif Rl["gun1"] is None:
                if cc > pp:
                    Rl.update(gun1=str(t.date()), gun=1)
            else:
                Rl["gun"] += 1
            gun_deg[ad] = cc / pp - 1
            if Rl["gun"] >= 4 and cc / pp - 1 >= 0.015 and not A.get("ftd"):
                A["ftd"] = dict(tarih=str(t.date()), endeks=ad, degisim=round(cc / pp - 1, 4), dip=Rl["dip"], seans=0)
                A["ftd_hacim_teyit"] = None
                notlar.append(f"{t.date()}: {ad} " + f"+%{100 * (cc / pp - 1):.2f}".replace(".", ",") + f" ile FTD ADAYI (ralli {Rl['gun']}. gün). Hacim teyidi elle: SPY/QQQ hacmi önceki günden yüksek mi?")
        # FTD gecerlilik
        if A.get("ftd"):
            fd = A["ftd"]
            if pd.Timestamp(fd["tarih"]) < t:
                fd["seans"] = fd.get("seans", 0) + 1
            # DENETIM 08.11: 10>20 FTD'den sonraki 15 seans icinde BIR KEZ olustuysa FTD gecerli kalir (eskiden 15. seanstan
            # sonra 10<20 olan her gun FTD siliniyordu)
            if fd["seans"] <= 15 and (s10.loc[t] > s20.loc[t] or (t in n10.index and n10.loc[t] > n20.loc[t])):
                fd["olustu_1020"] = True
            if fd.get("gun_dibi") and c < float(fd["gun_dibi"]):
                fd["gun_dibi_kirildi"] = True   # PLAN_ABD s2.2 YESIL: FTD gunu dibi kapanisla kirilmamis olmali (dip elle girilir)
            if A.get("ftd_hacim_teyit") is False:
                notlar.append(f"FTD {fd['tarih']} hacim teyidi 'false' → geçersiz sayıldı."); A["ftd"] = None
            elif fd["seans"] >= 15 and not fd.get("olustu_1020"):
                notlar.append(f"{t.date()}: FTD {fd['tarih']} sonrası 15 seansta 10>20 oluşmadı → FTD geçersiz."); A["ftd"] = None
        k = kosullar(t)
        kirmizi = k["ka"] or k["kb"] or bool(k["kc"])
        ftd_ok = bool(A.get("ftd"))
        tetik = ftd_ok or bool(k["s10"] > k["s20"])
        if A.get("pilot_freni"):
            tetik = tetik and ftd_ok and bool(k["spx"] > k["s50"])
        sari_k = (not kirmizi) and np.isfinite(k["vr"]) and bool(k["spx"] > k["s200"]) and tetik  # VIX o gun yoksa sayac ilerlemez
        A["sari_sayac"] = A.get("sari_sayac", 0) + 1 if sari_k else 0
        ndx_ok = bool(t in n10.index and n10.loc[t] > n20.loc[t] and n10.diff().loc[t] > 0 and n20.diff().loc[t] > 0)
        s5fi_ok = (A.get("manuel") or {}).get("s5fi") is not None and k["kc"] is not None and A["manuel"]["s5fi"] >= 50
        on_seans = bool((s10 > s20).loc[:t].iloc[-10:].all() and t in n10.index and (n10 > n20).loc[:t].iloc[-10:].all())
        yesil = (A["sari_sayac"] >= 3 and k["spx"] > k["s50"] and k["spx"] > k["s200"] and ndx_ok and np.isfinite(k["vr"])
                 and k["vr"] < 0.95 and s5fi_ok and ((ftd_ok and not A["ftd"].get("gun_dibi_kirildi")) or on_seans))
        durum = "KIRMIZI" if kirmizi else ("YEŞİL" if yesil else ("SARI" if A["sari_sayac"] >= 3 else "TURUNCU"))
        neden = []
        if k["ka"]: neden.append(f"a: VIX/VIX3M {f(k['vr'])} / önceki {f(k['vr_onceki'])}")
        if k["kb"]: neden.append("b: S&P 2 kapanış 200 GHO altında")
        if k["kc"]: neden.append("c: S5FI<50 ve S5TH<60")
        A["durum"] = durum
        A["gecmis"] = (A.get("gecmis") or [])[-40:] + [dict(tarih=str(t.date()), durum=durum, neden="; ".join(neden) or "—",
                                                            sari_sayac=A["sari_sayac"], spx=round(float(c), 2))]
        A["son_tarih"] = str(t.date())
        A["son_kapanis"]["SPX"] = round(float(c), 2)
        if t in ndx.index:
            A["son_kapanis"]["NDX"] = round(float(ndx.loc[t]), 2)
    # rapor (son islenen gun)
    t = pd.Timestamp(A["son_tarih"])
    if t not in spx.index:
        return A, dict(hata="S&P serisi yok", notlar=notlar)
    k = kosullar(t)
    i = spx.index.get_loc(t)
    rap = dict(t=t, k=k, notlar=notlar, spx=spx, ndx=ndx, vr=vr, s200=s200, ndx_t=ndx.loc[:t].index[-1] if len(ndx.loc[:t]) else None,
               n10=n10.loc[:t].iloc[-1] if len(n10.loc[:t]) else np.nan, n20=n20.loc[:t].iloc[-1] if len(n20.loc[:t]) else np.nan,
               yeni=[str(x.date()) for x in yeni], spx_fred_son=spx_f.index[-1] if len(spx_f) else None,
               vix_son=vix.index[-1] if len(vix) else None, teyitsiz=bool(A.get("teyitsiz")),
               spx_d=spx.iloc[i] / spx.iloc[i - 1] - 1)
    # en erken tarihler (ABD seanslari)
    def ileri(n):
        return sonraki(t, n, TATIL_ABD)
    vr_son = vr.loc[:t]
    n_vix = 0 if (len(vr_son) >= 2 and vr_son.iloc[-1] < 1 and vr_son.iloc[-2] < 1) else (1 if (len(vr_son) and vr_son.iloc[-1] < 1) else 2)
    Rs = A["ralli"]["SPX"]; Rn = A["ralli"]["NDX"]
    if A.get("ftd") or k["s10"] > k["s20"]:
        n_tet = 0
    else:
        g_max = max(Rs["gun"] if Rs["gun1"] else 0, Rn["gun"] if Rn["gun1"] else 0)
        n_tet = max(4 - g_max, 1) if g_max > 0 else 4
    if A["sari_sayac"] > 0:
        n_sari = max(3 - A["sari_sayac"], 0)
    else:
        n_sari = max(n_vix, n_tet, 1) + 2
    rap["en_erken"] = dict(kirmizi_cikis=ileri(n_vix) if n_vix else t, ftd=ileri(n_tet) if n_tet else None,
                           sari=ileri(n_sari) if n_sari else t, pilot=ileri(n_sari + 1) if n_sari else ileri(1))
    return A, rap


# ---------------------------------------------------------------------------------------------------------------
def takvim_bayraklari(bas, gun=14):
    bas = pd.Timestamp(bas).normalize(); bit = bas + pd.Timedelta(days=gun)
    out = []
    for b, e, p, o, kural, blok in TAKVIM:
        b_, e_ = pd.Timestamp(b), pd.Timestamp(e)
        if e_ >= bas and b_ <= bit:
            out.append((b_, e_, p, o, kural, blok))
    return sorted(out, key=lambda x: x[0])


def giris_engeli(tarih, kol, isim=None, bilanco=set(), aciklayan=set()):
    """tarih kapanisinda kol icin yeni giris engeli varsa neden metni; yoksa ''."""
    t = pd.Timestamp(tarih).normalize()
    for b, e, p, o, kural, blok in TAKVIM:
        if p != "BIST" or not (pd.Timestamp(b) <= t <= pd.Timestamp(e)):
            continue
        kl = blok.get("kol")
        if kl == "TUM" or (isinstance(kl, list) and kol in kl):
            return f"{o}: {kural}"
        if blok.get("isim") == "BILANCO" and isim is not None:
            isimler = [isim] if isinstance(isim, str) else list(isim)
            bek = [i for i in isimler if i in bilanco and i not in aciklayan]
            if bek:
                return f"A1: {', '.join(bek)} bilançosu 9.11 18:00'e kadar açıklanmadıysa giriş yok"
    return ""


# ---------------------------------------------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Gunluk oneri raporu (BIST/VIOP + ABD rejimi)")
    ap.add_argument("--cikti", required=True, help="cikti klasoru (oneri_*.md, SON.md, BILDIRIM.txt, durum.json, makro.json)")
    ap.add_argument("--veri", default=None, help="ham veri onbellegi (varsayilan: gecici klasor; depoya konmaz)")
    ap.add_argument("--tarih", default=None, help="BIST kesim tarihi YYYY-MM-DD (varsayilan: son tam kapanis)")
    ap.add_argument("--bas", default="2023-06-01", help="fiyat verisi baslangici")
    ap.add_argument("--bekle", type=float, default=0.4, help="istekler arasi bekleme (sn)")
    ap.add_argument("--butce", type=float, default=540, help="Is Yatirim indirmesi icin zaman butcesi (sn, calisma basindan)")
    ap.add_argument("--isy-son", type=float, default=360, help="Is Yatirim kapaliysa en son yoklama zamani (sn, calisma basindan)")
    ap.add_argument("--cevrimdisi", action="store_true", help="hic istek atma; onbellekten oku (deneme)")
    ap.add_argument("--durum-yazmadan", action="store_true", help="durum.json'u guncelleme (deneme)")
    a = ap.parse_args()
    veri = a.veri or tempfile.mkdtemp(prefix="gunluk_veri_")
    pxdir = os.path.join(veri, "px")
    for d in (veri, pxdir, a.cikti):
        os.makedirs(d, exist_ok=True)
    simdi = datetime.now(TSI)
    bugun = pd.Timestamp(simdi.date())
    seans_bitmedi = simdi.weekday() < 5 and simdi.hour * 60 + simdi.minute < 18 * 60 + 20
    kesim = pd.Timestamp(a.tarih) if a.tarih else (bugun - pd.Timedelta(days=1) if seans_bitmedi else bugun)
    beklenen_bist = onceki_veya_ayni(kesim)
    print(f"gunluk_oneri: {simdi:%Y-%m-%d %H:%M} TSI, kesim {kesim.date()}, veri {veri}", flush=True)

    M, makro_yeni = makro_yukle(os.path.join(a.cikti, "makro.json"))
    DUR, durum_yeni = durum_yukle(os.path.join(a.cikti, "durum.json"))
    hesap = float(DUR["ayarlar"].get("hesap_tl", 1e6))
    makro_yas = (bugun - pd.Timestamp(M.get("guncellendi", "2000-01-01"))).days

    # ---- BIST verisi ----------------------------------------------------------------------------------------------
    if a.cevrimdisi and os.path.exists(os.path.join(veri, "endeks_kap.json")):
        _e = json.load(open(os.path.join(veri, "endeks_kap.json"))); b100, b50, kap_k = _e["XU100"], _e["XU050"], "KAP önbellek"
    elif a.cevrimdisi:
        b100, b50, kap_k = bt.BIST100_YEDEK, bt.BIST50_YEDEK, "yedek"
    else:
        b100, b50, kap_k = bt.endeks_listeleri(veri)
    kaynak("KAP endeks listesi", "OK" if kap_k.startswith("KAP") else "YEDEK", None, f"BIST100 {len(b100)} hisse ({kap_k})")
    kume_uye = sorted({u for v in bs.KUMELER.values() for u in v})
    hisseler = sorted(set(bt.VIOP) | set(b100) | set(kume_uye) | set(bs.K2_SEPET) | {"TRENJ"})
    endeksler = ["XU100", "XU030", "XBANK", "USDTRY", "TLREF"]
    D, bos = {}, []
    bas = datetime.strptime(a.bas, "%Y-%m-%d")
    t_isy = time.time()
    kodlar = endeksler + hisseler

    def fiyat_turu(liste, etiket):
        for i, k in enumerate(liste, 1):
            if time.time() - t_isy > a.butce and not ISY["down"] and not a.cevrimdisi:
                ISY["butce_asildi"] = True
            s = isy_seri(k, pxdir, bas, simdi.replace(tzinfo=None), a.bekle, a.cevrimdisi or ISY.get("butce_asildi", False))
            s = s[s.index <= kesim] if len(s) else s
            if len(s): D[k] = s.astype(float)
            if i == 1 and ISY["down"]:
                print(f"  {etiket}: Is Yatirim baglantisi kurulamadi (devre kesici); onbellek kullaniliyor", flush=True)
            if i % 40 == 0: print(f"  {etiket} {i}/{len(liste)} ({time.time() - T0:.0f} sn)", flush=True)
    fiyat_turu(kodlar, "fiyat")

    # ---- likidite: Borsa Istanbul pay bultenleri (60 gun); olmazsa HisseTekil ------------------------------------------
    son_tah = D["XU100"].index[-1] if "XU100" in D else beklenen_bist
    HVb, n_b, pbt, PB = likidite_bulten(son_tah, veri, min(a.bekle, 0.3), a.cevrimdisi)
    kaynak("Borsa İstanbul pay piyasası bülteni", "OK" if n_b >= 40 and pbt is not None and pbt >= son_tah else ("EKSİK" if n_b else "YOK"),
           pbt.date() if pbt is not None else None, f"{n_b}/60 gün; 60g medyan TL hacim (likidite sırası) ve yedek kapanış")
    print(f"  pay bulteni {n_b} gun ({time.time() - T0:.0f} sn)", flush=True)

    # ---- ikinci tur: Is Yatirim kopmussa eksik seriler bir kez daha (aralikli erisim) -------------------------------
    eksik = [k for k in kodlar if k not in D or (len(D[k]) and D[k].index[-1] < beklenen_bist)]
    if eksik and ISY["down"] and not a.cevrimdisi and time.time() - T0 < 330:
        print(f"  ikinci tur: {len(eksik)} eksik/bayat seri", flush=True)
        ISY.update(down=False, hata_ardisik=0, basari=0, ikinci_tur=len(eksik))
        fiyat_turu(eksik, "ikinci tur")
    # ---- VIOP bulteni ---------------------------------------------------------------------------------------------
    (B1, g1), (B0, g0) = viop_iki_bulten(kesim, veri, a.bekle, a.cevrimdisi)
    if B1 is not None:
        B1 = B1.copy(); B1["ONCEKI UZLASMA FIYATI"] = pd.to_numeric(B1["ONCEKI UZLASMA FIYATI"].astype(str).str.replace(",", "."), errors="coerce")

    # ---- ABD verisi -----------------------------------------------------------------------------------------------
    spx_f = fred("SP500", veri, a.bekle, a.cevrimdisi); ndx_f = fred("NASDAQ100", veri, a.bekle, a.cevrimdisi)
    vix = cboe("VIX", veri, a.bekle, a.cevrimdisi); vix3m = cboe("VIX3M", veri, a.bekle, a.cevrimdisi)
    beklenen_abd = onceki_veya_ayni(bugun - pd.Timedelta(days=1), TATIL_ABD)  # 21:05 TSI'de bugunku ABD seansi acik
    for ad, s_, gec in (("FRED SP500", spx_f, 1), ("FRED NASDAQ100", ndx_f, 1), ("CBOE VIX", vix, 0), ("CBOE VIX3M", vix3m, 0)):
        if not len(s_):
            kaynak(ad, "YOK", None, "indirilemedi"); continue
        lim = onceki_veya_ayni(beklenen_abd - pd.Timedelta(days=1), TATIL_ABD) if gec else beklenen_abd
        kaynak(ad, "OK" if s_.index[-1] >= lim else "BAYAT", s_.index[-1].date(),
               "FRED ~1 iş günü gecikmeli" if gec else "ABD kapanışı 00:00 TSİ (kış); VIX 00:15")

    # ---- Is Yatirim hala kapaliysa araliklarla yokla (DENETIM 08.11: erisim birkac dakikalik pencerelerle geliyor; bos
    #      onbellekli bulut calismasinda tek sans ilk 2 dakika olmasin). Her ~60 sn'de TEK istek; son yoklama --isy-son sn'ye kadar.
    eksik = [k for k in kodlar if k not in D or (len(D[k]) and D[k].index[-1] < beklenen_bist)]
    while eksik and ISY["down"] and not a.cevrimdisi and time.time() - T0 < a.isy_son:
        time.sleep(max(0.0, min(45.0, a.isy_son - (time.time() - T0))))
        ISY.update(down=False, hata_ardisik=0, basari=0); ISY["yoklama"] = ISY.get("yoklama", 0) + 1
        dene = isy_istek("XU100", (simdi.replace(tzinfo=None) - timedelta(days=10)), simdi.replace(tzinfo=None), a.bekle)
        print(f"  yoklama {ISY['yoklama']}: Is Yatirim {'ACIK' if len(dene) else 'kapali'} ({time.time() - T0:.0f} sn)", flush=True)
        if len(dene):
            ISY["yoklama_basari"] = True
            fiyat_turu(eksik, "yoklama turu")
        else:
            ISY["down"] = True
        eksik = [k for k in kodlar if k not in D or (len(D[k]) and D[k].index[-1] < beklenen_bist)]

    bos = [k for k in kodlar if k not in D]
    bist_ok = "XU100" in D and "XBANK" in D and "SAHOL" in D and "AKBNK" in D and len(D["XU100"]) > 260
    son = D["XU100"].index[-1] if "XU100" in D else None
    HV = {}
    if bist_ok:
        # DENETIM 08.11: likidite sirasi tum evrende (fiyati inmeyen hisseler de sirada yer tutar); eskiden yalniz D'dekiler
        # siralaniyordu ve Is Yatirim yarida kopunca kalan hisseler yapay olarak ilk 75'e girebiliyordu
        HV = {k: v for k, v in HVb.items() if k in set(hisseler)}
        if n_b < 40:   # bulten yoksa HisseTekil (Is Yatirim) yedegi
            HV = {}
            for i, k in enumerate(hisseler, 1):
                if k not in D: continue
                gec = time.time() - T0 > a.butce + 60
                h = isy_hacim(k, veri, kesim, a.bekle, a.cevrimdisi or gec)
                if gec: ISY["hacim_butce"] = True
                if h is not None and len(h):
                    h = h[h.index <= son]
                    HV[k] = float(h["hacim"].iloc[-60:].median()) if len(h) >= 20 else np.nan
                if i % 40 == 0: print(f"  hacim {i}/{len(hisseler)} ({time.time() - T0:.0f} sn)", flush=True)
            kaynak("İş Yatırım HisseTekil (hacim, yedek)", "OK" if len(HV) >= 100 else ("EKSİK" if HV else "YOK"), None,
                   f"{len(HV)} hisse 60g medyan TL hacim")
    isy_not = f"{ISY['istek']} istek" + (f"; ikinci tur {ISY['ikinci_tur']} seri" if ISY.get("ikinci_tur") else "") + \
              (f"; {ISY['yoklama']} yoklama" + (" (açıldı)" if ISY.get("yoklama_basari") else " (açılmadı)") if ISY.get("yoklama") else "") + \
              (f"; eksik geçmiş tekrarı {ISY['kisa_tekrar']}" if ISY.get("kisa_tekrar") else "") + \
              (f" (hâlâ kısa/delikli: {', '.join(ISY['supheli'][:10])}{' …' if len(ISY['supheli']) > 10 else ''}; yeni halka arzlar normal)" if ISY.get("supheli") else "") + \
              ("; BAĞLANTI KOPTU (devre kesici) → önbellek" if ISY["down"] else "") + \
              ("; zaman bütçesi aşıldı → kalanlar önbellekten" if ISY.get("butce_asildi") or ISY.get("hacim_butce") else "")
    if son is not None:
        kaynak("İş Yatırım ChartData (fiyat)", ("ÖNBELLEK" if (ISY["down"] or a.cevrimdisi) else "OK") if son >= beklenen_bist else "BAYAT", son.date(),
               f"{len(D)}/{len(kodlar)} seri; bulunamayan: {', '.join(bos[:12]) + (' …' if len(bos) > 12 else '') or '—'}; {isy_not}")
    else:
        kaynak("İş Yatırım ChartData (fiyat)", "YOK", None, isy_not)
    if not bist_ok and PB is not None:
        kaynak("Borsa İstanbul pay piyasası bülteni", "OK", pbt.date(),
               "YEDEK KİP: son tetikler bu kapanışla kontrol edildi" if (DUR["bist"].get("tetikler")) else "YEDEK KİP: durum.json'da kayıtlı tetik yok")

    if B1 is not None:
        ref = son if son is not None else beklenen_bist
        kaynak("Borsa İstanbul VİOP bülteni", "OK" if g1 >= ref else "BAYAT", g1.date(),
               f"önceki bülten {g0.date() if g0 is not None else '—'}; bülten ~20:28–20:49 TSİ'de çıkar")
    else:
        kaynak("Borsa İstanbul VİOP bülteni", "YOK", None, "indirilemedi")

    # ---- hesaplar ---------------------------------------------------------------------------------------------------
    R = None
    if bist_ok:
        try:
            R = bist_hesapla(D, HV, M, B1, g1, b100, simdi, hesap)
        except Exception as e:  # bolum dusse de rapor devam eder
            print("  BIST hesap hatasi:", repr(e), flush=True); R = None; KAYNAK["BIST hesap"] = dict(durum="HATA", son=None, notu=repr(e)[:120])
    sonraki_seans = sonraki(son if son is not None else beklenen_bist)
    PS = KZ = AL_ = BZ = None
    for ad, fn in (("PS", lambda: pr_sahol(D, hesap, R["k9_risk"] if R else 0.0025)), ("KZ", lambda: pr_koza(D, hesap, R["k9_risk"] if R else 0.0025)),
                   ("AL", lambda: pr_altin(B1, g1, D, hesap)), ("BZ", lambda: pr_baz(B1, g1, B0, g0, D))):
        try:
            if ad in ("PS", "KZ") and not bist_ok: continue
            v = fn()
            if ad == "PS": PS = v
            elif ad == "KZ": KZ = v
            elif ad == "AL": AL_ = v
            else: BZ = v
        except Exception as e:
            print(f"  {ad} hatasi: {e!r}", flush=True)
    A = DUR["abd"]; abd = None
    if len(spx_f) and len(vix) and len(vix3m):
        try:
            A, abd = abd_guncelle(A, spx_f, ndx_f, vix, vix3m)
        except Exception as e:
            print("  ABD hesap hatasi:", repr(e), flush=True); abd = dict(hata=repr(e)[:150], notlar=[])
    DUR["abd"] = A

    # ---- karar listesi ----------------------------------------------------------------------------------------------
    ns = sonraki_seans
    aciklayan = set(M.get("bilanco_aciklayanlar_9_11") or [])
    eylem, tetik = [], []   # eylem: (oncelik, metin); tetik: dict
    kisa = {}               # metin -> bildirim icin kisa hali (DENETIM 08.11: bildirimde boyut/saat/stop kalsin)
    ISLEM_P = {2, 3, 4, 6}  # islem iceren oncelikler (0 KRIZ/veri, 1 takvim engeli, 5/7/8 bilgi-kagit, 9 engellenen, 10 bilgi)
    yon_metin = lambda y: "AL" if y > 0 else "SAT"
    kriz_var = bool(R and R["kriz_var"])
    tum_engel = giris_engeli(ns, "_TUM_")
    if R is None:
        eylem.append((0, f"**BIST verisi yok** → bugün BIST için yeni sinyal üretilemedi; yeni giriş yok. Açık pozisyonlar dünkü stop/çıkış "
                         f"seviyeleriyle (aşağıdaki son tetikler ve durum.json) yönetilir."))
    elif kriz_var:
        tk = [k for k, v in R["kriz"].items() if v[1]]
        eylem.append((0, f"**KRİZ kesicisi ({', '.join(tk)})** → 5 işlem günü hiçbir kolda yeni giriş yok; K4/K5/K9 stop = max(iz-stop, "
                         f"bugünkü kapanış × 0,90); hedgesiz K3 kapanır; K1 sürer (PLAN_BIST §2.2)."))
    # acik pozisyonlar (elle girilen)
    for p in DUR.get("acik_pozisyonlar") or []:
        try:
            kol, en = p.get("kol"), p.get("enstruman"); gt = pd.Timestamp(p.get("giris_tarihi"))
            gun = is_gunu_say(gt, son if son is not None else beklenen_bist)
            ek = ""; ks = f"{kol} {en}: tut"
            if kol == "K4" and R is not None and en in D:
                c = D[en]; mx = c[c.index >= gt].max()
                gf = float(p.get("giris_fiyati") or 0)
                iz = 0.90 if (gf > 0 and mx >= 2 * gf) else 0.85   # E5: +%100 kârda iz-stop %10
                stp = iz * mx; durdu = c.iloc[-1] <= stp
                ek = (f"iz-stop {f(stp)} (en yüksek kapanış {f(mx)} × {f(iz)}); bugün {f(c.iloc[-1])} → "
                      + ("**STOP: ertesi gün 18:01–18:05 risk azaltan satış, limit max(taban; P_son × 0,97)**" if durdu else
                         ("**SÜRE (E2): ertesi gün 18:01–18:05 sat, limit max(önceki kapanış × 0,94; P_son × 0,97)**" if gun >= 120 else "tut"))
                      + (f"; 120 gün süre {gun}/120" if gun else ""))
                ks = (f"K4 {en} STOP: 18:01–18:05 sat (kapanış {f(c.iloc[-1])} ≤ {f(stp)})" if durdu else
                      (f"K4 {en} SÜRE ÇIKIŞI 18:01–18:05" if gun >= 120 else f"K4 {en} tut (iz-stop {f(stp)})"))
            elif kol == "K1":
                ck = sonraki(gt, 20)
                ek = f"{gun}/20 iş günü; çıkış {tr_tarih(ck)} 17:55 (VİOP çıkış sırası); felaket stopu bacak nominalinin −%8'i"
                ks = f"K1 {en} ÇIKIŞ 17:55" if ck <= ns else f"K1 {en} gün {gun}/20 (çıkış {ck:%d.%m})"
            elif kol == "PRATIK_SAHOL" and PS is not None:
                zz = PS["z"].iloc[-1]; yon = 1 if str(p.get("yon", "")).upper().startswith(("LONG", "AL")) else -1
                ek = f"z {f(zz)} → " + ("**ÇIKIŞ: |z| ≤ 1,5, ertesi gün uzlaşmada kapat**" if yon * zz >= -1.5 else "tut (çıkış |z| ≤ 1,5)")
                ks = f"PRATİK SAHOL/AKBNK " + ("ÇIKIŞ uzlaşmada" if yon * zz >= -1.5 else f"tut (z {f(zz)})")
            elif kol in ("KOZA", "ALTIN", "TUPRS"):
                ck = sonraki(gt, 2)
                ek = (("**" if ck <= ns else "") + f"planlanan çıkış {tr_tarih(ck)} 18:00–18:10 uzlaşma" + ("**" if ck <= ns else "")
                      + "; çıkış günü 17:50'de aynı yönde sinyal sürüyorsa 2 gün uzat" + (" (≤6 gün)" if kol == "KOZA" else ""))
                ks = f"{kol} {en} " + (f"ÇIKIŞ {ck:%d.%m} 18:00–18:10 (sinyal sürüyorsa +2 gün)" if ck <= ns else f"tut (çıkış {ck:%d.%m})")
            elif kol == "XU030_BAZ":
                ek = f"çıkış {tr_tarih(sonraki(gt, 1))} uzlaşmada"; ks = f"XU030 baz ÇIKIŞ {sonraki(gt, 1):%d.%m} uzlaşma"
            isimler = [x for x in str(en).replace(",", "/").replace(" ", "/").split("/") if x]
            if ns == pd.Timestamp("2026-11-09"):
                bek = [x for x in isimler if x in bs.BILANCO_9_11 and x not in aciklayan]
                if bek:
                    ek += f" — **A1: {', '.join(bek)} bilançosu 9.11 18:00'e kadar KAP'ta yoksa pozisyon 9.11 gecesi taşınmaz → 9.11 18:00–18:10'da kapat**"
                    ks += f"; A1: {', '.join(bek)} bilançosu yoksa 9.11 18:00–18:10 kapat"
            m_ = f"Açık pozisyon {kol} {en} {p.get('yon', '')} (giriş {gt:%d.%m}): {ek}"
            # yalniz 'tut' gerektiren pozisyon islem sayilmaz (oncelik 5: izle); stop/cikis/A1 islemdir (2)
            eylem.append((2 if ("**" in ek or "ÇIKIŞ" in ks or "STOP" in ks) else 5, m_)); kisa[m_] = ks
        except Exception as e:
            eylem.append((2, f"Açık pozisyon kaydı okunamadı ({p}): {e}"))
    if R is not None:
        # K4 (rejim tavanı: KAPALI 2 / GEÇİŞ 4 / AÇIK 6 açık K4; kümede 1 (KAPALI) / 2; durum.json'daki açık K4'ler düşülür)
        tavan = {"KAPALI": 2, "GEÇİŞ": 4, "AÇIK": 6}[R["durum"]]
        kume_tav = 1 if R["durum"] == "KAPALI" else 2
        acik_k4 = [p_.get("enstruman") for p_ in DUR.get("acik_pozisyonlar") or [] if p_.get("kol") == "K4"]
        kume_say = {}
        for e_ in acik_k4:
            kk_ = R["K"].at[e_, "kume"] if e_ in R["K"].index else "—"
            kume_say[kk_] = kume_say.get(kk_, 0) + 1
        yer = tavan - len(acik_k4)
        for k, x in R["nit"].iterrows():
            eng = tum_engel or giris_engeli(ns, "K4", k, bs.BILANCO_9_11, aciklayan) or ("KRİZ" if kriz_var else "")
            if not eng and yer <= 0:
                eng = f"K4 tavanı dolu ({R['durum']}: en çok {tavan} açık K4)"
            if not eng and x.kume != "—" and kume_say.get(x.kume, 0) >= kume_tav:
                eng = f"aynı kümeden ({x.kume}) en çok {kume_tav} pozisyon"
            if not eng:
                yer -= 1; kume_say[x.kume] = kume_say.get(x.kume, 0) + 1
            lim = x.kapanis * 1.06
            metin = (f"K4 **{k} AL (spot{' / VİOP-47' if x.viop else ''})** — {tr_tarih(ns)} 18:01–18:05 kapanış seansı limitli alış, "
                     f"limit min({f(lim)}; P_son × 1,03); iz-stop (E1) kapanış ≤ girişten beri en yüksek kapanış × 0,85 (bugünkü kapanışla ≈ {f(x.kapanis * 0.85)}); "
                     f"boyut {f(x.tl / 1e3, 'f0')} bin TL (stop mesafesi %{int(100 * x.stop)} ile; {f(hesap / 1e6, 'f1')} mn TL hesap, r₀ {pc2(R['r0'])}); çıkış iz-stop ya da 120 gün")
            eylem.append((9, f"~~{metin}~~ → **giriş yok: {eng}**") if eng else (2, metin))
            kisa[metin] = f"K4 {k} AL 18:01–18:05 limit ≤ {f(lim)}, {f(x.tl / 1e3, 'f0')} bin TL, iz-stop %15"
        # K1
        z1 = R["z1"].iloc[-1]
        if abs(z1) >= 2:
            yon = "F_SAHOL SAT + F_AKBNK AL" if z1 > 0 else "F_SAHOL AL + F_AKBNK SAT"
            kap = bool(M.get("kural0")) and (M.get("komisyon_viop_bps") or 99) <= 5
            fs = on_vade(B1, "SAHOL", g1, sonra=sonraki(ns, 20)) if B1 is not None else None
            fa = on_vade(B1, "AKBNK", g1, sonra=sonraki(ns, 20)) if B1 is not None else None
            n_s = int(0.075 * hesap / ((fs["UZLASMA FIYATI"] if fs is not None else D["SAHOL"].iloc[-1]) * 100))
            n_a = int(0.075 * hesap / ((fa["UZLASMA FIYATI"] if fa is not None else D["AKBNK"].iloc[-1]) * 100))
            mt = (f"K1 **{yon}** (z {f(z1)}) — {tr_tarih(ns)} 17:50 kontrol (bacak ±%9 ise giriş yok), 17:55 limit karşı en iyi ±%0,3, "
                  f"18:05 ±%0,6; kontrat {fs['SOZLESME KODU'] if fs is not None else 'F_SAHOL (çıkıştan sonra biten vade)'} / {fa['SOZLESME KODU'] if fa is not None else 'F_AKBNK'}, "
                  f"bacak başı hesabın %7,5'i ≈ {n_s} / {n_a} kontrat; çıkış 20. iş günü ({tr_tarih(sonraki(ns, 20))}); felaket stopu −%8")
            eng = giris_engeli(ns, "K1", ["SAHOL", "AKBNK"], bs.BILANCO_9_11, aciklayan)
            if R["k1_model"] is not None and R["k1_model"]["giris_i"] <= len(R["k1_idx"]) - 1:
                eylem.append((8, f"K1: z {f(z1)} ama modelde açık K1 işlemi var (sinyal {R['k1_model']['sinyal']:%d.%m}) → yeni giriş yok"))
            elif eng:
                eylem.append((9, f"~~{mt}~~ → **giriş yok: {eng}**"))
            elif not kap:
                eylem.append((5, mt + " → **KÂĞIT** (Kural 0 / komisyon ≤ 5 bps kapısı makro.json'da açık değil)"))
            else:
                eylem.append((2, mt))
            kisa[mt] = f"K1 {yon} {n_s}/{n_a} kontrat 17:55 (z {f(z1)}), çıkış {sonraki(ns, 20):%d.%m}"
            kisa[mt + " → **KÂĞIT** (Kural 0 / komisyon ≤ 5 bps kapısı makro.json'da açık değil)"] = f"K1 kâğıt: {yon} (z {f(z1)})"
    # PRATIK SAHOL/AKBNK (DENETIM 08.11: 'girerdi' yalniz YENI bolumun ilk gunu; suren bolumde model pozisyonu bilgi olarak)
    if PS is not None:
        zz = PS["z"].iloc[-1]
        mod = DUR["ayarlar"].get("pratik_sahol_akbnk", "kagit")
        if PS["act"].startswith("KAPAT"):
            m_ = f"PRATİK SAHOL/AKBNK: model bugün |z| ≤ 1,5 ile ÇIKTI (z {f(zz)}) → elde varsa {tr_tarih(ns)} 18:00–18:10 uzlaşmada kapat"
            eylem.append((4, m_)); kisa[m_] = "PRATİK SAHOL/AKBNK: elde varsa 18:00–18:10 uzlaşmada KAPAT"
        if "AÇ" in PS["act"]:
            yon = "F_SAHOL SAT + F_AKBNK AL" if zz > 0 else "F_SAHOL AL + F_AKBNK SAT"
            mt = (f"PRATİK SAHOL/AKBNK z {f(zz)} (|z| > 1,5, yeni bölüm): kural bugünkü uzlaşmada **{yon}** ({PS['n'][0]}:{PS['n'][1]} kontrat, K9 riski) girerdi; 21:05'te kaçtı. Ertesi gün girişi test edilmedi → yarın 17:50'de |z| hâlâ > 1,5 "
                  f"ise yalnız {'kâğıt' if mod != 'canli' else 'yarım boy'}; çıkış |z| ≤ 1,5 olunca uzlaşmada")
            eng = tum_engel or ("KRİZ" if kriz_var else "") or giris_engeli(ns, "K9", ["SAHOL", "AKBNK"], bs.BILANCO_9_11, aciklayan)
            eylem.append((9, f"{mt} → **giriş yok: {eng}**") if eng else (6 if mod == "canli" else 7, mt))
            kisa[mt] = f"PRATİK SAHOL/AKBNK {yon} ({'yarım boy, ' if mod == 'canli' else 'kâğıt, '}17:50'de |z|>1,5 ise; z {f(zz)})"
        elif PS["side"] != 0:
            eylem.append((5, f"PRATİK SAHOL/AKBNK: model {'LONG' if PS['side'] > 0 else 'SHORT'} {PS['held']} gündür (giriş {PS['T'][-1]['giris']:%d.%m}); "
                             f"çıkış |z| ≤ 1,5 (bugün {f(zz)}); yeni giriş yok"))
        elif abs(zz) > 1.5:
            eylem.append((7, f"PRATİK SAHOL/AKBNK z {f(zz)} eşik dışında ama bu bölümün girişi zaten yapıldı/atlandı → yeni giriş yok"))
    # KOZA
    if KZ is not None:
        zz = KZ["L"].z3
        if KZ["pos"] is not None and KZ["pos"]["i0"] == len(KZ["idx"]) - 1:
            s = KZ["pos"]["s"]
            cik = sonraki(ns, 2)
            ft = on_vade(B1, "TRMET", g1, sonra=cik) if B1 is not None else None
            fh = on_vade(B1, "TRALT", g1, sonra=cik) if B1 is not None else None
            eng = tum_engel or giris_engeli(ns, "K9", ["TRMET", "TRALT"], bs.BILANCO_9_11, aciklayan) or ("KRİZ" if kriz_var else "")
            mt = (f"KOZA z3 {f(zz)}: **{'TRMET1! AL + TRALT1! SAT' if s > 0 else 'TRMET1! SAT + TRALT1! AL'}** — bugünkü uzlaşma (kuralın girişi) kaçtı; "
                  f"ertesi gün girişi (E2, test edildi: h2 +30 bps, t 2,6) {tr_tarih(ns)} 18:00–18:10, 2–3 parçada limitli; "
                  f"{KZ['n'][0]} {ft['SOZLESME KODU'] if ft is not None else 'TRMET'} : {KZ['n'][1]} {fh['SOZLESME KODU'] if fh is not None else 'TRALT'} "
                  f"(K9 riski {pc2(R['k9_risk'] if R else 0.0025)}, β {f(KZ['L'].bH)}); çıkış {tr_tarih(cik)} uzlaşma, aynı yönde |z3|>1,5 ise +2 gün (≤6)")
            eylem.append((9, f"~~{mt}~~ → **giriş yok: {eng}**") if eng else (4, mt))
            kisa[mt] = (f"KOZA {'TRMET1! AL + TRALT1! SAT' if s > 0 else 'TRMET1! SAT + TRALT1! AL'} {KZ['n'][0]}:{KZ['n'][1]} kontrat "
                        f"18:00–18:10 uzlaşma, çıkış {cik:%d.%m} (z3 {f(zz)})")
        elif KZ["pos"] is None and abs(zz) > 1.5:
            eylem.append((7, f"KOZA z3 {f(zz)} eşik üstü ama kural girişi yok ({'kilit şüphesi: TRMET/TRALT ±%9,5' if KZ['kilit'] else 'aynı yönde 6 günlük işlem yeni bitti; z3 bant içine dönmeli'})"))
        elif KZ["pos"] is not None:
            ex = KZ["pos"]["exit"]; kalan = ex - (len(KZ["idx"]) - 1)
            eylem.append((5, f"KOZA: model pozisyonu {'TRMET AL/TRALT SAT' if KZ['pos']['s'] > 0 else 'TRMET SAT/TRALT AL'} "
                             f"(giriş {KZ['idx'][KZ['pos']['i0']]:%d.%m}); planlanan çıkış {kalan}. iş günü sonra ({tr_tarih(sonraki(son, kalan)) if kalan > 0 else 'bugün'}); "
                             "çıkış günü 17:50'de z3 aynı yönde > 1,5 ise uzat"))
    # ALTIN
    if AL_ is not None and abs(AL_["z"]) > 1:
        eylem.append((7, f"ALTIN → TRALT: {AL_['kod']} uzlaşma değişimi {f(AL_['g'], '%')} (z {f(AL_['z'])}) eşiği aştı; kural bugünkü uzlaşmada "
                         f"**{'TRALT1! AL + XU030D1! SAT' if AL_['z'] > 0 else 'TRALT1! SAT + XU030D1! AL'}** girerdi → kaçtı, ertesi gün girişi test edilmedi: işlem yok; "
                         f"17:55 alarmı kurulu değilse kur (TRADINGVIEW_ALARMLARI.md §4)"))
    # BAZ
    if BZ is not None and abs(BZ["z"]) > 1:
        eylem.append((7, f"XU030 bazı: Δb {f(BZ['db'] * 1e4, 'f0')} bps (z {f(BZ['z'])}) → kural 18:10–18:15'te **{'XU030D1! SAT' if BZ['z'] > 0 else 'XU030D1! AL'}** "
                         f"açıp {tr_tarih(ns)} uzlaşmasında kapatırdı; bu akşam için geç (yalnız canlı alarmla)"))
    # canli izleme hatirlatmasi (TradingView)
    izle_tv = []
    if KZ is not None and KZ["pos"] is None:
        izle_tv.append(f"Koza TRMET ≥ {f(KZ['tet_al'])} / ≤ {f(KZ['tet_sat'])}")
    if PS is not None and PS["side"] == 0:
        izle_tv.append(f"SAHOL/AKBNK z ±1,5 (SAHOL ≥ {f(PS['tet'][1.5][0])} / ≤ {f(PS['tet'][-1.5][0])}; {DUR['ayarlar'].get('pratik_sahol_akbnk', 'kagit')})")
    if AL_ is not None:
        izle_tv.append("altın 17:55 TVC:GOLD dünkü 17:55'e göre ±%1,70")
    if BZ is not None:
        izle_tv.append("XU030D1!/XU030 oranı " + f"{BZ['oran_alt']:.4f}–{BZ['oran_ust']:.4f}".replace(".", ",") + " dışı (18:10)")
    izle_tv.append("TUPRS z (tuprs_alarm.pine, sabah)")
    eng_tv = tum_engel or giris_engeli(ns, "K9", ["TRMET", "TRALT"], bs.BILANCO_9_11, aciklayan)
    eylem.append((8, f"TradingView canlı alarmları ({tr_tarih(ns)} 17:45–17:55): " + "; ".join(izle_tv)
                  + (f". **Not:** {tr_tarih(ns)} için engel: {eng_tv}" if eng_tv else "")))
    # takvim (sonraki seans)
    for b, e, p, o, kural, blok in takvim_bayraklari(ns, 0):
        eylem.append((1 if p == "BIST" and blok else 10, f"Takvim {tr_tarih(ns)} [{p}]: {o} — {kural}"))
    # ABD
    if abd and "k" in abd:
        izin = A["durum"] in ("SARI", "YEŞİL")
        kisa_abd = f"ABD {A['durum']}: pilot izinli 16:45–17:15 TSİ, işlem başı %0,25 risk"
        eylem.append((3 if izin else 10, f"ABD rejimi **{A['durum']}** ({abd['t']:%d.%m} kapanışı) → " +
                      ("pilot izinli: 16:45–17:15 TSİ bekleyen emir, işlem başı %0,25 risk, yakın bölgede tek pozisyon (PLAN_ABD §2.2)" if izin
                       else f"yeni canlı giriş yok; en erken SARI kapanışı {tr_tarih(abd['en_erken']['sari'])}, en erken pilot {tr_tarih(abd['en_erken']['pilot'])} 16:45–17:15")))
        kisa[eylem[-1][1]] = kisa_abd

    # ---- tetikler (yarin) ---------------------------------------------------------------------------------------------
    def tet(kol, en, kosul, seviye, bugun_, islem, canli=False, zaman=None):
        if seviye is None or bugun_ is None or not np.isfinite(seviye) or not np.isfinite(bugun_) or bugun_ == 0:
            return
        op = "≥" if ("≥" in kosul or ">" in kosul) else "≤"
        tetik.append(dict(kol=kol, en=en, kosul=kosul, op=op, seviye=float(seviye), bugun=float(bugun_), uzak=float(seviye) / float(bugun_) - 1,
                          islem=islem, canli=canli, zaman=zaman or ("canlı 17:45–17:55 (aynı gün uzlaşma)" if canli else "BIST kapanışı → ertesi gün emir")))
    if R is not None:
        for k, x in R["izle"].iterrows():
            tet("K4", k, "kapanış >", x.tetik, x.kapanis, f"K4 sinyali → {tr_tarih(sonraki(ns))} 18:01–18:05 AL (limit kapanış×1,06 / P_son×1,03)")
        tt = R["k1_tet"]
        tet("K1", "SAHOL", "kapanış ≥ (AKBNK sabit)", tt.get("SAHOL_z+2"), D["SAHOL"].iloc[-1], "z=+2 → ertesi gün F_SAHOL SAT + F_AKBNK AL")
        tet("K1", "AKBNK", "kapanış ≤ (SAHOL sabit)", tt.get("AKBNK_z+2"), D["AKBNK"].iloc[-1], "z=+2 → ertesi gün F_SAHOL SAT + F_AKBNK AL")
        tet("K1", "SAHOL", "kapanış ≤ (AKBNK sabit)", tt.get("SAHOL_z-2"), D["SAHOL"].iloc[-1], "z=−2 → ertesi gün F_SAHOL AL + F_AKBNK SAT")
        tet("K1", "AKBNK", "kapanış ≥ (SAHOL sabit)", tt.get("AKBNK_z-2"), D["AKBNK"].iloc[-1], "z=−2 → ertesi gün F_SAHOL AL + F_AKBNK SAT")
        # yarinin SMA'si yarinin kapanisini da icerir: kapanis > SMA_n(yarin)  <=>  kapanis > son (n-1) kapanisin ortalamasi (kesin)
        tet("Rejim T3", "XU100", "kapanış > yarının SMA50 (5 kapanış gerekir)", D["XU100"].iloc[-49:].mean(), R["xu"], "T3=1 (GEÇİŞ için M1 + M2/M4/M5 de gerekir)")
        tet("Rejim M5", "XBANK", "kapanış > yarının SMA200", D["XBANK"].iloc[-199:].mean(), R["xb"], "M5=1")
        tet("Rejim T1", "XU100", "kapanış > yarının SMA200", D["XU100"].iloc[-199:].mean(), R["xu"], "AÇIK rejim (K4 r₀ %0,75)")
    if PS is not None and PS["side"] == 0:
        kg = "" if DUR["ayarlar"].get("pratik_sahol_akbnk", "kagit") == "canli" else " (kâğıt)"
        for tg, (ps_, pa_) in PS["tet"].items():
            yon = ("F_SAHOL SAT + F_AKBNK AL" if tg > 0 else "F_SAHOL AL + F_AKBNK SAT") + kg
            tet("PRATİK", "SAHOL", f"{'≥' if tg > 0 else '≤'} (AKBNK sabit), z={'+' if tg > 0 else '−'}1,5", ps_, PS["pa"], f"aynı gün uzlaşmada {yon}", True)
            tet("PRATİK", "AKBNK", f"{'≤' if tg > 0 else '≥'} (SAHOL sabit), z={'+' if tg > 0 else '−'}1,5", pa_, PS["pb"], f"aynı gün uzlaşmada {yon}", True)
    if KZ is not None and KZ["pos"] is None:
        tet("KOZA", "TRMET", "kapanış ≥ (TRALT, TRENJ yatay)", KZ["tet_al"], KZ["PM"], "aynı gün uzlaşmada TRMET1! AL + TRALT1! SAT", True)
        tet("KOZA", "TRMET", "kapanış ≤ (TRALT, TRENJ yatay)", KZ["tet_sat"], KZ["PM"], "aynı gün uzlaşmada TRMET1! SAT + TRALT1! AL", True)
    if abd and "k" in abd:
        k = abd["k"]
        s200_yarin = abd["spx"].loc[:abd["t"]].iloc[-199:].mean()   # yarinin 200 GHO'su yarinin kapanisini da icerir (kesin esik)
        if k["spx"] > k["s200"]:
            tet("ABD", "S&P 500", "kapanış < yarının 200 GHO", s200_yarin, k["spx"], "2 kapanış üst üste altında → KIRMIZI (b), sayım yeniden", zaman="ABD kapanışı (00:00 TSİ)")
        else:
            tet("ABD", "S&P 500", "kapanış > yarının 200 GHO", s200_yarin, k["spx"], "SARI şartı (S&P > 200 GHO)", zaman="ABD kapanışı (00:00 TSİ)")
        for ad in ("SPX", "NDX"):
            Rl = A["ralli"][ad]
            if Rl["gun1"] and Rl["gun"] >= 3 and not A.get("ftd"):
                kap = A["son_kapanis"].get(ad)
                tet("ABD FTD", "S&P 500" if ad == "SPX" else "Nasdaq-100", "kapanış ≥ +%1,5 (ralli ≥4. gün)", kap * 1.015 if kap else None, kap,
                    "FTD adayı (hacim teyidi elle) → SARI tetiği", zaman="ABD kapanışı (00:00 TSİ)")
            if Rl["gun1"]:
                tet("ABD ralli", "S&P 500" if ad == "SPX" else "Nasdaq-100", "kapanış < ralli dibi", Rl["dip"], A["son_kapanis"].get(ad),
                    "ralli denemesi sıfırlanır, FTD en erken 4 seans sonra", zaman="ABD kapanışı (00:00 TSİ)")
        if np.isfinite(k["vr"]):
            tet("ABD VIX", "VIX/VIX3M", "< 1,00 (2 kapanış)" if k["vr"] >= 1 else "≥ 1,00", 1.0, k["vr"],
                "KIRMIZI (a) çıkışı" if k["vr"] >= 1 else "KIRMIZI (a) yeniden", zaman="VIX kapanışı (00:15 TSİ)")
    yakin = sorted([t_ for t_ in tetik if abs(t_["uzak"]) <= 0.03], key=lambda t_: abs(t_["uzak"]))

    # degrade kip: dunku tetikleri pay bulteniyle kontrol
    degrade, degrade_yakin = [], []
    if R is None and PB is not None:
        for t_ in DUR["bist"].get("tetikler") or []:
            en = t_["en"]
            if en in PB.index and np.isfinite(PB.at[en, "KAPANIS FIYATI"]):
                c = PB.at[en, "KAPANIS FIYATI"]
                ust = "≥" in t_["kosul"] or ">" in t_["kosul"]
                ok = c >= t_["seviye"] if ust else c <= t_["seviye"]
                degrade.append([t_["kol"], en, t_["kosul"], f(t_["seviye"]), f(c), "**TETİKLENDİ**" if ok else "—", t_["islem"]])
                if not ok and abs(t_["seviye"] / c - 1) <= 0.03:
                    degrade_yakin.append(dict(kol=t_["kol"], en=en, op="≥" if ust else "≤", seviye=t_["seviye"], uzak=t_["seviye"] / c - 1))

    # ---- RAPOR ---------------------------------------------------------------------------------------------------
    tarih_etiket = son if son is not None else (g1 if g1 is not None else beklenen_bist)
    tag = pd.Timestamp(tarih_etiket).strftime("%Y%m%d")
    md = [f"# Günlük öneri — {tr_tarih(tarih_etiket)} kapanışı (üretim {simdi:%d.%m.%Y %H:%M} TSİ)", "",
          f"Sonraki BIST seansı: **{tr_tarih(ns)}**. Hesap büyüklüğü (durum.json): {f(hesap / 1e6, 'f1')} mn TL. "
          "Bilgi amaçlıdır; yatırım tavsiyesi değildir. Kurallar: PLAN_BIST.md, PLAN_ABD.md, 2026-11-04_kapanis_1-3gun/PRATIK_LISTE.md.", ""]
    uyarilar, kisa_uyari = [], []
    if makro_yas > 7:
        uyarilar.append(f"makro.json {makro_yas} gündür güncellenmedi (son {M.get('guncellendi')}) → M1/M2/KRİZ (c, d)/K6 BAYAT olabilir.")
        kisa_uyari.append(f"makro.json {makro_yas} gün eski")
    if makro_yeni:
        uyarilar.append("makro.json bu çalışmada 05.11 plan değerleriyle oluşturuldu; Perşembe rezervinden sonra güncelleyin.")
    if bist_ok and bos:
        uyarilar.append(f"{len(bos)} seri indirilemedi ({', '.join(bos[:8])}{' …' if len(bos) > 8 else ''}): bu isimler K4 taramasında, küme RS'inde ve "
                        "PRATİK sinyallerde yok; liste kısa değilse raporu 30–60 dk sonra yeniden üretin.")
        kisa_uyari.append(f"{len(bos)} seri eksik")
    if ISY["down"]:
        uyarilar.append("İş Yatırım bağlantısı koptu: BIST hesapları " + ("önbellekteki verilerle yapıldı." if bist_ok else "yapılamadı (veri yok)."))
        kisa_uyari.append("İş Yatırım yok" + (" (önbellek)" if bist_ok else ""))
    bayat = [k for k, v in KAYNAK.items() if v["durum"] in ("BAYAT", "YOK")]
    if bayat:
        uyarilar.append("BAYAT/YOK kaynak: " + ", ".join(bayat) + " (§6).")
        kisa_ad = {"Borsa İstanbul pay piyasası bülteni": "pay bülteni", "Borsa İstanbul VİOP bülteni": "VİOP bülteni",
                   "İş Yatırım ChartData (fiyat)": "İş Yatırım", "FRED SP500": "FRED", "FRED NASDAQ100": "FRED",
                   "CBOE VIX": "CBOE", "CBOE VIX3M": "CBOE", "KAP endeks listesi": "KAP"}
        kb = [x for x in dict.fromkeys(kisa_ad.get(b, b.split(" (")[0]) for b in bayat) if not (x == "İş Yatırım" and ISY["down"])]
        if kb:
            kisa_uyari.append("bayat/yok: " + ", ".join(kb))
    if uyarilar:
        md += ["> **Uyarı:** " + " ".join(uyarilar), ""]

    md += ["## 0. BUGÜN NE YAPILIR (sonraki seans için, öncelik sırasıyla)", ""]
    sirali = sorted(eylem, key=lambda x: x[0])
    aktif = [m for p, m in sirali if p in ISLEM_P]
    if not aktif:
        neden = [] if R is not None else ["BIST verisi yok"]
        if R is not None:
            neden.append(f"BIST rejimi {R['durum']}, KRİZ {'VAR' if kriz_var else 'yok'}, K4 nitelikli {len(R['nit'])}, K1 z {f(R['z1'].iloc[-1])}")
        if KZ is not None: neden.append(f"Koza z3 {f(KZ['L'].z3)}")
        if PS is not None: neden.append(f"SAHOL/AKBNK z {f(PS['z'].iloc[-1])}")
        if abd and "k" in abd: neden.append(f"ABD {A['durum']}")
        sirali = [(0, "**İşlem yok** — " + ("; ".join(neden) or "veri yok") + ".")] + sirali
    for i, (p, m) in enumerate(sirali[:10], 1):
        md.append(f"{i}. {m}")
    md += ["", f"**Yarın tetiklenebilecekler** (tetiğe ≤ %3; seviye = {tr_tarih(ns)} kapanışı için kesin fiyat; 'canlı' satırlar aynı gün uzlaşmada "
           "işlem ister → 17:45–17:55 TradingView alarmı, bkz. ../TRADINGVIEW_ALARMLARI.md):", ""]
    if yakin:
        md.append(tablo(["Kol", "Enstrüman", "Koşul", "Tetik", "Bugün", "Gereken", "Tetiklenirse", "Zaman"],
                        [[t_["kol"], t_["en"], t_["kosul"], f(t_["seviye"]) if t_["seviye"] > 5 else f(t_["seviye"], "f2"),
                          f(t_["bugun"]), f(t_["uzak"], "%"), t_["islem"], t_["zaman"]] for t_ in yakin]))
    else:
        md.append("_Tetiğe %3 içinde yaklaşan yok._")
    if degrade:
        md += ["", f"**Yedek kip:** son başarılı çalışmanın ({DUR['bist'].get('son_tarih')}) tetikleri, Borsa İstanbul pay bülteni {pbt.date()} kapanışıyla:",
               tablo(["Kol", "Hisse", "Koşul", "Tetik", "Bülten kapanışı", "Durum", "İşlem"], degrade)]
    md.append("")

    # 1. rejim
    md += ["## 1. BIST rejimi ve KRİZ kesicisi (PLAN_BIST §2)", ""]
    if R is None:
        sb = DUR["bist"]
        md += [f"_Veri yok._ Son başarılı hesap: {sb.get('son_tarih') or '—'} → rejim {sb.get('rejim') or '—'}, KRİZ {sb.get('kriz') or '—'}.", ""]
    else:
        md += [tablo(["Kod", "Koşul", "Değer", "Durum"], [
            ["T1", "XU100 > SMA200", f"{f(R['xu'], 'f0')} vs {f(R['xs200'], 'f0')} ({f(R['xu'] / R['xs200'] - 1, '%')})", int(R["T1"])],
            ["T2", "XU100 12 ay > nakit (max TLREF, PPF %45,5)", f"{f(R['xu12'], '%')} vs TLREF {f(R['nakit12'], '%')}; eşik ~{f(R['t2_esik'], 'f0')}", int(R["T2"])],
            ["T3", "son 5 kapanış > SMA50", f"SMA50 {f(R['xs50'], 'f0')} ({f(R['xu'] / R['xs50'] - 1, '%')})", int(R["T3"])],
            ["M1", "net rezerv 3 hafta artış (makro.json)", " → ".join(f(float(v), "f1") for v in R["nr"]) + " mlr $", int(R["M1"])],
            ["M2", "aylık TÜFE < %2, 2 ay (makro.json)", " / ".join(f"{k}: {f(float(v))}" for k, v in R["tufe"] if v is not None), int(R["M2"])],
            ["M4", "CDS < 230 ve düşüyor (teyitli)", f"{R['cds']} (teyitli {'E' if R['cds_ok'] else 'H'})", int(R["M4"])],
            ["M5", "XBANK > SMA200", f"{f(R['xb'], 'f0')} vs {f(R['xb200'], 'f0')} ({f(R['xb'] / R['xb200'] - 1, '%')})", int(R["M5"])]]),
            "", f"**Durum: {R['durum']}** ({R['acik']}/7 açık) → K4 r₀ {pc2(R['r0'])}, K9 (1–3 günlük sinyaller) risk {pc2(R['k9_risk'])}; ertesi işlem gününden geçerli.", "",
            "**KRİZ kesicisi:**", tablo(["Tetik", "Değer", "Tetiklendi"], [[k, v[0], "**EVET**" if v[1] else "—"] for k, v in R["kriz"].items()]), ""]
        if R["kriz_yakin"] and not kriz_var:
            md += [f"> KRİZ (d) yakın: son haftalık net rezerv değişimi {f(float(R['nr_deg'][-1]), 'f1')} mlr $. Bir hafta daha ≤ −5 gelirse tetiklenir ({(son + pd.Timedelta(days=(3 - son.weekday()) % 7 or 7)):%d.%m} Perşembe 14:30 rezervi).", ""]
        md += [f"Makro: makro.json (güncellendi {M.get('guncellendi')}, {makro_yas} gün önce{' → BAYAT' if makro_yas > 7 else ''}).", ""]

    # 2. plan kurallari
    md += ["## 2. Plan kuralları (bist_sinyal.py mantığı)", ""]
    if R is None:
        md += ["_Veri yok._", ""]
    else:
        z1, z2 = R["z1"].iloc[-1], R["z2"].iloc[-1]
        tt = R["k1_tet"]
        km = R["k1_model"]
        md += ["### K1 SAHOL↔AKBNK (60 gün ln oran z, |z| ≥ 2, ertesi gün giriş, 20 gün) ve K2 KCHOL/sepet (kâğıt)",
               tablo(["Kol", "z", "Son |z|≥2 kesişimi", "Not"], [
                   ["K1", f(z1), R["kes1"].date() if R["kes1"] is not None else "—",
                    ("SİNYAL" if abs(z1) >= 2 else "sinyal yok") + (f"; model işlemi: sinyal {km['sinyal']:%d.%m}, çıkış 20. gün" if km is not None else "")],
                   ["K2", f(z2), R["kes2"].date() if R["kes2"] is not None else "—", "yalnız yeni kesişimde; varsayılan kâğıt"
                    + (f"; **sepet eksik: {', '.join(u for u in bs.K2_SEPET if u not in D)} → z güvenilmez**" if any(u not in D for u in bs.K2_SEPET) else "")]]),
               "", f"K1 tam tetikler (öbür bacak sabit; SAHOL {f(D['SAHOL'].iloc[-1])}, AKBNK {f(D['AKBNK'].iloc[-1])}): z=+2 → SAHOL ≥ {f(tt.get('SAHOL_z+2'))} "
               f"ya da AKBNK ≤ {f(tt.get('AKBNK_z+2'))}; z=−2 → SAHOL ≤ {f(tt.get('SAHOL_z-2'))} ya da AKBNK ≥ {f(tt.get('AKBNK_z-2'))}. "
               f"Kapı: Kural 0 = {'E' if M.get('kural0') else 'H'}, komisyon = {M.get('komisyon_viop_bps') or '—'} bps (≤ 5 gerekir).",
               "", f"TradingView oran alarmı (BIST:SAHOL/BIST:AKBNK, 1G, 'Bar kapanışında'): **≥ {f4(tt.get('SAHOL_z+2', np.nan) / D['AKBNK'].iloc[-1])}** (z=+2 → F_SAHOL SAT + F_AKBNK AL) "
               f"ya da **≤ {f4(tt.get('SAHOL_z-2', np.nan) / D['AKBNK'].iloc[-1])}** (z=−2 → F_SAHOL AL + F_AKBNK SAT); bugünkü oran {f4(D['SAHOL'].iloc[-1] / D['AKBNK'].iloc[-1])}. "
               "Seviyeler her akşam bu rapordan güncellenir; giriş ertesi gün 17:55.", ""]
        nit, izle = R["nit"], R["izle"]
        md += [f"### K4 kırılım (evren: ilk 75 likit; likidite {R['liq_n']} hissede)", ""]
        if len(nit):
            md += [tablo(["Hisse", "Kapanış", "RS", "Lik.", "Küme/Blok", "Stop", "Boyut bin TL", "Engel (sonraki seans)"],
                         [[k, f(x.kapanis), int(x.rs), int(x.lsira), f"{x.kume}/{x.blok}", f"%{int(100 * x.stop)}", f(x.tl / 1e3, "f0"),
                           giris_engeli(ns, "K4", k, bs.BILANCO_9_11, aciklayan) or "—"] for k, x in nit.iterrows()]), ""]
        else:
            md += ["Nitelikli: **yok**.", ""]
        md += ["Bekleme listesi (tetiğe ≤ %15, şablonun 5 koşulundan ≥ 4'ü):",
               tablo(["Hisse", "Kapanış", "Tetik (kapanış >)", "Gereken", "Şablon", "RS", "Lik.", "Küme", "Bilanço 9.11"],
                     [[k, f(x.kapanis), f(x.tetik), f(x.uzak, "%"), "".join("✓" if x[c] else "✗" for c in ["tt_dizilim", "tt_egim", "tt_dip", "tt_zirve", "tt_rs"]),
                       "—" if pd.isna(x.rs) else int(x.rs), "—" if pd.isna(x.lsira) else int(x.lsira), x.kume,
                       "bekliyor" if (k in bs.BILANCO_9_11 and k not in aciklayan and son <= pd.Timestamp("2026-11-09")) else "—"] for k, x in izle.head(12).iterrows()]) if len(izle) else "_Yok._", ""]
        KS = R["KS"]
        if len(KS):
            md += ["### Küme 12 ay RS (K7 filtresi, K4 önceliği; ilk 8)",
                   tablo(["Sıra", "Küme", "Blok", "RS 12 ay", "rel 3 ay", "TL 3 ay", "> nakit 3 ay", "126g RS zirvesinden gün", "Genişlik 50"],
                         [[i + 1, x.kume, x.blok, f(x.rs12, "%"), f(x.rel3, "%"), f(x.tl3, "%"), "E" if x.tl3 > R["nakit3"] else "H",
                           "**0**" if x.gun126 == 0 else x.gun126, f(x.gen50, "%u")] for i, x in KS.head(8).iterrows()]), ""]
        md += [f"### VİOP resmî bülten (uzlaşma; bülten {g1.date() if g1 is not None else 'YOK'})"]
        if R["vsat"]:
            md += [tablo(["Kontrat", "Gün", "Uzlaşma", "XU030", "İma basit", "İma bileşik", "TLREF", "Eşik (mevduat neti+3)", "Nakit-taşıma"],
                         [[v["kod"], v["T"], f(v["F"], "f0"), f(v["S"], "f0"), f(v["basit"], "%u"), f(v["bil"], "%u"), f(v["tlref"], "%u"),
                           f(v["esik"], "%u"), "AÇ (Kural 0 gerekli)" if v["ac"] else "kapalı"] for v in R["vsat"]])]
        if R["usd_on"]:
            u = R["usd_on"]
            md += ["", f"F_USDTRY ön ay {u['kod']}: uzlaşma {f(u['F'])}, spot {f(u['S'])}, {u['T']} gün → ima TL basit **{f(u['ima'], '%u')}** "
                       f"(KRİZ e eşiği %{M['politika_faizi'] + 5:.0f})."]
        if R["hisse_vadeli"]:
            md += ["", "Pay vadelileri (§1.5 long kuralı: mevduat neti − ima ≥ 3 puan, açık poz. ≥ 20.000, hacim ≥ 100 mn TL):",
                   tablo(["Kontrat", "Gün", "Uzlaşma", "Spot", "İma", "Mevduat neti − ima", "Hacim mn TL", "Açık poz.", "Kural"], R["hisse_vadeli"])]
        md += ["", "**K6 carry kapısı:** " + ("AÇIK" if all(R["k6"].values()) else "KAPALI") + " — " +
               "; ".join(f"{k}: {'✓' if v else '✗'}" for k, v in R["k6"].items()), ""]

    # 3. PRATIK
    md += ["## 3. 1–3 günlük PRATİK sinyaller (PLAN_BIST'te K9 kanalı: fikir kartı, risk ≤ %0,25 KAPALI / %0,5 diğer, en çok 2)", "",
           "Karar anı kapanış penceresi (17:50–18:10). Bu rapor 21:05'te çıktığı için **bugün tetiklenen sinyalin kendi giriş anı geçmiştir**; "
           "rapor yarının tetik fiyatlarını verir, aynı gün yakalamak için TradingView alarmı gerekir.", ""]
    satir = []
    if PS is not None:
        zz = PS["z"].iloc[-1]; t15 = PS["tet"]
        satir.append(["SAHOL/AKBNK artık z (β250 gecikmeli, z60)", f"z {f(zz)}, β {f(PS['beta'], 'f2')}",
                      f"z=+1,5: SAHOL ≥ {f(t15[1.5][0])} ya da AKBNK ≤ {f(t15[1.5][1])}; z=−1,5: SAHOL ≤ {f(t15[-1.5][0])} ya da AKBNK ≥ {f(t15[-1.5][1])}",
                      f"z>+1,5: F_SAHOL SAT + F_AKBNK AL; z<−1,5 tersi; {PS['n'][0]}:{PS['n'][1]} kontrat (K9 riski {pc2(R['k9_risk'] if R else 0.0025)}, kötü durum %9; rehber %1 riskte 4 katı); aynı gün uzlaşma; çıkış |z| ≤ 1,5",
                      f"model: {'LONG' if PS['side'] > 0 else 'SHORT' if PS['side'] < 0 else 'yok'}{(' (%d g)' % PS['held']) if PS['side'] else ''}, bugün {PS['act']}; "
                      f"mod: {DUR['ayarlar'].get('pratik_sahol_akbnk', 'kagit')} (K1 öncelikli)"])
    else:
        satir.append(["SAHOL/AKBNK artık z", "veri yok", "—", "—", "—"])
    if KZ is not None:
        L = KZ["L"]
        satir.append(["Koza z3 (TRMET − β·ort(TRALT,TRENJ), 3 gün)", f"z3 {f(L.z3)}, σ60 {f(L.sd60 * 1e4, 'f0')} bps, β_TA {f(L.bH)}",
                      f"TRMET ≥ {f(KZ['tet_al'])} (AL) / ≤ {f(KZ['tet_sat'])} (SAT), TRALT ve TRENJ yatayken",
                      f"z3>+1,5: TRMET1! AL + TRALT1! SAT (1:{f(L.bH * KZ['PM'] / KZ['PH'], 'f1')}); {KZ['n'][0]}:{KZ['n'][1]} kontrat (G {f(KZ['G'] / 1e3, 'f0')} bin TL); uzlaşmada gir, 2 gün, sinyal sürerse +2 (≤6)",
                      ("model: AÇIK " + ("TRMET AL/TRALT SAT" if KZ["pos"]["s"] > 0 else "TRMET SAT/TRALT AL") + f" (giriş {KZ['idx'][KZ['pos']['i0']]:%d.%m})" if KZ["pos"] else "model: pozisyon yok")
                      + ("; bugün kilit şüphesi" if KZ["kilit"] else "")])
    else:
        satir.append(["Koza z3", "veri yok", "—", "—", "—"])
    if AL_ is not None:
        satir.append(["Altın → TRALT (vekil: VİOP " + AL_["kod"] + " uzlaşma değişimi)", f"g {f(AL_['g'], '%')}, z {f(AL_['z'])} (σ %1,70 sabit)",
                      f"yarın 17:55 TVC:GOLD, bugünkü 17:55 fiyatına göre ±%1,70 (VİOP uzlaşmasıyla ≈ {f(AL_['F'] * math.exp(AL_['sig']), 'f1')} / {f(AL_['F'] * math.exp(-AL_['sig']), 'f1')})",
                      f"z>+1: TRALT1! AL + XU030D1! SAT; 1 XU030D : {AL_.get('N', '?')} TRALT1! (β {f(AL_.get('beta', np.nan))}); 1 mn TL'de 1 birim; 2 gün",
                      "canlı karar 17:55 (altin.pine alarmı)"])
    else:
        satir.append(["Altın → TRALT", "veri yok (bülten)", "—", "—", "—"])
    if BZ is not None:
        satir.append(["XU030 kapanış bazı sıçraması", f"b {f(BZ['b'] * 1e4, 'f0')} bps, Δb {f(BZ['db'] * 1e4, 'f0')} bps (z {f(BZ['z'])}; σ≈50 bps sabit)",
                      f"18:10–18:15 F/S oranı > {BZ['oran_ust']:.5f} (SAT) ya da < {BZ['oran_alt']:.5f} (AL)".replace(".", ",") + f"; bugünkü spotla F ≥ {f(BZ['F_ust'], 'f0')} / ≤ {f(BZ['F_alt'], 'f0')}",
                      "ucuz kapandıysa XU030D1! AL, pahalıysa SAT; ertesi gün uzlaşmada kapat; 1 mn TL'de 1 kontrat (K9 riski)",
                      "**TradingView alarmıyla izlenir** (canlı 18:10 fiyatı gerekir; bülten değeri yalnız bilgi)"])
    else:
        satir.append(["XU030 kapanış bazı", "veri yok", "—", "—", "TradingView alarmıyla izlenir"])
    satir.append(["TUPRS ← ABD rafinerileri (VLO, MPC, PSX, PBF − β·SPX)", "ABD tekil hisse verisi meşru kaynaktan yok",
                  "sinyal ABD kapanışında (00:00 TSİ) kesinleşir", "|z|>1: F_TUPRS z yönünde t uzlaşması, t+2 uzlaşmasında çık",
                  "**TradingView alarmıyla izlenir** (tuprs_alarm.pine)"])
    md += [tablo(["Sinyal", "Bugün", "Yarın tetik", "Tetiklenirse işlem (1 mn TL)", "Durum"], satir), ""]
    if KZ is not None and KZ["trades"]:
        md += ["Koza pratik kural, son işlemler (spot verisiyle yeniden oynatma): " + "; ".join(
            f"{KZ['idx'][p['i0']]:%d.%m} {'+' if p['s'] > 0 else '−'}TRMET → {KZ['idx'][p['out']]:%d.%m}" for p in KZ["trades"][-3:]), ""]
    if PS is not None and PS["T"]:
        md += ["SAHOL/AKBNK model, son işlemler: " + "; ".join(
            f"{t_['giris']:%d.%m} {'LONG' if t_['yon'] > 0 else 'SHORT'} (z {f(t_['z'])}) → {t_['cikis']:%d.%m}" if t_["cikis"] is not None else
            f"{t_['giris']:%d.%m} {'LONG' if t_['yon'] > 0 else 'SHORT'} açık" for t_ in PS["T"][-3:]), ""]

    # 4. takvim
    md += ["## 4. Takvim bayrakları (önümüzdeki 14 gün; statik tablo, PLAN_BIST §3.10/§7, PLAN_ABD §7)", ""]
    tb = takvim_bayraklari(ns, 14)
    md += [tablo(["Tarih", "Piyasa", "Olay", "Kural"], [[(f"{b:%d.%m}" + (f"–{e:%d.%m}" if e != b else "")), p, o, k] for b, e, p, o, k, _ in tb]) if tb else "_Yok._", "",
           "Otomatik **değil**: temettü (K3/K3b, A6), bedelsiz (A5), ZPAT (K5) pencereleri ve KAP olayları (TVF/birleşme/tedbir). Her Cuma KAP taraması elle; "
           "bilançosunu açıklayan isimleri makro.json 'bilanco_aciklayanlar_9_11' listesine, MSCI'dan çıkarılanları 'msci_cikarilanlar' listesine yazın.", ""]
    if son is not None and son <= pd.Timestamp("2026-11-09"):
        bek = sorted(x for x in bs.BILANCO_9_11 if x not in aciklayan)
        md += [f"9.11'e kadar bilanço bekleyen (KAP teyitli değil): {', '.join(bek)}.", ""]

    # 5. ABD
    md += ["## 5. ABD rejimi (PLAN_ABD §2.2–2.6; durum.json)", ""]
    if not abd or "k" not in abd:
        md += [f"_Veri yok_ ({(abd or {}).get('hata', 'FRED/CBOE indirilemedi')}). Son durum (durum.json): **{A.get('durum')}** ({A.get('son_tarih')}).", ""]
    else:
        k = abd["k"]; t = abd["t"]; Rs, Rn = A["ralli"]["SPX"], A["ralli"]["NDX"]
        md += [f"Hesap günü **{t:%d.%m.%Y}** (FRED SP500 son {abd['spx_fred_son'].date() if abd['spx_fred_son'] is not None else '—'}"
               + (", S&P kapanışı teyitsiz kaynak (durum.json 'teyitsiz')" if abd["teyitsiz"] else "")
               + f"; CBOE VIX son {abd['vix_son'].date() if abd['vix_son'] is not None else '—'}). Bu çalışmada işlenen yeni ABD günleri: {', '.join(abd['yeni']) or 'yok'}.", "",
               tablo(["Girdi", "Değer", "Koşul"], [
                   ["S&P 500", f"{f(k['spx'])} ({f(abd['spx_d'], '%')})", "—"],
                   ["S&P / 200 GHO", f"{f(k['s200'])} → oran " + f"{k['spx'] / k['s200']:.3f}".replace(".", ","), ("üstünde" if k["spx"] > k["s200"] else "**altında**") + ("; yakın bölge (< 1,02)" if k["spx"] / k["s200"] < 1.02 else "")],
                   ["S&P 10 / 20 / 50 GHO", f"{f(k['s10'], 'f0')} / {f(k['s20'], 'f0')} / {f(k['s50'], 'f0')}", "10 > 20 ✓" if k["s10"] > k["s20"] else "10 < 20 ✗"],
                   ["Nasdaq-100 10 / 20 GHO", f"{f(abd['n10'], 'f0')} / {f(abd['n20'], 'f0')} ({abd['ndx_t'].date() if abd['ndx_t'] is not None else '—'})", "10 > 20 ✓" if abd["n10"] > abd["n20"] else "10 < 20 ✗"],
                   ["VIX/VIX3M bugün / önceki", f"{f(k['vr'])} / {f(k['vr_onceki'])}", "KIRMIZI (a)" if k["ka"] else "< 1,00 ✓"],
                   ["KIRMIZI (b) S&P 2 kapanış < 200 GHO", "evet" if k["kb"] else "hayır", "—"],
                   ["KIRMIZI (c) S5FI<50 ve S5TH<60", "veri yok (TradingView INDEX:S5FI/S5TH, durum.json 'manuel')" if k["kc"] is None else ("evet" if k["kc"] else "hayır"), "elle"],
                   ["Ralli denemesi S&P", f"dip {f(Rs['dip'])} ({Rs['dip_tarihi']}); " + (f"1. gün {Rs['gun1']}, bugün {Rs['gun']}. gün" if Rs["gun1"] else "başlamadı"), "FTD 4. günden itibaren"],
                   ["Ralli denemesi NDX", f"dip {f(Rn['dip'])} ({Rn['dip_tarihi']}); " + (f"1. gün {Rn['gun1']}, bugün {Rn['gun']}. gün" if Rn["gun1"] else "başlamadı"), "—"],
                   ["FTD", (f"{A['ftd']['tarih']} {A['ftd']['endeks']} {f(A['ftd']['degisim'], '%')} (hacim teyidi: {A.get('ftd_hacim_teyit')}; durum.json 'ftd_hacim_teyit' true/false); "
                            f"15 seans içinde 10>20: {'oluştu' if A['ftd'].get('olustu_1020') else 'henüz yok'} ({A['ftd'].get('seans', 0)}. seans); "
                            f"FTD günü dibi (YEŞİL şartı, durum.json abd.ftd.gun_dibi elle): {A['ftd'].get('gun_dibi') or 'girilmedi'}"
                            + (" → **kırıldı, YEŞİL olunmaz**" if A['ftd'].get('gun_dibi_kirildi') else "") if A.get("ftd") else "yok"), "geçerli FTD ya da S&P 10>20 = SARI tetiği"],
                   ["SARI sayacı (3 kapanış kuralı)", str(A.get("sari_sayac", 0)), "3 → SARI"],
                   ["Pilot freni (elle)", "AKTİF" if A.get("pilot_freni") else "yok", "aktifse FTD + S&P > 50 GHO ek şartı"]]),
               "", f"**Durum: {A['durum']}** → " + ({"KIRMIZI": "yeni canlı giriş yok, yalnız gölge kayıt", "TURUNCU": "yeni canlı giriş yok, yalnız gölge kayıt",
                                                     "SARI": "günde ≤ 2 giriş, ≤ 4 açık, yakın bölgede 1 pozisyon / ısı ≤ %0,5; AI dışı izinli kümeler",
                                                     "YEŞİL": "faz boyutu, günde ≤ 3 giriş"}.get(A["durum"], "—"))
               + "; durum ertesi günün 16:45 emir bloğundan geçerli.", "",
               f"En erken: KIRMIZI (a) çıkışı {tr_tarih(abd['en_erken']['kirmizi_cikis'])} kapanışı; SARI tetiği (FTD/10>20) "
               f"{tr_tarih(abd['en_erken']['ftd']) if abd['en_erken']['ftd'] else 'mevcut'}; SARI kapanışı {tr_tarih(abd['en_erken']['sari'])}; "
               f"canlı pilot {tr_tarih(abd['en_erken']['pilot'])} 16:45–17:15 TSİ (takvim yasakları ayrıca: 17.11, 25.11, 27.11, 9.12). "
               "YEŞİL için S5FI ≥ 50 elle teyit edilmeli.", ""]
        for n_ in abd["notlar"]:
            md.append(f"- {n_}")
        if abd["notlar"]:
            md.append("")
        son5 = (A.get("gecmis") or [])[-5:]
        if son5:
            md += ["Son günler: " + "; ".join(f"{g['tarih'][5:]} {g['durum']}" for g in son5), ""]

    # 6. tazelik
    md += ["## 6. Veri tazeliği", "",
           tablo(["Kaynak", "Son tarih", "Durum", "Not"], [[k, v["son"] or "—", v["durum"], v["notu"]] for k, v in KAYNAK.items()] +
                 [["makro.json (elle)", M.get("guncellendi"), "BAYAT" if makro_yas > 7 else "OK", f"{makro_yas} gün önce"],
                  ["durum.json ABD sayaçları", A.get("son_tarih"), "OK", "PLAN_ABD §2.3–2.4"]]),
           "", f"Çalışma süresi {time.time() - T0:.0f} sn. Komut: `python3 kod/gunluk_oneri.py --cikti gunluk --veri <önbellek>`. Ayrıntı: ../OTOMASYON.md.", ""]
    metin = "\n".join(md)
    out = os.path.join(a.cikti, f"oneri_{tag}.md")
    open(out, "w", encoding="utf-8").write(metin)
    open(os.path.join(a.cikti, "SON.md"), "w", encoding="utf-8").write(metin)

    # ---- BILDIRIM ----------------------------------------------------------------------------------------------------
    # DENETIM 08.11: bildirim EYLEMLE baslar (telefonda ilk ~100 karakter gorunur), baglam sonra gelir
    kisa_t = lambda d: f"{['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'][pd.Timestamp(d).weekday()]} {pd.Timestamp(d):%d.%m}"
    aktif = [m for p, m in sorted(eylem, key=lambda x: x[0]) if p in ISLEM_P]
    if aktif:
        temiz = lambda s: s.replace("**", "").replace("~~", "").split(" — ")[0]
        parca = [f"{kisa_t(ns)} İŞLEM ({len(aktif)}): " + " | ".join(temiz(kisa.get(m, m))[:160] for m in aktif[:3])]
    else:
        parca = [f"{kisa_t(ns)}: İŞLEM YOK" + (" (BIST verisi yok)" if R is None else "")]
    kagit = [kisa[m] for p, m in sorted(eylem, key=lambda x: x[0]) if p in (5, 7) and m in kisa]
    if kagit:
        parca.append("İzle/kâğıt: " + " | ".join(kagit[:3]))
    dg_tet = [r_ for r_ in degrade if "TETİKLENDİ" in r_[5]]
    if dg_tet:
        parca.append("YEDEK KİP tetiklenen: " + ", ".join(f"{r_[1]} {r_[2].split(' ')[0]} {r_[3]} ({r_[0]})" for r_ in dg_tet[:3]))
    parca.append(f"{pd.Timestamp(tarih_etiket):%d.%m} kapanışı: " + (f"BIST {R['durum']}" + (", KRİZ VAR" if kriz_var else "") if R is not None else "BIST veri yok"))
    tk_ns = [o.split(" (")[0] for b_, e_, p_, o, k_, bl in takvim_bayraklari(ns, 0) if p_ == "BIST" and bl]
    if tk_ns:
        parca.append("Takvim: " + "; ".join(tk_ns))
    if yakin or degrade_yakin:
        yb = sorted(yakin + degrade_yakin, key=lambda t_: (t_["kol"].startswith("ABD"), abs(t_["uzak"])))
        parca.append("Yakın tetik: " + ", ".join(f"{t_['en']} {t_['op']}{f(t_['seviye'])} ({t_['kol']})" for t_ in yb[:4]))
    if abd and "k" in abd:
        parca.append(f"ABD {A['durum']} (VIX/VIX3M {f(abd['k']['vr'])}); en erken pilot {abd['en_erken']['pilot']:%d.%m}")
    else:
        parca.append(f"ABD veri yok (son durum {A.get('durum')}, {A.get('son_tarih')})")
    if kisa_uyari:
        parca.append("Uyarı: " + "; ".join(kisa_uyari))
    parca.append("Ayrıntı gunluk/SON.md")
    bil = ". ".join(parca)
    if len(bil) > 600:
        bil = bil[:596] + " …"
    open(os.path.join(a.cikti, "BILDIRIM.txt"), "w", encoding="utf-8").write(bil + "\n")

    # ---- durum.json ----------------------------------------------------------------------------------------------------
    DUR["son_calisma"] = f"{simdi:%Y-%m-%d %H:%M} TSI"
    if R is not None:
        DUR["bist"] = dict(son_tarih=str(son.date()), rejim=R["durum"], kriz="VAR" if kriz_var else "yok",
                           tetikler=[dict(kol=t_["kol"], en=t_["en"], kosul=t_["kosul"], seviye=round(t_["seviye"], 6), islem=t_["islem"])
                                     for t_ in tetik if t_["kol"] in ("K4", "K1", "PRATİK", "KOZA") and abs(t_["uzak"]) <= 0.10])
    if not a.durum_yazmadan:
        json.dump(DUR, open(os.path.join(a.cikti, "durum.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    print("yazildi:", out)
    print("BILDIRIM:", bil)
    print(f"sure {time.time() - T0:.0f} sn")


if __name__ == "__main__":
    main()
