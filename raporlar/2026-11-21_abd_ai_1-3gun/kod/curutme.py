"""D3 çürütme (doğrulayıcı kod ajanı). Parametre taraması yok; yalnız önceden tanımlı saldırılar.

Kullanım: python3 kod/curutme.py
Girdi: kod/ortak.py (değiştirilmez), veri/gunluk (XLF XLE XLV XLI XLY XLP XLB DIA MDY EFA EEM EWT EWY EWJ
indir.py ile indirilmiş olmalı), veri/sonuc/B1_1530.csv.
Çıktı: veri/sonuc/D3_curutme_tablolar.md (bütün saldırı tabloları), stdout'a kısa özet.
"""
import sys
import math
from pathlib import Path

import numpy as np
import pandas as pd

KOD = Path(__file__).resolve().parent
sys.path.insert(0, str(KOD))
import ortak as o  # noqa: E402

TKV = o.TK()
SON = o.SON_GUN
T_ = o.evren("T")
C_ = o.evren("Ç")
DIS_ABD = ["XLF", "XLE", "XLV", "XLI", "XLY", "XLP", "XLB", "DIA", "MDY"]
DIS_INTL = ["EFA", "EEM", "EWT", "EWY", "EWJ"]
DIS = DIS_ABD + DIS_INTL
VIX = o.yukle("^VIX")["Close"].reindex(TKV)
RG = o._rejim_gunleri()
OUT = []


def yaz(s=""):
    OUT.append(s)
    print(s, flush=True)


def f(v, nd=1):
    if v is None:
        return ""
    if isinstance(v, (float, np.floating)):
        return "" if not np.isfinite(v) else f"{v:.{nd}f}"
    return str(v)


def tab(df, nd=1, baslik=None):
    if baslik:
        yaz(f"\n**{baslik}**\n")
    cols = list(df.columns)
    yaz("| " + " | ".join(map(str, cols)) + " |")
    yaz("|" + "---|" * len(cols))
    for _, r in df.iterrows():
        yaz("| " + " | ".join(f(v, nd) for v in r.values) + " |")


def kt(x, giris, h=1):
    """ortalama, kümeli t (giriş günü; h>=2 hafta), n"""
    x = np.asarray(x, float)
    if len(x) < 2:
        return (x.mean() if len(x) else np.nan), np.nan, len(x)
    m, se, t, p = o._kume_t(x, o._kume_etiket(pd.DatetimeIndex(giris), h))
    return m, t, len(x)


def donemler(isl, sutun="alfa_bps"):
    d = o._donem_no(isl["giris"])
    out = {}
    for p, ad in enumerate(["P1", "P2", "P3"]):
        m = d == p
        out[ad] = isl.loc[m, sutun].mean() if m.any() else np.nan
        out["n" + ad] = int(m.sum())
    s12 = isl["giris"] >= o.SON12_BAS
    out["son12"] = isl.loc[s12, sutun].mean() if s12.any() else np.nan
    out["t_son12"] = kt(isl.loc[s12, sutun], isl.loc[s12, "giris"])[1] if s12.sum() > 2 else np.nan
    return out


# ---------------------------------------------------------------- sinyaller
def b1_sinyal(kodlar):
    Cl, H, L = o._mat("AClose", kodlar), o._mat("AHigh", kodlar), o._mat("ALow", kodlar)
    with np.errstate(all="ignore"):
        ibs = (Cl - L) / (H - L)
    Cp = Cl.shift(1)
    f3 = (Cl < Cp) & (Cp < Cl.shift(2)) & (Cl.shift(2) < Cl.shift(3))
    return ibs, ibs < 0.2, f3


def isl_al(S, h=1, bilanco_at=True, test_id=None):
    return o.islemler(S, h=h, getiri="ham", bilanco_at=bilanco_at, test_id=test_id)


def sec(D, isl, kodlar):
    """T x N matristen işlemlerin (giris, kod) değerleri."""
    ii = TKV.get_indexer(pd.DatetimeIndex(isl["giris"]))
    jj = isl["kod"].map({c: j for j, c in enumerate(kodlar)}).values
    D = D.values if hasattr(D, "values") else D
    return D[ii, jj]


def ufuk_alfa(isl, kodlar, h, cikis="kapanis"):
    """Aynı girişler için h günlük / açılış çıkışlı ham ve alfa (araç x dönem sabit etkisi)."""
    F = o._ileri_ham(kodlar, h, cikis)
    B = o._beklenen(kodlar, h, cikis, "ham")
    g = sec(F, isl, kodlar)
    return g, g - sec(B, isl, kodlar)


def acilis_giris(isl, kodlar):
    """Kapanışta alamayıp t+1 AÇILIŞTA alırsa: açılış(t+1)->kapanış(t+1) ve açılış(t+1)->kapanış(t+2)."""
    O, C = o._mat("AOpen", kodlar), o._mat("AClose", kodlar)
    out = {}
    for ad, R in (("ac_k1", (C.shift(-1) / O.shift(-1) - 1) * 1e4), ("ac_k2", (C.shift(-2) / O.shift(-1) - 1) * 1e4)):
        Bk = o._donem_ort(R)
        g = sec(R, isl, kodlar)
        out[ad] = (g, g - sec(Bk, isl, kodlar))
    return out


# ---------------------------------------------------------------- F1d farkı
def fark(isl, hi):
    x = isl["alfa_bps"].values
    g = isl["giris"].values
    m1, s1, _, _ = o._kume_t(x[hi], g[hi]) if hi.sum() > 1 else (np.nan, np.nan, 0, 0)
    m0, s0, _, _ = o._kume_t(x[~hi], g[~hi]) if (~hi).sum() > 1 else (np.nan, np.nan, 0, 0)
    se = math.sqrt(s1 ** 2 + s0 ** 2) if np.isfinite(s1) and np.isfinite(s0) else np.nan
    d = m1 - m0
    return d, (d / se if se and np.isfinite(se) and se > 0 else np.nan), int(hi.sum()), int((~hi).sum()), m1, m0


