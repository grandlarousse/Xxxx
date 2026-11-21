"""Asama 1: Yahoo chart API ham JSON indirir (ham dizinine). Kullanim: python3 -I veri_indir.py <ham_dizin>"""
import sys, os, json, time, urllib.parse, requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from evren_tanim import KODLAR
ham = sys.argv[1]; os.makedirs(ham, exist_ok=True)
now = int(time.time())
H = {"User-Agent": "Mozilla/5.0"}
def yol(k): return os.path.join(ham, urllib.parse.quote(k, safe="") + ".json")
fail = {}
def cek(k):
    q = urllib.parse.quote(k, safe="")
    last = None
    for i in range(3):
        host = "query1" if i == 0 else "query2"
        try:
            r = requests.get(f"https://{host}.finance.yahoo.com/v8/finance/chart/{q}?period1=1104537600&period2={now}&interval=1d&events=div%2Csplit", headers=H, timeout=30)
            if r.status_code == 200:
                j = r.json()
                if j["chart"]["result"]:
                    return j
                last = str(j["chart"].get("error"))
            else:
                last = f"HTTP {r.status_code}"
        except Exception as e:
            last = repr(e)[:100]
        time.sleep(1.0)
    fail[k] = last
    return None
if __name__ == "__main__":
    import random
    for k, g in KODLAR:
        if os.path.exists(yol(k)): continue
        j = cek(k)
        if j:
            json.dump(j, open(yol(k), "w"))
        time.sleep(random.uniform(0.3, 0.5))
    json.dump(fail, open(os.path.join(ham, "_basarisiz.json"), "w"), indent=1)
    print("bitti, basarisiz:", fail)
