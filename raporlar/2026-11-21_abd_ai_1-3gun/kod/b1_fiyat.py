"""B1 — fiyat/zamanlama aileleri (PROTOKOL.md madde 9, B1 listesi: 21 birincil test) ve tanılar.

Tek komut:  python kod/b1_fiyat.py
Çıktılar (veri/sonuc/): B1_sonuc.csv, B1_islemler.csv, B1_rejim.csv, B1_ekonomi.csv, B1_tasima.csv,
B1_1530.csv, B1_F6.csv, B1_F6_sinyal.csv, B1_acik.csv, B1_kontrol.csv, B1_ozet.md (tablo taslağı).
ortak.py değiştirilmez; imzalar aynen kullanılır.
"""
from __future__ import annotations
import sys, math, time
from pathlib import Path
import numpy as np
import pandas as pd

KOD = Path(__file__).resolve().parent
sys.path.insert(0, str(KOD))
import ortak as o  # noqa: E402

AJAN = "B1"
T0 = time.time()
TKV = o.TK()
SON = o.SON_GUN
T_, C_, Y_, A_ = o.evren("T"), o.evren("Ç"), o.evren("YENİ"), o.evren("ARAÇ")
OZEL = ["SOXL", "TQQQ", "USD", "TECL", "NVDL", "AMDL", "MUU", "DRAM", "SKHY"]
YENI_ARAC_KISA = ["DRAM", "SKHY"]          # 250 gün geçmişi olmayan, gevşek filtreli tanı
SQ5 = math.sqrt(5)


def log(*a):
    print(f"[{time.time() - T0:6.0f}s]", *a, flush=True)


# ---------------------------------------------------------------- matrisler
def M(kodlar):
    return (o._mat("AClose", kodlar), o._mat("AHigh", kodlar), o._mat("ALow", kodlar), o._mat("Volume", kodlar))


def rsi_bilesen(Cl):
    """Wilder RSI(2): ortalama kazanç/kayıp (alpha = 1/2), her sütun kendi geçerli günlerinde."""
    ag, al = {}, {}
    for c in Cl.columns:
        s = Cl[c].dropna()
        d = s.diff()
        ag[c] = d.clip(lower=0).ewm(alpha=0.5, adjust=False, min_periods=2).mean()
        al[c] = (-d).clip(lower=0).ewm(alpha=0.5, adjust=False, min_periods=2).mean()
    return pd.DataFrame(ag).reindex(Cl.index), pd.DataFrame(al).reindex(Cl.index)


def _rsi(ag, al):
    with np.errstate(all="ignore"):
        r = 100 - 100 / (1 + ag / al)
    return r.where(al > 0, 100.0).where(ag.notna() & al.notna())


def sinyaller(kodlar, syn=None):
    """Madde 9 B1 sinyalleri (t kapanışında bilinen). syn verilirse t günü C/H/L ve hacim oranı
    15:30 sentetik değerleriyle değiştirilir, geçmiş (t-1'e kadar) gerçek kalır.
    Dönüş: {ad: (bool DataFrame, güç DataFrame)}."""
    Cl, H, L, V = M(kodlar)
    Cp = Cl.shift(1)
    if syn is None:
        Ct, Ht, Lt = Cl, H, L
        vr = V / V.shift(1).rolling(20, min_periods=20).mean()
    else:
        Ct, Ht, Lt, vr = syn["C"][kodlar], syn["H"][kodlar], syn["L"][kodlar], syn["VR"][kodlar]
    with np.errstate(all="ignore"):
        ibs = (Ct - Lt) / (Ht - Lt)
    sma200 = Cl.rolling(200, min_periods=200).mean() + (Ct - Cl) / 200
    ag, al = rsi_bilesen(Cl)
    if syn is None:
        rsi = _rsi(ag, al)
    else:
        d = Ct - Cp
        rsi = _rsi(0.5 * ag.shift(1) + 0.5 * d.clip(lower=0), 0.5 * al.shift(1) + 0.5 * (-d).clip(lower=0))
    r = Ct / Cp - 1
    sd60 = (Cl / Cp - 1).rolling(60, min_periods=60).std().shift(1)        # t-1'e kadar 60 gün
    f3 = (Ct < Cp) & (Cp < Cl.shift(2)) & (Cl.shift(2) < Cl.shift(3))
    max19 = Cl.shift(1).rolling(19, min_periods=19).max()                 # t-19..t-1
    brk = Ct >= max19                                                     # C_t = son 20 kapanışın en yükseği
    out = {
        "F1a": (ibs < 0.2, 1 - ibs),
        "F1b": ((ibs < 0.2) & (Ct > sma200), 1 - ibs),
        "F1c": (ibs > 0.8, ibs),
        "F2": (rsi < 10, 100 - rsi),
        "F3": (f3, -(Ct / Cl.shift(3) - 1)),
        "F4a": (r < -2 * sd60, -r / sd60),
        "F4b": (r > 2 * sd60, r / sd60),
        "F5a": (brk & (vr > 1.5), vr),
        "F5b": (brk & (vr <= 1.5), Ct / max19 - 1),
    }
    return out


