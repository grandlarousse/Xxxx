"""1) İşlenebilirlik + kopya grupları. Çalıştır: python3 -I kod/ajan_abd_endeks/01_islenebilirlik.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import ae, lib

t = pd.read_csv(os.path.join(ae.ROOT, "sonuclar", "tarama.csv"))
tv = pd.read_csv(os.path.join(ae.ROOT, "sonuclar", "tv_etf.csv"))[["sym", "tv", "durum"]]
x = t[t.sym.isin(ae.FAM)].merge(tv, on="sym", how="left")
x["grup"] = x.sym.map(ae.SYM2GRP)
x["cost_over_3d"] = x["cost_rt_bp"] / x["med_abs_3d_bp"]
# 1.000 / 10.000 USD maliyet
x["cost_1000_bp"] = 30 + x["spread_bp"]; x["cost_10000_bp"] = 3 + x["spread_bp"]

# Kaldıraç kaybı: (L^2-L)/2 * sigma_dayanak^2 / gün (son 1 yıl dayanak oynaklığı)
base = {"SP500": "SPY", "NDX": "QQQ", "R2K": "IWM", "DOW": "DIA"}
sig1y = {}
for b in base.values():
    r = np.log(lib.load(b)["c"]).diff().tail(252)
    sig1y[b] = r.std()
def drag(row):
    L = row["lev"]
    if abs(L) <= 1 and row["grup"] not in ("SP500_ters", "NDX_ters", "R2K_ters", "DOW_ters"): return 0.0
    g = row["grup"].split("_")[0]
    s = sig1y.get(base.get(g, "SPY"), np.nan)
    return (L * L - L) / 2 * s * s * 1e4 * 3
x["kaldirac_kaybi_3g_bp"] = x.apply(drag, axis=1)

# Korelasyon tabanlı kopya çiftleri
R = pd.DataFrame({s: np.log(lib.load(s)["c"]).diff() for s in ae.FAM})
R = R[R.index >= "2022-06-01"]
C = R.corr(); sd = R.std()
pairs = []
for i, a in enumerate(ae.FAM):
    for b in ae.FAM[i + 1:]:
        if abs(C.loc[a, b]) > 0.97:
            pairs.append({"a": a, "b": b, "corr": C.loc[a, b], "sd_orani_b_a": sd[b] / sd[a]})
pd.DataFrame(pairs).sort_values("corr", ascending=False).to_csv(os.path.join(ae.OUT, "kopya_ciftleri.csv"), index=False)

cols = ["sym", "grup", "lev", "tv", "med_dollar_vol_m", "spread_bp", "cost_rt_bp", "cost_1000_bp", "cost_10000_bp",
        "vol_1d_bp", "med_abs_3d_bp", "cost_over_1d_vol", "cost_over_3d", "gap_share", "worst_1d_1y", "kaldirac_kaybi_3g_bp", "first", "n"]
x = x[cols].sort_values(["grup", "med_dollar_vol_m"], ascending=[True, False])
x.to_csv(os.path.join(ae.OUT, "islenebilirlik.csv"), index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 200)
print(x.round(3).to_string(index=False))
print("\nKopya çiftleri (|corr|>0.97):", len(pairs))
