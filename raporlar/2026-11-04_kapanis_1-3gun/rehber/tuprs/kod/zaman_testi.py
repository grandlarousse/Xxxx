"""Yürütme zamanı duyarlılığı (spot vekili): pratik kuralın pozisyon tarihleriyle, TUPRS spot
 (a) kapanış müzayedesi (günlük kapanış, ~18:10) -> (a) ; (b) 18:00 öncesi son fiyat (Yahoo saatlik 17:30 barının kapanışı); (c) ~17:30 fiyatı (16:30 barının kapanışı).
 Ayrıca VİOP uzlaşma vs spot kapanış ilişkisi. Yalnız saatlik verinin kapsadığı dönem (2023-12+; 17:30 barı daha kısa)."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd, cl_t as cl
S = cl.S
h = pd.read_parquet(S + "/data/h1/TUPRS.IS.parquet")
h["hm"] = h.index.tz_convert("Europe/Istanbul").strftime("%H:%M"); h["ld"] = pd.to_datetime(h["ldate"]).dt.normalize()
b1730 = h[h["hm"] == "17:30"].set_index("ld")["c"]; b1630 = h[h["hm"] == "16:30"].set_index("ld")["c"]
d = cl.dly("TUPRS.IS")["c"]
Pz = pd.read_csv(cl.OUT + "/pratik_pozisyonlar.csv", parse_dates=["giris", "cikis"])
rows = []
for _, r in Pz.iterrows():
    a, b = r["giris"], r["cikis"]
    if a in b1730.index and b in b1730.index and a in d.index and b in d.index:
        rows.append(dict(giris=a, yon=r["yon"], spot_kap=r["yon"] * np.log(d[b] / d[a]) * 1e4, spot_1800=r["yon"] * np.log(b1730[b] / b1730[a]) * 1e4,
                         spot_1730=r["yon"] * np.log(b1630[b] / b1630[a]) * 1e4 if (a in b1630.index and b in b1630.index) else np.nan, viop=r["brut_bps"]))
T = pd.DataFrame(rows)
print("n", len(T), "dönem", T.giris.min().date(), T.giris.max().date())
for col in ["viop", "spot_kap", "spot_1800", "spot_1730"]:
    print(col, "ort brüt bps", round(T[col].mean(), 1), "t", round(cl.tstat(T[col]), 2))
print("fark (18:00 öncesi - kapanış) ort", round((T.spot_1800 - T.spot_kap).mean(), 1), "std", round((T.spot_1800 - T.spot_kap).std(), 1))
print("işaret uyumu viop vs spot_1800", round((np.sign(T.viop) == np.sign(T.spot_1800)).mean(), 3))
