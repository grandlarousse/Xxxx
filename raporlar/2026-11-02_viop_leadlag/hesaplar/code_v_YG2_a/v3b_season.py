"""v_YG2_a / 3b: mevsim testi. LH = log(C/P1430) (17:30 TSİ -> kapanış; yıl boyu ölçülebilir) yaz/kış sezonlarına göre;
yaz günlerinde CA sinyali; koşulsuz C->07:30 kayması (uzun-yalnız ayağın ne kadarı piyasa kayması?)."""
import numpy as np, pandas as pd, vcommon as v
P = v.load(); S = P[~P.stock.isin(["XU030", "XU100"])].copy()
y0 = S.date.dt.year - (S.date.dt.month < 6)
S["season"] = np.where(S.summer, "Y" + S.date.dt.year.astype(str), "K" + y0.astype(str) + "/" + (y0 + 1).astype(str))
rows = []
for se, gg in S.groupby("season"):
    b = gg.LH.notna() & gg.y_c730.notna() & ~gg.half
    if b.sum() < 100: continue
    dd, ntr, pnl = v.port(gg, "LH", "y_c730", 0.0025, b.values); m, t, n = v.nw_t(dd)
    d = gg[b][["y_c730", "LH", "date"]].dropna(); bb, s_, nn, G = v.ols_cl(d.y_c730.values, d[["LH"]].values, d.date.values)
    r = dict(season=se, days=n, LH_port_bps=m, LH_port_t=t, b_LH=bb[1], t_b_LH=bb[1] / s_[1], drift_c730_bps=1e4 * gg.y_c730.mean())
    bc = gg.CA.notna() & gg.y_c730.notna()
    if bc.sum() > 100:
        dd2, _, _ = v.port(gg, "CA", "y_c730", 0.0025, bc.values); m2, t2, _ = v.nw_t(dd2)
        d = gg[bc][["y_c730", "CA", "date"]].dropna(); bb, s_, nn, G = v.ols_cl(d.y_c730.values, d[["CA"]].values, d.date.values)
        r.update(CA_port_bps=m2, CA_port_t=t2, b_CA=bb[1], t_b_CA=bb[1] / s_[1])
        # uzun-yalnız ayak ve kayma
        L = gg[bc & (gg.CA < -0.0025)]; Sh = gg[bc & (gg.CA > 0.0025)]
        r.update(long_leg_bps=1e4 * L.y_c730.mean(), short_leg_bps=-1e4 * Sh.y_c730.mean())
    rows.append(r)
R = pd.DataFrame(rows); pd.set_option("display.width", 250); print(R.round(2).to_string())
# toplu: yaz vs kış
for lab, m in [("YAZ", S.summer), ("KIŞ", ~S.summer)]:
    b = m & S.LH.notna() & S.y_c730.notna() & ~S.half
    dd, ntr, pnl = v.port(S, "LH", "y_c730", 0.0025, b.values); mm, t, n = v.nw_t(dd)
    print(lab, f"LH-port {mm:.2f} (t {t:.2f}), gün {n}, koşulsuz C->07:30 kayması {1e4 * S[b].y_c730.mean():.2f} bps")
# yaz: kayma düzeltmeli uzun/kısa ayak (aynı günün kesitsel ortalaması çıkarılarak)
b = S.CA.notna() & S.y_c730.notna()
S["y_dm"] = S.y_c730 - S.groupby("date").y_c730.transform("mean")
for lab, m in [("uzun (CA<-25)", b & (S.CA < -0.0025)), ("kısa (CA>25)", b & (S.CA > 0.0025))]:
    x = S[m]; sg = -np.sign(x.CA)
    print(lab, "brüt", round(1e4 * (sg * x.y_c730).mean(), 2), " kesitsel-ortalama-düzeltmeli", round(1e4 * (sg * x.y_dm).mean(), 2), " n", len(x))
R.to_csv(v.RES + "/v3b_season.csv", index=False)
