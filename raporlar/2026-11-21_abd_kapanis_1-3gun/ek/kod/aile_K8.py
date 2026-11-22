# -*- coding: utf-8 -*-
"""aile_K8.py - Aile S: sistematik lead-lag taramasi ve boru hatti plasebosu (YONTEM 7, "S").

Tek komut:   python3 -I aile_K8.py hepsi        (plasebo dahil ~25-40 dk; asamalar ayri da calisir)
Asamalar:    python3 -I aile_K8.py is            hazirlik + IS taramasi -> veri/aday_K8.csv (OOS'a bakmaz)
             python3 -I aile_K8.py oos           aday dosyasini okur, OOS onayi + BH %10
             python3 -I aile_K8.py plasebo perm 0 50     plasebo parcasi (tip: perm | kaydir; [bas, son) )
             python3 -I aile_K8.py ozet          plasebo ozeti, tekil plasebo p-degerleri
             python3 -I aile_K8.py degerlendir   islem bazinda sinama -> veri/sonuc_K8.csv
Ara sonuclar: scratchpad/tarama/ (ham veri depoya yazilmaz).

Tarama tanimi (hepsi IS verisiyle ya da veriden bagimsiz, OOS'a bakmadan sabitlendi):
  * Evren: |korelasyon| > 0,98 olanlar teke indirilir (IS). SPY (korunma/kontrol) ve ^IRX (yuzde getiri anlamsiz) disarida.
  * Sepetler: kapanis sinifina gore ayri kumelenir (ABD16 <= 46, ONCE <= 4, SONRA <= 10; toplam <= 60).
    SONRA sepetleri 1 gun gecikmeli, ONCE ve ABD16 ayni gun (motor.artik_getiri guvenli=True).
  * X = sepet uyelerinin artik getirilerinin (X - b*SPY - b*sektor, kayan 250 gun) esit agirlikli ortalamasi.
  * Y = hedefin SPY ile korunmali ileri getirisi (giris K, h = 1,2,3). Hedef: ABD16, islem goren,
    60 gunluk dolar hacmi >= 200 mln $, o gune kadar sifir hacimli gunu yok (motor.tarama_hedef_maskesi).
    Duzey 'uye': tek kod. Duzey 'sepet': sepetin o gun uygun uyelerinin ortalamasi (>= 2 hedef uyeli sepetler).
  * Regresyon: Y ~ a + b*X + c*Y_t + d*SPY_t (motor.tarama_regresyon; h>1 icin Newey-West hac=h-1).
  * Sepet -> kendi uyesi: X o uye cikarilarak (birini-disarida-birak) hesaplanir. Sepet -> kendisi sinanmaz.
  * IS: |t| >= 3,5 olanlarin en yuksek 200'u aday. OOS: ayni yonde tek yanli p, 200 aday uzerinde BH %10.
  * Plasebo 1: hedef tarafi (Y, Y_t, SPY_t) motor.blok_permutasyon ile (20 gun, ayni yil x VIX kovasi) yer degistirir.
    Plasebo 2: X matrisi +40..+250 gun dairesel kayar (motor.dairesel_kaydir). Zincirin tamami yeniden calisir.
  * Islem kurali (OOS'a bakmadan yazildi): z = z_skor(X, 250); |z| > 1 ise yon = isaret(b_IS) * isaret(z),
    hedef(ler)de K girisi, h = taramadaki h, SPY:250 korunmali. Izgara: pencere 60/250, esik 1/2.
"""
import os
import sys
import time
import pickle
import warnings
from math import erfc, sqrt

import numpy as np
import pandas as pd

KOD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOD)
import motor as M  # noqa: E402

VERI = M.VERI_DIZIN
ARA = os.environ.get("TARAMA_DIZIN",
                     "/tmp/claude-0/-home-user-Xxxx/b23916bf-451a-5d36-8905-d1866417ce1f/scratchpad/tarama")
