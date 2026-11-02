"""Adim 9: h1 orneklemi (HK 2024-09+) on-acilis varyantlarinin backtest t'si ve baslangic tarihi duyarliligi."""
import sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_C4C5_a")
import vlib as V, numpy as np, pandas as pd
from s02_hk_timing import signals, TR
for sym in ["1787.HK", "2899.HK"]:
    S = signals(sym)
    for st in ["2024-08-01", "2024-09-01", "2024-11-01", "2025-01-01"]:
        for sc in ["CLOSE", "P0400", "P0630", "OPEN"]:
            df = pd.concat([S[sc].rename("s"), TR["intra"].rename("y")], axis=1).dropna(); df = df[df.index >= st]
            if sc != "CLOSE" and sc != "OPEN": pass
            c, t, n = V.zt(df.y, df.s)
            out = []
            for cost in [8, 10, 15]:
                r, _ = V.bt(df.s, df.y, cost); out.append(f"c{cost}: {r['ALL']['mean_bps']:+.1f}bps sh{r['ALL']['sharpe']:+.2f} t{r['ALL']['t']:+.2f}")
            print(f"{sym} {st} {sc:6s} n={n} corr={c:+.3f} t={t:+.2f} | " + " | ".join(out))
