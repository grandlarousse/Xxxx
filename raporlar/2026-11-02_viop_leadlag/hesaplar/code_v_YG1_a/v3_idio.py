"""v3: Hisseye özgü gap fade (idio = gap_i − gap_XU030, β=1), XU030 vadelisiyle hedge vekili: PnL = intra_i − intra_XU030.
+ ham fade'in 'aynı yönde kaç hisse gap yaptı' kovalarına göre kırılımı (piyasa geneli vs tekil gap), gün- ve işlem-ağırlıklı.
+ h1 girişleri (P0730, TP1, TP2) ile idio fade. Çıktı: res/v3_idio.csv, res/v3_buckets.csv
"""
import numpy as np, pandas as pd, vc
TG = vc.VIOP
D = {s: vc.decomp(s) for s in TG + ["XU030"]}
idx = vc.cal(); idx = idx[idx >= "2014-01-01"]
G = pd.DataFrame({s: D[s]["gap"] for s in TG}).reindex(idx); I = pd.DataFrame({s: D[s]["intra"] for s in TG}).reindex(idx)
gm = D["XU030"]["gap"].reindex(idx); im = D["XU030"]["intra"].reindex(idx)
liq = pd.read_csv(vc.RES + "/v1_liq.csv", index_col=0); LIQ = list(liq.index[liq["rank"] <= 23]); ILL = list(liq.index[liq["rank"] > 23])
PER = {"IS14-20": idx < vc.SPLIT, "IS16-20": (idx >= "2016-01-01") & (idx < vc.SPLIT), "OOS21-26": idx >= vc.SPLIT, "2024+": idx >= "2024-01-01", "2025": idx.year == 2025, "2026-08..10": idx >= "2026-08-01"}
rows = []
def rec(spec, R, per=PER):
    pp = R.mean(axis=1); tot = R.sum(axis=1, min_count=1); cnt = R.notna().sum(axis=1); o = dict(spec=spec)
    for pn, m in per.items():
        x = pp[m].dropna(); mm, t, n = vc.nw_mean(x.values, 5); o[f"{pn}_DW"] = 1e4 * mm; o[f"{pn}_DWt"] = t
        xs = tot[m].dropna(); _, tt, _ = vc.nw_mean(xs.values, 5); o[f"{pn}_TW"] = 1e4 * xs.sum() / max(cnt[m].sum(), 1); o[f"{pn}_TWt"] = tt
        o[f"{pn}_n"] = int(cnt[m].sum())
    rows.append(o); return pp
idio = G.sub(gm, axis=0)
ok = G.notna() & I.notna() & gm.notna().values[:, None] & im.notna().values[:, None]
YR = {}
for thr in [0.01, 0.02]:
    pos = (-np.sign(idio)).where((idio.abs() > thr) & ok, 0.0)
    for uni, cols in [("47", TG), ("likit23", LIQ), ("illikit24", ILL)]:
        R_raw = (pos * I).where(pos != 0)[cols]
        R_hed = (pos * I.sub(im, axis=0)).where(pos != 0)[cols]
        rec(f"idio>{thr:.0%} {uni} ham E0->C", R_raw)
        pp = rec(f"idio>{thr:.0%} {uni} hedge'li E0->C", R_hed)
        if uni == "47": YR[f"idio>{thr:.0%} hedge DW"] = 1e4 * pp.groupby(pp.index.year).mean()
        if uni == "47":
            for side, msk in [("idio-UP short", idio > 0), ("idio-DOWN long", idio < 0)]:
                p2 = pos.where(msk, 0.0); rec(f"idio>{thr:.0%} 47 {side} hedge'li", (p2 * I.sub(im, axis=0)).where(p2 != 0))
            # hedge bacağının katkısı: −pos·intra_XU030
            rec(f"idio>{thr:.0%} 47 yalnız hedge bacağı (−pos·intra_XU030)", (-pos * pd.DataFrame(np.repeat(im.values[:, None], len(TG), 1), index=idx, columns=TG)).where(pos != 0))
