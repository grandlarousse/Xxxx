import sys, os, json, glob; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ll, universe as u, pandas as pd, numpy as np
grp = {}
for g, v in u.G.items():
    for x in v: grp.setdefault(x, g)
for x in u.VIOP: grp[x + ".IS"] = "VIOP"
for x in u.BIST_EXTRA: grp.setdefault(x + ".IS", "BIST_other")
files = sorted(glob.glob(os.path.join(ll.BASE, "daily", "*.parquet")))
R = {}; cat = []
for f in files:
    sym = os.path.basename(f)[:-8]
    try:
        r = ll.ret(sym)
    except Exception as e:
        print("fail", sym, e); continue
    r = r[r.index >= "2005-01-01"]
    m = ll.meta(sym)
    nn = int(r.notna().sum()); zero = float((r == 0).mean())
    cat.append({"sym": sym, "group": grp.get(sym, "BIST_other" if sym.endswith(".IS") else "?"), "name": m.get("longName") or m.get("shortName"), "ccy": m.get("currency"), "exch": m.get("fullExchangeName"), "tz": m.get("exchangeTimezoneName"), "type": m.get("instrumentType"), "first": str(r.first_valid_index().date()) if nn else None, "n": nn, "zero_frac": round(zero, 3)})
    R[sym] = r
P = pd.DataFrame(R)
P.to_parquet(os.path.join(ll.BASE, "panel_ret_bistcal.parquet"))
C = pd.DataFrame(cat); C.to_csv(os.path.join(ll.BASE, "catalog.csv"), index=False)
D = {}
for s in u.VIOP + ["XU030", "XU100", "XBANK", "XUSIN", "XHOLD"]:
    d = ll.decomp(s); d = d[d.index >= "2014-01-01"]
    for c in d: D[(s, c)] = d[c]
DP = pd.DataFrame(D); DP.columns = pd.MultiIndex.from_tuples(DP.columns); DP.to_parquet(os.path.join(ll.BASE, "panel_decomp_bist.parquet"))
print(P.shape, DP.shape); print(C.groupby("group").size())
print(C[C.zero_frac > 0.3][["sym", "zero_frac", "n"]].to_string())
