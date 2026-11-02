"""Görev 5: (a) vadeli kapanış (XU030 18:15, pay vadelisi 18:10) vs spot kapanış (18:10):
     m_t = ln(F_close/F_settle) (uzlaşma = son 10 dk VWAP) ve b_close - b_settle -> ertesi spot gap / vadeli gece getirisi.
  (b) vadeli açılış (09:30; 23.09.2022'den beri 09:20-09:30 tek fiyat açılış seansı) vs spot açılış (09:55 müzayede, 10:00 sürekli):
     gF = ln(F_open_{t+1}/F_settle_t), gS = spot gap_{t+1}. gS ~ gF (beta, R2). Kalıntı u = gS - beta_hat*gF (genişleyen pencere) -> spot gün-içi_{t+1}.
     gF -> spot gün-içi_{t+1} (spot açılışı vadeli bilgisini eksik/aşırı mı fiyatlıyor?)
  (c) akşam seansı: bülten fiyatları akşam seansını içermiyor (04_evening.py). ES akşam penceresi (15->20 UTC) -> vadeli gün-içi_{t+1} / spot gün-içi_{t+1}.
"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from vcommon import *
import statsmodels.api as sm
B = pd.read_parquet(RES + "/basis_panel.parquet")
D = pd.read_parquet(RES + "/daily_all.parquet")
out = []
def ols(y, X, lags=5):
    df = pd.concat([y.rename("y"), X], axis=1).replace([np.inf, -np.inf], np.nan).dropna()
    if len(df) < 100: return None
    m = sm.OLS(df["y"], sm.add_constant(df.drop(columns="y"))).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    return m, len(df)
recs = []
for u in STOCKS + ["XU030", "XLBNK"]:
    g = B[B["und"] == u].set_index("date").sort_index().copy()
    d = D[D["und"] == u].set_index("date").sort_index()
    g["F_open"] = d["L_open"].reindex(g.index); g["F_prev_settle"] = d["L_prev_settle"].reindex(g.index)
    g["F_prev_close"] = d["L_prev_close"].reindex(g.index)
    # (a) kapanış sonrası
    g["m"] = np.log(g["L_close"] / g["L_settle"])
    g["db"] = g["b_L_close"] - g["b_L"]
    g["gF"] = np.log(g["F_open"] / g["F_prev_settle"])      # vadeli gece (uzlaşma -> 09:30 açılış)
    g["gFc"] = np.log(g["F_open"] / g["F_prev_close"])      # vadeli gece (kapanış -> açılış)
    g["y_gap"] = g["sp_gap"].shift(-1); g["y_intra"] = g["sp_intra"].shift(-1)
    g["y_gFc"] = g["gFc"].shift(-1); g["y_Fintra"] = g["L_r_intra"].shift(-1)
    rec = dict(und=u)
    r = ols(g["y_gap"], g[["m"]])
    if r: rec.update(m_gap_b=r[0].params["m"], m_gap_t=r[0].tvalues["m"], n_a=r[1])
    r = ols(g["y_gFc"], g[["m"]])
    if r: rec.update(m_fgap_b=r[0].params["m"], m_fgap_t=r[0].tvalues["m"])
    r = ols(g["y_gap"], g[["db"]])
    if r: rec.update(db_gap_b=r[0].params["db"], db_gap_t=r[0].tvalues["db"])
    # (b) açılış: gS_t ~ gF_t  (aynı gün t: vadeli 09:30 açılışı spot 10:00 açılışından önce)
    r = ols(g["sp_gap"], g[["gF"]])
    if r:
        rec.update(open_beta=r[0].params["gF"], open_r2=r[0].rsquared, n_b=r[1])
    # genişleyen pencere beta -> kalıntı (look-ahead yok)
    x = g[["sp_gap", "gF", "sp_intra"]].dropna()
    if len(x) > 200:
        cov = (x["sp_gap"] * x["gF"]).expanding(120).mean().shift(1) - (x["sp_gap"].expanding(120).mean().shift(1) * x["gF"].expanding(120).mean().shift(1))
        var = x["gF"].expanding(120).var().shift(1)
        bh = cov / var
        x["u"] = x["sp_gap"] - bh * x["gF"]
        g["u"] = x["u"]
        r = ols(g["sp_intra"], g[["u"]])
        if r: rec.update(u_intra_b=r[0].params["u"], u_intra_t=r[0].tvalues["u"], u_intra_n=r[1])
        r = ols(g["sp_intra"], g[["gF"]])
        if r: rec.update(gF_intra_b=r[0].params["gF"], gF_intra_t=r[0].tvalues["gF"])
        # IS/OOS
        for per, a, b in [("IS", "2000", "2022-12-31"), ("OOS", "2023-01-01", "2100")]:
            gg = g[(g.index >= a) & (g.index <= b)]
            r = ols(gg["sp_intra"], gg[["u"]])
            if r: rec.update({f"u_intra_t_{per}": r[0].tvalues["u"], f"u_intra_b_{per}": r[0].params["u"], f"n_{per}": r[1]})
    recs.append(rec)
    g["und"] = u
    out.append(g.reset_index()[["date", "und", "m", "db", "gF", "gFc", "u", "sp_gap", "sp_intra", "y_gap", "y_intra", "y_gFc", "y_Fintra", "L_r_intra", "L_r_set"]] if "u" in g else
               g.reset_index()[["date", "und", "m", "db", "gF", "gFc", "sp_gap", "sp_intra", "y_gap", "y_intra", "y_gFc", "y_Fintra", "L_r_intra", "L_r_set"]])
R = pd.DataFrame(recs).set_index("und")
R.to_csv(RES + "/openclose_tests.csv")
O = pd.concat(out, ignore_index=True); O.to_parquet(RES + "/openclose_panel.parquet", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
print(R.round(3).to_string())
# (c) ES akşam penceresi -> ertesi gün-içi (vadeli ve spot), 2024-06+
es = ll.raw("ES=F", "h1"); esc = pd.Series(es["c"].values, index=es.index + pd.Timedelta(hours=1))
def at(ts):
    pos = esc.index.searchsorted(ts, side="right") - 1
    return esc.values[pos] if pos >= 0 else np.nan
cal = pd.DatetimeIndex(sorted(D["date"].unique())); cal = cal[cal >= "2024-06-12"]
E = []
for i in range(1, len(cal)):
    T0, T1 = cal[i - 1], cal[i]
    a15, a20, a0630 = at((T0 + pd.Timedelta(hours=15)).tz_localize("UTC")), at((T0 + pd.Timedelta(hours=20)).tz_localize("UTC")), at((T1 + pd.Timedelta(hours=6, minutes=30)).tz_localize("UTC"))
    a1500 = at((T1 + pd.Timedelta(hours=15)).tz_localize("UTC"))
    E.append(dict(date=T1, es_ev=np.log(a20 / a15), es_night=np.log(a0630 / a20), es_day=np.log(a1500 / a0630), gapdays=(T1 - T0).days))
E = pd.DataFrame(E).set_index("date"); E = E[E["gapdays"] <= 4]
res_c = []
for u in ["XU030", "XLBNK", "THYAO", "GARAN", "AKBNK"]:
    g = O[O["und"] == u].set_index("date").join(E, how="inner")
    for y in ["L_r_intra", "sp_intra", "gF"]:
        r = ols(g[y], g[["es_ev", "es_night"]])
        if r: res_c.append(dict(und=u, y=y, b_ev=r[0].params["es_ev"], t_ev=r[0].tvalues["es_ev"], b_night=r[0].params["es_night"], t_night=r[0].tvalues["es_night"], r2=r[0].rsquared, n=r[1]))
        # ES gün-içi kontrollü (eşzamanlı) - sadece bilgi
    # açılışa göre: akşam bilgisinin açılış gap'indeki payı (R2 ayrıştırması)
    x = g[["gF", "es_ev", "es_night"]].dropna()
    if len(x) > 100:
        r2_ev = sm.OLS(x["gF"], sm.add_constant(x[["es_ev"]])).fit().rsquared; r2_n = sm.OLS(x["gF"], sm.add_constant(x[["es_night"]])).fit().rsquared
        r2_b = sm.OLS(x["gF"], sm.add_constant(x[["es_ev", "es_night"]])).fit().rsquared
        res_c.append(dict(und=u, y="R2_decomp_gF", b_ev=r2_ev, t_ev=np.nan, b_night=r2_n, t_night=np.nan, r2=r2_b, n=len(x)))
RC = pd.DataFrame(res_c); RC.to_csv(RES + "/evening_es_tests.csv", index=False)
print(RC.round(3).to_string())
