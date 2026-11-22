# -*- coding: utf-8 -*-
"""aile_K4a.py - Aile D (1): kendi serisinde uc hareket ve kisa vadeli donus, rejimle (gorev K4a).
Calistir:  python3 -I aile_K4a.py      (tek komut; ~6-8 dk; motor.py / yukle.py degistirilmez)

Kapsam: R8-01..R8-08, R1-03, R1-04, R1-11, R1-14, R7-10 + yontem denetcisi eki (IBS, RSI(2),
ust uste dusus, -2/-3 sigma). Sira: (1) sinyaller + ileriye bakma testi, (2) YALNIZ IS -> aday_K4a.csv,
(3) yalniz adaylar OOS, (4) gecenler icin tam satirlar, rejim, VIX>30 bolumleri, 15:30 testi,
(5) bugunku durum. Ciktilar ../veri/ altinda (sonuc_K4a.csv standart sema + K4a_*.csv ekleri)."""
import os
import sys
import time

KOD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOD)
import numpy as np
import pandas as pd
import motor as M
import yukle

VERI = M.VERI_DIZIN
F_ADAY = os.path.join(VERI, "aday_K4a.csv")
F_OOS = os.path.join(VERI, "K4a_oos_kontrol.csv")
F_SONUC = os.path.join(VERI, "sonuc_K4a.csv")
F_BOLUM = os.path.join(VERI, "K4a_vix30_bolum.csv")
F_FELAKET = os.path.join(VERI, "K4a_felaket.csv")
F_ANALOG = os.path.join(VERI, "K4a_bugun_analog.csv")
F_BUGUN = os.path.join(VERI, "K4a_bugun_sinyal.csv")
F_TETIK = os.path.join(VERI, "K4a_tetik_23kasim.csv")
F_1530 = os.path.join(VERI, "K4a_1530.csv")
F_SINIF = os.path.join(VERI, "K4a_sinif.csv")

ENDEKS = ["SPY", "QQQ", "IWM", "DIA"]
SEKTOR = ["SMH", "SOXX", "XBI", "KRE", "XLE"]
LEV = {"SPY": [("UPRO", "SPXU"), ("SSO", "SDS")], "QQQ": [("TQQQ", "SQQQ"), ("QLD", "QID")],
       "SOXX": [("SOXL", "SOXS")], "IWM": [("TNA", "TZA")]}
YAYIN = {"R8-01": "2025 (E*Trade notu; veri 1957-2024)", "R8-02": "2025 (E*Trade notu)",
         "R8-03": "2005 (Giot; WP 2002)", "R8-04": "1992 (Sentana-Wadhwani)",
         "R8-05": "2019 (Baltussen-van Bekkum-Da)", "R8-06": "bilinmiyor (SentimenTrader blog)",
         "R8-07": "bilinmiyor (PriceActionLab blog; RSI(2) Connors 2008)", "R8-08": "bilinmiyor (CXO)",
         "R1-03": "2019 (Fassas-Hourvouliades)", "R1-04": "2017/18 (Bandelli-Wang, CXO; veri 1991-2017)",
         "R1-11": "2023-25 (Lay Quant blog)", "R1-14": "yok (hipotez)",
         "R7-10": "2020 (Boyarchenko-Larsen-Whelan SR917)", "K4a": "denetci eki (IBS ~2013, RSI(2) 2008)"}
FELAKET = {"2008-09..11": ("2008-09-01", "2008-11-30"), "2020-02..03": ("2020-02-01", "2020-03-31"),
           "2022": ("2022-01-01", "2022-12-31"), "2026-10..11": ("2026-10-01", "2026-11-20")}
SON_GUN = pd.Timestamp("2026-11-20")
YENI_GUN = pd.Timestamp("2026-11-23")


