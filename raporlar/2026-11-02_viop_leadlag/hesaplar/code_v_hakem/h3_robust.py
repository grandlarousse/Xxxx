"""H3: sağlamlık — kendi gecikmesi/piyasa gecikmesi/aynı gün gap kontrolü, doğrusal olmama, likidite, saatlik ayrıştırma (2023-12+),
backtest (hisse ve portföy; 8/15 bps, 2 bacak 16/30), yurt içi (DOM) aile. Çıktı res/h3_*.csv + res/h3_summary.txt"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import vh
from peers import PEERS, SECTOR, FAMOUS, DOM

t0 = time.time()
L = lambda k: pd.read_parquet(vh.RES + f"/{k}.parquet").loc[vh.START:vh.END]
Y_h, Y_raw, G_h, CC_res = L("Y_h"), L("Y_raw"), L("G_h"), L("CC_res")
XU = L("XU"); VOL = L("VOL")
STOCKS = list(PEERS.keys()); idx = Y_h.index
Zres = L("X_res").apply(vh.zscore); Zown = L("OWN_l1").apply(vh.zscore); Zdom = L("X_dom").apply(vh.zscore)
Zgap = G_h.apply(vh.zscore)
xul = pd.DataFrame({s: XU["xu_cc"].shift(1) for s in STOCKS}).apply(vh.zscore)
PERS = ["ALL", "IS", "OOS"]
txt = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); txt.append(s)
def pooled(Y, Zl, per="ALL", cols=None):
    m = vh.period_mask(idx, per); cols = cols or STOCKS
    return vh.pooled_dk(Y.loc[m, cols], [z.loc[m, cols] for z in Zl])

# ---------- A) kontroller ----------
P("== A) Kontrollü havuzlanmış regresyon (hedef: hedge'li gün-içi; katsayılar bps/1σ, DK t) ==")
rows = []
for nm, Zl in [("z_res", [Zres]), ("z_res + kendi artık(t-1) + XU100(t-1)", [Zres, Zown, xul]),
               ("z_res + aynı gün hedge'li gap (açılışta bilinir)", [Zres, Zgap]),
               ("z_res + kendi(t-1) + XU100(t-1) + gap_t", [Zres, Zown, xul, Zgap])]:
    for per in PERS:
        r = pooled(Y_h, Zl, per)
        rows.append({"model": nm, "per": per, **{f"b{i}": 1e4 * r["b"][i] for i in range(len(Zl))}, **{f"t{i}": r["t_dk"][i] for i in range(len(Zl))}})
A = pd.DataFrame(rows); A.to_csv(vh.RES + "/h3_controls.csv", index=False); P(A.round(2).to_string(index=False))

# ---------- B) doğrusal olmama ----------
P("\n== B) z kovalarına göre ortalama hedge'li gün-içi (bps; tüm hisse-günler) ==")
bins = [-9, -2, -1, -0.5, 0.5, 1, 2, 9]
st = []
for per in PERS:
    m = vh.period_mask(idx, per)
    zz = Zres.loc[m, STOCKS].values.ravel(); yy = Y_h.loc[m, STOCKS].values.ravel()
    ok = ~np.isnan(zz) & ~np.isnan(yy); zz, yy = zz[ok], yy[ok]
    cat = pd.cut(zz, bins)
    g = pd.DataFrame({"c": cat, "y": yy}).groupby("c", observed=True)["y"].agg(["mean", "count", "std"])
    g["bps"] = 1e4 * g["mean"]; g["t_iid"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    g["per"] = per; st.append(g.reset_index())
B = pd.concat(st); B.to_csv(vh.RES + "/h3_buckets.csv", index=False); P(B[["per", "c", "count", "bps", "t_iid"]].round(2).to_string(index=False))

# ---------- C) likidite ----------
P("\n== C) Likidite terciline göre (spot TL hacim medyanı 2021+) ==")
med = VOL.loc["2021-01-01":, STOCKS].median().sort_values()
terc = np.array_split(med.index.tolist(), 3)
rows = []
for i, cols in enumerate(terc):
    for per in PERS:
        r = pooled(Y_h, [Zres], per, list(cols))
        rows.append({"tercil": ["düşük", "orta", "yüksek"][i], "hisseler": ",".join(cols), "per": per, "b": 1e4 * r["b"][0], "t": r["t_dk"][0]})
C = pd.DataFrame(rows); C.to_csv(vh.RES + "/h3_liquidity.csv", index=False); P(C[["tercil", "per", "b", "t"]].round(2).to_string(index=False))
for i, cols in enumerate(terc): P(f"  {['düşük','orta','yüksek'][i]}: {', '.join(cols)}")

# ---------- D) saatlik ayrıştırma (2023-12+) ----------
P("\n== D) Saatlik: açılış->07:30 UTC (ilk 30 dk sürekli işlem) ve 07:30->kapanış; ayrıca 08:30 sonrası ==")
H1 = vh.SCR + "/data/h1/"
def h1_close_at(sym, hhmm):
    d = pd.read_parquet(H1 + sym + ".parquet"); d = d[d.index.strftime("%H:%M") == hhmm]
    s = pd.Series(d["c"].values, index=pd.DatetimeIndex(pd.to_datetime(d["ldate"]).dt.normalize())); return s[~s.index.duplicated(keep="last")]
seg = {}
xr = vh.raw("XU100.IS")
xo = xr["o"].reindex(idx); xc = xr["c"].reindex(idx)
x0730 = h1_close_at("XU100.IS", "06:30").reindex(idx); x0830 = h1_close_at("XU100.IS", "07:30").reindex(idx)
S1, S2, S3 = {}, {}, {}
for s in STOCKS:
    if not os.path.exists(H1 + s + ".IS.parquet"): continue
    d = vh.raw(s + ".IS"); o = d["o"].reindex(idx); c = d["c"].reindex(idx)
    c1 = h1_close_at(s + ".IS", "06:30").reindex(idx); c2 = h1_close_at(s + ".IS", "07:30").reindex(idx)
    ok = Y_raw[s].notna()
    S1[s] = (np.log(c1 / o) - np.log(x0730 / xo)).where(ok)
    S2[s] = (np.log(c / c1) - np.log(xc / x0730)).where(ok)
    S3[s] = (np.log(c / c2) - np.log(xc / x0830)).where(ok)
S1, S2, S3 = pd.DataFrame(S1), pd.DataFrame(S2), pd.DataFrame(S3)
hcols = [s for s in S1.columns if S1[s].loc["2023-12-01":].notna().sum() > 300]
mm = idx >= pd.Timestamp("2023-12-01")
rows = []
for nm, Y in [("açılış->07:30 (ilk 30 dk)", S1), ("07:30->kapanış", S2), ("08:30->kapanış", S3), ("tüm gün-içi (günlük, aynı dönem)", Y_raw.sub(XU["xu_intra"], axis=0))]:
    r = vh.pooled_dk(Y.loc[mm, hcols], [Zres.loc[mm, hcols]])
    rows.append({"segment": nm, "b_bps": 1e4 * r["b"][0], "t_dk": r["t_dk"][0], "nobs": r["nobs"]})
Dh = pd.DataFrame(rows); Dh.to_csv(vh.RES + "/h3_hourly_segments.csv", index=False); P(Dh.round(2).to_string(index=False)); P(f"  hisse sayısı {len(hcols)}; hedef = hisse − XU100 (β=1) segment getirisi")

# ---------- E) backtest ----------
P("\n== E) Backtest (ön-kayıt: pozisyon = sign(z) ; mod 'her gün' ve '|z|>1'; hedef hedge'li gün-içi (XU030 vadelisi ile hedge varsayımı) ve ham) ==")
def bt_panel(Y, Zx, thr, cost_bps, cols=None):
    cols = cols or STOCKS
    Zv = Zx[cols]; Yv = Y[cols]
    pos = np.sign(Zv).where(Zv.abs() > thr, 0.0).where(Yv.notna() & Zv.notna(), 0.0)
    pnl = pos * Yv.fillna(0) - (cost_bps / 1e4) * pos.abs()
    nact = pos.abs().sum(axis=1)
    port = (pnl.sum(axis=1) / nact).where(nact > 0)
    return pos, pnl, port, nact
rows = []; yrs = []
for tgt_nm, Y, legs in [("hedge'li", Y_h, 2), ("ham", Y_raw, 1)]:
    for thr in [0.0, 1.0]:
        for cst in [0, 8, 15]:
            ccost = cst * legs if cst > 0 else 0
            pos, pnl, port, nact = bt_panel(Y, Zres, thr, ccost)
            for per in PERS:
                m = vh.period_mask(idx, per)
                pp = port[m]; act = pp.notna()
                se, n = vh.nw_se_mean(pp[act].values)
                full = pp.fillna(0.0)
                # pozisyon başına ortalama (tüm hisse-gün)
                pa = pnl[m].values[pos[m].values != 0]
                rows.append({"hedef": tgt_nm, "thr": thr, "maliyet_toplam_bps": ccost, "per": per, "gün": int(act.sum()), "poz_gun": int((pos[m] != 0).values.sum()),
                             "poz_basi_bps": 1e4 * pa.mean(), "portfoy_gunluk_bps": 1e4 * pp[act].mean(), "t_NW": pp[act].mean() / se,
                             "sharpe": full.mean() * 252 / (full.std() * np.sqrt(252)), "isabet": float((pp[act] > 0).mean()),
                             "ort_aktif_hisse": float(nact[m][act].mean())})
            if cst == 8:
                yy = (1e4 * port.groupby(port.index.year).mean()).round(1).to_dict(); yrs.append({"hedef": tgt_nm, "thr": thr, "maliyet": ccost, **yy})
E = pd.DataFrame(rows); E.to_csv(vh.RES + "/h3_backtest_portfolio.csv", index=False)
P(E.round(2).to_string(index=False))
EY = pd.DataFrame(yrs); EY.to_csv(vh.RES + "/h3_backtest_years.csv", index=False); P("\nYıllara göre portföy günlük ort. (bps, maliyet 8/bacak):"); P(EY.to_string(index=False))
# hisse bazında
rows = []
for s in STOCKS:
    for thr in [0.0, 1.0]:
        for cst, legs in [(8, 2), (15, 2), (8, 1), (15, 1)]:
            Y = Y_h if legs == 2 else Y_raw
            z = Zres[s]; y = Y[s]
            pos = np.sign(z).where(z.abs() > thr, 0.0).where(y.notna() & z.notna(), 0.0)
            gross = pos * y; pnl = gross - cst * legs / 1e4 * pos.abs()
            r = {"stock": s, "thr": thr, "cost": cst * legs, "hedef": "hedge'li" if legs == 2 else "ham"}
            for per in PERS:
                m = vh.period_mask(idx, per); act = (pos[m] != 0)
                st_ = vh.bt_stats(pnl[m], act); r[f"n_{per}"] = st_.get("n"); r[f"bps_{per}"] = st_.get("mean_bps"); r[f"t_{per}"] = st_.get("t"); r[f"sh_{per}"] = st_.get("sharpe")
                r[f"gross_{per}"] = 1e4 * gross[m][act].mean() if act.sum() else np.nan
            rows.append(r)
ES = pd.DataFrame(rows); ES.to_csv(vh.RES + "/h3_backtest_stock.csv", index=False)
for thr in [0.0, 1.0]:
    for cst, hed in [(16, "hedge'li"), (30, "hedge'li"), (8, "ham"), (15, "ham")]:
        q = ES[(ES.thr == thr) & (ES.cost == cst) & (ES.hedef == hed)]
        P(f" hisse bazında thr={thr} maliyet={cst} {hed}: OOS net>0 {int((q.bps_OOS>0).sum())}/47, OOS Sharpe medyan {q.sh_OOS.median():.2f}, OOS t>2 {int((q.t_OOS>2).sum())}, IS net>0 {int((q.bps_IS>0).sum())}/47, brüt OOS medyan {q.gross_OOS.median():.1f} bps")

# ---------- F) yurt içi aile ----------
P("\n== F) YURT İÇİ (DOM) emsal artığı t-1 -> hedge'li gün-içi t ==")
dcols = [s for s in STOCKS if Zdom[s].notna().sum() > 500]
rows = []
for nm, Zl in [("z_dom", [Zdom]), ("z_dom + kendi(t-1) + XU100(t-1)", [Zdom, Zown, xul]), ("z_dom + z_res(dış)", [Zdom, Zres]),
               ("z_dom + z_res + kendi + XU100", [Zdom, Zres, Zown, xul])]:
    for per in PERS:
        r = pooled(Y_h, Zl, per, dcols)
        rows.append({"model": nm, "per": per, **{f"b{i}": 1e4 * r["b"][i] for i in range(len(Zl))}, **{f"t{i}": r["t_dk"][i] for i in range(len(Zl))}})
F = pd.DataFrame(rows); F.to_csv(vh.RES + "/h3_dom.csv", index=False); P(F.round(2).to_string(index=False)); P(f"  hisse sayısı {len(dcols)}")
# DOM -> gap (açılışta mı fiyatlanıyor?)
for per in PERS:
    r = pooled(G_h, [Zdom], per, dcols); P(f"  z_dom -> hedge'li gap {per}: b {1e4*r['b'][0]:.2f} bps t {r['t_dk'][0]:.2f}")
rows = []
for s in dcols:
    rr = {"stock": s, "dom": ",".join(DOM.get(s, []))}
    for per in PERS:
        m = vh.period_mask(idx, per)
        b, t, n, c = vh.ols_nw(Y_h[s].values[m].astype(float), Zdom[s].values[m].astype(float)); rr[f"b_{per}"] = 1e4 * b; rr[f"t_{per}"] = t
    rows.append(rr)
FD = pd.DataFrame(rows); FD["q_ALL"] = vh.bh(vh.p2(FD.t_ALL.values)); FD.to_csv(vh.RES + "/h3_dom_stock.csv", index=False)
P(f"  hisse bazında DOM: b>0 {int((FD.b_ALL>0).sum())}/{len(FD)}, t>2 {int((FD.t_ALL>2).sum())}, t<-2 {int((FD.t_ALL<-2).sum())}, BH q<0,05 {int((FD.q_ALL<0.05).sum())}")
P(FD.sort_values("t_ALL")[["stock", "dom", "b_ALL", "t_ALL", "q_ALL", "t_IS", "t_OOS"]].round(2).to_string(index=False))

open(vh.RES + "/h3_summary.txt", "w").write("\n".join(txt)); print(f"bitti {time.time()-t0:.1f}s")
