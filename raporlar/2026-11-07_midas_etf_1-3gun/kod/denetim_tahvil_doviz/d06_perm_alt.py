"""DENETİM — ay+haftanın günü eşlenik permütasyonu IS/OOS ayrı ve yalnız A-3=Cuma işlemleri (TMV brüt, C0 h=2). python3 -I"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np, pandas as pd, lib
from d01_s1_yeniden import IDX, A10, sim
rng = np.random.default_rng(7)
c = lib.load("TMV").reindex(IDX)["c"].values; r2 = np.r_[c[2:] / c[:-2] - 1, [np.nan, np.nan]]
t = sim("TMV", A10, 3, 1, "C0"); sp = IDX.get_indexer(t.sig_date)
ym = IDX.year * 100 + IDX.month; dow = IDX.dayofweek; ar = np.arange(len(IDX))
for lab, m in (("IS", t.sig_date <= "2021-12-31"), ("OOS", t.sig_date > "2021-12-31"), ("A-3=Cuma", dow[sp] == 4), ("A-3=Per/Çar", dow[sp] != 4)):
    s = sp[np.asarray(m)]; obs = np.nanmean(r2[s])
    pools = [np.where((ym == ym[q]) & (dow == dow[q]) & (np.abs(ar - q) > 2) & np.isfinite(r2))[0] for q in s]
    sims = np.array([np.nanmean(r2[[rng.choice(p) for p in pools]]) for _ in range(5000)])
    print(f"{lab:12s} n={len(s):3d} TMV brüt {obs*1e4:6.1f} bp | eşlenik sim ort {sims.mean()*1e4:6.1f} bp | p={(np.sum(sims>=obs)+1)/5001:.4f}")
