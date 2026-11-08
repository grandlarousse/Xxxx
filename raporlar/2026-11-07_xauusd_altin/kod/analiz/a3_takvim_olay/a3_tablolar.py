"""RAPOR.md için tablo üretici: results_all.csv + registry -> tablolar_*.md (aile bazında tam test tablosu)."""
import os, sys, pandas as pd, numpy as np
O = os.path.dirname(os.path.abspath(__file__)); S = os.path.abspath(f"{O}/../.."); sys.path.insert(0, f"{S}/code")
from lib_altin import bh_fdr, REG_DIR
R = pd.read_csv(f"{O}/results_all.csv"); reg = pd.read_csv(f"{REG_DIR}/a3_takvim_olay.csv"); yon = reg.family != "oynaklik"
reg["q"] = np.nan; reg.loc[yon, "q"] = bh_fdr(reg.p[yon].fillna(1).values)  # yön testleri içinde BH (oynaklık testleri ayrı)
reg.to_csv(f"{O}/registry_with_q.csv", index=False)
R = R.merge(reg[["test_id", "q"]].drop_duplicates("test_id"), on="test_id", how="left")
fam = {"haftanin_gunu": "Haftanın günü", "ay_donumu": "Ay dönümü", "ay_mevsim": "Ay mevsimselliği", "ceyrek_yil": "Çeyrek / yıl sonu", "fomc": "FOMC",
       "cpi_nfp": "CPI / NFP", "tatil": "Tatiller ve bayramlar", "comex_vade": "COMEX opsiyon vadesi / FND / BCOM", "viop_vade": "VİOP vadesi / roll", "asya": "Asya festivalleri"}
def f(x, n=1):
    return "" if pd.isna(x) else f"{x:.{n}f}"
out = []
for k, nm in fam.items():
    g = R[R.family == k]
    out.append(f"\n**{nm}** ({len(g)} test)\n\n| test | n olay | fark/koşullu ort. (bps) | t tam | t IS | t OOS | yıl aynı işaret | erken spot t | t (uç hariç) | OOS Sharpe net | OOS Sharpe demeaned | q (BH) |\n|---|---|---|---|---|---|---|---|---|---|---|---|")
    for _, r in g.iterrows():
        out.append(f"| {r.test_id} | {int(r.n_ev)} | {f(r.diff_bps)} | {f(r.t,2)} | {f(r.t_is,2)} | {f(r.t_oos,2)} | {int(r.yrs_same_sign)}/{int(r.yrs)} | {f(r.get('early_t'),2)} | {f(r.t_ex_outlier,2)} | {f(r.get('sh_oos'),2)} | {f(r.get('sh_oos_dm'),2)} | {f(r.q,2)} |")
open(f"{O}/tablolar.md", "w").write("\n".join(out))
print(len(R), "satır tabloya yazıldı")
