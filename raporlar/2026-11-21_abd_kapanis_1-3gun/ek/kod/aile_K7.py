# -*- coding: utf-8 -*-
"""aile_K7.py - Aile G: bilanco etrafinda 1-3 gunluk kurallar (K7).
Kurallar: R6-01, R6-02, R6-03, R6-04, R6-06, R5-07, R5-08 + EK (bilanco oncesi prim, yontem denetcisi).
Calistirma:  python3 -I aile_K7.py            (hepsi: is -> oos -> tam -> bugun)
             python3 -I aile_K7.py is|oos|tam|bugun   (asama asama; sonraki asama oncekinin dosyasini okur)
Ciktilar: ../veri/aday_K7.csv (OOS'a bakmadan once), ../veri/sonuc_K7.csv (standart sema),
          ../veri/K7_tepki_denetim.csv, ../veri/K7_bugun.csv, ../veri/K7_oos_tarama.csv
Notlar:
- Tepki gunu: bilanco_tarihleri.csv 'ilk_tepki_gunu' (kabul damgasi) = R. Hacim yontemi: {R-1, R, R+1} icinde
  hacmi en yuksek gun. Islem filtresinde yalniz R kapanisinda bilinen kisim kullanilir (hacim(R) >= hacim(R-1));
  R+1 karsilastirmasi ileriye bakma oldugu icin yalniz denetim oranina girer (sapma 1).
- Bilanco oncesi kurallarda (R6-03, R6-04, EK, R6-06) olay tarihi onceden ilan edilmis kabul edilir ve hacim
  filtresi uygulanmaz (filtre olay sonrasi veriye bakar).
- Evren: 'buyuk' = donem basi evreni (evren_donem_basi.csv; STRES gunlerinde IS listesi) ve tema degil;
  'kucuk' = bilanco verisi olan diger hisseler (tema dahil; hayatta kalma yanliligi tam).
"""
import os
import sys
import time

import numpy as np
import pandas as pd

KOD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOD)
import motor as M          # noqa: E402
from yukle import bilanco  # noqa: E402

VERI = M.VERI_DIZIN
ADAY = os.path.join(VERI, "aday_K7.csv")
SONUC = os.path.join(VERI, "sonuc_K7.csv")
OOS_TARAMA = os.path.join(VERI, "K7_oos_tarama.csv")
DENETIM = os.path.join(VERI, "K7_tepki_denetim.csv")
BUGUN = os.path.join(VERI, "K7_bugun.csv")
TEMA_GRUP = {"h_ai_altyapi", "h_kuantum", "h_kripto", "h_gunes", "h_ev_cin", "h_meme"}
TOHUM = 20261121
YAYIN = {"R6-01": 2021, "R6-02": 2021, "R6-03": 2014, "R6-04": 2007, "EK": 2007, "R6-06": 2008,
         "R5-07": 2022, "R5-08": 2012}


