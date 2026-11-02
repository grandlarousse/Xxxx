"""Adım 2b/3: Çoklu test (BH-FDR), kaydırılmış null, IS->OOS ve PRE (2005–2013) replikasyonu, hacim filtresi, bayat fiyat bayrağı,
lider/takipçi asimetrisi ve yıllara göre istikrar.
Girdi: res/scan_long.parquet, res/null_t.npz, res/volfilt.parquet. Çıktı: res/fdr.txt, res/pairs_sig.parquet, res/leader_scores.csv,
y_hisse_matrix.parquet (out/)
"""
import sys, os, numpy as np, pandas as pd
from scipy import stats
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hdata
sys.path.insert(0, hdata.SCR + "/code"); import ll
S = pd.read_parquet(os.path.join(hdata.RES, "scan_long.parquet"))
for c in ["target", "leader", "dep", "lag", "period"]: S[c] = S[c].astype(str)
S = S[S.target != S.leader]
S["p"] = 2 * stats.norm.sf(S["t"].abs())
liq = hdata.load()["liq"]
TGT = hdata.VIOP
out = []
def P(*a):
    s = " ".join(str(x) for x in a); out.append(s); print(s, flush=True)

# ---------- pivot: her (target, leader, dep, lag) için dönem sütunları ----------
W = S.pivot_table(index=["target", "leader", "dep", "lag"], columns="period", values=["b", "t", "pc", "n"], aggfunc="first")
W.columns = [f"{a}_{b}" for a, b in W.columns]
W = W.reset_index()
W["p_FULL"] = 2 * stats.norm.sf(W["t_FULL"].abs()); W["p_IS"] = 2 * stats.norm.sf(W["t_IS"].abs()); W["p_OOS"] = 2 * stats.norm.sf(W["t_OOS"].abs())
W["p_PRE"] = 2 * stats.norm.sf(W["t_PRE"].abs()) if "t_PRE" in W else np.nan
ok = W["t_FULL"].notna()
P(f"Toplam test (FULL, tüm dep x lag): {int(ok.sum())}  | hedef {W.target.nunique()} x lider {W.leader.nunique()}")
# aile: dep (tüm laglar birlikte)
W["bh_dep"] = False; W["padj_dep"] = np.nan; W["bh_deplag"] = False; W["bh_all"] = False
for d in W.dep.unique():
    m = ok & (W.dep == d)
    rej, pa = ll.fdr(W.loc[m, "p_FULL"].values, 0.05); W.loc[m, "bh_dep"] = rej; W.loc[m, "padj_dep"] = pa
    for k in W.lag.unique():
        mk = m & (W.lag == k)
        if mk.sum():
            rej, _ = ll.fdr(W.loc[mk, "p_FULL"].values, 0.05); W.loc[mk, "bh_deplag"] = rej
rej, pa = ll.fdr(W.loc[ok, "p_FULL"].values, 0.05); W.loc[ok, "bh_all"] = rej; W.loc[ok, "padj_all"] = pa
# IS-aile BH
W["bh_IS"] = False
for d in W.dep.unique():
    for k in W.lag.unique():
        mk = (W.dep == d) & (W.lag == k) & W["t_IS"].notna()
        if mk.sum():
            rej, _ = ll.fdr(W.loc[mk, "p_IS"].values, 0.05); W.loc[mk, "bh_IS"] = rej
W["rep_OOS"] = (np.sign(W["t_OOS"]) == np.sign(W["t_IS"])) & (W["p_OOS"] < 0.05)
W["same_sign_OOS"] = np.sign(W["t_OOS"]) == np.sign(W["t_FULL"])
W["rep_PRE"] = (np.sign(W["t_PRE"]) == np.sign(W["t_FULL"])) & (W["p_PRE"] < 0.05)

