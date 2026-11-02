"""10:30 versiyonunda 47 hisse: ham ve XU030 hedge'li; dairesel kaydırma ile max-t null; BH."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_K1_b")
from kb import *
from scipy import stats
rng = np.random.default_rng(11)
P = pd.read_parquet(OUT + "/panel_b.parquet")
X = daily("XU030", is_index=True); hx = h1("XU030"); f = hx[hx.hm == 630].set_index("day")
X["m_r2"] = np.log(X.c / f.c.reindex(X.index))
P = P[P.date >= "2023-11-30"]
G = P.pivot(index="date", columns="sym", values="gap"); R2 = P.pivot(index="date", columns="sym", values="r2")
MR = X.m_r2.reindex(G.index)
H2 = R2.sub(MR, axis=0)
def tv(Gm, Rm, cost):
    o = {}
    for s in Gm.columns:
        g = Gm[s].values; r = Rm[s].values; m = (np.abs(g) > 0.01) & np.isfinite(r) & np.isfinite(g)
        o[s] = nwt(-np.sign(g[m]) * r[m] * 1e4 - cost)[:2]
    return pd.DataFrame(o, index=["m", "t"]).T
for lab, RR, c in [("10:30 ham net10", R2, 10), ("10:30 XU030-hedge net13", H2, 13)]:
    T0 = tv(G, RR, c); n = G.shape[0]
    mx = []
    for k in rng.choice(np.arange(40, n - 40), 300, replace=False):
        Gs = pd.DataFrame(np.roll(G.values, k, axis=0), index=G.index, columns=G.columns); mx.append(tv(Gs, RR, c).t.max())
    mx = np.array(mx)
    p = 2 * (1 - stats.norm.cdf(T0.t.abs()))
    print(f"{lab}: pozitif {int((T0.m > 0).sum())}/47, medyan {T0.m.median():.1f}, CIMSA {T0.loc['CIMSA','m']:.1f} (t {T0.loc['CIMSA','t']:.2f}), OYAKC {T0.loc['OYAKC','m']:.1f} (t {T0.loc['OYAKC','t']:.2f}), "
          f"maks t {T0.t.max():.2f} {T0.t.idxmax()} | null maks-t %95 {np.quantile(mx, .95):.2f}, p(CIMSA) {(mx >= T0.loc['CIMSA','t']).mean():.3f}, p(OYAKC) {(mx >= T0.loc['OYAKC','t']).mean():.3f} | BH geçen: {list(T0.index[bh(p)])}")
    print("   ilk 6:", T0.sort_values("t", ascending=False).head(6).round(2).to_dict("index"))
