"""B0: VİOP bülteni 2017-04-03..2019-12-31 (diğer iki indirici bu aralığa en son gelecek). Ortak dizin, dosya varsa atla, istek arası 0,5 sn.
Diğer indiricilerin 404 listesi (code_y_makro_y/dl_viop_log.txt, data/viop/_status.json) okunur, tekrar denenmez."""
import os, json, time, subprocess, datetime as dt
S = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"; D = S + "/data/viop"
LOG = S + "/out/code_v_G3_a/res/dl_2017_2019.txt"
miss = set()
for p in [S + "/out/code_y_makro_y/dl_viop_log.txt", LOG]:
    if os.path.exists(p): miss |= set(open(p).read().split())
st = D + "/_status.json"
if os.path.exists(st):
    try: miss |= {k for k, v in json.load(open(st)).items() if v == 404}
    except Exception: pass
d = dt.date(2017, 4, 3); n_ok = n_bad = 0
while d <= dt.date(2019, 12, 31):
    k = d.strftime("%Y%m%d"); fn = f"{D}/viop_{k}.csv"
    if d.weekday() < 5 and not os.path.exists(fn) and k not in miss:
        tmp = fn + f".part{os.getpid()}"
        code = "0"
        for att in range(3):
            r = subprocess.run(["curl", "-s", "-o", tmp, "-w", "%{http_code}", "--max-time", "60", f"https://www.borsaistanbul.com/data/vadeli/viop_{k}.csv"], capture_output=True, text=True)
            code = r.stdout.strip()
            if code in ("200", "404"): break
            time.sleep(3)
        if code == "200" and os.path.getsize(tmp) > 20000:
            if not os.path.exists(fn): os.replace(tmp, fn)
            else: os.remove(tmp)
            n_ok += 1
        else:
            if os.path.exists(tmp): os.remove(tmp)
            open(LOG, "a").write(k + "\n"); n_bad += 1
        time.sleep(0.5)
    d += dt.timedelta(days=1)
print("DONE", n_ok, n_bad)
