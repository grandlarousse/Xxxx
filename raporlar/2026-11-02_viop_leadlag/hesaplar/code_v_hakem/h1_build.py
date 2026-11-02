"""H1: panelleri kur (hepsi kendi hizalamamla). Çıktı res/*.parquet
 Y_raw  : hisse gün-içi ln(c/o)
 Y_h    : hedge'li gün-içi = intra_s - b_s * intra_XU100 (b: geçmiş 250g, t-1'e kadar)
 G_h    : hedge'li gap
 CC_res : hisse cc artığı (cc_s - b * cc_XU100) [yurt içi aile için]
 PR     : emsal pencere getirisi (BIST günü t'ye atanan), PI: emsalin bölge endeksi pencere getirisi, PB: beta (geçmiş)
 X_res  : sepet artığı ortalaması (emsal - beta*bölge endeksi), X_raw: ham sepet, X_mkt: sepetin piyasa bileşeni (beta*endeks), X_d1: emsal - endeks (beta=1)
 X_res_<REG>: bölge alt-sepeti artığı (AM / EU / ASIA)
 X_dom  : yurt içi emsal cc artığı (t-1), OWN_l1: hissenin kendi cc artığı (t-1)
"""
import sys, os, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import vh
from peers import PEERS, DOM, SECTOR

t0 = time.time()
cal = vh.bist_cal()
STOCKS = list(PEERS.keys())
xu = vh.bist_decomp("XU100"); xu30 = vh.bist_decomp("XU030")
D = {s: vh.bist_decomp(s) for s in STOCKS}
Y_raw = pd.DataFrame({s: D[s]["intra"] for s in STOCKS})
G_raw = pd.DataFrame({s: D[s]["gap"] for s in STOCKS})
CC = pd.DataFrame({s: D[s]["cc"] for s in STOCKS})
xi = xu["intra"]; xg = xu["gap"]; xc = xu["cc"]
def hedge(A, x):
    B = A.apply(lambda c: vh.roll_beta(c, x))
    return A - B.mul(x, axis=0), B
Y_h, BY = hedge(Y_raw, xi)
G_h, _ = hedge(G_raw, xg)
CC_res, _ = hedge(CC, xc)
print("hedef panelleri", f"{time.time()-t0:.1f}s", flush=True)

# ---- emsaller ----
allp = sorted(set(p for v in PEERS.values() for p in v))
meta = []
PR, PI = {}, {}
idx_cache = {}
for p in allp:
    b = vh.bucket(p)
    r = vh.foreign_ret(p)
    if r is None or b == "sync":
        meta.append({"peer": p, "bucket": b, "region": vh.region_name(p), "index": vh.region_index(p), "ok": False, "n": 0}); continue
    ix = vh.region_index(p)
    if ix not in idx_cache:
        ri = vh.foreign_ret(ix); idx_cache[ix] = ri
    ri = idx_cache[ix]
    # ortak seans günleri: emsal ve endeks aynı yerel takvim; emsalin işlem görmediği gün endeks getirisi de pencereye girmesin diye ortak günlerde hizala
    common = r.index.intersection(ri.index)
    rr = r.reindex(common); ii = ri.reindex(common)
    PR[p] = vh.to_bist_window(rr, b); PI[p] = vh.to_bist_window(ii, b)
    meta.append({"peer": p, "bucket": b, "region": vh.region_name(p), "index": ix, "ok": True, "n": int(PR[p].loc[vh.START:].notna().sum()),
                 "first": str(PR[p].first_valid_index().date()) if PR[p].notna().any() else ""})
PR = pd.DataFrame(PR); PI = pd.DataFrame(PI)
PB = pd.DataFrame({p: vh.roll_beta(PR[p], PI[p]) for p in PR.columns})
PE = PR - PB * PI          # artık
PM = PB * PI               # piyasa bileşeni
PD1 = PR - PI              # beta=1 fark
meta = pd.DataFrame(meta); meta.to_csv(vh.RES + "/peer_meta.csv", index=False)
print("emsaller", PR.shape, "kullanılamayan", int((~meta.ok).sum()), f"{time.time()-t0:.1f}s", flush=True)

def basket(P, peers, minp=2):
    cols = [c for c in peers if c in P.columns]
    if not cols: return pd.Series(np.nan, index=P.index)
    X = P[cols]; k = X.notna().sum(axis=1)
    need = min(minp, len(cols))
    return X.mean(axis=1).where(k >= need)

out = {}
for name, P in [("X_res", PE), ("X_raw", PR), ("X_mkt", PM), ("X_d1", PD1)]:
    out[name] = pd.DataFrame({s: basket(P, PEERS[s]) for s in STOCKS})
for reg, regs in [("AM", {"AM"}), ("EU", {"EU"}), ("ASIA", {"JP", "KR", "TW", "AU"})]:
    out["X_res_" + reg] = pd.DataFrame({s: basket(PE, [p for p in PEERS[s] if vh.region_name(p) in regs], minp=1) for s in STOCKS})
out["NPEER"] = pd.DataFrame({s: PE[[c for c in PEERS[s] if c in PE.columns]].notna().sum(1) for s in STOCKS})

# ---- yurt içi (DOM) ----
dom_codes = sorted(set(p for v in DOM.values() for p in v))
DD = {c: (D[c] if c in D else vh.bist_decomp(c)) for c in dom_codes}
DCC = pd.DataFrame({c: DD[c]["cc"] for c in dom_codes})
DRES, _ = hedge(DCC, xc)
out["X_dom"] = pd.DataFrame({s: basket(DRES, DOM.get(s, []), minp=1).shift(1) for s in STOCKS})
out["OWN_l1"] = CC_res.shift(1)
# likidite: 20g ort. TL hacim (bilgi amaçlı)
VOL = pd.DataFrame({s: (vh.raw(s + ".IS")["v"] * vh.raw(s + ".IS")["c"]).reindex(cal) for s in STOCKS})

for k, v in {"Y_raw": Y_raw, "Y_h": Y_h, "G_raw": G_raw, "G_h": G_h, "CC": CC, "CC_res": CC_res, "BY": BY, "PR": PR, "PI": PI, "PB": PB, "PE": PE, "VOL": VOL, **out}.items():
    v.astype("float64").to_parquet(vh.RES + f"/{k}.parquet")
pd.DataFrame({"xu_intra": xi, "xu_gap": xg, "xu_cc": xc, "xu30_intra": xu30["intra"], "xu30_gap": xu30["gap"]}).to_parquet(vh.RES + "/XU.parquet")
print("bitti", f"{time.time()-t0:.1f}s")
