"""(i) Rapor tabloları (markdown) — CSV çıktılarından üretir: tablolar.md"""
import pandas as pd, numpy as np, os
OUT = os.path.dirname(os.path.abspath(__file__))
def md(df, floatfmt=2):
    df = df.copy()
    for c in df.columns:
        if df[c].dtype.kind == "f": df[c] = df[c].map(lambda v: "" if pd.isna(v) else f"{v:.{floatfmt}f}")
    h = "| " + " | ".join(map(str, df.columns)) + " |\n|" + "|".join(["---"] * len(df.columns)) + "|\n"
    return h + "\n".join("| " + " | ".join(map(str, r)) + " |" for r in df.values) + "\n"
o = []
def fam_table(f, title, early=None, hs=(1, 3, 5, 10)):
    d = pd.read_csv(f"{OUT}/{f}")
    d = d[d.h.isin(hs)]
    piv = d.pivot_table(index=["test_id", "predictor"], columns="h", values="t", aggfunc="first")
    piv.columns = [f"t(h={c})" for c in piv.columns]
    x = d[d.h == 5].set_index(["test_id", "predictor"])[["ic", "t_is", "t_oos", "yrs_same"]].rename(columns={"ic": "IC(h5)", "t_is": "t_IS(h5)", "t_oos": "t_OOS(h5)", "yrs_same": "yıl(h5)"})
    t = piv.join(x).reset_index()
    if early:
        e = pd.read_csv(f"{OUT}/{early}"); e = e[e.h == 5][["test_id", "t"]].rename(columns={"t": "t_2010-16(h5)"})
        t = t.merge(e, on="test_id", how="left")
    t = t.drop(columns=["test_id"])
    o.append(f"### {title}\n\n" + md(t) + "\n")
fam_table("a_cot_ic.csv", "(a) CFTC COT (kapanma dönemleri hariç)", "a_cot_early.csv")
fam_table("b_shfe_ic.csv", "(b) Şanghay primi, SHFE, 518880.SS", "b_shfe_early.csv")
fam_table("c_asia_ic.csv", "(c) Asya endeksleri ve Çin altın hisseleri", "c_asia_early.csv")
fam_table("d_gpr_ic.csv", "(d) GPR (ham dosyadan yeniden kuruldu)", "d_gpr_early.csv")
fam_table("e_viop_ic.csv", "(e) VİOP yerel konumlanma (t-1 bülteni)")
s = pd.read_csv(f"{OUT}/f_deep_summary.csv")
c1 = ["cand", "h", "rule", "t_full", "t_is", "t_oos", "yrs", "t_ctrl", "t_ctrl_is", "t_ctrl_oos", "t_exroll", "rule_bps", "rule_bps_dm"]
o.append("### (f) Adaylar — kontrollü regresyon ve dışlamalar\n\n" + md(s[c1]) + "\n")
c2 = ["cand", "h", "rule", "sh_full", "sh_is", "sh_oos", "sh_oos_dm", "sh_oos_10bps", "long_oos", "long_oos_dm", "short_oos", "short_oos_dm", "bh_oos", "sig_changes_yr"]
o.append("### (f) Adaylar — işlem kuralı Sharpe (net 5 bps; 10 bps stres)\n\n" + md(s[c2]) + "\n")
y = pd.read_csv(f"{OUT}/f_deep_yearly_sharpe.csv")
o.append("### (f) Yıllık net Sharpe (5 bps)\n\n" + md(y) + "\n")
p = pd.read_csv(f"{OUT}/f_deep_placebo.csv")
o.append("### (f) Placebo (x'in kaydırılması; −1/−2 = gelecek bilgisi, yasak)\n\n" + md(p, 3) + "\n")
g = pd.read_csv(f"{OUT}/g_cn_variants.csv")[["test_id", "h", "n", "ic", "t", "t_is", "t_oos", "yrs_same"]]
o.append("### (g) Çin altın hisse artığı — varyantlar\n\n" + md(g, 3) + "\n")
q = pd.read_csv(f"{OUT}/g_cn_quintiles.csv").pivot(index="quintile", columns="period", values="fwd5_bps").reset_index()
o.append("### (g) Artık bileşik beşli dilimleri — ortalama fwd5 (bps)\n\n" + md(q, 1) + "\n")
open(f"{OUT}/tablolar.md", "w").write("# a6 tablo eki (otomatik)\n\n" + "\n".join(o))
print("ok")
