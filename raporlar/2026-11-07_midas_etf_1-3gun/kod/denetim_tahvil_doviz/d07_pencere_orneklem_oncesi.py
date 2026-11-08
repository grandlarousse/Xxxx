"""DENETİM — komşu pencereler örneklem öncesinde (TLT 2002-2016, TBT 2008-2016; Yahoo) ve örneklemde (lib.load). python3 -I"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np, pandas as pd, lib
from d01_s1_yeniden import IDX, A10, OUT, tstat
from d03_s1_orneklem_oncesi import yahoo, AD, window
rows = []
for k1, k2 in ((5, 1), (4, 1), (3, 1), (3, 2), (2, 1), (3, 0)):
    for sym, lo in (("TLT", "2002-08-15"), ("TBT", "2008-06-01")):
        d = yahoo(sym); d = d[d.index < pd.Timestamp("2016-11-07")]
        r = window(d, AD[(AD > lo) & (AD < "2016-11-07")], k1, k2, "C0")
        dd = lib.load(sym); dd = dd.rename(columns={"c": "ac"})
        r2 = window(dd, A10[(A10 > "2016-11-12")], k1, k2, "C0")
        rows.append((f"A-{k1}->A{-k2:+d}", sym, len(r), r.mean() * 1e4, tstat(r), len(r2), r2.mean() * 1e4, tstat(r2)))
R = pd.DataFrame(rows, columns=["pencere", "sym", "n_once", "brut_once_bp", "t_once", "n_orneklem", "brut_orneklem_bp", "t_orneklem"])
print(R.round(2).to_string(index=False)); R.to_csv(os.path.join(OUT, "d07_pencere_once_sonra.csv"), index=False)
