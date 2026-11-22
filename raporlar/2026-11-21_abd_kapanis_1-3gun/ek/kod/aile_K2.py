# -*- coding: utf-8 -*-
"""aile_K2.py - Aile B: goreli gecikme, ciftler, artik ve kesitsel donus (YONTEM surum 2).

Tek komut:  python3 -I aile_K2.py            (bakis + IS taramasi + aday dosyasi + OOS + ek testler)
Asamalar :  python3 -I aile_K2.py --asama bakis|is|oos|ek
  is  : butun kural x varyantlari YALNIZ IS'te (yeni yapi: IS2) degerlendirir, aday_K2.csv yazar.
  oos : yalniz aday_K2.csv'deki adaylari tam degerlendirir (OOS, SON, giris A/G, korunma, komisyon,
        rejim, bootstrap), sonuc_K2.csv'yi yazar.
  ek  : OOS'tan gecenler icin kapanis gercekciligi (15:30), kaldiracli satir, komsu parametreler.
Getiri, maliyet, istatistik ve siniflama hesaplari motor.py ile yapilir; burada yalniz sinyal uretilir.
Ara sinyaller scratchpad'de onbelleklenir (ham veri depoya yazilmaz)."""
import argparse
import os
for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_k, "1")      # paylasilan makine: BLAS tek iplik (PCA dongusu icin cok daha hizli)
import pickle
import sys
import time

KOD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOD)
import numpy as np
import pandas as pd
import motor as M
import yukle

VERI = M.VERI_DIZIN
ADAY = os.path.join(VERI, "aday_K2.csv")
SONUC = os.path.join(VERI, "sonuc_K2.csv")
EK_CSV = os.path.join(VERI, "ek_K2.csv")
ONB = os.environ.get("K2_ONBELLEK",
                     "/tmp/claude-0/-home-user-Xxxx/b23916bf-451a-5d36-8905-d1866417ce1f/scratchpad/k2_sinyal.pkl")
SEK11 = ["XLK", "XLF", "XLE", "XLV", "XLI", "XLY", "XLP", "XLU", "XLB", "XLRE", "XLC"]
KAYNAK_YIL = {"R2-03": 2016, "R2-06": 2018, "R4-10": None, "R4-11": 2025, "R5-01": 2010, "R5-02": 2010,
              "R5-03": 2010, "R5-04": 2020, "R5-05": 2012, "R5-06": 2012, "R5-09": 2006, "R5-10": 2015,
              "R5-11": 2023, "KS-ETF": None, "KS-HIS": None}
T0_ILK = "2009-06-01"          # sinyal donguleri bu tarihten baslar (IS 2010 icin pencere payi)


def _isaret(cond_pos, cond_neg, idx, cols=None):
    a = np.where(cond_pos, 1, np.where(cond_neg, -1, 0))
    if cols is None:
        return pd.Series(a, index=idx).astype(int)
    return pd.DataFrame(a, index=idx, columns=cols).astype(int)


def _v(kid, ad, hedef, sig, girdi, kor, guc=None, giris="K", hat="ana", rej=False, bil=None):
    return dict(kid=kid, base=kid.split(":")[0], ad=ad, hedef=hedef, sig=sig, guc=guc, girdi=girdi,
                kor=kor, giris=giris, hat=hat, rej=rej, bil=bil)


# ----------------------------------------------------------------------------- ortak baglam
class Baglam:
    def __init__(self, mm, HIS=None):
        self.mm = mm
        self.idx = mm.idx
        self.T = len(mm.idx)
        self.R = mm.getiri("kk").copy()
        self.evr = mm.donem_basi_evreni()
        self.EM = mm.evren_maskesi(self.evr)
        self.HIS = list(HIS) if HIS is not None else sorted(set(self.evr.kod) & set(mm.kodlar))
        self.grup = {k: str(mm.evren.at[k, "grup"]) for k in self.HIS}
        self.sek = {k: M.GRUP_SEKTOR.get(self.grup[k]) for k in self.HIS}
        self.i0 = int(self.idx.searchsorted(pd.Timestamp(T0_ILK)))
        # bilanco ilk tepki gunleri (tatile denk gelirse sonraki islem gunu)
        B = yukle.bilanco()
        B = B[B.kod.isin(self.HIS) & B.ilk_tepki_gunu.notna()]
        p = self.idx.searchsorted(pd.to_datetime(B.ilk_tepki_gunu))
        ok = p < self.T
        col = {k: i for i, k in enumerate(self.HIS)}
        E = np.zeros((self.T, len(self.HIS)), bool)
        E[p[ok], B.kod.map(col).to_numpy()[ok]] = True
        self.E = pd.DataFrame(E, index=self.idx, columns=self.HIS)
        self.bil_var = pd.Series([k in set(B.kod) for k in self.HIS], index=self.HIS)
        # makro gunleri (FOMC karar + CPI/istihdam)
        F = yukle.fomc()
        F = F[F.tur.isin(["planli", "olaganustu_toplanti", "konferans_gorusmesi"]) & F.aciklama_var.astype(bool)]
        Mk = yukle.makro()
        g = pd.DatetimeIndex(pd.concat([F.karar_gunu, Mk.tarih]))
        self.makro = pd.Series(self.idx.isin(g), index=self.idx)

    def blc(self, L):
        """[t-L+1, t] icinde bilanco ilk tepki gunu var mi (tarih x hisse)."""
        return self.E.rolling(L, min_periods=1).max().astype(bool)


