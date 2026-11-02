"""ANA MATRİS: (47 VİOP + XU100/XU030/XBANK) x tüm BIST-dışı semboller.
Aileler (Y=hedef, X=sürücü dönüşümü), pencere: full/is/oos/3y/1y
  sync     : cc_t            ~ d_t
  sync_usd : (cc_t - USDTRY_t) ~ d_t
  pc_xu    : resid(cc|XU100) ~ resid(d|XU100)              (senkron kısmi)
  pc_xt    : resid(cc|XU100,USDTRY) ~ resid(d|XU100,USDTRY)
  pc_glob  : resid(cc|10 küresel faktör) ~ resid(d|aynı)   (ortak küresel faktör sonrası)
  gap_l1   : gap_t   ~ d_{t-1}
  intra_l1 : intra_t ~ d_{t-1}      (ABD/Avrupa sürücüsü için işlenebilir öncülük)
  intra_l0 : intra_t ~ d_t          (sadece asia_pre kovasında işlenebilir)
  cum25    : cc_t    ~ sum_{k=2..5} d_{t-k}   (işlenebilir, çok günlü sürüklenme)
  rev      : d_{t+1} ~ cc_t          (ters yön: hisse önde)
Çalıştır: nice -n 10 python3 matrix.py   -> out/tarama_matrix.parquet + cache/*.npz
"""
import os, sys, time, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tlib import *

t0 = time.time()
P, DP = load_panels()
cat = pd.read_csv(os.path.join(DATA, "catalog.csv")).set_index("sym")
rows = VIOP + IDXROWS
drivers = [c for c in P.columns if not c.endswith(".IS") and P[c].notna().sum() > 0]
X = P[drivers]
idx = P.index
CC = P[[r + ".IS" for r in rows]].values
GAP = DP.reindex(idx).loc[:, [(r, "gap") for r in rows]].values
INTRA = DP.reindex(idx).loc[:, [(r, "intra") for r in rows]].values
xu = P["XU100.IS"].values; usd = P["TRY=X"].values
GLOB = ["EEM", "^GSPC", "^STOXX50E", "BZ=F", "GC=F", "HG=F", "DX-Y.NYB", "^TNX"]
Cxu = xu[:, None]; Cxt = np.column_stack([xu, usd]); Cgl = np.column_stack([xu, usd] + [P[g].values for g in GLOB])

# sürücü meta
dm = pd.DataFrame(index=drivers)
dm["group"] = [cat.loc[d, "group"] if d in cat.index else "?" for d in drivers]
dm["name"] = [cat.loc[d, "name"] if d in cat.index else "" for d in drivers]
dm["tz"] = [cat.loc[d, "tz"] if d in cat.index else "" for d in drivers]
dm["exch"] = [cat.loc[d, "exch"] if d in cat.index else "" for d in drivers]
dm["bucket"] = [bucket(d, dm.loc[d, "tz"], dm.loc[d, "exch"]) for d in drivers]
nn = X.notna().sum(); zf = (X == 0).sum() / nn.replace(0, np.nan)
dm["n_2014"] = nn.values; dm["zero_frac_2014"] = zf.round(3).values
dm["sparse"] = (dm["zero_frac_2014"] > 0.3) | (dm["n_2014"] < 1000)
dm["mirror"] = dm.index.isin(MIRROR)
dm["tv"] = [tv(d, dm.loc[d, "exch"]) for d in drivers]
dm.to_parquet(os.path.join(CACHE, "driver_meta.parquet"))

def shifted(A, k):
    out = np.full_like(A, np.nan)
    if k > 0: out[k:] = A[:-k]
    elif k < 0: out[:k] = A[-k:]
    else: out = A.copy()
    return out

def cum25(A):
    return shifted(A, 2) + shifted(A, 3) + shifted(A, 4) + shifted(A, 5)

def win_mask(w):
    a, b = WIN[w]; return (idx >= pd.Timestamp(a)) & (idx <= pd.Timestamp(b))

