"""1b) Senkronizasyon sağlamlığı: 2024-06-12..2026-10-30 penceresinde sürücüleri saatlik 15:00 UTC anlık fiyatla (BIST kapanışı)
ölçerek (C) varyans ayrıştırmasını tekrarla ve günlük kapanışlı (A) sürümle karşılaştır. EEM/TUR hariç (15:00 UTC'de ABD nakit seansı yok/eksik).
"""
import numpy as np, pandas as pd
from common import *
from vardec import r2_engine, shapley
from dy import matrix, SHORT
drv = ["ES=F", "^STOXX50E", "^VIX", "DX-Y.NYB", "BZ=F", "GC=F", "^TNX", "TRY=X"]
a, b = "2024-06-12", "2026-10-30"
rows = []
MA = matrix(STOCKS, drivers=drv, align="A"); MC = matrix(STOCKS, drivers=drv, align="C")
for al, M in [("A", MA), ("C", MC)]:
    F = pd.DataFrame({SHORT[d]: M[SHORT[d]] for d in drv})
    for d in drv: F[SHORT[d] + "_l1"] = F[SHORT[d]].shift(1)
    G = [c for d in drv if d != "TRY=X" for c in (SHORT[d], SHORT[d] + "_l1")]; TRc = ["USDTRY", "USDTRY_l1"]
    for s in STOCKS + ["XU100"]:
        D = F[G + TRc].copy(); D["y"] = M[s]
        if s != "XU100": D["MKT"] = M["XU100"]; D["SEC"] = peer_factor(s)
        d = D[(D.index >= a) & (D.index <= b)].dropna()
        cols = G + TRc + (["MKT", "SEC"] if s != "XU100" else [])
        r2, n = r2_engine(d["y"].values, d[cols].values); ix = {c: i for i, c in enumerate(cols)}
        groups = {"global": [ix[c] for c in G], "trmakro": [ix[c] for c in TRc]}
        if s != "XU100": groups.update({"piyasa": [ix["MKT"]], "sektor": [ix["SEC"]]})
        sh, alone, uniq, full, v = shapley(groups, r2)
        rows.append({"align": al, "stock": s, "n": n, "r2_full_adj": full, **{f"sh_{k}": x for k, x in sh.items()}, **{f"alone_{k}": x for k, x in alone.items()}})
R = pd.DataFrame(rows); R.to_csv(os.path.join(CACHE, "vardec_sync_compare.csv"), index=False)
print(R.groupby("align")[[c for c in R.columns if c.startswith(("sh_", "alone_", "r2"))]].median().round(3).T)
print(R[R.stock == "XU100"].round(3).to_string())
