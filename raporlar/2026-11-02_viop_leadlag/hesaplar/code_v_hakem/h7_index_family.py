"""H7: (a) Piyasa geneli bilgi: bölge endeksi penceresi -> XU100/XU030 gap ve gün-içi (açılışta tam/aşırı mı?).
(b) Tarama ajanının KENDİ matrisindeki t'leri (tarama_matrix.parquet) yalnız ön-kayıtlı 560 (hisse, emsal) çiftine daraltınca BH kaç geçiş verir?"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import vh
from peers import PEERS
txt = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); txt.append(s)
cal = vh.bist_cal()
xu = vh.bist_decomp("XU100"); x30 = vh.bist_decomp("XU030")
def W(sym): return vh.to_bist_window(vh.foreign_ret(sym), vh.bucket(sym))
rows = []
for drv in ["^GSPC", "^STOXX", "^N225", "^KS11", "^AXJO"]:
    w = W(drv)
    for nm, d in [("XU100", xu), ("XU030", x30)]:
        for col in ["gap", "intra"]:
            for per in ["ALL", "IS", "OOS"]:
                m = vh.period_mask(cal, per)
                b, t, n, c = vh.ols_nw(d[col].values[m].astype(float), vh.zscore(w).reindex(cal).values[m].astype(float))
                rows.append({"sürücü": drv, "kova": vh.bucket(drv), "hedef": nm, "parça": col, "per": per, "b_bps_1σ": 1e4 * b, "t_NW": t, "corr": c, "n": n})
A = pd.DataFrame(rows); A.to_csv(vh.RES + "/h7_index.csv", index=False)
P("== (a) Bölge endeksi (öncül pencere, z) -> BIST endeksi gap / gün-içi ==")
P(A[A.per == "ALL"].pivot_table(index=["sürücü", "hedef"], columns="parça", values=["b_bps_1σ", "t_NW"]).round(2).to_string())
P(A[(A.parça == "intra")].pivot_table(index=["sürücü", "hedef"], columns="per", values="t_NW").round(2).to_string())

# (b)
M = pd.read_parquet(vh.SCR + "/out/tarama_matrix.parquet", columns=["stock", "driver", "bucket", "t_intra_l1_full", "t_intra_l0_full", "q_intra_l1_full", "q_intra_l0_full", "intra_l1_full", "intra_l0_full"])
pairs = pd.DataFrame([(s, p) for s, v in PEERS.items() for p in v], columns=["stock", "driver"])
J = pairs.merge(M, on=["stock", "driver"], how="left")
J["t_tradeable"] = np.where(J.bucket == "asia_pre", J.t_intra_l0_full, J.t_intra_l1_full)
J["q_48k"] = np.where(J.bucket == "asia_pre", J.q_intra_l0_full, J.q_intra_l1_full)
J = J[J.t_tradeable.notna()]
J["q_fam"] = vh.bh(vh.p2(J.t_tradeable.values))
P(f"\n== (b) Tarama matrisinin kendi t'leri, ön-kayıtlı aile ({len(J)} çift; Asya için lag0, diğerleri lag1; ham gün-içi) ==")
P(f"  t>0 oranı {np.mean(J.t_tradeable>0):.3f}; t>2: {(J.t_tradeable>2).sum()}, t<-2: {(J.t_tradeable<-2).sum()}; 48k ailesindeki q<0,05: {(J.q_48k<0.05).sum()} (Asya lag0 q'su tüm-kova intra_l0 ailesinden); aile-içi BH q<0,05: {(J.q_fam<0.05).sum()}")
P("  en iyi 15:"); P(J.sort_values("t_tradeable", ascending=False).head(15)[["stock", "driver", "bucket", "t_tradeable", "q_48k", "q_fam"]].round(4).to_string(index=False))
J.to_csv(vh.RES + "/h7_tarama_prereg_family.csv", index=False)
# null'da beklenen: aile=560, iki yönlü p<0,05 -> ~28 (14+/14-)
open(vh.RES + "/h7_summary.txt", "w").write("\n".join(txt))
