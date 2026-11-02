"""Adım 2d: Piyasa-göreli taramanın FDR / null / replikasyon özeti + en güçlü adaylar. Çıktı: res/rel.txt, res/wide_rel.parquet"""
import sys, os, numpy as np, pandas as pd
from scipy import stats
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hdata
sys.path.insert(0, hdata.SCR + "/code"); import ll
S = pd.read_parquet(os.path.join(hdata.RES, "scan_rel.parquet")); S = S[S.target != S.leader]
W = S.pivot_table(index=["target", "leader", "dep", "lag"], columns="period", values=["b", "t", "pc", "n"]).reset_index()
W.columns = ["_".join([a for a in c if a]) for c in W.columns]
for p in ["FULL", "IS", "OOS"]: W[f"p_{p}"] = 2 * stats.norm.sf(W[f"t_{p}"].abs())
W["bh"] = False; W["bh_IS"] = False
for d in W.dep.unique():
    for k in W.lag.unique():
        m = (W.dep == d) & (W.lag == k) & W.t_FULL.notna(); W.loc[m, "bh"] = ll.fdr(W.loc[m, "p_FULL"].values)[0]
        m2 = (W.dep == d) & (W.lag == k) & W.t_IS.notna(); W.loc[m2, "bh_IS"] = ll.fdr(W.loc[m2, "p_IS"].values)[0]
W["rep"] = (np.sign(W.t_IS) == np.sign(W.t_OOS)) & (W.p_OOS < 0.05)
Z = np.load(os.path.join(hdata.RES, "null_rel.npz"), allow_pickle=True); NT = Z["t"].astype(float)
tg = list(Z["targets"]); ld = list(Z["leaders"]); dps = list(Z["deps"]); prs = list(Z["periods"])
self_ = np.array([[a == b for b in ld] for a in tg])
out = []
def P(*a):
    s = " ".join(str(x) for x in a); out.append(s); print(s, flush=True)
P("Piyasa-göreli tarama (hedef - β_IS·XU100; kontroller + EW177): aile özeti")
P("dep lag test p<0.05 |t|>3 BH05 IS-BH OOS-rep% | null p<0.05 | null |t|>3 | null BH05 | IS top200 rep gerçek / null")
for d in ["cc_rel", "gap_rel", "intra_rel"]:
    for k in ["1", "2", "c5"]:
        x = W[(W.dep == d) & (W.lag == k) & W.t_FULL.notna()]
        s = f"{d:9s} {k:3s} {len(x):5d} {int((x.p_FULL<0.05).sum()):5d} {int((x.t_FULL.abs()>3).sum()):4d} {int(x.bh.sum()):4d} {int(x.bh_IS.sum()):4d} {100*x.loc[x.bh_IS,'rep'].mean() if x.bh_IS.sum() else float('nan'):5.1f}"
        xi = x.dropna(subset=["t_IS"]).copy(); xi["a"] = xi.t_IS.abs(); top = xi.nlargest(200, "a"); rr = 100 * top.rep.mean()
        if k == "1":
            di = dps.index(d); fi = prs.index("FULL"); ii = prs.index("IS"); oi = prs.index("OOS")
            tn = NT[:, :, di, fi, :].copy(); tn[:, self_] = np.nan; pn = 2 * stats.norm.sf(np.abs(tn))
            n05 = np.nanmean([(pn[i] < 0.05).sum() for i in range(len(pn))]); n3 = np.nanmean([(np.abs(tn[i]) > 3).sum() for i in range(len(pn))])
            nbh = np.mean([ll.fdr(pn[i][np.isfinite(pn[i])])[0].sum() for i in range(len(pn))])
            reps = []
            for i in range(len(pn)):
                a = NT[i, :, di, ii, :].copy(); b = NT[i, :, di, oi, :].copy(); a[self_] = np.nan
                f = np.argsort(-np.nan_to_num(np.abs(a).ravel(), nan=-1))[:200]
                reps.append(100 * np.mean((np.sign(a.ravel()[f]) == np.sign(b.ravel()[f])) & (np.abs(b.ravel()[f]) > 1.96)))
            s += f" | {n05:.0f} | {n3:.1f} | {nbh:.2f} | {rr:.1f} / {np.mean(reps):.1f} (maks {np.max(reps):.1f})"
        else:
            s += f" | - | - | - | {rr:.1f} / -"
        P(s)
liq = hdata.load()["liq"]
W["liq_ratio"] = liq["tov_med_oos_mnTL"].reindex(W.leader).values / liq["tov_med_oos_mnTL"].reindex(W.target).values
cols = ["target", "leader", "dep", "lag", "b_FULL", "t_FULL", "pc_FULL", "t_IS", "t_OOS", "liq_ratio", "n_FULL"]
x = W[W.bh].copy(); P(f"\nBH05 keşifleri ({len(x)}):"); P(x.sort_values("t_FULL")[cols].round(3).to_string(index=False))
x = W[(W.lag == "1")].copy(); x["a"] = x.t_FULL.abs()
x["both"] = (np.sign(x.t_IS) == np.sign(x.t_OOS)) & (x.t_IS.abs() > 2) & (x.t_OOS.abs() > 2)
P(f"\nlag1: IS ve OOS'ta ayrı ayrı |t|>2 ve aynı işaret olan çift sayısı: {int(x.both.sum())} (bağımsızlık altında beklenen ≈ {0.5*0.0455**2*len(x):.1f})")
P(x[x.both].sort_values("a", ascending=False)[cols].head(30).round(3).to_string(index=False))
W.to_parquet(os.path.join(hdata.RES, "wide_rel.parquet"))
open(os.path.join(hdata.RES, "rel.txt"), "w").write("\n".join(out))
# tam matrise ekle (dep = cc_rel/gap_rel/intra_rel)
M = pd.read_parquet(os.path.join(hdata.OUT, "y_hisse_matrix.parquet"))
M = M[~M.dep.astype(str).str.endswith("_rel")]
R = W.rename(columns={"bh": "bh_deplag"})[["target", "leader", "dep", "lag", "b_FULL", "t_FULL", "pc_FULL", "n_FULL", "p_FULL", "bh_deplag", "b_IS", "t_IS", "b_OOS", "t_OOS", "rep", "liq_ratio"]].rename(columns={"rep": "rep_OOS"})
R["stale_flag"] = R.liq_ratio > 3
pd.concat([M, R], ignore_index=True).to_parquet(os.path.join(hdata.OUT, "y_hisse_matrix.parquet"))