def bilanco_bol(v, bg, L):
    """Hisse sinyalini bilanco iceren / icermeyen olarak ikiye ayirir (bilanco verisi olmayan hisseler disarida)."""
    S = v["sig"]
    W = bg.blc(L).reindex(columns=S.columns, fill_value=False)
    var = bg.bil_var.reindex(S.columns, fill_value=False).to_numpy()[None, :]
    has = W.to_numpy() & var
    no = (~W.to_numpy()) & var
    out = []
    for etiket, msk, ad in (("BLC-", no, "bilanco icermeyen"), ("BLC+", has, "bilanco iceren")):
        s2 = S.where(msk, 0).astype(int)
        w = dict(v)
        w.update(kid=v["kid"] + "|" + etiket, ad=v["ad"] + f" [{ad}, L={L}]", sig=s2,
                 guc=None if v["guc"] is None else v["guc"].where(msk, 0.0), bil=etiket)
        out.append(w)
    return out


def _desil(X, mask, q, ters=False):
    """Her gun mask icindeki X'e gore en dusuk q payi +1, en yuksek q payi -1 (ters=True: tersi)."""
    Xm = X.where(mask)
    rk = Xm.rank(axis=1, method="first")
    n = rk.notna().sum(axis=1)
    d = np.floor(n * q).clip(lower=1)
    d = d.where(n >= 2, 0)
    dusuk = rk.le(d, axis=0)
    yuksek = rk.gt(n - d, axis=0) & rk.notna()
    S = _isaret(dusuk.to_numpy(), yuksek.to_numpy(), X.index, X.columns)
    return -S if ters else S


# ----------------------------------------------------------------------------- kurallar
def k_R2_03(bg):
    mm, R = bg.mm, bg.R
    b = mm.beta("GLD", 60)["GDX"].copy()
    e = R["GLD"] - R["GDX"] / b.where(b.abs() > 0.05)
    s3 = e.rolling(3, min_periods=3).sum()
    out = []
    for w in (60, 250):
        z = M.z_skor(s3, w)
        sig = _isaret((z > 1.5).to_numpy(), (z < -1.5).to_numpy(), bg.idx)
        for hd in ("GDX", "GDXJ"):
            out.append(_v(f"R2-03:{hd}-w{w}", f"GLD - GDX/b60 3 gunluk artik z(w{w}) >+1,5 al / <-1,5 sat -> {hd}",
                          hd, sig, "GLD,GDX kk; b60(GDX~GLD); z penceresi t-1", "yok"))
    return out


def k_R2_06(bg):
    mm, R = bg.mm, bg.R
    b = mm.beta("SPY", 60)["HYG"].copy()
    e = R["HYG"] - b * R["SPY"]
    lo, hi = M.genisleyen_esik(e, 0.10), M.genisleyen_esik(e, 0.90)
    sig = _isaret((e > hi).to_numpy(), (e < lo).to_numpy(), bg.idx)
    return [_v(f"R2-06:{hd}", f"HYG - b60*SPY artigi ust %10 al / alt %10 sat -> {hd} (curutme testi)",
               hd, sig, "HYG,SPY kk; genisleyen %10/%90 (t-1)", "yok") for hd in ("SPY", "IWM")]


def k_R4_10(bg):
    mm, R = bg.mm, bg.R
    fol = ["AMD", "AVGO", "MU", "SMCI", "SMH"]
    b = mm.beta("NVDA", 60)[fol].copy()
    rN = R["NVDA"]
    gap = R[fol] - b.mul(rN, axis=0)
    dus = (rN <= -0.04).to_numpy()[:, None]
    yuk = (rN >= 0.04).to_numpy()[:, None]
    sat = dus & (gap >= 0.02).to_numpy()
    al = yuk & (gap <= -0.02).to_numpy()
    sig = _isaret(al, sat, bg.idx, fol)
    return [_v("R4-10:takipci", "NVDA |r|>=%4 gunu beta tahmininin 2 puan gerisinde kalan takipci: yon NVDA ile",
               None, sig, "NVDA, AMD, AVGO, MU, SMCI, SMH kk; b60(~NVDA)", "yok", guc=gap.abs())]


