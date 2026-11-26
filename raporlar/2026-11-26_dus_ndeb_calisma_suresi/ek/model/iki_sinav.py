#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MODEL_TANIMI.md 9. bolum: iki sinav uzantisi (DUS + NDEB Virtual OSCE). Yalniz numpy.

Kullanim:
  python3 iki_sinav.py          # hesap + CSV (cikti/iki_sinav/) + IKI_SINAV.md
  python3 iki_sinav.py rapor    # yalniz IKI_SINAV.md (CSV'lerden)

sim.py'den ice aktarilanlar (sim.py degistirilmez):
  sample_params, derive   parametre cekimi (Latin hiperkup), ogrenme dayanagi kabulu, a / Fcrit / b1 / b2
  Mint, Lload             gun ici etkili saat ve yuk integralleri
  ref_sim                 temel kosu (yalniz DUS) ve motor esitlik sinamasi
  wcsv, rcsv, F, tr, h05  CSV ve bicim yardimcilari;  G0_DUS, Z95 sabitleri
ref_sim'in takvimi tek sinavlidir (tek son donem, bos gun yok). Bu yuzden gun dongusu `yurut` icinde ayni
sira ve ayni kurallarla, takvimi disaridan alacak bicimde kurulmus ve ref_sim'e esitligi sinanmistir.

Bu model olcum degil, varsayimlari tutarli bir programa ceviren hesap aracidir.
"""
import os, sys, time, math, itertools, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
from sim import sample_params, derive, Mint, Lload, ref_sim, wcsv, rcsv, F, tr, h05, G0_DUS, Z95

OUT = os.path.join(HERE, 'cikti', 'iki_sinav')
SEED, ND = 101, 1000
H3S = (6.0, 7.0)
YUKLER = ('K1', 'K2', 'K3')
E_DUS, HMAX = 332, 361
SIRALAR = ('S1', 'S2', 'S3')
OSCE = {'S1': 95, 'S2': 175, 'S3': 361}
BOS = (0, 3, 7)
PAY = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
OMEGA = (('dusuk', 0.40, 0.25), ('orta', 0.55, 0.35), ('yuksek', 0.70, 0.50))
GAPS = (0.05, 0.15, 0.30)
ELS = (0.83, 1.0)
TAPER_T, TAPER_PSI, SON = 3, 0.75, 30
KMAX, KBOS = 300, 150
OLURLUK = 0.90

_IX = np.array(list(itertools.product(range(len(ELS)), range(3), range(5), range(5))))
C_EL = np.array(ELS)[_IX[:, 0]]
C_DN = np.array([o[1] for o in OMEGA])[_IX[:, 1]]
C_ND = np.array([o[2] for o in OMEGA])[_IX[:, 1]]
C_D1 = PAY[_IX[:, 2]]; C_D2 = PAY[_IX[:, 3]]
NC = len(_IX)
SHP = (len(ELS), 3, 5, 5)
O_BOS = np.repeat(np.array(BOS), 25); O_D1 = np.tile(np.repeat(PAY, 5), 3); O_D2 = np.tile(PAY, 15)


# ---------------------------------------------------------------- takvim
def yukleri_oku():
    """ana_tablo.csv: (b1), 360 gun, saglam politika. Donus: {(h3, K): (hA, hB, d, n, haftalik_saat)}"""
    out = {}
    for r in rcsv(os.path.join(HERE, 'cikti', 'ana_tablo.csv')):
        if r['amac'] == 'b1' and F(r['ufuk']) == 360 and F(r['h3']) in H3S:
            out[(F(r['h3']), r['K'])] = (F(r['hA']), F(r['hB']), int(F(r['d'])), int(F(r['n'])), F(r['haftalik_saat']))
    return out


def carpan(pol, sinavlar, bos=None, H=HMAX):
    """Gunluk saat carpani. Takvim 0. gune bagli; son 3 gun x0,75 hafif haftanin yerine gecer, haftalik
    dinlenme surer (SONUC.md 10. bolumdeki yorum). Son sinavdan sonra 0. bos = (ilk gun, gun sayisi)."""
    hA, hB, d, n = pol[:4]
    m = np.zeros(H)
    for t in range(min(H, max(sinavlar))):
        w, dow = divmod(t, 7)
        if dow >= d:
            mm = 0.0
        elif any(E - TAPER_T <= t < E for E in sinavlar):
            mm = TAPER_PSI
        elif n > 0 and (w + 1) % n == 0:
            mm = 0.5
        else:
            mm = 1.0
        if bos and bos[0] <= t < bos[0] + bos[1]:
            mm = 0.0
        m[t] = mm
    return m


def pay_takvimi(sira, D1, D2):
    """Virtual OSCE payi [gun, secenek]. S1/S2: D1 = OSCE'den 30 gun oncesine kadar, D2 = son 30 gun, sonra 0.
    S3: D1 = DUS'tan 30 gun oncesine kadar, D2 = DUS'tan onceki son 30 gun, DUS'tan sonra 1."""
    P = np.zeros((HMAX, len(D1)))
    if sira in ('S1', 'S2'):
        E = OSCE[sira]
        P[:E - SON] = D1; P[E - SON:E] = D2
    else:
        P[:E_DUS - SON] = D1; P[E_DUS - SON:E_DUS] = D2; P[E_DUS:] = 1.0
    return P


# ---------------------------------------------------------------- yorgunluk ve e(t): paydan bagimsiz, bir kez
def yurut(pr, hA, hB, M):
    """sim.ref_sim'in gun dongusu (ayni sira: sabah cokus denetimi -> q -> e -> f1 -> f2), takvim disaridan.
    M[t, sutun]: gunluk saat carpani. Her gun (t, f1, f2, cokus, e, net saat) uretir; t = H'de e = None."""
    H, n = M.shape; nd = len(pr['h0'])
    lev, idx = np.unique(M, return_inverse=True); idx = np.asarray(idx).reshape(M.shape)

    def EX(m):
        ha, hb = hA * m, hB * m
        E = Mint(0.0, ha, pr['u50'], pr['s']) + pr['eB'] * Mint(ha, ha + hb, pr['u50'], pr['s'])
        W = Lload(ha, pr['h0'], pr['gamma']) + pr['cB'] * (Lload(ha + hb, pr['h0'], pr['gamma'])
                                                         - Lload(ha, pr['h0'], pr['gamma']))
        return E, np.maximum(0.0, W - pr['h0'])
    full = [EX(m) for m in lev]; half = [EX(m / 2.0) for m in lev]
    Ef = np.stack([x[0] for x in full], 1); Xf = np.stack([x[1] for x in full], 1)
    Eh = np.stack([x[0] for x in half], 1); Xh = np.stack([x[1] for x in half], 1)
    c_ = lambda k: pr[k][:, None]
    Fc = c_('Fcrit'); a = c_('a')
    f1 = np.zeros((nd, n)); f2 = np.zeros((nd, n)); col = np.zeros((nd, n), bool)
    for t in range(H + 1):
        col = np.where(col, f2 >= 0.3 * Fc, f2 >= Fc * (1 + 1e-9))
        q = 1.0 / (1.0 + c_('b1') * f1 + c_('b2') * f2)
        q = np.where(col, q * c_('qcol'), q)
        if t == H:
            yield t, f1, f2, col, None, None
            return
        ix = idx[t]
        E = np.where(col, Eh[:, ix], Ef[:, ix]); X = np.where(col, Xh[:, ix], Xf[:, ix])
        Hh = np.where(col, 0.5, 1.0) * ((hA + hB) * M[t])[None, :]
        yield t, f1, f2, col, q * E, Hh
        f1 = (f1 + X) * c_('rho1')
        f2 = f2 * np.where(col, c_('rho2c'), c_('rho2')) + np.maximum(f1 - a, 0.0)


