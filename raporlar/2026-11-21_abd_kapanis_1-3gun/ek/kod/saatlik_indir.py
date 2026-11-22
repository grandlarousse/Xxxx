"""Yahoo 60m (range=730d) ham JSON indirir. Kullanim: python3 -I saatlik_indir.py <ham60_dizin>
Evren: evren.csv kapanis_sinifi==ABD16, tur ETF/hisse, adv60_usd >= 50e6."""
import sys, os, json, time, random, urllib.parse, requests
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
KOD = os.path.dirname(os.path.abspath(__file__)); VERI = os.path.join(os.path.dirname(KOD), "veri")
ham = sys.argv[1]; os.makedirs(ham, exist_ok=True)
ev = pd.read_csv(os.path.join(VERI, "evren.csv"), dtype={"kod": str})
kodlar = ev[(ev.kapanis_sinifi == "ABD16") & ev.tur.isin(["ETF", "hisse"]) & (ev.adv60_usd >= 50e6)].kod.tolist()
H = {"User-Agent": "Mozilla/5.0"}
def yol(k): return os.path.join(ham, urllib.parse.quote(k, safe="") + ".json")
def cek(k):
    if os.path.exists(yol(k)): return k, "var"
    last = None
    for i in range(4):
        host = "query1" if i % 2 == 0 else "query2"
        try:
            ek = "range=730d" if i < 2 else f"period1={int(time.time()) - 729 * 86400}&period2={int(time.time())}"   # genc kodlarda range=730d -> HTTP 422
            r = requests.get(f"https://{host}.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(k, safe='')}?interval=60m&{ek}", headers=H, timeout=30)
            if r.status_code == 200 and r.json()["chart"]["result"] and r.json()["chart"]["result"][0].get("timestamp"):
                tmp = yol(k) + ".tmp"; open(tmp, "w").write(r.text); os.replace(tmp, yol(k)); return k, "ok"
            last = f"HTTP {r.status_code}"
        except Exception as e:
            last = repr(e)[:100]
        time.sleep(2 + 2 * i)
    return k, last
with ThreadPoolExecutor(3) as ex:
    sonuc = dict(ex.map(lambda k: (time.sleep(random.uniform(0.2, 0.6)), cek(k))[1], kodlar))
bas = {k: v for k, v in sonuc.items() if v not in ("ok", "var")}
json.dump(bas, open(os.path.join(ham, "_basarisiz.json"), "w"), indent=1)
print("toplam", len(kodlar), "basarisiz", bas)