def f10_z(kodlar, syn=None):
    """z = 5 günlük birikimli artık / (60 günlük artık σ (t-1'e kadar) × √5). Artık: o._gunluk_tur 'artik'."""
    res = o._gunluk_tur(kodlar, "artik")
    sd = res.rolling(60, min_periods=60).std().shift(1)
    if syn is None:
        rt = res
    else:
        Cl = o._mat("AClose", kodlar)
        sm = o._mat("AClose", ["SMH"])["SMH"]
        b = o._beta(kodlar).shift(1)
        rk = (syn["C"][kodlar] / Cl.shift(1) - 1) * 1e4
        rs = (syn["C"]["SMH"] / sm.shift(1) - 1) * 1e4
        rt = rk - b.mul(rs, axis=0)
    cum = res.shift(1).rolling(4, min_periods=4).sum() + rt
    with np.errstate(all="ignore"):
        z = cum / (sd * SQ5)
    return z.where(sd > 0)


def cikis_sma5(kodlar):
    Cl = o._mat("AClose", kodlar)
    return Cl > Cl.rolling(5, min_periods=5).mean()


def sinyal_seti(kodlar, syn=None, f10=True):
    s = sinyaller(kodlar, syn)
    if f10:
        z = f10_z(kodlar, syn)
        s["F10a"] = (z < -2, -z)
        s["F10b"] = (z > 2, z)
    return s


# ---------------------------------------------------------------- test tanımları (madde 9)
#        ad,   aile,  varyant, kaynak, yon, h, getiri, F2 çıkışı
TANIM = [("F1a", "F1", "a", "lit", +1, 1, "ham", False),
         ("F1b", "F1", "b", "lit", +1, 1, "ham", False),
         ("F1c", "F1", "c", "lit", -1, 1, "ham", False),
         ("F2", "F2", "", "lit", +1, 3, "ham", True),
         ("F3", "F3", "", "lit", +1, 1, "ham", False),
         ("F4a", "F4", "a", "lit", +1, 1, "ham", False),
         ("F4b", "F4", "b", "lit", +1, 1, "ham", False),
         ("F5a", "F5", "a", "turev", +1, 1, "ham", False),
         ("F5b", "F5", "b", "turev", +1, 1, "ham", False),
         ("F10a", "F10", "a", "lit", +1, 1, "artik", False),
         ("F10b", "F10", "b", "lit", -1, 1, "artik", False)]
TD = {t[0]: t for t in TANIM}
EVR = {"C": C_, "T": T_}


def tid(ad, ev, h):
    return f"{ad}_{ev}_h{h}"


def isl_al(ad, kodlar, S, G, test_id, filtre=True, ek_maske=None):
    _, aile, var, kay, yon, h, get, f2 = TD[ad]
    sig = S if ek_maske is None else (S & ek_maske)
    return o.islemler(sig, h=h, getiri=get, bilanco_at=True, cikis_sinyal=cikis_sma5(kodlar) if f2 else None,
                      guc=G, test_id=test_id, filtre=filtre, yon=yon)


# ---------------------------------------------------------------- yardımcılar
def boot_ort(isl, n=2000, seed=0, sutun="alfa_bps"):
    """Giriş gününe göre blok yeniden örneklemeli %90 aralık (ortalama)."""
    if len(isl) < 2:
        return np.nan, np.nan
    g = isl.groupby("giris")[sutun].agg(["sum", "count"])
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(g), (n, len(g)))
    m = g["sum"].values[idx].sum(1) / g["count"].values[idx].sum(1)
    return np.percentile(m, 5), np.percentile(m, 95)


def vix_seri(gecikme=0):
    v = o.yukle("^VIX")["Close"].reindex(TKV)     # madde 2.3: VIX t barıyla
    return v.shift(gecikme)


def fark(isl, hi_ser, h):
    """hi (bool, tarih) gruplarında alfa farkı; gruplar tarihçe ayrık -> se = √(se1²+se0²)."""
    hi = hi_ser.reindex(pd.DatetimeIndex(isl["giris"])).values == True  # noqa: E712
    x = isl["alfa_bps"].values
    g = o._kume_etiket(isl["giris"], h)
    m1, s1, _, _ = o._kume_t(x[hi], g[hi])
    m0, s0, _, _ = o._kume_t(x[~hi], g[~hi])
    d = m1 - m0
    se = math.sqrt(s1 ** 2 + s0 ** 2) if np.isfinite(s1) and np.isfinite(s0) else np.nan
    tt = d / se if se and np.isfinite(se) and se > 0 else np.nan
    G = len(np.unique(g))
    p = 2 * o._st.t.sf(abs(tt), max(G - 2, 1)) if np.isfinite(tt) else np.nan
    return dict(d=d, se=se, t=tt, p=p, m1=m1, m0=m0, n1=int(hi.sum()), n0=int((~hi).sum()), hi=hi)


