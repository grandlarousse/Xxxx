"""VİOP günlük bülten indirici (2017-03-06 .. 2026-11-06). Yalnız hisse dışı vadeli satırlarını (F_*, pazar != D_EQ) UTF-8 olarak saklar."""
import os, sys, time, json, datetime as dt, subprocess, concurrent.futures as cf, threading
S = sys.argv[1]; D = f"{S}/data/viop_f"; os.makedirs(D, exist_ok=True)
lock = threading.Lock(); status_fn = f"{D}/_status.json"
status = json.load(open(status_fn)) if os.path.exists(status_fn) else {}
def days(a, b):
    d = a
    while d <= b:
        if d.weekday() < 5: yield d
        d += dt.timedelta(days=1)
def job(d):
    k = d.strftime("%Y%m%d"); fn = f"{D}/viop_{k}.csv"
    if os.path.exists(fn) or status.get(k) == 404: return k, "skip"
    url = f"https://www.borsaistanbul.com/data/vadeli/viop_{k}.csv"; tmp = f"{S}/data/tmp_{k}.csv"
    code = 0
    for att in range(5):
        r = subprocess.run(["curl", "-sS", "-o", tmp, "-w", "%{http_code}", "--max-time", "60", "-A", "Mozilla/5.0", url], capture_output=True, text=True)
        try: code = int(r.stdout.strip() or 0)
        except: code = 0
        if code in (200, 404): break
        time.sleep(2 * (2 ** att))
    if code == 200 and os.path.exists(tmp) and os.path.getsize(tmp) > 20000:
        raw = open(tmp, "rb").read().decode("windows-1254", errors="replace").splitlines()
        keep = raw[:2] + [l for l in raw[2:] if l.split(";")[1:2] and l.split(";")[1].startswith("F_") and l.split(";")[3] != "D_EQ"]
        open(fn + ".part", "w").write("\n".join(keep) + "\n"); os.replace(fn + ".part", fn)
    res = code
    if os.path.exists(tmp): os.remove(tmp)
    time.sleep(0.4)
    return k, res
ds = list(days(dt.date(2017, 3, 6), dt.date(2026, 11, 6)))
n = 0
with cf.ThreadPoolExecutor(3) as ex:
    for k, res in ex.map(job, ds):
        n += 1
        with lock:
            if res != "skip": status[k] = res
            if n % 100 == 0:
                json.dump(status, open(status_fn, "w")); print(k, n, len(ds), flush=True)
json.dump(status, open(status_fn, "w"))
print("DONE", sum(1 for v in status.values() if v == 200), "ok", sum(1 for v in status.values() if v == 404), "404", sum(1 for v in status.values() if v not in (200, 404)), "other", flush=True)
