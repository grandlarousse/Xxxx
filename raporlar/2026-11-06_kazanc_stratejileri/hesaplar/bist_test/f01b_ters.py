"""f01_hisse.py ile ayni, listeyi TERS sirada isler (en fazla 2 paralel istek kuralina uygun ikinci isci)."""
import os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from f01_hisse import one, SP, SIB
mem = json.load(open(SP + "/data/bist_test/kap_endeks_uyeleri.json"))
codes = list(dict.fromkeys(mem["XUTUM"] + sum([mem[k] for k in mem if k.startswith("X")], [])))
sib = set(x[:-5] for x in os.listdir(SIB) if x.endswith(".json"))
codes = [c for c in codes if c not in sib][::-1]
for c in codes:
    st = one(c); print(c, st, flush=True)
    if st not in ("cached", "sib"): time.sleep(0.7)
