"""B5: VİOP endeks vadelisi ile 'açılışta sat, kapanışta kapat' backtesti (+ gece tarafı), maliyet hassasiyeti, yıllar, IS/OOS,
ACILIS'in yıllara göre tanım tutarlılığı (spot gap/intra ile korelasyon), spot ile aynı günlerde karşılaştırma.
Giriş: ACILIS (09:30 TSİ açılış seansı/ilk işlem), çıkış: KAPANIS (18:10 son işlem). Roll yok (aynı gün aynı sözleşme)."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_G3_a")
from vcommon import *
import warnings; warnings.filterwarnings("ignore")
R = S + "/out/code_v_G3_a/res"; pd.set_option("display.width", 260)
d = pd.read_parquet(R + "/viop_fut.parquet")
print("VİOP gün sayısı", d.TARIH.nunique(), d.TARIH.min().date(), d.TARIH.max().date())
def front(und):
    x = d[d["SOZLESME KODU"].str.match(rf"^F_{und}\d{{4}}$")].copy()
    x = x[x["VADE TARIHI"] > x["TARIH"]].sort_values(["TARIH", "VADE TARIHI"])
    f = x.groupby("TARIH").head(1).set_index("TARIH")
    allk = x.set_index(["TARIH", "SOZLESME KODU"])["KAPANIS FIYATI"]
    dates = sorted(x.TARIH.unique()); prevd = dict(zip(dates[1:], dates[:-1]))
    f["kap_prev"] = [allk.get((prevd.get(t), c), np.nan) for t, c in zip(f.index, f["SOZLESME KODU"])]
    o = f["ACILIS FIYATI"]; c = f["KAPANIS FIYATI"]
    out = pd.DataFrame({"f_gap": np.log(o / f["ONCEKI UZLASMA FIYATI"]), "f_gapc": np.log(o / f.kap_prev), "f_intra": np.log(c / o),
                        "f_intra_u": np.log(f["UZLASMA FIYATI"] / o), "has_os": f["ACILIS SEANSI FIYATI"].notna(), "ntr": f["ISLEM SAYISI"],
                        "days_to_exp": (f["VADE TARIHI"] - f.index).dt.days, "basis_c": np.nan})
    for k in ["f_gap", "f_gapc", "f_intra", "f_intra_u"]:
        out.loc[(out[k].abs() > LIM) | ~np.isfinite(out[k]), k] = np.nan
    return out, f
COSTS = [0, 1, 2, 3, 4, 6, 8]
allrows = []
for und in ["XU030", "XLBNK", "X10XB", "XSD25"]:
    F, raw = front(und)
    sp = decomp(und + ".IS", start="2017-01-01")
    Z = F.join(sp[["gap", "intra", "c"]], how="left")
    Z["basis_c"] = np.log(raw["UZLASMA FIYATI"] / Z["c"])
    print(f"\n######## {und}: gün {len(Z)}, f_intra var {Z.f_intra.notna().sum()}, açılış seansı olan gün oranı by yıl:",
          Z.groupby(Z.index.year).has_os.mean().round(2).to_dict())
    # Tanım tutarlılığı: yıllara göre korelasyon ve sd
    q = Z.dropna(subset=["f_gap", "gap", "f_intra", "intra"])
    C = q.groupby(q.index.year).apply(lambda g: pd.Series(dict(n=len(g), c_gap=g.f_gap.corr(g.gap), c_intra=g.f_intra.corr(g.intra),
                                                               sd_fgap=1e4 * g.f_gap.std(), sd_sgap=1e4 * g.gap.std(), sd_fin=1e4 * g.f_intra.std(), sd_sin=1e4 * g.intra.std(),
                                                               f_gap=1e4 * g.f_gap.mean(), s_gap=1e4 * g.gap.mean(), f_intra=1e4 * g.f_intra.mean(), s_intra=1e4 * g.intra.mean(),
                                                               t_f_intra=tstat(g.f_intra), basis_bps=1e4 * g.basis_c.median(), dte=g.days_to_exp.median())))
    print(C.round(2).to_string())
    C.to_csv(R + f"/b5_{und}_years.csv")
    # Backtest
    st = -Z.f_intra
    for nm, sl in [("ALL", slice(None)), ("IS 2017-2020", slice(None, "2020")), ("OOS 2021-2026", slice("2021", None)), ("2023-12..2026-10", slice("2023-12-01", "2026-10-31")),
                   ("OOS ex-kriz", None)]:
        if sl is None:
            s = st.loc["2021":].dropna()
            m = pd.Series(False, index=s.index)
            for a, b in [("2021-12-01", "2021-12-31"), ("2023-06-01", "2023-06-30"), ("2025-03-15", "2025-04-15"), ("2026-09-01", "2026-10-31")]:
                m |= (s.index >= a) & (s.index <= b)
            s = s[~m]
        else:
            s = st.loc[sl].dropna()
        if len(s) < 20: continue
        r = dict(und=und, per=nm, n=len(s), gross=1e4 * s.mean(), t=tstat(s), t_nw=nw_t(s), hit=(s > 0).mean(), sd=1e4 * s.std())
        for c in COSTS: r[f"net{c}"] = 1e4 * s.mean() - c
        r["sharpe_net2"] = (s.mean() - 2e-4) / s.std() * np.sqrt(250); r["sharpe_net4"] = (s.mean() - 4e-4) / s.std() * np.sqrt(250)
        allrows.append(r)
    # gece tarafı (uzun kapanış->açılış)
    for nm, sl in [("ALL", slice(None)), ("IS 2017-2020", slice(None, "2020")), ("OOS 2021-2026", slice("2021", None))]:
        g1 = Z.f_gapc.loc[sl].dropna()
        if len(g1) > 20:
            allrows.append(dict(und=und + "_GECE(long kap->aç)", per=nm, n=len(g1), gross=1e4 * g1.mean(), t=tstat(g1), t_nw=nw_t(g1), hit=(g1 > 0).mean(), sd=1e4 * g1.std(),
                                **{f"net{c}": 1e4 * g1.mean() - c for c in COSTS}))
    # yıl bazında brüt ve net2
    yy = st.dropna().groupby(st.dropna().index.year).agg(["count", "mean"]); yy["mean"] *= 1e4
    print("yıllık aç-sat brüt (bps):", yy["mean"].round(1).to_dict(), " pozitif yıl:", int((yy["mean"] > 0).sum()), "/", len(yy))
    # yıl-blok bootstrap
    s = st.dropna(); yrs = sorted(set(s.index.year)); by = {y: s[s.index.year == y].values for y in yrs}; rng = np.random.default_rng(1)
    bs = np.array([np.concatenate([by[y] for y in rng.choice(yrs, len(yrs))]).mean() for _ in range(4000)])
    print("yıl-blok bootstrap brüt CI95", np.round(1e4 * np.percentile(bs, [2.5, 50, 97.5]), 2), "P(brüt<=0)", round((bs <= 0).mean(), 3), "P(brüt<=2bps)", round((bs <= 2e-4).mean(), 3), "P(brüt<=4bps)", round((bs <= 4e-4).mean(), 3))
    Z.to_parquet(R + f"/b5_{und}_panel.parquet")
B = pd.DataFrame(allrows); B.to_csv(R + "/b5_bt.csv", index=False)
print("\n== BACKTEST ÖZET (bps/gün)"); print(B.round(2).to_string())
