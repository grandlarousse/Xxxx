#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MODEL_TANIMI.md v2 (bolum 1-8, 10) uygulamasi. Yalniz numpy.

Kullanim:
  python3 sim.py                # hesap (ara sonuclar cikti/ara/ altinda saklanir) + CSV + SONUC.md
  python3 sim.py --temiz        # ara sonuclari silip bastan
  python3 sim.py rapor          # yalniz SONUC.md (CSV'lerden)
  python3 sim.py --hizli --cikti /tmp/x   # kucuk duman kosusu

Bu model olcum degil, varsayimlari tutarli bir programa ceviren hesap aracidir.
"""
import os
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ.setdefault(_v, '1')
import sys, csv, json, math, time, argparse, shutil
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
HORIZONS = [30, 90, 120, 150, 180, 270, 360]
H3S = [5.0, 6.0, 7.0, 8.0]
SEEDS = [101, 202]
HB_VALS = np.array([0.0, 1.0, 2.0, 3.0])
D_VALS = np.array([5, 6, 7])
N_VALS = np.array([0, 6, 4, 3])            # 0 = hafif hafta yok
OPTS = [(0, 1.0)] + [(T, psi) for T in (3, 7, 14) for psi in (0.5, 0.75, 1.25)]
MULTS = np.array([0.0, 0.25, 0.375, 0.5, 0.625, 0.75, 1.0, 1.25])
HALF_IDX = np.array([0, 1, 2, 1, 4, 2, 3, 4])   # cokuste saat carpani yarilanir
MI_ONE, MI_HALF = 6, 3
PSI_MI = np.array([3, 5, 7])
TOLS = (0.02, 0.01, 0.05)
GAPS = (0.05, 0.15, 0.30)
G0_DUS = 0.3
Z95 = 1.6448536269514722
BIG = 1e30
LAMBDAS = (0.0, 0.02, 0.05)
Y_H = [90, 360]
OBJ = ('a', 'b1', 'b1e0')
KN = ('K0', 'K1', 'K2', 'K3')
PARAM_NAMES = ['h0', 'v1', 'u50', 's', 'eB', 'cB', 'gamma', 'tau1', 'tau2', 'q1', 'qK', 'qcol',
               'tauG', 'S', 'kN', 'e1', 'e2', 'Pgec', 'sigP']
BUF_VARS = ('sumE', 'sumH', 'AD', 'BD', 'AN', 'BN', 'f1', 'f2', 'qa', 'qr', 'ql', 'peak', 'ever')
NI, DU = 520, 1.0 / 32.0
_GX64, _GW64 = np.polynomial.legendre.leggauss(64)
_GX4, _GW4 = np.polynomial.legendre.leggauss(4)


# ---------------------------------------------------------------- temel fonksiyonlar
def Mint(lo, hi, u50, s):
    """int_lo^hi 1/(1+(u/u50)^s) du, 64 noktali Gauss-Legendre (referans yol)."""
    lo = np.asarray(lo, float); hi = np.asarray(hi, float)
    half = (hi - lo) / 2.0; mid = (hi + lo) / 2.0
    u = mid[..., None] + half[..., None] * _GX64
    v = 1.0 / (1.0 + (u / np.asarray(u50)[..., None]) ** np.asarray(s)[..., None])
    return (v * _GW64).sum(-1) * half


def build_Mcum(u50, s):
    """Birikimli integral tablosu, adim 1/32 saat (hizli motor)."""
    edges = np.arange(NI) * DU
    u = (edges[:, None] + (_GX4[None, :] + 1.0) * 0.5 * DU).ravel()
    v = 1.0 / (1.0 + (u[None, :] / u50[:, None]) ** s[:, None])
    seg = (v.reshape(len(u50), NI, 4) * _GW4).sum(-1) * (DU / 2.0)
    return np.concatenate([np.zeros((len(u50), 1)), np.cumsum(seg, axis=1)], axis=1)


def Lload(h, h0, gamma):
    """Yuksek talepli h saatin yuku: int_0^h (1 + gamma*max(0,u-h0)) du."""
    return h + gamma * np.maximum(0.0, h - h0) ** 2 / 2.0


def f1_mornings(x, rho):
    """6 gun x fazla yuk + 1 gun dinlenme dongusunde duragan sabah f1 degerleri (k=1..7)."""
    x = np.asarray(x, float); rho = np.asarray(rho, float)
    F6 = x * rho * (1 - rho ** 6) / ((1 - rho) * (1 - rho ** 7))
    F0 = rho * F6
    out = []
    for k in range(1, 7):
        out.append(F0 * rho ** k + x * rho * (1 - rho ** k) / (1 - rho))
    out.append(F0)
    return np.stack(out, axis=-1)


def a_closed(x1, rho1):
    return x1 * rho1 * (1 - rho1 ** 6) / ((1 - rho1) * (1 - rho1 ** 7))


def fcrit_closed(x3, rho1, rho2, a):
    F = f1_mornings(x3, rho1)
    u = np.maximum(0.0, F - np.asarray(a)[..., None])
    k = np.arange(1, 8)
    G0 = (u * np.asarray(rho2)[..., None] ** (7 - k)).sum(-1) / (1 - rho2 ** 7)
    G = G0; best = np.zeros_like(G0)
    for j in range(7):
        G = G * rho2 + u[..., j]
        best = np.maximum(best, G)
    return best


def param_ranges(h3):
    return [('h0', 3.0, min(5.5, h3 - 1.0), 'lin'), ('v1', .25, .75, 'lin'), ('u50', 4.0, 10.0, 'lin'),
            ('s', 2.0, 6.0, 'lin'), ('eB', .3, .7, 'lin'), ('cB', .3, .8, 'lin'), ('gamma', 0.0, .4, 'lin'),
            ('tau1', .5, 2.0, 'lin'), ('tau2', 7.0, 28.0, 'lin'), ('q1', .93, .99, 'lin'),
            ('qK', .6, .9, 'lin'), ('qcol', .3, .6, 'lin'), ('tauG', 90.0, 400.0, 'lin'),
            ('S', 30.0, 1000.0, 'log'), ('kN', .25, .6, 'lin'), ('e1', 0.0, .03, 'lin'),
            ('e2', 0.0, .10, 'lin'), ('Pgec', .64, .69, 'lin'), ('sigP', .03, .05, 'lin')]


def g180_anchor(u50, s, S, tauG):
    e = Mint(0.0, 6.0, u50, s)
    g = np.full_like(e, G0_DUS)
    for t in range(180):
        et = e if (t % 7) < 6 else 0.0
        g = g - g / tauG + (et / S) * (1.0 - g)
    return g


def _stats(M):
    return np.column_stack([M.mean(0), np.percentile(M, 5, axis=0), np.percentile(M, 50, axis=0),
                            np.percentile(M, 95, axis=0)])


def sample_params(h3, seed, n_target):
    """Latin hiperkup + ogrenme dayanagi kabulu. Ilk n_target kabul edilen cekim kullanilir."""
    rng = np.random.default_rng([int(seed), int(round(h3 * 10))])
    rr = param_ranges(h3); k = len(rr)
    n0 = 4 * n_target
    while True:
        X = np.empty((n0, k))
        for j, (nm, lo, hi, kind) in enumerate(rr):
            u = (rng.permutation(n0) + rng.random(n0)) / n0
            X[:, j] = lo + u * (hi - lo) if kind == 'lin' else np.exp(np.log(lo) + u * (np.log(hi) - np.log(lo)))
        g = g180_anchor(X[:, 2], X[:, 3], X[:, 13], X[:, 12])
        ok = (g >= 0.65) & (g <= 0.90)
        if ok.sum() >= n_target:
            break
        n0 *= 2
    idx = np.flatnonzero(ok)[:n_target]
    pr = {nm: X[idx, j].copy() for j, (nm, _, _, _) in enumerate(rr)}
    info = dict(n_prior=n0, n_acc=int(ok.sum()), prior_stats=_stats(X), acc_stats=_stats(X[ok]),
                used_stats=_stats(X[idx]))
    return pr, info


def derive(pr, h3):
    d = dict(pr)
    h0 = pr['h0']; gam = pr['gamma']
    h1 = h0 + pr['v1'] * (h3 - h0)
    rho1 = np.exp(-1.0 / pr['tau1']); rho2 = np.exp(-1.0 / pr['tau2'])
    a = a_closed(Lload(h1, h0, gam) - h0, rho1)
    Fcrit = fcrit_closed(Lload(h3, h0, gam) - h0, rho1, rho2, a)
    d.update(h3=np.full_like(h0, h3), h1=h1, rho1=rho1, rho2=rho2, rho2c=np.exp(-1.0 / (3.0 * pr['tau2'])),
             a=a, Fcrit=Fcrit, b1=(1.0 / pr['q1'] - 1.0) / a, b2=(1.0 / pr['qK'] - 1.0) / Fcrit)
    return d


def klev_from(qa, qr, ql, ever, peakn, tol):
    """Yazildigi gibi (literal) kumeler ve ic ice seviye: K3 yazildigi gibi; K2=(K0|K1|K2 kosulu)&K3; K1=(K0|K1 kosulu)&K3."""
    thr = 1.0 - tol
    K0 = qa >= thr
    K1l = (qr < 1e29) & (qr >= thr)
    K2l = (ql < 1e29) & (ql >= thr) & ~ever
    K3l = ~ever & (peakn <= 0.8)
    kl = np.full(K0.shape, 4, np.int8)
    kl[K3l] = 3; kl[K3l & K2l] = 2; kl[K3l & K1l] = 1; kl[K3l & K0] = 0
    return kl, (K0, K1l, K2l, K3l)


def delay_days(H, k):
    return int(math.floor(H * k / 4.0 + 0.5))


# ---------------------------------------------------------------- politika izgarasi
class Grid:
    def __init__(self, step=0.5, maxday=360):
        self.step = step
        self.hA_vals = np.arange(1.0, 10.0 + 1e-9, step)
        nA = len(self.hA_vals)
        iA, iB, iD, iN = np.meshgrid(np.arange(nA), np.arange(4), np.arange(3), np.arange(4), indexing='ij')
        self.p_hA = self.hA_vals[iA.ravel()]; self.p_hB = HB_VALS[iB.ravel()]
        self.p_d = D_VALS[iD.ravel()]; self.p_n = N_VALS[iN.ravel()]
        self.P = self.p_hA.size
        self.combo = (iA * 4 + iB).ravel()
        self.cA = np.repeat(self.hA_vals, 4); self.cB = np.tile(HB_VALS, nA)
        t = np.arange(maxday); w = t // 7; dow = t % 7
        rest = dow[:, None] >= self.p_d[None, :]
        nn = np.where(self.p_n > 0, self.p_n, 1)[None, :]
        light = (self.p_n[None, :] > 0) & (((w[:, None] + 1) % nn) == 0)
        mi = np.where(rest, 0, np.where(light, MI_HALF, MI_ONE))
        self.cf = self.combo[None, :] * 8 + mi
        self.ch = self.combo[None, :] * 8 + HALF_IDX[mi]
        self.Htab = ((self.cA + self.cB)[:, None] * MULTS[None, :]).ravel()
        self.hf = self.Htab[self.cf]; self.hh = self.Htab[self.ch]
        self.pen_rest = np.where(self.p_d <= 6, 0.0, BIG)
        self.pen_rest3 = np.tile(self.pen_rest, 3)
        wk = np.arange(maxday // 7 + 2)
        self.pen_light = np.where((self.p_n[None, :] > 0) & ((wk[:, None] % nn) == 0), 0.0, BIG)
        self.fk = []
        for dw in range(7):
            restd = dw >= self.p_d
            mi3 = np.where(restd[None, :], 0, PSI_MI[:, None])
            cf = (self.combo[None, :] * 8 + mi3).ravel(); ch = (self.combo[None, :] * 8 + HALF_IDX[mi3]).ravel()
            self.fk.append((cf, ch, self.Htab[cf], self.Htab[ch]))
        self.cumH = np.vstack([np.zeros(self.P), np.cumsum(self.hf, axis=0)])
        self.sub6 = np.flatnonzero((self.p_hB == 0) & (self.p_d == 6) & (self.p_n == 0))
        self._ph = {}

    def planH(self, L, nopt=len(OPTS)):
        """Planlanan toplam net saat (cokus yok varsayimiyla), [nopt*P]."""
        key = (L, nopt)
        if key not in self._ph:
            out = np.full((nopt, self.P), np.nan)
            out[0] = self.cumH[L]
            for o in range(1, nopt):
                T, psi = OPTS[o]
                if T <= L:
                    h = self.cumH[L - T].copy()
                    for tt in range(L - T, L):
                        h += np.where(tt % 7 >= self.p_d, 0.0, psi * (self.p_hA + self.p_hB))
                    out[o] = h
            self._ph[key] = out.ravel()
        return self._ph[key]

    def fields(self, nopt=len(OPTS)):
        oi = np.repeat(np.arange(nopt), self.P); pi = np.tile(np.arange(self.P), nopt)
        return dict(hA=self.p_hA[pi], hB=self.p_hB[pi], d=self.p_d[pi], n=self.p_n[pi],
                    T=np.array([o[0] for o in OPTS])[oi], psi=np.array([o[1] for o in OPTS])[oi], p=pi, o=oi)


# ---------------------------------------------------------------- hizli motor
def engine(pr, grid, main_H, lam=0.0, forks=True, do_b2=True, tols=TOLS, chunk=40, debug=None):
    nd_all = len(pr['h0']); nopt = len(OPTS) if forks else 1
    nH = len(main_H); NP = nopt * grid.P; nt = len(tols)
    acc = dict(sumreg=np.zeros((nH, 3, 4, NP)), featcnt=np.zeros((nH, 4, NP)), cliffcnt=np.zeros((nH, NP)),
               Jstar=np.zeros((nd_all, nH, 3, 4)), best=np.zeros((nd_all, nH, 3, 4), np.int32),
               ceil=np.zeros((nd_all, nH, 4)), Jb_at_a=np.zeros((nd_all, nH, 4)),
               Jb_at_e0=np.zeros((nd_all, nH, 4)), Ja_at_b=np.zeros((nd_all, nH, 4)),
               h3eq_nc=np.zeros((nd_all, nH)), h3eq_k3=np.zeros((nd_all, nH)), nest=np.zeros((nH, 11)))
    if nt > 1:
        acc['sumreg_tol'] = np.zeros((nt - 1, nH, 2, 3, NP))
        acc['best_tol'] = np.zeros((nd_all, nt - 1, nH, 2, 3), np.int32)
    if do_b2:
        acc['b2cnt'] = np.zeros((4, 3, nH, 4, NP), np.int32)
        acc['b2key'] = np.full((nd_all, nH, 3, 4), np.inf)
        acc['b2D'] = np.zeros((nd_all, nH, 3, 4), np.int16)
        acc['b2pol'] = np.zeros((nd_all, nH, 3, 4), np.int32)
    for c0 in range(0, nd_all, chunk):
        sl = slice(c0, min(nd_all, c0 + chunk))
        _chunk({k: v[sl] for k, v in pr.items()}, grid, list(main_H), lam, forks, do_b2, tols, acc, sl, debug)
    return acc


def _chunk(pr, grid, main_H, lam, forks, do_b2, tols, acc, sl, debug):
    nd = len(pr['h0']); P = grid.P; nopt = len(OPTS) if forks else 1; NP = nopt * P
    c_ = lambda k: pr[k][:, None]
    Mcum = build_Mcum(pr['u50'], pr['s'])
    aH = (grid.cA[:, None] * MULTS[None, :]).ravel(); tH = ((grid.cA + grid.cB)[:, None] * MULTS[None, :]).ravel()
    iA = np.rint(aH / DU).astype(np.int64); iT = np.rint(tH / DU).astype(np.int64)
    EA = Mcum[:, iA]
    Etab = EA + c_('eB') * (Mcum[:, iT] - EA)
    h0 = c_('h0'); gam = c_('gamma')
    CA = Lload(aH[None, :], h0, gam); CT = Lload(tH[None, :], h0, gam)
    Xtab = np.maximum(0.0, CA + c_('cB') * (CT - CA) - h0)
    b1 = c_('b1'); b2 = c_('b2'); Fc = c_('Fcrit'); Fin = Fc * (1 + 1e-9); Fex = 0.3 * Fc; qcol = c_('qcol')
    rho1 = c_('rho1'); rho2 = c_('rho2'); rho2c = c_('rho2c'); a = c_('a')
    cg = 1.0 - 1.0 / c_('tauG'); invS = 1.0 / c_('S'); invSN = 1.0 / (c_('kN') * c_('S'))
    rho3 = math.exp(-1.0 / 120.0)
    ar = np.arange(nd)

    def morning(s, pr_, pl_):
        ft = s['f2'] if lam == 0 else s['f2'] + s['f3']
        c = np.where(s['col'], ft >= Fex, ft >= Fin)
        q = 1.0 / (1.0 + b1 * s['f1'] + b2 * ft)
        if c.any():
            q = np.where(c, q * qcol, q); s['ever'] |= c
        np.minimum(s['qa'], q, out=s['qa'])
        if pr_ is not None:
            np.minimum(s['qr'], q + pr_, out=s['qr'])
        if pl_ is not None:
            np.minimum(s['ql'], q + pl_, out=s['ql'])
        np.maximum(s['peak'], ft, out=s['peak'])
        s['col'] = c; s['q'] = q

    def apply(s, cf, ch, hf, hh):
        c = s['col']
        E = np.take(Etab, cf, axis=1); X = np.take(Xtab, cf, axis=1)
        if c.any():
            E = np.where(c, np.take(Etab, ch, axis=1), E); X = np.where(c, np.take(Xtab, ch, axis=1), X)
            s['sumH'] += np.where(c, hh, hf); r2 = np.where(c, rho2c, rho2)
        else:
            s['sumH'] += hf; r2 = rho2
        e = s['q'] * E
        s['sumE'] += e
        r = e * invS; cc = cg - r; s['AD'] *= cc; s['BD'] *= cc; s['BD'] += r
        r = e * invSN; cc = cg - r; s['AN'] *= cc; s['BN'] *= cc; s['BN'] += r
        f1 = s['f1']; f1 += X; f1 *= rho1
        f2 = s['f2']; f2 *= r2; f2 += np.maximum(f1 - a, 0.0)
        if lam != 0:
            f3 = s['f3']; f3 *= rho3; f3 += lam * f2

    z = lambda: np.zeros((nd, P))
    st = dict(f1=z(), f2=z(), f3=z(), q=np.ones((nd, P)), sumE=z(), sumH=z(), AD=np.ones((nd, P)), BD=z(),
              AN=np.ones((nd, P)), BN=z(), qa=np.full((nd, P), BIG), qr=np.full((nd, P), BIG),
              ql=np.full((nd, P), BIG), peak=z(), col=np.zeros((nd, P), bool), ever=np.zeros((nd, P), bool))
    Ls = set(main_H); Lmap = {}
    if do_b2:
        for hi, H in enumerate(main_H):
            for k in range(4):
                L = H - delay_days(H, k)
                Ls.add(L); Lmap.setdefault(L, []).append((hi, k, H - L))
    fork_at = {}
    if forks:
        for L in Ls:
            for iT, T in enumerate((3, 7, 14)):
                if L - T >= 0:
                    fork_at.setdefault(L - T, []).append((L, iT, T))
    bufs = {}

    def get_buf(L):
        if L not in bufs:
            B = {k: (np.zeros((nd, NP), bool) if k == 'ever' else np.zeros((nd, NP))) for k in BUF_VARS}
            B['_valid'] = np.zeros(nopt, bool)
            bufs[L] = B
        return bufs[L]

    def store(L, o0, nb, s):
        B = get_buf(L)
        for k in BUF_VARS:
            B[k][:, o0 * P:(o0 + nb) * P] = s[k]
        B['_valid'][o0:o0 + nb] = True

    def finalize(L):
        B = bufs.pop(L)
        inv = np.repeat(~B['_valid'], P)
        peakn = B['peak'] / Fc
        pen = np.exp(-(c_('e1') * B['f1'] / a + c_('e2') * B['f2'] / Fc))
        kl0, lit = klev_from(B['qa'], B['qr'], B['ql'], B['ever'], peakn, tols[0])
        kl0[:, inv] = 4
        if debug is not None and L in debug['L']:
            dd = {k: B[k].copy() for k in BUF_VARS}; dd['klev'] = kl0.copy()
            debug['buf'].setdefault(L, []).append(dd)
        if L in main_H:
            hi = main_H.index(L)
            Ja = B['sumE']; gD = B['AD'] * G0_DUS + B['BD']; Jb = gD * pen
            objs = (Ja, Jb, gD)
            for ti, tol in enumerate(tols):
                kl = kl0 if ti == 0 else klev_from(B['qa'], B['qr'], B['ql'], B['ever'], peakn, tol)[0]
                for K in range(4 if ti == 0 else 3):
                    feas = kl <= K
                    for oi in range(3 if ti == 0 else 2):
                        J = objs[oi]
                        Jm = np.where(feas, J, -1.0)
                        bi = Jm.argmax(1); Js = Jm[ar, bi]
                        reg = np.where(feas, 1.0 - J / Js[:, None], 1.0).sum(0)
                        if ti == 0:
                            acc['sumreg'][hi, oi, K] += reg
                            acc['Jstar'][sl, hi, oi, K] = Js; acc['best'][sl, hi, oi, K] = bi
                        else:
                            acc['sumreg_tol'][ti - 1, hi, oi, K] += reg
                            acc['best_tol'][sl, ti - 1, hi, oi, K] = bi
                    if ti == 0:
                        acc['featcnt'][hi, K] += feas.sum(0)
                        acc['ceil'][sl, hi, K] = np.where(feas, B['sumH'], -1.0).max(1)
                        ba = acc['best'][sl, hi, 0, K]; bb = acc['best'][sl, hi, 1, K]; b0 = acc['best'][sl, hi, 2, K]
                        acc['Jb_at_a'][sl, hi, K] = Jb[ar, ba]; acc['Jb_at_e0'][sl, hi, K] = Jb[ar, b0]
                        acc['Ja_at_b'][sl, hi, K] = Ja[ar, bb]
            K0, K1l, K2l, K3l = lit
            hasr = B['qr'] < 1e29; hasl = B['ql'] < 1e29
            acc['nest'][hi] += [K0.sum(), K1l.sum(), K2l.sum(), K3l.sum(), (K0 & ~K1l).sum(),
                                (K0 & ~K1l & hasr).sum(), (K1l & ~K2l).sum(), (K1l & ~K2l & hasl).sum(),
                                (K1l & ~K3l).sum(), (K2l & ~K3l).sum(), (K0 & ~K3l).sum()]
            acc['cliffcnt'][hi] += B['ever'].sum(0)
            sub = grid.sub6; hs = grid.p_hA[sub][None, :]
            acc['h3eq_nc'][sl, hi] = np.where(~B['ever'][:, sub], hs, 0.0).max(1)
            acc['h3eq_k3'][sl, hi] = np.where(kl0[:, sub] <= 3, hs, 0.0).max(1)
        if do_b2 and L in Lmap:
            ANp = B['AN'] * pen; BNp = B['BN'] * pen
            keyb = B['sumH'] + 1e-4 * np.minimum(peakn, 5.0)
            thr = (pr['Pgec'] + Z95 * pr['sigP'])[:, None]
            for (hi, k, D) in Lmap[L]:
                decay = (1.0 - 1.0 / pr['tauG']) ** D
                for gi, gap in enumerate(GAPS):
                    g0p = ((pr['Pgec'] - gap) * decay)[:, None]
                    ok = (ANp * g0p + BNp) >= thr
                    for K in range(4):
                        feas = ok & (kl0 <= K)
                        acc['b2cnt'][K, gi, hi, k] += feas.sum(0)
                        key = np.where(feas, keyb, np.inf)
                        j = key.argmin(1); kv = key[ar, j]
                        cur = acc['b2key'][sl, hi, gi, K]; upd = kv < cur
                        acc['b2key'][sl, hi, gi, K] = np.where(upd, kv, cur)
                        acc['b2D'][sl, hi, gi, K] = np.where(upd, k, acc['b2D'][sl, hi, gi, K])
                        acc['b2pol'][sl, hi, gi, K] = np.where(upd, j, acc['b2pol'][sl, hi, gi, K])

    maxL = max(Ls)
    for t in range(maxL + 1):
        chk = (t > 0 and t % 7 == 0)
        morning(st, grid.pen_rest if chk else None, grid.pen_light[t // 7] if chk else None)
        if t in fork_at:
            for (L, iT, T) in fork_at[t]:
                fs = {k: np.tile(v, (1, 3)) for k, v in st.items()}
                for tt in range(t, L):
                    apply(fs, *grid.fk[tt % 7])
                    morning(fs, grid.pen_rest3 if (tt + 1) % 7 == 0 else None, None)
                store(L, 1 + 3 * iT, 3, fs)
        if t in Ls:
            store(t, 0, 1, st)
            finalize(t)
        if t < maxL:
            apply(st, grid.cf[t], grid.ch[t], grid.hf[t], grid.hh[t])


# ---------------------------------------------------------------- referans benzetici (bagimsiz yol)
def ref_sim(pr, pols, H, lam=0.0, tol=0.02, extra=None, keep_e=()):
    """Duz gun dongusu; politikalar (hA,hB,d,n,T,psi) listesi; extra: {sutun: (gun, +saat)}."""
    nd = len(pr['h0']); n = len(pols)
    plA = np.zeros((H, n)); plB = np.zeros((H, n))
    restchk = np.zeros((H + 1, n), bool); lightchk = np.zeros((H + 1, n), bool)
    for j, (hA, hB, d, nn, T, psi) in enumerate(pols):
        for t in range(H):
            w, dow = divmod(t, 7)
            if dow >= d:
                m = 0.0
            elif t >= H - T:
                m = psi
            elif nn > 0 and (w + 1) % nn == 0:
                m = 0.5
            else:
                m = 1.0
            plA[t, j] = hA * m; plB[t, j] = hB * m
        for t in range(7, H + 1, 7):
            if d <= 6:
                restchk[t, j] = True
            if nn > 0 and (t // 7) % nn == 0 and t <= H - T:
                lightchk[t, j] = True
    if extra:
        for j, (day, dh) in extra.items():
            plA[day, j] += dh
    cache = {}

    def EX(ha, hb):
        key = (round(float(ha), 9), round(float(hb), 9))
        if key not in cache:
            E = Mint(0.0, ha, pr['u50'], pr['s']) + pr['eB'] * Mint(ha, ha + hb, pr['u50'], pr['s'])
            W = Lload(ha, pr['h0'], pr['gamma']) + pr['cB'] * (Lload(ha + hb, pr['h0'], pr['gamma'])
                                                             - Lload(ha, pr['h0'], pr['gamma']))
            cache[key] = (E, np.maximum(0.0, W - pr['h0']))
        return cache[key]

    c_ = lambda k: pr[k][:, None]
    Fc = c_('Fcrit'); a = c_('a'); S = c_('S'); cg = 1.0 - 1.0 / c_('tauG')
    f1 = np.zeros((nd, n)); f2 = np.zeros((nd, n)); f3 = np.zeros((nd, n))
    col = np.zeros((nd, n), bool); ever = np.zeros((nd, n), bool)
    sumE = np.zeros((nd, n)); sumH = np.zeros((nd, n)); AD = np.ones((nd, n)); BD = np.zeros((nd, n))
    AN = np.ones((nd, n)); BN = np.zeros((nd, n))
    qa = np.full((nd, n), BIG); qr = np.full((nd, n), BIG); ql = np.full((nd, n), BIG); peak = np.zeros((nd, n))
    es = {j: np.zeros((H, nd)) for j in keep_e}
    for t in range(H + 1):
        ft = f2 + f3
        col = np.where(col, ft >= 0.3 * Fc, ft >= Fc * (1 + 1e-9))
        q = 1.0 / (1.0 + c_('b1') * f1 + c_('b2') * ft)
        q = np.where(col, q * c_('qcol'), q)
        qa = np.minimum(qa, q)
        qr = np.where(restchk[t][None, :], np.minimum(qr, q), qr)
        ql = np.where(lightchk[t][None, :], np.minimum(ql, q), ql)
        peak = np.maximum(peak, ft); ever = ever | col
        if t == H:
            break
        E = np.empty((nd, n)); X = np.empty((nd, n)); Hh = np.empty((nd, n))
        for j in range(n):
            Ef, Xf = EX(plA[t, j], plB[t, j]); Eh, Xh = EX(plA[t, j] / 2.0, plB[t, j] / 2.0)
            cj = col[:, j]
            E[:, j] = np.where(cj, Eh, Ef); X[:, j] = np.where(cj, Xh, Xf)
            Hh[:, j] = np.where(cj, 0.5, 1.0) * (plA[t, j] + plB[t, j])
        e = q * E
        sumE += e; sumH += Hh
        for j in keep_e:
            es[j][t] = e[:, j]
        r = e / S; AD, BD = AD * (cg - r), BD * (cg - r) + r
        r = e / (c_('kN') * S); AN, BN = AN * (cg - r), BN * (cg - r) + r
        f1 = (f1 + X) * c_('rho1')
        f2 = f2 * np.where(col, c_('rho2c'), c_('rho2')) + np.maximum(f1 - a, 0.0)
        if lam != 0:
            f3 = f3 * math.exp(-1.0 / 120.0) + lam * f2
    gD = AD * G0_DUS + BD
    P = gD * np.exp(-(c_('e1') * f1 / a + c_('e2') * f2 / Fc))
    kl, _ = klev_from(qa, qr, ql, ever, peak / Fc, tol)
    return dict(sumE=sumE, sumH=sumH, gD=gD, P=P, AD=AD, BD=BD, AN=AN, BN=BN, f1=f1, f2=f2, qa=qa, qr=qr, ql=ql,
                peak=peak, ever=ever, klev=kl, es=es)


# ---------------------------------------------------------------- gorevler
def p1path(o, h3, s): return os.path.join(o, 'ara', 'p1_h%d_s%d.npz' % (int(h3), s))
def ypath(o, h3, lam): return os.path.join(o, 'ara', 'y_h%d_l%03d.npz' % (int(h3), int(round(lam * 100))))
def convpath(o, step): return os.path.join(o, 'ara', 'conv_%03d.npz' % int(round(step * 100)))
def p2path(o, h3): return os.path.join(o, 'ara', 'p2_h%d.json' % int(h3))


def run_task(task):
    kind = task[0]; t0 = time.time()
    if kind == 'p1':
        _, h3, seed, n, o = task
        path = p1path(o, h3, seed)
        if os.path.exists(path):
            return (kind, h3, seed, 0.0, 0)
        pr, info = sample_params(h3, seed, n)
        prd = derive(pr, h3)
        acc = engine(prd, Grid(0.5), HORIZONS, chunk=40)
        out = dict(acc)
        for k, v in prd.items():
            out['par_' + k] = v
        out.update(n_prior=info['n_prior'], n_acc=info['n_acc'], prior_stats=info['prior_stats'],
                   acc_stats=info['acc_stats'], used_stats=info['used_stats'], secs=time.time() - t0)
        np.savez(path + '.tmp.npz', **out); os.replace(path + '.tmp.npz', path)
        return (kind, h3, seed, time.time() - t0, 1)
    if kind == 'y':
        _, h3, lam, n, o = task
        path = ypath(o, h3, lam)
        if os.path.exists(path):
            return (kind, h3, lam, 0.0, 0)
        pr, _ = sample_params(h3, SEEDS[0], n)
        acc = engine(derive(pr, h3), Grid(0.5), Y_H, lam=lam, forks=False, do_b2=False, tols=(TOLS[0],), chunk=100)
        np.savez(path + '.tmp.npz', ceil=acc['ceil'], h3eq_nc=acc['h3eq_nc'], h3eq_k3=acc['h3eq_k3'],
                 secs=time.time() - t0)
        os.replace(path + '.tmp.npz', path)
        return (kind, h3, lam, time.time() - t0, 1)
    if kind == 'conv':
        _, step, nconv, n, o = task
        path = convpath(o, step)
        if os.path.exists(path):
            return (kind, step, nconv, 0.0, 0)
        pr, _ = sample_params(6.0, SEEDS[0], n)
        pr = {k: v[:nconv] for k, v in pr.items()}
        acc = engine(derive(pr, 6.0), Grid(step), HORIZONS, do_b2=False, tols=(TOLS[0],), chunk=20)
        np.savez(path + '.tmp.npz', sumreg=acc['sumreg'], Jstar=acc['Jstar'], secs=time.time() - t0)
        os.replace(path + '.tmp.npz', path)
        return (kind, step, nconv, time.time() - t0, 1)
    if kind == 'p2':
        return task_p2(task[1:])
    raise ValueError(kind)


def task_p2(args):
    h3, o, cells = args
    path = p2path(o, h3)
    if os.path.exists(path):
        return ('p2', h3, 0, 0.0, 0)
    t0 = time.time()
    R = [dict(np.load(p1path(o, h3, s))) for s in SEEDS]
    pr = {k[4:]: np.concatenate([r[k] for r in R]) for k in R[0] if k.startswith('par_')}
    Jstar = np.concatenate([r['Jstar'] for r in R])
    deltas = [-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0]
    curve = []; marg = []; cons = []
    for (hi, oi, K, pol, er) in cells:
        H = HORIZONS[hi]; hA, hB, d, n, T, psi = pol
        pols = []; dl = []
        for de in deltas:
            if 1.0 <= hA + de <= 10.0:
                pols.append((hA + de, hB, d, n, T, psi)); dl.append(de)
        j0 = dl.index(0.0)
        tm = next((t for t in range(H // 2, H - T) if t % 7 < d), None)
        extra = {}; keep = ()
        if tm is not None:
            pols.append(tuple(pol)); jm = len(pols) - 1; extra = {jm: (tm, 0.5)}; keep = (j0, jm)
        res = ref_sim(pr, pols, H, extra=extra, keep_e=keep)
        J = res['sumE'] if oi == 0 else res['P']
        Js = Jstar[:, hi, oi, K]
        feas = res['klev'] <= K
        reg = np.where(feas, np.clip(1.0 - J / Js[:, None], 0.0, None), 1.0)
        base = dict(h3=h3, ufuk=H, amac=OBJ[oi], K=KN[K])
        for j, de in enumerate(dl):
            ratio = J[:, j] / J[:, j0]
            curve.append(dict(base, delta=de, hA=hA + de, ort_pismanlik=float(reg[:, j].mean()),
                              p95_pismanlik=float(np.percentile(reg[:, j], 95)),
                              ihlal_orani=float(1.0 - feas[:, j].mean()),
                              ucurum_olasiligi=float(res['ever'][:, j].mean()),
                              J_orani_ort=float(ratio.mean()), J_orani_p05=float(np.percentile(ratio, 5))))
        cons.append([float(er), float(reg[:, j0].mean())])
        if tm is not None:
            e0 = res['es'][j0]; e1 = res['es'][jm]
            gain = e1[tm] - e0[tm]; loss = (e0[tm + 1:] - e1[tm + 1:]).sum(0)
            dP = res['P'][:, jm] - res['P'][:, j0]
            marg.append(dict(base, gun=tm, ayni_gun_kazanc=float(gain.mean()), sonraki_kayip=float(loss.mean()),
                             kayip_bolu_kazanc=float(loss.mean() / gain.mean()), net=float((gain - loss).mean()),
                             kaybin_kazanci_astigi_pay=float((loss > gain).mean()), dP_ort=float(dP.mean()),
                             dP_goreli=float((dP / res['P'][:, j0]).mean())))
    with open(path, 'w') as f:
        json.dump(dict(curve=curve, marg=marg, cons=cons, secs=time.time() - t0), f)
    return ('p2', h3, 0, time.time() - t0, 1)


# ---------------------------------------------------------------- yardimcilar
def fmt(v):
    if isinstance(v, (float, np.floating)):
        return '' if not np.isfinite(v) else ('%.6g' % v)
    if isinstance(v, (np.integer,)):
        return str(int(v))
    return v


def wcsv(path, rows):
    cols = []
    for r in rows:
        for c in r:
            if c not in cols:
                cols.append(c)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(cols)
        for r in rows:
            w.writerow([fmt(r.get(c, '')) for c in cols])


def q3(v):
    v = np.asarray(v, float)
    if v.size == 0:
        return [np.nan] * 3
    return [float(np.percentile(v, q)) for q in (25, 50, 75)]


def mode(v):
    vals, cnt = np.unique(v, return_counts=True)
    return vals[cnt.argmax()]


def rank_avg(v):
    u, inv, cnt = np.unique(v, return_inverse=True, return_counts=True)
    cs = np.cumsum(cnt)
    return (cs - (cnt - 1) / 2.0)[inv]


def prcc(X, y):
    """Kismi sira korelasyonu: her sutun icin, digerleri sabitken."""
    if np.all(y == y[0]):
        return np.full(X.shape[1], np.nan)
    Z = np.column_stack([np.apply_along_axis(rank_avg, 0, X), rank_avg(y)])
    Pm = np.linalg.pinv(np.corrcoef(Z.T))
    return -Pm[:-1, -1] / np.sqrt(np.diag(Pm)[:-1] * Pm[-1, -1])


def addq(row, name, v):
    a, b, c = q3(v)
    row[name + '_q1'] = a; row[name + '_med'] = b; row[name + '_q3'] = c


# ---------------------------------------------------------------- toplama ve CSV
def aggregate(o, procs):
    grid = Grid(0.5); P = grid.P; NP = len(OPTS) * P
    A = grid.fields()
    planH = [grid.planH(H) for H in HORIZONS]
    ana = []; duy = []; ort = []; sond = []; b2t = []; b2k = []; ysen = []; kisa = []; kisad = []; ucur = []
    marj = []; kabul = []; p2tasks = []; sinama = []
    nest_tot = np.zeros(11); mono_ok = 0; mono_n = 0; h3ret = []; bnd = dict(n=0, hi=0, lo=0, hb=0)
    for h3 in H3S:
        R = [dict(np.load(p1path(o, h3, s))) for s in SEEDS]
        N = sum(len(r['par_h0']) for r in R)
        cat = lambda k: np.concatenate([r[k] for r in R], axis=0)
        sumreg = sum(r['sumreg'] for r in R); feat = sum(r['featcnt'] for r in R)
        cliff = sum(r['cliffcnt'] for r in R); srt = sum(r['sumreg_tol'] for r in R)
        best = cat('best'); Jstar = cat('Jstar'); ceil = cat('ceil')
        h1v = cat('par_h1')
        X = np.column_stack([cat('par_' + nm) for nm in PARAM_NAMES])
        nest_tot += sum(r['nest'].sum(0) for r in R)
        mono_ok += int(np.all(np.diff(ceil, axis=2) >= -1e-9, axis=2).sum()); mono_n += ceil.shape[0] * ceil.shape[1]
        h3ret.append(cat('h3eq_nc')[:, HORIZONS.index(360)] == h3)
        for si, r in enumerate(R):
            kabul.append(dict(h3=h3, tohum=SEEDS[si], n_onsel=int(r['n_prior']), n_kabul=int(r['n_acc']),
                              kabul_orani=float(r['n_acc']) / float(r['n_prior']), n_kullanilan=len(r['par_h0'])))
            for j, nm in enumerate(PARAM_NAMES):
                ps = r['prior_stats'][j]; as_ = r['acc_stats'][j]; us = r['used_stats'][j]
                marj.append(dict(h3=h3, tohum=SEEDS[si], parametre=nm, onsel_ort=ps[0], onsel_p05=ps[1],
                                 onsel_p50=ps[2], onsel_p95=ps[3], kabul_ort=as_[0], kabul_p05=as_[1],
                                 kabul_p50=as_[2], kabul_p95=as_[3], kullanilan_ort=us[0], kullanilan_p50=us[2]))
        cells = []
        for hi, H in enumerate(HORIZONS):
            for K in range(4):
                cw = ceil[:, hi, K] / H * 7.0
                rob = {}
                for oi, obj in enumerate(OBJ):
                    sr = sumreg[hi, oi, K]; ri = int(sr.argmin()); er = sr[ri] / N
                    rs = [int(r['sumreg'][hi, oi, K].argmin()) for r in R]
                    b = best[:, hi, oi, K]
                    hAo = A['hA'][b]; hBo = A['hB'][b]; wk = planH[hi][b] / H * 7.0
                    row = dict(h3=h3, ufuk=H, amac=obj, K=KN[K], hA=A['hA'][ri], hB=A['hB'][ri], d=A['d'][ri],
                               n=A['n'][ri], T=A['T'][ri], psi=A['psi'][ri], haftalik_saat=planH[hi][ri] / H * 7.0,
                               toplam_saat=planH[hi][ri], beklenen_pismanlik=er, p95_pismanlik=np.nan,
                               ihlal_orani=1.0 - feat[hi, K][ri] / N, ucurum_olasiligi=cliff[hi][ri] / N)
                    addq(row, 'opt_hA', hAo); addq(row, 'opt_hB', hBo); addq(row, 'opt_gunluk', hAo + hBo)
                    addq(row, 'opt_haftalik', wk)
                    addq(row, 'opt_hA_eksi_h1', hAo - h1v)
                    row.update(opt_d_mod=mode(A['d'][b]), opt_n_mod=mode(A['n'][b]), opt_T_mod=mode(A['T'][b]))
                    addq(row, 'tavan_haftalik', cw)
                    row.update(sinir_hA10=float((hAo == 10).mean()), sinir_hA1=float((hAo == 1).mean()),
                               sinir_hB3=float((hBo == 3).mean()), hA_tohum1=A['hA'][rs[0]], hA_tohum2=A['hA'][rs[1]],
                               hB_tohum1=A['hB'][rs[0]], hB_tohum2=A['hB'][rs[1]],
                               haftalik_tohum1=planH[hi][rs[0]] / H * 7.0, haftalik_tohum2=planH[hi][rs[1]] / H * 7.0)
                    if oi < 2 and K < 3:
                        for ti, tl in enumerate(('001', '005')):
                            rt = int(srt[ti, hi, oi, K].argmin())
                            row['hA_tol' + tl] = A['hA'][rt]; row['hB_tol' + tl] = A['hB'][rt]
                            row['haftalik_tol' + tl] = planH[hi][rt] / H * 7.0
                    row['n_cekim'] = N
                    ana.append(row); rob[oi] = ri
                    cnt = np.bincount(A['o'][b], minlength=len(OPTS)) / float(N)
                    for oo, (T, psi) in enumerate(OPTS):
                        sond.append(dict(h3=h3, ufuk=H, amac=obj, K=KN[K], T=T, psi=psi, pay=cnt[oo],
                                         saglam=int(A['o'][ri] == oo)))
                    if oi < 2:
                        bnd['n'] += N; bnd['hi'] += int((hAo == 10).sum()); bnd['lo'] += int((hAo == 1).sum())
                        bnd['hb'] += int((hBo == 3).sum())
                        cells.append((hi, oi, K, [float(A['hA'][ri]), float(A['hB'][ri]), int(A['d'][ri]),
                                                  int(A['n'][ri]), int(A['T'][ri]), float(A['psi'][ri])], float(er)))
                        p1 = prcc(X, hAo); p2 = prcc(X, wk)
                        for j, nm in enumerate(PARAM_NAMES):
                            lo = X[:, j] <= np.median(X[:, j])
                            duy.append(dict(h3=h3, ufuk=H, amac=obj, K=KN[K], parametre=nm, prcc_hA=p1[j],
                                            prcc_haftalik=p2[j], hA_alt_yari_med=float(np.median(hAo[lo])),
                                            hA_ust_yari_med=float(np.median(hAo[~lo])),
                                            haftalik_alt_yari_med=float(np.median(wk[lo])),
                                            haftalik_ust_yari_med=float(np.median(wk[~lo]))))
                ba = best[:, hi, 0, K]; bb = best[:, hi, 1, K]; b0 = best[:, hi, 2, K]
                Jsb = Jstar[:, hi, 1, K]
                ort.append(dict(
                    h3=h3, ufuk=H, K=KN[K], ayni_politika=float((ba == bb).mean()),
                    ayni_taban=float((A['p'][ba] == A['p'][bb]).mean()),
                    hA_fark_05=float((np.abs(A['hA'][ba] - A['hA'][bb]) <= 0.5).mean()),
                    gunluk_fark_05=float((np.abs(A['hA'][ba] + A['hB'][ba] - A['hA'][bb] - A['hB'][bb]) <= 0.5).mean()),
                    haftalik_fark_med=float(np.median(planH[hi][bb] - planH[hi][ba]) / H * 7.0),
                    a_opt_b1_pismanlik=float((1.0 - cat('Jb_at_a')[:, hi, K] / Jsb).mean()),
                    b1_opt_a_pismanlik=float((1.0 - cat('Ja_at_b')[:, hi, K] / Jstar[:, hi, 0, K]).mean()),
                    e0_ayni_politika=float((b0 == bb).mean()),
                    e0_hA_fark_05=float((np.abs(A['hA'][b0] - A['hA'][bb]) <= 0.5).mean()),
                    e0_opt_b1_pismanlik=float((1.0 - cat('Jb_at_e0')[:, hi, K] / Jsb).mean()),
                    saglam_hA_a=A['hA'][rob[0]], saglam_hA_b1=A['hA'][rob[1]], saglam_hA_e0=A['hA'][rob[2]],
                    saglam_haftalik_a=planH[hi][rob[0]] / H * 7.0, saglam_haftalik_b1=planH[hi][rob[1]] / H * 7.0,
                    saglam_ayni=int(rob[0] == rob[1]), saglam_e0_ayni=int(rob[2] == rob[1])))
            # ucurum olasiligi (T=0 secenegi) ve K olurluk paylari
            for p in range(P):
                ucur.append(dict(h3=h3, ufuk=H, hA=grid.p_hA[p], hB=grid.p_hB[p], d=grid.p_d[p], n=grid.p_n[p],
                                 ucurum_olasiligi=cliff[hi][p] / N, K0_pay=feat[hi, 0][p] / N, K1_pay=feat[hi, 1][p] / N,
                                 K2_pay=feat[hi, 2][p] / N, K3_pay=feat[hi, 3][p] / N))
            # kisa ufuk
            nc = cat('h3eq_nc')[:, hi]; k3 = cat('h3eq_k3')[:, hi]
            row = dict(h3=h3, ufuk=H)
            addq(row, 'h3es_ucurumsuz', nc); addq(row, 'h3es_K3', k3)
            addq(row, 'tavanK3_haftalik', ceil[:, hi, 3] / H * 7.0)
            addq(row, 'tavanK3_oran360', (ceil[:, hi, 3] / H) / (ceil[:, -1, 3] / 360.0))
            row['sinirda_pay'] = float((nc == 10).mean()); row['ucurumsuz_eksi_h3_med'] = float(np.median(nc - h3))
            kisa.append(row)
        for nm_t, y in (('h3es_ucurumsuz_30_eksi_h3', cat('h3eq_nc')[:, 0] - h3),
                        ('h3es_K3_30_eksi_h3', cat('h3eq_k3')[:, 0] - h3),
                        ('tavanK3_30_bolu_360', (ceil[:, 0, 3] / 30.0) / (ceil[:, -1, 3] / 360.0))):
            pc = prcc(X, y)
            for j, nm in enumerate(PARAM_NAMES):
                kisad.append(dict(h3=h3, hedef=nm_t, parametre=nm, prcc=pc[j]))
        p2tasks.append(('p2', h3, o, cells))
        # b2
        b2cnt = sum(r['b2cnt'] for r in R); b2key = cat('b2key'); b2D = cat('b2D'); b2pol = cat('b2pol')
        for hi, H in enumerate(HORIZONS):
            Dd = [delay_days(H, k) for k in range(4)]
            for gi, gap in enumerate(GAPS):
                kar = dict(h3=h3, ufuk=H, acik=gap, karar_K='yok')
                firstK = np.full(N, 4)
                for K in range(3, -1, -1):
                    firstK[np.isfinite(b2key[:, hi, gi, K])] = K
                for K in range(4):
                    kar['pay_' + KN[K]] = float((firstK == K).mean())
                kar['pay_yok'] = float((firstK == 4).mean())
                selk = np.where(firstK < 4, firstK, 0)
                kk = b2key[np.arange(N), hi, gi, selk]; okd = firstK < 4
                addq(kar, 'cekim_saat', kk[okd])
                pol = b2pol[np.arange(N), hi, gi, selk][okd]
                addq(kar, 'cekim_gunluk', A['hA'][pol] + A['hB'][pol])
                done = False
                for K in range(4):
                    fin = np.isfinite(b2key[:, hi, gi, K])
                    row = dict(h3=h3, ufuk=H, acik=gap, K=KN[K], olurluk_orani=float(fin.mean()))
                    addq(row, 'saat', b2key[fin, hi, gi, K])
                    pol = b2pol[fin, hi, gi, K]
                    addq(row, 'gunluk', A['hA'][pol] + A['hB'][pol])
                    row['hA_med'] = float(np.median(A['hA'][pol])) if fin.any() else np.nan
                    row['gecikme_mod'] = Dd[int(mode(b2D[fin, hi, gi, K]))] if fin.any() else np.nan
                    share = b2cnt[K, gi, hi] / float(N)          # [4, NP]
                    hrs = np.stack([grid.planH(H - Dd[k]) for k in range(4)])
                    cand = np.where(share >= 0.9, hrs + 1e-6 * (A['hA'] + A['hB'])[None, :], np.inf)
                    cand[np.isnan(cand)] = np.inf
                    if np.isfinite(cand).any():
                        k, ix = np.unravel_index(int(cand.argmin()), cand.shape)
                        sg = dict(saglam_gecikme=Dd[k], saglam_hA=A['hA'][ix], saglam_hB=A['hB'][ix],
                                  saglam_d=A['d'][ix], saglam_n=A['n'][ix], saglam_T=A['T'][ix],
                                  saglam_psi=A['psi'][ix], saglam_toplam_saat=hrs[k, ix],
                                  saglam_gunluk=A['hA'][ix] + A['hB'][ix],
                                  saglam_haftalik=hrs[k, ix] / max(1, H - Dd[k]) * 7.0, saglam_olurluk=share[k, ix])
                        row.update(sg)
                        if not done:
                            kar['karar_K'] = KN[K]; kar.update(sg); done = True
                    b2t.append(row)
                b2k.append(kar)
        # Y senaryosu
        for lam in LAMBDAS:
            y = np.load(ypath(o, h3, lam))
            for hi, H in enumerate(Y_H):
                row = dict(h3=h3, **{'lambda': lam}, ufuk=H)
                addq(row, 'tavanK3_haftalik', y['ceil'][:, hi, 3] / H * 7.0)
                addq(row, 'h3es_ucurumsuz', y['h3eq_nc'][:, hi]); addq(row, 'h3es_K3', y['h3eq_k3'][:, hi])
                row['h3_cokus_payi'] = float((y['h3eq_nc'][:, hi] < h3).mean())
                row['n_cekim'] = len(y['ceil'])
                ysen.append(row)
    # ikinci gecis: pismanlik egrisi ve marjinal sinama (referans benzetici)
    t0 = time.time()
    with Pool(procs) as pool:
        res = list(pool.imap_unordered(run_task, p2tasks))
    ncomp = sum(r[4] for r in res)
    with open(os.path.join(o, 'ara', 'duvar.log'), 'a') as f:
        f.write('ikinci_gecis;%.1f;%d\n' % (time.time() - t0, ncomp))
    curve = []; marg = []; cons = []
    for h3 in H3S:
        with open(p2path(o, h3)) as f:
            d = json.load(f)
        curve += d['curve']; marg += d['marg']; cons += d['cons']
    p95 = {(c['h3'], c['ufuk'], c['amac'], c['K']): c['p95_pismanlik'] for c in curve if c['delta'] == 0}
    for r in ana:
        r['p95_pismanlik'] = p95.get((r['h3'], r['ufuk'], r['amac'], r['K']), np.nan)
    # ozetler
    poz = []
    for h3 in H3S:
        for obj in OBJ[:2]:
            for K in KN:
                for de in sorted(set(c['delta'] for c in curve)):
                    cc = [c for c in curve if c['h3'] == h3 and c['amac'] == obj and c['K'] == K and c['delta'] == de]
                    if cc:
                        row = dict(h3=h3, amac=obj, K=K, delta=de, n_ufuk=len(cc))
                        for kf in ('ort_pismanlik', 'p95_pismanlik', 'ihlal_orani', 'ucurum_olasiligi', 'J_orani_ort',
                                   'J_orani_p05'):
                            row[kf] = float(np.mean([c[kf] for c in cc]))
                        poz.append(row)
    doz = []
    for obj in OBJ[:2]:
        tmp = []
        for nm in PARAM_NAMES:
            rr = [r for r in duy if r['amac'] == obj and r['parametre'] == nm]
            v1 = np.array([r['prcc_hA'] for r in rr], float); v2 = np.array([r['prcc_haftalik'] for r in rr], float)
            dh = np.array([r['hA_ust_yari_med'] - r['hA_alt_yari_med'] for r in rr], float)
            tmp.append(dict(amac=obj, parametre=nm, ort_mutlak_prcc_hA=float(np.nanmean(np.abs(v1))),
                            ort_prcc_hA=float(np.nanmean(v1)), ort_mutlak_prcc_haftalik=float(np.nanmean(np.abs(v2))),
                            ort_prcc_haftalik=float(np.nanmean(v2)), ort_hA_ust_eksi_alt=float(np.nanmean(dh)),
                            n_hucre=len(rr)))
        tmp.sort(key=lambda r: -r['ort_mutlak_prcc_hA'])
        for i, r in enumerate(tmp):
            r['sira'] = i + 1
        doz += tmp
    soz = []
    for obj in OBJ[:2]:
        for H in HORIZONS:
            for (T, psi) in OPTS:
                rr = [r for r in sond if r['amac'] == obj and r['ufuk'] == H and r['K'] == 'K3' and r['T'] == T
                      and r['psi'] == psi]
                soz.append(dict(amac=obj, ufuk=H, K='K3', T=T, psi=psi, pay_ort=float(np.mean([r['pay'] for r in rr])),
                                saglam_hucre=int(sum(r['saglam'] for r in rr)), n_h3=len(rr)))
    # yakinsama (0,25 izgara)
    c5 = np.load(convpath(o, 0.5)); c25 = np.load(convpath(o, 0.25)); g25 = Grid(0.25)
    yak = []
    for hi, H in enumerate(HORIZONS):
        for oi in range(2):
            for K in range(4):
                i5 = int(c5['sumreg'][hi, oi, K].argmin()); i25 = int(c25['sumreg'][hi, oi, K].argmin())
                yak.append(dict(h3=6.0, ufuk=H, amac=OBJ[oi], K=KN[K], hA_05=grid.p_hA[i5 % P],
                                hA_025=g25.p_hA[i25 % g25.P], hB_05=grid.p_hB[i5 % P], hB_025=g25.p_hB[i25 % g25.P],
                                Jyildiz_kazanc=float((c25['Jstar'][:, hi, oi, K] / c5['Jstar'][:, hi, oi, K]).mean() - 1.0),
                                n_cekim=len(c5['Jstar'])))
    # sinamalar (kosu duzeyi)
    def S(name, ok, val, thr, note):
        sinama.append(dict(sinama=name, sonuc='gecti' if ok else 'kaldi', sayi=val, esik=thr, aciklama=note))
    S('K_tavan_sirasi', mono_ok == mono_n, mono_ok / float(mono_n), '=1',
      'tavan(K0)<=tavan(K1)<=tavan(K2)<=tavan(K3) saglayan (cekim,ufuk) payi; ic ice birlesim kumeleriyle')
    n0, n1, n2, n3, v01, v01a, v12, v12a, v13, v23, v03 = nest_tot
    S('K_literal_K0_K1', v01 == 0, v01 / max(n0, 1), '=0', 'yazildigi gibi K0 uyesi olup K1 (d<=6 sarti) disinda kalan pay')
    S('K_literal_K0_K1_uygulanabilir', v01a == 0, v01a / max(n0, 1), '=0', 'ayni, yalniz dinlenme gunu olan politikalarda')
    S('K_literal_K1_K2', v12 == 0, v12 / max(n1, 1), '=0', 'yazildigi gibi K1 uyesi olup K2 (n sonlu sarti) disinda kalan pay')
    S('K_literal_K1_K2_uygulanabilir', v12a == 0, v12a / max(n1, 1), '=0', 'ayni, yalniz hafif haftasi tamamlanmis politikalarda')
    S('K_literal_K1_K3', v13 == 0, v13 / max(n1, 1), '=0', 'K1 uyesi olup K3 disinda kalan pay')
    S('K_literal_K2_K3', v23 == 0, v23 / max(n2, 1), '=0', 'K2 uyesi olup K3 disinda kalan pay')
    S('K_literal_K0_K3', v03 == 0, v03 / max(n0, 1), '=0', 'K0 uyesi olup K3 disinda kalan pay')
    m = [r for r in ana if r['amac'] in ('a', 'b1')]
    ag = float(np.mean([abs(r['hA_tohum1'] - r['hA_tohum2']) <= 0.5 for r in m]))
    S('iki_tohum_uyumu_hA', ag >= 0.9, ag, '>=0.9', 'ana tabloda (a, b1) iki tohumun saglam hA farki <= 0,5 olan hucre payi')
    agw = float(np.mean([abs(r['haftalik_tohum1'] - r['haftalik_tohum2']) <= 3.0 for r in m]))
    S('iki_tohum_uyumu_haftalik', agw >= 0.9, agw, '>=0.9', 'iki tohumun saglam haftalik saat farki <= 3 olan hucre payi')
    S('izgara_ust_sinir_hA10', bnd['hi'] / bnd['n'] < 0.05, bnd['hi'] / bnd['n'], '<0.05', 'cekim basina optimumun hA=10 sinirina yapisma payi (a, b1, tum hucreler)')
    S('izgara_alt_sinir_hA1', bnd['lo'] / bnd['n'] < 0.05, bnd['lo'] / bnd['n'], '<0.05', 'cekim basina optimumun hA=1 sinirina yapisma payi')
    S('izgara_ust_sinir_hB3', bnd['hb'] / bnd['n'] < 0.05, bnd['hb'] / bnd['n'], '<0.05', 'cekim basina optimumun hB=3 sinirina yapisma payi')
    yk = float(np.mean([abs(r['hA_05'] - r['hA_025']) <= 0.25 for r in yak]))
    S('izgara_025_yakinsama_hA', yk >= 0.9, yk, '>=0.9', 'h3=6: 0,25 izgarada saglam hA farki <= 0,25 olan hucre payi')
    gk = float(np.max([r['Jyildiz_kazanc'] for r in yak]))
    S('izgara_025_Jyildiz_kazanc_ort', True, float(np.mean([r['Jyildiz_kazanc'] for r in yak])), 'bilgi', '0,25 izgaranin en iyi J degerine hucre ortalamasi katkisi (bilgi satiri)')
    S('izgara_025_Jyildiz_kazanc', gk < 0.005, gk, '<0.005', '0,25 izgaranin cekim basina en iyi J degerine en buyuk ortalama katkisi')
    cd = float(np.max(np.abs(np.array(cons)[:, 0] - np.array(cons)[:, 1])))
    S('motor_referans_tutarliligi', cd < 2e-3, cd, '<0.002', 'saglam politikanin beklenen pismanligi: hizli motor ile referans benzetici farki (en buyuk)')
    hr = float(np.concatenate(h3ret).mean())
    S('h3_girdi_cikti', hr == 1.0, hr, '=1', 'lambda=0, 360 gun: 6 gun/hafta ucurumsuz en yuksek hA = h3 olan cekim payi (dongusellik denetimi)')
    mk = min(k['n_kullanilan'] for k in kabul)
    S('kabul_sayisi', mk >= 1000, mk, '>=1000', 'senaryo ve tohum basina kullanilan kabul edilmis cekim (en az)')
    # sure
    sure = []
    lp = os.path.join(o, 'ara', 'duvar.log')
    if os.path.exists(lp):
        tot = 0.0
        for ln in open(lp):
            nm, sec, nc = ln.strip().split(';')
            if int(nc) > 0:
                sure.append(dict(asama=nm, duvar_s=float(sec), hesaplanan_gorev=int(nc))); tot += float(sec)
        sure.append(dict(asama='toplam', duvar_s=tot, hesaplanan_gorev=sum(s['hesaplanan_gorev'] for s in sure)))
    for nm, rows in (('ana_tablo', ana), ('pismanlik_egrisi', curve), ('pismanlik_ozet', poz), ('duyarlilik', duy),
                     ('duyarlilik_ozet', doz), ('marjinaller', marj), ('kabul_orani', kabul), ('ortusme', ort),
                     ('son_donem', sond), ('son_donem_ozet', soz), ('b2_acik_tablosu', b2t), ('b2_karar', b2k),
                     ('y_senaryosu', ysen), ('kisa_ufuk', kisa), ('kisa_ufuk_duyarlilik', kisad),
                     ('ucurum_olasiligi', ucur), ('marjinal_sinama', marg), ('yakinsama', yak), ('sinamalar', sinama),
                     ('sure', sure)):
        wcsv(os.path.join(o, nm + '.csv'), rows)


# ---------------------------------------------------------------- ana akis
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', nargs='?', default='hepsi', choices=['hepsi', 'rapor', 'topla'])
    ap.add_argument('--n', type=int, default=1000)
    ap.add_argument('--nconv', type=int, default=250)
    ap.add_argument('--cikti', default=os.path.join(HERE, 'cikti'))
    ap.add_argument('--procs', type=int, default=4)
    ap.add_argument('--temiz', action='store_true')
    ap.add_argument('--hizli', action='store_true')
    a = ap.parse_args()
    o = a.cikti
    if a.hizli:
        a.n = 40; a.nconv = 20
    if a.cmd == 'rapor':
        rapor(o); return
    if a.temiz and os.path.isdir(os.path.join(o, 'ara')):
        shutil.rmtree(os.path.join(o, 'ara'))
    os.makedirs(os.path.join(o, 'ara'), exist_ok=True)
    if a.cmd == 'hepsi':
        tasks = [('p1', h3, s, a.n, o) for s in SEEDS for h3 in H3S]
        tasks += [('conv', st, min(a.nconv, a.n), a.n, o) for st in (0.25, 0.5)]
        tasks += [('y', h3, lam, a.n, o) for h3 in H3S for lam in LAMBDAS]
        t0 = time.time(); nc = 0
        with Pool(a.procs) as pool:
            for r in pool.imap_unordered(run_task, tasks, chunksize=1):
                nc += r[4]
                print('gorev %s %s %s: %.0f s%s' % (r[0], r[1], r[2], r[3], '' if r[4] else ' (kayitli)'), flush=True)
        with open(os.path.join(o, 'ara', 'duvar.log'), 'a') as f:
            f.write('birinci_gecis;%.1f;%d\n' % (time.time() - t0, nc))
        print('birinci gecis: %.0f s' % (time.time() - t0), flush=True)
    t0 = time.time()
    aggregate(o, a.procs)
    print('toplama + ikinci gecis: %.0f s' % (time.time() - t0), flush=True)
    rapor(o)


# ---------------------------------------------------------------- rapor (SONUC.md; her sayi CSV'den)
def rcsv(path):
    with open(path, encoding='utf-8') as f:
        return list(csv.DictReader(f))


def F(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return float('nan')


def tr(x, nd=1):
    x = F(x)
    return '–' if not np.isfinite(x) else ('%.*f' % (nd, x)).replace('.', ',')


def h05(x):
    x = F(x)
    return '–' if not np.isfinite(x) else tr(math.floor(x * 2 + 0.5) / 2.0, 1)


def pc(x, nd=0):
    x = F(x)
    return '–' if not np.isfinite(x) else tr(100.0 * x, nd)


def rapor(o):
    R = lambda n: rcsv(os.path.join(o, n + '.csv'))
    ana = {(F(r['h3']), int(r['ufuk']), r['amac'], r['K']): r for r in R('ana_tablo')}
    poz = {(F(r['h3']), r['amac'], r['K'], F(r['delta'])): r for r in R('pismanlik_ozet')}
    ks = {(F(r['h3']), int(r['ufuk'])): r for r in R('kisa_ufuk')}
    kd = R('kisa_ufuk_duyarlilik')
    so = {(r['amac'], int(r['ufuk']), int(F(r['T'])), F(r['psi'])): r for r in R('son_donem_ozet')}
    ot = {(F(r['h3']), int(r['ufuk']), r['K']): r for r in R('ortusme')}
    bk = {(F(r['h3']), int(r['ufuk']), F(r['acik'])): r for r in R('b2_karar')}
    doz = R('duyarlilik_ozet'); ys = R('y_senaryosu'); sn = R('sinamalar'); yak = R('yakinsama')
    sure = R('sure'); ms = {(F(r['h3']), int(r['ufuk']), r['amac'], r['K']): r for r in R('marjinal_sinama')}
    kab = R('kabul_orani')
    L = []; W = L.append
    A = lambda h3, H, obj, K: ana[(float(h3), H, obj, K)]
    nlab = lambda n: 'yok' if int(F(n)) == 0 else '%d hf' % int(F(n))
    sd = lambda T, psi: 'yok' if int(F(T)) == 0 else '%d g × %s' % (int(F(T)), tr(psi, 2))
    pol = lambda r, p='': '%s + %s' % (h05(r[p + 'hA']), h05(r[p + 'hB']))
    rng3 = lambda r, k, f=h05: '%s [%s–%s]' % (f(r[k + '_med']), f(r[k + '_q1']), f(r[k + '_q3']))
    ncek = int(F(A(6, 180, 'a', 'K3')['n_cekim']))
    W('# Model sonuçları (v2): net odaklı çalışma saati')
    W('')
    W('Her sayı `cikti/` altındaki CSV dosyalarından `python3 sim.py rapor` ile yazıldı (saatler 0,5 hassasiyetle). Model '
      'ölçüm değil hesap aracıdır; "optimum" yalnız bu varsayımlar altında geçerlidir. Senaryo başına %d kabul edilmiş '
      'çekim, iki tohum.' % ncek)
    W('')
    # ---- 1
    W('## 1. Ana sonuç')
    W('')
    rr = [A(h3, 180, 'a', 'K3') for h3 in H3S]
    slope = (F(rr[-1]['hA']) - F(rr[0]['hA'])) / (H3S[-1] - H3S[0])
    P6 = lambda d, k, obj='a', h3=6.0: F(poz[(h3, obj, 'K3', d)][k])
    uq = lambda v: v[0] if len(set(v)) == 1 else ' / '.join(v)
    r6 = rr[1]
    top = [r['parametre'] for r in doz if r['amac'] == 'a'][:3]
    W('Bu varsayımlar altında sağlam politika girdideki tavanla birlikte kayar: 180 gün, K3, (a) amacında h3 = %s için '
      'günde %s saat yüksek talepli çalışma (hB = %s; haftada %s gün; haftalık %s saat); h3\'teki her 1 saat sağlam '
      'hA\'yı ortalama %s saat oynatır, yani sayı bulgu değil, girdinin geri gelişidir. Modelin katkısı biçimdir: sağlam '
      'politikadan günde 1 saat aşağı inmek çıktıyı h3 = 6\'da %%%s, h3 = 7\'de %%%s düşürür; 1 saat yukarı çıkınca '
      'uçurum olasılığı %%%s ve %%%s, çıktı kaybı %%%s ve %%%s olur (+2 saatte %%%s ve %%%s). Çekim başına optimum K3 '
      'tavanında değil, kronik birikimin başladığı h1 eşiğinin çevresindedir (h3 = 6, 180 gün: optimum hA − h1 ortancası '
      '%s saat [%s; %s]); sonucu en çok %s oynatır; 30 günlük ufuk K3 tavanını yalnız ×%s yükseltir.'
      % (' / '.join(tr(h, 0) for h in H3S), ' / '.join(h05(r['hA']) for r in rr), uq([h05(r['hB']) for r in rr]),
         uq([r['d'] for r in rr]), ' / '.join(h05(r['haftalik_saat']) for r in rr), tr(slope, 2),
         pc(1 - P6(-1.0, 'J_orani_ort')), pc(1 - P6(-1.0, 'J_orani_ort', h3=7.0)),
         pc(P6(1.0, 'ucurum_olasiligi')), pc(P6(1.0, 'ucurum_olasiligi', h3=7.0)),
         pc(1 - P6(1.0, 'J_orani_ort')), pc(1 - P6(1.0, 'J_orani_ort', h3=7.0)),
         pc(1 - P6(2.0, 'J_orani_ort')), pc(1 - P6(2.0, 'J_orani_ort', h3=7.0)),
         tr(r6['opt_hA_eksi_h1_med'], 2), tr(r6['opt_hA_eksi_h1_q1'], 2), tr(r6['opt_hA_eksi_h1_q3'], 2),
         ', '.join(top), tr(ks[(6.0, 30)]['tavanK3_oran360_med'], 2)))
    W('')
    # ---- 2
    W('## 2. Ana tablo (h3 = 6 ve h3 = 7)')
    W('')
    cel = [r for k, r in ana.items() if k[2] in ('a', 'b1')]
    W('Sağlam politika = beklenen pişmanlığı en küçük politika (kısıtı çiğnediği çekimde pişmanlık 1). Aralık = varsayım '
      'aralığı: çekim başına optimum hA ortancası [Q1–Q3]. Son dönem: gün × ψ. Sağlam politikada hB > 0 olan hücre %d, '
      'haftada 7 günden az çalışılan hücre %d (toplam %d): model dinlenme gününe yalnız yorgunluk sönümüyle değer verir; '
      'bu bulgu değil, model sınırıdır.'
      % (sum(F(r['hB']) > 0 for r in cel), sum(int(F(r['d'])) < 7 for r in cel), len(cel)))
    for h3 in (6.0, 7.0):
        W('')
        W('**Tablo 2 — h3 = %s (kaynak: cikti/ana_tablo.csv)**' % tr(h3, 0))
        W('')
        W('| Ufuk | K | (a) hA + hB | gün | hafif | son dönem | hft. saat | aralık (hA) | (b1) hA + hB | gün | hafif | son dönem | hft. saat | aralık (hA) |')
        W('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
        for H in HORIZONS:
            for K in KN:
                cs = []
                for obj in ('a', 'b1'):
                    r = A(h3, H, obj, K)
                    cs.append('%s | %s | %s | %s | %s | %s' % (pol(r), r['d'], nlab(r['n']), sd(r['T'], r['psi']),
                                                              h05(r['haftalik_saat']), rng3(r, 'opt_hA')))
                W('| %d | %s | %s | %s |' % (H, K, cs[0], cs[1]))
    W('')
    # ---- 3
    W('## 3. Pişmanlık eğrisinin asimetrisi')
    W('')
    m3 = ms.get((6.0, 180, 'a', 'K3')); m0 = ms.get((6.0, 180, 'a', 'K0'))
    W('Sağlam hA δ saat kaydırıldı (ufuk ortalaması). Kısıtı çiğneyen çekimde pişmanlık tanım gereği 1\'dir; kısıttan '
      'bağımsız ölçü çıktı oranıdır (J(δ)/J(0)). Marjinal sınama (h3 = 6, 180 gün, (a)): tek güne +0,5 saat K3 '
      'politikasında aynı gün %s etkili saat kazandırır, sonraki günlerde %s kaybettirir; K0 politikasında kayıp/kazanç '
      '%s (marjinal_sinama.csv).'
      % (tr(m3['ayni_gun_kazanc'], 2), tr(m3['sonraki_kayip'], 2), tr(m0['kayip_bolu_kazanc'], 2)))
    W('')
    W('**Tablo 3 — K3, ufuk ortalaması (kaynak: cikti/pismanlik_ozet.csv)**')
    W('')
    dl = [-2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0]
    W('| h3 | amaç | ölçü | −2 | −1 | −0,5 | 0 | +0,5 | +1 | +2 |')
    W('|---|---|---|---|---|---|---|---|---|---|')
    for h3 in (6.0, 7.0):
        for obj in ('a', 'b1'):
            for lab, key, fn in (('ort. pişmanlık %', 'ort_pismanlik', pc), ('%95 pişmanlık %', 'p95_pismanlik', pc),
                                 ('kısıt ihlali %', 'ihlal_orani', pc), ('uçurum %', 'ucurum_olasiligi', pc),
                                 ('çıktı oranı', 'J_orani_ort', lambda x: tr(x, 2))):
                vals = [fn(poz[(h3, obj, 'K3', d)][key]) if (h3, obj, 'K3', d) in poz else '–' for d in dl]
                W('| %s | %s | %s | %s |' % (tr(h3, 0), obj, lab, ' | '.join(vals)))
    W('')
    # ---- 4
    W('## 4. Kısa ufukta tavanın üstüne çıkma')
    W('')

    def topk(h3, hedef, n=3):
        rr = sorted([r for r in kd if F(r['h3']) == h3 and r['hedef'] == hedef and np.isfinite(F(r['prcc']))],
                    key=lambda r: -abs(F(r['prcc'])))[:n]
        return ', '.join('%s (%s)' % (r['parametre'], tr(r['prcc'], 2)) for r in rr)
    W('Temel modelde (λ = 0) kısa ufuk tavanı az yükseltir: h3 = 6\'da 30 günlük K3 tavanı 360 günlüğün ortanca ×%s '
      '[%s–%s] katı, 90 günde ×%s. Oranı en çok oynatanlar (PRCC, h3 = 6): %s.'
      % (tr(ks[(6.0, 30)]['tavanK3_oran360_med'], 2), tr(ks[(6.0, 30)]['tavanK3_oran360_q1'], 2),
         tr(ks[(6.0, 30)]['tavanK3_oran360_q3'], 2), tr(ks[(6.0, 90)]['tavanK3_oran360_med'], 2),
         topk(6.0, 'tavanK3_30_bolu_360')))
    W('')
    W('**Tablo 4 (kaynak: cikti/kisa_ufuk.csv, kisa_ufuk_duyarlilik.csv)**')
    W('')
    W('| h3 | ufuk | uçurumsuz en yüksek hA (6 gün/hf) | K3 için en yüksek hA (6 gün/hf) | K3 tavanı (hft. saat) | tavan / 360 günlük tavan |')
    W('|---|---|---|---|---|---|')
    for h3 in H3S:
        for H in (30, 90, 360):
            r = ks[(h3, H)]
            W('| %s | %d | %s | %s | %s | %s |' % (tr(h3, 0), H, rng3(r, 'h3es_ucurumsuz'), rng3(r, 'h3es_K3'),
                                                 rng3(r, 'tavanK3_haftalik'),
                                                 rng3(r, 'tavanK3_oran360', lambda x: tr(x, 2))))
    W('')
    # ---- 5
    W('## 5. Son dönem (T, ψ) seçimleri')
    W('')
    cnt = {}
    for obj in ('a', 'b1'):
        rr = [r for k, r in ana.items() if k[2] == obj]
        cnt[obj] = (len(rr), sum(int(F(r['T'])) == 0 for r in rr),
                    sum(int(F(r['T'])) > 0 and F(r['psi']) > 1 for r in rr),
                    sum(int(F(r['T'])) > 0 and F(r['psi']) < 1 for r in rr))
    W('Sağlam politikalarda (%d hücre/amaç): (a) son dönem yok %d, hızlanma %d, azaltma %d; (b1) yok %d, hızlanma %d, '
      'azaltma %d. (a) yalnız saati saydığı için sonda hızlanır; (b1) sınav günü yorgunluk cezası yüzünden kısa, hafif '
      'azaltmayı seçer. Tablo: çekim başına optimumların payı (K3, dört h3 ortalaması).'
      % (cnt['a'][0], cnt['a'][1], cnt['a'][2], cnt['a'][3], cnt['b1'][1], cnt['b1'][2], cnt['b1'][3]))
    W('')
    W('**Tablo 5 — son dönem payı, % (kaynak: cikti/son_donem_ozet.csv, ana_tablo.csv)**')
    W('')
    cols = [('a', 30), ('a', 180), ('a', 360), ('b1', 30), ('b1', 180), ('b1', 360)]
    W('| son dönem | ' + ' | '.join('(%s) %d gün' % c for c in cols) + ' |')
    W('|---|' + '---|' * len(cols))
    for (T, psi) in OPTS:
        W('| %s | ' % sd(T, psi) + ' | '.join(pc(so[(c[0], c[1], T, psi)]['pay_ort']) for c in cols) + ' |')
    W('')
    # ---- 6
    W('## 6. (a) ile (b1) örtüşmesi')
    W('')
    o6 = ot[(6.0, 180, 'K3')]
    W('Çekim başına en iyi politikalar birebir nadiren aynıdır (son dönem ayrışır), günlük saatte yakındır: h3 = 6, K3, '
      '180 günde hA farkı ≤ 0,5 olan çekim %%%s; (a)\'nın en iyisi (b1) ölçüsünde ortalama %%%s kaybeder. e1 = e2 = 0 '
      'referansının (b1) pişmanlığı %%%s: fark büyük ölçüde sınav günü cezasındandır.'
      % (pc(o6['hA_fark_05']), pc(o6['a_opt_b1_pismanlik'], 1), pc(o6['e0_opt_b1_pismanlik'], 1)))
    W('')
    W('**Tablo 6 — K3 (kaynak: cikti/ortusme.csv)**')
    W('')
    W('| h3 | ufuk | aynı politika % | aynı taban (hA, hB, gün, hafif) % | hA farkı ≤ 0,5 % | (a) en iyisinin (b1) pişmanlığı % | e=0 ile aynı politika % | e=0 en iyisinin (b1) pişmanlığı % | sağlam hA: a / b1 / e=0 |')
    W('|---|---|---|---|---|---|---|---|---|')
    for h3 in (6.0, 7.0):
        for H in HORIZONS:
            r = ot[(h3, H, 'K3')]
            W('| %s | %d | %s | %s | %s | %s | %s | %s | %s / %s / %s |'
              % (tr(h3, 0), H, pc(r['ayni_politika']), pc(r['ayni_taban']), pc(r['hA_fark_05']),
                 pc(r['a_opt_b1_pismanlik'], 1), pc(r['e0_ayni_politika']), pc(r['e0_opt_b1_pismanlik'], 1),
                 h05(r['saglam_hA_a']), h05(r['saglam_hA_b1']), h05(r['saglam_hA_e0'])))
    W('')
    # ---- 7
    W('## 7. (b2) Virtual OSCE: açık tablosu ve karar kuralı')
    W('')
    W('Karar kuralı: Pr(geçme) ≥ 0,95 koşulunu çekimlerin en az %90\'ında sağlayan politikalar içinde önce en düşük K, '
      'sonra en az toplam net saat (eşitlikte en düşük tepe f2); gecikme D birlikte seçilir. "Çekim başına" sütunları '
      'kuralın her çekime ayrı uygulanmasıdır. Saatler S kabulüne ve κN\'ye doğrudan bağlıdır.')
    W('')
    W('**Tablo 7 — h3 = 6 (kaynak: cikti/b2_karar.csv)**')
    W('')
    W('| açık (Pgeç − g0) | ufuk | karar K | gecikme (gün) | hA + hB | gün | toplam net saat | hft. saat | olurluk % | çekim başına toplam saat | çekim başına günlük saat | hiçbir politika yetmez % |')
    W('|---|---|---|---|---|---|---|---|---|---|---|---|')
    for gap in GAPS:
        for H in HORIZONS:
            r = bk[(6.0, H, gap)]
            W('| %s | %d | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |'
              % (tr(gap, 2), H, r['karar_K'], tr(r['saglam_gecikme'], 0), pol(r, 'saglam_'), tr(r['saglam_d'], 0),
                 tr(r['saglam_toplam_saat'], 0), h05(r['saglam_haftalik']), pc(r['saglam_olurluk']),
                 rng3(r, 'cekim_saat', lambda x: tr(x, 0)), rng3(r, 'cekim_gunluk'), pc(r['pay_yok'])))
    W('')
    # ---- 8
    W('## 8. Duyarlılık: ilk 5 parametre')
    W('')
    tolr = [r for k, r in ana.items() if k[2] in ('a', 'b1') and k[3] != 'K3']
    d1 = float(np.mean([abs(F(r['hA_tol001']) - F(r['hA'])) for r in tolr]))
    d5 = float(np.mean([abs(F(r['hA_tol005']) - F(r['hA'])) for r in tolr]))
    W('Hedef: çekim başına optimum hA; PRCC (kısmi sıra korelasyonu) bütün hücrelerin ortalaması; "üst − alt" '
      'parametrenin üst ve alt yarısındaki optimum hA ortancalarının farkı. h3 senaryo eksenidir ve hepsinden baskındır. '
      'tol 0,01 ile sağlam hA (K0–K2) ortalama %s, tol 0,05 ile %s saat değişir.' % (tr(d1, 2), tr(d5, 2)))
    W('')
    W('**Tablo 8 (kaynak: cikti/duyarlilik_ozet.csv, ana_tablo.csv)**')
    W('')
    W('| amaç | sıra | parametre | ort. mutlak PRCC (hA) | ort. PRCC (hA) | ort. mutlak PRCC (hft. saat) | üst − alt yarı (hA, saat) |')
    W('|---|---|---|---|---|---|---|')
    for obj in ('a', 'b1'):
        for r in [r for r in doz if r['amac'] == obj][:5]:
            W('| %s | %s | %s | %s | %s | %s | %s |' % (obj, r['sira'], r['parametre'], tr(r['ort_mutlak_prcc_hA'], 2),
                                                    tr(r['ort_prcc_hA'], 2), tr(r['ort_mutlak_prcc_haftalik'], 2),
                                                    tr(r['ort_hA_ust_eksi_alt'], 2)))
    W('')
    # ---- 9
    W('## 9. Y senaryosu (yavaş birikim)')
    W('')
    yd = {(F(r['h3']), F(r['lambda']), int(r['ufuk'])): r for r in ys}
    W('λ > 0\'da h3 düzeni tanım gereği çöker; bilgi veren, tavanın ne kadar indiğidir: h3 = 6\'da altı günlük düzende '
      'uçurumsuz en yüksek hA %s saatten λ = 0,02 ile 90 günde %s, 360 günde %s saate; λ = 0,05 ile %s ve %s saate iner. '
      'Uzun ufuktaki temkin bu senaryodan gelir.'
      % (h05(yd[(6.0, 0.0, 360)]['h3es_ucurumsuz_med']), h05(yd[(6.0, 0.02, 90)]['h3es_ucurumsuz_med']),
         h05(yd[(6.0, 0.02, 360)]['h3es_ucurumsuz_med']), h05(yd[(6.0, 0.05, 90)]['h3es_ucurumsuz_med']),
         h05(yd[(6.0, 0.05, 360)]['h3es_ucurumsuz_med'])))
    W('')
    W('**Tablo 9 — %d çekim, tohum 1, son dönemsiz politikalar (kaynak: cikti/y_senaryosu.csv)**' % int(F(ys[0]['n_cekim'])))
    W('')
    W('| h3 | λ | ufuk | K3 tavanı (hft. saat) | uçurumsuz en yüksek hA (6 gün/hf) | K3 için en yüksek hA (6 gün/hf) | h3 düzeninin çöktüğü çekim % |')
    W('|---|---|---|---|---|---|---|')
    for r in ys:
        W('| %s | %s | %s | %s | %s | %s | %s |' % (tr(r['h3'], 0), tr(r['lambda'], 2), r['ufuk'], rng3(r, 'tavanK3_haftalik'),
                                                rng3(r, 'h3es_ucurumsuz'), rng3(r, 'h3es_K3'), pc(r['h3_cokus_payi'])))
    W('')
    # ---- 10
    W('## 10. Yorum kararları, sınamalar, azaltılanlar')
    W('')
    for t in (
        'S önseli tanımda yok: log-tekdüze 30–1000 etkili saat; DUS için g0 = 0,3.',
        '(b2): g0 = Pgeç − açık, S_N = κN·S; gecikmede g unutmayla düşer; pişmanlık tanımsız olduğundan %90 olurluk kuralı.',
        'Takvim ilk çalışma gününe bağlı; son dönemde ψ hafif haftanın yerine geçer, haftalık dinlenme sürer.',
        'Çöküşte hA ve hB birlikte yarılanır; sınav sabahı çöküşe ek ceza yok (tanımda yok).',
        'K kümeleri yazıldığı gibi iç içe değil: d = 7 ya da hafif haftasız politika K0\'da olup K1/K2 koşuluna giremiyor; K1 ve K2 son kontrol sabahından sonra çöküşe ya da 0,8·Fcrit aşımına izin veriyor. Tanım düzeltilmedi; uygulanan yorum: K3 yazıldığı gibi, K2 = (K0 ∪ K1 ∪ K2 koşulu) ∩ K3, K1 = (K0 ∪ K1 koşulu) ∩ K3.',
        'Kısıtı çiğneyen çekimde pişmanlık 1; tavan = kısıtı sağlayan en yüksek toplam net saat.',
    ):
        W('- ' + t)
    W('')
    sv = {r['sinama']: r for r in sn}
    px = os.path.join(o, 'pytest.xml')
    if os.path.exists(px):
        import xml.etree.ElementTree as ET
        ts = ET.parse(px).getroot()
        ts = ts if ts.tag == 'testsuite' else ts.find('testsuite')
        nt = int(ts.get('tests')); nf = int(ts.get('failures')) + int(ts.get('errors')); nsk = int(ts.get('skipped'))
        fails = [tc.get('name') for tc in ts.iter('testcase') if tc.find('failure') is not None or tc.find('error') is not None]
        unit_ok = not any('kosu_duzeyi' not in f for f in fails)
        W('**Sınamalar.** pytest: %d sınama, %d geçti, %d kaldı (cikti/pytest.xml); birim sınamalar%s. Kalanlar koşu '
          'düzeyindedir (cikti/sinamalar.csv): "K_literal" satırları kümelerin yazıldığı gibi iç içe olmadığını gösterir '
          '(yorumla giderildi); hB = 3 sınırı çekim başına optimumların %%%s kadarında bağlayıcıdır; 0,25 ızgara en iyi J '
          'değerini en çok %%%s artırır (sağlam hA değişmez).'
          % (nt, nt - nf - nsk, nf, 'ın hepsi geçti' if unit_ok else ' içinde kalan var: ' + ', '.join(fails),
             pc(sv['izgara_ust_sinir_hB3']['sayi']), pc(sv['izgara_025_Jyildiz_kazanc']['sayi'], 1)))
    else:
        W('**Sınamalar.** pytest çıktısı bulunamadı (cikti/pytest.xml yok); koşu düzeyi sınamalar aşağıda.')
    W('')
    W('| sınama | sonuç | sayı | eşik |')
    W('|---|---|---|---|')
    for r in sn:
        W('| %s | %s | %s | %s |' % (r['sinama'], 'geçti' if r['sonuc'] == 'gecti' else 'kaldı', tr(r['sayi'], 4), r['esik']))
    W('')
    tot = [x for x in sure if x['asama'] == 'toplam']
    W('**Azaltılanlar.** Ana koşuda yok: tam ızgara (%d politika × %d ufuk), senaryo ve tohum başına %d kabul. Yan '
      'koşular küçük: 0,25 ızgara yalnız h3 = 6, %d çekim; Y senaryosu tohum 1, son dönemsiz politikalar. Süre: %s s '
      '(4 süreç; sure.csv).'
      % (Grid(0.5).P * len(OPTS), len(HORIZONS), min(int(F(k['n_kullanilan'])) for k in kab),
         int(F(yak[0]['n_cekim'])), tr(tot[0]['duvar_s'], 0) if tot else '–'))
    W('')
    # ---- 11
    W('## 11. Bu çıktı hangi cümleyle sunulmalı')
    W('')
    W('"Bu tablo ölçüm değil; \'süresiz sürdürebildiğin tavan h3 şu kadarsa tutarlı program şudur\' diyen bir hesap '
      'aracıdır. Saat sayıları h3 varsayımını geri verir; güvenilecek kısım biçimdir: tavanın biraz altında kalmanın '
      'maliyeti küçük, üstüne çıkmanın maliyeti büyüktür, kısa ufuk bunu çok az değiştirir. Hepsi yeterli uyku koşuluna '
      'bağlıdır."')
    W('')
    text = '\n'.join(L)
    path = os.path.join(HERE, 'SONUC.md') if os.path.abspath(o) == os.path.join(HERE, 'cikti') else os.path.join(o, 'SONUC.md')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    nw = sum(len(ln.split()) for ln in L if not ln.startswith('|') and not ln.startswith('**Tablo'))
    print('SONUC.md yazildi: %s (tablo ve tablo basligi disi %d kelime)' % (path, nw), flush=True)


if __name__ == '__main__':
    main()
