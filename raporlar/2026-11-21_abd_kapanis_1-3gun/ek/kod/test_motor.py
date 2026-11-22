# -*- coding: utf-8 -*-
"""test_motor.py - motor.py testleri. Calistirma:  python3 -I test_motor.py
pytest gerekmez. Sentetik panelle calisir; gercek panel bulunursa ileriye bakma testi onunla da yapilir."""
import os
import sys
import time
import traceback

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import motor as M
from motor import Motor

GIRIS_CIKIS = [("K", 1, "kapanis"), ("K", 2, "kapanis"), ("K", 3, "kapanis"), ("A", 1, "kapanis"),
               ("A", 3, "kapanis"), ("G", 1, "kapanis"), ("G", 3, "kapanis"), ("K", 1, "acilis")]


# ----------------------------------------------------------------------------- sentetik veri
def mini(fiyat, hacim=1e7, acilis=None, adj=None, sinif=None, idx=None, evren_ek=None):
    """fiyat: {kod: kapanis dizisi}. Kucuk, elle denetlenebilir panel."""
    T = len(next(iter(fiyat.values())))
    idx = idx if idx is not None else pd.bdate_range("2021-01-04", periods=T)
    c = pd.DataFrame({k: np.asarray(v, float) for k, v in fiyat.items()}, index=idx)
    o = pd.DataFrame({k: np.asarray((acilis or {}).get(k, fiyat[k]), float) for k in fiyat}, index=idx)
    a = pd.DataFrame({k: np.asarray((adj or {}).get(k, fiyat[k]), float) for k in fiyat}, index=idx)
    v = pd.DataFrame({k: np.full(T, (hacim.get(k, 1e7) if isinstance(hacim, dict) else hacim), float)
                      for k in fiyat}, index=idx)
    ev = pd.DataFrame({"kod": list(fiyat), "tur": "hisse", "kapanis_sinifi": "ABD16",
                       "maliyet_bps": 1.5, "kaldirac": 1.0, "grup": "x"})
    for k, s in (sinif or {}).items():
        ev.loc[ev.kod == k, "kapanis_sinifi"] = s
    for k, d in (evren_ek or {}).items():
        for col, val in d.items():
            ev.loc[ev.kod == k, col] = val
    return {"open": o, "high": np.maximum(o, c), "low": np.minimum(o, c), "close": c, "adjclose": a,
            "volume": v, "evren": ev}


def sentetik(T=3100, tohum=1, ekili=0.3):
    """2014-01-02'den T is gunu. Y_{t+1} = ekili * X_t + gurultu (kapanistan kapanisa)."""
    rng = np.random.default_rng(tohum)
    idx = pd.bdate_range("2014-01-02", periods=T)
    r = {}
    r["SPY"] = rng.normal(0.0003, 0.010, T)
    r["X"] = rng.normal(0.0, 0.015, T)
    ry = rng.normal(0.0, 0.010, T)
    ry[1:] += ekili * r["X"][:-1]
    r["Y"] = ry
    for i in range(1, 9):
        r[f"H{i}"] = (0.5 + 0.15 * i) * r["SPY"] + rng.normal(0.0, 0.012, T)
    r["LEV"] = 2.0 * r["SPY"] + rng.normal(0.0, 0.002, T)
    r["BTC-USD"] = rng.normal(0.0, 0.03, T)
    # VIX: ortalamaya donen duzey, kovalarin hepsi her yil gorulsun
    lv = np.zeros(T)
    for t in range(1, T):
        lv[t] = 0.97 * lv[t - 1] + rng.normal(0.0, 0.07)
    vix = 21.0 * np.exp(lv + 0.25 * np.sin(np.arange(T) / 40.0))
    irx = 2.0 + 1.5 * np.sin(np.arange(T) / 300.0)
    close, adj, opn, vol = {}, {}, {}, {}
    for k, x in r.items():
        tr = 100.0 * np.cumprod(1.0 + x)                 # toplam getiri yolu (adjclose)
        tem = np.zeros(T)
        if k in ("H1", "SPY"):
            tem[63::63] = 0.005                           # ceyreklik %0,5 temettu
        f = np.cumprod(1.0 - tem)                         # fiyat yolu = toplam getiri * f
        cl = tr * f
        ad = cl * (f[-1] / f) / f[-1] * f[-1]             # adjclose = close * (f_son / f_t)
        ad = cl * (f[-1] / f)
        u = rng.uniform(0.2, 0.8, T)
        onc = np.r_[cl[0], cl[:-1]] * np.r_[1.0, (1.0 - tem[1:])]
        op = onc * (1.0 + u * x)
        close[k], adj[k], opn[k] = cl, ad, op
        vol[k] = np.full(T, 5e6) * rng.uniform(0.7, 1.3, T)
    vol["SPY"] *= 20
    vol["H8"] = np.full(T, 1e5)                           # ~10 mln $: hedef suzgecinden gecemez
    close["^VIX"], adj["^VIX"], opn["^VIX"] = vix, vix, vix * 1.01
    close["^IRX"], adj["^IRX"], opn["^IRX"] = irx, irx, irx
    vol["^VIX"] = np.zeros(T)
    vol["^IRX"] = np.zeros(T)
    kodlar = list(close)
    df = lambda d: pd.DataFrame({k: d[k] for k in kodlar}, index=idx)
    c, o = df(close), df(opn)
    ev = pd.DataFrame({"kod": kodlar, "tur": "hisse", "kapanis_sinifi": "ABD16", "maliyet_bps": 3.0,
                       "kaldirac": 1.0, "grup": "h_x"})
    ev = ev.set_index("kod")
    ev.loc["SPY", ["tur", "maliyet_bps"]] = ["ETF", 1.5]
    ev.loc["LEV", ["tur", "kaldirac", "grup", "maliyet_bps"]] = ["ETF", 2.0, "kaldirac_ters", 4.0]
    ev.loc["BTC-USD", ["tur", "kapanis_sinifi", "maliyet_bps"]] = ["kripto", "SONRA", 1.5]
    ev.loc["^VIX", ["tur", "kapanis_sinifi", "maliyet_bps"]] = ["endeks", "VIX1615", np.nan]
    ev.loc["^IRX", ["tur", "kapanis_sinifi", "maliyet_bps"]] = ["endeks", "ONCE", np.nan]
    ev.loc["H8", "maliyet_bps"] = 15.0
    return {"open": o, "high": np.maximum(o, c), "low": np.minimum(o, c), "close": c,
            "adjclose": df(adj), "volume": df(vol), "evren": ev.reset_index()}


_SENT = {}


def sm():
    if "m" not in _SENT:
        _SENT["m"] = Motor(sentetik())
    return _SENT["m"]


def ayni(a, b):
    a, b = np.asarray(a), np.asarray(b)
    if a.shape != b.shape:
        return False
    if a.dtype.kind in "fc":
        return bool(np.array_equal(a, b, equal_nan=True))
    return bool((a == b).all())


def kural_sinyal(m, hedefler):
    """Motorun butun guvenli yollarini kullanan ornek kural (ileriye bakma testleri icin)."""
    r = m.girdi_getiri(hedefler)
    z = z_ = M.z_skor(r, 20)
    vx = m.girdi("^VIX", alan="close")
    es = M.genisleyen_esik(vx, 0.3, 250)
    kosul = (vx > es).to_numpy()[:, None]
    art = m.artik_getiri(hedefler, sektor={h: "LEV" for h in hedefler} if "LEV" in m.kpos else None)
    sr = M.genisleyen_sira(art.abs().iloc[:, 0], 250).to_numpy()[:, None]
    s = pd.DataFrame(0, index=m.idx, columns=hedefler)
    s[(z < -1.0).to_numpy() & kosul] = 1
    s[(z > 1.0).to_numpy() & kosul & (sr > 0.2)] = -1
    return s, z_.abs()