def hi_of(isl):
    return (VIX.reindex(pd.DatetimeIndex(isl["giris"])).values >= 25)


# ---------------------------------------------------------------- yoğunlaşma
def epizot_haric(isl, k=5):
    ep = o._epizot(isl["giris"])
    e = isl["giris"].map(ep)
    top = isl.groupby(e)["alfa_bps"].sum().nlargest(k).index
    return isl[~e.isin(top)], [str(isl.loc[e == i, "giris"].min().date()) for i in top]


def kayan(isl, metrik, yil=3, en_az=30):
    bas = pd.date_range(isl["giris"].min(), isl["giris"].max() - pd.DateOffset(years=yil), freq="MS")
    r = []
    for s in bas:
        sub = isl[(isl["giris"] >= s) & (isl["giris"] < s + pd.DateOffset(years=yil))]
        if len(sub) >= en_az:
            v = metrik(sub)
            if np.isfinite(v):
                r.append((s, v))
    if not r:
        return np.nan, "", np.nan
    v = np.array([x[1] for x in r])
    i = int(np.nanargmin(v))
    return v[i], f"{r[i][0].date()}+{yil}y", (v > 0).mean()


def yogunlasma(ad, isl, d_mod=False):
    """d_mod: F1d (fark) metriği."""
    if d_mod:
        def met(x):
            return fark(x, hi_of(x))[0]

        def tst(x):
            d, t, n1, n0, _, _ = fark(x, hi_of(x))
            return d, t, n1
    else:
        def met(x):
            return x["alfa_bps"].mean()

        def tst(x):
            return kt(x["alfa_bps"], x["giris"])
    rows = []
    rows.append(("tam", *tst(isl)))
    m = ~((isl["giris"] >= "2020-02-01") & (isl["giris"] <= "2020-04-30"))
    rows.append(("2020 Şub-Nis hariç", *tst(isl[m])))
    if d_mod:
        hi = hi_of(isl)
        hx, eps = epizot_haric(isl[hi])
        x5 = pd.concat([hx, isl[~hi]])
    else:
        x5, eps = epizot_haric(isl)
    rows.append(("en iyi 5 epizot hariç", *tst(x5)))
    if d_mod:
        gun = isl[hi].groupby("giris")["alfa_bps"].sum().nlargest(20).index
    else:
        gun = isl.groupby("giris")["alfa_bps"].sum().nlargest(20).index
    rows.append(("en iyi 20 giriş günü hariç", *tst(isl[~isl["giris"].isin(gun)])))
    rows.append(("yalnız 2021+", *tst(isl[isl["giris"] >= "2021-01-01"])))
    rows.append(("yalnız 2023+", *tst(isl[isl["giris"] >= "2023-01-01"])))
    for k in ("SMH", "QQQ"):
        if k in set(isl["kod"]):
            rows.append((f"yalnız {k}", *tst(isl[isl["kod"] == k])))
    mn, pen, pay = kayan(isl, met)
    df = pd.DataFrame(rows, columns=["kesit", "alfa_bps", "t", "n"])
    tab(df, baslik=f"{ad}: yoğunlaşma (en iyi 5 epizot başlangıcı: {', '.join(eps)})")
    yaz(f"\n{ad}: 3 yıllık kayan alfa (aylık kaydırma) en düşük {f(mn)} bps ({pen}); pencerelerin "
        f"%{f(100 * pay, 0)}'i > 0.")
    # yıl yıl
    yy = []
    for y, g in isl.groupby(isl["giris"].dt.year):
        if d_mod:
            d, t, n1, n0, m1, m0 = fark(g, hi_of(g))
            yy.append((y, n1, m1, n0, m0, d))
        else:
            yy.append((y, len(g), g["alfa_bps"].mean(), kt(g["alfa_bps"], g["giris"])[1]))
    cols = ["yıl", "n_VIX>=25", "alfa_hi", "n_VIX<25", "alfa_lo", "fark"] if d_mod else ["yıl", "n", "alfa_bps", "t"]
    yt = pd.DataFrame(yy, columns=cols)
    tab(yt, baslik=f"{ad}: yıl yıl")
    if not d_mod:
        yaz(f"\n{ad}: alfası > 0 olan yıl {int((yt['alfa_bps'] > 0).sum())}/{len(yt)}; en iyi yıl katkısı "
            f"çıkınca alfa: {f(isl[isl['giris'].dt.year != yt.loc[yt['alfa_bps'].mul(yt['n']).idxmax(), 'yıl']]['alfa_bps'].mean())}")
    return df, mn


# ================================================================ 0) yeniden üretim
yaz("# D3 çürütme tabloları\n")
yaz(f"Üretim: kod/curutme.py; son gün {SON.date()}.\n")
ibsT, f1aT, f3T = b1_sinyal(T_)
I_F1a = isl_al(f1aT, test_id="F1a_T_h1")
I_F3 = isl_al(f3T, test_id="F3_T_h1")
ibsC, f1aC, f3C = b1_sinyal(C_)
I_F1aCT = isl_al(pd.concat([f1aC, f1aT], axis=1), test_id="F1d_CT_h1")
SOXR = o.yukle("^SOX")["Close"].pct_change(fill_method=None).reindex(TKV)
I_F11a = o.islemler((SOXR <= -0.03).fillna(False).rename("SMH"), h=1, getiri="ham", test_id="F11a")
I_F11b = o.islemler((SOXR >= 0.03).fillna(False).rename("SMH"), h=1, getiri="ham", test_id="F11b")

