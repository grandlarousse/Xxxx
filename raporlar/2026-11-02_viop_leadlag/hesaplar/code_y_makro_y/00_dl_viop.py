"""VİOP günlük bülteni indirici (2017-04 .. 2026-10). Ortak dizin: data/viop/viop_YYYYMMDD.csv. Dosya varsa atlar. İstek arası >=0,35 sn."""
import os, sys, time, subprocess
import pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
sys.path.insert(0, S + "/code"); import ll
OUT = S + "/data/viop"; os.makedirs(OUT, exist_ok=True)
LOG = S + "/out/code_y_makro_y/dl_viop_log.txt"
cal = ll.bist_cal(); cal = cal[(cal >= "2017-03-01") & (cal <= "2026-10-30")][::-1]
miss = set(open(LOG).read().split()) if os.path.exists(LOG) else set()
n_ok = n_skip = n_404 = 0
for d in cal:
    ds = d.strftime("%Y%m%d"); fn = f"{OUT}/viop_{ds}.csv"
    if os.path.exists(fn) or ds in miss: n_skip += 1; continue
    tmp = fn + f".part{os.getpid()}"
    for attempt in range(3):
        r = subprocess.run(["curl", "-s", "-o", tmp, "-w", "%{http_code}", "--max-time", "60", f"https://www.borsaistanbul.com/data/vadeli/viop_{ds}.csv"], capture_output=True, text=True)
        code = r.stdout.strip()
        if code in ("200", "404"): break
        time.sleep(3)
    if code == "200" and os.path.getsize(tmp) > 20000:
        if not os.path.exists(fn): os.replace(tmp, fn)
        else: os.remove(tmp)
        n_ok += 1
    else:
        if os.path.exists(tmp): os.remove(tmp)
        open(LOG, "a").write(ds + "\n"); n_404 += 1
    time.sleep(0.35)
    if (n_ok + n_404) % 100 == 0: print(ds, n_ok, n_404, n_skip, flush=True)
print("DONE", n_ok, n_404, n_skip)
