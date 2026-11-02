"""H6: İşlenebilirlik — GERÇEK VİOP pay vadelisi fiyatlarıyla (BIST günlük bülteni, 2017-03+).
Ön ay = o gün en yüksek TL hacimli SSF kontratı. f_intra = ln(kapanış/açılış) (VİOP açılışı 09:30 TSİ ilk işlem; kapanış son işlem).
Hedge: XU030 endeks vadelisi ön ayı gün-içi, geçmiş 250g beta. Filtre: işlem sayısı >= 20 (bayat ilk/son işlem fiyatını azaltmak için).
Ayrıca uzlaşma fiyatı (settle, son 10 dk AOF) ile ln(settle/open)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import vh
from peers import PEERS
txt = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); txt.append(s)
v = pd.read_parquet(vh.SCR + "/data/viop_panel.parquet")
v = v[(v.segment.isin(["SSF", "INF"])) & v.open.gt(0) & v.close.gt(0)]
v = v.sort_values("value_tl").groupby(["date", "root"]).tail(1)
STOCKS = list(PEERS.keys())
cal = vh.bist_cal()
def piv(col): return v.pivot_table(index="date", columns="root", values=col, aggfunc="last").reindex(cal)
O, C, ST, TR, VAL = piv("open"), piv("close"), piv("settle"), piv("trades"), piv("value_tl")
fi = np.log(C / O); fs = np.log(ST / O)
for A in (fi, fs):
    A[(A > vh.LUP) | (A < vh.LDN)] = np.nan
ok = TR >= 20
fi = fi.where(ok); fs = fs.where(ok)
xf = fi["XU030"]; xfs = fs["XU030"]
L = lambda k: pd.read_parquet(vh.RES + f"/{k}.parquet").loc[vh.START:vh.END]
Zres = L("X_res").apply(vh.zscore); Y_h = L("Y_h"); Y_raw = L("Y_raw")
cols = [s for s in STOCKS if s in fi.columns and fi[s].notna().sum() > 300]
def hed(A, x):
    return pd.DataFrame({s: A[s] - vh.roll_beta(A[s], x) * x for s in cols})
FH = hed(fi, xf).loc[vh.START:vh.END]; FSH = hed(fs, xfs).loc[vh.START:vh.END]; FR = fi[cols].loc[vh.START:vh.END]
idx = FH.index
P(f"VİOP hisse sayısı {len(cols)}; gözlem (işlem>=20) {int(FR.notna().sum().sum())}; dönem {FR.first_valid_index().date()}–{FR.last_valid_index().date()}")
rows = []
for nm, Y in [("VİOP ön ay gün-içi ham", FR), ("VİOP gün-içi − β·XU030 vadeli", FH), ("VİOP uzlaşma/açılış − β·XU030", FSH)]:
    for per in ["ALL", "IS", "OOS"]:
        m = vh.period_mask(idx, per)
        if m.sum() < 100: continue
        r = vh.pooled_dk(Y.loc[m, cols], [Zres.loc[m, cols]])
        rows.append({"hedef": nm, "per": per, "b_bps": 1e4 * r["b"][0], "t_dk": r["t_dk"][0], "nobs": r["nobs"]})
# aynı günlerde spot karşılaştırma
msk = FH.notna()
for per in ["ALL", "IS", "OOS"]:
    m = vh.period_mask(idx, per)
    r = vh.pooled_dk(Y_h.loc[idx[m], cols].where(msk.loc[idx[m], cols]), [Zres.loc[idx[m], cols]])
    rows.append({"hedef": "SPOT hedge'li, aynı günler", "per": per, "b_bps": 1e4 * r["b"][0], "t_dk": r["t_dk"][0], "nobs": r["nobs"]})
R = pd.DataFrame(rows); R.to_csv(vh.RES + "/h6_viop_reg.csv", index=False)
P("== Havuzlanmış eğim (bps / 1σ sinyal) — IS burada 2017-03..2020 =="); P(R.round(2).to_string(index=False))
# backtest (VİOP)
P("\n== VİOP backtest: pozisyon sign(z), |z|>thr; maliyet hisse bacağı c, hedge bacağı XU030 vadelisi h ==")
rows = []
for tgt, Y, hleg in [("ham", FR, 0), ("hedge'li", FH, 1)]:
    for thr in [0.0, 1.0, 2.0]:
        for c, h in [(0, 0), (8, 0), (8, 3), (15, 3), (15, 15)]:
            if tgt == "ham" and h > 0: continue
            Zv = Zres.reindex(idx)[cols]
            pos = np.sign(Zv).where(Zv.abs() > thr, 0.0).where(Y.notna() & Zv.notna(), 0.0)
            pnl = pos * Y.fillna(0) - (c + h * hleg) / 1e4 * pos.abs()
            nact = pos.abs().sum(axis=1); port = (pnl.sum(axis=1) / nact).where(nact > 0)
            for per in ["ALL", "IS", "OOS"]:
                m = vh.period_mask(idx, per); pp = port[m]; act = pp.notna()
                if act.sum() < 30: continue
                se, n = vh.nw_se_mean(pp[act].values); full = pp.fillna(0)
                pa = pnl[m].values[pos[m].values != 0]
                rows.append({"hedef": tgt, "thr": thr, "c_hisse": c, "c_hedge": h * hleg, "per": per, "gün": int(act.sum()), "poz": int((pos[m] != 0).values.sum()),
                             "poz_basi_bps": 1e4 * pa.mean(), "port_bps": 1e4 * pp[act].mean(), "t": pp[act].mean() / se, "sharpe": full.mean() * 252 / (full.std() * np.sqrt(252))})
B = pd.DataFrame(rows); B.to_csv(vh.RES + "/h6_viop_bt.csv", index=False); P(B.round(2).to_string(index=False))
# likidite: hisse bazında VİOP medyan TL hacim (2021+) ve hisse bazında eğim
rows = []
for s in cols:
    b, t, n, c_ = vh.ols_nw(FH[s].values.astype(float), Zres.reindex(idx)[s].values.astype(float))
    rows.append({"stock": s, "viop_medyan_TL_mn": VAL[s].loc["2021":].median() / 1e6, "b_viop_h": 1e4 * b, "t": t, "n": n})
S = pd.DataFrame(rows).sort_values("viop_medyan_TL_mn"); S.to_csv(vh.RES + "/h6_viop_stock.csv", index=False)
P("\nVİOP hisse bazında (hedge'li gün-içi; medyan günlük ön-ay hacmi 2021+):"); P(S.round(2).to_string(index=False))
q = S.viop_medyan_TL_mn.quantile([1/3, 2/3]).values
for nm, sel in [("düşük", S.viop_medyan_TL_mn <= q[0]), ("orta", (S.viop_medyan_TL_mn > q[0]) & (S.viop_medyan_TL_mn <= q[1])), ("yüksek", S.viop_medyan_TL_mn > q[1])]:
    cc = S[sel].stock.tolist(); r = vh.pooled_dk(FH[cc], [Zres.reindex(idx)[cc]])
    P(f"  VİOP likidite {nm} ({len(cc)}): b {1e4*r['b'][0]:.2f} bps t {r['t_dk'][0]:.2f}")
open(vh.RES + "/h6_summary.txt", "w").write("\n".join(txt))
