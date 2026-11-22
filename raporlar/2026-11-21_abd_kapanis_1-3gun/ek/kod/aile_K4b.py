# -*- coding: utf-8 -*-
"""aile_K4b.py - Aile D (2): akis vekilleri, kapitulasyon/genislik, kaldiracli ETF yolu.
Kurallar: R3-01..R3-04, R3-11 (uygulama denetimi), R8-10 (yol testi, betimsel), R8-11 (= R3-03 SPY %2),
yontem denetcisi ekleri (a) VIX - RV20, VIXY sicramasi, (b) evren genisligi, (c) buyuk gun + IBS.
Calistir:  python3 -I aile_K4b.py
Sira (YONTEM): 1) sinyaller + bakis testi  2) YALNIZ IS tarama -> aday_K4b.csv  3) yalniz adaylarda OOS ve
tam degerlendirme  4) gecenlerde 15:30 testi, ters/kaldiracli ETF satirlari, komsu parametre, bugun.
Ciktilar (../veri): aday_K4b.csv, sonuc_K4b.csv, karar_K4b.csv, kayma_K4b.csv (R3-11), yol_K4b.csv (R8-10),
kapanis1530_K4b.csv, bugun_K4b.csv."""
import os
import sys
import time
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
KOD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOD)
import motor as M                      # noqa: E402
from yukle import saatlik, dix_gex     # noqa: E402

VERI = M.VERI_DIZIN
Y = {k: os.path.join(VERI, f"{k}_K4b.csv") for k in
     ("aday", "sonuc", "karar", "kayma", "yol", "kapanis1530", "bugun")}
T0 = time.time()
m = M.Motor()
IDX = m.idx
GEX = dix_gex()["gex"].astype(float)
GEX.index = pd.to_datetime(GEX.index)


def log(*a):
    print(f"[{time.time() - T0:6.1f}s]", *a, flush=True)


# ============================================================================ sinyal yapi taslari
def ters(r, thr):
    """|r| >= thr ise ters yon: dususte +1, yukseliste -1."""
    return (-np.sign(r) * (r.abs() >= thr)).fillna(0).astype(int)


def ibs_sinyal(r, b, thr, lo=0.1, hi=0.9, kontrol=False):
    if kontrol:
        orta = (b >= 0.3) & (b <= 0.7)
        up, dn = (r >= thr) & orta, (r <= -thr) & orta
    else:
        up, dn = (r >= thr) & (b >= hi), (r <= -thr) & (b <= lo)
    out = up.astype(int) * -1 + dn.astype(int)
    return out.fillna(0).astype(int) if hasattr(out, "fillna") else out


def ibs(mm, k):
    c, h, lo = mm.girdi(k, "close"), mm.girdi(k, "high"), mm.girdi(k, "low")
    rg = h - lo
    return (c - lo) / rg.where(rg > 0)


def gex_kosul(idx, tip):
    g = GEX.reindex(idx).shift(1)            # GEX(t-1): kapanistan sonra yayimlanir -> t kapanisinda bilinen
    if tip == "gex<0":
        return g < 0
    if tip == "gex>0":
        return g > 0
    return g <= g.rolling(252, min_periods=126).quantile(0.2)   # 252 gunluk alt %20 (pencere t-1 degeri dahil)


def genislik_maskesi(mm):
    tab = mm.donem_basi_evreni()
    mk = mm.evren_maskesi(tab).copy()
    is_kod = [k for k in tab.loc[tab["donem"] == "IS", "kod"] if k in mm.kpos]
    stres = np.asarray(mm.idx < pd.Timestamp("2010-01-01"))
    mk.loc[stres, is_kod] = True              # STRES icin 2010 evreni (sapma; yalniz STRES/TUM/bolum satirlari)
    kol = [c for c in mk.columns if mk[c].any()]
    return mk[kol]


def genislik(mm, tip, P1530=None):
    mk = genislik_maskesi(mm)
    kol = list(mk.columns)
    ac = mm.girdi(kol, "adjclose")
    if tip == "dus":
        r = ac / ac.shift(1) - 1
        if P1530 is not None:
            r = r.where(P1530.isna(), P1530 / ac.shift(1) - 1)
        pay = ((r < 0) & mk).sum(axis=1) / ((r.notna()) & mk).sum(axis=1).replace(0, np.nan)
        return pay
    ma = ac.rolling(20, min_periods=20).mean()
    ust = ac > ma
    if P1530 is not None:
        ma2 = ma + (P1530 - ac) / 20.0
        ust = ust.where(P1530.isna(), P1530 > ma2)
    gec = ac.notna() & ma.notna()
    return (ust & mk).sum(axis=1) / (gec & mk).sum(axis=1).replace(0, np.nan)