# ----------------------------------------------------------------------------- testler
def test_ileri_getiri_hizasi():
    """Elle hesaplanmis 6 satirlik ornek."""
    ac = [100.0, 101.0, 103.0, 102.0, 105.0, 104.0]
    ao = [99.5, 100.5, 102.0, 103.5, 104.0, 106.0]
    m = Motor(mini({"Z": ac}, acilis={"Z": ao}))
    nan = np.nan
    bekle = {
        ("K", 1, "kapanis"): [101 / 100 - 1, 103 / 101 - 1, 102 / 103 - 1, 105 / 102 - 1, 104 / 105 - 1, nan],
        ("K", 2, "kapanis"): [103 / 100 - 1, 102 / 101 - 1, 105 / 103 - 1, 104 / 102 - 1, nan, nan],
        ("K", 3, "kapanis"): [102 / 100 - 1, 105 / 101 - 1, 104 / 103 - 1, nan, nan, nan],
        ("A", 1, "kapanis"): [101 / 100.5 - 1, 103 / 102 - 1, 102 / 103.5 - 1, 105 / 104 - 1, 104 / 106 - 1, nan],
        ("A", 2, "kapanis"): [103 / 100.5 - 1, 102 / 102 - 1, 105 / 103.5 - 1, 104 / 104 - 1, nan, nan],
        ("G", 1, "kapanis"): [103 / 101 - 1, 102 / 103 - 1, 105 / 102 - 1, 104 / 105 - 1, nan, nan],
        ("G", 2, "kapanis"): [102 / 101 - 1, 105 / 103 - 1, 104 / 102 - 1, nan, nan, nan],
        ("K", 1, "acilis"): [100.5 / 100 - 1, 102 / 101 - 1, 103.5 / 103 - 1, 104 / 102 - 1, 106 / 105 - 1, nan],
    }
    for (g, h, c), b in bekle.items():
        f = m.ileri(g, h, c)["Z"].to_numpy()
        assert np.allclose(f, b, equal_nan=True, rtol=0, atol=1e-14), (g, h, c, f, b)
    kk = m.getiri("kk")["Z"].to_numpy()
    assert np.isnan(kk[0]) and np.isclose(kk[2], 103 / 101 - 1)
    assert np.isclose(m.getiri("gece")["Z"].to_numpy()[3], 103.5 / 103 - 1)
    assert np.isclose(m.getiri("gunici")["Z"].to_numpy()[3], 102 / 103.5 - 1)


def test_gecikme_siniflari():
    m = sm()
    for alan in ("adjclose", "close", "open", "volume"):
        for k in ("BTC-USD", "^VIX"):
            assert ayni(m.girdi(k, alan).to_numpy(), m.df(alan, ham=True)[k].shift(1).to_numpy()), (k, alan)
        for k in ("SPY", "^IRX", "X"):
            assert ayni(m.girdi(k, alan).to_numpy(), m.df(alan, ham=True)[k].to_numpy()), (k, alan)
    assert ayni(m.girdi("^VIX", "close", sizintili=True).to_numpy(), m.df("close", ham=True)["^VIX"].to_numpy())
    for fn in (lambda: m.girdi("BTC-USD", sizintili=True), lambda: m.girdi_getiri("BTC-USD", sizintili=True)):
        try:
            fn()
            raise AssertionError("SONRA sinifi ayni gun verildi")
        except ValueError:
            pass
    ham = m.getiri("kk", ham=True)
    assert ayni(m.getiri("kk").to_numpy(), m.girdi_getiri(m.kodlar).to_numpy())
    assert ayni(m.df("close")["BTC-USD"].to_numpy(), m.df("close", ham=True)["BTC-USD"].shift(1).to_numpy())
    g = m.girdi_getiri(["SPY", "BTC-USD", "^VIX"])
    assert ayni(g["SPY"].to_numpy(), ham["SPY"].to_numpy())
    assert ayni(g["BTC-USD"].to_numpy(), ham["BTC-USD"].shift(1).to_numpy())
    assert ayni(g["^VIX"].to_numpy(), ham["^VIX"].shift(1).to_numpy())
    assert ayni(m.girdi(["SPY", "^VIX"])["^VIX"].to_numpy(), m.df("adjclose", ham=True)["^VIX"].shift(1).to_numpy())
    art = m.artik_getiri(["BTC-USD"], guvenli=True)["BTC-USD"]
    art0 = m.artik_getiri(["BTC-USD"], guvenli=False)["BTC-USD"]
    assert ayni(art.to_numpy(), art0.shift(1).to_numpy())
    # SONRA / endeks hedef olamaz
    s = pd.Series(1, index=m.idx)
    for k in ("BTC-USD", "^VIX", "^IRX"):
        try:
            m.islemler(s, k)
            raise AssertionError(f"{k} hedef kabul edildi")
        except ValueError:
            pass
    # rejim VIX(t-1) kullanir
    rj = m.rejim()
    v = m.df("close", ham=True)["^VIX"].to_numpy()
    assert ayni(rj["vix_1"].to_numpy()[1:], v[:-1])
    i = 500
    bek = 2 if v[i - 1] > 30 else (1 if v[i - 1] >= 20 else 0)
    assert rj["kova_no"].iat[i] == bek


def test_ekili_lead_lag():
    """Y_{t+1} = 0,3 X_t + gurultu: Giris K, h=1'de bulunur; Giris G'de kaybolur."""
    m = sm()
    rx = m.girdi_getiri("X")
    s = np.sign(rx).fillna(0).astype(int)

    def tstat(x):
        return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))
    k = m.islemler(s, "Y", giris="K", h=1)
    g = m.islemler(s, "Y", giris="G", h=1)
    a = m.islemler(s, "Y", giris="A", h=1)
    assert len(k) > 2500 and len(g) > 2500
    tk, tg, ta = tstat(k["brut"]), tstat(g["brut"]), tstat(a["brut"])
    assert tk > 10, tk
    assert abs(tg) < 3, tg
    assert 0 < ta < tk, (ta, tk)
    assert abs(k["brut"].mean() - 0.3 * rx.abs().mean()) < 4e-4
    # ayni sey tarama regresyonunda: katsayi ~0,3
    Yf = m.ileri("K", 1)[["Y"]]
    b, t, n = M.tarama_regresyon(m.girdi_getiri(["X", "H1"]), Yf, kontrol_y=m.getiri("kk")[["Y"]],
                                 kontrol_ortak=m.getiri("kk")["SPY"])
    assert abs(b.loc["X", "Y"] - 0.3) < 0.05 and t.loc["X", "Y"] > 10 and abs(t.loc["H1", "Y"]) < 3.5
    bg, tg2, _ = M.tarama_regresyon(m.girdi_getiri(["X"]), m.ileri("G", 1)[["Y"]],
                                    kontrol_y=m.getiri("kk")[["Y"]], kontrol_ortak=m.getiri("kk")["SPY"])
    assert abs(tg2.loc["X", "Y"]) < 3.5
    # degerlendir de gormeli
    r = m.degerlendir(s, "Y", kural_id="T1", h=(1,), giris=("K", "G"), gece=False, korunma="yok",
                      komisyon="sabit", donemler=["IS"], rejimler=False, bootstrap=True)
    rk = r[r.giris == "K"].iloc[0]
    rg = r[r.giris == "G"].iloc[0]
    assert rk.t_olcekli > 8 and rk.p_bootstrap < 0.01 and rk.p_wilcoxon < 0.001
    assert rg.net_bps < 0 and rk.net_bps > 20