# ============================================================================ girdi ilkelleri
class G:
    """t kapanisinda bilinen ilkel seriler. ovr: (tarih x kod) 15:30 fiyati -> yalniz t gunu fiyati
    degistirilir (gecmis gercek kapanis). ek: {kod: fiyat} -> 2026-11-23 icin varsayimsal satir eklenir.
    fiyat: 'adjclose' (birincil) ya da 'close' (yalniz bolunme duzeltmeli; YONTEM 2 ortusme kontrolu)."""

    def __init__(self, mm, ovr=None, fiyat="adjclose", ek=None):
        self.mm, self.ovr, self.fiyat, self.ek = mm, ovr, fiyat, ek
        self._c = {}
        self.idx = mm.idx if ek is None else mm.idx.append(pd.DatetimeIndex([YENI_GUN]))

    def _uz(self, d, son=None):
        """ek modunda bir satir ekle (son: eklenecek deger; None -> NaN)."""
        if self.ek is None:
            return d
        if isinstance(d, pd.Series):
            return pd.concat([d, pd.Series([np.nan if son is None else son], index=[YENI_GUN])])
        row = pd.DataFrame([son if son is not None else [np.nan] * d.shape[1]], index=[YENI_GUN], columns=d.columns)
        return pd.concat([d, row])

    def _base(self, kods):
        key = ("b", tuple(kods))
        if key not in self._c:
            mm = self.mm
            C = self._uz(mm.girdi(kods, self.fiyat))
            Craw = self._uz(mm.girdi(kods, "close"))
            H = self._uz(mm.girdi(kods, "high"))
            L = self._uz(mm.girdi(kods, "low"))
            Pt = None
            if self.ovr is not None:
                O = self.ovr.reindex(index=self.idx, columns=kods)
                Pt = O * (C / Craw)
                H = H.where(O.isna(), np.maximum(H, O))   # gunluk yuksek/dusuk (15:30 sonrasi sizinti; not)
                L = L.where(O.isna(), np.minimum(L, O))
            if self.ek is not None:
                cs = C.iloc[-2]
                p = pd.Series({k: self.ek.get(k, np.nan) for k in kods})
                rat = (C.iloc[-2] / Craw.iloc[-2])
                C.iloc[-1] = (p * rat).values
                Craw.iloc[-1] = p.values
                H.iloc[-1] = np.maximum(p.values, Craw.iloc[-2].values)
                L.iloc[-1] = np.minimum(p.values, Craw.iloc[-2].values)
            self._c[key] = (C, Craw, H, L, Pt)
        return self._c[key]

    def rt(self, kods):
        C = self._base(kods)[0]
        return C / C.shift(1) - 1.0

    def r(self, kods):
        C, _, _, _, Pt = self._base(kods)
        if Pt is None:
            return self.rt(kods)
        return Pt / C.shift(1) - 1.0

    @staticmethod
    def _seri_np(a):
        out = np.zeros_like(a)
        for i in range(a.shape[0]):
            out[i] = (out[i - 1] + 1.0) * a[i] if i else a[i]
        return out

    def streak_t(self, kods):
        key = ("st", tuple(kods))
        if key not in self._c:
            r = self.rt(kods)
            d = (r < 0).to_numpy(float)
            self._c[key] = pd.DataFrame(self._seri_np(d), index=r.index, columns=r.columns)
        return self._c[key]

    def streak(self, kods):
        st = self.streak_t(kods)
        if self.ovr is None:
            return st
        ro = self.r(kods)
        return pd.DataFrame(np.where(ro < 0, st.shift(1) + 1, 0.0), index=st.index, columns=st.columns).where(ro.notna())

    def _rsi_parca(self, kods):
        key = ("rsi", tuple(kods))
        if key not in self._c:
            C = self._base(kods)[0]
            d = (C - C.shift(1)).to_numpy(float)
            up, dn = np.where(d > 0, d, 0.0), np.where(d < 0, -d, 0.0)
            up[np.isnan(d)], dn[np.isnan(d)] = np.nan, np.nan
            ag, dl = np.full_like(up, np.nan), np.full_like(dn, np.nan)
            for i in range(up.shape[0]):
                if i == 0:
                    ag[i], dl[i] = up[i], dn[i]
                    continue
                pa, pd_ = ag[i - 1], dl[i - 1]
                ag[i] = np.where(np.isnan(pa), up[i], 0.5 * pa + 0.5 * up[i])
                dl[i] = np.where(np.isnan(pd_), dn[i], 0.5 * pd_ + 0.5 * dn[i])
            self._c[key] = (pd.DataFrame(ag, index=C.index, columns=C.columns),
                            pd.DataFrame(dl, index=C.index, columns=C.columns))
        return self._c[key]

    @staticmethod
    def _rsi(ag, dl):
        with np.errstate(divide="ignore", invalid="ignore"):
            x = 100.0 - 100.0 / (1.0 + ag / dl)
        return x.where(dl > 0, 100.0).where(ag.notna())

    def rsi2(self, kods):
        ag, dl = self._rsi_parca(kods)
        if self.ovr is None:
            return self._rsi(ag, dl)
        C, _, _, _, Pt = self._base(kods)
        d = Pt - C.shift(1)
        ago = 0.5 * ag.shift(1) + 0.5 * d.clip(lower=0)
        dlo = 0.5 * dl.shift(1) + 0.5 * (-d).clip(lower=0)
        return self._rsi(ago, dlo).where(Pt.notna())

    def ibs(self, kods):
        C, Craw, H, L, Pt = self._base(kods)
        x = (Craw if Pt is None else self.ovr.reindex(index=self.idx, columns=kods))
        rng = H - L
        return ((x - L) / rng).where(rng > 0).clip(0, 1)

    def sig20(self, kods):
        s = self.mm.sigma20()[kods].copy()
        if self.ek is not None:
            r = self.mm._gh("kk")[kods]
            s = self._uz(s, list(r.iloc[-20:].std().values))
        return s

    def z(self, kods):
        return self.r(kods) / self.sig20(kods)

    def alt200(self, kods):
        C, _, _, _, Pt = self._base(kods)
        if Pt is None:
            return C < C.rolling(200, min_periods=200).mean()
        ma = (C.shift(1).rolling(199, min_periods=199).sum() + Pt) / 200.0
        return (Pt < ma).where(Pt.notna(), False).astype(bool)

    def mac5(self, kods):
        if self.ovr is None:
            return self.r(kods).rolling(5, min_periods=5).sum()
        return self.rt(kods).shift(1).rolling(4, min_periods=4).sum() + self.r(kods)

    def vix1(self, kod="^VIX", sz=False):
        """SONRA sinifi: guvenli girdi 1 gun gecikmeli. sz=True: ayni gun (yalniz sizintili ust sinir)."""
        if sz:
            return self._uz(self.mm.girdi(kod, "close", sizintili=True))
        v = self.mm.girdi(kod, "close")
        if self.ek is None:
            return v
        return self._uz(v, float(self.mm.A["close"][-1, self.mm.kpos[kod]]))

    def hisse(self):
        if "hk" not in self._c:
            mk = self.mm.evren_maskesi()
            ks = [k for k in mk.columns if mk[k].any()]
            self._c["hk"] = ks
            self._c["mk"] = self._uz(mk[ks].astype(float)).fillna(0).astype(bool)
        return self._c["hk"]

    def maske(self):
        self.hisse()
        return self._c["mk"]


def bc(s, kods):
    return pd.DataFrame(np.repeat(s.to_numpy()[:, None], len(kods), axis=1), index=s.index, columns=kods)


def _sig(cond, yon):
    return cond.fillna(False).astype(bool).astype(int) * yon


def bekle(c, n=5):
    """ilk tetiklenmeden sonra n gun bekleme (sirali)."""
    a = c.fillna(False).to_numpy(bool)
    out = np.zeros_like(a)
    son = -10 ** 9
    for i in np.flatnonzero(a):
        if i - son > n:
            out[i] = True
            son = i
    return pd.Series(out, index=c.index)


def kume_ilk(c, bosluk=20):
    a = c.fillna(False).to_numpy(bool)
    out = np.zeros_like(a)
    son = -10 ** 9
    for i in np.flatnonzero(a):
        if i - son > bosluk:
            out[i] = True
        son = i
    return pd.Series(out, index=c.index)


