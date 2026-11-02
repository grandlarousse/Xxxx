"""Fon krizi (01.09–30.10.2026) kesiti: hangi hisseler düştü? kriz getirisi ~ kriz öncesi getiri (Oca–Ağu 2026), likidite (TL hacim), VİOP/BIST100 üyeliği."""
from ye_common import *
cat = pd.read_csv(SCR + "/data/catalog.csv"); B = cat[cat.group.isin(["VIOP", "BIST_other"])].sym
STK = [s for s in B if not s.startswith("X")]
R = pd.DataFrame({s[:-3]: stk_ret(s) for s in STK}); TV = pd.DataFrame({s[:-3]: turnover(s) for s in STK}).reindex(R.index)
W = pd.read_parquet(RES + "/weights.parquet")
in100 = set(W["XU100"].iloc[-1].dropna()[lambda x: x > 0.001].index) if "XU100" in W.columns.get_level_values(0) else set()
cr = 100 * (np.exp(R.loc["2026-09-01":"2026-10-30"].sum(min_count=20)) - 1)
pre = 100 * (np.exp(R.loc["2026-01-01":"2026-08-31"].sum(min_count=60)) - 1)
lt = np.log(TV.loc["2026-06-01":"2026-08-31"].median())
dd = R.loc["2026-09-01":"2026-10-30"]; taban = (dd < np.log(0.905)).sum()
D = pd.DataFrame({"crisis_%": cr, "pre_2026_%": pre, "log_turnover_JunAug": lt, "taban_gun": taban, "viop": [s in VIOP for s in R.columns], "nnls_xu100": [s in in100 for s in R.columns]}).dropna(subset=["crisis_%"])
print("n =", len(D))
print("Spearman(kriz, kriz öncesi 2026):", round(D["crisis_%"].corr(D["pre_2026_%"], method="spearman"), 3), " Spearman(kriz, log hacim):", round(D["crisis_%"].corr(D["log_turnover_JunAug"], method="spearman"), 3))
print("medyan kriz getirisi: VİOP", round(D[D.viop]["crisis_%"].median(), 1), "| VİOP dışı", round(D[~D.viop]["crisis_%"].median(), 1), "| NNLS-XU100 ağırlıklı", round(D[D.nnls_xu100]["crisis_%"].median(), 1), "| diğer", round(D[~D.nnls_xu100]["crisis_%"].median(), 1))
D["pre_q"] = pd.qcut(D["pre_2026_%"].rank(method="first"), 5, labels=["P1 düşük", "P2", "P3", "P4", "P5 yüksek"])
print(D.groupby("pre_q")[["crisis_%", "taban_gun"]].median().round(1).to_string())
print("en kötü 15:", D.sort_values("crisis_%").head(15)[["crisis_%", "pre_2026_%", "taban_gun", "viop"]].round(1).to_string())
print("VİOP en kötü 8:", D[D.viop].sort_values("crisis_%").head(8)[["crisis_%", "pre_2026_%"]].round(1).to_string())
D.to_csv(RES + "/fon_krizi_kesit.csv")