def _yol_karsilastir(m, m2, i0, hedefler, etiket):
    """T0 (konum i0) oncesindeki butun turetilmis girdiler bit duzeyinde ayni olmali."""
    kontrol = {}
    for alan in ("adjclose", "close", "open", "high", "low", "volume", "adjopen"):
        kontrol["girdi:" + alan] = lambda mm, a=alan: mm.girdi(mm.kodlar, a).to_numpy()
    for tur in ("kk", "gece", "gunici"):
        kontrol["girdi_getiri:" + tur] = lambda mm, t=tur: mm.girdi_getiri(mm.kodlar, t).to_numpy()
    kontrol["beta250"] = lambda mm: mm.beta("SPY", 250).to_numpy()
    kontrol["beta60"] = lambda mm: mm.beta("SPY", 60).to_numpy()
    kontrol["sigma20"] = lambda mm: mm.sigma20().to_numpy()
    kontrol["adv60"] = lambda mm: mm.adv60()
    kontrol["kademe"] = lambda mm: mm.kademe()
    kontrol["hedef_uygun"] = lambda mm: mm.hedef_uygun()
    kontrol["temettu"] = lambda mm: mm.temettu_orani()
    kontrol["temettu_kum"] = lambda mm: (mm.temettu_orani(), mm._c["temcs"])[1]
    kontrol["ham_fiyat_k"] = lambda mm: mm.ham_fiyat("k")
    kontrol["ham_fiyat_a"] = lambda mm: mm.ham_fiyat("a")
    kontrol["irx"] = lambda mm: mm._irx1()
    kontrol["zor"] = lambda mm: mm._zor("oto")
    for c in ("vix_1", "kova_no", "ust200", "bolum"):
        kontrol["rejim:" + c] = lambda mm, c=c: mm.rejim()[c].to_numpy()
    kontrol["rejim:ad"] = lambda mm: (mm.rejim()["rejim"].to_numpy() == mm.rejim()["rejim"].to_numpy())
    kontrol["artik"] = lambda mm: mm.artik_getiri(hedefler).to_numpy()
    kontrol["artik_tek"] = lambda mm: mm.artik_getiri(hedefler, sektor=None).to_numpy()
    kontrol["gen_esik"] = lambda mm: M.genisleyen_esik(mm.girdi_getiri(hedefler), 0.9).to_numpy()
    kontrol["gen_sira"] = lambda mm: M.genisleyen_sira(mm.girdi_getiri(hedefler[:2])).to_numpy()
    kontrol["z_skor"] = lambda mm: M.z_skor(mm.girdi_getiri(hedefler), 20).to_numpy()
    kp = np.array([m.kpos[h] for h in hedefler])
    gg, kk = np.meshgrid(np.arange(m.T), kp, indexing="ij")
    for kom in M.KOMISYONLAR:
        for tip in ("k", "a"):
            kontrol[f"bacak:{kom}:{tip}"] = lambda mm, kom=kom, tip=tip: mm.bacak_bps(gg, kk, tip, kom)
    for ad, fn in kontrol.items():
        a, b = np.asarray(fn(m)), np.asarray(fn(m2))
        assert ayni(a[:i0], b[:i0]), f"{etiket}: ileriye bakma -> {ad}"
    assert not ayni(m.beta("SPY", 60).to_numpy()[i0 + 5:], m2.beta("SPY", 60).to_numpy()[i0 + 5:]), \
        "bozma etkisiz: test bir sey sinamiyor"
    assert m.rejim()["rejim"].iloc[:i0].equals(m2.rejim()["rejim"].iloc[:i0])


def _islem_karsilastir(m, m2, i0, hedefler, etiket):
    s1, g1 = kural_sinyal(m, hedefler)
    s2, g2 = kural_sinyal(m2, hedefler)
    assert ayni(s1.to_numpy()[:i0], s2.to_numpy()[:i0]), f"{etiket}: sinyal ileriye bakiyor"
    assert ayni(g1.to_numpy()[:i0], g2.to_numpy()[:i0])
    assert (s1.to_numpy()[:i0] != 0).sum() > 100
    toplam = 0
    for g, h, c in GIRIS_CIKIS:
        for kr in ("yok", "SPY:250", "SPY:60"):
            a = m.islemler(s1, giris=g, h=h, cikis=c, korunma=kr, guc=g1)
            b = m2.islemler(s2, giris=g, h=h, cikis=c, korunma=kr, guc=g2)
            a = a[a.t_pos < i0 - 5].reset_index(drop=True)
            b = b[b.t_pos < i0 - 5].reset_index(drop=True)
            assert len(a) == len(b) and len(a) > 20, (etiket, g, h, c, kr, len(a), len(b))
            for col in a.columns:
                if col == "anormal":            # tanim geregi donem ortalamasina bagli
                    continue
                x, y = a[col].to_numpy(), b[col].to_numpy()
                if x.dtype.kind == "f":
                    assert ayni(x, y), f"{etiket}: ileriye bakma -> islem {col} ({g},{h},{c},{kr})"
                else:
                    assert (x == y).all(), f"{etiket}: ileriye bakma -> islem {col} ({g},{h},{c},{kr})"
            for kom in M.KOMISYONLAR:
                ga = m.gunluk(m.islemler(s1, giris=g, h=h, cikis=c, korunma=kr, guc=g1), kom).to_numpy()
                gb = m2.gunluk(m2.islemler(s2, giris=g, h=h, cikis=c, korunma=kr, guc=g2), kom).to_numpy()
                assert ayni(ga[:i0 - 6], gb[:i0 - 6]), f"{etiket}: gunluk seri ({g},{h},{c},{kr},{kom})"
            toplam += len(a)
    return toplam


def test_ileriye_bakmama_sentetik():
    m = sm()
    hedefler = ["Y", "H1", "H2", "H3", "H4", "LEV"]
    for T0 in ("2019-03-05", "2022-08-17"):
        m2 = m.bozuk_kopya(T0, tohum=11)
        i0 = int(m.idx.searchsorted(pd.Timestamp(T0)))
        _yol_karsilastir(m, m2, i0, hedefler, "sentetik " + T0)
        n = _islem_karsilastir(m, m2, i0, hedefler, "sentetik " + T0)
        assert n > 500
    # T0 OOS icindeyken IS satirlari (anormal dahil) birebir ayni kalmali
    T0 = "2020-06-01"
    m2 = m.bozuk_kopya(T0, tohum=3)
    s1, _ = kural_sinyal(m, hedefler)
    s2, _ = kural_sinyal(m2, hedefler)
    kw = dict(kural_id="LB", h=(1, 3), donemler=["IS"], korunma=("yok", "SPY:60"))
    r1, r2 = m.degerlendir(s1, **kw), m2.degerlendir(s2, **kw)
    say = r1.select_dtypes("number").columns
    for col in say:
        assert ayni(r1[col].to_numpy(float), r2[col].to_numpy(float)), f"IS satirlari T0 sonrasindan etkilendi: {col}"
    assert r1["n_islem"].sum() > 1000
    # bakis_testi: temiz kural gecer, ileriye bakan kural yakalanir
    ok, _ = m.bakis_testi(lambda mm: kural_sinyal(mm, hedefler)[0], T0=("2018-05-02", "2023-01-10"))
    assert ok
    kotu = lambda mm: (mm.getiri("kk")["Y"].shift(-1) > 0).astype(int)
    ok2, _ = m.bakis_testi(kotu, T0=("2018-05-02",))
    assert not ok2
    kotu2 = lambda mm: (mm.girdi_getiri("Y") > mm.girdi_getiri("Y").quantile(0.9)).astype(int)
    ok3, _ = m.bakis_testi(kotu2, T0=("2018-05-02",))
    assert not ok3, "tum orneklem yuzdeligi yakalanmadi"


