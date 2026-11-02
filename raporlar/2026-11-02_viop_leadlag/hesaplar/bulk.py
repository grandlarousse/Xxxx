import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from concurrent.futures import ThreadPoolExecutor
import universe as u, ydl
kind = sys.argv[1]; which = sys.argv[2]
if which == "all":
    syms = [s + ".IS" for s in u.VIOP + u.BIST_EXTRA] + sorted({x for v in u.G.values() for x in v})
elif which == "core":  # saatlik/5dk için
    syms = [s + ".IS" for s in u.VIOP + ["XU030","XU100","XBANK","XUSIN","XHOLD","XLBNK"]] + sys.argv[3].split(",")
res = {}
def job(s):
    r = ydl.fetch(s, kind); time.sleep(0.2); return s, r
with ThreadPoolExecutor(4) as ex:
    for s, r in ex.map(job, syms):
        res[s] = r
json.dump(res, open(os.path.join(ydl.BASE, f"dl_status_{kind}_{which}.json"), "w"), indent=0)
bad = {k: v for k, v in res.items() if not (v.startswith("ok") or v == "cached")}
print(kind, which, "total", len(res), "bad", len(bad)); print(bad)
