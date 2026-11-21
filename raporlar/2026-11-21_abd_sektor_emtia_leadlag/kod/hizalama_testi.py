"""Hizalama sınaması: bir öncü serinin (vadeli, endeks, yabancı hisse) t çubuğu ABD kapanışında biliniyor mu?

Mantık: f = öncünün t getirisi, r = ABD'de işlem gören karşılığının t getirisi. Eğer öncünün çubuğu 16:00 ET'den
sonra kapanıyorsa, (f - r) farkı karşılığın ERTESİ GECE getirisini (kapanış t -> açılış t+1) öngörür.
Kullanım: python3 kod/hizalama_testi.py
"""
import os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak as o

CIFTLER = [("CL=F","USO"),("BZ=F","BNO"),("NG=F","UNG"),("RB=F","UGA"),("GC=F","GLD"),("SI=F","SLV"),("HG=F","CPER"),
           ("PL=F","PPLT"),("PA=F","PALL"),("ZC=F","CORN"),("ZW=F","WEAT"),("ZS=F","SOYB"),("SB=F","CANE"),("ES=F","SPY"),
           ("NQ=F","QQQ"),("ZN=F","IEF"),("ZB=F","TLT"),("BTC=F","BITO"),("BTC-USD","BITO"),("BTC-USD","IBIT"),
           ("EURUSD=X","FXE"),("USDJPY=X","FXY"),("DX-Y.NYB","UUP"),("^TNX","IEF"),("^VIX","VIXY"),("^N225","EWJ"),
           ("^GDAXI","EWG"),("^HSI","FXI"),("2330.TW","TSM"),("BHP.AX","BHP"),("ASML.AS","ASML"),("SHEL.L","SHEL")]

def test(onc, kar, bas="2012-01-01"):
    f = o.hizali_getiri(onc, bilinen=False)
    c, op = o.panel("adjclose", [kar])[kar], o.panel("ao", [kar])[kar]
    r, gece = np.log(c).diff(), np.log(op / c.shift(1))
    d = pd.DataFrame({"f": f, "r": r, "gece_s": gece.shift(-1), "r_s": r.shift(-1), "r_o": r.shift(1)}).dropna()
    d = d[d.index >= bas]
    fark = d.f - d.r
    return dict(oncu=onc, karsilik=kar, n=len(d), corr_ayni_gun=round(d.f.corr(d.r), 2), corr_karsilik_ertesi=round(d.f.corr(d.r_s), 3),
                corr_karsilik_onceki=round(d.f.corr(d.r_o), 3), fark_ertesi_gece=round(fark.corr(d.gece_s), 3))

if __name__ == "__main__":
    t = pd.DataFrame([test(a, b) for a, b in CIFTLER])
    t.to_csv(os.path.join(o.KOK, "ek", "hizalama_testi.csv"), index=False)
    print(t.to_string(index=False))
