"""Bagimsiz yeniden kodlama (protokol madde 12 olcut 9).

Yalniz kod/PROTOKOL.md ve ham veriden (veri/gunluk, veri/bilanco, veri/bolunme.csv) yazildi.
ortak.py ve b1/b2/b3 betikleri okunmadi, ice aktarilmadi.

Kullanim:
  python kod/yeniden_kodlama.py --cikti veri/sonuc/yeniden_kodlama_kor.csv            # kor tur (varsayilan tanimlar)
  python kod/yeniden_kodlama.py --fiyat duzeltilmis --cikti ...                       # 3 $ esigi duzeltilmis Close'a
  python kod/yeniden_kodlama.py --sade ek/d3_sade.csv                                  # madde 3 sade tablolar
Tanim secenekleri (kor varsayilan ilk deger):
  --fiyat bolunmemis|duzeltilmis|aclose   3 $ esiginin uygulandigi fiyat
  --f3 ge3|eq3                             F3: en az 3 / tam 3 dusuk kapanis
  --maske acik|kapali                      F1-F5 bilanco maskesi
  --bozuk kesin|tolerans                   bozuk satir kontrolu (tolerans: 1e-6 goreli)
  --ciro dahil|haric                       20 gunluk medyan ciroya t gunu dahil mi
  --son12 p3|kendi                         son 12 ay alfasi: P3 ortalamasindan / kendi penceresinin ortalamasindan
"""
import argparse
import os
import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VG = os.path.join(KOK, "veri", "gunluk")
VB = os.path.join(KOK, "veri", "bilanco")

T_EVREN = ["SMH", "SOXX", "QQQ", "XLK", "SPY", "IWM"]
M1 = set("NVDA AMD AVGO TSM MU MSFT GOOGL META AMZN AAPL TSLA SOXL SOXS TQQQ SQQQ".split()) | set(T_EVREN)
DONEMLER = {"P1": ("2010-01-01", "2019-12-31"), "P2": ("2020-01-01", "2022-12-31"),
            "P3": ("2023-01-01", "2026-11-20")}
SON12_BAS = pd.Timestamp("2025-11-21")
SON_GUN = pd.Timestamp("2026-11-20")


def dosya(kod):
    return os.path.join(VG, kod.replace("^", "_").replace("=", "_") + ".csv")


def oku(kod):
    df = pd.read_csv(dosya(kod), parse_dates=["Date"]).set_index("Date").sort_index()
    df = df[df.index <= SON_GUN]
    return df


_BOL = None


def bolunme():
    global _BOL
    if _BOL is None:
        _BOL = pd.read_csv(os.path.join(KOK, "veri", "bolunme.csv"), parse_dates=["tarih"])
    return _BOL


def bolunmemis_close(kod, df):
    """yfinance Close bolunmeye gore duzeltilmistir; o gun gercekte islem goren fiyat = Close x (t'den sonraki bolunme oranlari carpimi)."""
    b = bolunme()
    b = b[b.kod == kod]
    carp = pd.Series(1.0, index=df.index)
    for _, s in b.iterrows():
        carp[df.index < s.tarih] *= s.oran
    return df["Close"] * carp


def donem(tarih):
    if tarih < pd.Timestamp("2020-01-01"):
        return "P1"
    if tarih < pd.Timestamp("2023-01-01"):
        return "P2"
    return "P3"