def k_R4_11(bg):
    mm, R = bg.mm, bg.R
    btc = yukle.kripto_1600()["BTC-USD"].reindex(bg.idx)
    rB = btc / btc.shift(1) - 1.0                       # 16:00 -> 16:00 ET (ABD16 ile es zamanli)
    mn = ["MARA", "RIOT", "CLSK", "WGMI"]
    bask = R[mn].mean(axis=1, skipna=True)
    v = rB.notna() & bask.notna()
    x, y = rB.where(v), bask.where(v)
    r = lambda s: s.rolling(60, min_periods=30).mean()
    beta = ((r(x * y) - r(x) * r(y)) / (r(x * x) - r(x) ** 2)).shift(1)
    art = bask - beta * rB
    al = (art < -0.05).to_numpy()[:, None] & R[mn].notna().to_numpy()
    sat = (art > 0.05).to_numpy()[:, None] & R[mn].notna().to_numpy()
    sig = _isaret(al, sat, bg.idx, mn)
    guc = pd.DataFrame(np.repeat(art.abs().to_numpy()[:, None], len(mn), 1), index=bg.idx, columns=mn)
    return [_v("R4-11:madenci", "Madenci sepeti - b60*BTC(16:00) artigi <-%5 al / >+%5 sat (MARA,RIOT,CLSK,WGMI)",
               None, sig, "BTC-USD 16:00 ET (kripto_1600), madenci kk; b60 t-1", "yok", guc=guc, hat="yeni")]


def _ou(eps, W, kmin, ok):
    """Avellaneda-Lee: X = kumulatif artik; X[0..W-1] uzerinde AR(1); s = (X[W]-m)/sigma_eq."""
    X = np.cumsum(eps, 0)
    x0, x1 = X[:W - 1], X[1:W]
    m0, m1 = x0.mean(0), x1.mean(0)
    v0 = ((x0 - m0) ** 2).sum(0)
    with np.errstate(invalid="ignore", divide="ignore"):
        b = ((x0 - m0) * (x1 - m1)).sum(0) / np.where(v0 > 0, v0, np.nan)
        a = m1 - b * m0
        res = x1 - a - b * x0
        ve = res.var(0, ddof=1)
        kap = -np.log(b) * 252
        mu = a / (1 - b)
        seq = np.sqrt(ve / (1 - b * b))
        s = (X[W] - mu) / seq
    good = ok & (b > 0) & (b < 1) & (kap > kmin) & np.isfinite(s)
    return np.where(good, s, np.nan)


def s_skor_tek(Y, F, i0, W=60, kmin=8.4):
    """Tek faktorlu (hisse basina sektor ETF'i) s-skoru; tahmin penceresi [t-W, t-1], X[W] t gununu icerir."""
    T, N = Y.shape
    S = np.full((T, N), np.nan)
    for t in range(max(W, i0), T):
        y, f = Y[t - W:t + 1], F[t - W:t + 1]
        ok = np.isfinite(y).all(0) & np.isfinite(f).all(0)
        if not ok.any():
            continue
        ye, fe = y[:-1], f[:-1]
        fm, ym = fe.mean(0), ye.mean(0)
        vf = ((fe - fm) ** 2).sum(0)
        with np.errstate(invalid="ignore", divide="ignore"):
            beta = ((fe - fm) * (ye - ym)).sum(0) / np.where(vf > 0, vf, np.nan)
        eps = y - (ym - beta * fm) - beta * f
        S[t] = _ou(eps, W, kmin, ok)
    return S


def _s_sinyal(S, cols, bg, kid, ad, girdi):
    Sd = pd.DataFrame(S, index=bg.idx, columns=cols)
    em = bg.EM[cols]
    sig = _isaret(((Sd < -1.25) & em).to_numpy(), ((Sd > 1.25) & em).to_numpy(), bg.idx, cols)
    v = _v(kid, ad, None, sig, girdi, "SPY:60", guc=Sd.abs().where(em, 0.0).fillna(0.0))
    return [v] + bilanco_bol(v, bg, 5)


def k_R5_01_02(bg):
    mm, R = bg.mm, bg.R
    cols = [k for k in bg.HIS if bg.sek[k] in mm.kpos]
    Y = R[cols].to_numpy()
    F = np.column_stack([R[bg.sek[k]].to_numpy() for k in cols])
    out = _s_sinyal(s_skor_tek(Y, F, bg.i0), cols, bg, "R5-01:s125",
                    "Sektor ETF artigi s-skoru (AL): s<-1,25 al, s>+1,25 sat; kappa>8,4", "hisse, GRUP_SEKTOR ETF; W=60")
    vol = mm.df("volume")[cols]
    for L in (10, 20):
        w = (vol.rolling(L, min_periods=L).mean().shift(1) / vol.where(vol > 0)).to_numpy()
        out += _s_sinyal(s_skor_tek(Y * w, F, bg.i0), cols, bg, f"R5-02:hac{L}",
                         f"Hacim ayarli s-skoru (ort.hacim{L}/hacim): s<-1,25 al, s>+1,25 sat", "hisse, hacim, sektor ETF; W=60")
    return out


