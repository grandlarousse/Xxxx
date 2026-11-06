"""1) Dalga tanimi (ex-post etiket): Ken French 49 sektor, aylik VW getiri.
RS_i = kumulatif (1+r_i)/(1+r_m). log RS uzerinde zigzag (geri donus esigi thr).
Dalga = yukari bacak; bacak icinde <=12 ay icinde RS >= +G (G=40%/50%) yapan bir alt pencere var.
Dalga baslangici = bacak dibi, tepe = bacak tepesi. Sonuclar (cikti) sadece etiketleme icin; kurallar bunu kullanmaz.
"""
import numpy as np
import pandas as pd
from ff_load import load_monthly49, load_ff_monthly

OUT = "/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/data/dalga_abd/out"
import os
os.makedirs(OUT, exist_ok=True)


def base_data(start="1927-01"):
    m = load_monthly49()
    ff = load_ff_monthly()
    R = m["vw"] / 100.0
    RM = (ff["Mkt-RF"] + ff["RF"]) / 100.0
    RF = ff["RF"] / 100.0
    R = R.loc[start:]
    RM = RM.loc[start:]
    RF = RF.loc[start:]
    return R, RM, RF, m


def zigzag_up_legs(x, thr):
    """x: numpy log seri. thr: log esik. Doner: [(lo_i, hi_i, ongoing)] yukari bacaklar."""
    n = len(x)
    legs = []
    lo_i = hi_i = 0
    mode = 0
    for t in range(1, n):
        if mode == 0:
            if x[t] > x[hi_i]:
                hi_i = t
            if x[t] < x[lo_i]:
                lo_i = t
            if x[hi_i] - x[lo_i] >= thr:
                mode = 1 if hi_i > lo_i else -1
                if mode == -1:
                    lo_i = t if x[t] <= x[lo_i] else lo_i
        elif mode == 1:
            if x[t] > x[hi_i]:
                hi_i = t
            elif x[hi_i] - x[t] >= thr:
                legs.append((lo_i, hi_i, False))
                mode = -1
                lo_i = t
        else:
            if x[t] < x[lo_i]:
                lo_i = t
            elif x[t] - x[lo_i] >= thr:
                mode = 1
                hi_i = t
    if mode == 1:
        legs.append((lo_i, hi_i, True))
    return legs


def max_window_gain(x, a, b, w=12):
    best = -np.inf
    for i in range(a, b):
        j_hi = min(b, i + w)
        if j_hi > i:
            g = np.max(x[i + 1:j_hi + 1]) - x[i]
            if g > best:
                best = g
    return best


def find_waves(R, RM, gain=0.40, thr=np.log(1 / 0.8), win=12):
    rows = []
    for ind in R.columns:
        r = R[ind].dropna()
        if len(r) < 36:
            continue
        rm = RM.loc[r.index]
        x = np.cumsum(np.log1p(r.values) - np.log1p(rm.values))
        x = np.concatenate([[0.0], x])  # x[k] = ay k sonu (k=0: baslangic oncesi)
        idx = [r.index[0] - 1] + list(r.index)
        p = np.concatenate([[0.0], np.cumsum(np.log1p(r.values))])
        pm = np.concatenate([[0.0], np.cumsum(np.log1p(rm.values))])
        for lo, hi, ong in zigzag_up_legs(x, thr):
            g = max_window_gain(x, lo, hi, win)
            if g >= np.log(1 + gain):
                post = {}
                for h in (12, 24):
                    if hi + h < len(x):
                        post[f"rs_post{h}"] = np.exp(x[hi + h] - x[hi]) - 1
                        post[f"abs_post{h}"] = np.exp(p[hi + h] - p[hi]) - 1
                    else:
                        post[f"rs_post{h}"] = np.nan
                        post[f"abs_post{h}"] = np.nan
                # dalga kazancinin ne kadari 24 ayda geri verildi (log olcek)
                if hi + 24 < len(x):
                    mn = np.min(x[hi:hi + 25])
                    giveback = (x[hi] - mn) / (x[hi] - x[lo])
                else:
                    giveback = np.nan
                rows.append(dict(ind=ind, start=idx[lo], peak=idx[hi], lo_i=lo, hi_i=hi, ongoing=ong,
                                 months=hi - lo, rs_gain=np.exp(x[hi] - x[lo]) - 1,
                                 abs_gain=np.exp(p[hi] - p[lo]) - 1,
                                 mkt_gain=np.exp(pm[hi] - pm[lo]) - 1,
                                 max12=np.exp(g) - 1, giveback24=giveback, **post))
    return pd.DataFrame(rows)


if __name__ == "__main__":
    R, RM, RF, m = base_data()
    allw = {}
    for gain in (0.40, 0.50):
        for thrp in (0.15, 0.20, 0.25):
            w = find_waves(R, RM, gain=gain, thr=np.log(1 / (1 - thrp)))
            allw[(gain, thrp)] = w
            print(f"gain>={gain:.0%} thr={thrp:.0%}: n={len(w)}, medyan RS kazanc={w.rs_gain.median():.0%}, "
                  f"medyan sure={w.months.median():.0f} ay, medyan abs={w.abs_gain.median():.0%}, "
                  f"post12 RS medyan={w.rs_post12.median():+.1%}, post24 RS medyan={w.rs_post24.median():+.1%}, "
                  f"giveback24 medyan={w.giveback24.median():.0%}")
    w = allw[(0.40, 0.20)]
    w.to_pickle(os.path.join(OUT, "waves_40_20.pkl"))
    allw[(0.50, 0.20)].to_pickle(os.path.join(OUT, "waves_50_20.pkl"))
    w["dec"] = (w.start.apply(lambda p: p.year) // 10) * 10
    print(w.groupby("dec").agg(n=("ind", "size"), rs_med=("rs_gain", "median"), mo_med=("months", "median"),
                                post12=("rs_post12", "median"), post24=("rs_post24", "median"),
                                gb=("giveback24", "median")))
    # sektor-ay sayisi (dalga sikligi normalize)
    nobs = R.notna().sum().sum()
    print("sektor-ay basina dalga baslangici:", len(w) / nobs * 12, "yilda sektor basina")
    print(w.groupby("ind").size().sort_values(ascending=False).head(15))
    print(w.sort_values("start").tail(40)[["ind", "start", "peak", "months", "rs_gain", "abs_gain", "max12", "ongoing", "rs_post12", "giveback24"]].to_string())
