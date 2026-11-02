"""10:30 girişi yarıyıllık istikrar (ham ve XU030 hedge'li), CIMSA/OYAKC + düşük likidite havuzu."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_K1_b")
from kb import *
P = pd.read_parquet(OUT + "/panel_b.parquet")
X = daily("XU030", is_index=True); hx = h1("XU030"); f = hx[hx.hm == 630].set_index("day")
X["m_r2"] = np.log(X.c / f.c.reindex(X.index)); P = P.merge(X[["m_r2"]], left_on="date", right_index=True, how="left")
P = P[(P.gap.abs() > 0.01) & P.r2.notna()].copy(); P["sg"] = -np.sign(P.gap)
P["raw"] = P.sg * P.r2 * 1e4 - 10; P["hed"] = P.sg * (P.r2 - P.m_r2) * 1e4 - 13
P["hy"] = P.date.dt.year.astype(str) + "H" + np.where(P.date.dt.month <= 6, "1", "2")
for who, df in [("CIMSA", P[P.sym == "CIMSA"]), ("OYAKC", P[P.sym == "OYAKC"]), ("dusuk", P[P.liqT == "dusuk"])]:
    g = df.groupby("hy").agg(n=("raw", "size"), ham=("raw", "mean"), hedge=("hed", "mean")).round(1)
    print(who, g.T.to_string(), "\n  ham>0 yarıyıl:", (g.ham > 0).sum(), "/", len(g), " hedge>0:", (g.hedge > 0).sum(), "/", len(g))