# ----------------------------------------------------------------------------- hazirlik
class Veri:
    def __init__(self, m):
        self.m = m
        idx = m.idx
        T = m.T
        ev = m.evren
        B = bilanco().dropna(subset=["ilk_tepki_gunu"]).copy()
        B["kod"] = B["kod"].astype(str)
        ok = [k for k in B["kod"].unique() if k in m.kpos and str(ev.at[k, "tur"]) == "hisse"
              and m.sinif.get(k) == "ABD16" and np.isfinite(ev.at[k, "maliyet_bps"])]
        B = B[B["kod"].isin(ok)]
        B["iR"] = idx.searchsorted(B["ilk_tepki_gunu"].values)
        B["iF"] = idx.searchsorted(B["filing_date"].values)
        B = B[(B["iR"] < T) & (B["iR"] > 25)].sort_values(["kod", "iR"])
        onceki = B.groupby("kod")["iR"].shift(1)
        self.n_ham = len(B)
        B = B[~((B["iR"] - onceki) < 5)].copy()          # ayni ceyrekte ikinci 2.02 (on duyuru vb.) atilir
        self.n_tekrar = self.n_ham - len(B)
        self.kodlar = sorted(B["kod"].unique())
        self.c = {k: i for i, k in enumerate(self.kodlar)}
        kp = np.array([m.kpos[k] for k in self.kodlar])
        self.kp = kp
        V = m.A["volume"][:, kp]
        R = m.getiri("kk")[self.kodlar].to_numpy()       # hisseler ABD16: ayni gun guvenli
        rS = m.getiri("kk")["SPY"].to_numpy()
        self.R, self.rS, self.V = R, rS, V
        B["ci"] = B["kod"].map(self.c).astype(int)
        iR, ci = B["iR"].to_numpy(), B["ci"].to_numpy()
        vm1 = V[iR - 1, ci]
        v0 = V[iR, ci]
        vp1 = np.where(iR + 1 < T, V[np.minimum(iR + 1, T - 1), ci], np.nan)
        taban = np.array([np.nanmean(V[i - 20:i, c]) for i, c in zip(iR, ci)])
        B["hacim_oran"] = v0 / taban
        B["uyum_rt"] = v0 >= vm1
        B["uyum_lit"] = (v0 >= vm1) & ~(vp1 > v0)
        B["AR"] = R[iR, ci] - rS[iR]
        self.B = B
        # sektor ETF'ine gore artik (hisse - sektor ETF), ayni gun
        sek = [M.GRUP_SEKTOR.get(str(ev.at[k, "grup"]), "SPY") for k in self.kodlar]
        sek = [s if s in m.kpos else "SPY" for s in sek]
        RS = m.getiri("kk")[sek].to_numpy()
        self.rel = R - RS
        self.sektor = dict(zip(self.kodlar, sek))
        # tema sinifi
        ilk = pd.to_datetime(ev.loc[self.kodlar, "ilk_tarih"])
        grup = ev.loc[self.kodlar, "grup"].astype(str)
        self.tema = ((ilk >= pd.Timestamp("2015-01-01")) | grup.isin(TEMA_GRUP)).to_numpy()
        # donem basi evreni
        yol = os.path.join(VERI, "evren_donem_basi.csv")
        tab = pd.read_csv(yol) if os.path.exists(yol) else m.donem_basi_evreni()
        EM = m.evren_maskesi(tab).to_numpy()[:, kp].copy()
        stres = M.donem_maskesi(idx, "STRES")
        is_k = [self.c[k] for k in tab.loc[tab["donem"] == "IS", "kod"] if k in self.c]
        EM[np.ix_(stres, is_k)] = True                   # sapma 3: STRES gunlerinde IS listesi
        var = np.isfinite(m.A["adjclose"][:, kp])
        self.U = {"B": EM & ~self.tema[None, :] & var, "K": ~(EM & ~self.tema[None, :]) & var}
        # bilanco penceresi (R-1, R, R+1) ve olay gunu
        EW = np.zeros((T, len(kp)), bool)
        ER = np.zeros((T, len(kp)), bool)
        for d in (-1, 0, 1):
            j = np.clip(iR + d, 0, T - 1)
            EW[j, ci] = True
        ER[iR, ci] = True
        self.EW, self.ER = EW, ER

    def df(self, A):
        return pd.DataFrame(A, index=self.m.idx, columns=self.kodlar)


def olay_matris(v, s, c, val, guc):
    """Olay listesinden (s: sinyal gunu, c: sutun) sinyal ve guc matrisi; ayni hucrede guclu olan kalir."""
    T, N = v.m.T, len(v.kodlar)
    S = np.zeros((T, N))
    G = np.zeros((T, N))
    ok = (s >= 0) & (s < T) & np.isfinite(guc) & (val != 0)
    s, c, val, guc = s[ok], c[ok], val[ok], guc[ok]
    o = np.argsort(guc, kind="mergesort")
    S[s[o], c[o]] = val[o]
    G[s[o], c[o]] = guc[o]
    return S, G


def yon_varyant(S, yon):
    if yon == "uzun":
        return np.where(S > 0, S, 0.0)
    if yon == "kisa":
        return np.where(S < 0, S, 0.0)
    return S


def genisleyen_q(s, x, qs=(0.2, 0.8), en_az=100):
    """Olay duzeyinde genisleyen yuzdelikler: her olay icin yalniz sinyal gunu < s olan olaylardan."""
    o = np.argsort(s, kind="mergesort")
    ss, xs = s[o], x[o]
    out = np.full((len(s), len(qs)), np.nan)
    gunler = np.unique(ss)
    sol = np.searchsorted(ss, gunler, side="left")
    for g, i0 in zip(gunler, sol):
        if i0 < en_az:
            continue
        gecmis = xs[:i0]
        gecmis = gecmis[np.isfinite(gecmis)]
        if len(gecmis) < en_az:
            continue
        qv = np.quantile(gecmis, qs)
        out[o[ss == g]] = qv
    return out


