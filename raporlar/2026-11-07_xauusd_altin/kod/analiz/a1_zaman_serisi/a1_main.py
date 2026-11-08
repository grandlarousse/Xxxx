#!/usr/bin/env python3
"""a1_zaman_serisi — VİOP F_XAUUSD: altının kendi fiyat dinamiği → fwd1/3/5 (uzlaşmadan uzlaşmaya).
Çalıştır: python3 -W ignore a1_main.py   (kayıt dosyası registry/a1_zaman_serisi.csv baştan yazılır)
Çıktılar: ic_results.csv, bt_results.csv, is_secim.csv, robust.csv, placebo.csv, tables_*.md
"""
import os, sys, json, warnings
warnings.filterwarnings("ignore")
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
sys.path.insert(0, f"{S}/code"); sys.path.insert(0, f"{S}/out/a1_zaman_serisi")
from lib_altin import *
from a1_feats import *

AG = "a1_zaman_serisi"; OUT = f"{S}/out/{AG}"; os.makedirs(OUT, exist_ok=True)
REGF = f"{REG_DIR}/{AG}.csv"
if os.path.exists(REGF): os.remove(REGF)
H = [1, 3, 5]
EARLY = (pd.Timestamp("2010-01-01"), pd.Timestamp("2016-12-31"))

d = load_viop(); s = load_spot()
Y = {h: d[f"fwd{h}"] for h in H}
SY = {h: s[f"sfwd{h}"] for h in H}

# ---------------- öznitelikler ----------------
Fs_cal = price_feats(s.s_p15)                       # spot takvimi 2010+ (15:00 UTC)
Fs_cal["rvq"] = expanding_pct(Fs_cal.rv20)          # rv20'nin genişleyen yüzdeliği (ileriye bakmasız)
loc_s, rng_s = spot_range_loc(s.index, s.s_p15, hourly("XAUUSD"))
Fs_cal["loc_s"] = loc_s
# gün içi segmentler (spot, hepsi <=15:00 UTC t)
Fs_cal["segA_15p_20p"] = np.log(s.xau_p20_prev / s.xau_p15_prev)   # t-1 ABD öğleden sonra
Fs_cal["segB_20p_07"] = np.log(s.xau_p07 / s.xau_p20_prev)          # Asya gecesi
Fs_cal["segC_07_13"] = np.log(s.xau_p13 / s.xau_p07)                # Avrupa sabahı
Fs_cal["segD_13_15"] = np.log(s.xau_p15 / s.xau_p13)                # ABD açılışı/veri saati
gvz_s = s.y__GVZ
Fs_cal["gvz"] = gvz_s; Fs_cal["dgvz"] = np.log(gvz_s).diff(); Fs_cal["dgvz5"] = np.log(gvz_s).diff(5)
Fs_cal["vrp"] = gvz_s - 100 * Fs_cal.rv20
for k in [1, 5, 20]:
    Fs_cal[f"ret{k}_hiV"] = Fs_cal[f"ret{k}"].where(Fs_cal.rvq > 2 / 3)
    Fs_cal[f"ret{k}_loV"] = Fs_cal[f"ret{k}"].where(Fs_cal.rvq < 1 / 3)
Fs = to_viop(Fs_cal, d.index)                       # VİOP günlerine as-of

Pv = np.exp(d.v_ret.cumsum())                       # VİOP roll-ayarlı uzlaşma endeksi (gün t 15:10 UTC)
Fv = price_feats(Pv)
Fv1 = Fv.shift(1)
# VİOP mikro yapı (gün t: seans sonu 15:15 UTC → cutoff SONRASI)
M = pd.DataFrame(index=d.index)
M["loc_v"] = ((d.v_settle - d.v_low) / (d.v_high - d.v_low)).where(d.v_high > d.v_low)
lv = np.log(d.v_tot_volume)
M["vshock"] = lv - lv.rolling(20).median().shift(1)
M["doi"] = np.log(d.v_tot_oi).diff()
M["pv_conf"] = np.sign(d.v_ret) * M.doi
M["vs_conf"] = np.sign(d.v_ret) * M.vshock
M["sc"] = np.log(d.v_settle / d.v_close)
M["svw"] = np.log(d.v_settle / d.v_vwap)
M1 = M.shift(1)