def k_R5_03(bg, Wc=252, W=60):
    R = bg.R
    cols = bg.HIS
    Y = R[cols].to_numpy()
    EMn = bg.EM[cols].to_numpy()
    T, N = Y.shape
    S = {"k15": np.full((T, N), np.nan), "v55": np.full((T, N), np.nan)}
    for t in range(max(Wc, bg.i0), T):
        u = EMn[t] & np.isfinite(Y[t - Wc:t + 1]).all(0)
        if u.sum() < 40:
            continue
        Z = Y[t - Wc:t][:, u]
        mu, sd = Z.mean(0), Z.std(0, ddof=1)
        Zs = (Z - mu) / sd
        ev, V = np.linalg.eigh(Zs.T @ Zs / (Wc - 1))
        ev, V = ev[::-1], V[:, ::-1]
        k55 = int(np.searchsorted(np.cumsum(ev) / ev.sum(), 0.55) + 1)
        y = Y[t - W:t + 1][:, u]
        for ad, k in (("k15", 15), ("v55", k55)):
            Fw = y @ (V[:, :k] / sd[:, None])
            Xd = np.column_stack([np.ones(W + 1), Fw])
            Xe = Xd[:-1]
            coef = np.linalg.solve(Xe.T @ Xe, Xe.T @ y[:-1])
            eps = y - Xd @ coef
            S[ad][t, u] = _ou(eps, W, 8.4, np.ones(u.sum(), bool))
    out = []
    for ad, a2 in (("k15", "k=15"), ("v55", "%55 varyans")):
        out += _s_sinyal(S[ad], cols, bg, f"R5-03:{ad}", f"PCA artigi s-skoru ({a2}, 252g korelasyon): s<-1,25 al, s>+1,25 sat",
                         "evren hisseleri; PCA 252g t-1; W=60")
    return out


def k_R5_04(bg):
    mm, R = bg.mm, bg.R
    cols = bg.HIS
    top = mm.evren_maskesi(bg.evr[bg.evr.sira <= 30])[cols]
    s60 = R[cols].rolling(60, min_periods=30).std().shift(1)
    z = R[cols] / s60.where(s60 > 0)
    base = _desil(z, top, 0.10)
    v1 = mm.girdi("^VIX", "close")
    kos = {"hepsi": pd.Series(True, index=bg.idx), "a_vix30": v1 >= 30, "b_vix20": v1 < 20,
           "c_vix30_tepealti": (v1 >= 30) & (v1 < v1.rolling(5, min_periods=5).max())}
    out = []
    for ad, c in kos.items():
        sig = base.where(np.broadcast_to(c.to_numpy()[:, None], base.shape), 0).astype(int)
        v = _v(f"R5-04:{ad}", f"Buyuk hisse (ilk 30) z=r/sigma60 en dusuk %10 al, en yuksek %10 sat; kosul {ad} (VIX t-1)",
               None, sig, "hisse kk, sigma60 t-1, ^VIX(t-1)", "SPY:60", guc=z.abs().fillna(0.0))
        out += [v] + bilanco_bol(v, bg, 1)
    return out


def k_R5_05(bg):
    R = bg.R
    cols = bg.HIS
    adj = R[cols].sub(R["SPY"], axis=0)
    sc = -adj.rolling(5, min_periods=5).mean()
    sig = _desil(sc, bg.EM[cols], 0.10, ters=True)          # en yuksek skor (en cok dusen) uzun
    v = _v("R5-05:nagel5", "Nagel 5 gecikmeli piyasa-ayarli donus: son 5 gun (r_i - r_SPY) en dusuk %10 al, en yuksek %10 sat",
           None, sig, "hisse ve SPY kk", "SPY:60", guc=sc.abs().fillna(0.0))
    return [v] + bilanco_bol(v, bg, 5)


def k_R5_06(bg):
    mm = bg.mm
    P = mm.girdi(SEK11 + ["SPY"], "adjclose")
    r5 = P / P.shift(5) - 1.0
    rel = r5[SEK11].sub(r5["SPY"], axis=0)
    v1 = mm.girdi("^VIX", "close")
    rk = rel.rank(axis=1, method="first")
    n = rk.notna().sum(axis=1)
    dus, yuk = rk.le(2, axis=0), rk.gt(n - 2, axis=0) & rk.notna()
    hi = (v1 >= 30).to_numpy()[:, None]
    lo = (v1 < 20).to_numpy()[:, None]
    s_hi = _isaret(dus.to_numpy() & hi, yuk.to_numpy() & hi, bg.idx, SEK11)
    s_lo = _isaret(yuk.to_numpy() & lo, dus.to_numpy() & lo, bg.idx, SEK11)
    g = rel.abs().fillna(0.0)
    return [_v("R5-06:vix30_donus", "VIX(t-1)>=30: 5 gunluk SPY'ye goreli en kotu 2 sektor al, en iyi 2 sat", None, s_hi,
               "11 SPDR + SPY adjclose, ^VIX(t-1)", "yok", guc=g),
            _v("R5-06:vix20_devam", "Kontrol: VIX(t-1)<20: en iyi 2 sektor al, en kotu 2 sat (devam)", None, s_lo,
               "11 SPDR + SPY adjclose, ^VIX(t-1)", "yok", guc=g)]


