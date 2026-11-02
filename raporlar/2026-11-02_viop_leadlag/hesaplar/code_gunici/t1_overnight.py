"""GÖREV 1 + 3 (+ akşam seansı pencere ayrıştırması): gece bilgisinin BIST açılış gap'ine emilimi, ilk saat / gün sonu devam-dönüş,
gölge BIST (TUR/TKC kapanış sonrası), DAX/STOXX kalan kısmı. Çalıştır: python t1_overnight.py
Zamanlama: BIST günü t için gece penceresi = [15:00 UTC (t-1), 07:00 UTC (t)] (t-1 = önceki BIST işlem günü).
Sinyal yalnızca açılıştan önce bilinen bilgiden; işlem girişleri 07:30 UTC (h1 06:30 barı kapanışı) veya açılış fiyatı (iyimser).
Yarım gün (arife) ve yarım günü izleyen günler hariç.
"""
import numpy as np, pandas as pd
import g_common as g
from g_common import ll

D = g.bist_days()
D = D[~D["half"] & ~D["prev_half"]]
days = D.index
prev = pd.DatetimeIndex(D["prev"].values)
SPLIT = pd.Timestamp("2025-07-01")

# ---------- sürücü gece getirileri ----------
def night(sym, t0="15:00", t1="07:00", age0=1.5, age1=16.0, prevday=True):
    a = g.snap_at(sym, g.utc(prev if prevday else days, t0), max_age_h=age0).values
    b = g.snap_at(sym, g.utc(days, t1), max_age_h=age1).values
    return pd.Series(np.log(b / a), index=days)

X = pd.DataFrame(index=days)
for s in ["ES=F", "NQ=F", "BZ=F", "GC=F", "TRY=X", "EURTRY=X", "BTC-USD"]:
    X[s] = night(s, age1=3.0)
# ABD seansında işlem gören ETF'ler: 15:30 UTC (BIST kapanışından sonraki ilk h1 bar sonu) -> ABD kapanışı (07:00'deki son fiyat)
for s in ["TUR", "TKC", "EEM"]:
    X[s] = night(s, t0="15:30", age0=1.1, age1=72.0)
# Avrupa: 15:00 -> Avrupa kapanışı (yaz 15:30 / kış 16:30)
for s in ["^GDAXI", "^STOXX"]:
    X[s] = night(s, t0="15:00", age0=1.1, age1=72.0)
# temizlik: aşırı değerler (veri hatası) -> 8 sigma
for c in X:
    sd = X[c].std(); X.loc[X[c].abs() > 8 * sd, c] = np.nan
# BTC hafta sonu/boşluklarda 3 saatlik yaş kuralı sorun değil (7/24)
# ES alt pencereleri (akşam seansı analizi): w1 15:00-16:00 (seanslar arası), w2 16:00-20:00 (VİOP akşam seansı 19-23 TSİ), w3 20:00-07:00
W = pd.DataFrame(index=days)
for s in ["ES=F", "BZ=F", "GC=F", "TRY=X"]:
    p15 = g.snap_at(s, g.utc(prev, "15:00"), max_age_h=1.5).values
    p16 = g.snap_at(s, g.utc(prev, "16:00"), max_age_h=1.5).values
    p20 = g.snap_at(s, g.utc(prev, "20:00"), max_age_h=1.5).values
    p07 = g.snap_at(s, g.utc(days, "07:00"), max_age_h=3.0).values
    W[s + "_w1"] = np.log(p16 / p15); W[s + "_w2"] = np.log(p20 / p16); W[s + "_w3"] = np.log(p07 / p20)
# TUR: 15:30 -> 19:30(son bar başı ~ 20:00 kapanışa yakın) ve ES aynı pencere
X["ES_1530_usclose"] = np.log(g.snap_at("ES=F", g.utc(prev, "20:00"), max_age_h=1.5).values / g.snap_at("ES=F", g.utc(prev, "15:30"), max_age_h=1.5).values)
X.to_parquet(g.RES + "/t1_X_night.parquet"); W.to_parquet(g.RES + "/t1_W_windows.parquet")

