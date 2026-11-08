"""(a) GLD / GLDM akışları -> GLD/IAU ileri getiri; ters yön; VİOP hedefi.
Bilgi zamanı: SSGA günlük pay sayısı ve NAV, gün D için D akşamı (ABD, ~18:00–20:00 ET = 22:00–01:00 UTC) yayımlanır.
  lag1: ETF günü t için son SSGA günü D < t (yani D = t-1) -> t 15:00 ET'de bilinir.
  lag2: bir önceki SSGA günü (t-2) -> pay sayısının güncellenmesi T+1 ise daha temiz.
VİOP günü t için: SSGA günü D < t (takvim günü) -> D akşamı ABD = D+1 ~01:00 UTC < t 15:00 UTC.
"""
from common import *
import warnings; warnings.filterwarnings("ignore")
d = load_etf()
rows = []

def flow_feats(nh):
    S_ = np.log(nh["shares"].where(nh["shares"] > 0))
    f = pd.DataFrame(index=nh.index)
    f["f1"] = S_.diff(); f["f5"] = S_.diff(5); f["f20"] = S_.diff(20)
    for k in ["f1", "f5", "f20"]:
        sd = f[k].rolling(250, min_periods=120).std().shift(1)   # yalnız geçmiş
        f["z" + k] = f[k] / sd
    # uçlar: genişleyen geçmiş yüzdelikler (en az 250 gözlem)
    for k in ["f1", "f5"]:
        q90 = f[k].expanding(250).quantile(0.9).shift(1); q10 = f[k].expanding(250).quantile(0.1).shift(1)
        f[k + "_top"] = (f[k] > q90).astype(float).where(q90.notna()); f[k + "_bot"] = (f[k] < q10).astype(float).where(q10.notna())
    return f

def align(f, idx, lag):
    """ETF/VİOP günü t'ye, SSGA günü D < t olan son (lag=1) ya da ondan önceki (lag=2) değeri getir."""
    ff = f.copy(); ff = ff.shift(lag - 1)
    pos = ff.index.searchsorted(idx, side="left") - 1   # D < t
    out = pd.DataFrame(np.where(pos[:, None] >= 0, ff.values[np.clip(pos, 0, None)], np.nan), index=idx, columns=ff.columns)
    return out

nh = pd.read_parquet(f"{P}/etf_gld_navhist.parquet"); nh.index = pd.to_datetime(nh.index)
nm = pd.read_parquet(f"{P}/etf_gldm_navhist.parquet"); nm.index = pd.to_datetime(nm.index)
F = flow_feats(nh); FM = flow_feats(nm)
# kontrol: panel flow_gld_shares ile hizalama
chk = align(pd.DataFrame({"s": nh.shares}), d.index, 1)["s"]
print("panel flow_gld_shares ile uyum:", float((chk == d.flow_gld_shares).mean()))

rG = lr(d.c_GLD); rI = lr(d.c_IAU)
for lag in (1, 2):
    A = align(F, d.index, lag)
    for k in ["f1", "f5", "f20", "zf1", "zf5", "zf20"]:
        for h in (1, 3, 5, 10):
            rows.append(test("a_flow_gld", f"a_gld_{k}_lag{lag}_GLD_h{h}", f"GLD {k} (SSGA D=t-{lag})", A[k], fwd(rG, h), h, note=f"lag{lag}"))
        if lag == 1:
            for h in (1, 5):
                rows.append(test("a_flow_gld", f"a_gld_{k}_lag{lag}_IAU_h{h}", f"GLD {k} (D=t-1) -> IAU", A[k], fwd(rI, h), h, note="IAU teyit"))
    if lag == 1:
        for k in ["f1_top", "f1_bot", "f5_top", "f5_bot"]:
            for h in (1, 3, 5, 10):
                rows.append(mean_diff_test("a_flow_gld_uc", f"a_gld_{k}_lag1_GLD_h{h}", f"GLD akış ucu {k} (D=t-1)", A[k], fwd(rG, h), h))

# placebo (ileriye bakma kontrolü): zf5 lag1
A1 = align(F, d.index, 1)
pl = {h: placebo_lead(A1["zf5"], rG, h) for h in (1, 5)}
print("placebo zf5:", pl)
pl1 = {h: placebo_lead(A1["zf1"], rG, h) for h in (1, 5)}
print("placebo zf1:", pl1)

# GLDM akışları (2018-06+; tamamı OOS)
for lag in (1, 2):
    A = align(FM, d.index, lag)
    for k in ["zf1", "zf5", "zf20"]:
        for h in (1, 3, 5):
            rows.append(test("a_flow_gldm", f"a_gldm_{k}_lag{lag}_GLD_h{h}", f"GLDM {k} (D=t-{lag})", A[k], fwd(rG, h), h, note="GLDM 2018-06+, IS yok"))

# Toplam (GLD+GLDM) dolar akışı z-skoru, lag1
tot = pd.DataFrame({"g": nh.shares * nh.nav, "m": (nm.shares * nm.nav).reindex(nh.index)}).ffill()
fl_usd = (nh.shares.diff() * nh.nav).add((nm.shares.diff() * nm.nav).reindex(nh.index).fillna(0), fill_value=0)
fl_rel = fl_usd / tot.sum(axis=1).shift(1)
zt = (fl_rel.rolling(5).sum()) / fl_rel.rolling(5).sum().rolling(250, min_periods=120).std().shift(1)
At = align(pd.DataFrame({"z": zt}), d.index, 1)["z"]
for h in (1, 3, 5):
    rows.append(test("a_flow_tot", f"a_tot_z5_lag1_GLD_h{h}", "GLD+GLDM $akış 5g z (D=t-1)", At, fwd(rG, h), h))