def test_ileriye_bakmama_gercek_panel():
    try:
        m = Motor()
    except Exception as e:
        print(f"    (gercek panel yok, atlandi: {type(e).__name__})")
        return
    hedefler = [k for k in ["SPY", "QQQ", "IWM", "XLF", "XLE", "AAPL", "NVDA", "JPM", "TQQQ", "SOXL",
                            "TLT", "GLD", "XOM", "MSFT", "AMD"] if k in m.kpos]
    T0 = "2021-06-15"
    m2 = m.bozuk_kopya(T0, tohum=5)
    i0 = int(m.idx.searchsorted(pd.Timestamp(T0)))
    _yol_karsilastir(m, m2, i0, hedefler, "gercek")
    n = _islem_karsilastir(m, m2, i0, hedefler, "gercek")
    assert n > 2000
    for k in ("^VIX", "^VIX3M", "BTC-USD", "ES=F", "CL=F", "EURUSD=X"):
        if k in m.kpos:
            assert m.sinif[k] in ("SONRA", "VIX1615"), k
            assert ayni(m.girdi(k).to_numpy(), m.df("adjclose", ham=True)[k].shift(1).to_numpy())
            try:
                m.girdi(k, sizintili=True)
                assert k in m.vix_ailesi, f"{k} ayni gun verildi"
            except ValueError:
                assert k not in m.vix_ailesi
    assert "^VIX" in m.vix_ailesi and "BTC-USD" not in m.vix_ailesi and "ES=F" not in m.vix_ailesi
    assert ayni(m.girdi("^VIX", "close", sizintili=True).to_numpy(), m.df("close", ham=True)["^VIX"].to_numpy())
    assert m._temettu is not None, "temettu tablosu yuklenmedi"
    # gercek fiyat (bolunme geri alinmis): NVDA 2010 basi ~18 $, AAPL 2014-06-06 ~645 $
    if "NVDA" in m.kpos:
        p = m.ham_fiyat("k")[m.idx.get_loc(pd.Timestamp("2010-01-04")), m.kpos["NVDA"]]
        assert 15 < p < 22, p
    if "AAPL" in m.kpos:
        p = m.ham_fiyat("k")[m.idx.get_loc(pd.Timestamp("2014-06-06")), m.kpos["AAPL"]]
        assert 600 < p < 700, p
    # SPY ceyreklik temettu tablosu
    tem = m.temettu_orani()[:, m.kpos["SPY"]]
    assert 80 <= (tem > 0).sum() <= 92 and tem.max() < 0.02


def test_beta_ve_sigma():
    m = sm()
    r = m.getiri("kk")
    for w in (250, 60):
        b = m.beta("SPY", w)
        for t, k in ((1000, "H3"), (2500, "LEV"), (700, "Y")):
            x, y = r["SPY"].to_numpy()[t - w:t], r[k].to_numpy()[t - w:t]
            bek = np.cov(x, y)[0, 1] / np.var(x, ddof=1)
            assert abs(b[k].iat[t] - bek) < 1e-9, (w, t, k, b[k].iat[t], bek)
    assert abs(m.beta("SPY", 250)["LEV"].iloc[400:].mean() - 2.0) < 0.05
    assert m.beta("SPY", 250).iloc[:125].isna().all().all()
    t = 900
    bek = r["H2"].to_numpy()[t - 20:t].std(ddof=1)
    assert abs(m.sigma20()["H2"].iat[t] - bek) < 1e-12
    # korunmali ileri getiri = r_Y - beta_t * r_M
    fk = m.ileri_korunmali("K", 2, "kapanis", "SPY", 60, ["H3"])["H3"].iat[t]
    bek = m.ileri("K", 2)["H3"].iat[t] - m.beta("SPY", 60)["H3"].iat[t] * m.ileri("K", 2)["SPY"].iat[t]
    assert abs(fk - bek) < 1e-15


def test_rejim_ve_bolum():
    T = 320
    vix = np.full(T, 15.0)
    for i in (210, 211, 225, 250, 271, 291):
        vix[i] = 35.0
    vix[230] = 30.0          # 30 tam: orta kova
    vix[231] = 20.0          # 20 tam: orta kova
    spy = np.r_[np.linspace(100, 150, 240), np.linspace(150, 90, 80)]
    m = Motor(mini({"SPY": spy, "^VIX": vix}, sinif={"^VIX": "VIX1615"}))
    rj = m.rejim()
    b = rj["bolum"].to_numpy()
    # VIX(t-1) > 30 -> t = konum + 1. 210,211,225 ayni bolum (bosluk 13); 250 (bosluk 24) yeni;
    # 271 (bosluk 20) yeni; 291 (bosluk 19) ayni.
    assert b[211] == 1 and b[212] == 1 and b[226] == 1, b[205:230]
    assert b[251] == 2 and b[272] == 3 and b[292] == 3
    assert (b > 0).sum() == 6 and b[210] == 0
    k = rj["kova_no"].to_numpy()
    assert k[231] == 1 and k[232] == 1 and k[233] == 0 and k[211] == 2 and k[0] == -1
    u = rj["ust200"].to_numpy()
    assert (u[:200] == -1).all()
    ma = pd.Series(spy).rolling(200).mean().to_numpy()
    for t in (201, 239, 260, 300):
        assert u[t] == int(spy[t - 1] > ma[t - 1]), t
    assert rj["rejim"].iat[211] == "V>30|UST"


