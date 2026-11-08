"""Denetim kripto ek kontroller: kaldıraç kaybı, BITO dağıtımı, uzun dönem Perşembe (UTC günlük), BTC seans
permütasyonu, kopya likiditesi, kaçırılan fırsat testi (IBIT gece primi büyük pozisyonda / koşullu).
Çalıştır: python3 -I kod/denetim_kripto/d_ek.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import dk, lib

pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
ROOT = dk.ROOT; OUT = dk.OUT

print("=== 1) Kaldıraç/ters takip kaybı e = r_lev - L r_1x (günlük, bp) ===")
IB = lib.load("IBIT"); EA = lib.load("ETHA")
for lev, base, Lm in (("BITX", IB, 2), ("BITU", IB, 2), ("SBIT", IB, -2), ("BITI", IB, -1), ("ETHU", EA, 2)):
    a = lib.load(lev).c.pct_change(); b = base.c.pct_change()
    e = (a - Lm * b).dropna()
    print(f"  {lev}: ort {e.mean()*1e4:6.1f} bp/gün (t={dk.tt(e):.2f}), medyan {e.median()*1e4:.1f}, n={len(e)}")

print("\n=== 2) BITO dağıtım kaydı ===")
bo = lib.load("BITO")
print(f"  BITO div toplamı (veri): {bo['div'].sum():.4f} $; div>0 gün sayısı: {(bo['div']>0).sum()}")
g = (bo.o / bo.c.shift(1) - 1) - (IB.o / IB.c.shift(1) - 1).reindex(bo.index)
first = pd.Series(bo.index, index=bo.index).groupby([bo.index.year, bo.index.month]).transform("min") == pd.Series(bo.index, index=bo.index)
print(f"  BITO-IBIT açılış boşluğu farkı: ay ilk günü {g[first].mean()*1e4:.0f} bp (n={g[first].notna().sum()}), diğer {g[~first].mean()*1e4:.0f} bp")

print("\n=== 3) Uzun dönem: BTC UTC günlük mumunda haftanın günleri (2016-11..2023-05 ve 2023-06+) ===")
d = pd.read_parquet(os.path.join(ROOT, "data", "crypto", "BTC-USD.parquet")); d.index = pd.to_datetime(d.index)
r = d.c / d.o - 1
for a, b in (("2016-11-01", "2023-05-31"), ("2023-06-01", "2026-11-07")):
    z = r[a:b]; dw = z.groupby(z.index.dayofweek).agg(["mean", "count", "std"])
    dw["t"] = dw["mean"] / (dw["std"] / np.sqrt(dw["count"]))
    print(f"  {a}..{b}:", {int(k): (round(v["mean"] * 1e4, 1), round(v["t"], 2)) for k, v in dw.iterrows()}, "(0=Pzt ... 3=Per; bp, t)")

print("\n=== 4) BTC 09:30-16:00 ET (saatlik) Perşembe: 5 günün en iyisi permütasyonu (2023-06+) ===")
BS = dk.btc_session("BTC-USD"); BS = BS[BS.index >= "2023-06-01"]
x = pd.DataFrame({"r": BS.c / BS.o - 1}).dropna(); x["wk"] = x.index.to_period("W")
obs = -x.r[x.index.dayofweek == 3].mean()
rng = np.random.default_rng(5); dows = x.index.dayofweek.values; rv = x.r.values; cnt = 0; reps = 5000
idx = list(x.groupby("wk").indices.values())
for k in range(reps):
    lab = dows.copy()
    for ii in idx: lab[ii] = rng.permutation(lab[ii])
    worst = max(-rv[lab == j].mean() for j in range(5))
    cnt += worst >= obs
print(f"  Perşembe BTC gün içi {-obs*1e4:.1f} bp; 'en kötü gün' seçimine göre düzeltilmiş p={cnt/reps:.4f}")
for y, g_ in x.groupby(x.index.year):
    gt = g_.r[g_.index.dayofweek == 3]
    print(f"   {y}: Perşembe {gt.mean()*1e4:6.1f} bp (n={len(gt)}), diğer {g_.r[g_.index.dayofweek != 3].mean()*1e4:6.1f}")

print("\n=== 5) Kaçırılan fırsat testi: IBIT gece (C0 al -> O1 sat) büyük pozisyonda ve koşullu ===")
on = (IB.o.shift(-1) / IB.c - 1).dropna(); idr = (IB.c / IB.o - 1).reindex(on.index)
for pos in (2500, 10000, 25000):
    c = dk.comm_bp(pos) + dk.tarama_spread("IBIT")
    print(f"  her gece, {pos}$: net {(on.mean()*1e4 - c):.1f} bp (brüt {on.mean()*1e4:.1f}, t_brüt={dk.tt(on):.2f}), n={len(on)}")
z = idr / idr.rolling(60).std().shift(1)
for lab, m in (("gün içi z<=-1 (gün içi sert düşüş sonrası gece)", z <= -1), ("gün içi z>=+1", z >= 1), ("Perşembe gecesi (Per kapanış->Cum açılış)", on.index.dayofweek == 3),
               ("Çarşamba gecesi", on.index.dayofweek == 2)):
    s = on[m.reindex(on.index).fillna(False).values] if hasattr(m, "reindex") else on[m]
    print(f"  {lab}: n={len(s)}, brüt {s.mean()*1e4:.1f} bp, t={dk.tt(s):.2f}")
# BTC 16:00ET->09:30 (gece) uzun 2023-06+ serisinde Perşembe gün içi düşüş sonrası
bon = (BS.o.shift(-1) / BS.c - 1); bid = BS.c / BS.o - 1
m = (BS.index.dayofweek == 3)
print(f"  BTC Perşembe gün içi -> Perşembe gecesi (16:00->Cum 09:30): {bon[m].mean()*1e4:.1f} bp (t={dk.tt(bon[m].dropna()):.2f}, n={m.sum()})")
