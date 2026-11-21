"""Yahoo chart API'den günlük OHLCV indirir (bir kez). Çıktı: veri/ham/<sembol>.csv + veri/meta.csv

Kullanım:  python3 indir.py [veri_dizini] [--yalniz-eksik]
- Tarih: borsanın yerel takvim günü (zaman damgası borsanın saat dilimine çevrilir; yaz saati dahil). Sütunlar: open, high, low, close (bölünmeye göre düzeltilmiş),
  adjclose (temettüye göre de düzeltilmiş), volume, dividend, split.
- Hata veren semboller veri/indirme_hatalari.txt dosyasına yazılır; betik durmaz.
"""
import csv
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from evren import tum_semboller, grup_haritasi  # noqa: E402

BAS = 946684800  # 2000-01-01
UA = "Mozilla/5.0 (X11; Linux x86_64) research-client"


def dosya_adi(sembol):
    return sembol.replace("^", "_idx_").replace("=", "_eq_").replace("/", "_")


def cek(sembol, bitis, deneme=4):
    q = urllib.parse.quote(sembol, safe="")
    son_hata = None
    for i in range(deneme):
        host = "query1" if i % 2 == 0 else "query2"
        url = (
            f"https://{host}.finance.yahoo.com/v8/finance/chart/{q}"
            f"?period1={BAS}&period2={bitis}&interval=1d&events=div%2Csplits&includeAdjustedClose=true"
        )
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=40) as r:
                d = json.loads(r.read())
            res = d["chart"]["result"]
            if not res:
                raise ValueError(str(d["chart"].get("error"))[:120])
            return res[0]
        except Exception as e:  # noqa: BLE001
            son_hata = f"{type(e).__name__}: {str(e)[:120]}"
            if "404" in son_hata or "Not Found" in son_hata:
                break
            time.sleep(1.5 * (i + 1))
    raise RuntimeError(son_hata)


def isle(sembol, veri_dizini, bitis):
    r = cek(sembol, bitis)
    meta = r["meta"]
    ts = r.get("timestamp") or []
    if not ts:
        raise RuntimeError("bos seri")
    q = r["indicators"]["quote"][0]
    adj = (r["indicators"].get("adjclose") or [{}])[0].get("adjclose") or q["close"]
    off = meta.get("gmtoffset", 0)
    # DİKKAT: meta.gmtoffset yalnız BUGÜNKÜ farktır. Gece yarısı damgalı seriler (vadeli, kur) yaz saatinde
    # sabit farkla bir gün geriye kayar. Bu yüzden tarih, borsanın saat dilimiyle (yaz saati dahil) hesaplanır.
    try:
        tz = ZoneInfo(meta.get("exchangeTimezoneName") or "UTC")
    except Exception:  # noqa: BLE001
        tz = timezone.utc
    ev = r.get("events", {})
    div = {int(k): v.get("amount") for k, v in ev.get("dividends", {}).items()}
    spl = {int(k): f"{v.get('numerator')}:{v.get('denominator')}" for k, v in ev.get("splits", {}).items()}
    satirlar, gorulen = [], set()
    for i, t in enumerate(ts):
        c = q["close"][i]
        if c is None:
            continue
        gun = datetime.fromtimestamp(t, tz=tz).strftime("%Y-%m-%d")
        if gun in gorulen:  # aynı güne ikinci (canlı) satır
            satirlar.pop()
        gorulen.add(gun)
        satirlar.append([gun, q["open"][i], q["high"][i], q["low"][i], c, adj[i], q["volume"][i], div.get(t, ""), spl.get(t, "")])
    yol = os.path.join(veri_dizini, "ham", dosya_adi(sembol) + ".csv")
    with open(yol, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "open", "high", "low", "close", "adjclose", "volume", "dividend", "split"])
        w.writerows(satirlar)
    return {
        "sembol": sembol,
        "dosya": dosya_adi(sembol) + ".csv",
        "tur": meta.get("instrumentType"),
        "borsa": meta.get("exchangeName"),
        "borsa_tam": meta.get("fullExchangeName"),
        "saat_dilimi": meta.get("exchangeTimezoneName"),
        "gmtoffset": off,
        "para": meta.get("currency"),
        "ad": meta.get("longName") or meta.get("shortName"),
        "ilk": satirlar[0][0],
        "son": satirlar[-1][0],
        "n": len(satirlar),
    }


def main():
    veri_dizini = next((a for a in sys.argv[1:] if not a.startswith("--")), os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "veri"))
    yalniz_eksik = "--yalniz-eksik" in sys.argv
    os.makedirs(os.path.join(veri_dizini, "ham"), exist_ok=True)
    bitis = int(time.time()) + 86400
    semboller = tum_semboller()
    if yalniz_eksik:
        semboller = [s for s in semboller if not os.path.exists(os.path.join(veri_dizini, "ham", dosya_adi(s) + ".csv"))]
    gruplar = grup_haritasi()
    metalar, hatalar = [], []

    def is_(s):
        try:
            m = isle(s, veri_dizini, bitis)
            m["gruplar"] = ";".join(gruplar.get(s, []))
            return m, None
        except Exception as e:  # noqa: BLE001
            return None, (s, str(e))

    with ThreadPoolExecutor(max_workers=6) as ex:
        for k, (m, h) in enumerate(ex.map(is_, semboller), 1):
            if m:
                metalar.append(m)
            else:
                hatalar.append(h)
            if k % 50 == 0:
                print(f"{k}/{len(semboller)} tamam, {len(hatalar)} hata", flush=True)

    meta_yol = os.path.join(veri_dizini, "meta.csv")
    eski = []
    if yalniz_eksik and os.path.exists(meta_yol):
        with open(meta_yol) as f:
            eski = list(csv.DictReader(f))
    alanlar = ["sembol", "dosya", "tur", "borsa", "borsa_tam", "saat_dilimi", "gmtoffset", "para", "ad", "ilk", "son", "n", "gruplar"]
    with open(meta_yol, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=alanlar)
        w.writeheader()
        for m in sorted(eski + metalar, key=lambda x: x["sembol"]):
            w.writerow({a: m.get(a, "") for a in alanlar})
    with open(os.path.join(veri_dizini, "indirme_hatalari.txt"), "w") as f:
        for s, e in hatalar:
            f.write(f"{s}\t{e}\n")
    print(f"BITTI: {len(metalar)} indirildi, {len(hatalar)} hata -> {veri_dizini}", flush=True)


if __name__ == "__main__":
    main()
