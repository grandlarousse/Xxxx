"""v5: Maliyet duyarlılığı (gidiş-dönüş, işlem başına): taban 8 / 15 / 30 bps, kademeli (likit23 8, illikit24 15 veya 30)
+ SSF tik maliyeti = 1 tik (0,01 TL) / GÜNCEL fiyat (30.10.2026 kapanışı) — Yahoo fiyatı bölünme düzeltmeli olduğundan tarihsel nominal fiyat yok.
Hedge'li stratejide XU030 vadelisi için +3 bps. Gün-ağırlıklı (DW) ve işlem-ağırlıklı (TW) net.
Ana spesifikasyonlar: günlük E0 (2014–26), h1 dönemi E0 / TP1 / P0730 / TP2 -> C, idio hedge'li E0 ve P0730/TP1 (h1), CIMSA/OYAKC.
Çıktı: res/v5_costs.csv, res/v5_years.csv, res/v5_tick.csv"""
import numpy as np, pandas as pd, vc
TG = vc.VIOP
D = {s: vc.decomp(s) for s in TG + ["XU030"]}
H = {s: vc.h1_panel(s) for s in TG + ["XU030"]}
idx = vc.cal(); idx = idx[idx >= "2014-01-01"]
liq = pd.read_csv(vc.RES + "/v1_liq.csv", index_col=0); LIQ = list(liq.index[liq["rank"] <= 23])
px_now = pd.Series({s: D[s]["c"].dropna().iloc[-1] for s in TG})
tick_bps = 1e4 * 0.01 / px_now
pd.DataFrame({"px_2026_10_30": px_now, "ssf_tick_bps": tick_bps, "likit23": [s in LIQ for s in TG]}).sort_values("ssf_tick_bps", ascending=False).to_csv(vc.RES + "/v5_tick.csv")
SCEN = {"brüt": pd.Series(0.0, index=TG)}
for b in [8, 15, 30]: SCEN[f"{b}+tik"] = b + tick_bps
SCEN["kademeli 8/15+tik"] = pd.Series({s: (8 if s in LIQ else 15) for s in TG}) + tick_bps
SCEN["kademeli 8/30+tik"] = pd.Series({s: (8 if s in LIQ else 30) for s in TG}) + tick_bps

G = pd.DataFrame({s: D[s]["gap"] for s in TG}).reindex(idx); I = pd.DataFrame({s: D[s]["intra"] for s in TG}).reindex(idx)
gm = D["XU030"]["gap"].reindex(idx); im = D["XU030"]["intra"].reindex(idx)
ok = G.notna() & I.notna()
rows = []
def ev(spec, R, periods, extra=0.0, cols=TG):
    R = R[cols]
    for sc, cost in SCEN.items():
        c = (cost[cols] + (extra if sc != "brüt" else 0.0)) / 1e4
        N = R - c.values[None, :]
        N = N.where(R.notna())
        dw = N.mean(axis=1); tw = N.sum(axis=1, min_count=1); cnt = N.notna().sum(axis=1)
        for pn, m in periods.items():
            x = dw[m].dropna(); mm, t, n = vc.nw_mean(x.values, 5); xs = tw[m].dropna(); _, tt, _ = vc.nw_mean(xs.values, 5)
            rows.append(dict(spec=spec, scen=sc, period=pn, DW_bps=1e4 * mm, DWt=t, TW_bps=1e4 * xs.sum() / max(cnt[m].sum(), 1), TWt=tt, trades=int(cnt[m].sum()), days=n,
                             DW_sharpe=(x.mean() / x.std() * np.sqrt(252)) if len(x) > 30 else np.nan))
PD = {"IS14-20": idx < vc.SPLIT, "IS16-20": (idx >= "2016-01-01") & (idx < vc.SPLIT), "OOS21-26": idx >= vc.SPLIT, "2024+": idx >= "2024-01-01"}
pos = (-np.sign(G)).where((G.abs() > 0.01) & ok, 0.0)
ev("E0 |gap|>1% 47 (günlük)", (pos * I).where(pos != 0), PD)
ev("E0 |gap|>1% illikit24 (günlük)", (pos * I).where(pos != 0), PD, cols=[s for s in TG if s not in LIQ])
ev("E0 |gap|>1% likit23 (günlük)", (pos * I).where(pos != 0), PD, cols=LIQ)
pu = pos.where(G > 0, 0.0); ev("E0 yalnız gap-UP short 47 (günlük)", (pu * I).where(pu != 0), PD)
idio = G.sub(gm, axis=0); pi = (-np.sign(idio)).where((idio.abs() > 0.01) & ok & gm.notna().values[:, None] & im.notna().values[:, None], 0.0)
ev("idio>1% hedge'li E0 47 (günlük)", (pi * I.sub(im, axis=0)).where(pi != 0), PD, extra=3.0)
for s in ["CIMSA", "OYAKC"]:
    ev(f"{s} E0 |gap|>1% (günlük)", (pos * I).where(pos != 0), PD, cols=[s])
