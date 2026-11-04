"""FOMC/NFP/CPI risk iddiası ve akşam seansı (ES) iddiasının hızlı bağımsız kontrolü."""
import numpy as np, pandas as pd, cl, ev, hsnap
o = pd.read_csv(cl.S + "/out/olay_tarihleri.csv"); o["date"] = pd.to_datetime(o["date"])
c = cl.cal(); r = ev.R("XU030"); pos = pd.Series(np.arange(len(c)), index=c)
fomc = o[(o["type"] == "FOMC") & (o["timing"] == "after_close")]["date"]
cpi = o[(o["type"] == "USDATA") & (o["sub"] == "CPI")]["date"]; nfp = o[(o["type"] == "USDATA") & (o["sub"] == "NFP")]["date"]
rng = np.random.default_rng(5)
def entries(dates, kind):
    out = []
    for d in dates:
        k = np.searchsorted(c.values, np.datetime64(d), side="right" if kind == "after" else "left") - 1
        if k >= 0: out.append(c[k])
    return pd.DatetimeIndex(sorted(set(out)))
for nm, dates, kind in (("FOMC", fomc, "after"), ("NFP(2023-12+)", nfp, "in"), ("CPI(2023-12+)", cpi, "in")):
    ent = entries(dates, kind)
    for h in (1, 2, 3):
        y = cl.fwd(r, h).dropna() * 1e4; st = "2023-12-01" if "2023" in nm else "2017-03-06"; y = y[y.index >= st]
        e = y.reindex(ent).dropna(); oth = y.drop(e.index, errors="ignore")
        ratio = e.std() / oth.std()
        bs = np.array([oth.sample(len(e), random_state=int(rng.integers(1e9))).std() / oth.std() for _ in range(2000)])
        print(nm, "h", h, "n", len(e), "std oranı", round(ratio, 2), "bootstrap p(>=)", round((bs >= ratio).mean(), 3), "ort olay", round(e.mean(), 1), "t", round(cl.tstat(e), 2),
              "IS(<2022)", round(e[e.index < "2022"].mean(), 1), "OOS", round(e[e.index >= "2022"].mean(), 1))
# Akşam seansı: ES 15:00->20:00 UTC hareketi ile ertesi uzlaşma getirisi
es15 = hsnap.snap_h("ES=F", 15, 0); es20 = hsnap.snap_h("ES=F", 20, 0)
eve = np.log(es20 / es15).reindex(c)
y1 = r.shift(-1)
df = pd.concat([eve.rename("eve"), y1.rename("y1")], axis=1).dropna(); df = df[df.index >= "2024-06-15"]
b = np.polyfit(df["eve"], df["y1"], 1); R2 = np.corrcoef(df["eve"], df["y1"])[0, 1] ** 2
print("akşam ES (15->20 UTC) -> ertesi XU030 uzlaşma getirisi: n", len(df), "beta", round(b[0], 3), "R2", round(R2, 3))
