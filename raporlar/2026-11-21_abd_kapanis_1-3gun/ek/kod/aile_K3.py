# -*- coding: utf-8 -*-
"""aile_K3.py - Aile C (capraz varlik -> endeks/sektor), YONTEM surum 2.
Calistirma:  python3 -I aile_K3.py            (IS tarama -> aday_K3.csv -> OOS -> sonuc_K3.csv)
             python3 -I aile_K3.py --yalniz-is (yalniz IS tarama ve aday dosyasi; OOS'a bakmaz)
Sira bozulmaz: aday listesi OOS hesaplanmadan ONCE diske yazilir.
Cikti: ../veri/aday_K3.csv, ../veri/sonuc_K3.csv (motor SEMA), ../veri/K3_ek.json (gece/bugun/korunma ozetleri).
Ham veri depoya yazilmaz."""
import json
import os
import sys
import time

import numpy as np
import pandas as pd

KOD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOD)
import motor as M  # noqa: E402

VERI = M.VERI_DIZIN
ADAY_YOL = os.path.join(VERI, "aday_K3.csv")
SONUC_YOL = os.path.join(VERI, "sonuc_K3.csv")
EK_YOL = os.path.join(VERI, "K3_ek.json")
AILE = "C"
ULKE = ["EWJ", "FXI", "KWEB", "EWZ", "EWT", "EWY", "INDA", "TUR"]
SEKTOR4 = ["XLY", "XLI", "XLB", "XLF"]


# ----------------------------------------------------------------------------- yardimcilar
def iki(pos, neg, idx):
    """pos -> +1, neg -> -1 (ikisi birden olamaz), NaN -> 0."""
    s = pd.Series(0, index=idx, dtype=int)
    s[pos.fillna(False).to_numpy(bool)] = 1
    s[neg.fillna(False).to_numpy(bool)] = -1
    return s


def C(mm, k):
    return mm.girdi(k, "adjclose")


def R(mm, k):
    return mm.girdi_getiri(k)


