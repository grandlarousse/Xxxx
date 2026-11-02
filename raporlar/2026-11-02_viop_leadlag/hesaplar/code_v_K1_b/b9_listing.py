"""Ham VİOP bültenlerinden 47 hissenin pay vadelisinin ilk görüldüğü tarih (birincil kaynak: borsaistanbul.com viop_YYYYMMDD.csv)."""
import sys, glob, re, os; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_K1_b")
from kb import *
files = sorted(glob.glob(S + "/data/viop/viop_2*.csv"))
first = {}; last = {}; pat = re.compile(rb";F_([A-Z0-9]+?)(\d{4});")
for f in files:
    d = os.path.basename(f)[5:13]
    try: b = open(f, "rb").read()
    except Exception: continue
    roots = set(m.group(1).decode() for m in pat.finditer(b))
    for r in roots:
        first.setdefault(r, d); last[r] = d
rows = [dict(sym=s, ilk=first.get(s), son=last.get(s)) for s in VIOP]
R = pd.DataFrame(rows); R["ilk"] = pd.to_datetime(R.ilk); R["son"] = pd.to_datetime(R.son)
print("dosya:", len(files), files[0][-12:-4], files[-1][-12:-4])
print(R.sort_values("ilk").to_string()); R.to_csv(OUT + "/res_b9_listing.csv", index=False)
