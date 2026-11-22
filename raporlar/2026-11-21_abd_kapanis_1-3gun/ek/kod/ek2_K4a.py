# -*- coding: utf-8 -*-
"""ek2_K4a.py - YONTEM Ek 2: K4a kurallari 'muzayede' komisyon senaryosuyla (gorev RF1b).
Kural uretimi aile_K4a.py'den AYNEN alinir (ice aktarma); tek fark komisyon=("hisse","muzayede").
  python3 -I ek2_K4a.py is <i0> <i1>     # kural tanimlari [i0, i1) icin yalniz IS -> scratchpad
  python3 -I ek2_K4a.py oos              # aday_ek2_RF1b.csv'deki K4a adaylari icin OOS + SON + Giris A"""
import os
import sys
import time

KOD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOD)
import numpy as np        # noqa: E402
import pandas as pd       # noqa: E402
import motor as M         # noqa: E402
import aile_K4a as A      # noqa: E402
import ek2_ortak_RF1b as E  # noqa: E402

AILE = "K4a"


def hazirla():
    m = M.Motor()
    KL = A.kurallar()
    return m, KL


def asama_is(i0, i1):
    t0 = time.time()
    m, KL = hazirla()
    g0 = A.G(m)
    out = []
    for i, k in enumerate(KL):
        if i < i0 or i >= i1 or k["sz"]:
            continue
        s, guc = k["fn"](g0)
        res = A.calis(m, {**k}, s, guc, h=(1, 2, 3), giris=("K",), gece=True, korunma="yok", komisyon=E.KOMS,
                      donemler=["IS"], rejimler=False)
        r = res[0]
        r = r[(r.donem == "IS") & (r.rejim == "hepsi")].copy()
        r["anahtar"] = A.anahtar(k)
        r["ki"] = i
        out.append(r)
    D = pd.concat(out, ignore_index=True)
    D["cok"] = D.hedef.str.startswith("COK(")
    D["tek_yon"] = D.yon.isin(["uzun", "kisa"])
    D["aday"] = [A.gecer(r, r.cok, r.tek_yon) for _, r in D.iterrows()]
    D["t_karar"] = np.where(D.cok, D.t_kume, D.t_olcekli)
    D["is_donem"], D["oos_donem"], D["aile_g"] = "IS", "OOS", AILE
    E.yaz_is(D, AILE, f"_{i0}_{i1}")
    print(f"{AILE} IS [{i0},{i1}): {len(D)} satir; aday hisse={int(D[D.komisyon == 'hisse'].aday.sum())} "
          f"muzayede={int(D[D.komisyon == 'muzayede'].aday.sum())} ({time.time() - t0:.0f} sn)", flush=True)


def asama_oos():
    t0 = time.time()
    m, KL = hazirla()
    g0 = A.G(m)
    AD = pd.read_csv(E.F_ADAY)
    AD = AD[AD.aile_g == AILE]
    satir, tum = [], []
    for _, a in AD.iterrows():
        k = KL[int(a.ki)]
        s, guc = k["fn"](g0)
        hh = int(a.h)
        kw = dict(giris=("K", "A"), korunma="yok", komisyon=E.KOMS, donemler=["OOS", "SON"], rejimler=False,
                  bootstrap=True)
        kw.update({} if k["degisken"] else A.hkw(hh))
        res, isl_d = A.calis(m, k, s, guc, **kw)
        res = res[(res.h == hh) & (res.cikis == a.cikis) & (res.rejim == "hepsi")].copy()
        res["anahtar"], res["ki"] = a.anahtar, a.ki
        tum.append(res)
        isl = isl_d.get(("K", hh, a.cikis, "yok"))
        sat = E.ozetle(m, a, res, isl, lambda x: A.gecer(x, a.cok, a.tek_yon), ("OOS", "SON"), AILE)
        satir.append(sat)
        print(a.anahtar, hh, a.cikis, "OOS muz:", round(sat.get("K_OOS_muzayede_net", np.nan), 1),
              round(sat.get("K_OOS_muzayede_t", np.nan), 2), flush=True)
    pd.DataFrame(satir).to_pickle(os.path.join(E.SCR, f"oos_{AILE}.pkl"))
    pd.concat(tum, ignore_index=True).to_pickle(os.path.join(E.SCR, f"oossema_{AILE}.pkl"))
    print(f"{AILE} OOS bitti: {len(satir)} aday ({time.time() - t0:.0f} sn)")


if __name__ == "__main__":
    if sys.argv[1] == "is":
        asama_is(int(sys.argv[2]), int(sys.argv[3]))
    else:
        asama_oos()
