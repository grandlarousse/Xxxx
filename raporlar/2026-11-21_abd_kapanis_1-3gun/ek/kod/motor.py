# -*- coding: utf-8 -*-
"""motor.py - ortak backtest motoru (YONTEM.md surum 2'ye bagli).

Kullanim (ayrinti MOTOR.md):
    import sys; sys.path.insert(0, "<...>/ek/kod")
    from motor import Motor
    m = Motor()                                   # gercek panel
    r = m.girdi_getiri("SPY")                     # sinyalde kullanilacak guvenli seri
    s = (r <= -0.02).astype(int)                  # {-1,0,+1}, t gunune hizali
    sonuc = m.degerlendir(s, "SPY", kural_id="D001", aile="D", ad="SPY<=-2% al")

Zaman kurali: t satirindaki her sinyal girdisi yalniz t kapanisinda (16:00 ET) bilinen
veriden uretilir. Motorun kendi turettigi her sey (beta, rejim, esik, sigma, maliyet kademesi)
t-1'de biter. Ileri getiriler sinyal gunu t'ye hizalidir.
"""
import math
import os
import sys

import numpy as np
import pandas as pd

KOD_DIZIN = os.path.dirname(os.path.abspath(__file__))
VERI_DIZIN = os.path.join(os.path.dirname(KOD_DIZIN), "veri")

# ----------------------------------------------------------------------------- sabitler
DONEMLER = {
    "STRES": ("2005-01-01", "2009-12-31"),
    "IS": ("2010-01-01", "2019-12-31"),
    "OOS": ("2020-01-01", "2023-12-31"),
    "SON": ("2024-01-01", "2026-11-20"),
}
YENI_YAPI = {"IS2": ("2020-01-01", "2023-12-31"), "OOS2": ("2024-01-01", "2026-11-20")}
# turetilmis donemler: (baslangic, bitis, cikarilacak araliklar)
TUREV_DONEMLER = {
    "IS+OOS": ("2010-01-01", "2023-12-31", []),
    "TUM": ("2005-01-01", "2026-11-20", []),
    "OOS-2020": ("2020-01-01", "2023-12-31", [("2020-01-01", "2020-12-31")]),
    "OOS-2022": ("2020-01-01", "2023-12-31", [("2022-01-01", "2022-12-31")]),
    "OOS-SubNis2020": ("2020-01-01", "2023-12-31", [("2020-02-01", "2020-04-30")]),
}
STANDART_DONEMLER = ["STRES", "IS", "OOS", "SON", "IS+OOS", "TUM",
                     "OOS-2020", "OOS-2022", "OOS-SubNis2020"]
DONEM_BASI = {"IS": "2010-01-01", "OOS": "2020-01-01", "SON": "2024-01-01"}

VIX_KOVA_AD = ["V<20", "V20-30", "V>30"]
REJIMLER = (["hepsi"] + VIX_KOVA_AD + ["UST", "ALT"]
            + [f"{v}|{u}" for v in VIX_KOVA_AD for u in ("UST", "ALT")])

KOMISYONLAR = ("hisse", "sabit", "oransal")
# Ana ajan eki (maliyet duyarliligi): kapanis/acilis muzayedesi emri (MOC/MOO). Emir muzayedenin tek
# fiyatindan dolar; alis-satis farki odenmez. Bacak maliyeti yalniz komisyondur (1,5 $ / 10.000 $ = 1,5 bps),
# hacim kademesi ve VIX carpani uygulanmaz. Varsayilan senaryolara dahil DEGILDIR; yalniz acikca istenirse.
KOMISYON_EK = ("muzayede",)
EMIR_USD = 10_000.0          # YONTEM 8: 10.000 $'lik emir
HISSE_BASI = 0.005           # $ / hisse, en az 1 $
SABIT_EMIR = 1.5             # $ / emir
ORANSAL_BPS = 20.0
YARIM_SENT = 0.005           # 0,5 sent / fiyat tabani
ODUNC_GENEL = 0.005          # yillik
ODUNC_ZOR = 0.10             # yillik, zor odunc alinanlara EK
TEMETTU_KESINTI = 0.30
TEMETTU_ESIK = 3e-4          # adjclose/close oranindaki sicrama bundan kucukse yuvarlama gurultusu
HEDEF_ADV_ALT = 20e6         # 60 gunluk dolar hacmi alt siniri (hedef suzgeci)
MAKS_POZ = 5
BOOT_BLOK, BOOT_TEKRAR, BOOT_TOHUM = 10, 5000, 20261121

# Birlesme oncesi kabuk donemleri: bu tarihten ONCEKI veri silinir (YONTEM 3; tarihler d2_D notundan)
KABUK_KESIM = {"QUBT": "2018-01-01", "MARA": "2014-01-01", "CLSK": "2019-01-01",
               "WULF": "2022-01-01", "KEEL": "2021-01-01", "LEU": "2017-01-01"}

# artik getiri icin varsayilan sektor vekili (yalniz panelde olanlar kullanilir; cagiran degistirebilir)
GRUP_SEKTOR = {"h_yazilim": "XLK", "h_yari_iletken": "SMH", "h_saglik": "XLV", "h_banka": "XLF",
               "h_enerji": "XLE", "h_tuketici": "XLY", "h_sanayi_diger": "XLI", "h_mega": "QQQ",
               "h_elektrik_nukleer": "XLU", "h_uzay_savunma": "XLI", "h_fintech": "XLF",
               "h_maden_metal": "XLB", "h_seyahat": "XLY", "h_ai_altyapi": "XLK",
               "h_kuantum": "XLK", "h_konut": "XLY", "h_gunes": "XLK", "h_ev_cin": "XLY",
               "h_kripto": "XLK", "h_meme": "IWM"}

SEMA = ["kural_id", "aile", "ad", "girdi", "hedef", "yon", "h", "giris", "cikis", "korunma",
        "komisyon", "donem", "rejim", "n_islem", "yillik_islem", "brut_bps", "net_bps",
        "anormal_bps", "isabet", "medyan_bps", "sigma_bps", "net_sigma", "t_olcekli", "t_kume",
        "t_anormal", "p_bootstrap", "p_wilcoxon", "basabas_bps", "en_kotu_bps", "mdd_pct", "yillik_net_pct",
        "en_iyi5suz_bps", "en_iyi_aysiz_bps", "maliyet2x_net_bps", "pozitif_yil_orani",
        "uzun_bps", "kisa_bps", "uzun_n", "kisa_n", "bolum_sayisi", "bolum_pozitif_orani", "notlar"]


# ----------------------------------------------------------------------------- saf yardimcilar
def donem_maskesi(idx, ad):
    """idx (DatetimeIndex) icin donem 'ad'in gun maskesi (bool dizi)."""
    if ad in DONEMLER or ad in YENI_YAPI:
        a, b = (DONEMLER.get(ad) or YENI_YAPI[ad])
        cikar = []
    elif ad in TUREV_DONEMLER:
        a, b, cikar = TUREV_DONEMLER[ad]
    else:
        raise KeyError(f"bilinmeyen donem: {ad}")
    m = np.asarray((idx >= pd.Timestamp(a)) & (idx <= pd.Timestamp(b)))
    for c0, c1 in cikar:
        m &= ~np.asarray((idx >= pd.Timestamp(c0)) & (idx <= pd.Timestamp(c1)))
    return m


def _norm_p2(z):
    return math.erfc(abs(z) / math.sqrt(2.0)) if np.isfinite(z) else np.nan


def wilcoxon_p(x):
    """Wilcoxon isaretli sira testi, iki yanli p (normal yaklasim, bag ve sureklilik duzeltmeli)."""
    x = np.asarray(x, float)
    x = x[np.isfinite(x) & (x != 0)]
    n = x.size
    if n < 10:
        return np.nan
    a = np.abs(x)
    sira = np.argsort(a, kind="mergesort")
    _, ters, say = np.unique(a[sira], return_inverse=True, return_counts=True)
    ust = np.cumsum(say)
    r = np.empty(n)
    r[sira] = (ust - (say - 1) / 2.0)[ters]
    wp = r[x > 0].sum()
    mu = n * (n + 1) / 4.0
    var = n * (n + 1) * (2 * n + 1) / 24.0 - ((say ** 3 - say).sum()) / 48.0
    if var <= 0:
        return np.nan
    d = wp - mu
    z = (d - 0.5 * np.sign(d)) / math.sqrt(var)
    return _norm_p2(z)


def bootstrap_p(x, ort_blok=BOOT_BLOK, tekrar=BOOT_TEKRAR, tohum=BOOT_TOHUM):
    """Duragan blok bootstrap (Politis-Romano) ile H0: ortalama = 0 icin iki yanli p-degeri.
    x: gunluk kar/zarar serisi (sifir gunler dahil). Seri ortalamasi cikarilir, dairesel
    bloklarla (uzunluk ~ Geometrik(1/ort_blok)) yeniden orneklenir; p = (1 + #|ort*| >= |ort|) / (1 + tekrar)."""
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    n = x.size
    if n < 20 or not np.any(x != x[0]):
        return np.nan
    m0 = x.mean()
    xc = x - m0
    cs = np.concatenate([[0.0], np.cumsum(np.concatenate([xc, xc]))])
    rng = np.random.default_rng(tohum)
    p = 1.0 / ort_blok
    K = int(n * p * 1.6 + 60)
    say = 0
    kalan = tekrar
    while kalan > 0:
        B = min(kalan, 1000)
        while True:
            L = rng.geometric(p, size=(B, K))
            np.minimum(L, n, out=L)
            cum = np.cumsum(L, axis=1)
            if cum[:, -1].min() >= n:
                break
            K = int(K * 1.5) + 10
        onceki = cum - L
        Le = np.clip(n - onceki, 0, L)
        s = rng.integers(0, n, size=(B, K))
        mb = (cs[s + Le] - cs[s]).sum(axis=1) / n
        say += int((np.abs(mb) >= abs(m0) - 1e-18).sum())
        kalan -= B
    return (say + 1.0) / (tekrar + 1.0)


def bh(p, q=0.10):
    """Benjamini-Hochberg. p: dizi (NaN'lar test sayisina katilmaz). Donus: (reddet bool, q_deger)."""
    p = np.asarray(p, float)
    iyi = np.isfinite(p)
    red = np.zeros(p.shape, bool)
    qd = np.full(p.shape, np.nan)
    m = int(iyi.sum())
    if m == 0:
        return red, qd
    pi = p[iyi]
    sira = np.argsort(pi, kind="mergesort")
    ps = pi[sira]
    oran = ps * m / np.arange(1, m + 1)
    qs = np.minimum.accumulate(oran[::-1])[::-1]
    qs = np.minimum(qs, 1.0)
    qi = np.empty(m)
    qi[sira] = qs
    qd[iyi] = qi
    red[iyi] = qi <= q
    return red, qd


