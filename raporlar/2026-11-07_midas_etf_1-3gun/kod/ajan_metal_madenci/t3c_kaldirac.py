"""H12 (MM06): kaldıraçlı/ters ürünlerde h günlük sapma e_h = r_LETF(t,t+h) - L*r_baz(t,t+h) (basit getiri),
öngörü: -((L^2-L)/2)*h*sigma_g^2 (sigma_g: dayanağın 20 günlük günlük std'si, t'de bilinir). Gece/gün içi ayrımı yok.
NUGT/DUST/JNUG/JDST 2020 öncesinde 3x idi (Direxion kaldıraç indirimi) -> bu ürünler için yalnız 2020-06 sonrası.
Çalıştır: python3 -I kod/ajan_metal_madenci/t3c_kaldirac.py
Çıktı: sonuclar/aile_metal_madenci/kaldirac_sapma.csv"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import mm

DIREXION = {"NUGT", "DUST", "JNUG", "JDST"}

def main():
    rows = []
    for le, (b, L) in mm.LEV.items():
        d1 = mm.load(le)["c"]; d0 = mm.load(b)["c"].reindex(d1.index)
        if le in DIREXION:  # Direxion madenci ürünleri 2020'de 3x'ten 2x'e indirildi -> yalnız 2x dönemi
            d1 = d1[d1.index >= pd.Timestamp("2020-06-01")]; d0 = d0.reindex(d1.index)
        sig = np.log(d0).diff().rolling(20).std()
        for h in (1, 2, 3):
            rl = d1.shift(-h) / d1 - 1; rb = d0.shift(-h) / d0 - 1
            e = (rl - L * rb).dropna()
            pred = (-((L * L - L) / 2) * h * sig ** 2).reindex(e.index)
            for per, m in (("tum", slice(None)), ("son1y", e.index >= e.index[-1] - pd.Timedelta(days=365))):
                ee = e[m]; pp = pred[m]
                rows.append({"letf": le, "baz": b, "L": L, "h": h, "donem": per, "n": len(ee),
                             "ort_sapma_bp": ee.mean() * 1e4, "medyan_sapma_bp": ee.median() * 1e4, "ongoru_bp": pp.mean() * 1e4,
                             "sapma_std_bp": ee.std() * 1e4,
                             "yuksek_vol_sapma_bp": ee[sig.reindex(ee.index) >= 0.03].mean() * 1e4 if (sig.reindex(ee.index) >= 0.03).any() else np.nan})
    R = pd.DataFrame(rows); R.to_csv(os.path.join(mm.OUTD, "kaldirac_sapma.csv"), index=False)
    pd.set_option("display.width", 200)
    print(R.round(2).to_string(index=False))

if __name__ == "__main__":
    main()