# ---------------------------------------------------------------- 1) birincil testler
def ana_testler():
    sonuc, islem_hepsi, rejim_hepsi, isl_sakla = [], [], [], {}
    sig = {ev: sinyal_seti(k, f10=True) for ev, k in EVR.items()}
    for ad, aile, var, kay, yon, h, get, f2 in TANIM:
        evler = ["T", "C"]                       # T önce (alfa_temiz için)
        alfa_T = np.nan
        for ev in evler:
            kodlar = EVR[ev]
            birincil = 1 if (ev == "C" or aile != "F10") else 0
            S, G = sig[ev][ad]
            t_id = tid(ad, ev, h)
            isl = isl_al(ad, kodlar, S, G, t_id)
            notu = []
            if f2:
                notu.append("çıkış: C > 5g ort. ya da en geç 3. gün; alfa_h2/h3 sabit tutma")
            if aile == "F10" and ev == "T":
                notu.append("tanı: ölçüt 7 için T karşılığı (SMH artığı ≡ 0)")
            r = o.test(isl, alfa_temiz=(alfa_T if ev == "C" else np.nan), test_id=t_id, ajan=AJAN, aile=aile,
                       varyant=var, birincil=birincil, kaynak=kay, evren=ev, h=h, cikis="kapanis",
                       getiri_turu=get, yon=yon, notu="; ".join(notu))
            if ev == "T":
                alfa_T = r["alfa_bps"]
                if birincil:      # ölçüt 7: T satırı temiz havuzun kendisi -> alfa_temiz = kendi alfası
                    r["alfa_temiz"] = r["alfa_bps"]
                    r["not"] = "; ".join([x for x in [r.get("not", ""), "alfa_temiz = kendi alfası (T)"] if x])
            sonuc.append(r)
            isl_sakla[t_id] = isl
            islem_hepsi.append(isl)
            if birincil:
                rejim_hepsi.append(o.rejim(isl))
            log(t_id, "n", r["n_islem"], "alfa %.1f t %.2f" % (r["alfa_bps"], r["t_kume"]))
    return sonuc, islem_hepsi, rejim_hepsi, isl_sakla, sig


def f1d(sig, gecikme=0, birincil=1):
    """F1d: F1a alfasının VIX >= 25 eksi VIX < 25 farkı, Ç+T birlikte."""
    kodlar = C_ + T_
    S = pd.concat([sig["C"]["F1a"][0], sig["T"]["F1a"][0]], axis=1)
    G = pd.concat([sig["C"]["F1a"][1], sig["T"]["F1a"][1]], axis=1)
    t_id = "F1d_CT_h1" if gecikme == 0 else "F1d_CT_h1_vixt1"
    isl = o.islemler(S, h=1, getiri="ham", bilanco_at=True, guc=G, test_id=t_id, yon=1)
    hi_ser = vix_seri(gecikme) >= 25
    f = fark(isl, hi_ser, 1)
    r = {c: np.nan for c in o.SONUC_SUTUN}
    hi = f["hi"]
    x = isl["alfa_bps"].values
    r.update(test_id=t_id, ajan=AJAN, aile="F1", varyant="d", birincil=birincil, kaynak="lit", evren="C+T", h=1,
             cikis="kapanis", getiri_turu="ham", yon=1, n_islem=len(isl), n_gun=isl["giris"].nunique(),
             n_arac=isl["kod"].nunique(), ilk_tarih=str(isl["giris"].min().date()),
             son_tarih=str(isl["giris"].max().date()), ort_bps=isl.loc[hi, "getiri_bps"].mean(),
             kosulsuz_bps=(isl["getiri_bps"] - isl["alfa_bps"]).mean(), alfa_bps=f["d"], se_bps=f["se"],
             t_kume=f["t"], p_kume=f["p"], p_birincil=f["p"], mde_bps=2.84 * f["se"],
             medyan_bps=np.median(x[hi]) - np.median(x[~hi]), isabet=(isl.loc[hi, "getiri_bps"] > 0).mean())
    mal = isl.loc[hi, "maliyet_bps"].mean()
    r.update(maliyet_bps=mal, alfa_net_bps=f["m1"] - mal, alfa_net_2x_bps=f["m1"] - 2 * mal,
             mutlak_net_bps=isl.loc[hi, "getiri_bps"].mean() - mal)
    r["alfa_ham_bps"] = f["d"]
    # en iyi %1 (en az 10) yüksek-VIX işlemi ve en iyi 5 yüksek-VIX giriş günü çıkınca fark
    xi = isl[hi]
    k = max(10, math.ceil(0.01 * len(xi)))
    at = xi["alfa_bps"].nlargest(k).index
    r["alfa_ust1suz_bps"] = isl.loc[hi].drop(at)["alfa_bps"].mean() - f["m0"]
    gun = xi.groupby("giris")["alfa_bps"].sum().nlargest(5).index
    r["alfa_5gunsuz_bps"] = xi[~xi["giris"].isin(gun)]["alfa_bps"].mean() - f["m0"]
    dn = o._donem_no(isl["giris"])
    for p_, ad in enumerate(["P1", "P2", "P3"]):
        ff = fark(isl[dn == p_], hi_ser, 1)
        r[f"alfa_{ad}"], r[f"t_{ad}"], r[f"n_{ad}"] = ff["d"], ff["t"], ff["n1"]
    ff = fark(isl[isl["giris"] >= o.SON12_BAS], hi_ser, 1)
    r["alfa_son12"], r["t_son12"], r["n_son12"] = ff["d"], ff["t"], ff["n1"]
    # t_takvim: günlük açık pozisyon fazla getirisi, giriş günü VIX >= 25 kuklasına HAC(5) regresyon
    ts = o._takvim_serisi(isl)
    hv = hi_ser.reindex(TKV).shift(1).reindex(ts.index).fillna(False)
    try:
        r["t_takvim"] = o._hac_fark_t(pd.Series(ts.values, dtype=float), pd.Series(hv.values.astype(float)), 5)[1]
    except Exception:
        r["t_takvim"] = np.nan
    # p_perm: VIX >= 25 göstergesi dairesel kaydırılır (sinyal matrisi yerine), 500 tekrar, iki yönlü
    hv_arr = hi_ser.reindex(TKV).fillna(False).values
    ii = TKV.get_indexer(pd.DatetimeIndex(isl["giris"]))
    pa = []
    for kk in o._kaydirmalar(500, len(TKV), 0):
        hh = np.roll(hv_arr, int(kk))[ii]
        if hh.any() and (~hh).any():
            pa.append(x[hh].mean() - x[~hh].mean())
    pa = np.array(pa)
    r["p_perm"] = (np.sum(np.abs(pa) >= abs(f["d"])) + 1) / (len(pa) + 1)
    # ikincil: h2, h3, açılış çıkışı farkları
    for ad_, hh_, cx in (("alfa_h2_bps", 2, "kapanis"), ("alfa_h3_bps", 3, "kapanis"), ("alfa_acilis_bps", 1, "acilis")):
        y = o.islemler(S, h=hh_, cikis=cx, getiri="ham", bilanco_at=True)
        r[ad_] = fark(y, hi_ser, hh_)["d"]
    ft = fark(isl[isl["kod"].isin(T_)], hi_ser, 1)
    r["alfa_temiz"] = ft["d"]
    r["supheli"] = bool((np.isfinite(f["t"]) and abs(f["t"]) > 5) or abs(f["d"]) > 100)
    r["not"] = (f"fark testi: VIX>=25 n={f['n1']} alfa {f['m1']:.1f}; VIX<25 n={f['n0']} alfa {f['m0']:.1f}; "
                f"alfa_net = yüksek-VIX alfa - maliyet; p_perm VIX göstergesi kaydırılarak; "
                f"VIX {'t' if gecikme == 0 else 't-1'} barı")
    if r["supheli"]:
        r["not"] += "; ŞÜPHELİ: |t|>5 ya da |alfa|>100 bps"
    log(t_id, "fark %.1f t %.2f (hi %d, lo %d)" % (f["d"], f["t"], f["n1"], f["n0"]))
    return r, isl, hi_ser


