"""Görev 2: genel_tum.csv'nin aile içi özeti. Küme temsilcileri (37 bağımsız birim) üzerinden tutarlılık.
Çıktı: sonuclar/aile_sektor_tematik/genel_aile_ozet.csv"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import *

g = pd.read_csv(os.path.join(ROOT, "sonuclar", "genel_tum.csv"))
g = g[g.sym.isin(FAM)].copy()
print("aile satırı (test sayısı, genel kütüphane):", len(g), "ETF:", g.sym.nunique())
g["fdr_aile"] = lib.bh_fdr(g["p"].values, 0.10)
print("aile içi BH-FDR q=0.10 geçen satır:", int(g.fdr_aile.sum()))
g["cl"] = g.sym.map(CL_OF)
r = g[g.sym.isin(REPS)]
key = ["sig", "mode", "h", "exit"]
agg = r.groupby(key).agg(n_rep=("sym", "size"), pos_net=("mean_net_bp", lambda x: (x > 0).mean()),
                         med_net=("mean_net_bp", "median"), med_gross=("mean_gross_bp", "median"),
                         med_edge=("edge_bp", "median"), pos_is=("is_net_bp", lambda x: (x > 0).mean()),
                         pos_oos=("oos_net_bp", lambda x: (x > 0).mean()), med_is=("is_net_bp", "median"),
                         med_oos=("oos_net_bp", "median"), med_t=("t", "median"), n_t2=("t", lambda x: (x >= 2).sum()),
                         med_n=("n", "median"), fdr_n=("fdr_aile", "sum")).reset_index()
# işaret testi (temsilciler arasında, bağımsız varsayımıyla bile iyimser)
from scipy.stats import binomtest
agg["p_sign"] = [binomtest(int(round(a * b)), int(b), 0.5, alternative="greater").pvalue for a, b in zip(agg.pos_net, agg.n_rep)]
agg = agg.sort_values("med_net", ascending=False)
agg.to_csv(os.path.join(OUT, "genel_aile_ozet.csv"), index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 80)
print(agg.head(40).round(2).to_string())
print("\nFDR geçen satırlar (tümü):")
print(g[g.fdr_aile][["sym", "sig", "mode", "h", "exit", "n", "mean_net_bp", "t", "is_net_bp", "oos_net_bp", "years_pos_frac"]].sort_values("t", ascending=False).round(2).to_string())
