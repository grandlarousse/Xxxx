#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bist_sinyal.py - PLAN_BIST.md kurallarinin gunluk aksam sinyalleri (swing; gun-ici degil).

NE YAPAR (her kapanistan sonra; 18:15 TSI sonrasi spot, 20:45 TSI sonrasi VIOP bulteni)
  1. Rejim gostergesi (plan s2): T1 XU100>SMA200, T2 TSMOM12, T3 5/5 kapanis SMA50 ustu, M1/M2/M4 (elle girilen
     makro), M5 XBANK>SMA200 -> AÇIK / GEÇİŞ / KAPALI ve KRİZ kesicisi (a-f).
  2. K4 kirilim adaylari (plan s3 K4, s4): B52 (bugun haric 252 gun zirvesi) + trend sablonu 7 kosul,
     likidite (60g medyan TL hacim, ilk 75), dislama listesi (statik + dinamik), kume/blok, boyut ornekleri.
  3. Kume 12 ay RS siralamasi (dalga_bist s4 tanimi: R = kume EW / XU100, skor R_t/R_t-252 - 1), 3 ay TL > nakit
     filtresi, 126g RS kirilimi.
  4. K1 SAHOL/AKBNK ve K2 KCHOL/sepet z-skorlari (60 gun, bugun dahil), kesisim tarihi ve K1 tam tetikleri.
  5. VIOP: RESMI bulten (viop_YYYYMMDD.csv) UZLASMA FIYATI ile XU030 ima basit/bilesik TL orani, TLREF ve
     mevduat neti +3 puan esigi; F_USDTRY on ay ima orani (KRİZ e); pay vadelisi ima oranlari.
  Cikti: <cikti>/bist_sinyal_<SONVERITARIHI>.md

KULLANIM
  python3 bist_sinyal.py --veri <onbellek_klasoru> --cikti <cikti_klasoru> [--makro makro.json] [--tarih YYYY-MM-DD]
  Makro dosyasi yoksa <veri>/makro.json aranir; o da yoksa betikteki 05.11.2026 degerleri kullanilir ve ciktida
  "VARSAYILAN" diye isaretlenir. Alanlar MAKRO_VARSAYILAN sozlugunde.

NOTLAR
  * python3 + requests + pandas + numpy. Varsayilan istek basliklari (User-Agent degistirilmez), istekler arasi bekleme.
  * Fiyatlar Is Yatirim ChartData (duzeltilmis kapanis), hacim Is Yatirim HisseTekil (TL), VIOP Borsa Istanbul bulteni.
  * Seans bitmeden (hafta ici 18:20 TSI oncesi) calisirsa bugunku (bitmemis) bar atilir.
  * Bilgi amaclidir; yatirim tavsiyesi degildir.