# ============================================================================ 15:30 verisi
S60 = saatlik()
C_HAM = m.df("close", ham=True)
ADJ_ORAN = m.df("adjclose", ham=True) / C_HAM
P1530_RAW = S60["acilis_1530"].copy()
P1530_RAW.index = pd.to_datetime(P1530_RAW.index)
P1530_RAW = P1530_RAW.reindex(IDX)
P1530_RAW[pd.Series(S60["yarim_gun"]).reindex(IDX).fillna(False).to_numpy(bool)] = np.nan  # yarim gun 12:30: disarida
H60_BAS = P1530_RAW.dropna(how="all").index.min()


def r1530(k):
    if k not in P1530_RAW.columns:
        return None
    return P1530_RAW[k] / C_HAM[k].shift(1) - 1


def ibs1530(k):
    """15:30 fiyatiyla IBS; yuksek/dusuk butun gunun degeri (son 30 dk'yi icerir: sizintili yaklasim)."""
    hi, lo = m.df("high", ham=True)[k], m.df("low", ham=True)[k]
    rg = hi - lo
    return (P1530_RAW[k] - lo) / rg.where(rg > 0)


# ============================================================================ kural listesi
K = []   # her kural: id, ad, girdi, fn(mm), hedef, cok, yeni, guc_fn, tip, s1530 (fn veya None), kaynak_yil


def ekle(**kw):
    kw.setdefault("cok", False)
    kw.setdefault("yeni", False)
    kw.setdefault("guc_fn", None)
    kw.setdefault("s1530", None)
    kw.setdefault("yayin", "")
    K.append(kw)


# R3-01: |SPY| >= %2 ters yon, GEX alt orneklemleri (GEX(t-1))
for hd in ("SPY", "QQQ"):
    for gk in ("gex<0", "gex>0", "gexalt20"):
        def f(mm, gk=gk):
            return (ters(mm.girdi_getiri("SPY"), 0.02) * gex_kosul(mm.idx, gk).to_numpy()).astype(int)

        def f15(gk=gk):
            r = r1530("SPY")
            return (ters(r, 0.02) * gex_kosul(IDX, gk).to_numpy()).astype(int)
        ekle(id=f"R3-01.{hd}.{gk}", ad=f"|SPY|>=%2 ters yon, {gk} (GEX t-1)", girdi="SPY kk(t), GEX(t-1)",
             fn=f, hedef=hd, s1530=f15, yayin="2021 (JFE)")

# R3-02: kapanis konumu vekili (+ kontrol IBS 0,3-0,7)
for hd in ("SPY", "QQQ"):
    for kt in (False, True):
        def f(mm, hd=hd, kt=kt):
            return ibs_sinyal(mm.girdi_getiri(hd), ibs(mm, hd), 0.015, kontrol=kt)

        def f15(hd=hd, kt=kt):
            return ibs_sinyal(r1530(hd), ibs1530(hd), 0.015, kontrol=kt)
        ekle(id=f"R3-02.{hd}.{'kontrol' if kt else 'ana'}",
             ad=f"{hd} |r|>=%1,5 ve IBS {'0,3-0,7 (kontrol)' if kt else 'uc (>=0,9 / <=0,1)'} -> ters",
             girdi=f"{hd} kk(t), IBS(t)", fn=f, hedef=hd, s1530=f15, yayin="2026 (EOD makalesi Eylul 2026)")

# R3-03 (+R8-11 = SPY e2): kendi getirisi |r| >= e ters yon
for hd in ("SPY", "QQQ"):
    for e in (1, 2, 3, 4):
        def f(mm, hd=hd, e=e):
            return ters(mm.girdi_getiri(hd), e / 100)

        def f15(hd=hd, e=e):
            return ters(r1530(hd), e / 100)
        kid = f"R3-03.{hd}.e{e}" + ("/R8-11" if (hd == "SPY" and e == 2) else "")
        ekle(id=kid, ad=f"{hd} |r|>=%{e} -> ters yon", girdi=f"{hd} kk(t)", fn=f, hedef=hd, s1530=f15,
             yayin="CXO (2006-2011 verisi); R8-11 ayni kural")

# R3-04: tek hisse kaldiracli ETF dayanaklari +-%6 ters (yeni yapi, cok hedefli)
H4 = ["NVDA", "TSLA", "MSTR", "COIN", "AMD", "PLTR"]


