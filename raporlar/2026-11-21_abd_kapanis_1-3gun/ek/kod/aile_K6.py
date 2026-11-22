# -*- coding: utf-8 -*-
"""aile_K6.py - Aile F (volatilite urunleri, VIX vade yapisi, VRP) ve H (DIX/GEX konumlanma).
Tek komut:  python3 -I aile_K6.py
Sira (YONTEM 7): 1) butun kural x varyantlar YALNIZ IS'te -> aday_K6.csv yazilir; 2) yalniz adaylar OOS;
3) OOS'tan gecenler tam degerlendirme (SON, A/G, gece, korunma, 3 komisyon, rejim, bootstrap).
Ciktilar: ../veri/aday_K6.csv, ../veri/sonuc_K6.csv, ../veri/kuyruk_K6.csv, ../veri/bugun_K6.csv
Kurallar:
 - ^VIX ailesi (SONRA, 16:15 ET) sinyalde 1 gun gecikmeli (m.girdi); ayni gun ^VIX yalniz '-SIZ' satirlari.
 - SVXY ve UVXY 28.02.2018 oncesi (_E) ve sonrasi (_Y) ayri arac (panel kopyasina ayri sutun olarak eklenir).
 - DIX/GEX kapanistan sonra yayimlanir: giris A (t+1 acilis).
 - Kisa volatilite: XIV 5-6 Subat 2018 kaybi elle eklenir ('olay dahil' / 'olay haric')."""
import os
import sys
import time

import numpy as np
import pandas as pd

KOD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOD)
import motor as M  # noqa: E402
import yukle  # noqa: E402

VERI = M.VERI_DIZIN
ADAY_YOL = os.path.join(VERI, "aday_K6.csv")
SONUC_YOL = os.path.join(VERI, "sonuc_K6.csv")
KUYRUK_YOL = os.path.join(VERI, "kuyruk_K6.csv")
BUGUN_YOL = os.path.join(VERI, "bugun_K6.csv")
KESIM = pd.Timestamp("2018-02-28")
SV = ["SVXY_E", "SVXY_Y"]
T0 = time.time()


def log(*a):
    print(f"[{time.time() - T0:6.1f}s]", *a, flush=True)


# ----------------------------------------------------------------------------- panel (+ _E/_Y araclari)
def panel_genis():
    P = yukle.panel()
    ev = P["evren"]
    yeni = []
    for kod in ("SVXY", "UVXY"):
        for ek, maske in (("_E", P["close"].index < KESIM), ("_Y", P["close"].index >= KESIM)):
            ad = kod + ek
            for a in ("open", "high", "low", "close", "adjclose", "volume", "adjopen"):
                if a in P:
                    s = P[a][kod].copy()
                    s[~maske] = np.nan
                    P[a] = P[a].assign(**{ad: s})
            r = ev[ev.kod == kod].copy()
            r["kod"] = ad
            r["kaldirac"] = {"SVXY_E": -1.0, "SVXY_Y": -0.5, "UVXY_E": 2.0, "UVXY_Y": 1.5}[ad]
            yeni.append(r)
    P["evren"] = pd.concat([ev] + yeni, ignore_index=True)
    return P


# ----------------------------------------------------------------------------- ozellikler
def b(c, v=1):
    return c.fillna(False).astype(int) * v if c.dtype == object else c.astype(int) * v


def ozellik(m, siz=False):
    """siz=False: VIX ailesi t-1 degeri (t kapanisinda bilinen). siz=True: ayni gun (sizintili).
    HV10 (SPY) de VIX ile ayni gune hizalanir: siz=False'ta HV10(t-1)."""
    vix = m.girdi("^VIX", "close", sizintili=siz)
    v3m = m.girdi("^VIX3M", "close", sizintili=siz)
    vvix = m.girdi("^VVIX", "close", sizintili=siz)
    lr = np.log1p(m.girdi_getiri("SPY"))
    hv10 = lr.rolling(10, min_periods=10).std() * np.sqrt(252) * 100
    if not siz:
        hv10 = hv10.shift(1)
    return dict(vix=vix, v3m=v3m, vvix=vvix, hv10=hv10, oran=v3m / vix, roll=(v3m - vix) / 21.0)


def rk(s, w=252):
    return s.rolling(w, min_periods=w).rank(pct=True)


# Her kural: fn(m, siz) -> {varyant: (sinyal, hedef)} ; META: h, korunma, giris, kisa_vol hedef fn
def r101(m, siz=False):
    f = ozellik(m, siz)
    up, dn = f["roll"] > 0.10, f["roll"] < -0.10
    d = {"VIXY iki yonlu (roll>+0,10 VIXY kisa; roll<-0,10 VIXY uzun) [vekil]": (b(dn) - b(up), "VIXY"),
         "VIXY uzun bacak (roll<-0,10) [vekil]": (b(dn), "VIXY")}
    for k in SV:
        d[f"{k} uzun (roll>+0,10) [vekil]"] = (b(up), k)
    return d


