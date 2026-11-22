# -*- coding: utf-8 -*-
"""aile_K9.py - Aile N (gece-gunduz) + R7-10 (satis gunu sonrasi kosullu gece donusu) + risk/boyut tablosu.
Calistirma (tek komut):  python3 -I aile_K9.py            (butun asamalar)
                          python3 -I aile_K9.py risk       (yalniz risk/boyut tablosu)
Sira (YONTEM 7, gorev K9): 1) sinyaller -> 2) YALNIZ IS tarama -> aday_K9.csv (OOS'a bakmadan once)
-> 3) OOS yalniz adaylar -> 4) OOS'tan gecenler icin tam satirlar, Giris A/G, rejim, VIX>30 bolumleri,
saglamlik, 15:30 kapanis gercekciligi -> 5) betimleyici gece/gunduz kirilimi -> 6) risk/boyut tablosu.
Cikti: ../veri/sonuc_K9.csv (motor SEMA), ../veri/aday_K9.csv, ../veri/ozet_K9.csv,
       ../veri/risk_ve_boyut_tablosu.csv. Ham veri depoya yazilmaz."""
import os
import sys
import time

import numpy as np
import pandas as pd

KOD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOD)
import motor as M                     # noqa: E402
from motor import Motor, yaz_sonuc, VERI_DIZIN, SEMA   # noqa: E402

SONUC = os.path.join(VERI_DIZIN, "sonuc_K9.csv")
ADAY = os.path.join(VERI_DIZIN, "aday_K9.csv")
OZET = os.path.join(VERI_DIZIN, "ozet_K9.csv")
RISK = os.path.join(VERI_DIZIN, "risk_ve_boyut_tablosu.csv")
T0 = time.time()


def log(*a):
    print(f"[{time.time() - T0:6.1f}s]", *a, flush=True)


m = Motor()
EV = m.evren
VAR = lambda k: k in m.kpos      # noqa: E731

GENIS = [k for k in ["SPY", "QQQ", "IWM", "DIA"] if VAR(k)]
SEKTOR = [k for k in ["XLK", "XLF", "XLE", "XLV", "XLY", "XLP", "XLI", "XLB", "XLU", "XLRE", "XLC"] if VAR(k)]
KALD = [k for k in ["TQQQ", "SQQQ", "UPRO", "SPXU", "SPXL", "SPXS", "SOXL", "SOXS", "TNA", "TZA",
                    "TECL", "TECS", "FAS", "FAZ", "LABU", "LABD"] if VAR(k)]
YY = [k for k in ["NVDL", "TSLL", "CONL", "MSTU", "MSTX", "BITX", "IBIT"] if VAR(k)]
TEMA_GRUP = ["h_ai_altyapi", "h_kripto", "h_kuantum", "h_elektrik_nukleer", "h_uzay_savunma", "h_meme",
             "h_gunes", "h_ev_cin"]
TEMA = [k for k in m.kodlar if str(EV.at[k, "tur"]) == "hisse" and str(EV.at[k, "grup"]) in TEMA_GRUP]
EVT = m.donem_basi_evreni()
HISSE = sorted(set(EVT["kod"]) & set(m.kodlar))
EVM = m.evren_maskesi(EVT)[HISSE].to_numpy()
R710_HEDEF = ["SPY", "QQQ", "SPXL", "TQQQ"]
IBS_ESIK = 0.2          # "kapanis gunun dibine yakin": IBS <= 0,2 (kuralda sayi yok; onceden sabit secildi)


# ----------------------------------------------------------------------------- sinyaller
def s_hep(kod):
    def f(mm):
        c = mm.girdi(kod, "close")
        return pd.Series(np.isfinite(c.to_numpy()).astype(int), index=mm.idx)
    return f


def s_hep_cok(kodlar, maske=None):
    def f(mm):
        c = mm.girdi(kodlar, "close").to_numpy()
        s = np.isfinite(c).astype(int)
        if maske is not None:
            s = s * maske
        return pd.DataFrame(s, index=mm.idx, columns=kodlar)
    return f


def s_spy(esik, yon, ibs=None):
    """R7-10: SPY kk getirisi <= esik (yon=+1) ya da >= esik (yon=-1); ibs: SPY IBS <= ibs ek sarti."""
    def f(mm):
        r = mm.girdi_getiri("SPY")
        k = (r <= esik) if yon > 0 else (r >= esik)
        if ibs is not None:
            c, hi, lo = mm.girdi("SPY", "close"), mm.girdi("SPY", "high"), mm.girdi("SPY", "low")
            ib = (c - lo) / (hi - lo).where(hi > lo)
            k = k & (ib <= ibs)
        return (k.astype(int) * yon).astype(int)
    return f


