"""Görev 3 testleri: baz anomalisi_t -> spot_{t+1} (gap, gün-içi, cc) ve vadeli_{t+1} (uzlaşma, kapanış); yakınsama hızı; temettü beklentisi.
anom_dev = (b - b*) - geçmiş 60g medyanı (t hariç). Temettü penceresi (vade+7g içinde ex-tarih) olan günler 'nodiv' sürümünde dışlanır.
"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from vcommon import *
import statsmodels.api as sm
B = pd.read_parquet(RES + "/basis_panel.parquet").sort_values(["und", "date"])
B["ndays"] = B.groupby("und")["date"].shift(-1) - B["date"]
for c in ["sp_gap", "sp_intra", "sp_cc", "L_r_set", "L_r_cls", "L_r_intra", "anom"]:
    B[f"y_{c}"] = B.groupby("und")[c].shift(-1)
B.loc[B["ndays"] > pd.Timedelta(days=5), [c for c in B if c.startswith("y_")]] = np.nan
B["d_anom"] = B["y_anom"] - B["anom"]
B["nodiv"] = B["div_near"].fillna(0) == 0
SIGS = ["anom_dev", "anom_close_dev"]
TG = ["y_sp_gap", "y_sp_intra", "y_sp_cc", "y_L_r_set", "y_L_r_cls", "y_L_r_intra"]
def reg(df, y, s, ctrl=("sp_cc", "L_r_set")):
    cols = [s] + list(ctrl)
    d = df[[y] + cols].replace([np.inf, -np.inf], np.nan).dropna()
    if len(d) < 120: return None
    X = sm.add_constant(d[cols]); m = sm.OLS(d[y], X).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
    return m.params[s], m.tvalues[s], len(d), d[s].std()
rows = []
for u, g in B.groupby("und"):
    g = g.set_index("date")
    for s in SIGS:
        for y in TG + ["d_anom"]:
            for ver in ["all", "nodiv"]:
                gg = g if ver == "all" else g[g["nodiv"]]
                for per, a, b in [("ALL", "2000", "2100"), ("IS", "2000", "2022-12-31"), ("OOS", "2023-01-01", "2100")]:
                    x = gg[(gg.index >= a) & (gg.index <= b)]
                    r = reg(x, y, s, ctrl=() if y == "d_anom" else ("sp_cc", "L_r_set"))
                    if r: rows.append(dict(und=u, sig=s, tgt=y, ver=ver, per=per, beta=r[0], t=r[1], n=r[2], sd_sig_bps=1e4 * r[3], bps_per_sd=1e4 * r[0] * r[3]))
R = pd.DataFrame(rows); R.to_csv(RES + "/basis_tests_ts.csv", index=False)
# Fama-MacBeth (hisseler): kontrolsüz ve kontrollü (spot cc_t, vadeli r_t); likidite alt örneklemi
LQ = pd.read_csv(RES + "/liquidity_raw.csv").set_index("und")["liq_class"]
B["liq"] = B["und"].map(LQ)
fm = []
S_ = B[B["und"].isin(STOCKS)]
for s in SIGS:
    for y in TG:
        for ver in ["all", "nodiv"]:
            d = S_ if ver == "all" else S_[S_["nodiv"]]
            for ct in [(), ("sp_cc", "L_r_set")]:
                for r in fama_macbeth(d, s, y, ct): r.update(ver=ver, sub="all"); fm.append(r)
        for sub, cl in [("AB", ["A", "B"]), ("CD", ["C", "D"])]:
            d = S_[S_["liq"].isin(cl)]
            for r in fama_macbeth(d, s, y, ("sp_cc", "L_r_set"), min_n=8): r.update(ver="all", sub=sub); fm.append(r)
FM = pd.DataFrame(fm); FM.to_csv(RES + "/basis_tests_fm.csv", index=False)
pd.set_option("display.width", 250)
print(FM.pivot_table(index=["sig", "ver", "sub", "ctrls", "tgt"], columns="per", values=["bps_per_sd", "t"]).round(2).to_string())
A = R[(R["per"] == "ALL") & (R["tgt"] != "d_anom")].copy(); A["p"] = ll.t_to_p(A["t"]); A["fdr"], A["padj"] = ll.fdr(A["p"].values)
print("TS testleri:", len(A), "FDR geçen:", int(A["fdr"].sum()))
print(A.groupby(["sig", "tgt", "ver"]).agg(med_t=("t", "median"), frac_pos=("t", lambda x: (x > 0).mean()), n_fdr=("fdr", "sum"), med_bps=("bps_per_sd", "median")).round(2).to_string())
# yakınsama: d_anom ~ anom_dev  (kappa)
K = R[(R["tgt"] == "d_anom") & (R["sig"] == "anom_dev") & (R["ver"] == "all") & (R["per"] == "ALL")]
print("yakınsama katsayısı (d_anom ~ anom_dev) medyan:", K["beta"].median().round(3), "XU030:", K.loc[K["und"] == "XU030", "beta"].round(3).tolist())
print(R[(R["und"].isin(["XU030", "XLBNK"])) & (R["sig"] == "anom_dev") & (R["ver"] == "all")].round(3).to_string())
# ---- temettü beklentisi: örtük temettü = r*tau - b, gerçekleşen div_L ile (vadeye 5-25 gün kala, temettülü günler) ----
T = B[B["und"].isin(STOCKS) & (B["div_L"] > 0) & B["L_dte"].between(3, 40)].copy()
T["impl_div"] = T["r_tl"] * T["tau_L"] - T["b_L"]; T = T.dropna(subset=["impl_div", "div_L"])
T["impl_div"] = T["r_tl"] * T["tau_L"] - T["b_L"]
m = sm.OLS(T["impl_div"], sm.add_constant(T["div_L"])).fit(cov_type="cluster", cov_kwds={"groups": T["und"].astype("category").cat.codes})
print(f"\nTemettü: örtük ~ gerçekleşen: eğim {m.params['div_L']:.3f} (t {m.tvalues['div_L']:.1f}), sabit {1e4*m.params['const']:.1f} bps, R2 {m.rsquared:.3f}, n {len(T)}, hisse {T['und'].nunique()}")
# temettüsüz dönemde aynı ölçüt (sabit = ortalama anomali)
N = B[B["und"].isin(STOCKS) & (B["div_near"] == 0) & B["L_dte"].between(3, 40)]
print(f"Temettüsüz günlerde ortalama (r*tau - b): {1e4*(N['r_tl']*N['tau_L']-N['b_L']).median():.1f} bps (medyan), n {len(N)}")
pd.DataFrame([dict(slope=m.params['div_L'], t=m.tvalues['div_L'], const_bps=1e4 * m.params['const'], r2=m.rsquared, n=len(T))]).to_csv(RES + "/basis_dividend.csv", index=False)