# ----------------------------------------------------------------------------- varyantlar
def varyantlar(v):
    """Her varyant: dict(kid, kural, ad, girdi, h, gece, kor, yon, uni, S, G, rejim_test)."""
    m, B, T = v.m, v.B, v.m.T
    iR, ci = B["iR"].to_numpy(), B["ci"].to_numpy()
    AR = B["AR"].to_numpy()
    uy = B["uyum_rt"].to_numpy()
    ho = B["hacim_oran"].to_numpy()
    out = []

    def ekle(kural, ek, ad, girdi, S, G, h, gece, kor, yon, uni, rejim_test=False):
        S = (yon_varyant(S, yon) * v.U[uni]).astype(np.int8)
        out.append(dict(kid=f"{kural}/{ek}/{uni}/{yon}", kural=kural, ad=ad, girdi=girdi, h=h, gece=gece,
                        kor=kor, yon=yon, uni=uni, S=S, G=G, rejim_test=rejim_test))

    # R6-01 G1: tepki gunu yonunde
    val = np.where(uy & (ho >= 2) & (AR >= 0.05), 1, np.where(uy & (ho >= 2) & (AR <= -0.05), -1, 0))
    S1, G1 = olay_matris(v, iR, ci, val, np.abs(AR))
    # R6-02 G2: |AR| >= 8% donus
    val = np.where(uy & (np.abs(AR) >= 0.08), -np.sign(AR), 0)
    S2, G2 = olay_matris(v, iR, ci, val, np.abs(AR))
    for uni in ("B", "K"):
        for yon in ("iki", "uzun", "kisa"):
            ekle("R6-01", "AR5", "G1 tepki gunu yonunde tasima: AR>=+5% ve hacim>=2x uzun, AR<=-5% kisa",
                 "8-K 2.02 R gunu, r-rSPY, hacim/20g", S1, G1, (1, 2, 3), True, "yok", yon, uni)
            ekle("R6-02", "AR8", "G2 tepki gunu |AR|>=8% ters yon",
                 "8-K 2.02 R gunu, r-rSPY", S2, G2, (1, 2, 3), True, "yok", yon, uni, rejim_test=True)
    # R6-03 So-Wang: t-4 -> t-2 piyasaya gore getiri, genisleyen 20/80 yuzdelik, giris t-2, cikis t+1
    ac = m.A["adjclose"]
    spy = ac[:, m.kpos["SPY"]]
    for tdef, tcol in (("tF", "iF"), ("tR", "iR")):
        t0 = B[tcol].to_numpy()
        s = t0 - 2
        okk = s - 2 >= 0
        pre = np.full(len(B), np.nan)
        pre[okk] = (ac[s[okk], v.kp[ci[okk]]] / ac[s[okk] - 2, v.kp[ci[okk]]]
                    - spy[s[okk]] / spy[s[okk] - 2])
        for uni in ("B", "K"):
            ins = v.U[uni][np.clip(s, 0, T - 1), ci] & okk
            q = np.full((len(B), 2), np.nan)
            q[ins] = genisleyen_q(s[ins], pre[ins])
            val = np.where(pre < q[:, 0], 1, np.where(pre > q[:, 1], -1, 0))
            val = np.where(ins & np.isfinite(q[:, 0]), val, 0)
            S3, G3 = olay_matris(v, s, ci, val, np.abs(pre))
            for yon in ("iki", "uzun", "kisa"):
                ekle("R6-03", tdef, f"G3 So-Wang bilanco oncesi donus (t={'dosyalama' if tdef == 'tF' else 'tepki'} gunu)",
                     "t-4->t-2 getiri - SPY, genisleyen 20/80 yuzdelik", S3, G3, (3,), False, "yok", yon, uni)
    # R6-04 bilanco oncesi prim: R-k'da al (SPY korunmali), cikis R-1 ya da R+1
    for k in (10, 5, 3):
        for cik, hh in (("Rm1", k - 1), ("Rp1", k + 1)):
            s = iR - k
            S4, G4 = olay_matris(v, s, ci, np.ones(len(B)), np.ones(len(B)))
            for uni in ("B", "K"):
                ekle("R6-04", f"k{k}{cik}", f"G4 bilanco oncesi prim: R-{k} kapanisinda al, cikis {'R-1' if cik == 'Rm1' else 'R+1'}",
                     "8-K 2.02 tarihi (onceden ilan varsayimi)", S4, G4, (hh,), False, "SPY:250", "uzun", uni)
    # EK (denetci): aciklamadan h gun once al, R-1 kapanisinda cik (h=2, R6-04 k3Rm1 ile ayni oldugu icin yok)
    for hh in (1, 3):
        s = iR - 1 - hh
        S5, G5 = olay_matris(v, s, ci, np.ones(len(B)), np.ones(len(B)))
        for uni in ("B", "K"):
            ekle("EK", f"h{hh}", f"EK bilanco oncesi prim: R-{1 + hh} kapanisinda al, R-1 kapanisinda cik",
                 "8-K 2.02 tarihi (onceden ilan varsayimi)", S5, G5, (hh,), False, "SPY:250", "uzun", uni)
    # R6-06 Thomas-Zhang: liderin R gunu takipcinin AR'si S; takipcinin R_f-h kapanisinda -sign(S), R_f'de cik
    grup = m.evren.loc[v.kodlar, "grup"].astype(str).to_numpy()
    tar = m.idx[iR]
    sezon = tar.year.to_numpy() * 4 + (tar.month.to_numpy() - 1) // 3
    E = pd.DataFrame({"iR": iR, "ci": ci, "grup": grup[ci], "sezon": sezon})
    lid = E.loc[E.groupby(["grup", "sezon"])["iR"].idxmin(), ["grup", "sezon", "iR", "ci"]]
    lid = lid.rename(columns={"iR": "iL", "ci": "cL"})
    F = E.merge(lid, on=["grup", "sezon"])
    F = F[(F["ci"] != F["cL"]) & (F["iR"] > F["iL"])]
    Sg = v.R[F["iL"].to_numpy(), F["ci"].to_numpy()] - v.rS[F["iL"].to_numpy()]
    for hh in (1, 2):
        okk = (F["iR"].to_numpy() - hh) >= F["iL"].to_numpy()
        val = np.where(okk & (Sg >= 0.03), -1, np.where(okk & (Sg <= -0.03), 1, 0))
        S6, G6 = olay_matris(v, F["iR"].to_numpy() - hh, F["ci"].to_numpy(), val, np.abs(Sg))
        for uni in ("B", "K"):
            for yon in ("iki", "uzun", "kisa"):
                ekle("R6-06", f"h{hh}", f"G6 emsal (grup lideri) tepkisinin takipci bilancosunda donusu, R_f-{hh} giris, R_f cikis",
                     "grup lideri R gunu, takipci r-rSPY", S6, G6, (hh,), False, "yok", yon, uni)
    # R5-07 IRRX: 5 gunluk (hisse - sektor ETF), bilanco haric; kesitsel 20/80
    rel = v.rel
    rel_x = np.where(v.EW, 0.0, rel)
    s5_v1 = pd.DataFrame(rel_x).rolling(5, min_periods=5).sum().to_numpy()
    s5_raw = pd.DataFrame(rel).rolling(5, min_periods=5).sum().to_numpy()
    yakin = pd.DataFrame(v.ER.astype(float)).rolling(5, min_periods=1).max().to_numpy() > 0
    s5_v2 = np.where(yakin, np.nan, s5_raw)
    sig63 = pd.DataFrame(v.R).rolling(63, min_periods=50).std().to_numpy()
    for vk, X in (("v1", s5_v1), ("v2", s5_v2)):
        for alt in ("hepsi", "yuksek_sigma"):
            for uni in ("B", "K"):
                Xu = np.where(v.U[uni] & np.isfinite(sig63), X, np.nan)
                if alt == "yuksek_sigma":
                    sr = pd.DataFrame(np.where(np.isfinite(Xu), sig63, np.nan)).rank(axis=1, pct=True).to_numpy()
                    Xu = np.where(sr > 0.8, Xu, np.nan)
                n_ok = np.isfinite(Xu).sum(axis=1)
                rk = pd.DataFrame(Xu).rank(axis=1, pct=True).to_numpy()
                S7 = np.where(rk <= 0.2, 1.0, np.where(rk > 0.8, -1.0, 0.0))
                S7[n_ok < 10] = 0.0
                S7 = np.nan_to_num(S7)
                G7 = np.nan_to_num(np.abs(rk - 0.5))
                for yon in ("iki", "uzun", "kisa"):
                    ekle("R5-07", f"{vk}_{alt}", f"R5-7 IRRX 5g sektore gore donus ({'bilanco gunleri cikarilmis' if vk == 'v1' else 'bilanco yakininda dislanmis'}, {alt})",
                         "5g (hisse-sektor ETF), bilanco penceresi", S7, G7, (1, 2, 3), True, "SPY:250", yon, uni)
    # R5-08: |hisse - sektor| >= esik; (a) tepki gunu yonunde, (b) bilancosuz gunde ters
    absr = np.abs(rel)
    ERu = np.zeros_like(v.ER)
    ERu[iR[uy], ci[uy]] = True
    for esik in (0.05, 0.07, 0.10):
        Sa = np.where(ERu & (absr >= esik), np.sign(rel), 0.0)
        Sb = np.where(~v.EW & (absr >= esik), -np.sign(rel), 0.0)
        Gg = np.nan_to_num(absr)
        for alt, Sx in (("a", np.nan_to_num(Sa)), ("b", np.nan_to_num(Sb))):
            for uni in ("B", "K"):
                for yon in ("iki", "uzun", "kisa"):
                    ekle("R5-08", f"{alt}{int(esik * 100)}",
                         f"R5-8 |hisse-sektor|>={int(esik * 100)}%: " + ("tepki gunu yonunde (suruklenme)" if alt == "a" else "bilancosuz gunde ters (donus)"),
                         "hisse-sektor ETF ayni gun, bilanco tarihleri", Sx, Gg, (1, 2, 3), True, "SPY:250", yon, uni)
    return out