"""
import argparse, json, math, os, sys, time
from datetime import datetime, timedelta
import numpy as np, pandas as pd, requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bist_tarama as bt  # noqa: E402  (seri, endeks_listeleri, viop_bulten, VIOP, TSI, S)

HT_URL = "https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/HisseTekil"

# ---- plan s4.3 / dalga_bist s1: kumeler -------------------------------------------------------------------------
KUMELER = {
    "BANKA": "AKBNK GARAN YKBNK ISCTR VAKBN HALKB TSKB ALBRK SKBNK",
    "HOLDİNG": "KCHOL SAHOL DOHOL AGHOL ALARK TKFEN NTHOL GLYHO",
    "HAVACILIK": "THYAO PGSUS TAVHL CLEBI",
    "RAFİNERİ": "TUPRS PETKM AYGAZ TRCAS",
    "ÇELİK": "EREGL KRDMD ISDMR BRSAN CEMTS KCAER IZMDC",
    "KOZA_ALTIN": "TRALT TRMET TRENJ",
    "SAVUNMA": "ASELS OTKAR SDTTR ALTNY ONRYT",
    "ÇİMENTO": "CIMSA OYAKC AKCNS BTCIM NUHCM AFYON BSOKE GOLTS KONYA",
    "ELK_EKİPMAN": "ASTOR EUPWR GESAN KONTR PRKAB",
    "PERAKENDE": "BIMAS MGROS SOKM MAVI CRFSA",
    "OTOMOTİV": "FROTO TOASO DOAS TTRAK KARSN ASUZU",
    "OTO_YAN": "EGEEN BRISA KORDS FMIZP JANTS",
    "TELEKOM": "TCELL TTKOM",
    "GYO": "EKGYO ISGYO TRGYO SNGYO HLGYO OZKGY RYGYO",
    "KİMYA": "SASA AKSA ALKIM DYOBY KMPUR",
    "GÜBRE": "GUBRF HEKTS BAGFS",
    "CAM_SERAMİK": "SISE KUTPO EGSER USAK QUAGR",
    "GIDA": "ULKER AEFES CCOLA TATGD TUKAS BANVT PNSUT",
    "ELK_ÜRETİM": "AKSEN ENJSA ZOREN ODAS AYDEM AKENR",
    "YENİLENEBİLİR": "GWIND NATEN CWENE ALFAS SMRTG YEOTK",
    "TEKNOLOJİ": "LOGO NETAS KAREL INDES LINK ARDYZ FONET ALCTL",
    "BEYAZ_EŞYA": "ARCLK VESTL VESBE",
    "SİGORTA": "ANSGR AKGRT ANHYT TURSG AGESA RAYSG",
    "SAĞLIK": "SELEC DEVA ECILC LKMNH MPARK",
}
KUMELER = {k: v.split() for k, v in KUMELER.items()}
BLOK = {"BANKA": "Blok1", "HOLDİNG": "Blok1", "HAVACILIK": "Blok1", "TELEKOM": "Blok1", "GYO": "Blok1",
        "ELK_EKİPMAN": "Blok2", "YENİLENEBİLİR": "Blok2", "TEKNOLOJİ": "Blok2", "ELK_ÜRETİM": "Blok2",
        "ÇİMENTO": "Blok3", "OTO_YAN": "Blok3", "KİMYA": "Blok3", "CAM_SERAMİK": "Blok3", "BEYAZ_EŞYA": "Blok3",
        "SAĞLIK": "Blok3", "RAFİNERİ": "Ayrıştırıcı", "SAVUNMA": "Ayrıştırıcı", "KOZA_ALTIN": "Ayrıştırıcı",
        "ENERJİ_DAĞITIM": "Diğer"}
# K4 sayiminda plan s4.3: ENJSA, AHGAZ, ENERY tek kume; AHGAZ+ENERY tek isim (Ahlatci grubu, aktif geri alim)
K4_KUME_OZEL = {"ENJSA": "ENERJİ_DAĞITIM", "AHGAZ": "ENERJİ_DAĞITIM", "ENERY": "ENERJİ_DAĞITIM"}
ISIM_GRUBU = {"AHGAZ": "AHLATCI", "ENERY": "AHLATCI"}
GERI_ALIM = {"AHGAZ", "ENERY"}  # KAP 1693367 / 1693368 (05.11): neredeyse her gun ihracci geri alimi

# ---- plan s4.2 dislama listesi ------------------------------------------------------------------------------------
DISLAMA = {
    "SPK suç duyurusu": "KTLEV GUNDG DSTKF OZATD TRHOL ODINE VSNMD IEYHO ALKLC ANELE PASEU SELEC MANAS",
    "fon payı/fiili dolaşım >%20": "PASEU KTLEV ANELE TEHOL DSTKF IEYHO TMPOL ODINE ISVEA MAGEN BALSU ISKPL DAGI INFO "
                                   "TRHOL OZATD GUNDG PEKGY SKYLP SELEC KARCL GLRMK",
    "Tera/Pusula/Hedef/kayyum": "TERA TEHOL TRHOL HEDEF HDFGS DSTKF BIGEN",
}
DISLAMA_KOD = {}
for neden, kodlar in DISLAMA.items():
    for k in kodlar.split():
        DISLAMA_KOD.setdefault(k, neden)
LIMIT_ISIM = set("GUBRF TKFEN BRSAN HALKB SASA ASTOR VESTL HEKTS".split())  # %25 stop mesafesi (plan K4 Boyut)
K2_SEPET = ["TUPRS", "FROTO", "TOASO", "ARCLK", "YKBNK", "AYGAZ"]
# A1 (plan s3.10): 3C konsolide son gun 9.11; bilancosunu 9.11 18:00'den once aciklamamis isimler (KAP teyitli degil)
BILANCO_9_11 = set("KCHOL BIMAS PGSUS TCELL SOKM DOAS AKSEN ALARK EREGL ARCLK KRDMD ASTOR GUBRF HEKTS OYAKC CIMSA "
                   "TKFEN TRALT TRMET EKGYO VESTL ODAS AHGAZ ENERY RYSAS".split())

# ---- elle girilen makro (05.11.2026 degerleri; her Persembe 14:30 ve ayin 3'unde guncellenir) ----------------------
MAKRO_VARSAYILAN = {
    "kaynak": "VARSAYILAN (PLAN_BIST.md 05.11.2026 degerleri) - guncelleyin",
    "politika_faizi": 36.0,                 # %
    "mevduat_32g_brut": 39.52,              # % (banka ortalamasi, 100 bin TL)
    "net_rezerv_swap_haric": [["onceki hafta", 30.8], ["son hafta (5.11 yayini)", 24.3]],  # mlr $, eski -> yeni
    "brut_rezerv": 158.1,                   # mlr $
    "yabanci_dibs_hafta_mn_usd": -750,      # son hafta
    "tufe_aylik": [["2026-09", None], ["2026-10", 2.58]],  # % aylik, eski -> yeni
    "cds5y": 248, "cds5y_20g_once": None, "cds_teyitli": False,
    "msci_danisma": False,                  # MSCI Turkiye siniflandirma danismasi acildi mi
    "kural0": False,                        # araci kurum: teminat faizi / PPF teminati yazili teyit edildi mi
    "komisyon_viop_bps": None,              # yon basina, BSMV ve borsa payi dahil
    "usd_faiz": 0.039,                      # USDTRY ima TL orani icin USD kisa faiz varsayimi
}


def tsi_simdi():
    return datetime.now(bt.TSI)


def hacim_serisi(kod, veri, bugun, bekle):
    """HisseTekil'den gunluk TL hacim ve ham kapanis; onbellek <veri>/hacim/<KOD>.csv (son ~200 gun)."""
    d = os.path.join(veri, "hacim"); os.makedirs(d, exist_ok=True)
    f = os.path.join(d, kod + ".csv")
    eski = pd.read_csv(f, index_col=0, parse_dates=True) if os.path.exists(f) else None
    bas = (eski.index[-1] - pd.Timedelta(days=10)) if eski is not None and len(eski) else bugun - pd.Timedelta(days=200)
    p = {"hisse": kod, "startdate": bas.strftime("%d-%m-%Y"), "enddate": bugun.strftime("%d-%m-%Y")}
    yeni = None
    for k in range(3):
        try:
            r = bt.S.get(HT_URL, params=p, timeout=60)
            if r.status_code == 200 and r.text.strip():
                v = r.json().get("value") or []
                if v:
                    yeni = pd.DataFrame({"hacim": [x.get("HGDG_HACIM") for x in v],
                                         "ham": [x.get("HG_KAPANIS") for x in v]},
                                        index=pd.to_datetime([x["HGDG_TARIH"] for x in v], format="%d-%m-%Y"))
                break
            if r.status_code == 429:
                time.sleep(10 * (k + 1))
        except (requests.RequestException, ValueError):
            time.sleep(2 * (k + 1))
    time.sleep(bekle)
    if yeni is None:
        return eski
    s = yeni if eski is None else pd.concat([eski[eski.index < yeni.index[0]], yeni])
    s = s[~s.index.duplicated(keep="last")].sort_index().iloc[-260:]
    s.to_csv(f)
    return s


def yuzdelik(x):
    return (x.rank(pct=True) * 99).round(0)