def f304(mm):
    return ters(mm.girdi_getiri(H4), 0.06)


def g304(mm):
    return mm.girdi_getiri(H4).abs()


def f304_15():
    r = pd.DataFrame({k: r1530(k) for k in H4})
    return ters(r, 0.06)


ekle(id="R3-04.COK6", ad="Tek hisse (NVDA,TSLA,MSTR,COIN,AMD,PLTR) |r|>=%6 -> ters", girdi="hisse kk(t)",
     fn=f304, hedef=None, cok=True, yeni=True, guc_fn=g304, s1530=f304_15, yayin="2026 (arXiv 2608.03703)")

# Ek (a1): VIX(t-1) - RV20(t-1) z-skoru; z>esik uzun, z<-esik kisa (SPY)
for w in (60, 250):
    for zt in (1, 2):
        def f(mm, w=w, zt=zt):
            v = mm.girdi("^VIX", "close")                        # VIX(t-1)
            rv = (mm.girdi_getiri("SPY").rolling(20, min_periods=20).std() * np.sqrt(252) * 100).shift(1)
            z = M.z_skor(v - rv, w)
            return pd.Series(np.where(z > zt, 1, np.where(z < -zt, -1, 0)), index=mm.idx).astype(int)
        ekle(id=f"K4b-a1.w{w}.z{zt}", ad=f"VIX(t-1)-RV20(t-1) z({w})>{zt} uzun / <-{zt} kisa", girdi="^VIX(t-1), SPY",
             fn=f, hedef="SPY", s1530=(lambda f=f: f(m)))   # butun girdiler t-1: 15:30'da da ayni

# Ek (a2): VIXY tek gun sicramasi -> SPY uzun
for e in (10, 20):
    def f(mm, e=e):
        return (mm.girdi_getiri("VIXY") >= e / 100).astype(int)

    def f15(e=e):
        r = r1530("VIXY")
        return (r >= e / 100).astype(int) if r is not None else None
    ekle(id=f"K4b-a2.vixy{e}", ad=f"VIXY gunluk >= +%{e} -> SPY uzun", girdi="VIXY kk(t)", fn=f, hedef="SPY",
         s1530=f15)

# Ek (b): evren genisligi -> SPY uzun
for tip, e in (("ma", 10), ("ma", 20), ("dus", 90)):
    def f(mm, tip=tip, e=e):
        pay = genislik(mm, tip)
        return ((pay >= e / 100) if tip == "dus" else (pay < e / 100)).astype(int)

    def f15(tip=tip, e=e):
        mk = genislik_maskesi(m)
        P = P1530_RAW.reindex(columns=mk.columns) * ADJ_ORAN.reindex(columns=mk.columns)
        pay = genislik(m, tip, P1530=P)
        return ((pay >= e / 100) if tip == "dus" else (pay < e / 100)).astype(int)
    ad = (f"Evrenin %{e}'i ya da fazlasi dustu -> SPY uzun" if tip == "dus"
          else f"20g ort. ustundeki hisse payi < %{e} -> SPY uzun")
    ekle(id=f"K4b-b.{tip}{e}", ad=ad, girdi="donem basi evreni (150 hisse) kapanislari", fn=f, hedef="SPY",
         s1530=f15)

# Ek (c1): buyuk gun |r|>=%2 + IBS ucta -> ters (SPY, QQQ)
for hd in ("SPY", "QQQ"):
    def f(mm, hd=hd):
        return ibs_sinyal(mm.girdi_getiri(hd), ibs(mm, hd), 0.02)

    def f15(hd=hd):
        return ibs_sinyal(r1530(hd), ibs1530(hd), 0.02)
    ekle(id=f"K4b-c1.{hd}", ad=f"{hd} |r|>=%2 ve IBS ucta -> ters", girdi=f"{hd} kk(t), IBS(t)", fn=f, hedef=hd,
         s1530=f15)

# Ek (c2): tek hisse kaldiracli urun dayanaklari |r|>=%2 + IBS ucta -> ters (yeni yapi, cok hedefli)
H4c = ["NVDA", "TSLA", "MSTR", "COIN"]


def fc2(mm):
    return pd.DataFrame({k: ibs_sinyal(mm.girdi_getiri(k), ibs(mm, k), 0.02) for k in H4c})


def gc2(mm):
    return mm.girdi_getiri(H4c).abs()


def fc2_15():
    return pd.DataFrame({k: ibs_sinyal(r1530(k), ibs1530(k), 0.02) for k in H4c})


