"""BIST Borçlanma Araçları Piyasası (BAP) kesin alım-satım günlük bülteni indirici.
URL: https://borsaistanbul.com/data/ttb/{YYYY}/{AA}/ttb{YYYYAAGG}{S}.zip ; S=3 (CSV, ~2020+) yoksa S=2 (XLS, eski).
Kayıt: data/bap/ttbYYYYMMDD{S}.zip (ortak). Dosya varsa atla. İstek arası 0,6 sn."""
import os, sys, time, subprocess
S = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
sys.path.insert(0, S + "/code"); import ll
OUT = S + "/data/bap"; os.makedirs(OUT, exist_ok=True)
LOG = S + "/out/code_y_makro_y/dl_bap_log.txt"
cal = ll.bist_cal(); cal = cal[(cal >= "2013-06-01") & (cal <= "2026-10-30")][::-1]
miss = set(open(LOG).read().split()) if os.path.exists(LOG) else set()
def get(url, fn):
    tmp = fn + f".part{os.getpid()}"
    for a in range(3):
        r = subprocess.run(["curl", "-s", "-o", tmp, "-w", "%{http_code}", "--max-time", "60", url], capture_output=True, text=True)
        code = r.stdout.strip()
        if code in ("200", "404"): break
        time.sleep(3)
    ok = code == "200" and os.path.exists(tmp) and open(tmp, "rb").read(2) == b"PK"  # 404 sayfası HTML; geçerli zip PK ile başlar (bazı geçerli zipler <9 KB)
    if ok: os.replace(tmp, fn)
    elif os.path.exists(tmp): os.remove(tmp)
    return ok
n = 0
for d in cal:
    ds = d.strftime("%Y%m%d"); y, m = ds[:4], ds[4:6]
    if any(os.path.exists(f"{OUT}/ttb{ds}{s}.zip") for s in "23") or ds in miss: continue
    ok = False
    for s in (("3", "2") if ds >= "20190101" else ("2", "3")):
        ok = get(f"https://borsaistanbul.com/data/ttb/{y}/{m}/ttb{ds}{s}.zip", f"{OUT}/ttb{ds}{s}.zip"); time.sleep(0.6)
        if ok: break
    if not ok: open(LOG, "a").write(ds + "\n")
    n += 1
    if n % 100 == 0: print(ds, n, flush=True)
print("DONE", n)
