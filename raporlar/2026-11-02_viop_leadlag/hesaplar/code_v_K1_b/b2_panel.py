"""47 hisse paneli: günlük gap/intra + saatlik 10:30, 11:30, 17:30 fiyatları + likidite rankı. -> panel_b.parquet"""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_K1_b")
from kb import *
def tick(p):
    return np.select([p < 20, p < 50, p < 100, p < 250, p < 500, p < 1000, p < 2500], [0.01, 0.02, 0.05, 0.10, 0.25, 0.50, 1.00], 2.50)
fr = []; chk = []
for s in VIOP:
    d = daily(s)
    d["sym"] = s
    d["liq60"] = d.tlv_raw.rolling(60, min_periods=40).median().shift(1)
    h = h1(s)
    if h is not None:
        f = h[h.hm == 630].set_index("day"); f2 = h[h.hm == 730].set_index("day"); f3 = h[h.hm == 1330].set_index("day")
        d["h1_o"] = f.o.reindex(d.index); d["p1030"] = f.c.reindex(d.index)
        d["p1130"] = f2.c.reindex(d.index); d["p1730"] = f3.c.reindex(d.index)
        okh = (d.h1_o / d.o - 1).abs() < 0.002
        inrng = (d.p1030 <= d.h * 1.001) & (d.p1030 >= d.l * 0.999) & (d.p1130 <= d.h * 1.001) & (d.p1130 >= d.l * 0.999)
        chk.append(dict(sym=s, n_h1=int(d.h1_o.notna().sum()), open_match=round(okh[d.h1_o.notna()].mean(), 4), inrange=round(inrng[d.h1_o.notna()].mean(), 4)))
        bad = ~(okh & inrng)
        d.loc[bad, ["p1030", "p1130", "p1730"]] = np.nan
        d.loc[~((d.p1730 <= d.h * 1.001) & (d.p1730 >= d.l * 0.999)), "p1730"] = np.nan
    d["r1"] = np.log(d.p1030 / d.o) if "p1030" in d else np.nan
    d["r2"] = np.log(d.c / d.p1030) if "p1030" in d else np.nan
    d["r12"] = np.log(d.p1130 / d.p1030) if "p1030" in d else np.nan
    d["r3"] = np.log(d.c / d.p1130) if "p1130" in d else np.nan
    d["r2x"] = np.log(d.p1730 / d.p1030) if "p1730" in d else np.nan
    d["reltick"] = tick(d.c) / d.c * 1e4
    fr.append(d.reset_index().rename(columns={"index": "date"}))
P = pd.concat(fr, ignore_index=True)
P["liqrank"] = P.groupby("date").liq60.rank(pct=True)
P["liqT"] = pd.cut(P.liqrank, [0, 1/3, 2/3, 1.0001], labels=["dusuk", "orta", "yuksek"])
P.to_parquet(OUT + "/panel_b.parquet")
C = pd.DataFrame(chk); print(C.describe().round(4).to_string()); print(C.sort_values("open_match").head(8).to_string())