def tek_yonlu(var):
    return var["yon"] in ("uzun", "kisa")


def gecti(row, tek, t_esik=2.0):
    ok = (row["net_bps"] > 0) and (row["t_kume"] >= t_esik)
    if tek:
        ok = ok and (row["anormal_bps"] > 0) and (row["t_anormal"] >= t_esik)
    return bool(ok)


def deg(m, var, S=None, **kw):
    S = var["S"] if S is None else S
    sdf = pd.DataFrame(S, index=m.idx, columns=VERI_V.kodlar)
    gdf = pd.DataFrame(var["G"], index=m.idx, columns=VERI_V.kodlar)
    nz = (S != 0).any(axis=0)
    if not nz.any():
        return None
    sdf, gdf = sdf.loc[:, nz], gdf.loc[:, nz]
    notlar = f"varyant={var['kid']}; evren={'buyuk' if var['uni'] == 'B' else 'kucuk/tema'}; yayin={YAYIN[var['kural']]}"
    if var["kor"] == "SPY:250" and var["kural"] in ("R5-07", "R5-08"):
        notlar += "; sektor korunmasi yerine SPY"
    notlar = kw.pop("notlar_ek", "") + notlar
    return m.degerlendir(sdf, kural_id=var["kid"], aile="G", ad=var["ad"], girdi=var["girdi"],
                         guc=gdf, notlar=notlar, **kw)