S9 = pd.DataFrame(False, index=TKV, columns=C_)
meta9 = {}
for k in C_:
    b = o.bilanco(k)
    if not len(b):
        continue
    iA = TKV.get_indexer(pd.DatetimeIndex(b["A"]))
    iT = TKV.get_indexer(pd.DatetimeIndex(b["tepki"]))
    for a_, t_, (_, r) in zip(iA, iT, b.iterrows()):
        if a_ >= 0 and t_ >= 0:
            S9.iloc[a_, C_.index(k)] = True
            i0 = TKV.searchsorted(r.duyuru)
            meta9[(k, TKV[a_])] = dict(yontem=r.yontem, zaman=r.zaman, i0=i0, iA=a_, iT=t_)
I_F9b = o.islemler(S9, h=1, getiri="ham", test_id="F9b")
d0 = fark(I_F1aCT, hi_of(I_F1aCT))
rep = pd.DataFrame([
    ("F1a_T_h1", len(I_F1a), I_F1a["alfa_bps"].mean(), kt(I_F1a["alfa_bps"], I_F1a["giris"])[1], 4350, 17.21),
    ("F3_T_h1", len(I_F3), I_F3["alfa_bps"].mean(), kt(I_F3["alfa_bps"], I_F3["giris"])[1], 1996, 18.92),
    ("F1d_CT_h1", len(I_F1aCT), d0[0], d0[1], 30587, 56.86),
    ("F11a_SMH_h1", len(I_F11a), I_F11a["alfa_bps"].mean(), kt(I_F11a["alfa_bps"], I_F11a["giris"])[1], 226, 43.35),
    ("F11b_SMH_h1", len(I_F11b), I_F11b["alfa_bps"].mean(), kt(I_F11b["alfa_bps"], I_F11b["giris"])[1], 220, -42.22),
    ("F9b_C_h1", len(I_F9b), I_F9b["alfa_bps"].mean(), kt(I_F9b["alfa_bps"], I_F9b["giris"])[1], 2079, 57.66),
], columns=["test", "n", "alfa_bps", "t_kume", "n_rapor", "alfa_rapor"])
tab(rep, nd=2, baslik="0. Bağımsız yeniden üretim (bu betik)")

# ================================================================ 1) evren dışı
yaz("\n## 1. Evren dışı tekrar (önceden sabit 14 ETF, aynı tanım, maliyet 10 bps varsayımı)\n")
ibsD, f1aD, f3D = b1_sinyal(DIS)
rows = []
per = []
for ad, S in (("F1a", f1aD), ("F3", f3D)):
    isl = isl_al(S, test_id=ad + "_DIS")
    for grup, kodlar in (("ABD 9", DIS_ABD), ("ABD dışı 5", DIS_INTL), ("hepsi 14", DIS)):
        x = isl[isl["kod"].isin(kodlar)]
        m, t, n = kt(x["alfa_bps"], x["giris"])
        dp = donemler(x)
        rows.append((ad, grup, n, m, t, m - 10, dp["P1"], dp["P2"], dp["P3"], dp["son12"]))
    for k, g in isl.groupby("kod"):
        per.append((ad, k, len(g), g["alfa_bps"].mean(), kt(g["alfa_bps"], g["giris"])[1]))
    T_ref = I_F1a if ad == "F1a" else I_F3
    dp = donemler(T_ref)
    m, t, n = kt(T_ref["alfa_bps"], T_ref["giris"])
    rows.append((ad, "T (karşılaştırma)", n, m, t, m - 10, dp["P1"], dp["P2"], dp["P3"], dp["son12"]))
    if ad == "F1a":
        I_F1a_DIS = isl
tab(pd.DataFrame(rows, columns=["kural", "grup", "n", "alfa", "t_kume", "net10", "P1", "P2", "P3", "son12"]),
    baslik="Havuz sonuçları")
pt = pd.DataFrame(per, columns=["kural", "kod", "n", "alfa", "t"])
tab(pt.pivot(index="kod", columns="kural", values="alfa").reset_index(), baslik="ETF başına alfa (bps)")
yaz(f"\nF1a: 14 ETF'nin {int((pt[pt.kural=='F1a'].alfa > 0).sum())}'inde alfa > 0; "
    f"F3: {int((pt[pt.kural=='F3'].alfa > 0).sum())}/14.")

# ================================================================ 2) IBS mi düşüş günü mü
yaz("\n## 2. IBS mi, düşüş günü mü? (T evreni, bütün uygun günler; y = ertesi gün ham getiri, bps)\n")