DRV = ["ES=F", "NQ=F", "BZ=F", "GC=F", "TRY=X", "EURTRY=X", "TUR", "TKC", "EEM", "^GDAXI", "^STOXX", "BTC-USD"]
JOINT = ["ES=F", "BZ=F", "GC=F", "TRY=X", "TUR", "^GDAXI"]   # BTC kısa örneklem nedeniyle ayrı
SYMS = g.IDX + g.VIOP

def expanding_fit(y, Xm, minn=120):
    """Her t için t-1'e kadarki veriyle OLS -> tahmin (look-ahead yok)."""
    df = pd.concat([y.rename("y"), Xm], axis=1).dropna()
    yv = df["y"].values; Xv = np.column_stack([np.ones(len(df)), df.drop(columns="y").values])
    pred = np.full(len(df), np.nan)
    for i in range(minn, len(df)):
        b = np.linalg.lstsq(Xv[:i], yv[:i], rcond=None)[0]; pred[i] = Xv[i] @ b
    return pd.Series(pred, index=df.index)

rows_abs, rows_joint, rows_cont, rows_bt, rows_win, rows_drift = [], [], [], [], [], []
BI = {}
for s in SYMS:
    try: B = g.bist_intraday(s, days)
    except Exception as e: print("skip", s, e); continue
    BI[s] = B
    # (a) emilim: tek tek sürücüler
    for d in DRV:
        c, t, n = g.corr_t(B["gap"], X[d])
        r = g.ols(B["gap"], X[d].rename("x"))
        ci, ti, _ = g.corr_t(B["intra"], X[d]); c1, t1, _ = g.corr_t(B["r1"], X[d]); cr, tr, _ = g.corr_t(B["rest"], X[d])
        sub = pd.concat([B["gap"], X[d]], axis=1).dropna()
        c_is = sub[sub.index < SPLIT].corr().iloc[0, 1] if (sub.index < SPLIT).sum() > 40 else np.nan
        c_oos = sub[sub.index >= SPLIT].corr().iloc[0, 1] if (sub.index >= SPLIT).sum() > 40 else np.nan
        last1y = sub[sub.index >= sub.index.max() - pd.DateOffset(years=1)].corr().iloc[0, 1]
        rows_abs.append(dict(stock=s, driver=d, corr_gap=c, t_gap=t, beta_gap=r["b"][0] if r else np.nan, r2=c ** 2, n=n,
                             corr_gap_IS=c_is, corr_gap_OOS=c_oos, corr_gap_1y=last1y,
                             corr_intra=ci, t_intra=ti, corr_r1=c1, t_r1=t1, corr_rest=cr, t_rest=tr))
    # (b) ortak model
    r = g.ols(B["gap"], X[JOINT])
    rb = g.ols(B["gap"], X[JOINT + ["BTC-USD"]])
    if r is None: print("joint none", s); continue
    rows_joint.append(dict(stock=s, r2_joint=r["r2"], n=r["n"], **{f"b_{k}": v for k, v in zip(r["names"], r["b"])},
                           **{f"t_{k}": v for k, v in zip(r["names"], r["t"])}, r2_joint_btc=rb["r2"] if rb else np.nan, n_btc=rb["n"] if rb else 0,
                           t_btc_in_joint=rb["t"][-1] if rb else np.nan))
    # (c) devam/dönüş
    ghat = expanding_fit(B["gap"], X[JOINT]); e = B["gap"] - ghat
    out = dict(stock=s)
    for tgt in ["r30", "r1", "rest", "intra", "r_0730_close"]:
        for nm, sig in [("gap", B["gap"]), ("ghat", ghat), ("resid", e)]:
            c, t, n = g.corr_t(B[tgt], sig); out[f"c_{tgt}_{nm}"] = c; out[f"t_{tgt}_{nm}"] = t
    out["n"] = int(pd.concat([B["intra"], e], axis=1).dropna().shape[0])
    out["mean_gap_bps"] = 1e4 * B["gap"].mean(); out["mean_intra_bps"] = 1e4 * B["intra"].mean(); out["mean_r1_bps"] = 1e4 * B["r1"].mean(); out["mean_rest_bps"] = 1e4 * B["rest"].mean()
    rows_cont.append(out)
    # (d) backtestler
    for nm, sig, tgt, lab in [("resid_rev_0730", -e, B["r_0730_close"], "pos=-sign(gap-ghat); giriş 07:30, çıkış kapanış"),
                              ("resid_rev_open", -e, B["intra"], "pos=-sign(gap-ghat); giriş açılış (iyimser)"),
                              ("ghat_cont_0730", ghat, B["r_0730_close"], "pos=sign(ghat); giriş 07:30"),
                              ("gap_rev_0730", -B["gap"], B["r_0730_close"], "pos=-sign(gap); giriş 07:30"),
                              ("es_night_cont_0730", X["ES=F"], B["r_0730_close"], "pos=sign(ES gece); giriş 07:30"),
                              ("short_open_cover_close", pd.Series(-1.0, index=B.index).where(B["intra"].notna()), B["intra"], "her gün açılışta sat, kapanışta kapat")]:
        dfb = pd.concat([sig.rename("s"), tgt.rename("y")], axis=1).dropna()
        if len(dfb) < 60: continue
        sd = dfb["s"].expanding(60).std().shift(1)
        for thr in [0.0, 0.5]:
            pos = np.sign(dfb["s"]).where(dfb["s"].abs() > thr * sd.fillna(np.inf), 0.0) if thr > 0 else np.sign(dfb["s"])
            for cost in [0.0, 8.0, 15.0]:
                pnl = pos * dfb["y"] - cost / 1e4 * pos.abs()
                for per, msk in [("ALL", slice(None)), ("IS", dfb.index < SPLIT), ("OOS", dfb.index >= SPLIT)]:
                    st = g.bt_stats(pnl[msk], pos[msk])
                    rows_bt.append(dict(stock=s, strat=nm, desc=lab, thr_sd=thr, cost_bps=cost, period=per, **st))
    # (e) akşam seansı pencereleri (ES alt pencereleri)
    rw = g.ols(B["gap"], W[["ES=F_w1", "ES=F_w2", "ES=F_w3"]])
    r0 = g.ols(B["gap"], W[["ES=F_w3"]]); r12 = g.ols(B["gap"], W[["ES=F_w1", "ES=F_w2"]])
    if rw:
        rows_win.append(dict(stock=s, n=rw["n"], b_w1=rw["b"][0], t_w1=rw["t"][0], b_w2=rw["b"][1], t_w2=rw["t"][1], b_w3=rw["b"][2], t_w3=rw["t"][2],
                             r2_all=rw["r2"], r2_w12_only=r12["r2"], r2_w3_only=r0["r2"],
                             sd_w1_bps=1e4 * W["ES=F_w1"].std(), sd_w2_bps=1e4 * W["ES=F_w2"].std(), sd_w3_bps=1e4 * W["ES=F_w3"].std()))
    # TUR'un ES'e ek katkısı ve DAX kalan
    pc_tur, _ = ll.partial_corr(B["gap"], X["TUR"], [X["ES=F"]])
    pc_tkc, _ = ll.partial_corr(B["gap"], X["TKC"], [X["ES=F"], X["TUR"]])
    pc_dax, _ = ll.partial_corr(B["gap"], X["^GDAXI"], [X["ES=F"]])
    rows_win[-1].update(dict(pc_TUR_given_ES=pc_tur, pc_TKC_given_ES_TUR=pc_tkc, pc_DAXrem_given_ES=pc_dax))

pd.DataFrame(rows_abs).to_csv(g.RES + "/t1_absorb.csv", index=False)
pd.DataFrame(rows_joint).to_csv(g.RES + "/t1_joint.csv", index=False)
pd.DataFrame(rows_cont).to_csv(g.RES + "/t1_cont.csv", index=False)
pd.DataFrame(rows_bt).to_csv(g.RES + "/t1_bt.csv", index=False)
pd.DataFrame(rows_win).to_csv(g.RES + "/t1_windows.csv", index=False)
pd.to_pickle(BI, g.RES + "/t1_BI.pkl")
print("done", len(rows_abs), len(rows_bt))
