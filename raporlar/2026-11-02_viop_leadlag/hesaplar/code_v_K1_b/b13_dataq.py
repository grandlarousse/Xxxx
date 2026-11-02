"""Açılış verisi kalitesi yıllara göre (CIMSA, OYAKC, XU100) + en iyi işlemlerin günleri."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_K1_b")
from kb import *
X = daily("XU100", is_index=True)
for s in ["CIMSA", "OYAKC"]:
    d = daily(s); r = raw_daily(s); r = r[r.index >= "2014-01-01"]
    pc = r.c.shift(1)
    q = pd.DataFrame({
        "o==önceki_c": (r.o == pc), "o==h": (r.o == r.h), "o==l": (r.o == r.l), "o==c": (r.o == r.c), "o==h==l": (r.o == r.h) & (r.o == r.l)}).groupby(r.index.year).mean().round(3)
    q["corr(gap,XU100gap)"] = pd.concat([d.gap, X.gap.rename("m")], axis=1).dropna().groupby(lambda x: x.year).apply(lambda z: z.iloc[:, 0].corr(z.m)).round(2)
    q["sd_gap_bps"] = (d.gap.groupby(d.index.year).std() * 1e4).round(0)
    q["sd_intra_bps"] = (d.intra.groupby(d.index.year).std() * 1e4).round(0)
    q["corr(gap,intra)"] = d[["gap", "intra"]].dropna().groupby(lambda x: x.year).apply(lambda z: z.gap.corr(z.intra)).round(3)
    q["n|gap|>1%"] = (d.gap.abs() > 0.01).groupby(d.index.year).sum()
    print(s); print(q.to_string())
    x = fade(d.gap, d.intra); best = x.sort_values(ascending=False).head(12).index
    print(d.loc[best, ["o", "h", "l", "c", "cc", "gap", "intra"]].assign(pnl=x.loc[best]).round(4).to_string())