ekle(id="K4b-c2.COK4", ad="NVDA,TSLA,MSTR,COIN |r|>=%2 ve IBS ucta -> ters", girdi="hisse kk(t), IBS(t)",
     fn=fc2, hedef=None, cok=True, yeni=True, guc_fn=gc2, s1530=fc2_15)


# ============================================================================ yardimcilar
def karar_satirlari(df, donem):
    d = df[(df.korunma == "yok") & (df.komisyon == "hisse") & (df.rejim == "hepsi") & (df.donem == donem)
           & (df.giris == "K")]
    return d


def tstat(row, cok):
    return row["t_kume"] if cok else row["t_olcekli"]


def gecer(row, cok, esik=2.0):
    t = tstat(row, cok)
    ok = (row["n_islem"] > 0) and (row["net_bps"] > 0) and np.isfinite(t) and (t >= esik)
    if row["yon"] in ("uzun", "kisa"):
        ok = ok and (row["anormal_bps"] > 0) and np.isfinite(row["t_anormal"]) and (row["t_anormal"] >= 2)
    return bool(ok)


# ============================================================================ 1) sinyaller + bakis
log(f"{len(K)} kural-varyanti; bakis testi")
SIG, GUC = {}, {}
for k in K:
    s = k["fn"](m)
    tamam, rap = m.bakis_testi(k["fn"])
    assert tamam, (k["id"], rap)
    SIG[k["id"]] = s
    GUC[k["id"]] = k["guc_fn"](m) if k["guc_fn"] else None
log("bakis testi: hepsi temiz")

# ============================================================================ 2) YALNIZ IS tarama
tarama, adaylar = [], []
for k in K:
    don = ["IS2", "IS"] if k["yeni"] else ["IS"]       # yeni yapida IS (2010-2019) = ETF oncesi bilgi satiri
    d = m.degerlendir(SIG[k["id"]], k["hedef"], kural_id=k["id"], aile="D", ad=k["ad"], girdi=k["girdi"],
                      h=(1, 2, 3), giris=("K", "A"), gece=True, korunma=("yok",), komisyon=("hisse",),
                      donemler=don, rejimler=False, guc=GUC[k["id"]], bootstrap=False,
                      notlar=f"yayin={k['yayin']}" if k["yayin"] else "")
    tarama.append(d)
    kd = karar_satirlari(d, "IS2" if k["yeni"] else "IS")
    for _, r in kd.iterrows():
        if gecer(r, k["cok"]):
            adaylar.append({"kural_id": k["id"], "h": int(r["h"]), "cikis": r["cikis"], "yon": r["yon"],
                            "donem": r["donem"], "n_islem": r["n_islem"], "net_bps": r["net_bps"],
                            "anormal_bps": r["anormal_bps"], "t_olcekli": r["t_olcekli"], "t_kume": r["t_kume"],
                            "t_anormal": r["t_anormal"], "karar_olcusu": "t_kume" if k["cok"] else "t_olcekli",
                            "yeni_yapi": k["yeni"]})
TARAMA = pd.concat(tarama, ignore_index=True)
ADAY = pd.DataFrame(adaylar, columns=["kural_id", "h", "cikis", "yon", "donem", "n_islem", "net_bps",
                                      "anormal_bps", "t_olcekli", "t_kume", "t_anormal", "karar_olcusu",
                                      "yeni_yapi"])
ADAY.to_csv(Y["aday"], index=False)
n_test = sum(len(karar_satirlari(t, "IS2" if k["yeni"] else "IS")) for t, k in zip(tarama, K))
log(f"IS tarama bitti: {n_test} test, {len(ADAY)} aday -> {Y['aday']}")
print(ADAY.round(2).to_string(index=False))

# R3-11 kayma (IS, butun kurallar): Giris K - Giris A
ky = TARAMA[(TARAMA.korunma == "yok") & (TARAMA.rejim == "hepsi") & (TARAMA.cikis == "kapanis")]
ky = ky.pivot_table(index=["kural_id", "donem", "h"], columns="giris", values=["net_bps", "brut_bps", "n_islem"])
ky.columns = [f"{a}_{b}" for a, b in ky.columns]
ky = ky.reset_index()
ky["kayma_net_bps"] = ky["net_bps_K"] - ky["net_bps_A"]

