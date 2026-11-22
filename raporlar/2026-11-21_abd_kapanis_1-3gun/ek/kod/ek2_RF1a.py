# -*- coding: utf-8 -*-
"""ek2_RF1a.py - YONTEM Ek 2 (maliyet duyarliligi, kapanis/acilis muzayedesi emri) : aileler K1, K2, K3, K7.
Ozgun aile betikleri DEGISTIRILMEZ; modul olarak ice aktarilir, kural/varyant uretimi ve aday olcutu AYNEN
kullanilir. Tek fark: eleme ve degerlendirme komisyon=("muzayede",) ile yapilir.
Calistirma (asama asama; her asama oncekinin ara dosyasini okur):
  python3 -I ek2_RF1a.py is K1|K2|K3|K7      -> ARA/is_<aile>.pkl  (yalniz IS / IS2)
  python3 -I ek2_RF1a.py aday                -> ../veri/aday_ek2_RF1a.csv  (OOS'a bakmadan ONCE)
  python3 -I ek2_RF1a.py oos K1|K2|K3|K7     -> ARA/oos_<aile>.pkl  (yalniz adaylar, OOS / OOS2, bootstrap)
  python3 -I ek2_RF1a.py detay K1|K2|K3|K7   -> ARA/detay_<aile>.pkl/.json (OOS'ta ayni yon ve t>=2 olanlar)
  python3 -I ek2_RF1a.py sonuc               -> ../veri/sonuc_ek2_RF1a.csv (motor SEMA)
"""
import os
import sys
import json
import time

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
KOD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOD)

import numpy as np
import pandas as pd
import motor as M

VERI = M.VERI_DIZIN
KOM = os.environ.get("EK2_KOM", "muzayede")     # "hisse" yalniz yeniden uretim denetimi icin
ARA = "/tmp/claude-0/-home-user-Xxxx/b23916bf-451a-5d36-8905-d1866417ce1f/scratchpad/ek2/RF1a"
if KOM != "muzayede":
    ARA = os.path.join(ARA, "denetim_" + KOM)
os.makedirs(ARA, exist_ok=True)
ADAY_YOL = os.path.join(VERI, "aday_ek2_RF1a.csv")
SONUC_YOL = os.path.join(VERI, "sonuc_ek2_RF1a.csv")
if KOM != "muzayede":                                       # denetim kosusu proje dosyalarina yazmaz
    ADAY_YOL = os.path.join(ARA, "aday_denetim.csv")
    SONUC_YOL = os.path.join(ARA, "sonuc_denetim.csv")
BIRINCIL_IS_ADAY = {"K1": 1, "K2": 0, "K3": 1, "K7": 23}   # d4_<aile>.md


def _t(row, cok):
    return row["t_kume"] if cok else row["t_olcekli"]


# ============================================================================= aile adaptorleri
class K1:
    ad = "K1"

    def __init__(self):
        import aile_K1 as A
        self.A = A
        self.m, self.kay = A.motor()
        self.V = {v["vid"]: v for v in A.varyantlar()}
        self.birimler = list(self.V) + [f"R6-05-{yad}" for _, yad in A.R6_05]

    def hat(self, b):
        return "ana" if b.startswith("R6-05") else self.V[b]["hat"]

    def calis(self, b, donemler, combos=None, korunma=None, giris=("K",), komisyon=(KOM,), rejimler=False,
              bootstrap=False, islem_dondur=False):
        A, m, kay = self.A, self.m, self.kay
        if b.startswith("R6-05"):
            yon = 1 if b.endswith("kural") else -1
            combos = combos or [(1, "kapanis"), (2, "kapanis"), (3, "kapanis"), (1, "acilis")]
            return A.r6_05_degerlendir(m, kay, yon, b.split("-")[-1], donemler, combos, giris=giris, komisyon=komisyon,
                                       rejimler=rejimler, bootstrap=bootstrap, islem_dondur=islem_dondur)
        v = self.V[b]
        if combos is None:
            h, gece = (1, 2, 3), True
        else:
            h = tuple(sorted({int(x) for x, c in combos if c == "kapanis"}))
            gece = any(c == "acilis" for _, c in combos)
        return A.degerlendir_varyant(m, kay, v, donemler, h=h, gece=gece, korunma=korunma, giris=giris,
                                     komisyon=komisyon, rejimler=rejimler, bootstrap=bootstrap, islem_dondur=islem_dondur)

    def is_satirlari(self, b):
        dn = ["IS2"] if self.hat(b) == "yeni" else ["IS"]
        return self.calis(b, dn)

    def aday_mi(self, row, b, esik=2.0):
        return bool(self.A.gecti(_Satir(row), esik=esik))

    def kor_varsayilan(self, b):
        return None


