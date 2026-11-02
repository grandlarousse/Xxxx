"""Tarama sürprizlerinin mekanizma/stabilite kontrolü: H1 (sürücü_{t-1} -> hisse-XU100 gün-içi) FDR geçenler, IS/OOS NW-t."""
import pandas as pd, numpy as np, elib
from elib import R, DEC
S = pd.read_csv(elib.RES + "/scan_all.csv")
h = S[(S.test == "H1") & S.fdr].sort_values("t", key=abs, ascending=False)
xud = DEC("XU100"); rows = []
for r in h.itertuples():
    d = DEC(r.stock); st = elib.lead_stats(d.intra - xud.intra, R(r.sym).shift(1))
    rows.append({"stock": r.stock, "sym": r.sym, "group": r.group, "t_scan": round(r.t, 2), "padj": round(r.padj, 3), "c_is": round(st["is"][0], 3), "t_is": round(st["is"][1], 2), "c_oos": round(st["oos"][0], 3), "t_oos": round(st["oos"][1], 2)})
O = pd.DataFrame(rows); O.to_csv(elib.RES + "/scan_H1_fdr_isoos.csv", index=False); print(O.to_string(index=False))