# ============================================================================ 3) OOS: yalniz adaylar
TAM, ISL, KARAR = [], {}, []
aday_kural = list(dict.fromkeys(ADAY["kural_id"]))
KMAP = {k["id"]: k for k in K}
for kid in aday_kural:
    k = KMAP[kid]
    hset = set(ADAY.loc[ADAY.kural_id == kid, "h"].astype(int))
    hh = tuple(sorted(x for x in hset if x > 0)) or (1,)
    kor = ("yok",) if k["hedef"] == "SPY" else ("yok", "SPY:250", "SPY:60")
    don = ["IS", "IS2", "OOS2", "TUM"] if k["yeni"] else None
    d, isl = m.degerlendir(SIG[kid], k["hedef"], kural_id=kid, aile="D", ad=k["ad"], girdi=k["girdi"],
                           h=hh, giris=("K", "A", "G"), gece=(0 in hset), korunma=kor, komisyon=M.KOMISYONLAR,
                           donemler=don, rejimler=True, guc=GUC[kid], bootstrap=True, islem_dondur=True,
                           notlar=f"yayin={k['yayin']}" if k["yayin"] else "")
    d = d[d.h.isin(list(hset))]
    TAM.append(d)
    ISL[kid] = isl
    od = "OOS2" if k["yeni"] else "OOS"
    sd = "OOS2" if k["yeni"] else "SON"
    for h in sorted(hset):
        ck = "acilis" if h == 0 else "kapanis"
        sel = lambda dn, g="K", kr="yok", kom="hisse", rj="hepsi": d[(d.donem == dn) & (d.giris == g) & (d.h == h)
                                                                    & (d.cikis == ck) & (d.korunma == kr)
                                                                    & (d.komisyon == kom) & (d.rejim == rj)]
        o, s_, i_ = sel(od), sel(sd), sel("IS2" if k["yeni"] else "IS")
        if not len(o):
            continue
        o, s_, i_ = o.iloc[0], s_.iloc[0], i_.iloc[0]
        esik = 3.0 if k["yeni"] else 2.0
        gec = gecer(o, k["cok"], esik)
        a = sel(od, g="A") if h > 0 else pd.DataFrame()
        gG = sel(od, g="G") if h > 0 else pd.DataFrame()
        ikey = ("K", h, ck, "yok")
        _, boz = m.bolum_ozeti(isl[ikey], "hisse")
        KARAR.append({"kural_id": kid, "ad": k["ad"], "hedef": o["hedef"], "yon": o["yon"], "h": h, "cikis": ck,
                      "giris": "K", "korunma": "yok", "yeni_yapi": k["yeni"],
                      "is_net_bps": i_["net_bps"], "is_t": tstat(i_, k["cok"]),
                      "oos_net_bps": o["net_bps"], "oos_n": o["n_islem"], "oos_t": tstat(o, k["cok"]),
                      "oos_t_anormal": o["t_anormal"], "oos_anormal_bps": o["anormal_bps"],
                      "oos_p": o["p_bootstrap"] if np.isfinite(o["p_bootstrap"]) else 1.0,
                      "oos_p_wilcoxon": o["p_wilcoxon"], "oos_gecti": gec,
                      "son_net_bps": s_["net_bps"] if not k["yeni"] else np.nan,
                      "son_t": tstat(s_, k["cok"]) if not k["yeni"] else np.nan,
                      "girisA_oos_net_bps": a.iloc[0]["net_bps"] if len(a) else np.nan,
                      "girisA_oos_t": tstat(a.iloc[0], k["cok"]) if len(a) else np.nan,
                      "girisG_oos_net_bps": gG.iloc[0]["net_bps"] if len(gG) else np.nan,
                      "basabas_bps": o["basabas_bps"], "net_sigma": o["net_sigma"],
                      "yillik_net_pct": o["yillik_net_pct"], "yillik_islem": o["yillik_islem"],
                      "maliyet2x_net_bps": o["maliyet2x_net_bps"], "en_iyi5suz_bps": o["en_iyi5suz_bps"],
                      "en_iyi_aysiz_bps": o["en_iyi_aysiz_bps"], "uzun_bps": o["uzun_bps"], "kisa_bps": o["kisa_bps"],
                      "vix30_bolum": boz.get("bolum_sayisi", 0),
                      "vix30_ayni_isaret": boz.get("ayni_isaret_orani", np.nan),
                      "vix30_net_bps": boz.get("net_bps", np.nan), "vix30_destekli": boz.get("destekli", False)})
    log(f"OOS: {kid} bitti")

