"""v3b: JETS kontrolünde AIR t düşüşü: örneklem mi, eşdoğrusallık mı? + bacak bacak."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_A4_b")
from core import *
SG = pd.read_parquet(RES + "/signals.parquet"); AIR = SG.AIR_C
X1 = bist_day("XU100.IS")
J = to_bist(ret_own("JETS")); zJ = to_bist(zs(ret_own("JETS")).clip(-3, 3))
SPX = to_bist(ret_own("^GSPC"))
US_raw = sector_signal([], US_AIR, resid=False)["US"]
for st in ["THYAO", "PGSUS", "TAVHL"]:
    d = bist_day(st + ".IS"); y = d.intra[d.index >= "2015-06-01"]
    M = pd.DataFrame({"AIR": AIR, "zEU": SG.zEU_C, "zUS": SG.zUS_C, "JETS": J, "SPX": SPX, "zUSraw": US_raw, "own_gap": d.gap, "XU_cc": X1.cc.shift(1)})
    for cols in [["AIR"], ["AIR", "JETS"], ["zEU", "zUS"], ["zEU", "zUS", "JETS"], ["zEU", "JETS"], ["zEU", "zUSraw"], ["JETS"], ["zUSraw"], ["zUS"], ["zEU"], ["zEU", "JETS", "SPX"]]:
        r, n = ols_nw(y, M[cols])
        print(st, "2015-06+", cols, " | ".join(f"{c} {r.loc[c,'coef']:.3f} (t {r.loc[c,'t']:.2f})" for c in cols), "n", n)
    # backtest: JETS z yerine
    for nm, s in [("AIR", AIR), ("zEU+zJETS", SG.zEU_C + zJ), ("zEU+zUSraw", SG.zEU_C + US_raw), ("zEU_only", SG.zEU_C), ("zUS_only", SG.zUS_C)]:
        r = bt_periods(s, d.intra, 8, 1.0, ("IS", "OOS", "ALL"))
        print("   bt", nm, {p: (round(r[p]["bps"], 1), round(r[p]["t"], 2)) for p in r})
