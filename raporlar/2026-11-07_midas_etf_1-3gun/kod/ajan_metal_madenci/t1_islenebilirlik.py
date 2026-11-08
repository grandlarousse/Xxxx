"""Görev 1: işlenebilirlik (tarama.csv) + kopya grupları + korelasyonlar.
Çalıştır: python3 -I kod/ajan_metal_madenci/t1_islenebilirlik.py
Çıktı: sonuclar/aile_metal_madenci/islenebilirlik.csv, kopya_korelasyon.csv"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import mm

PTP = {"UGL": "PTP (ProShares Trust II, K-1)", "GLL": "PTP (ProShares Trust II, K-1)", "AGQ": "PTP (ProShares Trust II, K-1)",
       "ZSL": "PTP (ProShares Trust II, K-1)", "CPER": "PTP olasılığı yüksek (USCF emtia havuzu, K-1)",
       "DBB": "PTP olasılığı yüksek (Invesco DB emtia havuzu, K-1)"}
GRANTOR = {"GLD", "IAU", "GLDM", "SLV", "SIVR", "PPLT", "PALL"}

def main():
    t = pd.read_csv(os.path.join(mm.ROOT, "sonuclar", "tarama.csv"))
    t = t[t.sym.isin(mm.FAM)].copy()
    t["kume"] = t.sym.map(mm.CLUSTER)
    t["maliyet_1000"] = 30 + t["spread_bp"]; t["maliyet_10000"] = 3 + t["spread_bp"]
    t["cost_over_3d"] = t["cost_rt_bp"] / t["med_abs_3d_bp"]
    t["yapi"] = t.sym.map(lambda s: PTP.get(s, "grantor trust (fiziki)" if s in GRANTOR else "1940 Kanunu ETF"))
    tv = mm.tv_map(); t["tv"] = t.sym.map(tv)
    cols = ["sym", "kume", "tv", "lev", "yapi", "med_dollar_vol_m", "spread_bp", "cost_rt_bp", "maliyet_1000", "maliyet_10000",
            "vol_1d_bp", "med_abs_1d_bp", "med_abs_3d_bp", "cost_over_1d_vol", "cost_over_3d", "gap_share", "worst_1d_1y", "ret_1y", "first", "n"]
    t = t[cols].sort_values(["kume", "med_dollar_vol_m"], ascending=[True, False])
    t.to_csv(os.path.join(mm.OUTD, "islenebilirlik.csv"), index=False)
    pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
    print(t.round(3).to_string(index=False))
    # kopya grupları: getiri korelasyonları
    R = pd.DataFrame({s: np.log(mm.load(s)["c"]).diff() for s in mm.FAM}).dropna(how="all")
    pairs = [("GLD", "IAU"), ("GLD", "GLDM"), ("SLV", "SIVR"), ("GDX", "GDXJ"), ("GDX", "RING"), ("SIL", "SILJ"), ("GDX", "SIL"),
             ("URA", "URNM"), ("COPX", "XME"), ("CPER", "DBB"), ("CPER", "COPX"), ("GLD", "GDX"), ("SLV", "SIL"), ("GLD", "SLV"),
             ("PPLT", "PALL"), ("LIT", "REMX"), ("GDX", "NUGT"), ("GDXJ", "JNUG"), ("SLV", "AGQ"), ("GLD", "UGL")]
    rows = []
    for a, b in pairs:
        d = R[[a, b]].dropna(); d1 = d.tail(252)
        rows.append({"a": a, "b": b, "corr_tum": d[a].corr(d[b]), "corr_1y": d1[a].corr(d1[b]),
                     "beta_1y_b_on_a": np.cov(d1[b], d1[a])[0, 1] / d1[a].var()})
    c = pd.DataFrame(rows); c.to_csv(os.path.join(mm.OUTD, "kopya_korelasyon.csv"), index=False)
    print(c.round(3).to_string(index=False))

if __name__ == "__main__":
    main()