# ---------- null ----------
Z = np.load(os.path.join(hdata.RES, "null_t.npz"), allow_pickle=True)
NT = Z["t"]; ntg = list(Z["targets"]); nld = list(Z["leaders"]); ndeps = list(Z["deps"]); nper = list(Z["periods"])
selfmask = np.array([[t == l for l in nld] for t in ntg])  # (47,177)
P("\n=== Aile özeti (lag ve dep bazında; FULL 2014–2026) ===")
P("dep  lag  test  p<0.05  |t|>3  BH05(dep,lag)  BH05(dep-ailesi)  pozitif%  IS-BH  OOS-rep%  PRE-rep%(cc)  null: p<0.05 ort | |t|>3 ort | p<=p* ort (beklenen sahte) | null BH05 ort")
fam_rows = []
for d in ["cc", "gap", "intra", "intra_g"]:
    for k in ["1", "2", "3", "4", "5", "c5"]:
        m = ok & (W.dep == d) & (W.lag == k)
        if not m.sum(): continue
        x = W[m]; nt = len(x); n05 = int((x.p_FULL < 0.05).sum()); n3 = int((x.t_FULL.abs() > 3).sum())
        nb = int(x.bh_deplag.sum()); nbd = int(x.bh_dep.sum()); pos = 100 * (x.loc[x.bh_deplag, "t_FULL"] > 0).mean() if nb else np.nan
        isb = int(x.bh_IS.sum()); rep = 100 * x.loc[x.bh_IS, "rep_OOS"].mean() if isb else np.nan
        prer = 100 * x.loc[x.bh_deplag, "rep_PRE"].mean() if (nb and d == "cc" and k in ("1", "c5")) else np.nan
        nul = {}
        if k == "1" and d in ndeps:
            di = ndeps.index(d); fi = nper.index("FULL")
            tn = NT[:, :, di, fi, :].astype(float); tn[:, selfmask] = np.nan
            pn = 2 * stats.norm.sf(np.abs(tn))
            pstar = x.loc[x.bh_deplag, "p_FULL"].max() if nb else 0.05 * 1 / nt
            nul = {"n05": np.nanmean([(pn[s] < 0.05).sum() for s in range(len(pn))]),
                   "n3": np.nanmean([(np.abs(tn[s]) > 3).sum() for s in range(len(pn))]),
                   "nstar": np.nanmean([(pn[s] <= pstar).sum() for s in range(len(pn))]),
                   "nbh": np.nanmean([ll.fdr(pn[s][np.isfinite(pn[s])], 0.05)[0].sum() for s in range(len(pn))])}
        fam_rows.append(dict(dep=d, lag=k, tests=nt, p05=n05, t3=n3, bh=nb, bh_fam=nbd, pos_pct=pos, is_bh=isb, oos_rep=rep, pre_rep=prer, **{f"null_{a}": b for a, b in nul.items()}))
        P(f"{d:7s} {k:3s} {nt:5d} {n05:6d} {n3:5d} {nb:6d} {nbd:6d} {pos if pos==pos else float('nan'):6.1f} {isb:5d} {rep if rep==rep else float('nan'):6.1f} {prer if prer==prer else float('nan'):6.1f}   "
          + (f"{nul['n05']:.0f} | {nul['n3']:.1f} | {nul['nstar']:.1f} | {nul['nbh']:.1f}" if nul else ""))
fam = pd.DataFrame(fam_rows); fam.to_csv(os.path.join(hdata.RES, "family_summary.csv"), index=False)
P(f"Toplam BH05(dep-ailesi) keşif: {int(W.bh_dep.sum())}; tüm-test BH05: {int(W.bh_all.sum())}")

# null replikasyon: IS top-200 |t| -> OOS aynı işaret & p<0.05 (gerçek vs null)
P("\n=== IS top-200 (|t_IS|) -> OOS replikasyon (lag1): gerçek vs null ===")
for d in ["cc", "gap", "intra"]:
    m = ok & (W.dep == d) & (W.lag == "1") & W.t_IS.notna()
    x = W[m].copy(); x["a"] = x.t_IS.abs(); top = x.nlargest(200, "a")
    real = 100 * top.rep_OOS.mean()
    di = ndeps.index(d); ii = nper.index("IS"); oi = nper.index("OOS")
    rr = []
    for s in range(NT.shape[0]):
        ti = NT[s, :, di, ii, :].astype(float).copy(); to = NT[s, :, di, oi, :].astype(float).copy(); ti[selfmask] = np.nan
        f = np.argsort(-np.nan_to_num(np.abs(ti).ravel(), nan=-1))[:200]
        a = ti.ravel()[f]; b = to.ravel()[f]
        rr.append(100 * np.mean((np.sign(a) == np.sign(b)) & (2 * stats.norm.sf(np.abs(b)) < 0.05)))
    P(f"{d}: gerçek {real:.1f}%  null ort {np.mean(rr):.1f}% (maks {np.max(rr):.1f}%)  | top-200 IS |t| aralığı {top.a.min():.2f}-{top.a.max():.2f}")

