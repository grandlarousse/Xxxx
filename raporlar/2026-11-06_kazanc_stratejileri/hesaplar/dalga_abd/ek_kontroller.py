"""7) Ek kontroller: t-istatistikleri, kayan 5 yillik fark, guncel momentum siralamasi (2026-09 sonu),
swing kurallarinda maliyet stresi, GSY canli olaylar icin piyasa kosusu karsilastirmasi."""
import os
import numpy as np
import pandas as pd
from dalga_tanim import base_data, OUT
from kurallar import rotation, perf

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 40)

R, RM, RF, m = base_data()
rot = pd.read_pickle(os.path.join(OUT, "rot_series.pkl"))
rsb = pd.read_pickle(os.path.join(OUT, "rsb_series.pkl"))

def tstat(s, b):
    x = (s - b).dropna()
    return x.mean() / x.std() * np.sqrt(len(x)), x.mean() * 12

print("== Aylik fark t-istatistigi (kural - piyasa), aylik ortalama fark x12 ==")
for k in ["B_L12s0_k3_plain", "C_L12s0_k3_abs", "B_L6s0_k5_plain", "B_L3s0_k5_plain", "D_L6s1_k10_buf", "B_L1s0_k10_plain"]:
    s = rot[k][0]
    out = []
    for p0, p1 in (("1930", "2026"), ("1930", "1999"), ("2000", "2026"), ("2015", "2026")):
        t, a = tstat(s.loc[p0:p1], RM.loc[p0:p1])
        out.append(f"{p0}-{p1}: {a*100:+.1f}%/y t={t:.2f}")
    print(k, " | ".join(out))
for k in ["A_N12_trail15_none", "A_N6_time12_none", "A_N12_time12_none"]:
    s = rsb[k][1]
    out = []
    for p0, p1 in (("1930", "2026"), ("1930", "1999"), ("2000", "2026"), ("2015", "2026")):
        t, a = tstat(s.loc[p0:p1], RM.loc[p0:p1])
        out.append(f"{p0}-{p1}: {a*100:+.1f}%/y t={t:.2f}")
    print(k, " | ".join(out))

# kayan 60 ay fark (B_L12s0_k3)
s = rot["B_L12s0_k3_plain"][0]
ex = np.log1p(s) - np.log1p(RM)
roll = ex.rolling(60).sum() / 5
print("\nB_L12s0_k3: kayan 5y yillik log fark < 0 olan ay orani (1935+):", round((roll.loc["1935":] < 0).mean(), 3),
      " 2000+:", round((roll.loc["2000":] < 0).mean(), 3), " son deger:", round(roll.iloc[-1], 3))
# B_L12s0_k3 icin en kotu 12 aylik fark donemleri
r12 = ex.rolling(12).sum()
print("en kotu 12 ay fark:", round(np.expm1(r12.min()), 3), r12.idxmin(), " 2015+ en kotu:", round(np.expm1(r12.loc["2015":].min()), 3), r12.loc["2015":].idxmin())

# ---- Guncel siralama (2026-09 sonu itibariyla, Ekim icin sinyal)
lr = np.log1p(R)
rows = {}
for L in (1, 3, 6, 12):
    rows[f"m{L}"] = np.expm1(lr.iloc[-L:].sum())
X = pd.DataFrame(rows)
lrel = lr.sub(np.log1p(RM), axis=0).cumsum()
X["rs_12m_high"] = lrel.iloc[-1] >= lrel.iloc[-13:-1].max(axis=0)
X["rs_6m_high"] = lrel.iloc[-1] >= lrel.iloc[-7:-1].max(axis=0)
X["rs_vs_12m_max"] = np.expm1(lrel.iloc[-1] - lrel.iloc[-13:].max())
for L in (3, 6, 12):
    X[f"rank{L}"] = X[f"m{L}"].rank(ascending=False).astype(int)
print("\n== 2026-09 sonu: 12 ay momentuma gore ilk 12 sektor ==")
print(X.sort_values("m12", ascending=False).head(12).round(3).to_string())
print("\n== 6 ay momentum ilk 8 ==")
print(X.sort_values("m6", ascending=False).head(8)[["m6", "m3", "m1", "rank12", "rs_6m_high"]].round(3).to_string())
print("\nSon 12 ayin tutulan sektorleri (B_L12s0_k3):")
W = rot["B_L12s0_k3_plain"][1]
for t in W.index[-13:-1]:
    print(t, list(W.columns[W.loc[t] > 0]))
W5 = rot["B_L6s0_k5_plain"][1]
print("B_L6s0_k5 son agirliklar:", W5.index[-2], list(W5.columns[W5.iloc[-2] > 0]))

# ---- Piyasa 24 ay kosusu (GSY'de en guclu cokus belirteci)
M24 = np.expm1(np.log1p(RM).rolling(24).sum())
E = pd.read_pickle(os.path.join(OUT, "gsy_events.pkl"))
print("\nPiyasa 24 ay getirisi 2026-09:", round(M24.iloc[-1], 3), " olaylarin medyani:", round(E.mkt24.median(), 3),
      " tum aylar yuzdeligi:", round((M24.dropna() < M24.iloc[-1]).mean(), 3))

# ---- Swing maliyet stresi (temsilci kurallar)
from swing_haftalik import run, port, pstats
for N, ek, X_, H in [(52, "rstrail", 0.10, 0), (52, "time", 0, 13), (26, "pxtrail", 0.12, 0)]:
    for c in (0.001, 0.0025):
        tr = run(N=N, exit_kind=ek, X=X_, H=H, c=c)
        p, n = port(tr, c=c)
        tr15 = tr[tr.entry >= "2015-01-01"]
        print(f"swing N{N} {ek}{X_ or H} c={c}: islem/yil={len(tr)/98:.1f} ort rel={tr.rel_net.mean():+.4f} 2015+ ort rel={tr15.rel_net.mean():+.4f} "
              f"CAGR31={pstats(p,'1931')['cagr']:.3f} CAGR15={pstats(p,'2015')['cagr']:.3f}")