def panel_reg(kodlar, etiket):
    Y = o._ileri_ham(kodlar, 1, "kapanis")
    Bk = o._beklenen(kodlar, 1, "kapanis", "ham")
    Cl, H, L = o._mat("AClose", kodlar), o._mat("AHigh", kodlar), o._mat("ALow", kodlar)
    with np.errstate(all="ignore"):
        ibs = ((Cl - L) / (H - L)).values
    r = (Cl / Cl.shift(1) - 1).values * 1e4
    sd = (Cl / Cl.shift(1) - 1).rolling(60, min_periods=60).std().shift(1).values * 1e4
    E = o.uygun(kodlar).values
    v = np.repeat(VIX.values[:, None], len(kodlar), 1)
    dn = np.repeat(o._donem_no(TKV)[:, None], len(kodlar), 1)
    jj = np.repeat(np.arange(len(kodlar))[None, :], len(TKV), 0)
    tt = np.repeat(np.arange(len(TKV))[:, None], len(kodlar), 1)
    y = Y.values
    ok = E & np.isfinite(y) & np.isfinite(ibs) & np.isfinite(r) & np.isfinite(v) & np.isfinite(sd) & (sd > 0)
    y, ibs, r, v, dn, jj, tt, sd = (a[ok] for a in (y, ibs, r, v, dn, jj, tt, sd))
    bek = Bk[ok]
    fe = jj * 3 + dn
    _, fei = np.unique(fe, return_inverse=True)
    D = np.zeros((len(y), fei.max() + 1))
    D[np.arange(len(y)), fei] = 1
    d_ibs = (ibs < 0.2).astype(float)
    d_dn = (r < 0).astype(float)
    z = r / sd
    specs = {
        "a: IBS<0,2 + r_t + VIX": [d_ibs, r, v],
        "b: IBS<0,2 + düşüş kuklası + r_t/σ60 + VIX": [d_ibs, d_dn, z, v],
        "c: b + VIX>=25 × IBS<0,2": [d_ibs, d_dn, z, v, d_ibs * (v >= 25)],
        "d: IBS sürekli + r_t/σ60 + VIX": [ibs * 100, z, v],
    }
    adlar = {"a: IBS<0,2 + r_t + VIX": ["IBS<0,2", "r_t (bps)", "VIX"],
             "b: IBS<0,2 + düşüş kuklası + r_t/σ60 + VIX": ["IBS<0,2", "düşüş", "r/σ", "VIX"],
             "c: b + VIX>=25 × IBS<0,2": ["IBS<0,2", "düşüş", "r/σ", "VIX", "IBS×VIX25"],
             "d: IBS sürekli + r_t/σ60 + VIX": ["IBS (puan başına)", "r/σ", "VIX"]}
    rr = []
    for s, X in specs.items():
        Xm = np.column_stack(X + [D])
        b, se, G = o._ols_kume(y, Xm, tt)
        for i, a in enumerate(adlar[s]):
            rr.append((etiket, s, a, b[i], b[i] / se[i]))
    tab(pd.DataFrame(rr, columns=["evren", "model", "değişken", "katsayı_bps", "t_kume"]), nd=2,
        baslik=f"Panel regresyon, araç × dönem sabit etkisi, tarihe göre kümeli ({etiket}; n={len(y)})")
    a = y - bek
    g = []
    for nm, m in (("düşüş & IBS<0,2", (r < 0) & (ibs < 0.2)), ("düşüş & IBS>=0,2", (r < 0) & (ibs >= 0.2)),
                  ("yükseliş & IBS<0,2", (r >= 0) & (ibs < 0.2)), ("yükseliş & IBS>=0,2", (r >= 0) & (ibs >= 0.2))):
        mm, t, n = kt(a[m], TKV[tt[m]])
        g.append((etiket, nm, n, mm, t))
    tab(pd.DataFrame(g, columns=["evren", "hücre", "n", "ertesi gün alfa", "t_kume"]), baslik=f"Dört hücre ({etiket})")
    # düşüş büyüklüğü eşlenmiş karşılaştırma: aynı r/σ beşlisinde IBS<0,2 vs >=0,2
    qs = np.nanquantile(z[r < 0], [0, .2, .4, .6, .8, 1])
    e = []
    for i in range(5):
        m = (r < 0) & (z >= qs[i]) & (z <= qs[i + 1])
        m1, t1, n1 = kt(a[m & (ibs < .2)], TKV[tt[m & (ibs < .2)]])
        m0, t0, n0 = kt(a[m & (ibs >= .2)], TKV[tt[m & (ibs >= .2)]])
        e.append((etiket, f"düşüş beşlisi {i+1} (r/σ {qs[i]:.2f}..{qs[i+1]:.2f})", n1, m1, n0, m0, m1 - m0))
    tab(pd.DataFrame(e, columns=["evren", "dilim", "n IBS<0,2", "alfa", "n IBS>=0,2", "alfa ", "fark"]),
        baslik=f"Düşüş büyüklüğü eşlenmiş ({etiket})")


panel_reg(T_, "T")
panel_reg(DIS_ABD, "evren dışı ABD 9")

# ================================================================ 3) yoğunlaşma
yaz("\n## 3. Yoğunlaşma\n")
yogunlasma("F1a_T", I_F1a)
yogunlasma("F3_T", I_F3)
yogunlasma("F11a_SMH", I_F11a)
yogunlasma("F1d_CT (fark)", I_F1aCT, d_mod=True)

# ================================================================ 4) yürütme
yaz("\n## 4. Yürütme\n")
ex = []
kume = {"F1a_T": (I_F1a, T_), "F3_T": (I_F3, T_), "F11a_SMH": (I_F11a, ["SMH"]),
        "F1a_CT VIX>=25 (F1d bacağı)": (I_F1aCT[hi_of(I_F1aCT)].reset_index(drop=True), C_ + T_),
        "F9b_C": (I_F9b, C_)}
for ad, (isl, kodlar) in kume.items():
    v30 = VIX.reindex(pd.DatetimeIndex(isl["giris"])).values >= 30
    a, g = isl["alfa_bps"], isl["ham_bps"]
    row = dict(kural=ad, n=len(isl), alfa=a.mean(), ham_ort=g.mean(), net_alfa_sinif=(a - isl["maliyet_bps"]).mean(),
               net_alfa_20=a.mean() - 20, net_alfa_30=a.mean() - 30, n_vix30=int(v30.sum()),
               alfa_vix30=a[v30].mean(), net30_vix30=a[v30].mean() - 30, ham_vix30_net30=g[v30].mean() - 30)
    if ad != "F9b_C":
        ac = acilis_giris(isl, kodlar)
        for k_, (gg, aa) in ac.items():
            ok = np.isfinite(aa)
            row[f"{k_}_alfa"] = np.nanmean(aa)
            row[f"{k_}_t"] = kt(aa[ok], isl["giris"][ok], 1 if k_ == "ac_k1" else 2)[1]
            row[f"{k_}_ham"] = np.nanmean(gg)
        ok = np.isfinite(ac["ac_k1"][1])
        row["ac_k1_vix30_alfa"] = np.nanmean(ac["ac_k1"][1][v30])
        row["gece_t1acilis_alfa"] = np.nanmean(ufuk_alfa(isl, kodlar, 1, "acilis")[1])
    ex.append(row)