ADAY = os.path.join(VERI, "aday_K8.csv")
SONUC = os.path.join(VERI, "sonuc_K8.csv")
H = (1, 2, 3)
T_ESIK, N_ADAY, BH_Q = 3.5, 200, 0.10
K_SINIF = ((0, 46), (1, 4), (2, 10))          # ABD16, ONCE, SONRA sepet sayilari (toplam <= 60)
ADV_ALT = 200e6
warnings.filterwarnings("ignore", category=RuntimeWarning)


def nanort(a):
    c = np.isfinite(a).sum(axis=1)
    s = np.nansum(a, axis=1)
    return np.where(c > 0, s / np.maximum(c, 1), np.nan)


# ----------------------------------------------------------------------------- hazirlik
def hazirla(m):
    ev = m.evren
    IS = M.donem_maskesi(m.idx, "IS")
    R = m.getiri("kk", ham=True)
    dv = pd.DataFrame(m.A["close"] * m.A["volume"], index=m.idx, columns=m.kodlar)
    isdv = dv[IS].mean().fillna(0.0)
    sinif = ev["kapanis_sinifi"].astype(str)
    sno = sinif.map({"ABD16": 0, "ONCE": 1}).fillna(2).astype(int)
    kald = (ev["kaldirac"].astype(float) != 1.0).astype(int)
    sira = pd.DataFrame({"k": kald, "s": sno, "v": -isdv}).sort_values(["k", "s", "v"], kind="mergesort").index.tolist()
    sira = ["SPY"] + [c for c in sira if c != "SPY"]           # likit ve kaldiracsiz olan basta
    tut, harita = m.tekillestir(sira, 0.98, "IS")
    C = R.loc[IS, tut].corr(min_periods=250).to_numpy()        # ters urunler: korelasyon < -0,98
    tut2 = []
    for i, k in enumerate(tut):
        es = next((j for j in tut2 if np.isfinite(C[i, j]) and C[i, j] < -0.98), None)
        if es is None:
            tut2.append(i)
        else:
            harita[k] = "-" + tut[es]
    tut = [tut[i] for i in tut2]
    evr = [c for c in tut if c not in ("SPY", "^IRX")]
    # kumeleme: kapanis sinifina gore ayri
    kume = pd.Series(-1, index=evr, dtype=int)
    ofs = 0
    for s, k in K_SINIF:
        ks = [c for c in evr if sno[c] == s]
        if not ks:
            continue
        km = m.kumele(ks, k=min(k, len(ks)), donem="IS")
        iyi = km[km >= 0]
        kume[iyi.index] = iyi + ofs
        ofs += int(iyi.max()) + 1 if len(iyi) else 0
    uye = kume[kume >= 0]
    K = int(uye.max()) + 1
    A = m.artik_getiri(list(uye.index), "SPY", "oto", 250, True)
    An = A.to_numpy(float)
    kno = uye.to_numpy()
    X = np.column_stack([nanort(An[:, kno == k]) for k in range(K)])
    # hedefler
    E = m.tarama_hedef_maskesi(ADV_ALT)
    hed = [c for c in evr if sinif[c] == "ABD16" and np.isfinite(ev.at[c, "maliyet_bps"])
           and int(E.loc[IS, c].sum()) >= 250]
    En = E[hed].to_numpy()
    Rh = R[hed].to_numpy(float)
    hk = np.array([int(kume.get(c, -1)) for c in hed])          # hedefin sepeti (-1: sepetsiz)
    FHu = {h: np.where(En, m.ileri_korunmali("K", h, "kapanis", "SPY", 250, kodlar=hed).to_numpy(float), np.nan)
           for h in H}
    CYu = np.where(En, Rh, np.nan)
    # birini-disarida-birak X (hedef kendi sepetindeyse)
    apos = {c: i for i, c in enumerate(uye.index)}
    LOO = np.full((m.T, len(hed)), np.nan)
    for j, c in enumerate(hed):
        k = hk[j]
        if k < 0:
            continue
        blk = An[:, kno == k]
        if blk.shape[1] < 2:
            continue
        aj = An[:, apos[c]]
        cnt = np.isfinite(blk).sum(axis=1) - np.isfinite(aj)
        LOO[:, j] = np.where(cnt > 0, (np.nansum(blk, axis=1) - np.nan_to_num(aj)) / np.maximum(cnt, 1), np.nan)
    # hedef sepetleri (>= 2 hedef uye)
    ysep = [k for k in range(K) if (hk == k).sum() >= 2]
    FH, CY = {}, None
    for h in H:
        FH[h] = np.column_stack([FHu[h]] + [nanort(FHu[h][:, hk == k]) for k in ysep])
    CY = np.column_stack([CYu] + [nanort(CYu[:, hk == k]) for k in ysep])
    spy = R["SPY"].to_numpy(float)
    D = {"evr": evr, "harita": harita, "kume": kume, "K": K, "X": X, "LOO": LOO, "hed": hed, "hk": hk,
         "ysep": ysep, "FH": FH, "CY": CY, "spy": spy, "Nm": len(hed),
         "yad": hed + [f"S{k:02d}" for k in ysep],
         "IS": IS, "OOS": M.donem_maskesi(m.idx, "OOS"), "idx": m.idx}
    return D


