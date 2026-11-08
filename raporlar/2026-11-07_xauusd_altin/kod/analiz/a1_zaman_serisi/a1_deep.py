#!/usr/bin/env python3
"""a1_zaman_serisi — ikinci aşama: (1) IS'te yönü belirlenen 'kuyruk momentumu' (2σ / Bollinger z>2 sonrası hareket yönünde),
(2) oynaklık rejimine koşullu momentum/dönüş, (3) aday sinyallerin sağlamlık kontrolleri (roll, uç dönemler, winsor, düşük hacim,
VİOP-t / t-1 / spot sürümleri, erken spot 2010-2016, katı maliyet), (4) gün içi segment hedef kıyası.
Önce a1_main.py çalışmış olmalı (kayıt dosyasına EKLER). Çalıştır: python3 -W ignore a1_deep.py
"""
import os, sys, json, warnings
warnings.filterwarnings("ignore")
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
sys.path.insert(0, f"{S}/code"); sys.path.insert(0, f"{S}/out/a1_zaman_serisi")
from lib_altin import *
from a1_feats import *

AG = "a1_zaman_serisi"; OUT = f"{S}/out/{AG}"
H = [1, 3, 5]
EARLY = (pd.Timestamp("2010-01-01"), pd.Timestamp("2016-12-31"))
d = load_viop(); s = load_spot(); r_v = d.v_ret
Y = {h: d[f"fwd{h}"] for h in H}

Fs_cal = price_feats(s.s_p15); Fs_cal["rvq"] = expanding_pct(Fs_cal.rv20)
Fs = to_viop(Fs_cal, d.index)
Fv = price_feats(np.exp(d.v_ret.cumsum())); Fv["rvq"] = expanding_pct(Fv.rv20, minp=250)
Fv1 = Fv.shift(1)

# ---- maskeler ----
roll = (d.v_code != d.v_code.shift(1))
roll_win = {h: (sum(roll.shift(-k).fillna(False).astype(int) for k in range(1, h + 1)) > 0) for h in H}
roll_near = roll.rolling(3, center=True, min_periods=1).max().astype(bool)          # roll günü ±1
def win(a, b): return (d.index >= a) & (d.index <= b)
EXT = win("2020-03-01", "2020-04-30") | win("2026-01-01", "2026-03-31")
lowliq = d.v_volume < d.v_volume.rolling(250, min_periods=60).quantile(0.10).shift(1)
pre_ev = d.index < "2020-09-18"


def tail_pos(F, thr=2.0, kind="z"):
    z = F.z1 if kind == "z" else F.bbz
    return pd.Series(np.where(z > thr, 1.0, np.where(z < -thr, -1.0, 0.0)), index=F.index).where(z.notna())


def volreg_pos(F, k, lo=1 / 3, hi=2 / 3):
    sg = np.sign(F[f"ret{k}"]); q = F.rvq
    return pd.Series(np.where(q < lo, sg, np.where(q > hi, -sg, 0.0)), index=F.index).where(q.notna() & sg.notna())


def strict_cost_bt(pos, r, h, cost_bps=5.0, demean=False):
    """Katı uygulama: her gün sermayenin 1/h'i ile pozisyon açılır ve h gün sonra KAPATILIR; aynı yönde yenileme netleştirilmez.
    Maliyet = her alt portföyde |pos| × cost (gidiş-dönüş) / h, günlük."""
    rr = r - r.mean() if demean else r
    p = pos.reindex(rr.index).fillna(0).clip(-1, 1)
    eff = sum(p.shift(k).fillna(0) for k in range(h)) / h
    gross = eff.shift(1) * rr
    cost = p.abs().shift(1).fillna(0) * cost_bps / 1e4 / h
    net = (gross - cost).dropna()
    return net.mean() * 252 / (net.std() * np.sqrt(252))