class _Satir:
    """dict/Series satirini K1.gecti'nin bekledigi nitelik erisimine cevirir."""
    def __init__(self, r):
        self.__dict__.update(dict(r))


class K2:
    ad = "K2"

    def __init__(self):
        import aile_K2 as A
        self.A = A
        self.m = M.Motor()
        self.V = {v["kid"]: v for v in A.butun_varyantlar(self.m)}
        self.birimler = list(self.V)

    def hat(self, b):
        return self.V[b]["hat"]

    def calis(self, b, donemler, combos=None, korunma=None, giris=None, komisyon=(KOM,), rejimler=None,
              bootstrap=False, islem_dondur=False):
        v = self.V[b]
        h = (1, 2, 3) if combos is None else tuple(sorted({int(x) for x, c in combos if c == "kapanis"}))
        gece = False if combos is None else any(c == "acilis" for _, c in combos)
        return self.m.degerlendir(v["sig"], v["hedef"], kural_id=v["kid"], aile="B", ad=v["ad"], girdi=v["girdi"],
                                  h=h, giris=giris or (v["giris"],), gece=gece, korunma=korunma or (v["kor"],),
                                  komisyon=komisyon, donemler=donemler,
                                  rejimler=v["rej"] if rejimler is None else rejimler, guc=v["guc"],
                                  bootstrap=bootstrap, islem_dondur=islem_dondur,
                                  notlar=f"ek2=muzayede; hat={v['hat']}")

    def is_satirlari(self, b):
        dn = ["IS2"] if self.hat(b) == "yeni" else ["IS"]
        r = self.calis(b, dn)
        return r

    def aday_mi(self, row, b, esik=2.0):
        if row["rejim"] != "hepsi":
            return False
        return self.A.gecti(row, self.A._coklu(self.V[b]), esik)

    def giris_varsayilan(self, b):
        return self.V[b]["giris"]


class K3:
    ad = "K3"

    def __init__(self):
        import aile_K3 as A
        self.A = A
        self.m = M.Motor()
        self.V = {f"{v['kid']}|{v['var']}": v for v in A.varyantlar()}
        self.birimler = list(self.V)
        self._S = {}

    def hat(self, b):
        return "ana"

    def sinyal(self, b):
        if b not in self._S:
            self._S[b] = self.V[b]["fn"](self.m)
        return self._S[b]

    def calis(self, b, donemler, combos=None, korunma=("yok",), giris=("K",), komisyon=(KOM,), rejimler=False,
              bootstrap=False, islem_dondur=False):
        v = self.V[b]
        S, G = self.sinyal(b)
        cok = isinstance(S, pd.DataFrame)
        if combos is None:
            h, gece = v["hs"], v["gece"]
        else:
            h = tuple(sorted({int(x) for x, c in combos if c == "kapanis"}))
            gece = any(c == "acilis" for _, c in combos)
        return self.m.degerlendir(S, v["hedef"], kural_id=v["kid"], aile=self.A.AILE, ad=v["ad"], girdi=v["girdi"],
                                  h=h, giris=giris, gece=gece, korunma=korunma or ("yok",), komisyon=komisyon,
                                  donemler=donemler, rejimler=rejimler, guc=G if cok else None, bootstrap=bootstrap,
                                  islem_dondur=islem_dondur, notlar=f"ek2=muzayede; varyant={v['var']}; yayin={v['yayin']}")

    def is_satirlari(self, b):
        return self.calis(b, ["IS"])

    def aday_mi(self, row, b, esik=2.0):
        S, _ = self.sinyal(b)
        cok = isinstance(S, pd.DataFrame)
        t = _t(row, cok)
        ok = (row["net_bps"] > 0) and np.isfinite(t) and t >= esik
        if row["yon"] != "iki":
            ok = ok and row["anormal_bps"] > 0 and np.isfinite(row["t_anormal"]) and row["t_anormal"] >= 2
        return bool(ok)


class K7:
    ad = "K7"

    def __init__(self):
        import aile_K7 as A
        self.A = A
        self.m = M.Motor()
        self.v = A.Veri(self.m)
        A.VERI_V = self.v
        self.V = {x["kid"]: x for x in A.varyantlar(self.v)}
        self.birimler = list(self.V)

    def hat(self, b):
        return "ana"

    def calis(self, b, donemler, combos=None, korunma=None, giris=("K",), komisyon=(KOM,), rejimler=None,
              bootstrap=False, islem_dondur=False):
        var = self.V[b]
        if combos is None:
            h, gece = var["h"], var["gece"]
        else:
            h = tuple(sorted({int(x) for x, c in combos if c == "kapanis"}))
            gece = any(c == "acilis" for _, c in combos)
        return self.A.deg(self.m, var, h=h, giris=giris, gece=gece, korunma=korunma or (var["kor"],),
                          komisyon=komisyon, donemler=donemler,
                          rejimler=var["rejim_test"] if rejimler is None else rejimler,
                          bootstrap=bootstrap, islem_dondur=islem_dondur, notlar_ek="ek2=muzayede; ")

    def is_satirlari(self, b):
        return self.calis(b, ["IS"])

    def aday_mi(self, row, b, esik=2.0):
        var = self.V[b]
        rejs = ["hepsi", "V<20", "V>30"] if var["rejim_test"] else ["hepsi"]
        if row["rejim"] not in rejs:
            return False
        return bool(self.A.gecti(row, self.A.tek_yonlu(var), esik) and row["n_islem"] >= (10 if esik == 2.0 else 0))