def yukle_D(m=None, zorla=False):
    os.makedirs(ARA, exist_ok=True)
    yol = os.path.join(ARA, "hazirlik.pkl")
    if os.path.exists(yol) and not zorla:
        with open(yol, "rb") as f:
            return pickle.load(f)
    D = hazirla(m or M.Motor())
    with open(yol, "wb") as f:
        pickle.dump(D, f, protocol=4)
    return D


# ----------------------------------------------------------------------------- tarama
def tara(D, X, LOO, FH, CY, spy, rows, ycols=None):
    """Bir donem (rows) icin butun (sepet, hedef, h) ciftlerinin b, t, n degerleri: {h: (B, T, N)} K x Ntot."""
    K, Nm = D["K"], D["Nm"]
    hk, ysep = D["hk"], D["ysep"]
    Ntot = Nm + len(ysep)
    Xr = np.array(X[rows], float)
    Lr = LOO[rows]
    sp = spy[rows]
    cols = range(Ntot) if ycols is None else sorted(set(int(c) for c in ycols))
    out = {}
    for h in H:
        Y = FH[h][rows]
        C = CY[rows]
        B = np.full((K, Ntot), np.nan)
        TT = np.full((K, Ntot), np.nan)
        NN = np.zeros((K, Ntot))
        sc = [c for c in cols if c >= Nm]
        if sc:
            b, t, n = M.tarama_regresyon(Xr, Y[:, sc], kontrol_y=C[:, sc], kontrol_ortak=sp, hac=h - 1)
            B[:, sc], TT[:, sc], NN[:, sc] = b, t, n
            for c in sc:                               # sepet -> kendisi sinanmaz
                B[ysep[c - Nm], c] = np.nan
                TT[ysep[c - Nm], c] = np.nan
        for j in cols:
            if j >= Nm:
                continue
            k = hk[j]
            if k >= 0:
                eski = Xr[:, k].copy()
                Xr[:, k] = Lr[:, j]
            b, t, n = M.tarama_regresyon(Xr, Y[:, [j]], kontrol_y=C[:, [j]], kontrol_ortak=sp, hac=h - 1)
            if k >= 0:
                Xr[:, k] = eski
            B[:, j], TT[:, j], NN[:, j] = b[:, 0], t[:, 0], n[:, 0]
        out[h] = (B, TT, NN)
    return out


def aday_sec(tis):
    Tall = np.stack([tis[h][1] for h in H])
    a = np.abs(Tall)
    a[~np.isfinite(a)] = 0.0
    n35 = int((a >= T_ESIK).sum())
    flat = np.argsort(-a, axis=None, kind="mergesort")[:N_ADAY]
    flat = flat[a.ravel()[flat] >= T_ESIK]
    return Tall, a, n35, flat


