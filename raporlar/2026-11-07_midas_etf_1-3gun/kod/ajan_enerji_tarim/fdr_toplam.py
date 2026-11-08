"""Test sayımı ve BH-FDR (q=0.10).
  (i)  aileye özel testler (testler_*.csv; strateji testlerinde tek yönlü p, tanımlayıcı/regresyonda iki yönlü p)
  (ii) genel kütüphanenin aile içi satırları (genel_tum.csv, 28 ETF x 297 = 8316 satır; tek yönlü p: net>0)
  (iii) birleşik.
Önce h_dogalgaz.py, h_petrol.py, h_tarim_leadlag.py, leadlag_ozet.py, ek_kontroller.py çalıştırılmış olmalı.
Çalıştırma: python3 -I kod/ajan_enerji_tarim/fdr_toplam.py"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from scipy import stats as st
import ortak as O, lib

pd.set_option("display.width", 250)
own = pd.concat([pd.read_csv(f).assign(dosya=os.path.basename(f)) for f in sorted(glob.glob(os.path.join(O.OUT, "testler_*.csv")))], ignore_index=True)
gen = pd.read_csv(os.path.join(O.OUT, "genel_aile.csv"))
gen["p1"] = st.t.sf(gen["t"].fillna(-9), (gen["n"] - 1).clip(lower=2))
own["fdr_own"] = lib.bh_fdr(own["p1"].fillna(1).values, 0.10)
allp = np.concatenate([own["p1"].fillna(1).values, gen["p1"].fillna(1).values])
fl = lib.bh_fdr(allp, 0.10)
own["fdr_birlesik"] = fl[:len(own)]; gen["fdr_birlesik"] = fl[len(own):]
own.to_csv(os.path.join(O.OUT, "fdr_aileye_ozel.csv"), index=False)
print(f"Aileye özel test sayısı: {len(own)} (strateji {int((own.kind=='strateji').sum())}, tanımlayıcı {int((own.kind=='tanimlayici').sum())}, regresyon {int((own.kind=='regresyon').sum())})")
print(f"Genel kütüphane aile içi test sayısı: {len(gen)}  -> toplam {len(own) + len(gen)}")
print(f"BH-FDR q=0.10 | yalnız aileye özel: {int(own.fdr_own.sum())} geçen | birleşik: {int(own.fdr_birlesik.sum()) + int(gen.fdr_birlesik.sum())} geçen")
print("\nAileye özel FDR geçenler:")
print(own[own.fdr_own][["hyp", "sym", "desc", "mode", "h", "kind", "sign", "n", "net_bp", "t", "p1", "fdr_birlesik"]].round(4).to_string(index=False))
st_ = own[(own.kind == "strateji") & (own.sign == 1)]
print(f"\nUzun (long) strateji testleri: {len(st_)} | yalnız bunlar arasında BH-FDR geçen: {int(lib.bh_fdr(st_['p1'].fillna(1).values, 0.10).sum())}")
print("En düşük p'li 8 long strateji testi:")
print(st_.sort_values("p1").head(8)[["hyp", "sym", "mode", "h", "n", "net_bp", "t", "is_net_bp", "oos_net_bp", "years_pos", "p1"]].round(4).to_string(index=False))
for hyp in ["EN01k_EIA_kis_KOLD", "EN01_EIA_KOLD"]:
    r = own[(own.hyp == hyp) & (own["mode"] == "C0") & (own.h == 1)]
    if len(r):
        p = float(r.p1.iloc[0]); m = len(own)
        print(f"{hyp} C0 h1: p1={p:.4f}; BH için en iyi durumda gereken p <= {0.10 * 1 / m:.5f} (m={m}, sıra 1)")
