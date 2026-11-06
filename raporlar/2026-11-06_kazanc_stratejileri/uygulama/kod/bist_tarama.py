#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BIST / VIOP haftalik tarama (swing, gun-ici degil).

NE YAPAR
  Is Yatirim ChartData (gunluk, temettu/bolunme duzeltmeli kapanis) verisiyle:
   (a) piyasa rejimi : XU100 / XU030 / XBANK  ->  50/150/200 GHO, 200 GHO egimi, 20g gerceklesen vol
   (b) RS siralamasi  : IBD tarzi agirlikli getiri  2*r3a + r6a + r9a + r12a  -> 0-99 yuzdelik
       Minervini "trend sablonu": fiyat>50>150>200 GHO, 200 GHO 1 aydir yukseliyor,
       52h zirveye <=%25 uzak, 52h dibin >=%30 ustu, RS>=70
   (c) 3-1 / 6-1 / 12-1 ay momentum yuzdelikleri (son 1 ay haric)
   (d) sektor endeksi momentum siralamasi
   (e) 52h zirveye uzaklik, 20/50 GHO'ya uzaklik, kapanislardan ATR-benzeri gunluk oynaklik
       (ATR~ = 14g ort.|getiri| * 1,25 ; stop icin 2xATR~ onerilir) ; VIOP vadelisi olanlar isaretli
  Ayrica: USD bazli 3a/6a getiri (USDTRY ile), piyasa genisligi (50/200 GHO ustu oran), VIOP XU030 / USDTRY
  vadelilerinden baz ve ima edilen TL faizi (TLREF ile karsilastirma), aciga satis yapilabilirlik (BIST50) bayragi.
  VIOP fiyati YALNIZ resmi bultenin UZLASMA FIYATI'ndan alinir (viop_YYYYMMDD.csv; 06.11.2026 duzeltmesi,
  eski ChartData fiyati 5.11'de %23,3 gibi yanlis bir ima oran uretiyordu; dogrusu %29,3). Bulten ~20:30-20:50 TSI'de cikar.