def r102(m, siz=False):
    f = ozellik(m, siz)
    up = f["roll"] > 0.10
    d = {}
    for k in SV:
        d[f"{k} uzun (roll>+0,10 ve VIX>21) [vekil]"] = (b(up & (f["vix"] > 21)), k)
        d[f"{k} uzun (roll>+0,10 ve VIX<21; karsilastirma) [vekil]"] = (b(up & (f["vix"] < 21)), k)
    return d


def r105(m, siz=False):
    f = ozellik(m, siz)
    vrp = (f["vix"] - f["hv10"]).rolling(5, min_periods=5).mean()
    pos, neg = vrp > 0, vrp <= 0
    d = {"VIXY iki yonlu (VRP5>0 kisa; VRP5<=0 uzun)": (b(neg) - b(pos), "VIXY"),
         "VIXY uzun bacak (VRP5<=0)": (b(neg), "VIXY")}
    for k in SV:
        d[f"{k} uzun (VRP5>0; nakit varyanti)"] = (b(pos), k)
    return d


def r106(m, siz=False):
    f = ozellik(m, siz)
    o = f["oran"]
    d = {"VIXY uzun bacak (VIX3M/VIX<1)": (b(o < 1), "VIXY")}
    for e in (1.00, 1.05, 1.10):
        d[f"VIXY iki yonlu (VIX3M/VIX>{e:.2f} kisa; <1 uzun)"] = (b(o < 1) - b(o > e), "VIXY")
        for k in SV:
            d[f"{k} uzun (VIX3M/VIX>{e:.2f})"] = (b(o > e), k)
    return d


def r107(m, siz=False):
    f = ozellik(m, siz)
    ev, eg = f["vix"] - f["hv10"], f["v3m"] - f["vix"]
    kisa = eg > 0
    uzun = (ev < 0) & (eg < 0)
    d = {"VIXY iki yonlu (egim>0 kisa; eVRP<0 ve egim<0 uzun)": (b(uzun) - b(kisa), "VIXY"),
         "VIXY uzun bacak (eVRP<0 ve egim<0)": (b(uzun), "VIXY")}
    for k in SV:
        d[f"{k} uzun (egim>0)"] = (b(kisa), k)
    return d


def r108(m, siz=False):
    f = ozellik(m, siz)
    vix, r = f["vix"], f["vix"] / f["v3m"]
    ins = (r >= 1)
    run = (~ins).cumsum()
    rmax = vix.where(ins).groupby(run).cummax()
    olay = (~ins) & ins.shift(1, fill_value=False) & (rmax.shift(1) >= 30)
    c35 = (vix >= 35) & (vix.shift(1) < 35)
    d = {}
    for ad, c in (("buyu bitisi (VIX/VIX3M>=1 ve VIX>=30 sonrasi <1)", olay), ("VIX>=35 ilk kapanis", c35)):
        d[f"VIXY kisa ({ad})"] = (b(c, -1), "VIXY")
        for k in SV:
            d[f"{k} uzun ({ad})"] = (b(c), k)
    return d


def r109(m, siz=False):
    f = ozellik(m, siz)
    ch = f["vix"].pct_change(fill_method=None)
    s1 = rk(ch) >= 0.8
    s2 = ch >= 0.20
    s3 = rk(m.girdi_getiri("VIXY")) >= 0.8          # ayni gun VIXY vekili (ABD16)
    d = {}
    for ad, c in (("VIX %deg ust %20 (252g)", s1), ("VIX %deg>=+%20", s2), ("VIXY getirisi ust %20 (252g; ayni gun vekil)", s3)):
        for k in ("VIXY", "UVXY_E", "UVXY_Y"):
            d[f"{k} uzun ({ad})"] = (b(c), k)
        d[f"TERS: VIXY kisa, sicramadan 2 gun sonra, 8 gun ({ad})"] = (b(c.shift(2, fill_value=False), -1), "VIXY")
    return d


def r110(m, siz=False):
    f = ozellik(m, siz)
    c = f["vix"] >= 35
    r = f["vix"] / f["v3m"]
    d = {}
    for ad, cc in (("hepsi", c), ("VIX/VIX3M>1", c & (r > 1)), ("VIX/VIX3M<1", c & (r < 1))):
        for k in SV + ["VIXY"]:
            d[f"{k} uzun (VIX>=35, {ad})"] = (b(cc), k)
        if ad != "hepsi":                           # 'hepsi' SPY/QQQ = R8-03 VIX>=35 (cift sayilmaz)
            for k in ("SPY", "QQQ"):
                d[f"{k} uzun (VIX>=35, {ad})"] = (b(cc), k)
    return d


def r113(m, siz=False):
    f = ozellik(m, siz)
    duz = (f["vix"] / f["v3m"]) < 1
    d = {}
    for ad, c in (("VVIX ust %10 (252g) ve VIX/VIX3M<1", (rk(f["vvix"]) >= 0.9) & duz),
                  ("VVIX/VIX ust %10 (252g) ve VIX/VIX3M<1", (rk(f["vvix"] / f["vix"]) >= 0.9) & duz)):
        d[f"VIXY kisa ({ad})"] = (b(c, -1), "VIXY")
        for k in SV:
            d[f"{k} uzun ({ad})"] = (b(c), k)
    return d


