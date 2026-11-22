# -*- coding: utf-8 -*-
"""aile_K1.py - Aile A (lider -> takipci) backtest'i, YONTEM surum 2.

Tek komut:   python3 -I aile_K1.py            (asamalar sirayla: is -> oos -> detay -> bugun)
Asama asama: python3 -I aile_K1.py is | oos | is_sabit | oos_sabit | detay | bugun
(is_sabit/oos_sabit: duyarlilik - aday elemesi emir basi sabit 1,5 $ komisyonla; aday_K1_sabit.csv)
Ciktilar: ../veri/aday_K1.csv (OOS'a bakmadan once), ../veri/sonuc_K1.csv (motor SEMA'si).
Ara dosyalar (ham veri degil, yeniden uretilebilir): scratchpad/k1/.
Getiri, maliyet, istatistik ve siniflama motor.py ile; burada yalniz sinyal serileri uretilir."""
import os
import sys
import time
import json

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import motor as M          # noqa: E402
import yukle               # noqa: E402

VERI = M.VERI_DIZIN
ADAY_YOL = os.path.join(VERI, "aday_K1.csv")
SONUC_YOL = os.path.join(VERI, "sonuc_K1.csv")
ARA = os.path.join(os.path.dirname(yukle.PANEL.rstrip("/")), "k1")
os.makedirs(ARA, exist_ok=True)
NAN = np.nan
RNG_TOHUM = 20261121

# ----------------------------------------------------------------------------- tema kumeleri (gorev metni, onceden yazili)
# ad, liderler, takipciler, hat ('ana' | 'yeni' | 'ikisi'), tema sinifi
KUMELER = {
    "YI": ("yari iletken", ["NVDA", "TSM", "AVGO"],
           ["AMD", "MU", "MRVL", "AMAT", "LRCX", "KLAC", "ASML", "ON", "MCHP", "SMCI", "SOXX", "SMH"], "ana", False),
    "KR": ("kripto (BTC 16:00 ET)", ["BTC16"],
           ["MSTR", "COIN", "MARA", "RIOT", "CLSK", "IREN", "HUT", "WULF", "CIFR", "HOOD"], "ikisi", True),
    "EV": ("elektrikli arac", ["TSLA"], ["RIVN", "LCID", "NIO", "XPEV", "LI"], "yeni", True),
    "NK": ("nukleer/elektrik", ["CCJ", "CEG", "VST"], ["OKLO", "SMR", "UEC", "LEU", "NNE", "BWXT", "URA"], "ana", True),
    "KU": ("kuantum", ["IONQ"], ["RGTI", "QBTS", "QUBT"], "yeni", True),
    "UZ": ("uzay", ["RKLB"], ["ASTS", "LUNR", "PL"], "yeni", True),
    "YZ": ("yapay zeka yazilimi", ["PLTR"], ["AI", "SOUN", "BBAI"], "yeni", True),
    "BN": ("bankalar", ["JPM"], ["BAC", "C", "WFC", "KRE"], "ana", False),
    "EN": ("enerji", ["XOM"], ["OXY", "DVN", "SLB", "HAL", "XOP"], "ana", False),
    "CN": ("Cin", ["BABA"], ["PDD", "JD", "BIDU", "KWEB", "FXI"], "ana", False),
    "HY": ("havayolu", ["DAL"], ["UAL", "AAL", "LUV", "JETS"], "ana", False),
    "KO": ("konut", ["DHI"], ["LEN", "PHM", "TOL", "XHB", "ITB"], "ana", False),
    "KI": ("kilo ilaci", ["LLY"], ["NVO", "VKTX", "HIMS"], "ana", True),
}
SEKTORLER = ["XLB", "XLE", "XLF", "XLI", "XLK", "XLP", "XLU", "XLV", "XLY", "XLRE", "XLC"]
R6_GRUPLAR = ["h_yari_iletken", "h_banka", "h_yazilim", "h_enerji", "h_saglik", "h_tuketici", "h_sanayi_diger"]
R47_DISI = ("h_mega", "h_meme")