def families(Xm):
    """Xm: T x B sürücü matrisi -> {fam: (Y, Xtrans, windows, resid_controls)}"""
    Xl1 = shifted(Xm, 1)
    return {
        "sync": (CC, Xm, ["full", "is", "oos", "3y", "1y"], None),
        "sync_usd": (CC - usd[:, None], Xm, ["full", "is", "oos", "1y"], None),
        "pc_xu": (CC, Xm, ["full", "is", "oos", "3y", "1y"], Cxu),
        "pc_xt": (CC, Xm, ["full", "is", "oos", "1y"], Cxt),
        "pc_glob": (CC, Xm, ["full", "is", "oos"], Cgl),
        "gap_l1": (GAP, Xl1, ["full", "is", "oos", "1y"], None),
        "intra_l1": (INTRA, Xl1, ["full", "is", "oos", "1y"], None),
        "intra_l0": (INTRA, Xm, ["full", "is", "oos", "1y"], None),
        "cum25": (CC, cum25(Xm), ["full", "is", "oos", "1y"], None),
        "rev": (CC, shifted(Xm, -1), ["full", "is", "oos", "1y"], None),
    }

def run(Xm, fams=None, wins=None, tag=""):
    res = {}
    for f, (Y, Xt, ws, C) in families(Xm).items():
        if fams and f not in fams: continue
        for w in ws:
            if wins and w not in wins: continue
            m = win_mask(w)
            Yw, Xw = Y[m], Xt[m]
            if C is not None:
                Cw = C[m]; Yw = resid(Yw, Cw); Xw = resid(Xw, Cw)
            c, n, t, b = mcorr(Yw, Xw, min_n=150 if w == "1y" else 250)
            res[(f, w)] = (c, n, t, b)
    return res

if __name__ == "__main__":
    res = run(X.values)
    # uzun format tablo
    A, B = len(rows), len(drivers)
    base = pd.DataFrame({"stock": np.repeat(rows, B), "driver": np.tile(drivers, A)})
    cols = {}
    for (f, w), (c, n, t, b) in res.items():
        cols[f"{f}_{w}"] = c.ravel(); cols[f"t_{f}_{w}"] = t.ravel()
        if w in ("full", "is", "oos"): cols[f"n_{f}_{w}"] = n.ravel().astype(np.int32)
        if f == "sync" and w == "full": cols["beta_sync_full"] = b.ravel()
    M = pd.concat([base, pd.DataFrame(cols)], axis=1)
    M = M.merge(dm[["group", "bucket", "sparse", "mirror", "n_2014", "zero_frac_2014", "tv"]], left_on="driver", right_index=True, how="left")
    M["is_index_row"] = M["stock"].isin(IDXROWS)
    # kontrol değişkeninin kendisi sürücüyse kısmi korelasyon tanımsız
    for f, ctrl in [("pc_xt", {"TRY=X"}), ("pc_glob", set(GLOB) | {"TRY=X"})]:
        bad = M["driver"].isin(ctrl)
        for c in [c for c in M.columns if c.startswith(f) or c.startswith("t_" + f)]: M.loc[bad, c] = np.nan
    # p ve BH-FDR (yalnız 47 VİOP satırı, tam dönem, aile bazında)
    v = ~M["is_index_row"]
    for f in ["sync", "sync_usd", "pc_xu", "pc_xt", "pc_glob", "gap_l1", "intra_l1", "intra_l0", "cum25", "rev"]:
        for w in ["full", "is", "oos"]:
            p = p_from_t(M[f"t_{f}_{w}"].values); M[f"p_{f}_{w}"] = p
            if w == "full":
                pa = np.full(len(M), np.nan); pa[v.values] = bh_adj(p[v.values]); M[f"q_{f}_full"] = pa
    for c in M.columns:
        if M[c].dtype == np.float64: M[c] = M[c].astype(np.float32)
    M.to_parquet(os.path.join(OUT, "tarama_matrix.parquet"), index=False)
    print("matrix", M.shape, "sürücü", B, "satır", A, f"{time.time()-t0:.1f}s")
