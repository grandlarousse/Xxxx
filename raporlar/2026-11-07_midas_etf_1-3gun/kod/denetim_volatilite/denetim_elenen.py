"""Denetim: elenen/ölçüm iddialarından örnekler (VO01, H_kont09, VO03 koşulsuz kayıp, E2 Pazartesi). Kendi motorum.
Çalıştırma: python3 -I kod/denetim_volatilite/denetim_elenen.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, pandas as pd
import dlib, lib
vix = lib.vol_index("VIX"); v3 = lib.vol_index("VIX3M")
sv = lib.load("SVXY"); idx = sv.index
R = (vix / v3).reindex(idx); V = vix.reindex(idx); sma10 = V.rolling(10).mean()
# VO01: R<0.90 & VIX<SMA10 -> SVXY, max 3 gün, R>=1 olursa erken çıkış (C0)
s = ((R < 0.90) & (V < sma10)).fillna(False); ex = (R >= 1.0).fillna(False).values
c = sv.c.values; o = sv.o.values; n = len(sv); COST = dlib.cost("SVXY")
for mode in ("C0", "O1", "C1"):
    out = []; busy = -1
    for i in range(n):
        if not s.values[i] or i < busy: continue
        if mode == "C0": e, ep, last, f = i, c[i], i + 3, i + 1
        elif mode == "O1":
            e = i + 1; last = i + 3; f = e
            if e >= n: break
            ep = o[e]
        else:
            e = i + 1; last = i + 4; f = e + 1
            if e >= n or i + 1 <= busy: continue
            ep = c[e]
        if last >= n: break
        x = last
        for j in range(f, last + 1):
            if ex[j]: x = j; break
        out.append(c[x] / ep - 1 - COST / 1e4); busy = x
    out = np.array(out); print(f"VO01 SVXY {mode}: n={len(out)} net={out.mean()*1e4:.1f} t={dlib.tstat(out):.2f}")
# H_kont09 O1 h1
s2 = (R < 0.90).fillna(False)
t_ = dlib.sim(sv, s2, 1, "O1", COST); print(f"H_kont09 SVXY O1 h1: n={len(t_)} net={t_.net.mean()*1e4:.1f} t={dlib.tstat(t_.net):.2f}")
# VO03 koşulsuz günlük ortalama
for sym in ["VXX", "VIXY", "UVXY", "UVIX", "SVXY", "SVIX", "VIXM"]:
    d = lib.load(sym); r = d.c.pct_change().dropna()
    print(f"  {sym}: günlük ort {r.mean()*1e4:6.1f} bp, medyan {r.median()*1e4:6.1f}, gece ort {(d.o/d.c.shift(1)-1).mean()*1e4:6.1f}, gün içi ort {(d.c/d.o-1).mean()*1e4:6.1f}")
# E2 Pazartesi gün içi (O1 h1, Cuma sinyali)
for sym in ["SVXY", "SVIX", "VXX"]:
    d = lib.load(sym); dow = pd.Series(d.index.dayofweek, index=d.index)
    nxt = dow.shift(-1)
    s3 = (nxt == 0).fillna(False)
    t3 = dlib.sim(d, s3, 1, "O1", dlib.cost(sym)); x = dlib.summ(t3)
    print(f"E2 {sym} Pazartesi gün içi: n={x['n']} net={x['net_bp']:.1f} t={x['t']:.2f} IS={x['is_net_bp']:.1f} (t {x['is_t']:.2f}) OOS={x['oos_net_bp']:.1f} (t {x['oos_t']:.2f})")
