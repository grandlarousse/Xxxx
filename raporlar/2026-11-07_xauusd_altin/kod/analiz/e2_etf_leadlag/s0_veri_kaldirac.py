"""s0: veri kontrolü, buy&hold, ters/kaldıraçlı ETF'lerin 1/3/5 günlük gerçekleşen kaldıracı ve aşınması."""
from e2_common import *
d = load()
rows = []
for und in TARGETS + ["SIL"]:
    r = ret_of(d, und)
    for nm, s, e in [("full", None, None), ("is", None, "2017-12-31"), ("oos", "2018-01-01", None), ("2022+", "2022-01-01", None)]:
        rr = r.copy()
        if s: rr = rr[rr.index >= s]
        if e: rr = rr[rr.index <= e]
        rr = rr.dropna()
        rows.append(dict(etf=und, period=nm, n=len(rr), start=str(rr.index.min().date()), ann_ret=round(rr.mean()*252*100, 2), ann_vol=round(rr.std()*np.sqrt(252)*100, 2),
                         sharpe=round(rr.mean()/rr.std()*np.sqrt(252), 2)))
bh = pd.DataFrame(rows); bh.to_csv(f"{OUT}/s0_buyhold.csv", index=False); print(bh.to_string())
lev = []
for inv, und, Lnom in [("GLL", "GLD", -2), ("UGL", "GLD", 2), ("DUST", "GDX", None), ("NUGT", "GDX", None), ("JDST", "GDXJ", None), ("JNUG", "GDXJ", None), ("ZSL", "SLV", -2), ("AGQ", "SLV", 2), ("GDXU", "GDX", 3)]:
    if f"c_{inv}" not in d: continue
    for nm, s, e in [("2008-2019", None, "2020-03-31"), ("2020-04+", "2020-04-01", None), ("2022+", "2022-01-01", None)]:
        for h in (1, 3, 5):
            b, c, n = realized_lev(d, inv, und, h, s, e)
            # aşınma: ters ETF yıllık log getiri - b * dayanak yıllık log getiri
            ci = np.log(d[f"c_{inv}"]); cu = np.log(d[f"c_{und}"])
            if s: ci = ci[ci.index >= s]; cu = cu[cu.index >= s]
            if e: ci = ci[ci.index <= e]; cu = cu[cu.index <= e]
            ri = ci.diff(); ru = cu.diff(); m = ri.notna() & ru.notna()
            drag = (ri[m].mean() - b * ru[m].mean()) * 252 if np.isfinite(b) else np.nan
            lev.append(dict(inv=inv, und=und, period=nm, h=h, beta=round(b, 3) if np.isfinite(b) else np.nan, corr=round(c, 3) if np.isfinite(c) else np.nan, n=n,
                            ann_drag_pct=round(drag*100, 2) if np.isfinite(drag) else np.nan))
lev = pd.DataFrame(lev); lev.to_csv(f"{OUT}/s0_kaldirac.csv", index=False); print(lev.to_string())
# bilgi zamanı denetimi: y_*_avail < cut_utc her gün
cut = pd.to_datetime(d["cut_utc"])
viol = {}
for c in [c for c in d.columns if c.endswith("_avail")]:
    a = pd.to_datetime(d[c], utc=True)
    v = int((a >= cut).sum()); viol[c] = v
print("avail ihlali (olmalı 0):", {k: v for k, v in viol.items() if v > 0})
json.dump(viol, open(f"{OUT}/s0_avail_ihlal.json", "w"))