# ============================================================================ kural listesi
def kurallar():
    K = []

    def ekle(id_, ad, girdi, hedef, fn, yon, aile="D", tip="", sz=False, degisken=None):
        K.append(dict(id=id_, ad=ad, girdi=girdi, hedef=hedef, fn=fn, yon=yon, aile=aile, tip=tip,
                      sz=sz, baz=id_.split(":")[0], degisken=degisken))

    # --- R8-01: uc dusus gunu
    for T in ("SPY", "QQQ"):
        ekle("R8-01:r<=-3%", f"{T} kk getiri <= -%3: kapanista uzun", f"{T} r(t)", T,
             lambda g, T=T: (_sig(g.r([T]) <= -0.03, 1), None), "uzun", tip="r")
    # --- R8-02: ertesi gun teyitli giris (SPY)
    for bn, (lo, hi) in {"-3,5..-2,5": (-0.035, -0.025), "<=-3,5": (-9.0, -0.035)}.items():
        for tn, yukari in (("ertesi_yukari", True), ("ertesi_asagi", False)):
            def fn(g, lo=lo, hi=hi, yukari=yukari):
                rp = g.rt(["SPY"]).shift(1)
                r = g.r(["SPY"])
                c = (rp > lo) & (rp <= hi) & ((r > 0) if yukari else (r < 0))
                return _sig(c, 1), None
            ekle(f"R8-02:{bn}:{tn}", f"SPY r(t-1) {bn}% ve t gunu {'yukari' if yukari else 'asagi'}: t kapanisinda uzun",
                 "SPY r(t-1), r(t)", "SPY", fn, "uzun", tip="r")
    # --- R8-03: asiri VIX seviyesi (VIX(t-1); ayni gun yalniz sizintili satir)
    kosul = {">=35": lambda v: v >= 35, ">=40": lambda v: v >= 40, ">=50": lambda v: v >= 50,
             "yuzdelik252>=97": lambda v: v.rolling(252, min_periods=252).rank(pct=True) >= 0.97,
             "25-35(kontrol)": lambda v: (v >= 25) & (v < 35)}
    for T in ("SPY", "QQQ"):
        for kn, kf in kosul.items():
            for bk in (False, True):
                def fn(g, T=T, kf=kf, bk=bk):
                    c = kf(g.vix1())
                    c = bekle(c, 5) if bk else c
                    return _sig(bc(c, [T]), 1), None
                ekle(f"R8-03:VIX(t-1){kn}{':bekle5' if bk else ''}", f"VIX(t-1) {kn}{' (5 gun bekleme)' if bk else ''}: {T} uzun",
                     "^VIX(t-1)", T, fn, "uzun", aile="F", tip="vix")
    for kn in (">=35", ">=40", ">=50"):
        def fn(g, kf=kosul[kn]):
            return _sig(bc(kf(g.vix1(sz=True)), ["SPY"]), 1), None
        ekle(f"R8-03-SZ:VIX(t){kn}", f"SIZINTILI UST SINIR: ayni gun VIX(16:15) {kn}: SPY uzun", "^VIX(t) sizintili",
             "SPY", fn, "uzun", aile="F", tip="vix", sz=True)
    # --- R8-04: VIX kosullu asimetrik donus
    for T in ("SPY", "QQQ"):
        for vn, vf in (("VIX(t-1)>=30", lambda v: v >= 30), ("VIX(t-1)<20(kontrol)", lambda v: v < 20)):
            for bn in ("uzun", "kisa", "iki"):
                def fn(g, T=T, vf=vf, bn=bn):
                    v = bc(vf(g.vix1()), [T])
                    r = g.r([T])
                    s = _sig(v & (r <= -0.015), 1) if bn in ("uzun", "iki") else 0
                    s = s + (_sig(v & (r >= 0.015), -1) if bn in ("kisa", "iki") else 0)
                    return s, None
                ekle(f"R8-04:{vn}:{bn}", f"{vn}: {T} r<=-%1,5 uzun / r>=+%1,5 kisa ({bn} bacak)", f"{T} r(t), ^VIX(t-1)",
                     T, fn, bn, tip="r")
    # --- R8-05: MAC(5)
    for T in ("SPY", "QQQ"):
        for vn in ("hepsi", "VIX(t-1)>=30"):
            def fn(g, T=T, vn=vn):
                s = -np.sign(g.mac5([T])).fillna(0).astype(int)
                if vn != "hepsi":
                    s = s * bc(g.vix1() >= 30, [T]).astype(int)
                return s, None
            ekle(f"R8-05:MAC5:{vn}", f"{T} -(son 5 gun getiri toplami) isareti ({vn})", f"{T} r(t-4..t)", T, fn, "iki", tip="mac")
    # --- R8-06: tam N gunluk dusus serisi
    for T in ("SPY", "QQQ"):
        for N in (5, 6, 7):
            ekle(f"R8-06:seri=={N}", f"{T} ust uste {N}. dusus kapanisi: uzun", f"{T} r", T,
                 lambda g, T=T, N=N: (_sig(g.streak([T]) == N, 1), None), "uzun", tip="st")
    # --- R8-07: RSI(2) < 10, degisken cikis (RSI>70 / >90, en cok 5 gun)
    for ex in (70, 90):
        ekle(f"R8-07:RSI2<10:cikis>{ex}", f"SPY RSI(2)<10 uzun; cikis RSI(2)>{ex} kapanisi, en cok 5 gun", "SPY RSI(2)", "SPY",
             lambda g: (_sig(g.rsi2(["SPY"]) < 10, 1), None), "uzun", tip="rsi", degisken=ex)
    # --- R8-08: ayi piyasasi rallisi
    for T, esik in (("SPY", 0.03), ("QQQ", 0.04)):
        for yn, y in (("kisa", -1), ("uzun(karsilastirma)", 1)):
            def fn(g, T=T, esik=esik, y=y):
                c = bc(g.alt200(["SPY"])["SPY"] & (g.vix1() >= 30), [T]) & (g.r([T]) >= esik)
                return _sig(c, y), None
            ekle(f"R8-08:{yn}", f"SPY<200g ort ve VIX(t-1)>=30 ve {T} r>=+%{esik*100:.0f}: {yn}", f"{T} r, SPY 200g, ^VIX(t-1)",
                 T, fn, "kisa" if y < 0 else "uzun", tip="r")
    # --- R1-03: VIX3M/VIX - 1 alt %20 (backwardation) ; kontrol contango
    for T in ("SPY", "QQQ"):
        for kn in ("alt%20", "s>0(kontrol)"):
            def fn(g, T=T, kn=kn):
                s = g.vix1("^VIX3M") / g.vix1("^VIX") - 1.0
                c = (s < M.genisleyen_esik(s, 0.20)) if kn == "alt%20" else (s > 0)
                return _sig(bc(c, [T]), 1), None
            ekle(f"R1-03:egim_{kn}", f"VIX3M/VIX-1 (t-1) {kn}: {T} uzun", "^VIX3M, ^VIX (t-1)", T, fn, "uzun", tip="vix")
    # --- R1-04: VIX 504 gunluk zirve
    for T in ("SPY", "QQQ"):
        for kn in ("hepsi", "kume_ilk"):
            def fn(g, T=T, kn=kn):
                v = g.vix1()
                c = v >= v.rolling(504, min_periods=504).max()
                c = kume_ilk(c, 20) if kn == "kume_ilk" else c
                return _sig(bc(c, [T]), 1), None
            ekle(f"R1-04:VIX504zirve:{kn}", f"VIX(t-1) 504 gun zirvesi ({kn}): {T} uzun", "^VIX(t-1)", T, fn, "uzun", tip="vix")
    # --- R1-11: VIX/VIX3M < 1 iken tut ; ters yon
    for T in ("SPY", "QQQ"):
        for kn, f in (("<1", lambda x: x < 1), (">1(ters)", lambda x: x > 1)):
            def fn(g, T=T, f=f):
                return _sig(bc(f(g.vix1("^VIX") / g.vix1("^VIX3M")), [T]), 1), None
            ekle(f"R1-11:VIX/VIX3M{kn}", f"VIX/VIX3M (t-1) {kn}: {T} uzun (gunluk yenilenen tutma)", "^VIX, ^VIX3M (t-1)",
                 T, fn, "uzun", tip="vix")
    # --- R1-14: VIX9D/VIX
    for T in ("SPY", "QQQ"):
        for e in (1.00, 1.05, 1.10, 1.20):
            def fn(g, T=T, e=e):
                return _sig(bc(g.vix1("^VIX9D") / g.vix1("^VIX") >= e, [T]), 1), None
            ekle(f"R1-14:VIX9D/VIX>={e:.2f}", f"VIX9D/VIX (t-1) >= {e:.2f}: {T} uzun", "^VIX9D, ^VIX (t-1)", T, fn, "uzun", tip="vix")
    # --- R7-10: satis gunu sonrasi (gece cikisi = gece satiri)
    for T in ("SPY", "QQQ"):
        for kn, f, y in (("r<=-1,5%", lambda r: r <= -0.015, 1), ("r<=-2,5%", lambda r: r <= -0.025, 1),
                         ("r>=+1,5%(kisa)", lambda r: r >= 0.015, -1)):
            ekle(f"R7-10:{kn}", f"{T} {kn}: kapanista {'uzun' if y > 0 else 'kisa'}", f"{T} r(t)", T,
                 lambda g, T=T, f=f, y=y: (_sig(f(g.r([T])), y), None), "uzun" if y > 0 else "kisa", tip="r")
    # --- denetci eki: IBS, RSI(2), ust uste >=k dusus, -2/-3 sigma
    ek = {"IBS<0,2": (lambda g, k: g.ibs(k) < 0.2, lambda g, k: 0.2 - g.ibs(k), 1, "ibs"),
          "IBS>0,8": (lambda g, k: g.ibs(k) > 0.8, lambda g, k: g.ibs(k) - 0.8, -1, "ibs"),
          "RSI2<10": (lambda g, k: g.rsi2(k) < 10, lambda g, k: 10 - g.rsi2(k), 1, "rsi"),
          "RSI2>90": (lambda g, k: g.rsi2(k) > 90, lambda g, k: g.rsi2(k) - 90, -1, "rsi"),
          "seri>=3": (lambda g, k: g.streak(k) >= 3, lambda g, k: g.streak(k), 1, "st"),
          "seri>=5": (lambda g, k: g.streak(k) >= 5, lambda g, k: g.streak(k), 1, "st"),
          "seri>=7": (lambda g, k: g.streak(k) >= 7, lambda g, k: g.streak(k), 1, "st"),
          "z<=-2": (lambda g, k: g.z(k) <= -2, lambda g, k: -g.z(k), 1, "z"),
          "z<=-3": (lambda g, k: g.z(k) <= -3, lambda g, k: -g.z(k), 1, "z")}
    for kn, (cf, gf, y, tip) in ek.items():
        for T in ENDEKS + SEKTOR + ["HISSE"]:
            def fn(g, T=T, cf=cf, gf=gf, y=y):
                if T == "HISSE":
                    ks = g.hisse()
                    mk = g.maske()
                    c = cf(g, ks) & mk
                    return _sig(c, y), gf(g, ks).where(c)
                return _sig(cf(g, [T]), y), None
            ekle(f"K4a-{kn}", f"{'Donem basi 150 hisse' if T == 'HISSE' else T} {kn}: kapanista {'uzun' if y > 0 else 'kisa'}",
                 f"{T} {kn}", T, fn, "uzun" if y > 0 else "kisa", tip=tip)
    return K


