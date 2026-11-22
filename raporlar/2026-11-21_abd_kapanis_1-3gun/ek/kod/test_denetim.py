# -*- coding: utf-8 -*-
"""test_denetim.py - motor.py'nin BAGIMSIZ karsi testleri (kod denetimi, gorev KD).

Calistir:  python3 -I test_denetim.py            (hepsi: a b c d e)
           python3 -I test_denetim.py a b d      (secili bolumler)
Referans hesaplar motoru KULLANMAZ: dogrudan yukle.panel() + duz pandas/numpy.
  a) rastgele kurallarda islem listesinin islem islem yeniden hesabi (giris/cikis gunu, brut, beta,
     maliyet+finansman, sigma, anormal)
  b) gelecekten sizinti: 1 gun ileri kaydirilmis (hileli) sinyal devasa kenar vermeli, durust vermemeli
  c) saf gurultu kurallari: p-degeri dagilimi tekduze mi, %5'te yanlis pozitif orani
  d) SPY gece / gun ici getirileri 2005-2026: panelden dogrudan ve motorla
  e) yardimci islevler: blok permutasyon, BH, Wilcoxon, bootstrap, genisleyen esik, donem siniri,
     portfoy tavani, degerlendir satiri, SONRA gecikmesi
Kucuk sonuc tablosu: ../veri/denetim_sonuc.csv
"""
import math
import os
import sys
import time

KOD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOD)
import numpy as np
import pandas as pd
import yukle
import motor as M

T00 = time.time()
BOLUM = [a for a in sys.argv[1:] if a in "abcde"] or list("abcde")
SONUC = []          # (test, olcu, deger, gecti)
HATA = []


def kayit(test, olcu, deger, gecti=None):
    SONUC.append((test, olcu, deger, gecti))
    isaret = "" if gecti is None else ("  [GECTI]" if gecti else "  [KALDI]")
    print(f"  {test:<4} {olcu:<58} {deger}{isaret}", flush=True)
    if gecti is False:
        HATA.append(f"{test}: {olcu} = {deger}")


# ----------------------------------------------------------------------------- referans (motorsuz)
P = yukle.panel()
C = P["close"].where(P["close"] > 0)
O = P["open"].where(P["open"] > 0)
H_, L_ = P["high"], P["low"]
AC = P["adjclose"].where(P["adjclose"] > 0)
AO = O * AC / C
V = P["volume"]
EV = P["evren"].set_index("kod")
IDX = C.index
T = len(IDX)
R = AC.pct_change(fill_method=None)
VIX1 = C["^VIX"].shift(1)
IRX1 = C["^IRX"].ffill().shift(1).fillna(0.0).clip(lower=0.0)
KOVA = np.where(VIX1 > 30, 2, np.where(VIX1 >= 20, 1, 0))
KOVA[VIX1.isna().to_numpy()] = -1
_ma = C["SPY"].rolling(200).mean()
UST = pd.Series(np.where(_ma.notna(), (C["SPY"] > _ma).astype(int), -1), index=IDX).shift(1).fillna(-1).astype(int).to_numpy()
DON = np.full(T, "", dtype=object)
for _d, (_a, _b) in {"STRES": ("2005-01-01", "2009-12-31"), "IS": ("2010-01-01", "2019-12-31"),
                     "OOS": ("2020-01-01", "2023-12-31"), "SON": ("2024-01-01", "2026-11-20")}.items():
    DON[(IDX >= _a) & (IDX <= _b)] = _d
KAL = yukle.kalite().set_index("kod")["bolunmeler"]
try:
    TEM = yukle.temettu()
except Exception:
    TEM = pd.DataFrame(index=IDX)
_cache = {}


def onb(ad, y, fn):
    if (ad, y) not in _cache:
        _cache[(ad, y)] = fn(y)
    return _cache[(ad, y)]


def adv_ref(y):
    return onb("adv", y, lambda k: (C[k] * V[k]).rolling(60).mean().shift(1).to_numpy())


def carpan_ref(y):
    def f(k):
        c = np.ones(T)
        b = KAL.get(k)
        if isinstance(b, str):
            for parca in b.split():
                tarih, pay, payda = parca.split(":")
                c[np.asarray(IDX < pd.Timestamp(tarih))] *= float(pay) / float(payda)
        return c
    return onb("carpan", y, f)


def temoran_ref(y):
    def f(k):
        fa = AC[k] / C[k]
        d = 1.0 - fa.shift(1) / fa
        d = d.where(d >= 3e-4, 0.0).fillna(0.0).to_numpy()
        if k in TEM.columns:
            tb = TEM[k].reindex(IDX) / C[k].shift(1)
            tb = tb.where(tb > 0, 0.0).fillna(0.0).to_numpy()
            d = np.maximum(d, tb)
        return np.cumsum(d)
    return onb("tem", y, f)


def kademe_ref(y):
    def f(k):
        a = adv_ref(k)
        kd = np.where(a > 1e9, 1.5, np.where(a >= 200e6, 3.0, np.where(a >= 50e6, 7.0, 15.0)))
        if float(EV.at[k, "kaldirac"]) != 1.0:
            kd = kd + 1.0
        return np.maximum(kd, float(EV.at[k, "maliyet_bps"]))
    return onb("kademe", y, f)


def bacak_ref(y, gun, tip, kom):
    px = ((C if tip == "k" else O)[y].to_numpy() * carpan_ref(y))[gun]
    taban = np.maximum(kademe_ref(y)[gun], 0.005 / px * 1e4)
    if kom == "hisse":
        k = np.maximum(1.0, 0.005 * 10000.0 / px) / 10000.0 * 1e4
    elif kom == "sabit":
        k = 1.5
    else:
        k = 20.0
    return taban + k


def maliyet_ref(y, t, gi, ci, tipg, tipc, isaret, agirlik, ngun, kom):
    v = VIX1.to_numpy()
    cg = np.where((v[t] > 30) | (v[gi] > 30), 2.0, 1.0)
    cc = np.where((v[t] > 30) | (v[ci] > 30), 2.0, 1.0)
    islem = (bacak_ref(y, gi, tipg, kom) * cg + bacak_ref(y, ci, tipc, kom) * cc) / 1e4 * agirlik
    nakit = ngun * IRX1.to_numpy()[t] / 100.0 / 252.0
    tcs = temoran_ref(y)
    tem = 0.30 * (tcs[ci] - tcs[gi])
    gun = np.maximum(np.asarray((IDX[ci] - IDX[gi]).days), 1)
    zor = (~(adv_ref(y)[t] >= 50e6)) | (float(EV.at[y, "kaldirac"]) != 1.0) | (str(EV.at[y, "grup"]) == "kaldirac_ters")
    odunc = (0.005 + 0.10 * zor) * gun / 360.0
    fin = np.where(isaret > 0, nakit + tem, np.where(isaret < 0, odunc, 0.0)) * agirlik
    return islem, fin


