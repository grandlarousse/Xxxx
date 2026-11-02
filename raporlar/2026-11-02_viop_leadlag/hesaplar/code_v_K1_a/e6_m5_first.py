"""(b) 5 dk (son ~60 gün, 47 hisse havuz): açılış müzayede fiyatı -> ilk sürekli işlem dakikaları. Geri dönüş açılış seansı fiyatında mı?
r0 = log(07:05 kapanış / açılış), r1 = log(07:30/07:05), r2 = log(kapanış/07:30). Gap'e regresyon (havuz, gün kümeli yerine NW)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_K1_a")
from vk import *
R4 = pd.read_csv(OUT + "/res_e4_all47.csv").set_index("sym")
pool = []
for s in VIOP:
    M = m5(s)
    if M is None: continue
    d = decomp(s, start="2026-07-01")
    g = lambda hm: M[M.hm == hm].set_index("day")["c"]
    x = d.join(g(700).rename("q0705"), how="inner").join(g(725).rename("q0730"), how="inner").join(M[M.hm == 700].set_index("day")["o"].rename("first_trade"), how="inner")
    x = x.dropna(subset=["gap", "intra"])
    for c_ in ["q0705", "q0730", "first_trade"]:
        bad = (x[c_] > x.h * 1.0005) | (x[c_] < x.l * 0.9995); x.loc[bad, c_] = np.nan
    x = x.dropna()
    x["r_ft"] = np.log(x.first_trade / x.o); x["r0"] = np.log(x.q0705 / x.o); x["r1"] = np.log(x.q0730 / x.q0705); x["r2"] = np.log(x.c / x.q0730)
    x["sym"] = s; x["liq"] = R4.loc[s, "liq_grp"]; pool.append(x)
P = pd.concat(pool)
print("havuz n", len(P), "gün", P.index.nunique(), "aralık", P.index.min().date(), P.index.max().date())
def reg(Q, col):
    # gün kümeli SE: gün içi kesitsel korelasyonu hesaba kat (basit cluster)
    y = Q[col].values; X = np.column_stack([np.ones(len(Q)), Q.gap.values]); b = np.linalg.lstsq(X, y, rcond=None)[0]; u = y - X @ b
    XtXi = np.linalg.inv(X.T @ X); meat = np.zeros((2, 2))
    for _, idx in Q.groupby(level=0).indices.items():
        sx = (X[idx] * u[idx, None]).sum(0); meat += np.outer(sx, sx)
    se = np.sqrt(np.diag(XtXi @ meat @ XtXi)); return b[1], b[1] / se[1]
for lg in ["düşük", "orta", "yüksek", "hepsi"]:
    Q = P if lg == "hepsi" else P[P.liq == lg]
    out = [f"{lg:7s} n={len(Q)}"]
    for col, lab in [("intra", "açılış->kapanış"), ("r_ft", "açılış->ilk işlem"), ("r0", "açılış->10:05"), ("r1", "10:05->10:30"), ("r2", "10:30->kapanış")]:
        b, t = reg(Q, col); out.append(f"{lab}: {b:+.3f} (t{t:+.1f})")
    print(" | ".join(out))
    y = Q[Q.gap.abs() > 0.01]
    for lab, tc in [("açılış", "intra"), ("10:05 giriş", None), ("10:30 giriş", "r2")]:
        tgt = (y.r1 + y.r2) if tc is None else y[tc]
        pn = (-np.sign(y.gap) * tgt).groupby(level=0).mean()
        m, t, n = nw_mean_t(pn.values, lags=2); print(f"    fade |gap|>%1 brüt, {lab}: {1e4*m:+.1f} bps (t{t:+.2f}) gün {n} işlem {len(y)}")
# açılış müzayedesi ile ilk sürekli işlem arasındaki mutlak fark (bps) — 'açılış gürültüsü' büyüklüğü
P["abs_ft"] = 1e4 * P.r_ft.abs(); P["abs_r0"] = 1e4 * P.r0.abs()
print(P.groupby("liq")[["abs_ft", "abs_r0"]].median().round(1))
P.to_parquet(OUT + "/res_e6_m5_pool.parquet")