def anahtar(k):
    return f"{k['id']}|{k['hedef']}"


# ============================================================================ degisken cikis (R8-07)
def degisken_islem(mm, entry, cond, hedef, giris="K", korunma="yok", cap=5):
    e = entry.reindex(mm.idx).fillna(0).to_numpy() != 0
    c = cond.reindex(mm.idx).fillna(False).to_numpy(bool)
    T = e.size
    b = 1 if giris == "G" else 0
    Kd = np.full(T, cap)
    for d in range(cap, 0, -1):
        ix = np.arange(T) + b + d
        hit = np.zeros(T, bool)
        ok = ix < T
        hit[ok] = c[ix[ok]]
        Kd = np.where(hit, d, Kd)
    acc, son = [], -10 ** 9
    for t in np.flatnonzero(e):
        if t >= son:
            acc.append(t)
            son = t + Kd[t]
    acc = np.array(acc, int)
    parca = []
    for k in range(1, cap + 1):
        tt = acc[Kd[acc] == k]
        if tt.size == 0:
            continue
        s = pd.Series(0, index=mm.idx)
        s.iloc[tt] = 1
        parca.append(mm.islemler(s, hedef, giris=giris, h=k, korunma=korunma))
    return parca


def degisken_rows(mm, entry, cond, hedef, meta, girisler=("K",), korunmalar=("yok",), komlar=("hisse",),
                  donemler=("IS",), rejimler=False, bootstrap=False):
    satir, isl_d = [], {}
    var_gun = np.isfinite(mm.A["adjclose"][:, mm.kpos[hedef]])
    ay_tum = (mm.idx.year * 12 + mm.idx.month).to_numpy()
    yil_tum = mm.idx.year.to_numpy()
    for g in girisler:
        for kr in korunmalar:
            parca = degisken_islem(mm, entry, cond, hedef, g, kr)
            isl = pd.concat(parca).sort_values("t_pos").reset_index(drop=True)
            isl_d[(g, 5, f"rsi>{meta['degisken']}", kr)] = isl
            tpos = isl["t_pos"].to_numpy()
            kova, ust = isl["kova_no"].to_numpy(), isl["ust200"].to_numpy()
            rm = {"hepsi": np.ones(len(isl), bool)}
            if rejimler:
                for i, v in enumerate(M.VIX_KOVA_AD):
                    rm[v] = kova == i
                rm["UST"], rm["ALT"] = ust == 1, ust == 0
                for i, v in enumerate(M.VIX_KOVA_AD):
                    rm[f"{v}|UST"], rm[f"{v}|ALT"] = (kova == i) & (ust == 1), (kova == i) & (ust == 0)
            for kom in komlar:
                net = isl["net_" + kom].to_numpy()
                seri_tum = sum(mm.gunluk(p, kom).to_numpy() for p in parca)
                for dn in donemler:
                    dm = M.donem_maskesi(mm.idx, dn)
                    td = dm[tpos]
                    for rj, rmk in rm.items():
                        sec = td & rmk
                        o = mm._ozet(net[sec], isl["brut"].to_numpy()[sec],
                                     (net - isl["islemmal_" + kom].to_numpy())[sec], isl["anormal"].to_numpy()[sec],
                                     isl["olcekli_" + kom].to_numpy()[sec], tpos[sec], isl["yon"].to_numpy()[sec],
                                     isl["bolum"].to_numpy()[sec], ay_tum[tpos][sec], yil_tum[tpos][sec],
                                     np.abs(isl["beta"].to_numpy(float))[sec])
                        nt = ["degisken cikis: h=en cok 5"]
                        if o["n_islem"]:
                            nt.append(f"yil_n={o.pop('_yil_n')}")
                            if o.get("_anormal_eksik"):
                                nt.append(f"anormal_eksik={o['_anormal_eksik']}")
                            if rj == "hepsi":
                                seri = seri_tum[dm]
                                o["mdd_pct"] = M.mdd(seri) * 100
                                o["yillik_net_pct"] = seri.mean() * 252 * 100
                                if bootstrap:
                                    o["p_bootstrap"] = M.bootstrap_p(seri)
                        o["yillik_islem"] = o["n_islem"] / max((dm & var_gun).sum(), 1) * 252
                        o.update(kural_id=meta["id"], aile=meta["aile"], ad=meta["ad"], girdi=meta["girdi"], hedef=hedef,
                                 yon="uzun", h=5, giris=g, cikis=f"rsi>{meta['degisken']}", korunma=kr, komisyon=kom,
                                 donem=dn, rejim=rj, notlar="; ".join(nt))
                        satir.append(o)
    return M._sema_df(satir), isl_d


# ============================================================================ degerlendirme sarmalayicilari
def sinyal_al(k, g):
    s, guc = k["fn"](g, k["hedef"]) if False else k["fn"](g)
    return s, guc


