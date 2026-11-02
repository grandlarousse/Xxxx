"""(1) Zamanla değişen likidite tercilleri (t-1'e kadar 60g medyan TL hacim, her gün kesitsel) -> havuz fade (look-ahead'siz gruplama).
(2) CIMSA/OYAKC 10:30 girişte yıllara göre ve yoğunlaşma. (3) Koordinatör panel (ll çıktısı) ile corr(gap,intra) 2021+ karşılaştırması (yalnız tanı)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_K1_a")
from vk import *
pool = []
for s in VIOP:
    d = decomp(s).dropna(subset=["gap", "intra"]).copy()
    full = load_daily(s); tl = (full.v * full.c).rolling(60, min_periods=40).median().shift(1)
    d["tl60"] = tl.reindex(d.index); d["sym"] = s; pool.append(d[["gap", "intra", "tl60", "sym"]])
P = pd.concat(pool).dropna()
P["liq"] = P.groupby(level=0).tl60.transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False) if len(x) >= 9 else np.nan)
for lab, msk in [("IS", P.index < SPLIT), ("IS16", (P.index >= "2016") & (P.index < SPLIT)), ("OOS", P.index >= SPLIT)]:
    for lg, nm in [(0, "düşük"), (1, "orta"), (2, "yüksek")]:
        x = P[msk & (P.liq == lg) & (P.gap.abs() > 0.01)]
        pn = (-np.sign(x.gap) * x.intra - 0.001).groupby(level=0).mean(); m, t, n = nw_mean_t(pn.values)
        cg = P[msk & (P.liq == lg)]; c = cg.gap.corr(cg.intra)
        print(f"zamanla değişen likidite {lab:4s} {nm:6s}: fade net10 {1e4*m:+6.1f} bps (t{t:+.2f}) gün {n} işlem {len(x)} | havuz corr(gap,intra) {c:+.3f}")
# (2)
for s in ["CIMSA", "OYAKC"]:
    d = decomp(s, start="2023-11-01"); H = h1(s)
    p1 = H[H.hm == 630].set_index("day")["c"].rename("p1"); x = d.join(p1, how="inner").dropna(subset=["gap", "intra", "p1"]); x = x[x.index >= "2023-12-01"]
    x = x[(x.p1 <= x.h * 1.0005) & (x.p1 >= x.l * 0.9995)]
    y = x[x.gap.abs() > 0.01]; pn = 1e4 * (-np.sign(y.gap) * np.log(y.c / y.p1) - 0.001); po = 1e4 * (-np.sign(y.gap) * y.intra - 0.001)
    print(s, "10:30 giriş yıllık ort. bps:", pn.groupby(pn.index.year).mean().round(0).to_dict(), "n:", pn.groupby(pn.index.year).size().to_dict())
    print(s, "açılış giriş yıllık ort. bps:", po.groupby(po.index.year).mean().round(0).to_dict())
    srt = pn.sort_values(ascending=False); print(s, f"10:30 giriş toplam {pn.sum():.0f} bps, en iyi 5 işlem payı {srt.iloc[:5].sum()/pn.sum():.0%}, en iyi 10 {srt.iloc[:10].sum()/pn.sum():.0%}; en iyi 5 hariç ort {srt.iloc[5:].mean():+.1f} (t {nw_mean_t(srt.iloc[5:].sort_index().values)[1]:+.2f})")
    for side, msk in [("long (gap<0)", y.gap < 0), ("short (gap>0)", y.gap > 0)]:
        m, t, n = nw_mean_t(pn[msk].values); print(f"   {s} 10:30 {side}: {m:+.1f} bps (t{t:+.2f}) n {n}")
# (3) tanı: koordinatör paneli
D = pd.read_parquet(S + "/data/panel_decomp_bist.parquet"); D = D[D.index >= "2021-01-01"]
cc = {s: D[(s, "gap")].corr(D[(s, "intra")]) for s in VIOP if (s, "gap") in D.columns}
cc = pd.Series(cc); print("ll paneli 2021+ corr(gap,intra): min %.3f max %.3f medyan %.3f" % (cc.min(), cc.max(), cc.median()))
R4 = pd.read_csv(OUT + "/res_e4_all47.csv").set_index("sym"); cmp_ = pd.DataFrame({"ll_panel": cc, "bizim": R4.corr_OOS}).dropna()
print("fark |ll-bizim| medyan %.3f maks %.3f (%s)" % ((cmp_.ll_panel - cmp_.bizim).abs().median(), (cmp_.ll_panel - cmp_.bizim).abs().max(), (cmp_.ll_panel - cmp_.bizim).abs().idxmax()))