VERI_V = None


# ----------------------------------------------------------------------------- asamalar
def asama_is(m, vs):
    satir, aday = [], []
    for var in vs:
        r = deg(m, var, h=var["h"], giris=("K",), gece=var["gece"], korunma=(var["kor"],), komisyon=("hisse",),
                donemler=["IS"], rejimler=var["rejim_test"], bootstrap=False, notlar_ek="asama=IS; ")
        if r is None:
            continue
        satir.append(r)
        rejs = ["hepsi", "V<20", "V>30"] if var["rejim_test"] else ["hepsi"]
        for _, x in r[r["rejim"].isin(rejs)].iterrows():
            aday.append({"kid": var["kid"], "kural": var["kural"], "uni": var["uni"], "yon_var": var["yon"],
                         "h": int(x["h"]), "cikis": x["cikis"], "rejim": x["rejim"], "korunma": var["kor"],
                         "n_islem": x["n_islem"], "is_net_bps": x["net_bps"], "is_anormal_bps": x["anormal_bps"],
                         "is_t_kume": x["t_kume"], "is_t_anormal": x["t_anormal"],
                         "aday": gecti(x, tek_yonlu(var)) and x["n_islem"] >= 10})
    A = pd.DataFrame(aday)
    A.to_csv(ADAY, index=False)
    return pd.concat(satir, ignore_index=True), A


def asama_oos(m, vs, A):
    byk = {v["kid"]: v for v in vs}
    C = A[A["aday"]]
    satir, tar = [], []
    for kid, g in C.groupby("kid", sort=False):
        var = byk[kid]
        hs = tuple(sorted({int(h) for h in g["h"] if h > 0}))
        gece = bool((g["cikis"] == "acilis").any())
        r = deg(m, var, h=hs or (1,), giris=("K",), gece=gece, korunma=(var["kor"],), komisyon=("hisse",),
                donemler=["OOS"], rejimler=var["rejim_test"], bootstrap="tum" if var["rejim_test"] else True,
                notlar_ek="asama=OOS; ")
        satir.append(r)
        for _, a in g.iterrows():
            x = r[(r["h"] == a["h"]) & (r["cikis"] == a["cikis"]) & (r["rejim"] == a["rejim"])]
            if not len(x):
                continue
            x = x.iloc[0]
            p = x["p_bootstrap"] if np.isfinite(x["p_bootstrap"]) else 1.0
            tar.append({**a.to_dict(), "oos_n": x["n_islem"], "oos_net_bps": x["net_bps"],
                        "oos_anormal_bps": x["anormal_bps"], "oos_t_kume": x["t_kume"],
                        "oos_t_anormal": x["t_anormal"], "oos_p": p,
                        "oos_gecti": gecti(x, tek_yonlu(var))})
    Tt = pd.DataFrame(tar)
    Tt.to_csv(OOS_TARAMA, index=False)
    return (pd.concat(satir, ignore_index=True) if satir else None), Tt


def asama_tam(m, vs, Tt):
    byk = {v["kid"]: v for v in vs}
    G = Tt[Tt["oos_gecti"]] if len(Tt) else Tt
    satir = []
    for kid, g in G.groupby("kid", sort=False):
        var = byk[kid]
        hs = tuple(sorted({int(h) for h in g["h"] if h > 0})) or (1,)
        r = deg(m, var, h=hs, giris=("K", "A", "G"), gece=var["gece"], korunma=("yok", "SPY:250", "SPY:60"),
                donemler=None, rejimler=True, bootstrap=True, notlar_ek="asama=tam; ")
        satir.append(r)
    return pd.concat(satir, ignore_index=True) if satir else None