def mdd(seri):
    """Gunluk getiri serisinin (bilesik) en buyuk dususu, negatif oran olarak."""
    x = np.asarray(seri, float)
    if x.size == 0:
        return np.nan
    eq = np.cumprod(1.0 + np.nan_to_num(x))
    tepe = np.maximum.accumulate(np.maximum(eq, 1.0))
    return float((eq / tepe - 1.0).min())


def genisleyen_esik(seri, q, min_gozlem=250):
    """Genisleyen pencereli yuzdelik esik: t satirindaki deger, serinin YALNIZ t-1'e kadarki
    gozlemlerinin q-yuzdeligidir (q in [0,1]). Series ya da DataFrame."""
    return seri.expanding(min_periods=min_gozlem).quantile(q).shift(1)


def genisleyen_sira(seri, min_gozlem=250):
    """t gunundeki degerin, t-1'e kadarki gecmis dagilimdaki yuzdelik sirasi ([0,1]; gecmiste
    <= olanlarin orani). Series ya da DataFrame."""
    if isinstance(seri, pd.DataFrame):
        return seri.apply(lambda s: genisleyen_sira(s, min_gozlem))
    import bisect
    v = seri.to_numpy(float)
    out = np.full(v.size, np.nan)
    gecmis = []
    for i, a in enumerate(v):
        if np.isfinite(a):
            if len(gecmis) >= min_gozlem:
                out[i] = bisect.bisect_right(gecmis, a) / len(gecmis)
            bisect.insort(gecmis, a)
    return pd.Series(out, index=seri.index, name=seri.name)