AILELER = {"K1": K1, "K2": K2, "K3": K3, "K7": K7}


def cok_hedef(row):
    return str(row["hedef"]).startswith("COK(")


# ============================================================================= asamalar
def asama_is(aile):
    t0 = time.time()
    a = AILELER[aile]()
    print(f"{aile}: hazirlik {time.time() - t0:.0f} sn, {len(a.birimler)} birim", flush=True)
    sat = []
    for b in a.birimler:
        r = a.is_satirlari(b)
        if r is None or not len(r):
            continue
        r = r.copy()
        r["birim"] = b
        r["hat"] = a.hat(b)
        r["aday"] = [a.aday_mi(x, b) for _, x in r.iterrows()]
        sat.append(r)
    IS = pd.concat(sat, ignore_index=True)
    IS["aile_kod"] = aile
    IS.to_pickle(os.path.join(ARA, f"is_{aile}.pkl"))
    n_test = int((IS["rejim"] == "hepsi").sum())
    print(f"{aile}: IS {len(IS)} satir ({n_test} 'hepsi'), aday {int(IS.aday.sum())}, {time.time() - t0:.0f} sn", flush=True)


def asama_aday():
    par = []
    for aile in AILELER:
        IS = pd.read_pickle(os.path.join(ARA, f"is_{aile}.pkl"))
        A = IS[IS["aday"]].copy()
        A["olcu"] = np.where(A["hedef"].astype(str).str.startswith("COK("), "t_kume", "t_olcekli")
        A["is_t"] = np.where(A["olcu"] == "t_kume", A["t_kume"], A["t_olcekli"])
        A["dogrulama_donemi"] = np.where(A["donem"] == "IS2", "OOS2", "OOS")
        A["oos_esik_t"] = np.where(A["donem"] == "IS2", 3.0, 2.0)
        A["birincil_is_aday_sayisi_aile"] = BIRINCIL_IS_ADAY[aile]
        A["ek2_test_sayisi_aile"] = int((IS["rejim"] == "hepsi").sum()) if aile != "K7" else int(
            IS["rejim"].isin(["hepsi", "V<20", "V>30"]).sum())
        par.append(A)
        print(f"{aile}: test {int((IS['rejim'] == 'hepsi').sum())}, aday {len(A)} (birincil {BIRINCIL_IS_ADAY[aile]})")
    A = pd.concat(par, ignore_index=True)
    kol = ["aile_kod", "birim", "kural_id", "aile", "ad", "hedef", "yon", "h", "giris", "cikis", "korunma", "komisyon",
           "donem", "rejim", "hat", "n_islem", "brut_bps", "net_bps", "anormal_bps", "t_olcekli", "t_kume", "t_anormal",
           "olcu", "is_t", "basabas_bps", "dogrulama_donemi", "oos_esik_t", "birincil_is_aday_sayisi_aile",
           "ek2_test_sayisi_aile"]
    A[kol].to_csv(ADAY_YOL, index=False)
    print(f"{len(A)} aday -> {ADAY_YOL}")
    if len(A):
        print(A[["aile_kod", "birim", "h", "cikis", "korunma", "rejim", "n_islem", "brut_bps", "net_bps", "is_t",
                 "t_anormal"]].round(2).to_string(index=False))


def _sec(r, a):
    """r (sonuc satirlari) icinden aday satiri a ile ayni h/cikis/korunma/giris/rejim."""
    x = r[(r["h"] == a["h"]) & (r["cikis"] == a["cikis"]) & (r["korunma"] == a["korunma"])
          & (r["giris"] == a["giris"]) & (r["rejim"] == a["rejim"])]
    return x


