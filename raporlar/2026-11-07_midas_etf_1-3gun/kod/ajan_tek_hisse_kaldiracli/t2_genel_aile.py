"""Görev 2: genel_tum.csv (gerçek ETF verisi, 2022+) aile içi tutarlılık.
Bağımsız birim = dayanak hisse: her dayanaktan bir uzun 2x ETF (NVDL, TSLL, MSTU, CONL, AAPU, AMZU, METU, MSFU, GGLL).
Ters ETF'ler (TSLQ, NVDS) ve kopya (NVDU) ayrı raporlanır (bağımsız kanıt değil).
Not: ETF geçmişleri 2022+ olduğundan genel_tum'da IS (<=2021) boştur; IS/OOS kanıtı t3'teki dayanak testinden gelir.
Çalıştırma: python3 -I kod/ajan_tek_hisse_kaldiracli/t2_genel_aile.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import thk, lib

pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40); pd.set_option("display.max_rows", 200)
g = pd.read_csv(os.path.join(thk.ROOT, "sonuclar", "genel_tum.csv"))
g["fdr_tum"] = lib.bh_fdr(g["p"].values, 0.10)
f = g[g.sym.isin(thk.FAM)].copy()
f["fdr_aile"] = lib.bh_fdr(f["p"].values, 0.10)
prim = list(thk.PRIMARY.values())
key = ["sig", "mode", "h", "exit"]
P = f[f.sym.isin(prim)]
agg = P.groupby(key).agg(k=("sym", "size"), n_top=("n", "sum"), net_ort=("mean_net_bp", "mean"),
                         brut_ort=("mean_gross_bp", "mean"), edge_ort=("edge_bp", "mean"),
                         pozitif=("mean_net_bp", lambda x: int((x > 0).sum())),
                         t_ge2=("t", lambda x: int((x >= 2).sum())), t_le_m2=("t", lambda x: int((x <= -2).sum())),
                         stouffer=("t", lambda x: x.sum() / np.sqrt(len(x))),
                         fdr_aile=("fdr_aile", "sum"), fdr_tum=("fdr_tum", "sum"),
                         yil_poz=("years_pos_frac", "mean")).reset_index()
agg["pozitif_oran"] = agg["pozitif"] / agg["k"]
# ters ETF'ler ve kopya için aynı sinyal
for e in ["TSLQ", "NVDS", "NVDU"]:
    sub = f[f.sym == e].set_index(key)[["mean_net_bp", "t"]].rename(columns={"mean_net_bp": f"{e}_net", "t": f"{e}_t"})
    agg = agg.merge(sub, left_on=key, right_index=True, how="left")
agg = agg.sort_values("stouffer", ascending=False)
agg.to_csv(os.path.join(thk.OUT, "genel_aile_tutarlilik.csv"), index=False)
f.to_csv(os.path.join(thk.OUT, "genel_aile_satirlar.csv"), index=False)
print("aile satır:", len(f), " aile FDR geçen:", int(f.fdr_aile.sum()), " tüm evren FDR geçen (aile):", int(f.fdr_tum.sum()))
print(f[f.fdr_aile | f.fdr_tum][["sym", "sig", "mode", "h", "exit", "n", "mean_gross_bp", "mean_net_bp", "t", "p", "win", "years_pos_frac", "fdr_aile", "fdr_tum"]].round(3).to_string())
print("\nEn tutarlı 25 (9 bağımsız dayanağın birincil ETF'i):")
cols = key + ["k", "n_top", "brut_ort", "net_ort", "pozitif", "t_ge2", "t_le_m2", "stouffer", "fdr_aile", "yil_poz", "TSLQ_net", "NVDS_net", "NVDU_net"]
print(agg[cols].head(25).round(2).to_string())
print("\nEn olumsuz 10:")
print(agg[cols].tail(10).round(2).to_string())
