"""Sentetik birim testleri: python kod/test_ortak.py  (pytest ile de çalışır)."""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
sys.path.insert(0, str(Path(__file__).parent))
import ortak as o


def _sentetik(n=3000, etki=0.006, oran=0.1, seed=1):
    rng = np.random.default_rng(seed)
    idx = pd.bdate_range("2012-01-02", periods=n)
    sig = pd.Series(rng.random(n) < oran, index=idx)
    r = rng.normal(0.0003, 0.012, n)
    r[1:] += etki * sig.values[:-1]          # D'deki sinyal D+1 getirisini artırır
    c = pd.Series(100 * np.cumprod(1 + r), index=idx)
    return sig, c


def test_bilinen_sinyal_geri_bulunur():
    sig, c = _sentetik()
    res = o.olay_testi(sig, o.ileri_getiri(c, 1), h=1, n_boot=1000)
    assert abs(res["fazla"] - 0.006) < 0.002, res["fazla"]
    assert res["nw_t"] > 4 and res["fazla_hac_t"] > 4 and res["boot_p"] < 0.01, res
    # maliyet ortalamayı tam bps kadar düşürür
    res2 = o.olay_testi(sig, o.ileri_getiri(c, 1), h=1, maliyet_bps=10, n_boot=200)
    assert abs(res["ortalama"] - res2["ortalama"] - 0.001) < 1e-12


def test_gelecege_bakis_yok():
    sig, c = _sentetik()
    ileri = o.ileri_getiri(c, 1)
    # sinyal 1 gün geç bilinseydi (kaydırılmış) etki kaybolur
    kay = o.olay_testi(sig.shift(1).fillna(False), ileri, h=1, n_boot=1000)
    assert abs(kay["fazla"]) < 0.0015 and kay["boot_p"] > 0.01, kay
    # D gününün kendi getirisiyle kurulan sinyal (D kapanışında bilinir) ileri getiriyi taşımaz:
    # ileri_getiri D'nin getirisini içermiyorsa fazla ~ 0 olmalı
    rng = np.random.default_rng(5)
    c2 = pd.Series(100 * np.cumprod(1 + rng.normal(0, 0.01, 3000)), index=c.index)
    s2 = o.gunluk_getiri(c2) > 0
    r2 = o.olay_testi(s2, o.ileri_getiri(c2, 1), h=1, n_boot=500)
    assert abs(r2["fazla"]) < 0.001, r2
    # h=3 ve bindirme elemesi: işlemler arası en az 3 gün
    e = o.bindirmeyi_ele(sig, 3)
    pos = np.flatnonzero(e.values)
    assert (np.diff(pos) >= 3).all()


def test_hizalama_ve_fdr():
    abd = pd.DatetimeIndex(["2026-01-05", "2026-01-06", "2026-01-07", "2026-01-08"])
    yerel = pd.Series([100, 101, 103.02, 104.0],
                      index=pd.DatetimeIndex(["2026-01-02", "2026-01-05", "2026-01-07", "2026-01-08"]))
    h = o.hizala(yerel, getiri=True, gecikme=0, takvim=abd)
    assert np.isclose(h["2026-01-05"], 0.01) and np.isnan(h["2026-01-06"])   # yerel tatil -> NaN
    assert np.isclose(h["2026-01-07"], 0.02)                                  # 2 günlük yerel getiri
    h1 = o.hizala(yerel, getiri=True, gecikme=1, takvim=abd)
    assert np.isclose(h1["2026-01-06"], 0.01)
    from statsmodels.stats.multitest import multipletests
    p = np.array([0.001, 0.008, 0.039, 0.041, 0.042, 0.06, 0.074, 0.205, 0.212, 0.216])
    adj, rej = o.bh_fdr(p, 0.05)
    ref = multipletests(p, 0.05, "fdr_bh")
    assert np.allclose(adj, ref[1]) and (rej == ref[0]).all()


if __name__ == "__main__" and len(sys.argv) == 1:
    for f in [test_bilinen_sinyal_geri_bulunur, test_gelecege_bakis_yok, test_hizalama_ve_fdr]:
        f(); print("GEÇTİ", f.__name__)