# ---------------------------------------------------------------- 2) 15:30 testi (madde 7)
def saatlik_sentetik(kodlar):
    """Kod başına günlük: P1530 (15:30 barı açılışı), C1530 (15:30 barı kapanışı), Hh/Ll (09:30-14:30 barları),
    Vp (09:30-14:30 hacmi). Yalnız tam günler (7 bar, son bar 15:30)."""
    Cd = o._mat("AClose", kodlar)
    C, H, L, VR, S30 = {}, {}, {}, {}, {}
    for k in kodlar:
        h = o.yukle(k, saatlik=True)
        gun = pd.DatetimeIndex(h.index.tz_localize(None).normalize())
        saat = h.index.strftime("%H:%M")
        df = pd.DataFrame({"gun": gun, "saat": saat, "O": h["Open"].values, "C": h["Close"].values,
                           "H": h["High"].values, "L": h["Low"].values, "V": h["Volume"].values})
        n = df.groupby("gun").size()
        son = df.groupby("gun")["saat"].last()
        tam = n.index[(n == 7) & (son == "15:30")]
        df = df[df["gun"].isin(tam)]
        b15 = df[df["saat"] == "15:30"].set_index("gun")
        once = df[df["saat"] <= "14:30"].groupby("gun")
        p1530, c1530 = b15["O"], b15["C"]
        hh, ll, vp = once["H"].max(), once["L"].min(), once["V"].sum()
        a = Cd[k].reindex(p1530.index)
        f = a / c1530
        cs = a * p1530 / c1530
        C[k] = cs
        H[k] = np.maximum(hh * f, cs)
        L[k] = np.minimum(ll * f, cs)
        VR[k] = vp / vp.shift(1).rolling(20, min_periods=20).mean()   # aynı saat dilimi hacmi, önceki 20 tam gün
        S30[k] = (c1530 / p1530 - 1) * 1e4
    tr = lambda d: pd.DataFrame(d).reindex(TKV)  # noqa: E731
    return dict(C=tr(C), H=tr(H), L=tr(L), VR=tr(VR), S30=tr(S30))


