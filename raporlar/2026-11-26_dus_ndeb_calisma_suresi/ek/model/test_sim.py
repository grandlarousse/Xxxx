# -*- coding: utf-8 -*-
"""Sart sinamalar (MODEL_TANIMI.md, bolum 8). Calistirma:
  python3 -m pytest -q test_sim.py --junitxml=cikti/pytest.xml
Kosu duzeyi sinamalar cikti/sinamalar.csv dosyasindan okunur (dosya yoksa atlanir).
"""
import os, sys, csv
import numpy as np
import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sim  # noqa: E402


@pytest.fixture(scope='module')
def pr6():
    pr, _ = sim.sample_params(6.0, 7, 60)
    return sim.derive(pr, 6.0)


@pytest.fixture(scope='module')
def dbg(pr6):
    d = {'L': [30, 90], 'buf': {}}
    acc = sim.engine(pr6, sim.Grid(0.5), [30, 90], forks=True, do_b2=False, tols=(0.02,), chunk=100, debug=d)
    return d, acc


def test_s2_arctan():
    """s=2'de E = u50*arctan(h/u50) (tablo ve referans integral)."""
    u50 = np.linspace(4, 10, 13); s = np.full(13, 2.0)
    M = sim.build_Mcum(u50, s)
    for h in (0.5, 3.0, 6.0, 10.0, 16.25):
        exact = u50 * np.arctan(h / u50)
        assert np.max(np.abs(M[:, int(round(h * 32))] - exact)) < 1e-10
        assert np.max(np.abs(sim.Mint(0.0, h, u50, s) - exact)) < 1e-10


def test_tablo_referans_integral(pr6):
    M = sim.build_Mcum(pr6['u50'], pr6['s'])
    for h in (1.0, 4.5, 9.0, 13.0):
        assert np.max(np.abs(M[:, int(round(h * 32))] - sim.Mint(0.0, h, pr6['u50'], pr6['s']))) < 1e-9


def test_fazla_yuk_yoksa_f_sifir(pr6, dbg):
    """W <= L(h0) ise f == 0 ve q == 1 (hizli motor, T=0 secenegi)."""
    d, _ = dbg
    g = sim.Grid(0.5); B = d['buf'][90][0]; P = g.P
    W = sim.Lload(g.p_hA[None, :], pr6['h0'][:, None], pr6['gamma'][:, None]) + pr6['cB'][:, None] * (
        sim.Lload((g.p_hA + g.p_hB)[None, :], pr6['h0'][:, None], pr6['gamma'][:, None])
        - sim.Lload(g.p_hA[None, :], pr6['h0'][:, None], pr6['gamma'][:, None]))
    m = W <= pr6['h0'][:, None]
    assert m.sum() > 1000
    assert np.all(B['peak'][:, :P][m] == 0) and np.all(B['f1'][:, :P][m] == 0)
    assert np.all(B['qa'][:, :P][m] == 1.0) and np.all(B['klev'][:, :P][m] == 0)
    assert not B['ever'][:, :P][m].any()


def test_f1_kapali_bicim(pr6):
    """Duragan f1'in kapali bicimi: 6 gun x + 1 gun dinlenme; uzun benzetimle karsilastir."""
    x = sim.Lload(pr6['h1'], pr6['h0'], pr6['gamma']) - pr6['h0']
    rho = pr6['rho1']
    f = np.zeros_like(x); mx = np.zeros_like(x)
    for t in range(7 * 400):
        f = (f + (x if t % 7 < 6 else 0.0)) * rho
        if t >= 7 * 399:
            mx = np.maximum(mx, f)
    a = x * rho * (1 - rho ** 6) / ((1 - rho) * (1 - rho ** 7))
    assert np.max(np.abs(mx / a - 1)) < 1e-10
    assert np.max(np.abs(pr6['a'] / a - 1)) < 1e-12
    assert np.max(np.abs(sim.f1_mornings(x, rho).max(-1) / a - 1)) < 1e-12


def test_fcrit_kapali_bicim(pr6):
    """Fcrit: hA=h3, 6 gun/hafta rejiminin duragan en yuksek f2 degeri; uzun benzetimle."""
    x = sim.Lload(6.0, pr6['h0'], pr6['gamma']) - pr6['h0']
    f1 = np.zeros_like(x); f2 = np.zeros_like(x); mx = np.zeros_like(x)
    for t in range(7 * 300):
        f1 = (f1 + (x if t % 7 < 6 else 0.0)) * pr6['rho1']
        f2 = f2 * pr6['rho2'] + np.maximum(0.0, f1 - pr6['a'])
        if t >= 7 * 299:
            mx = np.maximum(mx, f2)
    assert np.max(np.abs(mx / pr6['Fcrit'] - 1)) < 1e-8