def beta_ref(y, mk, w):
    ry, rm = R[y], R[mk]
    ok = ry.notna() & rm.notna()
    a, b = ry.where(ok), rm.where(ok)
    mp = max(w // 2, 20)
    return (a.rolling(w, min_periods=mp).cov(b) / b.rolling(w, min_periods=mp).var()).shift(1)


def ileri_ref(y, giris, h, cikis):
    """(ileri getiri serisi, giris ofseti, cikis ofseti, giris tipi, cikis tipi, tutulan gun)."""
    ac, ao = AC[y], AO[y]
    if cikis == "acilis":
        return ao.shift(-1) / ac - 1.0, 0, 1, "k", "a", 1
    if giris == "K":
        return ac.shift(-h) / ac - 1.0, 0, h, "k", "k", h
    if giris == "A":
        return ac.shift(-h) / ao.shift(-1) - 1.0, 1, h, "a", "k", h
    # G: YONTEM metni 'cikis t+h' der; motor (MOTOR.md yorum 1) t+1+h kullanir. Referans motorun tanimi.
    return ac.shift(-(h + 1)) / ac.shift(-1) - 1.0, 1, h + 1, "k", "k", h


def ref_islemler(s, y, giris, h, cikis, kor, kom):
    F, go, co, tg, tc, ngun = ileri_ref(y, giris, h, cikis)
    adv = adv_ref(y)
    ok = (s.reindex(IDX).fillna(0).to_numpy() != 0) & (adv >= 20e6) & F.notna().to_numpy()
    FH = F.copy()
    beta = pd.Series(0.0, index=IDX)
    if kor:
        mk, w = kor
        beta = beta_ref(y, mk, w)
        FM = ileri_ref(mk, giris, h, cikis)[0]
        FH = F - beta * FM
        ok &= FH.notna().to_numpy()
    # ortusmeme: zaman = 2*gun + (kapanis ? 1 : 0); yeni giris zamani >= son cikis zamani
    tut, son_cikis = [], -1
    for i in np.flatnonzero(ok):
        gz = 2 * (i + go) + (1 if tg == "k" else 0)
        if gz >= son_cikis:
            tut.append(i)
            son_cikis = 2 * (i + co) + (1 if tc == "k" else 0)
    t = np.array(tut, dtype=int)
    yon = s.reindex(IDX).fillna(0).to_numpy()[t].astype(float)
    gi, ci = t + go, t + co
    b = beta.to_numpy()[t]
    brut = yon * FH.to_numpy()[t]
    islem, fin = maliyet_ref(y, t, gi, ci, tg, tc, yon, np.ones(t.size), ngun, kom)
    if kor:
        i2, f2 = maliyet_ref(kor[0], t, gi, ci, tg, tc, -yon * np.sign(b), np.abs(b), ngun, kom)
        islem, fin = islem + i2, fin + f2
    mal = islem + fin
    # anormal: ayni ana donem x VIX(t-1) kovasindaki uygun gunlerin kosulsuz ortalamasi (>= 20 gozlem)
    x = FH.where(adv >= 20e6).to_numpy()
    taban = np.full(T, np.nan)
    # Ana ajan kurali (denetim bulgusu 4 sonrasi): hucrede 20'den az gozlem varsa taban, ayni VIX
    # kovasinin butun donemlerdeki havuzlanmis ortalamasidir (o da 20'den azsa NaN).
    for d in ("STRES", "IS", "OOS", "SON"):
        for k in (0, 1, 2):
            rows = (DON == d) & (KOVA == k)
            if not rows.any():
                continue
            if np.isfinite(x[rows]).sum() >= 20:
                taban[rows] = np.nanmean(x[rows])
            else:
                hv = x[KOVA == k]
                if np.isfinite(hv).sum() >= 20:
                    taban[rows] = np.nanmean(hv)
    sg = R[y].rolling(20).std().shift(1).to_numpy()[t]
    return pd.DataFrame({"t": t, "giris_tarihi": IDX[gi], "cikis_tarihi": IDX[ci], "yon": yon, "beta": b,
                         "brut": brut, "net": brut - mal, "islemmal": islem, "sigma20": sg,
                         "anormal": yon * (FH.to_numpy()[t] - taban[t]), "kova": KOVA[t], "ust": UST[t],
                         "donem": DON[t]})


def sinyal_uret(tur, y, x, rng):
    r = R[y]
    if tur == "dusus":
        return (r <= -x).astype(int)
    if tur == "yukselis_kisa":
        return -(r >= x).astype(int)
    if tur == "ibs":
        ibs = (C[y] - L_[y]) / (H_[y] - L_[y])
        return (ibs < 0.2).astype(int) - (ibs > 0.8).astype(int)
    if tur == "seri3":
        a = (r < 0).astype(int)
        u = (r > 0).astype(int)
        return ((a.rolling(3).sum() == 3).astype(int) - (u.rolling(3).sum() == 3).astype(int))
    u = rng.random(T)
    return pd.Series(np.where(u < 0.04, -1, np.where(u < 0.08, 1, 0)), index=IDX)


print(f"panel {C.shape}, {IDX[0].date()} -> {IDX[-1].date()}; bolumler: {BOLUM}", flush=True)
m = M.Motor()
print(f"motor yuklendi ({time.time() - T00:.1f} sn)", flush=True)
HAVUZ = [k for k in ["SPY", "QQQ", "IWM", "XLE", "XLF", "TLT", "GLD", "NVDA", "AAPL", "JPM", "XOM", "KO",
                     "TSLA", "TQQQ", "SOXL", "AMD", "BAC", "EEM", "MSFT", "XLU"]
         if k in C.columns and str(EV.at[k, "kapanis_sinifi"]) == "ABD16" and np.isfinite(EV.at[k, "maliyet_bps"])]


# ----------------------------------------------------------------------------- (a) islem islem
def bolum_a():
    print("\n(a) Islem listesi: motor vs duz pandas", flush=True)
    rng = np.random.default_rng(20261121)
    turler = ["dusus", "yukselis_kisa", "ibs", "seri3", "gurultu"]
    zorunlu = [("K", "kapanis"), ("A", "kapanis"), ("G", "kapanis"), ("K", "acilis")]
    en_kotu = {}
    toplam, uyusmayan = 0, 0
    sabit_kural = {12: ("SOXL", "yukselis_kisa", 0.03, "K", "kapanis", 2, "SPY:250", "hisse"),
                   13: ("TQQQ", "dusus", 0.03, "A", "kapanis", 1, "yok", "sabit")}
    for i in range(14):
        y = HAVUZ[int(rng.integers(len(HAVUZ)))]
        tur = turler[int(rng.integers(len(turler)))]
        x = float(rng.choice([0.01, 0.015, 0.02, 0.03]))
        g, ck = zorunlu[i] if i < 4 else zorunlu[int(rng.integers(4))]
        h = int(rng.integers(1, 4))
        kr = ["yok", "SPY:250", "SPY:60"][int(rng.integers(3))]
        if y == "SPY":
            kr = "yok"
        kom = ["hisse", "sabit", "oransal"][int(rng.integers(3))]
        if i in sabit_kural:
            if sabit_kural[i][0] not in HAVUZ:
                continue
            y, tur, x, g, ck, h, kr, kom = sabit_kural[i]
        s = sinyal_uret(tur, y, x, rng)
        e = m.islemler(s, y, giris=g, h=h, cikis=ck, korunma=kr)
        kor = None if kr == "yok" else (kr.split(":")[0], int(kr.split(":")[1]))
        r = ref_islemler(s, y, g, h, ck, kor, kom)
        toplam += len(r)
        ayni_liste = len(e) == len(r) and bool((e["t_pos"].to_numpy() == r["t"].to_numpy()).all())
        if not ayni_liste:
            uyusmayan += 1
            kayit("a", f"kural {i + 1} {y} {tur} {g}/{h}/{ck}/{kr}", f"LISTE FARKLI motor={len(e)} ref={len(r)}", False)
            continue
        f = {"giris_gunu": int((e["giris_tarihi"].to_numpy() != r["giris_tarihi"].to_numpy()).sum()),
             "cikis_gunu": int((e["cikis_tarihi"].to_numpy() != r["cikis_tarihi"].to_numpy()).sum()),
             "yon": int((e["yon"].to_numpy() != r["yon"].to_numpy()).sum()),
             "kova": int((e["kova_no"].to_numpy() != r["kova"].to_numpy()).sum()),
             "ust200": int((e["ust200"].to_numpy() != r["ust"].to_numpy()).sum()),
             "donem": int((e["donem"].to_numpy() != r["donem"].to_numpy()).sum())}
        for a, b in (("brut", "brut"), ("beta", "beta"), ("net_" + kom, "net"), ("sigma20", "sigma20"),
                     ("anormal", "anormal")):
            xa, xb = e[a].to_numpy(float), r[b].to_numpy(float)
            fark = np.abs(xa - xb)
            fark[np.isnan(xa) & np.isnan(xb)] = 0.0
            f[a] = float(np.nanmax(fark)) if fark.size else 0.0
            if np.isnan(fark).any():
                f[a] = float("inf")
        iyi = (f["giris_gunu"] + f["cikis_gunu"] + f["yon"] + f["kova"] + f["ust200"] + f["donem"] == 0
               and f["brut"] < 1e-9 and f["beta"] < 1e-6 and f["net_" + kom] < 1e-9
               and f["sigma20"] < 1e-9 and f["anormal"] < 1e-9)
        for k, v in f.items():
            kk = "net" if k.startswith("net_") else k
            en_kotu[kk] = max(en_kotu.get(kk, 0), v)
        kayit("a", f"kural {i + 1} {y} {tur} {g}/{h}/{ck}/{kr}/{kom} n={len(r)}",
              f"maks fark: brut {f['brut']:.1e} net {f['net_' + kom]:.1e} beta {f['beta']:.1e} anormal {f['anormal']:.1e}", iyi)
    kayit("a", "toplam karsilastirilan islem", toplam)
    kayit("a", "en kotu farklar (14 kural)", {k: (v if isinstance(v, int) else float(f"{v:.2e}")) for k, v in en_kotu.items()},
          uyusmayan == 0)


# ----------------------------------------------------------------------------- (b) sizinti
def bolum_b():
    print("\n(b) Gelecekten sizinti: hileli (1 gun ileri) ve durust sinyal", flush=True)
    r = R["SPY"]
    hileli = (r.shift(-1) > 0.005).astype(int)        # t gununde, t+1 getirisini biliyor
    durust = (r > 0.005).astype(int)
    out = {}
    for ad, s in (("hileli", hileli), ("durust", durust)):
        for g, h, ck in (("K", 1, "kapanis"), ("A", 1, "kapanis"), ("G", 1, "kapanis"), ("K", 1, "acilis")):
            e = m.islemler(s, "SPY", giris=g, h=h, cikis=ck, korunma="yok")
            b = e["brut"].to_numpy()
            tt = b.mean() / (b.std(ddof=1) / math.sqrt(b.size))
            out[(ad, g, ck)] = (b.mean() * 1e4, tt, (b > 0).mean(), b.size)
    hk, dk = out[("hileli", "K", "kapanis")], out[("durust", "K", "kapanis")]
    kayit("b", "hileli K h=1: brut bps / t / isabet / n", f"{hk[0]:.1f} / {hk[1]:.1f} / {hk[2]:.3f} / {hk[3]}",
          hk[0] > 50 and hk[2] > 0.999 and hk[1] > 20)
    kayit("b", "durust K h=1: brut bps / t / isabet / n", f"{dk[0]:.2f} / {dk[1]:.2f} / {dk[2]:.3f} / {dk[3]}",
          abs(dk[1]) < 4 and abs(dk[0]) < 25)
    ha, hg, hn = out[("hileli", "A", "kapanis")], out[("hileli", "G", "kapanis")], out[("hileli", "K", "acilis")]
    kayit("b", "hileli A h=1 (gun ici kisim) bps / t", f"{ha[0]:.1f} / {ha[1]:.1f}", ha[0] > 20)
    kayit("b", "hileli K->acilis (gece kisim) bps / t", f"{hn[0]:.1f} / {hn[1]:.1f}", hn[0] > 5)
    kayit("b", "hileli G h=1 (t+1 -> t+2; sizinti bitmeli) bps / t", f"{hg[0]:.2f} / {hg[1]:.2f}", abs(hg[1]) < 4)
    # gece + gun ici = kk (hizalama): hileli K = A (+) gece birlesimi
    tam_h, _ = m.bakis_testi(lambda mm: (mm.getiri(ham=True)["SPY"].shift(-1) > 0.005).astype(int))
    tam_d, _ = m.bakis_testi(lambda mm: (mm.getiri(ham=True)["SPY"] > 0.005).astype(int))
    kayit("b", "bakis_testi hileli sinyali yakaliyor / durustu geciriyor", f"{not tam_h} / {tam_d}", (not tam_h) and tam_d)
    # tek gunluk sinyal: giris/cikis gunu ve getiri elle
    i0 = int(IDX.searchsorted(pd.Timestamp("2018-02-05")))
    s1 = pd.Series(0, index=IDX)
    s1.iloc[i0] = 1
    tamam = True
    for g, h, ck, pay, payda in (("K", 2, "kapanis", AC["QQQ"].iat[i0 + 2], AC["QQQ"].iat[i0]),
                                 ("A", 2, "kapanis", AC["QQQ"].iat[i0 + 2], AO["QQQ"].iat[i0 + 1]),
                                 ("G", 2, "kapanis", AC["QQQ"].iat[i0 + 3], AC["QQQ"].iat[i0 + 1]),
                                 ("K", 1, "acilis", AO["QQQ"].iat[i0 + 1], AC["QQQ"].iat[i0])):
        e = m.islemler(s1, "QQQ", giris=g, h=h, cikis=ck)
        tamam &= len(e) == 1 and abs(e["brut"].iat[0] - (pay / payda - 1.0)) < 1e-12
    kayit("b", "tek gun sinyal (QQQ 2018-02-05): 4 giris turunde getiri elle hesapla ayni", tamam, tamam)
    # SONRA / VIX gecikmesi
    g1 = m.girdi("BTC-USD", "close").to_numpy()
    h1 = P["close"]["BTC-USD"].shift(1).to_numpy()
    ok1 = bool(np.allclose(g1, h1, equal_nan=True))
    v1 = m.girdi("^VIX", "close").to_numpy()
    ok2 = bool(np.allclose(v1, P["close"]["^VIX"].shift(1).to_numpy(), equal_nan=True))
    ok3 = bool(np.allclose(m.girdi("^VIX", "close", sizintili=True).to_numpy(), P["close"]["^VIX"].to_numpy(), equal_nan=True))
    try:
        m.girdi("BTC-USD", "close", sizintili=True)
        ok4 = False
    except ValueError:
        ok4 = True
    sonra = [k for k in C.columns if str(EV.at[k, "kapanis_sinifi"]) != "ABD16" and str(EV.at[k, "kapanis_sinifi"]) != "ONCE"]
    G = m.getiri()
    ok5 = all(np.allclose(G[k].to_numpy(), R[k].shift(1).to_numpy(), equal_nan=True) for k in sonra)
    once = [k for k in C.columns if str(EV.at[k, "kapanis_sinifi"]) == "ONCE"]
    ok6 = all(np.allclose(G[k].to_numpy(), R[k].to_numpy(), equal_nan=True) for k in once + ["SPY"])
    kayit("b", f"SONRA ({len(sonra)} kod) girdi/getiri 1 gun gecikmeli; VIX t-1; sizintili yalniz VIX",
          f"{ok1} {ok2} {ok3} {ok4} {ok5}", ok1 and ok2 and ok3 and ok4 and ok5)
    kayit("b", f"ONCE ({len(once)} kod) ve ABD16 ayni gun", ok6, ok6)
    try:
        m.islemler(pd.Series(1, index=IDX), "BTC-USD")
        ok7 = False
    except ValueError:
        ok7 = True
    kayit("b", "SONRA kod hedef olamaz", ok7, ok7)


# ----------------------------------------------------------------------------- (c) gurultu
def _p_ozet(p):
    p = np.asarray(p, float)
    p = p[np.isfinite(p)]
    u = np.sort(p)
    n = u.size
    ks = float(np.max(np.maximum(np.arange(1, n + 1) / n - u, u - np.arange(0, n) / n))) if n else np.nan
    return n, float((p < 0.05).mean()), float((p < 0.10).mean()), float(p.mean()), ks


def bolum_c():
    print("\n(c) Saf gurultu kurallari (H0 dogru): p-degeri kalibrasyonu", flush=True)
    dm = M.donem_maskesi(m.idx, "IS")
    pos = np.flatnonzero(dm)
    icerde = dm.copy()
    icerde[pos[-4:]] = False
    rng = np.random.default_rng(11)
    N = 300
    pb, pt, pw, nn = [], [], [], []
    t0 = time.time()
    for i in range(N):
        y = HAVUZ[int(rng.integers(len(HAVUZ)))]
        pr = math.exp(rng.uniform(math.log(0.01), math.log(0.25)))
        hh = int(rng.integers(1, 4))
        u = rng.random(T)
        s = np.where(u < pr / 2, -1, np.where(u < pr, 1, 0)) * icerde
        isl = m.islemler(pd.Series(s, index=m.idx), y, giris="K", h=hh, korunma="yok")
        brut = isl["brut"].to_numpy()
        x = brut / isl["sigma20"].to_numpy()
        x = x[np.isfinite(x)]
        if x.size < 10:
            continue
        seri = m.gunluk(isl, net=False).to_numpy()[dm]
        pb.append(M.bootstrap_p(seri, tekrar=2000, tohum=1000 + i))
        tt = x.mean() / (x.std(ddof=1) / math.sqrt(x.size))
        pt.append(math.erfc(abs(tt) / math.sqrt(2)))
        pw.append(M.wilcoxon_p(brut))
        nn.append(x.size)
    nn = np.array(nn)
    for ad, p in (("bootstrap", pb), ("t_olcekli (normal p)", pt), ("wilcoxon", pw)):
        n, f5, f10, ort, ks = _p_ozet(p)
        # 300 kuralda %5'in standart hatasi ~1,26 puan: kabul 2%-9%; KS %1 kritik deger ~1,63/sqrt(n)
        kayit("c1", f"simetrik +-1 gurultu, brut, IS: {ad} n={n}", f"p<0,05: {f5:.3f}  p<0,10: {f10:.3f}  ort p: {ort:.3f}  KS: {ks:.3f} (kritik {1.63 / math.sqrt(n):.3f})",
              0.02 <= f5 <= 0.09 and ks < 1.63 / math.sqrt(n))
    az = nn < 40
    if az.sum() >= 20:
        kayit("c1", f"az islemli kurallar (n<40; {int(az.sum())} kural): p<0,05 bootstrap / t / wilcoxon",
              f"{(np.array(pb)[az] < 0.05).mean():.3f} / {(np.array(pt)[az] < 0.05).mean():.3f} / {(np.nan_to_num(np.array(pw)[az], nan=1.0) < 0.05).mean():.3f}")
    uc = (np.array(pb) < 0.05) & (np.array(pt) < 0.05) & (np.nan_to_num(np.array(pw), nan=1.0) < 0.05)
    iki = ((np.array(pb) < 0.05).astype(int) + (np.array(pt) < 0.05) + (np.nan_to_num(np.array(pw), nan=1.0) < 0.05)) >= 2
    kayit("c1", "uc olcunun en az ikisi p<0,05 (UYGUN kosulu) / ucu birden", f"{iki.mean():.3f} / {uc.mean():.3f}")
    print(f"     ({time.time() - t0:.0f} sn)", flush=True)

    # c2: yalniz uzun gurultu, NET getiri (motorun raporladigi t) -> maliyet ve surukleme (drift) etkisi
    for hh in (1, 3):
        rng = np.random.default_rng(12)
        tn, tb, ta, yn = [], [], [], []
        for i in range(200):
            y = HAVUZ[int(rng.integers(len(HAVUZ)))]
            pr = math.exp(rng.uniform(math.log(0.05), math.log(0.5)))
            s = (rng.random(T) < pr).astype(int) * icerde
            isl = m.islemler(pd.Series(s, index=m.idx), y, giris="K", h=hh, korunma="yok")
            sg = isl["sigma20"].to_numpy()
            for hedefl, kol in ((tn, "net_sabit"), (tb, "brut"), (ta, "anormal")):
                x = isl[kol].to_numpy() / sg
                x = x[np.isfinite(x)]
                hedefl.append(x.mean() / (x.std(ddof=1) / math.sqrt(x.size)))
            yn.append(y)
        tn, tb, ta = np.array(tn), np.array(tb), np.array(ta)
        for ad, tt in (("NET (sabit komisyon)", tn), ("BRUT", tb), ("ANORMAL", ta)):
            kayit("c2", f"yalniz-uzun gurultu, IS, h={hh}, 200 kural, {ad}: t>=2 / t<=-2 / ort t",
                  f"{(tt >= 2).mean():.3f} / {(tt <= -2).mean():.3f} / {tt.mean():.2f}")
        d = pd.DataFrame({"y": yn, "t": tn}).groupby("y")["t"].mean().sort_values()
        kayit("c2", f"h={hh}: hedefe gore ort. net t (en dusuk 2, en yuksek 3)", f"{d.head(2).round(2).to_dict()} ... {d.tail(3).round(2).to_dict()}")

    # c3: cok hedefli, ayni gun ayni yon (kesitsel bagimlilik): t_olcekli sisiyor mu, t_kume duzeltiyor mu
    try:
        ev = pd.read_csv(os.path.join(M.VERI_DIZIN, "evren_donem_basi.csv"))
        hs = [k for k in ev.loc[ev["donem"] == "IS", "kod"].tolist() if k in m.kpos][:40]
    except Exception:
        hs = HAVUZ
    rng = np.random.default_rng(13)
    ay_tum = (m.idx.year * 12 + m.idx.month).to_numpy()
    yil_tum = m.idx.year.to_numpy()
    for hh in (1, 3):
        to, tk, pbb = [], [], []
        for i in range(100):
            u = rng.random(T)
            dsig = np.where(u < 0.05, -1, np.where(u < 0.10, 1, 0)) * icerde
            S = pd.DataFrame(np.repeat(dsig[:, None], len(hs), axis=1), index=m.idx, columns=hs)
            isl = m.islemler(S, giris="K", h=hh, korunma="yok")
            brut = isl["brut"].to_numpy()
            tp = isl["t_pos"].to_numpy()
            o = M.Motor._ozet(brut, brut, brut, isl["anormal"].to_numpy(), brut / isl["sigma20"].to_numpy(), tp,
                              isl["yon"].to_numpy(), isl["bolum"].to_numpy(), ay_tum[tp], yil_tum[tp],
                              np.zeros(len(isl)))
            to.append(o.get("t_olcekli", np.nan))
            tk.append(o.get("t_kume", np.nan))
            pbb.append(M.bootstrap_p(m.gunluk(isl, net=False).to_numpy()[dm], tekrar=1000, tohum=5000 + i))
        to, tk, pbb = np.array(to), np.array(tk), np.array(pbb)
        kayit("c3", f"{len(hs)} hedef ayni gun ayni yon, h={hh}, 100 kural: |t_olcekli|>=1,96 / |t_kume|>=1,96 / p_boot<0,05",
              f"{(np.abs(to) >= 1.96).mean():.2f} / {(np.abs(tk) >= 1.96).mean():.2f} / {(pbb < 0.05).mean():.2f}")


# ----------------------------------------------------------------------------- (d) gece / gun ici
def bolum_d():
    print("\n(d) SPY gece ve gun ici getirileri, 2005-2026", flush=True)
    ac, ao = AC["SPY"], AO["SPY"]
    gece = (ao / ac.shift(1) - 1.0).dropna()
    gun = (ac / ao - 1.0).iloc[1:]
    kk = (ac / ac.shift(1) - 1.0).dropna()
    kayit("d", f"dogrudan panel, {gece.index[0].date()} -> {gece.index[-1].date()}, {len(gece)} gun: gece toplam (basit) / bilesik",
          f"{gece.sum() * 100:.1f}% / {((1 + gece).prod() - 1) * 100:.1f}%")
    kayit("d", "dogrudan panel: gun ici toplam (basit) / bilesik", f"{gun.sum() * 100:.1f}% / {((1 + gun).prod() - 1) * 100:.1f}%")
    kayit("d", "dogrudan panel: kapanis-kapanis toplam (basit) / bilesik; (1+gece)(1+gunici)=(1+kk) hatasi",
          f"{kk.sum() * 100:.1f}% / {((1 + kk).prod() - 1) * 100:.1f}%; {float(np.abs((1 + gece) * (1 + gun) - (1 + kk)).max()):.1e}")
    s = pd.Series(1, index=IDX)
    eg = m.islemler(s, "SPY", giris="K", h=1, cikis="acilis")
    ea = m.islemler(s, "SPY", giris="A", h=1, cikis="kapanis")
    ek = m.islemler(s, "SPY", giris="K", h=1, cikis="kapanis")
    # motor: sinyal gunu t -> gece getirisi t+1 gunune aittir; dogrudan seriyle ayni gunlerde karsilastir
    dg = gece.reindex(eg["cikis_tarihi"]).to_numpy()
    da = gun.reindex(ea["cikis_tarihi"]).to_numpy()
    dk = kk.reindex(ek["cikis_tarihi"]).to_numpy()
    f1 = float(np.abs(dg - eg["brut"].to_numpy()).max())
    f2 = float(np.abs(da - ea["brut"].to_numpy()).max())
    f3 = float(np.abs(dk - ek["brut"].to_numpy()).max())
    kayit("d", f"motor (her gun al; {len(eg)} islem, ilk sinyal {eg['t'].iat[0].date()}): gece / gun ici / kk toplam",
          f"{eg['brut'].sum() * 100:.1f}% / {ea['brut'].sum() * 100:.1f}% / {ek['brut'].sum() * 100:.1f}%")
    kayit("d", "ayni gunlerde dogrudan hesap: gece / gun ici / kk toplam", f"{dg.sum() * 100:.1f}% / {da.sum() * 100:.1f}% / {dk.sum() * 100:.1f}%")
    kayit("d", "islem islem en buyuk fark: gece / gun ici / kk", f"{f1:.1e} / {f2:.1e} / {f3:.1e}", max(f1, f2, f3) < 1e-12)
    eksik = len(gece) - len(eg)
    kayit("d", "motorun kapsamadigi gun sayisi (ilk 60 gun hacim penceresi + son gun)", eksik, eksik <= 62)
    # gunluk seri toplami = islem toplami (tek hedef, ortusme yok)
    gs = m.gunluk(ek, komisyon="sabit", net=True)
    kayit("d", "gunluk seri toplami - islem net toplami (K h=1, sabit)", f"{float(gs.sum() - ek['net_sabit'].sum()):.1e}",
          abs(float(gs.sum() - ek["net_sabit"].sum())) < 1e-9)
    return {"gece": float(gece.sum()), "gun": float(gun.sum())}


# ----------------------------------------------------------------------------- (e) yardimcilar
def bolum_e():
    print("\n(e) Yardimci islevler", flush=True)
    # e1 blok permutasyon
    dm = M.donem_maskesi(m.idx, "IS")
    ar = np.arange(T)
    kova = m.rejim()["kova_no"].to_numpy()
    yil = m.idx.year.to_numpy()
    sabit, gecerli, kor = [], True, []
    x = np.random.default_rng(5).normal(size=T)
    y = 0.5 * x + np.random.default_rng(6).normal(size=T)
    c0 = np.corrcoef(x[dm], y[dm])[0, 1]
    for k in range(200):
        perm = m.blok_permutasyon(20, np.random.default_rng(k), maske=dm)
        gecerli &= bool((np.sort(perm) == ar).all()) and bool((perm[~dm] == ar[~dm]).all())
        gecerli &= bool((yil[perm] == yil).all()) and bool((kova[perm] == kova).all())
        sabit.append((perm[dm] == ar[dm]).mean())
        kor.append(np.corrcoef(x[dm], y[perm][dm])[0, 1])
    kucuk = 0
    hucre = yil * 10 + kova
    for hc in np.unique(hucre[dm]):
        n = int((dm & (hucre == hc)).sum())
        if n <= 20:
            kucuk += n
    kayit("e1", "blok_permutasyon: gecerli permutasyon, hucre (yil x VIX kovasi) ici, maske disi sabit", gecerli, gecerli)
    kayit("e1", "IS'te yerinde kalan gun orani (200 cekilis ort. / en cok); <=20 gunluk hucrelerdeki gun orani",
          f"{np.mean(sabit):.3f} / {np.max(sabit):.3f}; {kucuk / dm.sum():.3f}", np.mean(sabit) <= kucuk / dm.sum() + 0.01)
    kayit("e1", "ekili bag (korelasyon) gercek / plasebo ort. / plasebo |maks|", f"{c0:.3f} / {np.mean(kor):.4f} / {np.max(np.abs(kor)):.3f}",
          abs(np.mean(kor)) < 0.02)
    # e2 BH
    rng = np.random.default_rng(3)
    tamam = True
    for _ in range(300):
        n = int(rng.integers(1, 60))
        p = np.where(rng.random(n) < 0.3, rng.random(n) * 0.01, rng.random(n))
        q = float(rng.choice([0.05, 0.10]))
        red, _qd = M.bh(p, q)
        ps = np.sort(p)
        kk = np.flatnonzero(ps <= np.arange(1, n + 1) / n * q)
        esik = ps[kk[-1]] if kk.size else -1.0
        tamam &= bool((red == (p <= esik)).all())
    kayit("e2", "BH: 300 rastgele p kumesinde tanimdan hesapla ayni", tamam, tamam)
    # e3 Wilcoxon: bagimsiz uygulama (pandas rank) ve kucuk n icin tam dagilim
    tamam, enb = True, 0.0
    for _ in range(200):
        n = int(rng.integers(12, 200))
        xx = np.round(rng.standard_t(4, n) + rng.choice([0, 0.2]), int(rng.choice([1, 3, 6])))
        xx0 = xx[xx != 0]
        rk = pd.Series(np.abs(xx0)).rank().to_numpy()
        wp = rk[xx0 > 0].sum()
        nn = xx0.size
        _, say = np.unique(np.abs(xx0), return_counts=True)
        var = nn * (nn + 1) * (2 * nn + 1) / 24.0 - (say ** 3 - say).sum() / 48.0
        dd = wp - nn * (nn + 1) / 4.0
        z = (dd - 0.5 * np.sign(dd)) / math.sqrt(var)
        pr = math.erfc(abs(z) / math.sqrt(2))
        pm = M.wilcoxon_p(xx)
        if nn >= 10:
            enb = max(enb, abs(pr - pm))
    kayit("e3", "Wilcoxon: bagimsiz normal-yaklasim uygulamasiyla en buyuk p farki", f"{enb:.1e}", enb < 1e-12)
    # tam dagilim (n=12, bagsiz): P(W+ <= w) sayarak
    xx = np.array([1.1, -0.4, 2.3, 0.7, -0.2, 1.9, 3.1, -0.9, 0.5, 1.4, 2.8, -0.1])
    rk = pd.Series(np.abs(xx)).rank().to_numpy()
    wp = rk[xx > 0].sum()
    say = np.zeros(12 * 13 // 2 + 1)
    say[0] = 1
    for r_ in range(1, 13):
        yeni = say.copy()
        yeni[r_:] += say[:-r_]
        say = yeni
    da = say / say.sum()
    mu = 12 * 13 / 4.0
    p_tam = min(1.0, 2 * min(da[: int(wp) + 1].sum(), da[int(wp):].sum()))
    kayit("e3", "Wilcoxon n=12 ornek: tam p / motor p (normal yaklasim)", f"{p_tam:.4f} / {M.wilcoxon_p(xx):.4f}",
          abs(p_tam - M.wilcoxon_p(xx)) < 0.01)
    # e4 bootstrap: iid ve AR(1) seride kalibrasyon; guc
    rng = np.random.default_rng(4)
    for ad, phi in (("iid", 0.0), ("AR(1) phi=0,3", 0.3)):
        ps = []
        for i in range(300):
            e_ = rng.standard_t(4, 1000)
            z_ = np.empty(1000)
            z_[0] = e_[0]
            for j in range(1, 1000):
                z_[j] = phi * z_[j - 1] + e_[j]
            ps.append(M.bootstrap_p(z_, tekrar=1000, tohum=i))
        n, f5, f10, ort, ks = _p_ozet(ps)
        kayit("e4", f"bootstrap_p, {ad}, n=1000, 300 seri: p<0,05 / p<0,10 / KS", f"{f5:.3f} / {f10:.3f} / {ks:.3f}",
              0.02 <= f5 <= 0.10)
    z_ = rng.normal(0.15, 1.0, 1000)
    kayit("e4", "bootstrap_p guc: ortalama 0,15 sigma, n=1000 (t~4,7)", f"{M.bootstrap_p(z_):.4f}", M.bootstrap_p(z_) < 0.01)
    # e5 genisleyen esik / z-skor / genisleyen sira: deger ve gelecege bagimsizlik
    xs = pd.Series(np.random.default_rng(8).normal(size=800))
    ge = M.genisleyen_esik(xs, 0.1)
    tamam = all(abs(ge.iat[t] - np.quantile(xs.to_numpy()[:t], 0.1)) < 1e-12 for t in (250, 400, 799))
    tamam &= bool(ge.iloc[:250].isna().all())
    x2 = xs.copy()
    x2.iloc[500:] = 99.0
    tamam &= bool(np.allclose(M.genisleyen_esik(x2, 0.1).to_numpy()[:501], ge.to_numpy()[:501], equal_nan=True))
    zs = M.z_skor(xs, 60)
    tamam &= abs(zs.iat[300] - (xs.iat[300] - xs.iloc[240:300].mean()) / xs.iloc[240:300].std()) < 1e-10
    tamam &= bool(np.allclose(M.z_skor(x2, 60).to_numpy()[:500], zs.to_numpy()[:500], equal_nan=True))
    gsr = M.genisleyen_sira(xs)
    tamam &= abs(gsr.iat[600] - (xs.to_numpy()[:600] <= xs.iat[600]).mean()) < 1e-12
    kayit("e5", "genisleyen_esik / z_skor / genisleyen_sira: t-1'de biter, deger elle ayni", tamam, tamam)
    # e6 donem siniri
    s = pd.Series(1, index=IDX)
    e3 = m.islemler(s, "SPY", giris="K", h=3)
    tasan = e3[(e3["donem"] == "IS") & (e3["cikis_tarihi"] > pd.Timestamp("2019-12-31"))]
    kayit("e6", "donem siniri: IS'te sinyal, OOS'ta cikis (her gun al, SPY, K h=3)", f"{len(tasan)} islem; sinyal {[str(x.date()) for x in tasan['t']]}")
    ters = e3[(e3["donem"] == "OOS") & (e3["t"] < pd.Timestamp("2020-01-01"))]
    kayit("e6", "OOS etiketli ama sinyali IS'te olan islem", len(ters), len(ters) == 0)
    # e7 portfoy tavani
    hs = HAVUZ[:12]
    S = pd.DataFrame(1, index=IDX, columns=hs)
    for hh, g in ((2, "K"), (3, "A"), (1, "G")):
        ep = m.islemler(S, giris=g, h=hh)
        pfy = ep[ep["portfoyde"]]
        acik = np.zeros(T + 5, int)
        for a, b in zip(pfy["giris_tarihi"], pfy["cikis_tarihi"]):
            ia, ib = IDX.get_loc(a), IDX.get_loc(b)
            acik[(ia + 1 if g != "A" else ia):ib + 1] += 1      # pozisyonun kar/zarar yazdigi gunler
        if g == "K":
            ayni = True
            for k in hs[:4]:
                tek = m.islemler(S[k], k, giris=g, h=hh)
                cok = ep[ep["hedef"] == k]
                ayni &= len(tek) == len(cok) and bool(np.array_equal(tek["t_pos"].to_numpy(), cok["t_pos"].to_numpy())) \
                    and bool(np.allclose(tek["net_hisse"].to_numpy(), cok["net_hisse"].to_numpy(), atol=1e-14))
            kayit("e7", "cok hedefli islem listesi = hedef hedef tek listeler (4 hedef)", ayni, ayni)
            kayit("e7", "guc verilmeyince portfoye giren hedefler (12 aday, tavan 5)", sorted(pfy["hedef"].unique().tolist()))
        kayit("e7", f"portfoy tavani {g} h={hh}: en cok eszamanli pozisyon; portfoyde/toplam", f"{acik.max()}; {len(pfy)}/{len(ep)}", acik.max() <= 5)
    # e8 degerlendir satiri vs referans
    y, kom = "XLE", "hisse"
    sx = (R[y] <= -0.02).astype(int) - (R[y] >= 0.025).astype(int)
    sn = m.degerlendir(sx, y, kural_id="DEN", h=(2,), giris=("A",), gece=False, korunma=("SPY:60",), komisyon=(kom,),
                       donemler=["IS", "OOS", "SON"], rejimler=True, bootstrap=False)
    rf = ref_islemler(sx, y, "A", 2, "kapanis", ("SPY", 60), kom)
    tamam, ayr, nan_anormal = True, [], []

    def yakin(u, v, tol=1e-6):
        return (np.isnan(u) and np.isnan(v)) or abs(u - v) < tol
    yil_s, ay_s = IDX.year.to_numpy()[rf["t"].to_numpy()], (IDX.year * 12 + IDX.month).to_numpy()[rf["t"].to_numpy()]
    for dn in ("IS", "OOS", "SON"):
        for rj, msk in (("hepsi", np.ones(len(rf), bool)), ("V>30", rf["kova"].to_numpy() == 2),
                        ("V<20|UST", (rf["kova"].to_numpy() == 0) & (rf["ust"].to_numpy() == 1))):
            sec = (rf["donem"] == dn).to_numpy() & msk
            a = rf[sec]
            b = sn[(sn["donem"] == dn) & (sn["rejim"] == rj)].iloc[0]
            net = a["net"].to_numpy()
            n = net.size
            xo = (a["net"] / a["sigma20"]).to_numpy()
            tt = xo.mean() / (xo.std(ddof=1) / math.sqrt(xo.size)) if xo.size > 2 else np.nan
            iyi = (int(b["n_islem"]) == n)
            if n:
                an = a["anormal"].to_numpy()
                if np.isnan(an).any():
                    nan_anormal.append(f"{dn}/{rj}: {int(np.isnan(an).sum())}/{n}")
                k5 = max(3, int(math.ceil(0.05 * n)))
                ays = pd.Series(net).groupby(ay_s[sec]).sum()
                yls = pd.Series(net).groupby(yil_s[sec]).sum()
                bek = {"brut_bps": a["brut"].mean() * 1e4, "net_bps": net.mean() * 1e4,
                       "anormal_bps": np.nanmean(an) * 1e4 if np.isfinite(an).any() else np.nan,
                       "t_olcekli": tt, "isabet": (net > 0).mean(), "medyan_bps": np.median(net) * 1e4,
                       "en_kotu_bps": net.min() * 1e4,
                       "basabas_bps": a["brut"].mean() * 1e4 / (2 * (1 + np.abs(a["beta"]).mean())),
                       "maliyet2x_net_bps": (net - a["islemmal"].to_numpy()).mean() * 1e4,
                       "t_kume": net.mean() / (net.std(ddof=1) / math.sqrt(n)) if n > 1 else np.nan,
                       "en_iyi5suz_bps": np.sort(net)[:n - k5].mean() * 1e4 if n > k5 else np.nan,
                       "en_iyi_aysiz_bps": net[ay_s[sec] != ays.idxmax()].mean() * 1e4 if len(ays) > 1 else np.nan,
                       "pozitif_yil_orani": (yls > 0).mean(),
                       "uzun_n": (a["yon"] > 0).sum(), "kisa_n": (a["yon"] < 0).sum()}
                for kol, v in bek.items():
                    if not yakin(float(b[kol]), float(v)):
                        iyi = False
                        print("       e8 fark:", dn, rj, kol, b[kol], v)
            tamam &= bool(iyi)
            if dn == "OOS" and rj == "hepsi":
                ayr = [n, round(float(a["brut"].mean()) * 1e4, 2), round(float(net.mean()) * 1e4, 2), round(float(tt), 3)]
    kayit("e8", "degerlendir satirlari (XLE iki yonlu, A h=2, SPY:60; 3 donem x 3 rejim x 15 sutun) referansla ayni",
          f"{tamam}; OOS n/brut/net/t = {ayr}", tamam)
    kayit("e8", "anormal getirisi NaN olan islemler (hucrede < 20 gun; ortalamadan sessizce dusuyor)", "; ".join(nan_anormal) or "yok")
    # e8b p_bootstrap satiri = gunluk serinin donem kesiti
    isl = m.islemler(sx, y, giris="A", h=2, korunma="SPY:60")
    dmo = M.donem_maskesi(m.idx, "OOS")
    so = m.gunluk(isl[(isl["donem"] == "OOS")], komisyon=kom).to_numpy()[dmo]
    snb = m.degerlendir(sx, y, kural_id="DEN", h=(2,), giris=("A",), gece=False, korunma=("SPY:60",), komisyon=(kom,),
                        donemler=["OOS"], rejimler=False, bootstrap=True).iloc[0]
    kayit("e8", "p_bootstrap (OOS) = bootstrap_p(gunluk seri, OOS gunleri); yillik_net_pct ayni",
          f"{snb['p_bootstrap']:.4f} / {M.bootstrap_p(so):.4f}; {snb['yillik_net_pct']:.4f} / {so.mean() * 25200:.4f}",
          abs(snb["p_bootstrap"] - M.bootstrap_p(so)) < 1e-12 and abs(snb["yillik_net_pct"] - so.mean() * 25200) < 1e-9)
    # e13 gunluk seri: gun gun bagimsiz kurulum (korunmali A h=2 tek hedef; cok hedefli K h=2 esit agirlik)
    isl = m.islemler(sx, y, giris="A", h=2, korunma="SPY:60")
    ref_g = np.zeros(T)
    for t_, yon_, b_ in zip(isl["t_pos"].to_numpy(), isl["yon"].to_numpy(float), isl["beta"].to_numpy(float)):
        oy, om = AO[y].iat[t_ + 1], AO["SPY"].iat[t_ + 1]
        ref_g[t_ + 1] += yon_ * ((AC[y].iat[t_ + 1] - oy) / oy - b_ * (AC["SPY"].iat[t_ + 1] - om) / om)
        ref_g[t_ + 2] += yon_ * ((AC[y].iat[t_ + 2] - AC[y].iat[t_ + 1]) / oy
                                 - b_ * (AC["SPY"].iat[t_ + 2] - AC["SPY"].iat[t_ + 1]) / om)
    f1 = float(np.abs(m.gunluk(isl, net=False).to_numpy() - ref_g).max())
    f2 = abs(float(m.gunluk(isl, komisyon="oransal").sum() - isl["net_oransal"].sum()))
    ep = m.islemler(pd.DataFrame(1, index=IDX, columns=HAVUZ[:12]), giris="K", h=2)
    pfy = ep[ep["portfoyde"]]
    top, say = np.zeros(T), np.zeros(T)
    for k_, g_ in pfy.groupby("hedef"):
        tp = g_["t_pos"].to_numpy()
        a_ = AC[k_].to_numpy()
        for j in (1, 2):
            np.add.at(top, tp + j, (a_[tp + j] - a_[tp + j - 1]) / a_[tp])
            np.add.at(say, tp + j, 1)
    ref_p = np.where(say > 0, top / np.maximum(say, 1), 0.0)
    f3 = float(np.abs(m.gunluk(ep, net=False).to_numpy() - ref_p).max())
    kayit("e13", "gunluk seri gun gun: korunmali A h=2 brut fark / net toplam farki / 12 hedef esit agirlik fark",
          f"{f1:.1e} / {f2:.1e} / {f3:.1e}", f1 < 1e-12 and f2 < 1e-9 and f3 < 1e-12)
    # e12 VIX>30 bolumleri: bagimsiz hesap
    v30 = np.flatnonzero((VIX1 > 30).to_numpy())
    no = np.cumsum(np.r_[True, np.diff(v30) - 1 >= 20])
    bol = np.zeros(T, int)
    bol[v30] = no
    okb = bool((m.rejim()["bolum"].to_numpy() == bol).all())
    son5 = [str(IDX[v30[no == k]][0].date()) for k in range(max(1, no.max() - 4), no.max() + 1)]
    kayit("e12", f"VIX(t-1)>30 bolumleri bagimsiz hesapla ayni; bolum sayisi {no.max()}, VIX>30 gun {v30.size}; son 5 bolum baslangici",
          f"{okb}; {son5}", okb)
    # e9 beta / sigma / rejim: gelecege bagimsizlik (T0 sonrasi bozulunca T0 dahil oncesi ayni)
    mb = m.bozuk_kopya("2016-05-02", 3)
    i0 = int(IDX.searchsorted(pd.Timestamp("2016-05-02")))
    kp = [m.kpos[k] for k in HAVUZ]
    tamam = True
    for ad, fn in (("beta250", lambda mm: mm.beta("SPY", 250).to_numpy()), ("beta60", lambda mm: mm.beta("SPY", 60).to_numpy()),
                   ("sigma20", lambda mm: mm.sigma20().to_numpy()), ("adv60", lambda mm: mm.adv60()),
                   ("kademe", lambda mm: mm.kademe()), ("uygun", lambda mm: mm.hedef_uygun().astype(float)),
                   ("vix_1", lambda mm: mm.rejim()[["vix_1", "kova_no", "ust200", "bolum"]].to_numpy(float))):
        a, b = fn(m), fn(mb)
        if a.shape[1] == m.N:
            a, b = a[:, kp], b[:, kp]
        tamam &= bool(np.array_equal(a[:i0 + 1], b[:i0 + 1], equal_nan=True))
    kayit("e9", "beta/sigma/adv/kademe/uygun/rejim: T0 gunu dahil oncesi, T0 sonrasi veriden bagimsiz", tamam, tamam)
    a, b = m.artik_getiri(HAVUZ).to_numpy(), mb.artik_getiri(HAVUZ).to_numpy()
    ok = bool(np.array_equal(a[:i0], b[:i0], equal_nan=True))
    # deger: NVDA ~ SPY + sektor, pencere [t-250, t-1], sabitli EKK
    sk = M.GRUP_SEKTOR.get(str(EV.at["NVDA", "grup"]))
    art = m.artik_getiri("NVDA")
    enb = 0.0
    if sk in C.columns:
        for t in (1500, 3000, 5200):
            w = slice(t - 250, t)
            Z = np.column_stack([np.ones(250), R["SPY"].to_numpy()[w], R[sk].to_numpy()[w]])
            th = np.linalg.lstsq(Z, R["NVDA"].to_numpy()[w], rcond=None)[0]
            bek = R["NVDA"].iat[t] - th[1] * R["SPY"].iat[t] - th[2] * R[sk].iat[t]
            enb = max(enb, abs(bek - art.iat[t]))
    kayit("e9", f"artik_getiri: gelecege bagimsiz; NVDA~SPY+{sk} 3 gunde elle EKK ile fark", f"{ok}; {enb:.1e}", ok and enb < 1e-9)
    # e10 tarama_regresyon vs elle EKK (HC0 ve Newey-West), eksik verili
    rng = np.random.default_rng(21)
    Tn, K, N = 900, 5, 4
    X = rng.normal(size=(Tn, K))
    Y = 0.1 * X[:, [0]] + rng.normal(size=(Tn, N)) * (1 + np.abs(X[:, [1]]))
    Cy = rng.normal(size=(Tn, N))
    Co = rng.normal(size=Tn)
    X[rng.random(X.shape) < 0.05] = np.nan
    Y[rng.random(Y.shape) < 0.03] = np.nan
    Cy[rng.random(Cy.shape) < 0.02] = np.nan
    Co[rng.random(Tn) < 0.01] = np.nan
    ms = rng.random(Tn) < 0.9
    enb_b, enb_t = 0.0, 0.0
    for hac in (0, 2):
        B, TS, NN = M.tarama_regresyon(X, Y, kontrol_y=Cy, kontrol_ortak=Co, maske=ms, hac=hac, min_n=100)
        for k in range(K):
            for j in range(N):
                rows = ms & np.isfinite(Y[:, j]) & np.isfinite(Cy[:, j]) & np.isfinite(Co)
                xk = X[rows, k]
                w = np.isfinite(xk)
                Z = np.column_stack([xk, np.ones(rows.sum()), Cy[rows, j], Co[rows]])[w]
                yy = Y[rows, j][w]
                th = np.linalg.lstsq(Z, yy, rcond=None)[0]
                inv = np.linalg.inv(Z.T @ Z)
                sc = np.zeros((rows.sum(), 4))
                sc[w] = Z * (yy - Z @ th)[:, None]
                Sm = sc.T @ sc
                for lag in range(1, hac + 1):
                    Gm = sc[lag:].T @ sc[:-lag]
                    Sm = Sm + (1 - lag / (hac + 1.0)) * (Gm + Gm.T)
                n = w.sum()
                tt = th[0] / math.sqrt((inv @ Sm @ inv)[0, 0] * n / (n - 4))
                enb_b, enb_t = max(enb_b, abs(th[0] - B[k, j])), max(enb_t, abs(tt - TS[k, j]))
    kayit("e10", "tarama_regresyon (5x4 cift, eksik verili, HC0 ve NW-2): elle EKK ile en buyuk fark b / t", f"{enb_b:.1e} / {enb_t:.1e}",
          enb_b < 1e-9 and enb_t < 1e-7)
    # e11 IS disi veriden bagimsizlik: kumeleme, tekillestirme, donem basi evreni
    mb2 = m.bozuk_kopya("2020-01-02", 9)
    ks = [k for k in m.kodlar if str(EV.at[k, "kapanis_sinifi"]) == "ABD16"][:150]
    ok1 = bool((m.kumele(ks, k=30) == mb2.kumele(ks, k=30)).all())
    ok2 = m.tekillestir(ks)[0] == mb2.tekillestir(ks)[0]
    e1_, e2_ = m.donem_basi_evreni(), mb2.donem_basi_evreni()
    ok3 = all(e1_.loc[e1_["donem"] == d, "kod"].tolist() == e2_.loc[e2_["donem"] == d, "kod"].tolist() for d in ("IS", "OOS"))
    kayit("e11", "kumele / tekillestir (IS) ve donem basi evreni (IS, OOS): 2020 sonrasi veriden bagimsiz", f"{ok1} {ok2} {ok3}", ok1 and ok2 and ok3)


# ----------------------------------------------------------------------------- calistir
if __name__ == "__main__":
    for b_ in BOLUM:
        {"a": bolum_a, "b": bolum_b, "c": bolum_c, "d": bolum_d, "e": bolum_e}[b_]()
    df = pd.DataFrame(SONUC, columns=["test", "olcu", "deger", "gecti"])
    yol = os.path.join(M.VERI_DIZIN, "denetim_sonuc.csv")
    if set(BOLUM) == set("abcde"):
        df.to_csv(yol, index=False)
        print(f"\nyazildi: {yol}")
    n_g = int((df["gecti"] == True).sum())      # noqa: E712
    n_k = int((df["gecti"] == False).sum())     # noqa: E712
    print(f"\nOZET: {n_g} kontrol gecti, {n_k} kaldi, {int(df['gecti'].isna().sum())} bilgi satiri; {time.time() - T00:.0f} sn")
    for h_ in HATA:
        print("  KALDI ->", h_)
    sys.exit(1 if n_k else 0)
