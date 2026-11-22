# -*- coding: utf-8 -*-
"""ek2_K5.py - YONTEM Ek 2: K5 (takvim) kurallari 'muzayede' komisyon senaryosuyla (gorev RF1b).
Kural uretimi aile_K5.py'den AYNEN (ice aktarma). Tek fark komisyon=("hisse","muzayede").
  python3 -I ek2_K5.py is | oos"""
import os
import sys
import time

KOD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOD)
import numpy as np        # noqa: E402
import pandas as pd       # noqa: E402
import motor as M         # noqa: E402
import aile_K5 as A       # noqa: E402
import ek2_ortak_RF1b as E  # noqa: E402

AILE = "K5"


def hazirla():
    m = M.Motor()
    tk = A.Takvim(m.idx)
    return m, A.kurallar(m, tk)


def aile_ad(k):
    return "E" if not k["kid"].startswith("R7-03") else "H"


def asama_is():
    t0 = time.time()
    m, K = hazirla()
    out = []
    for ki, k in enumerate(K):
        s, g = A.sinyal_al(m, k)
        for hed in k["hedefler"]:
            ss, hh = A.hedef_ve_sinyal(k, s, hed)
            cok, tekyon = k["cok"], A.tek_yonlu(ss)
            r = m.degerlendir(ss, hh, kural_id=k["kid"], aile=aile_ad(k), ad=k["ad"], girdi=k["girdi"], h=k["h"],
                              giris=("K",), gece=False, korunma=("yok",), komisyon=E.KOMS, donemler=["IS"],
                              rejimler=False, guc=g, notlar=f"yayin={A.yayin_yili(k['kid'])}; {k['tanim']}")
            r = r.copy()
            r["anahtar"], r["ki"], r["hedef_kod"], r["cok"], r["tek_yon"] = f"{ki}|{hed}", ki, hed, cok, tekyon
            r["aday"] = [A.gecer(x, cok, tekyon)[0] for _, x in r.iterrows()]
            out.append(r)
    D = pd.concat(out, ignore_index=True)
    D["t_karar"] = np.where(D.cok, D.t_kume, D.t_olcekli)
    D["is_donem"], D["oos_donem"], D["aile_g"] = "IS", "OOS", AILE
    E.yaz_is(D, AILE)
    print(f"{AILE} IS: {len(D)} satir; aday hisse={int(D[D.komisyon == 'hisse'].aday.sum())} "
          f"muzayede={int(D[D.komisyon == 'muzayede'].aday.sum())} ({time.time() - t0:.0f} sn)", flush=True)


def asama_oos():
    t0 = time.time()
    m, K = hazirla()
    AD = pd.read_csv(E.F_ADAY)
    AD = AD[AD.aile_g == AILE]
    satir, tum = [], []
    for _, a in AD.iterrows():
        k = K[int(a.ki)]
        s, g = A.sinyal_al(m, k)
        hed = a.anahtar.split("|", 1)[1]
        ss, hh_ = A.hedef_ve_sinyal(k, s, hed)
        h = int(a.h)
        res, isl_d = m.degerlendir(ss, hh_, kural_id=k["kid"], aile=aile_ad(k), ad=k["ad"], girdi=k["girdi"],
                                   h=(h,), giris=("K", "A"), gece=False, korunma=("yok",), komisyon=E.KOMS,
                                   donemler=["OOS", "SON"], rejimler=False, guc=g, bootstrap=True,
                                   islem_dondur=True)
        res = res[(res.h == h) & (res.cikis == "kapanis") & (res.rejim == "hepsi")].copy()
        res["anahtar"], res["ki"] = a.anahtar, a.ki
        tum.append(res)
        sat = E.ozetle(m, a, res, isl_d.get(("K", h, "kapanis", "yok")),
                       lambda x: A.gecer(x, bool(a.cok), bool(a.tek_yon))[0], ("OOS", "SON"), AILE)
        satir.append(sat)
        print(a.anahtar, h, flush=True)
    pd.DataFrame(satir).to_pickle(os.path.join(E.SCR, f"oos_{AILE}.pkl"))
    if tum:
        pd.concat(tum, ignore_index=True).to_pickle(os.path.join(E.SCR, f"oossema_{AILE}.pkl"))
    print(f"{AILE} OOS bitti: {len(satir)} aday ({time.time() - t0:.0f} sn)")


if __name__ == "__main__":
    asama_is() if sys.argv[1] == "is" else asama_oos()
