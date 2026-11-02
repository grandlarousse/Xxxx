import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_E3_b")
"""04: Plasebolar. (i) bayat sinyal k=2..5 ve 'gelecek' sinyal; (ii) rastgele işaret (10.000) BT ve regresyon;
(iii) yıl-içi karıştırma; (iv) kesitsel: tüm BIST hisseleri (Yahoo, likit) hedge'li gün-içi; (v) sektör/tema plasebo hisseleri."""
import vb, numpy as np, pandas as pd, os
rng = np.random.default_rng(11)
F = pd.read_parquet(vb.RES + "/F.parquet"); G = F[F.index >= "2014-01-01"].copy()
s = F["A_USREF"]; y = F["y_h"]; yr = F["y_raw"]
def per_t(sig, tgt):
    out = {}
    for pk, m in [("ALL", tgt.index >= "2014"), ("IS", (tgt.index >= "2014") & (tgt.index < vb.SPLIT)), ("OOS", tgt.index >= vb.SPLIT)]:
        _, t, n = vb.nw(tgt[m], sig[m].rename("x")); out[pk] = round(float(t["x"]), 2)
    return out
print("(i) gecikme profili, hedef y_h (A_USREF lag1 = k=1):")
for k in range(0, 7):
    sg = s.shift(k - 1)  # A_ zaten lag1; k=0 => ABD t günü (BIST kapanışından SONRA biter -> işlenemez; sadece bilgi)
    print(f"  k={k}", per_t(sg, y), " | ham:", per_t(sg, yr))
print("  k=-1 (gelecek ABD günü t+1, plasebo)", per_t(s.shift(-2), y))
# (ii) rastgele işaret: BT |z|>1 brüt ve regresyon
pnl, pos = vb.bt(s, y, 1.0); pnl = pnl[pnl.index >= "2014"]; pos = pos[pos.index >= "2014"]
act = pos != 0
obs = {pk: pnl[act & m].mean() for pk, m in [("ALL", pnl.index >= "2014"), ("IS", pnl.index < vb.SPLIT), ("OOS", pnl.index >= vb.SPLIT)]}
yy = y.reindex(pos.index)[act]; pp = pos[act]; isv = (pp.index < vb.SPLIT)
N = 10000
flips = rng.choice([-1.0, 1.0], size=(N, len(pp)))
sims = (flips * (pp.values * yy.values)[None, :])
for pk, m in [("ALL", np.ones(len(pp), bool)), ("IS", isv), ("OOS", ~isv)]:
    d = sims[:, m].mean(1); print(f"(ii) rastgele işaret BT |z|>1 {pk}: gözlenen {1e4*obs[pk]:.1f} bps, p = {(d >= obs[pk]).mean():.4f}  (%95 null üst {1e4*np.percentile(d,95):.1f})")
# rastgele işaret regresyon: sinyalin işaretini rastgele çevir, |değer| korunur
x = s.reindex(G.index); yv = y.reindex(G.index); mm = x.notna() & yv.notna(); xv = x[mm].values; yvv = yv[mm].values; isx = x[mm].index < vb.SPLIT
def cor(a, b): return np.corrcoef(a, b)[0, 1]
c0 = {"ALL": cor(xv, yvv), "IS": cor(xv[isx], yvv[isx]), "OOS": cor(xv[~isx], yvv[~isx])}
cs = {"ALL": [], "IS": [], "OOS": []}
for i in range(5000):
    f = rng.choice([-1.0, 1.0], len(xv)); xf = xv * f
    cs["ALL"].append(cor(xf, yvv)); cs["IS"].append(cor(xf[isx], yvv[isx])); cs["OOS"].append(cor(xf[~isx], yvv[~isx]))
for pk in cs: print(f"(ii) rastgele işaret corr {pk}: gözlenen {c0[pk]:.3f}, p = {(np.array(cs[pk]) >= c0[pk]).mean():.4f}")
# (iii) yıl içinde gün karıştırma (yıl yapısı korunur)
yrs = x[mm].index.year.values; ca = []
for i in range(3000):
    xs = xv.copy()
    for Y in np.unique(yrs):
        ix = np.where(yrs == Y)[0]; xs[ix] = xs[rng.permutation(ix)]
    ca.append(cor(xs, yvv))
print(f"(iii) yıl-içi karıştırma corr ALL: gözlenen {c0['ALL']:.3f}, p = {(np.array(ca) >= c0['ALL']).mean():.4f}")
# (iv) kesitsel: tüm BIST hisseleri
cat = pd.read_csv(vb.D + "/catalog.csv")
bist = cat[cat.sym.str.endswith(".IS") & (cat.type == "EQUITY")].sym.tolist()
cal = vb.bist_cal("2013-01-01"); xu = vb.bist_dec("XU100.IS", cal).intra
rows = []
for b in bist:
    try:
        d = vb.bist_dec(b, cal)
    except Exception:
        continue
    d = d[d.index >= "2014-01-01"]
    if d.intra.notna().sum() < 1000: continue
    tv = (d.v * d.c).rolling(250, min_periods=50).median()
    liquid = (d.intra.notna()) & (d.v > 0)
    yh = (d.intra - xu.reindex(d.index)).where(liquid)
    r = {"sym": b, "n": int(yh.notna().sum()), "zero_intra_frac": float((d.intra == 0).mean()), "med_tv_mnTL_2025": float(tv[tv.index >= "2025"].median() / 1e6) if (tv.index >= "2025").any() else np.nan}
    for pk, m in [("ALL", yh.index >= "2014"), ("IS", yh.index < vb.SPLIT), ("OOS", yh.index >= vb.SPLIT)]:
        if yh[m].notna().sum() < 250: r["t_" + pk] = np.nan; continue
        _, t, n = vb.nw(yh[m], s.reindex(yh.index)[m].rename("x")); r["t_" + pk] = float(t["x"])
    rows.append(r)
X = pd.DataFrame(rows).sort_values("t_ALL", ascending=False).reset_index(drop=True); X.to_csv(vb.RES + "/04_cross_section.csv", index=False)
X2 = X[X.zero_intra_frac < 0.15]
print(f"\n(iv) kesitsel: {len(X)} BIST hissesi (n>=1000), likit alt küme (gün-içi sıfır oranı<%15): {len(X2)}")
print(X.head(12).round(2).to_string())
print("TUPRS sırası ALL:", int(X.index[X.sym == "TUPRS.IS"][0]) + 1, "/", len(X), " |t_ALL|>2 sayısı:", int((X.t_ALL.abs() > 2).sum()), " şans beklentisi ~", round(0.05 * len(X), 1))
print("t_ALL dağılımı: ort", round(X.t_ALL.mean(), 2), "sd", round(X.t_ALL.std(), 2), " IS ort", round(X.t_IS.mean(), 2), " OOS ort", round(X.t_OOS.mean(), 2))