def tez_1530(syn, sig_gun, kontrol):
    rows = []
    for ev, kodlar in EVR.items():
        sig_b = sinyal_seti(kodlar, syn, f10=True)
        gecerli = syn["C"][kodlar].notna()
        for ad, aile, var, kay, yon, h, get, f2 in TANIM:
            if aile == "F10" and ev == "T":
                continue
            t_id = tid(ad, ev, h)
            SA, GA = sig_gun[ev][ad]
            SB, GB = sig_b[ad]
            iA = isl_al(ad, kodlar, SA & gecerli, GA, t_id)
            iB = isl_al(ad, kodlar, SB & gecerli, GB, t_id)
            rows.append(_1530_satir(t_id, iA, iB, syn, kodlar, get))
    # F1d: A = VIX t, B/C = VIX t-1 (15:30'da bilinen)
    kodlar = C_ + T_
    gec = syn["C"][kodlar].notna()
    sig_b = {ev: sinyal_seti(EVR[ev], syn, f10=False) for ev in EVR}
    SA = pd.concat([sig_gun["C"]["F1a"][0], sig_gun["T"]["F1a"][0]], axis=1) & gec
    SB = pd.concat([sig_b["C"]["F1a"][0], sig_b["T"]["F1a"][0]], axis=1) & gec
    iA = o.islemler(SA, h=1, bilanco_at=True)
    iB = o.islemler(SB, h=1, bilanco_at=True)
    s30 = _s30(iB, syn, kodlar, "ham")
    iC = iB.copy()
    iC["alfa_bps"] = ((1 + iB["getiri_bps"] / 1e4) * (1 + s30 / 1e4) - 1) * 1e4 - (iB["getiri_bps"] - iB["alfa_bps"])
    hA, hB = vix_seri(0) >= 25, vix_seri(1) >= 25
    a, b, c = fark(iA, hA, 1)["d"], fark(iB, hB, 1)["d"], fark(iC, hB, 1)["d"]
    rows.append(dict(test_id="F1d_CT_h1", n_A=len(iA), n_B=len(iB), uyum_A_B=_uyum(iA, iB), uyum_B_A=_uyum(iB, iA),
                     A_bps=a, B_bps=b, C_bps=c, son30dk_bps=np.nanmean(s30), oran_B_A=b / a if a else np.nan,
                     not_="fark; B/C'de VIX t-1"))
    return pd.DataFrame(rows).rename(columns={"not_": "not"})


def _uyum(x, y):
    a = set(zip(x["giris"], x["kod"]))
    b = set(zip(y["giris"], y["kod"]))
    return len(a & b) / len(a) if a else np.nan


def _s30(isl, syn, kodlar, get):
    t = pd.DatetimeIndex(isl["giris"])
    S = syn["S30"]
    v = np.array([S.at[g, k] for g, k in zip(t, isl["kod"])], float)
    if get == "artik":
        b = o._beta(kodlar)
        sm = S["SMH"].reindex(t).values
        bb = np.array([b.at[g, k] for g, k in zip(t, isl["kod"])], float)
        v = v - bb * sm
    return v


def _1530_satir(t_id, iA, iB, syn, kodlar, get):
    s30 = _s30(iB, syn, kodlar, get) if len(iB) else np.array([])
    bek = iB["getiri_bps"] - iB["alfa_bps"]
    cC = ((1 + iB["getiri_bps"] / 1e4) * (1 + s30 / 1e4) - 1) * 1e4 - bek
    a, b = iA["alfa_bps"].mean(), iB["alfa_bps"].mean()
    return dict(test_id=t_id, n_A=len(iA), n_B=len(iB), uyum_A_B=_uyum(iA, iB), uyum_B_A=_uyum(iB, iA),
                A_bps=a, B_bps=b, C_bps=cC.mean(), son30dk_bps=np.nanmean(s30) if len(s30) else np.nan,
                oran_B_A=b / a if a else np.nan, not_="")