def s_kendi_z(kodlar, W, esik, maske=None):
    def f(mm):
        r = mm.girdi_getiri(kodlar)
        z = M.z_skor(r, W)
        s = (z < -esik).astype(int).to_numpy()
        if maske is not None:
            s = s * maske
        return pd.DataFrame(s, index=mm.idx, columns=kodlar)
    return f


def g_kendi_z(kodlar, W):
    def f(mm):
        return -M.z_skor(mm.girdi_getiri(kodlar), W)
    return f


# Kural tanimlari: (kural_id, ad, girdi, sinyal_fn, hedefler(list: tek hedefli kosular / str 'COK'),
#                   cok_kodlar, guc_fn, cikislar, hat, yayin, notlar)
KURALLAR = []
for k in GENIS + SEKTOR + KALD:
    KURALLAR.append(dict(id="N1", ad="Kosulsuz gece: kapanista al, acilista sat", girdi=f"{k} (sinyal her gun)",
                         fn=s_hep(k), hedef=k, guc=None, mod="gece", hat="ana", yayin="",
                         grup="kaldirac" if k in KALD else ("sektor" if k in SEKTOR else "genis")))
KURALLAR.append(dict(id="N1-HISSE", ad="Kosulsuz gece, donem basi 150 hisse havuzu",
                     girdi="donem basi evreni (sinyal her gun)", fn=s_hep_cok(HISSE, EVM), hedef=HISSE,
                     guc=None, mod="gece", hat="ana", yayin="", grup="hisse"))
KURALLAR.append(dict(id="N1-TEMA", ad="Kosulsuz gece, tema hisseleri havuzu", girdi="tema hisseleri (her gun)",
                     fn=s_hep_cok(TEMA), hedef=TEMA, guc=None, mod="gece", hat="ana", yayin="", grup="tema"))
if YY:
    KURALLAR.append(dict(id="N1-YY", ad="Kosulsuz gece, 2020 sonrasi kaldiracli tek hisse/kripto ETF havuzu",
                         girdi=",".join(YY), fn=s_hep_cok(YY), hedef=YY, guc=None, mod="gece", hat="yy",
                         yayin="", grup="yy"))
R710 = [("R7-10a", "SPY kk <= -%1,5 -> uzun (onceden yazili)", -0.015, 1, None),
        ("R7-10b", "SPY kk <= -%2,5 -> uzun (onceden yazili)", -0.025, 1, None),
        ("R7-10s", "SPY kk >= +%1,5 -> kisa (simetrik kontrol, onceden yazili)", 0.015, -1, None),
        ("R7-10c", "SPY kk <= -%1 -> uzun (gorev metni)", -0.01, 1, None),
        ("R7-10d", "SPY kk <= -%2 -> uzun (gorev metni)", -0.02, 1, None),
        ("R7-10e", f"SPY kk <= -%1 ve IBS <= {IBS_ESIK} -> uzun (gorev metni)", -0.01, 1, IBS_ESIK)]
for kid, ad, e, y, ib in R710:
    for k in R710_HEDEF:
        if VAR(k):
            KURALLAR.append(dict(id=kid, ad=ad, girdi="SPY kk getiri (t)" + (", SPY IBS (t)" if ib else ""),
                                 fn=s_spy(e, y, ib), hedef=k, guc=None, mod="kural", hat="ana",
                                 yayin="2020 (NY Fed SR917; yayin sonrasi: 2021+)", grup="r710"))
for ad_g, kods, msk in (("SEKTOR", SEKTOR, None), ("HISSE", HISSE, EVM), ("TEMA", TEMA, None)):
    for W in (60, 250):
        for e in (1.0, 2.0):
            KURALLAR.append(dict(id=f"N3-{ad_g}-z{int(e)}-{W}",
                                 ad=f"Kendi gunluk getirisi z({W}) < -{e:g} -> uzun, {ad_g.lower()} havuzu",
                                 girdi=f"hedefin kendi kk getirisi z-skoru ({W} gun)", fn=s_kendi_z(kods, W, e, msk),
                                 hedef=kods, guc=g_kendi_z(kods, W), mod="kural", hat="ana", yayin="",
                                 grup=ad_g.lower()))


def cok(kr):
    return not isinstance(kr["hedef"], str)


def hedef_ad(kr):
    return kr["hedef"] if not cok(kr) else f"COK({len(kr['hedef'])})"


def sinyal_al(kr, mm=None):
    mm = mm or m
    s = kr["fn"](mm)
    if not cok(kr):
        s = s.rename(kr["hedef"])
    g = kr["guc"](mm) if kr["guc"] else None
    return s, g


def deg(kr, **kw):
    s, g = sinyal_al(kr)
    hed = kr["hedef"]
    base = dict(kural_id=kr["id"], aile="N" if kr["id"].startswith("N") else "D", ad=kr["ad"],
                girdi=kr["girdi"], guc=g, notlar=(f"yayin={kr['yayin']}" if kr["yayin"] else "")
                + ("; hat=yeni_yapi" if kr["hat"] == "yy" else ""))
    base.update(kw)
    return m.degerlendir(s if not cok(kr) else s, hed if not cok(kr) else None, **base)


