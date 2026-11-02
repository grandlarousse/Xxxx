"""Yön karışımı plasebosu: strateji net short eğilimli mi? Koşulsuz gün-içi drift (10:30->kapanış ve açılış->kapanış) ne kadarını açıklar?"""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_K1_b")
from kb import *
P = pd.read_parquet(OUT + "/panel_b.parquet")
X = daily("XU030", is_index=True); hx = h1("XU030"); f = hx[hx.hm == 630].set_index("day")
X["m_r2"] = np.log(X.c / f.c.reindex(X.index)); P = P.merge(X[["m_r2", "gap", "intra"]].rename(columns={"gap": "m_gap", "intra": "m_intra"}), left_on="date", right_index=True, how="left")
rng = np.random.default_rng(3)
for s in ["CIMSA", "OYAKC"]:
    d = P[(P.sym == s)].copy()
    for lab, per, col in [("10:30", d.r2.notna(), "r2"), ("açılış OOS", (d.date > IS_END), "intra"), ("açılış IS", (d.date <= IS_END), "intra")]:
        z = d[per & d[col].notna() & d.gap.notna()]
        tr = z[z.gap.abs() > 0.01]; sg = -np.sign(tr.gap)
        act = (sg * tr[col] * 1e4).mean()
        frac_short = (sg < 0).mean(); mu_all = z[col].mean() * 1e4
        drift_part = ((sg * mu_all).mean())
        # rastgele gün, aynı long/short sayısı
        sims = []
        for b in range(3000):
            idx = rng.choice(len(z), len(tr), replace=True); sims.append((sg.values * z[col].values[idx] * 1e4).mean())
        sims = np.array(sims)
        mkt = (sg * tr.m_r2 * 1e4).mean() if col == "r2" else (sg * tr.m_intra * 1e4).mean()
        print(f"{s} {lab}: brüt fade {act:.1f} bps | short oranı {frac_short:.2f} | koşulsuz ort {col} {mu_all:.1f} bps -> yön karışımı drift payı {drift_part:.1f} | "
              f"rastgele gün plasebo ort {sims.mean():.1f}, %95 {np.quantile(sims, .95):.1f}, p(>=gerçek) {(sims >= act).mean():.3f} | aynı günlerde XU030 katkısı (-sgn*XU030) {mkt:.1f}")
# XU030 kendi gap'i -> 10:30 sonrası (h1 dönemi) ve tüm dönem
X2 = X[X.m_r2.notna()]
for thr in [0.005, 0.01]:
    t = X2[X2.gap.abs() > thr]; x = -np.sign(t.gap) * t.m_r2 * 1e4; m, tt, n = nwt(x.values); print(f"XU030 kendi |gap|>{thr}: 10:30->kapanış fade brüt {m:.1f} t {tt:.2f} n {n}")
print("XU030 koşulsuz 10:30->kapanış ort (h1 dönemi):", round(X2.m_r2.mean() * 1e4, 1), "bps; açılış->kapanış:", round(X2.intra.mean() * 1e4, 1))
