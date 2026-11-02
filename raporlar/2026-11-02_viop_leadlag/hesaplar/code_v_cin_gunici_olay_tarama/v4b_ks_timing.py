"""TR1 ek: KS11/N225/TWII günlük etiket zamanlaması (h1 ile) + ES_{t-2} ve Asya ortak faktörü."""
import os, numpy as np, pandas as pd
from vcore import *
log = open(f"{OUT}/v4b_ks_timing.log", "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s); log.write(s + "\n")
for sym in ["^KS11", "^N225"]:
    h = bars(sym, "h1"); d = frame(sym)["c"]
    hl = h.groupby(pd.to_datetime(h["ldate"]))["c"].last()
    rd = np.log(d).diff(); rh = np.log(hl).diff()
    J = pd.concat([rd.rename("d"), rh.rename("h")], axis=1).dropna()
    P(f"{sym}: corr(günlük_t, h1 son-bar_t) {J.d.corr(J.h):.3f} | (günlük_t, h1_t-1) {J.d.corr(J.h.shift(1)):.3f} | (günlük_t, h1_t+1) {J.d.corr(J.h.shift(-1)):.3f} n {len(J)}")
c = cal(); x30 = decomp("XU030.IS"); y = x30["intra"]
es = ret("ES=F", "c"); ks = ret("^KS11", "c"); nk = ret("^N225", "c"); tw = ret("^TWII", "c"); ax = ret("^AXJO", "c") if os.path.exists(f"{D}/daily/^AXJO.parquet") else None
for lab, x in [("ES_{t-2}", es.shift(2)), ("ES_{t-1}", es.shift(1)), ("^GSPC_{t-2}", ret("^GSPC", "c").shift(2)), ("EEM_{t-2}", ret("EEM").shift(2)), ("AXJO_{t-1}", ax.shift(1) if ax is not None else None)]:
    if x is None: continue
    rows, yr, same, tot = full_report(y, x); P(f"  {lab:12s} {fmt(rows, yr, same, tot)}")
# Asya t-1 ortak faktörü: KS11, N225, TWII ortalaması; KS11'in ona göre artığı
A = pd.concat([ks.shift(1), nk.shift(1), tw.shift(1)], axis=1); A.columns = ["k", "n", "t"]
asia = A.mean(axis=1)
rows, yr, same, tot = full_report(y, asia); P(f"  Asya-3 ort._{{t-1}} {fmt(rows, yr, same, tot)}")
rows, yr, same, tot = full_report(y, ks.shift(1), A[["n", "t"]]); P(f"  KS11_{{t-1}} | N225,TWII_{{t-1}} {fmt(rows, yr, same, tot)}")
rows, yr, same, tot = full_report(y, ks.shift(1), pd.concat([es.shift(2).rename("e2"), es.shift(1).rename("e1")], axis=1)); P(f"  KS11_{{t-1}} | ES_{{t-1,t-2}} {fmt(rows, yr, same, tot)}")
# KS11_{t-1} -> XU030 gün-içi: ilk saat vs gün geri kalanı (h1, 2023-12+)
sn = snap("XU030.IS", ["07:30", "08:30", "15:10"])
d = frame("XU030.IS")
o = d["o"].reindex(sn.index)
p1 = np.log(sn["08:30"] / o).reindex(c); rest = np.log(d["c"].reindex(sn.index) / sn["08:30"]).reindex(c)
for lab, tg in [("açılış->08:30", p1), ("08:30->kapanış", rest), ("açılış->kapanış (aynı dönem)", y.loc["2023-12":])]:
    r = pc(tg, ks.shift(1), None, ("2023-12-01", "2026-12-31")); P(f"  h1 dönemi KS11_{{t-1}} -> XU030 {lab}: r {r['r']:+.3f} t {r['t']:.2f} n {r['n']}")
log.close()