def full_bt(name, pos, h, ret=r_v, reg=True, fam="bt2", note=""):
    b5 = bt_summary(pos, ret, h, 5); b10 = bt_summary(pos, ret, h, 10)
    bl = bt_summary(pos.clip(lower=0), ret, h, 5); bs = bt_summary(pos.clip(upper=0), ret, h, 5)
    ism = ret.index <= IS_END
    fdm = backtest(pos, ret, h, 5, demean=True); dis = backtest(pos[ism], ret[ism], h, 5, demean=True); doo = backtest(pos[~ism], ret[~ism], h, 5, demean=True)
    g = fdm["pnl"].groupby(fdm["pnl"].index.year); ym = g.mean()[g.size() > 60]
    yr_sh = (g.mean() / g.std() * np.sqrt(252)).round(2).to_dict()
    oo = ret.index > IS_END
    row = dict(strat=name, h=h, sh_full=b5["full"]["sharpe"], shdm_full=b5["full"]["sharpe_demeaned"], sh_is=b5["is"]["sharpe"], shdm_is=b5["is"]["sharpe_demeaned"],
               sh_oos=b5["oos"]["sharpe"], shdm_oos=b5["oos"]["sharpe_demeaned"], sh_oos10=b10["oos"]["sharpe"], shdm_oos10=b10["oos"]["sharpe_demeaned"],
               ann_oos=b5["oos"]["ann"], hit_oos=b5["oos"]["hit"], expo=b5["full"]["exposure"], turn=b5["full"]["turnover"],
               long_shdm_is=bl["is"]["sharpe_demeaned"], long_shdm_oos=bl["oos"]["sharpe_demeaned"], short_shdm_is=bs["is"]["sharpe_demeaned"], short_shdm_oos=bs["oos"]["sharpe_demeaned"],
               long_sh_oos=bl["oos"]["sharpe"], short_sh_oos=bs["oos"]["sharpe"],
               strict5_oos=round(strict_cost_bt(pos[oo], ret[oo], h, 5), 2), strict5dm_oos=round(strict_cost_bt(pos[oo], ret[oo], h, 5, True), 2),
               t_dm_full=fdm["t_daily"], t_dm_is=dis["t_daily"], t_dm_oos=doo["t_daily"], yrs_pos=f"{int((ym > 0).sum())}/{len(ym)}", yr_sharpe_dm=json.dumps({int(k): v for k, v in yr_sh.items()}))
    if reg:
        register(AG, fam, f"{name}|h{h}", name, h, dict(ic=row["shdm_full"], t=row["t_dm_full"], n=fdm["n_days"], t_is=row["t_dm_is"], t_oos=row["t_dm_oos"],
                 ic_oos=row["shdm_oos"], yrs_same_sign=int((ym > 0).sum()), yrs=len(ym)), note or "backtest; ic=demeaned Sharpe; t=demeaned net günlük t (5bps)")
    return row


def early_bt(name, pos_cal, h, reg=True):
    m = (s.index >= EARLY[0]) & (s.index <= EARLY[1])
    p, r = pos_cal[m], s.s_ret[m]
    a = backtest(p, r, h, 5); b = backtest(p, r, h, 5, demean=True)
    bl = backtest(p.clip(lower=0), r, h, 5, demean=True); bs = backtest(p.clip(upper=0), r, h, 5, demean=True)
    g = b["pnl"].groupby(b["pnl"].index.year).mean()
    out = dict(strat=name, h=h, e_sh=round(a["sharpe"], 2), e_shdm=round(b["sharpe"], 2), e_t=round(b["t_daily"], 2), e_long_dm=round(bl["sharpe"], 2), e_short_dm=round(bs["sharpe"], 2),
               e_yrs=f"{int((g > 0).sum())}/{len(g)}")
    if reg:
        register(AG, "bt2_early", f"{name}|spot_early|h{h}", name, h, dict(ic=out["e_shdm"], t=b["t_daily"], n=b["n_days"], yrs_same_sign=int((g > 0).sum()), yrs=len(g)),
                 "backtest 2010-2016 spot; ic=demeaned Sharpe")
    return out