def test_g_duragan(pr6):
    """g'nin duragan degeri: sabit e ile g* = (e/S)/(e/S + 1/tauG)."""
    res = sim.ref_sim(pr6, [(3.0, 0.0, 7, 0, 0, 1.0)], 6000)
    assert np.all(res['qa'] == 1.0)
    r = sim.Mint(0.0, 3.0, pr6['u50'], pr6['s']) / pr6['S']
    gs = r / (r + 1.0 / pr6['tauG'])
    assert np.max(np.abs(res['gD'][:, 0] - gs)) < 1e-5


def test_kabul_capasi(pr6):
    """Kabul edilen cekimler ogrenme dayanagini saglar (referans benzeticiyle, q=1 zorlanarak)."""
    g = sim.g180_anchor(pr6['u50'], pr6['s'], pr6['S'], pr6['tauG'])
    assert np.all((g >= 0.65) & (g <= 0.90))
    e = sim.Mint(0.0, 6.0, pr6['u50'], pr6['s']); gg = np.full_like(e, 0.3)
    for t in range(180):
        gg = gg - gg / pr6['tauG'] + ((e if t % 7 < 6 else 0.0) / pr6['S']) * (1 - gg)
    assert np.allclose(g, gg)


def test_h3_rejimi(pr6):
    """h3 rejimi 360 gunde cokmez ve Fcrit'e yaklasir; h3 + 0,5 coker."""
    res = sim.ref_sim(pr6, [(6.0, 0.0, 6, 0, 0, 1.0), (6.5, 0.0, 6, 0, 0, 1.0)], 360)
    assert not res['ever'][:, 0].any()
    rel = res['peak'][:, 0] / pr6['Fcrit']
    assert rel.max() <= 1 + 1e-9 and rel.min() > 0.99
    assert res['ever'][:, 1].mean() >= 0.95


def test_motor_referans_uyumu(pr6, dbg):
    """Hizli motor (tablo + dallanma) ile duz referans benzetici ayni sonucu verir."""
    d, _ = dbg
    g = sim.Grid(0.5); F = g.fields()
    rng = np.random.default_rng(3)
    for H in (30, 90):
        B = d['buf'][H][0]
        idx = rng.choice(len(F['hA']), 40, replace=False)
        pols = [(F['hA'][i], F['hB'][i], int(F['d'][i]), int(F['n'][i]), int(F['T'][i]), F['psi'][i]) for i in idx]
        res = sim.ref_sim(pr6, pols, H)
        for k in ('sumE', 'sumH', 'f1', 'f2', 'qa', 'peak', 'AD', 'BD', 'AN', 'BN'):
            assert np.allclose(B[k][:, idx], res[k], rtol=1e-9, atol=1e-11), k
        for k in ('qr', 'ql'):
            assert np.allclose(np.minimum(B[k][:, idx], 2.0), np.minimum(res[k], 2.0), rtol=1e-9), k
        assert np.array_equal(B['ever'][:, idx], res['ever'])
        assert (B['klev'][:, idx] != res['klev']).mean() < 0.002


def test_K_ic_ice(pr6, dbg):
    """K0 <= K1 <= K2 <= K3: tavanlar tekduze; kume seviyeleri birlesimle ic ice."""
    _, acc = dbg
    assert np.all(np.diff(acc['ceil'], axis=2) >= -1e-9)
    assert np.all(np.diff(acc['featcnt'], axis=1) >= 0)
    assert np.all(acc['Jstar'][:, :, :, 1:] >= acc['Jstar'][:, :, :, :-1] - 1e-12)


def test_planlanan_saat(pr6, dbg):
    """Cokus olmayan politikalarda uygulanan saat = planlanan saat."""
    d, _ = dbg
    g = sim.Grid(0.5)
    for H in (30, 90):
        B = d['buf'][H][0]; ph = g.planH(H)
        m = ~B['ever']
        assert np.allclose(B['sumH'][m], np.broadcast_to(ph[None, :], B['sumH'].shape)[m])


def test_lhs_araliklar():
    pr, info = sim.sample_params(5.0, 11, 50)
    for nm, lo, hi, _ in sim.param_ranges(5.0):
        assert pr[nm].min() >= lo and pr[nm].max() <= hi
    assert pr['h0'].max() <= 4.0
    assert info['n_acc'] >= 50


def _rows():
    p = os.path.join(HERE, 'cikti', 'sinamalar.csv')
    if not os.path.exists(p):
        return []
    with open(p, encoding='utf-8') as f:
        return list(csv.DictReader(f))


@pytest.mark.parametrize('row', _rows(), ids=lambda r: r['sinama'])
def test_kosu_duzeyi(row):
    """Kosu duzeyi sinamalar: K ic iceligi, iki tohum, izgara siniri, 0,25 yakinsama, vb."""
    assert row['sonuc'] == 'gecti', '%s: sayi=%s esik %s (%s)' % (row['sinama'], row['sayi'], row['esik'], row['aciklama'])
