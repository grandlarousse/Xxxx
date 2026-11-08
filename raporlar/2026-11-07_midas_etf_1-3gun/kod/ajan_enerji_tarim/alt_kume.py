"""Hazır sonuçların aile alt kümesi + aile tutarlılık tablosu (ilk çalıştırılacak betik).
  sonuclar/aile_enerji_tarim/genel_aile.csv  : genel_tum.csv'nin 28 aile ETF'i (8316 satır) + tek yönlü p (net>0) + aile içi BH-FDR
  sonuclar/aile_enerji_tarim/leadlag_aile.csv: leadlag_sweep.csv'nin aile hedefleri
  sonuclar/aile_enerji_tarim/aile_tutarlilik.csv: 8 küme temsilcisinde sinyal x mod x h tutarlılığı (Stouffer t)
Çalıştırma: python3 -I kod/ajan_enerji_tarim/alt_kume.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from scipy import stats as st
import ortak as O, lib

g = pd.read_csv(os.path.join(lib.ROOT, "sonuclar", "genel_tum.csv"))
f = g[g.sym.isin(O.FAM)].copy()
f["p1"] = st.t.sf(f["t"].fillna(-9), (f["n"] - 1).clip(lower=2))
f["fdr1_aile"] = lib.bh_fdr(f["p1"].values, 0.10)
f["esik"] = (f.mean_net_bp > 0) & (f.t >= 2) & (f.is_net_bp > 0) & (f.oos_net_bp > 0) & (f.years_pos_frac >= 0.6) & (f.n >= 40)
f.to_csv(os.path.join(O.OUT, "genel_aile.csv"), index=False)
L = pd.read_csv(os.path.join(lib.ROOT, "sonuclar", "leadlag_sweep.csv"))
L[L.target.isin(O.FAM)].to_csv(os.path.join(O.OUT, "leadlag_aile.csv"), index=False)
REP = ["USO", "UNG", "XLE", "OIH", "DBA", "CORN", "WEAT", "CANE"]
x = f[f.sym.isin(REP)].assign(both=lambda d: (d.is_net_bp > 0) & (d.oos_net_bp > 0))
k = ["sig", "mode", "h", "exit"]
a = x.groupby(k).agg(n_etf=("sym", "size"), pozitif_net=("mean_net_bp", lambda s: int((s > 0).sum())),
                     pozitif_kenar=("edge_bp", lambda s: int((s > 0).sum())), is_oos_pozitif=("both", "sum"),
                     ort_net_bp=("mean_net_bp", "mean"), t_toplam=("t", "sum")).reset_index()
a["stouffer_t"] = a["t_toplam"] / np.sqrt(a["n_etf"])
a = a.drop(columns="t_toplam").sort_values("stouffer_t", ascending=False)
a.to_csv(os.path.join(O.OUT, "aile_tutarlilik.csv"), index=False)
print(f"genel aile satırı {len(f)}; tek yönlü aile içi FDR geçen {int(f.fdr1_aile.sum())}; eşiği biçimsel geçen {int(f.esik.sum())}")
print(f[f.esik].sort_values("t", ascending=False)[["sym", "sig", "mode", "h", "exit", "n", "mean_net_bp", "t", "is_net_bp", "oos_net_bp", "years_pos_frac"]].round(2).to_string(index=False))
print("\nAile tutarlılığı (küme temsilcileri: " + ", ".join(REP) + ") ilk 10:")
print(a.head(10).round(2).to_string(index=False))