def z_skor(seri, pencere, min_gozlem=None):
    """z_t = (x_t - ort(x[t-W..t-1])) / std(x[t-W..t-1]); pencere t-1'de biter (YONTEM 2)."""
    mp = min_gozlem or max(5, pencere // 2)
    o = seri.rolling(pencere, min_periods=mp).mean().shift(1)
    s = seri.rolling(pencere, min_periods=mp).std().shift(1)
    return (seri - o) / s.where(s > 0)


def dairesel_kaydir(X, k=None, rng=None, en_az=40, en_cok=250):
    """Plasebo 2: sinyal matrisini k gun (varsayilan rastgele +40..+250) dairesel kaydirir.
    Donus: (kaydirilmis X, k). X: ndarray ya da DataFrame (indeks korunur)."""
    if k is None:
        rng = rng or np.random.default_rng(0)
        k = int(rng.integers(en_az, en_cok + 1))
    if isinstance(X, (pd.DataFrame, pd.Series)):
        Y = X.copy()
        Y.iloc[:] = np.roll(X.to_numpy(), k, axis=0)
        return Y, k
    return np.roll(np.asarray(X), k, axis=0), k


def tarama_regresyon(X, Y, kontrol_y=None, kontrol_ortak=None, maske=None, hac=0, min_n=250):
    """YONTEM 7 tarama istatistigi, vektorel.
    Her (k, j) cifti icin:  Y[:, j] ~ a + b * X[:, k] + c * kontrol_y[:, j] + d' * kontrol_ortak
      X            : T x K sinyal matrisi (X'in artik getirisi, t gunune hizali)
      Y            : T x N hedef matrisi (Y'nin korunmali ileri getirisi, t gunune hizali)
      kontrol_y    : T x N (Y'nin t gunu getirisi) ya da None
      kontrol_ortak: T ya da T x q (ornegin SPY'nin t gunu getirisi) ya da None
      maske        : T bool (ornegin IS gunleri)
      hac          : Newey-West gecikmesi (h gunluk ortusen hedef icin h-1); 0 = White (HC0)
    NaN'lar cift bazinda disarida birakilir. Donus: (b, t, n) -> K x N DataFrame/ndarray."""
    Xd = X.to_numpy(float) if isinstance(X, pd.DataFrame) else np.asarray(X, float)
    Yd = Y.to_numpy(float) if isinstance(Y, pd.DataFrame) else np.asarray(Y, float)
    if Xd.ndim == 1:
        Xd = Xd[:, None]
    if Yd.ndim == 1:
        Yd = Yd[:, None]
    T, K = Xd.shape
    N = Yd.shape[1]
    Cy = None if kontrol_y is None else (kontrol_y.to_numpy(float) if isinstance(kontrol_y, pd.DataFrame)
                                         else np.asarray(kontrol_y, float).reshape(T, -1))
    Co = None
    if kontrol_ortak is not None:
        Co = np.asarray(kontrol_ortak.to_numpy(float) if hasattr(kontrol_ortak, "to_numpy")
                        else kontrol_ortak, float).reshape(T, -1)
    ms = np.ones(T, bool) if maske is None else np.asarray(maske, bool)
    if Co is not None:
        ms = ms & np.isfinite(Co).all(axis=1)
    B = np.full((K, N), np.nan)
    TS = np.full((K, N), np.nan)
    NN = np.zeros((K, N))
    for j in range(N):
        y = Yd[:, j]
        rows = ms & np.isfinite(y)
        if Cy is not None:
            rows = rows & np.isfinite(Cy[:, j])
        if rows.sum() < min_n:
            continue
        yj = y[rows]
        parca = [np.ones(yj.size)]
        if Cy is not None:
            parca.append(Cy[rows, j])
        if Co is not None:
            parca.extend(Co[rows].T)
        Z = np.column_stack(parca)
        q = Z.shape[1]
        Xj = Xd[rows]
        W = np.isfinite(Xj)
        X0 = np.where(W, Xj, 0.0)
        Wf = W.astype(float)
        n = Wf.sum(axis=0)
        M = np.zeros((K, q + 1, q + 1))
        rhs = np.zeros((K, q + 1))
        M[:, 0, 0] = (X0 * X0).sum(axis=0)
        xz = X0.T @ Z
        M[:, 0, 1:] = xz
        M[:, 1:, 0] = xz
        for a in range(q):
            for b in range(a, q):
                v = Wf.T @ (Z[:, a] * Z[:, b])
                M[:, 1 + a, 1 + b] = v
                M[:, 1 + b, 1 + a] = v
        rhs[:, 0] = X0.T @ yj
        rhs[:, 1:] = Wf.T @ (Z * yj[:, None])
        iyi = (n >= max(min_n, q + 3)) & (M[:, 0, 0] > 0)
        if not iyi.any():
            continue
        Mi = M[iyi]
        try:
            inv = np.linalg.inv(Mi)
        except np.linalg.LinAlgError:
            inv = np.linalg.pinv(Mi)
        th = np.einsum("kab,kb->ka", inv, rhs[iyi])
        Xi = X0[:, iyi]
        Wi = Wf[:, iyi]
        E = (yj[:, None] - Xi * th[:, 0][None, :] - Z @ th[:, 1:].T) * Wi
        G = Xi * inv[:, 0, 0][None, :] + Z @ inv[:, 0, 1:].T
        S = E * G * Wi
        var = (S * S).sum(axis=0)
        for lag in range(1, int(hac) + 1):
            var = var + 2.0 * (1.0 - lag / (hac + 1.0)) * (S[lag:] * S[:-lag]).sum(axis=0)
        ni = n[iyi]
        var = var * ni / np.maximum(ni - (q + 1), 1.0)
        with np.errstate(invalid="ignore", divide="ignore"):
            ts = th[:, 0] / np.sqrt(np.where(var > 0, var, np.nan))
        B[iyi, j] = th[:, 0]
        TS[iyi, j] = ts
        NN[:, j] = n
    if isinstance(X, pd.DataFrame) and isinstance(Y, pd.DataFrame):
        f = lambda a: pd.DataFrame(a, index=X.columns, columns=Y.columns)
        return f(B), f(TS), f(NN)
    return B, TS, NN


def _sema_df(satirlar):
    df = pd.DataFrame(satirlar)
    for c in SEMA:
        if c not in df.columns:
            df[c] = np.nan
    return df[SEMA]


def yaz_sonuc(df, yol, ekle=False):
    """Standart semayla CSV yazar (sutun sirasi SEMA; ekle=True ise dosyanin sonuna ekler)."""
    eksik = [c for c in SEMA if c not in df.columns]
    if eksik:
        raise ValueError(f"semada eksik sutun: {eksik}")
    d = df[SEMA].copy()
    say = d.select_dtypes("number").columns
    d[say] = d[say].round(5)
    var = ekle and os.path.exists(yol)
    d.to_csv(yol, index=False, mode="a" if var else "w", header=not var)
    return yol


def _gun_ofset(giris, h, cikis):
    """(giris gunu ofseti, cikis gunu ofseti, giris fiyati, cikis fiyati, serbest kalma adimi, gun sayisi)."""
    if cikis == "acilis":
        if giris != "K":
            raise ValueError("gece tutma (cikis='acilis') yalniz giris='K' ile")
        return 0, 1, "k", "a", 1, 1
    if cikis != "kapanis":
        raise ValueError("cikis 'kapanis' ya da 'acilis'")
    h = int(h)
    if h < 1:
        raise ValueError("h >= 1")
    if giris == "K":
        return 0, h, "k", "k", h, h
    if giris == "A":
        return 1, h, "a", "k", h, h
    if giris == "G":
        return 1, h + 1, "k", "k", h, h
    raise ValueError("giris K, A ya da G")


def _korunma_coz(korunma):
    """'yok' -> None; 'SPY' -> ('SPY',250); 'SPY:60' -> ('SPY',60)."""
    if korunma in (None, "yok", ""):
        return None
    if ":" in korunma:
        k, w = korunma.rsplit(":", 1)
        return k, int(w)
    return korunma, 250


# ----------------------------------------------------------------------------- motor
class Motor:
    """Panel + onbellek. P verilmezse gercek panel yuklenir (yukle.panel()).
    P: {'open','high','low','close','adjclose','volume': DataFrame (tarih x kod), 'evren': DataFrame}."""

    ALANLAR = ("open", "high", "low", "close", "adjclose", "volume")

    def __init__(self, P=None, kalite_df=None, kabuk_kes=True, temettu_df=None):
        if P is None:
            if KOD_DIZIN not in sys.path:
                sys.path.insert(0, KOD_DIZIN)
            import yukle
            P = yukle.panel()
            if kalite_df is None:
                try:
                    kalite_df = yukle.kalite()
                except Exception:
                    kalite_df = None
            if temettu_df is None:
                try:
                    temettu_df = yukle.temettu()      # ex-date x kod, hisse basina tutar (sabit tablo)
                except Exception:
                    temettu_df = None
        self._kalite = kalite_df
        self._temettu = temettu_df
        self._kabuk_kes = kabuk_kes
        self.idx = pd.DatetimeIndex(P["close"].index)
        self.kodlar = [str(c) for c in P["close"].columns]
        self.kpos = {k: i for i, k in enumerate(self.kodlar)}
        self.T, self.N = len(self.idx), len(self.kodlar)
        ev = P["evren"].copy()
        ev["kod"] = ev["kod"].astype(str)
        ev = ev.set_index("kod").reindex(self.kodlar)
        for c, v in (("tur", "hisse"), ("kapanis_sinifi", "ABD16"), ("grup", ""), ("kaldirac", 1.0)):
            if c not in ev.columns:
                ev[c] = v
            ev[c] = ev[c].fillna(v)
        if "maliyet_bps" not in ev.columns:
            ev["maliyet_bps"] = 1.5
        self.evren = ev
        self.sinif = ev["kapanis_sinifi"].astype(str).to_dict()
        # VIX ailesi (Cboe 16:15 ET): sinif VIX1615, ya da evren notu/kapanis_et bunu gosteriyor
        nt = ev["not"].astype(str) if "not" in ev.columns else pd.Series("", index=ev.index)
        ket = ev["kapanis_et"].astype(str) if "kapanis_et" in ev.columns else pd.Series("", index=ev.index)
        self.vix_ailesi = set(ev.index[(ev["kapanis_sinifi"].astype(str) == "VIX1615")
                                       | nt.str.contains("VIX1615") | (ket == "16:15")])
        self.A = {}
        for a in self.ALANLAR:
            x = P[a].to_numpy(dtype=float, copy=True)
            if a != "volume":
                x[~(x > 0)] = np.nan          # sifir/negatif fiyat (CL=F 2020-04-20) kullanilmaz
            self.A[a] = x
        if kabuk_kes:
            for k, tarih in KABUK_KESIM.items():
                if k in self.kpos:
                    i0 = int(self.idx.searchsorted(pd.Timestamp(tarih)))
                    for a in self.ALANLAR:
                        self.A[a][:i0, self.kpos[k]] = np.nan
        self.A["adjopen"] = self.A["open"] * self.A["adjclose"] / self.A["close"]
        self._gunno = self.idx.values.astype("datetime64[D]").astype(np.int64)
        self._c = {}
        self.notlar = []

    # ------------------------------------------------------------------ temel erisim
    def df(self, alan, ham=False):
        """Alan matrisi (tarih x kod). Varsayilan GUVENLI: SONRA/VIX1615 sutunlari 1 gun gecikmeli
        (girdi() ile ayni). ham=True yalniz hedef fiyati/denetim icindir, sinyalde kullanmayin."""
        if ham:
            return pd.DataFrame(self.A[alan], index=self.idx, columns=self.kodlar)
        return self.girdi(self.kodlar, alan)

    def _kodlar(self, kod):
        tek = isinstance(kod, str)
        ks = [kod] if tek else list(kod)
        for k in ks:
            if k not in self.kpos:
                raise KeyError(f"panelde yok: {k}")
        return tek, ks

    def girdi(self, kod, alan="adjclose", sizintili=False):
        """GUVENLI sinyal girdisi: t satiri, t gunu 16:00 ET'de bilinen degerdir.
        kapanis_sinifi SONRA ve VIX1615 olan kodlar 1 islem gunu gecikmeli doner.
        sizintili=True yalniz VIX ailesinde (16:15 ET; ayni gun ^VIX, 'sizintili ust sinir' satiri
        icin) kabul edilir; diger SONRA kodlarinda hata verir."""
        tek, ks = self._kodlar(kod)
        out = {}
        for k in ks:
            s = self.A[alan][:, self.kpos[k]]
            sn = self.sinif.get(k, "ABD16")
            if sn in ("SONRA", "VIX1615"):
                if sizintili:
                    if k not in self.vix_ailesi:
                        raise ValueError(f"{k}: SONRA sinifi ayni gun kullanilamaz (sizintili yalniz VIX ailesi)")
                    s = s.copy()
                else:
                    s = np.concatenate([[np.nan], s[:-1]])
            else:
                s = s.copy()
            out[k] = s
        d = pd.DataFrame(out, index=self.idx)
        return d[ks[0]] if tek else d

    def girdi_getiri(self, kod, tur="kk", sizintili=False):
        """Guvenli girdi getirisi. tur: 'kk' kapanistan kapanisa, 'gece', 'gunici'.
        SONRA/VIX1615 kodlarinda getirinin kendisi 1 gun gecikmelidir."""
        tek, ks = self._kodlar(kod)
        r = self._gh(tur)[ks]
        gec = [k for k in ks if self.sinif.get(k, "ABD16") in ("SONRA", "VIX1615")]
        if gec:
            if sizintili and any(k not in self.vix_ailesi for k in gec):
                raise ValueError("SONRA sinifi ayni gun kullanilamaz")
            if not sizintili:
                r = r.copy()
                r[gec] = r[gec].shift(1)
        return r[ks[0]] if tek else r

    def getiri(self, tur="kk", ham=False):
        """Getiri matrisi (tarih x kod), ileri doldurmasiz. 'kk': adjclose_t/adjclose_{t-1}-1;
        'gece': adjopen_t/adjclose_{t-1}-1; 'gunici': adjclose_t/adjopen_t-1.
        Varsayilan GUVENLI: SONRA/VIX1615 sutunlari 1 gun gecikmeli (girdi_getiri ile ayni).
        ham=True: gecikmesiz (yalniz hedef getirisi/denetim icin; sinyalde kullanmayin)."""
        if ham:
            return self._gh(tur)
        key = ("getiri_guvenli", tur)
        if key not in self._c:
            self._c[key] = self.girdi_getiri(self.kodlar, tur)
        return self._c[key]

    def _gh(self, tur="kk"):
        """HAM getiri matrisi (ic kullanim)."""
        key = ("getiri", tur)
        if key not in self._c:
            ac, ao = self.A["adjclose"], self.A["adjopen"]
            onc = np.vstack([np.full((1, self.N), np.nan), ac[:-1]])
            with np.errstate(invalid="ignore", divide="ignore"):
                if tur == "kk":
                    r = ac / onc - 1.0
                elif tur == "gece":
                    r = ao / onc - 1.0
                elif tur == "gunici":
                    r = ac / ao - 1.0
                else:
                    raise ValueError("tur: kk, gece, gunici")
            self._c[key] = pd.DataFrame(r, index=self.idx, columns=self.kodlar)
        return self._c[key]

    # ------------------------------------------------------------------ ileri getiri
    def _ileri_np(self, giris, h, cikis, kp):
        ac, ao = self.A["adjclose"][:, kp], self.A["adjopen"][:, kp]

        def ileri_al(x, k):
            if k == 0:
                return x
            y = np.full_like(x, np.nan)
            y[:-k] = x[k:]
            return y
        go, co, gf, cf, _, _ = _gun_ofset(giris, h, cikis)
        payda = ileri_al(ac if gf == "k" else ao, go)
        pay = ileri_al(ac if cf == "k" else ao, co)
        with np.errstate(invalid="ignore", divide="ignore"):
            return pay / payda - 1.0

    def ileri(self, giris="K", h=1, cikis="kapanis", kodlar=None):
        """Ileri getiri, SINYAL GUNU t'ye hizali (tarih x kod).
        K: adjclose[t+h]/adjclose[t]-1; A: adjclose[t+h]/adjopen[t+1]-1;
        G: adjclose[t+1+h]/adjclose[t+1]-1 (bir gun gecikmeli giris, h gun tutma);
        cikis='acilis' (yalniz K): adjopen[t+1]/adjclose[t]-1 (gece tutma)."""
        ks = self.kodlar if kodlar is None else self._kodlar(kodlar)[1]
        kp = np.array([self.kpos[k] for k in ks])
        return pd.DataFrame(self._ileri_np(giris, h, cikis, kp), index=self.idx, columns=ks)

    def beta(self, piyasa="SPY", pencere=250):
        """Kayan beta (tarih x kod): t satiri yalniz [t-pencere, t-1] gunluk kk getirilerini kullanir.
        En az pencere/2 ortak gozlem; yoksa NaN."""
        key = ("beta", piyasa, pencere)
        if key not in self._c:
            r = self._gh("kk").to_numpy()
            x = r[:, self.kpos[piyasa]]
            v = np.isfinite(r) & np.isfinite(x)[:, None]
            y0 = np.where(v, r, 0.0)
            x0 = np.where(v, x[:, None], 0.0)

            def rs(a):
                return pd.DataFrame(a).rolling(pencere, min_periods=1).sum().to_numpy()
            n = rs(v.astype(float))
            sx, sy, sxy, sxx = rs(x0), rs(y0), rs(x0 * y0), rs(x0 * x0)
            with np.errstate(invalid="ignore", divide="ignore"):
                cov = sxy - sx * sy / n
                var = sxx - sx * sx / n
                b = cov / var
            b[(n < max(pencere // 2, 20)) | ~(var > 1e-14)] = np.nan
            b = np.vstack([np.full((1, self.N), np.nan), b[:-1]])       # t-1'de biter
            self._c[key] = pd.DataFrame(b, index=self.idx, columns=self.kodlar)
        return self._c[key]

    def ileri_korunmali(self, giris="K", h=1, cikis="kapanis", piyasa="SPY", pencere=250, kodlar=None):
        """Korunmali ileri getiri: r_Y - beta_t * r_M (ayni giris/cikis; beta t-1'e kadar)."""
        ks = self.kodlar if kodlar is None else self._kodlar(kodlar)[1]
        f = self.ileri(giris, h, cikis, ks)
        fm = self._ileri_np(giris, h, cikis, np.array([self.kpos[piyasa]]))[:, 0]
        b = self.beta(piyasa, pencere)[ks].to_numpy()
        return f - b * fm[:, None]

    def sigma20(self):
        """Gunluk kk getirinin 20 gunluk standart sapmasi, t-1'de biter (tarih x kod)."""
        if "sigma20" not in self._c:
            self._c["sigma20"] = self._gh("kk").rolling(20, min_periods=20).std().shift(1)
        return self._c["sigma20"]

    def artik_getiri(self, kodlar, piyasa="SPY", sektor="oto", pencere=250, guvenli=True):
        """X'in artik getirisi: r_X,t - b1*r_piyasa,t - b2*r_sektor,t; b'ler [t-pencere, t-1]
        penceresinden (iki degiskenli kayan regresyon). sektor: 'oto' (GRUP_SEKTOR), None ya da
        {kod: sektor_kodu}. Sektor serisi yoksa tek faktore duser. guvenli=True ise SONRA/VIX1615
        kodlarinin artigi 1 gun gecikmeli doner."""
        tek, ks = self._kodlar(kodlar)
        R = self._gh("kk")
        rm = R[piyasa].to_numpy()
        B1 = self.beta(piyasa, pencere)
        if sektor == "oto":
            sektor = {k: GRUP_SEKTOR.get(str(self.evren.at[k, "grup"])) for k in ks}
        sektor = sektor or {}
        out = {}
        mp = max(pencere // 2, 20)
        for k in ks:
            rx = R[k].to_numpy()
            s = sektor.get(k)
            art = rx - B1[k].to_numpy() * rm
            if k == piyasa:
                art = rx.copy()
            if s and s in self.kpos and s not in (k, piyasa):
                rsk = R[s].to_numpy()
                v = np.isfinite(rx) & np.isfinite(rm) & np.isfinite(rsk)
                d = pd.DataFrame({"y": np.where(v, rx, 0.0), "a": np.where(v, rm, 0.0),
                                  "b": np.where(v, rsk, 0.0), "n": v.astype(float)})
                for p, q in (("y", "a"), ("y", "b"), ("a", "a"), ("b", "b"), ("a", "b")):
                    d[p + q] = d[p] * d[q]
                S = d.rolling(pencere, min_periods=1).sum().shift(1)
                n = S["n"]
                caa = S["aa"] - S["a"] ** 2 / n
                cbb = S["bb"] - S["b"] ** 2 / n
                cab = S["ab"] - S["a"] * S["b"] / n
                cya = S["ya"] - S["y"] * S["a"] / n
                cyb = S["yb"] - S["y"] * S["b"] / n
                det = caa * cbb - cab ** 2
                tamam = ((n >= mp) & (det > 1e-18 * 1.0) & (det > 1e-6 * caa * cbb)).to_numpy()
                with np.errstate(invalid="ignore", divide="ignore"):
                    b1 = ((cya * cbb - cyb * cab) / det).to_numpy()
                    b2 = ((cyb * caa - cya * cab) / det).to_numpy()
                with np.errstate(invalid="ignore"):
                    iki = rx - b1 * rm - b2 * rsk
                art = np.where(tamam & np.isfinite(iki), iki, art)
            if guvenli and self.sinif.get(k, "ABD16") in ("SONRA", "VIX1615"):
                art = np.concatenate([[np.nan], art[:-1]])
            out[k] = art
        d = pd.DataFrame(out, index=self.idx)
        return d[ks[0]] if tek else d

    # ------------------------------------------------------------------ rejim
    def rejim(self, vix="^VIX", spy="SPY"):
        """Rejim tablosu (tarih indeksli), hepsi t-1 bilgisiyle:
        vix_1 = VIX(t-1); kova_no 0/1/2 (<20, 20-30 [uclar dahil], >30; yoksa -1); vix_kova (ad);
        ust200 = SPY(t-1) kapanisi > t-1'de biten 200 gunluk ortalama (1/0; bilinmiyorsa -1);
        rejim = 'V<20|UST' gibi; bolum = VIX(t-1) > 30 gunlerinin bolum kimligi (1,2,...; degilse 0).
        Bolum: iki VIX>30 gunu arasinda 20'den az VIX<=30 gunu varsa ayni bolum."""
        key = ("rejim", vix, spy)
        if key in self._c:
            return self._c[key]
        if vix in self.kpos:
            v1 = np.concatenate([[np.nan], self.A["close"][:-1, self.kpos[vix]]])
        else:
            v1 = np.full(self.T, np.nan)
            self.notlar.append("VIX serisi yok: rejim tanimsiz")
        kova = np.where(v1 > 30, 2, np.where(v1 >= 20, 1, 0)).astype(int)
        kova[~np.isfinite(v1)] = -1
        if spy in self.kpos:
            c = pd.Series(self.A["close"][:, self.kpos[spy]])
            ma = c.rolling(200, min_periods=200).mean()
            ust = np.where(ma.notna() & c.notna(), (c > ma).astype(int), -1)
            ust = np.concatenate([[-1], ust[:-1]]).astype(int)
        else:
            ust = np.full(self.T, -1)
        bolum = np.zeros(self.T, int)
        son, no = -10 ** 9, 0
        for i in np.flatnonzero(kova == 2):
            if i - son - 1 >= 20:
                no += 1
            bolum[i] = no
            son = i
        kova_ad = np.array(VIX_KOVA_AD + ["?"], dtype=object)[kova]
        ust_ad = np.array(["ALT", "UST", "?"], dtype=object)[ust]
        d = pd.DataFrame({"vix_1": v1, "kova_no": kova, "vix_kova": kova_ad, "ust200": ust,
                          "rejim": [f"{a}|{b}" for a, b in zip(kova_ad, ust_ad)], "bolum": bolum},
                         index=self.idx)
        self._c[key] = d
        return d

    # ------------------------------------------------------------------ hacim, maliyet parcalari
    def adv60(self):
        """60 gunluk ortalama dolar hacmi, t-1'de biter (tarih x kod, ndarray). Kriptoda hacim zaten USD."""
        if "adv60" not in self._c:
            dv = self.A["close"] * self.A["volume"]
            for k in self.kodlar:
                if str(self.evren.at[k, "tur"]) == "kripto":
                    dv[:, self.kpos[k]] = self.A["volume"][:, self.kpos[k]]
            a = pd.DataFrame(dv).rolling(60, min_periods=60).mean().shift(1).to_numpy()
            self._c["adv60"] = a
        return self._c["adv60"]

    def hedef_uygun(self):
        """Hedef suzgeci (tarih x kod, bool ndarray): kapanis sinifi ABD16, maliyeti tanimli ve
        t-1'e kadarki 60 gunluk dolar hacmi >= 20 milyon $."""
        if "uygun" not in self._c:
            u = self.adv60() >= HEDEF_ADV_ALT
            ok = np.array([(self.sinif.get(k, "ABD16") == "ABD16")
                           and np.isfinite(self.evren.at[k, "maliyet_bps"]) for k in self.kodlar])
            self._c["uygun"] = u & ok[None, :]
        return self._c["uygun"]

    def tarama_hedef_maskesi(self, adv_alt=200e6):
        """Sistematik tarama hedef suzgeci (YONTEM 7.1; tarih x kod bool DataFrame): hedef_uygun,
        t-1'e kadarki 60 gunluk dolar hacmi >= adv_alt ve ilk veri gununden t-1'e kadar hic sifir
        hacimli gun yok (yalniz gecmise bakar)."""
        v = self.A["volume"]
        var = np.isfinite(self.A["close"])
        sifir = np.cumsum(var & ~(v > 0), axis=0)
        sifir = np.vstack([np.zeros((1, self.N), int), sifir[:-1]])
        ms = self.hedef_uygun() & (self.adv60() >= adv_alt) & (sifir == 0)
        return pd.DataFrame(ms, index=self.idx, columns=self.kodlar)

    def kademe(self):
        """Hacim kademesi bps (tarih x kod): t-1'e kadarki 60 gunluk dolar hacmine gore
        >1 mlr: 1,5; 200 mln-1 mlr: 3; 50-200 mln: 7; <50 mln ya da bilinmiyor: 15; kaldiracli/ters +1.
        Muhafazakar: evren.csv'deki (bugunku hacimle hesaplanmis) maliyet_bps'in altina inmez."""
        if "kademe" not in self._c:
            a = self.adv60()
            k = np.full(a.shape, 15.0)
            k[a >= 50e6] = 7.0
            k[a >= 200e6] = 3.0
            k[a > 1e9] = 1.5
            kal = (self.evren["kaldirac"].to_numpy(float) != 1.0).astype(float)
            k = k + kal[None, :]
            st = self.evren["maliyet_bps"].to_numpy(float)
            k = np.maximum(k, st[None, :])          # st NaN ise NaN (islem gormez)
            k[:, ~np.isfinite(st)] = np.nan
            self._c["kademe"] = k
        return self._c["kademe"]

    def _ham_carpan(self):
        """Yahoo close bolunmeye gore duzeltilmis; islem gunundeki GERCEK fiyat = close * carpan.
        Carpan veri_kalite.csv'deki bolunme listesinden (sabit tablo). Tablo yoksa 1."""
        if "carpan" not in self._c:
            f = np.ones((self.T, self.N))
            if self._kalite is not None and "bolunmeler" in self._kalite.columns:
                for kod, b in zip(self._kalite["kod"].astype(str), self._kalite["bolunmeler"]):
                    if kod not in self.kpos or not isinstance(b, str):
                        continue
                    for parca in b.split():
                        try:
                            tarih, pay, payda = parca.split(":")
                            oran = float(pay) / float(payda)
                            i0 = int(self.idx.searchsorted(pd.Timestamp(tarih)))
                        except Exception:
                            continue
                        f[:i0, self.kpos[kod]] *= oran
            else:
                self.notlar.append("bolunme tablosu yok: fiyat tabani bolunme duzeltmeli fiyattan")
            self._c["carpan"] = f
        return self._c["carpan"]

    def ham_fiyat(self, tip="k"):
        """Islem gunundeki gercek (bolunme duzeltmesiz) kapanis ('k') ya da acilis ('a') fiyati."""
        key = ("ham", tip)
        if key not in self._c:
            self._c[key] = self.A["close" if tip == "k" else "open"] * self._ham_carpan()
        return self._c[key]

    def temettu_orani(self):
        """Temettu orani (tarih x kod, ndarray): temettu gunu (ex-date) temettu / onceki kapanis,
        diger gunler 0. Kaynak: yukle.temettu() tablosu (varsa) ile adjclose/close oranindaki
        sicramadan (>= 3 bps) turetilen oranin buyugu; tablo yoksa yalniz ikincisi."""
        if "tem" not in self._c:
            with np.errstate(invalid="ignore", divide="ignore"):
                f = self.A["adjclose"] / self.A["close"]
                d = 1.0 - f[:-1] / f[1:]
            d = np.vstack([np.zeros((1, self.N)), d])
            d[~np.isfinite(d) | (d < TEMETTU_ESIK)] = 0.0
            if self._temettu is not None:
                D = self._temettu.reindex(index=self.idx, columns=self.kodlar).to_numpy(float)
                onc = np.vstack([np.full((1, self.N), np.nan), self.A["close"][:-1]])
                with np.errstate(invalid="ignore", divide="ignore"):
                    tab = D / onc
                tab[~np.isfinite(tab) | (tab < 0)] = 0.0
                d = np.maximum(d, tab)
            else:
                self.notlar.append("temettu tablosu yok: adjclose/close oranindan turetildi")
            self._c["tem"] = d
            self._c["temcs"] = np.cumsum(d, axis=0)
        return self._c["tem"]

    def _irx1(self):
        """Nakit faizi: ^IRX (yillik %), ileri doldurulmus ve 1 gun gecikmeli; yoksa 0."""
        if "irx1" not in self._c:
            if "^IRX" in self.kpos:
                s = pd.Series(self.A["close"][:, self.kpos["^IRX"]]).ffill().shift(1).fillna(0.0)
                self._c["irx1"] = np.clip(s.to_numpy(), 0.0, None)
            else:
                self._c["irx1"] = np.zeros(self.T)
                self.notlar.append("^IRX yok: nakit faizi 0")
        return self._c["irx1"]

    def _zor(self, zor_odunc):
        """Zor odunc maskesi (tarih x kod). 'oto': kaldiracli/ters urunler, kaldirac_ters grubu ve
        t-1'e kadarki 60 gunluk dolar hacmi < 50 mln $ olanlar."""
        if zor_odunc is True:
            return np.ones((self.T, self.N), bool)
        if zor_odunc is False or zor_odunc is None:
            return np.zeros((self.T, self.N), bool)
        if isinstance(zor_odunc, str) and zor_odunc == "oto":
            if "zor" not in self._c:
                sab = ((self.evren["kaldirac"].to_numpy(float) != 1.0)
                       | (self.evren["grup"].astype(str).to_numpy() == "kaldirac_ters"))
                self._c["zor"] = ~(self.adv60() >= 50e6) | sab[None, :]
            return self._c["zor"]
        z = np.zeros((self.T, self.N), bool)
        for k in zor_odunc:
            if k in self.kpos:
                z[:, self.kpos[k]] = True
        return z

    def bacak_bps(self, gun, kp, tip, komisyon):
        """Tek bacak maliyeti (bps), VIX carpani HARIC: max(hacim kademesi, 0,5 sent/fiyat) + komisyon.
        gun, kp: konum dizileri; tip: 'k' kapanis / 'a' acilis fiyati.
        komisyon: 'hisse' (0,005 $/hisse, en az 1 $, 10.000 $ emir), 'sabit' (1,5 $/emir), 'oransal' (20 bps)."""
        ham = self.ham_fiyat(tip)[gun, kp]
        with np.errstate(invalid="ignore", divide="ignore"):
            taban = np.maximum(self.kademe()[gun, kp], YARIM_SENT / ham * 1e4)
            if komisyon == "hisse":
                kom = np.maximum(1.0, HISSE_BASI * EMIR_USD / ham) / EMIR_USD * 1e4
            elif komisyon == "sabit":
                kom = np.full(np.shape(ham), SABIT_EMIR / EMIR_USD * 1e4)
            elif komisyon == "oransal":
                kom = np.full(np.shape(ham), ORANSAL_BPS)
            elif komisyon == "muzayede":
                return np.full(np.shape(ham), SABIT_EMIR / EMIR_USD * 1e4)   # yalniz komisyon; kademe yok
            else:
                raise ValueError(f"komisyon: {KOMISYONLAR + KOMISYON_EK}")
        return taban + kom

    def _poz_maliyet(self, t, gi, ci, kp, gf, cf, isaret, agirlik, ngun, komisyon, zor):
        """Bir pozisyon bacagi icin (giris islem maliyeti, cikis islem maliyeti, finansman), getiri birimi.
        isaret: +1 uzun / -1 kisa; agirlik: |pozisyon| (hedefte 1, korunmada |beta|)."""
        v1 = self.rejim()["vix_1"].to_numpy()
        vt = v1[t] > 30
        cg = np.where(vt | (v1[gi] > 30), 2.0, 1.0)
        cc = np.where(vt | (v1[ci] > 30), 2.0, 1.0)
        if komisyon == "muzayede":                    # muzayede emrinde VIX carpani yok
            cg = np.ones_like(cg)
            cc = np.ones_like(cc)
        mg = self.bacak_bps(gi, kp, gf, komisyon) * cg / 1e4 * agirlik
        mc = self.bacak_bps(ci, kp, cf, komisyon) * cc / 1e4 * agirlik
        self.temettu_orani()
        tcs = self._c["temcs"]
        nakit = ngun * self._irx1()[t] / 100.0 / 252.0
        tem = TEMETTU_KESINTI * (tcs[ci, kp] - tcs[gi, kp])
        takvim = np.maximum(self._gunno[ci] - self._gunno[gi], 1)
        odunc = (ODUNC_GENEL + ODUNC_ZOR * zor[t, kp]) * takvim / 360.0
        fin = np.where(isaret > 0, nakit + tem, odunc) * agirlik
        return mg, mc, fin

    # ------------------------------------------------------------------ islem listesi
    def _sinyal_matris(self, sinyal, hedef, guc):
        if isinstance(sinyal, pd.Series):
            if hedef is None or not isinstance(hedef, str):
                raise ValueError("Series sinyal icin hedef kodu (str) verin")
            sinyal = sinyal.to_frame(hedef)
            if isinstance(guc, pd.Series):
                guc = guc.to_frame(hedef)
        elif hedef is not None:
            hk = [hedef] if isinstance(hedef, str) else list(hedef)
            sinyal = sinyal[hk]
        ks = [str(c) for c in sinyal.columns]
        for k in ks:
            if k not in self.kpos:
                raise KeyError(f"hedef panelde yok: {k}")
            if self.sinif.get(k, "ABD16") != "ABD16":
                raise ValueError(f"{k}: hedef yalniz ABD16 sinifindan olabilir")
            if not np.isfinite(self.evren.at[k, "maliyet_bps"]):
                raise ValueError(f"{k}: dogrudan islem gormez (maliyet tanimsiz), hedef olamaz")
        S = sinyal.reindex(self.idx).to_numpy(float)
        S = np.nan_to_num(S, nan=0.0)
        if not np.isin(S, (-1.0, 0.0, 1.0)).all():
            raise ValueError("sinyal degerleri {-1, 0, +1} olmali")
        if guc is None:
            # Ana ajan duzeltmesi (denetim bulgusu 5): guc verilmezse esitlik sutun sirasina gore degil,
            # veriden bagimsiz sabit tohumlu sozde-rastgele sirayla bozulur (portfoy hep ilk sutunlari secmesin).
            G = np.abs(S) * (1.0 + 1e-6 * np.random.default_rng(20261121).random(S.shape))
        else:
            G = np.nan_to_num(guc.reindex(index=self.idx, columns=sinyal.columns).to_numpy(float), nan=0.0)
        return S.astype(np.int8), G, ks

    def islemler(self, sinyal, hedef=None, giris="K", h=1, cikis="kapanis", korunma="yok",
                 guc=None, zor_odunc="oto", maks_poz=MAKS_POZ):
        """{-1,0,+1} sinyalinden ortusmeyen islem listesi (DataFrame, sinyal gunune gore sirali).
        sinyal: Series (hedef=kod) ya da DataFrame (tarih x hedef kodlari). +1 uzun, -1 kisa.
        Bir hedefte t gununde islem acildiysa t+1..t+h-1 sinyalleri atlanir.
        korunma: 'yok', 'SPY' (=SPY:250), 'SPY:60', '<kod>:<pencere>'.
        guc: sinyal gucu (ayni bicim); portfoyde 5'ten fazla aday varsa buyuk olan secilir.
        Sutunlar: hedef, t, giris_tarihi, cikis_tarihi, yon, beta, brut, net_<komisyon>,
        mal_<komisyon> (toplam maliyet+finansman), malg_<komisyon> (giris bacagi), islemmal_<komisyon>,
        anormal, sigma20, olcekli_<komisyon> (net/sigma20), kova_no, ust200, rejim, bolum, donem,
        guc, portfoyde, t_pos, hedef_pos, giris, h, cikis, korunma."""
        S, G, ks = self._sinyal_matris(sinyal, hedef, guc)
        go, co, gf, cf, adim, ngun = _gun_ofset(giris, h, cikis)
        cpos = np.array([self.kpos[k] for k in ks])
        F = self._ileri_np(giris, h, cikis, cpos)
        uyg = self.hedef_uygun()[:, cpos]
        gecerli = (S != 0) & uyg & np.isfinite(F)
        kor = _korunma_coz(korunma)
        if kor:
            mk, mw = kor
            if self.sinif.get(mk, "ABD16") != "ABD16" or not np.isfinite(self.evren.at[mk, "maliyet_bps"]):
                raise ValueError(f"{mk}: korunma araci ABD16 ve islem goren bir kod olmali")
            mp = self.kpos[mk]
            Bm = self.beta(mk, mw).to_numpy()[:, cpos]
            FM = self._ileri_np(giris, h, cikis, np.array([mp]))[:, 0]
            FH = F - Bm * FM[:, None]
            gecerli &= np.isfinite(FH)
        else:
            FH = F
        rr, cc = np.nonzero(gecerli)
        # ortusmeme: hedef basina ileriye dogru acgozlu (yalniz gecmise bakar)
        tut = np.zeros(rr.size, bool)
        son = np.full(len(ks), -10 ** 9)
        for i in range(rr.size):
            c = cc[i]
            if rr[i] >= son[c] + adim:
                tut[i] = True
                son[c] = rr[i]
        t = rr[tut]
        c = cc[tut]
        kp = cpos[c]
        n = t.size
        yon = S[t, c].astype(float)
        gi, ci = t + go, t + co
        rej = self.rejim()
        kova = rej["kova_no"].to_numpy()[t]
        ust = rej["ust200"].to_numpy()[t]
        # kosulsuz taban: ayni varlik, ayni ana donem, ayni VIX(t-1) kovasi (uygun gunler)
        taban, donem_ad, _ = self._taban_np(FH, uyg)
        brut = yon * FH[t, c]
        anormal = yon * (FH[t, c] - taban[t, c])
        sg = self.sigma20().to_numpy()[t, kp]
        sg = np.where(sg > 0, sg, np.nan)
        zor = self._zor(zor_odunc)
        d = {"hedef": np.array(ks, dtype=object)[c], "t": self.idx[t], "giris_tarihi": self.idx[gi],
             "cikis_tarihi": self.idx[ci], "yon": yon.astype(int),
             "beta": Bm[t, c] if kor else np.zeros(n), "brut": brut}
        for kom in KOMISYONLAR + KOMISYON_EK:
            mg, mc, fin = self._poz_maliyet(t, gi, ci, kp, gf, cf, yon, np.ones(n), ngun, kom, zor)
            if kor:
                b = Bm[t, c]
                mpz = np.full(n, mp)
                hg, hc, hfin = self._poz_maliyet(t, gi, ci, mpz, gf, cf, -yon * np.sign(b),
                                                 np.abs(b), ngun, kom, zor)
                mg, mc, fin = mg + hg, mc + hc, fin + hfin
            d["net_" + kom] = brut - mg - mc - fin
            d["mal_" + kom] = mg + mc + fin
            d["malg_" + kom] = mg
            d["islemmal_" + kom] = mg + mc
            d["olcekli_" + kom] = (brut - mg - mc - fin) / sg
        d.update({"anormal": anormal, "sigma20": sg, "kova_no": kova, "ust200": ust,
                  "rejim": rej["rejim"].to_numpy()[t], "bolum": rej["bolum"].to_numpy()[t],
                  "donem": donem_ad[t], "guc": G[t, c]})
        # portfoy secimi: en cok maks_poz eszamanli pozisyon, fazlasi sinyal gucune gore (ileriye dogru)
        pf = np.zeros(n, bool)
        if n:
            bas = np.flatnonzero(np.r_[True, t[1:] != t[:-1]])
            bit = np.r_[bas[1:], n]
            acik = []
            for b0, b1 in zip(bas, bit):
                gun = t[b0]
                if acik:
                    acik = [x for x in acik if x > gun]
                kap = maks_poz - len(acik)
                if kap <= 0:
                    continue
                if b1 - b0 <= kap:
                    sec = np.arange(b0, b1)
                else:
                    sec = b0 + np.argsort(-d["guc"][b0:b1], kind="mergesort")[:kap]
                pf[sec] = True
                acik.extend([gun + adim] * len(sec))
        d.update({"portfoyde": pf, "t_pos": t, "hedef_pos": kp})
        df = pd.DataFrame(d)
        df["giris"], df["h"], df["cikis"], df["korunma"] = giris, (0 if cikis == "acilis" else int(h)), cikis, korunma
        return df

    def _taban_np(self, FH, uyg):
        """Kosulsuz taban matrisi: her (gun, hedef) icin, ayni hedefin ayni ANA donem (STRES/IS/OOS/SON)
        ve ayni VIX(t-1) kovasindaki uygun gunlerde ileri getirisinin ortalamasi (en az 20 gozlem)."""
        kv = self.rejim()["kova_no"].to_numpy()
        FHu = np.where(uyg, FH, np.nan)
        taban = np.full(FH.shape, np.nan)
        donem_ad = np.full(self.T, "", dtype=object)
        tablo = []
        # Ana ajan duzeltmesi (denetim bulgusu 4): hucrede (donem x VIX kovasi) 20'den az gozlem varsa
        # taban, ayni VIX kovasinin butun donemlerdeki (2005-2026) havuzlanmis ortalamasina duser.
        # Boylece SON x VIX>30 islemleri (hucrede yalniz 15 gun) anormal getiriden sessizce dusmez.
        havuz = {}
        for kno in (0, 1, 2):
            alt = FHu[kv == kno]
            say = np.isfinite(alt).sum(axis=0)
            with np.errstate(invalid="ignore", divide="ignore"):
                mu = np.nansum(alt, axis=0) / say
            mu[say < 20] = np.nan
            havuz[kno] = mu
        for d in DONEMLER:
            dm = donem_maskesi(self.idx, d)
            donem_ad[dm] = d
            for kno in (0, 1, 2):
                rows = dm & (kv == kno)
                if not rows.any():
                    continue
                alt = FHu[rows]
                say = np.isfinite(alt).sum(axis=0)
                with np.errstate(invalid="ignore", divide="ignore"):
                    mu = np.nansum(alt, axis=0) / say
                mu[say < 20] = np.nan
                mu = np.where(np.isfinite(mu), mu, havuz[kno])
                taban[rows] = mu
                tablo.append((d, VIX_KOVA_AD[kno], say, mu))
        return taban, donem_ad, tablo

    def kosulsuz_taban(self, kodlar, giris="K", h=1, cikis="kapanis", korunma="yok"):
        """Kosulsuz taban tablosu: kod x ana donem x VIX(t-1) kovasi -> gozlem sayisi ve ortalama
        ileri getiri (bps). Anormal getiri = yon * (ileri getiri - bu ortalama)."""
        tek, ks = self._kodlar(kodlar)
        cpos = np.array([self.kpos[k] for k in ks])
        F = self._ileri_np(giris, h, cikis, cpos)
        kor = _korunma_coz(korunma)
        if kor:
            FM = self._ileri_np(giris, h, cikis, np.array([self.kpos[kor[0]]]))[:, 0]
            F = F - self.beta(kor[0], kor[1]).to_numpy()[:, cpos] * FM[:, None]
        _, _, tablo = self._taban_np(F, self.hedef_uygun()[:, cpos])
        sat = [{"kod": k, "donem": d, "vix_kova": v, "n": int(say[i]), "taban_bps": mu[i] * 1e4}
               for d, v, say, mu in tablo for i, k in enumerate(ks)]
        return pd.DataFrame(sat)

    def bolum_ozeti(self, isl, komisyon="hisse"):
        """VIX(t-1) > 30 bolumleri bazinda ozet (YONTEM 5, 'bugunku rejimde destekli' olcutu).
        Donus: (bolum tablosu, ozet sozlugu). destekli = >= 4 bolum, bolumlerin >= %70'i genel isaretle
        ayni, en buyuk bolum cikarilinca isaret korunuyor ve maliyet x2 ile net > 0."""
        d = isl[isl["bolum"] > 0]
        if len(d) == 0:
            return pd.DataFrame(), {"bolum_sayisi": 0, "destekli": False}
        net = d["net_" + komisyon]
        g = d.groupby("bolum")
        tab = pd.DataFrame({"ilk": g["t"].min(), "son": g["t"].max(), "n": g.size(),
                            "net_bps": g["net_" + komisyon].mean() * 1e4,
                            "brut_bps": g["brut"].mean() * 1e4})
        isaret = np.sign(net.mean())
        buyuk = tab["n"].idxmax()
        kalan = net[d["bolum"] != buyuk]
        net2 = (net - d["islemmal_" + komisyon]).mean()
        oz = {"bolum_sayisi": int(len(tab)), "n_islem": int(len(d)), "net_bps": net.mean() * 1e4,
              "ayni_isaret_orani": float((np.sign(tab["net_bps"]) == isaret).mean()),
              "en_buyuk_bolum": int(buyuk),
              "en_buyuk_haric_net_bps": kalan.mean() * 1e4 if len(kalan) else np.nan,
              "maliyet2x_net_bps": net2 * 1e4}
        oz["destekli"] = bool(oz["bolum_sayisi"] >= 4 and oz["ayni_isaret_orani"] >= 0.70 and isaret > 0
                              and len(kalan) and kalan.mean() > 0 and net2 > 0)
        return tab, oz

    def _katki(self, isl, komisyon="hisse", net=True):
        """Portfoydeki islemlerin gunluk katkilari: (gun konumu, deger, islem satir no).
        Deger, o gun acik pozisyon sayisina bolunmustur (esit agirlik)."""
        bos = (np.zeros(0, int), np.zeros(0), np.zeros(0, int))
        if len(isl) == 0:
            return bos
        sat = np.flatnonzero(isl["portfoyde"].to_numpy())
        if sat.size == 0:
            return bos
        giris, cikis, korunma = isl["giris"].iat[0], isl["cikis"].iat[0], isl["korunma"].iat[0]
        h = max(int(isl["h"].iat[0]), 1)
        t = isl["t_pos"].to_numpy()[sat]
        kp = isl["hedef_pos"].to_numpy()[sat]
        yon = isl["yon"].to_numpy(float)[sat]
        beta = isl["beta"].to_numpy(float)[sat]
        ac, ao = self.A["adjclose"], self.A["adjopen"]
        if cikis == "acilis":
            iz = [(0, ac), (1, ao)]
        elif giris == "K":
            iz = [(0, ac)] + [(k, ac) for k in range(1, h + 1)]
        elif giris == "A":
            iz = [(1, ao)] + [(k, ac) for k in range(1, h + 1)]
        else:
            iz = [(1, ac)] + [(1 + k, ac) for k in range(1, h + 1)]
        kor = _korunma_coz(korunma)
        mp = self.kpos[kor[0]] if kor else None

        def yol(sut):
            m = [arr[t + o, sut] for o, arr in iz]
            for k in range(1, len(m)):
                m[k] = np.where(np.isfinite(m[k]), m[k], m[k - 1])
            return m
        my = yol(kp)
        mm = yol(np.full(t.size, mp)) if kor else None
        gunler, deger, kim = [], [], []
        son = len(iz) - 1
        for k in range(1, len(iz)):
            p = (my[k] - my[k - 1]) / my[0]
            if kor:
                p = p - beta * (mm[k] - mm[k - 1]) / mm[0]
            p = yon * p
            if net:
                if k == 1:
                    p = p - isl["malg_" + komisyon].to_numpy()[sat]
                if k == son:
                    p = p - (isl["mal_" + komisyon].to_numpy()[sat] - isl["malg_" + komisyon].to_numpy()[sat])
            gunler.append(t + iz[k][0])
            deger.append(p)
            kim.append(sat)
        gunler, deger, kim = np.concatenate(gunler), np.concatenate(deger), np.concatenate(kim)
        say = np.bincount(gunler, minlength=self.T)
        return gunler, deger / say[gunler], kim

    def gunluk(self, isl, komisyon="hisse", net=True):
        """Gunluk takvim-zamani kar/zarar serisi (Series, butun takvim; pozisyonsuz gun 0).
        Ayni gun acik pozisyonlar esit agirlikli; yalniz portfoyde=True islemler (en cok 5 eszamanli)."""
        g, v, _ = self._katki(isl, komisyon, net)
        return pd.Series(np.bincount(g, weights=v, minlength=self.T), index=self.idx)

    # ------------------------------------------------------------------ degerlendirme
    @staticmethod
    def _ozet(net, brut, net2, anorm, olc, tpos, yon, bolum, ay, yil, beta_mutlak):
        o = {"n_islem": int(net.size)}
        n = net.size
        if n == 0:
            return o
        bacak = 2.0 * (1.0 + float(beta_mutlak.mean()))     # hedef 2 bacak + korunma 2*|beta|
        ort = net.mean()
        o["brut_bps"] = brut.mean() * 1e4
        o["net_bps"] = ort * 1e4
        fa = anorm[np.isfinite(anorm)]
        o["anormal_bps"] = fa.mean() * 1e4 if fa.size else np.nan
        o["_anormal_eksik"] = int(n - fa.size)       # tabani olmayan (hucrede < 20 gun) islem sayisi
        o["isabet"] = float((net > 0).mean())
        o["medyan_bps"] = float(np.median(net)) * 1e4
        o["en_kotu_bps"] = net.min() * 1e4
        o["basabas_bps"] = brut.mean() * 1e4 / bacak
        o["maliyet2x_net_bps"] = net2.mean() * 1e4
        fo = olc[np.isfinite(olc)]
        if fo.size:
            o["net_sigma"] = fo.mean()
        if n > 1:
            sd = net.std(ddof=1)
            o["sigma_bps"] = sd * 1e4
            if fo.size > 2:
                so = fo.std(ddof=1)
                if so > 0:
                    o["t_olcekli"] = fo.mean() / (so / math.sqrt(fo.size))
            # tarihe gore kumelenmis standart hata (sinyal gunu = kume)
            _, ters = np.unique(tpos, return_inverse=True)
            gs = np.bincount(ters, weights=net - ort)
            G = gs.size
            if G > 1:
                se = math.sqrt(G / (G - 1.0) * float((gs * gs).sum())) / n
                if se > 0:
                    o["t_kume"] = ort / se
            # Ana ajan eki (denetim bulgusu 3): anormal getirinin tarihe gore kumelenmis t'si.
            # Yalniz uzun (ya da yalniz kisa) kurallarda varligin kendi egilimini ayiklar.
            ma = np.isfinite(anorm)
            if ma.sum() > 2:
                a = anorm[ma]
                am = a.mean()
                _, tra = np.unique(tpos[ma], return_inverse=True)
                ga = np.bincount(tra, weights=a - am)
                Ga = ga.size
                if Ga > 1:
                    sea = math.sqrt(Ga / (Ga - 1.0) * float((ga * ga).sum())) / a.size
                    if sea > 0:
                        o["t_anormal"] = am / sea
        o["p_wilcoxon"] = wilcoxon_p(net)
        k = max(3, int(math.ceil(0.05 * n)))
        if n > k:
            o["en_iyi5suz_bps"] = np.partition(net, n - k)[:n - k].mean() * 1e4
        ua, ti = np.unique(ay, return_inverse=True)
        if ua.size > 1:
            at = np.bincount(ti, weights=net)
            kal = ti != int(np.argmax(at))
            o["en_iyi_aysiz_bps"] = net[kal].mean() * 1e4
        uy, yi = np.unique(yil, return_inverse=True)
        o["pozitif_yil_orani"] = float((np.bincount(yi, weights=net) > 0).mean())
        o["_yil_n"] = int(uy.size)
        u, ks = yon > 0, yon < 0
        o["uzun_n"], o["kisa_n"] = int(u.sum()), int(ks.sum())
        if o["uzun_n"]:
            o["uzun_bps"] = net[u].mean() * 1e4
        if o["kisa_n"]:
            o["kisa_bps"] = net[ks].mean() * 1e4
        bm = bolum > 0
        if bm.any():
            ub, bi = np.unique(bolum[bm], return_inverse=True)
            bo = np.bincount(bi, weights=net[bm]) / np.bincount(bi)
            o["bolum_sayisi"] = int(ub.size)
            o["bolum_pozitif_orani"] = float((bo > 0).mean())
        else:
            o["bolum_sayisi"] = 0
        return o

    def degerlendir(self, sinyal, hedef=None, *, kural_id, aile="", ad="", girdi="",
                    h=(1, 2, 3), giris=("K", "A"), gece=True,
                    korunma=("yok", "SPY:250", "SPY:60"), komisyon=KOMISYONLAR,
                    donemler=None, rejimler=True, guc=None, bootstrap=False,
                    zor_odunc="oto", notlar="", islem_dondur=False):
        """Bir kural icin standart sonuc satirlari (SEMA sutunlari):
        donem x rejim x h x giris x cikis x korunma x komisyon.
          sinyal   : Series ({-1,0,+1}, tarih indeksli) + hedef=kod, ya da DataFrame (tarih x hedefler)
          giris    : K (t kapanisi), A (t+1 acilisi), G (t+1 kapanisi; gecikme denetimi)
          gece     : True ise 'K -> t+1 acilisi' satirlari da uretilir (h=0, cikis='acilis')
          korunma  : 'yok', 'SPY:250', 'SPY:60' ... (beta t-1'e kadar)
          donemler : varsayilan STANDART_DONEMLER (yeni yapi hatti icin ['IS2','OOS2'] verin)
          rejimler : True = 12 rejim satiri; False = yalniz 'hepsi'
          bootstrap: False; True = rejim 'hepsi' satirlarinda; 'tum' = n_islem >= 10 olan her satirda
          islem_dondur: True ise (sonuc, {(giris,h,cikis,korunma): islem listesi}) doner."""
        donemler = list(donemler or STANDART_DONEMLER)
        rej_list = REJIMLER if rejimler else ["hepsi"]
        if isinstance(korunma, str):
            korunma = (korunma,)
        if isinstance(giris, str):
            giris = (giris,)
        if isinstance(komisyon, str):
            komisyon = (komisyon,)
        if isinstance(h, int):
            h = (h,)
        S, _, ks = self._sinyal_matris(sinyal, hedef, guc)
        hedef_ad = ks[0] if len(ks) == 1 else f"COK({len(ks)})"
        yon_ad = "uzun" if (S >= 0).all() else ("kisa" if (S <= 0).all() else "iki")
        cpos = np.array([self.kpos[k] for k in ks])
        var_gun = np.isfinite(self.A["adjclose"][:, cpos]).any(axis=1)
        dmask = {d: donem_maskesi(self.idx, d) for d in donemler}
        dyil = {d: max((dmask[d] & var_gun).sum(), 1) / 252.0 for d in donemler}
        ay_tum = (self.idx.year * 12 + self.idx.month).to_numpy()
        yil_tum = self.idx.year.to_numpy()
        kombin = [(g, hh, "kapanis") for g in giris for hh in h]
        if gece:
            kombin.append(("K", 1, "acilis"))
        satirlar, islem_s = [], {}
        for g, hh, ck in kombin:
            for kr in korunma:
                if kr != "yok" and ks == [_korunma_coz(kr)[0]]:
                    continue                      # hedef korunma aracinin kendisi: satir uretilmez
                isl = self.islemler(sinyal, hedef, giris=g, h=hh, cikis=ck, korunma=kr, guc=guc,
                                    zor_odunc=zor_odunc)
                if islem_dondur:
                    islem_s[(g, 0 if ck == "acilis" else hh, ck, kr)] = isl
                tpos = isl["t_pos"].to_numpy()
                brut = isl["brut"].to_numpy()
                anorm = isl["anormal"].to_numpy()
                yon = isl["yon"].to_numpy()
                bolum = isl["bolum"].to_numpy()
                kova = isl["kova_no"].to_numpy()
                ust = isl["ust200"].to_numpy()
                ay, yil = ay_tum[tpos], yil_tum[tpos]
                babs = np.abs(isl["beta"].to_numpy(float))
                rmask = {"hepsi": np.ones(len(isl), bool)}
                if rejimler:
                    for i, v in enumerate(VIX_KOVA_AD):
                        rmask[v] = kova == i
                    rmask["UST"], rmask["ALT"] = ust == 1, ust == 0
                    for i, v in enumerate(VIX_KOVA_AD):
                        rmask[f"{v}|UST"] = (kova == i) & (ust == 1)
                        rmask[f"{v}|ALT"] = (kova == i) & (ust == 0)
                disari = int((~isl["portfoyde"]).sum()) if len(isl) else 0
                for kom in komisyon:
                    net = isl["net_" + kom].to_numpy()
                    net2 = net - isl["islemmal_" + kom].to_numpy()
                    olc = isl["olcekli_" + kom].to_numpy()
                    kg, kv, kk = self._katki(isl, kom, True)
                    for dn in donemler:
                        dm = dmask[dn]
                        td = dm[tpos]
                        for rj in rej_list:
                            sec = td & rmask[rj]
                            o = self._ozet(net[sec], brut[sec], net2[sec], anorm[sec], olc[sec],
                                           tpos[sec], yon[sec], bolum[sec], ay[sec], yil[sec], babs[sec])
                            nt = []
                            if o["n_islem"]:
                                ks_ = sec[kk]
                                seri = np.bincount(kg[ks_], weights=kv[ks_], minlength=self.T)[dm]
                                o["mdd_pct"] = mdd(seri) * 100.0
                                o["yillik_net_pct"] = seri.mean() * 252.0 * 100.0
                                if bootstrap == "tum" and o["n_islem"] >= 10 or (bootstrap is True and rj == "hepsi"):
                                    o["p_bootstrap"] = bootstrap_p(seri)
                                nt.append(f"yil_n={o.pop('_yil_n')}")
                                if o.get("_anormal_eksik"):       # denetim: sessiz dusme yerine not
                                    nt.append(f"anormal_eksik={o['_anormal_eksik']}")
                            o["yillik_islem"] = o["n_islem"] / dyil[dn]
                            if disari and rj == "hepsi" and dn == donemler[0]:
                                nt.append(f"portfoy_disi={disari}")
                            if notlar:
                                nt.append(notlar)
                            o.update({"kural_id": kural_id, "aile": aile, "ad": ad, "girdi": girdi,
                                      "hedef": hedef_ad, "yon": yon_ad,
                                      "h": 0 if ck == "acilis" else hh, "giris": g, "cikis": ck,
                                      "korunma": kr, "komisyon": kom, "donem": dn, "rejim": rj,
                                      "notlar": "; ".join(nt)})
                            satirlar.append(o)
        sonuc = _sema_df(satirlar)
        return (sonuc, islem_s) if islem_dondur else sonuc

    # ------------------------------------------------------------------ tarama yardimcilari
    def tekillestir(self, kodlar=None, esik=0.98, donem="IS", min_gun=250):
        """Korelasyonu > esik olan kodlari teke indirir (yalniz 'donem' verisiyle; varsayilan IS).
        Verilen sirada ilk gelen tutulur (likit olani basa koyun). Donus: (tutulanlar, {atilan: temsilci})."""
        ks = self.kodlar if kodlar is None else list(kodlar)
        R = self._gh("kk").loc[donem_maskesi(self.idx, donem), ks]
        C = R.corr(min_periods=min_gun).to_numpy()
        tut, harita = [], {}
        for i, k in enumerate(ks):
            es = next((j for j in tut if np.isfinite(C[i, j]) and C[i, j] > esik), None)
            if es is None:
                tut.append(i)
            else:
                harita[k] = ks[es]
        return [ks[i] for i in tut], harita

    def kumele(self, kodlar=None, k=60, donem="IS", min_gun=500, piyasa="SPY"):
        """Evreni YALNIZ 'donem' (varsayilan IS) getirileriyle <= k sepete kumeler
        (1 - korelasyon uzakligi, ortalama baglantili toplayici kumeleme).
        piyasa verilirse korelasyon, donem ici tek betayla piyasadan arindirilmis artik getirilerden
        hesaplanir (yoksa genis endeks ve sektorler tek dev kumede toplanir); piyasa=None: ham getiri.
        Donus: Series kod -> kume no (0..); donemde yeterli verisi olmayanlar -1."""
        ks = self.kodlar if kodlar is None else list(kodlar)
        dm = donem_maskesi(self.idx, donem)
        R = self._gh("kk").loc[dm, ks]
        if piyasa is not None and piyasa in self.kpos:
            x = self._gh("kk").loc[dm, piyasa]
            xm = x - x.mean()
            with np.errstate(invalid="ignore", divide="ignore"):
                b = R.apply(lambda y: (xm * (y - y.mean())).sum() / (xm[y.notna()] ** 2).sum())
            R = R - np.outer(x.to_numpy(), b.to_numpy())
            if piyasa in R.columns:
                R[piyasa] = x                      # piyasa kodu kendi basina kalir
        yeter = R.notna().sum() >= min_gun
        var = [c for c in ks if yeter[c]]
        out = pd.Series(-1, index=ks, dtype=int)
        n = len(var)
        if n == 0:
            return out
        D = 1.0 - R[var].corr(min_periods=min_gun // 2).to_numpy()
        D[~np.isfinite(D)] = 2.0
        np.fill_diagonal(D, np.inf)
        boy = np.ones(n)
        etiket = np.arange(n)
        aktif = n
        while aktif > k:
            i, j = divmod(int(np.argmin(D)), n)
            if not np.isfinite(D[i, j]):
                break
            yeni = (boy[i] * D[i] + boy[j] * D[j]) / (boy[i] + boy[j])
            D[i], D[:, i] = yeni, yeni
            D[i, i] = np.inf
            D[j], D[:, j] = np.inf, np.inf
            boy[i] += boy[j]
            etiket[etiket == j] = i
            aktif -= 1
        _, no = np.unique(etiket, return_inverse=True)
        out[var] = no
        return out

    def sepet_getiri(self, kume, tur="kk", guvenli=True):
        """Sepet (kume) getirisi: uyelerin o gun mevcut getirilerinin esit agirlikli ortalamasi."""
        kume = kume[kume >= 0]
        R = self.girdi_getiri(list(kume.index), tur) if guvenli else self._gh(tur)[list(kume.index)]
        return R.T.groupby(kume.to_numpy()).mean().T

    def blok_permutasyon(self, blok=20, rng=None, maske=None):
        """Plasebo 1: satir permutasyonu (uzunluk T). Y_plasebo = Y[perm] (butun Y'lere AYNI perm).
        Gunler (takvim yili, VIX(t-1) kovasi) hucrelerine ayrilir; her hucrenin gunleri sirayla
        'blok' gunluk parcalara bolunur ve parcalar yalniz o hucrenin icinde yer degistirir.
        maske disindaki gunler yerinde kalir."""
        rng = rng or np.random.default_rng(0)
        kova = self.rejim()["kova_no"].to_numpy()
        yil = self.idx.year.to_numpy()
        ms = np.ones(self.T, bool) if maske is None else np.asarray(maske, bool)
        perm = np.arange(self.T)
        hucre = yil * 10 + kova
        for hc in np.unique(hucre[ms]):
            pos = np.flatnonzero(ms & (hucre == hc))
            if pos.size <= blok:
                continue
            parcalar = [pos[i:i + blok] for i in range(0, pos.size, blok)]
            # Denetim duzeltmesi: duz rastgele siralama hucre basina ortalama 1 parcayi (IS gunlerinin
            # ~%10'u) yerinde birakiyor, plasebo gercek sinyal-getiri baginin bir kismini tasiyordu.
            # Hicbir gun yerinde kalmayana kadar yeniden cekilir (>= 2 parcada her zaman mumkun).
            for _ in range(500):
                sira = rng.permutation(len(parcalar))
                yeni = np.concatenate([parcalar[i] for i in sira])
                if not (yeni == pos).any():
                    break
            perm[pos] = yeni
        return perm

    # ------------------------------------------------------------------ donem basi evreni
    def donem_basi_evreni(self, n=150, pencere=250, min_gun=125, yaz=None):
        """Donem basi hisse evreni: 01.01.2010, 01.01.2020, 01.01.2024 ONCESINDEKI 'pencere' islem
        gununun ortalama dolar hacmine gore ilk n hisse (tur == 'hisse'; pencerede en az min_gun gun).
        Donus: DataFrame (donem, kesim_tarihi, sira, kod, dolar_hacmi). yaz: CSV yolu."""
        dv = self.A["close"] * self.A["volume"]
        hisse = np.array([str(self.evren.at[k, "tur"]) == "hisse" for k in self.kodlar])
        sat = []
        for dn, tarih in DONEM_BASI.items():
            i1 = int(self.idx.searchsorted(pd.Timestamp(tarih)))
            i0 = max(i1 - pencere, 0)
            alt = dv[i0:i1]
            say = (np.isfinite(alt) & (alt > 0)).sum(axis=0)
            with np.errstate(invalid="ignore", divide="ignore"):
                ort = np.nansum(alt, axis=0) / np.maximum(np.isfinite(alt).sum(axis=0), 1)
            ort[(say < min_gun) | ~hisse] = -1.0
            sira = np.argsort(-ort, kind="mergesort")
            sira = [i for i in sira if ort[i] > 0][:n]
            for s, i in enumerate(sira, 1):
                sat.append({"donem": dn, "kesim_tarihi": tarih, "sira": s, "kod": self.kodlar[i],
                            "dolar_hacmi": round(float(ort[i]), 0)})
        d = pd.DataFrame(sat)
        if yaz:
            d.to_csv(yaz, index=False)
        return d

    def evren_maskesi(self, tablo=None):
        """Donem basi evreninden sinyal maskesi (tarih x kod, bool DataFrame): bir hisse yalniz
        secildigi donemin gunlerinde True. STRES donemi icin evren tanimli degil (False)."""
        tablo = self.donem_basi_evreni() if tablo is None else tablo
        M = np.zeros((self.T, self.N), bool)
        for dn in DONEM_BASI:
            dm = donem_maskesi(self.idx, dn)
            kp = [self.kpos[k] for k in tablo.loc[tablo["donem"] == dn, "kod"] if k in self.kpos]
            M[np.ix_(dm, kp)] = True
        return pd.DataFrame(M, index=self.idx, columns=self.kodlar)

    # ------------------------------------------------------------------ ileriye bakma denetimi
    def bozuk_kopya(self, T0, tohum=0):
        """T0 ve sonrasindaki butun fiyat/hacim verisi rastgele bozulmus yeni Motor."""
        rng = np.random.default_rng(tohum)
        i0 = int(self.idx.searchsorted(pd.Timestamp(T0)))
        P = {}
        for a in self.ALANLAR:
            x = self.A[a].copy()
            x[i0:] = x[i0:] * np.exp(rng.normal(0.0, 0.3, size=x[i0:].shape))
            if a == "volume":
                x[i0:] = np.round(x[i0:] * rng.uniform(0.0, 3.0, size=x[i0:].shape))
            P[a] = pd.DataFrame(x, index=self.idx, columns=self.kodlar)
        P["evren"] = self.evren.reset_index()
        return Motor(P, kalite_df=self._kalite, kabuk_kes=self._kabuk_kes, temettu_df=self._temettu)

    def bakis_testi(self, sinyal_fn, T0=("2015-06-15", "2021-03-10", "2025-02-03"), tohum=7):
        """Bir kuralin ileriye bakip bakmadigini sinar. sinyal_fn(motor) -> Series/DataFrame.
        T0 sonrasi veri bozulur; T0'dan onceki sinyal degerleri birebir ayni kalmalidir.
        Donus: (gecti mi, [(T0, farkli satir sayisi, ilk farkli tarih)])."""
        s0 = sinyal_fn(self)
        s0 = s0.to_frame("s") if isinstance(s0, pd.Series) else s0
        rapor, tamam = [], True
        for k, t0 in enumerate(T0):
            if pd.Timestamp(t0) <= self.idx[0] or pd.Timestamp(t0) > self.idx[-1]:
                continue
            s1 = sinyal_fn(self.bozuk_kopya(t0, tohum + k))
            s1 = s1.to_frame("s") if isinstance(s1, pd.Series) else s1
            a = s0.loc[s0.index < pd.Timestamp(t0)]
            b = s1.loc[s1.index < pd.Timestamp(t0)].reindex(index=a.index, columns=a.columns)
            x, y = a.to_numpy(float), b.to_numpy(float)
            fark = ~((x == y) | (np.isnan(x) & np.isnan(y)))
            sat = fark.any(axis=1)
            if sat.any():
                tamam = False
                rapor.append((t0, int(sat.sum()), a.index[np.argmax(sat)]))
            else:
                rapor.append((t0, 0, None))
        return tamam, rapor


_varsayilan = None


def motor():
    """Gercek panelle tekil Motor (surec basina bir kez yuklenir)."""
    global _varsayilan
    if _varsayilan is None:
        _varsayilan = Motor()
    return _varsayilan


if __name__ == "__main__":
    _m = motor()
    _yol = os.path.join(VERI_DIZIN, "evren_donem_basi.csv")
    _e = _m.donem_basi_evreni(yaz=_yol)
    print(_e.groupby("donem").size().to_dict(), "->", _yol)
    print(_e.groupby("donem").head(5).to_string(index=False))