KARAR = pd.DataFrame(KARAR)
if len(KARAR):
    KARAR["bh_yerel_10"] = M.bh(KARAR["oos_p"].to_numpy(float), 0.10)
    ky2 = pd.concat(TAM)
    ky2 = ky2[(ky2.korunma == "yok") & (ky2.rejim == "hepsi") & (ky2.komisyon == "hisse") & (ky2.cikis == "kapanis")]
    ky2 = ky2.pivot_table(index=["kural_id", "donem", "h"], columns="giris", values=["net_bps", "brut_bps", "n_islem"])
    ky2.columns = [f"{a}_{b}" for a, b in ky2.columns]
    ky2 = ky2.reset_index()
    ky2["kayma_net_bps"] = ky2["net_bps_K"] - ky2["net_bps_A"]
    ky = pd.concat([ky, ky2[~ky2.donem.isin(["IS", "IS2"])]], ignore_index=True)
ky.to_csv(Y["kayma"], index=False)

# ============================================================================ 4) gecenler: 15:30, uygulama, komsu
EK = []
k1530 = []
GECEN = KARAR[KARAR.oos_gecti] if len(KARAR) else KARAR
UYG_ETF = {"SPY": [("SPY", "SDS"), ("UPRO", "SPXU")], "QQQ": [("QQQ", "QID"), ("TQQQ", "SQQQ")]}
for _, g in (GECEN.iterrows() if len(GECEN) else []):
    kid, h = g["kural_id"], int(g["h"])
    k = KMAP[kid]
    ck = "acilis" if h == 0 else "kapanis"
    hh = max(h, 1)
    # 15:30 kapanis gercekciligi
    s15 = k["s1530"]() if k["s1530"] else None
    if s15 is not None:
        base = SIG[kid]
        b2 = base.loc[base.index >= H60_BAS]
        s2 = s15.reindex(base.index).fillna(0).astype(int)
        s2 = s2.where(base.index >= H60_BAS, 0) if isinstance(s2, pd.Series) else s2.mul((base.index >= H60_BAS), axis=0)
        i0 = m.islemler(base.where(base.index >= H60_BAS, 0) if isinstance(base, pd.Series)
                        else base.mul((base.index >= H60_BAS), axis=0), k["hedef"], giris="K", h=hh, cikis=ck,
                        guc=GUC[kid])
        i1 = m.islemler(s2, k["hedef"], giris="K", h=hh, cikis=ck, guc=GUC[kid])
        a0 = set(zip(i0["t"], i0["hedef"]))
        a1 = set(zip(i1["t"], i1["hedef"]))
        b_ = np.asarray(b2 != 0).sum() if isinstance(b2, pd.Series) else int((b2 != 0).to_numpy().sum())
        k1530.append({"kural_id": kid, "h": h, "baslangic": str(H60_BAS.date()), "n_K": len(i0), "n_1530": len(i1),
                      "ortusme_K_icinde": len(a0 & a1) / max(len(a0), 1),
                      "brut_K_bps": i0["brut"].mean() * 1e4, "brut_1530_bps": i1["brut"].mean() * 1e4,
                      "net_K_bps": i0["net_hisse"].mean() * 1e4, "net_1530_bps": i1["net_hisse"].mean() * 1e4,
                      "koruma_net": (i1["net_hisse"].mean() / i0["net_hisse"].mean()) if len(i0) and len(i1) else np.nan,
                      "olay_30_ustu": len(i1) >= 30, "not": "IBS kurallarinda yuksek/dusuk butun gunun (sizintili)"})
    # ters/kaldiracli ETF uygulama satirlari (iki yonlu, tek hedefli SPY/QQQ kurallari)
    if k["hedef"] in UYG_ETF:
        for uz, ks in UYG_ETF[k["hedef"]]:
            s = SIG[kid]
            if uz == k["hedef"] and (s >= 0).all():
                continue
            sd = pd.DataFrame({uz: (s > 0).astype(int), ks: (s < 0).astype(int)}) if uz != ks else None
            if (s >= 0).all():
                sd = pd.DataFrame({uz: (s > 0).astype(int)})
            d = m.degerlendir(sd, None, kural_id=f"{kid}.uyg-{uz}/{ks}", aile="D", ad=k["ad"] + f" [uygulama {uz}/{ks}]",
                              girdi=k["girdi"], h=(hh,), giris=("K", "A"), gece=(h == 0), korunma=("yok",),
                              komisyon=M.KOMISYONLAR, rejimler=False, bootstrap=True,
                              notlar="uygulama satiri: uzun bacak " + uz + ", kisa sinyal " + ks + " alimi")
            EK.append(d[d.h == h])
log("gecenler: 15:30 ve uygulama satirlari bitti")