# =====================================================================================
# ADIM 0 ÖZ SINAMASI (PROTOKOL 13.1) — gerçek veride. Çalıştır: python kod/test_ortak.py oz
# Sonuçlar ek/oz_sinama.json'a yazılır.
# =====================================================================================
import json, tempfile, time

C = None


def _C():
    global C
    if C is None:
        C = o.evren("Ç")
    return C


def _rastgele(rng, kume=True, p_gun=0.1, p_ic=0.5, p_iid=0.05):
    t = o.TK()
    n = len(_C())
    if kume:
        g = rng.random(len(t)) < p_gun
        S = g[:, None] & (rng.random((len(t), n)) < p_ic)
    else:
        S = rng.random((len(t), n)) < p_iid
    return pd.DataFrame(S, index=t, columns=_C())


def oz_yanlis_alarm(tekrar=200, seed=11):
    rng = np.random.default_rng(seed)
    sonuc = {}
    for ad, kume, h in [("iid_h1", False, 1), ("kumeli_h1", True, 1), ("kumeli_h3", True, 3)]:
        p, tk = [], []
        for _ in range(tekrar):
            isl = o.islemler(_rastgele(rng, kume), h)
            r = o.test(isl, perm=0, ikincil=False, h=h)
            p.append(r["p_kume"]); tk.append(r["t_takvim"])
        p, tk = np.array(p), np.array(tk)
        sonuc[ad] = dict(tekrar=tekrar, yanlis_alarm=float(np.mean(p < 0.05)),
                         t_takvim_abs2=float(np.mean(np.abs(tk) >= 2)))
        print(ad, sonuc[ad], flush=True)
    # p_perm'in kendisi (100 tekrar, 500 kaydırma)
    pp = []
    for _ in range(100):
        isl = o.islemler(_rastgele(rng, True), 1)
        pp.append(o.test(isl, perm=500, ikincil=False, seed=int(rng.integers(1e9)))["p_perm"])
    sonuc["p_perm_kumeli_h1"] = dict(tekrar=100, yanlis_alarm=float(np.mean(np.array(pp) <= 0.05)))
    print("p_perm", sonuc["p_perm_kumeli_h1"], flush=True)
    for v in sonuc.values():
        assert v["yanlis_alarm"] <= 0.07, sonuc
    return sonuc


def oz_ekilmis_kenar(tekrar=50, kenar=20.0, seed=12):
    """Rastgele kümeli sinyalin t+1 getirisine +20 bps ekilir (günlük ve ileri matrislere tutarlı);
    tahmin edilen alfa ~20 bps olmalı (sabit etki sinyal günlerini de içerdiğinden ~20*(1-yoğunluk))."""
    rng = np.random.default_rng(seed)
    kod = tuple(_C())
    kg, ki = ("gunluk", kod), ("ileri", kod, 1, "kapanis")
    o._gunluk_ham(list(kod)); o._ileri_ham(list(kod), 1, "kapanis")
    G0, F0 = o._onbellek[kg].copy(), o._onbellek[ki].copy()
    est, tt, est0, yog = [], [], [], []
    try:
        for _ in range(tekrar):
            S = _rastgele(rng, True, p_gun=0.2)
            for k in [k for k in o._onbellek if k[0] == "bek"]:
                del o._onbellek[k]
            o._onbellek[kg], o._onbellek[ki] = G0.copy(), F0.copy()
            r0 = o.test(o.islemler(S, 1), perm=0, ikincil=False)
            Sv = S.values
            gv, fv = G0.values.copy(), F0.values.copy()
            gv[1:][Sv[:-1]] += kenar
            fv[Sv] += kenar
            g = pd.DataFrame(gv, index=G0.index, columns=G0.columns)
            f = pd.DataFrame(fv, index=F0.index, columns=F0.columns)
            for k in [k for k in o._onbellek if k[0] == "bek"]:
                del o._onbellek[k]
            o._onbellek[kg], o._onbellek[ki] = g, f
            r = o.test(o.islemler(S, 1), perm=0, ikincil=False)
            est.append(r["alfa_bps"]); tt.append(r["t_kume"]); est0.append(r0["alfa_bps"])
            yog.append(np.nanmean(np.where(np.isfinite(F0.values), Sv, np.nan)))
    finally:
        o._onbellek[kg], o._onbellek[ki] = G0, F0
        for k in [k for k in o._onbellek if k[0] == "bek"]:
            del o._onbellek[k]
    est, tt, est0 = map(np.array, (est, tt, est0))
    bek = kenar * (1 - float(np.mean(yog)))   # madde 4.1 sabit etkisi sinyal günlerini de içerir
    s = dict(tekrar=tekrar, kenar=kenar, beklenen=bek, ort_tahmin=float(est.mean()), ort_fark=float((est - est0).mean()),
             tespit_t2=float(np.mean(tt >= 2)), medyan_t=float(np.median(tt)))
    print("ekilmis", s, flush=True)
    assert abs(s["ort_tahmin"] - kenar) < 3 and abs(s["ort_fark"] - bek) < 0.5, s
    return s


