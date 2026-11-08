"""Adım 8: C1 COT gecikmeli yayın dönemi kontrolü (ABD hükümeti kapanmaları: 2018-12-22..2019-03-31, 2025-10-01..2025-12-31).
Bu dönemlerde COT bileşeni NaN yapılır (kalan bileşenlerin ortalaması) ve ayrıca bu günler pozisyon dışı bırakılır."""
import numpy as np, pandas as pd
from rep_stats import bt_full, split_ic
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"; OUT = f"{S}/out/a8_ml_kombinasyon_rep"
XV = pd.read_parquet(f"{OUT}/feat_viop.parquet"); v = pd.read_parquet(f"{OUT}/base_viop.parquet")
C1 = {"px_r20": 1, "px_r250": 1, "xa_dxy_d5": -1, "rt_real10_d5": -1, "sh_prem_d5": 1, "cot_mm_z52": -1}
shut = (XV.index.to_series().between("2018-12-22", "2019-03-31")) | (XV.index.to_series().between("2025-10-01", "2025-12-31"))
def score(X):
    zs = []
    for c in C1:
        x = X[c] * C1[c]; mu = x.expanding(250).mean().shift(1); sd = x.expanding(250).std().shift(1); zs.append(((x - mu) / sd).clip(-3, 3))
    return pd.concat(zs, axis=1)
Z = score(XV); base = Z.mean(axis=1)
Z2 = Z.copy(); Z2.loc[shut.values, "cot_mm_z52"] = np.nan; alt = Z2.mean(axis=1)
for nm, z in (("taban", base), ("COT kapanma NaN", alt)):
    p = np.sign(z).fillna(0)
    print(nm, "OOS h1:", bt_full(p.loc["2022":], v.ret.loc["2022":], 1), "| IC:", {k: round(split_ic(z, v.fwd1, 1)[k], 3) for k in ("ic", "t", "t_is", "t_oos")})
p = np.sign(base).fillna(0); p[shut.values] = 0
print("kapanma günleri pozisyonsuz OOS h1:", bt_full(p.loc["2022":], v.ret.loc["2022":], 1))
print("pozisyon değişen gün sayısı (COT NaN):", int((np.sign(base) != np.sign(alt)).sum()))
# 2026 hariç OOS ve yıllık Sharpe (h1)
from rep_stats import bt
p = np.sign(base).fillna(0)
print("C1 OOS 2022-2025:", bt_full(p.loc["2022":"2025"], v.ret.loc["2022":"2025"], 1))
z = bt(p, v.ret.loc["2018-03":], 1)["pnl"]; print("C1 yıllık Sharpe:", z.groupby(z.index.year).apply(lambda g: round(float(g.mean() / g.std() * np.sqrt(252)), 2)).to_dict())
print("C1 uzun oranı yıl yıl:", (p.loc["2018-03":] > 0).groupby(p.loc["2018-03":].index.year).mean().round(2).to_dict())
