"""Adv1: C1..C5 yeniden üretim, alt dönemler, maliyet, veri kontrolleri (temettü/bölünme/adjclose)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e1_etf_zaman_takvim_adv")
from adv_common import *
pd.set_option("display.width", 250)
M = cal_masks(idx)
first, pre = M["first"], M["pre"]
basket = first | pre
R = {t: np.log(d[f"c_{t}"]).diff() for t in ["GDX", "GDXJ", "GLD", "NUGT", "JNUG", "SPY", "IAU", "SLV"]}
SUB = [("2008-12", "2008-01-01", "2012-12-31"), ("2013-17", "2013-01-01", "2017-12-31"), ("2018-21", "2018-01-01", "2021-12-31"), ("2022-26", "2022-01-01", "2026-12-31"),
       ("full", None, None), ("IS", None, "2017-12-31"), ("OOS", "2018-01-01", None)]
rows = []
for nm, m, tks in [("C1_sepet", basket, ["GDXJ", "GDX", "JNUG", "NUGT"]), ("ilk_gun", first, ["GDXJ", "GDX"]), ("C2_tatil_oncesi", pre, ["GDX", "GDXJ", "GLD"]),
                   ("C4_Ocak", pd.Series(idx.month == 1, index=idx), ["GLD"])]:
    for t in tks:
        for sn, a, b in SUB:
            e = ev(m, R[t], a, b)
            rows.append(dict(claim=nm, etf=t, sub=sn, **e))
T = pd.DataFrame(rows); print(T.to_string())
T.to_csv(f"{O}/adv1_alt_donem.csv", index=False)

# maliyet duyarlılığı (yalnız uzun), OOS ve tam
rows = []
for nm, m, t, cs in [("C1", basket, "GDXJ", [0, 10, 20, 40]), ("C1", basket, "GDX", [0, 10, 20, 40]), ("C1", basket, "JNUG", [20, 40, 60]), ("C1", basket, "NUGT", [20, 40, 60]),
                     ("C2", pre, "GDX", [0, 10, 20, 40]), ("C4", pd.Series(idx.month == 1, index=idx), "GLD", [10, 20])]:
    for c in cs:
        net = bt_day(m, R[t], c)
        for sn, a, b in SUB:
            p = net
            if a: p = p[p.index >= a]
            if b: p = p[p.index <= b]
            rows.append(dict(claim=nm, etf=t, cost=c, sub=sn, **perf(p)))
C = pd.DataFrame(rows)
print(C.pivot_table(index=["claim", "etf", "cost"], columns="sub", values="sh").to_string())
print(C.pivot_table(index=["claim", "etf", "cost"], columns="sub", values="ann").to_string())
C.to_csv(f"{O}/adv1_maliyet.csv", index=False)

# veri kontrolleri: adjclose/close oranı sıçramaları (temettü), |r|>25% günler, ters bölünme
for t in ["GDX", "GDXJ", "NUGT", "JNUG", "DUST", "JDST", "GLD"]:
    y = yahoo(t)
    ratio = np.log(y.adjclose / y.close).diff()
    big = ratio[ratio.abs() > 1e-4]
    rc = np.log(y.close).diff(); ra = np.log(y.adjclose).diff()
    print(f"\n{t}: temettü/düzeltme günleri {len(big)}; |adj r|>25% günler:", ra[ra.abs() > 0.25].round(3).to_dict())
    print("  close vs adjclose |fark|>20% (bölünme izi):", (rc - ra)[(rc - ra).abs() > 0.2].round(3).to_dict())
    # temettü günleri olay günlerine denk geliyor mu
    bd = big.index.intersection(idx)
    print("  düzeltme günleri (son 10):", [(str(x.date()), round(big[x] * 1e4, 1), bool(basket.get(x, False))) for x in bd[-10:]])
    # panel c_ ile adjclose eşleşmesi
    if f"c_{t}" in d:
        cc = d[f"c_{t}"].dropna(); aa = y.adjclose.reindex(cc.index)
        print("  panel c_ == yahoo adjclose max |log fark|:", float(np.nanmax(np.abs(np.log(cc / aa)))))
