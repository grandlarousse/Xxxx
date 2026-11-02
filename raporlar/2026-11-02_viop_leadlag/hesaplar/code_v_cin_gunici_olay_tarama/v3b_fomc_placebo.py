"""V2 ek: gap~ES_{t-1} betası haftanın gününe göre; FOMC-dışı Çarşamba plasebosu; ES ayrık gece (h1) ile FOMC."""
import numpy as np, pandas as pd
from vcore import *
exec(open("v3_olay.py").read().split("# ---------------- V3")[0].split("log = open")[0])
c = cal()
MYs = open("v3_olay.py").read().split('MY = """')[1].split('"""')[0].split()
MY = pd.DatetimeIndex(MYs)
react = pd.DatetimeIndex([c[c.searchsorted(d, side="right")] for d in MY])
es = ret("ES=F", "c"); es_l = es.shift(1); g = decomp("XU100.IS")
isF = c.isin(react)
out = open(f"{OUT}/v3b_fomc_placebo.log", "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s); out.write(s + "\n")
df = pd.DataFrame({"y": g.gap, "x": es_l, "F": isF, "wd": c.weekday, "yr": c.year}, index=c).loc["2014":].dropna()
gapdays = pd.Series(c[1:] - c[:-1], index=c[1:]).dt.days.reindex(df.index)
df["cons"] = gapdays.values == 1  # önceki BIST günü dün mü (tatil/hafta sonu değil)
for wd in range(5):
    for lab, m in [("tümü", df.wd == wd), ("FOMC-dışı", (df.wd == wd) & ~df.F), ("ardışık+FOMC-dışı", (df.wd == wd) & ~df.F & df.cons)]:
        d = df[m]; b, t, _ = hc_t(d.y, d.x); P(f"tepki günü {['Pzt','Sal','Çar','Per','Cum'][wd]} {lab:18s} β {b:.3f} r {d.y.corr(d.x):.3f} t {t:.2f} n {len(d)}")
d = df[df.F]; b, t, _ = hc_t(d.y, d.x); P(f"FOMC tepki günleri β {b:.3f} r {d.y.corr(d.x):.3f} n {len(d)}  (hafta günü dağılımı {d.wd.value_counts().to_dict()})")
# Perşembe (Çarşamba gecesi) FOMC-dışı vs FOMC: fark testi
m = (df.wd == 3)
d = df[m].copy(); d["xf"] = d.x * d.F
X = np.column_stack([np.ones(len(d)), d.x, d.F.astype(float), d.xf]); bb = np.linalg.lstsq(X, d.y, rcond=None)[0]; e = d.y - X @ bb
XtXi = np.linalg.inv(X.T @ X); V = XtXi @ (X.T * e.values ** 2) @ X @ XtXi
P(f"Perşembe tepki günleri içinde FOMC farkı: Δβ {bb[3]:.3f} tHC {bb[3]/np.sqrt(V[3,3]):.2f}")
# Pazartesi (hafta sonu) betası düşükse 'normal' ortalamayı aşağı çeker
P("tüm günler β (Pzt hariç, FOMC-dışı):", round(hc_t(df[(df.wd != 0) & ~df.F].y, df[(df.wd != 0) & ~df.F].x)[0], 3))
# yıllar: Perşembe FOMC-dışı β
P("yıllara göre Per FOMC-dışı β:", {yr: round(hc_t(df[(df.wd == 3) & ~df.F & (df.yr == yr)].y, df[(df.wd == 3) & ~df.F & (df.yr == yr)].x)[0], 2) for yr in range(2014, 2027)})
# IS/OOS
for w, (a, b_) in [("IS", WIN["IS"]), ("OOS", WIN["OOS"])]:
    d = df.loc[a:b_]
    for lab, m in [("FOMC", d.F), ("Per FOMC-dışı", (d.wd == 3) & ~d.F), ("diğer tümü", ~d.F)]:
        dd = d[m]; P(f"  {w} {lab:14s} β {hc_t(dd.y, dd.x)[0]:.3f} r {dd.y.corr(dd.x):.3f} n {len(dd)}")
out.close()
# |gap| FOMC tepki günleri vs FOMC-dışı Perşembe
out = open(f"{OUT}/v3b_fomc_placebo.log", "a")
for w, (a, b_) in [("tam", WIN["tam"]), ("IS", WIN["IS"]), ("OOS", WIN["OOS"])]:
    d = df.loc[a:b_]
    fa = d[d.F].y.abs(); th = d[(d.wd == 3) & ~d.F].y.abs(); al = d[~d.F].y.abs()
    from scipy import stats
    u = stats.mannwhitneyu(fa, th, alternative="greater")
    P(f"|gap| {w}: FOMC ort {fa.mean()*1e4:.0f} bps medyan {fa.median()*1e4:.0f} | Per FOMC-dışı ort {th.mean()*1e4:.0f} medyan {th.median()*1e4:.0f} | tüm diğer ort {al.mean()*1e4:.0f} medyan {al.median()*1e4:.0f} | oran(FOMC/Per) {fa.mean()/th.mean():.2f} MW p {u.pvalue:.3f}")
out.close()