def ceza(pr, f1, f2):
    """Sinav gunu carpani exp(-(e1*f1/a + e2*f2/Fcrit)), [cekim, sutun]."""
    return np.exp(-(pr['e1'][:, None] * f1 / pr['a'][:, None] + pr['e2'][:, None] * f2 / pr['Fcrit'][:, None]))


# ---------------------------------------------------------------- iki stoklu bilgi
def bilgi(pr, e, Hh, pay, omDN, omND, eL, snaps, kN=None):
    """gD ve gN (tanimin 4. bolumundeki denklem; S_D = S, S_N = kN*S, tauG ortak).
    e, Hh: [gun, cekim]; pay: [gun, secenek]; omDN, omND, eL: [secenek].
    g = A*g0 + B bicimi (dogrusal): acik duzeyi sonradan uygulanir. GX: aktarim olmasaydi (omegaND = 0) gD;
    gD - GX = Virtual OSCE calismasinin gD'ye katkisi. Donus: {gun: dict(AD, BD, GX, AN, BN, hN)} (o gunun sabahi)."""
    T = pay.shape[0]; nd = e.shape[1]; C = pay.shape[1]
    kN = pr['kN'] if kN is None else kN
    invS = (1.0 / pr['S'])[:, None]; invSN = (1.0 / (kN * pr['S']))[:, None]
    cg = (1.0 - 1.0 / pr['tauG'])[:, None]
    wT = omND[None, :] * eL[None, :] * pay                 # Virtual OSCE saatinden gD'ye aktarim
    wD = (1.0 - pay) + wT                                  # gD'ye giren toplam agirlik
    wN = eL[None, :] * pay + omDN[None, :] * (1.0 - pay)   # gN'ye giren toplam agirlik
    w0 = 1.0 - pay                                         # aktarimsiz gD agirligi
    AD = np.ones((nd, C)); BD = np.zeros((nd, C)); GX = np.full((nd, C), G0_DUS)
    AN = np.ones((nd, C)); BN = np.zeros((nd, C)); hN = np.zeros((nd, C))
    out = {}
    for t in range(T + 1):
        if t in snaps:
            out[t] = dict(AD=AD.copy(), BD=BD.copy(), GX=GX.copy(), AN=AN.copy(), BN=BN.copy(), hN=hN.copy())
        if t == T:
            break
        x = e[t][:, None] * invS; y = e[t][:, None] * invSN
        rD = x * wD[t][None, :]
        kD = cg - rD
        AD *= kD; BD *= kD; BD += rD
        rX = x * w0[t][None, :]
        GX *= (cg - rX); GX += rX
        rN = y * wN[t][None, :]
        kNf = cg - rN
        AN *= kNf; BN *= kNf; BN += rN
        hN += Hh[t][:, None] * pay[t][None, :]
    return out


def gun_esdegeri(egri, hedef, adim=1):
    """Ortalama P = hedef olan k (dogrusal aradeger). Egri once tekduze azalan zarfina indirilir.
    adim > 1: egri yalniz k = 0, adim, 2*adim, ... noktalarinda okunur (hafif hafta dongusunun ayni evresi).
    Donus: (k, sinirda mi)."""
    env = np.minimum.accumulate(egri[::adim])
    if hedef >= env[0]:
        return 0.0, 0
    alt = np.flatnonzero(env <= hedef)
    if alt.size == 0:
        return float(adim * (len(env) - 1)), 1
    k = int(alt[0])
    return adim * ((k - 1) + (env[k - 1] - hedef) / (env[k - 1] - env[k])), 0


