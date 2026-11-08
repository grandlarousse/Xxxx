"""s6: Sıra-tabanlı kısmi regresyon (C1, C2), IS/OOS buy&hold, kayıt üzerinde BH-FDR, IS→OOS aktarım oranı, özet tablolar.
Önce s1..s5 çalışmış olmalı."""
import sys, json; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a4_abd_capraz")
from a4_common import *
from scipy import stats as st

reg_reset("s6_")
d = load_viop(); idx = d.index
def rank_partial(x, y, ctrl, h):
    D = pd.concat([x.rename("x"), y.rename("y"), ctrl], axis=1).dropna()
    def one(m):
        q = D[m].rank(); q = (q - q.mean()) / q.std()
        return nw_ols(q["y"], q.drop(columns="y"), lags=max(h, 5))["t"]
    return dict(t=one(D.index == D.index), t_is=one(D.index <= IS_END), t_oos=one(D.index > IS_END), n=len(D))

rm = np.log(d.y_GDXJ).diff(); rg = np.log(d.y_GLD).diff()
b = rm.rolling(60, min_periods=40).cov(rg).shift(1) / rg.rolling(60, min_periods=40).var().shift(1)
c1 = zscale(rm - b * rg)
c2 = zscale((d.ust_nom10 - d.ust_nom2).diff(5))
C = gold_controls(d); C["spx"] = zscale(np.log(d["y__GSPC"]).diff()); C["vix"] = zscale(np.log(d["y__VIX"]).diff())
C["gld1"] = zscale(rg)
out = {}
for nm, x, h in (("C1_GDXJ_artik", c1, 3), ("C2_egri_d5", c2, 1)):
    r = rank_partial(x, d[f"fwd{h}"], C, h); out[nm] = r
    reg("s6_sirakismi", f"s6_{nm}_sirakismi", nm + " sıra-kısmi | g1,g5,spx,vix,gld1", h, r)
print("Sıra-tabanlı kısmi t:", {k: {kk: round(vv, 2) for kk, vv in v.items()} for k, v in out.items()})
# buy & hold IS / OOS
bh = {}
for nm, m in (("full", idx == idx), ("is", idx <= IS_END), ("oos", idx > IS_END)):
    r = backtest(pd.Series(1.0, index=idx[m]), d.v_ret[m], 1, 0); bh[nm] = round(r["sharpe"], 2)
print("Buy&hold Sharpe (maliyetsiz):", bh)

# ---- kayıt üzerinde FDR ----
R = pd.read_csv(f"{S}/out/registry/{AGENT}.csv")
print("Toplam kayıtlı test:", len(R), "\nAile başına:", R.family.value_counts().to_dict())
R["p"] = R["p"].astype(float)
ok = R.p.notna()
R.loc[ok, "q_global"] = bh_fdr(R.loc[ok, "p"].values)
R["q_aile"] = np.nan
for f, g in R[ok].groupby("family"):
    R.loc[g.index, "q_aile"] = bh_fdr(g.p.values)
R.to_csv(f"{OUT}/kayit_fdr.csv", index=False)
print("q_global<0.10:", int((R.q_global < 0.10).sum()), " q_global<0.20:", int((R.q_global < 0.20).sum()))
print(R.sort_values("p").head(15)[["test_id", "h", "ic", "t", "t_is", "t_oos", "p", "q_global", "q_aile"]].round(4).to_string())
# null beklentisi: |t|>=2 oranı
for fam in ["s1_ic", "s1_kismi", "s1_buyuk", "s2_madenci_artik", "s2_madenci_oran", "s3_pencere"]:
    g = R[R.family == fam]; print(f"{fam}: n={len(g)} |t|>=2 oranı={(g.t.abs() >= 2).mean():.3f} (null≈0.046)")
# IS -> OOS aktarım: |t_is|>=2 olanlar
T = R[R.family.isin(["s1_ic", "s1_buyuk", "s2_madenci_oran", "s2_madenci_artik", "s2_madenci_buyuk", "s2_gsr_z", "s2_gsr_d", "s2_reelmodel_seviye", "s2_reelmodel_degisim", "s2_gld_hacim", "s2_gld_hacim_buyuk", "s3_pencere"])].copy()
sel = T[T.t_is.abs() >= 2]
same = (np.sign(sel.t_is) == np.sign(sel.t_oos))
print(f"IS |t|>=2 seçilen: {len(sel)}; OOS aynı işaret: {same.mean():.2f}; OOS aynı işaret ve |t|>=2: {(same & (sel.t_oos.abs() >= 2)).mean():.2f}")
print(sel.assign(same=same)[["test_id", "t_is", "t_oos", "same"]].round(2).to_string())
json.dump(dict(rank_partial=out, buyhold=bh, n_tests=int(len(R))), open(f"{OUT}/s6_ozet.json", "w"), indent=1, default=float)

# birincil test evreni (s1/s2/s3; tanı ve sağlamlık varyantları hariç): varyantlar BH'yi yapay olarak gevşetebilir
prim = R[R.family.str.match(r"^s[123]_") & ~R.family.str.contains("emilim")].copy()
prim["q_birincil"] = bh_fdr(prim.p.values)
print("Birincil test sayısı:", len(prim), " Bonferroni p eşiği:", 0.05 / len(prim))
print(prim.sort_values("p").head(8)[["test_id", "t", "p", "q_birincil"]].round(4).to_string())
prim.to_csv(f"{OUT}/kayit_fdr_birincil.csv", index=False)
