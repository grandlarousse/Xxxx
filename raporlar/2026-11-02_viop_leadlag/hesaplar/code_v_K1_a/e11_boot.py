"""Kalın kuyruk: işlem bootstrap (iid ve 20-işlem blok) %95 GA, P(ort<=0). Yıllık tablo (n, net bps) kesin değerler."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_K1_a")
from vk import *
rng = np.random.default_rng(11)
def boot(x, B=5000, block=1):
    x = np.asarray(x); n = len(x); nb = int(np.ceil(n / block)); ms = np.empty(B)
    for b in range(B):
        st_ = rng.integers(0, n - block + 1, nb); idx = (st_[:, None] + np.arange(block)).ravel()[:n]; ms[b] = x[idx].mean()
    return np.quantile(ms, [0.025, 0.975]) * 1e4, (ms <= 0).mean()
for s in ["CIMSA", "OYAKC"]:
    d = decomp(s).dropna(subset=["gap", "intra"]); b = d[d.gap.abs() > 0.01]; p = -np.sign(b.gap) * b.intra - 0.001
    yr = pd.DataFrame({"n": p.groupby(p.index.year).size(), "net_bps": (1e4 * p.groupby(p.index.year).mean()).round(1)})
    print(s, "yıllık:", yr.T.to_string())
    for lab, q in [("IS", p[p.index < SPLIT]), ("OOS", p[p.index >= SPLIT])]:
        for blk in [1, 20]:
            ci, pz = boot(q.values, block=blk); print(f"  {s} {lab} blok={blk}: ort {1e4*q.mean():+.1f} GA95 [{ci[0]:+.1f}, {ci[1]:+.1f}] P(<=0)={pz:.3f}")
    H = h1(s); dd = decomp(s, start="2023-11-01"); p1 = H[H.hm == 630].set_index("day")["c"].rename("p1")
    x = dd.join(p1, how="inner").dropna(subset=["gap", "intra", "p1"]); x = x[(x.index >= "2023-12-01") & (x.p1 <= x.h * 1.0005) & (x.p1 >= x.l * 0.9995)]
    y = x[x.gap.abs() > 0.01]; q = -np.sign(y.gap) * np.log(y.c / y.p1) - 0.001
    for blk in [1, 10]:
        ci, pz = boot(q.values, block=blk); print(f"  {s} 10:30 giriş blok={blk}: ort {1e4*q.mean():+.1f} GA95 [{ci[0]:+.1f}, {ci[1]:+.1f}] P(<=0)={pz:.3f} n={len(q)}")