# ---------------------------------------------------------------- 3) taşıma (madde 3.2)
def tasima(sonuc, sig_cache):
    rows, isl_arac = [], {}
    adaylar = [r for r in sonuc if r["birincil"] == 1 and r.get("yon", 1) == 1 and np.isfinite(r["t_kume"])
               and abs(r["t_kume"]) >= 2]
    for r in adaylar:
        t_id = r["test_id"]
        ad = t_id.split("_")[0]
        for ev_ad, kodlar in (("YENİ", Y_), ("ARAÇ", A_)):
            if ad == "F1d":
                S = sig_cache[ev_ad]["F1a"][0]
                G = sig_cache[ev_ad]["F1a"][1]
                hi = (vix_seri(0) >= 25).reindex(TKV).fillna(False)
                msk = pd.DataFrame({k: hi for k in kodlar})
                isl = o.islemler(S & msk, h=1, bilanco_at=True, guc=G, test_id=f"F1d_{ev_ad}")
                get = "ham"
            else:
                S, G = sig_cache[ev_ad][ad]
                isl = isl_al(ad, kodlar, S, G, f"{ad}_{ev_ad}_h{TD[ad][5]}")
                get = TD[ad][6]
            isl_arac[(t_id, ev_ad)] = isl
            gruplar = [("havuz", isl)] + [(k, isl[isl["kod"] == k]) for k in kodlar]
            for k, x in gruplar:
                lo, hi_ = boot_ort(x)
                rows.append(dict(test_id=t_id, kaynak_t=r["t_kume"], evren=ev_ad, kod=k, ozel=int(k in OZEL),
                                 getiri_turu=get, n_islem=len(x), n_gun=x["giris"].nunique() if len(x) else 0,
                                 ort_bps=x["getiri_bps"].mean() if len(x) else np.nan,
                                 alfa_bps=x["alfa_bps"].mean() if len(x) else np.nan, ar05_bps=lo, ar95_bps=hi_,
                                 medyan_bps=x["getiri_bps"].median() if len(x) else np.nan,
                                 isabet=(x["getiri_bps"] > 0).mean() if len(x) else np.nan,
                                 maliyet_bps=x["maliyet_bps"].mean() if len(x) else np.nan,
                                 alfa_net_bps=(x["alfa_bps"] - x["maliyet_bps"]).mean() if len(x) else np.nan,
                                 en_kotu_bps=x["getiri_bps"].min() if len(x) else np.nan,
                                 alfa_P3_bps=x.loc[x["giris"] >= "2023-01-01", "alfa_bps"].mean() if len(x) else np.nan,
                                 n_P3=int((x["giris"] >= "2023-01-01").sum()) if len(x) else 0,
                                 alfa_son12_bps=x.loc[x["giris"] >= o.SON12_BAS, "alfa_bps"].mean() if len(x) else np.nan,
                                 filtre="tam (madde 2.2)", not_=("n<30: yalnız betimsel" if len(x) < 30 else "")))
            # 250 gün geçmişi olmayan özel kodlar: gevşek filtre tanısı (birincil=0)
            kisa = [k for k in YENI_ARAC_KISA if k in kodlar]
            if kisa and ad != "F1d":
                Sx, Gx = sinyal_seti(kisa, f10=(TD[ad][1] == "F10"))[ad]
                Cl = o._mat("AClose", kisa)
                ok = pd.DataFrame({k: (~o.fiyat(k)["bozuk"]) & (o.fiyat(k)["gercek_fiyat"] >= 3)
                                   & (o.fiyat(k)["ciro"].rolling(20, min_periods=20).median() >= 20e6) for k in kisa}).reindex(TKV).fillna(False)
                x = o.islemler(Sx & ok & Cl.notna(), h=TD[ad][5], getiri=TD[ad][6], bilanco_at=True,
                               cikis_sinyal=cikis_sma5(kisa) if TD[ad][7] else None, filtre=False)
                for k in kisa:
                    xx = x[x["kod"] == k]
                    lo, hi_ = boot_ort(xx)
                    rows.append(dict(test_id=t_id, kaynak_t=r["t_kume"], evren=ev_ad, kod=k, ozel=1, getiri_turu=TD[ad][6],
                                     n_islem=len(xx), n_gun=xx["giris"].nunique() if len(xx) else 0,
                                     ort_bps=xx["getiri_bps"].mean() if len(xx) else np.nan,
                                     alfa_bps=xx["alfa_bps"].mean() if len(xx) else np.nan, ar05_bps=lo, ar95_bps=hi_,
                                     medyan_bps=xx["getiri_bps"].median() if len(xx) else np.nan,
                                     isabet=(xx["getiri_bps"] > 0).mean() if len(xx) else np.nan,
                                     maliyet_bps=xx["maliyet_bps"].mean() if len(xx) else np.nan,
                                     alfa_net_bps=(xx["alfa_bps"] - xx["maliyet_bps"]).mean() if len(xx) else np.nan,
                                     en_kotu_bps=xx["getiri_bps"].min() if len(xx) else np.nan,
                                     filtre="tanı: 250 gün geçmiş şartı kaldırıldı", not_="birincil=0; yalnız betimsel"))
        log("taşıma", t_id)
    return pd.DataFrame(rows).rename(columns={"not_": "not"}), isl_arac


# ---------------------------------------------------------------- 4) tanılar
def f6(sonuc_isl):
    """Kod x dönem: gece (C_{t-1} -> O_t) ve gün içi (O_t -> C_t) ortalamaları; ayrıca sinyal başına
    t+1 açılışta ve t+1 kapanışta çıkışın ham farkı."""
    rows = []
    kodlar = T_ + A_ + ["DRAM", "SKHY"] + C_
    for k in kodlar:
        d = o.fiyat(k).dropna(subset=["AClose", "AOpen"]).loc[:SON]
        gece = (d["AOpen"] / d["AClose"].shift(1) - 1) * 1e4
        gi = (d["AClose"] / d["AOpen"] - 1) * 1e4
        top = (d["AClose"] / d["AClose"].shift(1) - 1) * 1e4
        for dad, (b, e) in list(o.DONEMLER.items()) + [("2021+", ("2021-01-01", "2026-11-20")),
                                                       ("son12", (str(o.SON12_BAS.date()), "2026-11-20")),
                                                       ("tam", ("2010-01-01", "2026-11-20"))]:
            m = (d.index >= b) & (d.index <= e)
            g_, i_, t_ = gece[m].dropna(), gi[m].dropna(), top[m].dropna()
            if len(t_) < 20:
                continue
            tt = lambda s: s.mean() / (s.std() / math.sqrt(len(s))) if s.std() > 0 else np.nan  # noqa: E731
            rows.append(dict(kod=k, evren=("T" if k in T_ else "ARAÇ" if k in A_ else "YENİ" if k in Y_ else "Ç"),
                             donem=dad, n_gun=len(t_), gece_bps=g_.mean(), t_gece=tt(g_), gun_ici_bps=i_.mean(),
                             t_gun_ici=tt(i_), toplam_bps=t_.mean(),
                             gece_payi=g_.mean() / (g_.mean() + i_.mean()) if (g_.mean() + i_.mean()) != 0 else np.nan,
                             gece_var_payi=g_.var() / (g_.var() + i_.var())))
    f6k = pd.DataFrame(rows)
    # sinyal başına açılış/kapanış çıkışı farkı (ham)
    srows = []
    for key, isl in sonuc_isl.items():
        if len(isl) == 0:
            continue
        kodlar = sorted(isl["kod"].unique())
        Fa = o._ileri_ham(kodlar, 1, "acilis")
        Fc = o._ileri_ham(kodlar, 1, "kapanis")
        t = pd.DatetimeIndex(isl["giris"])
        a = np.array([Fa.at[g, k] for g, k in zip(t, isl["kod"])], float)
        c = np.array([Fc.at[g, k] for g, k in zip(t, isl["kod"])], float)
        ok = np.isfinite(a) & np.isfinite(c)
        sub = isl[ok]
        for kk, msk in [("havuz", np.ones(ok.sum(), bool))] + [(k, (sub["kod"] == k).values) for k in OZEL + ["SMH", "QQQ"] if k in kodlar]:
            if msk.sum() == 0:
                continue
            aa, cc = a[ok][msk], c[ok][msk]
            d = cc - aa
            srows.append(dict(test_id=key[0] if isinstance(key, tuple) else key,
                              evren=key[1] if isinstance(key, tuple) else key.split("_")[1], kod=kk, n=int(msk.sum()),
                              acilis_cikis_bps=aa.mean(), kapanis_cikis_bps=cc.mean(), fark_gun_ici_bps=d.mean(),
                              t_fark=d.mean() / (d.std() / math.sqrt(len(d))) if len(d) > 2 and d.std() > 0 else np.nan,
                              fark_2021sonrasi_bps=d[pd.DatetimeIndex(sub["giris"][msk]) >= "2021-01-01"].mean()))
    return f6k, pd.DataFrame(srows)