# ---------- hacim filtresi ve bayat fiyat ----------
V = pd.read_parquet(os.path.join(hdata.RES, "volfilt.parquet"))
for c in ["target", "leader", "dep", "lag", "period"]: V[c] = V[c].astype(str)
V = V[V.period == "FULL"][["target", "leader", "dep", "t", "b"]].rename(columns={"t": "t_volf", "b": "b_volf"})
W = W.merge(V.assign(lag="1"), on=["target", "leader", "dep", "lag"], how="left")
W["liq_ratio"] = (liq["tov_med_oos_mnTL"].reindex(W.leader).values / liq["tov_med_oos_mnTL"].reindex(W.target).values)
W["stale_flag"] = W["liq_ratio"] > 3
P("\n=== Hacim filtresi (lag1, FULL-BH keşifleri): filtre sonrası aynı işaret & |t|>2 oranı ===")
for d in ["cc", "gap", "intra"]:
    x = W[(W.dep == d) & (W.lag == "1") & W.bh_deplag]
    if len(x):
        P(f"{d}: keşif {len(x)}; filtre sonrası korunan {100*((np.sign(x.t_volf)==np.sign(x.t_FULL))&(x.t_volf.abs()>2)).mean():.1f}%; "
          f"medyan |t| {x.t_FULL.abs().median():.2f} -> {x.t_volf.abs().median():.2f}; lider/hedef likidite oranı>3 (bayat riski) payı {100*x.stale_flag.mean():.1f}%")
# likit-lider/illikit-hedef: likidite oranına göre keşif yoğunluğu
P("\n=== Likidite oranı (lider/hedef OOS medyan TL hacmi) kovalarına göre lag1 cc keşif oranı ve ort. t ===")
x = W[ok & (W.dep == "cc") & (W.lag == "1")].copy()
x["kova"] = pd.cut(np.log10(x.liq_ratio), [-9, -1, -0.5, 0, 0.5, 1, 9], labels=["<0.1", "0.1-0.3", "0.3-1", "1-3", "3-10", ">10"])
P(x.groupby("kova").apply(lambda g: pd.Series({"n": len(g), "bh%": 100 * g.bh_deplag.mean(), "ort_t": g.t_FULL.mean(), "pos_bh": int((g.bh_deplag & (g.t_FULL > 0)).sum()), "neg_bh": int((g.bh_deplag & (g.t_FULL < 0)).sum())})).round(2).to_string())

# ---------- lider/takipçi asimetrisi ----------
P("\n=== Lider skorları (cc lag1 FULL; BH(dep,lag) keşif sayısı, + ve −) ===")
x = W[ok & (W.dep == "cc") & (W.lag == "1")]
ls = x.groupby("leader").agg(n_pos=("bh_deplag", lambda s: int((s & (x.loc[s.index, "t_FULL"] > 0)).sum())),
                             n_neg=("bh_deplag", lambda s: int((s & (x.loc[s.index, "t_FULL"] < 0)).sum())),
                             mean_t=("t_FULL", "mean"), mean_abs_t=("t_FULL", lambda s: s.abs().mean()))
