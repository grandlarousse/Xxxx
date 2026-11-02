"""Görev 3: Baz = ln(F/S) ile teorik taşıma (r_TL*tau - temettü) farkı; anomali -> ertesi gün spot/vadeli.
- Spot: Yahoo 'c' (bölünme düzeltmeli, temettü düzeltmesiz). Bülten fiyatı düzeltmesiz -> ölçek K_t vade sonu günlerinde
  (pay vadelisinde vade sonu uzlaşma = spot kapanış seansı fiyatı) kalibre edilir; vade arasında sıçrama günü ln(F/S)'deki en büyük kırılım.
- r_TL: USDTRY vadeli takvim yayılımı ln(F2/F1)/(tau2-tau1) + r_USD(^IRX). 5 günlük medyan. -> results/rates.parquet
- Temettü: Yahoo adj/c oranındaki sıçrama (ex-tarih), d = 1 - f_{e-1}/f_e. Teorik baz b* = r*tau - sum(d_e, e in (t, vade]).
Çıktı: results/basis_panel.parquet, results/basis_tests.csv
"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from vcommon import *
import statsmodels.api as sm
D = pd.read_parquet(RES + "/daily_all.parquet")
# ---- faiz ----
u = D[D["und"] == "USDTRY"].set_index("date").sort_index()
tau1, tau2 = u["c1_dte"] / 365, u["c2_dte"] / 365
rdiff = np.log(u["c2_settle"] / u["c1_settle"]) / (tau2 - tau1)
irx = ll.daily("^IRX", "c") / 100
r_usd = irx.reindex(rdiff.index, method="ffill")
r_tl = (rdiff + r_usd).rolling(5, min_periods=2).median()
rates = pd.DataFrame({"r_tl_impl": r_tl, "r_diff_raw": rdiff, "r_usd": r_usd})
rates.to_parquet(RES + "/rates.parquet")
print("r_TL (USDTRY örtük, yıllık) yıl sonları:\n", r_tl.groupby(r_tl.index.year).agg(["mean", "min", "max"]).round(3).to_string())
# ---- dayanak bazında ----
def divs(sym):
    d = spot_daily(sym.replace(".IS", "")) if False else None
    raw = ll.raw(sym).copy(); raw.index = pd.DatetimeIndex(raw["ldate"].values); raw = raw[~raw.index.duplicated(keep="last")]
    f = raw["adj"] / raw["c"]; dd = 1 - f.shift(1) / f
    dd = dd[(dd > 0.001) & (dd < 0.3)]
    return dd
def build(und):
    g = D[D["und"] == und].set_index("date").sort_index().copy()
    if "s_c" not in g or g["s_c"].isna().all(): return None
    q = np.log(g["L_settle"] / g["s_c"])
    # K kalibrasyonu
    if und in IDX:
        k = np.round(q / np.log(10)) * np.log(10)  # 10'un kuvvetleri (endeks ölçek değişimi)
        lnK = k
    else:
        exp_days = g.index[g["c1_dte"] == 0]
        KE = np.log(g.loc[exp_days, "c1_settle"] / g.loc[exp_days, "s_c"])
        lnK = pd.Series(np.nan, index=g.index)
        prevE = None
        for E in exp_days:
            seg = (g.index > (prevE if prevE is not None else g.index[0] - pd.Timedelta(days=1))) & (g.index <= E)
            if prevE is not None and abs(KE[E] - KE[prevE]) > 0.02:
                qq = q[seg]; dq = qq.diff().abs()
                # ilk gün: önceki vadeye göre fark
                dq.iloc[0] = abs(qq.iloc[0] - q[q.index <= prevE].iloc[-1]) if (q.index <= prevE).any() else 0
                s = dq.idxmax()
                lnK[seg & (g.index < s)] = KE[prevE]; lnK[seg & (g.index >= s)] = KE[E]
            else:
                lnK[seg] = KE[E]
            prevE = E
        lnK = lnK.ffill()
    g["lnK"] = lnK
    g["S_true"] = g["s_c"] * np.exp(g["lnK"])
    for p in ["L", "c1", "c2"]:
        g[f"b_{p}"] = np.log(g[f"{p}_settle"] / g["S_true"])
    g["b_L_close"] = np.log(g["L_close"] / g["S_true"])
    g["tau_L"] = g["L_dte"] / 365
    g["r_tl"] = rates["r_tl_impl"].reindex(g.index).ffill()
    # temettü
    if und not in IDX:
        dd = divs(SPOT[und])
        divsum = []
        for t, E in zip(g.index, g["L_expiry"]):
            if pd.isna(E): divsum.append(np.nan); continue
            divsum.append(dd[(dd.index > t) & (dd.index <= E)].sum())
        g["div_L"] = divsum
        g["div_near"] = [dd[(dd.index > t) & (dd.index <= E + pd.Timedelta(days=7))].sum() if pd.notna(E) else np.nan for t, E in zip(g.index, g["L_expiry"])]
    else:
        g["div_L"] = 0.0; g["div_near"] = 0.0
    g["b_star"] = g["r_tl"] * g["tau_L"] - g["div_L"]
    g["anom"] = g["b_L"] - g["b_star"]
    g["anom_close"] = g["b_L_close"] - g["b_star"]
    # bayat / kötü günler
    bad = (g["L_trades"] < 5) | (g["s_v"].fillna(0) <= 0) | (g["anom"].abs() > 0.10) | (g["L_dte"] <= 0)
    g.loc[bad, ["anom", "anom_close"]] = np.nan
    # sapma: kendi 60g medyanından (geçmiş, t dahil değil)
    g["anom_dev"] = g["anom"] - g["anom"].rolling(60, min_periods=20).median().shift(1)
    g["anom_close_dev"] = g["anom_close"] - g["anom_close"].rolling(60, min_periods=20).median().shift(1)
    # hedefler
    dc = spot_decomp(und)
    if dc is not None:
        g = g.join(dc[["cc", "gap", "intra"]].add_prefix("sp_"), how="left")
    g["und"] = und
    return g
parts = [build(x) for x in STOCKS + ["XU030", "XLBNK", "X10XB"]]
B = pd.concat([p for p in parts if p is not None])
B.index.name = "date"
keep = ["und", "L_code", "L_dte", "L_settle", "L_close", "S_true", "lnK", "b_L", "b_c1", "b_c2", "b_L_close", "tau_L", "r_tl", "div_L", "div_near", "b_star",
        "anom", "anom_close", "anom_dev", "anom_close_dev", "L_r_set", "L_r_cls", "L_r_intra", "L_r_on", "sp_cc", "sp_gap", "sp_intra", "L_trades", "value_tl", "s_value_tl"]
B = B[keep].reset_index()
B.to_parquet(RES + "/basis_panel.parquet", index=False)
print("basis panel", B.shape)
# ----- özet: vade sonu yakınsaması, baz düzeyi -----
st = B[B["und"].isin(STOCKS)]
st["dte_b"] = pd.cut(st["L_dte"], [0, 3, 7, 14, 21, 31, 45, 70, 400])
print("\nPay vadelisi: ortalama baz, teorik ve anomali (bps) DTE kovasına göre:")
print((1e4 * st.groupby("dte_b")[["b_L", "b_star", "anom"]].median()).round(1).to_string())
print("\nanomali |medyan| ve std (bps) yıl bazında:")
print((1e4 * st.groupby(st["date"].dt.year)["anom"].agg(["median", "std"])).round(1).to_string())
