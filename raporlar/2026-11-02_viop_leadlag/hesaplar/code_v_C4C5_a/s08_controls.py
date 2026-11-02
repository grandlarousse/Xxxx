"""Adim 8: kontrollu regresyonlar (brief tuzak 3): hedefin kendi gecikmesi, XU100 gecikmesi, acilis gap'i.
 KRDMD oc_t ~ SHFE HC (FULL/GAPD/OCD) + KRDMD cc_{t-1} + XU100 cc_{t-1} + KRDMD gap_t + XU100 intra_{t-1}
 TRALT oc_t ~ 600547.SS CLOSE / 1787.HK CLOSE + ayni kontroller."""
import sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_C4C5_a")
import vlib as V, numpy as np, pandas as pd
from s02_hk_timing import signals, C, TR, XU
KR = V.bist_daily("KRDMD.IS"); HC = V.shfe_main("HC"); HC = HC[HC.index.isin(C)]
z = lambda s: (s - s.mean()) / s.std()
def reg(lab, y, sig, own, start):
    D = pd.concat([y.rename("y"), sig.rename("sig"), own["cc"].shift(1).rename("own_cc1"), XU["cc"].shift(1).rename("xu_cc1"), own["gap"].rename("own_gap"),
                   XU["intra"].shift(1).rename("xu_oc1"), own["intra"].shift(1).rename("own_oc1")], axis=1).dropna()
    D = D[D.index >= start]
    for spec in [["sig"], ["sig", "own_cc1", "xu_cc1"], ["sig", "own_cc1", "xu_cc1", "own_gap"], ["sig", "own_oc1", "xu_oc1", "own_gap", "xu_cc1"]]:
        p, t, n = V.nw(z(D.y), pd.DataFrame({c: z(D[c]) for c in spec}))
        print(f"{lab:34s} [{'+'.join(spec):38s}] n={n} " + " ".join(f"{c}={p[c]:+.3f}({t[c]:+.2f})" for c in spec))
    for a, b in [("2018-11-28", "2020-12-31"), ("2021-01-01", "2023-12-31"), ("2024-01-01", "2026-12-31")]:
        g = D[(D.index >= a) & (D.index <= b)]
        if len(g) < 60: continue
        p, t, n = V.nw(z(g.y), pd.DataFrame({c: z(g[c]) for c in ["sig", "own_cc1", "xu_cc1", "own_gap"]}))
        print(f"   alt-donem {a[:4]}-{b[:4]}: n={n} sig={p['sig']:+.3f}(t={t['sig']:+.2f})")
reg("KRDMD oc ~ HC FULL(taze)", KR["intra"], HC["r_cc"], KR, "2018-11-28")
reg("KRDMD oc ~ HC GAPD", KR["intra"], HC["r_gap"], KR, "2018-11-28")
reg("KRDMD oc ~ HC OCD", KR["intra"], HC["r_oc"], KR, "2018-11-28")
S1 = signals("1787.HK"); S3 = signals("600547.SS")
reg("TRALT oc ~ 1787.HK CLOSE", TR["intra"], S1["CLOSE"], TR, "2018-10-01")
reg("TRALT oc ~ 600547.SS CLOSE", TR["intra"], S3["CLOSE"], TR, "2014-01-01")
reg("TRALT oc ~ 1787.HK OPEN", TR["intra"], S1["OPEN"], TR, "2018-10-01")