def calis(m, k, sig, guc, **kw):
    """degerlendir ya da degisken cikis; tek hedefte Series."""
    meta = k
    if k["degisken"]:
        kw2 = {a: kw[a] for a in ("donemler", "rejimler", "bootstrap") if a in kw}
        gir = kw.get("giris", ("K",))
        gir = (gir,) if isinstance(gir, str) else gir
        kor = kw.get("korunma", "yok")
        kor = (kor,) if isinstance(kor, str) else kor
        kom = kw.get("komisyon", "hisse")
        kom = (kom,) if isinstance(kom, str) else kom
        rsi = G(m).rsi2(["SPY"])["SPY"]
        return degisken_rows(m, sig["SPY"], rsi > k["degisken"], "SPY", meta, girisler=gir, korunmalar=kor,
                             komlar=kom, **kw2)
    isl_iste = kw.pop("islem_dondur", False)
    if k["hedef"] == "HISSE":
        S = sig.loc[:, sig.abs().sum() > 0]
        res = m.degerlendir(S, None, guc=guc[S.columns], kural_id=k["id"], aile=k["aile"], ad=k["ad"], girdi=k["girdi"],
                            islem_dondur=True, **kw)
    else:
        res = m.degerlendir(sig[k["hedef"]], k["hedef"], kural_id=k["id"], aile=k["aile"], ad=k["ad"], girdi=k["girdi"],
                            islem_dondur=True, **kw)
    return res


def gecer(row, cok, tek_yon, tmin=2.0):
    def f(x):
        return float(x) if pd.notna(x) else np.nan
    t = f(row["t_kume"]) if cok else f(row["t_olcekli"])
    ok = f(row["net_bps"]) > 0 and t >= tmin
    if tek_yon:
        ok = ok and f(row["anormal_bps"]) > 0 and f(row["t_anormal"]) >= 2.0
    return bool(ok)


def hkw(hh):
    return dict(h=(hh,) if hh else (), gece=(hh == 0))


# ============================================================================ raporlama yardimcilari
def bolum_tablo(isl, etiket, kom="hisse"):
    d = isl[isl["bolum"] > 0]
    if len(d) == 0:
        return pd.DataFrame()
    g = d.groupby("bolum")
    t = pd.DataFrame({"ilk_islem": g["t"].min().dt.date, "son_islem": g["t"].max().dt.date, "n": g.size(),
                      "toplam_net_bps": g["net_" + kom].sum() * 1e4, "ort_net_bps": g["net_" + kom].mean() * 1e4,
                      "en_kotu_bps": g["net_" + kom].min() * 1e4, "isabet": g["net_" + kom].apply(lambda x: (x > 0).mean())})
    for a, b in etiket.items():
        t.insert(0, a, b)
    return t.reset_index()


def felaket_tablo(isl, etiket, kom="hisse"):
    out = []
    for fn, (a, b) in FELAKET.items():
        d = isl[(isl["t"] >= pd.Timestamp(a)) & (isl["t"] <= pd.Timestamp(b))].sort_values("t")
        x = d["net_" + kom].to_numpy()
        ard, en_ard, cum, en_cum = 0, 0, 0.0, 0.0
        for v in x:
            if v <= 0:
                ard += 1
                cum += v
            else:
                ard, cum = 0, 0.0
            en_ard, en_cum = max(en_ard, ard), min(en_cum, cum)
        out.append({**etiket, "donem": fn, "n": len(x), "toplam_net_bps": x.sum() * 1e4 if len(x) else np.nan,
                    "isabet": (x > 0).mean() if len(x) else np.nan, "en_kotu_bps": x.min() * 1e4 if len(x) else np.nan,
                    "en_uzun_ardisik_kayip": en_ard, "en_buyuk_ardisik_kayip_bps": en_cum * 1e4})
    return out


def bugun_analog(m):
    """SPY'de bugune benzeyen gunler: ust uste >=7 dusus; VIX(t) ayni gun (16:15, betimsel); 200g ort konumu."""
    g = G(m)
    C = m.df("adjclose", ham=True)
    st = g.streak_t(["SPY", "QQQ"])
    v = pd.Series(m.A["close"][:, m.kpos["^VIX"]], index=m.idx)
    c = C["SPY"]
    ma = c.rolling(200, min_periods=200).mean()
    dd = c / c.rolling(252, min_periods=60).max() - 1
    sat = []
    for i in np.flatnonzero((st["SPY"].to_numpy() >= 5)):
        t = m.idx[i]
        row = {"tarih": t.date(), "spy_seri": int(st["SPY"].iat[i]), "qqq_seri": int(st["QQQ"].iat[i]),
               "vix_t": round(v.iat[i], 2), "vix_t-1": round(v.iat[i - 1], 2),
               "spy_200g_fark_pct": round((c.iat[i] / ma.iat[i] - 1) * 100, 2) if pd.notna(ma.iat[i]) else np.nan,
               "spy_zirveden_pct": round(dd.iat[i] * 100, 2)}
        for kod in ("SPY", "QQQ"):
            for h in (1, 2, 3, 5):
                row[f"{kod}_{h}g_pct"] = (C[kod].iat[i + h] / C[kod].iat[i] - 1) * 100 if i + h < m.T else np.nan
        sat.append(row)
    d = pd.DataFrame(sat)
    d["kosul"] = ""
    d.loc[d.spy_seri >= 7, "kosul"] = "seri>=7"
    d.loc[(d.spy_seri >= 7) & (d.spy_200g_fark_pct < 0), "kosul"] = "seri>=7 & 200g alti"
    d.loc[(d.spy_seri >= 5) & (d.vix_t >= 30), "kosul"] += "|seri>=5 & VIX(t)>=30"
    return d


def analog_ozet(d):
    sat = []
    for ad, msk in {"seri>=7 (her gun)": d.spy_seri >= 7, "seri==7 (ilk gun)": d.spy_seri == 7,
                    "seri==7 & 200g alti": (d.spy_seri == 7) & (d.spy_200g_fark_pct < 0),
                    "seri>=7 & VIX(t)>=30": (d.spy_seri >= 7) & (d.vix_t >= 30),
                    "seri>=5 & VIX(t)>=30": (d.spy_seri >= 5) & (d.vix_t >= 30),
                    "seri>=5 & VIX(t)>=30 & 200g alti": (d.spy_seri >= 5) & (d.vix_t >= 30) & (d.spy_200g_fark_pct < 0)}.items():
        x = d[msk & (pd.to_datetime(d.tarih) < SON_GUN)]
        for kod in ("SPY", "QQQ"):
            for h in (1, 2, 3, 5):
                y = x[f"{kod}_{h}g_pct"].dropna()
                sat.append({"kosul": ad, "kod": kod, "h": h, "n_gun": len(y),
                            "bagimsiz_seri": int((pd.to_datetime(x.tarih).diff().dt.days.fillna(99) > 10).sum()),
                            "ort_pct": y.mean(), "medyan_pct": y.median(), "isabet": (y > 0).mean() if len(y) else np.nan,
                            "en_kotu_pct": y.min(), "en_iyi_pct": y.max()})
    return pd.DataFrame(sat)


