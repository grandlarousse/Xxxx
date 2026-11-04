"""Lead-lag mi, momentum mu? h2 hedge'li ileri getiri ~ altın z + TRALT'ın kendi aynı gün hedge'li hareketi (z) [+ XU030]"""
import pl, numpy as np, pandas as pd
cl, ev = pl.cl, pl.ev
pl.install_panel(); c = cl.cal()
g0 = ev.R("XAUUSD"); z = cl.zscale(g0, 250, 100)
L = ev.legs("TRALT"); own = cl.zscale(L["hedged"], 250, 100); own_raw = cl.zscale(L["raw"], 250, 100)
m = cl.zscale(ev.R("XU030"), 250, 100)
for h in (1, 2, 3):
    y = cl.fwd(L["hedged"], h); y = y[y.index >= "2018-12-17"] * 1e4
    for lab, X in (("yalnız altın", pd.concat([z.rename("z_altin")], axis=1)),
                   ("altın + TRALT kendi (hedge'li) + XU030", pd.concat([z.rename("z_altin"), own.rename("z_TRALT_kendi"), m.rename("z_XU030")], axis=1)),
                   ("yalnız TRALT kendi", pd.concat([own.rename("z_TRALT_kendi")], axis=1)),
                   ("altın + altın(t-1) + kendi(t-1)", pd.concat([z.rename("z_altin"), z.shift(1).rename("z_altin_t1"), own.rename("z_TRALT_kendi"), own.shift(1).rename("kendi_t1")], axis=1))):
        o = pl.cl.nw_reg(y, X, h + 1)
        print(f"h{h} | {lab:40s} n={o[1]} | " + " ; ".join(f"{k}: b={o[0].loc[k,'b']:+.1f} t={o[0].loc[k,'t']:+.2f}" for k in X.columns))
# aynı gün korelasyon: TRALT hedge'li vs altın (senkron bağ)
b = pd.concat([z, own], axis=1).dropna(); print("aynı gün corr(z_altin, z_TRALT_kendi)", round(b.corr().iloc[0, 1], 3))
# z_altin'in TRALT kendi hareketinden arındırılmış kısmı ile kural