ROWS = []; EROWS = []
print("kuyruk momentumu...")
# (1) Kuyruk momentumu — yön a1_main IS sonuçlarından (REV stratejileri IS'te negatif → hareket yönünde). Eşik ön-tanımlı 2; 1.5/2.5 sağlamlık.
for kind, thrs in [("z", [1.5, 2.0, 2.5]), ("bb", [2.0])]:
    for thr in thrs:
        nm = f"TAILMOM_{kind}{thr}"
        for h in H:
            ROWS.append(full_bt(nm, tail_pos(Fs, thr, kind), h))
            EROWS.append(early_bt(nm, tail_pos(Fs_cal, thr, kind), h))
            # VİOP uzlaşma sürümleri (t: kapanışta hesaplanan, t-1: temiz)
            ROWS.append(full_bt(nm + "_vt", tail_pos(Fv, thr, kind), h))
            ROWS.append(full_bt(nm + "_vt1", tail_pos(Fv1, thr, kind), h))

print("oynaklık rejimi...")
# (2) Oynaklık rejimine koşullu: düşük oynaklıkta momentum, yüksekte dönüş. k IS'te seçilir.
for k in [1, 5, 20]:
    for h in H:
        ROWS.append(full_bt(f"VOLREG_{k}", volreg_pos(Fs, k), h))
        EROWS.append(early_bt(f"VOLREG_{k}", volreg_pos(Fs_cal, k), h))
        lo_only = volreg_pos(Fs, k).where(Fs.rvq < 1 / 3, 0); hi_only = volreg_pos(Fs, k).where(Fs.rvq > 2 / 3, 0)
        ROWS.append(full_bt(f"VOLREG_{k}_LOWVOL_MOM", lo_only, h))
        ROWS.append(full_bt(f"VOLREG_{k}_HIGHVOL_REV", hi_only, h))
        ROWS.append(full_bt(f"VOLREG_{k}_vt", volreg_pos(Fv, k), h))
BT2 = pd.DataFrame(ROWS); EB = pd.DataFrame(EROWS)
BT2 = BT2.merge(EB, on=["strat", "h"], how="left")
BT2.to_csv(f"{OUT}/bt2_results.csv", index=False)

# IS seçimi (yalnız IS demeaned Sharpe ile): kuyruk eşiği ve VOLREG k
sel = []
for fam, cands in [("TAILMOM", ["TAILMOM_z1.5", "TAILMOM_z2.0", "TAILMOM_z2.5", "TAILMOM_bb2.0"]), ("VOLREG", ["VOLREG_1", "VOLREG_5", "VOLREG_20"])]:
    for h in H:
        sub = BT2[BT2.strat.isin(cands) & (BT2.h == h)]
        b = sub.loc[sub.shdm_is.idxmax()]
        sel.append(dict(aile=fam, h=h, secilen=b.strat, shdm_is=b.shdm_is, shdm_oos=b.shdm_oos, sh_oos=b.sh_oos, shdm_oos10=b.shdm_oos10, t_dm_oos=b.t_dm_oos,
                        e_shdm=b.e_shdm, yrs_pos=b.yrs_pos))
pd.DataFrame(sel).to_csv(f"{OUT}/is_secim2.csv", index=False)

# ---- (3) Sağlamlık: IC düzeyinde ----
print("sağlamlık...")
def ic_variants(x, h, name):
    y = Y[h]; L = max(h, 5); out = dict(sig=name, h=h)
    def _ic(xx, yy):
        r = ic(xx, yy, L); return round(r["ic"], 4), round(r["t"], 2)
    out["base"] = _ic(x, y)
    out["excl_roll_win"] = _ic(x[~roll_win[h]], y[~roll_win[h]])
    out["excl_roll_near"] = _ic(x[~roll_near], y[~roll_near])
    out["excl_extreme"] = _ic(x[~EXT], y[~EXT])
    lo_, hi_ = y.quantile([0.01, 0.99]); out["winsor_y"] = _ic(x, y.clip(lo_, hi_))
    out["excl_lowliq"] = _ic(x[~lowliq], y[~lowliq])
    out["pre_evening"] = _ic(x[pre_ev], y[pre_ev]); out["post_evening"] = _ic(x[~pre_ev], y[~pre_ev])
    r = ic(x, y, L, method="pearson"); out["pearson"] = (round(r["ic"], 4), round(r["t"], 2))
    return out

