"""03: ASELS savunma sürücüleri. A) yıllık rejim; B) Kore lag0 (BIST açılışından önce kapanır); C) Avrupa post-BIST-close (saatlik);
D) saatlik senkron/öncülük; E) jeopolitik olay çalışması (haber tarihli); F) veri güdümlü EU_DEF şok günleri."""
from sv import *
import statsmodels.api as sm
pd.set_option("display.width", 220)
a = R("ASELS"); m = R("XU100"); fx = R("FXAL"); a_usd = a - fx; m_usd = m - fx
dd = ll.decomp("ASELS")
D = {k: drv(k) for k in ["EU_DEF", "US_DEF", "KR_DEF", "ITA", "ESLT", "RHM.DE", "^KS11", "ES=F", "^STOXX", "OTKAR.IS"]}
# ---------- A) yıllık rejim
rows = []
for y in range(2010, 2027):
    s, e = f"{y}-01-01", f"{y}-12-31"; r = {"year": y}
    for k in ["EU_DEF", "US_DEF", "KR_DEF", "ESLT", "OTKAR.IS"]:
        aa = a[(a.index >= s) & (a.index <= e)]
        r["c_" + k] = pd.concat([aa, D[k]], axis=1).dropna().corr().iloc[0, 1]
        r["pc_" + k] = ll.partial_corr(aa, D[k], [m])[0]
    au = a_usd[(a_usd.index >= s) & (a_usd.index <= e)]
    r["pcUSD_EU_DEF"] = ll.partial_corr(au, D["EU_DEF"], [m_usd, D["^STOXX"]])[0]
    r["pc_EU_DEF_ctrl_stoxx"] = ll.partial_corr(a[(a.index >= s) & (a.index <= e)], D["EU_DEF"], [m, D["^STOXX"]])[0]
    rows.append(r)
A = pd.DataFrame(rows).set_index("year"); A.to_csv(RES + "/03A_regime_year.csv")
print("A) yıllık (c=ham, pc=XU100 kontrollü):"); print(A[["c_EU_DEF", "pc_EU_DEF", "pc_EU_DEF_ctrl_stoxx", "pcUSD_EU_DEF", "pc_US_DEF", "pc_KR_DEF", "pc_ESLT", "pc_OTKAR.IS"]].round(2).to_string())
for lab, s, e in [("2014-2021", "2014-01-01", "2021-12-31"), ("2022-2026", "2022-01-01", "2026-12-31"), ("2024-2026", "2024-01-01", "2026-12-31")]:
    aa = a[(a.index >= s) & (a.index <= e)]
    x = {k: round(ll.partial_corr(aa, D[k], [m, D["^STOXX"]])[0], 3) for k in ["EU_DEF", "US_DEF", "KR_DEF", "RHM.DE"]}
    x2 = {k: round(ll.partial_corr(aa, D[k], [m])[0], 3) for k in ["EU_DEF", "US_DEF", "KR_DEF", "RHM.DE"]}
    print("rejim", lab, "pc|XU100:", x2, " pc|XU100+STOXX:", x)
# ---------- B) Kore lag0 -> ASELS gap/intra (Kore 06:30 UTC kapanır, BIST 07:00'de açılır)
print("\nB) Kore savunma (lag0, BIST öncesi) -> ASELS")
for y in ["gap", "intra"]:
    for lab, s, e in [("ALL", "2014", "2027"), ("IS", "2014", "2021"), ("OOS", "2021", "2027"), ("2022+", "2022", "2027")]:
        z = pd.concat([dd[y].rename("y"), D["KR_DEF"].rename("kr"), D["^KS11"].rename("ks"), D["ES=F"].shift(1).rename("es1"), m.shift(1).rename("m1")], axis=1).dropna()
        z = z[(z.index >= s) & (z.index < e)]
        mm = sm.OLS(z.y, sm.add_constant(z[["kr", "ks", "es1"]])).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
        b, t, n = ll.nw_t(z.y, z.kr)
        print(f"  {y:5s} {lab:5s} uni: corr {z.y.corr(z.kr):.3f} t {t:.2f} | multi(kr|KS11,ES lag1): b_kr {mm.params['kr']:.3f} t {mm.tvalues['kr']:.2f}  n {n}")