def r409(m, siz=False):
    f = ozellik(m, siz)
    r = m.girdi_getiri("SPY")
    dev = b(r > 0.01) - b(r < -0.01)
    d = {}
    for ad, c in (("VIX>25", f["vix"] > 25), ("VIX>30", f["vix"] > 30), ("VIX<20", f["vix"] < 20)):
        d[f"IWM devam (SPY>+%1 al, <-%1 sat), {ad}"] = (dev * b(c), "IWM")
        d[f"IWM geri donus (ters isaret), {ad}"] = (-dev * b(c), "IWM")
    return d


def r512(m, siz=False):
    f = ozellik(m, siz)
    q = m.girdi("QQQ")
    q20 = q / q.shift(20) - 1
    her = pd.Series(1, index=m.idx)
    kos = b((f["vix"] >= 30) & (q20.abs() < 0.05))
    return {"TQQQ+SQQQ birlikte aciga satis (her gun)": (pd.DataFrame({"TQQQ": -her, "SQQQ": -her}), None),
            "TQQQ+SQQQ aciga satis (VIX>=30 ve |QQQ 20g|<%5)": (pd.DataFrame({"TQQQ": -kos, "SQQQ": -kos}), None)}


def r803(m, siz=False):
    f = ozellik(m, siz)
    v = f["vix"]
    c35 = (v >= 35).to_numpy()
    bek = np.zeros(len(v), bool)
    son = -10 ** 9
    for i in np.flatnonzero(c35):
        if i - son > 5:
            bek[i] = True
            son = i
    sig = {"VIX>=35": v >= 35, "VIX>=40": v >= 40, "VIX>=50": v >= 50, "VIX 252g yuzdelik>=%97": rk(v) >= 0.97,
           "VIX 25-35 kovasi (karsilastirma)": (v >= 25) & (v < 35),
           "VIX>=35, ilk tetik + 5 gun bekleme": pd.Series(bek, index=v.index)}
    d = {}
    for ad, c in sig.items():
        for k in ("SPY", "QQQ", "UPRO"):
            d[f"{k} uzun ({ad})"] = (b(c), k)
    return d


def dg_seri(m):
    D = yukle.dix_gex().reindex(m.idx)
    return D["dix"], D["gex"]


def r307(m, siz=False):
    dix, _ = dg_seri(m)
    d = {}
    for ad, c in (("DIX>=0,45", dix >= 0.45), ("DIX 252g ust %10", rk(dix) >= 0.9)):
        for k in ("SPY", "QQQ", "SPXL"):
            d[f"{k} uzun ({ad})"] = (b(c), k)
    return d


def r306(m, siz=False):
    _, gex = dg_seri(m)
    r = rk(gex.diff())
    lo, hi = r <= 0.2, r >= 0.8
    d = {}
    for k in ("SPY", "QQQ"):
        d[f"{k} iki yonlu (dGEX ust %20 uzun, alt %20 kisa)"] = (b(hi) - b(lo), k)
        d[f"{k} iki yonlu TERS isaret"] = (b(lo) - b(hi), k)
        d[f"{k} uzun bacak (dGEX ust %20)"] = (b(hi), k)
        d[f"{k} kisa bacak (dGEX alt %20)"] = (b(lo, -1), k)
    return d


KURALLAR = [  # (id, ad, fn, h, korunma, giris, F mi, kaynak yili)
    ("R1-01", "Simon-Campasano roll (VIX3M-VIX)/21 vekili", r101, (1, 2, 3, 5), ("yok", "SPY:250"), "K", True, 2013),
    ("R1-02", "Roll + VIX>21", r102, (1, 2, 3, 5), ("yok",), "K", True, 2013),
    ("R1-05", "Cooper VRP anahtari (VIX-HV10, 5g ort)", r105, (1, 2, 3), ("yok",), "K", True, 2013),
    ("R1-06", "Cooper roll anahtari (VIX3M/VIX)", r106, (1, 2, 3), ("yok",), "K", True, 2013),
    ("R1-07", "Zarattini ikili sinyal (eVRP + egim), agirliksiz", r107, (1, 2, 3), ("yok",), "K", True, 2025),
    ("R1-08", "Cheng: buyu sonu SVXY", r108, (1, 2, 3), ("yok",), "K", True, 2019),
    ("R1-09", "VIX sicramasi sonrasi uzun vol momentumu", r109, (1, 2, 3), ("yok",), "K", True, 2012),
    ("R1-10", "VIX>=35 durum testi", r110, (1, 2, 3), ("yok",), "K", True, None),
    ("R1-13", "VVIX yuksek + duz vade -> kisa vol", r113, (1, 2, 3, 5), ("yok",), "K", True, 2015),
    ("R4-09", "Lead-lag stres filtresi (R4-3 SPY->IWM ile)", r409, (1,), ("yok", "SPY:250"), "K", True, 2022),
    ("R5-12", "TQQQ+SQQQ birlikte aciga satis", r512, (1, 2, 3, 5), ("yok",), "K", True, 2009),
    ("R8-03", "Asiri VIX seviyesi -> SPY uzun (Giot)", r803, (1, 2, 3, 5), ("yok",), "K", True, 2002),
    ("R3-07", "DIX yuksek -> uzun", r307, (1, 2, 3, 5), ("yok",), "A", False, 2018),
    ("R3-06", "GEX degisimi yonu", r306, (1, 2, 3), ("yok",), "A", False, 2026),
]
VERI_YOK = [("R1-12", "VIX1D geri donus", "^VIX1D panelde yok (2023'ten beri yayimlaniyor); VIX9D vekil sayilmaz (esikler VIX1D'ye ozgu)"),
            ("R3-08", "Toplam aciga satis akisi (FINRA)", "FINRA short volume panelde yok"),
            ("R3-09", "Hisse aciga satis orani (negatif kontrol)", "FINRA hisse bazinda short volume panelde yok"),
            ("R3-10", "Put/call asiriligi", "Cboe equity put/call orani panelde yok")]