ex = pd.DataFrame(ex)
tab(ex[["kural", "n", "alfa", "ham_ort", "net_alfa_sinif", "net_alfa_20", "net_alfa_30", "n_vix30", "alfa_vix30",
        "net30_vix30", "ham_vix30_net30"]], baslik="(a) Maliyet duyarlılığı (net = alfa − maliyet; ham_vix30_net30 = mutlak getiri − 30)")
tab(ex[ex.kural != "F9b_C"][["kural", "gece_t1acilis_alfa", "ac_k1_alfa", "ac_k1_t", "ac_k1_ham", "ac_k2_alfa", "ac_k2_t",
                              "ac_k2_ham", "ac_k1_vix30_alfa"]],
    baslik="(b) Ertesi açılışta giriş: gece_t1acilis = kapanış→t+1 açılış (kaçırılan kısım); ac_k1 = açılış(t+1)→kapanış(t+1); ac_k2 = açılış(t+1)→kapanış(t+2)")
b15 = pd.read_csv(o.SONUC / "B1_1530.csv")
b15 = b15[b15.test_id.isin(["F1a_T_h1", "F3_T_h1", "F1a_C_h1", "F3_C_h1", "F1d_CT_h1"])]
tab(b15[["test_id", "n_A", "n_B", "uyum_A_B", "A_bps", "B_bps", "C_bps", "son30dk_bps", "oran_B_A"]], nd=2,
    baslik="(c) B1_1530.csv özeti (son 730 gün; A kapanış sinyali, B 15:30 sinyal + kapanış girişi, C 15:30 giriş)")

# ================================================================ 5) tutma süresi
yaz("\n## 5. Tutma süresi\n")
rows = []
H = {}
for h in (1, 2, 3):
    H[f"h{h}"] = ufuk_alfa(I_F1a, T_, h)
H["t+1 açılış"] = ufuk_alfa(I_F1a, T_, 1, "acilis")
ep = I_F1a["giris"].map(o._epizot(I_F1a["giris"]))
rng = np.random.default_rng(0)
for hucre in ("tam", "STRES", "BUGUN"):
    m = np.ones(len(I_F1a), bool) if hucre == "tam" else RG[hucre].reindex(pd.DatetimeIndex(I_F1a["giris"])).fillna(False).values.astype(bool)
    for ad, (g, a) in H.items():
        x = pd.DataFrame({"ep": ep[m].values, "g": g[m], "a": a[m]}).dropna()
        epm = x.groupby("ep")["g"].mean()
        bs = [epm.values[rng.integers(0, len(epm), len(epm))].mean() for _ in range(2000)] if len(epm) > 1 else [np.nan]
        rows.append((hucre, ad, len(x), len(epm), x["g"].mean(), x["a"].mean(), epm.mean(), (epm > 0).mean(),
                     np.percentile(bs, 5), np.percentile(bs, 95)))
tt5 = pd.DataFrame(rows, columns=["hücre", "çıkış", "n", "n_epizot", "ham_ort", "alfa", "epizot_ort_ham", "epizot_isabet",
                                  "ep_%5", "ep_%95"])
tab(tt5, baslik="F1a_T aynı girişler, farklı çıkışlar (ham ve alfa bps; epizot = arası ≥ 10 işlem günü)")
for hucre in ("STRES", "BUGUN"):
    m = RG[hucre].reindex(pd.DatetimeIndex(I_F1a["giris"])).fillna(False).values.astype(bool)
    d2 = H["h2"][0][m] - H["h1"][0][m]
    d3 = H["h3"][0][m] - H["h2"][0][m]
    yaz(f"\n{hucre}: 2. günün katkısı (h2−h1, toplamsal bps) ort {f(np.nanmean(d2))}, medyan {f(np.nanmedian(d2))}; "
        f"3. gün (h3−h2) ort {f(np.nanmean(d3))}, medyan {f(np.nanmedian(d3))}.")

# STRES epizotları tek tek (bugün VIX >= 30 ve T'nin tamamında IBS < 0,2)
mS = RG["STRES"].reindex(pd.DatetimeIndex(I_F1a["giris"])).fillna(False).values.astype(bool)
xs = I_F1a[mS].copy()
xs["h2_alfa"] = H["h2"][1][mS]
xs["h3_alfa"] = H["h3"][1][mS]
xs["ep"] = xs["giris"].map(o._epizot(xs["giris"]))
es = xs.groupby("ep").agg(bas=("giris", "min"), son=("giris", "max"), n=("alfa_bps", "size"), h1_alfa=("alfa_bps", "mean"),
                          h2_alfa=("h2_alfa", "mean"), h3_alfa=("h3_alfa", "mean"), h1_ham=("ham_bps", "mean"))
es["bas"] = es.bas.dt.date
es["son"] = es.son.dt.date
tab(es.reset_index(drop=True), baslik="F1a_T STRES (VIX ≥ 30) epizotları tek tek (işlem ortalaması, bps)")
x20 = xs[xs.giris.dt.year != 2020]
yaz(f"\nSTRES, 2020 hariç: n {len(x20)}, h1 alfa {f(x20.alfa_bps.mean())}, h2 {f(np.nanmean(x20.h2_alfa))}, "
    f"h3 {f(np.nanmean(x20.h3_alfa))}; epizot ortalamalarının medyanı h1 {f(es.h1_alfa.median())}.")
yaz(f"\nBugünkü rejim ({SON.date()}): VIX {f(RG.loc[SON, 'vix'])}, STRES {bool(RG.loc[SON, 'STRES'])}, BUGÜN {bool(RG.loc[SON, 'BUGUN'])}, "
    f"QQQ 200g üstü {bool(RG.loc[SON, 'qqq_ust'])}.")
