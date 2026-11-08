"""Aday enerji_tarim_S3 (genel kütüphane 'MR_bb20_alt' bulgusunun ailede incelenmesi):
Sinyal (USO verisiyle): t'de USO kapanışı < SMA20(USO) - 2*STD20(USO) (20 günlük alt Bollinger bandı, kapanış bazlı).
Giriş: C1 = t+1 kapanışı (bir gün bekle), çıkış t+3 kapanışı (h=2).  İşlem ETF'i: USO (PTP) ya da XOP (1940 Kanunu, PTP değil).
Uyarı: C0 (t kapanışında giriş) negatif -- etki 1 günlük gecikmeye bağlı (t+1 günü düşüş devam ediyor, t+2..t+3 dönüş).
genel_tum.csv taramasından seçildi (seçim yanlılığı); birleşik BH-FDR'yi geçmiyor.
Çalıştırma: python3 -I kod/ajan_enerji_tarim/aday_S3_uso_bb_gecikmeli.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import ortak as O, lib, inceleme as I
import strategies as S

pd.set_option("display.width", 250)
uso = lib.load("USO")
sig = S.LIB["MR_bb20_alt"](uso, None).reindex(uso.index).fillna(False).astype(bool)
sig.iloc[:200] = False
OTHERS = ("USO", "BNO", "DBO", "UCO", "PDBC", "GSG", "XLE", "OIH", "ERX", "GUSH", "DRIP", "SCO", "UNG", "DBA")
s, tr = I.rapor("S3a: USO alt Bollinger(20,2) kapanışı -> 1 gün bekle -> XOP long, C1, h=2", "XOP", sig, 2, "C1", diger=OTHERS)
s2, tr2 = I.rapor("S3b: aynı sinyal -> USO long, C1, h=2 (PTP)", "USO", sig, 2, "C1")
# her ETF'in KENDİ bandıyla (genel kütüphanedeki tanım) karşılaştırma
rows = []
for sym in ["USO", "BNO", "DBO", "USL", "XLE", "XOP", "OIH", "PDBC"]:
    d = lib.load(sym); sg = S.LIB["MR_bb20_alt"](d, None).reindex(d.index).fillna(False).astype(bool); sg.iloc[:200] = False
    ss, _ = O.full(sym, sg, 2, "C1")
    rows.append({"sym": sym, "kendi_bandi": True, **{k: ss[k] for k in ["n", "mean_gross_bp", "mean_net_bp", "t", "is_net_bp", "oos_net_bp", "years_pos_frac"]}})
print("\n-- Her ETF kendi Bollinger sinyaliyle (C1 h2):"); print(pd.DataFrame(rows).round(2).to_string(index=False))
# 2026 hariç
for nm, t_ in (("XOP", tr), ("USO", tr2)):
    x = t_[t_["sig_date"].dt.year < 2026]["net"]
    print(f"-- {nm}: 2026 hariç n={len(x)} net ort={x.mean()*1e4:.1f} bp t={x.mean()/(x.std()/np.sqrt(len(x))):.2f}")
