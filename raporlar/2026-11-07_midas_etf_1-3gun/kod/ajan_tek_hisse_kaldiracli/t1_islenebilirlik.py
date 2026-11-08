"""Görev 1: İşlenebilirlik + gerçekleşen kaldıraç + kopya grupları (tek hisse kaldıraçlı aile).
Çalıştırma: python3 -I kod/ajan_tek_hisse_kaldiracli/t1_islenebilirlik.py
Çıktılar: islenebilirlik.csv, kaldirac_yillik.csv, kopya_korelasyon.csv"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import thk, lib

pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
T = thk.tarama()
rows = []; lev_rows = []
R = {}
for e in thk.FAM:
    d = lib.load(e); s = thk.load_stock(thk.UNDER[e]).reindex(d.index)
    re = d["c"].pct_change(); rs = s["c"].pct_change()
    R[e] = re
    x = pd.DataFrame({"re": re, "rs": rs}).dropna()
    def reg(z):
        if len(z) < 30: return np.nan, np.nan, np.nan
        b = np.cov(z.re, z.rs)[0, 1] / z.rs.var()
        r2 = z.re.corr(z.rs) ** 2
        return b, r2, len(z)
    b_all, r2_all, n_all = reg(x)
    b_1y, r2_1y, _ = reg(x.tail(252))
    # gecelik (açılış boşluğu) kaldıracı: ETF boşluğu / hisse boşluğu
    ge = (d["o"] / d["c"].shift(1) - 1); gs = (s["o"] / s["c"].shift(1) - 1)
    gz = pd.DataFrame({"re": ge, "rs": gs}).dropna().tail(252)
    b_gap = np.cov(gz.re, gz.rs)[0, 1] / gz.rs.var() if len(gz) > 30 else np.nan
    L = round(b_1y * 2) / 2
    dev = (x.re - L * x.rs).tail(252)
    for y, z in x.groupby(x.index.year):
        b, r2, n = reg(z)
        lev_rows.append({"sym": e, "yil": y, "beta": b, "r2": r2, "n": n,
                         "sapma_bp_gun": (z.re - L * z.rs).mean() * 1e4, "iz_hatasi_bp": (z.re - L * z.rs).std() * 1e4})
    t = T.loc[e]
    rows.append({"sym": e, "dayanak": thk.UNDER[e], "ilk": t["first"], "fiyat": t["price"],
                 "med_dolar_hacim_mn": t["med_dollar_vol_m"], "makas_bp": t["spread_bp"], "maliyet_rt_bp_2500": t["cost_rt_bp"],
                 "maliyet_rt_bp_1000": 30 + t["spread_bp"], "maliyet_rt_bp_10000": 3 + t["spread_bp"],
                 "vol_1d_bp": t["vol_1d_bp"], "med_abs_3d_bp": t["med_abs_3d_bp"], "maliyet_vol_orani": t["cost_over_1d_vol"],
                 "gap_share": t["gap_share"], "worst_1d_1y": t["worst_1d_1y"], "ret_1y": t["ret_1y"],
                 "nominal_kaldirac": t["lev"], "beta_tum": b_all, "beta_1y": b_1y, "beta_gap_1y": b_gap, "r2_1y": r2_1y,
                 "L_tahmin": L, "sapma_bp_gun_1y": dev.mean() * 1e4, "iz_hatasi_bp_gun_1y": dev.std() * 1e4})
isl = pd.DataFrame(rows)
# kopya grupları
isl["kopya_grubu"] = isl["dayanak"]
isl.to_csv(os.path.join(thk.OUT, "islenebilirlik.csv"), index=False)
lev = pd.DataFrame(lev_rows); lev.to_csv(os.path.join(thk.OUT, "kaldirac_yillik.csv"), index=False)
C = pd.DataFrame(R).dropna(how="all")
cc = C.tail(252).corr()
cc.to_csv(os.path.join(thk.OUT, "kopya_korelasyon.csv"))
print(isl.round(3).to_string())
print(lev.pivot(index="sym", columns="yil", values="beta").round(2).to_string())
print(lev.pivot(index="sym", columns="yil", values="sapma_bp_gun").round(1).to_string())
print(cc.round(2).to_string())