def kisa_vol_mi(s, hedef):
    if isinstance(s, pd.DataFrame):
        return False
    if hedef in ("SVXY_E", "SVXY_Y"):
        return bool((s > 0).any())
    if hedef in ("VIXY", "UVXY_E", "UVXY_Y"):
        return bool((s < 0).any())
    return False


def cok_hedef(s):
    return isinstance(s, pd.DataFrame)


def t_karar(row, cok):
    return row["t_kume"] if cok else row["t_olcekli"]


def gecer(row, cok, tek_yon, esik=2.0):
    if not np.isfinite(row["net_bps"]) or row["n_islem"] < 2:
        return False
    t = t_karar(row, cok)
    ok = row["net_bps"] > 0 and np.isfinite(t) and t >= esik
    if tek_yon:
        ok = ok and np.isfinite(row["anormal_bps"]) and row["anormal_bps"] > 0 \
            and np.isfinite(row["t_anormal"]) and row["t_anormal"] >= 2
    return bool(ok)


# ----------------------------------------------------------------------------- XIV olayi
XIV = {pd.Timestamp("2018-02-02"): 115.55, pd.Timestamp("2018-02-05"): 99.00}
XIV_SON = 7.35      # 6 Subat kapanisi; sonrasi itfa (5,99 IV), muhafazakar olarak 7,35 sabit


def xiv_getiri(g, c, sv):
    """XIV'in [g kapanisi, c kapanisi] getirisi; g < 2 Subat ise oncesi SVXY (-1x) ile zincirlenir."""
    def fiyat(t):
        if t >= pd.Timestamp("2018-02-06"):
            return XIV_SON
        return XIV.get(t)
    pre = 1.0
    if g < pd.Timestamp("2018-02-02"):
        pre = sv.loc[pd.Timestamp("2018-02-02")] / sv.loc[g]
        g = pd.Timestamp("2018-02-02")
    if c < pd.Timestamp("2018-02-05"):
        return np.nan
    return pre * fiyat(c) / fiyat(g) - 1.0


def olay_satirlari(m, isl, sinyal, hedef, h, kom="hisse"):
    """IS (2010-2019) ve IS+OOS icin olay dahil / haric ozet. isl: giris K, cikis kapanis islem listesi."""
    sv = pd.Series(m.A["adjclose"][:, m.kpos["SVXY"]], index=m.idx)
    d = isl.copy()
    kv_yon = 1 if hedef in SV else -1                   # kisa vol yonu: SVXY uzun, VIXY/UVXY kisa
    d["olay"] = ((d["giris_tarihi"] <= pd.Timestamp("2018-02-05")) & (d["cikis_tarihi"] >= pd.Timestamp("2018-02-05"))
                 & (d["yon"] == kv_yon))
    net = d["net_" + kom].to_numpy(float).copy()
    sg = d["sigma20"].to_numpy(float)
    olcek = 0.5 if hedef == "SVXY_Y" else 1.0
    for i in np.flatnonzero(d["olay"].to_numpy()):
        xr = xiv_getiri(d["giris_tarihi"].iat[i], d["cikis_tarihi"].iat[i], sv)
        if np.isfinite(xr):
            net[i] = min(net[i], olcek * xr - d["mal_" + kom].iat[i])
    ek = []
    olay_notu = "olay penceresinde pozisyon yok"
    if d["olay"].any():
        olay_notu = "olay penceresinde pozisyon VAR (gercek veriyle; XIV ile degistirildi)"
    elif hedef in ("SVXY_Y",) and isinstance(sinyal, pd.Series):
        # arac o tarihte yok: sinyal acik olsaydi -0,5x XIV kaybi varsayimsal islem olarak eklenir
        ii = m.idx.get_loc(pd.Timestamp("2018-02-06"))
        for t in range(ii - h, ii):
            if t >= 0 and sinyal.iat[t] == kv_yon:
                g, c = m.idx[t], m.idx[min(t + h, len(m.idx) - 1)]
                xr = xiv_getiri(g, c, sv)
                ek.append(olcek * xr - 0.002)
                olay_notu = f"arac yokken sinyal {g.date()} acikti: -0,5x XIV varsayimsal islem eklendi ({olcek * xr * 100:.1f}%)"
                break
    satir = []
    for dn, (a, z) in (("IS", ("2010-01-01", "2019-12-31")), ("IS+OOS", ("2010-01-01", "2023-12-31"))):
        msk = ((d["t"] >= a) & (d["t"] <= z)).to_numpy()
        for tur in ("dahil", "haric"):
            if tur == "dahil":
                x = np.r_[net[msk], ek]
                s = np.r_[sg[msk], [np.nanmean(sg[msk]) if msk.any() else np.nan] * len(ek)]
            else:
                kk = msk & ~d["olay"].to_numpy()
                x, s = d["net_" + kom].to_numpy(float)[kk], sg[kk]
            o = x / s
            o = o[np.isfinite(o)]
            tt = o.mean() / o.std(ddof=1) * np.sqrt(o.size) if o.size > 2 else np.nan
            satir.append(dict(donem=dn, rejim="hepsi", n_islem=int(x.size), net_bps=np.nanmean(x) * 1e4 if x.size else np.nan,
                              t_olcekli=tt, en_kotu_bps=np.nanmin(x) * 1e4 if x.size else np.nan,
                              notlar=f"XIV olay {tur}; {olay_notu}"))
    return satir