def f1dyn():
    kodlar = T_
    Cl, H, L, V = M(kodlar)
    ibs = (Cl - L) / (H - L)
    isl = o.islemler(ibs < 0.2, h=3, getiri="ham", bilanco_at=True, cikis_sinyal=ibs > 0.8, guc=1 - ibs,
                     test_id="F1dyn_T_h3", yon=1)
    r = o.test(isl, test_id="F1dyn_T_h3", ajan=AJAN, aile="F1dyn", varyant="dyn", birincil=0, kaynak="lit",
               evren="T", h=3, cikis="kapanis", getiri_turu="ham", yon=1,
               notu="tanı: IBS>0,8 ilk kapanışta ya da en geç 3. gün çıkış; alfa_h2/h3 sabit tutma")
    log("F1dyn", r["n_islem"], "%.1f t %.2f" % (r["alfa_bps"], r["t_kume"]))
    return r, isl


def acik_sinyaller(sig_cache):
    """20.11.2026 kapanışında açık birincil sinyaller (filtreden geçen) + F2'de hâlâ açık pozisyonlar."""
    rows = []
    vix = vix_seri(0).loc[SON]
    for ev_ad, kodlar in (("Ç", C_), ("T", T_), ("YENİ", Y_), ("ARAÇ", A_)):
        U = o.uygun(kodlar).loc[SON]
        bm = pd.Series(o._bilanco_maske(kodlar, 1)[TKV.get_loc(SON)], index=kodlar)
        for ad, (S, G) in sig_cache[ev_ad].items():
            s = S.loc[SON].fillna(False).astype(bool)
            for k in s.index[s.values]:
                rows.append(dict(sinyal=ad, yon=TD[ad][4], evren=ev_ad, kod=k, tarih=str(SON.date()),
                                 guc=float(G.at[SON, k]) if pd.notna(G.at[SON, k]) else np.nan,
                                 filtre_gecer=bool(U[k]), bilanco_maske=bool(bm[k]),
                                 birincil_evren=bool((ev_ad == "Ç") or (ev_ad == "T" and TD[ad][1] != "F10")),
                                 not_=("F1d koşulu: VIX %.1f >= 25" % vix if ad == "F1a" and vix >= 25 else "")))
        # F2: tek pozisyon kuralıyla son 15 günü yürüt (giriş sinyal kapanışında; çıkış C > 5g ort. ya da 3. gün;
        # çıkış günü yeni giriş olabilir). 20.11 kapanışından sonra açık kalanlar listelenir.
        rows[:] = [x for x in rows if not (x["sinyal"] == "F2" and x["evren"] == ev_ad)]
        S2, U2, ex = sig_cache[ev_ad]["F2"][0], o.uygun(kodlar), cikis_sma5(kodlar)
        gun = TKV[-15:]
        for k in kodlar:
            acik = None
            for i, g in enumerate(gun):
                if acik is not None and (bool(ex.at[g, k]) or i - acik >= 3):
                    acik = None
                if acik is None and bool(S2.at[g, k]) and bool(U2.at[g, k]):
                    acik = i
            if acik is not None:
                n = len(gun) - 1 - acik
                rows.append(dict(sinyal="F2", yon=1, evren=ev_ad, kod=k, tarih=str(gun[acik].date()), guc=np.nan,
                                 filtre_gecer=True, bilanco_maske=False, birincil_evren=ev_ad in ("Ç", "T"),
                                 not_=("yeni giriş 20.11" if n == 0 else f"açık pozisyon, {n} gün taşındı")))
    return pd.DataFrame(rows).rename(columns={"not_": "not"})


