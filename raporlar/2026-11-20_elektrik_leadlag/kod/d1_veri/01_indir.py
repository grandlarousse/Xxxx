"""D1 adim 1: ham indirme (Yahoo + Is Yatirim). Kullanim:
  python3 -I 01_indir.py <RAW_DIR> [END=2026-11-20]
Cikti (ham, degistirilmeden): <RAW_DIR>/yahoo/<KOD>.json, <RAW_DIR>/isy_hisse/<KOD>.json, <RAW_DIR>/isy_endeks/<KOD>.json
ve <RAW_DIR>/fetch_log.txt. Mevcut dosya atlanir (yeniden indirmek icin sil)."""
import os, sys, time, json, random, datetime as dt, requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from concurrent.futures import ThreadPoolExecutor
from universe import STOCKS, IDX_ISY, IDX_YAHOO
RAW = sys.argv[1]
END = "2026-11-20"
for a in sys.argv[2:]:
    if a.startswith("END="): END = a[4:]
e = dt.date.fromisoformat(END)
S = requests.Session(); S.headers["User-Agent"] = "Mozilla/5.0"
ISY = "https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/"
def valid(kind, txt):
    try:
        j = json.loads(txt)
        if kind == "yahoo": return len(j["chart"]["result"][0]["timestamp"])
        if kind == "isy_hisse": return len(j["value"])
        return len(j["data"])
    except Exception:
        return 0
def get(kind, url, params, retries=5):
    for a in range(retries):
        try:
            r = S.get(url, params=params, timeout=120)
            if r.status_code == 200 and valid(kind, r.text) > 0: return r.text
        except Exception:
            pass
        time.sleep(2 ** a * 0.5 + random.random())
    return None
def job(t):
    kind, code = t
    out = os.path.join(RAW, kind, code + ".json")
    if os.path.exists(out): return t, "cached"
    if kind == "yahoo":
        p2 = int(dt.datetime(e.year, e.month, e.day, tzinfo=dt.timezone.utc).timestamp()) + 86400
        txt = get(kind, f"https://query1.finance.yahoo.com/v8/finance/chart/{code}.IS",
                  {"period1": 946684800, "period2": p2, "interval": "1d", "events": "div,splits"})
    elif kind == "isy_hisse":
        txt = get(kind, ISY + "Data.aspx/HisseTekil", {"hisse": code, "startdate": "01-01-2000", "enddate": e.strftime("%d-%m-%Y")})
    else:
        txt = get(kind, ISY + "ChartData.aspx/IndexHistoricalAll",
                  {"period": 1440, "from": "20000101000000", "to": e.strftime("%Y%m%d") + "235959", "endeks": code})
    if not txt: return t, "FAIL"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f: f.write(txt)
    return t, f"ok n={valid(kind, txt)} bytes={len(txt)}"
jobs = [("yahoo", s) for s in STOCKS + IDX_YAHOO] + [("isy_hisse", s) for s in STOCKS] + [("isy_endeks", s) for s in IDX_ISY]
os.makedirs(RAW, exist_ok=True)
with ThreadPoolExecutor(4) as ex, open(os.path.join(RAW, "fetch_log.txt"), "a") as lg:
    for t, r in ex.map(job, jobs):
        line = f"{dt.datetime.now().isoformat(timespec='seconds')} {t[0]} {t[1]} {r}"
        print(line, flush=True); lg.write(line + "\n")
