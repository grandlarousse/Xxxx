"""(e) Akşam seansı (VİOP endeks vadelileri 19:00-23:00 TSİ = 16:00-20:00 UTC). Bültende akşam fiyatı yok -> ES=F saatlik vekil.
Soru: BIST kapanışında (uzlaşma t) açılan F_XU030 pozisyonu için akşam seansı ne sağlar?
 1) Ertesi uzlaşma getirisi r(t->t+1) varyansının ne kadarı akşam seansı süresince (ES 15:00->20:00 UTC) ortaya çıkıyor?
    r_next ~ ES_ev(15->20) + ES_night(20->06) + ES_day(06->15, t+1).  -> kısmi R2.
 2) Akşamda bilinen ES hareketi ertesi uzlaşmayı ne kadar öngörüyor (b_ev)? Akşam fiyatı ~ settle_t*exp(g*ES_ev) varsayımıyla
    akşam seansında pozisyonu kapatmanın / tersine çevirmenin risk etkisi. g iki uçla: g = b_ev (akşam fiyatı ertesi beklentiyi tam yansıtır)
    ve g = beta_sync (gün içi saatlik XU030~ES eşzamanlı beta).
 3) 'Akşam stop' kuralı: uzun pozisyon, ES_ev < -x ise akşamda kapat (akşam fiyatı modelle). Ortalama, std, en kötü %1, MaxDD.
 4) 'Akşam giriş': akşamda ES_ev yönünde gir, ertesi uzlaşmada çık: kâr = r_next - g*ES_ev (g'ye çok duyarlı -> yalnız sınır).
"""
import numpy as np, pandas as pd, klib as K, ll
import statsmodels.api as sm
F = K.fut_panel(); R = F["XU030"].dropna()
es = K.snap  # helper
e15 = K.snap("ES=F", "15:15"); e20 = K.snap("ES=F", "20:00"); e06 = K.snap("ES=F", "06:00"); e15b = K.snap("ES=F", "15:00")
cal = R.index[R.index >= "2024-06-12"]
rows = []
for i in range(len(cal) - 1):
    t0, t1 = cal[i], cal[i + 1]
    if (t1 - t0).days > 4: continue
    a = e15.get(t0); b = e20.get(t0); c = e06.get(t1); d = e15b.get(t1)
    rows.append(dict(date=t0, es_ev=np.log(b / a), es_night=np.log(c / b), es_day=np.log(d / c), r_next=R.get(t1), wd=t0.weekday()))
E = pd.DataFrame(rows).set_index("date").dropna()
X = sm.add_constant(E[["es_ev", "es_night", "es_day"]]); m = sm.OLS(E["r_next"], X).fit(cov_type="HC1")
print(m.summary().tables[1]); print("R2", round(m.rsquared, 3), "n", len(E))
def r2(cols):
    return sm.OLS(E["r_next"], sm.add_constant(E[cols])).fit().rsquared
full = r2(["es_ev", "es_night", "es_day"])
part = {c: full - r2([x for x in ["es_ev", "es_night", "es_day"] if x != c]) for c in ["es_ev", "es_night", "es_day"]}
only = {c: r2([c]) for c in ["es_ev", "es_night", "es_day"]}
var_share = {c: (m.params[c] ** 2 * E[c].var()) / E["r_next"].var() for c in ["es_ev", "es_night", "es_day"]}
print("kısmi R2", {k: round(v, 3) for k, v in part.items()}, "tek başına R2", {k: round(v, 3) for k, v in only.items()}, "varyans payı", {k: round(v, 3) for k, v in var_share.items()})
b_ev_only = sm.OLS(E["r_next"], sm.add_constant(E[["es_ev"]])).fit(cov_type="HC1")
g_hi = b_ev_only.params["es_ev"]
# eşzamanlı beta: spot XU030 saatlik vs ES saatlik (07:00-15:00 UTC)
x = ll.raw("XU030.IS", "h1"); x = x[~x.index.duplicated()]; xs = pd.Series(np.log(x["c"]).diff().values, index=x.index)
eh = ll.raw("ES=F", "h1"); eh = eh[~eh.index.duplicated()]
# ES'i BIST bar bitişlerine hizala
ends = x.index + pd.Timedelta(minutes=60)
def at(ts):
    s = pd.Series(eh["c"].values, index=eh.index + pd.Timedelta(minutes=60)).sort_index()
    pos = s.index.searchsorted(ts, side="right") - 1; return np.where(pos >= 0, s.values[np.clip(pos, 0, None)], np.nan)
