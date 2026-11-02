"""V2 ek: h1 ile kesin gece penceresi (15:00->07:00 UTC ES) — FOMC gecesi β vs diğer; ve ES günlük getirisinin kapanış-sonrası payı haftanın gününe göre."""
import numpy as np, pandas as pd
from vcore import *
c = cal(); c = c[c >= "2024-06-01"]
prev = pd.Series(c[:-1], index=c[1:])
sn = snap("ES=F", ["15:00", "07:00", "21:00"])
ESn = pd.Series(np.log(sn["07:00"].reindex(prev.index).values / sn["15:00"].reindex(prev.values).values), index=prev.index)
g = decomp("XU100.IS").reindex(prev.index)
MY = pd.DatetimeIndex(open("v3_olay.py").read().split('MY = """')[1].split('"""')[0].split())
cc = cal(); react = pd.DatetimeIndex([cc[cc.searchsorted(d, side="right")] for d in MY])
df = pd.DataFrame({"y": g.gap, "x": ESn, "F": prev.index.isin(react), "wd": prev.index.weekday}).dropna()
out = open(f"{OUT}/v3c_fomc_h1.log", "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s); out.write(s + "\n")
for lab, m in [("FOMC", df.F), ("diğer", ~df.F), ("Per FOMC-dışı", (df.wd == 3) & ~df.F)]:
    d = df[m]; b, t, _ = hc_t(d.y, d.x); P(f"XU100 gap ~ ES(15->07 h1) {lab:14s} β {b:.3f} r {d.y.corr(d.x):.3f} tHC {t:.2f} n {len(d)}")
P("|ES gece| ort. (bps): FOMC", round(df[df.F].x.abs().mean() * 1e4), "diğer", round(df[~df.F].x.abs().mean() * 1e4))
# günlük ES getirisinde kapanış sonrası (15->21 UTC) payı, haftanın gününe göre
es = ret("ES=F", "c")
post = np.log(sn["21:00"] / sn["15:00"])
d2 = pd.DataFrame({"post": post, "full": es.reindex(post.index)}).dropna()
d2["wd"] = d2.index.weekday
P("ES günlük getiri varyansında 15->21 UTC payı (2024-06+), gün:", {wd: round(np.var(g_.post) / np.var(g_.full), 2) for wd, g_ in d2.groupby("wd")})
P("cov(post, full)/var(full) (regresyon payı):", {wd: round(np.cov(g_.post, g_.full)[0, 1] / np.var(g_.full, ddof=1), 2) for wd, g_ in d2.groupby("wd")})
out.close()