def tek_yanli_p(z):
    z = np.asarray(z, float)
    return np.array([0.5 * erfc(v / sqrt(2.0)) if np.isfinite(v) else 1.0 for v in z])


def boru_hatti(D, X, LOO, FH, CY, spy):
    """IS secimi -> OOS onayi zincirinin tamami. Donus: ozet sozlugu."""
    tis = tara(D, X, LOO, FH, CY, spy, D["IS"])
    Tall, a, n35, flat = aday_sec(tis)
    o = {"n_test": int(np.isfinite(Tall).sum()), "n35": n35, "n_aday": int(len(flat)),
         "maks_t_is": float(a.max()), "n_gecen": 0, "maks_z_oos": np.nan, "n_z2": 0, "n_z3": 0}
    if len(flat) == 0:
        return o
    _, _, yc = np.unravel_index(flat, Tall.shape)
    toos = tara(D, X, LOO, FH, CY, spy, D["OOS"], ycols=yc)
    Toos = np.stack([toos[h][1] for h in H])
    z = np.sign(Tall.ravel()[flat]) * Toos.ravel()[flat]
    red, _ = M.bh(tek_yanli_p(z), BH_Q)
    o.update({"n_gecen": int(red.sum()), "maks_z_oos": float(np.nanmax(z)) if np.isfinite(z).any() else np.nan,
              "n_z2": int((z >= 2).sum()), "n_z3": int((z >= 3).sum())})
    return o


# ----------------------------------------------------------------------------- asamalar
def asama_is():
    t0 = time.time()
    m = M.Motor()
    D = yukle_D(m, zorla=True)
    K, Nm = D["K"], D["Nm"]
    kume = D["kume"]
    print(f"evren {len(D['evr'])} kod (teke indirilen {len(D['harita'])}), sepet {K}, hedef uye {Nm}, "
          f"hedef sepet {len(D['ysep'])}  [{time.time() - t0:.0f} sn]")
    boy = kume[kume >= 0].value_counts().sort_index()
    print("sepet boylari:", boy.to_dict())
    tis = tara(D, D["X"], D["LOO"], D["FH"], D["CY"], D["spy"], D["IS"])
    Tall, a, n35, flat = aday_sec(tis)
    n_test = int(np.isfinite(Tall).sum())
    hi, xi, yi = np.unravel_index(flat, Tall.shape)
    uy = {k: ";".join(kume.index[kume == k]) for k in range(K)}
    sat = []
    for r, (h_i, x, y) in enumerate(zip(hi, xi, yi), 1):
        h = H[h_i]
        B, TT, NN = tis[h]
        duzey = "uye" if y < Nm else "sepet"
        sat.append({"aday_id": f"S-{r:03d}", "x_sepet": int(x), "x_uyeler": uy[int(x)], "y": D["yad"][y],
                    "y_no": int(y), "duzey": duzey, "h": h,
                    "ayni_sepet": bool(duzey == "uye" and D["hk"][y] == x),
                    "b_is": B[x, y], "t_is": TT[x, y], "n_is": int(NN[x, y]),
                    "y_uyeler": D["yad"][y] if duzey == "uye" else ";".join(
                        c for c, k in zip(D["hed"], D["hk"]) if k == D["ysep"][y - Nm])})
    ad = pd.DataFrame(sat)
    ad.to_csv(ADAY, index=False)
    pd.Series({"n_test": n_test, "n35": n35, "n_aday": len(ad), "K": K, "Nm": Nm, "Nysep": len(D["ysep"]),
               "n_evren": len(D["evr"]), "n_tekil_atilan": len(D["harita"])}).to_csv(os.path.join(ARA, "is_ozet.csv"))
    kume.rename("sepet").to_csv(os.path.join(ARA, "sepetler.csv"))
    print(f"IS: test {n_test}, |t|>={T_ESIK}: {n35}, aday {len(ad)} -> {ADAY}  [{time.time() - t0:.0f} sn]")
    print(ad.head(25)[["aday_id", "x_sepet", "y", "duzey", "h", "ayni_sepet", "b_is", "t_is", "n_is"]].to_string(index=False))
    print("aday dagilimi: duzey", ad.duzey.value_counts().to_dict(), "h", ad.h.value_counts().to_dict(),
          "ayni_sepet", int(ad.ayni_sepet.sum()), "isaret+", int((ad.t_is > 0).sum()))


