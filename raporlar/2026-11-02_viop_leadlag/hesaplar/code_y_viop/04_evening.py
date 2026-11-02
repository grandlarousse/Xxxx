"""Görev 5a: Bültendeki fiyat alanları akşam seansını (19:00-23:00 TSİ = 16:00-20:00 UTC) içeriyor mu?
Testler (ES=F saatlik, 2024-06+):
 (i)  gap_f = log(open_{T+1}/settle_T) ~ ES_ev (15:00->20:00 UTC, T) + ES_night (20:00 T -> 06:00 UTC T+1)
 (ii) excess_high_{T+1} = log(H_f,T+1) - log(max spot-h1-high_{T+1} * e^{basis}) ~ ES evening path max (16-20 UTC)
      kontrol: pay vadelileri (akşam seansı yok) aynı regresyon. İçeriyorsa XU030'da eğim>0, payda ~0.
 (iii) close_T vs settle_T: log(close/settle) std (akşam fiyatı olsaydı büyük olurdu) ve ES 15:00->20:00 ile korelasyonu.
"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from vcommon import *
D = pd.read_parquet(RES + "/daily_all.parquet")
es = ll.raw("ES=F", "h1").copy()
es_end = es.index + pd.Timedelta(hours=1)
esc = pd.Series(es["c"].values, index=es_end); esh = pd.Series(es["h"].values, index=es_end); esl = pd.Series(es["l"].values, index=es_end)
def at(ts):
    pos = esc.index.searchsorted(ts, side="right") - 1
    return np.where(pos >= 0, esc.values[np.clip(pos, 0, None)], np.nan)
rows = []
cal = pd.DatetimeIndex(sorted(D["date"].unique()))
cal = cal[cal >= "2024-06-12"]
for i in range(1, len(cal)):
    T0, T1 = cal[i - 1], cal[i]
    t15 = (T0 + pd.Timedelta(hours=15, minutes=0)).tz_localize("UTC"); t20 = (T0 + pd.Timedelta(hours=20)).tz_localize("UTC")
    t06 = (T1 + pd.Timedelta(hours=6)).tz_localize("UTC")
    b15, b20, b06 = at([t15])[0], at([t20])[0], at([t06])[0]
    w = esh[(esh.index > t15) & (esh.index <= t20)]; wl = esl[(esl.index > t15) & (esl.index <= t20)]
    wn = esh[(esh.index > t20) & (esh.index <= t06)]; wnl = esl[(esl.index > t20) & (esl.index <= t06)]
    rows.append(dict(date=T1, prev=T0, es_ev=np.log(b20 / b15), es_night=np.log(b06 / b20),
                     ev_up=np.log(w.max() / b15) if len(w) else np.nan, ev_dn=np.log(wl.min() / b15) if len(wl) else np.nan,
                     n_up=np.log(wn.max() / b15) if len(wn) else np.nan, n_dn=np.log(wnl.min() / b15) if len(wnl) else np.nan,
                     day_gap=(T1 - T0).days))
E = pd.DataFrame(rows).set_index("date")
# ES 15:00 T -> 15:00 T+1 içinde gün-içi (T+1 06:30-15:00) yolunu da al (gündüz seansı kontrolü)
def spot_h1_hilo(sym):
    h = ll.raw(sym, "h1").copy(); h["d"] = h.index.tz_convert(None).normalize()
    g = h.groupby("d").agg(hh=("h", "max"), ll_=("l", "min"))
    return g
import statsmodels.api as sm
res = []
for u in ["XU030", "XLBNK", "THYAO", "AKBNK", "GARAN", "YKBNK", "ISCTR", "ASELS", "TUPRS", "SAHOL", "KCHOL", "EREGL", "BIMAS", "TCELL"]:
    g = D[D["und"] == u].set_index("date").sort_index()
    g = g.join(E, how="inner")
    # aynı sözleşme: L sözleşmesi T+1; prev_settle ile ölç
    g["gap_f"] = np.log(g["L_open"] / g["L_prev_settle"])
    sh = spot_h1_hilo(SPOT[u])
    g = g.join(sh, how="left")
    g["basis"] = np.log(g["L_settle"] / g["s_c"])
    g["xs_hi"] = np.log(g["L_high"]) - np.log(g["hh"]) - g["basis"]
    g["xs_lo"] = np.log(g["L_low"]) - np.log(g["ll_"]) - g["basis"]
    # akşam yolu: settle_T seviyesinden ES'in akşam max'ı (endeks beta~1 varsayımı yok; eğim tahmin edilir)
    g["cl_set"] = np.log(g["L_close"] / g["L_settle"])
    g = g[(g["day_gap"] <= 4) & g["gap_f"].notna()]
    X = g[["es_ev", "es_night"]].dropna(); y = g.loc[X.index, "gap_f"]
    m = sm.OLS(y, sm.add_constant(X)).fit(cov_type="HC1")
    # excess high ~ ev_up (akşam), n_up (gece) ; excess low ~ ev_dn, n_dn
    Z = g[["xs_hi", "ev_up", "n_up", "xs_lo", "ev_dn", "n_dn"]].dropna()
    mh = sm.OLS(Z["xs_hi"], sm.add_constant(Z[["ev_up", "n_up"]])).fit(cov_type="HC1")
    ml = sm.OLS(Z["xs_lo"], sm.add_constant(Z[["ev_dn", "n_dn"]])).fit(cov_type="HC1")
    # (iii) close vs settle (aynı gün T+1) ile o günün ES 15->20 (T+1 akşamı) korelasyonu: E kaydırılmış
    E2 = E[["es_ev"]].copy(); E2.index = E["prev"]  # es_ev gün T'ye ait
    gg = D[D["und"] == u].set_index("date").sort_index().join(E2, how="inner")
    gg["cl_set"] = np.log(gg["L_close"] / gg["L_settle"])
    c3 = gg[["cl_set", "es_ev"]].dropna().corr().iloc[0, 1]
    res.append(dict(und=u, n=len(y), b_ev=m.params["es_ev"], t_ev=m.tvalues["es_ev"], b_night=m.params["es_night"], t_night=m.tvalues["es_night"], r2=m.rsquared,
                    hi_b_ev=mh.params["ev_up"], hi_t_ev=mh.tvalues["ev_up"], hi_b_n=mh.params["n_up"], hi_t_n=mh.tvalues["n_up"],
                    lo_b_ev=ml.params["ev_dn"], lo_t_ev=ml.tvalues["ev_dn"], lo_b_n=ml.params["n_dn"], lo_t_n=ml.tvalues["n_dn"],
                    xs_hi_mean_bps=1e4 * Z["xs_hi"].mean(), xs_lo_mean_bps=1e4 * Z["xs_lo"].mean(),
                    cl_set_std_bps=1e4 * gg["cl_set"].std(), corr_clset_esev=c3))
R = pd.DataFrame(res).set_index("und")
pd.set_option("display.width", 250); print(R.round(3).to_string())
R.to_csv(RES + "/evening_test.csv")

# (iv) Aynı gün T bülteni akşam seansının ilk kısmını (16:00-17:45 UTC, bülten üretimi ~17:00-18:00 UTC) içeriyor mu?
rows = []
for T0 in cal:
    t15 = (T0 + pd.Timedelta(hours=15, minutes=15)).tz_localize("UTC"); t1745 = (T0 + pd.Timedelta(hours=17, minutes=45)).tz_localize("UTC")
    b15 = at([t15])[0]
    w = esh[(esh.index > t15 + pd.Timedelta(minutes=45)) & (esh.index <= t1745)]; wl = esl[(esl.index > t15 + pd.Timedelta(minutes=45)) & (esl.index <= t1745)]
    rows.append(dict(date=T0, e_up=np.log(w.max() / b15) if len(w) else np.nan, e_dn=np.log(wl.min() / b15) if len(wl) else np.nan))
E3 = pd.DataFrame(rows).set_index("date")
out = []
for u in ["XU030", "XLBNK", "THYAO", "GARAN", "AKBNK"]:
    g = D[D["und"] == u].set_index("date").sort_index().join(E3, how="inner")
    sh = spot_h1_hilo(SPOT[u]); g = g.join(sh, how="left"); g["basis"] = np.log(g["L_settle"] / g["s_c"])
    g["hi_vs_set"] = np.log(g["L_high"] / g["L_settle"]); g["lo_vs_set"] = np.log(g["L_low"] / g["L_settle"])
    g["xs_hi"] = np.log(g["L_high"]) - np.log(g["hh"]) - g["basis"]; g["xs_lo"] = np.log(g["L_low"]) - np.log(g["ll_"]) - g["basis"]
    Z = g[["xs_hi", "xs_lo", "e_up", "e_dn"]].dropna()
    out.append(dict(und=u, n=len(Z), c_xshi_eup=Z["xs_hi"].corr(Z["e_up"]), c_xslo_edn=Z["xs_lo"].corr(Z["e_dn"])))
print(pd.DataFrame(out).round(3).to_string())