def nakit_getiri(tlref, bas, son):
    """TLREF ile gunluk bilesik nakit getirisi (bas, son] (takvim gunu)."""
    t = tlref.loc[:son]
    t = t[t.index >= bas - pd.Timedelta(days=7)]
    if len(t) < 2:
        return np.nan
    gun = pd.date_range(bas, son, freq="D")[1:]
    oran = t.reindex(gun.union(t.index)).ffill().reindex(gun) / 100
    return float(np.prod(1 + oran.values / 365) - 1)


def z_seri(x, L=60):
    return (x - x.rolling(L).mean()) / x.rolling(L).std()


def temiz_fiyat(p):
    """rv_lag.py tanimi: |gunluk getiri| > %60 maskelenir, fiyat getirilerden yeniden kurulur."""
    r = p.pct_change()
    r = r.mask(r.abs() > 0.6)
    return (1 + r.fillna(0)).cumprod().where(p.notna()) * p.dropna().iloc[0]


def bisect(f, a, b, n=80):
    fa = f(a)
    for _ in range(n):
        m = (a + b) / 2
        fm = f(m)
        if (fm > 0) == (fa > 0):
            a, fa = m, fm
        else:
            b = m
    return (a + b) / 2


def k1_tetikler(sah, akb):
    """Diger bacak sabitken z=+2 ve z=-2 veren tam fiyatlar (60 gun, bugun dahil; plan K1)."""
    x = (np.log(sah) - np.log(akb)).dropna()
    s0, a0 = sah.iloc[-1], akb.iloc[-1]

    def z_ile(ps, pa):
        xx = x.copy(); xx.iloc[-1] = math.log(ps) - math.log(pa); w = xx.iloc[-60:]
        return (xx.iloc[-1] - w.mean()) / w.std()
    out = {}
    try:
        out["SAHOL_z+2"] = bisect(lambda p: z_ile(p, a0) - 2, s0 * 0.5, s0 * 1.6)
        out["SAHOL_z-2"] = bisect(lambda p: z_ile(p, a0) + 2, s0 * 0.5, s0 * 1.6)
        out["AKBNK_z+2"] = bisect(lambda p: z_ile(s0, p) - 2, a0 * 0.5, a0 * 1.6)
        out["AKBNK_z-2"] = bisect(lambda p: z_ile(s0, p) + 2, a0 * 0.5, a0 * 1.6)
    except Exception:
        pass
    return out


def son_kesisim(z, esik=2.0):
    """|z| < esik'ten |z| >= esik'e son gecis tarihi."""
    a = z.abs()
    k = (a >= esik) & (a.shift(1) < esik)
    return k[k].index[-1] if k.any() else None


def fmt(v, t="f2"):
    if v is None or (isinstance(v, float) and not np.isfinite(v)):
        return "—"
    if t == "%":  # Turkce: +%3,8 / −%16,5
        return ("+" if v >= 0 else "−") + f"%{abs(100 * v):.1f}".replace(".", ",")
    if t == "%u":
        return ("−" if v < 0 else "") + f"%{abs(100 * v):.1f}".replace(".", ",")
    if t == "f0":
        return f"{v:,.0f}".replace(",", ".").replace("-", "−")
    if t == "f1":
        return f"{v:.1f}".replace(".", ",").replace("-", "−")
    return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".").replace("-", "−")


