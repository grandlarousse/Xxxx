#!/usr/bin/env python3
"""Adım 4: VOLREG5, TAILMOM-BB, dönüş kuralları (REV-NEG), klasik trend (MA50 vb.) bağımsız yeniden hesap."""
import sys, json, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a1_zaman_serisi_rep")
from rutil import *
B, SP = load(); r_v = B.v_ret; P = SP.p15; lp = SP.lp; r = SP.r
q = exp_pct(r.rolling(20).std())
V = lambda x: asof_to(pd.DataFrame({"x": x}), B.index).x
def sgn_where(cond_pos, cond_neg, valid):
    return pd.Series(np.where(cond_pos, 1.0, np.where(cond_neg, -1.0, 0.0)), index=valid.index).where(valid.notna())
# öznitelikler (spot 15:00 UTC)
sma = lambda n: P.rolling(n).mean()
bbz = (P - sma(20)) / P.rolling(20).std()
sig20 = r.rolling(20, min_periods=15).std(); z1 = r / sig20.shift(1)
def rsi(n):
    d = P.diff(); up = d.clip(lower=0).ewm(alpha=1/n, adjust=False, min_periods=n).mean(); dn = (-d).clip(lower=0).ewm(alpha=1/n, adjust=False, min_periods=n).mean()
    return (100 - 100 / (1 + up / dn)).where(dn > 0, 100.0).where(up.notna())
rsi2 = rsi(2); ma200 = sma(200)
s_ = np.sign(r).fillna(0); grp = (s_ != s_.shift()).cumsum(); streak = s_.groupby(grp).cumsum().where(r.notna())
def mom(k): return lp - lp.shift(k)
def volreg(k=5, lo=1/3, hi=2/3, side="both"):
    sg = np.sign(mom(k)); p = pd.Series(np.where(q < lo, sg, np.where(q > hi, -sg, 0.0)), index=SP.index).where(q.notna() & sg.notna())
    if side == "lo": p = p.where(q < lo, 0.0)
    if side == "hi": p = p.where(q > hi, 0.0)
    return p
def donchian(N):
    hi_ = P.shift(1).rolling(N).max(); lo_ = P.shift(1).rolling(N).min()
    ev = pd.Series(np.where(P > hi_, 1.0, np.where(P < lo_, -1.0, 0.0)), index=P.index).where(hi_.notna())
    return ev.replace(0, np.nan).ffill()
POS = {
    "VOLREG_5": volreg(5), "VOLREG_3": volreg(3), "VOLREG_10": volreg(10), "VOLREG_5_lo": volreg(5, side="lo"), "VOLREG_5_hi": volreg(5, side="hi"),
    "TAILMOM_bb2": sgn_where(bbz > 2, bbz < -2, bbz),
    "BB_REV": sgn_where(bbz < -2, bbz > 2, bbz),
    "SIG2_REV": sgn_where(z1 < -2, z1 > 2, z1),
    "RSI2_X": sgn_where(rsi2 < 10, rsi2 > 90, rsi2),
    "RSI2_CONNORS": sgn_where((rsi2 < 10) & (P > ma200), (rsi2 > 90) & (P < ma200), ma200),
    "STREAK_REV": sgn_where(streak <= -3, streak >= 3, streak),
    "REV_1": -np.sign(r),
    "PMA_50": np.sign(P - sma(50)).where(sma(50).notna()),
    "X_20_100": np.sign(sma(20) - sma(100)).where(sma(100).notna()),
    "X_50_200": np.sign(sma(50) - sma(200)).where(sma(200).notna()),
    "DON_55": donchian(55),
    "TSMOM_250": np.sign(mom(250)),
}
def yr_consist(pnl):
    g = pnl.groupby(pnl.index.year); m = g.mean()[g.size() > 60]; return f"{int((m > 0).sum())}/{len(m)}"