FAM_A = [f"ret{k}" for k in K] + [f"vsr{k}" for k in K]
FAM_B = ["pma20", "pma50", "pma100", "pma200", "x5_20", "x10_50", "x20_100", "x50_200", "dbrk20", "dbrk55", "dst20", "dst55", "d52"]
FAM_C = ["rsi2", "rsi14", "rsi2_lo", "rsi2_hi", "rsi14_lo", "rsi14_hi", "bbz", "bb_lo", "bb_hi", "streak", "up3", "dn3", "z1", "up2s", "dn2s"]
FAM_D = ["rv5", "rv20", "rv60", "dlrv"]
FAM_D2 = ["gvz", "dgvz", "dgvz5", "vrp"] + [f"ret{k}_{v}" for k in [1, 5, 20] for v in ["hiV", "loV"]]
FAM_G = ["segA_15p_20p", "segB_20p_07", "segC_07_13", "segD_13_15"]
EVENTS = {"rsi2_lo", "rsi2_hi", "rsi14_lo", "rsi14_hi", "bb_lo", "bb_hi", "up3", "dn3", "up2s", "dn2s", "dbrk20", "dbrk55"}
FAMOF = {**{f: "a_mom" for f in FAM_A}, **{f: "b_trend" for f in FAM_B}, **{f: "c_rev" for f in FAM_C}, **{f: "d_vol" for f in FAM_D + FAM_D2},
         **{f: "g_intraday" for f in FAM_G}, "loc_s": "e_micro", "loc_v": "e_micro", "vshock": "e_micro", "doi": "e_micro", "pv_conf": "e_micro",
         "vs_conf": "e_micro", "sc": "f_settle", "svw": "f_settle"}
INFO = {"spot": "gün t 15:00 UTC spot (temiz)", "vt": "gün t 15:10 UTC uzlaşma (KAPANIŞTA HESAPLANAN)", "vt1": "gün t-1 15:15 UTC (temiz)",
        "mt": "gün t seans sonu 15:15-15:20 UTC (CUTOFF SONRASI)", "mt1": "gün t-1 seans sonu (temiz)", "gvz": "t-1 ABD 16:15 ET (temiz)"}

ROWS = []; EROWS = []


def ev_stats(x, y, h):
    dd = pd.concat([x.rename("x"), y.rename("y")], axis=1).dropna()
    e = dd[dd.x == 1]
    if len(e) < 10: return dict(n_ev=len(e), m_ev=np.nan, m_all=np.nan, t_ev=np.nan, n_ev_oos=np.nan, m_ev_oos=np.nan)
    r = nw_ols(dd.y, dd.x, lags=max(h, 5))
    eo = e[e.index > IS_END]
    return dict(n_ev=len(e), m_ev=e.y.mean() * 1e4, m_all=dd.y.mean() * 1e4, t_ev=r["t"], n_ev_oos=len(eo), m_ev_oos=eo.y.mean() * 1e4 if len(eo) else np.nan)


def run_ic(x, feat, src, h, y=None, fam=None, note=""):
    fam = fam or FAMOF.get(feat, "x")
    y = Y[h] if y is None else y
    st = split_stats(x, y, h)
    row = dict(fam=fam, feat=feat, src=src, h=h, info=INFO.get(src, src), **{k: v for k, v in st.items() if k != "by_year"})
    row["by_year"] = json.dumps({int(k): v for k, v in st["by_year"].items()})
    if feat in EVENTS or x.dropna().isin([0, 1]).all(): row.update(ev_stats((x == 1).astype(float).where(x.notna()), y, h))
    register(AG, fam, f"{feat}|{src}|h{h}", feat, h, st, note or INFO.get(src, src))
    ROWS.append(row); return row


