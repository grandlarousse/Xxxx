"""47 hisse corr(gap, intra): 2021+ ve 2016+; ayrıca koordinatör panelinde 2023-02-08 satırı var mı?"""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_K1_b")
from kb import *
P = pd.read_parquet(OUT + "/panel_b.parquet")
r = {}
for s, d in P.groupby("sym"):
    a = d[d.date >= "2021-01-01"][["gap", "intra"]].dropna(); b = d[d.date >= "2016-01-01"][["gap", "intra"]].dropna()
    r[s] = dict(c21=a.gap.corr(a.intra), c16=b.gap.corr(b.intra), c21_spear=a.gap.corr(a.intra, method="spearman"))
R = pd.DataFrame(r).T
print("2021+: min %.3f max %.3f medyan %.3f negatif %d/47 | spearman medyan %.3f negatif %d/47" % (R.c21.min(), R.c21.max(), R.c21.median(), (R.c21 < 0).sum(), R.c21_spear.median(), (R.c21_spear < 0).sum()))
print("2016+: min %.3f max %.3f medyan %.3f negatif %d/47" % (R.c16.min(), R.c16.max(), R.c16.median(), (R.c16 < 0).sum()))
print("en negatif 2021+:", R.c21.sort_values().head(5).round(3).to_dict(), " en pozitif:", R.c21.sort_values().tail(3).round(3).to_dict())
D = pd.read_parquet(S + "/data/panel_decomp_bist.parquet")
print("koordinatör paneli CIMSA 2023-02-06..16:"); print(D.loc["2023-02-06":"2023-02-16", [("CIMSA", "gap"), ("CIMSA", "intra")]].round(4))
