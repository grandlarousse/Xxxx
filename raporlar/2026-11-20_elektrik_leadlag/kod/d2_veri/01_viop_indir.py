"""VİOP günlük bülten indirici + süzgeç. Kaynak: https://www.borsaistanbul.com/data/vadeli/viop_YYYYMMDD.csv
Ham dosya indirilir, yalnız ilgili satırlar RAW/viop_filt/viop_YYYYMMDD.csv (utf-8; 1. satır başlık) olarak saklanır, ham dosya silinir.
Saklanan satırlar (kod F_ ile başlar):
  - pay vadelisi: segment SSF ve dayanak AKSEN.E ENJSA.E ODAS.E ASTOR.E ALARK.E
  - XU030 endeks vadelisi: segment INF ve dayanak D_XU030D (sınıf DE_BIST30_FUT)
  - baz yük elektrik: segment ENF ve kod F_ELCBAS* (aylık, çeyreklik, yıllık)
404 = dosya yok (tatil). Durum: RAW/viop_filt/_status.json  {YYYYMMDD: "404" | "200|toplam|ssf|inf|enf" | "ERR<kod>"}
Kullanım: python3 -I 01_viop_indir.py   (8 eşzamanlı curl; var olan/404 günler atlanır, hatalılar yeniden denenir)"""
import os, sys, json, time, subprocess, datetime as dt
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from d2common import RAW, START, END, UA
TMP = RAW + "/viop_tmp"; FILT = RAW + "/viop_filt"; ST = FILT + "/_status.json"
UND = {"AKSEN.E", "ENJSA.E", "ODAS.E", "ASTOR.E", "ALARK.E"}
status = json.load(open(ST)) if os.path.exists(ST) else {}

def days(a, b):
    d = a
    while d <= b:
        if d.weekday() < 5: yield d
        d += dt.timedelta(days=1)

def filt(fn, out):
    with open(fn, encoding="cp1254", errors="replace") as fh: lines = fh.read().splitlines()
    hdr = [h.strip() for h in lines[0].split(";")]
    ic, isg, iu = hdr.index("SOZLESME KODU"), hdr.index("PAZAR SEGMENTI"), hdr.index("DAYANAK VARLIK")
    kept = []; n = [0, 0, 0]
    for ln in lines[2:]:
        f = ln.split(";")
        if len(f) < 20: continue
        code, seg, und = f[ic].strip(), f[isg].strip(), f[iu].strip()
        if not code.startswith("F_"): continue
        if seg == "SSF" and und in UND: n[0] += 1
        elif seg == "INF" and und == "D_XU030D": n[1] += 1
        elif seg == "ENF" and code.startswith("F_ELCBAS"): n[2] += 1
        else: continue
        kept.append(ln)
    with open(out + ".part", "w", encoding="utf-8") as fo: fo.write("\n".join([";".join(hdr)] + kept) + "\n")
    os.rename(out + ".part", out)
    return f"200|{len(lines) - 2}|{n[0]}|{n[1]}|{n[2]}"

def work(d):
    k = d.strftime("%Y%m%d"); out = f"{FILT}/viop_{k}.csv"; fn = f"{TMP}/viop_{k}.csv"
    url = f"https://www.borsaistanbul.com/data/vadeli/viop_{k}.csv"
    code = -1
    for att in range(4):
        try:
            r = subprocess.run(["curl", "-sS", "-A", UA, "-o", fn, "-w", "%{http_code}", "--max-time", "120", url], capture_output=True, text=True)
            code = int(r.stdout.strip() or 0)
        except Exception:
            code = -1
        if code == 404: break
        if code == 200:
            with open(fn, "rb") as fh: head = fh.read(6)
            if os.path.getsize(fn) > 20000 and head == b"TARIH;": break
            code = 1000  # 200 ama beklenen dosya değil
        time.sleep(2 * (att + 1))
    try:
        res = filt(fn, out) if code == 200 else ("404" if code == 404 else f"ERR{code}")
    except Exception as e:
        res = f"ERRparse:{type(e).__name__}"
    if os.path.exists(fn): os.remove(fn)
    return k, res

def main():
    a, b = dt.date.fromisoformat(START), dt.date.fromisoformat(END)
    todo = [d for d in days(a, b) if not (status.get(d.strftime("%Y%m%d"), "").startswith(("200", "404")))]
    print("todo", len(todo), flush=True)
    n = 0
    with ThreadPoolExecutor(8) as ex:
        for k, res in ex.map(work, todo):
            status[k] = res; n += 1
            if n % 100 == 0:
                json.dump(status, open(ST, "w")); print(n, k, res, flush=True)
    json.dump(status, open(ST, "w"), indent=0)
    from collections import Counter
    print("DONE", Counter(v.split("|")[0] for v in status.values()), flush=True)
if __name__ == "__main__": main()
