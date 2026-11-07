#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
02c_tuprs_duyarlilik.py - TUPRS <- ABD enerji sanayi artigi (Ken French 49 'Oil' - beta*piyasa), rehberdeki rafineri
kuralinin YAPISIYLA (hedge'siz, |z|>1, 2 gun, ortusmesiz) - yalniz duyarlilik; etiket aile P'ye gore verildi.
Amac: rafineri kuralinin (VLO/MPC/PSX/PBF; Yahoo kapali -> burada yeniden test EDILEMEZ) izinli veriyle bagimsiz
bir vekilini gormek. French verisi ~1 ay gecikmeli yayimlanir -> CANLI KULLANILAMAZ (canli vekil AMEX:XLE - b*SP:SPX).
"""
import os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak as o


def main():
    cal = o.takvim()
    r = o.bist_getiri("TUPRS", cal)
    f49 = o.french49(); ff = o.french_ff(); mkt = ff["MktRF"] + ff["RF"]
    y = f49["Oil"]; P = y - o.rolling_beta(y, mkt) * mkt
    L = o.us_to_bist(P, cal)
    z = (L / L.rolling(250, min_periods=100).std().shift(1))
    out = []
    for h in (1, 2, 3):
        fwd = sum(r.shift(-j) for j in range(1, h + 1))
        keep, son = [], -10**9
        for i, (zz, v) in enumerate(zip(z.values, fwd.values)):
            if np.isfinite(zz) and abs(zz) > 1 and np.isfinite(v) and i - son >= h and cal[i] >= pd.Timestamp("2014-01-01"):
                keep.append((cal[i], np.sign(zz) * v * 1e4)); son = i
        s = pd.Series(dict(keep))
        for c in (8.0, 15.5):
            n_ = s - c
            def tt(x):
                return x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 10 else np.nan
            is_ = n_[:"2020"]; oos = n_["2021":]; s24 = n_["2024":]
            top = (s.sort_values(ascending=False).iloc[10:] - c)
            out.append(f"h={h} maliyet {c:.1f}: n {len(n_)}, brut {s.mean():+.1f}, net {n_.mean():+.1f} (t {tt(n_):+.2f}); "
                       f"IS {is_.mean():+.1f} ({tt(is_):+.2f}) / OOS {oos.mean():+.1f} ({tt(oos):+.2f}) / 2024+ {s24.mean():+.1f} ({tt(s24):+.2f}); "
                       f"en iyi 10 haric {top.mean():+.1f} ({tt(top):+.2f})")
    out.append(f"Son French tarihi: {P.dropna().index[-1].date()} (canli degil)")
    txt = "\n".join(out); print(txt)
    open(os.path.join(o.V, "sonuc", "tuprs_duyarlilik.txt"), "w").write(txt + "\n")


if __name__ == "__main__":
    main()