def tablo(basliklar, satirlar):
    out = ["| " + " | ".join(basliklar) + " |", "|" + "---|" * len(basliklar)]
    out += ["| " + " | ".join(str(c) for c in s) + " |" for s in satirlar]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="PLAN_BIST gunluk sinyal")
    ap.add_argument("--veri", required=True, help="ham veri onbellek klasoru")
    ap.add_argument("--cikti", required=True, help="Markdown cikti klasoru")
    ap.add_argument("--makro", default=None, help="makro JSON (yoksa <veri>/makro.json, o da yoksa varsayilan)")
    ap.add_argument("--tarih", default=None, help="hesap tarihi YYYY-MM-DD (varsayilan: son tam kapanis)")
    ap.add_argument("--bas", default="2023-06-01", help="fiyat verisi baslangici")
    ap.add_argument("--bekle", type=float, default=0.7, help="istekler arasi bekleme (sn)")
    ap.add_argument("--yenile", action="store_true", help="fiyat onbellegini yeniden indir")
    ap.add_argument("--hacimsiz", action="store_true", help="HisseTekil hacim indirme (likidite filtresi onbellekten)")
    ap.add_argument("--cevrimdisi", action="store_true", help="hic istek atma; fiyat, hacim ve bulteni onbellekten oku")
    a = ap.parse_args()
    pxdir = os.path.join(a.veri, "px")
    for d in (a.veri, pxdir, a.cikti):
        os.makedirs(d, exist_ok=True)

    M = dict(MAKRO_VARSAYILAN)
    mf = a.makro or os.path.join(a.veri, "makro.json")
    if os.path.exists(mf):
        M.update(json.load(open(mf, encoding="utf-8"))); M.setdefault("kaynak", mf)
        if M["kaynak"].startswith("VARSAYILAN"): M["kaynak"] = mf

    simdi = tsi_simdi()
    bugun = pd.Timestamp(simdi.date())
    seans_bitmedi = simdi.weekday() < 5 and simdi.hour * 60 + simdi.minute < 18 * 60 + 20
    kesim = pd.Timestamp(a.tarih) if a.tarih else (bugun - pd.Timedelta(days=1) if seans_bitmedi else bugun)

    if a.cevrimdisi and os.path.exists(os.path.join(a.veri, "endeks_kap.json")):
        _e = json.load(open(os.path.join(a.veri, "endeks_kap.json"))); b100, b50, kaynak = _e["XU100"], _e["XU050"], "KAP önbellek"
    else:
        b100, b50, kaynak = bt.endeks_listeleri(a.veri)
    kume_uye = sorted({u for v in KUMELER.values() for u in v})
    hisseler = sorted(set(bt.VIOP) | set(b100) | set(kume_uye) | set(K2_SEPET))
    endeksler = ["XU100", "XU030", "XBANK", "USDTRY", "TLREF"]
    print(f"BIST100: {kaynak} ({len(b100)}); hisse: {len(hisseler)}; kesim {kesim.date()}", flush=True)

    D, bos = {}, []
    for i, k in enumerate(endeksler + hisseler, 1):
        if a.cevrimdisi:
            f = os.path.join(pxdir, k + ".csv")
            s = pd.read_csv(f, index_col=0, parse_dates=True)["px"] if os.path.exists(f) else pd.Series(dtype=float)
        else:
            s = bt.seri(k, pxdir, datetime.strptime(a.bas, "%Y-%m-%d"), simdi.replace(tzinfo=None), a.yenile, a.bekle)
        s = s[s.index <= kesim] if len(s) else s
        if len(s): D[k] = s.astype(float)
        else: bos.append(k)
        if i % 40 == 0: print(f"  fiyat {i}/{len(endeksler) + len(hisseler)}", flush=True)
    xu = D["XU100"]; son = xu.index[-1]
    tlref = D.get("TLREF"); usd = D.get("USDTRY")

    # ---- hacim / likidite -----------------------------------------------------------------------------------------
    HV = {}
    for i, k in enumerate(hisseler, 1):
        if k not in D: continue
        if a.hacimsiz or a.cevrimdisi:
            f = os.path.join(a.veri, "hacim", k + ".csv")
            h = pd.read_csv(f, index_col=0, parse_dates=True) if os.path.exists(f) else None
        else:
            h = hacim_serisi(k, a.veri, kesim, a.bekle)
        if h is not None and len(h):
            h = h[h.index <= son]
            HV[k] = float(h["hacim"].iloc[-60:].median()) if len(h) >= 20 else np.nan
        if i % 40 == 0: print(f"  hacim {i}/{len(hisseler)}", flush=True)
    liq_tum = pd.Series(HV).dropna().sort_values(ascending=False)
    liq = liq_tum[liq_tum.index.isin(set(bt.VIOP) | set(b100))]  # plan s4.1: tarama evreni VIOP-47 + BIST100
    lsira = pd.Series(np.arange(1, len(liq) + 1), index=liq.index)
    lsira_tum = pd.Series(np.arange(1, len(liq_tum) + 1), index=liq_tum.index)

    # ---- 1. rejim -------------------------------------------------------------------------------------------------
    sma = lambda s, n: s.rolling(n).mean()
    xs50, xs200 = sma(xu, 50), sma(xu, 200)
    T1 = bool(xu.iloc[-1] > xs200.iloc[-1])
    T3 = bool((xu.iloc[-5:] > xs50.iloc[-5:]).all())
    xu12 = xu.iloc[-1] / xu.iloc[-253] - 1
    nakit12 = nakit_getiri(tlref, xu.index[-253], son) if tlref is not None else np.nan
    ppf12 = 0.455  # plan s2.1 T2: karar icin gerceklesen brut PPF medyani (15.860 esigi)
    T2 = bool(xu12 > max(nakit12 if np.isfinite(nakit12) else 0, ppf12))
    xb = D["XBANK"]; M5 = bool(xb.iloc[-1] > sma(xb, 200).iloc[-1])
    nr = [v for _, v in M["net_rezerv_swap_haric"] if v is not None]
    nr_deg = list(np.diff(nr)) if len(nr) >= 2 else []
    M1 = bool(len(nr_deg) >= 3 and all(d > 0 for d in nr_deg[-3:]))
    tufe = [v for _, v in M["tufe_aylik"] if v is not None]
    M2 = bool(len(tufe) >= 2 and all(v < 2.0 for v in tufe[-2:]))
    cds, cds20, cds_ok = M.get("cds5y"), M.get("cds5y_20g_once"), bool(M.get("cds_teyitli"))
    M4 = bool(cds_ok and cds is not None and cds < 230 and cds20 is not None and cds < cds20)
    if T1:
        durum = "AÇIK"
    elif T3 and M1 and (M2 or M4 or M5):
        durum = "GEÇİŞ"
    else:
        durum = "KAPALI"
    acik_say = sum([T1, T2, T3, M1, M2, M4, M5])

    # ---- 5. VIOP bulteni ------------------------------------------------------------------------------------------
    B, btar = bt.viop_bulten(son, a.veri, bekle=a.bekle)
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
            if T <= 0 or not x["UZLASMA FIYATI"] > 0: continue
            basit = (x["UZLASMA FIYATI"] / S30 - 1) * 365 / T
            bil = (x["UZLASMA FIYATI"] / S30) ** (365 / T) - 1
            vsat.append([x["SOZLESME KODU"], x["VADE TARIHI"].date(), T, fmt(x["UZLASMA FIYATI"], "f0"), fmt(S30, "f0"),
                         fmt(basit, "%u"), fmt(bil, "%u"), fmt(tl_b, "%u"), fmt(mev_net + 0.03, "%u"),
                         "AÇ (Kural 0 da gerekli)" if basit >= mev_net + 0.03 else "kapalı",
                         fmt(x["ISLEM HACMI"] / 1e6, "f0"), fmt(x["ACIK POZISYON"], "f0")])
        Su, _ = spot_at("USDTRY")
        ur = B[B["SOZLESME KODU"].str.match(r"^F_USDTRY\d{4}$")].sort_values("VADE TARIHI")
        ur = ur[(ur["VADE TARIHI"] - btar).dt.days > 5]
        if len(ur) and np.isfinite(Su):
            x = ur.iloc[0]; T = (x["VADE TARIHI"] - btar).days
            ima = ((x["UZLASMA FIYATI"] / Su) * (1 + M["usd_faiz"] * T / 360) - 1) * 365 / T
            usd_on = dict(kod=x["SOZLESME KODU"], F=x["UZLASMA FIYATI"], S=Su, T=T, ima=ima)
        for k in ["SAHOL", "AKBNK", "GARAN", "YKBNK", "KCHOL", "ENJSA", "TUPRS", "THYAO", "BIMAS"]:
            Sk, _ = spot_at(k)
            r = B[B["SOZLESME KODU"].str.match(rf"^F_{k}\d{{4}}$")].sort_values("VADE TARIHI")
            r = r[(r["VADE TARIHI"] - btar).dt.days > 3].head(2)
            for _, x in r.iterrows():
                T = (x["VADE TARIHI"] - btar).days
                if not (np.isfinite(Sk) and x["UZLASMA FIYATI"] > 0): continue
                ima = (x["UZLASMA FIYATI"] / Sk - 1) * 365 / T
                hisse_vadeli.append([x["SOZLESME KODU"], T, fmt(x["UZLASMA FIYATI"]), fmt(Sk), fmt(ima, "%u"),
                                     f"{100 * (mev_net - ima):+.1f}".replace(".", ","),
                                     fmt(x["ISLEM HACMI"] / 1e6, "f0"), fmt(x["ACIK POZISYON"], "f0"),
                                     "E" if (mev_net - ima >= 0.03 and x["ACIK POZISYON"] >= 20000
                                             and x["ISLEM HACMI"] >= 1e8 and T > 30) else "H"])

    # ---- KRİZ kesicisi --------------------------------------------------------------------------------------------
    kriz = {}
    kriz["a XU100 5 gün ≤ −%8"] = (xu.iloc[-1] / xu.iloc[-6] - 1, xu.iloc[-1] / xu.iloc[-6] - 1 <= -0.08)
    hiz = (usd.iloc[-1] / usd.iloc[-11]) ** (252 / 10) - 1 if usd is not None and len(usd) > 11 else np.nan
    kriz["b USDTRY 10g yıllık > %35"] = (hiz, bool(np.isfinite(hiz) and hiz > 0.35))
    kriz["c CDS > 300 (teyitli)"] = (cds, bool(cds_ok and cds is not None and cds > 300))
    nr_kriz = bool((len(nr_deg) >= 2 and all(d <= -5 for d in nr_deg[-2:])) or (nr and nr[-1] < 0))
    kriz["d net rezerv 2 hafta ≤ −5 mlr $ ya da < 0"] = (" / ".join(fmt(float(d), "f1") for d in nr_deg[-2:]) + " mlr $ (haftalık değişim)" if nr_deg else None, nr_kriz)
    ekriz = bool(usd_on and usd_on["ima"] > M["politika_faizi"] / 100 + 0.05)
    kriz["e F_USDTRY ön ay ima > politika + 5"] = (usd_on["ima"] if usd_on else None, ekriz)
    kriz["f MSCI danışma"] = ("evet" if M.get("msci_danisma") else "hayır", bool(M.get("msci_danisma")))
    kriz_var = any(v[1] for v in kriz.values())

    # ---- K6 kapisi ------------------------------------------------------------------------------------------------
    k6 = {
        "1 net rezerv 2 hf değişim ≥ −2 ve seviye ≥ 20": bool(len(nr) >= 3 and nr[-1] - nr[-3] >= -2 and nr[-1] >= 20)
        if len(nr) >= 3 else bool(len(nr) >= 2 and nr[-1] - nr[-2] >= -2 and nr[-1] >= 20),
        "2 yabancı DİBS haftalık ≥ −500 mn $": bool(M["yabanci_dibs_hafta_mn_usd"] is not None and M["yabanci_dibs_hafta_mn_usd"] >= -500),
        "3 F_USDTRY ön ay ima ≤ politika + 5 (CDS yerine)": bool(usd_on and not ekriz),
        "4 USDTRY 10g yıllık ≤ %30": bool(np.isfinite(hiz) and hiz <= 0.30),
        "5 brüt rezerv ≥ 160": bool(M["brut_rezerv"] is not None and M["brut_rezerv"] >= 160),
        "6 Kural 0": bool(M.get("kural0")),
    }

    # ---- 2. K4 kirilim --------------------------------------------------------------------------------------------
    rows = []
    for k in hisseler:
        c = D.get(k)
        if c is None or len(c) < 260 or c.index[-1] < son: continue
        r = c.pct_change()
        s50, s150, s200 = sma(c, 50), sma(c, 150), sma(c, 200)
        onc252 = c.iloc[-253:-1].max()
        z252 = c.iloc[-252:].max(); d252 = c.iloc[-252:].min()
        g = lambda n: c.iloc[-1] / c.iloc[-1 - n] - 1
        rows.append(dict(kod=k, kapanis=c.iloc[-1], b52=bool(c.iloc[-1] > onc252), tetik=z252,
                         uzak=z252 / c.iloc[-1] - 1,
                         tt_dizilim=bool(c.iloc[-1] > s50.iloc[-1] > s150.iloc[-1] > s200.iloc[-1]),
                         tt_egim=bool(s200.iloc[-1] > s200.iloc[-22]), tt_dip=bool(c.iloc[-1] >= 1.25 * d252),
                         tt_zirve=bool(c.iloc[-1] >= 0.75 * z252), sma50=s50.iloc[-1],
                         R=0.4 * g(63) + 0.2 * g(126) + 0.2 * g(189) + 0.2 * g(252),
                         atr=r.abs().iloc[-14:].mean() * 1.25,
                         limit60=int((r.iloc[-60:].abs() >= 0.095).sum()),
                         limit60_up=int((r.iloc[-60:] >= 0.095).sum()), limit60_dn=int((r.iloc[-60:] <= -0.095).sum()),
                         gecmis=len(c), viop=k in bt.VIOP))
    K = pd.DataFrame(rows).set_index("kod")
    K["lsira"] = lsira.reindex(K.index)
    rs_ev = [k for k in K.index if lsira_tum.get(k, 999) <= 150] if len(lsira_tum) >= 50 else list(K.index)
    K["rs"] = np.nan; K.loc[rs_ev, "rs"] = yuzdelik(K.loc[rs_ev, "R"])
    K["tt_rs"] = K.rs >= 80
    K["tt_puan"] = K[["tt_dizilim", "tt_egim", "tt_dip", "tt_zirve", "tt_rs"]].sum(axis=1) + 2  # +B52 ve evren ayrica
    stok_kume = {u: kk for kk, uu in KUMELER.items() for u in uu}
    stok_kume.update(K4_KUME_OZEL)
    K["kume"] = [stok_kume.get(k, "—") for k in K.index]
    K["blok"] = [BLOK.get(stok_kume.get(k, ""), "Diğer") for k in K.index]

    def dislama_nedeni(k):
        n = []
        if k in DISLAMA_KOD: n.append(DISLAMA_KOD[k])
        if K.at[k, "limit60"] >= 3:
            n.append(f"60g'de {K.at[k, 'limit60']} limit kapanış: {K.at[k, 'limit60_up']}↑/{K.at[k, 'limit60_dn']}↓")
        if K.at[k, "gecmis"] < 252: n.append("<252 gün")
        return "; ".join(n)
    K["dislama"] = [dislama_nedeni(k) for k in K.index]
    K["evren75"] = K.lsira <= 75
    K["tt_tam"] = K.tt_dizilim & K.tt_egim & K.tt_dip & K.tt_zirve & K.tt_rs
    K["nitelikli"] = K.b52 & K.tt_tam & K.evren75 & (K.dislama == "")
    K["stop"] = [0.25 if (k in LIMIT_ISIM or K.at[k, "atr"] > 0.045) else 0.15 for k in K.index]
    r0 = {"AÇIK": 0.0075, "GEÇİŞ": 0.005, "KAPALI": 0.0025}[durum]
    K["nominal"] = r0 * np.where(K.viop, 1.0, 0.75) / K.stop
    once_bilanco = son < pd.Timestamp("2026-11-10")
    nit = K[K.nitelikli].sort_values("rs", ascending=False)
    izle = K[(~K.nitelikli) & (K.dislama == "") & (K.lsira <= 100) & (K.uzak <= 0.15) &
             ((K.tt_dizilim.astype(int) + K.tt_egim + K.tt_dip + K.tt_zirve + K.tt_rs) >= 4)].sort_values("uzak")

    def bayrak(k):
        b = []
        if once_bilanco and k in BILANCO_9_11: b.append("bilanço 9.11 akşamı → karar 10.11")
        if k in GERI_ALIM: b.append("aktif geri alım")
        if k in ISIM_GRUBU: b.append("AHGAZ+ENERY tek isim")
        if not K.at[k, "viop"]: b.append("spot ×0,75")
        if K.at[k, "stop"] == 0.25: b.append("stop %25")
        if not K.at[k, "evren75"]: b.append("K4 evreni dışı (likidite sırası > 75)")
        return ", ".join(b)

    def boyut(k):
        nom = K.at[k, "nominal"]
        cap = 0.02 * HV.get(k, np.nan)
        out = []
        for h in (1e6, 5e6, 20e6):
            tl = nom * h
            if np.isfinite(cap): tl = min(tl, cap)
            out.append(fmt(tl / 1e3, "f0"))
        return "/".join(out)

    # ---- 3. kume RS -----------------------------------------------------------------------------------------------
    ks = []
    xr = xu.pct_change()
    nakit3 = nakit_getiri(tlref, xu.index[-64], son) if tlref is not None else np.nan
    for kk, uu in KUMELER.items():
        rr = []
        for u in uu:
            s = D.get(u)
            if s is None or len(s) < 150: continue
            r = s.pct_change(); r = r.mask(r.abs() > 0.35, 0.0); r.iloc[:21] = np.nan
            rr.append(r.rename(u))
        if len(rr) < 2: continue
        R = pd.concat(rr, axis=1, sort=True).reindex(xu.index)
        ew = (1 + R.mean(axis=1).fillna(0)).cumprod()
        rel = ew / xu
        if rel.notna().sum() < 260: continue
        g50 = np.mean([D[u].iloc[-1] > sma(D[u], 50).iloc[-1] for u in R.columns if len(D[u]) >= 50])
        h126 = rel.iloc[-126:]
        ks.append(dict(kume=kk, blok=BLOK.get(kk, "Diğer"), rs12=rel.iloc[-1] / rel.iloc[-253] - 1,
                       rel3=rel.iloc[-1] / rel.iloc[-64] - 1, tl3=ew.iloc[-1] / ew.iloc[-64] - 1,
                       rma50=rel.iloc[-1] / rel.iloc[-50:].mean() - 1, gun126=int(len(h126) - 1 - int(np.argmax(h126.values))),
                       gen50=g50, uye=len(R.columns)))
    KS = pd.DataFrame(ks).sort_values("rs12", ascending=False).reset_index(drop=True)

    # ---- 4. ciftler -----------------------------------------------------------------------------------------------
    sah, akb = temiz_fiyat(D["SAHOL"]), temiz_fiyat(D["AKBNK"])
    x1 = (np.log(sah) - np.log(akb)).dropna(); z1 = z_seri(x1)
    tet = k1_tetikler(sah, akb)
    kc = temiz_fiyat(D["KCHOL"])
    sep = pd.concat([temiz_fiyat(D[u]) for u in K2_SEPET if u in D], axis=1)
    bk = np.exp(np.log(sep).diff().mean(axis=1).fillna(0).cumsum())
    x2 = (np.log(kc) - np.log(bk)).dropna(); z2 = z_seri(x2)
    kes1, kes2 = son_kesisim(z1), son_kesisim(z2)

    def cift_karar(z, kes, yeni_kesisim_sart):
        zz = z.iloc[-1]
        if abs(zz) < 2: return "sinyal yok"
        yon = "pay SAT / karşı AL" if zz > 0 else "pay AL / karşı SAT"
        if yeni_kesisim_sart and (kes is None or kes != z.index[-1]):
            return f"\\|z\\| ≥ 2 ama kesişim {kes.date() if kes is not None else '?'} → bayat, giriş yok"
        return f"SİNYAL: {yon}, giriş ertesi gün 17:55 (Kural 0 + komisyon kapısı)"

    # ---- cikti ----------------------------------------------------------------------------------------------------
    tag = son.strftime("%Y%m%d")
    bulten_not = (f"{btar.date()}" + (" (BAYAT: spot kesimi " + str(son.date()) + ")" if btar is not None and btar < son else "")) if btar is not None else "YOK"
    x30 = vsat[0] if vsat else None
    head = (f"**Özet {son.date()}:** Rejim **{durum}** ({acik_say}/7 açık) | KRİZ: **{'VAR' if kriz_var else 'yok'}** | "
            f"K4 nitelikli: **{len(nit)}** | K1 z **{fmt(z1.iloc[-1])}**, K2 z **{fmt(z2.iloc[-1])}** | "
            + (f"XU030 {x30[0]} ima basit **{x30[5]}** / bileşik {x30[6]} (eşik {x30[8]}) → **{x30[9]}**" if x30 else "VİOP bülteni yok")
            + f" | bülten {bulten_not}")
    md = [f"# BIST günlük sinyal — {son.date()} kapanışı (üretim {simdi:%Y-%m-%d %H:%M} TSİ)", "", head, "",
          f"Kaynak: İş Yatırım ChartData/HisseTekil (varsayılan başlık), Borsa İstanbul VİOP bülteni, KAP endeks listesi ({kaynak}). "
          f"Makro: {M['kaynak']}. Bulunamayan kod: {', '.join(bos) or '—'}. Bilgi amaçlıdır.", ""]
    md += ["## 1. Rejim (PLAN §2)", tablo(["Kod", "Koşul", "Değer", "Durum"], [
        ["T1", "XU100 > SMA200", f"{fmt(xu.iloc[-1], 'f0')} vs {fmt(xs200.iloc[-1], 'f0')} ({fmt(xu.iloc[-1] / xs200.iloc[-1] - 1, '%')})", int(T1)],
        ["T2", "XU100 12 ay > nakit 12 ay (max TLREF, PPF %45,5)", f"{fmt(xu12, '%')} vs TLREF bileşik {fmt(nakit12, '%')} / PPF +%45,5; bugünkü eşik ~{fmt(xu.iloc[-253] * (1 + max(nakit12 if np.isfinite(nakit12) else 0, ppf12)), 'f0')} (plan 30.11 eşiği 15.860)", int(T2)],
        ["T3", "XU100 son 5 kapanış > SMA50", f"SMA50 {fmt(xs50.iloc[-1], 'f0')} ({fmt(xu.iloc[-1] / xs50.iloc[-1] - 1, '%')})", int(T3)],
        ["M1", "Swap hariç net rezerv 3 hafta artış (elle)", " → ".join(fmt(float(v), "f1") for v in nr) + " mlr $", int(M1)],
        ["M2", "Aylık TÜFE < %2, 2 ay üst üste (elle)", " / ".join(f"{k}: {fmt(float(v), 'f2')}" for k, v in M["tufe_aylik"] if v is not None), int(M2)],
        ["M4", "CDS < 230 ve düşüyor (teyitli, elle)", f"{cds} (teyitli: {'E' if cds_ok else 'H'})", int(M4)],
        ["M5", "XBANK > SMA200", f"{fmt(xb.iloc[-1], 'f0')} vs {fmt(sma(xb, 200).iloc[-1], 'f0')}", int(M5)]]),
        "", f"**Durum: {durum}** → K4 r₀ = %{100 * r0:.2f}".replace(".", ",") + "; ertesi işlem gününden geçerli.", "",
        "**KRİZ kesicisi (herhangi biri):**", tablo(["Tetik", "Değer", "Tetiklendi"], [
            [k, (fmt(v[0], '%') if isinstance(v[0], float) else str(v[0])), "EVET" if v[1] else "—"] for k, v in kriz.items()]),
        "", f"**K6 carry kapısı:** {'AÇIK' if all(k6.values()) else 'KAPALI'} — " +
        "; ".join(f"{k}: {'✓' if v else '✗'}" for k, v in k6.items()), ""]
    md += ["## 2. K4 kırılım (PLAN §3 K4; evren ilk 75 likit, dışlama hariç)",
           f"Likidite sırası {len(liq)} hissede hesaplandı (60g medyan TL hacim). RS = 0,4·R3a+0,2·R6a+0,2·R9a+0,2·R12a, "
           f"ilk 150 likit içinde yüzdelik. Tetik = yarın aşılması gereken kapanış (bugün dahil 252 gün zirvesi).", ""]
    if len(nit):
        md += ["**Nitelikli (giriş ertesi gün kapanış seansı 18:01–18:05; alış limiti = min(bugün kapanış × 1,06; son fiyat × 1,03)):**",
               tablo(["Hisse", "Kapanış", "RS", "Likidite sırası", "Küme/Blok", "Stop", "Boyut % (1/5/20 mn TL, bin TL)", "Bayrak"],
                     [[k, fmt(x.kapanis), int(x.rs), int(x.lsira), f"{x.kume}/{x.blok}", f"%{int(100 * x.stop)}",
                       f"%{100 * x.nominal:.2f} ({boyut(k)})".replace(".", ","), bayrak(k)] for k, x in nit.iterrows()]), ""]
    else:
        md += ["**Nitelikli: yok.**", ""]
    md += ["**Bekleme listesi (tetiğe ≤ %15, şablonun 5 alt koşulundan ≥ 4'ü, ilk 100 likit):**",
           tablo(["Hisse", "Kapanış", "Tetik (kapanış >)", "Gereken", "Şablon (diz/eğim/dip/zirve/RS)", "RS", "Lik. sıra", "SMA50", "Küme", "Bayrak"],
                 [[k, fmt(x.kapanis), fmt(x.tetik), fmt(x.uzak, '%'),
                   "".join("✓" if x[c] else "✗" for c in ["tt_dizilim", "tt_egim", "tt_dip", "tt_zirve", "tt_rs"]),
                   "—" if pd.isna(x.rs) else int(x.rs), "—" if pd.isna(x.lsira) else int(x.lsira), fmt(x.sma50), x.kume, bayrak(k)]
                  for k, x in izle.head(15).iterrows()]) if len(izle) else "_Yok._", ""]
    b52b = K[K.b52 & ~K.nitelikli]
    md += ["Bugün 52 hafta kırılımı yapıp nitelik kazanmayanlar: " + (", ".join(
        f"{k} (" + ", ".join(x for x, ok in [("şablon eksik", not K.at[k, 'tt_tam']), ("evren dışı", not K.at[k, 'evren75']),
                                              ("dışlama", K.at[k, 'dislama'] != "")] if ok) + ")" for k in b52b.index) or "—"), ""]
    dis = K[(K.dislama != "") & (K.lsira <= 100)]
    md += [f"Dışlananlar (ilk 100 likit içinde): " + (", ".join(f"{k} ({x.dislama})" for k, x in dis.iterrows()) or "—"), ""]
    md += ["## 3. Küme 12 ay RS (dalga_bist §4; K7 filtresi ve K4 önceliği)",
           tablo(["Sıra", "Küme", "Blok", "RS 12 ay", "rel 3 ay", "TL 3 ay", "> nakit 3 ay", "R/MA50", "126g RS zirvesinden gün", "Genişlik 50", "Üye"],
                 [[i + 1, x.kume, x.blok, fmt(x.rs12, '%'), fmt(x.rel3, '%'), fmt(x.tl3, '%'),
                   "E" if x.tl3 > nakit3 else "H", fmt(x.rma50, '%'), ("**0 (KIRILIM)**" if x.gun126 == 0 else x.gun126),
                   fmt(x.gen50, '%u'), x.uye] for i, x in KS.iterrows()]),
           "", f"Nakit 3 ay (TLREF): {fmt(nakit3, '%')}. İlk 3: {', '.join(KS.kume.head(3))}. "
           f"Filtre (3 ay TL > nakit) geçen ilk 3 içinden: {', '.join(KS.head(3)[KS.head(3).tl3 > nakit3].kume) or 'yok → nakit'}.", ""]
    md += ["## 4. Çift kolları (PLAN §3 K1, K2)",
           tablo(["Kol", "z (60g, bugün dahil)", "Son \\|z\\| ≥ 2 kesişimi", "Karar"],
                 [["K1 SAHOL/AKBNK", fmt(z1.iloc[-1]), kes1.date() if kes1 is not None else "—", cift_karar(z1, kes1, False)],
                  ["K2 KCHOL/sepet", fmt(z2.iloc[-1]), kes2.date() if kes2 is not None else "—", cift_karar(z2, kes2, True)]]),
           "", f"K1 tam tetikler (diğer bacak sabit; SAHOL {fmt(D['SAHOL'].iloc[-1])}, AKBNK {fmt(D['AKBNK'].iloc[-1])}): "
           f"z=+2 → SAHOL ≥ {fmt(tet.get('SAHOL_z+2'))} ya da AKBNK ≤ {fmt(tet.get('AKBNK_z+2'))}; "
           f"z=−2 → SAHOL ≤ {fmt(tet.get('SAHOL_z-2'))} ya da AKBNK ≥ {fmt(tet.get('AKBNK_z-2'))}.", ""]
    md += [f"## 5. VİOP resmî bülten (uzlaşma fiyatı; bülten tarihi {bulten_not})",
           "İma basit oran = (F_uzlaşma / S_kapanış − 1) × 365 / gün; spot, bültenin kendi tarihindeki kapanış. "
           f"Eşik = 32 gün mevduat neti ({fmt(mev_net, '%u')}) + 3 puan.", ""]
    if vsat:
        md += [tablo(["Kontrat", "Vade", "Gün", "Uzlaşma", "XU030", "İma basit", "İma bileşik", "TLREF", "Eşik", "Nakit-taşıma", "Hacim mn TL", "Açık poz."], vsat), ""]
    if usd_on:
        md += [f"F_USDTRY ön ay {usd_on['kod']}: uzlaşma {fmt(usd_on['F'], 'f2')}, spot {fmt(usd_on['S'], 'f2')} (ChartData kapanışı; saat farkı ±1–2 puan), "
               f"{usd_on['T']} gün, USD faizi {fmt(M['usd_faiz'], '%u')} varsayımıyla ima TL basit **{fmt(usd_on['ima'], '%u')}** "
               f"(politika + 5 = %{M['politika_faizi'] + 5:.0f}).", ""]
    if hisse_vadeli:
        md += ["Pay vadelileri (long için vadeli kuralı §1.5: mevduat neti − ima ≥ 3 puan, açık poz. ≥ 20.000, hacim ≥ 100 mn TL, Kasım değil):",
               tablo(["Kontrat", "Gün", "Uzlaşma", "Spot", "İma basit", "Mevduat neti − ima (puan)", "Hacim mn TL", "Açık poz.", "Kural sağlanıyor"], hisse_vadeli), ""]
    md += ["## 6. Ertesi gün emir özeti", (
        "- KRİZ VAR: 5 işlem günü yeni giriş yok; K6 kapanır; hedgesiz K3 kapanır; K4/K5/K9 stop = max(iz-stop, kapanış × 0,90)."
        if kriz_var else "- KRİZ yok."),
        f"- K4: {'nitelikli ' + ', '.join(nit.index) + ' → takvim ve A-kurallarını (A1–A4) kontrol et' if len(nit) else 'emir yok'}.",
        f"- K1: {cift_karar(z1, kes1, False)}. K2: {cift_karar(z2, kes2, True)}.",
        f"- XU030 nakit-taşıma: {x30[9] if x30 else 'bülten yok'}; F_USDTRY ön ay ima {fmt(usd_on['ima'], '%u') if usd_on else '—'} (KRİZ e eşiği %{M['politika_faizi'] + 5:.0f}); K6 kapısı {'AÇIK' if all(k6.values()) else 'KAPALI'}.",
        "- Takvim kısıtları (PLAN §3.10 A1–A10), K3/K3b temettü takvimi ve bedelsiz pencereleri elle kontrol edilir; bu betik KAP'ı taramaz.",
        "- Emir limitleri (PLAN §3, §6.2): alış min(plan limiti; P_son × 1,03); risk azaltan satış max(taban; P_son × 0,97); 18:01–18:05.", ""]
    out = os.path.join(a.cikti, f"bist_sinyal_{tag}.md")
    open(out, "w", encoding="utf-8").write("\n".join(md))
    print("yazildi:", out)
    print(head)


if __name__ == "__main__":
    main()