def bt_variants(pos, h, name):
    out = dict(sig=name, h=h)
    def _sh(mask=None, ret=r_v):
        rr = ret.copy()
        if mask is not None: rr = rr.where(~mask)
        b = backtest(pos, rr, h, 5, demean=True); return round(b["sharpe"], 2), round(b["t_daily"], 2)
    out["base_dm"] = _sh()
    out["excl_extreme_dm"] = _sh(EXT)
    out["excl_roll_near_dm"] = _sh(roll_near)
    lo_, hi_ = r_v.quantile([0.01, 0.99]); out["winsor_dm"] = _sh(None, r_v.clip(lo_, hi_))
    out["excl_lowliq_dm"] = _sh(lowliq)
    out["pre_evening_dm"] = _sh(~pd.Series(pre_ev, index=d.index)); out["post_evening_dm"] = _sh(pd.Series(pre_ev, index=d.index))
    return out

RB = []; RBT = []
cands_ic = {"ret5_loV|spot": Fs.ret5.where(Fs.rvq < 1 / 3), "ret5_hiV|spot": Fs.ret5.where(Fs.rvq > 2 / 3), "ret1_loV|spot": Fs.ret1.where(Fs.rvq < 1 / 3),
            "z1|spot": Fs.z1, "segD_13_15|spot": to_viop(pd.DataFrame({"x": np.log(s.xau_p15 / s.xau_p13)}), d.index).x,
            "loc_s|spot": None, "pma50|vt": Fv.pma50, "sc|mt": np.log(d.v_settle / d.v_close), "rsi14_lo|vt1": Fv1.rsi14_lo}
loc_s, _ = spot_range_loc(s.index, s.s_p15, hourly("XAUUSD")); cands_ic["loc_s|spot"] = to_viop(pd.DataFrame({"x": loc_s}), d.index).x
for nm, x in cands_ic.items():
    for h in H: RB.append(ic_variants(x, h, nm))
for nm, p in {"TAILMOM_z2.0": tail_pos(Fs, 2.0), "TAILMOM_bb2.0": tail_pos(Fs, 2.0, "bb"), "VOLREG_5": volreg_pos(Fs, 5), "VOLREG_1": volreg_pos(Fs, 1),
              "PMA_50": Fs.pma50, "X_x20_100": Fs.x20_100, "W52_NEARHIGH_LONG": (Fs.d52 >= np.log(0.98)).astype(float).where(Fs.d52.notna())}.items():
    for h in H: RBT.append(bt_variants(p, h, nm))
pd.DataFrame(RB).to_csv(f"{OUT}/robust_ic.csv", index=False); pd.DataFrame(RBT).to_csv(f"{OUT}/robust_bt.csv", index=False)

# ---- (4) gün içi segment: spot hedefle 2017-2026 (dönem mi hedef mi?) ----
seg = np.log(s.xau_p15 / s.xau_p13); lsr = loc_s
SEG = []
for h in H:
    for nm, x in [("segD_13_15", seg), ("loc_s", lsr)]:
        for a, b in [("2010-01-01", "2016-12-31"), ("2017-03-01", "2021-12-31"), ("2022-01-01", "2026-12-31")]:
            m = (s.index >= a) & (s.index <= b); r = ic(x[m], s[f"sfwd{h}"][m], max(h, 5))
            SEG.append(dict(sig=nm, h=h, donem=f"{a[:4]}-{b[:4]}", hedef="spot 15:00->15:00", ic=round(r["ic"], 4), t=round(r["t"], 2)))
pd.DataFrame(SEG).to_csv(f"{OUT}/seg_spot_target.csv", index=False)
print("bitti. kayıt:", len(pd.read_csv(f"{REG_DIR}/{AG}.csv")))