# ---------------------------------------------------------------- hesap
def hesap():
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    yuk = yukleri_oku()
    R_h, R_o, R_p0, R_e, R_y, tests = [], [], [], [], [], []
    tmax = dict(motor=0.0, pay0=0.0, pay1=0.0, omega1=0.0, degismez=0.0, saat=0.0, egri0=0.0, s3pay0=0.0)
    mono = dict(pay=0, omega=0, n=0); cokus = []
    for h3 in H3S:
        pr, info = sample_params(h3, SEED, ND)
        prd = derive(pr, h3)
        nd = len(prd['h0'])
        kmed = float(np.median(prd['kN']))
        subs = {'hepsi': np.ones(nd, bool), 'kN_alt': prd['kN'] < kmed, 'kN_ust': prd['kN'] >= kmed}
        esik = (prd['Pgec'] + Z95 * prd['sigP'])[:, None]
        cgv = 1.0 - 1.0 / prd['tauG']
        for K in YUKLER:
            hA, hB, d, n, hafta = yuk[(h3, K)]
            pol = (hA, hB, d, n)
            R_y.append(dict(h3=h3, yuk=K, hA=hA, hB=hB, gun_hafta=d, hafif_hafta=n, haftalik_saat=hafta,
                            K0_ile_ayni=int(K == 'K1' and yuk[(h3, 'K0')][:4] == pol), n_cekim=nd,
                            n_onsel=info['n_prior'], n_kabul=info['n_acc']))
            # --- takvimler: 0 = temel (yalniz DUS); 1..9 = siralama x bos gun
            cols = [carpan(pol, [E_DUS])]
            for s in SIRALAR:
                for b in BOS:
                    cols.append(carpan(pol, sorted([OSCE[s], E_DUS]), bos=(min(OSCE[s], E_DUS), b)))
            M = np.stack(cols, 1); ncol = M.shape[1]
            e = np.zeros((ncol, HMAX, nd)); Hh = np.zeros((ncol, HMAX, nd)); snap = {}; ever = np.zeros((nd, ncol), bool)
            for t, f1, f2, col, et, ht in yurut(prd, hA, hB, M):
                ever |= col
                if t in (95, 175, E_DUS, HMAX):
                    snap[t] = ceza(prd, f1, f2)
                    if t == E_DUS:
                        fD = (f1[:, 0].copy(), f2[:, 0].copy())
                if et is not None:
                    e[:, t, :] = et.T; Hh[:, t, :] = ht.T
            cokus.append(float(ever.mean()))
            ozet0 = (float(e.sum()), float(np.abs(e).sum()), float(Hh.sum()), float(sum(v.sum() for v in snap.values())))
            # --- temel kosu: sim.ref_sim (bagimsiz yol) ve motor esitligi
            ref = ref_sim(prd, [(hA, hB, d, n, TAPER_T, TAPER_PSI)], E_DUS, keep_e=(0,))
            Pb = ref['P'][:, 0]
            tmax['motor'] = max(tmax['motor'], float(np.abs(e[0, :E_DUS] - ref['es'][0]).max()),
                                float(np.abs(fD[0] - ref['f1'][:, 0]).max()), float(np.abs(fD[1] - ref['f2'][:, 0]).max()))
            z = np.zeros(1); o1 = np.ones(1)
            r0 = bilgi(prd, e[0, :E_DUS], Hh[0, :E_DUS], np.zeros((E_DUS, 1)), z, z, o1 * 0.83, (E_DUS,))
            g0 = r0[E_DUS]['AD'][:, 0] * G0_DUS + r0[E_DUS]['BD'][:, 0]
            tmax['pay0'] = max(tmax['pay0'], float(np.abs(g0 - ref['gD'][:, 0]).max()),
                               float(np.abs(g0 * snap[E_DUS][:, 0] - Pb).max()))
            # S3 (bos 0) takviminde pay 0, omega 0: gD(332) temel kosuyla ayni
            r0 = bilgi(prd, e[7, :E_DUS], Hh[7, :E_DUS], np.zeros((E_DUS, 1)), z, z, o1 * 0.83, (E_DUS,))
            tmax['pay0'] = max(tmax['pay0'], float(np.abs(r0[E_DUS]['AD'][:, 0] * G0_DUS + r0[E_DUS]['BD'][:, 0]
                                                          - ref['gD'][:, 0]).max()))
            # pay 1, omegaND 0: gD yalniz unutmayla duser (S1, bos 0 takvimi)
            r1 = bilgi(prd, e[1, :E_DUS], Hh[1, :E_DUS], np.ones((E_DUS, 1)), o1 * 0.55, z, o1 * 0.83, (E_DUS,))
            tmax['pay1'] = max(tmax['pay1'], float(np.abs(r1[E_DUS]['AD'][:, 0] * G0_DUS + r1[E_DUS]['BD'][:, 0]
                                                          - G0_DUS * cgv ** E_DUS).max()))
            # toplam net saat korunumu: pay 1 iken Virtual OSCE saati = uygulanan toplam net saat
            tmax['saat'] = max(tmax['saat'], float(np.abs(r1[E_DUS]['hN'][:, 0] - Hh[1, :E_DUS].sum(0)).max()))
            # omega = 1, eL = 1, S_N = S: iki stok ayni ilerler (S1 takvimi, paylar 0,25 / 0,75)
            pt = pay_takvimi('S1', np.array([0.25]), np.array([0.75]))[:E_DUS]
            r2 = bilgi(prd, e[1, :E_DUS], Hh[1, :E_DUS], pt, o1, o1, o1, (95, E_DUS), kN=np.ones(nd))
            tmax['omega1'] = max(tmax['omega1'], *[float(np.abs(r2[g]['AD'] - r2[g]['AN']).max()) for g in (95, E_DUS)],
                                 *[float(np.abs(r2[g]['BD'] - r2[g]['BN']).max()) for g in (95, E_DUS)])
            # --- gun esdegeri egrisi: temel kosuda sinav k gun erkene cekilir (son 3 gun x0,75 korunur)
            Mk = np.stack([carpan(pol, [E_DUS - k], H=E_DUS) for k in range(KMAX + 1)], 1)
            Pk = np.zeros((nd, KMAX + 1)); A = np.ones((nd, KMAX + 1)); B = np.zeros((nd, KMAX + 1))
            invS = (1.0 / prd['S'])[:, None]; cg = cgv[:, None]
            for t, f1, f2, col, et, ht in yurut(prd, hA, hB, Mk):
                k = E_DUS - t
                if 0 <= k <= KMAX:
                    Pk[:, k] = (A[:, k] * G0_DUS + B[:, k]) * ceza(prd, f1[:, k:k + 1], f2[:, k:k + 1])[:, 0]
                if et is not None:
                    r = et * invS; A *= (cg - r); B *= (cg - r); B += r
            # --- ikinci olcu: sinav 332. gunde kalir, ondan onceki son k gun hic calisilmaz
            mb = carpan(pol, [E_DUS], H=E_DUS)
            Mb = np.stack([np.where(np.arange(E_DUS) >= E_DUS - k, 0.0, mb) for k in range(KBOS + 1)], 1)
            A = np.ones((nd, KBOS + 1)); B = np.zeros((nd, KBOS + 1))
            for t, f1, f2, col, et, ht in yurut(prd, hA, hB, Mb):
                if et is None:
                    Pz = (A * G0_DUS + B) * ceza(prd, f1, f2)
                else:
                    r = et * invS; A *= (cg - r); B *= (cg - r); B += r
            tmax['egri0'] = max(tmax['egri0'], float(np.abs(Pk[:, 0] - Pb).max()), float(np.abs(Pz[:, 0] - Pb).max()))
            adim = 7 * n if n > 0 else 1
            for tur, arr in (('sinav_erken', Pk), ('son_gunler_bos', Pz)):
                for k in range(arr.shape[1]):
                    R_e.append(dict(h3=h3, yuk=K, tur=tur, k_gun=k, P_ort=arr[:, k].mean(),
                                    P_kN_alt=arr[subs['kN_alt'], k].mean(), P_kN_ust=arr[subs['kN_ust'], k].mean()))
            # --- iki stok: siralama x bos gun x (eL, omega, D1, D2)
            FE = {s: np.zeros(SHP[:2] + (3, 3, 3, 5, 5)) for s in subs}
            MP = {s: np.zeros(SHP[:2] + (3, 3, 5, 5)) for s in subs}
            HR = {s: np.zeros_like(MP[s]) for s in subs}; CE = {s: np.zeros_like(MP[s]) for s in subs}
            CD = {s: np.zeros_like(MP[s]) for s in subs}
            SPAN = np.zeros((3, 3, 5, 5)); TOPH = np.zeros((3, 3))
            for si, s in enumerate(SIRALAR):
                E = OSCE[s]; T = max(E, E_DUS)
                pay = pay_takvimi(s, C_D1, C_D2)[:T]
                for bi, b in enumerate(BOS):
                    j = 1 + si * 3 + bi
                    r = bilgi(prd, e[j, :T], Hh[j, :T], pay, C_DN, C_ND, C_EL, (E, E_DUS))
                    PD = (r[E_DUS]['AD'] * G0_DUS + r[E_DUS]['BD']) * snap[E_DUS][:, j:j + 1]
                    tE = min(E, E_DUS); hN = r[E]['hN']
                    cE = r[tE]['AD'] * G0_DUS + r[tE]['BD'] - r[tE]['GX']
                    cD = r[E_DUS]['AD'] * G0_DUS + r[E_DUS]['BD'] - r[E_DUS]['GX']
                    akt = (pay[:, :25] > 0) & (M[:T, j] > 0)[:, None]
                    ilk = np.argmax(akt, 0); son = T - 1 - np.argmax(akt[::-1], 0)
                    SPAN[si, bi] = np.where(akt.any(0), son - ilk + 1, 0).reshape(5, 5)
                    TOPH[si, bi] = Hh[j, :T].sum(0).mean()
                    for sub, mk in subs.items():
                        MP[sub][:, :, si, bi] = PD[mk].mean(0).reshape(SHP)
                        HR[sub][:, :, si, bi] = hN[mk].mean(0).reshape(SHP)
                        CE[sub][:, :, si, bi] = cE[mk].mean(0).reshape(SHP)
                        CD[sub][:, :, si, bi] = cD[mk].mean(0).reshape(SHP)
                    for gi, gap in enumerate(GAPS):
                        PN = (r[E]['AN'] * (prd['Pgec'][:, None] - gap) + r[E]['BN']) * snap[E][:, j:j + 1]
                        ok = PN >= esik
                        for sub, mk in subs.items():
                            FE[sub][:, :, gi, si, bi] = ok[mk].mean(0).reshape(SHP)
                    if s == 'S3' and b == 0:   # pay (0,0): DUS P'si temel kosuyla ayni olmali
                        c00 = np.flatnonzero((C_D1 == 0) & (C_D2 == 0))
                        tmax['s3pay0'] = max(tmax['s3pay0'], float(np.abs(PD[:, c00] - Pb[:, None]).max()))
            ozet1 = (float(e.sum()), float(np.abs(e).sum()), float(Hh.sum()), float(sum(v.sum() for v in snap.values())))
            tmax['degismez'] = max(tmax['degismez'], max(abs(u - v) for u, v in zip(ozet0, ozet1)))
            f = FE['hepsi']
            mono['pay'] += int((np.diff(f, axis=5) < -1e-12).sum() + (np.diff(f, axis=6) < -1e-12).sum())
            mono['omega'] += int((np.diff(f, axis=1) < -1e-12).sum()); mono['n'] += f.size
            # --- hucreler ve karar kurali
            for var, sub, eLi in (('ana', 'hepsi', 0), ('eL_1', 'hepsi', 1), ('kN_alt', 'kN_alt', 0), ('kN_ust', 'kN_ust', 0)):
                mk = subs[sub]; Pbm = float(Pb[mk].mean()); egri = Pk[mk].mean(0); egriz = Pz[mk].mean(0)
                for oi, om in enumerate(OMEGA):
                    for gi, gap in enumerate(GAPS):
                        for si, s in enumerate(SIRALAR):
                            fe = FE[sub][eLi, oi, gi, si].ravel(); mp = MP[sub][eLi, oi, si].ravel()
                            hr = HR[sub][eLi, oi, si].ravel(); ce = CE[sub][eLi, oi, si].ravel()
                            cd = CD[sub][eLi, oi, si].ravel(); sp = SPAN[si].ravel()
                            ok = fe >= OLURLUK - 1e-12
                            row = dict(varyant=var, siralama=s, yuk=K, h3=h3, omega=om[0], acik=gap, eL=ELS[eLi],
                                       n_cekim=int(mk.sum()), hA=hA, hB=hB, olurlu=int(ok.any()))
                            if ok.any():
                                sira_ = np.lexsort((hr, -O_BOS, -fe, -np.round(mp, 10)))
                                b_ = int([o for o in sira_ if ok[o]][0])
                                kg, sinir = gun_esdegeri(egri, mp[b_], adim)
                                kgh, _ = gun_esdegeri(egri, mp[b_]); kz, sinz = gun_esdegeri(egriz, mp[b_])
                                uf = float((cgv[mk] ** (E_DUS - OSCE[s])).mean()) if s != 'S3' else float('nan')
                                row.update(D1=O_D1[b_], D2=O_D2[b_], bos_gun=int(O_BOS[b_]), olurluk_orani=fe[b_],
                                           osce_net_saat=hr[b_], osce_yayilma_hafta=sp[b_] / 7.0,
                                           osce_tam_gun_karsiligi=hr[b_] / (hA + hB), P_dus=mp[b_], P_temel=Pbm,
                                           kayip_yuzde=100.0 * (1.0 - mp[b_] / Pbm), kayip_puan=100.0 * (Pbm - mp[b_]),
                                           kayip_gun_son_gunler_bos=kz, kayip_gun_sinav_erken=kg,
                                           kayip_gun_sinav_erken_ham=kgh, gun_esdegeri_sinirda=int(bool(sinir or sinz)),
                                           aktarim_gD_osce_gunu_puan=100.0 * ce[b_], aktarim_gD_dus_gunu_puan=100.0 * cd[b_],
                                           aktarim_kalan_oran=(cd[b_] / ce[b_]) if ce[b_] > 0 else float('nan'),
                                           salt_unutma_carpani=uf)
                            m_ = int(np.lexsort((-mp, -fe))[0])
                            row.update(en_iyi_olurluk_orani=fe[m_], en_iyi_D1=O_D1[m_], en_iyi_D2=O_D2[m_],
                                       en_iyi_bos_gun=int(O_BOS[m_]), n_olurlu_secenek=int(ok.sum()))
                            R_h.append(row)
                            if var == 'ana':
                                for o in range(75):
                                    R_o.append(dict(siralama=s, yuk=K, h3=h3, omega=om[0], acik=gap, D1=O_D1[o], D2=O_D2[o],
                                                    bos_gun=int(O_BOS[o]), olurluk_orani=fe[o], P_dus=mp[o],
                                                    kayip_yuzde=100.0 * (1.0 - mp[o] / Pbm), osce_net_saat=hr[o],
                                                    osce_yayilma_hafta=sp[o] / 7.0))
                            if var in ('ana', 'eL_1'):
                                for bi, b in enumerate(BOS):   # pay (0,0): Virtual OSCE'ye ayri saat yok / S3'te yalniz DUS sonrasi
                                    R_p0.append(dict(varyant=var, siralama=s, yuk=K, h3=h3, omega=om[0], acik=gap, bos_gun=b,
                                                     olurluk_orani=FE[sub][eLi, oi, gi, si, bi, 0, 0],
                                                     osce_net_saat=HR[sub][eLi, oi, si, bi, 0, 0],
                                                     osce_yayilma_hafta=SPAN[si, bi, 0, 0] / 7.0))
            print('h3=%g %s bitti, %.1f s' % (h3, K, time.time() - t0), flush=True)

    ana = [r for r in R_h if r['varyant'] == 'ana']
    wcsv(os.path.join(OUT, 'hucreler.csv'), ana)
    wcsv(os.path.join(OUT, 'duyarlilik.csv'), R_h)
    wcsv(os.path.join(OUT, 'secenekler.csv'), R_o)
    wcsv(os.path.join(OUT, 'pay0_olurluk.csv'), R_p0)
    wcsv(os.path.join(OUT, 'temel_egri.csv'), R_e)
    wcsv(os.path.join(OUT, 'yukler.csv'), R_y)
    # --- omega etkisi (dusuk -> yuksek) ve siralama karsilastirmasi
    key = lambda r: (r['siralama'], r['yuk'], r['h3'], r['acik'])
    by = {(key(r), r['omega']): r for r in ana}
    R_om = []
    for k in sorted({key(r) for r in ana}):
        lo, mi, hi = by[(k, 'dusuk')], by[(k, 'orta')], by[(k, 'yuksek')]
        row = dict(siralama=k[0], yuk=k[1], h3=k[2], acik=k[3])
        for nm, r in (('dusuk', lo), ('orta', mi), ('yuksek', hi)):
            row.update({'olurlu_' + nm: r['olurlu'], 'saat_' + nm: r.get('osce_net_saat', float('nan')),
                        'kayip_yuzde_' + nm: r.get('kayip_yuzde', float('nan')),
                        'gun_bos_' + nm: r.get('kayip_gun_son_gunler_bos', float('nan')),
                        'gun_erken_' + nm: r.get('kayip_gun_sinav_erken', float('nan')),
                        'pay_' + nm: ('%g/%g/%d' % (r['D1'], r['D2'], r['bos_gun'])) if r['olurlu'] else 'olurlu degil'})
        if lo['olurlu'] and hi['olurlu']:
            row.update(saat_degisim=hi['osce_net_saat'] - lo['osce_net_saat'],
                       kayip_yuzde_degisim=hi['kayip_yuzde'] - lo['kayip_yuzde'],
                       gun_bos_degisim=hi['kayip_gun_son_gunler_bos'] - lo['kayip_gun_son_gunler_bos'],
                       gun_erken_degisim=hi['kayip_gun_sinav_erken'] - lo['kayip_gun_sinav_erken'])
        R_om.append(row)
    wcsv(os.path.join(OUT, 'omega_etkisi.csv'), R_om)
    R_s = []
    byc = {(r['yuk'], r['h3'], r['omega'], r['acik'], r['siralama']): r for r in ana}
    for K in YUKLER:
        for h3 in H3S:
            for om in OMEGA:
                for gap in GAPS:
                    rs = {s: byc[(K, h3, om[0], gap, s)] for s in SIRALAR}
                    row = dict(yuk=K, h3=h3, omega=om[0], acik=gap)
                    for s in SIRALAR:
                        r = rs[s]
                        row.update({s + '_olurlu': r['olurlu'], s + '_kayip_yuzde': r.get('kayip_yuzde', float('nan')),
                                    s + '_gun_bos': r.get('kayip_gun_son_gunler_bos', float('nan')),
                                    s + '_gun_erken': r.get('kayip_gun_sinav_erken', float('nan')),
                                    s + '_saat': r.get('osce_net_saat', float('nan')),
                                    s + '_en_iyi_olurluk': r['en_iyi_olurluk_orani']})
                    okl = sorted([(rs[s]['kayip_yuzde'], s) for s in SIRALAR if rs[s]['olurlu']])
                    if okl:
                        row.update(en_az_goturen=okl[0][1], n_olurlu_siralama=len(okl))
                        if len(okl) > 1:
                            row.update(fark_ikinciye_yuzde_puani=okl[1][0] - okl[0][0], ikinci=okl[1][1],
                                       fark_en_kotuye_yuzde_puani=okl[-1][0] - okl[0][0])
                    else:
                        row.update(en_az_goturen='yok', n_olurlu_siralama=0)
                    for s in ('S1', 'S2'):
                        r = rs[s]
                        row.update({s + '_aktarim_osce_puan': r.get('aktarim_gD_osce_gunu_puan', float('nan')),
                                    s + '_aktarim_dus_puan': r.get('aktarim_gD_dus_gunu_puan', float('nan')),
                                    s + '_aktarim_kalan_oran': r.get('aktarim_kalan_oran', float('nan')),
                                    s + '_salt_unutma': r.get('salt_unutma_carpani', float('nan'))})
                    R_s.append(row)
    wcsv(os.path.join(OUT, 'siralama_karsilastirma.csv'), R_s)
    # --- sinamalar
    def TS(ad, deger, esik, gecti, not_):
        tests.append(dict(sinama=ad, sonuc='geçti' if gecti else 'kaldı', sayi=deger, esik=esik, aciklama=not_))
    TS('motor_ref_sim_esitligi', tmax['motor'], '<1e-9', tmax['motor'] < 1e-9,
      'yurut ile sim.ref_sim: temel takvimde e(t), f1, f2 en buyuk mutlak fark')
    TS('pay0_omega0_gD_temel', tmax['pay0'], '<1e-9', tmax['pay0'] < 1e-9,
      'butun paylar 0, omega 0: gD ve P temel kosuyla (ref_sim) ayni; S3 takvimi dahil')
    TS('S3_pay00_P_temel', tmax['s3pay0'], '<1e-9', tmax['s3pay0'] < 1e-9, 'S3, DUS oncesi pay 0: DUS P = temel (omega ne olursa olsun)')
    TS('pay1_omegaND0_gD_yalniz_unutma', tmax['pay1'], '<1e-9', tmax['pay1'] < 1e-9, 'pay 1, omegaND 0: gD(332) = 0,3*(1-1/tauG)^332')
    TS('omega1_eL1_SN_esit_S_iki_stok_ayni', tmax['omega1'], '<1e-9', tmax['omega1'] < 1e-9, 'A ve B katsayilari iki stokta ayni')
    TS('yorgunluk_ve_e_paydan_bagimsiz', tmax['degismez'], '=0', tmax['degismez'] == 0.0,
      'yapisal: e(t), f1, f2 paylardan once bir kez hesaplanir; butun pay kosularindan sonra dizilerin toplami degismedi')
    TS('net_saat_korunumu', tmax['saat'], '<1e-9', tmax['saat'] < 1e-9, 'pay 1 iken Virtual OSCE net saati = uygulanan toplam net saat')
    TS('gun_esdegeri_egrisi_k0', tmax['egri0'], '<1e-9', tmax['egri0'] < 1e-9, 'k = 0 iken iki egri de temel P ile ayni')
    TS('olurluk_payla_azalmaz', mono['pay'], '=0', mono['pay'] == 0, 'pay artinca olurluk orani dusen secenek sayisi (%d karsilastirma)' % mono['n'])
    TS('olurluk_omegayla_azalmaz', mono['omega'], '=0', mono['omega'] == 0, 'omega artinca olurluk orani dusen secenek sayisi')
    TS('cokus_orani', max(cokus), 'bilgi', True, 'herhangi bir takvimde cokuse giren cekim orani (en yuksek)')
    TS('K1_K0_ayni_politika', float(all(r['K0_ile_ayni'] for r in R_y if r['yuk'] == 'K1')), 'bilgi', True,
      'ana_tablo.csv: (b1), 360 gun, K1 saglam politikasi K0 ile ayni mi (1 = evet)')
    TS('kabul_sayisi', float(min(r['n_cekim'] for r in R_y)), '>=1000', min(r['n_cekim'] for r in R_y) >= 1000, 'tohum 101')
    wcsv(os.path.join(OUT, 'sinamalar.csv'), tests)
    wcsv(os.path.join(OUT, 'sure.csv'), [dict(asama='hesap', duvar_s=round(time.time() - t0, 1), hucre=len(ana),
                                                secenek=len(R_o))])
    for r in tests:
        print('%-40s %-6s %s' % (r['sinama'], r['sonuc'], r['sayi']), flush=True)
    print('toplam %.1f s' % (time.time() - t0), flush=True)