KULLANIM  (Cuma kapanisindan sonra calistir: 18:20 TSI sonrasi; kapanis seansi 18:10'da biter)
  python3 bist_tarama.py                       # varsayilan: ./veri onbellek, ./tarama cikti
  python3 bist_tarama.py --veri ~/bist_veri --cikti ~/tarama
  python3 bist_tarama.py --yenile              # onbellegi tamamen yeniden indir
  python3 bist_tarama.py --gunici              # seans icindeki (bitmemis) bugunku bari da kullan
  Cikti: <cikti>/bist_tarama_<SONVERITARIHI>.csv, .md ve _viop.csv

NOTLAR
  * Sadece python3 + requests + pandas + numpy. Varsayilan istek basliklari, istekler arasi bekleme.
  * Seans saatinde calistirilirsa bugunku bar canli fiyattir; varsayilan olarak atilir.
  * 52h zirve/dip KAPANIS bazlidir (gun ici yuksek/dusuk yok). ATR~ da kapanistan turetilir.
  * BIST100 listesi KAP'tan (kap.org.tr/tr/Endeksler) cekilir; olmazsa asagidaki yedek liste kullanilir.
  * Bilgi amaclidir; yatirim tavsiyesi degildir.
"""
import argparse, json, os, re, sys, time
from datetime import datetime, timedelta, timezone
import numpy as np, pandas as pd, requests

URL = "https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/ChartData.aspx/IndexHistoricalAll"
KAP_URL = "https://www.kap.org.tr/tr/Endeksler"
TSI = timezone(timedelta(hours=3))

# VIOP pay vadeli sozlesmesi olan 47 dayanak (2026-11 itibariyla)
VIOP = ["AEFES","AKBNK","AKSEN","ALARK","ARCLK","ASELS","ASTOR","BIMAS","BRSAN","CIMSA","DOAS","DOHOL","EKGYO",
        "ENJSA","ENKAI","EREGL","FROTO","GARAN","GUBRF","HALKB","HEKTS","ISCTR","KCHOL","KRDMD","MGROS","ODAS",
        "OYAKC","PETKM","PGSUS","SAHOL","SASA","SISE","SOKM","TAVHL","TCELL","THYAO","TKFEN","TOASO","TRALT",
        "TRMET","TSKB","TTKOM","TUPRS","ULKER","VAKBN","VESTL","YKBNK"]
# Yedek BIST100 (1.10-31.12.2026 donemi, KAP 06.11.2026)
BIST100_YEDEK = ("BINHO AGHOL AHGAZ AKBNK AKCNS AKFYE AKSA AKSEN ALARK ALBRK ALTNY ANSGR AEFES ANHYT ARCLK ASELS ASTOR "
 "AYGAZ BTCIM BERA BIMAS BRSAN BRYAT CCOLA CVKMD CWENE CANTE CIMSA DOHOL DOAS ECZYT EGEEN EGGUB ECILC EKGYO ENJSA "
 "ENERY ENKAI EREGL EUREN FENER FROTO GWIND GLYHO GUBRF GLRMK GRSEL SAHOL HEKTS ENTRA ISDMR ISMEN KRDMD KARSN KATMR "
 "TCKRC KCAER KCHOL KORDS LMKDC MAVI MGROS MPARK OBAMS ODAS OTKAR OYAKC PAHOL PGSUS PETKM RYSAS RGYAS SASA SNGYO "
 "SOKM TABGD TAVHL TKFEN TOASO TRGYO TRMET TRENJ TUKAS TCELL TUPRS TRALT THYAO GARAN HALKB ISCTR TSKB TURSG SISE "
 "VAKBN TTKOM TTRAK ULKER VESTL YKBNK ZOREN").split()
BIST50_YEDEK = ("AKBNK AKSEN ALARK AEFES ASELS ASTOR BTCIM BIMAS BRSAN CCOLA CVKMD CWENE CANTE CIMSA DOAS ECILC EKGYO "
 "ENERY ENKAI EREGL FROTO GUBRF GLRMK SAHOL HEKTS KRDMD KCHOL MAVI MGROS OYAKC PGSUS PETKM SASA TAVHL TOASO TRMET TCELL "
 "TUPRS TRALT THYAO GARAN HALKB ISCTR TSKB TURSG SISE VAKBN TTKOM ULKER YKBNK").split()
REJIM = ["XU100", "XU030", "XBANK", "XU050", "XUTUM", "XLBNK", "X10XB", "XKURY", "XHARZ"]  # ilk 3 = ana rejim
SEKTOR = ["XBANK","XUSIN","XHOLD","XELKT","XGMYO","XKMYA","XMANA","XULAS","XTCRT","XGIDA","XILTM","XUTEK","XTAST",
          "XMADN","XSGRT","XBLSM","XUMAL","XUHIZ","XINSA","XTEKS","XKAGT","XTRZM","XSPOR","XMESY","XFINK","XAKUR","XYORT"]
FX = "USDTRY"

S = requests.Session()  # varsayilan basliklar (User-Agent degistirilmez)


def _istek(kod, bas, son, deneme=4):
    p = {"period": 1440, "from": bas.strftime("%Y%m%d000000"), "to": son.strftime("%Y%m%d235959"), "endeks": kod}
    for k in range(deneme):
        try:
            r = S.get(URL, params=p, timeout=60)
            if r.status_code == 429:
                time.sleep(10 * (k + 1)); continue
            if r.status_code == 200 and r.text.strip():
                d = r.json().get("data") or []
                if d:
                    ts = pd.to_datetime([x[0] for x in d], unit="ms") + pd.Timedelta(hours=3)  # UTC -> TSI gun
                    return pd.Series([float(x[1]) for x in d], index=ts.normalize(), name=kod)
        except (requests.RequestException, ValueError):
            pass
        time.sleep(2 * (k + 1))
        p["from"] = (bas - timedelta(days=k + 1)).strftime("%Y%m%d000000")  # bazi pencereler bos donuyor
    return pd.Series(dtype=float, name=kod)


def seri(kod, veri, bas, bugun, yenile, bekle):
    """Onbellekli gunluk kapanis serisi (veri/<KOD>.csv). Eksik kuyrugu son 15 gunden itibaren tamamlar."""
    f = os.path.join(veri, kod + ".csv")
    eski = None
    if os.path.exists(f) and not yenile:
        eski = pd.read_csv(f, index_col=0, parse_dates=True)["px"]
        if len(eski) and eski.index[0] <= pd.Timestamp(bas) + pd.Timedelta(days=10):
            yeni = _istek(kod, (eski.index[-1] - pd.Timedelta(days=15)).to_pydatetime(), bugun); time.sleep(bekle)
            s = pd.concat([eski[eski.index < (yeni.index[0] if len(yeni) else eski.index[-1] + pd.Timedelta(days=1))], yeni])
        else:
            eski = None
    if eski is None:
        s = _istek(kod, bas, bugun); time.sleep(bekle)
    s = s[~s.index.duplicated(keep="last")].sort_index()
    if len(s):
        s.rename("px").to_frame().to_csv(f)
    return s


def endeks_listeleri(veri):
    """KAP'tan XU100 ve XU050 uyeleri. XU050 = aciga satis yapilabilen paylar (SPK; 22.09.2026'dan beri yukari adim kurali)."""
    try:
        t = S.get(KAP_URL, timeout=60).text.replace('\\"', '"')
        out = {}
        for kod in ("XU100", "XU050"):
            i = t.find('"code":"%s","content":[' % kod)
            j = t.find('"explanation"', i)
            out[kod] = re.findall(r'"stockCode":"([A-Z0-9]+)"', t[i:j]) if i >= 0 else []
        if 90 <= len(out["XU100"]) <= 110 and 45 <= len(out["XU050"]) <= 55:
            json.dump(out, open(os.path.join(veri, "endeks_kap.json"), "w"))
            return out["XU100"], out["XU050"], "KAP"
    except requests.RequestException:
        pass
    return BIST100_YEDEK, BIST50_YEDEK, "yedek"


def metrikler(c, usd=None):
    """Tek seri icin son gun metrikleri. c: gunluk kapanis (pd.Series)."""
    c = c.dropna()
    n = len(c)
    if n < 60:
        return None
    r = c.pct_change()
    g = lambda k: c.iloc[-1] / c.iloc[-1 - k] - 1 if n > k else np.nan
    gs = lambda a, b: c.iloc[-1 - b] / c.iloc[-1 - a] - 1 if n > a else np.nan  # a gun once -> b gun once
    ma = {k: c.rolling(k).mean() for k in (20, 50, 150, 200)}
    son = c.iloc[-1]
    w = c.iloc[-252:]
    out = dict(
        tarih=c.index[-1].date(), kapanis=round(son, 2), n_gun=n,
        r1h=g(5), r1a=g(21), r3a=g(63), r6a=g(126), r9a=g(189), r12a=g(252),
        m3_1=gs(84, 21), m6_1=gs(147, 21), m12_1=gs(273, 21),
        gho20=ma[20].iloc[-1], gho50=ma[50].iloc[-1], gho150=ma[150].iloc[-1], gho200=ma[200].iloc[-1],
        gho200_1a_once=ma[200].iloc[-22] if n >= 222 else np.nan,
        zirve52=w.max(), dip52=w.min(),
        rv20=r.iloc[-20:].std() * np.sqrt(252),
        atr_yzd=r.abs().iloc[-14:].mean() * 1.25,  # kapanis bazli ATR% vekili
    )
    out["uzak20"] = son / out["gho20"] - 1
    out["uzak50"] = son / out["gho50"] - 1
    out["uzak200"] = son / out["gho200"] - 1 if pd.notna(out["gho200"]) else np.nan
    out["zirveye"] = son / out["zirve52"] - 1
    out["dipten"] = son / out["dip52"] - 1
    out["gho200_yukselen"] = bool(pd.notna(out["gho200_1a_once"]) and out["gho200"] > out["gho200_1a_once"])
    out["rs_ham"] = 2 * out["r3a"] + out["r6a"] + out["r9a"] + out["r12a"] if n > 252 else np.nan
    if usd is not None:
        u = (c / usd.reindex(c.index).ffill()).dropna()
        out["usd_r3a"] = u.iloc[-1] / u.iloc[-64] - 1 if len(u) > 64 else np.nan
        out["usd_r6a"] = u.iloc[-1] / u.iloc[-127] - 1 if len(u) > 127 else np.nan
    return out


BULTEN_URL = "https://www.borsaistanbul.com/data/vadeli/viop_{:%Y%m%d}.csv"


def viop_bulten(tarih, veri, geri=6, bekle=0.7):
    """Resmi Borsa Istanbul VIOP gunluk bulteni (uzlasma fiyatlari). tarih'ten geriye dogru ilk bulunan gun.
    Donus: (DataFrame, bulten_tarihi) ya da (None, None). Onbellek: <veri>/viop/viop_YYYYMMDD.csv.
    Not: bulten CSV'si ~20:30-20:50 TSI'de yayimlanir; uzlasma fiyati 18:55 sonrasi ilan edilir."""
    d = os.path.join(veri, "viop"); os.makedirs(d, exist_ok=True)
    g = pd.Timestamp(tarih).normalize()
    for _ in range(geri + 1):
        while g.weekday() >= 5: g -= pd.Timedelta(days=1)
        f = os.path.join(d, f"viop_{g:%Y%m%d}.csv")
        metin = None
        if os.path.exists(f):
            metin = open(f, encoding="utf-8", errors="replace").read()
        else:
            try:
                r = S.get(BULTEN_URL.format(g), timeout=60); time.sleep(bekle)
                if r.status_code == 200 and r.text.lstrip().startswith("TARIH;"):
                    metin = r.text; open(f, "w", encoding="utf-8").write(metin)
            except requests.RequestException:
                metin = None
        if metin and metin.lstrip().startswith("TARIH;"):
            satir = metin.splitlines()
            bas = [x.strip() for x in satir[0].split(";")]
            kayit = [x.split(";") for x in satir[2:] if x.strip()]  # 2. satir Ingilizce baslik
            df = pd.DataFrame([k[:len(bas)] + [""] * (len(bas) - len(k)) for k in kayit], columns=bas)
            for c in ("UZLASMA FIYATI", "KAPANIS FIYATI", "ISLEM HACMI", "ISLEM MIKTARI", "ACIK POZISYON"):
                df[c] = pd.to_numeric(df[c].str.replace(",", "."), errors="coerce")
            df["VADE TARIHI"] = pd.to_datetime(df["VADE TARIHI"], errors="coerce")
            df["TARIH"] = pd.to_datetime(df["TARIH"], errors="coerce")
            return df, g
        g -= pd.Timedelta(days=1)
    return None, None


def viop_fiyatlama(spot, tlref, usd_faiz, bas, veri="./veri"):
    """XU030 ve USDTRY vadelilerinden baz / ima edilen TL faizi.
    DUZELTME (06.11.2026): Eski surum vadeli fiyatini ChartData'dan aliyordu; bu seri spotla ayni ana ait degildi
    (5.11'de 14.605 -> %23,3 ima, YANLIS). Simdi yalniz resmi bulten UZLASMA FIYATI kullanilir ve spot, bultenin
    kendi tarihindeki kapanistan alinir (tarih eslesmesi). 5.11: 14.734 / 14.101 -> basit %29,3."""
    B, bt_ = viop_bulten(bas, veri)
    if B is None:
        return pd.DataFrame()
    sat = []
    for dayanak, filtre, n in (("XU030", B["SOZLESME KODU"].str.match(r"^F_XU030\d{4}$"), 2),
                               ("USDTRY", B["SOZLESME KODU"].str.match(r"^F_USDTRY\d{4}$"), 3)):
        s = spot.get(dayanak)
        if s is None or not len(s.loc[:bt_]):
            continue
        S0 = s.loc[:bt_].iloc[-1]; gs = s.loc[:bt_].index[-1]
        for _, x in B[filtre].sort_values("VADE TARIHI").head(n).iterrows():
            T = (x["VADE TARIHI"] - bt_).days
            F = x["UZLASMA FIYATI"]
            if not (T > 0 and F > 0): continue
            prim = F / S0 - 1
            r = tlref.loc[:bt_].iloc[-1] / 100 if tlref is not None and len(tlref.loc[:bt_]) else np.nan
            ima = ((1 + prim) * (1 + usd_faiz * T / 360) - 1) * 365 / T if dayanak == "USDTRY" else prim * 365 / T
            sat.append(dict(kontrat=x["SOZLESME KODU"], tarih=bt_.date(), spot_tarihi=gs.date(), vade=x["VADE TARIHI"].date(),
                            gun=T, vadeli=F, spot=round(S0, 4), prim=prim, ima_tl_faiz=ima, tlref=r,
                            teorik_fark=(F / (S0 * (1 + r * T / 365)) - 1) if dayanak == "XU030" else np.nan))
    return pd.DataFrame(sat)


def yuzdelik(x):
    return (x.rank(pct=True) * 99).round(0)


def rejim_etiketi(m):
    if m["kapanis"] > m["gho200"] and m["gho50"] > m["gho200"] and m["gho200_yukselen"]:
        return "BOGA (fiyat>200, 50>200, 200 yukselen)"
    if m["kapanis"] < m["gho200"] and m["gho50"] < m["gho200"]:
        return "AYI (fiyat<200, 50<200)"
    return "GECIS"


def md_tablo(df, kol, fmt):
    sat = ["| " + " | ".join(kol) + " |", "|" + "---|" * len(kol)]
    for _, x in df.iterrows():
        h = []
        for k in kol:
            v = x[k]
            f = fmt.get(k)
            if f == "%" and pd.notna(v): h.append(f"{100 * v:+.1f}")
            elif f == "f" and pd.notna(v): h.append(f"{v:,.2f}")
            elif f == "i" and pd.notna(v): h.append(f"{v:.0f}")
            elif isinstance(v, (bool, np.bool_)): h.append("E" if v else "-")
            else: h.append("" if pd.isna(v) else str(v))
        sat.append("| " + " | ".join(h) + " |")
    return "\n".join(sat)


def main():
    ap = argparse.ArgumentParser(description="BIST/VIOP haftalik tarama")
    ap.add_argument("--veri", default="./veri", help="onbellek klasoru (varsayilan ./veri)")
    ap.add_argument("--cikti", default="./tarama", help="cikti klasoru (varsayilan ./tarama)")
    ap.add_argument("--bas", default="2023-01-01", help="veri baslangici")
    ap.add_argument("--bekle", type=float, default=0.7, help="istekler arasi bekleme (sn)")
    ap.add_argument("--yenile", action="store_true", help="onbellegi yeniden indir")
    ap.add_argument("--gunici", action="store_true", help="bitmemis bugunku bari kullan")
    ap.add_argument("--usd_faiz", type=float, default=0.039, help="USD kisa faiz (USDTRY ima TL faizi icin)")
    a = ap.parse_args()
    os.makedirs(a.veri, exist_ok=True); os.makedirs(a.cikti, exist_ok=True)
    simdi = datetime.now(TSI)
    bugun = pd.Timestamp(simdi.date())
    seans_acik = simdi.weekday() < 5 and simdi.hour * 60 + simdi.minute < 18 * 60 + 20

    b100, b50, kaynak = endeks_listeleri(a.veri)
    hisseler = sorted(set(VIOP) | set(b100))
    kodlar = REJIM + [k for k in SEKTOR if k not in REJIM] + [FX, "TLREF"] + hisseler
    print(f"BIST100 kaynagi: {kaynak} ({len(b100)}), hisse evreni: {len(hisseler)}, toplam kod: {len(kodlar)}", flush=True)
    D, bos = {}, []
    for i, k in enumerate(kodlar, 1):
        s = seri(k, a.veri, datetime.strptime(a.bas, "%Y-%m-%d"), simdi.replace(tzinfo=None), a.yenile, a.bekle)
        if not a.gunici and seans_acik and len(s) and s.index[-1] == bugun:
            s = s.iloc[:-1]
        if len(s): D[k] = s
        else: bos.append(k)
        if i % 25 == 0: print(f"  {i}/{len(kodlar)}", flush=True)
    usd = D.get(FX)
    son_tarih = D["XU100"].index[-1]

    sat = []
    for k, s in D.items():
        if k in (FX, "TLREF"): continue
        m = metrikler(s, usd)
        if m is None: continue
        m["kod"] = k
        m["tip"] = "rejim" if k in REJIM else ("sektor" if k in SEKTOR else "hisse")
        m["viop"] = k in VIOP
        m["bist100"] = k in b100
        m["aciga_satis"] = k in b50
        m["bayat"] = s.index[-1] < son_tarih  # son islem gunu verisi yoksa (durdurma vs.)
        sat.append(m)
    T = pd.DataFrame(sat).set_index("kod")
    H = T[T.tip == "hisse"].copy()
    H["rs"] = yuzdelik(H["rs_ham"])
    for k in ("m3_1", "m6_1", "m12_1"):
        H[k + "_yzd"] = yuzdelik(H[k])
    H["mom_bilesik"] = H[["m3_1_yzd", "m6_1_yzd", "m12_1_yzd"]].mean(axis=1).round(0)
    H["t_dizilim"] = (H.kapanis > H.gho50) & (H.gho50 > H.gho150) & (H.gho150 > H.gho200)
    H["t_zirve25"] = H.zirveye >= -0.25
    H["t_dip30"] = H.dipten >= 0.30
    H["sablon"] = H.t_dizilim & H.gho200_yukselen & H.t_zirve25 & H.t_dip30 & (H.rs >= 70)
    H["sablon_puan"] = H[["t_dizilim", "gho200_yukselen", "t_zirve25", "t_dip30"]].sum(axis=1) + (H.rs >= 70)
    H["stop_2atr"] = (H.kapanis * (1 - 2 * H.atr_yzd)).round(2)
    X = T[T.tip != "hisse"].copy()
    sk = X[X.index.isin(SEKTOR)].copy()
    sk["sira_puan"] = (yuzdelik(sk.r1a) + yuzdelik(sk.r3a) + yuzdelik(sk.r6a) + yuzdelik(sk.uzak50)) / 4
    X.loc[sk.index, "sira_puan"] = sk["sira_puan"].round(0)
    X["rejim"] = [rejim_etiketi(X.loc[k]) for k in X.index]
    gen = dict(ust50=(H.kapanis > H.gho50).mean(), ust200=(H.kapanis > H.gho200).mean(),
               zirve10=(H.zirveye >= -0.10).mean(), sablon=H.sablon.mean())
    V = viop_fiyatlama({"XU030": D["XU030"], "USDTRY": usd}, D.get("TLREF"), a.usd_faiz, son_tarih, a.veri)
    TUM = pd.concat([X, H]).sort_values(["tip", "rs"], ascending=[True, False])
    tag = son_tarih.strftime("%Y%m%d")
    cs = os.path.join(a.cikti, f"bist_tarama_{tag}.csv")
    TUM.round(4).to_csv(cs, encoding="utf-8-sig")

    P = {"r1h": "%", "r1a": "%", "r3a": "%", "r6a": "%", "r12a": "%", "uzak20": "%", "uzak50": "%", "uzak200": "%",
         "zirveye": "%", "dipten": "%", "rv20": "%", "atr_yzd": "%", "usd_r3a": "%", "usd_r6a": "%",
         "kapanis": "f", "gho50": "f", "gho150": "f", "gho200": "f", "stop_2atr": "f",
         "rs": "i", "mom_bilesik": "i", "m3_1_yzd": "i", "m6_1_yzd": "i", "m12_1_yzd": "i", "sablon_puan": "i", "sira_puan": "i"}
    md = [f"# BIST/VIOP tarama — son veri {son_tarih.date()} (uretim {simdi:%Y-%m-%d %H:%M} TSI)",
          f"Evren: VIOP 47 + BIST100 ({kaynak}) = {len(H)} hisse; bos/bulunamayan: {', '.join(bos) or '-'}; "
          f"son gunu eksik (bayat): {', '.join(T.index[T.bayat]) or '-'}.",
          "Yuzdeler %; RS ve momentum 0-99 yuzdelik (evren ici). ATR~ = kapanis bazli 14g ort.|getiri|x1,25. "
          "52h zirve/dip kapanis bazli. Bilgi amaclidir.", "",
          "## (a) Rejim", md_tablo(X.loc[[k for k in REJIM if k in X.index]].reset_index(),
          ["kod", "kapanis", "gho50", "gho150", "gho200", "uzak50", "uzak200", "gho200_yukselen", "rv20", "r1h", "r1a", "r3a",
           "r6a", "r12a", "usd_r3a", "zirveye", "rejim"], P),
          f"\nGenislik (hisse evreni): 50 GHO ustu %{100*gen['ust50']:.0f} | 200 GHO ustu %{100*gen['ust200']:.0f} | "
          f"52h zirveye <=%10 %{100*gen['zirve10']:.0f} | trend sablonu %{100*gen['sablon']:.0f}", "",
          "### VIOP fiyatlama (resmi bulten uzlasma fiyati; baz, ima edilen TL faizi; XU030 temettu ihmal, USD faizi varsayim)",
          md_tablo(V, ["kontrat", "tarih", "spot_tarihi", "vade", "gun", "vadeli", "spot", "prim", "ima_tl_faiz", "tlref", "teorik_fark"],
                   {"prim": "%", "ima_tl_faiz": "%", "tlref": "%", "teorik_fark": "%", "vadeli": "f"}) if len(V) else "_VIOP verisi alinamadi._",
          ""]
    nsab = int(H.sablon.sum())
    md += [f"## (b) Trend sablonu gecenler ({nsab} hisse) — RS sirali",
           md_tablo(H[H.sablon].sort_values("rs", ascending=False).reset_index(),
                    ["kod", "viop", "kapanis", "rs", "r3a", "r6a", "r12a", "usd_r6a", "zirveye", "dipten", "uzak20", "uzak50",
                     "atr_yzd", "stop_2atr"], P) if nsab else "_Sablonu tam gecen hisse yok._", "",
           "### RS ilk 30 (sablon puani 0-5 ile)",
           md_tablo(H.sort_values("rs", ascending=False).head(30).reset_index(),
                    ["kod", "viop", "kapanis", "rs", "sablon_puan", "sablon", "r1a", "r3a", "r6a", "r12a", "zirveye", "uzak50",
                     "gho200_yukselen", "atr_yzd", "stop_2atr"], P), "",
           "## (c) Momentum (3-1 / 6-1 / 12-1 ay, yuzdelik) — bilesik ilk 25",
           md_tablo(H.sort_values("mom_bilesik", ascending=False).head(25).reset_index(),
                    ["kod", "viop", "mom_bilesik", "m3_1_yzd", "m6_1_yzd", "m12_1_yzd", "r1a", "uzak50", "zirveye"], P), "",
           "### Momentum son 15 (zayiflar; VIOP'ta kisa aday havuzu)",
           md_tablo(H.sort_values("mom_bilesik").head(15).reset_index(),
                    ["kod", "viop", "aciga_satis", "mom_bilesik", "r1a", "r3a", "r6a", "uzak50", "uzak200", "zirveye"], P), "",
           "## (d) Sektor endeksleri (sira puani = r1a, r3a, r6a, 50GHO uzakligi yuzdelik ortalamasi)",
           md_tablo(X[X.index.isin(SEKTOR)].sort_values("sira_puan", ascending=False).reset_index(),
                    ["kod", "sira_puan", "kapanis", "r1h", "r1a", "r3a", "r6a", "r12a", "usd_r6a", "uzak50", "uzak200",
                     "zirveye", "rejim"], P), "",
           "## (e) VIOP dayanaklari — stop boyutlama ve konum",
           md_tablo(H[H.viop].sort_values("rs", ascending=False).reset_index(),
                    ["kod", "kapanis", "rs", "sablon_puan", "r1a", "r3a", "uzak20", "uzak50", "uzak200", "zirveye", "rv20",
                     "atr_yzd", "stop_2atr"], P), ""]
    if len(V): V.round(4).to_csv(os.path.join(a.cikti, f"bist_tarama_{tag}_viop.csv"), index=False)
    mf = os.path.join(a.cikti, f"bist_tarama_{tag}.md")
    open(mf, "w", encoding="utf-8").write("\n".join(md))
    print("yazildi:", cs, mf)


if __name__ == "__main__":
    main()