# komsu parametre (yalniz gecenler): esik +-0,5 puan, z +-0,5, pencere +-%50 -> OOS K satiri
KOMSU = []
for _, g in (GECEN.iterrows() if len(GECEN) else []):
    kid, h = g["kural_id"], int(g["h"])
    k = KMAP[kid]
    ck = "acilis" if h == 0 else "kapanis"
    varyant = []
    if kid.startswith("R3-03"):
        hd, e = k["hedef"], int(kid.split(".e")[1][0])
        for e2 in (e - 0.5, e + 0.5):
            varyant.append((f"e{e2}", ters(m.girdi_getiri(hd), e2 / 100)))
    elif kid.startswith("R3-01"):
        gk = kid.split(".")[2]
        for e2 in (1.5, 2.5):
            varyant.append((f"e{e2}", (ters(m.girdi_getiri("SPY"), e2 / 100) * gex_kosul(IDX, gk).to_numpy()).astype(int)))
    elif kid.startswith("R3-02") or kid.startswith("K4b-c1"):
        hd = k["hedef"]
        e = 0.015 if kid.startswith("R3-02") else 0.02
        for e2 in (e - 0.005, e + 0.005):
            varyant.append((f"e{e2*100:.1f}", ibs_sinyal(m.girdi_getiri(hd), ibs(m, hd), e2, kontrol="kontrol" in kid)))
    elif kid.startswith("K4b-a2"):
        e = int(kid.split("vixy")[1])
        for e2 in (e * 0.75, e * 1.25):
            varyant.append((f"vixy{e2}", (m.girdi_getiri("VIXY") >= e2 / 100).astype(int)))
    for ad, s in varyant:
        isl = m.islemler(s, k["hedef"], giris="K", h=max(h, 1), cikis=ck, guc=GUC[kid])
        od = M.donem_maskesi(IDX, "OOS")[isl["t_pos"].to_numpy()]
        x = isl.loc[od, "net_hisse"]
        KOMSU.append({"kural_id": kid, "h": h, "komsu": ad, "oos_n": len(x), "oos_net_bps": x.mean() * 1e4})
KOMSU = pd.DataFrame(KOMSU)

# ============================================================================ R8-10: kaldiracli ETF yol testi (betimsel)
ACH = m.df("adjclose", ham=True)
rj = m.rejim().copy()
r_spy = m.girdi_getiri("SPY")
vix1 = m.girdi("^VIX", "close")
olay = {"hepsi": pd.Series(True, index=IDX), "K1_SPY<=-3%": r_spy <= -0.03, "K3_VIX(t-1)>=35": vix1 >= 35,
        "K4_VIX(t-1)>=30_|SPY|>=1.5%": (vix1 >= 30) & (r_spy.abs() >= 0.015)}
CIFT = [("TQQQ", "QQQ", 3), ("SQQQ", "QQQ", -3), ("UPRO", "SPY", 3), ("SPXL", "SPY", 3), ("SPXU", "SPY", -3),
        ("SPXS", "SPY", -3), ("SOXL", "SOXX", 3), ("SOXS", "SOXX", -3)]
yol = []
for etf, u, L in CIFT:
    for h in (1, 2, 3):
        re = ACH[etf].shift(-h) / ACH[etf] - 1
        ru = ACH[u].shift(-h) / ACH[u] - 1
        sap = (re - L * ru)
        ok = sap.notna() & (IDX >= pd.Timestamp("2010-03-15"))
        for on, om in olay.items():
            for kv in ["hepsi"] + M.VIX_KOVA_AD:
                sel = ok & om.fillna(False) & ((rj["vix_kova"] == kv) if kv != "hepsi" else True)
                x = sap[sel] * 1e4
                if len(x) < 5:
                    continue
                yol.append({"etf": etf, "dayanak": u, "kaldirac": L, "h": h, "olay": on, "vix_kova": kv, "n": len(x),
                            "ort_sapma_bps": x.mean(), "medyan_sapma_bps": x.median(), "p05_bps": x.quantile(0.05),
                            "p95_bps": x.quantile(0.95), "ort_abs_bps": x.abs().mean(),
                            "dayanak_abs_ort_bps": (L * ru[sel]).abs().mean() * 1e4})