def run_early(x, feat, h, fam=None):
    fam = (fam or FAMOF.get(feat, "x")) + "_early"
    m = (x.index >= EARLY[0]) & (x.index <= EARLY[1])
    xx, yy = x[m], SY[h][m]
    r = ic(xx, yy, max(h, 5))
    dd = pd.concat([xx.rename("x"), yy.rename("y")], axis=1).dropna()
    yr = dd.groupby(dd.index.year).apply(lambda g: g.x.corr(g.y, method="spearman") if len(g) > 20 else np.nan)
    st = dict(ic=r["ic"], t=r["t"], n=r["n"], yrs_same_sign=int((np.sign(yr) == np.sign(r["ic"])).sum()), yrs=int(yr.notna().sum()))
    register(AG, fam, f"{feat}|spot_early|h{h}", feat, h, st, "spot panel 2010-2016, hedef sfwd (15:00->15:00 UTC)")
    EROWS.append(dict(feat=feat, h=h, ic_e=r["ic"], t_e=r["t"], n_e=r["n"], yrs_e=st["yrs_same_sign"], nyrs_e=st["yrs"])); return st


print("IC testleri...")
for h in H:
    for f in FAM_A + FAM_B + FAM_C + FAM_D:
        run_ic(Fs[f], f, "spot", h)
        run_ic(Fv[f], f, "vt", h)
        run_early(Fs_cal[f], f, h)
    for f in [f"ret{k}" for k in [1, 2, 3, 5]] + [f"vsr{k}" for k in [1, 2, 3, 5]] + FAM_C:
        run_ic(Fv1[f], f, "vt1", h)
    for f in FAM_D2:
        run_ic(Fs[f], f, "gvz" if "gvz" in f or f == "vrp" else "spot", h)
        run_early(Fs_cal[f], f, h)
    for f in FAM_G + ["loc_s"]:
        run_ic(Fs[f], f, "spot", h)
        run_early(Fs_cal[f], f, h)
    for f in ["loc_v", "vshock", "doi", "pv_conf", "vs_conf", "sc", "svw"]:
        run_ic(M[f], f, "mt", h)
        run_ic(M1[f], f, "mt1", h)

R = pd.DataFrame(ROWS); E = pd.DataFrame(EROWS).drop_duplicates(["feat", "h"])
R = R.merge(E, on=["feat", "h"], how="left")
R["p"] = 2 * (1 - __import__("scipy").stats.norm.cdf(R.t.abs()))
R["q_bh_own"] = bh_fdr(R.p.fillna(1).values)
R.to_csv(f"{OUT}/ic_results.csv", index=False)
print("IC testleri:", len(R), " erken spot:", len(E))

# ---------------- IS'te parametre seçimi (spot kaynak, temiz) ----------------
GROUPS = {"TSMOM ham getiri ret_k": [f"ret{k}" for k in K], "TSMOM oynaklık ölçekli vsr_k": [f"vsr{k}" for k in K],
          "MA / kesişim / Donchian / 52h": FAM_B, "Kısa vade dönüş (RSI/BB/seri/2σ)": FAM_C, "Oynaklık rejimi": FAM_D + FAM_D2,
          "Gün içi segmentler": FAM_G}
sel = []
for gname, feats in GROUPS.items():
    for h in H:
        sub = R[(R.src.isin(["spot", "gvz"])) & (R.feat.isin(feats)) & (R.h == h)].copy()
        if sub.empty: continue
        b = sub.loc[sub.t_is.abs().idxmax()]
        sel.append(dict(grup=gname, h=h, secilen=b.feat, ic_is=b.ic_is, t_is=b.t_is, ic_oos=b.ic_oos, t_oos=b.t_oos, ayni_isaret=np.sign(b.ic_is) == np.sign(b.ic_oos),
                        t_full=b.t, yrs=f"{b.yrs_same_sign}/{b.yrs}", ic_early=b.ic_e, t_early=b.t_e))