def oz_gelecege_bakis():
    """Sinyal 1 gün ileri kaydırılır (t+1 IBS'si t'de kullanılır): test 'supheli' bayrağı kaldırmalı;
    meşru sürüm kaldırmamalı. Ayrıca bir işlemin getirisi ham fiyattan elle doğrulanır."""
    Cl, H, L = o._mat("AClose", _C()), o._mat("AHigh", _C()), o._mat("ALow", _C())
    ibs = (Cl - L) / (H - L)
    mesru = o.test(o.islemler(ibs < 0.2, 1), perm=0, ikincil=False)
    sizinti = o.test(o.islemler(ibs.shift(-1) < 0.2, 1), perm=0, ikincil=False)
    isl = o.islemler(ibs < 0.2, 1)
    r = isl.iloc[len(isl) // 2]
    c = o.fiyat(r["kod"])["AClose"]
    elle = (c.loc[r["cikis"]] / c.loc[r["giris"]] - 1) * 1e4
    i = c.index.get_loc(r["giris"])
    s = dict(mesru_t=float(mesru["t_kume"]), mesru_alfa=float(mesru["alfa_bps"]), mesru_supheli=mesru["supheli"],
             sizinti_t=float(sizinti["t_kume"]), sizinti_alfa=float(sizinti["alfa_bps"]),
             sizinti_supheli=sizinti["supheli"], elle_fark_bps=float(abs(elle - r["getiri_bps"])),
             cikis_ertesi_gun=bool(c.index[i + 1] == r["cikis"]))
    print("gelecege_bakis", s, flush=True)
    assert s["sizinti_supheli"] and not s["mesru_supheli"] and s["elle_fark_bps"] < 1e-6 and s["cikis_ertesi_gun"], s
    return s


def oz_uctan_uca(seed=13):
    rng = np.random.default_rng(seed)
    eski = o.SONUC
    tmp = Path(tempfile.mkdtemp())
    o.SONUC = tmp
    try:
        say = {"B1": 21, "B2": 27, "B3": 13}
        for ajan, n in say.items():
            rows = []
            for i in range(n):
                isl = o.islemler(_rastgele(rng, True), 1, test_id=f"{ajan}_{i}")
                aile = {"B1": "F1", "B2": "LL2", "B3": "F7"}[ajan]
                tid = f"{aile}{i}_C_h1"
                eg = o.egim_testi(o.zskor(o._gunluk_ham(["SMH"])["SMH"]).to_frame("SMH").reindex(columns=["SMH"]),
                                  perm=20) if (ajan == "B2" and i == 0) else None
                rows.append(o.test(isl, egim=eg, perm=50, ikincil=(i == 0), test_id=tid, ajan=ajan, aile=aile,
                                   varyant="a", birincil=1, kaynak="lit", evren="C", yon=1))
            if ajan == "B2":
                for asama in ("kesif", "dogrulama"):
                    for v in range(4):
                        isl = o.islemler(_rastgele(rng, True), 1)
                        rows.append(o.test(isl, perm=0, ikincil=False, test_id=f"LL6_{v}_{asama}", ajan=ajan,
                                           aile="LL6", varyant=f"oncul{v}|C", birincil=1, kaynak="lit",
                                           evren="C", asama=asama))
            o.kaydet(ajan, rows)
            if ajan == "B1":
                o.kaydet(ajan, isl, "islemler"); o.kaydet(ajan, o.rejim(isl), "rejim")
                o.kaydet(ajan, o.ekonomi(isl, "havuz", t_stat=2.0, n_boot=200, n_rast=100), "ekonomi")
        b, ll6, oz = o.birlestir()
        bek1 = b.loc[b.aile == "F1", "etiket"].str.contains("bekliyor|GÜÇSÜZ|ADAY|KULLANILAMAZ").all()
        k8_soru = b.loc[b.aile == "F1", "kontrol"].str.contains("8:\\?").all()
        # 15:30 ve yeniden kodlama dosyaları gelince 'bekliyor' kalkar
        f1 = b[b.aile == "F1"]
        pd.DataFrame({"test_id": f1.test_id, "A_bps": 10.0, "B_bps": 8.0, "oran_B_A": 0.8}).to_csv(tmp / "B1_1530.csv", index=False)
        pd.DataFrame({"test_id": b.test_id, "n_islem": b.n_islem, "alfa_bps": b.alfa_bps}).to_csv(tmp / "yeniden_kodlama.csv", index=False)
        b2, _, oz2 = o.birlestir()
        s = dict(n_birincil=oz["n_birincil"], q_dolu=bool(b.loc[b.birincil == 1, "q_bh"].notna().all()),
                 etiket_dolu=bool(b["etiket"].notna().all()), k8_bekliyor=bool(k8_soru),
                 sonra_bekliyor_yok=bool(~b2["kontrol"].str.contains("8:\\?|9:\\?").any()),
                 etiketler=b["etiket"].value_counts().to_dict(), ll6=dict((k, v) for k, v in oz.items() if k.startswith("ll6")),
                 dosyalar=sorted(p.name for p in tmp.iterdir()))
        print("uctan_uca", s, flush=True)
        assert s["n_birincil"] == 61 and s["q_dolu"] and s["etiket_dolu"] and s["k8_bekliyor"] and s["sonra_bekliyor_yok"] and bek1, s
        return s
    finally:
        o.SONUC = eski


def oz_hiz():
    Cl, H, L = o._mat("AClose", _C()), o._mat("ALow", _C()), o._mat("ALow", _C())
    Hh = o._mat("AHigh", _C())
    ibs = (Cl - L) / (Hh - L)
    t0 = time.time(); o.test(o.islemler(ibs < 0.2, 1)); a = time.time() - t0
    t0 = time.time(); o.test(o.islemler(ibs < 0.2, 3, cikis_sinyal=Cl > Cl.rolling(5).mean()), h=3); b = time.time() - t0
    X = pd.DataFrame({c: o.zskor(o._gunluk_ham(["SMH"])["SMH"]) for c in _C()})
    t0 = time.time(); o.egim_testi(X, perm=500); c = time.time() - t0
    s = dict(test_h1_sn=round(a, 1), test_h3_degisken_sn=round(b, 1), egim_500_sn=round(c, 1),
             tahmini_61_test_dk=round((45 * a + 8 * b + 8 * c) / 60, 1))
    print("hiz", s, flush=True)
    return s


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "oz":
    sonuc = {}
    for f in [oz_gelecege_bakis, oz_ekilmis_kenar, oz_uctan_uca, oz_hiz, oz_yanlis_alarm]:
        sonuc[f.__name__] = f()
        print("GEÇTİ", f.__name__, flush=True)
    (o.KOK / "ek" / "oz_sinama.json").write_text(json.dumps(sonuc, ensure_ascii=False, indent=1, default=str))
