"""Aday enerji_tarim_S1: EIA haftalık doğalgaz depolama raporu öncesi KOLD (−2x doğalgaz) long.
Kural: t = EIA doğalgaz depolama raporu gününden (data/events/eia_ng_storage.csv; normalde Perşembe 10:30 ET) bir önceki
işlem günü (normalde Çarşamba). KOLD t kapanışında alınır (C0), t+1 kapanışında satılır (h=1).
Varyant S1k: yalnız Kasım-Mart rapor günleri (çekiş sezonu) -- NOT: bu ayrım tam yıl sonucu görüldükten SONRA eklendi (post-hoc).
Dayanak (UNG) ve ayna (BOIL) için aynı günün getirisi de basılır.
Çalıştırma: python3 -I kod/ajan_enerji_tarim/aday_S1_eia_kold.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import ortak as O, lib, inceleme as I

pd.set_option("display.width", 250)
eia = O.events("eia_ng_storage")["date"]

def sig_for(sym, winter=False):
    idx = lib.load(sym).index
    s = O.day_before(idx, eia)
    if winter:
        nxt_month = pd.Series(list(idx[1:].month) + [idx[-1].month], index=idx)
        s = s & nxt_month.isin([11, 12, 1, 2, 3])
    return s

s, tr = I.rapor("S1: EIA öncesi gün KOLD long, C0, h=1 (tam yıl)", "KOLD", sig_for("KOLD"), 1, "C0",
                diger=("UNG", "BOIL", "UNL"), sig_for=lambda d: sig_for(d))
s2, tr2 = I.rapor("S1k: yalnız Kasım-Mart (post-hoc ayrım)", "KOLD", sig_for("KOLD", True), 1, "C0",
                  diger=("UNG", "BOIL", "UNL"), sig_for=lambda d: sig_for(d, True))
# Nisan-Ekim karşılaştırması
idx = lib.load("KOLD").index
summer = sig_for("KOLD") & ~sig_for("KOLD", True)
s3, tr3 = O.full("KOLD", summer, 1, "C0")
print("\n-- Nisan-Ekim (enjeksiyon sezonu) KOLD C0 h1:", {k: round(s3[k], 2) for k in ["n", "mean_gross_bp", "mean_net_bp", "t", "is_net_bp", "oos_net_bp", "years_pos_frac"]})
# Haftanın günü kontrolü: rapor günü olmayan Perşembeler (tatil kayması) yok denecek kadar az; rapor kayınca etki de kayıyor mu?
k = lib.load("KOLD"); rk = np.log(k["c"]).diff()
rep = O.on_dates(k.index, eia)
thu = pd.Series(k.index.dayofweek == 3, index=k.index)
print("\n-- KOLD günlük ort. (bp): rapor günü Perşembe: %.1f (n=%d) | rapor günü Perşembe değil: %.1f (n=%d) | rapor olmayan Perşembe: %.1f (n=%d) | diğer günler: %.1f"
      % (rk[rep & thu].mean() * 1e4, (rep & thu).sum(), rk[rep & ~thu].mean() * 1e4, (rep & ~thu).sum(), rk[~rep & thu].mean() * 1e4, (~rep & thu).sum(), rk[~rep & ~thu].mean() * 1e4))
# PTP başa baş: %10 brüt satış kesintisi = işlem başına ~1000 bp
print("\n-- PTP: %%10 brüt satış stopajı işlem başına ≈ -1000 bp; S1 ortalama net %.0f bp => stopaj uygulanırsa beklenti ≈ %.0f bp/işlem"
      % (s["mean_net_bp"], s["mean_net_bp"] - 1000))