# ----------------------------------------------------------------------------- yardimcilar
def rbeta(Y, x, W=250):
    """Y (DataFrame) sutunlarinin x'e kayan betasi; t satiri [t-W, t-1] (motor.beta ile ayni kural)."""
    Yv = Y.to_numpy(float)
    xv = np.asarray(x, float)[:, None]
    v = np.isfinite(Yv) & np.isfinite(xv)
    y0, x0 = np.where(v, Yv, 0.0), np.where(v, xv, 0.0)

    def rs(a):
        return pd.DataFrame(a).rolling(W, min_periods=1).sum().to_numpy()
    n = rs(v.astype(float))
    sx, sy, sxy, sxx = rs(x0), rs(y0), rs(x0 * y0), rs(x0 * x0)
    with np.errstate(invalid="ignore", divide="ignore"):
        b = (sxy - sx * sy / n) / (sxx - sx * sx / n)
        b[(n < max(W // 2, 20)) | ~((sxx - sx * sx / n) > 1e-14)] = NAN
    b = np.vstack([np.full((1, b.shape[1]), NAN), b[:-1]])
    return pd.DataFrame(b, index=Y.index, columns=Y.columns)


def zz(x_bugun, x_gecmis, W):
    """z = (x_t - ort(gecmis[t-W..t-1])) / std(gecmis[t-W..t-1]). x_bugun ile x_gecmis gunluk seride ayni;
    15:30 denemesinde x_bugun 15:30 fiyatindan, pencere istatistikleri gunluk kapanistan."""
    mp = max(5, W // 2)
    mu = x_gecmis.rolling(W, min_periods=mp).mean().shift(1)
    sd = x_gecmis.rolling(W, min_periods=mp).std().shift(1)
    return (x_bugun - mu) / sd.where(sd > 0)


def rcorr_lag(X, y, W):
    """Kayan korelasyon corr(X_s, y_s) (s pencere icinde), pencere t-1'de biter. X: T x N, y: T."""
    Xv = X.to_numpy(float)
    yv = np.asarray(y, float)[:, None]
    v = np.isfinite(Xv) & np.isfinite(yv)
    a, b = np.where(v, Xv, 0.0), np.where(v, yv, 0.0)

    def rs(z):
        return pd.DataFrame(z).rolling(W, min_periods=1).sum().to_numpy()
    n = rs(v.astype(float))
    sa, sb, sab, saa, sbb = rs(a), rs(b), rs(a * b), rs(a * a), rs(b * b)
    with np.errstate(invalid="ignore", divide="ignore"):
        c = (sab - sa * sb / n) / np.sqrt((saa - sa * sa / n) * (sbb - sb * sb / n))
    c[n < max(W // 2, 20)] = NAN
    c = np.vstack([np.full((1, c.shape[1]), NAN), c[:-1]])
    return pd.DataFrame(c, index=X.index, columns=X.columns)


def esit_guc(S, siddet):
    """guc: |siddet| (gun bazinda) x (1 + kucuk sabit tohumlu gurultu) -> esitlikler sutun sirasiyla bozulmaz."""
    G = np.abs(np.asarray(siddet, float))
    if G.ndim == 1:
        G = np.repeat(G[:, None], S.shape[1], axis=1)
    rng = np.random.default_rng(RNG_TOHUM)
    G = np.nan_to_num(G) * (1.0 + 1e-6 * rng.random(S.shape)) + 1e-9
    return pd.DataFrame(G, index=S.index, columns=S.columns)


class Kaynak:
    """Sinyal girdileri. R: t gunu getirisi (gunluk ya da 15:30); Rd: gecmis pencereler icin gunluk."""

    def __init__(self, mm, R=None, btc=None):
        self.mm = mm
        self.Rd = mm.getiri("kk").copy()
        self.R = self.Rd if R is None else R
        self.btc = btc

    def kod(self, k, gunluk=False):
        R = self.Rd if gunluk else self.R
        if k == "BTC16":
            return self.btc.copy()
        return R[k].copy()


def btc16_getiri(mm):
    F = yukle.kripto_1600()["BTC-USD"].reindex(mm.idx)
    return F / F.shift(1) - 1.0           # 16:00 -> 16:00 ET; ABD16 ile es zamanli (guvenli)


def lider_artik(kay, liderler, gunluk=False):
    """Lider sepeti: ham getiri ortalamasi ve artik (lider - beta*SPY) ortalamasi."""
    mm = kay.mm
    spy = kay.kod("SPY", gunluk)
    spy_d = kay.Rd["SPY"]
    ham, art = [], []
    for k in liderler:
        r = kay.kod(k, gunluk)
        rd = kay.btc if k == "BTC16" else kay.Rd[k]
        if k == "BTC16":
            b = rbeta(rd.to_frame("x"), spy_d.to_numpy(), 250)["x"]
        else:
            b = mm.beta("SPY", 250)[k].copy()
        ham.append(r)
        art.append(r - b * spy)
    ham = pd.concat(ham, axis=1).mean(axis=1, skipna=True)
    art = pd.concat(art, axis=1).mean(axis=1, skipna=True)
    return ham, art


def takipci_listesi(mm, takipciler):
    return [k for k in takipciler if k in mm.kpos and mm.sinif.get(k, "ABD16") == "ABD16"]


# ----------------------------------------------------------------------------- sinyal uretecleri
def sinyal_kume_i(kay, kume, W, esik, yon):
    """(i) Liderin artik getirisi z > esik -> takipci sepeti ayni yonde (yon=+1 devam, -1 donus)."""
    _, lid, tak, _, _ = KUMELER[kume]
    mm = kay.mm
    tak = takipci_listesi(mm, tak)
    _, a_b = lider_artik(kay, lid, gunluk=False)
    _, a_g = lider_artik(kay, lid, gunluk=True)
    z = zz(a_b, a_g, W)
    s = (np.sign(z) * (z.abs() > esik)).fillna(0.0) * yon
    S = pd.DataFrame(np.repeat(s.to_numpy()[:, None], len(tak), axis=1), index=mm.idx, columns=tak)
    return S, esit_guc(S, z.abs().to_numpy())


def sinyal_kume_ii(kay, kume, W, esik, yon):
    """(ii) Takipcinin lidere gore eksik kalmasi u = r_F - beta_FL*r_L; z_u < -esik -> al (yon=+1 yakalama),
    z_u > esik -> sat; yon=-1 ters (aradaki farkin devami)."""
    _, lid, tak, _, _ = KUMELER[kume]
    mm = kay.mm
    tak = takipci_listesi(mm, tak)
    L_b, _ = lider_artik(kay, lid, gunluk=False)
    L_g, _ = lider_artik(kay, lid, gunluk=True)
    Fg = kay.Rd[tak]
    Fb = kay.R[tak]
    B = rbeta(Fg, L_g.to_numpy(), 250)
    u_g = Fg - B.mul(L_g, axis=0)
    u_b = Fb - B.mul(L_b, axis=0)
    Z = zz(u_b, u_g, W)
    S = (-np.sign(Z) * (Z.abs() > esik)).fillna(0.0) * yon
    return S, esit_guc(S, Z.abs().to_numpy())


def sinyal_spy_esik(kay, hedef, esik, yon):
    """r_SPY,t >= +esik -> hedef al; <= -esik -> sat (yon=+1). yon=-1 ters."""
    r = kay.kod("SPY")
    s = (np.sign(r) * (r.abs() >= esik)).fillna(0.0) * yon
    return s.rename(hedef), None


def sinyal_r2_12(kay, yon):
    """R2-12: SPY <= -%2 -> TLT al; >= +%2 -> TLT sat (yon=+1 = kural)."""
    r = kay.kod("SPY")
    s = (-np.sign(r) * (r.abs() >= 0.02)).fillna(0.0) * yon
    return s.rename("TLT"), None


def _evren_kodlari(mm):
    if "evren_tab" not in mm._c:
        mm._c["evren_tab"] = mm.donem_basi_evreni()
        mm._c["evren_mask"] = mm.evren_maskesi(mm._c["evren_tab"])
    tab, U = mm._c["evren_tab"], mm._c["evren_mask"]
    kods = sorted(k for k in mm.kodlar if str(mm.evren.at[k, "tur"]) == "hisse")   # sabit sutun kumesi
    return kods, U[kods].to_numpy()


def r4_01_skor(kay, W):
    """Cartea tipi lider skoru (yaklasik): x~ = r / sigma20; m = evren ort. x~;
    lider = corr(x~_{s-1}, m_s) - corr(m_{s-1}, x~_s), pencere t-1'de biter."""
    mm = kay.mm
    key = ("k1_r401", W)
    if key in mm._c:
        return mm._c[key]
    kods, U = _evren_kodlari(mm)
    Rd = kay.Rd[kods]
    sg = mm.sigma20()[kods]
    X = (Rd / sg.where(sg > 0)).where(U)
    mser = X.mean(axis=1, skipna=True)
    lead = rcorr_lag(X.shift(1), mser.to_numpy(), W)
    follow = rcorr_lag(X, mser.shift(1).to_numpy(), W)
    net = (lead - follow).where(U)
    mm._c[key] = (kods, net)
    return kods, net


def sinyal_r4_01(kay, W, yon, buyuk=None):
    """R4-01 (buyuk=None) / R4-02 (buyuk=k: |lider sepeti r| > k x 60g sigma)."""
    mm = kay.mm
    kods, net = r4_01_skor(kay, W)
    N = net.to_numpy()
    rk = pd.DataFrame(N).rank(axis=1, pct=True).to_numpy()
    lider = rk >= 0.8
    takip = rk <= 0.2
    Rb = kay.R[kods].to_numpy()
    Rg = kay.Rd[kods].to_numpy()
    with np.errstate(invalid="ignore"):
        LR_b = np.nanmean(np.where(lider, Rb, NAN), axis=1)
        LR_g = np.nanmean(np.where(lider, Rg, NAN), axis=1)
    s = np.sign(np.nan_to_num(LR_b))
    if buyuk is not None:
        sd = pd.Series(LR_g).rolling(60, min_periods=30).std().shift(1).to_numpy()
        s = s * (np.abs(np.nan_to_num(LR_b)) > buyuk * np.nan_to_num(sd, nan=np.inf))
    S = np.where(takip, s[:, None] * yon, 0.0)
    S = pd.DataFrame(S, index=mm.idx, columns=kods)
    G = esit_guc(S, (1.0 - np.nan_to_num(rk)) * np.abs(np.nan_to_num(LR_b))[:, None])
    return S, G


def sinyal_r4_04(kay, yon):
    """R4-04: XLK - SPY > +%1,5 -> en dusuk betali 3 sektor ETF'i al (+SPY korunma); < -%1,5 tersi."""
    mm = kay.mm
    sek = [k for k in SEKTORLER if k != "XLK" and k in mm.kpos]
    d = kay.kod("XLK") - kay.kod("SPY")
    s = (np.sign(d) * (d.abs() > 0.015)).fillna(0.0) * yon
    B = mm.beta("SPY", 250)[sek].to_numpy().copy()
    B[~np.isfinite(B)] = np.inf
    rk = np.argsort(np.argsort(B, axis=1), axis=1) < 3
    ok = np.isfinite(mm.beta("SPY", 250)[sek].to_numpy())
    S = pd.DataFrame(np.where(rk & ok, s.to_numpy()[:, None], 0.0), index=mm.idx, columns=sek)
    return S, esit_guc(S, d.abs().to_numpy())


def sinyal_r4_05(kay, alfa=1.0):
    """R4-05: 250 gunluk ridge VAR(1) (11 SPDR sektor ETF'i); tahmini en yuksek 3 al, en dusuk 3 sat.
    lambda = alfa x ortalama ozdeger (tr(X'X)/k); tek deger, arama yok. Pencere: (r_{s-1}, r_s), s <= t."""
    mm = kay.mm
    sek = [k for k in SEKTORLER if k in mm.kpos]
    key = ("k1_r405", alfa)
    Rd = kay.Rd[sek].to_numpy()
    Rb = kay.R[sek].to_numpy()
    if key not in mm._c:
        T, k = Rd.shape
        Bs = [None] * T
        for t in range(251, T):
            Y = Rd[t - 249:t + 1]
            X = Rd[t - 250:t]
            ok = np.isfinite(Y).all(axis=0) & np.isfinite(X).all(axis=0)
            if ok.sum() < 6:
                continue
            Xo, Yo = X[:, ok], Y[:, ok]
            mx, my = Xo.mean(0), Yo.mean(0)
            Xc, Yc = Xo - mx, Yo - my
            XtX = Xc.T @ Xc
            lam = alfa * np.trace(XtX) / ok.sum()
            Bm = np.linalg.solve(XtX + lam * np.eye(ok.sum()), Xc.T @ Yc)
            Bs[t] = (ok, mx, my, Bm)
        mm._c[key] = Bs
    Bs = mm._c[key]
    T = len(Bs)
    S = np.zeros((T, len(sek)))
    G = np.zeros((T, len(sek)))
    for t in range(T):
        if Bs[t] is None:
            continue
        ok, mx, my, Bm = Bs[t]
        x = Rb[t, ok]
        if not np.isfinite(x).all():
            continue
        p = my + (x - mx) @ Bm
        o = np.argsort(p)
        idx = np.where(ok)[0]
        S[t, idx[o[-3:]]] = 1.0
        S[t, idx[o[:3]]] = -1.0
        G[t, idx] = np.abs(p - np.median(p))
    S = pd.DataFrame(S, index=mm.idx, columns=sek)
    return S, esit_guc(S, G)


def sinyal_r4_07(kay, yon):
    """R4-07: her grupta dolar hacmine gore ilk 3 = lider, alt ucte bir = takipci; lider sepeti > +%2 -> takipci al."""
    mm = kay.mm
    ev = mm.evren
    dv = (mm.df("close") * mm.df("volume")).rolling(250, min_periods=125).mean().shift(1)
    S_all, G_all = [], []
    for g in sorted(set(ev["grup"])):
        if not str(g).startswith("h_") or g in R47_DISI:
            continue
        kods = [k for k in ev.index[ev["grup"] == g] if k in mm.kpos and str(ev.at[k, "tur"]) == "hisse"]
        if len(kods) < 6:
            continue
        D = dv[kods].to_numpy()
        n_ok = np.isfinite(D).sum(axis=1)
        rk = pd.DataFrame(D).rank(axis=1, ascending=False).to_numpy()
        lider = rk <= 3
        alt_esik = n_ok - np.floor((n_ok - 3) / 3.0)          # liderler disindakilerin alt ucte biri
        takip = (rk > np.maximum(3, alt_esik)[:, None]) & np.isfinite(D) & (n_ok[:, None] >= 6)
        with np.errstate(invalid="ignore"):
            LR = np.nanmean(np.where(lider, kay.R[kods].to_numpy(), NAN), axis=1)
        s = np.sign(np.nan_to_num(LR)) * (np.abs(np.nan_to_num(LR)) > 0.02) * (n_ok >= 6)
        S = pd.DataFrame(np.where(takip, s[:, None] * yon, 0.0), index=mm.idx, columns=kods)
        S_all.append(S)
        G_all.append(pd.DataFrame(np.repeat(np.abs(np.nan_to_num(LR))[:, None], len(kods), 1),
                                  index=mm.idx, columns=kods))
    S = pd.concat(S_all, axis=1)
    return S, esit_guc(S, pd.concat(G_all, axis=1).to_numpy())


def r4_08_agirlik(kay):
    """Her ay sonu, 252 gunluk pencerede r_i,s = a + b1 r_i,s-1 + b2 r_m,s-1 + b3 r_j,s-1; |t(b3)| > 2 -> j lider
    (isaret b3). Agirliklar bir sonraki islem gununden itibaren gecerli (aylik yeniden kestirim)."""
    mm = kay.mm
    if "k1_r408" in mm._c:
        return mm._c["k1_r408"]
    kods, U = _evren_kodlari(mm)
    R = kay.Rd[kods].to_numpy()
    rm = kay.Rd["SPY"].to_numpy()
    idx = mm.idx
    ay = idx.year * 12 + idx.month
    sonlar = [i for i in range(len(idx) - 1) if ay[i] != ay[i + 1]]
    W_list = []
    for e in sonlar:
        if e < 260:
            continue
        sl = slice(e - 251, e + 1)
        Y = R[sl]
        Xl = R[e - 252:e]
        ml = rm[e - 252:e]
        ok = np.isfinite(Y).all(0) & np.isfinite(Xl).all(0) & U[e]
        if ok.sum() < 20 or not np.isfinite(ml).all():
            continue
        oi = np.where(ok)[0]
        Yo, Xo = Y[:, oi], Xl[:, oi]
        n = Yo.shape[0]
        Wm = np.zeros((len(kods), len(kods)))
        for a, i in enumerate(oi):
            Z = np.column_stack([np.ones(n), Xo[:, a], ml])
            Zp = np.linalg.pinv(Z)
            yt = Yo[:, a] - Z @ (Zp @ Yo[:, a])
            Xt = Xo - Z @ (Zp @ Xo)
            sxx = (Xt * Xt).sum(0)
            b3 = (yt @ Xt) / np.where(sxx > 0, sxx, NAN)
            ssr = (yt @ yt) - b3 ** 2 * sxx
            se = np.sqrt(np.maximum(ssr, 0) / (n - 4) / np.where(sxx > 0, sxx, NAN))
            tt = b3 / se
            tt[a] = 0.0
            sel = np.abs(np.nan_to_num(tt)) > 2
            Wm[i, oi[sel]] = np.sign(b3[sel])
        W_list.append((e, Wm))
    mm._c["k1_r408"] = (kods, W_list)
    return kods, W_list


def sinyal_r4_08(kay, yon=1.0):
    mm = kay.mm
    kods, W_list = r4_08_agirlik(kay)
    _, U = _evren_kodlari(mm)
    Rb = kay.R[kods]
    Rg = kay.Rd[kods]
    A5 = ((Rg.shift(1).rolling(4, min_periods=4).sum() + Rb) / 5.0).to_numpy()   # t-4..t, t gunu R'den
    T, N = A5.shape
    SC = np.full((T, N), NAN)
    for q, (e, Wm) in enumerate(W_list):
        bas = e + 1
        son = W_list[q + 1][0] + 1 if q + 1 < len(W_list) else T
        cnt = np.abs(Wm).sum(1)
        A = np.nan_to_num(A5[bas:son])
        V = np.isfinite(A5[bas:son]).astype(float)
        num = A @ Wm.T
        den = V @ np.abs(Wm).T
        with np.errstate(invalid="ignore", divide="ignore"):
            sc = num / den
        sc[:, cnt == 0] = NAN
        SC[bas:son] = sc
    SC = np.where(U, SC, NAN)
    grup = mm.evren.loc[kods, "grup"].astype(str).to_numpy()
    SCd = pd.DataFrame(SC, index=mm.idx, columns=kods)
    for g in set(grup):
        c = [k for k, gg in zip(kods, grup) if gg == g]
        SCd[c] = SCd[c].sub(SCd[c].mean(axis=1), axis=0)       # sektor-notr
    rk = SCd.rank(axis=1, pct=True).to_numpy()
    S = np.where(rk >= 0.9, 1.0, np.where(rk <= 0.1, -1.0, 0.0)) * yon
    S = pd.DataFrame(np.nan_to_num(S), index=mm.idx, columns=kods)
    return S, esit_guc(S, np.abs(np.nan_to_num(rk) - 0.5))


# ----------------------------------------------------------------------------- bilanco olaylari (YONTEM 2)
def bilanco_olaylari(mm):
    """ilk_tepki_gunu d; d-1, d, d+1 icinden hacim / 20 gunluk ortalama orani en yuksek gun d degilse olay atilir.
    Donus: DataFrame (kod, pos, tarih, AR) + ozet."""
    if "k1_bil" in mm._c:
        return mm._c["k1_bil"]
    b = yukle.bilanco()
    b = b[b["ilk_tepki_gunu"].notna()]
    V = mm.df("volume")
    ort20 = V.rolling(20, min_periods=15).mean().shift(1)
    oran = (V / ort20).to_numpy()
    R = mm.getiri("kk", ham=True)
    AR = (R - mm.beta("SPY", 250).mul(R["SPY"], axis=0)).to_numpy()
    sat, atilan, toplam = [], 0, 0
    for k, d in zip(b["kod"], b["ilk_tepki_gunu"]):
        if k not in mm.kpos:
            continue
        p = int(mm.idx.searchsorted(d))
        if p >= len(mm.idx) or mm.idx[p] != d or p < 1 or p + 1 >= len(mm.idx):
            continue
        j = mm.kpos[k]
        toplam += 1
        o = oran[p - 1:p + 2, j]
        if not np.isfinite(o).all() or int(np.argmax(o)) != 1:
            atilan += 1
            continue
        sat.append({"kod": k, "pos": p, "tarih": d, "AR": AR[p, j]})
    E = pd.DataFrame(sat).drop_duplicates(["kod", "pos"]).sort_values("pos").reset_index(drop=True)
    oz = {"olay": toplam, "atilan": atilan, "atilan_oran": atilan / max(toplam, 1)}
    mm._c["k1_bil"] = (E, oz)
    return E, oz


def sinyal_r6_05(kay, yon, h):
    """R6-05: grup (sektor) basina en buyuk 5 (250g dolar hacmi, ceyrek basi); ceyrekte ilk aciklayan = lider.
    Lider R gunu AR >= +%4 -> henuz aciklamamis takipcileri al, <= -%4 sat. Takipcinin tepki gunu <= R+h ise atlanir."""
    mm = kay.mm
    E, _ = bilanco_olaylari(mm)
    dv = (mm.df("close") * mm.df("volume")).rolling(250, min_periods=125).mean().shift(1)
    ev = mm.evren
    q = (mm.idx.year * 4 + (mm.idx.month - 1) // 3).to_numpy()
    olay_kod = set(E["kod"])
    S = pd.DataFrame(0.0, index=mm.idx, columns=sorted(olay_kod))
    G = S.copy()
    Ek = {k: g["pos"].to_numpy() for k, g in E.groupby("kod")}
    for g in R6_GRUPLAR:
        uye = [k for k in ev.index[ev["grup"] == g] if k in olay_kod]
        for qq in np.unique(q):
            pq = np.where(q == qq)[0]
            p0 = pq[0]
            d = dv.iloc[p0][uye].dropna()
            if len(d) < 5:
                continue
            top5 = list(d.sort_values(ascending=False).index[:5])
            ilk = {k: next((p for p in Ek[k] if pq[0] <= p <= pq[-1]), None) for k in top5}
            var = {k: p for k, p in ilk.items() if p is not None}
            if not var:
                continue
            lid = min(var, key=var.get)
            pL = var[lid]
            ar = float(E[(E.kod == lid) & (E.pos == pL)]["AR"].iloc[0])
            if not np.isfinite(ar) or abs(ar) < 0.04:
                continue
            for k in top5:
                if k == lid:
                    continue
                sonraki = [p for p in Ek[k] if p >= pL]
                if sonraki and sonraki[0] <= pL + h:
                    continue                    # takipci tutma suresi icinde aciklıyor (ya da ayni gun)
                S.iat[pL, S.columns.get_loc(k)] = np.sign(ar) * yon
                G.iat[pL, G.columns.get_loc(k)] = abs(ar)
    S = S.loc[:, (S != 0).any()]
    return S, esit_guc(S, G[S.columns].to_numpy())


def sinyal_r6_07(kay, yon):
    """R6-07: NVDA/MU (TSM, ASML'de 8-K yok) R gunu AR >= +%5 -> SMH al (+SPY korunma); JPM -> XLF."""
    mm = kay.mm
    E, _ = bilanco_olaylari(mm)
    S = pd.DataFrame(0.0, index=mm.idx, columns=["SMH", "XLF"])
    G = S.copy()
    for lid, hed in (("NVDA", "SMH"), ("MU", "SMH"), ("JPM", "XLF")):
        for _, r in E[E.kod == lid].iterrows():
            if np.isfinite(r.AR) and abs(r.AR) >= 0.05 and abs(r.AR) > G.iat[r.pos, G.columns.get_loc(hed)]:
                S.iat[r.pos, S.columns.get_loc(hed)] = np.sign(r.AR) * yon
                G.iat[r.pos, G.columns.get_loc(hed)] = abs(r.AR)
    return S, esit_guc(S, G.to_numpy())


def sinyal_r6_08(kay, yon):
    """R6-08: 250g dolar hacminde ilk 10 hisseden biri R gunu |AR| >= %6 ve QQQ ayni yonde >= %1,5 -> QQQ ayni yon."""
    mm = kay.mm
    E, _ = bilanco_olaylari(mm)
    dv = (mm.df("close") * mm.df("volume")).rolling(250, min_periods=125).mean().shift(1)
    kods = sorted(set(E["kod"]) & {k for k in mm.kodlar if str(mm.evren.at[k, "tur"]) == "hisse"})
    rk = dv[kods].rank(axis=1, ascending=False)
    q = kay.kod("QQQ")
    s = pd.Series(0.0, index=mm.idx, name="QQQ")
    best = pd.Series(0.0, index=mm.idx)
    for _, r in E[E.kod.isin(kods)].iterrows():
        if not (rk.iat[r.pos, kods.index(r.kod)] <= 10) or not np.isfinite(r.AR) or abs(r.AR) < 0.06:
            continue
        qq = q.iat[r.pos]
        if np.isfinite(qq) and np.sign(qq) == np.sign(r.AR) and abs(qq) >= 0.015 and abs(r.AR) > best.iat[r.pos]:
            s.iat[r.pos] = np.sign(r.AR) * yon
            best.iat[r.pos] = abs(r.AR)
    return s, None


# ----------------------------------------------------------------------------- varyant listesi
def varyantlar():
    V = []

    def ekle(vid, kural_id, ad, girdi, fn, korunma, hat="ana", tema=False, yayin="", tur="cok"):
        V.append(dict(vid=vid, kural_id=kural_id, ad=ad, girdi=girdi, fn=fn, korunma=korunma, hat=hat,
                      tema=tema, yayin=yayin, tur=tur))

    for kk, (kad, lid, tak, hat, tema) in KUMELER.items():
        hatlar = ["ana", "yeni"] if hat == "ikisi" else [hat]
        for ht in hatlar:
            for W in (60, 250):
                for es in (1.0, 2.0):
                    for yon, yad in ((1, "devam"), (-1, "donus")):
                        ekle(f"A-{kk}-i-W{W}-z{int(es)}-{yad}-{ht}", f"A-{kk}-i", f"{kad}: lider artik z>{es:g} (W{W}) -> takipci {yad}",
                             f"{'+'.join(lid)} - b*SPY (t)", (lambda kay, kk=kk, W=W, es=es, yon=yon: sinyal_kume_i(kay, kk, W, es, yon)),
                             ("SPY:250",), ht, tema)
                        ekle(f"A-{kk}-ii-W{W}-z{int(es)}-{'yakalama' if yon == 1 else 'ayrisma'}-{ht}", f"A-{kk}-ii",
                             f"{kad}: takipci-b*lider z<-{es:g} (W{W}) -> {'yakalama (al)' if yon == 1 else 'ayrisma devam'}",
                             f"takipci - b*{'+'.join(lid)} (t)", (lambda kay, kk=kk, W=W, es=es, yon=yon: sinyal_kume_ii(kay, kk, W, es, yon)),
                             ("SPY:250",), ht, tema)
    for yon, yad in ((1, "kural"), (-1, "ters")):
        for hed in ("HYG", "JNK", "LQD"):
            ekle(f"R2-05-{hed}-{yad}", "R2-05", f"SPY +-%1,5 -> {hed} ayni yon ({yad})", "SPY kk (t)",
                 (lambda kay, hed=hed, yon=yon: sinyal_spy_esik(kay, hed, 0.015, yon)), ("yok", "SPY:250"), yayin="2018", tur="tek")
        ekle(f"R2-12-{yad}", "R2-12", f"SPY +-%2 -> TLT ters yon ({yad})", "SPY kk (t)",
             (lambda kay, yon=yon: sinyal_r2_12(kay, yon)), ("yok",), yayin="2019", tur="tek")
        ekle(f"R4-03-{'devam' if yon == 1 else 'donus'}", "R4-03", f"SPY +-%1 -> IWM {'ayni' if yon == 1 else 'ters'} yon",
             "SPY kk (t)", (lambda kay, yon=yon: sinyal_spy_esik(kay, "IWM", 0.01, yon)), ("yok", "SPY:250"), yayin="2008", tur="tek")
        ekle(f"R4-04-{yad}", "R4-04", f"XLK-SPY +-%1,5 -> dusuk betali 3 sektor ({yad})", "XLK-SPY (t)",
             (lambda kay, yon=yon: sinyal_r4_04(kay, yon)), ("SPY:250",), yayin="2014")
        ekle(f"R4-07-{'devam' if yon == 1 else 'donus'}", "R4-07", f"grup ici buyuk 3 +-%2 -> kucuk ucte bir ({'devam' if yon == 1 else 'donus'})",
             "grup lider sepeti (t)", (lambda kay, yon=yon: sinyal_r4_07(kay, yon)), ("SPY:250",), yayin="2007")
        ekle(f"R6-07-{yad}", "R6-07", f"NVDA/MU/JPM bilanco AR +-%5 -> SMH/XLF ({yad})", "lider R gunu AR",
             (lambda kay, yon=yon: sinyal_r6_07(kay, yon)), ("SPY:250",), yayin="2012")
        ekle(f"R6-08-{yad}", "R6-08", f"ilk 10 bilanco |AR|>=%6 ve QQQ >=%1,5 -> QQQ ({yad})", "lider R gunu AR, QQQ (t)",
             (lambda kay, yon=yon: sinyal_r6_08(kay, yon)), ("yok",), yayin="2012", tur="tek")
        for W in (60, 250):
            ekle(f"R4-01-W{W}-{'devam' if yon == 1 else 'donus'}", "R4-01", f"Cartea lider sepeti isareti -> takipci (W{W}, {'devam' if yon == 1 else 'donus'})",
                 "lider sepeti r (t)", (lambda kay, W=W, yon=yon: sinyal_r4_01(kay, W, yon)), ("SPY:250",), yayin="2022")
            ekle(f"R4-02-W{W}-{'devam' if yon == 1 else 'donus'}", "R4-02", f"R4-01, yalniz |lider r|>1 sigma60 (W{W}, {'devam' if yon == 1 else 'donus'})",
                 "lider sepeti r (t)", (lambda kay, W=W, yon=yon: sinyal_r4_01(kay, W, yon, buyuk=1.0)), ("SPY:250",), yayin="2022")
    ekle("R4-05", "R4-05", "ridge VAR(1) sektor: en iyi 3 al, en kotu 3 sat", "11 sektor ETF r (t)",
         (lambda kay: sinyal_r4_05(kay)), ("yok",), yayin="2014")
    ekle("R4-08", "R4-08", "Granger liderleri 5g ortalama -> takipci ust/alt desil", "lider 5g getiri",
         (lambda kay: sinyal_r4_08(kay)), ("SPY:250",), yayin="2021")
    return V


R6_05 = [(yon, yad) for yon, yad in ((1, "kural"), (-1, "ters"))]

# ----------------------------------------------------------------------------- degerlendirme yardimcilari
def degerlendir_varyant(m, kay, v, donemler, h=(1, 2, 3), gece=True, korunma=None, **kw):
    korunma = korunma or v["korunma"]
    S, G = v["fn"](kay)
    hedef = S.name if isinstance(S, pd.Series) else None
    out = m.degerlendir(S, hedef, kural_id=v["vid"], aile="A", ad=v["ad"], girdi=v["girdi"], h=h, gece=gece,
                        korunma=korunma, guc=G, donemler=donemler,
                        notlar=f"kural={v['kural_id']}; hat={v['hat']}; tema={int(v['tema'])}" + (f"; yayin={v['yayin']}" if v["yayin"] else ""),
                        **kw)
    return out


def r6_05_degerlendir(m, kay, yon, yad, donemler, combos, **kw):
    """R6-05: takipci suzgeci h'ye bagli -> her h ayri sinyal. combos: [(h, cikis)]."""
    parcalar, isl = [], {}
    for h, ck in combos:
        hh = 1 if ck == "acilis" else h
        S, G = sinyal_r6_05(kay, yon, hh)
        r = m.degerlendir(S, None, kural_id=f"R6-05-{yad}", aile="A", ad=f"lider bilanco AR +-%4 -> aciklamamis 4 emsal ({yad})",
                          girdi="lider R gunu AR", h=() if ck == "acilis" else (h,), gece=(ck == "acilis"),
                          korunma=("SPY:250",), guc=G, donemler=donemler, notlar="kural=R6-05; hat=ana; tema=0; yayin=2008", **kw)
        if isinstance(r, tuple):
            r, i = r
            isl.update(i)
        parcalar.append(r)
    out = pd.concat(parcalar, ignore_index=True)
    return (out, isl) if kw.get("islem_dondur") else out


def gecti(r, esik=2.0):
    """Aday / OOS gecis olcutu (ana ajan notu 2-4)."""
    if not (np.isfinite(r.net_bps) and r.net_bps > 0):
        return False
    cok = str(r.hedef).startswith("COK(")
    t = r.t_kume if cok else r.t_olcekli
    if not (np.isfinite(t) and t >= esik):
        return False
    if r.yon in ("uzun", "kisa"):
        if not (np.isfinite(r.anormal_bps) and r.anormal_bps > 0 and np.isfinite(r.t_anormal) and r.t_anormal >= 2):
            return False
    return True


def motor():
    t0 = time.time()
    m = M.Motor()
    btc = btc16_getiri(m)
    kay = Kaynak(m, btc=btc)
    print(f"motor {time.time() - t0:.1f} sn", flush=True)
    return m, kay


# ----------------------------------------------------------------------------- asama 1: IS
def asama_is(kom="hisse"):
    ek_ = "" if kom == "hisse" else "_" + kom
    aday_yol = ADAY_YOL.replace(".csv", ek_ + ".csv")
    m, kay = motor()
    V = varyantlar()
    satir = []
    t0 = time.time()
    for v in V:
        dn = ["IS2"] if v["hat"] == "yeni" else ["IS"]
        r = degerlendir_varyant(m, kay, v, dn, giris=("K",), komisyon=(kom,), rejimler=False)
        r["_vid"] = v["vid"]
        satir.append(r)
    for yon, yad in R6_05:
        r = r6_05_degerlendir(m, kay, yon, yad, ["IS"], [(1, "kapanis"), (2, "kapanis"), (3, "kapanis"), (1, "acilis")],
                              giris=("K",), komisyon=(kom,), rejimler=False)
        r["_vid"] = f"R6-05-{yad}"
        satir.append(r)
    IS = pd.concat(satir, ignore_index=True)
    print(f"IS: {len(IS)} satir, {time.time() - t0:.0f} sn", flush=True)
    IS.to_pickle(os.path.join(ARA, f"is{ek_}.pkl"))
    IS["aday"] = [gecti(r) for r in IS.itertuples()]
    ad = IS[IS["aday"]].copy()
    ad["dogrulama_donemi"] = np.where(ad["donem"] == "IS2", "OOS2", "OOS")
    ad["oos_esik_t"] = np.where(ad["donem"] == "IS2", 3.0, 2.0)
    ad["olcu"] = np.where(ad["hedef"].astype(str).str.startswith("COK("), "t_kume", "t_olcekli")
    ad.drop(columns=["aday"]).to_csv(aday_yol, index=False)
    if kom != "hisse":
        return
    E, oz = bilanco_olaylari(m)
    json.dump({"test_sayisi": int(len(IS)), "aday": int(len(ad)), "bilanco": oz, "bilanco_olay_kalan": int(len(E))},
              open(os.path.join(ARA, "is_ozet.json"), "w"))
    print(f"test={len(IS)} aday={len(ad)} -> {ADAY_YOL}", flush=True)
    print(ad[["kural_id", "hedef", "yon", "h", "cikis", "korunma", "donem", "n_islem", "net_bps", "t_olcekli", "t_kume",
              "anormal_bps", "t_anormal"]].round(2).to_string(index=False), flush=True)


# ----------------------------------------------------------------------------- asama 2: OOS (yalniz adaylar)
def _vbul(V, vid):
    for v in V:
        if v["vid"] == vid:
            return v
    return None


def asama_oos(kom="hisse"):
    ek_ = "" if kom == "hisse" else "_" + kom
    m, kay = motor()
    V = varyantlar()
    ad = pd.read_csv(ADAY_YOL.replace(".csv", ek_ + ".csv"))
    sat = []
    for r in ad.itertuples():
        dn = [r.dogrulama_donemi]
        combo = [(int(r.h), r.cikis)]
        if r.kural_id.startswith("R6-05"):
            yon = 1 if r.kural_id.endswith("kural") else -1
            o = r6_05_degerlendir(m, kay, yon, r.kural_id.split("-")[-1], dn, combo, giris=("K",),
                                  komisyon=(kom,), rejimler=False, bootstrap=True)
        else:
            v = _vbul(V, r.kural_id)
            o = degerlendir_varyant(m, kay, v, dn, h=() if r.cikis == "acilis" else (int(r.h),), gece=(r.cikis == "acilis"),
                                    korunma=(r.korunma,), giris=("K",), komisyon=(kom,), rejimler=False, bootstrap=True)
        o = o[(o.korunma == r.korunma) & (o.cikis == r.cikis) & (o.h == r.h)].copy()
        o["is_net_bps"] = r.net_bps
        o["oos_esik_t"] = r.oos_esik_t
        sat.append(o)
    O = pd.concat(sat, ignore_index=True) if sat else pd.DataFrame(columns=M.SEMA)
    O["oos_gecti"] = [gecti(x, esik=e) for x, e in zip(O.itertuples(), O["oos_esik_t"])] if len(O) else []
    O.to_pickle(os.path.join(ARA, f"oos{ek_}.pkl"))
    if kom != "hisse":
        O["oos_gecti"] = False if not len(O) else O["oos_gecti"]
    print(O[["kural_id", "hedef", "h", "cikis", "korunma", "donem", "n_islem", "is_net_bps", "net_bps", "t_olcekli",
             "t_kume", "t_anormal", "p_bootstrap", "oos_gecti"]].round(3).to_string(index=False), flush=True)


# ----------------------------------------------------------------------------- asama 3: gecenler icin ayrinti + zorunlu ek (R4-03)
def saatlik_kaynak(m, kay):
    """15:30 ET fiyatindan t gunu getirisi (son ~730 gun; diger gunler NaN). Onceki gun gunluk 'close' ile."""
    S = yukle.saatlik()
    a = S["acilis_1530"].reindex(index=m.idx)
    c = m.df("close")
    R = pd.DataFrame(NAN, index=m.idx, columns=m.kodlar)
    ort = [k for k in a.columns if k in R.columns]
    R[ort] = a[ort] / c[ort].shift(1) - 1.0
    return Kaynak(m, R=R, btc=kay.btc)


def asama_detay():
    m, kay = motor()
    V = varyantlar()
    O = pd.read_pickle(os.path.join(ARA, "oos.pkl"))
    gec = O[O["oos_gecti"]] if len(O) else O
    sat, ek = [], {}
    kay15 = saatlik_kaynak(m, kay) if len(gec) else None
    son730 = m.idx >= pd.Timestamp("2023-12-26")
    for r in gec.itertuples():
        yeni = r.donem == "OOS2"
        dn = ["IS2", "OOS2"] if yeni else M.STANDART_DONEMLER
        kor = tuple(dict.fromkeys([r.korunma, "yok", "SPY:250", "SPY:60"]))
        if r.kural_id.startswith("R6-05"):
            yon = 1 if r.kural_id.endswith("kural") else -1
            combos = [(int(r.h), r.cikis)]
            o, isl = r6_05_degerlendir(m, kay, yon, r.kural_id.split("-")[-1], dn, combos, giris=("K", "A", "G"),
                                       bootstrap=True, islem_dondur=True)
        else:
            v = _vbul(V, r.kural_id)
            o, isl = degerlendir_varyant(m, kay, v, dn, korunma=kor, giris=("K", "A", "G"), bootstrap=True, islem_dondur=True)
        sat.append(o)
        # VIX > 30 bolumleri ve 15:30 denemesi (adayin kendi satiri)
        anahtar = ("K", 0 if r.cikis == "acilis" else int(r.h), r.cikis, r.korunma)
        i0 = isl.get(anahtar)
        tab, oz = m.bolum_ozeti(i0, "hisse") if i0 is not None else (None, {})
        bilgi = {"vix30": {k: (float(x) if isinstance(x, (float, np.floating)) else x) for k, x in oz.items()}}
        if not r.kural_id.startswith("R6-05"):
            v = _vbul(V, r.kural_id)
            S_k, G_k = v["fn"](kay)
            S_15, G_15 = v["fn"](kay15)
            hedef = S_k.name if isinstance(S_k, pd.Series) else None
            Sk = (S_k.to_frame() if isinstance(S_k, pd.Series) else S_k).mul(son730.astype(float), axis=0)
            S15 = (S_15.to_frame() if isinstance(S_15, pd.Series) else S_15).fillna(0.0).mul(son730.astype(float), axis=0)
            ak = (Sk != 0).to_numpy()
            a15 = (S15 != 0).to_numpy()
            ayni = ((Sk.to_numpy() == S15.to_numpy()) & ak).sum()
            ik = m.islemler(Sk if hedef is None else Sk[hedef], hedef, giris="K", h=max(int(r.h), 1), cikis=r.cikis,
                            korunma=r.korunma, guc=G_k)
            i15 = m.islemler(S15 if hedef is None else S15[hedef], hedef, giris="K", h=max(int(r.h), 1), cikis=r.cikis,
                             korunma=r.korunma, guc=G_15)
            bilgi["s1530"] = {"kapanis_tetik": int(ak.sum()), "s1530_tetik": int(a15.sum()), "ortak_ayni_yon": int(ayni),
                              "ortusme_orani": float(ayni / max(ak.sum(), 1)),
                              "kapanis_n": int(len(ik)), "kapanis_net_bps": float(ik["net_hisse"].mean() * 1e4) if len(ik) else NAN,
                              "s1530_n": int(len(i15)), "s1530_net_bps": float(i15["net_hisse"].mean() * 1e4) if len(i15) else NAN}
            bilgi["s1530"]["korunan_oran"] = (bilgi["s1530"]["s1530_net_bps"] / bilgi["s1530"]["kapanis_net_bps"]
                                              if bilgi["s1530"]["kapanis_net_bps"] else NAN)
        ek[f"{r.kural_id}|{r.h}|{r.cikis}|{r.korunma}"] = bilgi
    # Zorunlu ek: R4-03 SPY -> IWM, iki yon, 2008 oncesi / sonrasi
    for yad in ("devam", "donus"):
        v = _vbul(V, f"R4-03-{yad}")
        o, isl = degerlendir_varyant(m, kay, v, M.STANDART_DONEMLER, giris=("K", "A"), komisyon=("hisse",), rejimler=False,
                                     islem_dondur=True)
        if not len(gec) or f"R4-03-{yad}" not in set(gec.kural_id):
            sat.append(o)
        for (g, h, ck, kr), d in isl.items():
            if g != "K":
                continue
            t = pd.to_datetime(d["t"])
            for ad_, msk in (("2005-2007", t < "2008-01-01"), ("2008-2019", (t >= "2008-01-01") & (t < "2020-01-01")),
                             ("2020-2026", t >= "2020-01-01")):
                x = d.loc[msk, "net_hisse"]
                ols = d.loc[msk, "olcekli_hisse"].dropna()
                ek.setdefault("R4-03_2008", {})[f"{yad}|h{h}|{ck}|{kr}|{ad_}"] = {
                    "n": int(len(x)), "net_bps": round(float(x.mean() * 1e4), 2) if len(x) else None,
                    "t_olcekli": round(float(ols.mean() / ols.std() * np.sqrt(len(ols))), 2) if len(ols) > 2 else None}
    D = pd.concat(sat, ignore_index=True) if sat else pd.DataFrame(columns=M.SEMA)
    D.to_pickle(os.path.join(ARA, "detay.pkl"))
    json.dump(ek, open(os.path.join(ARA, "detay_ek.json"), "w"), indent=1, default=str)
    print(json.dumps(ek, indent=1, default=str)[:6000], flush=True)


# ----------------------------------------------------------------------------- asama 4: bugun + sonuc dosyasi
def asama_bugun():
    m, kay = motor()
    V = varyantlar()
    IS = pd.read_pickle(os.path.join(ARA, "is.pkl"))
    O = pd.read_pickle(os.path.join(ARA, "oos.pkl"))
    D = pd.read_pickle(os.path.join(ARA, "detay.pkl")) if os.path.exists(os.path.join(ARA, "detay.pkl")) else pd.DataFrame()
    for ek_ in ("_sabit",):
        for ad_ in ("is", "oos"):
            y = os.path.join(ARA, f"{ad_}{ek_}.pkl")
            if os.path.exists(y):
                X = pd.read_pickle(y)
                X = X.drop(columns=[c for c in X.columns if c not in M.SEMA])
                IS = pd.concat([IS, X], ignore_index=True)
    gec = O[O["oos_gecti"]] if len(O) else O
    bugun = {}
    for r in gec.itertuples():
        v = _vbul(V, r.kural_id)
        if v is None:
            continue
        S, _ = v["fn"](kay)
        son = S.iloc[-1]
        bugun[r.kural_id] = {"tarih": str(m.idx[-1].date()),
                             "acik": (son[son != 0].to_dict() if isinstance(son, pd.Series) else float(son))}
    json.dump(bugun, open(os.path.join(ARA, "bugun.json"), "w"), indent=1, default=str)
    # sonuc dosyasi: IS satirlari (hepsi) + OOS aday satirlari + gecenlerin ayrintisi (ve R4-03 eki)
    parca = [IS.drop(columns=[c for c in IS.columns if c not in M.SEMA]),
             O.drop(columns=[c for c in O.columns if c not in M.SEMA])]
    if len(D):
        parca.append(D.drop(columns=[c for c in D.columns if c not in M.SEMA]))
    T = pd.concat(parca, ignore_index=True)
    T = T.drop_duplicates(subset=["kural_id", "hedef", "h", "giris", "cikis", "korunma", "komisyon", "donem", "rejim"], keep="last")
    M.yaz_sonuc(T, SONUC_YOL)
    print(f"{len(T)} satir -> {SONUC_YOL}", flush=True)
    print(json.dumps(bugun, indent=1, default=str), flush=True)


if __name__ == "__main__":
    a = sys.argv[1] if len(sys.argv) > 1 else "hepsi"
    if a == "bakis":
        m, kay = motor()
        for vid in ["A-YI-i-W60-z1-devam-ana", "A-BN-ii-W250-z2-yakalama-ana", "A-KR-i-W60-z1-devam-ana", "R4-01-W60-devam",
                    "R4-02-W250-devam", "R4-04-kural", "R4-05", "R4-07-devam", "R4-08", "R6-07-kural", "R6-08-kural", "R4-03-devam"]:
            v = _vbul(varyantlar(), vid)

            def fn(mm, v=v):
                mm._c.pop("k1_r408", None)
                S, _ = v["fn"](Kaynak(mm, btc=kay.btc))
                return S
            ok, rap = m.bakis_testi(fn)
            print(vid, ok, rap if not ok else "", flush=True)
        sys.exit(0)
    for asama, f in (("is", asama_is), ("oos", asama_oos), ("is_sabit", lambda: asama_is("sabit")),
                     ("oos_sabit", lambda: asama_oos("sabit")), ("detay", asama_detay), ("bugun", asama_bugun)):
        if a in (asama, "hepsi"):
            t0 = time.time()
            f()
            print(f"[{asama}] {time.time() - t0:.0f} sn", flush=True)