YOL = pd.DataFrame(yol)
# ek kural: K1 gunu UPRO/TQQQ uzun, h=3; dayanak kapanisi giris kapanisinin %3 altina inerse o kapanista cik (brut)
dur = []
for etf, u in (("UPRO", "SPY"), ("TQQQ", "QQQ"), ("SOXL", "SOXX")):
    t_ = np.flatnonzero((olay["K1_SPY<=-3%"].fillna(False) & (IDX >= pd.Timestamp("2010-03-15"))).to_numpy())
    t_ = t_[t_ + 3 < len(IDX)]
    E, U = ACH[etf].to_numpy(), ACH[u].to_numpy()
    duz, stop = [], []
    for t in t_:
        duz.append(E[t + 3] / E[t] - 1)
        c = 3
        for j in (1, 2):
            if U[t + j] < 0.97 * U[t]:
                c = j
                break
        stop.append(E[t + c] / E[t] - 1)
    duz, stop = np.array(duz), np.array(stop)
    okm = np.isfinite(duz) & np.isfinite(stop)
    dur.append({"etf": etf, "dayanak": u, "kaldirac": 3, "h": 3, "olay": "K1 + %3 stop", "vix_kova": "hepsi",
                "n": int(okm.sum()), "ort_sapma_bps": (stop[okm] - duz[okm]).mean() * 1e4,
                "medyan_sapma_bps": np.median(stop[okm] - duz[okm]) * 1e4,
                "p05_bps": duz[okm].mean() * 1e4, "p95_bps": stop[okm].mean() * 1e4,
                "ort_abs_bps": np.nan, "dayanak_abs_ort_bps": np.nan})
YOL = pd.concat([YOL, pd.DataFrame(dur)], ignore_index=True)
YOL.to_csv(Y["yol"], index=False)

# ============================================================================ bugun (20.11.2026) ve 23.11 tetikleri
son = IDX[-1]
bg = []
for k in K:
    s = SIG[k["id"]]
    v = s.loc[son] if isinstance(s, pd.Series) else s.loc[son].to_dict()
    bg.append({"kural_id": k["id"], "sinyal_20_11": str(v)})
BUGUN = pd.DataFrame(bg)
c_ = C_HAM.loc[son]
dur_bilgi = {"SPY_kapanis": c_["SPY"], "QQQ_kapanis": c_["QQQ"],
             "SPY_r": r_spy.loc[son], "QQQ_r": m.girdi_getiri("QQQ").loc[son],
             "SPY_IBS": ibs(m, "SPY").loc[son], "QQQ_IBS": ibs(m, "QQQ").loc[son],
             "VIXY_r": m.girdi_getiri("VIXY").loc[son], "VIXY_kapanis": c_["VIXY"],
             "GEX_20_11": GEX.reindex(IDX).loc[son], "GEX_19_11": GEX.reindex(IDX).shift(1).loc[son],
             "genislik_ma20": genislik(m, "ma").loc[son], "genislik_dus": genislik(m, "dus").loc[son],
             "VIX_19_11": vix1.loc[son]}
for k_, v_ in dur_bilgi.items():
    BUGUN = pd.concat([BUGUN, pd.DataFrame([{"kural_id": "_durum_" + k_, "sinyal_20_11": f"{v_:.4f}"}])])
BUGUN.to_csv(Y["bugun"], index=False)

# ============================================================================ yaz
out = [TARAMA[~TARAMA.kural_id.isin(aday_kural)]] + TAM + EK
SON = pd.concat(out, ignore_index=True)
M.yaz_sonuc(SON, Y["sonuc"])
if len(KARAR):
    KARAR.to_csv(Y["karar"], index=False)
pd.DataFrame(k1530).to_csv(Y["kapanis1530"], index=False)
if len(KOMSU):
    KOMSU.to_csv(os.path.join(VERI, "komsu_K4b.csv"), index=False)
log(f"yazildi: {SON.shape} satir -> {Y['sonuc']}")
pd.set_option("display.width", 250)
print("\n== KARAR ==")
if len(KARAR):
    print(KARAR[["kural_id", "h", "yon", "is_net_bps", "is_t", "oos_net_bps", "oos_n", "oos_t", "oos_t_anormal", "oos_p",
                 "oos_gecti", "son_net_bps", "son_t", "girisA_oos_net_bps", "girisA_oos_t", "basabas_bps",
                 "vix30_bolum", "vix30_ayni_isaret"]].round(2).to_string(index=False))
print("\n== 15:30 ==")
print(pd.DataFrame(k1530).round(2).to_string(index=False) if k1530 else "yok")
print("\n== KOMSU ==")
print(KOMSU.round(1).to_string(index=False) if len(KOMSU) else "yok")
print("\n== BUGUN ==")
print(BUGUN.to_string(index=False))
log("bitti")