def test_maliyet_aritmetigi():
    T = 120
    idx = pd.bdate_range("2021-01-04", periods=T)      # 2021-01-04 Pazartesi
    vix = np.full(T, 15.0)
    vix[99] = 40.0                                      # VIX(t-1) > 30 -> t = 100
    c50 = np.full(T, 50.0)
    a50 = c50.copy()
    a50[:90] *= 0.99                                    # 90. gun temettu gunu: %1
    P = mini({"Z50": c50, "Z2": np.full(T, 2.0), "SPY": np.linspace(100, 110, T), "^VIX": vix,
              "^IRX": np.full(T, 5.0)},
             hacim={"Z50": 1e7, "Z2": 5e7, "SPY": 1e8, "^VIX": 0, "^IRX": 0},
             adj={"Z50": a50}, sinif={"^VIX": "VIX1615", "^IRX": "ONCE"}, idx=idx,
             evren_ek={"Z50": {"maliyet_bps": 3.0}, "Z2": {"maliyet_bps": 3.0},
                       "^VIX": {"maliyet_bps": np.nan}, "^IRX": {"maliyet_bps": np.nan}})
    m = Motor(P)
    # kademe: Z50 adv = 50*1e7 = 500 mln -> 3 bps; Z2 = 100 mln -> 7 bps (evren 3'un ustu); SPY > 1 mlr -> 1,5
    assert m.kademe()[80, m.kpos["Z50"]] == 3.0 and m.kademe()[80, m.kpos["Z2"]] == 7.0
    assert m.kademe()[80, m.kpos["SPY"]] == 1.5 and m.kademe()[30, m.kpos["Z50"]] == 15.0
    assert not m.hedef_uygun()[59, m.kpos["Z50"]] and m.hedef_uygun()[60, m.kpos["Z50"]]
    faiz = 5.0 / 100 / 252
    s = pd.Series(0, index=idx)
    s.iloc[70] = 1          # 70 = Pazartesi (70 % 5 == 0)
    s.iloc[74] = -1         # Cuma -> cikis Pazartesi (3 takvim gunu)
    s.iloc[100] = 1         # VIX(t-1) > 30: maliyet x2
    s.iloc[89] = 1          # t+1 = temettu gunu
    k = m.islemler(s, "Z50", giris="K", h=1).set_index("t_pos")
    # uzun, fiyat 50: bacak = max(3, 0,5 sent/50 = 1 bps) + komisyon
    bek = {"hisse": 2 * (3 + 1.0), "sabit": 2 * (3 + 1.5), "oransal": 2 * (3 + 20.0)}
    for kom, b in bek.items():
        assert np.isclose(k.at[70, "mal_" + kom], b / 1e4 + faiz, atol=1e-12), (kom, k.at[70, "mal_" + kom])
        assert np.isclose(k.at[70, "net_" + kom], -(b / 1e4 + faiz), atol=1e-12)
        assert np.isclose(k.at[70, "islemmal_" + kom], b / 1e4, atol=1e-12)
        assert np.isclose(k.at[70, "malg_" + kom], b / 2e4, atol=1e-12)
        # kisa: nakit faizi yok, odunc %0,5 * 3 gun / 360
        assert np.isclose(k.at[74, "mal_" + kom], b / 1e4 + 0.005 * 3 / 360, atol=1e-12)
        # VIX(t-1) > 30: islem maliyeti x2
        assert np.isclose(k.at[100, "mal_" + kom], 2 * b / 1e4 + faiz, atol=1e-12)
        # temettu gununu kapsayan uzun: brut %0 (toplam getiri), kesinti 0,30 * %1
        assert np.isclose(k.at[89, "mal_" + kom], b / 1e4 + faiz + 0.30 * 0.01, atol=1e-9)
    assert np.isclose(k.at[89, "brut"], 1 / 0.99 - 1)      # adjclose temettuyu getiriye katar
    # Giris A temettu gununde (t+1 acilisi): temettu alinmaz, kesinti yok
    a = m.islemler(s, "Z50", giris="A", h=1).set_index("t_pos")
    assert np.isclose(a.at[89, "mal_sabit"], 9.0 / 1e4 + faiz, atol=1e-12)
    # gece tutma: 1 gun faiz; K h=3: 3 gun faiz
    g = m.islemler(s, "Z50", giris="K", cikis="acilis").set_index("t_pos")
    assert np.isclose(g.at[70, "mal_sabit"], 9.0 / 1e4 + faiz, atol=1e-12)
    k3 = m.islemler(s, "Z50", giris="K", h=3).set_index("t_pos")
    assert np.isclose(k3.at[70, "mal_sabit"], 9.0 / 1e4 + 3 * faiz, atol=1e-12)
    # dusuk fiyat: 2 $ -> taban 0,5 sent/2 $ = 25 bps (> kademe 7); hisse basi 0,005*5000 = 25 $ = 25 bps
    s2 = pd.Series(0, index=idx)
    s2.iloc[70] = 1
    z = m.islemler(s2, "Z2", giris="K", h=1).iloc[0]
    assert np.isclose(z["mal_hisse"], 2 * (25 + 25) / 1e4 + faiz, atol=1e-12)
    assert np.isclose(z["mal_sabit"], 2 * (25 + 1.5) / 1e4 + faiz, atol=1e-12)
    assert np.isclose(z["mal_oransal"], 2 * (25 + 20) / 1e4 + faiz, atol=1e-12)
    # zor odunc: +%10
    zk = m.islemler(-s2, "Z50", giris="K", h=1, zor_odunc=True).iloc[0]
    assert np.isclose(zk["mal_sabit"], 9.0 / 1e4 + 0.105 * 1 / 360, atol=1e-12)
    # korunmali islem: maliyet = hedef + |beta| * korunma bacaklari + finansman
    ms = sm()
    sy = pd.Series(0, index=ms.idx)
    sy.iloc[1500] = 1
    hk = ms.islemler(sy, "H3", giris="K", h=2, korunma="SPY:60").iloc[0]
    hy = ms.islemler(sy, "H3", giris="K", h=2, korunma="yok").iloc[0]
    t = 1500
    b = ms.beta("SPY", 60)["H3"].iat[t]
    assert b > 0 and np.isclose(hk["beta"], b)
    sp = ms.kpos["SPY"]
    bac = (ms.bacak_bps(np.array([t]), np.array([sp]), "k", "sabit")[0]
           + ms.bacak_bps(np.array([t + 2]), np.array([sp]), "k", "sabit")[0]) / 1e4
    carp = 2.0 if ms.rejim()["vix_1"].iat[t] > 30 else 1.0
    if carp == 1.0 and not (ms.rejim()["vix_1"].iloc[[t, t + 2]] > 30).any():
        gun = max((ms.idx[t + 2] - ms.idx[t]).days, 1)
        bek = hy["mal_sabit"] + b * bac + b * 0.005 * gun / 360
        assert np.isclose(hk["mal_sabit"], bek, atol=1e-12), (hk["mal_sabit"], bek)
    assert np.isclose(hk["brut"], ms.ileri("K", 2)["H3"].iat[t] - b * ms.ileri("K", 2)["SPY"].iat[t])
    # ozet: maliyet x2 ve basabas
    r = m.degerlendir(s, "Z50", kural_id="M", h=(1,), giris="K", gece=False, korunma="yok",
                      komisyon="sabit", donemler=["OOS"], rejimler=False)
    row = r.iloc[0]
    assert row.n_islem == 4 and np.isclose(row.brut_bps, (1 / 0.99 - 1) / 4 * 1e4, atol=1e-6)
    assert np.isclose(row.basabas_bps, row.brut_bps / 2)
    assert np.isclose(row.maliyet2x_net_bps, row.net_bps - (9 * 3 + 18) / 4.0, atol=1e-6)