esx = pd.Series(np.log(at(ends)), index=x.index).diff()
df = pd.concat([xs.rename("x"), esx.rename("e")], axis=1).dropna()
df = df[(df.index.hour >= 7) & (df.index.hour <= 13) & (df.index >= "2024-06-12")]
df = df[(df["x"].abs() < 0.05) & (df["e"].abs() < 0.05)]
g_sync = sm.OLS(df["x"], sm.add_constant(df["e"])).fit().params["e"]
print("g_hi (b_ev, ertesi uzlaşmaya geçiş) =", round(g_hi, 3), " t", round(b_ev_only.tvalues['es_ev'], 2), " g_sync (gün içi saatlik beta) =", round(g_sync, 3))
out = []
for g_lab, g in (("g=b_ev", g_hi), ("g=beta_sync", g_sync)):
    ev_px = g * E["es_ev"]          # akşam seansı kapanışında model XU030 getirisi (uzlaşmadan)
    resid = E["r_next"] - ev_px      # akşamdan ertesi uzlaşmaya kalan
    for x_ in (0.0025, 0.005, 0.0075, 0.01):
        stop = E["es_ev"] < -x_
        pnl_hold = E["r_next"]; pnl_stop = np.where(stop, ev_px - 3e-4, E["r_next"])  # akşamda çıkış: ~3 bps ek maliyet
        pnl_stop = pd.Series(pnl_stop, index=E.index)
        for lab, p in (("tut", pnl_hold), ("akşam_stop", pnl_stop)):
            eq = p.cumsum()
            out.append(dict(g=g_lab, x_pct=x_ * 100, rule=lab, n=len(p), n_stop=int(stop.sum()), mean_bps=p.mean() * 1e4, sd_bps=p.std() * 1e4,
                            q01_bps=p.quantile(0.01) * 1e4, q05_bps=p.quantile(0.05) * 1e4, worst_bps=p.min() * 1e4, maxdd_pct=(eq - eq.cummax()).min() * 100,
                            mean_on_stopdays_hold=E["r_next"][stop].mean() * 1e4, mean_on_stopdays_after_ev=resid[stop].mean() * 1e4))
    # akşam giriş: |ES_ev|>x yönünde gir, kâr = r_next - g*ES_ev
    for x_ in (0.0025, 0.005, 0.01):
        sel = E["es_ev"].abs() > x_
        pr = (np.sign(E["es_ev"]) * resid)[sel]
        m_, t_, n_ = K.mean_nw(pr, 1)
        out.append(dict(g=g_lab, x_pct=x_ * 100, rule="akşam_giriş(ES yönü)", n=n_, mean_bps=m_ * 1e4, sd_bps=pr.std() * 1e4, t=t_))
O = pd.DataFrame(out); O.to_csv(K.RES + "/e_evening.csv", index=False)
pd.set_option("display.width", 250); print(O.round(2).to_string())
# Pazartesi etkisi: Cuma akşamı -> Pazartesi (hafta sonu) ayrı
E["fri"] = E["wd"] == 4
print("Cuma->Pzt r_next std", round(E[E.fri]["r_next"].std() * 1e4, 1), "diğer", round(E[~E.fri]["r_next"].std() * 1e4, 1))
E.to_csv(K.RES + "/e_evening_panel.csv")
