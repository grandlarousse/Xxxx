"""Görev 4: Açık pozisyon (AP) ve hacim değişimi -> ertesi gün getiri.
Özellikler (t günü, kapanıştan sonra bilinir):
  dOI   = sum(oi_chg)/sum(oi - oi_chg)  (t'de listelenen sözleşmeler; vadesi dolan seri mekanik düşüş yaratmaz)
  r     = vadeli L sözleşmesi uzlaşma getirisi (t)
  vsur  = ln(vadeli TL hacim) - geçmiş 20g ort.;  fsr = ln(vadeli/spot hacim) - geçmiş 60g medyan
  Etkileşimler: r*dOI_z (yeni long/short), r*vsur (hacim-getiri: Llorente vd. 2002)
Hedefler (t+1): spot gap, spot gün-içi, spot cc, vadeli uzlaşma getirisi; ve t+1..t+5 kümülatif spot cc.
Testler: hisse bazında OLS (NW t, kontroller: r_t, XU100 r_t, hedefin kendi gecikmesi) + Fama-MacBeth (tarih kesiti). BH-FDR.
"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from vcommon import *
import statsmodels.api as sm
D = pd.read_parquet(RES + "/daily_all.parquet")
F = load_panel(); F = F[F["und"].isin(ALL) & (F["expiry"] >= F["date"])]
g0 = F.groupby(["und", "date"]).agg(oi=("oi", "sum"), oichg=("oi_chg", "sum")).reset_index()
g0["oi_prev"] = g0["oi"] - g0["oichg"]
D = D.merge(g0[["und", "date", "oichg", "oi_prev"]], on=["und", "date"], how="left")
xu100 = ll.ret("XU100")
rows = []
panel = []
for u in STOCKS + ["XU030", "XLBNK"]:
    g = D[D["und"] == u].set_index("date").sort_index().copy()
    g["dOI"] = g["oichg"] / g["oi_prev"].where(g["oi_prev"] > 0)
    g.loc[g["dOI"].abs() > 2, "dOI"] = np.nan
    # vade sonu günü ve ertesi: AP mekanik (fiziki teslimat / yeni seri) -> işaretle
    g["exp_day"] = (g["c1_dte"] == 0)
    g["dOI_z"] = (g["dOI"] - g["dOI"].rolling(250, min_periods=60).mean().shift(1)) / g["dOI"].rolling(250, min_periods=60).std().shift(1)
    lv = np.log(g["value_tl"].where(g["value_tl"] > 0))
    g["vsur"] = lv - lv.rolling(20, min_periods=10).mean().shift(1)
    if "s_value_tl" in g:
        fs = np.log((g["value_tl"] / g["s_value_tl"]).where((g["value_tl"] > 0) & (g["s_value_tl"] > 0)))
        g["fsr"] = fs - fs.rolling(60, min_periods=20).median().shift(1)
    else: g["fsr"] = np.nan
    g["r"] = g["L_r_set"]
    sym = SPOT[u]
    dc = spot_decomp(u)
    g = g.join(dc[["cc", "gap", "intra"]].add_prefix("sp_"), how="left")
    g["m"] = xu100.reindex(g.index)
    # hedefler t+1
    for c in ["sp_gap", "sp_intra", "sp_cc", "L_r_set"]:
        g[f"y_{c}"] = g[c].shift(-1)
    g["y_cc_2_5"] = g["sp_cc"].shift(-2).rolling(4).sum().shift(-3)  # t+2..t+5
    g["rdOI"] = g["r"] * g["dOI_z"].clip(-4, 4)
    g["rv"] = g["r"] * g["vsur"].clip(-3, 3)
    g["rf"] = g["r"] * g["fsr"].clip(-3, 3)
    g["und"] = u
    panel.append(g.reset_index())
P = pd.concat(panel, ignore_index=True)
P = P[~P["exp_day"]]  # vade sonu günlerini sinyal günü olarak dışla
P.to_parquet(RES + "/oi_panel.parquet", index=False)
SIG = ["dOI_z", "rdOI", "vsur", "rv", "fsr", "rf"]
TGT = ["y_sp_gap", "y_sp_intra", "y_sp_cc", "y_L_r_set", "y_cc_2_5"]
def ts_test(g, s, y):
    cols = [s, "r", "m"] + ([s.replace("rdOI", "dOI_z").replace("rv", "vsur").replace("rf", "fsr")] if s in ("rdOI", "rv", "rf") else [])
    cols = list(dict.fromkeys(cols))
    df = g[[y] + cols].dropna()
    if len(df) < 120: return None
    Z = (df[cols] - df[cols].mean()) / df[cols].std()
    m = sm.OLS(df[y], sm.add_constant(Z)).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
    return m.params[s] * 1e4, m.tvalues[s], len(df)  # bps per 1 sd
res = []
for (u, g) in P.groupby("und"):
    g = g.set_index("date")
    for s in SIG:
        for y in TGT:
            for per, a, b in [("ALL", "2000", "2100"), ("IS", "2000", "2022-12-31"), ("OOS", "2023-01-01", "2100")]:
                gg = g[(g.index >= a) & (g.index <= b)]
                r = ts_test(gg, s, y)
                if r: res.append(dict(und=u, sig=s, tgt=y, per=per, b_bps_sd=r[0], t=r[1], n=r[2]))
R = pd.DataFrame(res)
# Fama-MacBeth (sadece hisseler): her gün kesit regresyonu y ~ z(s) (kesit standardize), eğimlerin NW t'si
fm = []
PS = P[P["und"].isin(STOCKS)]
LQ = pd.read_csv(RES + "/liquidity_raw.csv").set_index("und")["liq_class"]
for s_ in SIG:
    for y in TGT:
        ct = ("r",)
        for r in fama_macbeth(PS, s_, y, ct): r.update(sub="all"); fm.append(r)
        for r in fama_macbeth(PS[PS["und"].map(LQ).isin(["A", "B"])], s_, y, ct, min_n=8): r.update(sub="AB"); fm.append(r)
FM = pd.DataFrame(fm)
R.to_csv(RES + "/oi_ts_tests.csv", index=False); FM.to_csv(RES + "/oi_fm_tests.csv", index=False)
pd.set_option("display.width", 250)
print(FM.pivot_table(index=["sig", "sub", "tgt"], columns="per", values=["bps_per_sd", "t"]).round(2).to_string())
A = R[R["per"] == "ALL"].copy(); A["p"] = ll.t_to_p(A["t"]); A["fdr"], A["padj"] = ll.fdr(A["p"].values)
print("TS testleri:", len(A), "FDR geçen:", A["fdr"].sum())
print(A[A["fdr"]].sort_values("t").to_string())
print(A[A["und"].isin(["XU030", "XLBNK"])].round(2).to_string())