def cift_olaylari(bg, ayni_sektor, n_cift=20, Wf=252, Wt=126):
    """Gatev mesafe ciftleri: olay listesi (t_pos, uzun_kod, kisa_kod, |d|/sigma)."""
    mm = bg.mm
    cols = bg.HIS
    P = mm.df("adjclose")[cols].to_numpy()
    grp = np.array([bg.grup[k] for k in cols])
    ci = {k: i for i, k in enumerate(cols)}
    ev = []
    p0 = int(bg.idx.searchsorted(pd.Timestamp("2010-01-01")))
    while p0 < bg.T:
        d0 = bg.idx[p0]
        dn = "IS" if d0.year < 2020 else ("OOS" if d0.year < 2024 else "SON")
        uni = [ci[k] for k in bg.evr.loc[bg.evr.donem == dn, "kod"] if k in ci]
        f0 = p0 - Wf
        blok = P[f0:p0][:, uni]
        u = np.array(uni)[np.isfinite(blok).all(0) & (blok[0] > 0)]
        Pn = P[f0:p0][:, u] / P[f0, u]
        G = Pn.T @ Pn
        q = np.diag(G)
        D = q[:, None] + q[None, :] - 2 * G
        D[np.tril_indices(len(u))] = np.inf
        if ayni_sektor:
            D[grp[u][:, None] != grp[u][None, :]] = np.inf
        sec = np.argsort(D, axis=None)[:n_cift]
        ii, jj = np.unravel_index(sec, D.shape)
        p1 = min(p0 + Wt, bg.T)
        for a, b in zip(ii, jj):
            if not np.isfinite(D[a, b]):
                continue
            A, B = u[a], u[b]
            sig = np.std(Pn[:, a] - Pn[:, b], ddof=1)
            Q = P[p0 - 1:p1][:, [A, B]] / P[p0 - 1, [A, B]]
            d = Q[:, 0] - Q[:, 1]
            ac = np.abs(d) > 2 * sig
            for r in range(1, len(d)):
                if ac[r] and not ac[r - 1] and np.isfinite(d[r]) and np.isfinite(d[r - 1]):
                    kaz, kay = (A, B) if d[r] > 0 else (B, A)
                    ev.append((p0 - 1 + r, cols[kay], cols[kaz], abs(d[r]) / sig))
        p0 += Wt
    return pd.DataFrame(ev, columns=["t", "uzun", "kisa", "z"])


def _olay_sinyal(bg, ev):
    cols = bg.HIS
    ci = {k: i for i, k in enumerate(cols)}
    top = np.zeros((bg.T, len(cols)))
    mut = np.zeros((bg.T, len(cols)))
    g = np.zeros((bg.T, len(cols)))
    for k, (t, a, b, z) in enumerate(ev[["t", "uzun", "kisa", "z"]].itertuples(index=False)):
        zz = z + 1e-6 * k
        for kod, s in ((a, 1), (b, -1)):
            top[t, ci[kod]] += s
            mut[t, ci[kod]] += 1
            g[t, ci[kod]] = max(g[t, ci[kod]], zz)
    S = np.where(np.abs(top) == mut, np.sign(top), 0)
    return (pd.DataFrame(S, index=bg.idx, columns=cols).astype(int),
            pd.DataFrame(np.where(S != 0, g, 0.0), index=bg.idx, columns=cols))


def k_R5_09_10(bg):
    out = []
    E2 = bg.blc(2)
    bv = bg.bil_var
    spy = bg.R["SPY"].to_numpy()
    mak = bg.makro.to_numpy()
    for ayni, et in ((False, "tum"), (True, "sektor")):
        ev = cift_olaylari(bg, ayni)
        t = ev.t.to_numpy()
        bil_ok = bv.reindex(ev.uzun).to_numpy() & bv.reindex(ev.kisa).to_numpy()
        e_any = (E2.to_numpy()[t, [bg.HIS.index(k) for k in ev.uzun]] |
                 E2.to_numpy()[t, [bg.HIS.index(k) for k in ev.kisa]])
        alt = {"": np.ones(len(ev), bool), "|BLC-": bil_ok & ~e_any, "|BLC+": bil_ok & e_any}
        for ek, msk in alt.items():
            S, G = _olay_sinyal(bg, ev[msk])
            ad = f"Gatev mesafe cifti ({et}) 2 sigma ayrisma: kaybeden al, kazanan sat; bir gun bekle (giris G)"
            if ek:
                ad += " [bilanco " + ("icermeyen" if ek == "|BLC-" else "iceren") + ", [t-1,t]]"
            out.append(_v(f"R5-09:{et}{ek}", ad, None, S, "hisse adjclose; 252g olusum, 126g islem", "yok", guc=G,
                          giris="G", bil=ek.strip("|") or None))
        if not ayni:
            ortak = (np.abs(spy[t]) >= 0.01) | mak[t]
            for kid, msk, ad in (("R5-10:ortak_haber", bil_ok & ~e_any & ortak,
                                  "Cift ayrismasi yalniz |SPY|>=%1 ya da makro gunu ve [t-1,t] bilancosuz"),
                                 ("R5-10:bilanco_kaynakli", bil_ok & e_any,
                                  "Ters kosul: [t-1,t] icinde ciftin en az bir hissesinde bilanco")):
                S, G = _olay_sinyal(bg, ev[msk])
                out.append(_v(kid, ad, None, S, "R5-09 ciftleri, SPY kk, FOMC/CPI/istihdam, bilanco", "yok",
                              guc=G, giris="G"))
    return out


