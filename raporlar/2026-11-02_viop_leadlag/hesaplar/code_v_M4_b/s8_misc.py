"""s8: (a) FMG.AX tek basina ham getiri korelasyonu (kendi takvim / ffill) (b) gun-ici drift'ten arindirilmis alfa (c) TR kriz/olay gunleri haric."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vb, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
c = vb.cal()
for lab, f in [("kendi-takvim", lambda: vb.dret("FMG.AX").reindex(c)), ("ffill", lambda: vb.dret_ffill("FMG.AX"))]:
    x = f()
    for s in ["KRDMD.IS", "EREGL.IS", "BRSAN.IS"]:
        y = vb.bist(s).intra
        out = [lab, s]
        for a, e in [("2014", "2027"), ("2014", "2021"), ("2021", "2027"), ("2024", "2027")]:
            m = (x.index >= a) & (x.index < e); r, t, n = vb.corr_t(x[m], y); out += [f"{a}-{e}: r {r:.3f} t {t:.2f}"]
        print(" | ".join(out))
cA, _ = vb.comp(vb.JP_AU)
ev = pd.read_csv(os.path.join(vb.SCR, "out", "olay_tarihleri.csv"))
dcol = [k for k in ev.columns if "tarih" in k.lower() or "date" in k.lower()][0]
evd = pd.to_datetime(ev[dcol], errors="coerce").dropna()
excl = set()
for d in evd:
    i = c.searchsorted(d)
    for j in range(max(0, i - 1), min(len(c), i + 6)): excl.add(c[j])
print("olay sayisi", len(evd), "haric gun", len(excl))
for s in ["EREGL.IS", "KRDMD.IS", "BRSAN.IS"]:
    b = vb.bist(s)
    o = vb.bt(cA, b.intra)
    drift = b.intra.rolling(250, min_periods=60).mean().shift(1)
    o2 = vb.bt(cA, (b.intra - drift))
    o3 = o[~o.index.isin(excl)]
    for lab, oo in [("ham", o), ("drift-arindirilmis", o2), ("olay[-1,+5] haric", o3)]:
        r = vb.isoos(oo); print(s, lab, {k: round(v, 2) for k, v in r.items() if k[-3:] in ("bps", "_t") or k.endswith("_n")})
