# -*- coding: utf-8 -*-
"""ek2_K9.py - YONTEM Ek 2: K9 (gece-gunduz) kurallari 'muzayede' komisyon senaryosuyla (gorev RF1b).
Kural uretimi aile_K9.py'den AYNEN (ice aktarma). Tek fark komisyon=("hisse","muzayede").
Kosulsuz N1 kurallarinda anormal getiri tanim geregi ~0; t_anormal sarti degistirilmez. Ayrica (karar disi)
kosulsuz gece getirisinin bu senaryodaki neti betimlenir.
  python3 -I ek2_K9.py is | oos | betim"""
import os
import sys
import time

KOD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOD)
import numpy as np        # noqa: E402
import pandas as pd       # noqa: E402
import aile_K9 as A       # noqa: E402
import ek2_ortak_RF1b as E  # noqa: E402

AILE = "K9"
m = A.m


def gecer(x, kr):
    tt = A.anahtar_t(x, kr)
    return bool(x["giris"] == "K" and x["n_islem"] > 0 and x["net_bps"] > 0 and tt >= 2
                and x["anormal_bps"] > 0 and x["t_anormal"] >= 2)


def asama_is():
    t0 = time.time()
    out = []
    for i, kr in enumerate(A.KURALLAR):
        dn = ["IS2"] if kr["hat"] == "yy" else ["IS"]
        if kr["mod"] == "gece":
            r = A.deg(kr, h=(1,), giris=("A",), gece=True, korunma="yok", komisyon=E.KOMS, donemler=dn,
                      rejimler=False)
        else:
            r = A.deg(kr, h=(1, 2, 3), giris=("K", "A") if kr["grup"] == "r710" else ("K",), gece=True,
                      korunma="yok", komisyon=E.KOMS, donemler=dn, rejimler=False)
            if kr["grup"] == "r710":
                r = r[(r.giris == "K") | (r.h == 1)]
        r = r[r.giris == "K"].copy()                      # A (gunduz) satirlari ayristirma: test degil
        r["anahtar"] = f"{i}|{kr['id']}|{A.hedef_ad(kr)}"
        r["ki"], r["cok"], r["tek_yon"] = i, A.cok(kr), True
        r["aday"] = [gecer(x, kr) for _, x in r.iterrows()]
        r["is_donem"] = dn[0]
        r["oos_donem"] = "OOS2" if kr["hat"] == "yy" else "OOS"
        out.append(r)
    D = pd.concat(out, ignore_index=True)
    D["t_karar"] = np.where(D.cok, D.t_kume, D.t_olcekli)
    D["aile_g"] = AILE
    E.yaz_is(D, AILE)
    print(f"{AILE} IS: {len(D)} satir; aday hisse={int(D[D.komisyon == 'hisse'].aday.sum())} "
          f"muzayede={int(D[D.komisyon == 'muzayede'].aday.sum())} ({time.time() - t0:.0f} sn)", flush=True)


def asama_oos():
    t0 = time.time()
    AD = pd.read_csv(E.F_ADAY)
    AD = AD[AD.aile_g == AILE]
    satir, tum = [], []
    for _, a in AD.iterrows():
        kr = A.KURALLAR[int(a.ki)]
        dn = ["OOS2"] if kr["hat"] == "yy" else ["OOS", "SON"]
        if a.cikis == "acilis":
            r, isl_d = A.deg(kr, h=(1,), giris=(), gece=True, korunma="yok", komisyon=E.KOMS, donemler=dn,
                             rejimler=False, bootstrap=True, islem_dondur=True)
            key = ("K", 0, "acilis", "yok")
        else:
            r, isl_d = A.deg(kr, h=(int(a.h),), giris=("K", "A"), gece=False, korunma="yok", komisyon=E.KOMS,
                             donemler=dn, rejimler=False, bootstrap=True, islem_dondur=True)
            key = ("K", int(a.h), "kapanis", "yok")
        r = r[(r.h == int(a.h)) & (r.cikis == a.cikis)].copy()
        r["anahtar"], r["ki"] = a.anahtar, a.ki
        tum.append(r)
        sat = E.ozetle(m, a, r, isl_d.get(key), lambda x: gecer(x, kr), dn, AILE)
        sat["hat"] = kr["hat"]
        satir.append(sat)
        print(a.anahtar, a.h, a.cikis, flush=True)
    pd.DataFrame(satir).to_pickle(os.path.join(E.SCR, f"oos_{AILE}.pkl"))
    if tum:
        pd.concat(tum, ignore_index=True).to_pickle(os.path.join(E.SCR, f"oossema_{AILE}.pkl"))
    print(f"{AILE} OOS bitti: {len(satir)} aday ({time.time() - t0:.0f} sn)")


def asama_betim():
    """Karar disi: kosulsuz 'kapanista al, acilista sat' (N1) gece getirisi, iki maliyet senaryosu."""
    out = []
    for kr in A.KURALLAR:
        if kr["id"] != "N1" or kr["hedef"] not in ("SPY", "QQQ", "IWM", "DIA", "XLK", "XLF", "TQQQ", "UPRO"):
            continue
        r = A.deg(kr, h=(1,), giris=(), gece=True, korunma="yok", komisyon=E.KOMS,
                  donemler=["IS", "OOS", "SON", "TUM"], rejimler=False)
        out.append(r[["hedef", "komisyon", "donem", "n_islem", "brut_bps", "net_bps", "anormal_bps", "t_olcekli",
                      "t_anormal"]])
    B = pd.concat(out, ignore_index=True)
    B.to_csv(os.path.join(E.SCR, "betim_K9_gece.csv"), index=False)
    pd.set_option("display.width", 200)
    print(B.round(2).to_string(index=False))


if __name__ == "__main__":
    {"is": asama_is, "oos": asama_oos, "betim": asama_betim}[sys.argv[1]]()
