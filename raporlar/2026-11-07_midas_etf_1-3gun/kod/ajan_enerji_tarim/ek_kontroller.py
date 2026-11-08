"""Aday incelemelerinde yapılan ek kontroller (test sayımına dahil edilir):
  1) S1k mevsim tanımı komşuları (Eki-Mar, Kas-Nis, Ara-Şub, Kas-Şub, Nis-Eki) -- KOLD C0 h1
  2) Genel kütüphane 'MR_bb20_alt' ham petrol C1 bulgusunun gecikmeli-sinyal sağlamlığı (8 ETF x 3 mod x 3 h)
  3) S2 sinyalinin SPY'de (aile dışı) karşılaştırması
Çalıştırma: python3 -I kod/ajan_enerji_tarim/ek_kontroller.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import ortak as O, lib, strategies as S

pd.set_option("display.width", 250)
rows = []
eia = O.events("eia_ng_storage")["date"]
k = lib.load("KOLD"); idx = k.index
base = O.day_before(idx, eia)
nm = pd.Series(list(idx[1:].month) + [idx[-1].month], index=idx)
for name, ms in [("Eki-Mar", [10, 11, 12, 1, 2, 3]), ("Kas-Nis", [11, 12, 1, 2, 3, 4]), ("Ara-Sub", [12, 1, 2]), ("Kas-Sub", [11, 12, 1, 2]),
                 ("Nis-Eki", [4, 5, 6, 7, 8, 9, 10])]:
    s, _ = O.full("KOLD", base & nm.isin(ms), 1, "C0")
    O.register("S1k_komsu_" + name, "KOLD", f"EIA öncesi KOLD, rapor ayı {name}", "C0", 1, s, +1)
    rows.append({"kontrol": "S1k_komsu", "var": name, **{c: s[c] for c in ["n", "mean_gross_bp", "mean_net_bp", "t", "is_net_bp", "is_t", "oos_net_bp", "oos_t", "years_pos_frac"]}})
for sym in ["USO", "BNO", "DBO", "USL", "UCO", "PDBC", "XLE", "XOP"]:
    d = lib.load(sym); s0 = S.LIB["MR_bb20_alt"](d, None).reindex(d.index).fillna(False); s0.iloc[:200] = False
    sl = s0.shift(1).fillna(False).astype(bool)
    for m in ("C0", "O1", "C1"):
        for h in (1, 2, 3):
            s, _ = O.full(sym, sl, h, m)
            O.register("MRbb20_gecikmeli", sym, "MR_bb20_alt sinyali 1 gün gecikmeli", m, h, s, +1)
            rows.append({"kontrol": "MRbb20_gecikmeli", "var": f"{sym} {m} h{h}", **{c: s[c] for c in ["n", "mean_gross_bp", "mean_net_bp", "t", "is_net_bp", "is_t", "oos_net_bp", "oos_t", "years_pos_frac"]}})
ctx = {"VIX": lib.vol_index("VIX"), "VIX3M": lib.vol_index("VIX3M")}
d = lib.load("SPY"); sg = S.LIB["VX_backw_donus"](d, ctx).reindex(d.index).fillna(False).astype(bool); sg.iloc[:200] = False
s, _ = O.full("SPY", sg, 2, "C1")
O.register("S2_SPY_karsilastirma", "SPY", "VX_backw_donus SPY C1 h2", "C1", 2, s, +1)
rows.append({"kontrol": "S2_SPY", "var": "SPY C1 h2", **{c: s[c] for c in ["n", "mean_gross_bp", "mean_net_bp", "t", "is_net_bp", "is_t", "oos_net_bp", "oos_t", "years_pos_frac"]}})
R = pd.DataFrame(rows); R.to_csv(os.path.join(O.OUT, "ek_kontroller.csv"), index=False)
O.save_registry("ek_kontroller")
print(R.round(2).to_string(index=False))
