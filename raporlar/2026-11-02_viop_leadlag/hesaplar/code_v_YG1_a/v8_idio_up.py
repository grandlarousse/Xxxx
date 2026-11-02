"""v8: En tutarlı bileşen — hisseye özgü YUKARI gap (idio = gap − XU030 gap > +%1) -> hisse short + XU030 long (hedge), çıkış kapanış.
Günlük E0 (2014–26) ve h1 dönemi gerçekçi girişler (TP1, P0730, TP2), likit/illikit, maliyet (8/15/30 + tik + 3 bps hedge). DW ve TW."""
import numpy as np, pandas as pd, vc
TG = vc.VIOP
D = {s: vc.decomp(s) for s in TG + ["XU030"]}; H = {s: vc.h1_panel(s) for s in TG + ["XU030"]}
idx = vc.cal(); idx = idx[idx >= "2014-01-01"]
liq = pd.read_csv(vc.RES + "/v1_liq.csv", index_col=0); LIQ = list(liq.index[liq["rank"] <= 23]); ILL = [s for s in TG if s not in LIQ]
tick = pd.read_csv(vc.RES + "/v5_tick.csv", index_col=0)["ssf_tick_bps"].reindex(TG)
G = pd.DataFrame({s: D[s]["gap"] for s in TG}).reindex(idx); I = pd.DataFrame({s: D[s]["intra"] for s in TG}).reindex(idx)
gm = D["XU030"]["gap"].reindex(idx); im = D["XU030"]["intra"].reindex(idx)
idio = G.sub(gm, axis=0)
def show(lab, R, per):
    out = [lab]
    for cst in [0, 8, 15, 30]:
        c = (cst + tick + 3) if cst else 0 * tick
        N = (R - c.values[None, :] / 1e4).where(R.notna())
        for pn, m in per.items():
            dw = N.mean(axis=1)[m].dropna(); tw = N.sum(axis=1, min_count=1)[m].dropna(); n = int(N[m].notna().sum().sum())
            _, t1, _ = vc.nw_mean(dw.values, 5); _, t2, _ = vc.nw_mean(tw.values, 5)
            if cst in (0, 15): out.append(f"{pn}[c{cst}] DW {1e4*dw.mean():.1f}(t{t1:.1f}) TW {1e4*tw.sum()/max(n,1):.1f}(t{t2:.1f}) n{n}")
    print(" | ".join(out))
PD = {"IS14-20": idx < vc.SPLIT, "OOS21-26": idx >= vc.SPLIT, "2025": idx.year == 2025, "2026-08..10": idx >= "2026-08-01"}
ok = G.notna() & I.notna() & gm.notna().values[:, None] & im.notna().values[:, None]
for thr in [0.01, 0.02]:
    pos = pd.DataFrame(-1.0, index=idx, columns=TG).where((idio > thr) & ok, 0.0)
    for uni, cols in [("47", TG), ("likit23", LIQ), ("illikit24", ILL)]:
        R = (pos * I.sub(im, axis=0)).where(pos != 0)[cols].reindex(columns=TG)
        show(f"idio-UP>{thr:.0%} {uni} E0 hedge'li", R, PD)
days = H["GARAN"].index; days = days[days.isin(idx)]; half = days[len(days) // 2]
PH = {"h1_tum": np.ones(len(days), bool), "2.yari": days >= half, "2025": days.year == 2025, "2026": days.year == 2026}
f = lambda k: pd.DataFrame({s: H[s][k] for s in TG}).reindex(days)
O = pd.DataFrame({s: D[s]["o"] for s in TG}).reindex(days); C = pd.DataFrame({s: D[s]["c"] for s in TG}).reindex(days)
cons = (np.abs(np.log(f("h1_o") / O)) < 0.02) & ~(np.abs(np.log(C / f("P1430"))) > 0.10) & ~(np.abs(np.log(f("P0730") / O)) > 0.15) & ~f("half").fillna(True).astype(bool)
okd = ok.reindex(days).fillna(False) & cons; idd = idio.reindex(days)
cX = D["XU030"]["c"].reindex(days); oX = D["XU030"]["o"].reindex(days)
pos = pd.DataFrame(-1.0, index=days, columns=TG).where((idd > 0.01) & okd, 0.0)
for en in ["O", "TP1", "P0730", "TP2"]:
    Pin = O if en == "O" else f(en); xin = oX if en == "O" else H["XU030"][en].reindex(days)
    y = np.log(C / Pin).sub(np.log(cX / xin), axis=0)
    for uni, cols in [("47", TG), ("illikit24", ILL), ("likit23", LIQ)]:
        R = (pos * y).where((pos != 0) & y.notna())[cols].reindex(columns=TG)
        show(f"h1 idio-UP>1% {uni} {en}->C hedge'li", R, PH)