xi = W[ok & (W.dep == "intra") & (W.lag == "1")]
ls["intra_n_bh"] = xi.groupby("leader")["bh_deplag"].sum(); ls["intra_mean_t"] = xi.groupby("leader")["t_FULL"].mean()
xg = W[ok & (W.dep == "gap") & (W.lag == "1")]
ls["gap_n_bh"] = xg.groupby("leader")["bh_deplag"].sum(); ls["gap_mean_t"] = xg.groupby("leader")["t_FULL"].mean()
ls["tov_oos"] = liq["tov_med_oos_mnTL"].reindex(ls.index); ls["sector"] = liq["sector"].reindex(ls.index); ls["viop"] = ls.index.isin(TGT)
# yıllık istikrar: her yıl lider ort. t (47 hedef üzerinden)
Y = S[(S.dep == "cc") & (S.lag == "1") & S.period.str.startswith("Y")]
yt = Y.groupby(["leader", "period"])["t"].mean().unstack()
ls = ls.join(yt.add_prefix("mt_"))
ls["n_bh"] = ls.n_pos + ls.n_neg
ls = ls.sort_values("n_bh", ascending=False)
ls.to_csv(os.path.join(hdata.RES, "leader_scores.csv"))
P(ls[["n_pos", "n_neg", "mean_t", "intra_n_bh", "intra_mean_t", "gap_n_bh", "gap_mean_t", "tov_oos", "sector"]].head(30).round(2).to_string())
P("\nEn negatif ort. t (cc) liderler:"); P(ls.sort_values("mean_t")[["n_pos", "n_neg", "mean_t", "intra_mean_t", "tov_oos", "sector"]].head(12).round(2).to_string())
yrs = [c for c in ls.columns if c.startswith("mt_Y")]
rc = ls[yrs].corr(method="spearman")
cons = [rc.iloc[i, i + 1] for i in range(len(yrs) - 1)]
P(f"\nLider ort-t sıralamasının ardışık yıllar Spearman korelasyonu: " + ", ".join(f"{yrs[i][4:]}->{yrs[i+1][4:]}: {c:.2f}" for i, c in enumerate(cons)))
isy = [c for c in yrs if int(c[4:]) < 2021]; oosy = [c for c in yrs if int(c[4:]) >= 2021]
a = ls[isy].mean(1); b = ls[oosy].mean(1)
P(f"IS (2014–20) vs OOS (2021–26) lider ort-t Spearman: {a.corr(b, method='spearman'):.2f} (n={int((a.notna()&b.notna()).sum())})")
P(f"Lider ort-t ile likidite (log TL hacim) Spearman: {ls.mean_t.corr(np.log(ls.tov_oos), method='spearman'):.2f}")
# takipçi skorları
fs = x.groupby("target").agg(n_bh=("bh_deplag", "sum"), n_pos=("bh_deplag", lambda s: int((s & (x.loc[s.index, "t_FULL"] > 0)).sum())), mean_t=("t_FULL", "mean"))
fs["intra_n_bh"] = xi.groupby("target")["bh_deplag"].sum(); fs["gap_n_bh"] = xg.groupby("target")["bh_deplag"].sum()
yf = Y.groupby(["target", "period"])["t"].mean().unstack(); fs = fs.join(yf.add_prefix("mt_"))
fs["tov_oos"] = liq["tov_med_oos_mnTL"].reindex(fs.index)
fs = fs.sort_values("n_bh", ascending=False); fs.to_csv(os.path.join(hdata.RES, "follower_scores.csv"))
P("\n=== Takipçi skorları (hedef başına cc lag1 BH keşif) ==="); P(fs[["n_bh", "n_pos", "mean_t", "gap_n_bh", "intra_n_bh", "tov_oos"]].round(2).to_string())
fyrs = [c for c in fs.columns if c.startswith("mt_Y")]
a = fs[[c for c in fyrs if int(c[4:]) < 2021]].mean(1); b = fs[[c for c in fyrs if int(c[4:]) >= 2021]].mean(1)
P(f"Takipçi ort-t IS vs OOS Spearman: {a.corr(b, method='spearman'):.2f}")
# 47x47 yön asimetrisi
x47 = x[x.leader.isin(TGT)][["leader", "target", "t_FULL"]]
mrg = x47.merge(x47.rename(columns={"leader": "target", "target": "leader", "t_FULL": "t_rev"}), on=["leader", "target"])
mrg = mrg[mrg.leader < mrg.target]
mrg["asym"] = mrg.t_FULL - mrg.t_rev
P(f"\n47x47 çift yön asimetrisi: corr(t_ab, t_ba) = {mrg.t_FULL.corr(mrg.t_rev):.2f}; |t_ab - t_ba|>3 olan çift: {int((mrg.asym.abs()>3).sum())} / {len(mrg)}")
P(mrg.reindex(mrg.asym.abs().sort_values(ascending=False).index).head(15).round(2).to_string(index=False))

# en güçlü keşifler (FULL BH dep-ailesi), lag1 cc/gap/intra
cols = ["target", "leader", "dep", "lag", "b_FULL", "t_FULL", "pc_FULL", "t_IS", "t_OOS", "t_PRE", "t_volf", "liq_ratio", "n_FULL"]
for d in ["cc", "gap", "intra", "intra_g"]:
    xx = W[W.bh_dep & (W.dep == d)].copy(); xx["a"] = xx.t_FULL.abs()
    P(f"\n=== {d}: BH05 (dep ailesi) keşif {len(xx)}; lag dağılımı {xx.lag.value_counts().to_dict()}; pozitif {int((xx.t_FULL>0).sum())}; IS&OOS aynı işaret {int((np.sign(xx.t_IS)==np.sign(xx.t_OOS)).sum())} ===")
    P(xx.sort_values("a", ascending=False)[cols].head(40).round(3).to_string(index=False))
W.to_parquet(os.path.join(hdata.RES, "wide.parquet"))
# tam matris (out/)
keep = ["target", "leader", "dep", "lag", "b_FULL", "t_FULL", "pc_FULL", "n_FULL", "p_FULL", "padj_dep", "bh_dep", "bh_deplag", "b_IS", "t_IS", "b_OOS", "t_OOS",
        "t_PRE", "rep_OOS", "t_volf", "liq_ratio", "stale_flag"] + [c for c in W.columns if c.startswith("t_Y")]
W[[c for c in keep if c in W.columns]].to_parquet(os.path.join(hdata.OUT, "y_hisse_matrix.parquet"))
open(os.path.join(hdata.RES, "fdr.txt"), "w").write("\n".join(out))
