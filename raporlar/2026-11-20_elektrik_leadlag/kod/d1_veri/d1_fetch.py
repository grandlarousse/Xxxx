"""D1 adim 1: ham indirme (Yahoo + Is Yatirim). Kullanim:
  python3 -I d1_fetch.py <RAW_DIR> [END=2026-11-20]
Cikti: <RAW_DIR>/yahoo/<KOD>.json, <RAW_DIR>/isy_hisse/<KOD>.json, <RAW_DIR>/isy_endeks/<KOD>.json (ham, degismeden).
Mevcut dosya atlanir (silerek yeniden indir)."""
import os, sys, time, json, random, requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from concurrent.futures import ThreadPoolExecutor
from universe import STOCKS, IDX_ISY, IDX_YAHOO
RAW = sys.argv[1]
END = "2026-11-20"
for a in sys.argv[2:]:
    if a.startswith("END="): END = a[4:]
import datetime as dt
e = dt.date.fromisoformat(END)
S = requests.Session(); S.headers["User-Agent"] = "Mozilla/5.0"
def get(url, params=None, retries=5):
    for a in range(retries):
        try:
            r = S.get(url, params=params, timeout=90)
            if r.status_code == 200 and r.text.strip():
                return r.text
            if r.status_code in (404,):
                return None
        except Exception:
            pass
        time.sleep(2 ** a * 0.5 + random.random())
    return None
def save(sub, code, txt):
    p = os.path.join(RAW, sub); os.makedirs(p, exist_ok=True)
    with open(os.path.join(p, code + ".json"), "w") as f: f.write(txt)
def job(t):
    kind, code = t
    out = os.path.join(RAW, kind, code + ".json")
    if os.path.exists(out): return t, "cached"
    if kind == "yahoo":
        p2 = int(dt.datetime(e.year, e.month, e.day, tzinfo=dt.timezone.utc).timestamp()) + 3 * 86400
        txt = get(f"https://query1.finance.yahoo.com/v8/finance/chart/{code}.IS",
                  {"period1": 946684800, "period2": p2, "interval": "1d", "events": "div,splits"})
    elif kind == "isy_hisse":
        txt = get("https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/HisseTekil",
                  {"hisse": code, "startdate": "01-01-2010", "enddate": e.strftime("%d-%m-%Y")})
    else:
        txt = get("https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/ChartData.aspx/IndexHistoricalAll",
                  {"period": 1440, "from": "20000101000000", "to": e.strftime("%Y%m%d") + "235959", "endeks": code})
    if not txt: return t, "FAIL"
    save(kind, code, txt); return t, f"ok {len(txt)}"
jobs = [("yahoo", s) for s in STOCKS + IDX_YAHOO] + [("isy_hisse", s) for s in STOCKS] + [("isy_endeks", s) for s in IDX_ISY]
with ThreadPoolExecutor(4) as ex:
    for t, r in ex.map(job, jobs):
        print(t, r, flush=True)