def anahtar_t(r, kr):
    return r["t_kume"] if cok(kr) else r["t_olcekli"]


# ----------------------------------------------------------------------------- asamalar
def asama_bakis():
    """Her ayri sinyal islevi icin ileriye bakma testi (ayni islev tekrarlanmaz)."""
    goruldu, sonuc = set(), []
    for kr in KURALLAR:
        anahtar = (kr["id"], kr["girdi"]) if kr["id"] != "N1" else ("N1", "tek")
        if anahtar in goruldu:
            continue
        goruldu.add(anahtar)
        tamam, rap = m.bakis_testi(kr["fn"])
        sonuc.append((kr["id"], tamam))
        assert tamam, (kr["id"], rap)
    log(f"bakis_testi: {len(sonuc)} sinyal islevi, hepsi temiz")
    return len(sonuc)


def asama_is():
    satir, tum = [], []
    for kr in KURALLAR:
        dn = ["IS2"] if kr["hat"] == "yy" else ["IS"]
        if kr["mod"] == "gece":
            r = deg(kr, h=(1,), giris=("A",), gece=True, korunma="yok", komisyon="hisse", donemler=dn,
                    rejimler=False)
        else:
            r = deg(kr, h=(1, 2, 3), giris=("K", "A") if kr["grup"] == "r710" else ("K",), gece=True,
                    korunma="yok", komisyon="hisse", donemler=dn, rejimler=False)
            if kr["grup"] == "r710":
                r = r[(r.giris == "K") | (r.h == 1)]          # A yalniz h=1 (gunduz ayristirmasi)
        tum.append(r)
        for _, x in r.iterrows():
            uygun_test = x["giris"] == "K"                    # A (gunduz) satirlari ayristirma, aday olamaz
            tt = anahtar_t(x, kr)
            aday = bool(uygun_test and x["n_islem"] > 0 and x["net_bps"] > 0 and tt >= 2
                        and x["anormal_bps"] > 0 and x["t_anormal"] >= 2)
            satir.append(dict(kural_id=kr["id"], hedef=x["hedef"], grup=kr["grup"], hat=kr["hat"],
                              cok=cok(kr), giris=x["giris"], cikis=x["cikis"], h=x["h"],
                              test_sayilir=uygun_test, n_islem=x["n_islem"], net_bps=x["net_bps"],
                              anormal_bps=x["anormal_bps"], t_olcekli=x["t_olcekli"], t_kume=x["t_kume"],
                              t_anormal=x["t_anormal"], aday=aday, _kr=KURALLAR.index(kr)))
    T = pd.DataFrame(satir)
    T[T.aday].drop(columns=["_kr"]).to_csv(ADAY, index=False)
    log(f"IS tarama: {int(T.test_sayilir.sum())} test (+{int((~T.test_sayilir).sum())} gunduz ayristirma satiri),"
        f" {int(T.aday.sum())} aday -> {ADAY}")
    return T, pd.concat(tum, ignore_index=True)


def asama_oos(T):
    sat, tum = [], []
    for _, a in T[T.aday].iterrows():
        kr = KURALLAR[a["_kr"]]
        dn = ["OOS2"] if kr["hat"] == "yy" else ["OOS"]
        if a["cikis"] == "acilis":
            r = deg(kr, h=(1,), giris=(), gece=True, korunma="yok", komisyon="hisse", donemler=dn,
                    rejimler=False, bootstrap=True)
        else:
            r = deg(kr, h=(int(a["h"]),), giris=("K",), gece=False, korunma="yok", komisyon="hisse",
                    donemler=dn, rejimler=False, bootstrap=True)
        x = r.iloc[0]
        tt = anahtar_t(x, kr)
        esik = 3.0 if kr["hat"] == "yy" else 2.0
        gec = bool(x["n_islem"] > 0 and x["net_bps"] > 0 and tt >= esik and x["anormal_bps"] > 0
                   and x["t_anormal"] >= 2)
        p = x["p_bootstrap"] if np.isfinite(x["p_bootstrap"]) else 1.0
        sat.append(dict(a.drop(["_kr"]).to_dict(), oos_n=x["n_islem"], oos_net_bps=x["net_bps"],
                        oos_anormal_bps=x["anormal_bps"], oos_t=tt, oos_t_anormal=x["t_anormal"],
                        oos_p=p, oos_p_wilcoxon=x["p_wilcoxon"], oos_gecti=gec, _kr=a["_kr"]))
        tum.append(r)
    O = pd.DataFrame(sat)
    if len(O):
        red, q = M.bh(O["oos_p"].to_numpy(), 0.10)
        O["bh_aile_ici_q"] = q
    log(f"OOS: {len(O)} aday, {int(O.oos_gecti.sum()) if len(O) else 0} gecti")
    return O, (pd.concat(tum, ignore_index=True) if tum else None)


