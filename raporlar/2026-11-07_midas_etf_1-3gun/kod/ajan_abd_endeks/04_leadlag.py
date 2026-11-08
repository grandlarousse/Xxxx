"""4) Lead-lag (aile hedefleri). Çalıştır: python3 -I kod/ajan_abd_endeks/04_leadlag.py
(a) leadlag_sweep.csv'den aile hedefleri: eşzamanlı sürücüler (corr_1y, beta_1y) ve gecikmeli öncü testleri (lag, kendi gecikmesi kontrollü).
(b) EK TEST: 'yetişme' (catch-up) katsayısını hedefin KENDİ getirisine karşı kontrol ederek yeniden tahmin:
    r_T(t+1..t+h) = a + b*r_T(t) + k*gap_t,  gap_t = beta60_t*r_L(t) - r_T(t)   (Newey-West t, IS/OOS), BH-FDR q=0.10.
(c) Yetişme sinyalini işlem kuralına çevirip maliyetli backtest (en güçlü çiftler; z(gap)>1 -> hedef long, h=1 ve 3).
Çıktılar: sonuclar/aile_abd_endeks/leadlag_aile_ozet.csv, leadlag_catch_kontrollu.csv, leadlag_catch_backtest.csv"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import ae, lib
from scipy import stats as st

OUT = ae.OUT
L = pd.read_csv(os.path.join(ae.ROOT, "sonuclar", "leadlag_sweep.csv"))
x = L[L.target.isin(ae.FAM)].copy()
tv = pd.read_csv(os.path.join(ae.ROOT, "sonuclar", "tv_etf.csv")).set_index("sym")["tv"].to_dict()
TVL = {"VIX_dlog": "CBOE:VIX", "VIXTS_d": "CBOE:VIX/CBOE:VIX3M (oran)", "VVIX_dlog": "CBOE:VVIX", "OVX_dlog": "CBOE:OVX",
       "GVZ_dlog": "CBOE:GVZ", "DGS10_d": "TVC:US10Y", "DGS2_d": "TVC:US02Y", "DGS30_d": "TVC:US30Y", "DFII10_d": "FRED:DFII10",
       "T10YIE_d": "FRED:T10YIE", "BTC_16ET": "COINBASE:BTCUSD", "ETH_16ET": "COINBASE:ETHUSD", "HYOAS_d": "FRED:BAMLH0A0HYM2"}
def tvcode(l): return TVL.get(l, tv.get(l, "?"))
x["leader_tv"] = x.leader.map(tvcode)

# (a) özet: her hedef için en yüksek |corr_1y| 6 sürücü ve en yüksek |lag_t| 5 öncü
rows = []
for T, d in x.groupby("target"):
    d = d[d.leader != T]
    drv = d.reindex(d.corr_1y.abs().sort_values(ascending=False).index).head(6)
    for _, r in drv.iterrows():
        rows.append({"target": T, "tip": "eszamanli_surucu", "leader": r.leader, "tv": r.leader_tv, "corr_1y": r.corr_1y,
                     "beta_1y": r.beta_1y, "corr_full": r.corr_full})
    for h in ("h1", "h3"):
        lg = d.reindex(d["lag_t_" + h].abs().sort_values(ascending=False).index).head(5)
        for _, r in lg.iterrows():
            rows.append({"target": T, "tip": "gecikmeli_" + h, "leader": r.leader, "tv": r.leader_tv, "t": r["lag_t_" + h],
                         "t_is": r["lag_t_" + h + "_is"], "t_oos": r["lag_t_" + h + "_oos"], "bp_per_sd": r["lag_bp_per_sd_" + h],
                         "fdr10": bool(r["fdr10_lag_t_" + h]),
                         "ayni_isaret": bool(np.sign(r["lag_t_" + h + "_is"]) == np.sign(r["lag_t_" + h + "_oos"]))})
oz = pd.DataFrame(rows); oz.to_csv(os.path.join(OUT, "leadlag_aile_ozet.csv"), index=False)
n_lag_fdr = int(x.fdr10_lag_t_h1.sum() + x.fdr10_lag_t_h3.sum())
n_lag_fdr_ok = int(((x.fdr10_lag_t_h1) & (np.sign(x.lag_t_h1_is) == np.sign(x.lag_t_h1_oos))).sum() +
                   ((x.fdr10_lag_t_h3) & (np.sign(x.lag_t_h3_is) == np.sign(x.lag_t_h3_oos))).sum())
print(f"(a) aile hedefi x öncü satırı: {len(x)}; lag FDR geçen (h1+h3): {n_lag_fdr}; IS/OOS aynı işaretli: {n_lag_fdr_ok}")
n_catch_fdr = int(x.fdr10_catch_t_h1.sum() + x.fdr10_catch_t_h3.sum())
print(f"    catch (kontrolsüz) FDR geçen: {n_catch_fdr}; hedef dağılımı:",
      x[x.fdr10_catch_t_h1 | x.fdr10_catch_t_h3].target.value_counts().to_dict())

# (b) kendi getirisi kontrollü yetişme
def nw_t(y, X, lags):
    n, k = X.shape
    xtx = np.linalg.inv(X.T @ X); b = xtx @ X.T @ y; e = y - X @ b
    u = X * e[:, None]; S = u.T @ u
    for l in range(1, lags + 1):
        w = 1 - l / (lags + 1); G = u[l:].T @ u[:-l]; S += w * (G + G.T)
    V = xtx @ S @ xtx
    return b, b / np.sqrt(np.diag(V))

def fwd(r, h): return r[::-1].rolling(h).sum()[::-1].shift(-1)

spy_idx = lib.load("SPY").index
def lr(s): return np.log(lib.load(s)["c"]).diff().reindex(spy_idx)
LEAD = {}
for s in ["SPY", "QQQ", "IWM", "DIA", "TLT", "IEF", "HYG", "LQD", "SMH", "XLK", "XLF", "KRE", "XBI", "UUP", "FXY", "GLD", "USO", "EEM", "EWJ"]:
    LEAD[s] = lr(s)
vix = lib.vol_index("VIX").reindex(spy_idx); v3 = lib.vol_index("VIX3M").reindex(spy_idx)
LEAD["VIX_dlog"] = np.log(vix).diff(); LEAD["VIXTS_d"] = (vix / v3).diff()
LEAD["VVIX_dlog"] = np.log(lib.vol_index("VVIX").reindex(spy_idx)).diff()
for f in ["DGS10", "DGS2", "T10YIE"]:
    s = lib.fred(f)
    if s is not None: LEAD[f + "_d"] = s.reindex(spy_idx).diff()
b = lib.btc_at_us_close("BTC-USD").reindex(spy_idx); LEAD["BTC_16ET"] = np.log(b).diff()
TARGETS = ["SPY", "QQQ", "IWM", "DIA", "RSP", "MDY", "IWF", "IWD", "SPHB", "SPLV", "SCHD", "MTUM"]
CR = []
for T in TARGETS:
    y0 = lr(T)
    for Ln, xl in LEAD.items():
        if Ln == T: continue
        df = pd.DataFrame({"y": y0, "x": xl}).dropna()
        if len(df) < 400: continue
        beta60 = df["y"].rolling(60).cov(df["x"]) / df["x"].rolling(60).var()
        gap = beta60 * df["x"] - df["y"]
        rec = {"target": T, "leader": Ln, "tv": tvcode(Ln), "n": len(df)}
        for h in (1, 3):
            fy = fwd(y0, h).reindex(df.index)
            d2 = pd.DataFrame({"fy": fy, "own": df["y"], "gap": gap, "x": df["x"]}).dropna()
            Xm = np.column_stack([np.ones(len(d2)), d2["own"].values, d2["gap"].values])
            bb, tt = nw_t(d2["fy"].values, Xm, max(1, h))
            Xo = np.column_stack([np.ones(len(d2)), d2["gap"].values])
            bo, to = nw_t(d2["fy"].values, Xo, max(1, h))
            Xs = np.column_stack([np.ones(len(d2)), d2["own"].values])
            bs, ts = nw_t(d2["fy"].values, Xs, max(1, h))
            rec[f"catch_t_kontrolsuz_h{h}"] = to[1]; rec[f"own_t_h{h}"] = ts[1]
            rec[f"catch_t_kontrollu_h{h}"] = tt[2]; rec[f"catch_bp_per_sd_kontrollu_h{h}"] = bb[2] * d2["gap"].std() * 1e4
            for nm, m in (("is", d2.index <= lib.IS_END), ("oos", d2.index > lib.IS_END)):
                dd = d2[m]
                if len(dd) < 150:
                    rec[f"catch_t_kontrollu_h{h}_{nm}"] = np.nan; continue
                b2, t2 = nw_t(dd["fy"].values, np.column_stack([np.ones(len(dd)), dd["own"].values, dd["gap"].values]), max(1, h))
                rec[f"catch_t_kontrollu_h{h}_{nm}"] = t2[2]
        CR.append(rec)
cr = pd.DataFrame(CR)
for h in (1, 3):
    p = 2 * st.norm.sf(cr[f"catch_t_kontrollu_h{h}"].abs())
    cr[f"fdr10_kontrollu_h{h}"] = lib.bh_fdr(p, 0.10)
cr.to_csv(os.path.join(OUT, "leadlag_catch_kontrollu.csv"), index=False)
pd.set_option("display.width", 260); pd.set_option("display.max_rows", 400)
print("(b) kontrollü yetişme testi sayısı:", 2 * len(cr), " FDR geçen h1:", int(cr.fdr10_kontrollu_h1.sum()), " h3:", int(cr.fdr10_kontrollu_h3.sum()))
top = cr.reindex(cr.catch_t_kontrollu_h1.abs().sort_values(ascending=False).index).head(15)
print(top[["target", "leader", "catch_t_kontrolsuz_h1", "own_t_h1", "catch_t_kontrollu_h1", "catch_t_kontrollu_h1_is", "catch_t_kontrollu_h1_oos",
           "catch_bp_per_sd_kontrollu_h1", "fdr10_kontrollu_h1"]].round(2).to_string(index=False))
top = cr.reindex(cr.catch_t_kontrollu_h3.abs().sort_values(ascending=False).index).head(15)
print(top[["target", "leader", "catch_t_kontrolsuz_h3", "own_t_h3", "catch_t_kontrollu_h3", "catch_t_kontrollu_h3_is", "catch_t_kontrollu_h3_oos",
           "catch_bp_per_sd_kontrollu_h3", "fdr10_kontrollu_h3"]].round(2).to_string(index=False))

# (c) yetişme kuralı backtest: z(gap) = gap / sd60(gap) ; z>1 -> T long (öncü T'den daha iyi yaptı); z<-1 -> kontrol
BT = []
pairs = [("IWM", "SPY"), ("IWM", "QQQ"), ("QQQ", "SMH"), ("SPY", "HYG"), ("QQQ", "XLK"), ("MDY", "SPY"), ("RSP", "SPY"), ("SPY", "QQQ"),
         ("IWM", "KRE"), ("SPHB", "SPY")]
for T, Ln in pairs:
    d = lib.load(T)
    y = np.log(d["c"]).diff(); xl = LEAD[Ln].reindex(d.index)
    beta60 = y.rolling(60).cov(xl) / xl.rolling(60).var()
    gap = beta60 * xl - y; z = gap / gap.rolling(60).std()
    for nm, sg in (("z>+1 (hedef geride) -> long", z > 1), ("z<-1 (hedef önde) -> long", z < -1)):
        for h in (1, 3):
            for m in ("C0", "O1"):
                s, tr = ae.full_eval(d, sg, h, m, label=f"catch {T}<-{Ln} {nm}", sym=T)
                BT.append(ae.row(s, {"target": T, "leader": Ln, "kural": nm}))
bt = pd.DataFrame(BT); bt.to_csv(os.path.join(OUT, "leadlag_catch_backtest.csv"), index=False)
print("(c) yetişme backtest test sayısı:", len(bt))
print(bt[["target", "leader", "kural", "mode", "h", "n", "mean_gross_bp", "mean_net_bp", "t", "is_net_bp", "oos_net_bp", "years_pos_frac"]].round(2).to_string(index=False))

# (d) Reel faiz (DFII10) değişimi -> endeks 3 gün (sweep'te FDR geçmedi ama IS/OOS aynı işaretli: SPY -2.5, QQQ -3.0).
# DFII10 (Hazine reel getiri eğrisi) 16:00 ET'de kesin bilinmez -> yalnız O1/C1 modları. z = dDFII10 / sd60.
dr = lib.fred("DFII10")
RR = []
for T in ["SPY", "QQQ", "IWM", "DIA"]:
    d = lib.load(T)
    x_ = dr.reindex(d.index).diff(); z = x_ / x_.rolling(60).std()
    for nm, sg in (("reel faiz dustu z<-1 -> long", z < -1), ("reel faiz yukseldi z>+1 -> long (beklenen<0)", z > 1)):
        for m in ("O1", "C1"):
            s, tr = ae.full_eval(d, sg, 3, m, label=nm, sym=T)
            RR.append(ae.row(s, {"target": T, "leader": "DFII10_d", "kural": nm}))
rr = pd.DataFrame(RR); rr.to_csv(os.path.join(OUT, "leadlag_reel_faiz_backtest.csv"), index=False)
print("(d) reel faiz backtest test sayısı:", len(rr))
print(rr[["target", "kural", "mode", "h", "n", "mean_gross_bp", "mean_net_bp", "t", "is_net_bp", "oos_net_bp", "years_pos_frac"]].round(2).to_string(index=False))

# (e) Faiz kanalı adayı TIP (16:00 ET kapanışı bilinir -> C0 de mümkün): z(r_TIP) = r/sd60 ; z>+1 -> hedef long (3 gün)
tip_r = lib.load("TIP")["c"].pct_change()
TP = []
for T in ["SPY", "QQQ", "IWM", "DIA"]:
    d = lib.load(T)
    z = (tip_r / tip_r.rolling(60).std()).reindex(d.index)
    for nm, sg in (("TIP z>+1 -> long", z > 1), ("TIP z<-1 -> long (beklenen<0)", z < -1)):
        for m in ("C0", "O1", "C1"):
            s, tr = ae.full_eval(d, sg, 3, m, label=nm, sym=T)
            TP.append(ae.row(s, {"target": T, "leader": "TIP", "kural": nm}))
tp = pd.DataFrame(TP); tp.to_csv(os.path.join(OUT, "leadlag_tip_backtest.csv"), index=False)
print("(e) TIP backtest test sayısı:", len(tp))
print(tp[["target", "kural", "mode", "h", "n", "mean_gross_bp", "mean_net_bp", "t", "is_net_bp", "oos_net_bp", "years_pos_frac"]].round(2).to_string(index=False))
# aile alt kümesinde (yalnız aile hedefleri) lag testleri için BH-FDR
for c in ["lag_t_h1", "lag_t_h3"]:
    p = 2 * st.norm.sf(x[c].abs())
    print(f"aile alt kümesi BH-FDR {c}: {int(lib.bh_fdr(p, 0.10).sum())} / {len(x)} geçti")
