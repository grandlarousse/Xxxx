"""A4: m5 (son ~60 gün) ile açılış/kapanış müzayedesi kontrolü. Günlük o == m5 06:55 barı kapanışı mı? Gün-içi kaymanın
müzayede (14:55 c -> günlük kapanış) ve ilk 5/30 dk payı. Kısa örneklem: sadece artefakt kontrolü amaçlı."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_G3_a")
from vcommon import *
import warnings; warnings.filterwarnings("ignore")
rows = []; segs = {}
for sym in ["XU030.IS", "XU100.IS"] + [s + ".IS" for s in STOCKS]:
    try:
        m = pd.read_parquet(f"{D}/m5/{sym}.parquet").copy()
    except Exception: continue
    m["ldate"] = pd.to_datetime(m["ldate"]).dt.normalize(); m["hm"] = m.index.strftime("%H:%M")
    dd = decomp(sym, start="2026-07-01")
    pv = m.pivot_table(index="ldate", columns="hm", values="c", aggfunc="last")
    if "06:55" not in pv or "14:55" not in pv: continue
    X = pd.DataFrame({"o": dd.o, "c": dd.c, "intra": dd.intra}).join(pv[["06:55", "07:00", "07:25", "14:55"]], how="inner").dropna()
    rows.append(dict(sym=sym, n=len(X), o_eq_0655c=(np.abs(X.o / X["06:55"] - 1) < 2e-4).mean(),
                     first5=1e4 * np.log(X["07:00"] / X.o).mean(), o_0730=1e4 * np.log(X["07:25"] / X.o).mean(),
                     cont=1e4 * np.log(X["14:55"] / X["07:25"]).mean(), auction=1e4 * np.log(X.c / X["14:55"]).mean(), intra=1e4 * X.intra.mean()))
A = pd.DataFrame(rows).set_index("sym"); print(A.loc[["XU030.IS", "XU100.IS"]].round(2).to_string())
s = A.drop(["XU030.IS", "XU100.IS"]); print("47 hisse medyan:", s.median().round(2).to_dict())
A.to_csv(S + "/out/code_v_G3_a/res/a4_m5.csv")