# ---------- C) Avrupa post-BIST-close (15:00 -> 16:30 UTC) -> ASELS ertesi gün
eu_syms = ["RHM.DE", "BA.L", "LDO.MI", "SAAB-B.ST"]
post = pd.concat([np.log(ll.snap_daily(s, "16:40") / ll.snap_daily(s, "15:00")).rename(s) for s in eu_syms], axis=1).mean(axis=1)
espost = np.log(ll.snap_daily("ES=F", "21:00") / ll.snap_daily("ES=F", "15:00"))
cal = ll.bist_cal(); C = pd.DataFrame({"eu_post": post.reindex(cal), "es_post": espost.reindex(cal), "gap1": dd["gap"].shift(-1).reindex(cal), "intra1": dd["intra"].shift(-1).reindex(cal)}).dropna()
C = C[C.eu_post.abs() < 0.1]
for y in ["gap1", "intra1"]:
    b, t, n = ll.nw_t(C[y], C.eu_post)
    mm = sm.OLS(C[y], sm.add_constant(C[["eu_post", "es_post"]])).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
    print(f"C) ASELS {y} ~ EU_DEF post-close: corr {C[y].corr(C.eu_post):.3f} t {t:.2f} n {n} | +ES_post: b {mm.params['eu_post']:.3f} t {mm.tvalues['eu_post']:.2f}")
# ---------- D) saatlik: EU savunma saat (H-1:00,H:00] vs ASELS (H-1:30,H:30] (senkron yaklaşık) ve (H:30,H+1:30] (öncülük)
rows = []
for H in range(9, 15):
    eu = pd.concat([np.log(ll.snap_daily(s, f"{H}:00") / ll.snap_daily(s, f"{H-1}:00")).rename(s) for s in eu_syms], axis=1).mean(axis=1)
    as_sync = np.log(ll.snap_daily("ASELS.IS", f"{H}:30") / ll.snap_daily("ASELS.IS", f"{H-1}:30"))
    xu_sync = np.log(ll.snap_daily("XU100.IS", f"{H}:30") / ll.snap_daily("XU100.IS", f"{H-1}:30"))
    if H < 14:
        as_lead = np.log(ll.snap_daily("ASELS.IS", f"{H+1}:30") / ll.snap_daily("ASELS.IS", f"{H}:30"))
    else:
        as_lead = np.log(ll.snap_daily("ASELS.IS", "15:10") / ll.snap_daily("ASELS.IS", "14:30"))
    z = pd.concat([eu.rename("eu"), as_sync.rename("s"), as_lead.rename("l"), xu_sync.rename("x")], axis=1).dropna()
    z = z[(z.abs() < 0.08).all(axis=1)]
    rows.append({"H": H, "n": len(z), "sync_c": z.eu.corr(z.s), "sync_pc_xu": ll.partial_corr(z.s, z.eu, [z.x])[0], "lead_c": z.eu.corr(z.l), "lead_t": ll.nw_t(z.l, z.eu)[1]})
Dh = pd.DataFrame(rows); Dh.to_csv(RES + "/03D_hourly.csv", index=False); print("D) saatlik:"); print(Dh.round(3).to_string(index=False))
# ---------- E) olay çalışması: AR = r - beta*XU100 (beta: önceki 250g)
ev = pd.read_csv(CODE + "/events.csv", parse_dates=["bist_day0"])
beta = (a.rolling(250, min_periods=120).cov(m) / m.rolling(250, min_periods=120).var()).shift(1)
ar = a - beta * m
# olay günleri için TEMİZLENMEMİŞ getiri (2022-02-24 ASELS -%10 taban günü temizlikte NaN oluyordu)
a_raw = ll.ret("ASELS", clean=False).reindex(a.index); m_raw = ll.ret("XU100", clean=False).reindex(a.index); ar_raw = a_raw - beta * m_raw
eu_ar = D["EU_DEF"] - (D["EU_DEF"].rolling(250, min_periods=120).cov(D["^STOXX"]) / D["^STOXX"].rolling(250, min_periods=120).var()).shift(1) * D["^STOXX"]
idx = a.index
res = []
for _, r in ev.iterrows():
    p = idx.searchsorted(r.bist_day0)
    if p >= len(idx): continue
    d0 = idx[p]
    def car(s, k0, k1): return float(s.iloc[p + k0:p + k1 + 1].sum()) if p + k1 < len(s) else np.nan
    res.append({"date": d0.date(), "event": r.event, "type": r.type, "conf": r.date_conf, "ASELS_r0": a_raw.iloc[p], "ASELS_AR0": ar_raw.iloc[p],
                "ASELS_AR1": ar_raw.iloc[p + 1] if p + 1 < len(ar) else np.nan, "ASELS_CAR0_5": car(ar_raw, 0, 5), "XU100_r0": m_raw.iloc[p],
                "EU_DEF_r0": D["EU_DEF"].reindex(idx).iloc[p], "EU_DEF_AR0": eu_ar.reindex(idx).iloc[p], "EU_DEF_r1": D["EU_DEF"].reindex(idx).iloc[p + 1] if p + 1 < len(idx) else np.nan})