def _adf_t(e):
    de, el = np.diff(e), e[:-1]
    g = (el @ de) / (el @ el)
    r = de - g * el
    se = np.sqrt((r @ r) / (len(de) - 1) / (el @ el))
    return g / se


def k_R5_11(bg):
    mm = bg.mm
    out = []
    for A, B in (("GLD", "GDX"), ("XLE", "USO"), ("SMH", "SOXX"), ("XLE", "OIH")):
        P = mm.girdi([A, B], "adjclose")
        la, lb = np.log(P[A]), np.log(P[B])
        v = la.notna() & lb.notna()
        la, lb = la.where(v), lb.where(v)
        r = lambda s: s.rolling(60, min_periods=60).mean().shift(1)
        va, vb, cab = r(la * la) - r(la) ** 2, r(lb * lb) - r(lb) ** 2, r(la * lb) - r(la) * r(lb)
        hh = cab / vb
        mu = r(la) - hh * r(lb)
        sd = np.sqrt((va - 2 * hh * cab + hh * hh * vb).clip(lower=1e-12))
        z = (la - hh * lb - mu) / sd
        # yillik es-butunlesme: Y yili icin Y oncesi 252 gun, Engle-Granger ADF t < -3,34
        izin = pd.Series(False, index=bg.idx)
        for Y in range(2006, 2027):
            i1 = int(bg.idx.searchsorted(pd.Timestamp(f"{Y}-01-01")))
            x, y = lb.iloc[max(i1 - 252, 0):i1].to_numpy(), la.iloc[max(i1 - 252, 0):i1].to_numpy()
            ok = np.isfinite(x) & np.isfinite(y)
            if ok.sum() < 200:
                continue
            x, y = x[ok], y[ok]
            bb = np.polyfit(x, y, 1)
            if _adf_t(y - np.polyval(bb, x)) < -3.34:
                izin[(bg.idx.year == Y)] = True
        for thr in (1.5, 2.0, 2.5):
            sig = _isaret(((z < -thr) & izin).to_numpy(), ((z > thr) & izin).to_numpy(), bg.idx)
            out.append(_v(f"R5-11:{A}/{B}-z{thr}", f"ETF cifti {A}/{B} log-spread z(60) <-{thr}: {A} al + h*{B} sat; >+{thr} tersi; yillik ADF",
                          A, sig, f"{A},{B} adjclose; h ve z 60g t-1; ADF yillik", f"{B}:60"))
    return out


def k_KS(bg):
    mm, R = bg.mm, bg.R
    out = []
    artE = mm.artik_getiri(SEK11, piyasa="SPY", sektor=None, pencere=250)
    artH = mm.artik_getiri(bg.HIS, piyasa="SPY", sektor="oto", pencere=250)
    gr = pd.Series(bg.grup)
    em = bg.EM[bg.HIS]
    artH = artH.where(em)
    artHn = artH.sub(artH.T.groupby(gr).transform("mean").T, axis=None)      # sektor-notr: grup ortalamasi cikar
    s20 = mm.sigma20()[bg.HIS]
    for L in (1, 3, 5):
        cE = artE.rolling(L, min_periods=L).sum()
        sE = _desil(cE, cE.notna(), 0.20)
        out.append(_v(f"KS-ETF:L{L}", f"11 SPDR: {L} gunluk SPY artigi en kotu %20 al, en iyi %20 sat", None, sE,
                      "sektor ETF ve SPY kk, b250 t-1", "yok", guc=cE.abs().fillna(0.0), rej=True))
        cH = artHn.rolling(L, min_periods=L).sum()
        sH = _desil(cH, em & cH.notna(), 0.20)
        v = _v(f"KS-HIS:L{L}", f"150 hisse: {L} gunluk sektor-notr artik en kotu %20 al, en iyi %20 sat", None, sH,
               "hisse, SPY, sektor kk; iki faktorlu b250 t-1; grup ortalamasi cikarildi", "SPY:60",
               guc=(cH.abs() / (s20 * np.sqrt(L))).fillna(0.0), rej=True)
        out += [v] + bilanco_bol(v, bg, L)
    return out


