"""Bedelsiz olay calismasi: asama x pencere CAR izgarasi (onceden belirlenmis), alt gruplar, islem simulasyonlari, takvim-zamani portfoyu.
Cikti: <HERE>/sonuc/*.csv ve sonuc_tablolar.md (rapora kopyalanan tablolar)."""
import os, sys, numpy as np, pandas as pd
import f20_es as E
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = f"{HERE}/sonuc"; os.makedirs(OUT, exist_ok=True)
CACHE = E.CACHE
COST = 0.0025
ASAMA = {"p1": "YK/ilk duyuru", "p2": "SPK basvurusu", "p3": "SPK onayi", "hak": "Hak kullanim (bolunme) gunu"}
PENC = {   # onceden belirlenmis pencereler (islem gunu, t0'a gore)
    "p1": [(-60, -1), (-20, -1), (-5, -1), (0, 0), (0, 1), (1, 5), (1, 10), (1, 20), (1, 60)],
    "p2": [(-20, -1), (-5, -1), (0, 0), (0, 1), (1, 5), (1, 10), (1, 20)],
    "p3": [(-20, -1), (-5, -1), (0, 0), (0, 1), (1, 3), (1, 5), (1, 10), (1, 20)],
    "hak": [(-20, -1), (-5, -1), (-1, -1), (0, 0), (1, 5), (1, 10), (1, 20), (1, 60)]}
def oran_grup(x): return "<%100" if x < 100 else ("%100-499" if x < 500 else ">=%500")
def hazirla(M, ev):
    cal = M["cal"]; rows = []
    for i, e in ev.iterrows():
        k = e.kod
        if k not in M["R"].columns: continue
        r = dict(i=i, kod=k, hak_tarih=e.hak, oran=e.oran, tip=e.tip, yil=e.hak.year)
        r["j_hak"] = E.day_idx(cal, e.hak)
        for s in ["p1", "p2", "p3"]:
            r["j_" + s] = E.t0_idx(cal, e[s]) if pd.notna(e[s]) else None
            if r["j_" + s] is not None and r["j_hak"] is not None and r["j_" + s] > r["j_hak"]: r["j_" + s] = None
        jref = r["j_p1"] if r["j_p1"] is not None else (r["j_hak"] - 60 if r["j_hak"] is not None else None)
        if jref is None or jref < 60: continue
        r["al"], r["be"], r["nest"] = E.beta(M, k, jref)
        pdr = M["PDR"][k].iloc[max(0, jref - 1)]; pdv = M["PD"][k].iloc[max(0, jref - 1)]
        r["pd_yuzdelik"] = pdr; r["pd_tl"] = pdv
        # anormal hacim (TL): [-5,-1] ortalamasi ve t0 / [-120,-21] medyani  (P1 ve hak icin)
        for s in ["p1", "hak"]:
            j0 = r["j_" + s]
            if j0 is None or j0 < 125: continue
            v = M["VOL"][k]; base = v.iloc[j0 - 120:j0 - 20].median()
            if pd.notna(base) and base > 0:
                r["hacim_on5_" + s] = v.iloc[j0 - 5:j0].fillna(0).mean() / base; r["hacim_t0_" + s] = v.iloc[j0] / base if pd.notna(v.iloc[j0]) else np.nan
        rows.append(r)
    return pd.DataFrame(rows)
def car_tablosu(M, H):
    recs = []
    for _, h in H.iterrows():
        for s, W in PENC.items():
            j0 = h["j_" + s]
            if j0 is None or pd.isna(j0): continue
            j0 = int(j0)
            kil = bool(M["TAV"][h.kod].iloc[j0])
            for a, b in W:
                recs.append(dict(i=h.i, kod=h.kod, asama=s, pencere=f"[{a},{b}]", a=a, b=b, t0=M["cal"][j0], t0_tavan=kil,
                                 car=E.car(M, h.kod, j0, a, b), car_mm=E.car(M, h.kod, j0, a, b, h.al, h.be, "mm"),
                                 car_b=E.car(M, h.kod, j0, a, b, 0.0, h.be, "mm")))
    C = pd.DataFrame(recs)
    return C.merge(H[["i", "oran", "tip", "yil", "pd_yuzdelik"]], on="i", how="left")
