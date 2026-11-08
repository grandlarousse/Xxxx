"""Adım 6: A8-5 — C1 a priori z-skoru birleşimi (+px_r20, +px_r250, −xa_dxy_d5, −rt_real10_d5, +sh_prem_d5, −cot_mm_z52).
(a) sabit kural, genişleyen z (min 250 satır, shift 1 → yalnız geçmiş), ±3 kırpma, mevcut bileşenlerin ortalaması; VİOP ve spot.
(b) walk-forward C1 (r04 çıktısı, eğitim penceresi z'si) zamanlama Sharpe'ı.
Yıl-içi demeaned Sharpe: getiriden her yılın kendi ortalaması çıkarılır (yalnız atıf tanısı)."""
import numpy as np, pandas as pd, json, sys, os
from rep_stats import split_ic, ic_test, bt_full, bt
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"; OUT = f"{S}/out/a8_ml_kombinasyon_rep"
XS = pd.read_parquet(f"{OUT}/feat_spot.parquet"); XV = pd.read_parquet(f"{OUT}/feat_viop.parquet")
sp = pd.read_parquet(f"{OUT}/base_spot.parquet"); v = pd.read_parquet(f"{OUT}/base_viop.parquet")
C1 = {"px_r20": 1, "px_r250": 1, "xa_dxy_d5": -1, "rt_real10_d5": -1, "sh_prem_d5": 1, "cot_mm_z52": -1}

def score(X, cols):
    zs = []
    for c in cols:
        x = X[c] * C1[c]; mu = x.expanding(250).mean().shift(1); sd = x.expanding(250).std().shift(1)
        zs.append(((x - mu) / sd).clip(-3, 3))
    return pd.concat(zs, axis=1).mean(axis=1)

def yrdm(r): return r - r.groupby(r.index.year).transform("mean")

def sh(pos, r, h, cost=5.0, dm=False, ydm=False):
    rr = r.dropna(); rr = yrdm(rr) if ydm else rr
    z = bt(pos.reindex(rr.index).fillna(0), rr, h, cost, demean=dm); return round(z["sharpe"], 3) if z else np.nan

out = {}
for nm, cols in {"C1": list(C1), "hizli4": [c for c in C1 if c not in ("px_r20", "px_r250")], "yavas2": ["px_r20", "px_r250"]}.items():
    z = score(XV, cols); pos = np.sign(z).fillna(0)
    R = {}
    for hh in (1, 3, 5):
        st = split_ic(z.loc["2017-03-01":], v[f"fwd{hh}"].loc["2017-03-01":], hh)
        R[f"h{hh}"] = dict(ic=round(st["ic"], 4), t=round(st["t"], 3), t_is=round(st["t_is"], 3), t_oos=round(st["t_oos"], 3), yrs=st["yrs"],
                           sh_2020p=sh(pos.loc["2020":], v.ret.loc["2020":], hh), sh_2020p_dm=sh(pos.loc["2020":], v.ret.loc["2020":], hh, dm=True),
                           sh_2020p_yrdm=sh(pos.loc["2020":], v.ret.loc["2020":], hh, ydm=True),
                           sh_oos=sh(pos.loc["2022":], v.ret.loc["2022":], hh), sh_oos_dm=sh(pos.loc["2022":], v.ret.loc["2022":], hh, dm=True),
                           sh_pre2020=sh(pos.loc[:"2019"], v.ret.loc["2017-03":"2019"], hh), bh_pre2020=sh(pd.Series(1.0, index=v.index).loc[:"2019"], v.ret.loc["2017-03":"2019"], 1, 0.0),
                           first_valid=str(z.first_valid_index().date()))
        if hh == 1: R["by_year_h1"] = st["by_year"]
    out[f"viop_{nm}"] = R
# spot 2011–2019
zs = score(XS, list(C1)); ps_ = np.sign(zs).fillna(0)
st = ic_test(zs.loc["2011":"2019"], sp.sfwd1.loc["2011":"2019"], 5)
out["spot_C1_2011_19"] = dict(ic=round(st["ic"], 4), t=round(st["t"], 3), sh=sh(ps_.loc["2011":"2019"], sp.s_ret.loc["2011":"2019"], 1),
                              sh_yrdm=sh(ps_.loc["2011":"2019"], sp.s_ret.loc["2011":"2019"], 1, ydm=True),
                              bh=sh(pd.Series(1.0, index=sp.index).loc["2011":"2019"], sp.s_ret.loc["2011":"2019"], 1, 0.0), first_valid=str(zs.first_valid_index().date()))
# walk-forward C1 (kendi r04 tahminlerim)
for V in ("V1", "V3"):
    f = f"{OUT}/mypreds_{V}.parquet"
    if not os.path.exists(f): continue
    P = pd.read_parquet(f); P["date"] = pd.to_datetime(P.date)
    W = {}
    for hh in (1, 3, 5):
        sc = P[(P.model == "c1_apriori_score") & (P.h == hh)].set_index("date").yhat
        pos = np.sign(sc.where(sc.abs() > 1e-9, 0.0))
        if V == "V1":
            r = v.ret
            a = bt_full(pos.loc["2022":], r.loc["2022":], hh)
            W[f"h{hh}"] = dict(sh_2020p=sh(pos, r.loc["2020":], hh), oos=a, sh_2020p_yrdm=sh(pos, r.loc["2020":], hh, ydm=True),
                               ic_oos=round(ic_test(sc.loc["2022":], v[f"fwd{hh}"], max(hh, 5))["t"], 3))
        else:
            r = sp.s_ret.loc["2013":"2016"]
            W[f"h{hh}"] = dict(sh_2013_16=sh(pos, r, hh), bh=sh(pd.Series(1.0, index=r.index), r, 1, 0.0))
    out[f"wf_{V}_C1"] = W
json.dump(out, open(f"{OUT}/c1_rep.json", "w"), indent=1, default=str)
for k, val in out.items():
    print("=====", k)
    if isinstance(val, dict):
        for kk, vv in val.items(): print("  ", kk, vv)