# yıllar (E0 47, brüt ve kademeli 8/30+tik, DW)
YR = {}
R = (pos * I).where(pos != 0)
for sc in ["brüt", "15+tik", "kademeli 8/30+tik"]:
    N = (R - SCEN[sc].values[None, :] / 1e4).where(R.notna())
    YR[f"E0_47_{sc}"] = 1e4 * N.mean(axis=1).groupby(idx.year).mean()
    Ri = (pi * I.sub(im, axis=0)).where(pi != 0); Ni = (Ri - (SCEN[sc].values[None, :] + (3 if sc != "brüt" else 0)) / 1e4).where(Ri.notna())
    YR[f"idio_hedge_{sc}"] = 1e4 * Ni.mean(axis=1).groupby(idx.year).mean()
# h1 dönemi
days = H["GARAN"].index; days = days[days.isin(idx)]; half = days[len(days) // 2]
PH = {"h1_tum": np.ones(len(days), bool), "1.yari": days < half, "2.yari": days >= half, "2025": days.year == 2025, "2026": days.year == 2026}
f = lambda k: pd.DataFrame({s: H[s][k] for s in TG}).reindex(days)
O = pd.DataFrame({s: D[s]["o"] for s in TG}).reindex(days); C = pd.DataFrame({s: D[s]["c"] for s in TG}).reindex(days)
cons = (np.abs(np.log(f("h1_o") / O)) < 0.02) & ~(np.abs(np.log(C / f("P1430"))) > 0.10) & ~(np.abs(np.log(f("P0730") / O)) > 0.15) & ~f("half").fillna(True).astype(bool)
Gd = G.reindex(days); okd = ok.reindex(days).fillna(False) & cons
posd = (-np.sign(Gd)).where((Gd.abs() > 0.01) & okd, 0.0)
idd = idio.reindex(days); pid = (-np.sign(idd)).where((idd.abs() > 0.01) & okd, 0.0)
cX = D["XU030"]["c"].reindex(days); oX = D["XU030"]["o"].reindex(days)
for en in ["O", "TP1", "P0730", "TP2"]:
    Pin = O if en == "O" else f(en); y = np.log(C / Pin)
    ev(f"h1 |gap|>1% 47 {en}->C", (posd * y).where((posd != 0) & y.notna()), PH)
    ev(f"h1 |gap|>1% illikit24 {en}->C", (posd * y).where((posd != 0) & y.notna()), PH, cols=[s for s in TG if s not in LIQ])
    xin = oX if en == "O" else H["XU030"][en].reindex(days); yx = np.log(cX / xin)
    ev(f"h1 idio>1% hedge'li 47 {en}->C", (pid * y.sub(yx, axis=0)).where((pid != 0) & y.notna()), PH, extra=3.0)
    for s in ["CIMSA", "OYAKC"]:
        ev(f"h1 {s} {en}->C", (posd * y).where((posd != 0) & y.notna()), PH, cols=[s])
RT = pd.DataFrame(rows); RT.to_csv(vc.RES + "/v5_costs.csv", index=False)
pd.DataFrame(YR).to_csv(vc.RES + "/v5_years.csv")
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 1000)
main = RT[RT.period.isin(["OOS21-26", "IS16-20", "2.yari", "h1_tum", "2024+"])]
pv = main.pivot_table(index=["spec", "period"], columns="scen", values="DW_bps", sort=False)[list(SCEN)]
print("=== NET DW bps ==="); print(pv.round(1).to_string())
pv2 = main.pivot_table(index=["spec", "period"], columns="scen", values="TW_bps", sort=False)[list(SCEN)]
print("=== NET TW bps ==="); print(pv2.round(1).to_string())
pvt = main.pivot_table(index=["spec", "period"], columns="scen", values="DWt", sort=False)[list(SCEN)]
print("=== NET DW t ==="); print(pvt.round(2).to_string())
print(pd.DataFrame(YR).round(1).to_string())
print("tik bps (en yüksek 10):", tick_bps.sort_values(ascending=False).head(10).round(1).to_dict())