KURALLAR = [k_R2_03, k_R2_06, k_R4_10, k_R4_11, k_R5_01_02, k_R5_03, k_R5_04, k_R5_05, k_R5_06,
            k_R5_09_10, k_R5_11, k_KS]


def butun_varyantlar(mm, onbellek=True):
    """Butun kural x varyant sinyalleri; kural islevi basina scratchpad onbellegi."""
    bg = None
    V = []
    for fn in KURALLAR:
        yol = ONB.replace(".pkl", f"_{fn.__name__}.pkl")
        if onbellek and os.path.exists(yol):
            with open(yol, "rb") as f:
                V += pickle.load(f)
            continue
        bg = bg or Baglam(mm)
        t0 = time.time()
        out = fn(bg)
        print(f"  {fn.__name__}: {time.time() - t0:.1f} sn", flush=True)
        if onbellek:
            os.makedirs(os.path.dirname(ONB), exist_ok=True)
            with open(yol, "wb") as f:
                pickle.dump(out, f)
        V += out
    return V


# ----------------------------------------------------------------------------- degerlendirme
def _coklu(v):
    return isinstance(v["sig"], pd.DataFrame) and v["sig"].shape[1] > 1


def karar_t(row, coklu):
    return row["t_kume"] if coklu else row["t_olcekli"]


def gecti(row, coklu, esik=2.0):
    t = karar_t(row, coklu)
    ok = (row["n_islem"] > 0) and (row["net_bps"] > 0) and np.isfinite(t) and (t >= esik)
    if row["yon"] in ("uzun", "kisa"):
        ok = ok and (row["anormal_bps"] > 0) and np.isfinite(row["t_anormal"]) and (row["t_anormal"] >= 2)
    return bool(ok)


def asama_is(m):
    V = butun_varyantlar(m)
    sat, aday = [], []
    for v in V:
        dn = ["IS2"] if v["hat"] == "yeni" else ["IS"]
        r = m.degerlendir(v["sig"], v["hedef"], kural_id=v["kid"], aile="B", ad=v["ad"], girdi=v["girdi"],
                          h=(1, 2, 3), giris=(v["giris"],), gece=False, korunma=(v["kor"],), komisyon=("hisse",),
                          donemler=dn, rejimler=v["rej"], guc=v["guc"], notlar=f"asama=IS-tarama; hat={v['hat']}")
        sat.append(r)
        cok = _coklu(v)
        for _, row in r[r.rejim == "hepsi"].iterrows():
            if gecti(row, cok):
                aday.append(dict(kural_id=v["kid"], ad=v["ad"], hedef=row["hedef"], yon=row["yon"], h=int(row["h"]),
                                 giris=v["giris"], korunma=v["kor"], hat=v["hat"], coklu=cok,
                                 olcu="t_kume" if cok else "t_olcekli", n_islem=int(row["n_islem"]),
                                 is_net_bps=row["net_bps"], is_t=karar_t(row, cok), is_t_anormal=row["t_anormal"],
                                 is_anormal_bps=row["anormal_bps"], yayin_yili=KAYNAK_YIL.get(v["base"])))
    S = pd.concat(sat, ignore_index=True)
    A = pd.DataFrame(aday, columns=["kural_id", "ad", "hedef", "yon", "h", "giris", "korunma", "hat", "coklu", "olcu",
                                    "n_islem", "is_net_bps", "is_t", "is_t_anormal", "is_anormal_bps", "yayin_yili"])
    A.to_csv(ADAY, index=False)
    S.to_pickle(ONB.replace(".pkl", "_is.pkl"))
    n_test = int((S.rejim == "hepsi").sum())
    print(f"IS: {len(V)} sinyal, {n_test} kural x varyant (h dahil), {len(A)} aday -> {ADAY}")
    return S, A


