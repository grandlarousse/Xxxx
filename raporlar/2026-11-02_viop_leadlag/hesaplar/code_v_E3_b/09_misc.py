import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_E3_b")
"""09: (a) IS-yalnız taramada BH-FDR geçenler OOS'ta tutuyor mu? (b) gap / gün-içi payı. (c) z>1 günlerinin BIST tatil-sonrası ve Pazartesi kırılımı."""
import vb, numpy as np, pandas as pd
from scipy import stats as st
R = pd.read_csv(vb.RES + "/03_tuprs_scan.csv", index_col=0)
R = R.drop(index=["USREF", "OUTREF"], errors="ignore")
R["p_is"] = 2 * st.norm.sf(R.t_is.abs())
o = R.p_is.sort_values(); n = len(o); q = o.values * n / np.arange(1, n + 1); q = np.minimum.accumulate(q[::-1])[::-1]
R.loc[o.index, "padj_is"] = q
P = R[R.padj_is < 0.05].sort_values("p_is")
P["oos_aligned"] = np.sign(P.t_is) * P.t_oos
print(f"(a) IS-yalnız tarama: {n} sürücü, BH q<0,05 geçen: {len(P)}; OOS'ta aynı işaret ve t>1,96: {(P.oos_aligned > 1.96).sum()}")
print(P[["group", "t_is", "padj_is", "t_oos"]].round(3).to_string())
F = pd.read_parquet(vb.RES + "/F.parquet"); G = F[F.index >= "2014"]
print("\n(b) gap ve gün-içi betaları (ham TUPRS), A_USREF:")
for pk, m in [("ALL", G.index >= "2014"), ("IS", G.index < vb.SPLIT), ("OOS", G.index >= vb.SPLIT)]:
    g = G[m]; pg, tg, _ = vb.nw(g.tu_gap, g[["A_USREF"]]); pi, ti, _ = vb.nw(g.y_raw, g[["A_USREF"]]); pc, tc, _ = vb.nw(g.tu_cc, g[["A_USREF"]])
    print(f"  {pk}: gap b {pg['A_USREF']:.3f} (t {tg['A_USREF']:.2f}) | gün-içi b {pi['A_USREF']:.3f} (t {ti['A_USREF']:.2f}) | cc b {pc['A_USREF']:.3f} (t {tc['A_USREF']:.2f}) | gün-içi payı {pi['A_USREF']/(pg['A_USREF']+pi['A_USREF']):.2f}")
    pgh, tgh, _ = vb.nw(g.tu_gap - g.xu_gap, g[["A_USREF"]]); pih, tih, _ = vb.nw(g.y_h, g[["A_USREF"]])
    print(f"       hedge'li: gap b {pgh['A_USREF']:.3f} (t {tgh['A_USREF']:.2f}) | gün-içi b {pih['A_USREF']:.3f} (t {tih['A_USREF']:.2f}) | pay {pih['A_USREF']/(pgh['A_USREF']+pih['A_USREF']):.2f}")
# (c) sinyal olan günlerin hafta günü kırılımı
pnl, pos = vb.bt(F.A_USREF, F.y_raw, 1.0); a = (pos != 0) & (pnl.index >= "2014")
dw = pnl[a].groupby(pnl[a].index.dayofweek).agg(["mean", "count"]); dw["mean"] *= 1e4
print("\n(c) hafta günü (0=Pzt) |z|>1 brüt bps:"); print(dw.round(1).T.to_string())
# (d) sinyal büyüklüğü kovaları (doğrusallık)
z = vb.zsig(F.A_USREF.dropna(), 250).reindex(F.index); g = pd.DataFrame({"z": z, "y": F.y_raw, "yh": F.y_h}).dropna(); g = g[g.index >= "2014"]
g["b"] = pd.cut(g.z, [-99, -2, -1, -0.5, 0, 0.5, 1, 2, 99])
print("\n(d) z kovası -> ortalama ham ve hedge'li gün-içi (bps):"); print((g.groupby("b")[["y", "yh"]].mean() * 1e4).round(1).assign(n=g.groupby("b").size()).T.to_string())