class Arac:
    def __init__(self, kod, ayar):
        self.kod = kod
        df = oku(kod)
        self.df = df
        self.idx = df.index
        ac = df["AClose"]
        self.r1 = ac.pct_change()
        o, h, l, c = df["Open"], df["High"], df["Low"], df["Close"]
        if ayar.bozuk == "kesin":
            bozuk = (h < np.maximum(o, c)) | (l > np.minimum(o, c)) | (h == l)
        else:
            tol = 1e-6 * c
            bozuk = (h < np.maximum(o, c) - tol) | (l > np.minimum(o, c) + tol) | (h - l <= tol)
        bozuk = bozuk | df[["Open", "High", "Low", "Close", "AClose"]].isna().any(axis=1)
        if ayar.fiyat == "bolunmemis":
            fiyat = bolunmemis_close(kod, df)
        elif ayar.fiyat == "duzeltilmis":
            fiyat = c
        else:
            fiyat = ac
        ciro = c * df["Volume"]
        if ayar.ciro == "dahil":
            med = ciro.rolling(20).median()
        else:
            med = ciro.shift(1).rolling(20).median()
        gecmis = pd.Series(np.arange(len(df)) >= 250, index=df.index)
        self.uygun = (~bozuk) & (fiyat >= 3) & (med >= 20e6) & gecmis
        # donem gunluk ortalamalari (tum gunler)
        per = pd.Series([donem(d) for d in df.index], index=df.index)
        self.per = per
        self.mu = self.r1.groupby(per).mean().to_dict()
        son12 = self.r1[(self.idx >= SON12_BAS)]
        self.mu_son12 = son12.mean()
        # maliyet
        if kod in M1:
            self.maliyet = 10.0
        else:
            m250 = ciro.iloc[-250:].median()
            self.maliyet = 20.0 if m250 >= 300e6 else 40.0
        self.tepki = []  # bilanco tepki gunleri (index konumlari)


def tepki_gunleri(a):
    """Protokol 2.4. Doner: [(A_konum, R_konum)]"""
    yol = os.path.join(VB, a.kod + ".csv")
    if not os.path.exists(yol):
        return []
    b = pd.read_csv(yol, parse_dates=["tarih"])
    idx = a.idx
    vol = a.df["Volume"]
    relv = vol / vol.shift(1).rolling(20).mean()
    cikti = set()
    for _, s in b.iterrows():
        d = s.tarih
        if d > idx[-1]:
            continue
        z = str(s.zaman)
        i_ge = idx.searchsorted(d, side="left")  # ilk gun >= d
        i_gt = idx.searchsorted(d, side="right")  # ilk gun > d
        if z == "sonra":
            R = i_gt
        elif z in ("once", "seans"):
            R = i_ge
        else:
            c1 = i_ge
            c2 = i_ge + 1
            if c2 >= len(idx):
                R = c1
            else:
                v1, v2 = relv.iloc[c1], relv.iloc[c2] if c2 < len(idx) else np.nan
                R = c2 if (pd.notna(v2) and (pd.isna(v1) or v2 > v1)) else c1
        if R >= len(idx) or R < 1:
            continue
        cikti.add((R - 1, R))
    return sorted(cikti)


def islemler_uret(a, sinyal, h, maske):
    """sinyal: bool Series (a.idx). Tek pozisyon, t kapanisi -> t+h kapanisi."""
    s = sinyal.reindex(a.idx).fillna(False).astype(bool) & a.uygun
    poz = np.flatnonzero(s.values)
    ac = a.df["AClose"].values
    tep = np.array([r for _, r in a.tepki], dtype=int) if maske else np.array([], dtype=int)
    son_cikis = -1
    satir = []
    for i in poz:
        j = i + h
        if j >= len(ac):
            continue
        if i < son_cikis:
            continue
        if len(tep) and ((tep >= i) & (tep <= j)).any():
            continue
        satir.append((i, j))
        son_cikis = j
    return satir_tablo(a, satir)


def satir_tablo(a, satir):
    ac = a.df["AClose"].values
    rows = []
    for i, j in satir:
        t = a.idx[i]
        g = (ac[j] / ac[i] - 1) * 1e4
        p = donem(t)
        hh = j - i
        rows.append(dict(kod=a.kod, giris=t, cikis=a.idx[j], h=hh, getiri_bps=g, donem=p,
                         alfa_bps=g - a.mu[p] * 1e4 * hh,
                         alfa12_bps=g - a.mu_son12 * 1e4 * hh, maliyet=a.maliyet))
    return pd.DataFrame(rows)


