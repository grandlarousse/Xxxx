# -*- coding: utf-8 -*-
"""ek2_K6.py - YONTEM Ek 2: K6 (volatilite urunleri, DIX/GEX) kurallari 'muzayede' komisyon senaryosuyla
(gorev RF1b). Kural uretimi ve panel aile_K6.py'den AYNEN (ice aktarma). Tek fark komisyon=("hisse","muzayede");
odunc ucreti motorda oldugu gibi kalir.
  python3 -I ek2_K6.py is | oos"""
import os
import sys
import time

KOD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOD)
import numpy as np        # noqa: E402
import pandas as pd       # noqa: E402
import motor as M         # noqa: E402
import yukle              # noqa: E402
import aile_K6 as A       # noqa: E402
import ek2_ortak_RF1b as E  # noqa: E402

AILE = "K6"


def hazirla():
    P = A.panel_genis()
    return M.Motor(P, kalite_df=yukle.kalite(), temettu_df=yukle.temettu())


def asama_is():
    t0 = time.time()
    m = hazirla()
    out = []
    vno = 0
    for ri, (kid, ad, fn, H, KOR, G, F, yil) in enumerate(A.KURALLAR):
        dd = fn(m)
        for v, (s, hdf) in dd.items():
            vno += 1
            cok = A.cok_hedef(s)
            if (s.abs().sum().sum() if cok else s.abs().sum()) == 0:
                continue
            tek = bool((np.asarray(s) >= 0).all() or (np.asarray(s) <= 0).all())
            Hv = (8,) if v.startswith("TERS") else H
            res = m.degerlendir(s, hdf, kural_id=kid, aile="F" if F else "H", ad=f"{ad} | {v}", girdi=v, h=Hv,
                                giris=(G,), gece=(G == "K" and Hv != (8,)), korunma=KOR, komisyon=E.KOMS,
                                donemler=["IS"], rejimler=False, bootstrap=False,
                                notlar=f"asama=ek2_IS; vno={vno}; yayin={yil}")
            res = res.copy()
            res["anahtar"], res["ki"], res["vno"], res["cok"], res["tek_yon"] = f"{ri}|{v}", ri, vno, cok, tek
            res["aday"] = [A.gecer(x, cok, tek) for _, x in res.iterrows()]
            out.append(res)
    D = pd.concat(out, ignore_index=True)
    D["t_karar"] = np.where(D.cok, D.t_kume, D.t_olcekli)
    D["is_donem"], D["oos_donem"], D["aile_g"] = "IS", "OOS", AILE
    E.yaz_is(D, AILE)
    print(f"{AILE} IS: {len(D)} satir; aday hisse={int(D[D.komisyon == 'hisse'].aday.sum())} "
          f"muzayede={int(D[D.komisyon == 'muzayede'].aday.sum())} ({time.time() - t0:.0f} sn)", flush=True)


def asama_oos():
    t0 = time.time()
    m = hazirla()
    AD = pd.read_csv(E.F_ADAY)
    AD = AD[AD.aile_g == AILE]
    satir, tum = [], []
    for _, a in AD.iterrows():
        ri = int(a.ki)
        kid, ad, fn, H, KOR, G, F, yil = A.KURALLAR[ri]
        v = a.anahtar.split("|", 1)[1]
        s, hdf = fn(m)[v]
        hedef = hdf
        notu = ""
        if isinstance(hedef, str) and hedef in ("SVXY_E", "UVXY_E"):
            hedef, notu = hedef.replace("_E", "_Y"), "; OOS ardil arac (_E 2018'de kapandi)"
        hh = int(a.h) if a.cikis == "kapanis" else 1
        gir = tuple(dict.fromkeys((a.giris, "A")))
        res, isl_d = m.degerlendir(s, hedef, kural_id=kid, aile="F" if F else "H", ad=f"{ad} | {v}", girdi=v,
                                   h=(hh,), giris=gir, gece=(a.cikis == "acilis"), korunma=(a.korunma,),
                                   komisyon=E.KOMS, donemler=["OOS", "SON"], rejimler=False, bootstrap=True,
                                   notlar=f"asama=ek2_OOS{notu}; yayin={yil}", islem_dondur=True)
        res = res[(res.cikis == a.cikis) & (res.rejim == "hepsi")].copy()
        res["anahtar"], res["ki"] = a.anahtar, a.ki
        tum.append(res)
        key = (a.giris, 0 if a.cikis == "acilis" else hh, a.cikis, a.korunma)
        aa = a.copy()
        aa["h"] = 0 if a.cikis == "acilis" else hh
        sat = E.ozetle(m, aa, res, isl_d.get(key), lambda x: A.gecer(x, bool(a.cok), bool(a.tek_yon)),
                       ("OOS", "SON"), AILE)
        sat["giris_kural"], sat["korunma"] = a.giris, a.korunma
        satir.append(sat)
        print(a.anahtar, hh, a.cikis, a.korunma, flush=True)
    pd.DataFrame(satir).to_pickle(os.path.join(E.SCR, f"oos_{AILE}.pkl"))
    if tum:
        pd.concat(tum, ignore_index=True).to_pickle(os.path.join(E.SCR, f"oossema_{AILE}.pkl"))
    print(f"{AILE} OOS bitti: {len(satir)} aday ({time.time() - t0:.0f} sn)")


if __name__ == "__main__":
    asama_is() if sys.argv[1] == "is" else asama_oos()