def test_ortusmeme_ve_gunluk_seri():
    m = sm()
    s = pd.Series(1, index=m.idx)
    for g, h, c, adim in (("K", 3, "kapanis", 3), ("K", 1, "kapanis", 1), ("A", 2, "kapanis", 2),
                          ("G", 2, "kapanis", 2), ("K", 1, "acilis", 1)):
        isl = m.islemler(s, "H1", giris=g, h=h, cikis=c)
        d = np.diff(isl["t_pos"].to_numpy())
        assert (d == adim).all(), (g, h, c, np.unique(d))
        assert (isl["cikis_tarihi"] >= isl["giris_tarihi"]).all()
        if g == "K":
            assert (isl["giris_tarihi"] == isl["t"]).all()
        else:
            assert (isl["giris_tarihi"] > isl["t"]).all()
        for kr in ("yok", "SPY:250"):
            isl = m.islemler(s, "H1", giris=g, h=h, cikis=c, korunma=kr)
            for kom in M.KOMISYONLAR:
                gs = m.gunluk(isl, kom)
                assert np.isclose(gs.sum(), isl["net_" + kom].sum(), rtol=1e-9, atol=1e-10), (g, h, c, kr)
            assert np.isclose(m.gunluk(isl, "sabit", net=False).sum(), isl["brut"].sum(), rtol=1e-9)
    # hedef suzgeci: H8 (~10 mln $) hic islem uretmez; ilk 60 gun islem yok
    assert len(m.islemler(s, "H8")) == 0
    assert m.islemler(s, "H1")["t_pos"].min() == 60
    # sinyal dogrulama
    try:
        m.islemler(pd.Series(0.5, index=m.idx), "H1")
        raise AssertionError("gecersiz sinyal kabul edildi")
    except ValueError:
        pass
    # yon: kisa islem brutu = -ileri getiri
    k = m.islemler(-s, "H2", giris="K", h=2)
    f = m.ileri("K", 2)["H2"].to_numpy()[k["t_pos"].to_numpy()]
    assert np.allclose(k["brut"].to_numpy(), -f)
    # anormal = yon * (ileri - ayni donem/kova ortalamasi): sinyal her gun ise h=1'de ortalamasi ~0
    k1 = m.islemler(s, "H2", giris="K", h=1)
    assert abs(k1["anormal"].mean()) < 1e-12 + 1e-6
    tb = m.kosulsuz_taban(["H2"], "K", 1)
    assert set(tb.donem) <= set(M.DONEMLER) and tb.n.sum() == len(k1)
    assert np.isclose((tb.n * tb.taban_bps).sum() / tb.n.sum(), k1["brut"].mean() * 1e4)
    tab, oz = m.bolum_ozeti(k1, "sabit")
    assert oz["bolum_sayisi"] == len(tab) == k1.loc[k1.bolum > 0, "bolum"].nunique() >= 1
    assert tab["n"].sum() == (k1.bolum > 0).sum()
    # olcekli getiri
    i = 100
    sg = m.sigma20()["H2"].to_numpy()[k1["t_pos"].iat[i]]
    assert np.isclose(k1["olcekli_sabit"].iat[i], k1["net_sabit"].iat[i] / sg)


def test_en_cok_5_pozisyon():
    m = sm()
    hed = ["H1", "H2", "H3", "H4", "H5", "H6", "H7", "Y"]
    s = pd.DataFrame(0, index=m.idx, columns=hed)
    s.iloc[100::2] = 1                                  # iki gunde bir 8 sinyal, h=3: pozisyonlar ortusur
    guc = pd.DataFrame(np.tile(np.arange(1, 9, dtype=float), (m.T, 1)), index=m.idx, columns=hed)
    isl = m.islemler(s, giris="K", h=3, guc=guc)
    pf = isl[isl.portfoyde]
    assert len(isl) > len(pf) > 0
    ac = np.zeros(m.T + 5, int)
    for t in pf["t_pos"]:
        ac[t + 1:t + 4] += 1                            # K, h=3: t+1..t+3 gunleri acik
    assert ac.max() == 5, ac.max()
    ilk = pf[pf.t_pos == pf.t_pos.min()]
    assert sorted(ilk["hedef"]) == sorted(["H4", "H5", "H6", "H7", "Y"]), list(ilk["hedef"])
    g, v, kim = m._katki(isl, "sabit")
    assert np.bincount(g).max() == 5
    assert set(kim) <= set(np.flatnonzero(isl["portfoyde"].to_numpy()))
    # tek gun, h=1: gunluk seri = secilen 5 islemin ortalamasi
    s1 = pd.DataFrame(0, index=m.idx, columns=hed)
    s1.iloc[500] = 1
    i1 = m.islemler(s1, giris="K", h=1, guc=guc)
    assert len(i1) == 8 and i1.portfoyde.sum() == 5
    gs = m.gunluk(i1, "sabit")
    assert np.isclose(gs.iloc[501], i1.loc[i1.portfoyde, "net_sabit"].mean())
    assert (gs.drop(gs.index[501]) == 0).all()


def test_bootstrap():
    rng = np.random.default_rng(42)
    ps = np.array([M.bootstrap_p(rng.normal(0, 0.01, 400), tekrar=400, tohum=i) for i in range(400)])
    assert abs(ps.mean() - 0.5) < 0.06, ps.mean()
    for q in (0.05, 0.10, 0.25, 0.50, 0.75):
        o = (ps < q).mean()
        assert abs(o - q) < 0.07, (q, o)
    # ekili etki: ortalama 0,25 sigma, n = 1000
    x = rng.normal(0.0025, 0.01, 1000)
    p = M.bootstrap_p(x)
    assert p < 0.002, p
    assert M.bootstrap_p(x) == p                         # sabit tohum
    assert M.bootstrap_p(-x) == p or abs(M.bootstrap_p(-x) - p) < 1e-3
    # otokorelasyonlu seride blok bootstrap, bagimsiz varsayimdan daha temkinli olmali
    e = rng.normal(0, 0.01, 3000)
    ar = np.zeros(3000)
    for t in range(1, 3000):
        ar[t] = 0.6 * ar[t - 1] + e[t]
    ar = ar - ar.mean() + 2.0 * ar.std() / np.sqrt(3000)  # naif t = 2
    assert M.bootstrap_p(ar) > 0.12
    assert np.isnan(M.bootstrap_p(np.zeros(100)))


def test_wilcoxon_ve_bh():
    # n=10, hepsi pozitif: W+=55, mu=27,5, var=96,25, z=(27,5-0,5)/9,811 -> p ~ 0,00592
    p = M.wilcoxon_p(np.arange(1, 11, dtype=float))
    assert abs(p - 0.005922) < 2e-5, p
    rng = np.random.default_rng(3)
    ps = np.array([M.wilcoxon_p(rng.normal(0, 1, 60)) for _ in range(600)])
    assert abs((ps < 0.05).mean() - 0.05) < 0.03
    assert M.wilcoxon_p(rng.normal(0.5, 1, 200)) < 1e-6
    pv = np.array([0.001, 0.008, 0.039, 0.041, 0.042, 0.059, 0.074, 0.205, 0.212, 0.216])
    r05, _ = M.bh(pv, 0.05)
    r10, q = M.bh(pv, 0.10)
    assert r05.sum() == 2 and r05[:2].all()
    assert r10.sum() == 6 and r10[:6].all()
    assert np.isclose(q[0], 0.01) and np.isclose(q[-1], 0.216)
    karisik = np.array([0.212, np.nan, 0.001, 0.074, 0.008, 0.039, 0.216, 0.041, 0.042, 0.059, 0.205])
    r, qq = M.bh(karisik, 0.10)
    assert r.sum() == 6 and not r[1] and np.isnan(qq[1]) and r[2] and not r[0]
    assert (np.diff(M.bh(np.sort(pv))[1]) >= -1e-15).all()


