"""Denetim: çoklu test. genel_tum.csv (92k test) ve aile satırları (sektor+tematik+sektor_kaldiracli) üzerinde
(1) iki yönlü net p ile BH (ajanın yaptığı), (2) TEK YÖNLÜ (pozitif) p ile BH — maliyetin anlamlı kıldığı negatif satırlar
BH eşiğini gevşetmesin diye, (3) maliyetten bağımsız brüt kenar t'si (t_edge) ile tek yönlü BH, (4) Bonferroni.
python3 -I kod/denetim_sektor_tematik/d8_coklu_test.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from d_ortak import *
from scipy import stats as S
g = pd.read_csv(os.path.join(ROOT, "sonuclar/genel_tum.csv"))
g["p1"] = S.t.sf(g["t"], g["n"] - 1); g["p1e"] = S.t.sf(g["t_edge"], g["n"] - 1)
fam = g[g["cat"].isin(["sektor", "tematik", "sektor_kaldiracli"])].copy()
key = (g.sym == "SMH") & (g.sig == "MR_ibs_lt02") & (g["mode"] == "C0") & (g.h == 1) & (g["exit"] == "sabit")
for nm, df in (("tum_92k", g), ("aile_22k", fam)):
    k = key.reindex(df.index).fillna(False).values
    r = {"iki_yonlu_BH": bh(df["p"].values)[k][0], "tek_yonlu_BH": bh(df["p1"].values)[k][0], "brut_kenar_tek_yonlu_BH": bh(df["p1e"].values)[k][0],
         "bonferroni_iki_yonlu": bool(df.loc[k, "p"].values[0] < 0.05 / np.isfinite(df["p"]).sum()),
         "BH_gecen_iki_yonlu": int(bh(df["p"].values).sum()), "BH_gecen_tek_yonlu": int(bh(df["p1"].values).sum()),
         "SMH_p": float(df.loc[k, "p"].values[0]), "SMH_p1": float(df.loc[k, "p1"].values[0]), "SMH_p1e": float(df.loc[k, "p1e"].values[0])}
    print(nm, r)
    if nm == "aile_22k":
        f2 = df[bh(df["p1"].values)]
        print("  aile tek yönlü BH geçenler (sym sayısı):", f2.sym.value_counts().head(15).to_dict())

# Ajanın kendi 1302 testi: iki yönlü p -> tek yönlü (pozitif etki) p'ye çevir
f = pd.read_csv(os.path.join(ROOT, "sonuclar/aile_sektor_tematik/fdr_tum_testler.csv"))
f["p1"] = np.where(f["t"] > 0, f["p"] / 2, 1 - f["p"] / 2)
f["bh1"] = bh(f["p1"].values)
print("\nAjanın 1302 testi: iki yönlü BH geçen", int(f["fdr10"].sum()), "| tek yönlü (pozitif) BH geçen", int(f["bh1"].sum()))
print(f[f["bh1"]][["kaynak", "test", "t", "p1", "etki_bp"]].sort_values("p1").to_string())
# S1'den bağımsız (yarı iletken/teknoloji dışı) pozitif geçen var mı?
