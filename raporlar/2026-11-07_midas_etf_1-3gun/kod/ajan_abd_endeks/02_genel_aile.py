"""2) genel_tum.csv aile içi tutarlılık. Çalıştır: python3 -I kod/ajan_abd_endeks/02_genel_aile.py
Aile içi BH-FDR (q=0.10) tüm aile satırları (55 ETF) üzerinde; tutarlılık yalnız grup temsilcilerinde (ae.REPS) sayılır,
böylece kopyalar (SPY/VOO/IVV...) ve kaldıraçlı kopyalar bağımsız kanıt sayılmaz."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import ae, lib

g = pd.read_csv(os.path.join(ae.ROOT, "sonuclar", "genel_tum.csv"))
x = g[g.sym.isin(ae.FAM)].copy()
x["fdr_aile"] = lib.bh_fdr(x["p"].values, 0.10)
n_tests = len(x)
r = x[x.sym.isin(ae.REPS)].copy()
r["core"] = r.sym.isin(ae.CORE)
r["isoos_pos"] = (r.is_net_bp > 0) & (r.oos_net_bp > 0)
agg = r.groupby(["sig", "mode", "h", "exit"]).apply(lambda d: pd.Series({
    "n_rep": len(d),
    "pos_net": int((d.mean_net_bp > 0).sum()),
    "pos_net_core": int(((d.mean_net_bp > 0) & d.core).sum()),
    "isoos_pos": int(d.isoos_pos.sum()),
    "isoos_pos_core": int((d.isoos_pos & d.core).sum()),
    "t_ge2": int((d.t >= 2).sum()),
    "fdr_pos": int((d.fdr_aile & (d.mean_net_bp > 0)).sum()),
    "med_net_bp": d.mean_net_bp.median(),
    "med_gross_bp": d.mean_gross_bp.median(),
    "med_edge_bp": d.edge_bp.median(),
    "med_t": d.t.median(),
    "med_n": d.n.median(),
    "SPY_net": d.loc[d.sym == "SPY", "mean_net_bp"].mean(),
    "QQQ_net": d.loc[d.sym == "QQQ", "mean_net_bp"].mean(),
    "IWM_net": d.loc[d.sym == "IWM", "mean_net_bp"].mean(),
    "SPY_t": d.loc[d.sym == "SPY", "t"].mean(),
    "QQQ_t": d.loc[d.sym == "QQQ", "t"].mean(),
    "IWM_t": d.loc[d.sym == "IWM", "t"].mean(),
})).reset_index()
agg = agg.sort_values(["isoos_pos", "med_t"], ascending=False)
agg.to_csv(os.path.join(ae.OUT, "genel_aile_tutarlilik.csv"), index=False)
x[x.fdr_aile & (x.mean_net_bp > 0)].sort_values("t", ascending=False).to_csv(
    os.path.join(ae.OUT, "genel_aile_fdr_pozitif.csv"), index=False)

pd.set_option("display.width", 260); pd.set_option("display.max_rows", 200); pd.set_option("display.max_columns", 30)
print("Aile satır sayısı (test):", n_tests, " FDR geçen:", int(x.fdr_aile.sum()), " bunların pozitif olanı:",
      int((x.fdr_aile & (x.mean_net_bp > 0)).sum()))
print("Negatif FDR geçenlerin ETF dağılımı (ters/kaldıraç kaybı):")
print(x[x.fdr_aile & (x.mean_net_bp < 0)].sym.value_counts().head(15).to_string())
cols = ["sig", "mode", "h", "exit", "n_rep", "pos_net", "pos_net_core", "isoos_pos", "isoos_pos_core", "t_ge2", "fdr_pos",
        "med_net_bp", "med_edge_bp", "med_t", "med_n", "SPY_net", "SPY_t", "QQQ_net", "QQQ_t", "IWM_net", "IWM_t"]
print(agg[cols].head(45).round(2).to_string(index=False))