def asama_oos(aile):
    t0 = time.time()
    A = pd.read_csv(ADAY_YOL)
    A = A[A["aile_kod"] == aile]
    if not len(A):
        pd.DataFrame().to_pickle(os.path.join(ARA, f"oos_{aile}.pkl"))
        print(f"{aile}: aday yok")
        return
    a = AILELER[aile]()
    sat, oz = [], []
    for _, x in A.iterrows():
        b = x["birim"]
        combos = [(int(x["h"]) if x["cikis"] == "kapanis" else 1, x["cikis"])]
        rej = x["rejim"] != "hepsi"
        kw = dict(combos=combos, korunma=(x["korunma"],), giris=(x["giris"],), rejimler=True if rej else False)
        r = a.calis(b, [x["dogrulama_donemi"]], komisyon=(KOM,), bootstrap="tum" if rej else True, **kw)
        rh = a.calis(b, [x["dogrulama_donemi"]], komisyon=("hisse",), bootstrap=False, **kw)
        o, oh = _sec(r, x), _sec(rh, x)
        if not len(o):
            print("  satir bulunamadi", b, x["h"], x["cikis"])
            continue
        o, oh = o.iloc[0], (oh.iloc[0] if len(oh) else None)
        cok = cok_hedef(o)
        t = _t(o, cok)
        p = o["p_bootstrap"] if np.isfinite(o["p_bootstrap"]) else 1.0
        t2 = bool(a.aday_mi(o, b, esik=2.0)) if aile != "K7" else bool(
            a.A.gecti(o, a.A.tek_yonlu(a.V[b]), 2.0))
        oz.append(dict(aile_kod=aile, birim=b, kural_id=x["kural_id"], ad=x["ad"], hedef=x["hedef"], yon=x["yon"],
                       h=x["h"], giris=x["giris"], cikis=x["cikis"], korunma=x["korunma"], rejim=x["rejim"],
                       hat=x["hat"], dogrulama_donemi=x["dogrulama_donemi"], oos_esik_t=x["oos_esik_t"],
                       is_n=x["n_islem"], is_net_bps=x["net_bps"], is_t=x["is_t"], is_t_anormal=x["t_anormal"],
                       oos_n=o["n_islem"], oos_net_bps=o["net_bps"], oos_brut_bps=o["brut_bps"],
                       oos_anormal_bps=o["anormal_bps"], oos_t=t, oos_t_anormal=o["t_anormal"], oos_p=p,
                       oos_p_wilcoxon=o["p_wilcoxon"], oos_net_sigma=o["net_sigma"],
                       oos_t2=t2, birincil_oos_net_bps=(oh["net_bps"] if oh is not None else np.nan),
                       birincil_oos_t=(_t(oh, cok) if oh is not None else np.nan)))
        r["birim"] = b
        rh["birim"] = b
        sat += [r, rh]
    O = pd.DataFrame(oz)
    O.to_pickle(os.path.join(ARA, f"oos_{aile}.pkl"))
    pd.concat(sat, ignore_index=True).to_pickle(os.path.join(ARA, f"oos_satir_{aile}.pkl"))
    print(f"{aile}: OOS {len(O)} aday, t>=2 ayni yon: {int(O.oos_t2.sum())} ({time.time() - t0:.0f} sn)")
    print(O[["birim", "h", "cikis", "korunma", "rejim", "is_net_bps", "is_t", "oos_n", "oos_net_bps", "oos_t",
             "oos_t_anormal", "oos_p", "oos_t2", "birincil_oos_net_bps"]].round(3).to_string(index=False))


def asama_sonuc():
    par = []
    for aile in AILELER:
        IS = pd.read_pickle(os.path.join(ARA, f"is_{aile}.pkl"))
        par.append(IS)
        y = os.path.join(ARA, f"oos_satir_{aile}.pkl")
        if os.path.exists(y) and os.path.getsize(y) > 0:
            par.append(pd.read_pickle(y))
        y = os.path.join(ARA, f"detay_{aile}.pkl")
        if os.path.exists(y):
            par.append(pd.read_pickle(y))
    T = pd.concat(par, ignore_index=True)
    T["notlar"] = (T["notlar"].astype(str) + "; ek2=RF1a; aile_kod=" + T["aile_kod"].fillna("").astype(str)
                   if "aile_kod" in T else T["notlar"])
    T = T.drop(columns=[c for c in T.columns if c not in M.SEMA])
    T = T.drop_duplicates(subset=["kural_id", "ad", "hedef", "h", "giris", "cikis", "korunma", "komisyon", "donem",
                                  "rejim"], keep="last")
    M.yaz_sonuc(T, SONUC_YOL)
    print(f"{len(T)} satir -> {SONUC_YOL}")


if __name__ == "__main__":
    asama = sys.argv[1]
    if asama == "is":
        asama_is(sys.argv[2])
    elif asama == "aday":
        asama_aday()
    elif asama == "oos":
        asama_oos(sys.argv[2])
    elif asama == "detay":
        import ek2_RF1a_detay as D
        D.calis(sys.argv[2])
    elif asama == "sonuc":
        asama_sonuc()