def asama_oos():
    D = yukle_D()
    ad = pd.read_csv(ADAY)
    toos = tara(D, D["X"], D["LOO"], D["FH"], D["CY"], D["spy"], D["OOS"], ycols=ad.y_no.tolist())
    ad["b_oos"] = [toos[h][0][x, y] for h, x, y in zip(ad.h, ad.x_sepet, ad.y_no)]
    ad["t_oos"] = [toos[h][1][x, y] for h, x, y in zip(ad.h, ad.x_sepet, ad.y_no)]
    ad["n_oos"] = [int(toos[h][2][x, y]) for h, x, y in zip(ad.h, ad.x_sepet, ad.y_no)]
    ad["z_oos"] = np.sign(ad.t_is) * ad.t_oos
    ad["p_oos"] = tek_yanli_p(ad.z_oos)
    red, q = M.bh(ad.p_oos.to_numpy(), BH_Q)
    ad["bh_gecti"], ad["q_oos"] = red, q
    ad.to_csv(os.path.join(ARA, "oos_onay.csv"), index=False)
    print(f"OOS: aday {len(ad)}, ayni yon {(ad.z_oos > 0).sum()}, z>=2: {(ad.z_oos >= 2).sum()}, "
          f"z>=3: {(ad.z_oos >= 3).sum()}, BH %10 gecen: {int(red.sum())}, maks z: {ad.z_oos.max():.2f}")
    g = ad[ad.bh_gecti].sort_values("z_oos", ascending=False)
    print(g[["aday_id", "x_sepet", "y", "duzey", "h", "ayni_sepet", "t_is", "t_oos", "p_oos", "q_oos", "n_oos"]].to_string(index=False))
    return ad


def asama_plasebo(tip, bas, son):
    t0 = time.time()
    m = M.Motor()
    D = yukle_D(m)
    ms = D["IS"] | D["OOS"]
    sat = []
    for r in range(bas, son):
        if tip == "perm":
            rng = np.random.default_rng(1000 + r)
            perm = m.blok_permutasyon(blok=20, rng=rng, maske=ms)
            FH = {h: D["FH"][h][perm] for h in H}
            o = boru_hatti(D, D["X"], D["LOO"], FH, D["CY"][perm], D["spy"][perm])
            o["yerinde"] = float((perm[ms] == np.arange(m.T)[ms]).mean())
        elif tip == "kaydir":
            rng = np.random.default_rng(5000 + r)
            Xs, k = M.dairesel_kaydir(D["X"], rng=rng)
            Ls, _ = M.dairesel_kaydir(D["LOO"], k=k)
            o = boru_hatti(D, Xs, Ls, D["FH"], D["CY"], D["spy"])
            o["k"] = k
        elif tip == "gercek":                       # zincirin asamali kosuyla ayni sonucu verdigini denetler
            o = boru_hatti(D, D["X"], D["LOO"], D["FH"], D["CY"], D["spy"])
        else:
            raise ValueError(tip)
        o.update({"tip": tip, "tekrar": r})
        sat.append(o)
        if tip == "gercek":
            break
    df = pd.DataFrame(sat)
    df.to_csv(os.path.join(ARA, f"plasebo_{tip}_{bas:04d}_{son:04d}.csv"), index=False)
    print(f"plasebo {tip} [{bas},{son}): {time.time() - t0:.0f} sn; n_gecen ort {df.n_gecen.mean():.2f}, "
          f"maks {df.n_gecen.max()}, n35 ort {df.n35.mean():.0f}")
    return df


