"""Denetim: S1 kuralı Şubat 2018 (Volmageddon) ve diğer uzun dönem kuyruk olaylarında sinyal verir miydi?
Gerçek SVXY verisi 2018-09-18'de başlar (SMA200 ısınması: ilk sinyal 2019-07). Bu nedenle ajanın 'Şubat 2018: pozisyon yok'
ifadesi kuralın olaydan kaçındığını değil, verinin olmadığını gösterir. Burada (i) ajanın vekil serisi (-0,5x, VIX vade yapısı modeli),
(ii) VIXY'den -0,5x sentetik seri (2017-07+; SMA200 2018-05'te ısınır) ve (iii) SMA200 yerine daha kısa ısınma ile kontrol edilir.
Çalıştırma: python3 -I kod/denetim_volatilite/denetim_subat2018.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "ajan_volatilite"))
import numpy as np, pandas as pd
import dlib, lib, vlib
pd.set_option("display.width", 250)
COST = dlib.cost("SVXY")
px = vlib.synth_proxy(-0.5); pc = px.c
r = dlib.wilder_rsi(pc, 2); m = dlib.sma(pc, 200)
sig = ((r < 10) & (pc > m)).fillna(False)
w = pd.DataFrame({"vekil_c": pc, "ret_%": pc.pct_change() * 100, "rsi2": r, "sma200": m, "sinyal": sig}).loc["2018-01-25":"2018-02-12"]
print("Vekil -0,5x, Şubat 2018 çevresi:\n", w.round(2).to_string())
tr = dlib.sim(px, sig, 2, "C0", COST)
print("\nVekil S1 C0 h2 en kötü 8 işlem:"); print(tr.nsmallest(8, "net").assign(net_bp=lambda d: d.net * 1e4)[["sig", "giris", "cikis", "net_bp"]].round(0).to_string())
# VIX endeksi ile: 2018-02-02 kapanışında SVXY (-0,5x) 'RSI2<10 & SMA200 üstü' olurdu mu? VIXY'den sentetik kontrol
vx = lib.load("VIXY"); rc = vx.c.pct_change()
syn = 100 * (1 - 0.5 * rc.fillna(0)).cumprod()
rs = dlib.wilder_rsi(syn, 2); ms = dlib.sma(syn, 200)
print("\nVIXY'den -0,5x sentetik (2017-07+; SMA200 ancak 2018-05'te oluşur):")
print(pd.DataFrame({"syn": syn, "ret_%": syn.pct_change() * 100, "rsi2": rs, "sma200": ms, "sma50": dlib.sma(syn, 50)}).loc["2018-01-29":"2018-02-09"].round(2).to_string())
# Sentetik ile 2018-02-02 C0 girişinin 2 günlük sonucu
d0 = pd.Timestamp("2018-02-02"); i = syn.index.get_loc(d0)
print(f"\n2018-02-02 C0 giriş -> 2018-02-06 kapanış (-0,5x sentetik, 16:00 kapanışları): {(syn.iloc[i+2]/syn.iloc[i]-1)*100:.1f}%  (NAV 16:15 bazında daha kötü)")
print(f"VIX 2018-02-02: {lib.vol_index('VIX').loc['2018-02-02']:.2f}, 2018-02-05: {lib.vol_index('VIX').loc['2018-02-05']:.2f}")
# Vekil kuyruk tablosu: her yıl en kötü işlem
print("\nVekil S1 yıl yıl (n, ort net bp, en kötü bp):")
g = tr.groupby(tr.sig.dt.year).net
print(pd.DataFrame({"n": g.count(), "ort": (g.mean() * 1e4).round(0), "en_kotu": (g.min() * 1e4).round(0)}).T.to_string())
