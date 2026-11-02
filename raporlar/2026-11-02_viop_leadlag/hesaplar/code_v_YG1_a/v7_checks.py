"""v7: ek kontroller — (a) eski temizlik kuralıyla (tüm dönem ±%10,5) IS farkının kaynağı; (b) portföy düzeyinde plasebo (gap_{t-1});
(c) h1 P0730->C hisse bazında işaret oranı ve FDR."""
import numpy as np, pandas as pd, vc
TG = vc.VIOP
idx = vc.cal(); idx = idx[idx >= "2014-01-01"]
def port_stats(G, I, lab):
    pos = (-np.sign(G)).where(G.abs() > 0.01, 0.0).fillna(0.0); R = (pos * I).where(pos != 0)
    pp = R.mean(axis=1)
    out = [lab]
    for m in [idx < vc.SPLIT, idx >= vc.SPLIT]:
        mm, t, n = vc.nw_mean(pp[m].dropna().values, 5); out += [round(1e4 * mm, 1), round(t, 2), int(R[m].notna().sum().sum())]
    print(out)
D = {s: vc.decomp(s) for s in TG}
G = pd.DataFrame({s: D[s]["gap"] for s in TG}).reindex(idx); I = pd.DataFrame({s: D[s]["intra"] for s in TG}).reindex(idx)
port_stats(G, I, "güncel kural (rejime bağlı)  IS bps,t,n | OOS bps,t,n")
# eski kural: tüm dönem ±%10,5 (cc ve gap)
old = vc.SWITCH; vc.SWITCH = pd.Timestamp("1900-01-01")
D2 = {s: vc.decomp(s) for s in TG}; vc.SWITCH = old
G2 = pd.DataFrame({s: D2[s]["gap"] for s in TG}).reindex(idx); I2 = pd.DataFrame({s: D2[s]["intra"] for s in TG}).reindex(idx)
port_stats(G2, I2, "eski kural (tüm dönem ±%10,5)")
# yalnız iki kuralın farklı olduğu günler
diff = G.notna() & G2.isna()
print("yalnız güncel kuralda kalan hisse-gün:", int(diff.sum().sum()), " bunların |gap|>1% olanlarında fade ort bps:",
      round(1e4 * np.nanmean(((-np.sign(G)) * I).where(diff & (G.abs() > 0.01)).values), 1), " n", int((diff & (G.abs() > 0.01)).sum().sum()))
# plasebo portföy
G1 = G.shift(1)
for lab, msk in [("plasebo gap_{t-1} fade (tüm)", G1.abs() > 0.01), ("plasebo gap_{t-1} fade, bugün |gap|<=1%", (G1.abs() > 0.01) & (G.abs() <= 0.01))]:
    pos = (-np.sign(G1)).where(msk & I.notna(), 0.0).fillna(0.0); pp = (pos * I).where(pos != 0).mean(axis=1)
    r = [lab]
    for m in [idx < vc.SPLIT, idx >= vc.SPLIT]:
        mm, t, n = vc.nw_mean(pp[m].dropna().values, 5); r += [round(1e4 * mm, 1), round(t, 2)]
    print(r)
S = pd.read_csv(vc.RES + "/v2_h1_stock.csv")
for (en, ex), g in S.groupby(["entry", "exit"]):
    print(en, ex, "pozitif oran", round((g.bps > 0).mean(), 2), "medyan", round(g.bps.median(), 1), "FDR", int(g.fdr.sum()), "t>2:", list(g.stock[g.t > 2]))