# ----------------------------------------------------------------------------- ana akis
def main():
    log("panel yukleniyor")
    P = panel_genis()
    m = M.Motor(P, kalite_df=yukle.kalite(), temettu_df=yukle.temettu())
    log("motor hazir")

    # 0) ileriye bakma denetimi (kural basina, butun varyantlar birlikte)
    bakis = {}
    for kid, ad, fn, *_ in KURALLAR:
        def tum(mm, fn=fn):
            dd = fn(mm)
            cols = {}
            for i, (v, (s, hdf)) in enumerate(dd.items()):
                if isinstance(s, pd.DataFrame):
                    for c in s.columns:
                        cols[f"{i}_{c}"] = s[c]
                else:
                    cols[str(i)] = s
            return pd.DataFrame(cols)
        ok, rap = m.bakis_testi(tum)
        bakis[kid] = ok
        if not ok:
            log("BAKIS TESTI BASARISIZ", kid, rap)
    log("bakis testi:", bakis)

    # 1) YALNIZ IS tarama
    is_satir, varyantlar, olay_s = [], [], []
    vno = 0
    for kid, ad, fn, H, KOR, G, F, yil in KURALLAR:
        dd = fn(m)
        for v, (s, hdf) in dd.items():
            vno += 1
            cok = cok_hedef(s)
            S = s if cok else s
            if (S.abs().sum().sum() if cok else S.abs().sum()) == 0:
                continue
            tek = (np.asarray(S) >= 0).all() or (np.asarray(S) <= 0).all()
            Hv = (8,) if v.startswith("TERS") else H
            res, isl = m.degerlendir(s, hdf, kural_id=kid, aile="F" if F else "H", ad=f"{ad} | {v}",
                                     girdi=v, h=Hv, giris=(G,), gece=(G == "K" and Hv != (8,)), korunma=KOR,
                                     komisyon="hisse", donemler=["IS"], rejimler=False, bootstrap=False,
                                     notlar=f"asama=IS_tarama; vno={vno}; yayin={yil}", islem_dondur=True)
            res["vno"] = vno
            is_satir.append(res)
            varyantlar.append(dict(vno=vno, kid=kid, ad=ad, v=v, s=s, hedef=hdf, H=Hv, KOR=KOR, G=G, F=F,
                                   cok=cok, tek=tek, yil=yil, kisa_vol=kisa_vol_mi(s, hdf)))
            if kisa_vol_mi(s, hdf) and not cok:
                for hh in Hv:
                    k_ = ("K", hh, "kapanis", "yok")
                    if k_ in isl:
                        for o in olay_satirlari(m, isl[k_], s, hdf, hh):
                            o.update(kural_id=kid + "-XIV", aile="F", ad=f"{ad} | {v}", girdi=v, hedef=hdf,
                                     yon="uzun" if hdf in SV else "kisa", h=hh, giris="K", cikis="kapanis",
                                     korunma="yok", komisyon="hisse")
                            o["notlar"] += f"; vno={vno}"
                            olay_s.append(o)
        log(kid, "IS tamam; varyant", vno)
    IS = pd.concat(is_satir, ignore_index=True)
    test_n = len(IS)
    log("IS test sayisi (satir; komisyon=hisse, rejim=hepsi):", test_n)

    # 2) adaylar
    vmap = {v["vno"]: v for v in varyantlar}
    IS["aday"] = [gecer(IS.loc[i], vmap[IS.at[i, "vno"]]["cok"], vmap[IS.at[i, "vno"]]["tek"]) for i in IS.index]
    AD = IS[IS.aday].copy()
    AD.drop(columns=["aday"]).to_csv(ADAY_YOL, index=False)
    log(f"aday sayisi: {len(AD)} -> {ADAY_YOL}")
    print(AD[["kural_id", "vno", "girdi", "hedef", "h", "giris", "cikis", "korunma", "n_islem", "net_bps",
              "anormal_bps", "t_olcekli", "t_kume", "t_anormal"]].round(2).to_string(index=False), flush=True)

    # 3) adaylar OOS (bootstrap=True). _E araci OOS'ta yok -> ardil _Y araci (ayni sinyal)
    oos_s = []
    for r in AD.itertuples():
        v = vmap[r.vno]
        hedef = v["hedef"]
        notu = ""
        if hedef in ("SVXY_E", "UVXY_E"):
            hedef = hedef.replace("_E", "_Y")
            notu = "; OOS ardil arac (_E 2018'de kapandi)"
        hh = int(r.h) if r.cikis == "kapanis" else 1
        res = m.degerlendir(v["s"], hedef, kural_id=v["kid"], aile="F" if v["F"] else "H",
                            ad=f"{v['ad']} | {v['v']}", girdi=v["v"], h=(hh,), giris=(r.giris,),
                            gece=(r.cikis == "acilis"), korunma=(r.korunma,), komisyon="hisse",
                            donemler=["IS", "OOS"], rejimler=False, bootstrap=True,
                            notlar=f"asama=aday_OOS; vno={r.vno}{notu}; yayin={v['yil']}")
        if r.cikis == "acilis":
            res = res[res.cikis == "acilis"]
        else:
            res = res[res.cikis == "kapanis"]
        res["vno"] = r.vno
        oos_s.append(res)
    OO = pd.concat(oos_s, ignore_index=True) if oos_s else pd.DataFrame(columns=M.SEMA + ["vno"])
    OOS = OO[OO.donem == "OOS"].copy()
    OOS["gecti"] = [gecer(OOS.loc[i], vmap[OOS.at[i, "vno"]]["cok"], vmap[OOS.at[i, "vno"]]["tek"]) for i in OOS.index]
    log("OOS gecen:", int(OOS.gecti.sum()), "/", len(OOS))
    print(OOS[["kural_id", "vno", "girdi", "hedef", "h", "giris", "cikis", "n_islem", "net_bps", "anormal_bps",
               "t_olcekli", "t_kume", "t_anormal", "p_bootstrap", "gecti"]].round(3).to_string(index=False), flush=True)

    # 3b) adaylar icin bilgi amacli ek (secimde kullanilmaz): VIX(t-1)>30 bolumleri 2005-2023 (SON kilitli)
    #     ve giris A OOS sonucu
    ek_s = []
    for r in AD.itertuples():
        v = vmap[r.vno]
        hedef = v["hedef"]
        hh = int(max(r.h, 1))
        ck = r.cikis
        x = m.islemler(v["s"], hedef, giris="K", h=hh, cikis=ck, korunma=r.korunma)
        x = x[x["t"] <= pd.Timestamp("2023-12-31")]
        tab, oz = m.bolum_ozeti(x, "hisse")
        pos = float((tab["net_bps"] > 0).mean()) if len(tab) else np.nan
        ra = m.degerlendir(v["s"], hedef, kural_id=v["kid"], aile="F" if v["F"] else "H",
                           ad=f"{v['ad']} | {v['v']}", girdi=v["v"], h=(hh,), giris=("A",), gece=False,
                           korunma=(r.korunma,), komisyon="hisse", donemler=["OOS"], rejimler=False,
                           notlar=f"asama=aday_ek_girisA; vno={r.vno}; bilgi amacli")
        ra["vno"] = r.vno
        ek_s.append(ra)
        log(f"aday ek vno={r.vno}: V>30 bolum={oz.get('bolum_sayisi')} pozitif_oran={pos:.2f} "
            f"destekli={oz.get('destekli')} net={oz.get('net_bps', np.nan):.1f}; A-OOS net={ra.net_bps.iat[0]:.1f} "
            f"t={ra.t_olcekli.iat[0]:.2f}")
        ek_s.append(pd.DataFrame([dict(kural_id=v["kid"], aile="F" if v["F"] else "H", ad=f"{v['ad']} | {v['v']}",
                                       girdi=v["v"], hedef=hedef, h=r.h, giris="K", cikis=ck, korunma=r.korunma,
                                       komisyon="hisse", donem="2005-2023", rejim="V>30 bolum",
                                       n_islem=oz.get("n_islem", 0), net_bps=oz.get("net_bps", np.nan),
                                       bolum_sayisi=oz.get("bolum_sayisi", 0), bolum_pozitif_orani=pos,
                                       maliyet2x_net_bps=oz.get("maliyet2x_net_bps", np.nan),
                                       notlar=f"asama=aday_ek_bolum; vno={r.vno}; destekli={oz.get('destekli')}; "
                                              f"en_buyuk_haric={oz.get('en_buyuk_haric_net_bps', np.nan):.1f}")]))
    OO = pd.concat([OO] + ek_s, ignore_index=True) if ek_s else OO

    # 4) OOS'tan gecenler: tam degerlendirme
    tam_s, kuyruk = [], []
    for i in OOS.index[OOS.gecti]:
        r = OOS.loc[i]
        v = vmap[r.vno]
        hedef = r.hedef
        kor = ("yok", "SPY:250", "SPY:60", "SPXS:250")
        res, isl = m.degerlendir(v["s"], hedef, kural_id=v["kid"], aile="F" if v["F"] else "H",
                                 ad=f"{v['ad']} | {v['v']}", girdi=v["v"], h=(int(max(r.h, 1)),),
                                 giris=("K", "A", "G") if v["G"] == "K" else ("A", "G"), gece=(v["G"] == "K"),
                                 korunma=kor, bootstrap=True, islem_dondur=True,
                                 notlar=f"asama=tam; vno={r.vno}; yayin={v['yil']}")
        res["vno"] = r.vno
        tam_s.append(res)
        k_ = ("K", 0, "acilis", "yok") if r.cikis == "acilis" else (v["G"], int(max(r.h, 1)), "kapanis", "yok")
        tab, oz = m.bolum_ozeti(isl[k_], "hisse")
        log("tam", v["kid"], v["v"], hedef, "bolum:", oz)
        x = isl[k_]
        kuyruk.append(x.nsmallest(5, "net_hisse").assign(vno=r.vno, tur="en_kotu5"))
    TAM = pd.concat(tam_s, ignore_index=True) if tam_s else pd.DataFrame(columns=M.SEMA)

    # 5) kisa vol adaylarin sol kuyrugu (IS+OOS; SON kilitli) - aday olanlar
    for r in AD.itertuples():
        v = vmap[r.vno]
        if not v["kisa_vol"] or r.cikis != "kapanis":
            continue
        for hedef in ([v["hedef"], v["hedef"].replace("_E", "_Y")] if v["hedef"].endswith("_E") else [v["hedef"]]):
            x = m.islemler(v["s"], hedef, giris="K", h=int(r.h), korunma=r.korunma)
            x = x[x["t"] <= pd.Timestamp("2023-12-31")]
            kuyruk.append(x.nsmallest(5, "net_hisse").assign(vno=r.vno, tur="en_kotu5_IS+OOS"))
            for a, z, ad_ in (("2018-01-25", "2018-02-28", "Subat2018"), ("2020-02-15", "2020-04-15", "Mart2020")):
                y = x[(x["t"] >= a) & (x["t"] <= z)]
                if len(y):
                    kuyruk.append(y.assign(vno=r.vno, tur=ad_))
    # temsilci kisa vol stratejileri (aday olmasalar da sol kuyruk raporu; h=1, 2010-2023, SON kilitli)
    TEMSIL = [("R1-06", "SVXY_E uzun (VIX3M/VIX>1.00)"), ("R1-06", "SVXY_Y uzun (VIX3M/VIX>1.00)"),
              ("R1-06", "VIXY iki yonlu (VIX3M/VIX>1.00 kisa; <1 uzun)"), ("R1-05", "SVXY_E uzun (VRP5>0; nakit varyanti)"),
              ("R1-05", "SVXY_Y uzun (VRP5>0; nakit varyanti)"), ("R1-07", "SVXY_Y uzun (egim>0)"),
              ("R1-13", "SVXY_E uzun (VVIX ust %10 (252g) ve VIX/VIX3M<1)")]
    mdd_s = []
    for kid, vv in TEMSIL:
        v = next(x for x in varyantlar if x["kid"] == kid and x["v"] == vv)
        x = m.islemler(v["s"], v["hedef"], giris="K", h=1)
        x = x[(x["t"] >= pd.Timestamp("2010-01-01")) & (x["t"] <= pd.Timestamp("2023-12-31"))]
        gs = m.gunluk(x, "hisse")
        gs = pd.Series(np.asarray(gs, float).ravel()[:len(m.idx)], index=m.idx) if not isinstance(gs, pd.Series) else gs
        gs = gs[(gs.index >= "2010-01-01") & (gs.index <= "2023-12-31")]
        sub = {ad_: x[(x["t"] >= a) & (x["t"] <= z)]["net_hisse"] for a, z, ad_ in
               (("2018-01-25", "2018-02-28", "Subat2018"), ("2020-02-15", "2020-04-15", "Mart2020"))}
        mdd_s.append(dict(vno=v["vno"], kural=kid, varyant=vv, hedef=v["hedef"], n=len(x),
                          net_bps=x["net_hisse"].mean() * 1e4, mdd_pct=M.mdd(gs.fillna(0).to_numpy()) * 100,
                          en_kotu5_bps=list((x["net_hisse"].nsmallest(5) * 1e4).round(0)),
                          en_kotu5_tarih=[str(d.date()) for d in x.nsmallest(5, "net_hisse")["t"]],
                          subat2018_toplam_pct=(np.prod(1 + sub["Subat2018"]) - 1) * 100 if len(sub["Subat2018"]) else np.nan,
                          mart2020_toplam_pct=(np.prod(1 + sub["Mart2020"]) - 1) * 100 if len(sub["Mart2020"]) else np.nan))
        kuyruk.append(x.nsmallest(5, "net_hisse").assign(vno=v["vno"], tur="temsil_en_kotu5_2010-2023"))
    MDD = pd.DataFrame(mdd_s)
    MDD.to_csv(KUYRUK_YOL.replace(".csv", "_ozet.csv"), index=False)
    print(MDD.round(1).to_string(index=False), flush=True)
    if kuyruk:
        K = pd.concat(kuyruk, ignore_index=True)
        K[["vno", "tur", "hedef", "t", "giris_tarihi", "cikis_tarihi", "yon", "brut", "net_hisse"]].to_csv(KUYRUK_YOL, index=False)

    # 6) sizintili ust sinir satirlari (F kurallarinin ilk varyanti; test sayisina katilmaz)
    siz_s = []
    for kid, ad, fn, H, KOR, G, F, yil in KURALLAR:
        if not F:
            continue
        v0, (s0, h0) = next(iter(fn(m, siz=True).items()))
        res = m.degerlendir(s0, h0, kural_id=kid + "-SIZ", aile="F", ad=f"{ad} | {v0} | SIZINTILI UST SINIR",
                            girdi=v0 + " (ayni gun ^VIX)", h=H, giris=("K",), gece=False, korunma=("yok",),
                            komisyon="hisse", donemler=["IS", "OOS"], rejimler=False,
                            notlar="asama=sizintili_ust_sinir; karar icin KULLANILMAZ")
        siz_s.append(res)
    SIZ = pd.concat(siz_s, ignore_index=True)

    # 7) R3-05 tanimlayici (yon kurali degil): ertesi gun |SPY| ve std, GEX filtresi
    dix, gex = dg_seri(m)
    vix1 = m.girdi("^VIX", "close")
    r1 = m.getiri("kk", ham=True)["SPY"].shift(-1)          # t+1 getirisi (yalniz tanimlayici olcu)
    filt = (rk(gex) >= 0.75) & (vix1 < 20)
    neg = gex < 0
    r305 = []
    for dn, (a, z) in M.DONEMLER.items():
        if dn == "STRES":
            continue
        msk = (m.idx >= a) & (m.idx <= z) & r1.notna().to_numpy() & gex.notna().to_numpy()
        for ad_, c in (("GEX ust ceyrek ve VIX<20", filt), ("GEX<0", neg)):
            cc = c.to_numpy() & msk
            dd = (~c.to_numpy()) & msk
            if cc.sum() < 5:
                continue
            r305.append(dict(kural_id="R3-05", aile="H", ad="GEX oynaklik filtresi (tanimlayici)", girdi=ad_, hedef="SPY",
                             yon="filtre", h=1, giris="A", cikis="kapanis", korunma="yok", komisyon="yok",
                             donem=dn, rejim="hepsi", n_islem=int(cc.sum()),
                             sigma_bps=float(r1[cc].std() * 1e4),
                             notlar=f"filtre ici std={r1[cc].std() * 1e4:.1f} bps, ort|r|={r1[cc].abs().mean() * 1e4:.1f}; "
                                    f"disi std={r1[dd].std() * 1e4:.1f} bps, ort|r|={r1[dd].abs().mean() * 1e4:.1f}, n_dis={int(dd.sum())}; "
                                    "P&L kurali degil, test sayisina katilmadi"))
    R305 = pd.DataFrame(r305)

    VY = pd.DataFrame([dict(kural_id=k, aile="F" if k.startswith("R1") else "H", ad=a, notlar="VERI YOK: " + n)
                       for k, a, n in VERI_YOK])
    OLAY = pd.DataFrame(olay_s)
    hepsi = pd.concat([IS.drop(columns=["aday"]), OO, TAM, OLAY, SIZ, R305, VY], ignore_index=True)
    hepsi = hepsi.reindex(columns=M.SEMA)
    M.yaz_sonuc(hepsi, SONUC_YOL)
    log("sonuc satiri:", len(hepsi), "->", SONUC_YOL)

    # 8) bugun: 20 Kasim sinyali (durust) ve 23 Kasim sinyali (= ayni gun degerlerle; yalniz gecikmeli VIX kisimlari)
    bug = []
    son = m.idx[-1]
    for kid, ad, fn, H, KOR, G, F, yil in KURALLAR:
        d0 = fn(m)
        d1 = fn(m, siz=True)
        for v, (s, hdf) in d0.items():
            s1 = d1[v][0]
            a0 = s.iloc[-1] if not cok_hedef(s) else s.iloc[-1].to_dict()
            a1 = s1.iloc[-1] if not cok_hedef(s1) else s1.iloc[-1].to_dict()
            bug.append(dict(kural_id=kid, varyant=v, hedef=hdf, sinyal_20kas=a0, sinyal_23kas_vix_bilinen=a1))
    f0 = ozellik(m, siz=True)
    durum = {k: float(f0[k].iloc[-1]) for k in f0}
    durum.update(dix=float(dix.iloc[-1]), gex=float(gex.iloc[-1]), dgex_rk=float(rk(gex.diff()).iloc[-1]),
                 dix_rk=float(rk(dix).iloc[-1]), vvix_rk=float(rk(f0["vvix"]).iloc[-1]))
    B = pd.DataFrame(bug)
    B.to_csv(BUGUN_YOL, index=False)
    log("bugun:", {k: round(v, 3) for k, v in durum.items()}, "tarih", son.date())
    print(B[(B.sinyal_20kas.astype(str) != "0") | (B.sinyal_23kas_vix_bilinen.astype(str) != "0")].to_string(index=False))
    # ozet yazimi
    print("TEST_SAYISI", test_n, "ADAY", len(AD), "OOS_GECEN", int(OOS.gecti.sum()))


if __name__ == "__main__":
    main()