# ---------------- Ters yön: akışlar geçmiş getiriyi mi takip ediyor? (SSGA günü D bazında)
g = pd.DataFrame({"f1": F["f1"]})
gld_raw = pd.read_parquet(f"{P}/yahoo/GLD.parquet"); gld_raw.index = pd.to_datetime(gld_raw.index)
rr = np.log(gld_raw["adjclose"]).diff().reindex(g.index)
g["r0"] = rr; g["r1"] = rr.shift(1); g["r2_5"] = rr.shift(2).rolling(4).sum(); g["r6_20"] = rr.shift(6).rolling(15).sum(); g["f1_l1"] = g.f1.shift(1)
g = g[g.index >= "2005-01-01"]
import statsmodels.api as sm
gg = g.dropna()
m = sm.OLS(gg.f1 / gg.f1.std(), sm.add_constant(gg[["r0", "r1", "r2_5", "r6_20", "f1_l1"]] / gg[["r0", "r1", "r2_5", "r6_20", "f1_l1"]].std())).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
rev = pd.DataFrame({"beta_std": m.params, "t": m.tvalues}).round(3)
print("Ters yön (f1_D ~ r_D, r_D-1, r_D-2..5, r_D-6..20, f1_D-1):\n", rev)
rev.to_csv(f"{OUT}/a_reverse_regression.csv")
for c in ["r0", "r1", "r2_5", "r6_20"]:
    st = test("a_reverse", f"a_rev_f1_on_{c}", f"GLD f1_D ~ {c}", g[c], g["f1"], 1, note="ters yön: akış geçmiş getiriyi takip ediyor mu (tanı)")
    rows.append(st)
# alt dönemler
for a, b in [("2005", "2012"), ("2013", "2019"), ("2020", "2026")]:
    gg2 = gg[a:b]
    m2 = sm.OLS(gg2.f1 / gg2.f1.std(), sm.add_constant(gg2[["r0", "r1", "r2_5", "r6_20", "f1_l1"]] / gg2[["r0", "r1", "r2_5", "r6_20", "f1_l1"]].std())).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
    print(a, b, dict(zip(m2.params.index, [f"{p:.3f} (t={t:.1f})" for p, t in zip(m2.params, m2.tvalues)])))

# ---------------- VİOP hedefi (VİOP kendi bölünmesi: IS 2017-03..2021-12)
v = pd.read_parquet(f"{P}/panel_viop.parquet"); v.index = pd.to_datetime(v.index)
lib_altin.IS_END = pd.Timestamp("2021-12-31")
for lag in (1, 2):
    Av = align(F, v.index, lag)
    for k in ["zf1", "zf5", "zf20"]:
        for h in (1, 3, 5):
            rows.append(test("a_flow_viop", f"a_gld_{k}_lag{lag}_VIOP_h{h}", f"GLD {k} (SSGA D<t, lag{lag}) -> VİOP", Av[k], v[f"fwd{h}"], h, note="VİOP IS 2017-03..2021-12"))
lib_altin.IS_END = pd.Timestamp("2017-12-31")

res = pd.DataFrame(rows)
res.drop(columns=["by_year"], errors="ignore").to_csv(f"{OUT}/a_flows_tests.csv", index=False)
show = res[["test_id", "h", "n", "ic", "t", "t_is", "t_oos", "t_22", "yrs_same_sign", "yrs"]]
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 300)
print(show.round(3).to_string())

# ---------------- Strateji: IS'te seçilmiş kural (yalnız IS sonuçlarına bakılarak) -> OOS bir kez
best = res[(res.family == "a_flow_gld") & (res.test_id.str.contains("_GLD_"))].copy()
best["abs_t_is"] = best.t_is.abs()
b = best.sort_values("abs_t_is", ascending=False).iloc[0]
print("IS'te en güçlü akış öngörücüsü:", b.test_id, "t_is=", round(b.t_is, 2), "t_oos=", round(b.t_oos, 2))
json.dump({"is_best": b.test_id, "t_is": b.t_is, "t_oos": b.t_oos}, open(f"{OUT}/a_is_choice.json", "w"))
k = b.test_id.split("_")[2]; lag = int(b.test_id.split("lag")[1][0]); h = int(b.test_id.split("_h")[-1])
h = min(h, 5)
A = align(F, d.index, lag)
z = A[k] if k.startswith("z") else A[k] / A[k].rolling(250, min_periods=120).std().shift(1)
sg = np.sign(b.t_is)
srows = []
for thr in (0.0, 1.0):
    pos = (sg * np.sign(z) * (z.abs() > thr)).fillna(0)
    srows += strat_eval(f"akis_{k}_lag{lag}_thr{thr}", pos, "GLD", h, d)
pd.DataFrame(srows).to_csv(f"{OUT}/a_flows_strategies.csv", index=False)
print(pd.DataFrame(srows)[["strategy", "mode", "cost", "sh_is", "sh_oos", "sh_22", "shdm_oos", "bh_oos", "exposure_long", "exposure_short", "turnover_yr"]].to_string())