def zsig(S, w=252):
    """Kuraldaki 'S / sigma_252' (sigma t-1'de biter, ortalama cikarilmaz)."""
    sd = S.rolling(w, min_periods=w // 2).std().shift(1)
    return S / sd.where(sd > 0)


# ----------------------------------------------------------------------------- kurallar
def r201(mm, form):
    b = mm.beta("XLE", 60)["USO"].copy()
    e = R(mm, "USO") - b * R(mm, "XLE")
    S = e.rolling(5, min_periods=5).sum() if form == "S5" else e
    z = zsig(S)
    return iki(z > 1.5, z < -1.5, mm.idx), z.abs()


def r202(mm):
    x = C(mm, "USO") / C(mm, "USO").shift(5) - 1
    p = M.genisleyen_sira(x)
    return iki(p < 0.10, p > 0.90, mm.idx), (p - 0.5).abs()


def r204(mm):
    b = mm.beta("FCX", 60)["CPER"].copy()
    e = R(mm, "CPER") - b * R(mm, "FCX")
    z = zsig(e.rolling(3, min_periods=3).sum())
    return iki(z > 1.5, z < -1.5, mm.idx), z.abs()


def r208(mm, girdi, yon):
    tnx = mm.girdi("^TNX", "close")
    if girdi == "d10":
        d, e = tnx.diff(), 0.10
    else:
        d, e = (tnx - mm.girdi("^IRX", "close")).diff(), 0.08
    s = iki(d <= -e, d >= e, mm.idx)              # devam: faiz artisi -> banka kisa
    return (s if yon == "devam" else -s), d.abs()


def r209(mm, girdi):
    if girdi == "d10":
        d = mm.girdi("^TNX", "close").diff()
        return iki(d <= -0.10, d >= 0.10, mm.idx), d.abs()
    r = R(mm, "TLT")
    return iki(r >= 0.012, r <= -0.012, mm.idx), r.abs()


def r210(mm):
    b = mm.beta("XLU", 60)["TLT"].copy()
    e = R(mm, "TLT") - b * R(mm, "XLU")
    p = M.genisleyen_sira(e)
    return iki(p > 0.90, p < 0.10, mm.idx), (p - 0.5).abs()


def r211(mm):
    r = R(mm, "UUP")
    return iki(r <= -0.006, r >= 0.006, mm.idx), r.abs()


def r213(mm, L):
    rt = C(mm, "TLT") / C(mm, "TLT").shift(L) - 1
    rs = C(mm, "SPY") / C(mm, "SPY").shift(L) - 1
    return iki((rt > 0) & (rs > 0), (rt < 0) & (rs < 0), mm.idx), rs.abs()


def r214(mm, yon):
    g = C(mm, "GLD") / C(mm, "GLD").shift(20) - 1
    p = M.genisleyen_sira(g)
    s = iki(p < 0.10, p > 0.90, mm.idx)            # A: altin ust %10 -> sektor kisa
    if yon == "B":
        s = -s
    S = pd.DataFrame({k: s for k in SEKTOR4})
    G = pd.DataFrame({k: (p - 0.5).abs() for k in SEKTOR4})
    return S, G


def sepet_kodlari(mm):
    ev = mm.evren
    ok = (ev["kapanis_sinifi"] == "ABD16") & ev["maliyet_bps"].notna() & ev["tur"].isin(["hisse", "ETF"])
    ok &= ~ev["grup"].isin(["capraz_varlik"])
    ok &= ev["kaldirac"].astype(float) > 0
    ok &= ~ev.index.isin(["VXX", "VIXY", "UVXY", "SVXY"])
    return [k for k in ev.index[ok]]


def r809(mm, surum, sizintili=False):
    ks = sepet_kodlari(mm)
    P = mm.girdi(ks, "adjclose")
    mom = P.shift(21) / P.shift(252) - 1
    rk = mom.rank(axis=1, pct=True)
    spy = C(mm, "SPY")
    dd = spy / spy.cummax() - 1
    vix = mm.girdi("^VIX", "close", sizintili=sizintili)
    panik = (dd <= -0.15) & (vix >= 30) & (R(mm, "SPY") <= -0.025)
    pm = panik.fillna(False).to_numpy(bool)[:, None]
    uzun = (rk <= 0.10).to_numpy() & pm
    kisa = (rk >= 0.90).to_numpy() & pm
    S = np.zeros(rk.shape, dtype=int)
    S[uzun] = 1
    if surum == "LS":
        S[kisa] = -1
    S = pd.DataFrame(S, index=mm.idx, columns=ks)
    G = (rk - 0.5).abs()
    S = S.loc[:, (S != 0).any(axis=0)]
    return S, G[S.columns]


def sphb(mm, W, esik, yon):
    d = R(mm, "SPHB") - R(mm, "SPLV")
    z = M.z_skor(d, W)
    s = iki(z > esik, z < -esik, mm.idx)
    return (s if yon == "devam" else -s), z.abs()


def ulke(mm, W, esik):
    g = mm.girdi_getiri(ULKE, tur="gunici")
    z = M.z_skor(g, W)
    S = pd.DataFrame(0, index=mm.idx, columns=ULKE, dtype=int)
    S[(z > esik).fillna(False)] = -1
    S[(z < -esik).fillna(False)] = 1
    return S, z.abs()


# ----------------------------------------------------------------------------- varyant listesi
def varyantlar():
    V = []

    def ek(kid, var, ad, girdi, fn, hedef, yayin, hs=(1, 2, 3), gece=True):
        V.append(dict(kid=kid, var=var, ad=f"{ad} [{var}]", girdi=girdi, fn=fn, hedef=hedef,
                      yayin=yayin, hs=hs, gece=gece))
    for form in ("S5", "e1"):
        for hd in ("XLE", "XOP"):
            ek("R2-01", f"{form}|{hd}", "USO artigi (XLE'ye gore) +-1.5sigma -> " + hd, "USO, XLE kk; beta60",
               lambda mm, f=form: r201(mm, f), hd, 2017)
    for hd in ("JETS", "IYT", "XLY"):
        ek("R2-02", hd, "USO 5g getirisi ust/alt %10 -> " + hd + " ters", "USO 5g; genisleyen yuzdelik",
           r202, hd, 2009)
    for hd in ("FCX", "COPX"):
        ek("R2-04", hd, "CPER artigi (FCX'e gore) 3g +-1.5sigma -> " + hd, "CPER, FCX kk; beta60",
           r204, hd, 2017)
    for g in ("d10", "egri"):
        for yon in ("devam", "donus"):
            for hd in ("KRE", "XLF"):
                ek("R2-08", f"{g}|{yon}|{hd}", f"Faiz soku ({'d10y>=10bp' if g == 'd10' else 'd(10y-3a)>=8bp'}) {yon} -> {hd}",
                   "^TNX (ONCE 15:00 ET), ^IRX", lambda mm, a=g, b=yon: r208(mm, a, b), hd, 2012)
    for g in ("d10", "TLT"):
        for hd in ("ITB", "XHB"):
            ek("R2-09", f"{g}|{hd}", f"Faiz ({'d10y +-10bp' if g == 'd10' else 'TLT +-1.2%'}) -> {hd} ters",
               "^TNX / TLT", lambda mm, a=g: r209(mm, a), hd, None)
    ek("R2-10", "XLU", "TLT artigi (XLU'ya gore) ust/alt %10 -> XLU", "TLT, XLU kk; beta60", r210, "XLU", None)
    ek("R2-11", "EEM", "UUP +-0.6% -> EEM ters", "UUP kk", r211, "EEM", 2024)
    for L in (21, 252):
        for hd in ("SPY", "QQQ"):
            ek("R2-13", f"L{L}|{hd}", f"TLT ve SPY {L}g getiri isareti ayni -> {hd}", "TLT, SPY getirisi",
               lambda mm, a=L: r213(mm, a), hd, 2020)
    for yon in ("A", "B"):
        ek("R2-14", f"yon{yon}", f"GLD 20g ust/alt %10 -> XLY/XLI/XLB/XLF {'ters' if yon == 'A' else 'ayni'} yon",
           "GLD 20g; genisleyen yuzdelik", lambda mm, a=yon: r214(mm, a), None, 2017)
    for s in ("LS", "U"):
        ek("R8-09", s, f"Panik (SPY dd<=-15%, VIX(t-1)>=30, SPY<=-2.5%): 12-1 kaybedenler {'uzun, kazananlar kisa' if s == 'LS' else 'uzun'}",
           "sepet 12-1 getirisi, SPY, ^VIX(t-1)", lambda mm, a=s: r809(mm, a), None, 2014)
    for W in (60, 250):
        for e in (1.0, 2.0):
            for yon in ("devam", "donus"):
                ek("C-SPHB", f"W{W}|z{e:g}|{yon}", f"SPHB-SPLV z({W})>{e:g} {yon} -> SPY", "SPHB, SPLV kk",
                   lambda mm, a=W, b=e, c=yon: sphb(mm, a, b, c), "SPY", None)
    for W in (60, 250):
        for e in (1.0, 2.0):
            ek("C-ULKE", f"W{W}|z{e:g}", f"Ulke ETF ABD seansi (acilis->kapanis) z({W})>{e:g} -> ertesi gun donus",
               "ulke ETF gunici getirisi", lambda mm, a=W, b=e: ulke(mm, a, b), None, None, hs=(1,), gece=True)
    return V


def karar_t(row, cok, tek_yon):
    t = row["t_kume"] if cok else row["t_olcekli"]
    ok = (row["net_bps"] > 0) and np.isfinite(t) and t >= 2
    if tek_yon:
        ok = ok and row["anormal_bps"] > 0 and np.isfinite(row["t_anormal"]) and row["t_anormal"] >= 2
    return bool(ok), t


# ----------------------------------------------------------------------------- calistirma
def main(yalniz_is=False):
    t0 = time.time()
    m = M.Motor()
    V = varyantlar()
    # ileriye bakma denetimi (her sinyal ureteci bir kez)
    bakis = {}
    for v in V:
        anahtar = (v["kid"], v["var"].replace(v["hedef"], "") if v["hedef"] else v["var"])
        if anahtar in bakis:
            continue
        ok, rap = m.bakis_testi(lambda mm, f=v["fn"]: f(mm)[0])
        bakis[anahtar] = ok
        assert ok, (v["ad"], rap)
    print(f"bakis_testi: {len(bakis)} ureteci gecti ({time.time() - t0:.0f} sn)")

    # 1) YALNIZ IS tarama
    is_satir, aday = [], []
    for v in V:
        S, G = v["fn"](m)
        cok = isinstance(S, pd.DataFrame)
        r = m.degerlendir(S, v["hedef"], kural_id=v["kid"], aile=AILE, ad=v["ad"], girdi=v["girdi"],
                          h=v["hs"], giris=("K",), gece=v["gece"], korunma=("yok",), komisyon=("hisse",),
                          donemler=["IS"], rejimler=False, guc=G if cok else None, bootstrap=False,
                          notlar="asama=IS_tarama")
        for _, row in r.iterrows():
            tek_yon = row["yon"] != "iki"
            ok, t = karar_t(row, cok, tek_yon)
            aday.append(dict(kural_id=v["kid"], varyant=v["var"], ad=v["ad"], hedef=row["hedef"],
                             yon=row["yon"], h=int(row["h"]), cikis=row["cikis"], cok_hedef=cok,
                             olcu="t_kume" if cok else "t_olcekli", is_n=row["n_islem"],
                             is_net_bps=row["net_bps"], is_anormal_bps=row["anormal_bps"],
                             is_t=t, is_t_anormal=row["t_anormal"], aday=ok, yayin=v["yayin"]))
        is_satir.append(r)
    A = pd.DataFrame(aday)
    A.to_csv(ADAY_YOL, index=False)
    print(f"IS: {len(A)} varyant, {int(A.aday.sum())} aday -> {ADAY_YOL} ({time.time() - t0:.0f} sn)")
    print(A[A.aday][["kural_id", "varyant", "h", "cikis", "is_n", "is_net_bps", "is_t", "is_t_anormal"]].round(2).to_string())
    if yalniz_is:
        return

    # 2) OOS: yalniz adaylar
    vmap = {(v["kid"], v["var"]): v for v in V}
    son_satir, ek = [], {}
    aday_v = A[A.aday]
    oos_ozet = []
    for (kid, var), grp in aday_v.groupby(["kural_id", "varyant"], sort=False):
        v = vmap[(kid, var)]
        S, G = v["fn"](m)
        cok = isinstance(S, pd.DataFrame)
        hs = tuple(sorted({int(h) for h in grp.h if h > 0})) or (1,)
        hedge = ("yok",) if v["hedef"] == "SPY" else ("yok", "SPY:250", "SPY:60")
        kw = dict(kural_id=kid, aile=AILE, ad=v["ad"], girdi=v["girdi"], h=hs, gece=True,
                  korunma=hedge, guc=G if cok else None, rejimler=True)
        r1, isl = m.degerlendir(S, v["hedef"], giris=("K", "A", "G"), komisyon=("hisse",), bootstrap=True,
                                islem_dondur=True, notlar=f"asama=aday; yayin={v['yayin']}", **kw)
        r2 = m.degerlendir(S, v["hedef"], giris=("K", "A", "G"), komisyon=("sabit", "oransal"), bootstrap=False,
                           notlar=f"asama=aday; yayin={v['yayin']}", **kw)
        rr = pd.concat([r1, r2], ignore_index=True)
        son_satir.append(rr)
        for _, a in grp.iterrows():
            hh, ck = int(a.h), a.cikis
            sel = lambda d, g="K", kr="yok", kom="hisse", rj="hepsi": rr[(rr.donem == d) & (rr.giris == g) & (rr.h == hh) & (rr.cikis == ck)
                                                                      & (rr.korunma == kr) & (rr.komisyon == kom) & (rr.rejim == rj)]
            o = sel("OOS").iloc[0]
            tek_yon = o["yon"] != "iki"
            ok, t = karar_t(o, cok, tek_yon)
            sn = sel("SON").iloc[0]
            ga = sel("OOS", g="A") if ck == "kapanis" else sel("OOS", g="A").iloc[0:0]
            ik = isl[("K", 0 if ck == "acilis" else hh, ck, "yok")]
            _, boz = m.bolum_ozeti(ik, "hisse")
            oos_ozet.append(dict(kural_id=kid, varyant=var, h=hh, cikis=ck, hedef=o["hedef"], yon=o["yon"],
                                 is_net_bps=a.is_net_bps, is_t=a.is_t,
                                 oos_n=o["n_islem"], oos_net_bps=o["net_bps"], oos_anormal_bps=o["anormal_bps"],
                                 oos_t=t, oos_t_anormal=o["t_anormal"], oos_p=o["p_bootstrap"] if np.isfinite(o["p_bootstrap"]) else 1.0,
                                 oos_gecti=ok, son_n=sn["n_islem"], son_net_bps=sn["net_bps"],
                                 son_t=sn["t_kume"] if cok else sn["t_olcekli"],
                                 girisA_oos_net_bps=(ga.iloc[0]["net_bps"] if len(ga) else np.nan),
                                 girisA_oos_t=(ga.iloc[0]["t_kume" if cok else "t_olcekli"] if len(ga) else np.nan),
                                 basabas_bps=o["basabas_bps"], vix30_bolum=boz.get("bolum_sayisi"),
                                 vix30_ayni_isaret=boz.get("ayni_isaret_orani"), vix30_net=boz.get("net_bps"),
                                 vix30_destekli=boz.get("destekli"), yayin=v["yayin"],
                                 son_sinyal=(int(S.iloc[-1].abs().sum()) if cok else int(S.iloc[-1]))))
        print(f"  OOS {kid} {var}: {time.time() - t0:.0f} sn")
    O = pd.DataFrame(oos_ozet)
    # BH yalniz bilgi (aileler arasi duzeltmeyi ana ajan yapar)
    if len(O):
        O["bh10_aile_ici"], O["bh_q_aile_ici"] = M.bh(O["oos_p"].to_numpy(), 0.10)
    ek["oos_ozet"] = O.to_dict(orient="records")
    # sonuc dosyasi: aday olmayanlarin IS tarama satirlari + adaylarin tam satirlari
    IS = pd.concat(is_satir, ignore_index=True)
    aday_ad = set(aday_v["ad"])
    IS = IS[~IS["ad"].isin(aday_ad)]
    SON = pd.concat([IS] + son_satir, ignore_index=True)
    M.yaz_sonuc(SON, SONUC_YOL)
    with open(EK_YOL, "w") as f:
        json.dump(ek, f, ensure_ascii=False, indent=1, default=lambda x: None if x is None or (isinstance(x, float) and not np.isfinite(x)) else (x.item() if hasattr(x, "item") else str(x)))
    print(f"sonuc: {len(SON)} satir -> {SONUC_YOL} ({time.time() - t0:.0f} sn)")
    if len(O):
        print(O[["kural_id", "varyant", "h", "cikis", "is_net_bps", "oos_n", "oos_net_bps", "oos_t", "oos_t_anormal",
                 "oos_p", "oos_gecti", "son_net_bps", "son_t", "girisA_oos_net_bps", "basabas_bps",
                 "vix30_bolum", "vix30_ayni_isaret"]].round(2).to_string())


if __name__ == "__main__":
    main(yalniz_is="--yalniz-is" in sys.argv)
