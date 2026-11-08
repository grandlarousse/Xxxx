"""Aday enerji_tarim_S2 (genel kütüphane sinyali, ailede inceleme): VIX vade yapısı backwardation'dan çıkışı -> petrol/enerji long.
Sinyal (strategies.LIB['VX_backw_donus']): t'de CBOE:VIX/CBOE:VIX3M < 1.0 ve t-1'de >= 1.0 (VIX kapanışı 16:15 ET).
Giriş: C1 (t+1 kapanışı; VIX'in 16:15 kapanışı sorunu yok), çıkış t+3 kapanışı (h=2).
Not: genel_tum.csv taramasından (31 sinyal x 3 mod x 3 h) seçildi -> seçim yanlılığı riski yüksek.
Çalıştırma: python3 -I kod/ajan_enerji_tarim/aday_S2_vix_backw_petrol.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import ortak as O, lib, inceleme as I
import strategies as S

pd.set_option("display.width", 250)
ctx = {"VIX": lib.vol_index("VIX"), "VIX3M": lib.vol_index("VIX3M")}

def sig_for(sym):
    d = lib.load(sym)
    s = S.LIB["VX_backw_donus"](d, ctx).reindex(d.index).fillna(False).astype(bool)
    s.iloc[:200] = False
    return s

s, tr = I.rapor("S2: VIX/VIX3M backwardation çıkışı -> USO long, C1, h=2", "USO", sig_for("USO"), 2, "C1",
                diger=("BNO", "UCO", "SCO", "PDBC", "DBC", "XLE", "XOP", "OIH", "ERX", "GUSH", "UNG", "DBA", "CORN", "WEAT"), sig_for=sig_for)
ev = sig_for("USO"); ev = ev[ev]
print("\n-- Sinyal günleri yıl dağılımı:", ev.groupby(ev.index.year).size().to_dict())
print("-- Sinyal tarihleri (ilk 60):", [str(d.date()) for d in ev.index[:60]])
# SPY'de (aile dışı) aynı kural: sinyal genel risk iştahı mı?
ss, _ = O.full("SPY", sig_for("SPY"), 2, "C1")
print("\n-- Karşılaştırma SPY C1 h2:", {k: round(float(ss[k]), 2) for k in ["n", "mean_gross_bp", "mean_net_bp", "t", "is_net_bp", "oos_net_bp", "years_pos_frac"]})
# XLE ile non-PTP uygulama
s2, _ = I.rapor("S2 non-PTP uygulama: aynı sinyal -> XLE long, C1, h=2", "XLE", sig_for("XLE"), 2, "C1")