def tepki_denetim(v):
    B = v.B
    tam = B[(B["iR"] + 1 < v.m.T)]
    rng = np.random.default_rng(TOHUM)
    orn = tam.iloc[rng.choice(len(tam), 50, replace=False)]
    d = pd.DataFrame([
        {"olcu": "olay_sayisi_ham", "deger": v.n_ham},
        {"olcu": "ayni_ceyrek_tekrar_atilan", "deger": v.n_tekrar},
        {"olcu": "olay_sayisi", "deger": len(B)},
        {"olcu": "uyusmazlik_tam_yontem_tum", "deger": round(1 - tam["uyum_lit"].mean(), 4)},
        {"olcu": "uyusmazlik_tam_yontem_50orneklem", "deger": round(1 - orn["uyum_lit"].mean(), 4)},
        {"olcu": "uyusmazlik_gercek_zaman_tum(hacimR<hacimR-1)", "deger": round(1 - B["uyum_rt"].mean(), 4)},
        {"olcu": "uyusmazlik_yalniz_R+1_kaynakli", "deger": round((tam["uyum_rt"] & ~tam["uyum_lit"]).mean(), 4)},
    ])
    for s in ("KAPANIS_SONRASI", "ACILIS_ONCESI", "SEANS_ICI"):
        x = tam[tam["seans"] == s]
        d.loc[len(d)] = {"olcu": f"uyusmazlik_tam_{s}", "deger": round(1 - x["uyum_lit"].mean(), 4)}
    orn[["kod", "filing_date", "seans", "ilk_tepki_gunu", "uyum_lit", "uyum_rt", "hacim_oran"]].to_csv(
        DENETIM.replace(".csv", "_orneklem.csv"), index=False)
    d.to_csv(DENETIM, index=False)
    return d


def asama_bugun(m, v):
    """23.11-18.12.2026 icin beklenen bilanco gunleri (tahmini): bir yil onceki ayni ceyrek + 364 gun;
    ikinci tahmin son 4 aralik ortancasi. Son olay tahminden 45 gunden yakinsa zaten aciklamis sayilir."""
    B = v.B
    bas, bit = pd.Timestamp("2026-11-23"), pd.Timestamp("2026-12-18")
    sat = []
    for k, g in B.groupby("kod"):
        d = pd.DatetimeIndex(m.idx[g["iR"].to_numpy()]).sort_values()
        d = d[d <= pd.Timestamp("2026-11-20")]
        if len(d) < 4:
            continue
        son4 = d[-4:]
        aral = np.median(np.diff(son4.values).astype("timedelta64[D]").astype(int))
        t2 = d[-1] + pd.Timedelta(days=int(aral))
        onc = d[(d >= bas - pd.Timedelta(days=372)) & (d <= bit - pd.Timedelta(days=357))]
        t1 = onc[0] + pd.Timedelta(days=364) if len(onc) else pd.NaT
        tah = t1 if pd.notna(t1) else t2
        if not (bas <= tah <= bit):
            if not (bas <= t2 <= bit):
                continue
            tah = t2
        if (tah - d[-1]).days < 45:
            continue
        sat.append({"kod": k, "tahmini_tepki_gunu": tah.date(), "yontem": "yil_once+364" if tah == t1 else "son4_aralik",
                    "ikinci_tahmin": t2.date(), "son_tepki_gunu": d[-1].date(),
                    "gecen_yil_tepki": (onc[0].date() if len(onc) else None),
                    "seans_son": g["seans"].iloc[-1],
                    "evren": "buyuk" if v.U["B"][-1, v.c[k]] else "kucuk/tema", "grup": m.evren.at[k, "grup"],
                    "etiket": "tahmini"})
    d = pd.DataFrame(sat).sort_values("tahmini_tepki_gunu")
    d.to_csv(BUGUN, index=False)
    return d


# ----------------------------------------------------------------------------- R6-03 tanilari (OOS'tan gecen tek kural)
TANI = os.path.join(VERI, "K7_tani_R6-03.csv")


def so_wang(v, tcol="iR", uni="B", q=(0.2, 0.8), win=2, fiyat_s=None):
    """R6-03 olay tablosu: s = t0-2 sinyal gunu, pre = P[s]/P[s-win] - SPY ayni; genisleyen q yuzdelikleri.
    fiyat_s: (hisse_fiyat_dizisi, spy_fiyat_dizisi) verilirse s gunu fiyati bundan alinir (15:30 testi;
    oran ham kapanis olcegiyle kurulur)."""
    m, B, T = v.m, v.B, v.m.T
    ci = B["ci"].to_numpy()
    t0 = B[tcol].to_numpy()
    s = t0 - 2
    okk = s - win >= 0
    ss, kk = np.clip(s, win, T - 1), v.kp[ci]
    ac = m.A["adjclose"]
    spy = ac[:, m.kpos["SPY"]]
    pre = np.where(okk, ac[ss, kk] / ac[ss - win, kk] - spy[ss] / spy[ss - win], np.nan)
    ins = v.U[uni][np.clip(s, 0, T - 1), ci] & okk
    qq = np.full((len(B), 2), np.nan)
    qq[ins] = genisleyen_q(s[ins], pre[ins], qs=q)
    if fiyat_s is not None:
        ph, ps = fiyat_s
        cl = m.A["close"]
        pre = ph / cl[ss - win, kk] - ps / cl[ss - win, m.kpos["SPY"]]
    val = np.where(pre < qq[:, 0], 1, np.where(pre > qq[:, 1], -1, 0))
    val = np.where(ins & np.isfinite(qq[:, 0]), val, 0)
    return s, ci, val, pre, qq, ins