# ---- kovalar: aynı gün aynı yönde |gap|>1% olan hisse sayısı
pos = (-np.sign(G)).where((G.abs() > 0.01) & ok, 0.0)
nup = (G > 0.01).sum(axis=1); ndn = (G < -0.01).sum(axis=1)
same = pd.DataFrame(np.where(G.values > 0, nup.values[:, None], ndn.values[:, None]), index=idx, columns=TG)
brows = []
for lo, hi in [(1, 2), (3, 5), (6, 15), (16, 99)]:
    for side, msk in [("UP-short", G > 0.01), ("DOWN-long", G < -0.01)]:
        m = msk & (same >= lo) & (same <= hi) & ok
        R = (pos * I).where(m)
        for pn in ["IS14-20", "OOS21-26"]:
            pm = PER[pn]; x = R[pm]; tot = x.sum(axis=1, min_count=1).dropna()
            _, tt, _ = vc.nw_mean(tot.values, 5)
            brows.append(dict(bucket=f"{lo}-{hi}", side=side, period=pn, n=int(x.notna().sum().sum()), days=len(tot), TW_bps=1e4 * np.nanmean(x.values), TWt=tt))
B = pd.DataFrame(brows); B.to_csv(vc.RES + "/v3_buckets.csv", index=False)
# ---- h1 girişli idio (hedge: XU030 aynı anlık fiyatlar)
H = {s: vc.h1_panel(s) for s in TG + ["XU030"]}
days = H["GARAN"].index; days = days[days.isin(idx)]; half = days[len(days) // 2]
PH = {"h1_tum": np.ones(len(days), bool), "1.yari": days < half, "2.yari": days >= half, "2024": days.year == 2024, "2025": days.year == 2025, "2026": days.year == 2026}
Gd = G.reindex(days); Id = I.reindex(days); idd = idio.reindex(days)
C = pd.DataFrame({s: D[s]["c"] for s in TG}).reindex(days); O = pd.DataFrame({s: D[s]["o"] for s in TG}).reindex(days)
cX = D["XU030"]["c"].reindex(days); oX = D["XU030"]["o"].reindex(days)
okd = ok.reindex(days).fillna(False)
h1o = pd.DataFrame({s: H[s]["h1_o"] for s in TG}).reindex(days)
cons = (np.abs(np.log(h1o / O)) < 0.02) & ~(np.abs(np.log(C / pd.DataFrame({s: H[s]["P1430"] for s in TG}).reindex(days))) > 0.10) & ~(np.abs(np.log(pd.DataFrame({s: H[s]["P0730"] for s in TG}).reindex(days) / O)) > 0.15)
okd = okd & cons & ~pd.DataFrame({s: H[s]["half"] for s in TG}).reindex(days).fillna(True).astype(bool)
for thr in [0.01]:
    pos = (-np.sign(idd)).where((idd.abs() > thr) & okd, 0.0)
    for en in ["O", "P0730", "TP1", "TP2"]:
        Pin = O if en == "O" else pd.DataFrame({s: H[s][en] for s in TG}).reindex(days)
        xin = oX if en == "O" else H["XU030"][en].reindex(days)
        ys = np.log(C / Pin); yx = np.log(cX / xin)
        R = (pos * ys.sub(yx, axis=0)).where((pos != 0) & ys.notna())
        rec(f"h1 idio>1% 47 hedge'li {en}->C", R, PH)
        Rr = (pos * ys).where((pos != 0) & ys.notna()); rec(f"h1 idio>1% 47 ham {en}->C", Rr, PH)
RT = pd.DataFrame(rows); RT.to_csv(vc.RES + "/v3_idio.csv", index=False)
pd.set_option("display.width", 300); pd.set_option("display.max_columns", 60)
c1 = [c for c in RT.columns if c == "spec" or any(c.startswith(p) for p in ["IS14-20", "IS16-20", "OOS21-26", "2024+", "2025_", "2026-08"])]
print(RT[RT.spec.str.startswith("idio")][c1].round(1).to_string())
c2 = [c for c in RT.columns if c == "spec" or any(c.startswith(p) for p in ["h1_tum", "1.yari", "2.yari", "2024_", "2025_", "2026_"])]
print(RT[RT.spec.str.startswith("h1")][c2].dropna(axis=1, how="all").round(1).to_string())
print(pd.DataFrame(YR).round(1).to_string())
print(B.pivot_table(index=["bucket", "side"], columns="period", values=["TW_bps", "TWt", "n"]).round(1).to_string())