def asama_oos(m):
    V = {v["kid"]: v for v in butun_varyantlar(m)}
    S_is = pd.read_pickle(ONB.replace(".pkl", "_is.pkl"))
    A = pd.read_csv(ADAY)
    sat, ozet = [], []
    aday_anahtar = set()
    for kid, grp in A.groupby("kural_id", sort=False):
        v = V[kid]
        hs = tuple(sorted(grp.h.astype(int).unique()))
        dn = list(M.YENI_YAPI) if v["hat"] == "yeni" else None
        korl = [v["kor"]] + [k for k in ("yok", "SPY:250", "SPY:60", "SDS:60") if k != v["kor"]]
        if v["kor"].endswith(":60") and not v["kor"].startswith(("SPY", "SDS")):
            korl.append(v["kor"].replace(":60", ":250"))
        ort = dict(kural_id=kid, aile="B", ad=v["ad"], girdi=v["girdi"], guc=v["guc"], donemler=dn)
        r1 = m.degerlendir(v["sig"], v["hedef"], h=hs, giris=(v["giris"],), gece=False, korunma=(v["kor"],),
                           rejimler=True, bootstrap=True, notlar=f"asama=aday-birincil; hat={v['hat']}", **ort)
        r2 = m.degerlendir(v["sig"], v["hedef"], h=hs, giris=("K", "A", "G"), gece=True, korunma=tuple(korl),
                           rejimler=False, bootstrap=False, notlar=f"asama=aday-ek; hat={v['hat']}", **ort)
        anah = ["giris", "cikis", "h", "korunma", "komisyon", "donem", "rejim"]
        r2 = r2[~r2.set_index(anah).index.isin(r1.set_index(anah).index)]
        sat += [r1, r2]
        cok = _coklu(v)
        oosd, sond = ("OOS2", None) if v["hat"] == "yeni" else ("OOS", "SON")
        for hh in hs:
            aday_anahtar.add((kid, hh))
            b = r1[(r1.h == hh) & (r1.komisyon == "hisse") & (r1.rejim == "hepsi") & (r1.cikis == "kapanis")]
            o = b[b.donem == oosd].iloc[0]
            esik = 3.0 if v["hat"] == "yeni" else 2.0
            ozet.append(dict(kural_id=kid, h=hh, hat=v["hat"], oos_net_bps=o.net_bps, oos_n=o.n_islem,
                             oos_t=karar_t(o, cok), oos_t_anormal=o.t_anormal, oos_p=o.p_bootstrap,
                             oos_gecti=gecti(o, cok, esik)))
    S_is = S_is[~S_is.apply(lambda r: (r.kural_id, int(r.h)) in aday_anahtar, axis=1)]
    S = pd.concat([S_is] + sat, ignore_index=True)
    M.yaz_sonuc(S, SONUC)
    O = pd.DataFrame(ozet, columns=["kural_id", "h", "hat", "oos_net_bps", "oos_n", "oos_t", "oos_t_anormal",
                                    "oos_p", "oos_gecti"])
    O.to_csv(ONB.replace(".pkl", "_oos_ozet.csv"), index=False)
    print(O.to_string(index=False))
    print(f"sonuc: {len(S)} satir -> {SONUC}")
    return S, O


def asama_ek(m):
    """OOS'tan gecenler icin ek testler (kapanis gercekciligi 15:30, kaldiracli satir, komsu parametreler).
    Bu calismada OOS'tan gecen kural yok; gecen olursa ek testler burada eklenmeli (bilerek bos)."""
    yol = ONB.replace(".pkl", "_oos_ozet.csv")
    O = pd.read_csv(yol) if os.path.exists(yol) and os.path.getsize(yol) > 1 else pd.DataFrame()
    gecen = O[O.oos_gecti.astype(bool)] if len(O) else O
    if len(gecen) == 0:
        print("ek: OOS'tan gecen kural yok; kapanis gercekciligi / kaldiracli / komsu parametre testleri uygulanmadi.")
        return None
    raise NotImplementedError("OOS'tan gecen kural var: ek testleri yazin (YONTEM 4, 7).")


def asama_bakis(m):
    """Her kural islevi icin ileriye bakma denetimi (T0 sonrasi bozulan veri T0 oncesi sinyali degistirmemeli)."""
    sonuc = []
    HIS0 = Baglam(m).HIS        # sutun kumesi sabit: bozuk kopyada OOS/SON evreni degisse de karsilastirma ayni sutunlarda
    for fn in KURALLAR:
        def birlesik(mm, fn=fn):
            out = fn(Baglam(mm, HIS=HIS0))
            parca = []
            for v in out:
                s = v["sig"]
                s = s.to_frame(v["kid"]) if isinstance(s, pd.Series) else s.add_prefix(v["kid"] + "|")
                parca.append(s)
            return pd.concat(parca, axis=1)
        t0 = time.time()
        ok, rap = m.bakis_testi(birlesik)
        sonuc.append((fn.__name__, ok, rap))
        print(f"  bakis {fn.__name__}: {ok} {rap} ({time.time() - t0:.0f} sn)", flush=True)
    return sonuc


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--asama", default="hepsi", choices=["hepsi", "bakis", "is", "oos", "ek"])
    ap.add_argument("--yeniden", action="store_true", help="sinyal onbellegini sil")
    a = ap.parse_args()
    if a.yeniden:
        import glob
        for f in glob.glob(ONB.replace(".pkl", "_k_*.pkl")):
            os.remove(f)
    t0 = time.time()
    m = M.Motor()
    if a.asama in ("hepsi", "bakis"):
        asama_bakis(m)
    if a.asama in ("hepsi", "is"):
        asama_is(m)
    if a.asama in ("hepsi", "oos"):
        asama_oos(m)
    if a.asama in ("hepsi", "ek"):
        asama_ek(m)
    print(f"toplam {time.time() - t0:.0f} sn")