# STRES'te IBS mi, yalnız 'VIX >= 30' mu? T'nin bütün uygun günleri, ertesi gün alfa
Y1 = o._ileri_ham(T_, 1, "kapanis").values - o._beklenen(T_, 1, "kapanis", "ham")
Ev = o.uygun(T_).values & np.isfinite(Y1) & np.isfinite(ibsT.values)
st = RG["STRES"].values.astype(bool)[:, None] & Ev
rr = []
for ad, m in (("STRES, IBS<0,2", st & (ibsT.values < 0.2)), ("STRES, IBS>=0,2", st & (ibsT.values >= 0.2)),
              ("STRES, hepsi (koşulsuz al)", st), ("STRES değil, IBS<0,2", Ev & ~st & (ibsT.values < 0.2))):
    ii, jj = np.nonzero(m)
    a = Y1[ii, jj]
    mm, t, n = kt(a, TKV[ii])
    e = pd.Series(a).groupby(pd.Series(TKV[ii]).map(o._epizot(TKV[ii])).values).mean()
    rr.append((ad, n, mm, t, len(e), (e > 0).mean(), e.median()))
tab(pd.DataFrame(rr, columns=["kesit (T, bütün günler)", "n", "ertesi gün alfa", "t_kume", "n_epizot", "epizot_isabet",
                              "epizot_medyan"]), baslik="STRES'te IBS'in katkısı")

ibsS, f1aS, _ = b1_sinyal(["SOXL"])
I_S = isl_al(f1aS, test_id="F1a>SOXL")
r_ = []
for hucre in ("tam", "STRES"):
    m = np.ones(len(I_S), bool) if hucre == "tam" else RG["STRES"].reindex(pd.DatetimeIndex(I_S["giris"])).fillna(False).values.astype(bool)
    for ad, (g, a) in {"h1": ufuk_alfa(I_S, ["SOXL"], 1), "h2": ufuk_alfa(I_S, ["SOXL"], 2), "h3": ufuk_alfa(I_S, ["SOXL"], 3),
                       "t+1 açılış": ufuk_alfa(I_S, ["SOXL"], 1, "acilis")}.items():
        epm = pd.Series(g[m]).groupby(I_S.loc[m, "giris"].map(o._epizot(I_S.loc[m, "giris"])).values).mean()
        r_.append((hucre, ad, int(m.sum()), np.nanmean(g[m]), np.nanmedian(g[m]), np.nanmean(a[m]), len(epm), epm.mean(), (epm > 0).mean()))
tab(pd.DataFrame(r_, columns=["hücre", "çıkış", "n", "ham_ort", "ham_medyan", "alfa", "n_epizot", "epizot_ort", "epizot_isabet"]),
    baslik="SOXL kendi IBS < 0,2: tutma süresi (bps)")

smh = o.fiyat("SMH")["AClose"].reindex(TKV)
rs = smh.pct_change(fill_method=None)
for esik in (-0.05, -0.08):
    olay = rs.index[(rs <= esik).values]
    epd = o._epizot(olay)
    rr = []
    for kod in ("SMH", "SOXL"):
        c = o.fiyat(kod)["AClose"].reindex(TKV)
        op = o.fiyat(kod)["AOpen"].reindex(TKV)
        i = TKV.get_indexer(olay)
        yol = {}
        for k in range(1, 6):
            yol[k] = (c.values[np.minimum(i + k, len(TKV) - 1)] / c.values[i] - 1) * 1e4
            yol[k][i + k >= len(TKV)] = np.nan
        yol["açılış1"] = (op.values[np.minimum(i + 1, len(TKV) - 1)] / c.values[i] - 1) * 1e4
        dfp = pd.DataFrame(yol, index=olay)
        dfp["ep"] = [epd[d] for d in olay]
        epm = dfp.groupby("ep").mean()
        ilk = dfp.groupby("ep").head(1)
        for k in ["açılış1", 1, 2, 3, 4, 5]:
            rr.append((kod, f"{k}", len(dfp[k].dropna()), dfp[k].mean(), dfp[k].median(), (dfp[k] > 0).mean(),
                       len(epm), epm[k].mean(), (epm[k] > 0).mean(), ilk[k].mean()))
    tab(pd.DataFrame(rr, columns=["araç", "gün", "n_olay", "ort", "medyan", "isabet", "n_epizot", "epizot_ort",
                                  "epizot_isabet", "epizotun_ilk_olayı_ort"]),
        baslik=f"SMH ≤ {int(esik*100)}% günlerinden sonra birikimli yol (kapanıştan, bps)")
    if esik == -0.08:
        lst = []
        for d in olay:
            i = TKV.get_loc(d)
            r_ = {"tarih": str(d.date()), "SMH_gun": rs.iloc[i] * 1e4, "VIX": VIX.iloc[i]}
            for kod in ("SMH", "SOXL"):
                c = o.fiyat(kod)["AClose"].reindex(TKV).values
                for k in (1, 2, 3, 5):
                    r_[f"{kod}_h{k}"] = (c[i + k] / c[i] - 1) * 1e4 if i + k < len(TKV) else np.nan
            lst.append(r_)
        tab(pd.DataFrame(lst), nd=0, baslik="SMH ≤ −8% günleri tek tek")

# ================================================================ 6) F9b
yaz("\n## 6. F9b (bilanço öncesi al, tepki kapanışında sat)\n")
I9 = I_F9b.copy()
I9["yontem"] = [meta9.get((k, g), {}).get("yontem") for k, g in zip(I9.kod, I9.giris)]
I9["yil"] = I9["giris"].dt.year
yy = []
for y, g in I9.groupby("yil"):
    m, t, n = kt(g["alfa_bps"], g["giris"])
    yy.append((y, n, m, t, g["ham_bps"].mean(), g["ham_bps"].median(), (g["ham_bps"] > 0).mean()))
