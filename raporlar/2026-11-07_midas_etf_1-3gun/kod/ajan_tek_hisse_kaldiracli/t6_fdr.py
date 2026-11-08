"""Toplam test sayısı ve birleşik BH-FDR (q=0,10) — tek hisse kaldıraçlı aile.
Kapsam: (1) genel_tum aile ETF satırları, (2) dayanak genel kütüphane hisse satırları, (3) dayanak genel havuz satırları,
(4) hipotez testleri (hisse + havuz), (5) öncü kural testleri, (6) ek lead-lag regresyonları, (7) BTC ve SMH regresyonları,
(8) bilanço testleri, (9) S1 komşu/maliyet/gerçek ETF kontrolleri.
Çalıştırma: python3 -I kod/ajan_tek_hisse_kaldiracli/t6_fdr.py   Çıktı: fdr_tum_testler.csv"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import thk, lib

O = thk.OUT
parts = []
def add(fn, grp, pcol="p", label_cols=(), tcol="t", ncol=None):
    p = os.path.join(O, fn)
    if not os.path.exists(p): print("yok:", fn); return
    d = pd.read_csv(p)
    if pcol not in d.columns:
        d[pcol] = [lib.t_to_p(t, n) for t, n in zip(d[tcol], d[ncol])]
    lab = d[list(label_cols)].astype(str).agg("|".join, axis=1) if label_cols else pd.Series(fn, index=d.index)
    parts.append(pd.DataFrame({"grup": grp, "etiket": lab, "p": d[pcol], "t": d[tcol] if tcol in d.columns else np.nan}))
add("genel_aile_satirlar.csv", "1_genel_tum_aile_ETF", label_cols=("sym", "sig", "mode", "h", "exit"))
add("dayanak_genel_satirlar.csv", "2_dayanak_genel_hisse", label_cols=("stock", "sig", "mode", "h", "exit"))
add("dayanak_genel_havuz.csv", "3_dayanak_genel_havuz", pcol="p_havuz", label_cols=("sig", "mode", "h", "exit"), tcol="t_havuz")
add("hipotez_testleri.csv", "4_hipotez", label_cols=("hipotez", "duzey", "stock", "mode", "h"))
add("oncu_kural_testleri.csv", "5_oncu_kural", label_cols=("hipotez", "duzey", "stock", "mode", "h"))
add("leadlag_ek_regresyon.csv", "6_leadlag_ek", label_cols=("hisse", "oncu", "tip", "h"))
add("th06_btc_regresyon.csv", "7_btc_reg", tcol="t_x", ncol="n", label_cols=("hisse", "x", "y"))
s = pd.read_csv(os.path.join(O, "smh_nvda_regresyon.csv")); s = s[s.donem == "tum"]; s.to_csv(os.path.join(O, "_smh_tum.csv"), index=False)
add("_smh_tum.csv", "7_smh_reg", tcol="t_x", ncol="n", label_cols=("x", "y"))
os.remove(os.path.join(O, "_smh_tum.csv"))
add("bilanco_testleri.csv", "8_bilanco", label_cols=("test",))
s1 = os.path.join(O, "aday_S1_ozet.csv")
if os.path.exists(s1):
    d = pd.read_csv(s1)
    d = d[d.test != "dayanak_7"]   # ana satırlar hipotez_testleri'nde TH03 olarak zaten var
    d.to_csv(os.path.join(O, "_s1.csv"), index=False); add("_s1.csv", "9_S1_kontrol", label_cols=("test", "mode")); os.remove(os.path.join(O, "_s1.csv"))
A = pd.concat(parts, ignore_index=True)
A = A[np.isfinite(A.p)]
A["fdr"] = lib.bh_fdr(A.p.values, 0.10)
thr = A[A.fdr].p.max() if A.fdr.any() else np.nan
A.to_csv(os.path.join(O, "fdr_tum_testler.csv"), index=False)
print("Toplam test:", len(A), " BH-FDR q=0,10 eşik p <=", thr, " geçen:", int(A.fdr.sum()),
      " (pozitif t:", int((A.fdr & (A.t > 0)).sum()), ", negatif t:", int((A.fdr & (A.t < 0)).sum()), ")")
print(A.groupby("grup").agg(n=("p", "size"), gecen=("fdr", "sum")).to_string())
print("\nGeçen pozitifler:"); print(A[A.fdr & (A.t > 0)].sort_values("p").head(40).to_string(index=False))
key = A[A.etiket.str.contains("TH03_rsi2_trend_sma5cikis\\|havuz", regex=True)]
print("\nS1 (TH03) havuz satırları:"); print(key.to_string(index=False))
# yalnız strateji testleri (regresyonlar hariç) için ayrı FDR
St = A[~A.grup.isin(["6_leadlag_ek", "7_btc_reg", "7_smh_reg"])].copy()
St["fdr_strateji"] = lib.bh_fdr(St.p.values, 0.10)
print("\nYalnız strateji testleri:", len(St), " geçen:", int(St.fdr_strateji.sum()), " pozitif:", int((St.fdr_strateji & (St.t > 0)).sum()))
print(St[St.etiket.str.contains("TH03_rsi2_trend_sma5cikis\\|havuz", regex=True)].to_string(index=False))
