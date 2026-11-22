#!/usr/bin/env python3
"""Çürütücü A: 'VIX yüksekken günün dibine yakın kapanan hisse ETF'ini kapanışta al, 1-2 gün tut' (S1, S2).

Hesaplar bu betikte ortak.py'den BAĞIMSIZ yazıldı (kendi okuyucu, maliyet, HAC, portföy testi); ortak.py yalnız
çapraz kontrol (bölüm 0 ve 6) ve grup listesi için çağrılır. Çıktılar: ek/dogrulama/curutme_a/.
Çalıştırma: python3 kod/curutme_a.py   (5 dakikalık veri ek/dogrulama/curutme_a/5dk/*.json içinde olmalı)
"""
import datetime as dt
import json
import os
import sys
import time

import numpy as np
import pandas as pd

KOD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOD)
KOK = os.path.dirname(KOD)
HAM = os.path.join(KOK, "veri", "ham")
CIK = os.path.join(KOK, "ek", "dogrulama", "curutme_a")
os.makedirs(CIK, exist_ok=True)
T0 = time.time()
SATIR = []
pd.set_option("display.width", 250, "display.max_columns", 40, "display.max_rows", 200)


def yaz(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    SATIR.append(s)


def tablo(df, ad=None, nd=2):
    df = df.round(nd) if isinstance(df, (pd.DataFrame, pd.Series)) else df
    yaz(df.to_string())
    if ad:
        df.to_csv(os.path.join(CIK, ad))


# ---------------------------------------------------------------------------------------------------------------
# Bağımsız altyapı
# ---------------------------------------------------------------------------------------------------------------
_C = {}


def oku(s):
    if s not in _C:
        yol = os.path.join(HAM, s.replace("^", "_idx_").replace("=", "_eq_").replace("/", "_") + ".csv")
        d = pd.read_csv(yol, usecols=["date", "open", "high", "low", "close", "adjclose", "volume"], parse_dates=["date"])
        d = d.set_index("date").sort_index()
        d = d[~d.index.duplicated(keep="last")].apply(pd.to_numeric, errors="coerce")
        _C[s] = d[d["close"] > 0]
    return _C[s]


CAL = oku("SPY").index
CAL = CAL[CAL >= "2005-01-01"]
VIX = oku("^VIX")["close"].reindex(CAL)
DONEM = (("tum", None, None), ("is", None, "2018-12-31"), ("oos", "2019-01-01", None), ("son", "2024-01-01", None))


def _fwd(a, ao, h, giris):
    if giris == "kapanis":
        return a.shift(-h) / a - 1
    if giris == "acilis":
        return a.shift(-h) / ao.shift(-1) - 1
    if giris == "ertesi":
        return a.shift(-h - 1) / a.shift(-1) - 1
    if giris == "gece":
        return ao.shift(-1) / a - 1
    if giris == "gunici":
        return a.shift(-1) / ao.shift(-1) - 1
    raise ValueError(giris)


class Veri:
    def __init__(self, sembs):
        self.cols = list(sembs)
        g = lambda al: pd.DataFrame({s: oku(s)[al].reindex(CAL) for s in self.cols})  # noqa: E731
        self.c, self.hi, self.lo, self.o, self.a, self.v = g("close"), g("high"), g("low"), g("open"), g("adjclose"), g("volume")
        self.ao = self.o * self.a / self.c
        rng = self.hi - self.lo
        self.ibs = ((self.c - self.lo) / rng).where(rng > 0)
        dv = (self.c * self.v).rolling(60, min_periods=20).median().shift(1) / 1e6
        m = pd.DataFrame(20.0, index=CAL, columns=self.cols)
        m[dv >= 20] = 10.0
        m[dv >= 100] = 5.0
        self.cost = m / 1e4
        self.r = self.a.pct_change(fill_method=None)
        self._b = {}

    def beta(self, hs):
        if hs not in self._b:
            rh = oku(hs)["adjclose"].reindex(CAL).pct_change(fill_method=None)
            var = rh.rolling(250, min_periods=120).var()
            self._b[hs] = pd.DataFrame({c: (self.r[c].rolling(250, min_periods=120).cov(rh) / var).shift(1) for c in self.cols})
        return self._b[hs]

    def fwd(self, h, giris="kapanis", hedge=None):
        F = _fwd(self.a, self.ao, h, giris)
        if hedge:
            d = oku(hedge)
            ha = d["adjclose"].reindex(CAL)
            hao = (d["open"] * d["adjclose"] / d["close"]).reindex(CAL)
            F = F - self.beta(hedge).mul(_fwd(ha, hao, h, giris), axis=0)
        return F


def hac_t(z, lag=0):
    z = np.asarray(z, float)
    z = z[~np.isnan(z)]
    n = len(z)
    if n < 10:
        return np.nan
    m = z.mean()
    e = z - m
    v = (e @ e) / n
    for k in range(1, min(lag, n - 1) + 1):
        v += 2 * (e[k:] @ e[:-k]) / n
    return m / np.sqrt(v / n) if v > 0 else np.nan


def genis(maske, cols):
    return pd.DataFrame(np.repeat(np.asarray(maske, bool)[:, None], len(cols), axis=1), index=CAL, columns=cols)


def port(S, F, C, h, bas=None, bit=None, lag=None):
    """Gün bazlı eşit ağırlıklı portföy; sürüklenme hedef bazında, dönem içinde."""
    cols = [c for c in S.columns if c in F.columns]
    S, F, C = S[cols], F[cols], C[cols]
    m = np.ones(len(F), bool)
    if bas is not None:
        m &= F.index >= pd.Timestamp(bas)
    if bit is not None:
        m &= F.index <= pd.Timestamp(bit)
    F, S, C = F.loc[m], S.loc[m], C.loc[m]
    akt = S & F.notna()
    k = akt.sum(axis=1)
    var = k > 0
    if int(var.sum()) < 3:
        return None
    dr = F.mean()
    net = (F - C).where(akt)
    abn = (F - dr - C).where(akt)
    p_net = (net.sum(axis=1) / k).where(var)
    p_abn = (abn.sum(axis=1) / k).where(var)
    lag = h - 1 if lag is None else lag
    return {"n_gun": int(var.sum()), "n_islem": int(akt.values.sum()), "net_bps": p_net.mean() * 1e4, "abn_bps": p_abn.mean() * 1e4,
            "t_net": hac_t(p_net.fillna(0.0).values, lag), "t_abn": hac_t(p_abn.fillna(0.0).values, lag),
            "isabet": float((p_net[var] > 0).mean()), "std_bps": p_net[var].std() * 1e4,
            "p_net": p_net, "p_abn": p_abn, "k": k, "net_islem": net}


def ozet(S, V, h=1, giris="kapanis", hedge=None):
    cols = [c for c in S.columns if c != hedge]
    F, C = V.fwd(h, giris, hedge)[cols], V.cost[cols]
    lag = h - 1 if giris in ("kapanis", "acilis", "ertesi") else 0
    out = {}
    for ad, b, e in DONEM:
        p = port(S[cols], F, C, h, b, e, lag)
        if p is None:
            out.update({f"{ad}_n": 0})
            continue
        if ad == "tum":
            out.update({"n_gun": p["n_gun"], "n_islem": p["n_islem"], "net_bps": p["net_bps"], "abn_bps": p["abn_bps"],
                        "isabet": p["isabet"], "std_bps": p["std_bps"], "t_abn": p["t_abn"]})
        else:
            out.update({f"{ad}_n": p["n_gun"], f"{ad}_abn": p["abn_bps"], f"{ad}_t": p["t_abn"]})
    return out


def bloklar(esik=25, birlestir=0):
    hi = (VIX > esik).fillna(False).values
    bid, gno = np.full(len(hi), np.nan), np.full(len(hi), np.nan)
    e, prev, start = -1, -10 ** 9, None
    for p in np.flatnonzero(hi):
        if p - prev > 1 + birlestir:
            e += 1
            start = p
        bid[p], gno[p], prev = e, p - start, p
    return pd.Series(bid, index=CAL), pd.Series(gno, index=CAL)


def kume_t(x, g):
    x = x.dropna()
    g = g.reindex(x.index)
    m = x.mean()
    s = (x - m).groupby(g).sum()
    G, N = len(s), len(x)
    if G < 3:
        return np.nan, G
    return m / np.sqrt((s ** 2).sum() / N ** 2 * G / (G - 1)), G


def gunluk_pnl(S, V, h):
    cols = list(S.columns)
    r = V.r[cols]
    akt = S & V.fwd(h)[cols].notna()
    k = akt.sum(axis=1)
    w = akt.div(k.where(k > 0), axis=0).fillna(0.0) / h
    pnl = -(w * V.cost[cols]).sum(axis=1)
    for j in range(1, h + 1):
        pnl = pnl + (w.shift(j) * r).sum(axis=1)
    return pnl


def max_dusus(pnl):
    eq = (1 + pnl.fillna(0)).cumprod()
    dd = eq / eq.cummax() - 1
    dip = dd.idxmin()
    return float(dd.min()), eq.loc[:dip].idxmax(), dip, float(eq.iloc[-1] - 1)


SEPET = ["SPY", "QQQ", "XLK", "SMH", "SOXX", "IWM", "IJR", "XBI", "IBB", "EEM", "KRE", "XRT"]
V = Veri(SEPET)
DUSUK = V.ibs.lt(0.2)
V25, V20 = (VIX > 25).fillna(False), (VIX > 20).fillna(False)
S25 = DUSUK & genis(V25, SEPET)
S20 = DUSUK & genis(V20, SEPET)
BLK, GNO = bloklar(25, 0)
EP, EPNO = bloklar(25, 10)

# ---------------------------------------------------------------------------------------------------------------
yaz("=" * 30, "0) S1 yeniden üretim (bağımsız kod) ve ortak.py çapraz kontrolü")
import ortak as O  # noqa: E402

rows = []
for hedef, esik, h, rapor in (("IBB", 25, 2, "238/79.1/2.70/2.59"), ("IJR", 20, 1, "479/37.2/3.26/2.20"), ("EEM", 20, 1, "438/50.0/3.38/2.09"),
                              ("IBB", 20, 2, "446/47.7/2.58/2.23"), ("XBI", 20, 2, "456/64.5/2.15/3.39")):
    s = (S25 if esik == 25 else S20)[[hedef]]
    o = ozet(s, V, h)
    oo = O.donemli_test(s[hedef].astype(float), hedef, h)
    oh = ozet(s, V, h, hedge="SPY")
    rows.append({"hedef": hedef, "esik": esik, "h": h, "rapor n/bps/tIS/tOOS": rapor, "n": o["n_gun"], "abn": o["abn_bps"], "t_is": o["is_t"],
                 "t_oos": o["oos_t"], "ortak_n": oo.get("tum_n"), "ortak_abn": oo.get("tum_anormal_net_bps"), "ortak_tis": oo.get("is_t_anormal"),
                 "ortak_toos": oo.get("oos_t_anormal"), "spyhedge_abn": oh["abn_bps"], "spyhedge_tis": oh["is_t"], "spyhedge_toos": oh["oos_t"]})
tablo(pd.DataFrame(rows), "s1_yeniden_uretim.csv")
rows = []
for e_ in SEPET:
    for h in (1, 2):
        o, oh = ozet(S25[[e_]], V, h), (ozet(S25[[e_]], V, h, hedge="SPY") if e_ != "SPY" else {})
        rows.append({"etf": e_, "h": h, "n": o["n_gun"], "net": o["net_bps"], "abn": o["abn_bps"], "t_is": o.get("is_t"), "t_oos": o.get("oos_t"),
                     "son_abn": o.get("son_abn"), "hedge_abn": oh.get("abn_bps"), "hedge_tis": oh.get("is_t"), "hedge_toos": oh.get("oos_t")})
yaz("-- Sepetteki her ETF, VIX>25 & IBS<0,2 (tek tek):")
tablo(pd.DataFrame(rows), "s1_etf_tek_tek_vix25.csv")

# ---------------------------------------------------------------------------------------------------------------
yaz("=" * 30, "1) Tek bahis: sabit sepet portföyü, VIX>25 & IBS<0,2")
yaz("VIX>25 gün sayısı:", int(V25.sum()), "| kesintisiz blok:", int(BLK.max() + 1), "| birleşik dönem (ara<=10 gün):", int(EP.max() + 1))
P = {}
for h in (1, 2):
    F, C = V.fwd(h)[SEPET], V.cost[SEPET]
    p = port(S25, F, C, h)
    P[h] = p
    o = ozet(S25, V, h)
    yaz(f"\n--- h={h}: gün {p['n_gun']}, işlem {p['n_islem']}, gün başı ort ETF {p['n_islem'] / p['n_gun']:.1f}")
    yaz({k: round(v, 2) for k, v in o.items()})
    sn, sa = p["p_net"].dropna(), p["p_abn"].dropna()
    seri = pd.DataFrame({"net": sn, "abn": sa, "n_etf": p["k"].reindex(sn.index), "vix": VIX.reindex(sn.index), "blok": BLK.reindex(sn.index),
                         "donem": EP.reindex(sn.index), "blok_gun_no": GNO.reindex(sn.index)})
    seri.to_csv(os.path.join(CIK, f"gunluk_seri_h{h}.csv"))
    yt = seri.groupby(seri.index.year).agg(gun=("net", "size"), net_bps=("net", lambda x: x.mean() * 1e4), abn_bps=("abn", lambda x: x.mean() * 1e4),
                                           toplam_net_yuzde=("net", lambda x: x.sum() * 100), isabet=("net", lambda x: (x > 0).mean()),
                                           en_kotu_yuzde=("net", lambda x: x.min() * 100))
    yaz(f"Yıl yıl (h={h}); işlem olan yıl {len(yt)}, pozitif yıl {(yt.net_bps > 0).sum()}, VIX>25 hiç olmayan yıl {len(set(range(2005, 2027)) - set(yt.index))}")
    tablo(yt, f"yil_tablo_h{h}.csv")
    ek = seri.nsmallest(10, "net")[["net", "n_etf", "vix", "blok_gun_no"]].assign(net=lambda d: d.net * 100)
    yaz(f"En kötü 10 sinyal günü (h={h}, sepet net %):")
    tablo(ek, f"en_kotu_10_h{h}.csv")
    q = sn.quantile([0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99]) * 100
    yaz(f"Sepet-gün dağılımı % : ort {sn.mean() * 100:.2f}, medyan {sn.median() * 100:.2f}, std {sn.std() * 100:.2f}, çarpıklık {sn.skew():.2f}, "
        f"isabet {(sn > 0).mean():.3f}, en kötü %5 eşiği {q[0.05]:.2f}, en kötü %5 ort {sn[sn <= sn.quantile(0.05)].mean() * 100:.2f}, min {sn.min() * 100:.2f}, "
        f"maks {sn.max() * 100:.2f}, < -%2 gün payı {(sn < -0.02).mean():.3f}, < -%5 gün payı {(sn < -0.05).mean():.3f}")
    ti = p["net_islem"].stack()
    yaz(f"Tek ETF-işlem dağılımı %: n {len(ti)}, ort {ti.mean() * 100:.2f}, std {ti.std() * 100:.2f}, %5 {ti.quantile(0.05) * 100:.2f}, "
        f"en kötü %5 ort {ti[ti <= ti.quantile(0.05)].mean() * 100:.2f}, min {ti.min() * 100:.2f}, isabet {(ti > 0).mean():.3f}")
    pnl = gunluk_pnl(S25, V, h)
    dd, tepe, dip, top = max_dusus(pnl)
    yaz(f"Günlük MTM (sermaye 1/{h} dilim): toplam getiri {top * 100:.1f}%, en büyük düşüş {dd * 100:.1f}% ({tepe.date()} -> {dip.date()})")
    kay = (sn < 0).astype(int)
    seriuz = kay.groupby((kay != kay.shift()).cumsum()).cumsum().max()
    yaz(f"Art arda en çok kayıp sinyal günü: {int(seriuz)}; en kötü 5 ardışık sinyal günü toplamı {sn.rolling(5).sum().min() * 100:.1f}%, "
        f"en kötü 10 ardışık {sn.rolling(10).sum().min() * 100:.1f}%")
    # bağımsız dönemler ve kümelenmiş t
    for ad, lab in (("kesintisiz blok", BLK), ("birleşik dönem", EP), ("takvim çeyreği", pd.Series(CAL.year * 10 + CAL.quarter, index=CAL))):
        tk, G = kume_t(sa, lab)
        tn, _ = kume_t(sn, lab)
        ep = sn.groupby(lab.reindex(sn.index)).agg(["sum", "mean", "size"])
        epa = sa.groupby(lab.reindex(sa.index)).mean()
        yaz(f"Kümeleme = {ad}: küme {G}, kümelenmiş t(abn) {tk:.2f}, t(net) {tn:.2f}; küme toplamı > 0 oranı {(ep['sum'] > 0).mean():.2f}; "
            f"küme ortalamalarının t'si (her küme 1 oy, abn) {epa.mean() / epa.std() * np.sqrt(len(epa)):.2f}; "
            f"en iyi 5 kümenin toplam kazançtaki payı {ep['sum'].nlargest(5).sum() / ep['sum'].sum():.2f}")
    yaz(f"Saf HAC t (abn, tüm): {p['t_abn']:.2f}; yalnız sinyal günleri üzerinden düz t(net): {sn.mean() / sn.std() * np.sqrt(len(sn)):.2f}")
    if h == 1:
        ep = seri.groupby("blok").agg(bas=("net", lambda x: x.index[0].date()), bit=("net", lambda x: x.index[-1].date()), sinyal_gun=("net", "size"),
                                      toplam_net_yuzde=("net", lambda x: x.sum() * 100), ort_bps=("net", lambda x: x.mean() * 1e4))
        ep.to_csv(os.path.join(CIK, "blok_tablo_h1.csv"))
    # kriz dönemlerinin katkısı
    DN = {"2008-09": ("2008-01-01", "2009-12-31"), "2020": ("2020-01-01", "2020-12-31"), "2022": ("2022-01-01", "2022-12-31"),
          "2025-26": ("2025-01-01", "2026-12-31")}
    rows = []
    hepsi = np.zeros(len(CAL), bool)
    for ad, (b, e) in list(DN.items()) + [("dördü birden", (None, None))]:
        mk = hepsi.copy() if b is None else ((CAL >= b) & (CAL <= e))
        hepsi |= mk
        ic = sn[mk[CAL.get_indexer(sn.index)]]
        px = port(S25 & ~genis(mk, SEPET), F, C, h)
        rows.append({"donem": ad, "gun": len(ic), "ic_net_bps": ic.mean() * 1e4, "ic_abn_bps": sa.reindex(ic.index).mean() * 1e4,
                     "toplam_kazanc_payi": ic.sum() / sn.sum(), "haric_gun": px["n_gun"], "haric_net_bps": px["net_bps"], "haric_abn_bps": px["abn_bps"],
                     "haric_t_abn": px["t_abn"], "haric_isabet": px["isabet"]})
    yaz(f"Dönem katkısı ve tek tek çıkarınca (h={h}):")
    tablo(pd.DataFrame(rows), f"donem_katkisi_h{h}.csv")

# ---------------------------------------------------------------------------------------------------------------
yaz("=" * 30, "2) Kural ne katıyor? (sepet portföyü)")
sd = V.r.rolling(60, min_periods=40).std().shift(1)
Z1 = (V.r / sd).le(-1.5)
HEP = V.a.notna()
SPYD = V.ibs["SPY"].lt(0.2)
KIYAS = {
    "a) VIX>25, her gün hepsini al": HEP & genis(V25, SEPET),
    "b) IBS<0,2 (VIX koşulsuz)": DUSUK,
    "b2) IBS<0,2 & VIX<=25": DUSUK & genis(~V25, SEPET),
    "b3) IBS<0,2 & VIX<=20": DUSUK & genis(~V20, SEPET),
    "b4) IBS<0,2 & VIX 20-25": DUSUK & genis(V20 & ~V25, SEPET),
    "c) VIX>25 & IBS<0,2 [KURAL]": S25,
    "c') VIX>25 & IBS>=0,2 (tümleyen)": V.ibs.ge(0.2) & genis(V25, SEPET),
    "d) VIX>25 & getiri<=-1,5 sigma": Z1 & genis(V25, SEPET),
    "d0) getiri<=-1,5 sigma (VIX koşulsuz)": Z1,
    "e) VIX>25 & IBS<0,15 (sınır hariç)": V.ibs.lt(0.15) & genis(V25, SEPET),
    "e1) VIX>25 & IBS 0,15-0,20 (sınır)": V.ibs.ge(0.15) & V.ibs.lt(0.2) & genis(V25, SEPET),
    "e2) VIX>25 & IBS 0,20-0,25 (sınırın dışı)": V.ibs.ge(0.2) & V.ibs.lt(0.25) & genis(V25, SEPET),
    "e3) VIX>27 & IBS<0,15": V.ibs.lt(0.15) & genis((VIX > 27).fillna(False), SEPET),
    "e4) VIX 25-27 & IBS<0,2": DUSUK & genis(V25 & (VIX <= 27), SEPET),
    "f) VIX>25 & SPY IBS<0,2 günü: hepsini al": HEP & genis(V25 & SPYD, SEPET),
    "f') VIX>25 & SPY IBS>=0,2 günü: hepsini al": HEP & genis(V25 & ~SPYD, SEPET),
    "g) yalnız SPY: VIX>25 & IBS<0,2": S25[["SPY"]],
    "g') yalnız SPY: VIX>25 her gün": (HEP & genis(V25, SEPET))[["SPY"]],
    "h) VIX>20 & IBS<0,2": S20,
    "h') VIX>20 her gün hepsini al": HEP & genis(V20, SEPET),
    "i) VIX>30 & IBS<0,2": DUSUK & genis((VIX > 30).fillna(False), SEPET),
}
rows = []
for ad, S in KIYAS.items():
    for h in (1, 2):
        o = ozet(S, V, h)
        rows.append({"kural": ad, "h": h, **{k: o.get(k) for k in ("n_gun", "net_bps", "abn_bps", "isabet", "t_abn", "is_abn", "is_t", "oos_abn", "oos_t", "son_abn", "son_t")}})
for h in (1, 2):
    o = ozet(S25, V, h, hedge="SPY")
    rows.append({"kural": "c-hedge) KURAL, SPY hedge'li (SPY hariç 11 ETF)", "h": h, **{k: o.get(k) for k in ("n_gun", "net_bps", "abn_bps", "isabet", "t_abn", "is_abn", "is_t", "oos_abn", "oos_t", "son_abn", "son_t")}})
KT = pd.DataFrame(rows)
tablo(KT, "kiyas.csv")
# aynı gün kesit farkı: VIX>25 günlerinde düşük IBS'li ETF'ler eksi diğerleri
for h in (1, 2):
    F = V.fwd(h)[SEPET]
    lo_ = F.where(S25).mean(axis=1)
    hi_ = F.where(V.ibs.ge(0.2) & genis(V25, SEPET)).mean(axis=1)
    fark = (lo_ - hi_).dropna()
    tk, G = kume_t(fark, BLK)
    yaz(f"Aynı gün kesit farkı (düşük IBS - diğerleri), h={h}: gün {len(fark)}, ort {fark.mean() * 1e4:.1f} bps, düz t {fark.mean() / fark.std() * np.sqrt(len(fark)):.2f}, blok kümeli t {tk:.2f}")
# VIX>25 günleri içinde rastgele aynı sayıda ETF-gün (300 tekrar)
rng = np.random.default_rng(7)
for h in (1, 2):
    F, C = V.fwd(h)[SEPET], V.cost[SEPET]
    uyg = (HEP & genis(V25, SEPET) & F.notna()).values
    ger = port(S25, F, C, h)["abn_bps"]
    nn = (S25 & F.notna()).sum().values
    dag = []
    for _ in range(300):
        R = np.zeros_like(uyg)
        for j in range(len(SEPET)):
            ix = np.flatnonzero(uyg[:, j])
            R[rng.choice(ix, size=min(nn[j], len(ix)), replace=False), j] = True
        dag.append(port(pd.DataFrame(R, index=CAL, columns=SEPET), F, C, h)["abn_bps"])
    dag = np.array(dag)
    yaz(f"VIX>25 içinde rastgele gün plasebosu h={h}: gerçek {ger:.1f} bps; plasebo ort {dag.mean():.1f}, %95 {np.quantile(dag, 0.95):.1f}, maks {dag.max():.1f}; p = {(dag >= ger).mean():.3f}")

# ---------------------------------------------------------------------------------------------------------------
yaz("=" * 30, "3) Zamanlama gerçekçiliği")
rows = []
for ad, vv in (("VIX aynı gün (16:15 kapanışı)", VIX), ("VIX 1 gün gecikmeli", VIX.shift(1))):
    for esik in (25, 20):
        S = DUSUK & genis((vv > esik).fillna(False), SEPET)
        for h in (1, 2):
            o = ozet(S, V, h)
            rows.append({"vix": ad, "esik": esik, "h": h, **{k: o.get(k) for k in ("n_gun", "net_bps", "abn_bps", "t_abn", "is_t", "oos_t", "son_abn")}})
tablo(pd.DataFrame(rows), "vix_gecikme.csv")


def oku5(ad):
    with open(os.path.join(CIK, "5dk", ad + ".json")) as f:
        r = json.load(f)["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    ix = pd.to_datetime(r["timestamp"], unit="s", utc=True).tz_convert("America/New_York")
    d = pd.DataFrame({k: q[k] for k in ("open", "high", "low", "close")}, index=ix).astype(float)
    return d.dropna(subset=["close"])


try:
    T930, T1545, T1550, T16 = dt.time(9, 30), dt.time(15, 45), dt.time(15, 50), dt.time(16, 0)
    vd = oku5("_idx_VIX")
    vg = {}
    for gun, g in vd.groupby(vd.index.normalize()):
        t = g.index.time
        a, b = g[(t >= T930) & (t < T1545)], g[(t >= T930) & (t < T16)]
        if len(a) and len(b):
            vg[pd.Timestamp(gun.date())] = (a["close"].iloc[-1], b["close"].iloc[-1])
    rows = []
    for s in ("SPY", "QQQ", "SMH", "IWM", "XBI"):
        d5, gd = oku5(s), oku(s)
        f1 = gd["adjclose"].shift(-1) / gd["adjclose"] - 1
        gibs = (gd["close"] - gd["low"]) / (gd["high"] - gd["low"])
        for gun, g in d5.groupby(d5.index.normalize()):
            t = g.index.time
            ses = g[(t >= T930) & (t < T16)]
            key = pd.Timestamp(gun.date())
            if len(ses) < 60 or ses.index[-1].time() < T1550 or key not in gd.index or key not in vg:
                continue
            a, b = ses[ses.index.time < T1545], ses[ses.index.time < T1550]
            ib = lambda x: (x["close"].iloc[-1] - x["low"].min()) / (x["high"].max() - x["low"].min())  # noqa: E731
            rows.append({"gun": key, "etf": s, "ibs1545": ib(a), "ibs1550": ib(b), "ibs5_kap": ib(ses), "ibs_gunluk": gibs.get(key),
                         "son15": gd["close"][key] / a["close"].iloc[-1] - 1, "son10": gd["close"][key] / b["close"].iloc[-1] - 1,
                         "ileri1": f1.get(key), "vix1545": vg[key][0], "vix1600": vg[key][1], "vix_kap": oku("^VIX")["close"].get(key)})
    Z = pd.DataFrame(rows)
    Z.to_csv(os.path.join(CIK, "zamanlama_5dk.csv"), index=False)
    yaz(f"5 dk veri: {Z.gun.min().date()} - {Z.gun.max().date()}, {Z.gun.nunique()} gün x {Z.etf.nunique()} ETF = {len(Z)} ETF-gün")
    yaz(f"Günlük dosya IBS ile 5 dk'dan kapanış IBS farkı: ort mutlak {np.abs(Z.ibs_gunluk - Z.ibs5_kap).mean():.3f}; sinyal uyumu {((Z.ibs_gunluk < 0.2) == (Z.ibs5_kap < 0.2)).mean():.3f}")
    gunv = Z.drop_duplicates("gun")
    for e_ in (20, 25):
        yaz(f"VIX>{e_}: kapanışta {int((gunv.vix_kap > e_).sum())} gün, 15:45'te {int((gunv.vix1545 > e_).sum())} gün, uyuşmayan {int(((gunv.vix_kap > e_) != (gunv.vix1545 > e_)).sum())} gün; "
            f"16:00 ile 16:15 uyuşmayan {int(((gunv.vix_kap > e_) != (gunv.vix1600 > e_)).sum())} gün")
    yaz(f"VIX 15:45 -> günlük kapanış (16:15) mutlak fark: ort {np.abs(gunv.vix_kap - gunv.vix1545).mean():.2f} puan, maks {np.abs(gunv.vix_kap - gunv.vix1545).max():.2f}")
    rows = []
    for ad, K, E in (("IBS<0,2 (VIX koşulsuz) 15:45", Z.ibs_gunluk < 0.2, Z.ibs1545 < 0.2),
                     ("IBS<0,2 (VIX koşulsuz) 15:50", Z.ibs_gunluk < 0.2, Z.ibs1550 < 0.2),
                     ("IBS<0,2 & VIX>20, 15:45", (Z.ibs_gunluk < 0.2) & (Z.vix_kap > 20), (Z.ibs1545 < 0.2) & (Z.vix1545 > 20)),
                     ("IBS<0,2 & VIX>25, 15:45", (Z.ibs_gunluk < 0.2) & (Z.vix_kap > 25), (Z.ibs1545 < 0.2) & (Z.vix1545 > 25))):
        r_ = {"tanim": ad, "kapanis_sinyali": int(K.sum()), "erken_sinyal": int(E.sum()), "ikisi": int((K & E).sum()),
              "yakalama_orani": (K & E).sum() / max(K.sum(), 1), "isabetli_erken_orani": (K & E).sum() / max(E.sum(), 1)}
        for et, mk in (("ikisi", K & E), ("yalniz_kapanis(kacan)", K & ~E), ("yalniz_erken(yanlis)", E & ~K), ("sinyal_yok", ~K & ~E)):
            r_[f"son15_bps_{et}"] = Z.son15[mk].mean() * 1e4
            r_[f"ileri1_bps_{et}"] = Z.ileri1[mk].mean() * 1e4
        rows.append(r_)
    tablo(pd.DataFrame(rows).T, "zamanlama_ozet.csv")
    sinir = Z[(Z.ibs1545 >= 0.15) & (Z.ibs1545 < 0.25)]
    yaz(f"15:45'te IBS 0,15-0,25 olan ETF-gün: {len(sinir)}; kapanışta sınıfı değişen: {int(((sinir.ibs1545 < 0.2) != (sinir.ibs_gunluk < 0.2)).sum())}")
    yaz(f"15:45'te IBS<0,15 olan {int((Z.ibs1545 < 0.15).sum())} ETF-günün kapanışta IBS<0,2 kalma oranı: {(Z.ibs_gunluk[Z.ibs1545 < 0.15] < 0.2).mean():.3f}")
    yaz(f"Son 15 dk mutlak hareket (bps): ort {np.abs(Z.son15).mean() * 1e4:.1f}; VIX>25 günlerinde {np.abs(Z.son15[Z.vix_kap > 25]).mean() * 1e4:.1f}")
    kk = Z[(Z.ibs_gunluk < 0.2) & (Z.vix_kap > 20)]
    yaz("Kapanış sinyali (VIX>20) günlerinin dökümü:")
    yaz(kk.assign(son15=kk.son15 * 1e4, ileri1=kk.ileri1 * 1e4)[["gun", "etf", "ibs1545", "ibs_gunluk", "vix1545", "vix_kap", "son15", "ileri1"]].round(2).to_string(index=False))
except Exception as ex:  # noqa: BLE001
    yaz("5 dk bölümü çalışmadı:", repr(ex))

# ---------------------------------------------------------------------------------------------------------------
yaz("=" * 30, "4) Giriş ve çıkış seçenekleri (sepet, VIX>25 & IBS<0,2; ayrıca VIX>20)")
rows = []
for ead, S in (("VIX>25", S25), ("VIX>20", S20)):
    for ad, giris, h in (("kapanış -> +1 kapanış", "kapanis", 1), ("kapanış -> +2 kapanış", "kapanis", 2), ("kapanış -> +3 kapanış", "kapanis", 3),
                         ("kapanış -> ertesi açılış (yalnız gece)", "gece", 1), ("ertesi açılış -> ertesi kapanış (gün içi)", "gunici", 1),
                         ("ertesi açılış -> +2 kapanış", "acilis", 2), ("ertesi açılış -> +3 kapanış", "acilis", 3),
                         ("1 gün geç: +1 kapanış -> +2 kapanış", "ertesi", 1), ("1 gün geç: +1 kapanış -> +3 kapanış", "ertesi", 2)):
        o = ozet(S, V, h, giris)
        rows.append({"esik": ead, "secenek": ad, **{k: o.get(k) for k in ("n_gun", "net_bps", "abn_bps", "isabet", "std_bps", "t_abn", "is_t", "oos_t", "son_abn")}})
tablo(pd.DataFrame(rows), "giris_cikis.csv")

# ---------------------------------------------------------------------------------------------------------------
yaz("=" * 30, "5) Tehlike profili")
spy = V.a["SPY"]
UST200 = (spy > spy.rolling(200).mean()).fillna(False)
rows = []
for ad, mk in (("blokun ilk 3 günü", GNO.le(2)), ("blokun 4.+ günü", GNO.ge(3)), ("birleşik dönemin ilk 3 günü", EPNO.le(2)), ("birleşik dönemin 4-10. günü", EPNO.between(3, 9)),
               ("birleşik dönemin 11.+ günü", EPNO.ge(10)), ("SPY > 200g ort", UST200), ("SPY < 200g ort", ~UST200), ("VIX 25-30", VIX.between(25, 30)),
               ("VIX 30-40", (VIX > 30) & (VIX <= 40)), ("VIX > 40", VIX > 40), ("VIX bugün düne göre arttı", VIX > VIX.shift(1)), ("VIX bugün düne göre azaldı", VIX <= VIX.shift(1)),
               ("SPY günlük getiri < -%2", V.r["SPY"] < -0.02), ("SPY günlük getiri >= -%2", V.r["SPY"] >= -0.02),
               ("sepette >= 8 ETF tetikli", S25.sum(axis=1) >= 8), ("sepette 1-3 ETF tetikli", S25.sum(axis=1).between(1, 3))):
    S = S25 & genis(mk.fillna(False), SEPET)
    for h in (1, 2):
        p = port(S, V.fwd(h)[SEPET], V.cost[SEPET], h)
        if p is None:
            continue
        sn = p["p_net"].dropna()
        rows.append({"kosul": ad, "h": h, "gun": p["n_gun"], "net_bps": p["net_bps"], "abn_bps": p["abn_bps"], "t_abn": p["t_abn"], "isabet": p["isabet"],
                     "std_yuzde": sn.std() * 100, "yuzde5": sn.quantile(0.05) * 100, "min_yuzde": sn.min() * 100})
tablo(pd.DataFrame(rows), "tehlike.csv")
L = Veri(["QQQ", "TQQQ", "SOXX", "SOXL"])
rows = []
for taban, kal in (("QQQ", "TQQQ"), ("SOXX", "SOXL")):
    for h in (1, 2):
        fk, ft = L.fwd(h)[kal], L.fwd(h)[taban]
        r3 = 3 * L.r[taban]
        f3 = sum(np.log1p(r3.shift(-j)) for j in range(1, h + 1)).pipe(np.expm1)
        sig = L.ibs[taban].lt(0.2) & V25 & fk.notna() & ft.notna()
        a, b, c3 = fk[sig], ft[sig], f3[sig]
        mal = L.cost[kal].clip(lower=0.001)[sig]
        rows.append({"taban": taban, "kaldiracli": kal, "h": h, "n": int(sig.sum()), "ilk": a.index[0].date(), "taban_ort_yuzde": b.mean() * 100,
                     "3x_taban_ort_yuzde": c3.mean() * 100, "gercek_ort_yuzde": a.mean() * 100, "fark_bps(gercek-3x)": (a - c3).mean() * 1e4,
                     "fark_t": (a - c3).mean() / (a - c3).std() * np.sqrt(len(a)), "gercek_net_yuzde": (a - mal).mean() * 100, "std_yuzde": a.std() * 100,
                     "isabet": (a > 0).mean(), "yuzde5": a.quantile(0.05) * 100, "min_yuzde": a.min() * 100, "taban_min_yuzde": b.min() * 100})
yaz("Kaldıraçlı uygulama (aynı sinyal günleri, 2010'dan beri):")
tablo(pd.DataFrame(rows), "kaldirac.csv")

# ---------------------------------------------------------------------------------------------------------------
yaz("=" * 30, "6) Yarıiletken grubu (S2): hayatta kalma yanlılığı")
GRP = [s for s in O.grup("h_yariiletken") if os.path.exists(os.path.join(HAM, s + ".csv"))]
G = Veri(GRP)
ilk = pd.Series({s: oku(s).index[0] for s in GRP})
yaz(f"Grup: {len(GRP)} hisse; verisi 2005 öncesi başlayan {(ilk < '2005-01-01').sum()}, 2010 öncesi {(ilk < '2010-01-01').sum()}, 2015 sonrası başlayan {(ilk >= '2015-01-01').sum()}")
yaz("Yıla göre verisi olan hisse sayısı:", {y: int(G.a.loc[str(y)].notna().any().sum()) for y in (2005, 2008, 2010, 2015, 2020, 2022, 2026)})
E2 = Veri(["SMH", "SOXX"])
rows = []
for esik, h in ((25, 1), (20, 1), (20, 2)):
    vm = V25 if esik == 25 else V20
    Sg = G.ibs.lt(0.2) & genis(vm, GRP)
    oo = O.havuz_donemli(Sg.astype(float), h)
    yaz(f"ortak.py çapraz kontrol VIX>{esik} h{h}: gün {oo.get('tum_n_gun')}, abn {oo.get('tum_anormal_net_bps')}, t IS {oo.get('is_t_anormal')}, t OOS {oo.get('oos_t_anormal')}")
    eski, cok_eski = list(ilk[ilk < "2010-01-01"].index), list(ilk[ilk < "2005-01-01"].index)
    sm = G.ibs.lt(0.2).any(axis=1) & vm
    for ad, S, VV, kw in (("grup (tümü)", Sg, G, {}), ("grup: yalnız 2010 öncesi başlayanlar", Sg[eski], G, {}), ("grup: yalnız 2005 öncesi başlayanlar", Sg[cok_eski], G, {}),
                          ("grup, SPY hedge", Sg, G, {"hedge": "SPY"}), ("grup, SMH hedge (hisseye özgü pay)", Sg, G, {"hedge": "SMH"}),
                          ("grup koşulu: VIX>eşik her gün bütün hisseler", G.a.notna() & genis(vm, GRP), G, {}),
                          ("grup, ertesi açılış girişi", Sg, G, {"giris": "acilis"}), ("grup, yalnız gece", Sg, G, {"giris": "gece"}),
                          ("SMH (kendi IBS'i)", E2.ibs[["SMH"]].lt(0.2) & genis(vm, ["SMH"]), E2, {}), ("SMH, SPY hedge", E2.ibs[["SMH"]].lt(0.2) & genis(vm, ["SMH"]), E2, {"hedge": "SPY"}),
                          ("SOXX (kendi IBS'i)", E2.ibs[["SOXX"]].lt(0.2) & genis(vm, ["SOXX"]), E2, {}), ("SOXX, SPY hedge", E2.ibs[["SOXX"]].lt(0.2) & genis(vm, ["SOXX"]), E2, {"hedge": "SPY"}),
                          ("SMH: grup sinyal günlerinin hepsinde al", pd.DataFrame({"SMH": sm}), E2, {}),
                          ("SMH+SOXX, SPY hedge, ertesi açılış", E2.ibs.lt(0.2) & genis(vm, ["SMH", "SOXX"]), E2, {"hedge": "SPY", "giris": "acilis"})):
        hh = 1 if kw.get("giris") == "gece" else h
        o = ozet(S, VV, hh, kw.get("giris", "kapanis"), kw.get("hedge"))
        rows.append({"esik": esik, "h": h, "test": ad, **{k: o.get(k) for k in ("n_gun", "n_islem", "net_bps", "abn_bps", "isabet", "t_abn", "is_abn", "is_t", "oos_abn", "oos_t", "son_abn", "son_t")}})
tablo(pd.DataFrame(rows), "yariiletken.csv")

# ---------------------------------------------------------------------------------------------------------------
yaz("=" * 30, "7) Bugünkü durum (Kasım 2026)")
yaz("VIX son 15 gün:", VIX.tail(15).round(1).to_dict())
rows = []
f1, f2 = V.fwd(1)[SEPET] - V.cost[SEPET], V.fwd(2)[SEPET] - V.cost[SEPET]
for gun in CAL[CAL >= "2026-09-01"]:
    for e_ in SEPET:
        if S20.at[gun, e_]:
            rows.append({"gun": gun.date(), "etf": e_, "vix": VIX[gun], "vix>25": bool(S25.at[gun, e_]), "ibs": V.ibs.at[gun, e_],
                         "h1_net_yuzde": f1.at[gun, e_] * 100, "h2_net_yuzde": f2.at[gun, e_] * 100})
K = pd.DataFrame(rows)
K.to_csv(os.path.join(CIK, "kasim2026_islemler.csv"), index=False)
if len(K):
    kg = K.groupby(["gun", "vix>25"]).agg(vix=("vix", "first"), n_etf=("etf", "size"), h1_ort=("h1_net_yuzde", "mean"), h2_ort=("h2_net_yuzde", "mean"),
                                          etfler=("etf", lambda x: " ".join(x)))
    yaz("Eylül 2026'dan beri sinyal günleri (VIX>20 dahil; sepet ortalaması, net %):")
    yaz(kg.round(2).to_string())
    k25 = K[K["vix>25"]]
    yaz(f"Yalnız VIX>25: 2026-11 içinde sinyal günü {k25[k25.gun >= dt.date(2026, 11, 1)].gun.nunique()}, ETF-işlem {len(k25[k25.gun >= dt.date(2026, 11, 1)])}; "
        f"sonuçlanan h1 işlemlerin ort {k25.h1_net_yuzde.mean():.2f}% (n {k25.h1_net_yuzde.notna().sum()}), h2 ort {k25.h2_net_yuzde.mean():.2f}% (n {k25.h2_net_yuzde.notna().sum()})")
son = CAL[-1]
yaz(f"{son.date()} kapanışı: VIX {VIX[son]:.1f}; IBS:", V.ibs.loc[son].round(3).to_dict())
yaz("Açık (VIX>25 & IBS<0,2):", [e_ for e_ in SEPET if S25.at[son, e_]])
yaz("2026 yılı sepet serisi (h=1):")
yaz((P[1]["p_net"].dropna().loc["2026"] * 100).round(2).to_string())

yaz(f"\nSüre: {time.time() - T0:.1f} sn")
with open(os.path.join(CIK, "ozet.txt"), "w") as f:
    f.write("\n".join(SATIR) + "\n")
