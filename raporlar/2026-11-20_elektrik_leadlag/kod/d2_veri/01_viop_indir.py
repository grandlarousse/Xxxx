"""VİOP günlük bülten indirici + süzgeç (D2). Ham dosya indirilir, yalnız ilgili satırlar saklanır, ham dosya silinir.
Saklanan satırlar (F_ ile başlayan vadeliler):
  - pay vadelisi: dayanak AKSEN.E ENJSA.E ODAS.E ASTOR.E ALARK.E
  - XU030 endeks vadelisi: DAYANAK VARLIK D_XU030D (sınıf DE_BIST30_FUT; görev metnindeki 'sınıf D_XU030D' bülten sütununda aslında dayanak)
  - baz yük elektrik vadelileri: segment ENF, kod F_ELCBAS*
Çıktı: $DATA/viop_filt/viop_YYYYMMDD.txt (utf-8; 1. satır başlık, sonrası süzülmüş satırlar), _status.json
Kullanım: python3 -I 01_viop_indir.py   (8 eşzamanlı curl)
"""
import os, json, subprocess, datetime as dt, threading
from concurrent.futures import ThreadPoolExecutor
S = "/tmp/claude-0/-home-user-Xxxx/4917622c-a1fc-5288-a182-a19cca9a4438/scratchpad/el"
RAW = f"{S}/data/d2_raw"; FILT = f"{S}/data/viop_filt"
os.makedirs(RAW, exist_ok=True); os.makedirs(FILT, exist_ok=True)
ST = f"{FILT}/_status.json"
UND = {"AKSEN.E", "ENJSA.E", "ODAS.E", "ASTOR.E", "ALARK.E"}
status = json.load(open(ST)) if os.path.exists(ST) else {}
lock = threading.Lock()

def days(a, b):
    d = a
    while d <= b:
        if d.weekday() < 5: yield d
        d += dt.timedelta(days=1)

def keep(f):
    code, seg, cls, und = f[1].strip(), f[4].strip(), f[6].strip(), f[7].strip()  # sütunlar: 2 kod, 5 segment, 7 sınıf, 8 dayanak
    if not code.startswith("F_"): return False
    return (und in UND) or (und == "D_XU030D") or (cls == "DE_BIST30_FUT") or (seg == "ENF" and code.startswith("F_ELCBAS"))

def work(d):
    k = d.strftime("%Y%m%d")
    out = f"{FILT}/viop_{k}.txt"
    if os.path.exists(out): return k, "have"
    url = f"https://www.borsaistanbul.com/data/vadeli/viop_{k}.csv"
    fn = f"{RAW}/viop_{k}.csv"
    code = -1
    for att in range(4):
        try:
            r = subprocess.run(["curl", "-sS", "-o", fn, "-w", "%{http_code}", "--max-time", "90", url], capture_output=True, text=True)
            code = int(r.stdout.strip() or 0)
        except Exception:
            code = -1
        if code == 404: break
        if code == 200:
            sz = os.path.getsize(fn)
            with open(fn, "rb") as fh: head = fh.read(6)
            if sz > 20000 and head == b"TARIH;": break
            code = 1000  # 200 ama beklenen dosya değil
        import time; time.sleep(1.5 * (att + 1))
    if code == 200:
        with open(fn, encoding="cp1254", errors="replace") as fh: lines = fh.read().splitlines()
        hdr = lines[0]; kept = []
        for ln in lines[2:]:
            f = ln.split(";")
            if len(f) >= 22 and keep(f): kept.append(ln)
        with open(out + ".part", "w", encoding="utf-8") as fo: fo.write("\n".join([hdr] + kept) + "\n")
        os.rename(out + ".part", out)
        os.remove(fn)
        return k, f"200 total={len(lines)-2} kept={len(kept)}"
    if os.path.exists(fn): os.remove(fn)
    return k, str(code)

def main():
    a, b = dt.date(2017, 3, 1), dt.date(2026, 11, 19)
    todo = [d for d in days(a, b) if status.get(d.strftime("%Y%m%d")) != "404"]
    print("todo", len(todo), flush=True)
    n = 0
    with ThreadPoolExecutor(10) as ex:
        for k, res in ex.map(work, todo):
            with lock:
                if res != "have": status[k] = res if res == "404" or not res.startswith("200") else "200"
                n += 1
                if n % 100 == 0:
                    json.dump(status, open(ST, "w")); print(n, k, res, flush=True)
    json.dump(status, open(ST, "w"))
    from collections import Counter
    print(Counter(v for v in status.values()))
if __name__ == "__main__": main()