R = []
early = (SP.index >= "2010-01-01") & (SP.index <= "2016-12-31")
for nm, pc in POS.items():
    pv = V(pc)
    for h in [1, 3, 5]:
        o = bt_split(pv, r_v, h); rw = row(nm, h, o); rw["yrs_mean_pos"] = yr_consist(o["full_dm"]["pnl"])
        e = bt(pc[early], r[early], h, 5.0, demean=True); rw["early_shdm"] = round(e["sharpe"], 2); rw["early_t"] = round(e["t"], 2)
        el = bt(pc[early].clip(lower=0), r[early], h, 5.0, demean=True); es = bt(pc[early].clip(upper=0), r[early], h, 5.0, demean=True)
        rw["early_long"] = round(el["sharpe"], 2); rw["early_short"] = round(es["sharpe"], 2)
        # IC (pozisyon sinyali ile ileri getiri)
        st = ic_split(pv, B[f"fwd{h}"], h); rw.update(ic=round(st["ic"], 3), ic_t=round(st["t"], 2), ic_t_is=round(st["t_is"], 2), ic_t_oos=round(st["t_oos"], 2), ic_yrs=st["yrs"])
        sf = sum(r.shift(-k) for k in range(1, h + 1)); ie = ic_nw(pc[early], sf[early], max(h, 5)); rw["early_ic_t"] = round(ie["t"], 2)
        R.append(rw)
T = pd.DataFrame(R); T.to_csv(f"{OUT}/rep_others_bt.csv", index=False)
pd.set_option("display.width", 260); pd.set_option("display.max_columns", 50)
cols = ["sig", "h", "sh_full", "shdm_full", "t_full", "tnw_full", "shdm_is", "t_is", "shdm_oos", "t_oos", "sh_oos_net", "long_oos", "short_oos", "expo", "trades_yr", "yrs", "yrs_mean_pos",
        "early_shdm", "early_t", "early_long", "early_short", "ic", "ic_t", "ic_t_is", "ic_t_oos", "early_ic_t"]
print(T[cols].to_string(index=False))
# bbz IC (sürekli) h1
st = ic_split(V(bbz), B.fwd1, 1); print("\nbbz sürekli IC h1:", {k: (round(v, 3) if isinstance(v, float) else v) for k, v in st.items() if k != "by_year"})
# VOLREG ve hi bacağı spot dönemleri (2017-03 başlangıçla da)
print("\nSpot hedefli dönem Sharpe (drift çıkarılmış):")
for nm in ["VOLREG_5", "VOLREG_5_lo", "VOLREG_5_hi"]:
    for h in [1, 3, 5]:
        out = []
        for a, b in [("2010-01-01", "2016-12-31"), ("2017-01-01", "2021-12-31"), ("2017-03-01", "2021-12-31"), ("2022-01-01", "2026-12-31")]:
            m = (SP.index >= a) & (SP.index <= b); o = bt(POS[nm][m], r[m], h, 5.0, demean=True); out.append(f"{a[:7]}..{b[:4]}: {o['sharpe']:.2f} (t {o['t']:.2f})")
        print(nm, h, " | ".join(out))
# VOLREG 2026 aktif bacak
p26 = V(POS["VOLREG_5"]); a26 = p26[p26.index.year == 2026]; qv = V(q)
print("\n2026 VOLREG aktif gün payı:", round(float((a26 != 0).mean()), 2), "| bunların hi bacağı payı:", round(float(((qv[qv.index.year == 2026] > 2/3) & (a26 != 0)).sum() / max((a26 != 0).sum(), 1)), 2))
# VİOP ham ve demeaned TSMOM_5 (koşulsuz) — LOWMOM koşulunun katkısı
for h in [1, 5]:
    rw = row("TSMOM_5_all", h, bt_split(V(np.sign(mom(5))), r_v, h)); print({k: rw[k] for k in ["sig", "h", "shdm_full", "t_full", "shdm_is", "shdm_oos", "early_shdm"] if k in rw},
                                                                         "early:", round(bt(np.sign(mom(5))[early], r[early], h, 5.0, demean=True)["sharpe"], 2))
