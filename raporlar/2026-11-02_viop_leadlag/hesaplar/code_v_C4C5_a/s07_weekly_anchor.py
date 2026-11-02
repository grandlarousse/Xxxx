"""Adim 7: (c) haftalik sonucun hafta-sonu-gunu (capa) ve saat hizalamasina duyarliligi.
 - W-MON..W-FRI capalari; 5 gunluk ortusmeyen bloklar (5 farkli baslangic)
 - GC'yi 15:00 UTC'de (BIST kapanisi) h1'den orneklenmis seri ile (2024-06+) karsilastir."""
import sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_C4C5_a")
import vlib as V, numpy as np, pandas as pd
import s06_weekly_gold as S6
L, pc = S6.L, S6.pc
out = []
for anc in ["W-MON", "W-TUE", "W-WED", "W-THU", "W-FRI"]:
    W = L[["TRALT", "XU100", "AU", "GC", "GC_TL", "TRY"]].resample(anc).last().diff().dropna()
    out.append({"capa": anc, "n": len(W), "pc_AU": pc(W, "TRALT", "AU", ["XU100"]), "pc_GC": pc(W, "TRALT", "GC", ["XU100"]), "pc_GC_TL|XU,TRY": pc(W, "TRALT", "GC_TL", ["XU100", "TRY"]), "r_AU": W.TRALT.corr(W.AU), "r_GC": W.TRALT.corr(W.GC)})
for off in range(5):
    Lx = L[["TRALT", "XU100", "AU", "GC", "GC_TL", "TRY"]].iloc[off::5].diff().dropna()
    out.append({"capa": f"5g blok ofset {off}", "n": len(Lx), "pc_AU": pc(Lx, "TRALT", "AU", ["XU100"]), "pc_GC": pc(Lx, "TRALT", "GC", ["XU100"]), "pc_GC_TL|XU,TRY": pc(Lx, "TRALT", "GC_TL", ["XU100", "TRY"]), "r_AU": Lx.TRALT.corr(Lx.AU), "r_GC": Lx.TRALT.corr(Lx.GC)})
R = pd.DataFrame(out); print(R.round(3).to_string()); R.round(3).to_csv(S6.OUT + "s07_weekly_anchor.csv", index=False)
# GC 15:00 UTC snap (h1)
h = V.rawd("GC=F", "h1").copy(); s = h["c"].copy(); s.index = h.index + pd.Timedelta(hours=1); s = s[~s.index.duplicated(keep="last")].sort_index()
snap = {}
for t in L.index[L.index >= "2024-06-11"]:
    b = pd.Timestamp(t).tz_localize("UTC") + pd.Timedelta(hours=15); i = s.index.searchsorted(b, side="right") - 1
    if i >= 0 and (b - s.index[i]) <= pd.Timedelta(hours=2): snap[t] = np.log(s.iloc[i])
L2 = L[L.index >= "2024-06-11"].copy(); L2["GC1500"] = pd.Series(snap)
L2["GC1500"] = L2["GC1500"].ffill()
rows = []
for anc in ["W-MON", "W-WED", "W-FRI"]:
    W = L2[["TRALT", "XU100", "AU", "GC", "GC1500"]].resample(anc).last().diff().dropna()
    rows.append({"capa": anc, "n": len(W), **{f"pc_{d}": pc(W, "TRALT", d, ["XU100"]) for d in ["AU", "GC", "GC1500"]}})
Dd = L2[["TRALT", "XU100", "AU", "GC", "GC1500"]].diff().dropna()
rows.append({"capa": "gunluk", "n": len(Dd), **{f"pc_{d}": pc(Dd, "TRALT", d, ["XU100"]) for d in ["AU", "GC", "GC1500"]}})
print("\n2024-06+ (GC 15:00 UTC = BIST kapanisina hizali):"); print(pd.DataFrame(rows).round(3).to_string())
