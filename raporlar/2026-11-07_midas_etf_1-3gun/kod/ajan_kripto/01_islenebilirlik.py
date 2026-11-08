"""1) İşlenebilirlik + kopya grupları. Çalıştır: python3 -I kod/ajan_kripto/01_islenebilirlik.py
Çıktı: sonuclar/aile_kripto/islenebilirlik.csv, kopya_korelasyon.csv, dagitimlar.csv"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import kr, lib

scr = pd.read_csv(os.path.join(kr.ROOT, "sonuclar", "tarama.csv"))
tv = pd.read_csv(os.path.join(kr.ROOT, "sonuclar", "tv_etf.csv")).set_index("sym")
x = scr[scr.sym.isin(kr.FAM)].copy()
x["grup"] = x.sym.map(kr.SYM2GRP)
x["dayanak"] = x.sym.map(kr.UNDERLYING)
x["tv"] = x.sym.map(tv["tv"])
x["cost_1000"] = 2 * 1.5 / 1000 * 1e4 + x["spread_bp"]
x["cost_10000"] = 2 * 1.5 / 10000 * 1e4 + x["spread_bp"]
x["cost_over_3d_medabs"] = x["cost_rt_bp"] / x["med_abs_3d_bp"]

# kopya korelasyonları (ortak dönem) ve takip farkı
R = pd.DataFrame({s: np.log(lib.load(s)["c"]).diff() for s in kr.FAM})
rows = []
for g, ss in kr.GROUPS.items():
    base = ss[0]
    for s in ss[1:]:
        d = R[[base, s]].dropna()
        rows.append({"grup": g, "temsilci": base, "sym": s, "n_ortak": len(d), "corr": d.corr().iloc[0, 1],
                     "te_bp_gunluk": (d[s] - d[base]).std() * 1e4, "fark_ort_bp_gunluk": (d[s] - d[base]).mean() * 1e4})
# gruplar arası
pairs = [("IBIT", "BITO"), ("IBIT", "BITX"), ("IBIT", "ETHA"), ("IBIT", "BLOK"), ("IBIT", "MSTU"), ("IBIT", "CONL"),
         ("IBIT", "BITI"), ("BITX", "BITU"), ("ETHA", "ETHU"), ("BITI", "SBIT")]
for a, b in pairs:
    d = R[[a, b]].dropna()
    rows.append({"grup": "gruplar_arasi", "temsilci": a, "sym": b, "n_ortak": len(d), "corr": d.corr().iloc[0, 1],
                 "te_bp_gunluk": np.nan, "fark_ort_bp_gunluk": np.nan})
kc = pd.DataFrame(rows)
kc.to_csv(os.path.join(kr.OUT, "kopya_korelasyon.csv"), index=False)

# BITO: veri kaynağında dağıtım (temettü) kaydı YOK; ay başı açılış boşlukları dağıtım ex-date'leri gibi görünüyor
b = lib.load("BITO"); gap = b["o"] / b["c"].shift(1) - 1
ib = lib.load("IBIT"); gap_i = (ib["o"] / ib["c"].shift(1) - 1).reindex(b.index)
first_days = b.index.to_series().groupby([b.index.year, b.index.month]).transform("min") == b.index.to_series()
fd = pd.DataFrame({"bito_gap": gap, "ibit_gap": gap_i, "ay_ilk_gun": first_days}).dropna()
print("BITO açılış boşluğu - IBIT açılış boşluğu (bp), ayın ilk işlem günü vs diğer günler (2024-01+):")
print(((fd["bito_gap"] - fd["ibit_gap"]) * 1e4).groupby(fd["ay_ilk_gun"]).describe().round(1))

# dağıtımlar (ex-date stopaj riski)
drows = []
for s in kr.FAM:
    d = lib.load(s)
    dv = d[d["div"] > 0]
    if len(dv):
        y = (dv["div"] / d["raw_c"].shift(1).reindex(dv.index))
        drows.append({"sym": s, "n_dagitim": len(dv), "son_tarih": str(dv.index[-1].date()),
                      "ort_getiri_pct": float(y.mean() * 100), "maks_getiri_pct": float(y.max() * 100),
                      "son12ay_toplam_pct": float(y[y.index > d.index[-1] - pd.Timedelta(days=365)].sum() * 100)})
dd = pd.DataFrame(drows)
dd.to_csv(os.path.join(kr.OUT, "dagitimlar.csv"), index=False)
x = x.merge(dd[["sym", "n_dagitim", "son12ay_toplam_pct"]], on="sym", how="left")
cols = ["sym", "grup", "dayanak", "tv", "first", "n", "price", "med_dollar_vol_m", "spread_bp", "cost_rt_bp", "cost_1000",
        "cost_10000", "vol_1d_bp", "cost_over_1d_vol", "med_abs_3d_bp", "cost_over_3d_medabs", "gap_share", "lev",
        "worst_1d_1y", "ret_1y", "n_dagitim", "son12ay_toplam_pct"]
x = x[cols].sort_values(["grup", "med_dollar_vol_m"], ascending=[True, False])
x.to_csv(os.path.join(kr.OUT, "islenebilirlik.csv"), index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
print(x.round(3).to_string(index=False))
print(kc.round(4).to_string(index=False))
print(dd.round(3).to_string(index=False))
