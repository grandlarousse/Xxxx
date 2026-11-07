"""T02: (a) Birincil ailenin en iyi ekonomik adayi MedEq<-Hlth (L5,h5) icin SONRADAN yapilan
komsu-parametre ve yil-yil saglamlik (FDR'den gecmedi; burada yalniz 'filtre mi?' sorusu).
(b) Onceden belirlenmis tek test: Insur artigi, Atlantik kasirga zirvesi (Agu-Eki) vs Kas-Oca.
"""
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
import ortak as o
from t01_endustri_leadlag import RES, BETA, d, target_y, signal, win, T0, T1, IS_END, OOS_START

out = []
print("(a) MedEq <- Hlth komsu parametreler (varyant B = 1 gun atlamali)")
for L, h in [(3, 3), (3, 5), (5, 3), (5, 5), (5, 10), (10, 5), (10, 10), (20, 10)]:
    z = signal("Hlth", "MedEq", L)
    for var, skip in (("A", 0), ("B", 1)):
        y = target_y("MedEq", h, skip)
        r = dict(L=L, h=h, var=var)
        for per, a, b in (("tam", T0, T1), ("IS", T0, IS_END), ("OOS", OOS_START, T1)):
            bb, tt, pp, n = o.hac_ols(win(y, a, b), win(z, a, b), h + L + skip)
            r[per + "_b"] = bb; r[per + "_t"] = tt
        out.append(r)
R = pd.DataFrame(out)
print(R.round(2).to_string(index=False))
R.to_csv(f"{o.CIKTI}/t02_medeq_hlth_komsu.csv", index=False, float_format="%.4g")

# yil-yil (L5,h5, B)
z = signal("Hlth", "MedEq", 5); y = target_y("MedEq", 5, 1)
dd = pd.concat([z, y], axis=1).dropna(); dd.columns = ["z", "y"]
dd = dd[(dd.index >= T0) & (dd.index <= T1)]
yy = dd.groupby(dd.index.year).apply(lambda g: np.polyfit(g["z"], g["y"], 1)[0])
print("\nYil-yil egim (bps/sigma, B):", yy.round(1).to_dict())
print("pozitif yil:", int((yy > 0).sum()), "/", len(yy))
# kuyruk tablosu (tam donem, B): z<-1, -1..1, z>1
dd["k"] = pd.cut(dd["z"], [-99, -1, 1, 99], labels=["z<-1", "orta", "z>1"])
print(dd.groupby("k")["y"].agg(["count", "mean"]).round(1))
for per, a, b in (("IS", T0, IS_END), ("OOS", OOS_START, T1)):
    g = dd[(dd.index >= a) & (dd.index <= b)].groupby("k")["y"].mean().round(1).to_dict()
    print(per, g)
# hisseye cevrim icin: MedEq artigina dusen pay (beta) bilinmiyor (hisse verisi yok)

print("\n(b) Insur artigi: kasirga zirvesi Agu-Eki vs Kas-Oca vs diger (gunluk bps, 2010-2026/09)")
ri = RES["Insur"] * 1e4
ri = ri[(ri.index >= T0) & (ri.index <= T1)].dropna()
m = ri.index.month
grp = np.where(np.isin(m, [8, 9, 10]), "Agu-Eki", np.where(np.isin(m, [11, 12, 1]), "Kas-Oca", "Sub-Tem"))
G = pd.DataFrame({"r": ri.values, "g": grp}, index=ri.index)
print(G.groupby("g")["r"].agg(["count", "mean", "std"]).round(2))
x = pd.Series((grp == "Agu-Eki").astype(float), index=ri.index)
b, t, p, n = o.hac_ols(ri, x, 20)
print(f"Agu-Eki farki: {b:.2f} bps/gun, HAC t {t:.2f}, p {p:.3f}, n {n}; 63 gunluk sezon farki ~{b*63:.0f} bps")
x2 = pd.Series((grp == "Kas-Oca").astype(float), index=ri.index)
b2, t2, p2, _ = o.hac_ols(ri, x2, 20)
print(f"Kas-Oca farki: {b2:.2f} bps/gun, HAC t {t2:.2f}, p {p2:.3f}")
yr = G[G.g == "Agu-Eki"].groupby(G[G.g == "Agu-Eki"].index.year)["r"].sum().round(0)
print("Agu-Eki kumulatif artik (bps) yil-yil:", yr.to_dict())
for per, a, bnd in (("IS", T0, IS_END), ("OOS", OOS_START, T1)):
    bb, tt, _, _ = o.hac_ols(win(ri, a, bnd), win(x, a, bnd), 20)
    print(per, f"Agu-Eki farki {bb:.2f} bps/gun t {tt:.2f}")