def asama_tani(m, v):
    sat, ozet = [], []

    def kaydet(kid, ad, S, G, h=(3,), kor=("yok", "SPY:250"), donem=None):
        var = dict(kid=kid, kural="R6-03", uni="B", ad=ad, girdi="t-4->t-2 getiri - SPY", G=G, kor="yok")
        r = deg(m, var, S=S, h=h, giris=("K",), gece=False, korunma=kor, komisyon=("hisse",),
                donemler=donem or ["IS", "OOS", "SON", "TUM"], rejimler=False, bootstrap=True,
                notlar_ek="asama=tani; ")
        sat.append(r)
        return r

    # 1) taban: buyuk evrende butun olaylar, R-2 kapanisinda al, R+1 kapanisinda cik
    B = v.B
    s, ci, val, pre, qq, ins = so_wang(v)
    S0, G0 = olay_matris(v, s, ci, np.where(ins & np.isfinite(qq[:, 0]), 1, 0), np.abs(np.nan_to_num(pre)) + 1e-9)
    kaydet("R6-03/tR/B/tum_olaylar(tani)", "Taban: butun bilanco olaylari R-2 al, R+1 cik", (S0 * v.U["B"]).astype(np.int8), G0)
    # 2) komsu parametreler
    for q, win, ek in (((0.15, 0.85), 2, "q15"), ((0.25, 0.75), 2, "q25"), ((0.2, 0.8), 1, "w1"), ((0.2, 0.8), 3, "w3")):
        s, ci, val, pre, qq, ins = so_wang(v, q=q, win=win)
        S1, G1 = olay_matris(v, s, ci, np.where(val > 0, 1, 0), np.abs(pre))
        kaydet(f"R6-03/tR/B/uzun/{ek}(komsu)", f"G3 So-Wang uzun bacak, komsu parametre {ek}", (S1 * v.U["B"]).astype(np.int8), G1)
    # 3) VIX>30 bolumleri (TUM), K, h=3, yok ve SPY:250
    s, ci, val, pre, qq, ins = so_wang(v)
    SL, GL = olay_matris(v, s, ci, np.where(val > 0, 1, 0), np.abs(pre))
    SL = (SL * v.U["B"]).astype(np.int8)
    sdf = pd.DataFrame(SL, index=m.idx, columns=v.kodlar)
    gdf = pd.DataFrame(GL, index=m.idx, columns=v.kodlar)
    for kor in ("yok", "SPY:250"):
        isl = m.islemler(sdf, giris="K", h=3, korunma=kor, guc=gdf)
        tab, oz = m.bolum_ozeti(isl, "hisse")
        tab.to_csv(TANI.replace(".csv", f"_bolum_{kor.replace(':', '')}.csv"), index=False)
        ozet.append({"olcu": f"vix30_bolum_{kor}", "deger": str({k: (round(x, 2) if isinstance(x, float) else x) for k, x in oz.items()})})
        if kor == "yok":
            isl_k = isl
    # 4) 15:30 gercekcilik testi (son ~730 gun)
    from yukle import saatlik
    H = saatlik()
    p15 = H["acilis_1530"]
    T = m.T
    hp = np.full(len(B), np.nan)
    sp = np.full(len(B), np.nan)
    tar = m.idx[np.clip(s, 0, T - 1)]
    for j, (k, d) in enumerate(zip(np.array(v.kodlar)[ci], tar)):
        if d in p15.index and k in p15.columns:
            hp[j] = p15.at[d, k]
            sp[j] = p15.at[d, "SPY"] if "SPY" in p15.columns else np.nan
    s2, ci2, val2, pre2, qq2, ins2 = so_wang(v, fiyat_s=(hp, sp))
    pencere = np.isfinite(hp) & np.isfinite(sp) & ins
    kapanis_tet = pencere & (val > 0)
    s1530_tet = pencere & (val2 > 0)
    ort = (kapanis_tet & s1530_tet).sum()
    S15, G15 = olay_matris(v, s, ci, np.where(s1530_tet, 1, 0), np.abs(np.nan_to_num(pre2)) + 1e-9)
    S15 = (S15 * v.U["B"]).astype(np.int8)
    SK, GK = olay_matris(v, s, ci, np.where(kapanis_tet, 1, 0), np.abs(np.nan_to_num(pre)) + 1e-9)
    SK = (SK * v.U["B"]).astype(np.int8)
    i15 = m.islemler(pd.DataFrame(S15, index=m.idx, columns=v.kodlar), giris="K", h=3, korunma="yok",
                     guc=pd.DataFrame(G15, index=m.idx, columns=v.kodlar))
    iK = m.islemler(pd.DataFrame(SK, index=m.idx, columns=v.kodlar), giris="K", h=3, korunma="yok",
                    guc=pd.DataFrame(GK, index=m.idx, columns=v.kodlar))
    ozet += [{"olcu": "1530_pencere_olay", "deger": int(pencere.sum())},
             {"olcu": "1530_kapanis_tetik", "deger": int(kapanis_tet.sum())},
             {"olcu": "1530_tetik", "deger": int(s1530_tet.sum())},
             {"olcu": "1530_ortusme_orani(kapanis tetiklerinin)", "deger": round(ort / max(kapanis_tet.sum(), 1), 3)},
             {"olcu": "1530_net_bps_kapanis_sinyal", "deger": round(iK["net_hisse"].mean() * 1e4, 1)},
             {"olcu": "1530_net_bps_1530_sinyal", "deger": round(i15["net_hisse"].mean() * 1e4, 1)},
             {"olcu": "1530_korunan_oran", "deger": round(i15["net_hisse"].mean() / iK["net_hisse"].mean(), 3)},
             {"olcu": "1530_n_islem_1530", "deger": len(i15)}]
    # 5) bugun: guncel esik (20.11.2026'ya kadarki butun olaylar)
    son = ins & np.isfinite(pre) & (s <= T - 1)
    gq = np.quantile(pre[son & (s < T)], [0.2, 0.8])
    ozet.append({"olcu": "guncel_q20_q80_(t-4->t-2, SPY'ye gore)", "deger": f"{gq[0]:.4f} / {gq[1]:.4f}"})
    # yil bazinda
    isl_k["yil"] = pd.DatetimeIndex(isl_k["t"]).year
    yb = isl_k.groupby("yil")["net_hisse"].agg(["count", "mean"])
    ozet.append({"olcu": "yil_net_bps", "deger": "; ".join(f"{y}:{int(r['count'])}/{r['mean'] * 1e4:.0f}" for y, r in yb.iterrows())})
    pd.DataFrame(ozet).to_csv(TANI, index=False)
    return pd.concat(sat, ignore_index=True), pd.DataFrame(ozet), gq