def tablo(C, by=None, col="car"):
    out = []
    keys = ["asama", "pencere", "a", "b"] + ([by] if by else [])
    for kk, g in C.groupby(keys, sort=False):
        z = E.ozet(g[col], g.t0); z.update(dict(zip(keys, kk if isinstance(kk, tuple) else (kk,))))
        z["ort_mm"] = g.car_mm.mean(); z["med_mm"] = g.car_mm.median()
        out.append(z)
    T = pd.DataFrame(out)
    T["_o"] = T.asama.map({"p1": 0, "p2": 1, "p3": 2, "hak": 3}); T = T.sort_values(["_o", "a", "b"] + ([by] if by else [])).drop(columns="_o")
    return T
def islem(M, H, ad, giris, cikis, maxgec=10):
    """giris(h)->j (alis kapanisi), cikis(h, j_giris)->j (satis kapanisi). Tavan kilitli giris kaydirilir; taban kilitli cikis kaydirilir."""
    rec = []
    for _, h in H.iterrows():
        j = giris(h)
        if j is None or pd.isna(j): continue
        j = int(j)
        if j < 1 or j >= len(M["cal"]): continue
        kil0 = bool(M["TAV"][h.kod].iloc[j])
        jg, gec = E.dolabilir_giris(M, h.kod, j, maxgec)
        jc0 = cikis(h, j)
        if jc0 is None or pd.isna(jc0): continue
        jc0 = int(jc0)
        # (a) kilit yok sayilarak (teorik) ; (b) kilitli girisler atilir ; (c) gecikmeli giris
        ham_a, xu_a = E.bhar(M, h.kod, j, jc0)
        if jg is not None and jg < jc0:
            jc, gc = E.dolabilir_cikis(M, h.kod, jc0, maxgec)
            ham_c, xu_c = E.bhar(M, h.kod, jg, jc if jc is not None else jc0)
        else: ham_c = xu_c = np.nan; gec = None
        rec.append(dict(islem=ad, i=h.i, kod=h.kod, giris=M["cal"][j], gun=jc0 - j, kilitli_giris=kil0, gecikme=gec,
                        ham=ham_a, bhar=ham_a - xu_a if pd.notna(ham_a) else np.nan,
                        ham_dol=ham_c, bhar_dol=ham_c - xu_c if pd.notna(ham_c) else np.nan, oran=h.oran, yil=h.yil, pd_yuzdelik=h.pd_yuzdelik,
                        j_in=j, j_out=jc0, jg=jg))
    return pd.DataFrame(rec)
def islem_ozet(T, by=None):
    out = []
    for kk, g in (T.groupby(["islem"] + ([by] if by else []), sort=False)):
        kk = kk if isinstance(kk, tuple) else (kk,)
        a = E.ozet(g.bhar, g.giris); b = E.ozet(g.bhar_dol, g.giris)
        gd = g[g.bhar_dol.notna()]
        out.append(dict(zip(["islem"] + ([by] if by else []), kk)) | dict(
            N=a["N"], gun_med=g.gun.median(), kilitli_giris_pay=g.kilitli_giris.mean(),
            ham_ort=g.ham.mean(), ham_med=g.ham.median(), bhar_ort=a["ort"], bhar_med=a["med"], t=a["t"], isabet=a["isabet"],
            N_dol=b["N"], bhar_dol_ort=b["ort"], bhar_dol_med=b["med"], t_dol=b["t"], isabet_dol=b["isabet"],
            net_ham_dol_ort=(gd.ham_dol - COST).mean(), net_bhar_dol_ort=(gd.bhar_dol - COST).mean(), net_bhar_dol_med=(gd.bhar_dol - COST).median(),
            p5=b["p5"], p95=b["p95"]))
    return pd.DataFrame(out)