E = pd.DataFrame(res); E.to_csv(RES + "/03E_events.csv", index=False)
print("E) olaylar (bps):"); e2 = E.copy()
for c in [c for c in E.columns if c.startswith(("ASELS", "XU", "EU"))]: e2[c] = (1e4 * E[c]).round(0)
print(e2[["date", "type", "event", "ASELS_r0", "ASELS_AR0", "ASELS_AR1", "ASELS_CAR0_5", "XU100_r0", "EU_DEF_r0", "EU_DEF_AR0"]].to_string(index=False))
for ty in E.type.unique():
    z = E[E.type == ty]
    print(f"  tip={ty} n={len(z)} ort AR0 {1e4*z.ASELS_AR0.mean():.0f}bps (t {z.ASELS_AR0.mean()/(z.ASELS_AR0.std()/np.sqrt(len(z))):.2f}) ort CAR0-5 {1e4*z.ASELS_CAR0_5.mean():.0f}bps; EU_DEF_AR0 ort {1e4*z.EU_DEF_AR0.mean():.0f}bps; işaret uyumu AR0 vs EU_AR0 {(np.sign(z.ASELS_AR0)==np.sign(z.EU_DEF_AR0)).mean():.2f}")
# ---------- F) veri güdümlü EU_DEF şok günleri (EU_DEF STOXX'a göre anormal getirisi, geçmiş 250g sd ile z)
z = eu_ar / eu_ar.rolling(250, min_periods=120).std().shift(1)
F = pd.DataFrame({"z": z, "ar": ar, "gap1": dd["gap"].shift(-1), "intra1": dd["intra"].shift(-1), "ar1": ar.shift(-1), "car1_5": ar.shift(-1).rolling(5).sum().shift(-4)}).dropna(subset=["z", "ar"])
for thr in [2.0, 3.0]:
    for lab, s, e in [("2010-21", "2010", "2022"), ("2022-26", "2022", "2027")]:
        f = F[(F.index >= s) & (F.index < e)]
        up = f[f.z > thr]; dn = f[f.z < -thr]
        print(f"F) |z|>{thr} {lab}: UP n={len(up)} ASELS AR0 {1e4*up.ar.mean():.0f} AR1 {1e4*up.ar1.mean():.0f} intra1 {1e4*up.intra1.mean():.0f} | DOWN n={len(dn)} AR0 {1e4*dn.ar.mean():.0f} AR1 {1e4*dn.ar1.mean():.0f} intra1 {1e4*dn.intra1.mean():.0f}")
F.to_parquet(RES + "/03F_shock.parquet")
for lab, s, e in [("2010-21", "2010", "2022"), ("2022-26", "2022", "2027")]:
    f = F[(F.index >= s) & (F.index < e)]
    print(f"F) corr(ASELS AR0, EU_DEF z) {lab}: {f.ar.corr(f.z):.3f}; corr(AR1, z) {f.ar1.corr(f.z):.3f}; corr(intra1, z) {f[['intra1','z']].dropna().corr().iloc[0,1]:.3f}; corr(gap1,z) {f[['gap1','z']].dropna().corr().iloc[0,1]:.3f}")
