"""Günlük sinyal tablosu: rapordaki kuralların BUGÜNKÜ durumu.

Kullanım (ABD kapanışından 20 dakika önce, 15:40 ET; Türkiye saatiyle kışın 23:40, yazın 22:40):
    python3 kod/gunluk_sinyal.py            # veriyi Yahoo'dan taze çeker (yaklaşık 40 sembol), tabloyu basar
    python3 kod/gunluk_sinyal.py --tarih 2026-11-20   # geçmiş bir günün kapanış sinyalleri (indirilmiş veriden)

Seans açıkken çalıştırılırsa Yahoo'nun günlük çubuğu o ana kadarki en yüksek/en düşük/son fiyatı taşır; tablo
"geçici" sinyali gösterir. Kapanışa 20 dakika kala hesaplanan sinyal kapanışta değişebilir: IBS 0,15-0,25 arasındaysa
ya da VIX eşiğe 1 puandan yakınsa "SINIRDA" diye işaretlenir (temkin tercihi; geçmişte sınır bandı da çalıştı).
İşlem araçları QQQ, IWM, SMH'dir; diğer ETF'ler yalnız bilgi içindir (aynı bahsin başka görünümleri).

Kurallar ve sınıfları RAPOR.md bölüm 3'te. Bu betik yatırım tavsiyesi vermez; yalnız kuralın o günkü durumunu hesaplar.
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "Mozilla/5.0 (X11; Linux x86_64) research-client"

ISLEM = ["QQQ", "IWM", "SMH"]          # 1. kuralın uygulanacağı araçlar (RAPOR.md bölüm 3)
BILGI = ["SPY", "XLK", "SOXX", "IJR", "XBI", "IBB", "KRE", "XRT", "EEM"]   # yalnız bilgi: aynı bahsin başka görünümleri
PANIK_SEPETI = ISLEM + BILGI
DIGER = ["^VIX", "VLO", "MU", "WDC", "BG", "ADM", "RB=F", "HO=F", "CL=F", "ZL=F"]


def cek(sembol, gun=900):
    q = urllib.parse.quote(sembol, safe="")
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{q}?range={max(gun // 250 + 1, 2)}y&interval=1d&includeAdjustedClose=true"
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30) as r:
                res = json.loads(r.read())["chart"]["result"][0]
            break
        except Exception:  # noqa: BLE001
            time.sleep(1.5 * (i + 1))
    else:
        raise RuntimeError(f"{sembol} indirilemedi")
    tz = ZoneInfo(res["meta"].get("exchangeTimezoneName") or "UTC")
    q0 = res["indicators"]["quote"][0]
    adj = (res["indicators"].get("adjclose") or [{}])[0].get("adjclose") or q0["close"]
    d = pd.DataFrame({"open": q0["open"], "high": q0["high"], "low": q0["low"], "close": q0["close"], "adjclose": adj},
                     index=[datetime.fromtimestamp(t, tz=tz).strftime("%Y-%m-%d") for t in res["timestamp"]])
    d = d[d["close"].notna()]
    d = d[~d.index.duplicated(keep="last")]
    d.index = pd.to_datetime(d.index)
    return d


def yerel(sembol):
    ad = sembol.replace("^", "_idx_").replace("=", "_eq_")
    return pd.read_csv(os.path.join(KOK, "veri", "ham", ad + ".csv"), parse_dates=["date"]).set_index("date")


def z_gecmis(x, pencere=60, min_n=40):
    return x / x.rolling(pencere, min_periods=min_n).std().shift(1)


def kayan_beta(y, x, pencere=250, min_n=120):
    return (y.rolling(pencere, min_periods=min_n).cov(x) / x.rolling(pencere, min_periods=min_n).var()).shift(1)


def main():
    tarih = None
    if "--tarih" in sys.argv:
        tarih = pd.Timestamp(sys.argv[sys.argv.index("--tarih") + 1])
    oku = yerel if tarih is not None else cek
    v = {}
    for s in PANIK_SEPETI + DIGER:
        try:
            v[s] = oku(s)
        except Exception as e:  # noqa: BLE001
            print(f"UYARI: {s} okunamadı ({str(e)[:60]})")
    if tarih is not None:
        v = {s: d[d.index <= tarih] for s, d in v.items()}
    gun = v["SPY"].index[-1]
    simdi = datetime.now(timezone.utc).astimezone(ZoneInfo("America/New_York"))
    print(f"\nVeri günü: {gun.date()}   (şu an New York saati {simdi:%Y-%m-%d %H:%M}; seans açıksa değerler GEÇİCİDİR)\n")

    vix = float(v["^VIX"]["close"].iloc[-1])
    vix_dun = float(v["^VIX"]["close"].iloc[-2])
    rejim = "PANİK (VIX > 25): 1. kural devrede" if vix > 25 else ("GERGİN (20-25): 1. ve 3. kural kapalı" if vix > 20 else "SAKİN (VIX <= 20): 1. kural kapalı, 3. kural devrede")
    print(f"VIX {vix:.1f} (dünkü kapanış {vix_dun:.1f})   |  rejim: {rejim}")
    vix_sinir = abs(vix - 25) < 1
    if vix_sinir:
        print("  UYARI: VIX eşiğe 1 puandan yakın (SINIRDA). Dünkü kapanış > 25 ise kural yine geçerli sayılabilir.")

    # 1) Panik günü dönüşü: VIX > 25 ve IBS < 0,2 -> kapanışta AL, ertesi kapanışta sat (1 gün)
    sat = []
    for s in PANIK_SEPETI:
        d = v[s].iloc[-1]
        rng = d["high"] - d["low"]
        ibs = (d["close"] - d["low"]) / rng if rng > 0 else np.nan
        gunluk = v[s]["adjclose"].pct_change().iloc[-1] * 100
        kural = vix > 25 and ibs < 0.2
        sinirda = vix_sinir or (0.15 <= ibs < 0.25)
        if kural and not sinirda:
            durum = "AL" if s in ISLEM else "sinyal var (bilgi)"
        elif kural:
            durum = "SINIRDA: kural tutuyor (temkinliysen açma)"
        elif vix > 24 and ibs < 0.25:
            durum = "yok (eşiğe yakın)"
        else:
            durum = "—"
        sat.append((s, "işlem" if s in ISLEM else "bilgi", round(float(d["close"]), 2), round(float(gunluk), 2), round(float(ibs), 2), durum))
    t1 = pd.DataFrame(sat, columns=["ETF", "tür", "son", "gün %", "IBS", "1. kural"])
    print("\n1) PANİK GÜNÜ DÖNÜŞÜ  [VIX > 25 ve IBS < 0,2 -> kapanışta AL, ERTESİ KAPANIŞTA SAT (1 gün)]")
    print(t1.to_string(index=False))
    n_al = int((t1["1. kural"] == "AL").sum())
    print(f"   İşlem araçlarında açık sinyal: {n_al}. Birden çok ETF sinyal verse de TEK bahistir: toplam pozisyon sermayenin %15-20'sini geçmesin.")
    print("   Dün de pozisyon açtıysan bugün satma ve ekleme yapma; sinyal bittiği günün kapanışında sat. Kaldıraçlı ETF kullanma.")

    # 2) Öncülük kuralları (küçük boy)
    spy = np.log(v["SPY"]["adjclose"]).diff()

    def etiket(z, kosul=True):
        if not kosul:
            return "— (kural kapalı)"
        if z >= 1.1:
            return "AL"
        if z >= 0.9:
            return "SINIRDA"
        return "—"

    def artik(x):
        """(bugünkü artık, beta, z=1 eşiği, z). Artık = öncünün hareketi - beta x SPY'ın hareketi."""
        bt = kayan_beta(x, spy)
        res = x - bt * spy
        sd = res.rolling(60, min_periods=40).std().shift(1)
        return float(res.iloc[-1]), float(bt.iloc[-1]), float(sd.iloc[-1]), float(res.iloc[-1] / sd.iloc[-1])

    spy_y = float(spy.iloc[-1]) * 100
    print("\n2) ÖNCÜLÜK KURALLARI  [öncünün SPY'dan arındırılmış hareketi eşiği geçerse hedefi AL; küçük boy]")
    print(f"   Bugün SPY {spy_y:+.2f}%")
    try:
        x = np.log(v["MU"]["adjclose"]).diff().reindex(spy.index).fillna(0.0)
        res, bt, sd, z = artik(x)
        print(f"   2. kural  MU -> WDC (3 gün tut)")
        print(f"             MU {x.iloc[-1] * 100:+.2f}%  -  {bt:.1f} x SPY  =  {res * 100:+.2f}   (eşik +{sd * 100:.2f})   ->  {etiket(z)}")
        if z >= 0.9:
            # Kontrol göstergeleri (kod/mu_wdc_suzgec.py): MU gerçekten yükselmiş olmalı; SPY'ın düştüğü gün en güçlü hâl
            if x.iloc[-1] <= 0:
                print("             KONTROL: MU bugün düştü (yalnız piyasadan az düştü). Bu tür sinyal geçmişte çalışmadı -> ALMA")
            elif spy_y < 0:
                print("             KONTROL: SPY düştü, MU yükseldi -> GÜÇLÜ hâl (geçmişte ~+%1,2 / 3 gün, isabet %66)")
            else:
                print("             KONTROL: SPY de yükseldi -> ZAYIF hâl (geçmişte ~+%0,2 / 3 gün; tutarsız). Boyu yarıya indir ya da geç")
            print("             KONTROL: MU bugün ya da dün bilanço açıkladıysa ALMA (geçmişte bu günler zarar ettirdi)")
    except Exception as e:  # noqa: BLE001
        print("   MU hesaplanamadı:", str(e)[:80])
    try:
        lv = pd.concat({k: v[k]["close"] for k in ("RB=F", "HO=F", "CL=F")}, axis=1, sort=True).dropna()
        crack = (2 * lv["RB=F"] * 42 + lv["HO=F"] * 42 - 3 * lv["CL=F"]) / 3
        dcr = crack.diff().reindex(spy.index).fillna(0.0)
        res, bt, sd, z = artik(dcr)
        print(f"   3. kural  rafineri marjı -> VLO (2 gün tut; yalnız VIX <= 20 iken)")
        print(f"             marj {crack.iloc[-1]:.1f} $/varil, bugünkü değişim {dcr.iloc[-1]:+.2f} $, SPY düzeltmesiyle {res:+.2f} $   (eşik +{sd:.2f} $)   ->  {etiket(z, vix <= 20)}")
    except Exception as e:  # noqa: BLE001
        print("   rafineri marjı hesaplanamadı:", str(e)[:80])
    try:
        x = np.log(v["ZL=F"]["adjclose"]).diff().reindex(spy.index).fillna(0.0)
        res, bt, sd, z = artik(x)
        print(f"   izleme    soya yağı (ZL=F) -> BG, ADM (1 gün)")
        print(f"             ZL=F {x.iloc[-1] * 100:+.2f}%, SPY düzeltmesiyle {res * 100:+.2f}   (eşik +{sd * 100:.2f})   ->  {'İZLE: kâğıt üstünde kaydet (para koyma)' if z >= 1 else '—'}")
    except Exception as e:  # noqa: BLE001
        print("   soya yağı hesaplanamadı:", str(e)[:80])

    print("\nHatırlatma: emir kapanış müzayedesine (MOC/LOC) girer. Betiği 15:40 ET'de çalıştır, emri en geç 15:45 ET'de gir")
    print("(Türkiye saatiyle kışın 23:40 / 23:45, yazın 22:40 / 22:45). Kapanışı kaçırdıysan ertesi AÇILIŞTA girilebilir; ertesi kapanışa kaldıysan girme.")
    print("Kurallar geçmiş veriye dayanır, küçük ve belirsiz bir üstünlük verir; yatırım tavsiyesi değildir.\n")


if __name__ == "__main__":
    main()
