"""Plasebolar: bayat sinyal, gelecek sinyal, başka hissenin gap'i, gün karıştırma, dairesel kaydırma (max-t, 47 hisse ortak kaydırma)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_K1_b")
from kb import *
rng = np.random.default_rng(7)
P = pd.read_parquet(OUT + "/panel_b.parquet")
G = P.pivot(index="date", columns="sym", values="gap"); I = P.pivot(index="date", columns="sym", values="intra")
G = G[G.index >= "2014-01-01"]; I = I.reindex(G.index)
def fm(g, it, thr=0.01, c=10):
    m = (g.abs() > thr) & it.notna(); return (-np.sign(g[m]) * it[m] * 1e4 - c)
rows = []
for s in ["CIMSA", "OYAKC"]:
    g, it = G[s], I[s]
    for lab, sig in [("kendi gap_t", g), ("bayat gap_{t-1}", g.shift(1)), ("bayat gap_{t-2}", g.shift(2)), ("gelecek gap_{t+1}", g.shift(-1))]:
        x = fm(sig, it); 
        for per, z in [("IS", x[x.index <= IS_END]), ("OOS", x[x.index > IS_END])]:
            r = summ(z, f"{s} {lab} {per}"); rows.append(r)
    # başka hisselerin gap'i -> bu hissenin intra'sı (OOS)
    oth = []
    for j in G.columns:
        if j == s: continue
        x = fm(G[j], it); z = x[x.index > IS_END]; m, t, n = nwt(z.values); oth.append((j, m, t))
    O = pd.DataFrame(oth, columns=["j", "m", "t"])
    own = summ(fm(g, it)[lambda z: z.index > IS_END])
    print(s, "başka hisse gap'i -> intra OOS: medyan", round(O.m.median(), 1), "maks", round(O.m.max(), 1), O.loc[O.m.idxmax(), "j"],
          "kendi:", own["mean"], " kendi'den büyük olan:", (O.m >= own["mean"]).sum(), "/", len(O))
    print("   en yüksek 5:", O.sort_values("m", ascending=False).head(5).round(1).values.tolist())
    # gün karıştırma (yıl içinde gap'leri permüte et), OOS ortalama dağılımı
    x0 = own["mean"]; gg = g[g.index > IS_END]; ii = it[it.index > IS_END]; ok = gg.notna() & ii.notna(); gg, ii = gg[ok], ii[ok]
    yrs = gg.index.year.values; sims = []
    for b in range(2000):
        gp = gg.values.copy()
        for y in np.unique(yrs):
            k = np.where(yrs == y)[0]; gp[k] = gp[rng.permutation(k)]
        m = np.abs(gp) > 0.01; sims.append(np.mean(-np.sign(gp[m]) * ii.values[m] * 1e4 - 10))
    sims = np.array(sims); print(s, "gün karıştırma OOS: null ort", round(sims.mean(), 1), "95%", round(np.quantile(sims, .95), 1), "p=", round((sims >= x0).mean(), 4))
R = pd.DataFrame(rows); print(R.to_string()); R.to_csv(OUT + "/res_b4_placebo.csv", index=False)

# dairesel kaydırma: 47 hisse birlikte; OOS max-t ve CIMSA t'si
Go = G[G.index > IS_END]; Io = I[I.index > IS_END]
def tvec(gm, im):
    out = {}
    for s in gm.columns:
        g = gm[s].values; it = im[s].values; m = (np.abs(g) > 0.01) & np.isfinite(it) & np.isfinite(g)
        x = -np.sign(g[m]) * it[m] * 1e4 - 10; out[s] = nwt(x)[1]
    return pd.Series(out)
t0 = tvec(Go, Io); print("OOS gerçek t: CIMSA", round(t0.CIMSA, 2), "OYAKC", round(t0.OYAKC, 2), "maks", round(t0.max(), 2), t0.idxmax(), " t>2 sayısı", (t0 > 2).sum())
N = len(Go); mx = []; c_t = []; npos = []
shifts = rng.choice(np.arange(60, N - 60), 300, replace=False)
for k in shifts:
    gs = pd.DataFrame(np.roll(Go.values, k, axis=0), index=Go.index, columns=Go.columns)
    tv = tvec(gs, Io); mx.append(tv.max()); npos.append((tv > 2).sum())
mx = np.array(mx); npos = np.array(npos)
print("dairesel kaydırma null: max-t 95%", round(np.quantile(mx, .95), 2), " p(max>=CIMSA t)", round((mx >= t0.CIMSA).mean(), 3),
      " p(max>=OYAKC t)", round((mx >= t0.OYAKC).mean(), 3), " null t>2 sayısı ort", round(npos.mean(), 2), "gerçek", (t0 > 2).sum())
