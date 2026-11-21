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


if __name__ == "__main__":
    for f in [test_bilinen_sinyal_geri_bulunur, test_gelecege_bakis_yok, test_hizalama_ve_fdr]:
        f(); print("GEÇTİ", f.__name__)
