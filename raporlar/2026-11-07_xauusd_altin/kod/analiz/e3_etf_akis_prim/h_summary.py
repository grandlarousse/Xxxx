"""Kayıt özeti: test sayısı, aile bazında, BH-FDR (ajan içi)."""
from common import *
from lib_altin import bh_fdr
R = pd.read_csv(f"{S}/out/registry/{AGENT}.csv")
print("toplam kayıtlı test:", len(R))
print(R.groupby("family").size().to_string())
R["q_bh"] = np.nan
m = R.p.notna()
R.loc[m, "q_bh"] = bh_fdr(R.loc[m, "p"].values)
R["bonf_ok"] = R.p < 0.05 / m.sum()
R.to_csv(f"{OUT}/h_registry_with_fdr.csv", index=False)
cols = ["family", "test_id", "h", "n", "ic", "t", "t_is", "t_oos", "yrs_same_sign", "yrs", "q_bh", "bonf_ok"]
print(R[m].sort_values("p").head(45)[cols].round(4).to_string())
print("q<0.05 sayısı:", int((R.q_bh < 0.05).sum()), " | Bonferroni geçen:", int(R.bonf_ok.sum()))
print("tanı/işlem dışı aileler hariç q<0.05:", R[(R.q_bh < 0.05) & ~R.family.str.contains("diag|reverse|intraday|lasthour")][cols].round(4).to_string())
