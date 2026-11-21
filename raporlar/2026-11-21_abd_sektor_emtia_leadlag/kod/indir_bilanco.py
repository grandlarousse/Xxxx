"""Nasdaq bilanço takvimini gün gün indirir (2008'den bugüne). Çıktı: veri/bilanco_takvimi.csv

Sütunlar: tarih, sembol, eps, eps_beklenti, surpriz_yuzde, tahmin_sayisi, zaman, ceyrek.
Not: geçmiş tarihlerde 'zaman' alanı çoğunlukla 'time-not-supplied' gelir (açılış öncesi mi kapanış sonrası mı belli
değil). Tepki günü fiyat ve hacimden çıkarılmalı ya da SEC EDGAR 8-K kabul saatiyle (UTC) eşlenmelidir.
"""
import csv, json, os, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak as o

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) research-client", "Accept": "application/json"}

def gun(d):
    url = f"https://api.nasdaq.com/api/calendar/earnings?date={d}"
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                rows = ((json.loads(r.read()).get("data") or {}).get("rows")) or []
            return d, rows, None
        except Exception as e:  # noqa: BLE001
            hata = f"{type(e).__name__}: {str(e)[:80]}"
            time.sleep(1.5 * (i + 1))
    return d, [], hata

def main():
    gunler = [t.strftime("%Y-%m-%d") for t in o.oku("SPY").index if t >= pd.Timestamp("2008-01-01")]
    evren = set(o.abd_semboller("EQUITY"))
    yol = os.path.join(o.VERI, "bilanco_takvimi.csv")
    n_hata = 0
    with open(yol, "w", newline="") as f, ThreadPoolExecutor(max_workers=6) as ex:
        w = csv.writer(f)
        w.writerow(["tarih", "sembol", "eps", "eps_beklenti", "surpriz_yuzde", "tahmin_sayisi", "zaman", "ceyrek", "evrende"])
        for k, (d, rows, hata) in enumerate(ex.map(gun, gunler), 1):
            if hata:
                n_hata += 1
            for r in rows:
                s = (r.get("symbol") or "").replace(".", "-")
                w.writerow([d, s, r.get("eps"), r.get("epsForecast"), r.get("surprise"), r.get("noOfEsts"), r.get("time"), r.get("fiscalQuarterEnding"), int(s in evren)])
            if k % 500 == 0:
                print(f"{k}/{len(gunler)} gun, {n_hata} hata", flush=True)
    d = pd.read_csv(yol)
    print("BITTI", len(d), "satir;", int(d.evrende.sum()), "evren ici;", d[d.evrende == 1].sembol.nunique(), "sembol;", n_hata, "hatali gun")
    print(d[d.evrende == 1].groupby(d.tarih.str[:4]).size().to_string())

if __name__ == "__main__":
    main()
