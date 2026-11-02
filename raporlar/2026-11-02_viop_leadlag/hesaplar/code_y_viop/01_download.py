"""VİOP günlük bülten indirici. Ortak dizin: $S/data/viop/viop_YYYYMMDD.csv (ham, windows-1254).
Nazik: istekler arası >=0,3 sn; dosya varsa atla; 404 (tatil) -> _status.json'a yazılır, tekrar denenmez.
Sıra: 2023-01..bugün, sonra 2020-2022, sonra 2017-03..2019."""
import os, sys, time, json, datetime as dt, subprocess
S = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
D = f"{S}/data/viop"; os.makedirs(D, exist_ok=True)
ST = f"{D}/_status.json"
status = json.load(open(ST)) if os.path.exists(ST) else {}
def days(a, b):
    d = a
    while d <= b:
        if d.weekday() < 5: yield d
        d += dt.timedelta(days=1)
today = dt.date(2026, 11, 2)
blocks = [(dt.date(2023, 1, 1), today), (dt.date(2020, 1, 1), dt.date(2022, 12, 31)), (dt.date(2017, 3, 1), dt.date(2019, 12, 31))]
import urllib.request
n_ok = n_404 = n_skip = 0
for a, b in blocks:
    for d in sorted(days(a, b), reverse=False):
        k = d.strftime("%Y%m%d"); fn = f"{D}/viop_{k}.csv"
        if os.path.exists(fn) or status.get(k) == 404: n_skip += 1; continue
        url = f"https://www.borsaistanbul.com/data/vadeli/viop_{k}.csv"
        code = None
        for att in range(3):
            try:
                r = subprocess.run(["curl", "-sS", "-o", fn + ".part", "-w", "%{http_code}", "--max-time", "60", url], capture_output=True, text=True)
                code = int(r.stdout.strip() or 0)
                if code in (200, 404): break
            except Exception as e:
                code = -1
            time.sleep(2)
        if code == 200 and os.path.getsize(fn + ".part") > 20000:
            os.rename(fn + ".part", fn); n_ok += 1; status[k] = 200
        else:
            if os.path.exists(fn + ".part"): os.remove(fn + ".part")
            status[k] = code; n_404 += 1
        if (n_ok + n_404) % 50 == 0:
            json.dump(status, open(ST, "w")); print(k, n_ok, n_404, n_skip, flush=True)
        time.sleep(0.3)
json.dump(status, open(ST, "w")); print("DONE", n_ok, n_404, n_skip, flush=True)
