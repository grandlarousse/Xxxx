# -*- coding: utf-8 -*-
"""ek2_K4b.py - YONTEM Ek 2: K4b kurallari 'muzayede' komisyon senaryosuyla (gorev RF1b).
aile_K4b.py modul duzeyinde calistigi icin kural tanimlari kaynaktan, "1) sinyaller + bakis" bolumune kadar
AYNEN yurutulur (exec); dosya degistirilmez. Tek fark komisyon=("hisse","muzayede").
  python3 -I ek2_K4b.py is | oos"""
import os
import sys
import time

KOD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOD)
import numpy as np        # noqa: E402
import pandas as pd       # noqa: E402
import ek2_ortak_RF1b as E  # noqa: E402

AILE = "K4b"
_src = open(os.path.join(KOD, "aile_K4b.py"), encoding="utf-8").read()
_kes = _src.index("# ============================================================================ 1) sinyaller + bakis")
NS = {"__file__": os.path.join(KOD, "aile_K4b.py"), "__name__": "aile_K4b_tanim"}
exec(compile(_src[:_kes], "aile_K4b.py", "exec"), NS)
m, K, M = NS["m"], NS["K"], NS["M"]
KMAP = {k["id"]: k for k in K}


def gecer(row, k):
    return NS["gecer"](row, k["cok"])


def asama_is():
    t0 = time.time()
    out = []
    for i, k in enumerate(K):
        tamam, rap = m.bakis_testi(k["fn"])
        assert tamam, (k["id"], rap)
        s = k["fn"](m)
        g = k["guc_fn"](m) if k["guc_fn"] else None
        don = ["IS2", "IS"] if k["yeni"] else ["IS"]
        d = m.degerlendir(s, k["hedef"], kural_id=k["id"], aile="D", ad=k["ad"], girdi=k["girdi"],
                          h=(1, 2, 3), giris=("K", "A"), gece=True, korunma=("yok",), komisyon=E.KOMS,
                          donemler=don, rejimler=False, guc=g, bootstrap=False,
                          notlar=f"yayin={k['yayin']}" if k["yayin"] else "")
        kd = d[(d.korunma == "yok") & (d.rejim == "hepsi") & (d.donem == ("IS2" if k["yeni"] else "IS"))
               & (d.giris == "K")].copy()
        kd["anahtar"], kd["ki"], kd["cok"] = k["id"], i, k["cok"]
        kd["tek_yon"] = kd.yon.isin(["uzun", "kisa"])
        kd["aday"] = [gecer(r, k) for _, r in kd.iterrows()]
        kd["t_karar"] = np.where(kd.cok, kd.t_kume, kd.t_olcekli)
        kd["is_donem"] = "IS2" if k["yeni"] else "IS"
        kd["oos_donem"] = "OOS2" if k["yeni"] else "OOS"
        out.append(kd)
    D = pd.concat(out, ignore_index=True)
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
        k = K[int(a.ki)]
        s = k["fn"](m)
        g = k["guc_fn"](m) if k["guc_fn"] else None
        hh = int(a.h)
        don = ["OOS2"] if k["yeni"] else ["OOS", "SON"]
        res, isl_d = m.degerlendir(s, k["hedef"], kural_id=k["id"], aile="D", ad=k["ad"], girdi=k["girdi"],
                                   h=(hh,) if hh else (), giris=("K", "A"), gece=(hh == 0), korunma=("yok",),
                                   komisyon=E.KOMS, donemler=don, rejimler=False, guc=g, bootstrap=True,
                                   islem_dondur=True)
        res = res[(res.h == hh) & (res.cikis == a.cikis) & (res.rejim == "hepsi")].copy()
        res["anahtar"], res["ki"] = a.anahtar, a.ki
        tum.append(res)
        sat = E.ozetle(m, a, res, isl_d.get(("K", hh, a.cikis, "yok")), lambda x: gecer(x, k), don, AILE)
        satir.append(sat)
        print(a.anahtar, hh, a.cikis, flush=True)
    pd.DataFrame(satir).to_pickle(os.path.join(E.SCR, f"oos_{AILE}.pkl"))
    if tum:
        pd.concat(tum, ignore_index=True).to_pickle(os.path.join(E.SCR, f"oossema_{AILE}.pkl"))
    print(f"{AILE} OOS bitti: {len(satir)} aday ({time.time() - t0:.0f} sn)")


if __name__ == "__main__":
    asama_is() if sys.argv[1] == "is" else asama_oos()