def kume_ols(y, X, g):
    """Kumeli (CR1) OLS. Doner: beta, se."""
    y = np.asarray(y, float)
    X = np.asarray(X, float)
    XtX_inv = np.linalg.inv(X.T @ X)
    b = XtX_inv @ X.T @ y
    e = y - X @ b
    df = pd.DataFrame(X * e[:, None])
    S = df.groupby(np.asarray(g)).sum().values
    G = S.shape[0]
    n, k = X.shape
    meat = S.T @ S
    c = G / (G - 1) * (n - 1) / (n - k)
    V = c * XtX_inv @ meat @ XtX_inv
    return b, np.sqrt(np.diag(V))


def ozet(test_id, tr, ayar):
    r = dict(test_id=test_id, n_islem=len(tr))
    if len(tr) < 3:
        return r
    y = tr["alfa_bps"].values
    b, se = kume_ols(y, np.ones((len(y), 1)), tr["giris"].values)
    r.update(alfa_bps=b[0], se_bps=se[0], t_kume=b[0] / se[0], ort_bps=tr["getiri_bps"].mean(),
             n_gun=tr["giris"].nunique(), n_arac=tr["kod"].nunique(),
             maliyet_bps=tr["maliyet"].mean(), alfa_net_bps=(tr["alfa_bps"] - tr["maliyet"]).mean())
    for p in ["P1", "P2", "P3"]:
        q = tr[tr.donem == p]
        r[f"n_{p}"] = len(q)
        r[f"alfa_{p}"] = q["alfa_bps"].mean() if len(q) else np.nan
        if len(q) > 2:
            bb, ss = kume_ols(q["alfa_bps"].values, np.ones((len(q), 1)), q["giris"].values)
            r[f"t_{p}"] = bb[0] / ss[0]
    q = tr[tr.giris >= SON12_BAS]
    col = "alfa_bps" if ayar.son12 == "p3" else "alfa12_bps"
    r["n_son12"] = len(q)
    if len(q):
        r["alfa_son12"] = q[col].mean()
        if len(q) > 2:
            bb, ss = kume_ols(q[col].values, np.ones((len(q), 1)), q["giris"].values)
            r["t_son12"] = bb[0] / ss[0]
    return r


