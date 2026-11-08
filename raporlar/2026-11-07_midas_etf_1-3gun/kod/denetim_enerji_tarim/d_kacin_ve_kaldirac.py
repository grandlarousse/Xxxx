"""Denetim: (1) 'UNG/BOIL long'u EIA gününe taşıma' kaçın kuralının yıl yıl doğrulanması,
(2) UCO'nun USO/USL'ye göre efektif kaldıracı (2026'da 2x değil mi?).
Çalıştırma: python3 -I kod/denetim_enerji_tarim/d_kacin_ve_kaldirac.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import dsim as D, lib
from d_s1_eia_kold import eve_signal

for sym in ("UNG", "BOIL"):
    d = lib.load(sym); tr = D.sim(d, eve_signal(d), 1, "C0")
    y = tr.groupby(tr["sig"].dt.year)["brut"].mean() * 1e4
    print(f"{sym} rapor günü (arife kapanışı -> rapor kapanışı) brüt ort {tr['brut'].mean()*1e4:.1f} bp t={D.t_of(tr['brut']):.2f} n={len(tr)}; yıl yıl:", y.round(0).to_dict(),
          "| negatif yıl:", int((y < 0).sum()), "/", len(y))
    r = d["c"].pct_change(); print(f"  {sym} koşulsuz günlük ort {r.mean()*1e4:.1f} bp")
u, c, l = (lib.load(s)["c"].pct_change() for s in ("USO", "UCO", "USL"))
df = pd.DataFrame({"USO": u, "UCO": c, "USL": l}).dropna()
out = {}
for yy, g in df.groupby(df.index.year):
    out[yy] = {"UCO~USO": np.polyfit(g["USO"], g["UCO"], 1)[0], "UCO~USL": np.polyfit(g["USL"], g["UCO"], 1)[0], "USO~USL": np.polyfit(g["USL"], g["USO"], 1)[0],
               "corr UCO,USO": g["UCO"].corr(g["USO"]), "vol USO": g["USO"].std() * 1e4, "vol UCO": g["UCO"].std() * 1e4}
print(pd.DataFrame(out).T.round(2).to_string())