def main(asama="hepsi"):
    global VERI_V
    t0 = time.time()
    m = M.Motor()
    v = Veri(m)
    VERI_V = v
    vs = varyantlar(v)
    print(f"hazirlik {time.time() - t0:.0f} sn; {len(vs)} varyant cagrisi; {len(v.B)} olay, {len(v.kodlar)} hisse")
    if asama in ("hepsi", "bakis"):
        def imza(mm):
            vv = Veri(mm)
            w = np.arange(1, len(vv.kodlar) + 1, dtype=float)
            return pd.DataFrame({x["kid"]: (x["S"] * w).sum(axis=1) for x in varyantlar(vv)}, index=mm.idx)
        tamam, rap = m.bakis_testi(imza)
        print("bakis_testi:", tamam, rap)
        assert tamam, rap
    if asama in ("hepsi", "denetim", "is"):
        print(tepki_denetim(v).to_string(index=False))
    if asama in ("hepsi", "is"):
        R, A = asama_is(m, vs)
        M.yaz_sonuc(R, SONUC)
        print(f"IS: {len(A)} test, {int(A['aday'].sum())} aday ({time.time() - t0:.0f} sn)")
    if asama in ("hepsi", "oos"):
        A = pd.read_csv(ADAY)
        R, Tt = asama_oos(m, vs, A)
        if R is not None:
            M.yaz_sonuc(R, SONUC, ekle=True)
        print(f"OOS: {len(Tt)} aday satiri, {int(Tt['oos_gecti'].sum()) if len(Tt) else 0} gecti ({time.time() - t0:.0f} sn)")
    if asama in ("hepsi", "tam"):
        Tt = pd.read_csv(OOS_TARAMA)
        R = asama_tam(m, vs, Tt)
        if R is not None:
            M.yaz_sonuc(R, SONUC, ekle=True)
        print(f"tam: {0 if R is None else len(R)} satir ({time.time() - t0:.0f} sn)")
    if asama in ("hepsi", "tani"):
        R, oz, gq = asama_tani(m, v)
        M.yaz_sonuc(R, SONUC, ekle=True)
        print(oz.to_string(index=False))
    if asama in ("hepsi", "bugun"):
        print(asama_bugun(m, v).to_string(index=False))
    return m, v, vs


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "hepsi")