def saatlik_kontrol(kr, cikis, h):
    """YONTEM 4(b): son ~730 gun, sinyal 15:30 fiyatiyla; tetik ortusmesi ve Giris K kazancinin korunan payi."""
    from yukle import saatlik
    S = saatlik()
    p15 = S["acilis_1530"]
    hed = [kr["hedef"]] if not cok(kr) else list(kr["hedef"])
    gunler = p15.index.intersection(m.idx)
    i0 = int(m.idx.searchsorted(gunler.min()))
    kapo = pd.DataFrame(m.A["close"], index=m.idx, columns=m.kodlar).shift(1)
    if kr["grup"] == "r710":
        if "SPY" not in p15.columns:
            return {"not": "SPY saatlik yok"}
        r15 = (p15["SPY"] / kapo["SPY"].reindex(p15.index) - 1).reindex(m.idx)
        esik, yon = [(e, y) for kid, _, e, y, _ in R710 if kid == kr["id"]][0]
        k = (r15 <= esik) if yon > 0 else (r15 >= esik)
        s15 = pd.Series((k.fillna(False).astype(int) * yon).to_numpy(), index=m.idx).rename(kr["hedef"])
        notu = "IBS 15:30'da hesaplanamaz (gun ici yuksek/dusuk yok); yalniz getiri sarti" if "e" == kr["id"][-1] else ""
    else:
        W, e = int(kr["id"].split("-")[-1]), float(kr["id"].split("-z")[1].split("-")[0])
        r = m.girdi_getiri(hed)
        mu = r.rolling(W, min_periods=max(5, W // 2)).mean().shift(1)
        sd = r.rolling(W, min_periods=max(5, W // 2)).std().shift(1)
        r15 = (p15.reindex(columns=hed) / kapo[hed].reindex(p15.index) - 1).reindex(m.idx)
        z15 = (r15 - mu) / sd.where(sd > 0)
        s15 = (z15 < -e).astype(int)
        if kr["grup"] == "hisse":
            s15 = s15 * EVM
        notu = ""
    s0, g = sinyal_al(kr)
    pen = np.zeros(m.T, bool)
    pen[i0:] = True
    if cok(kr):
        s0 = s0.where(pen[:, None], 0)
        s15 = s15.where(pen[:, None], 0).astype(int)
    else:
        s0 = s0.where(pen, 0)
        s15 = s15.where(pen, 0).astype(int)
    a0, a1 = np.asarray(s0) != 0, np.asarray(s15) != 0
    ortus = (a0 & a1).sum() / max(a0.sum(), 1)
    i_0 = m.islemler(s0, kr["hedef"] if not cok(kr) else None, giris="K", h=h, cikis=cikis, guc=g)
    i_1 = m.islemler(s15, kr["hedef"] if not cok(kr) else None, giris="K", h=h, cikis=cikis,
                     guc=(-z15 if not kr["grup"] == "r710" else None))
    n0, n1 = i_0["net_hisse"].mean(), i_1["net_hisse"].mean()
    return {"tetik_K": int(a0.sum()), "tetik_1530": int(a1.sum()), "ortusme": float(ortus),
            "n_isl_K": len(i_0), "n_isl_1530": len(i_1), "net_K_bps": n0 * 1e4, "net_1530_bps": n1 * 1e4,
            "koruma": float(n1 / n0) if n0 and np.isfinite(n0) and n0 > 0 else np.nan, "not": notu}


def asama_ayrinti(O):
    tum, ek = [], []
    for _, o in O[O.oos_gecti].iterrows():
        kr = KURALLAR[o["_kr"]]
        dn = list(M.YENI_YAPI) if kr["hat"] == "yy" else None
        kor = ("yok", "SPY:250", "SPY:60")      # hedef SPY ise motor korunmali satiri kendisi atlar
        r, isl = deg(kr, h=(1, 2, 3), giris=("K", "A", "G"), gece=True, korunma=kor, donemler=dn,
                     rejimler=True, bootstrap=True, islem_dondur=True)
        tum.append(r)
        hh = 0 if o["cikis"] == "acilis" else int(o["h"])
        tab, oz = m.bolum_ozeti(isl[("K", hh, o["cikis"], "yok")], "hisse")
        try:
            sk = saatlik_kontrol(kr, o["cikis"], max(hh, 1))
        except Exception as e:      # noqa: BLE001
            sk = {"not": f"saatlik hata: {e}"}
        ek.append(dict(_kr=o["_kr"], hedef=o["hedef"], cikis=o["cikis"], h=o["h"], bolum=oz, saatlik=sk))
    return (pd.concat(tum, ignore_index=True) if tum else None), ek


def asama_betimleme():
    """Gece / gunduz kirilimi: N1 tek hedefli kodlar ve havuzlar, butun donemler ve rejimler (betimleyici)."""
    tum = []
    for kr in KURALLAR:
        if kr["mod"] != "gece":
            continue
        dn = list(M.YENI_YAPI) + ["TUM"] if kr["hat"] == "yy" else None
        tum.append(deg(kr, h=(1,), giris=("A",), gece=True, korunma="yok", donemler=dn,
                       rejimler=not cok(kr), komisyon=("hisse",) if cok(kr) else M.KOMISYONLAR))
    return pd.concat(tum, ignore_index=True)


def gece_ozeti():
    """NY Fed iddiasi ve yuksek VIX payi: brut gece / gunduz ortalamalari (bps/gun), alt donemlere gore."""
    g = m.ileri("K", 1, "acilis", GENIS + KALD[:6]) * 1e4
    d = m.ileri("A", 1, "kapanis", GENIS + KALD[:6]) * 1e4
    kk = m.ileri("K", 1, "kapanis", GENIS + KALD[:6]) * 1e4
    rj = m.rejim()
    out = []
    for ad, a, b in (("2010-2020", "2010-01-01", "2020-12-31"), ("2021-2026", "2021-01-01", "2026-11-20"),
                     ("2024-2026", "2024-01-01", "2026-11-20")):
        ms = (m.idx >= a) & (m.idx <= b)
        for v in (None, 0, 1, 2):
            mv = ms if v is None else ms & (rj["kova_no"].to_numpy() == v)
            for k in g.columns:
                out.append(dict(alt_donem=ad, vix=("hepsi" if v is None else M.VIX_KOVA_AD[v]), kod=k,
                                n=int(np.isfinite(g[k][mv]).sum()), gece_bps=g[k][mv].mean(),
                                gunduz_bps=d[k][mv].mean(), kk_bps=kk[k][mv].mean(),
                                gece_t=g[k][mv].mean() / (g[k][mv].std() / np.sqrt(np.isfinite(g[k][mv]).sum())),
                                gece_sd=g[k][mv].std(), gunduz_sd=d[k][mv].std()))
    return pd.DataFrame(out)


def bugun(O):
    """20.11.2026 kapanisinda sinyal durumu ve 23.11 icin tetik seviyeleri (R7-10 hepsi + gecen N3)."""
    son = m.idx[-1]
    c = m.A["close"][:, m.kpos["SPY"]]
    r = m.girdi_getiri("SPY")
    hi, lo = m.A["high"][-1, m.kpos["SPY"]], m.A["low"][-1, m.kpos["SPY"]]
    ibs = (c[-1] - lo) / (hi - lo)
    sat = [f"SPY {son.date()} kapanis {c[-1]:.2f}, gunluk getiri {r.iloc[-1] * 100:.2f}%, IBS {ibs:.2f}, "
           f"VIX(20.11) {m.A['close'][-1, m.kpos['^VIX']]:.1f}"]
    for kid, ad, e, y, ib in R710:
        acik = (r.iloc[-1] <= e) if y > 0 else (r.iloc[-1] >= e)
        if ib:
            acik = acik and ibs <= ib
        sat.append(f"{kid}: 20.11 sinyal {'ACIK' if acik else 'kapali'}; 23.11 tetik: SPY kapanis "
                   f"{'<=' if y > 0 else '>='} {c[-1] * (1 + e):.2f}" + (f" ve IBS <= {ib}" if ib else ""))
    if O is not None and len(O):
        for _, o in O[O.oos_gecti].iterrows():
            kr = KURALLAR[o["_kr"]]
            if kr["grup"] == "r710":
                continue
            s, g = sinyal_al(kr)
            acik = [k for k in s.columns if s[k].iloc[-1] != 0]
            W, e = int(kr["id"].split("-")[-1]), float(kr["id"].split("-z")[1].split("-")[0])
            rr = m.girdi_getiri(list(s.columns))
            mu, sd = rr.iloc[-W:].mean(), rr.iloc[-W:].std()
            esik = (mu - e * sd)
            cc = pd.Series(m.A["close"][-1, [m.kpos[k] for k in s.columns]], index=s.columns)
            sev = (cc * (1 + esik)).round(2)
            sat.append(f"{kr['id']}: 20.11 acik {len(acik)} kod {acik[:12]}; 23.11 tetik seviyesi (ilk 8): "
                       + ", ".join(f"{k}<={sev[k]}" for k in list(sev.index)[:8]))
    return sat


# ----------------------------------------------------------------------------- siniflama
def sinifla(o, R, ek):
    """YONTEM 9'a gore oneri. R: o kuralin tam satirlari; ek: bolum/saatlik."""
    if not o.get("aday", False):
        return "ELENDI", "IS'te aday olmadi"
    if not o.get("oos_gecti", False):
        same = o["oos_net_bps"] > 0
        if same and o["oos_t"] > 0:
            return "DUSUK", f"OOS ayni yon ama t={o['oos_t']:.2f} (<2) ya da anormal t yetersiz"
        return "ELENDI", f"OOS'ta isaret/t tutmadi (net {o['oos_net_bps']:.1f} bps, t {o['oos_t']:.2f})"
    hh = 0 if o["cikis"] == "acilis" else int(o["h"])
    base = R[(R.h == hh) & (R.cikis == o["cikis"]) & (R.korunma == "yok") & (R.komisyon == "hisse")
             & (R.rejim == "hepsi")]
    gk = base[base.giris == "K"].set_index("donem")
    eksik = []
    son = gk.loc["SON"] if "SON" in gk.index else (gk.loc["OOS2"] if "OOS2" in gk.index else None)
    tk = "t_kume" if o["cok"] else "t_olcekli"
    if o["oos_t"] < 2.5:
        eksik.append("OOS t<2,5")
    if o["oos_n"] < 30:
        eksik.append("az olay")
    if not (o["oos_p"] < 0.05 and o["oos_p_wilcoxon"] < 0.05):
        eksik.append("bootstrap/Wilcoxon p>=0,05")
    if son is None or not (son["net_bps"] > 0 and son[tk] >= 1.0):
        eksik.append("son donem zayif")
    a = base[(base.giris == "A") & (base.donem == "OOS")]
    if o["cikis"] == "acilis" or len(a) == 0 or not (a["net_bps"].iloc[0] > 0 and a[tk].iloc[0] >= 1.5):
        eksik.append("Giris A tutmuyor (D ailesinde zorunlu)")
    oos = gk.loc["OOS"] if "OOS" in gk.index else None
    if oos is not None:
        if not (oos["basabas_bps"] >= 3 * (oos["brut_bps"] - oos["net_bps"]) / 2 and oos["net_bps"] >= 10
                and oos["net_sigma"] >= 0.10):
            eksik.append("ekonomik taban")
        if not (oos["en_iyi5suz_bps"] > 0 and oos["maliyet2x_net_bps"] > 0):
            eksik.append("saglamlik")
    eksik.append("bagimsiz kod yok")
    if o["grup"] == "tema":
        return "DUSUK", "tema sinifi"
    return "KOSULLU", "; ".join(eksik)


# ----------------------------------------------------------------------------- risk / boyut tablosu
def risk_tablosu():
    T, son = m.T, m.T - 1
    ac, ao, cl = m.A["adjclose"], m.A["adjopen"], m.A["close"]
    dv = pd.DataFrame(cl * m.A["volume"]).rolling(60, min_periods=60).mean().to_numpy()[son]
    ok = [k for k in m.kodlar if m.sinif.get(k) == "ABD16" and np.isfinite(EV.at[k, "maliyet_bps"])
          and dv[m.kpos[k]] >= 100e6]
    kp = np.array([m.kpos[k] for k in ok])
    A = pd.DataFrame(ac[:, kp], index=m.idx, columns=ok)
    R1 = A / A.shift(1) - 1
    R2, R3 = A / A.shift(2) - 1, A / A.shift(3) - 1
    G = pd.DataFrame(ao[:, kp], index=m.idx, columns=ok) / A.shift(1) - 1
    I = A / pd.DataFrame(ao[:, kp], index=m.idx, columns=ok) - 1
    F1, F3 = A.shift(-1) / A - 1, A.shift(-3) / A - 1
    spy = R1["SPY"]
    vix = pd.Series(cl[:, m.kpos["^VIX"]], index=m.idx)
    v30 = (vix > 30).to_numpy()
    s10 = (m.idx >= "2010-01-01")

    def beta(n):
        x, y = spy.iloc[-n:], R1.iloc[-n:]
        return y.apply(lambda c: c.cov(x) / x.var())
    rows = pd.DataFrame(index=ok)
    rows["grup"] = [EV.at[k, "grup"] for k in ok]
    rows["tur"] = [EV.at[k, "tur"] for k in ok]
    rows["adv60_musd"] = (dv[kp] / 1e6).round(0)
    rows["fiyat"] = cl[son, kp].round(2)
    rows["kaldirac"] = [EV.at[k, "kaldirac"] for k in ok]
    rows["dayanak"] = [EV.at[k, "dayanak"] if isinstance(EV.at[k, "dayanak"], str) else "" for k in ok]
    rows["beta_spy_250"], rows["beta_spy_60"] = beta(250).round(3), beta(60).round(3)
    rows["beta_isaret_degisti"] = np.sign(rows.beta_spy_250) != np.sign(rows.beta_spy_60)
    for nm, X in (("1g", R1), ("2g", R2), ("3g", R3)):
        rows[f"sigma_{nm}_60_pct"] = (X.iloc[-60:].std() * 100).round(3)
        rows[f"sigma_{nm}_250_pct"] = (X.iloc[-250:].std() * 100).round(3)
    for nm, X in (("1g", F1), ("3g", F3)):
        x10, xv = X[s10], X[v30]
        rows[f"q01_{nm}_2010_pct"] = (x10.quantile(0.01) * 100).round(2)
        rows[f"q99_{nm}_2010_pct"] = (x10.quantile(0.99) * 100).round(2)
        rows[f"q01_{nm}_vix30_pct"] = (xv.quantile(0.01) * 100).round(2)
        rows[f"q99_{nm}_vix30_pct"] = (xv.quantile(0.99) * 100).round(2)
        rows[f"n_{nm}_vix30"] = xv.notna().sum()
    for n in (250,):
        vg, vi = G.iloc[-n:].var(), I.iloc[-n:].var()
        rows[f"gece_var_payi_{n}"] = (vg / (vg + vi)).round(3)
    vg, vi = G[s10].var(), I[s10].var()
    rows["gece_var_payi_2010"] = (vg / (vg + vi)).round(3)
    rows["en_kotu_1g_pct"] = (R1.min() * 100).round(2)
    rows["en_kotu_1g_tarih"] = R1.idxmin().dt.date.astype(str)
    rows["en_kotu_3g_pct"] = (R3.min() * 100).round(2)
    rows["en_kotu_3g_bitis"] = R3.idxmin().dt.date.astype(str)
    rows["veri_baslangic"] = A.apply(lambda c: c.first_valid_index()).dt.date.astype(str)
    kad = m.kademe()
    kad = (kad.to_numpy() if hasattr(kad, "to_numpy") else kad)[son, kp]
    px = cl[son, kp]
    kom = np.maximum(1.0, 0.005 * 10000 / px) / 10000 * 1e4
    bacak = np.maximum(np.maximum(kad, EV.loc[ok, "maliyet_bps"].to_numpy()), 0.005 / px * 1e4) + kom
    rows["maliyet_kademe_bps"] = np.maximum(kad, EV.loc[ok, "maliyet_bps"].to_numpy())
    rows["bacak_bps_hisse_kom"] = bacak.round(2)
    rows["gidis_donus_bps"] = (2 * bacak).round(2)
    # korelasyon kumesi (son 250 gun, |rho| >= 0,7; tam baglanti: kumede her cift >= 0,7)
    C = R1.iloc[-250:].corr(min_periods=120).abs().to_numpy()
    C = np.where(np.isfinite(C), C, 0.0)
    np.fill_diagonal(C, 1.0)
    kume = [[i] for i in range(len(ok))]
    S = C.copy()
    np.fill_diagonal(S, -1)
    aktif = np.ones(len(ok), bool)
    while True:
        Sm = np.where(aktif[:, None] & aktif[None, :], S, -1)
        i, j = np.unravel_index(np.argmax(Sm), Sm.shape)
        if Sm[i, j] < 0.7:
            break
        kume[i] += kume[j]
        kume[j] = []
        aktif[j] = False
        yeni = np.minimum(S[i], S[j])
        S[i, :], S[:, i] = yeni, yeni
        S[i, i] = -1
        S[j, :], S[:, j] = -1, -1
    lab = np.empty(len(ok), dtype=object)
    for kmb in kume:
        if kmb:
            bas = max(kmb, key=lambda q: dv[kp[q]])
            for q in kmb:
                lab[q] = f"{ok[bas]}({len(kmb)})" if len(kmb) > 1 else "tekil"
    rows["kor_kumesi"] = lab
    Cs = R1.iloc[-250:].corr(min_periods=120).to_numpy()
    yak = []
    for i in range(len(ok)):
        c = np.where(np.arange(len(ok)) == i, np.nan, Cs[i])
        o = np.argsort(-np.nan_to_num(np.abs(c), nan=-1))[:3]
        yak.append(", ".join(f"{ok[q]}:{c[q]:.2f}" for q in o if np.isfinite(c[q])))
    rows["en_yakin3"] = yak
    # boyut: 100 $ risk (10.000 $'in %1'i)
    rows["poz_1g_1sigma_usd"] = (100 / (rows.sigma_1g_60_pct / 100)).round(0)
    rows["poz_3g_1sigma_usd"] = (100 / (rows.sigma_3g_60_pct / 100)).round(0)
    for nm in ("1g", "3g"):
        ku = np.maximum(-rows[f"q01_{nm}_2010_pct"], -rows[f"q01_{nm}_vix30_pct"].fillna(-np.inf))
        kk = np.maximum(rows[f"q99_{nm}_2010_pct"], rows[f"q99_{nm}_vix30_pct"].fillna(-np.inf))
        rows[f"poz_{nm}_k99_uzun_usd"] = (100 / (ku / 100)).round(0)
        rows[f"poz_{nm}_k99_kisa_usd"] = (100 / (kk / 100)).round(0)
    # SPY ile korunma: kayan beta (250, t-1'e kadar) ile 1-3 gunluk varyans azalisi
    for h in (1, 2, 3):
        f = m.ileri("K", h, "kapanis", ok)
        fk = m.ileri_korunmali("K", h, "kapanis", "SPY", 250, ok)
        for ad, ms in (("250", np.arange(T) >= T - 250 - h), ("2010", s10)):
            ms = ms & (np.arange(T) < T - h)
            rows[f"kor_var_azalis_{h}g_{ad}"] = (1 - fk[ms].var() / f[ms].var()).round(3)
    rows.loc["SPY", [c for c in rows.columns if c.startswith("kor_var_azalis")]] = np.nan
    rows["korunma_ise_yaramiyor"] = (rows["kor_var_azalis_1g_250"] < 0.20) & (rows.index != "SPY")
    rows.index.name = "kod"
    rows = rows.sort_values("adv60_musd", ascending=False)
    rows.to_csv(RISK)
    log(f"risk tablosu: {len(rows)} kod -> {RISK}")
    return rows


# ----------------------------------------------------------------------------- ana akis
if __name__ == "__main__":
    asama = sys.argv[1] if len(sys.argv) > 1 else "hepsi"
    if asama in ("hepsi", "kural"):
        nb = asama_bakis()
        T, R_is = asama_is()
        O, R_oos = asama_oos(T)
        R_ay, ek = asama_ayrinti(O) if len(O) else (None, [])
        R_bet = asama_betimleme()
        parca = [R_is] + [x for x in (R_oos, R_bet, R_ay) if x is not None]
        R = pd.concat(parca, ignore_index=True)
        R = R.drop_duplicates(["kural_id", "hedef", "h", "giris", "cikis", "korunma", "komisyon", "donem", "rejim"],
                              keep="last")
        yaz_sonuc(R, SONUC)
        log(f"sonuc: {len(R)} satir -> {SONUC}")
        # ozet: her test satiri, aday/OOS/sinif
        Z = T.merge(O[["_kr", "hedef", "giris", "cikis", "h"] + [c for c in O.columns if c.startswith("oos") or c == "bh_aile_ici_q"]],
                    on=["_kr", "hedef", "giris", "cikis", "h"], how="left") if len(O) else T.copy()
        sn, gr = [], []
        for _, z in Z.iterrows():
            Rk = R[(R.kural_id == z["kural_id"]) & (R.hedef == z["hedef"])]
            s_, g_ = sinifla(z, Rk, ek)
            if not z["test_sayilir"]:
                s_, g_ = "-", "gunduz ayristirmasi (test degil)"
            sn.append(s_)
            gr.append(g_)
        Z["sinif"], Z["gerekce"] = sn, gr
        for e in ek:
            msk = (Z._kr == e["_kr"]) & (Z.hedef == e["hedef"]) & (Z.cikis == e["cikis"]) & (Z.h == e["h"])
            b, s = e["bolum"], e["saatlik"]
            Z.loc[msk, "vix30"] = (f"{b.get('bolum_sayisi', 0)} bolum, ayni isaret {b.get('ayni_isaret_orani', np.nan):.2f}, "
                                   f"destekli={b.get('destekli')}, net {b.get('net_bps', np.nan):.1f} bps")
            Z.loc[msk, "saatlik_1530"] = "; ".join(f"{k}={v:.3g}" if isinstance(v, float) else f"{k}={v}" for k, v in s.items())
        Z.drop(columns=["_kr"]).to_csv(OZET, index=False)
        log(f"ozet -> {OZET}")
        go = gece_ozeti()
        pd.set_option("display.width", 250)
        print(go[go.kod.isin(["SPY", "QQQ", "IWM", "TQQQ", "SQQQ"])].round(2).to_string(index=False))
        print("\n".join(bugun(O)))
        print(f"bakis_testi islev sayisi={nb}")
    if asama in ("hepsi", "risk"):
        rt = risk_tablosu()
        cols = ["beta_spy_250", "beta_spy_60", "sigma_1g_60_pct", "sigma_3g_60_pct", "q01_1g_vix30_pct",
                "q01_3g_vix30_pct", "gece_var_payi_250", "en_kotu_1g_pct", "en_kotu_1g_tarih", "gidis_donus_bps",
                "kor_kumesi", "poz_1g_1sigma_usd", "poz_3g_1sigma_usd", "poz_1g_k99_uzun_usd", "poz_3g_k99_uzun_usd",
                "kor_var_azalis_1g_250", "kor_var_azalis_3g_250"]
        print(rt.loc[[k for k in ["SPY", "QQQ", "TQQQ", "SQQQ", "SOXL", "SOXS", "NVDA", "TSLA", "MSTR", "IBIT"]
                      if k in rt.index], cols].to_string())
        print("korunma ise yaramiyor:", list(rt.index[rt.korunma_ise_yaramiyor]))
    log("bitti")