def kontroller(sonuc, isl_sakla):
    """Fazla iyi sonuç (|t|>5 ya da |alfa|>100) için: (i) sinyal 1 gün geciktirilince alfa; (ii) her testten
    5 rastgele işlemin getirisi ham CSV'den bağımsız yeniden hesaplanır."""
    rows = []
    rng = np.random.default_rng(1)
    cache = {}
    for r in sonuc:
        isl = isl_sakla.get(r["test_id"])
        if isl is None or len(isl) == 0:
            continue
        sec = isl.iloc[rng.choice(len(isl), min(5, len(isl)), replace=False)]
        hata = 0.0
        for _, x in sec.iterrows():
            if x["kod"] not in cache:
                cache[x["kod"]] = pd.read_csv(o.VERI / "gunluk" / f"{o.dosya_adi(x['kod'])}.csv", index_col=0,
                                              parse_dates=True)["AClose"].dropna()
            s = cache[x["kod"]]
            i = s.index.get_loc(x["giris"])
            g = (s.iloc[i + int(x["gun"])] / s.iloc[i] - 1) * 1e4
            hata = max(hata, abs(g - x["ham_bps"]))
        row = dict(test_id=r["test_id"], supheli=r.get("supheli"), t_kume=r["t_kume"], alfa_bps=r["alfa_bps"],
                   spot_kontrol_max_hata_bps=hata)
        if r.get("supheli"):
            a = o._ctx(isl)
            lag = a["sinyal"].shift(1).fillna(False).astype(bool)
            y = o.islemler(lag, h=a["h"], getiri=a["getiri"], bilanco_at=True,
                           cikis_sinyal=a["cikis_sinyal"], test_id=r["test_id"] + "_lag1")
            m, se, tt, p = o._kume_t(y["alfa_bps"].values, o._kume_etiket(y["giris"], a["h"]))
            row.update(lag1_alfa_bps=m, lag1_t=tt, lag1_n=len(y))
        rows.append(row)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- ana akış
def main():
    sonuc, islem_hepsi, rejim_hepsi, isl_sakla, sig = ana_testler()
    r1d, isl1d, _ = f1d(sig)
    sonuc.append(r1d)
    isl_sakla["F1d_CT_h1"] = isl1d
    islem_hepsi.append(isl1d)
    rj = o.rejim(isl1d)
    rj["test_id"] = "F1d_CT_h1"
    rj["not"] = rj["not"].astype(str) + "; F1a Ç+T işlemleri (fark değil, düzey)"
    rejim_hepsi.append(rj)
    r1d1, _, _ = f1d(sig, gecikme=1, birincil=0)
    sonuc.append(r1d1)
    rd, isld = f1dyn()
    sonuc.append(rd)
    islem_hepsi.append(isld)
    isl_sakla["F1dyn_T_h3"] = isld

    # 15:30
    syn = saatlik_sentetik(sorted(set(C_ + T_)))
    t15 = tez_1530(syn, sig, None)
    o.kaydet(AJAN, t15, "1530")
    log("15:30 bitti")

    # sinyal önbelleği (YENİ, ARAÇ) -> taşıma ve açık sinyaller
    sig_cache = {"Ç": sig["C"], "T": sig["T"], "YENİ": sinyal_seti(Y_, f10=True), "ARAÇ": sinyal_seti(A_, f10=True)}
    tas, isl_arac = tasima(sonuc, sig_cache)
    o.kaydet(AJAN, tas, "tasima")

    # ekonomi: |t| >= 2 alım sinyalleri (F1d hariç: fark testi)
    ek = []
    for r in sonuc:
        if r["birincil"] != 1 or r.get("yon", 1) != 1 or not np.isfinite(r["t_kume"]) or abs(r["t_kume"]) < 2:
            continue
        if r["test_id"].startswith("F1d"):
            continue
        isl = isl_sakla[r["test_id"]]
        e = o.ekonomi(isl, "havuz", t_stat=r["t_kume"])
        ek.append(e)
        if r["evren"] == "T":
            for k in ("SMH", "QQQ"):
                ek.append(o.ekonomi(isl, k, t_stat=r["t_kume"]))
        for (tidk, ev_ad), x in isl_arac.items():
            if tidk != r["test_id"] or ev_ad != "ARAÇ":
                continue
            for k in ("SOXL", "TQQQ", "USD", "TECL", "NVDL", "AMDL", "MUU"):
                if (x["kod"] == k).sum() >= 10:
                    e2 = o.ekonomi(x, k, t_stat=r["t_kume"])
                    e2["test_id"] = r["test_id"] + "@ARAÇ"
                    e2["not"] = (e2["not"].astype(str) + "; taşıma: Kelly kaynak testin t'siyle").str.strip("; ")
                    ek.append(e2)
        log("ekonomi", r["test_id"])
    EK = pd.concat(ek, ignore_index=True) if ek else pd.DataFrame()
    o.kaydet(AJAN, EK, "ekonomi")

    # tanılar
    f6k, f6s = f6({**{k: v for k, v in isl_sakla.items() if not k.startswith("F1d")},
                   **{(k[0], k[1]): v for k, v in isl_arac.items()}})
    o.kaydet(AJAN, f6k, "F6")
    o.kaydet(AJAN, f6s, "F6_sinyal")
    ac = acik_sinyaller(sig_cache)
    o.kaydet(AJAN, ac, "acik")
    kt = kontroller(sonuc, isl_sakla)
    o.kaydet(AJAN, kt, "kontrol")

    o.kaydet(AJAN, sonuc, "sonuc")
    o.kaydet(AJAN, pd.concat(islem_hepsi, ignore_index=True), "islemler")
    o.kaydet(AJAN, pd.concat(rejim_hepsi, ignore_index=True), "rejim")
    log("hepsi yazıldı")


if __name__ == "__main__":
    main()