def test_blok_permutasyon_ve_kaydirma():
    m = sm()
    rng = np.random.default_rng(9)
    kova = m.rejim()["kova_no"].to_numpy()
    yil = m.idx.year.to_numpy()
    for _ in range(5):
        p = m.blok_permutasyon(20, rng)
        assert ayni(np.sort(p), np.arange(m.T)), "permutasyon degil"
        assert (yil[p] == yil).all(), "yil siniri bozuldu"
        assert (kova[p] == kova).all(), "VIX kovasi siniri bozuldu"
        assert (p != np.arange(m.T)).mean() > 0.5
        # blok yapisi: hucre ici ardisik gunlerin cogu yine ardisik (hucre siralamasinda)
        hucre = yil * 10 + kova
        ardisik = 0
        toplam = 0
        for hc in np.unique(hucre):
            pos = np.flatnonzero(hucre == hc)
            sira = np.searchsorted(pos, p[pos])
            ardisik += (np.diff(sira) == 1).sum()
            toplam += len(pos) - 1
        assert ardisik / toplam > 0.90, ardisik / toplam
    ms = M.donem_maskesi(m.idx, "IS")
    p = m.blok_permutasyon(20, rng, maske=ms)
    assert (p[~ms] == np.flatnonzero(~ms)).all() and ms[p[ms]].all()
    X = m.getiri("kk")[["X", "Y"]]
    Xk, k = M.dairesel_kaydir(X, rng=rng)
    assert 40 <= k <= 250 and ayni(Xk.to_numpy()[k:], X.to_numpy()[:-k]) and ayni(Xk.to_numpy()[:k], X.to_numpy()[-k:])
    # plasebo ekili etkiyi yok eder
    Yf = m.ileri("K", 1)[["Y"]]
    _, t0, _ = M.tarama_regresyon(m.girdi_getiri(["X"]), Yf)
    Yp = pd.DataFrame(Yf.to_numpy()[m.blok_permutasyon(20, rng)], index=m.idx, columns=["Y"])
    _, t1, _ = M.tarama_regresyon(m.girdi_getiri(["X"]), Yp)
    _, t2, _ = M.tarama_regresyon(Xk[["X"]], Yf)
    assert t0.iat[0, 0] > 10 and abs(t1.iat[0, 0]) < 4 and abs(t2.iat[0, 0]) < 4


def test_tarama_regresyon_dogrudan():
    rng = np.random.default_rng(5)
    T, K, N = 900, 4, 3
    X = rng.normal(0, 1, (T, K))
    cy = rng.normal(0, 1, (T, N))
    co = rng.normal(0, 1, T)
    Y = 0.2 * X[:, [1]] + 0.5 * cy - 0.3 * co[:, None] + rng.normal(0, 1, (T, N)) * (1 + 0.5 * np.abs(X[:, [0]]))
    X[rng.random((T, K)) < 0.1] = np.nan
    Y[rng.random((T, N)) < 0.05] = np.nan
    ms = np.ones(T, bool)
    ms[:100] = False
    for hac in (0, 2):
        B, TS, NN = M.tarama_regresyon(X, Y, kontrol_y=cy, kontrol_ortak=co, maske=ms, hac=hac, min_n=100)
        for k, j in ((1, 0), (0, 2), (3, 1)):
            r = ms & np.isfinite(X[:, k]) & np.isfinite(Y[:, j])
            D = np.column_stack([X[r, k], np.ones(r.sum()), cy[r, j], co[r]])
            th, *_ = np.linalg.lstsq(D, Y[r, j], rcond=None)
            e = Y[r, j] - D @ th
            iv = np.linalg.inv(D.T @ D)
            S = (D * e[:, None]) @ iv[0]
            v = (S * S).sum()
            for lag in range(1, hac + 1):
                v += 2 * (1 - lag / (hac + 1)) * (S[lag:] * S[:-lag]).sum()
            v *= r.sum() / (r.sum() - 4)
            assert abs(B[k, j] - th[0]) < 1e-10, (k, j)
            assert NN[k, j] == r.sum()
            if hac == 0:
                assert abs(TS[k, j] - th[0] / np.sqrt(v)) < 1e-8, (k, j, TS[k, j], th[0] / np.sqrt(v))
            else:   # HAC: maske disi satirlar atildigi icin komsuluk yaklasik
                assert abs(TS[k, j] - th[0] / np.sqrt(v)) < 0.35 * abs(TS[k, j]) + 0.3
        assert TS[1, 0] > 4 and abs(B[1, 0] - 0.2) < 0.1


def test_kumele_ve_tekillestir():
    rng = np.random.default_rng(8)
    T = 1500
    idx = pd.bdate_range("2012-01-02", periods=T)
    f = rng.normal(0, 0.01, (T, 3))
    fiyat = {}
    for g in range(3):
        for i in range(4):
            fiyat[f"G{g}_{i}"] = 100 * np.cumprod(1 + f[:, g] + rng.normal(0, 0.004, T))
    fiyat["KOPYA"] = fiyat["G0_0"] * (1 + rng.normal(0, 1e-4, T))
    fiyat["YENI"] = np.r_[np.full(T - 100, np.nan), 100 * np.cumprod(1 + rng.normal(0, 0.01, 100))]
    m = Motor(mini(fiyat, idx=idx))
    km = m.kumele(k=3, donem="IS", min_gun=500)
    assert km["YENI"] == -1
    for g in range(3):
        assert km[[f"G{g}_{i}" for i in range(4)]].nunique() == 1
    assert km[km >= 0].nunique() == 3 and km["KOPYA"] == km["G0_0"]
    tut, har = m.tekillestir(esik=0.98, donem="IS")
    assert har == {"KOPYA": "G0_0"} and "KOPYA" not in tut and len(tut) == 13
    sg = m.sepet_getiri(km)
    assert sg.shape[1] == 3
    # kumeleme yalniz IS verisine bakar: IS sonrasi veriyi boz, sonuc degismez
    m2 = m.bozuk_kopya("2020-01-02", 1)
    assert (m2.kumele(k=3)[km.index] == km).all()


def test_genisleyen_esik():
    m = sm()
    r = m.girdi_getiri("H1")
    v = r.to_numpy()
    for q in (0.1, 0.9):
        e = M.genisleyen_esik(r, q, 250)
        assert e.iloc[:251].isna().all()
        for t in (251, 700, 2222):
            assert np.isclose(e.iat[t], np.nanquantile(v[:t], q), rtol=0, atol=1e-15), (q, t)
    sr = M.genisleyen_sira(r, 250)
    for t in (300, 1234):
        g = v[1:t]
        assert np.isclose(sr.iat[t], (g <= v[t]).mean())
    z = M.z_skor(r, 20)
    t = 800
    assert np.isclose(z.iat[t], (v[t] - v[t - 20:t].mean()) / v[t - 20:t].std(ddof=1))