def rapor():
    """IKI_SINAV.md: butun sayilar cikti/iki_sinav/ altindaki CSV'lerden okunur."""
    rd = lambda ad: rcsv(os.path.join(OUT, ad + '.csv'))
    hc, sk, oe, p0, du, sn, yk, eg, su = (rd(x) for x in ('hucreler', 'siralama_karsilastirma', 'omega_etkisi',
                                           'pay0_olurluk', 'duyarlilik', 'sinamalar', 'yukler', 'temel_egri', 'sure'))

    def nm(x, nd=1):
        x = F(x)
        if not np.isfinite(x):
            return '–'
        return tr(0.0 if abs(x) < 0.5 * 10 ** (-nd) else x, nd).replace('-', '−')
    pg = lambda x: ('%g' % F(x)).replace('.', ',')
    ac = lambda x: tr(x, 2)
    yz = lambda x, nd=1: nm(100.0 * F(x), nd)
    hs = lambda x: h05(x).replace('-', '−')
    ok = lambda r: r['olurlu'] == '1'
    H3 = ('6', '7'); AC = ('0.05', '0.15', '0.3'); OMS = ('dusuk', 'orta', 'yuksek')
    OMAD = {'dusuk': 'düşük', 'orta': 'orta', 'yuksek': 'yüksek'}
    Hc = {(r['siralama'], r['yuk'], r['h3'], r['omega'], r['acik']): r for r in hc}
    L = []; A = L.append

    def aralik(v, nd=2, carp=1.0):
        v = [carp * x for x in v if np.isfinite(x)]
        if not v:
            return '–'
        a_, b_ = nm(min(v), nd), nm(max(v), nd)
        return a_ if a_ == b_ else '%s–%s' % (a_, b_)

    def hcr(r):
        if not ok(r):
            return 'olurlu değil (en iyi %%%s)' % yz(r['en_iyi_olurluk_orani'], 1)
        return '%s / %s · %s s · %%%s' % (pg(r['D1']), pg(r['D2']), hs(r['osce_net_saat']), nm(r['kayip_yuzde'], 2))
    # --- ana sonuc icin sayilar
    k2 = lambda s_: [F(r['kayip_yuzde']) for r in hc if r['yuk'] == 'K2' and r['omega'] == 'orta' and r['siralama'] == s_ and ok(r)]
    olr = [r for r in hc if ok(r)]
    enk = max(olr, key=lambda r: F(r['kayip_yuzde']))
    s3 = [r for r in olr if r['siralama'] == 'S3']
    s3sifir = [r for r in s3 if F(r['D1']) == 0 and F(r['D2']) == 0]
    s3pay = [r for r in s3 if F(r['D1']) > 0 or F(r['D2']) > 0]
    s3kotu = 0
    for r in s3pay:
        dig = [Hc[(s_, r['yuk'], r['h3'], r['omega'], r['acik'])] for s_ in ('S1', 'S2')]
        dig = [F(o['kayip_yuzde']) for o in dig if ok(o)]
        s3kotu += int(bool(dig) and F(r['kayip_yuzde']) > max(dig))
    say = collections.Counter(r['en_az_goturen'] for r in sk)
    p0s3 = {(r['h3'], r['yuk'], r['acik'], r['omega'], r['bos_gun']): F(r['olurluk_orani']) for r in p0
            if r['varyant'] == 'ana' and r['siralama'] == 'S3'}
    p0b0 = [v for k, v in p0s3.items() if k[4] == '0']
    s1yok = [r for r in hc if r['siralama'] == 'S1' and not ok(r)]
    yokm = '; '.join('%s: açık %s' % (K, ' ve '.join(ac(a) for a in sorted({r['acik'] for r in s1yok if r['yuk'] == K}, key=float)))
                     for K in YUKLER if any(r['yuk'] == K for r in s1yok))
    bosk = ' / '.join(sorted({r['bos_gun'] for r in olr}))
    s3komb = ', '.join(sorted({'%s–%s' % (r['yuk'], OMAD[r['omega']]) for r in s3pay}))
    EG = {(r['h3'], r['yuk'], r['tur'], r['k_gun']): F(r['P_ort']) for r in eg}
    son100 = [100 * (EG[(h, K, 'sinav_erken', '0')] - EG[(h, K, 'sinav_erken', '100')]) for h in H3 for K in ('K1', 'K3')]
    gun1 = [100 * (EG[(h, K, 'son_gunler_bos', '0')] - EG[(h, K, 'son_gunler_bos', '1')]) for h in H3 for K in YUKLER]

    A('# İki sınav uzantısı: DUS + Virtual OSCE')
    A('')
    A('h3 = 6 ve 7, 1.000\'er çekim (tohum 101), %d hücre × 75 seçenek, hesap %s s. '
      'Sayılar `cikti/iki_sinav/` altındaki CSV\'lerden.' % (len(hc), nm(su[0]['duvar_s'], 0)))
    A('')
    A('## 1. Ana sonuç')
    A('')
    A('Aynı günlük yükle Virtual OSCE koşulunu da tutturmanın DUS sınav günü P\'sine maliyeti olurlu hücrelerde küçüktür: K2 yükü ve orta '
      'aktarımda S1\'de %%%s, S2\'de %%%s, S3\'te %%%s; en kötü hücrede %%%s (%s, %s, h3 = %s, %s aktarım). '
      'S3 (önce DUS, 29 gün sonra Virtual OSCE) %d karşılaştırmanın %d tanesinde DUS\'tan en az götüren sıralamadır ve %d hücrede maliyeti '
      'sıfırdır; ama DUS öncesi pay 0 iken koşulun tuttuğu çekim oranı %%%s arasında, %%90 eşiğinin iki yanındadır ve eşiğin altında '
      'kalan %d hücrenin (%s) %s S3 en pahalı sıralamadır (kayıp %%%s). '
      'S1 (1 Mart) %d hücrede hiçbir payla olurlu değildir (%s); boş gün bütün olurlu hücrelerde %s seçilmiştir.'
      % (aralik(k2('S1')), aralik(k2('S2')), aralik(k2('S3'), 1), nm(enk['kayip_yuzde'], 1), enk['siralama'], enk['yuk'], enk['h3'],
         OMAD[enk['omega']], len(sk), say['S3'], len(s3sifir), aralik(p0b0, 0, 100.0), len(s3pay), s3komb,
         'hepsinde' if s3kotu == len(s3pay) else ('%d tanesinde' % s3kotu),
         aralik([F(r['kayip_yuzde']) for r in s3pay], 1), len(s1yok), yokm, bosk))
    A('')
    A('**Kullanılan yükler (kaynak: yukler.csv; ana_tablo.csv, amaç b1, 360 gün).** K1 politikası K0 ile aynıdır.')
    A('')
    A('| h3 | yük | hA + hB | gün/hafta | hafif hafta | haftalık saat |')
    A('|---|---|---|---|---|---|')
    for r in yk:
        A('| %s | %s | %s + %s | %s | %s | %s |' % (r['h3'], r['yuk'], nm(r['hA']), nm(r['hB']), r['gun_hafta'],
                                                    'yok' if r['hafif_hafta'] == '0' else (r['hafif_hafta'] + ' haftada bir'), h05(r['haftalik_saat'])))
    A('')
    A('## 2. Sıralama karşılaştırması')
    A('')
    A('**Tablo 1 — K2 yükü, orta aktarım (kaynak: hucreler.csv).** Pay: Virtual OSCE payı. Gün-B: aynı kaybı veren '
      '"DUS\'tan önceki son k gün hiç çalışılmasa"; gün-A: "DUS k gün erkene alınsa".')
    A('')
    A('| h3 | açık | sıralama | pay D1 / D2 | boş gün | Virtual OSCE net saat | hafta | DUS kaybı % | gün-B | gün-A | koşulun tuttuğu çekim % |')
    A('|---|---|---|---|---|---|---|---|---|---|---|')
    for h in H3:
        for a in AC:
            for s_ in SIRALAR:
                r = Hc[(s_, 'K2', h, 'orta', a)]
                if ok(r):
                    A('| %s | %s | %s | %s / %s | %s | %s | %s | %s | %s | %s | %s |' % (
                        h, ac(a), s_, pg(r['D1']), pg(r['D2']), r['bos_gun'], hs(r['osce_net_saat']), nm(r['osce_yayilma_hafta']),
                        nm(r['kayip_yuzde'], 2), nm(r['kayip_gun_son_gunler_bos']), nm(r['kayip_gun_sinav_erken'], 0), yz(r['olurluk_orani'])))
                else:
                    A('| %s | %s | %s | olurlu değil | – | – | – | – | – | – | en iyi %s |' % (h, ac(a), s_, yz(r['en_iyi_olurluk_orani'])))
    A('')
    A('Gün-A büyüktür, çünkü modelde DUS bilgisi son aylarda doygundur: temel koşuda son 100 gün P\'ye yalnız %s puan katar, '
      'sınavdan önceki tek boş gün ise %s puan götürür (temel_egri.csv). Kaybın küçüklüğü bu varsayımın sonucudur; '
      'güvenilecek ölçü yüzde kayıptır.' % (aralik(son100, 1), aralik(gun1, 2)))
    A('')
    t2 = [r for r in sk if r['yuk'] == 'K2' and r['omega'] == 'orta']
    kal = [F(r[s_ + '_aktarim_kalan_oran']) for r in t2 for s_ in ('S1', 'S2')]
    salt = [F(r[s_ + '_salt_unutma']) for r in t2 for s_ in ('S1', 'S2')]
    A('**Tablo 2 — En az götüren sıralama ve aktarımın erimesi (K2, orta aktarım; kaynak: siralama_karsilastirma.csv).** Aktarım: '
      'Virtual OSCE çalışmasının gD\'ye kattığı puan, OSCE günü → DUS günü.')
    A('')
    A('| h3 | açık | en az götüren | ikinciye fark, yüzde puanı | en kötüye fark | S1 aktarım | S2 aktarım | yalnız unutmayla kalan, S1 / S2 % |')
    A('|---|---|---|---|---|---|---|---|')
    for r in t2:
        fk = lambda s_: ('%s → %s' % (nm(r[s_ + '_aktarim_osce_puan'], 1), nm(r[s_ + '_aktarim_dus_puan'], 2))) if r[s_ + '_olurlu'] == '1' else 'olurlu değil'
        A('| %s | %s | %s | %s | %s | %s | %s | %s |' % (
            r['h3'], ac(r['acik']), r['en_az_goturen'],
            ('%s (%s)' % (nm(r['fark_ikinciye_yuzde_puani'], 2), r['ikinci'])) if r.get('ikinci') else '–',
            nm(r['fark_en_kotuye_yuzde_puani'], 2), fk('S1'), fk('S2'), ' / '.join(yz(r[s_ + '_salt_unutma'], 0) for s_ in ('S1', 'S2'))))
    A('')
    A('gD\'ye aktarılan katkının DUS gününe yalnız %%%s kadarı kalır; yalnız unutma işleseydi %%%s kalırdı. Fark, sonraki DUS '
      'çalışmasının aynı bilgiyi zaten kazandıracak olmasındandır. gN\'nin sonraki düşüşü sonuca girmez.'
      % (aralik(kal, 0, 100.0), aralik(salt, 0, 100.0)))
    A('')
    A('## 3. Pay tablosu')
    A('')
    A('**Tablo 3 — Orta aktarım (kaynak: hucreler.csv).** Hücre: D1 / D2 · Virtual OSCE net saati · DUS kaybı %.')
    A('')
    A('| h3 | yük | açık | S1 | S2 | S3 |')
    A('|---|---|---|---|---|---|')
    for h in H3:
        for K in YUKLER:
            for a in AC:
                A('| %s | %s | %s | %s |' % (h, K, ac(a), ' | '.join(hcr(Hc[(s_, K, h, 'orta', a)]) for s_ in SIRALAR)))
    A('')
    A('Koşul hiçbir seçenekte bütün çekimlerde tutmaz: hücrelerin en iyi seçeneğinde oran %%%s. Eşik tavana yakın olduğundan '
      'paylar eşiğe duyarlıdır.' % aralik([F(r['en_iyi_olurluk_orani']) for r in hc], 1, 100.0))
    A('')
    A('## 4. Aktarım (ω) etkisi')
    A('')
    A('**Tablo 4 — K2 yükü; düşük → orta → yüksek (kaynak: omega_etkisi.csv).**')
    A('')
    A('| h3 | sıralama | açık | Virtual OSCE net saat | DUS kaybı % | gün-B |')
    A('|---|---|---|---|---|---|')
    OE = {(r['siralama'], r['yuk'], r['h3'], r['acik']): r for r in oe}
    for h in H3:
        for s_ in SIRALAR:
            for a in AC:
                r = OE[(s_, 'K2', h, a)]
                uc = lambda alan, f_: ' → '.join(f_(r[alan + o]) if r['olurlu_' + o] == '1' else 'yok' for o in OMS)
                A('| %s | %s | %s | %s | %s | %s |' % (h, s_, ac(a), uc('saat_', hs), uc('kayip_yuzde_', lambda x: nm(x, 2)),
                                                       uc('gun_bos_', nm)))
    ob = [r for r in oe if r['saat_degisim'] != '']
    A('')
    A('İki uçta da olurlu %d hücrede düşükten yükseğe geçişte ortalama değişim: Virtual OSCE net saati %s, DUS kaybı '
      '%s yüzde puanı, gün-B %s gün.'
      % (len(ob), hs(np.mean([F(r['saat_degisim']) for r in ob])), nm(np.mean([F(r['kayip_yuzde_degisim']) for r in ob]), 2),
         nm(np.mean([F(r['gun_bos_degisim']) for r in ob]), 1)))
    A('')
    A('## 5. S3\'ün olurluğu')
    A('')
    A('**Tablo 5 — DUS öncesi pay 0 iken koşulun sağlandığı çekim oranı, % (kaynak: pay0_olurluk.csv).** Eşik 90.')
    A('')
    A('| h3 | yük | açık | düşük ω, boş 0 | orta ω, boş 0 | yüksek ω, boş 0 | orta ω, boş 3 | orta ω, boş 7 |')
    A('|---|---|---|---|---|---|---|---|')
    for h in H3:
        for K in YUKLER:
            for a in AC:
                A('| %s | %s | %s | %s | %s | %s |' % (h, K, ac(a), ' | '.join(yz(p0s3[(h, K, a, o, '0')]) for o in OMS),
                                                    yz(p0s3[(h, K, a, 'orta', '3')]), yz(p0s3[(h, K, a, 'orta', '7')])))
    acet = max(max(p0s3[(h, K, a, o, '0')] for a in AC) - min(p0s3[(h, K, a, o, '0')] for a in AC) for h in H3 for K in YUKLER for o in OMS)
    gec = {o: [K for K in YUKLER if all(p0s3[(h, K, a, o, '0')] >= OLURLUK for h in H3 for a in AC)] for o in OMS}
    A('')
    A('Açık düzeyi oranı en çok %s puan oynatır. Eşiği her h3 ve açıkta geçen yükler: %s.'
      % (nm(100 * acet, 1), '; '.join('%s aktarımda %s' % (OMAD[o], ', '.join(gec[o]) or 'hiçbiri') for o in OMS)))
    A('')
    A('## 6. Duyarlılık')
    A('')
    A('**Tablo 6 — K2, orta aktarım; hücre: D1 / D2 · net saat · DUS kaybı % (kaynak: duyarlilik.csv).**')
    A('')
    A('| h3 | sıralama | açık | ana (eL = 0,83) | eL = 1,0 | κN alt yarı | κN üst yarı |')
    A('|---|---|---|---|---|---|---|')
    DU = {(r['varyant'], r['siralama'], r['yuk'], r['h3'], r['omega'], r['acik']): r for r in du}
    VAR = ('ana', 'eL_1', 'kN_alt', 'kN_ust')
    for h in H3:
        for s_ in SIRALAR:
            for a in AC:
                A('| %s | %s | %s | %s |' % (h, s_, ac(a), ' | '.join(hcr(DU[(v, s_, 'K2', h, 'orta', a)]) for v in VAR)))
    anah = sorted({k[1:] for k in DU})
    nol = {v: sum(ok(DU[(v,) + k]) for k in anah) for v in VAR}

    def fark(v1, v2, alan):
        d = [F(DU[(v2,) + k][alan]) - F(DU[(v1,) + k][alan]) for k in anah if ok(DU[(v1,) + k]) and ok(DU[(v2,) + k])]
        return float(np.median(d))
    A('')
    A('Dil yükü kalkınca (eL = 1) olurlu hücre sayısı %d → %d; ikisinde de olurlu hücrelerde ortanca değişim %s saat ve %s yüzde puanı. '
      'κN\'nin alt yarısında (Virtual OSCE kapsamı küçük) %d, üst yarısında %d hücre olurlu; üst yarı ortanca %s saat ve '
      '%s yüzde puanı daha pahalı.'
      % (nol['ana'], nol['eL_1'], hs(fark('ana', 'eL_1', 'osce_net_saat')), nm(fark('ana', 'eL_1', 'kayip_yuzde'), 2),
         nol['kN_alt'], nol['kN_ust'], hs(fark('kN_alt', 'kN_ust', 'osce_net_saat')), nm(fark('kN_alt', 'kN_ust', 'kayip_yuzde'), 2)))
    A('')
    A('## 7. Yorum kararları')
    A('')
    A('- sim.py\'den `sample_params`, `derive`, `Mint`, `Lload`, `ref_sim` içe aktarıldı; `ref_sim` tek sınavlı takvim kurduğundan gün '
      'döngüsü `yurut` içinde aynı kurallarla yinelendi.')
    A('- Boş günler ilk sınav gününden başlar (0 = sınav günü de çalışılır); hafif hafta takvimi 0. güne bağlıdır; ana tablodaki T ve ψ kullanılmadı.')
    A('- e(t) ve net saat aynı payla bölünür; gN0 = Pgeç − açık.')
    A('- Eşitlikte sıra: ortalama DUS P, olurluk oranı, daha çok boş gün.')
    A('- Kayıp = 1 − ort. P / ort. P(temel); hafta = payın sıfırdan büyük olduğu günlerin takvim aralığı.')
    A('- "Kaç güne denk" iki biçimde okunabildiğinden ikisi de verildi; gün-A, K2\'de 42 günlük hafif hafta döngüsünün aynı evresinde okundu.')
    A('- κN yarıları ortancadan bölündü; karar kuralı her yarıda yeniden uygulandı.')
    A('')
    A('## 8. Sınamalar (kaynak: sinamalar.csv)')
    A('')
    ACK = {'motor_ref_sim_esitligi': 'yurut ile sim.ref_sim: temel takvimde e(t), f1, f2 farkı',
           'pay0_omega0_gD_temel': 'bütün paylar 0, ω = 0: gD ve P temel koşuyla aynı',
           'S3_pay00_P_temel': 'S3, DUS öncesi pay 0: DUS P = temel',
           'pay1_omegaND0_gD_yalniz_unutma': 'pay 1, ωND = 0: gD(332) = 0,3·(1 − 1/τG)^332',
           'omega1_eL1_SN_esit_S_iki_stok_ayni': 'ω = 1, eL = 1, S_N = S: iki stok aynı ilerler',
           'yorgunluk_ve_e_paydan_bagimsiz': 'e(t), f1, f2 paylardan önce bir kez hesaplanır; pay koşularından sonra diziler değişmedi',
           'net_saat_korunumu': 'pay 1 iken Virtual OSCE net saati = toplam net saat',
           'gun_esdegeri_egrisi_k0': 'k = 0 iken iki gün eğrisi de temel P',
           'olurluk_payla_azalmaz': 'pay artınca olurluk oranı düşen seçenek sayısı',
           'olurluk_omegayla_azalmaz': 'ω artınca olurluk oranı düşen seçenek sayısı',
           'cokus_orani': 'herhangi bir takvimde çöküşe giren çekim oranı',
           'K1_K0_ayni_politika': 'K1 sağlam politikası K0 ile aynı mı (1 = evet)',
           'kabul_sayisi': 'h3 başına kabul edilmiş çekim (tohum 101)'}
    A('| sınama | sonuç | sayı | eşik | ne sınandı |')
    A('|---|---|---|---|---|')
    for r in sn:
        A('| %s | %s | %s | %s | %s |' % (r['sinama'], r['sonuc'], ('%.1e' % F(r['sayi'])).replace('.', ',') if 0 < abs(F(r['sayi'])) < 1e-3 else pg(r['sayi']),
                                          r['esik'], ACK.get(r['sinama'], r['aciklama'])))
    A('')
    A('## 9. Sunum cümlesi')
    A('')
    A('"Bu tablo ölçüm değil: aynı günlük yük iki sınava bölünürse, varsayılan aktarım ve kapsam oranlarıyla DUS\'tan ne gittiğini söyleyen '
      'bir hesap. Güvenilecek kısım yöndür: erken sapma geç sapmadan ucuzdur; önce DUS sıralamasının bedava olup olmadığını aktarım oranı '
      'ile DUS sonrası 29 günün yetip yetmediği belirler, ikisi de ölçülmemiştir. Kaybın küçüklüğü modelin doygunluk varsayımından gelir; '
      'sıralama sınavında küçük bir P farkının değerini model söylemez."')
    A('')
    yol = os.path.join(HERE, 'IKI_SINAV.md')
    with open(yol, 'w', encoding='utf-8') as f:
        f.write('\n'.join(L))
    kelime = sum(len(x.split()) for x in L if not x.startswith('|'))
    print('IKI_SINAV.md yazildi; tablo disi kelime: %d' % kelime, flush=True)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'rapor':
        rapor()
    else:
        hesap(); rapor()