SEL = pd.DataFrame(sel); SEL.to_csv(f"{OUT}/is_secim.csv", index=False)

# ---------------- backtestler ----------------
print("backtest...")
r_v = d.v_ret


def strat_positions(F):
    P = F["_P"]; out = {}
    for k in K: out[f"TSMOM_{k}"] = np.sign(F[f"ret{k}"])
    for n in [20, 50, 100, 200]: out[f"PMA_{n}"] = F[f"pma{n}"]
    for a in ["x5_20", "x10_50", "x20_100", "x50_200"]: out[f"X_{a}"] = F[a]
    for N in [20, 55]: out[f"DON_{N}"] = F[f"dst{N}"]
    out["REV_1"] = -np.sign(F.ret1); out["REV_5"] = -np.sign(F.ret5)
    r2 = F.rsi2
    out["RSI2_CONNORS"] = pd.Series(np.where((r2 < 10) & (P > F._ma200), 1.0, np.where((r2 > 90) & (P < F._ma200), -1.0, 0.0)), index=F.index).where(F._ma200.notna())
    out["RSI2_X"] = pd.Series(np.where(r2 < 10, 1.0, np.where(r2 > 90, -1.0, 0.0)), index=F.index).where(r2.notna())
    out["BB_REV"] = pd.Series(np.where(F.bbz < -2, 1.0, np.where(F.bbz > 2, -1.0, 0.0)), index=F.index).where(F.bbz.notna())
    out["SIG2_REV"] = pd.Series(np.where(F.z1 > 2, -1.0, np.where(F.z1 < -2, 1.0, 0.0)), index=F.index).where(F.z1.notna())
    out["STREAK_REV"] = pd.Series(np.where(F.streak >= 3, -1.0, np.where(F.streak <= -3, 1.0, 0.0)), index=F.index).where(F.streak.notna())
    out["W52_NEARHIGH_LONG"] = (F.d52 >= np.log(0.98)).astype(float).where(F.d52.notna())
    vt = (0.10 / (F._sig20 * np.sqrt(252))).clip(upper=1)
    out["TSMOM_20_VT10"] = np.sign(F.ret20) * vt
    out["TSMOM_250_VT10"] = np.sign(F.ret250) * vt
    return out


def yr_consist(pnl):
    g = pnl.groupby(pnl.index.year).mean(); g = g[pnl.groupby(pnl.index.year).size() > 60]
    return int((g > 0).sum()), int(len(g))


