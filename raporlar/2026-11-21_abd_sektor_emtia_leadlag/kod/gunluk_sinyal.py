"""Günlük sinyal tablosu: rapordaki kuralların BUGÜNKÜ durumu.

Kullanım (ABD kapanışından ~15 dakika önce, 15:40-15:45 ET; Türkiye saatiyle kışın 23:40, yazın 22:40):
    python3 kod/gunluk_sinyal.py            # veriyi Yahoo'dan taze çeker (yaklaşık 40 sembol), tabloyu basar
    python3 kod/gunluk_sinyal.py --tarih 2026-11-20   # geçmiş bir günün kapanış sinyalleri (indirilmiş veriden)

Seans açıkken çalıştırılırsa Yahoo'nun günlük çubuğu o ana kadarki en yüksek/en düşük/son fiyatı taşır; tablo
"geçici" sinyali gösterir. Kapanışa 10 dakika kala hesaplanan sinyal kapanışta değişebilir: IBS 0,15-0,25 arasındaysa
ya da VIX eşiğe 1 puandan yakınsa "SINIRDA" diye işaretlenir; bu durumda işlem açılmaz.

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

PANIK_SEPETI = ["QQQ", "XLK", "SMH", "SOXX", "IWM", "IJR", "XBI", "IBB", "KRE", "XRT", "EEM", "SPY"]
KALDIRACLI = {"QQQ": "TQQQ (3x)", "XLK": "TECL (3x)", "SMH": "SOXL (3x)", "SOXX": "SOXL (3x)", "IWM": "TNA (3x)", "XBI": "LABU (3x)",
              "KRE": "DPST (3x)", "SPY": "UPRO (3x)", "IBB": "LABU (3x, XBI endeksi)"}
DIGER = ["^VIX", "^VIX3M", "VLO", "PBF", "MU", "WDC", "BG", "ADM", "RB=F", "HO=F", "CL=F", "ZL=F"]


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
    vix3m = float(v["^VIX3M"]["close"].iloc[-1]) if "^VIX3M" in v else np.nan
    print(f"VIX {vix:.1f}   VIX/VIX3M {vix / vix3m:.2f}   |  rejim: {'PANİK (VIX > 25): 1. kural devrede' if vix > 25 else ('GERGİN (20-25): yalnız izleme' if vix > 20 else 'SAKİN (VIX <= 20): 1. kural kapalı')}")
    if abs(vix - 25) < 1:
        print("  UYARI: VIX eşiğe 1 puandan yakın: SINIRDA")

    # 1) Panik dönüşü: VIX > 25 ve IBS < 0,2 -> kapanışta AL, 1-2 gün tut
    sat = []
    for s in PANIK_SEPETI:
        d = v[s].iloc[-1]
        rng = d["high"] - d["low"]
        ibs = (d["close"] - d["low"]) / rng if rng > 0 else np.nan
        gunluk = v[s]["adjclose"].pct_change().iloc[-1] * 100
        durum = "—"
        if vix > 25 and ibs < 0.2:
            durum = "AL" if ibs < 0.15 else "AL (SINIRDA: IBS 0,15-0,20)"
        elif vix > 25 and ibs < 0.25:
            durum = "yok (SINIRDA: IBS 0,20-0,25)"
        sat.append((s, round(float(d["close"]), 2), round(float(gunluk), 2), round(float(ibs), 2), durum, KALDIRACLI.get(s, "")))
    t1 = pd.DataFrame(sat, columns=["ETF", "son", "gün %", "IBS", "1. kural (panik dönüşü)", "kaldıraçlı eşi"])
    print("\n1) PANİK DÖNÜŞÜ  [VIX > 25 ve IBS < 0,2 -> kapanışta AL, 1-2 gün]")
    print(t1.to_string(index=False))
    n_al = int(t1["1. kural (panik dönüşü)"].str.startswith("AL").sum())
    print(f"   Açık sinyal sayısı: {n_al}. Hepsi aynı bahistir (piyasa dönüşü); toplam riski tek pozisyon gibi boyutla.")

    # 2) Öncülük adayları (KOŞULLU / yeni rejim adayı; küçük boyut ya da yalnız izleme)
    spy = np.log(v["SPY"]["adjclose"]).diff()
    print("\n2) ÖNCÜLÜK ADAYLARI  [z >= +1 -> AL]")
    try:
        lv = pd.concat({k: v[k]["close"] for k in ("RB=F", "HO=F", "CL=F")}, axis=1, sort=True).dropna()
        crack = (2 * lv["RB=F"] * 42 + lv["HO=F"] * 42 - 3 * lv["CL=F"]) / 3
        dcr = crack.diff().reindex(spy.index).fillna(0.0)
        z_ham = z_gecmis(dcr).iloc[-1]
        z_art = z_gecmis(dcr - kayan_beta(dcr, spy) * spy).iloc[-1]
        print(f"   Rafineri marjı (3-2-1 crack) {crack.iloc[-1]:.1f} $/varil, günlük değişim {crack.diff().iloc[-1]:+.2f} $;"
              f" z ham {z_ham:+.2f}, z arındırılmış {z_art:+.2f}  ->  VLO (2 gün): {'AL' if z_art >= 1 else '—'};  PBF (3 gün): {'AL' if z_ham >= 1 else '—'}"
              f"{'   [VIX > 20: geçmişte bu rejimde çalışmadı]' if vix > 20 else ''}")
    except Exception as e:  # noqa: BLE001
        print("   crack hesaplanamadı:", str(e)[:80])
    for oncu, hedefler, h in (("MU", ["WDC"], 3), ("ZL=F", ["BG", "ADM"], 1)):
        try:
            x = np.log(v[oncu]["adjclose"]).diff().reindex(spy.index).fillna(0.0)
            z = z_gecmis(x - kayan_beta(x, spy) * spy).iloc[-1]
            print(f"   {oncu} piyasadan arındırılmış z {z:+.2f}  ->  {', '.join(hedefler)} ({h} gün): {'AL' if z >= 1 else '—'}")
        except Exception as e:  # noqa: BLE001
            print(f"   {oncu} hesaplanamadı:", str(e)[:80])

    print("\nHatırlatma: emir kapanış müzayedesine (MOC/LOC) girer; NYSE kesimi 15:50 ET, Nasdaq 15:55 ET, NYSE Arca 15:59 ET.")
    print("Kurallar geçmiş veriye dayanır, küçük ve belirsiz bir üstünlük verir; yatırım tavsiyesi değildir.\n")


if __name__ == "__main__":
    main()