def plasebo_oku():
    import glob
    ds = [pd.read_csv(f) for f in sorted(glob.glob(os.path.join(ARA, "plasebo_*.csv")))]
    return pd.concat(ds, ignore_index=True).drop_duplicates(["tip", "tekrar"]) if ds else pd.DataFrame()


def asama_ozet():
    ad = pd.read_csv(os.path.join(ARA, "oos_onay.csv"))
    pl = plasebo_oku()
    gercek = int(ad.bh_gecti.sum())
    n35 = int(pd.read_csv(os.path.join(ARA, "is_ozet.csv"), index_col=0).iloc[:, 0]["n35"])
    oz = []
    for tip in ("perm", "kaydir"):
        d = pl[pl.tip == tip]
        if d.empty:
            continue
        oz.append({"plasebo": tip, "tekrar": len(d), "gecen_medyan": d.n_gecen.median(),
                   "gecen_ort": d.n_gecen.mean(), "gecen_p95": d.n_gecen.quantile(0.95),
                   "gecen_maks": d.n_gecen.max(), "gercek_gecen": gercek,
                   "p_gecen": (1 + (d.n_gecen >= gercek).sum()) / (1 + len(d)),
                   "n35_medyan": d.n35.median(), "n35_p95": d.n35.quantile(0.95), "gercek_n35": n35,
                   "p_n35": (1 + (d.n35 >= n35).sum()) / (1 + len(d)),
                   "maks_t_is_p95": d.maks_t_is.quantile(0.95), "gercek_maks_t_is": ad.t_is.abs().max(),
                   "maks_z_oos_medyan": d.maks_z_oos.median(), "maks_z_oos_p95": d.maks_z_oos.quantile(0.95),
                   "gercek_maks_z_oos": ad.z_oos.max(),
                   "n_z2_medyan": d.n_z2.median(), "n_z2_p95": d.n_z2.quantile(0.95),
                   "gercek_n_z2": int((ad.z_oos >= 2).sum())})
    oz = pd.DataFrame(oz)
    oz.to_csv(os.path.join(ARA, "plasebo_ozet.csv"), index=False)
    print(oz.T.to_string())
    # tekil p: plasebodaki en yuksek yonlu OOS t dagilimina gore (iki plasebonun buyugu)
    for tip in ("perm", "kaydir"):
        d = pl[pl.tip == tip]
        mx = d.maks_z_oos.fillna(-np.inf).to_numpy()
        ad[f"p_plasebo_{tip}"] = [(1 + (mx >= z).sum()) / (1 + len(mx)) if np.isfinite(z) else 1.0 for z in ad.z_oos]
    ad["p_plasebo"] = ad[["p_plasebo_perm", "p_plasebo_kaydir"]].max(axis=1)
    ad.to_csv(os.path.join(ARA, "oos_onay.csv"), index=False)
    basarili = all(gercek > r.gecen_p95 for r in oz.itertuples()) and len(oz) == 2 and gercek > 0
    print("TARAMA", "BASARILI" if basarili else "BASARISIZ", f"(gercek {gercek})")
    return oz, basarili


# ----------------------------------------------------------------------------- islem bazinda sinama
def sinyal_kur(m, D, E, a, pencere=250, esik=1.0):
    """Tarama adayindan islem kurali: z_skor(X, pencere) esigi asinca yon = isaret(b_IS) * isaret(z)."""
    xs = D["LOO"][:, int(a.y_no)] if bool(a.ayni_sepet) else D["X"][:, int(a.x_sepet)]
    z = M.z_skor(pd.Series(np.array(xs, float), index=m.idx), pencere)
    s = (np.sign(z) * np.sign(a.t_is)).where(z.abs() > esik).fillna(0.0)
    hs = str(a.y_uyeler).split(";")
    S = pd.DataFrame({c: s.where(E[c], 0.0).astype(int) for c in hs})
    G = pd.DataFrame({c: z.abs() for c in hs})
    if len(hs) == 1:
        return S[hs[0]], hs[0], None, z
    return S, None, G, z