tab(pd.DataFrame(yy, columns=["yıl", "n", "alfa", "t", "ham_ort", "ham_medyan", "isabet"]), baslik="Yıl yıl")
q = I9.groupby(I9["giris"].dt.to_period("Q"))
qq = [(str(p), len(g), g["alfa_bps"].mean(), g["ham_bps"].median()) for p, g in q if p >= pd.Period("2023Q1")]
tab(pd.DataFrame(qq, columns=["çeyrek", "n", "alfa", "ham_medyan"]), baslik="Çeyrek çeyrek (2023+)")
alt = []
for ad, m in (("tam", np.ones(len(I9), bool)), ("2023+", I9.giris >= "2023-01-01"),
              ("son 8 çeyrek (2024Q4–2026Q3)", (I9.giris >= "2024-10-01") & (I9.giris < "2026-10-01")),
              ("son 12 ay", I9.giris >= o.SON12_BAS), ("yöntem=saat", I9.yontem == "saat"),
              ("yöntem=hacim (saat yok, ex-post seçim)", I9.yontem == "hacim"),
              ("saat & 2023+", (I9.yontem == "saat") & (I9.giris >= "2023-01-01"))):
    g = I9[m]
    mm, t, n = kt(g["alfa_bps"], g["giris"])
    alt.append((ad, n, mm, t, mm - 15 if n else np.nan, g["ham_bps"].median()))
tab(pd.DataFrame(alt, columns=["kesit", "n", "alfa", "t", "net(~15)", "ham_medyan"]), baslik="Alt kesitler (net: işlem başı ort. sınıf maliyeti ≈ %.1f bps)" % I9.maliyet_bps.mean())
h = I9["ham_bps"].sort_values()
k5 = max(1, int(round(0.05 * len(h))))
yaz(f"\nDağılım (ham): std {f(h.std())} bps; en kötü %5 ortalaması {f(h.iloc[:k5].mean())} bps; "
    f"≤ −%10 işlem payı %{f(100 * (h <= -1000).mean())}; ≤ −%20 %{f(100 * (h <= -2000).mean())}; "
    f"en iyi %5 ortalaması {f(h.iloc[-k5:].mean())}; çarpıklık {f(h.skew(), 2)}; "
    f"en iyi %5 çıkınca alfa {f(I9.loc[~I9.index.isin(h.index[-k5:]), 'alfa_bps'].mean())}.")
w = I9.nsmallest(10, "ham_bps")[["kod", "giris", "cikis", "ham_bps", "alfa_bps", "yontem"]]
w["giris"] = w.giris.dt.date
w["cikis"] = w.cikis.dt.date
tab(w, nd=0, baslik="En kötü 10 işlem")
# tarih kayması: A-1 -> A (yalnız öncesi), A-1 -> tepki (h=2, bir gün erken alım)
F1 = o._ileri_ham(C_, 1, "kapanis").values
F2 = o._ileri_ham(C_, 2, "kapanis").values
B1 = o._beklenen(C_, 1, "kapanis", "ham")
B2 = o._beklenen(C_, 2, "kapanis", "ham")
E9 = o.uygun(C_).values
ks = []
for (k, A), mt in meta9.items():
    j = C_.index(k)
    iA = mt["iA"]
    if iA < 1 or not E9[iA, j]:
        continue
    rec = dict(kod=k, A=A, yontem=mt["yontem"])
    rec["A-1→A"] = F1[iA - 1, j] - B1[iA - 1, j]
    rec["A→T (taban)"] = F1[iA, j] - B1[iA, j]
    rec["A-1→T"] = F2[iA - 1, j] - B2[iA - 1, j]
    rec["T→T+1"] = F1[iA + 1, j] - B1[iA + 1, j] if iA + 1 < len(TKV) else np.nan
    # saat yoksa gerçekçi kural: duyuru gününden önceki kapanışta al, duyurunun ertesi günü kapanışında sat
    i0 = mt["i0"]
    if mt["yontem"] == "hacim" and i0 >= 1 and i0 + 1 < len(TKV):
        rec["gercekci_hacim"] = F2[i0 - 1, j] - B2[i0 - 1, j]
        rec["ters_secim_hacim"] = (F1[i0 - 1, j] - B1[i0 - 1, j]) if iA == i0 else (F1[i0, j] - B1[i0, j])
    ks.append(rec)
ks = pd.DataFrame(ks)
kk = []
for c_ in ["A-1→A", "A→T (taban)", "A-1→T", "T→T+1"]:
    for ad, m in (("tam", np.ones(len(ks), bool)), ("2023+", ks.A >= "2023-01-01"), ("saat", ks.yontem == "saat")):
        x = ks.loc[m, c_].dropna()
        mm, t, n = kt(x, ks.loc[x.index, "A"], 2 if "A-1→T" in c_ else 1)
        kk.append((c_, ad, n, mm, t))
hz = ks[ks.yontem == "hacim"]
for c_ in ["A→T (taban)", "gercekci_hacim", "ters_secim_hacim"]:
    x = hz[c_].dropna()
    mm, t, n = kt(x, hz.loc[x.index, "A"], 2 if c_ == "gercekci_hacim" else 1)
    kk.append((c_, "yalnız saat bilinmeyen", n, mm, t))
tab(pd.DataFrame(kk, columns=["pencere", "kesit", "n", "alfa", "t"]),
    baslik="Tarih/saat kayması (A = duyurudan önceki son kapanış, T = tepki günü)")
yaz(f"\nSaat bilgisi olmayan olay payı: tam %{f(100 * (I9.yontem == 'hacim').mean())}, 2023+ "
    f"%{f(100 * (I9[I9.giris >= '2023-01-01'].yontem == 'hacim').mean())}.")