def test_degerlendir_semasi_ve_hizi():
    m = sm()
    r = m.girdi_getiri("H1")
    s = (r <= -0.015).astype(int) - (r >= 0.02).astype(int)
    t0 = time.time()
    son, isl = m.degerlendir(s, "H1", kural_id="S1", aile="D", ad="deneme", girdi="H1", islem_dondur=True)
    sure = time.time() - t0
    assert list(son.columns) == M.SEMA
    n_kombin = (2 * 3 + 1) * 3 * 3
    assert len(son) == n_kombin * len(M.STANDART_DONEMLER) * len(M.REJIMLER), len(son)
    assert len(isl) == 21
    print(f"    (degerlendir: {len(son)} satir, {sure:.1f} sn, bootstrapsiz)")
    assert sure < 20, sure
    # tutarlilik: donem ve rejim toplamlari
    a = son[(son.giris == "K") & (son.h == 1) & (son.korunma == "yok") & (son.komisyon == "sabit")]
    d = a[a.rejim == "hepsi"].set_index("donem")
    assert d.at["IS+OOS", "n_islem"] == d.at["IS", "n_islem"] + d.at["OOS", "n_islem"]
    assert d.at["TUM", "n_islem"] == d.loc[["STRES", "IS", "OOS", "SON"], "n_islem"].sum()
    b = a[a.donem == "IS"].set_index("rejim")
    assert b.loc[M.VIX_KOVA_AD, "n_islem"].sum() == b.at["hepsi", "n_islem"]
    assert b.loc[[f"{v}|{u}" for v in M.VIX_KOVA_AD for u in ("UST", "ALT")], "n_islem"].sum() \
        == b.loc[["UST", "ALT"], "n_islem"].sum()
    i = isl[("K", 1, "kapanis", "yok")]
    ii = i[i.donem == "IS"]
    assert np.isclose(b.at["hepsi", "net_bps"], ii["net_sabit"].mean() * 1e4)
    assert np.isclose(b.at["hepsi", "brut_bps"], ii["brut"].mean() * 1e4)
    assert np.isclose(b.at["hepsi", "uzun_n"], (ii.yon > 0).sum()) and b.at["hepsi", "kisa_n"] == (ii.yon < 0).sum()
    assert np.isclose(b.at["hepsi", "basabas_bps"], b.at["hepsi", "brut_bps"] / 2)
    assert np.isclose(b.at["hepsi", "en_kotu_bps"], ii["net_sabit"].min() * 1e4)
    x = np.sort(ii["net_sabit"].to_numpy())
    kk = max(3, int(np.ceil(0.05 * len(x))))
    assert np.isclose(b.at["hepsi", "en_iyi5suz_bps"], x[:-kk].mean() * 1e4)
    ay = ii.t.dt.year * 12 + ii.t.dt.month
    eniyi = ii.groupby(ay)["net_sabit"].sum().idxmax()
    assert np.isclose(b.at["hepsi", "en_iyi_aysiz_bps"], ii.loc[ay != eniyi, "net_sabit"].mean() * 1e4)
    yy = ii.groupby(ii.t.dt.year)["net_sabit"].sum()
    assert np.isclose(b.at["hepsi", "pozitif_yil_orani"], (yy > 0).mean())
    kume = ii.groupby("t_pos")["net_sabit"].sum() - ii.groupby("t_pos")["net_sabit"].count() * ii["net_sabit"].mean()
    G = len(kume)
    se = np.sqrt(G / (G - 1) * (kume ** 2).sum()) / len(ii)
    assert np.isclose(b.at["hepsi", "t_kume"], ii["net_sabit"].mean() / se)
    assert b.at["hepsi", "mdd_pct"] <= 0
    gs = m.gunluk(i, "sabit")
    dm = M.donem_maskesi(m.idx, "IS")
    kat = m._katki(i, "sabit")
    sec = (i.donem == "IS").to_numpy()[kat[2]]
    seri = np.bincount(kat[0][sec], weights=kat[1][sec], minlength=m.T)[dm]
    assert np.isclose(b.at["hepsi", "yillik_net_pct"], seri.mean() * 252 * 100)
    assert np.isclose(b.at["hepsi", "mdd_pct"], M.mdd(seri) * 100)
    assert abs(gs[dm].sum() - seri.sum()) < 5e-3
    # yaz_sonuc
    yol = os.path.join(os.environ.get("TMPDIR", "/tmp"), f"motor_test_{os.getpid()}.csv")
    try:
        M.yaz_sonuc(son.head(50), yol)
        M.yaz_sonuc(son.head(10), yol, ekle=True)
        geri = pd.read_csv(yol)
        assert list(geri.columns) == M.SEMA and len(geri) == 60
    finally:
        if os.path.exists(yol):
            os.remove(yol)
    # mdd
    assert np.isclose(M.mdd([0.1, -0.5, 0.2, -0.1]), -0.5) and np.isclose(M.mdd([-0.1, 0.05]), -0.1)


def test_donem_ve_evren():
    m = sm()
    for d, (a, b) in M.DONEMLER.items():
        dm = M.donem_maskesi(m.idx, d)
        if dm.any():
            assert m.idx[dm][0] >= pd.Timestamp(a) and m.idx[dm][-1] <= pd.Timestamp(b)
    top = sum(M.donem_maskesi(m.idx, d).astype(int) for d in M.DONEMLER)
    assert (top == 1).all()
    assert ayni(M.donem_maskesi(m.idx, "IS2"), M.donem_maskesi(m.idx, "OOS"))
    assert ayni(M.donem_maskesi(m.idx, "OOS2"), M.donem_maskesi(m.idx, "SON"))
    o = M.donem_maskesi(m.idx, "OOS")
    assert not M.donem_maskesi(m.idx, "OOS-2020")[m.idx.year == 2020].any()
    assert not M.donem_maskesi(m.idx, "OOS-2022")[m.idx.year == 2022].any()
    sn = M.donem_maskesi(m.idx, "OOS-SubNis2020")
    cik = (m.idx >= "2020-02-01") & (m.idx <= "2020-04-30")
    assert not sn[cik].any() and (sn | cik)[o].all() and not sn[~o].any()
    ev = m.donem_basi_evreni(n=5)
    assert set(ev.donem) == {"OOS", "SON"}                 # sentetik panel 2014'te baslar: IS evreni yok
    assert (ev.groupby("donem").size() == 5).all()
    assert not set(ev.kod) & {"SPY", "LEV", "^VIX", "BTC-USD"}
    # yalniz kesim tarihinden onceki veri: sonrasini boz, evren degismez
    ev2 = m.bozuk_kopya("2024-01-01", 2).donem_basi_evreni(n=5)
    assert ev.equals(ev2)
    em = m.evren_maskesi(ev)
    assert em.loc[M.donem_maskesi(m.idx, "OOS"), ev[ev.donem == "OOS"].kod.iloc[0]].all()
    assert not em.loc[M.donem_maskesi(m.idx, "IS")].any().any()


TESTLER = [test_ileri_getiri_hizasi, test_gecikme_siniflari, test_ekili_lead_lag, test_beta_ve_sigma,
           test_rejim_ve_bolum, test_maliyet_aritmetigi, test_ortusmeme_ve_gunluk_seri,
           test_en_cok_5_pozisyon, test_bootstrap, test_wilcoxon_ve_bh,
           test_blok_permutasyon_ve_kaydirma, test_tarama_regresyon_dogrudan,
           test_kumele_ve_tekillestir, test_genisleyen_esik, test_degerlendir_semasi_ve_hizi,
           test_donem_ve_evren, test_ileriye_bakmama_sentetik, test_ileriye_bakmama_gercek_panel]


def main():
    sec = sys.argv[1:]
    gecen, kalan = 0, []
    t00 = time.time()
    for fn in TESTLER:
        if sec and not any(s in fn.__name__ for s in sec):
            continue
        t0 = time.time()
        try:
            fn()
            gecen += 1
            print(f"GECTI  {fn.__name__}  ({time.time() - t0:.1f} sn)")
        except Exception:
            kalan.append(fn.__name__)
            print(f"KALDI  {fn.__name__}")
            traceback.print_exc()
    print(f"\n{gecen} test gecti, {len(kalan)} kaldi ({time.time() - t00:.0f} sn)")
    if kalan:
        print("KALANLAR:", ", ".join(kalan))
        sys.exit(1)


if __name__ == "__main__":
    main()