def asama_degerlendir(tam_liste=None):
    """Butun adaylar: temel kural (z250 > 1), IS ve OOS, K girisi, SPY:250, tek komisyon, bootstrap.
    tam_liste (aday_id listesi; varsayilan BH'den gecenler): izgara + butun donem/giris/korunma/komisyon/rejim."""
    t0 = time.time()
    m = M.Motor()
    D = yukle_D(m)
    E = m.tarama_hedef_maskesi(ADV_ALT)
    ad = pd.read_csv(os.path.join(ARA, "oos_onay.csv"))
    if tam_liste is None:
        tam_liste = ad.aday_id[ad.bh_gecti].tolist()
    parca = []
    for a in ad.itertuples():
        S, hed, G, _ = sinyal_kur(m, D, E, a)
        nt = (f"tarama: t_is={a.t_is:.2f} t_oos={a.t_oos:.2f} p_oos={a.p_oos:.4g} bh={'evet' if a.bh_gecti else 'hayir'}"
              f" p_plasebo={getattr(a, 'p_plasebo', np.nan):.3f} duzey={a.duzey} ayni_sepet={a.ayni_sepet}")
        ortak = dict(kural_id=a.aday_id, aile="S", girdi=f"sepet S{int(a.x_sepet):02d} artik getirisi [{a.x_uyeler[:80]}]",
                     notlar=nt, guc=G)
        tam = a.aday_id in tam_liste
        r = m.degerlendir(S, hed, ad=f"S{int(a.x_sepet):02d} -> {a.y} z250>1", h=(int(a.h),),
                          giris=("K", "A", "G") if tam else "K", gece=tam,
                          korunma=("yok", "SPY:250", "SPY:60") if tam else "SPY:250",
                          komisyon=M.KOMISYONLAR if tam else "hisse",
                          donemler=None if tam else ["IS", "OOS"], rejimler=tam, bootstrap=True, **ortak)
        parca.append(r)
        if tam:                                    # izgara: pencere 60/250 x esik 1/2 (temel disindaki 3 varyant)
            for pen, es in ((250, 2.0), (60, 1.0), (60, 2.0)):
                S2, hed2, G2, _ = sinyal_kur(m, D, E, a, pen, es)
                o2 = dict(ortak)
                o2["guc"] = G2
                o2["kural_id"] = f"{a.aday_id}-z{pen}-{es:g}"
                parca.append(m.degerlendir(S2, hed2, ad=f"S{int(a.x_sepet):02d} -> {a.y} z{pen}>{es:g}",
                                           h=(int(a.h),), giris=("K", "A"), gece=False, korunma="SPY:250",
                                           komisyon="hisse", donemler=["IS", "OOS", "SON"], rejimler=False,
                                           bootstrap=True, **o2))
    son = pd.concat(parca, ignore_index=True)
    M.yaz_sonuc(son, SONUC)
    print(f"{len(son)} satir -> {SONUC}  [{time.time() - t0:.0f} sn]")
    return son


if __name__ == "__main__":
    arg = sys.argv[1:] or ["hepsi"]
    if arg[0] == "is":
        asama_is()
    elif arg[0] == "oos":
        asama_oos()
    elif arg[0] == "plasebo":
        asama_plasebo(arg[1], int(arg[2]), int(arg[3]))
    elif arg[0] == "ozet":
        asama_ozet()
    elif arg[0] == "degerlendir":
        asama_degerlendir(arg[1].split(",") if len(arg) > 1 else None)
    elif arg[0] == "hepsi":
        asama_is()
        asama_oos()
        for tip in ("perm", "kaydir"):
            for b in range(0, 200, 50):
                asama_plasebo(tip, b, b + 50)
        asama_ozet()
        asama_degerlendir()
    else:
        raise SystemExit(__doc__)
