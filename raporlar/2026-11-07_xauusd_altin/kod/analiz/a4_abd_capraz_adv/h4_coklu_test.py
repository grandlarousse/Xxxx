"""h4: çoklu test. (1) Bonferroni / Holm / BH: a4 birincil (1.071), a4 tümü (1.213), proje kaydının tamamı (tüm ajanlar).
(2) Dairesel kaydırma (circular shift) permütasyonu: hedef v_ret serisi rastgele ≥250 gün kaydırılır (öngörücülerin kendi yapısı korunur),
madenci ailesi (11 madenci beta-artığı + 3 ETF oran × h∈{1,3,5}) içinde max |t| dağılımı → aile-düzeyi p.
(3) 'IS'te seçilen 33 kuraldan en az biri OOS'ta |t|≥t* aynı işaretli' olasılığı (bağımsızlık yaklaşımı)."""
import sys, glob, json; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a4_abd_capraz_adv")
from adv_common import *
from scipy import stats as st
rng = np.random.default_rng(7)

def holm(p):
    p = np.asarray(p, float); n = len(p); o = np.argsort(p); adj = np.empty(n)
    adj[o] = np.minimum(1, np.maximum.accumulate(p[o] * (n - np.arange(n))))
    return adj

reg = pd.read_csv(f"{S}/out/a4_abd_capraz/kayit_fdr_birincil.csv")
allr = pd.read_csv(f"{S}/out/registry/a4_abd_capraz.csv")
proj = pd.concat([pd.read_csv(f) for f in glob.glob(f"{S}/out/registry/*.csv")], ignore_index=True)
proj["p"] = pd.to_numeric(proj["p"], errors="coerce")
print("Proje kaydı satır:", len(proj), "geçerli p:", proj.p.notna().sum(), "ajan:", proj.agent.nunique())
targets = {"C1": "s2_artik_y_GDXJ_w1_h3", "C1b_kompozit(s4)": "s4_C1b_madenci_kompozit_bt_oos", "C2": "s1_ic_curve_10_2_w5_h1", "D1": "s1_emilim_y_DX_Y_NYB_w1"}
for nm, U in (("a4 birincil", reg), ("a4 tümü", allr), ("proje tümü", proj)):
    U = U[U.p.notna()].copy(); U["bonf"] = np.minimum(1, U.p * len(U)); U["holm"] = holm(U.p.values); U["bh"] = bh_fdr(U.p.values)
    print(f"== {nm}: n={len(U)}  Bonferroni p eşiği={0.05/len(U):.2e} (|t|>{st.norm.isf(0.025/len(U)):.2f})  min BH q={U.bh.min():.3f}  BH q<0.10 sayısı={(U.bh < 0.10).sum()}")
    for k, tid in targets.items():
        r = U[U.test_id.astype(str).str.startswith(tid)]
        if len(r): print(f"   {k:18s} {tid}: t={r.t.iloc[0]:.2f} p={r.p.iloc[0]:.2e} Bonf={r.bonf.iloc[0]:.3f} Holm={r.holm.iloc[0]:.3f} BH q={r.bh.iloc[0]:.3f}")

# ---------- (2) dairesel kaydırma
d = load_viop(); idx = d.index
def fast_rank_t(x, y, L):
    m = np.isfinite(x) & np.isfinite(y); x = x[m]; y = y[m]
    rx = st.rankdata(x); ry = st.rankdata(y); rx = (rx - rx.mean()) / rx.std(); ry = (ry - ry.mean()) / ry.std()
    n = len(rx); b = (rx * ry).sum() / (rx * rx).sum(); e = ry - b * rx; u = rx * e
    S0 = (u * u).sum()
    for l in range(1, L + 1):
        w = 1 - l / (L + 1); S0 += 2 * w * (u[l:] * u[:-l]).sum()
    se = np.sqrt(S0) / (rx * rx).sum()
    return b / se
miners = ["y_GDX", "y_GDXJ", "y_RING", "y_SIL", "y_NEM", "y_AEM", "y_B", "y_KGC", "y_FNV", "y_WPM", "y_RGLD"]
X = {m: miner_resid(d, m).values for m in miners}
for m in ["y_GDX", "y_GDXJ", "y_RING"]:
    X["oran_" + m] = zscale(np.log(d[m] / d.y_GLD).diff()).values
ret = d.v_ret.values
def family_max(r):
    best = 0
    for h in (1, 3, 5):
        y = sum(np.roll(r, -k) for k in range(1, h + 1)).astype(float); y[-h:] = np.nan
        for k, x in X.items():
            t = fast_rank_t(x, y, max(h, 5)); best = max(best, abs(t))
    return best
obs = family_max(ret)
print("gözlenen aile max |t| (", len(X) * 3, "test):", round(obs, 2))
N = 300; null = []
for i in range(N):
    sh = int(rng.integers(250, len(ret) - 250))
    null.append(family_max(np.roll(ret, sh)))
null = np.array(null)
print(f"dairesel kaydırma (N={N}): null max|t| medyan={np.median(null):.2f}, %95={np.quantile(null, .95):.2f}, %99={np.quantile(null, .99):.2f}; aile-düzeyi p(max≥gözlenen)={(null >= obs).mean():.3f}")
# tek test (GDXJ h3) kaydırma null
y3 = d.fwd3.values
t_obs = fast_rank_t(X["y_GDXJ"], y3, 5)
nul1 = []
for i in range(1000):
    sh = int(rng.integers(250, len(ret) - 250)); r = np.roll(ret, sh)
    y = (np.roll(r, -1) + np.roll(r, -2) + np.roll(r, -3)).astype(float); y[-3:] = np.nan
    nul1.append(fast_rank_t(X["y_GDXJ"], y, 5))
nul1 = np.array(nul1)
print(f"GDXJ h3 tek test: t={t_obs:.2f}; kaydırma null sd={nul1.std():.2f}; p(|t|≥gözlenen)={(np.abs(nul1) >= abs(t_obs)).mean():.4f}")

# ---------- (3) 33 IS-seçimli kuraldan en az birinin OOS'ta tesadüfen geçmesi
for tstar in (2.0, 2.39, 2.63):
    p1 = st.norm.sf(tstar)  # tek yönlü (aynı işaret)
    for K in (33, 11):
        print(f"K={K} bağımsız kural, OOS aynı işaret t≥{tstar}: P(en az 1)={1 - (1 - p1) ** K:.3f}  beklenen sayı={K * p1:.2f}")