def calistir(ayar):
    hedef = sorted(f[:-4] for f in os.listdir(VB) if f.endswith(".csv") and f != "kapsam.csv")
    cekirdek = []
    for k in hedef:
        if os.path.exists(dosya(k)) and oku(k).index[0] <= pd.Timestamp("2016-01-01"):
            cekirdek.append(k)
    araclar = {}
    for k in T_EVREN + cekirdek:
        a = Arac(k, ayar)
        a.tepki = tepki_gunleri(a)
        araclar[k] = a
    vix = oku("^VIX")["Close"]
    sox_r = oku("^SOX")["AClose"].pct_change()

    def sin_ibs(a):
        d = a.df
        rng = d["AHigh"] - d["ALow"]
        ibs = (d["AClose"] - d["ALow"]) / rng
        return ibs < 0.2

    def sin_f3(a):
        c = a.df["AClose"]
        dn = (c < c.shift(1)).astype(int)
        seri = dn.groupby((dn != dn.shift()).cumsum()).cumsum() * dn
        return (seri == 3) if ayar.f3 == "eq3" else (seri >= 3)

    def sin_f4b(a):
        sig = a.r1.shift(1).rolling(60).std()
        return a.r1 > 2 * sig

    maske = ayar.maske == "acik"
    TR = {}
    TR["F1a_T_h1"] = pd.concat([islemler_uret(araclar[k], sin_ibs(araclar[k]), 1, maske) for k in T_EVREN])
    TR["F1a_C_h1"] = pd.concat([islemler_uret(araclar[k], sin_ibs(araclar[k]), 1, maske) for k in cekirdek])
    TR["F3_T_h1"] = pd.concat([islemler_uret(araclar[k], sin_f3(araclar[k]), 1, maske) for k in T_EVREN])
    TR["F4b_T_h1"] = pd.concat([islemler_uret(araclar[k], sin_f4b(araclar[k]), 1, maske) for k in T_EVREN])
    smh = araclar["SMH"]
    sr = sox_r.reindex(smh.idx)
    TR["F11a_SMH_h1"] = islemler_uret(smh, sr <= -0.03, 1, False)
    TR["F11b_SMH_h1"] = islemler_uret(smh, sr >= 0.03, 1, False)
    # F9b: A kapanisinda al, tepki gunu kapanisinda sat
    f9 = []
    for k in cekirdek:
        a = araclar[k]
        satir = []
        son = -1
        for A, R in a.tepki:
            if A < 0 or not bool(a.uygun.iloc[A]) or A < son:
                continue
            satir.append((A, R))
            son = R
        f9.append(satir_tablo(a, satir))
    TR["F9b_C_h1"] = pd.concat(f9)

    sonuc = []
    for tid in ["F1a_T_h1", "F3_T_h1", "F9b_C_h1", "F11a_SMH_h1", "F11b_SMH_h1", "F4b_T_h1", "F1a_C_h1"]:
        sonuc.append(ozet(tid, TR[tid].reset_index(drop=True), ayar))
    # F1d: F1a (C+T) alfasinin VIX>=25 eksi VIX<25 farki
    ct = pd.concat([TR["F1a_T_h1"], TR["F1a_C_h1"]]).reset_index(drop=True)
    ct["vix"] = vix.reindex(ct["giris"]).values
    ct = ct.dropna(subset=["vix"])
    D = (ct["vix"] >= 25).astype(float).values
    X = np.column_stack([np.ones(len(ct)), D])
    b, se = kume_ols(ct["alfa_bps"].values, X, ct["giris"].values)
    r = dict(test_id="F1d_CT_h1", n_islem=len(ct), alfa_bps=b[1], se_bps=se[1], t_kume=b[1] / se[1],
             n_yuksek=int(D.sum()))
    for p in ["P1", "P2", "P3"]:
        q = ct[ct.donem == p]
        Dq = (q["vix"] >= 25).values
        r[f"n_{p}"] = len(q)
        if Dq.sum() > 0 and (~Dq).sum() > 0:
            r[f"alfa_{p}"] = q["alfa_bps"][Dq].mean() - q["alfa_bps"][~Dq].mean()
    q = ct[ct.giris >= SON12_BAS]
    Dq = (q["vix"] >= 25).values
    r["n_son12"] = len(q)
    if Dq.sum() > 0 and (~Dq).sum() > 0:
        r["alfa_son12"] = q["alfa_bps"][Dq].mean() - q["alfa_bps"][~Dq].mean()
    sonuc.append(r)
    return pd.DataFrame(sonuc), TR, araclar, ct


def ana():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fiyat", default="bolunmemis", choices=["bolunmemis", "duzeltilmis", "aclose"])
    ap.add_argument("--f3", default="ge3", choices=["ge3", "eq3"])
    ap.add_argument("--maske", default="acik", choices=["acik", "kapali"])
    ap.add_argument("--bozuk", default="kesin", choices=["kesin", "tolerans"])
    ap.add_argument("--ciro", default="dahil", choices=["dahil", "haric"])
    ap.add_argument("--son12", default="p3", choices=["p3", "kendi"])
    ap.add_argument("--cikti", default=None)
    ap.add_argument("--islem_dizin", default=None, help="islem tablolarini bu dizine yaz (inceleme icin)")
    ayar = ap.parse_args()
    s, TR, _, _ = calistir(ayar)
    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", 40)
    cols = ["test_id", "n_islem", "alfa_bps", "t_kume", "alfa_net_bps", "alfa_P1", "alfa_P2", "alfa_P3",
            "alfa_son12", "t_son12", "n_son12"]
    print(vars(ayar))
    print(s[[c for c in cols if c in s]].round(2).to_string(index=False))
    if ayar.cikti:
        s.round(4).to_csv(ayar.cikti, index=False)
    if ayar.islem_dizin:
        os.makedirs(ayar.islem_dizin, exist_ok=True)
        for k, v in TR.items():
            v.to_csv(os.path.join(ayar.islem_dizin, k + ".csv"), index=False)


if __name__ == "__main__":
    ana()
