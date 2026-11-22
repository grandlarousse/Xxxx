# -*- coding: utf-8 -*-
"""ornek_kural.py - uctan uca ornek:  python3 -I ornek_kural.py
Kural: SPY'nin gunluk (kapanistan kapanisa) getirisi <= -%2 ise kapanista SPY al, 1/2/3 gun tut.
Cikti: ../veri/ornek_sonuc.csv (standart sema)."""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motor import Motor, yaz_sonuc, VERI_DIZIN


def sinyal(m):
    """t gunune hizali {-1,0,+1}; yalniz t kapanisinda bilinen veri."""
    r = m.girdi_getiri("SPY")              # guvenli girdi: SPY ABD16, ayni gun
    return (r <= -0.02).astype(int)


if __name__ == "__main__":
    t0 = time.time()
    m = Motor()
    s = sinyal(m)
    temiz, rapor = m.bakis_testi(sinyal)   # T0 sonrasi veri bozulunca T0 oncesi sinyal degismemeli
    assert temiz, rapor
    sonuc, islemler = m.degerlendir(
        s, "SPY", kural_id="ORNEK-D01", aile="D", ad="SPY gunluk getiri <= -%2: kapanista SPY al",
        girdi="SPY kk getiri (t)", h=(1, 2, 3), giris=("K", "A", "G"), gece=True,
        korunma="yok",                     # hedef SPY'nin kendisi: SPY ile korunma anlamsiz
        bootstrap=True, islem_dondur=True)
    yol = yaz_sonuc(sonuc, os.path.join(VERI_DIZIN, "ornek_sonuc.csv"))
    print(f"{len(sonuc)} satir -> {yol}  ({time.time() - t0:.1f} sn, bootstrap dahil)")
    g = sonuc[(sonuc.komisyon == "hisse") & (sonuc.rejim == "hepsi")
              & sonuc.donem.isin(["STRES", "IS", "OOS", "SON"]) & sonuc.giris.isin(["K", "A"])]
    sut = ["donem", "giris", "cikis", "h", "n_islem", "brut_bps", "net_bps", "anormal_bps", "isabet",
           "t_olcekli", "p_bootstrap", "p_wilcoxon", "en_kotu_bps", "mdd_pct"]
    print(g[sut].round(2).to_string(index=False))
    tab, oz = m.bolum_ozeti(islemler[("K", 1, "kapanis", "yok")], "hisse")
    print("VIX(t-1) > 30 bolumleri (K, h=1):", {k: (round(v, 1) if isinstance(v, float) else v) for k, v in oz.items()})