POS_V = strat_positions(Fs)              # spot 15:00 UTC sinyali, VİOP uzlaşmasında işlem
POS_E = strat_positions(Fs_cal)          # erken spot kopyası
BT = []
for name, pos in POS_V.items():
    for h in H:
        b5 = bt_summary(pos, r_v, h, 5); b10 = bt_summary(pos, r_v, h, 10)
        bl = bt_summary(pos.clip(lower=0), r_v, h, 5); bs = bt_summary(pos.clip(upper=0), r_v, h, 5)
        full = backtest(pos, r_v, h, 5); fdm = backtest(pos, r_v, h, 5, demean=True)
        ism = r_v.index <= IS_END
        dis = backtest(pos[ism], r_v[ism], h, 5, demean=True); doo = backtest(pos[~ism], r_v[~ism], h, 5, demean=True)
        yc = yr_consist(fdm["pnl"])
        # erken spot (2010-2016) — spot 15:00->15:00 getirisi
        me = (s.index >= EARLY[0]) & (s.index <= EARLY[1])
        pe = POS_E[name][me]; re_ = s.s_ret[me]
        e5 = backtest(pe, re_, h, 5); edm = backtest(pe, re_, h, 5, demean=True)
        ebh = backtest(pd.Series(1.0, index=re_.index), re_, 1, 0)
        row = dict(strat=name, h=h,
                   sh_full=b5["full"]["sharpe"], shdm_full=b5["full"]["sharpe_demeaned"], sh_is=b5["is"]["sharpe"], shdm_is=b5["is"]["sharpe_demeaned"],
                   sh_oos=b5["oos"]["sharpe"], shdm_oos=b5["oos"]["sharpe_demeaned"], sh_oos_10=b10["oos"]["sharpe"], shdm_oos_10=b10["oos"]["sharpe_demeaned"],
                   ann_oos=b5["oos"]["ann"], hit_oos=b5["oos"]["hit"], expo=b5["full"]["exposure"], turn=b5["full"]["turnover"],
                   bh_full=b5["buyhold_sharpe_full"], long_sh_oos=bl["oos"]["sharpe"], long_shdm_oos=bl["oos"]["sharpe_demeaned"],
                   short_sh_oos=bs["oos"]["sharpe"], short_shdm_oos=bs["oos"]["sharpe_demeaned"], long_shdm_full=bl["full"]["sharpe_demeaned"], short_shdm_full=bs["full"]["sharpe_demeaned"],
                   t_dm_full=fdm["t_daily"], t_dm_is=dis["t_daily"], t_dm_oos=doo["t_daily"], yrs_pos_dm=f"{yc[0]}/{yc[1]}",
                   early_sh=e5 and round(e5["sharpe"], 2), early_shdm=edm and round(edm["sharpe"], 2), early_bh=round(ebh["sharpe"], 2), early_t_dm=edm and edm["t_daily"])
        BT.append(row)
        register(AG, "bt", f"{name}|spot->viop|h{h}", name, h, dict(ic=row["shdm_full"], t=fdm["t_daily"], n=fdm["n_days"], t_is=dis["t_daily"], t_oos=doo["t_daily"],
                 ic_oos=row["shdm_oos"], yrs_same_sign=yc[0], yrs=yc[1]), "backtest; ic=demeaned Sharpe full; t=demeaned günlük net PnL t (5bps)")
        register(AG, "bt_early", f"{name}|spot_early|h{h}", name, h, dict(ic=row["early_shdm"], t=row["early_t_dm"], n=edm and edm["n_days"]),
                 "backtest 2010-2016 spot; ic=demeaned Sharpe; t=demeaned günlük PnL t")
BTD = pd.DataFrame(BT); BTD.to_csv(f"{OUT}/bt_results.csv", index=False)
bh = {nm: backtest(pd.Series(1.0, index=r_v[m].index), r_v[m], 1, 0)["sharpe"] for nm, m in [("full", r_v.index > "1900"), ("is", r_v.index <= IS_END), ("oos", r_v.index > IS_END)]}
json.dump({k: round(v, 3) for k, v in bh.items()}, open(f"{OUT}/buyhold.json", "w"))
print("buy&hold Sharpe", bh)

# ---------------- placebo (ileriye bakma) ----------------
print("placebo...")
PL = []
for nm, x in [("ret1|spot", Fs.ret1), ("ret1|vt", Fv.ret1), ("ret1|vt1", Fv1.ret1), ("sc|mt", M.sc), ("sc|mt1", M1.sc), ("svw|mt", M.svw), ("svw|mt1", M1.svw),
              ("loc_v|mt", M.loc_v), ("loc_v|mt1", M1.loc_v), ("loc_s|spot", Fs.loc_s), ("segD_13_15|spot", Fs.segD_13_15), ("rsi2|spot", Fs.rsi2), ("rsi2|vt", Fv.rsi2),
              ("vshock|mt", M.vshock), ("doi|mt", M.doi)]:
    for h in [1, 5]:
        PL.append(dict(sig=nm, h=h, **{f"s{k}": v for k, v in placebo_lead(x, r_v, h).items()}))
pd.DataFrame(PL).to_csv(f"{OUT}/placebo.csv", index=False)
print("bitti. kayıt:", len(pd.read_csv(REGF)))
