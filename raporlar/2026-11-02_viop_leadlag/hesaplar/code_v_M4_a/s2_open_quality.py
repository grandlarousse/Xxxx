"""S2: Yahoo BIST açılış (o) kalite denetimi yıllara göre + kompozitin gap/intra etkisinin yıllara göre dağılımı.
Soru: 'o' bazı yıllarda önceki kapanışa eşitse (açılış eksik), intra = cc olur ve Asya bilgisinin gap'te fiyatlanan kısmı sahte 'gün-içi' görünür."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v, numpy as np, pandas as pd
pd.set_option("display.width", 250)
JP_AU = ["5411.T", "5401.T", "6301.T", "FMG.AX", "BHP.AX"]
comp = v.composite(JP_AU)
for st in ["EREGL.IS", "KRDMD.IS"]:
    d = v.decomp(st, start="2010-01-01"); d = d[d.index >= "2010-01-01"]
    q = pd.DataFrame({
        "o_eq_pc": np.isclose(d.o, d.pc, rtol=1e-6), "o_eq_c": np.isclose(d.o, d.c, rtol=1e-6),
        "gap0": d.gap.abs() < 1e-9, "intra_nan": d.intra.isna()}, index=d.index)
    Y = q.groupby(q.index.year).mean().round(3)
    # yıllık corr(gap, comp), corr(intra, comp)
    g = pd.concat([d.gap, d.intra, comp.rename("s")], axis=1).dropna()
    Y["corr_gap_comp"] = g.groupby(g.index.year).apply(lambda x: x.gap.corr(x.s)).round(3)
    Y["corr_intra_comp"] = g.groupby(g.index.year).apply(lambda x: x.intra.corr(x.s)).round(3)
    Y["sd_gap_bps"] = (1e4 * d.gap.groupby(d.index.year).std()).round(0)
    Y["sd_intra_bps"] = (1e4 * d.intra.groupby(d.index.year).std()).round(0)
    print(st); print(Y.to_string())
    # gap'i sıfır olan günler hariç intra etkisi
    g2 = g.copy(); g2["gap0"] = q.gap0.reindex(g2.index)
    for lab, sub in [("tüm", g2), ("gap!=0", g2[~g2.gap0]), ("gap==0", g2[g2.gap0])]:
        c, t, n = v.corr_t(sub.intra, sub.s); print(f"  {lab:8s} corr(intra,comp)={c:.3f} t={t:.2f} n={n}")