# ================================================================ 7) kaldıraçlı taşıma
yaz("\n## 7. Kaldıraçlı taşıma (F1a kuralı aracın KENDİ IBS'iyle; maliyet 10 bps)\n")
ibsL, f1aL, _ = b1_sinyal(["SOXL", "TQQQ"])
I_L = isl_al(f1aL, test_id="F1a>ARAC")
# ek: SMH/QQQ sinyaliyle SOXL/TQQQ al
sm = pd.DataFrame({"SOXL": f1aT["SMH"], "TQQQ": f1aT["QQQ"]})
I_L2 = isl_al(sm, bilanco_at=False, test_id="F1a(SMH/QQQ)>ARAC")
ozet7 = []
for ad, isl_ in (("kendi IBS", I_L), ("SMH/QQQ IBS", I_L2)):
    for kod, g in isl_.groupby("kod"):
        g = g.sort_values("giris").reset_index(drop=True)
        net = g["ham_bps"] - 10
        kayip = (net < 0).astype(int).values
        seri, en, top, entop, cur = 0, 0, 0.0, 0.0, 0.0
        for v, kv in zip(net.values, kayip):
            if kv:
                seri += 1
                cur += v
                en = max(en, seri)
                entop = min(entop, cur)
            else:
                seri, cur = 0, 0.0
        eq = (1 + 0.33 * net / 1e4).cumprod()
        dd = (eq / eq.cummax() - 1).min()
        yil = (g["cikis"].max() - g["giris"].min()).days / 365.25
        cagr = eq.iloc[-1] ** (1 / yil) - 1
        yr = g.assign(r=1 + 0.33 * net / 1e4).groupby(g["cikis"].dt.year)["r"].prod() - 1
        p3 = g["giris"] >= "2023-01-01"
        ozet7.append(dict(sinyal=ad, kod=kod, n=len(g), ham_ort=g["ham_bps"].mean(), alfa=g["alfa_bps"].mean(),
                          t=kt(g["alfa_bps"], g["giris"])[1], ham_P3=g.loc[p3, "ham_bps"].mean(),
                          ham_son12=g.loc[g.giris >= o.SON12_BAS, "ham_bps"].mean(),
                          isabet=(net > 0).mean(), en_kotu=net.min(),
                          en_kotu_tarih=str(g.loc[net.idxmin(), "giris"].date()), en_uzun_kayip_serisi=en,
                          en_kotu_seri_toplam=entop, buyuk_dusus_33=dd * 100, ybbo_33=cagr * 100,
                          en_kotu_yil_33=yr.min() * 100, en_kotu_yil=int(yr.idxmin()), yil_2026_33=yr.get(2026, np.nan) * 100))
tab(pd.DataFrame(ozet7), baslik="Özet (%33 sermaye ile, işlem başına net getirinin bileşiği; % değerler)")
L26 = I_L[I_L["giris"] >= "2026-01-01"].copy()
L26["VIX"] = VIX.reindex(pd.DatetimeIndex(L26.giris)).values
L26["SMH_gun"] = rs.reindex(pd.DatetimeIndex(L26.giris)).values * 1e4
L26["IBS"] = [ibsL.loc[d, k] for d, k in zip(L26.giris, L26.kod)]
L26["net"] = L26["ham_bps"] - 10
L26["giris"] = L26.giris.dt.date
L26["cikis"] = L26.cikis.dt.date
tab(L26[["kod", "giris", "cikis", "IBS", "SMH_gun", "VIX", "ham_bps", "net"]], nd=2, baslik="2026 işlemleri tek tek (kendi IBS)")
for ad, (a, b) in (("4–6 Kasım", ("2026-11-02", "2026-11-06")), ("13–20 Kasım", ("2026-11-13", "2026-11-20"))):
    x = I_L[(I_L.giris >= a) & (I_L.giris <= b)]
    yaz(f"\n{ad} haftası: {len(x)} işlem, ham toplam {f(x.ham_bps.sum())} bps, ort {f(x.ham_bps.mean())}.")
ac = o.acik_sinyal = None  # noqa
son_ibs = ibsL.loc[SON]
yaz(f"\n{SON.date()} kapanışı IBS: SOXL {f(son_ibs['SOXL'], 3)}, TQQQ {f(son_ibs['TQQQ'], 3)}; T evreni: "
    + ", ".join(f"{k} {f(ibsT.loc[SON, k], 3)}" for k in T_) + f"; VIX {f(VIX.loc[SON])}.")

# ================================================================ 8) bağımlılık
yaz("\n## 8. Bağımlılık: günde tek gözlem (T ortalaması)\n")
b8 = []
for ad, isl in (("F1a_T", I_F1a), ("F3_T", I_F3)):
    d = isl.groupby("giris")["alfa_bps"].mean()
    m = d.mean()
    t_iid = m / (d.std(ddof=1) / math.sqrt(len(d)))
    # Newey-West (5) günlük takvim serisi: sinyal yoksa 0 değil, yalnız sinyal günleri
    t_nw = o._nw_t(d.values, 5) if hasattr(o, "_nw_t") else np.nan
    b8.append((ad, len(isl), len(d), isl.groupby("giris").size().mean(), m, t_iid, t_nw,
               kt(isl["alfa_bps"], isl["giris"])[1]))
tab(pd.DataFrame(b8, columns=["kural", "n_islem", "n_gun", "gün başına işlem", "gün ort alfa", "t (iid gün)",
                              "t (NW5 gün)", "t_kume (rapor yöntemi)"]), nd=2)

(o.SONUC / "D3_curutme_tablolar.md").write_text("\n".join(OUT) + "\n", encoding="utf-8")
print("yazıldı:", o.SONUC / "D3_curutme_tablolar.md")
