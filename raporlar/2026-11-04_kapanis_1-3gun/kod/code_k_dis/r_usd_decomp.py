"""VİOP USDTRY sinyalinin ayrıştırması: bugünkü gün vs önceki günler; spot (h15) vs baz (vadeli - spot); 2024+ alt dönem."""
import numpy as np, pandas as pd, klib as K, ll
F = K.fut_panel(); M = pd.read_parquet(K.S + "/out/code_y_makro_y/res/macro_daily.parquet")
usd = F["USDTRY"]; y3 = K.fwd(F["THYAO"], 3); y3 = y3[y3.index >= "2017-03-06"]
def t(z, y=y3, a=None, b=None):
    yy = y
    if a: yy = yy[yy.index >= a]
    if b: yy = yy[yy.index <= b]
    r = K.reg(yy, z, 4); return round(r["t"], 2), round(r["b"] * 1e4, 1), r["n"]
for lab, z in [("V_USD k5 (t-4..t)", K.sdscale(K.cum(usd, 5, 0))), ("V_USD k4 lag1 (t-4..t-1)", K.sdscale(K.cum(usd, 4, 1))),
               ("V_USD bugün (k1)", K.sdscale(usd)), ("V_USD k5 lag2", K.sdscale(K.cum(usd, 5, 2)))]:
    print(lab, "tümü", t(z), "2017-21", t(z, a="2017", b="2021-12-31"), "2022-23", t(z, a="2022", b="2023-12-31"), "2024+", t(z, a="2024"))
# 2024+: spot h15 vs baz
h15 = M["h15_usd"].reindex(F.index); basis = usd - h15
for lab, z in [("spot h15 k5", K.sdscale(K.cum(h15, 5, 0), 120, 40)), ("baz (V-h15) k5", K.sdscale(K.cum(basis, 5, 0), 120, 40)), ("V_USD k5", K.sdscale(K.cum(usd, 5, 0), 120, 40))]:
    print(lab, "2024+", t(z, a="2024"))
print("corr(V_USD, h15) 2024+:", pd.concat([usd, h15], axis=1).dropna().corr().iloc[0, 1].round(3), " std V", usd["2024":].std().round(5), " std h15", h15["2024":].std().round(5))
# implied rate change d_ir12 (VİOP USDTRY vade yayılımı) k5
dir12 = M["d_ir12"].reindex(F.index).fillna(0)
print("d_ir12 k5", t(K.sdscale(K.cum(dir12, 5, 0))), " 2024+", t(K.sdscale(K.cum(dir12, 5, 0)), a="2024"))
