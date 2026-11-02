import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_E3_b")
"""11: Likit dönemde (2020+) gerçek F_TUPRS ile BT; net Sharpe ve blok bootstrap alt sınırı. Kesitsel tablodan seçili hisseler."""
import vb, numpy as np, pandas as pd
rng = np.random.default_rng(3)
W = pd.read_parquet(vb.RES + "/06_viop_daily.parquet")
F = pd.read_parquet(vb.RES + "/F.parquet"); z = vb.zsig(F.A_USREF.dropna(), 250).reindex(W.index)
pos = np.sign(z).where(z.abs() > 1, 0.0).fillna(0)
def boot(p, B=4000, blk=20):
    p = p.values; n = len(p); k = int(np.ceil(n / blk)); out = []
    for _ in range(B):
        st = rng.integers(0, n - blk + 1, k); s = np.concatenate([p[i:i + blk] for i in st])[:n]; out.append(s.mean())
    return np.percentile(out, [2.5, 5])
for nm, legs, a0 in [("f_intra", 1, "2020"), ("f_h", 2, "2020"), ("f_intra", 1, "2023"), ("f_h", 2, "2023")]:
    m = (W.index >= a0) & W[nm].notna()
    pp = (pos * W[nm])[m]; act = pos[m] != 0
    for cost in ([8, 15] if legs == 1 else [11, 18]):
        net = pp - cost / 1e4 * act
        ann = net[act].mean() * 252 * act.mean(); vol = net.std() * np.sqrt(252)
        lo = boot(net[act]) * 1e4
        print(f"{nm} {a0}+ maliyet {cost}: n {act.sum()}, net {1e4*net[act].mean():.1f} bps (t {vb.tstat(net[act]):.2f}), Sharpe {ann/vol:.2f}, blok-bootstrap %2,5/%5 alt: {lo[0]:.1f}/{lo[1]:.1f} bps")
X = pd.read_csv(vb.RES + "/04_cross_section.csv")
print("\nSeçili hisseler (hedge'li gün-içi ~ A_USREF):"); print(X[X.sym.isin(["TUPRS.IS", "AYGAZ.IS", "PETKM.IS", "THYAO.IS", "PGSUS.IS", "EREGL.IS", "SASA.IS", "KCHOL.IS", "AKBNK.IS", "BIMAS.IS"])].round(2).to_string())