# ============================================================================ ana akis
def main():
    t0 = time.time()
    m = M.Motor()
    KL = kurallar()
    print(f"{len(KL)} sinyal tanimi")
    g0 = G(m)
    SIG = {}
    for k in KL:
        SIG[anahtar(k)] = k["fn"](g0)

    # ---- (1) ileriye bakma testi: butun sinyaller tek tabloda
    def hepsi(mm):
        g = G(mm)
        parca = []
        for i, k in enumerate(KL):
            s, _ = k["fn"](g)
            if k["hedef"] == "HISSE":      # evren sutunlari kopyaya gore degisebilir: gunluk toplamlarla karsilastir
                s = pd.DataFrame({"top": s.sum(axis=1), "mut": s.abs().sum(axis=1)})
            parca.append(s.add_prefix(f"{i}|").astype(float))
        rs = g.rsi2(["SPY"]).add_prefix("rsi|")
        return pd.concat(parca + [rs], axis=1)
    temiz, rap = m.bakis_testi(hepsi)
    print("bakis_testi:", temiz, rap, f"{time.time() - t0:.0f} sn")
    assert temiz, rap

    # ---- (2) YALNIZ IS
    IS_rows = []
    for k in KL:
        if k["sz"]:
            continue
        s, guc = SIG[anahtar(k)]
        hh = (1, 2, 3)
        res = calis(m, {**k}, s, guc, h=hh, giris=("K",), gece=True, korunma="yok", komisyon="hisse",
                    donemler=["IS"], rejimler=False)
        r = res[0]
        r["anahtar"] = anahtar(k)
        IS_rows.append(r)
    ISd = pd.concat(IS_rows, ignore_index=True)
    ISd = ISd[(ISd.donem == "IS") & (ISd.rejim == "hepsi")]
    meta = {anahtar(k): k for k in KL}
    ISd["cok"] = ISd.anahtar.map(lambda a: meta[a]["hedef"] == "HISSE")
    ISd["tek_yon"] = ISd.yon.isin(["uzun", "kisa"])
    ISd["aday"] = [gecer(r, r.cok, r.tek_yon) for _, r in ISd.iterrows()]
    test_sayisi = len(ISd)
    print(f"IS: {test_sayisi} varyant, {ISd.aday.sum()} aday ({time.time() - t0:.0f} sn)")
    # adaylarin IS bootstrap'i, sonra dosyaya yaz (OOS'a bakmadan once)
    adaylar = ISd[ISd.aday].copy()
    pb = []
    for _, r in adaylar.iterrows():
        k = meta[r.anahtar]
        s, guc = SIG[r.anahtar]
        hh = int(r.h)
        kw = dict(giris=("K",), korunma="yok", komisyon="hisse", donemler=["IS"], rejimler=False, bootstrap=True)
        kw.update({} if k["degisken"] else hkw(hh))
        x = calis(m, k, s, guc, **kw)[0]
        x = x[(x.h == r.h) & (x.cikis == r.cikis) & (x.rejim == "hepsi")]
        pb.append(float(x.p_bootstrap.iat[0]) if len(x) else np.nan)
    adaylar["p_bootstrap"] = pb
    adaylar["yayin"] = adaylar.anahtar.map(lambda a: YAYIN.get(meta[a]["baz"], YAYIN.get(meta[a]["baz"][:3], "")))
    sut = ["anahtar", "kural_id", "ad", "hedef", "yon", "h", "giris", "cikis", "korunma", "komisyon", "donem", "n_islem",
           "brut_bps", "net_bps", "anormal_bps", "isabet", "t_olcekli", "t_kume", "t_anormal", "p_bootstrap", "p_wilcoxon",
           "cok", "tek_yon", "yayin"]
    adaylar[sut].to_csv(F_ADAY, index=False)
    print(f"aday dosyasi yazildi: {F_ADAY} ({len(adaylar)})")

    # ---- (3) OOS: yalniz adaylar
    oos = []
    for _, r in adaylar.iterrows():
        k = meta[r.anahtar]
        s, guc = SIG[r.anahtar]
        hh = int(r.h)
        kw = dict(giris=("K",), korunma="yok", komisyon="hisse", donemler=["OOS"], rejimler=False, bootstrap=True)
        kw.update({} if k["degisken"] else hkw(hh))
        x = calis(m, k, s, guc, **kw)[0]
        x = x[(x.h == r.h) & (x.cikis == r.cikis) & (x.rejim == "hepsi")].copy()
        x["anahtar"] = r.anahtar
        x["oos_gecti"] = gecer(x.iloc[0], r.cok, r.tek_yon) if len(x) and x.n_islem.iat[0] > 0 else False
        oos.append(x)
    OOSd = pd.concat(oos, ignore_index=True) if oos else pd.DataFrame(columns=M.SEMA + ["anahtar", "oos_gecti"])
    OOSd.to_csv(F_OOS, index=False)
    gecen = OOSd[OOSd.oos_gecti]
    print(f"OOS: {len(gecen)} / {len(OOSd)} gecti ({time.time() - t0:.0f} sn)")
    gecen_anahtar = set(gecen.anahtar)
    aday_anahtar = set(adaylar.anahtar)

    # ---- (4) rapor satirlari (butun sinyaller; aday listesi kilitlendikten sonra)
    anahtar_kural = ["R8-01:r<=-3%|SPY", "R8-01:r<=-3%|QQQ", "R8-06:seri==5|SPY", "R8-06:seri==7|SPY",
                     "R8-07:RSI2<10:cikis>70|SPY", "R8-07:RSI2<10:cikis>90|SPY", "R7-10:r<=-1,5%|SPY", "R7-10:r<=-2,5%|SPY",
                     "R8-04:VIX(t-1)>=30:uzun|SPY", "R8-03:VIX(t-1)>=35|SPY", "R1-04:VIX504zirve:kume_ilk|SPY",
                     "K4a-RSI2<10|SPY", "K4a-RSI2<10|QQQ", "K4a-IBS<0,2|SPY", "K4a-seri>=3|SPY", "K4a-seri>=5|SPY",
                     "K4a-seri>=7|SPY", "K4a-seri>=7|QQQ", "K4a-z<=-2|SPY", "K4a-z<=-3|SPY", "K4a-z<=-2|QQQ"]
    tum, bolum, fel, ISL = [], [], [], {}
    for k in KL:
        a = anahtar(k)
        s, guc = SIG[a]
        kw = dict(h=(1, 2, 3), gece=True, donemler=M.STANDART_DONEMLER, rejimler=True)
        if a in gecen_anahtar:
            kor = ("yok",) if k["hedef"] == "SPY" else ("yok", "SPY:250", "SPY:60", "SPXU:250")
            kw.update(giris=("K", "A", "G"), korunma=kor, komisyon=M.KOMISYONLAR, bootstrap=True)
        elif a in aday_anahtar:
            kw.update(giris=("K", "A"), korunma="yok", komisyon="hisse", bootstrap=True)
        else:
            kw.update(giris=("K",), korunma="yok", komisyon="hisse", bootstrap=False)
        if k["degisken"]:
            kw.pop("h"), kw.pop("gece")
        res, isl = calis(m, k, s, guc, **kw)
        res = res.copy()
        res["notlar"] = res["notlar"].fillna("") + f"; yayin={YAYIN.get(k['baz'], YAYIN.get(k['baz'][:3], ''))}" + \
            ("; SIZINTILI UST SINIR (karar disi)" if k["sz"] else "")
        tum.append(res)
        if a in gecen_anahtar or a in anahtar_kural:
            ISL[a] = isl
            for (gg, hh, ck, kr), d in isl.items():
                if gg != "K" or kr != "yok" or (hh not in (1, 3, 5) and ck == "kapanis"):
                    continue
                et = {"anahtar": a, "giris": gg, "h": hh, "cikis": ck}
                bt = bolum_tablo(d, et)
                if len(bt):
                    bolum.append(bt)
                fel.extend(felaket_tablo(d, et))
    print(f"rapor satirlari tamam ({time.time() - t0:.0f} sn)")

    # ---- kaldiracli ETF uygulama satirlari (ayni sinyal, gercek ETF fiyati)
    for k in KL:
        if k["hedef"] not in LEV or k["sz"]:
            continue
        a = anahtar(k)
        s, _ = SIG[a]
        x = s[k["hedef"]]
        for boga, ayi in LEV[k["hedef"]]:
            if k["degisken"]:
                ent = (x > 0).astype(int)
                rsi = G(m).rsi2(["SPY"])["SPY"]
                for lev in (boga,):
                    kk = {**k, "id": f"{k['id']}|{lev}", "ad": k["ad"] + f" -> {lev}"}
                    r_, _ = degisken_rows(m, ent, rsi > k["degisken"], lev, kk, donemler=("IS", "OOS", "SON", "TUM"))
                    r_["notlar"] = r_["notlar"] + "; kaldiracli uygulama satiri"
                    tum.append(r_)
                continue
            D = pd.DataFrame({boga: (x > 0).astype(int), ayi: (x < 0).astype(int)})
            D = D.loc[:, D.sum() > 0]
            if D.shape[1] == 0:
                continue
            gir = ("K", "A") if a in gecen_anahtar else ("K",)
            kw = dict(kural_id=f"{k['id']}|{'/'.join(D.columns)}", aile=k["aile"], ad=k["ad"] + f" -> {'/'.join(D.columns)}",
                      girdi=k["girdi"], h=(1, 2, 3), gece=True, giris=gir, korunma="yok", komisyon="hisse",
                      donemler=["IS", "OOS", "SON", "TUM"], rejimler=(a in gecen_anahtar), bootstrap=(a in gecen_anahtar),
                      notlar=f"kaldiracli uygulama satiri (sinyal {k['hedef']})")
            r_ = m.degerlendir(D[D.columns[0]], D.columns[0], **kw) if D.shape[1] == 1 else m.degerlendir(D, None, **kw)
            tum.append(r_)
    SON = pd.concat(tum, ignore_index=True)
    M.yaz_sonuc(SON[M.SEMA], F_SONUC)
    print(f"sonuc yazildi: {len(SON)} satir ({time.time() - t0:.0f} sn)")
    if bolum:
        pd.concat(bolum, ignore_index=True).to_csv(F_BOLUM, index=False)
    pd.DataFrame(fel).to_csv(F_FELAKET, index=False)

    # ---- (5) gecenler: 15:30 testi, bolunme-duzeltmeli ortusme, sinif onerisi
    ek_sat, sinif = [], []
    if gecen_anahtar:
        Hs = yukle.saatlik()
        o1530 = Hs["acilis_1530"]
        g_o = G(m, ovr=o1530)
        g_c = G(m, fiyat="close")
        pen = (m.idx >= o1530.index[0]) & (m.idx <= o1530.index[-1])
        for a in sorted(gecen_anahtar):
            k = meta[a]
            s, guc = SIG[a]
            so, guco = k["fn"](g_o)
            sc, _ = k["fn"](g_c)
            ust = float((sc.to_numpy() == s.to_numpy()).all(axis=1)[s.abs().sum(axis=1).to_numpy() > 0].mean()) \
                if (s.abs().sum(axis=1) > 0).any() else np.nan
            orj = s.where(pd.Series(pen, index=m.idx), 0, axis=0)
            yen = so.fillna(0).astype(int).where(pd.Series(pen, index=m.idx), 0, axis=0)
            ob, yb = orj.to_numpy() != 0, yen.to_numpy() != 0
            r = gecen[gecen.anahtar == a].iloc[0]
            hh = int(r.h)
            if k["degisken"]:
                rsi = G(m).rsi2(["SPY"])["SPY"]
                n0 = pd.concat(degisken_islem(m, orj["SPY"], rsi > k["degisken"], "SPY"))
                n1 = pd.concat(degisken_islem(m, yen["SPY"], rsi > k["degisken"], "SPY"))
            elif k["hedef"] == "HISSE":
                c0 = orj.columns[orj.abs().sum() > 0]
                c1 = yen.columns[yen.abs().sum() > 0]
                n0 = m.islemler(orj[c0], None, giris="K", h=max(hh, 1), cikis="acilis" if hh == 0 else "kapanis", guc=guc[c0])
                n1 = m.islemler(yen[c1], None, giris="K", h=max(hh, 1), cikis="acilis" if hh == 0 else "kapanis",
                                guc=guco[c1] if guco is not None else None)
            else:
                T = k["hedef"]
                n0 = m.islemler(orj[T], T, giris="K", h=max(hh, 1), cikis="acilis" if hh == 0 else "kapanis")
                n1 = m.islemler(yen[T], T, giris="K", h=max(hh, 1), cikis="acilis" if hh == 0 else "kapanis")
            ek_sat.append({"anahtar": a, "h": hh, "pencere": f"{o1530.index[0].date()}..{o1530.index[-1].date()}",
                           "tetik_kapanis": int(ob.sum()), "tetik_1530": int(yb.sum()),
                           "ortak": int((ob & yb).sum()), "ortusme_orj_payi": (ob & yb).sum() / max(ob.sum(), 1),
                           "n_islem_kapanis": len(n0), "net_bps_kapanis": n0["net_hisse"].mean() * 1e4 if len(n0) else np.nan,
                           "n_islem_1530": len(n1), "net_bps_1530": n1["net_hisse"].mean() * 1e4 if len(n1) else np.nan,
                           "korunan_pay": (n1["net_hisse"].mean() / n0["net_hisse"].mean()) if len(n0) and len(n1) else np.nan,
                           "bolunme_duz_fiyat_ortusme": ust,
                           "not": "15:30 fiyati t gunu kapanisi yerine; gunluk yuksek/dusuk (IBS) 15:30 sonrasini da icerir"})
        pd.DataFrame(ek_sat).to_csv(F_1530, index=False)

    # sinif onerisi (YONTEM 9) - butun aday/varyantlar
    def sec(a, h, ck, dn, gir="K", kr="yok", kom="hisse", rj="hepsi"):
        k = meta[a]
        x = SON[(SON.kural_id == k["id"]) & (SON.hedef.astype(str).str.startswith("COK") if k["hedef"] == "HISSE" else (SON.hedef == k["hedef"]))
                & (SON.h == h) & (SON.cikis == ck) & (SON.donem == dn) & (SON.giris == gir) & (SON.korunma == kr)
                & (SON.komisyon == kom) & (SON.rejim == rj)]
        return x.iloc[0] if len(x) else None
    mal = {}
    for _, r in ISd.iterrows():
        a = r.anahtar
        k = meta[a]
        cok = k["hedef"] == "HISSE"
        tcol = "t_kume" if cok else "t_olcekli"
        rec = {"anahtar": a, "kural_id": k["id"], "hedef": k["hedef"], "yon": r.yon, "h": r.h, "cikis": r.cikis,
               "aday": bool(r.aday), "is_net_bps": r.net_bps, "is_t": r[tcol], "is_t_anormal": r.t_anormal}
        o = OOSd[(OOSd.anahtar == a) & (OOSd.h == r.h) & (OOSd.cikis == r.cikis)] if len(OOSd) else []
        if not r.aday:
            rec.update(sinif="ELENDI", gerekce="IS adayligi yok (net<=0 ya da t<2" + (" ya da t_anormal<2)" if r.yon != "iki" else ")"))
        elif len(o) == 0 or not bool(o.oos_gecti.iat[0]):
            oo = o.iloc[0] if len(o) else None
            rec.update(oos_net_bps=oo.net_bps if oo is not None else np.nan, oos_t=oo[tcol] if oo is not None else np.nan,
                       oos_p=oo.p_bootstrap if oo is not None else np.nan, oos_n=oo.n_islem if oo is not None else 0)
            if oo is not None and oo.net_bps > 0:
                rec.update(sinif="DUSUK", gerekce="IS ve OOS ayni yon ama OOS t<2 ya da anormal getiri sarti yok")
            else:
                rec.update(sinif="ELENDI", gerekce="OOS'ta isaret dondu")
        else:
            hh, ck = int(r.h), r.cikis
            oo = sec(a, hh, ck, "OOS")
            sn = sec(a, hh, ck, "SON")
            aa = sec(a, hh, ck, "OOS", gir="A") if ck == "kapanis" else None
            tumr = sec(a, hh, ck, "TUM")
            iso = sec(a, hh, ck, "IS+OOS")
            eks = []
            t = oo[tcol]
            if t < 2.5:
                eks.append("OOS t<2,5")
            if oo.n_islem < 30:
                eks.append("az olay")
            p_ok = sum([t >= 1.96, (oo.p_bootstrap < 0.05) if pd.notna(oo.p_bootstrap) else False, oo.p_wilcoxon < 0.05])
            if p_ok < 2:
                eks.append("anlamlilik (3 olcunun ikisi p<0,05 degil)")
            if aa is None or not (aa.net_bps > 0 and aa.t_kume >= 1.5 if cok else aa.net_bps > 0 and aa.t_olcekli >= 1.5):
                eks.append("uygulama (Giris A net>0, t>=1,5 yok)")
            if sn is None or not (sn.net_bps > 0 and (sn[tcol] >= 1.0)):
                eks.append("zayiflama (son donem net>0, t>=1 yok)")
            if not (oo.en_iyi5suz_bps > 0 and oo.en_iyi_aysiz_bps > 0 and oo.maliyet2x_net_bps > 0):
                eks.append("saglamlik")
            if iso is not None and iso.pozitif_yil_orani < 0.65:
                eks.append("pozitif yil < %65")
            for dn in ("OOS-2020", "OOS-2022", "OOS-SubNis2020"):
                x = sec(a, hh, ck, dn)
                if x is None or not x.net_bps > 0:
                    eks.append(f"{dn} isaret")
            maliyet_bacak = (oo.brut_bps - oo.net_bps) / 2.0
            ekon = []
            if not oo.basabas_bps >= 3 * maliyet_bacak:
                ekon.append("basabas<3x maliyet")
            if not oo.net_bps >= 10:
                ekon.append("net<10bps")
            if not oo.net_sigma >= 0.10:
                ekon.append("net/sigma<0,10")
            if not oo.yillik_islem * oo.net_bps / 100 >= 3:
                ekon.append("yillik net<%3")
            tb, oz = m.bolum_ozeti(ISL[a][(("K", hh, ck, "yok") if not meta[a]["degisken"] else ("K", 5, ck, "yok"))])
            if ekon:
                snf, ger = "ELENDI", "anlamli ama onemsiz: " + ", ".join(ekon)
            elif not eks:
                snf, ger = "UYGUN (bagimsiz kod ve BH bekleniyor)", "butun olcutler saglandi"
            else:
                etk = []
                for e in eks:
                    etk.append("zayiflama" if "zayiflama" in e else "uygulama" if "uygulama" in e else "az olay" if "az" in e
                               else "rejim" if "isaret" in e or "yil" in e else e)
                snf, ger = "KOSULLU", "; ".join(dict.fromkeys(etk))
            rec.update(oos_net_bps=oo.net_bps, oos_t=t, oos_p=oo.p_bootstrap, oos_n=oo.n_islem,
                       son_net_bps=sn.net_bps if sn is not None else np.nan, son_t=sn[tcol] if sn is not None else np.nan,
                       girisA_oos_net_bps=aa.net_bps if aa is not None else np.nan, basabas_bps=oo.basabas_bps,
                       vix30=f"{int(tumr.bolum_sayisi)} bolum, %{tumr.bolum_pozitif_orani*100:.0f} pozitif" if tumr is not None else "",
                       bugunku_rejim="destekli" if oz.get("destekli") else "bugunku rejimde sinanmadi/kullanma",
                       sinif=snf, gerekce=ger, eksikler="; ".join(eks + ekon))
        sinif.append(rec)
    pd.DataFrame(sinif).to_csv(F_SINIF, index=False)

    # ---- (6) bugun: 20 Kasim sinyal durumu, analoglar, 23 Kasim tetikleri
    bg = []
    for k in KL:
        s, _ = SIG[anahtar(k)]
        v = s.loc[SON_GUN]
        bg.append({"anahtar": anahtar(k), "deger_20kasim": int(v.sum()) if k["hedef"] == "HISSE" else int(v.iloc[0]),
                   "not": "HISSE: sinyal veren hisse sayisi (isaretli toplam)" if k["hedef"] == "HISSE" else ""})
    pd.DataFrame(bg).to_csv(F_BUGUN, index=False)
    an = bugun_analog(m)
    an.to_csv(F_ANALOG, index=False)
    analog_ozet(an).to_csv(F_ANALOG.replace(".csv", "_ozet.csv"), index=False)
    # 23 Kasim: varsayimsal kapanis fiyati taramasi (gecenler + anahtar kurallar, tek hedefli)
    tet = []
    for a in sorted(gecen_anahtar | set(anahtar_kural)):
        k = meta[a]
        if k["hedef"] == "HISSE":
            continue
        T = k["hedef"]
        c0 = float(m.A["close"][-1, m.kpos[T]])
        grid = np.round(np.arange(-0.10, 0.0501, 0.0025), 4)
        tetik = []
        for x in grid:
            gx = G(m, ek={T: c0 * (1 + x), "SPY": float(m.A["close"][-1, m.kpos["SPY"]]) * (1 + x) if T != "SPY" else c0 * (1 + x)})
            sx, _ = k["fn"](gx)
            tetik.append(int(sx[T].iloc[-1]))
        tetik = np.array(tetik)
        on = grid[tetik != 0]
        tet.append({"anahtar": a, "kapanis_20kasim": c0, "tetik_var": bool(on.size),
                    "tetik_araligi_pct": f"{on.min()*100:+.2f}%..{on.max()*100:+.2f}%" if on.size else "tarama araliginda yok (-10%..+5%)",
                    "tetik_fiyat_araligi": f"{c0*(1+on.min()):.2f}..{c0*(1+on.max()):.2f}" if on.size else "",
                    "yon": int(tetik[tetik != 0][0]) if on.size else 0,
                    "not": "IBS icin varsayim: kapanis=gun dususu (dusus) / gun yuksegi (yukselis); SPY hedef disinda SPY ayni oranda varsayildi; VIX(t-1)=20 Kasim kapanisi 35,89"})
    pd.DataFrame(tet).to_csv(F_TETIK, index=False)
    print(f"bitti ({time.time() - t0:.0f} sn). test={test_sayisi} aday={len(adaylar)} oos_gecen={len(gecen)}")


if __name__ == "__main__":
    main()
