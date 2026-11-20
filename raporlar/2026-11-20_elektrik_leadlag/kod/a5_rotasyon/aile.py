"""A5 aile düzeyi çoklu test: (1) BH-FDR (q=0,10) IS p-değerlerine; (2) aile içi en iyi sonucun şansla çıkma olasılığı
(bütün tarih sinyalleri aynı miktarda dairesel kaydırılır; en büyük t'nin sıfır dağılımı); (3) aday kuralların
vadeli fiyatlı (evaluate_viop) ve XU030 ile korunmuş (β × XU030 SAT) sonuçları.
Kullanım: python3 -I aile.py <panel_is> <tarama.csv>"""
import os
import sys
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'ortak'))
import elib  # noqa: E402
import rules  # noqa: E402

pd.set_option('display.width', 250); pd.set_option('display.max_rows', 500); pd.set_option('display.max_columns', 40)


def target_series(P):
    """Tarih sinyalleri için hedefin günlük own-fazla getirisi sinyalden bağımsızdır: y[hedef, h](t)."""
    idx = P['ret_cc'].index
    Y = {}
    for hedef in ['sepet', 'likit10', 'viop3']:
        allsig, mn = rules.target_sig(P, pd.Series(True, index=idx), hedef)
        for h in (1, 2, 3):
            M, fl = elib.excess_measures(P, h, 'long', list(allsig.columns))
            y, _, _ = elib.day_series(allsig, M['own'], fl, mn)
            Y[(hedef, h)] = y[y.index <= elib.IS_END]
    return pd.DataFrame(Y)


def maxt(Y, S):
    """Bütün (sinyal × hedef × h) uzun testlerinde basit t (ortalama / (std/√n)); dönen: t matrisi (sinyal × sütun)."""
    y = Y.values
    ok = np.isfinite(y).astype(float)
    y0 = np.nan_to_num(y)
    n = S.T @ ok
    s1 = S.T @ y0
    s2 = S.T @ (y0 * y0)
    mu = s1 / np.maximum(n, 1)
    var = (s2 / np.maximum(n, 1) - mu ** 2) * n / np.maximum(n - 1, 1)
    t = mu / np.sqrt(np.maximum(var, 1e-30) / np.maximum(n, 1))
    t[n < 20] = np.nan
    return t


def family_test(P, n_iter=1000, seed=0):
    Y = target_series(P)
    Sd = rules.signals(P)
    names = list(Sd)
    S = np.column_stack([Sd[k].reindex(Y.index).values for k in names]).astype(float)
    T = maxt(Y, S)
    real_max, real_min = np.nanmax(T), np.nanmin(T)
    rng = np.random.default_rng(seed)
    n = len(Y)
    mx, mn = [], []
    for _ in range(n_iter):
        k = int(rng.integers(30, n - 30))
        t = maxt(Y, np.roll(S, k, axis=0))
        mx.append(np.nanmax(t)); mn.append(np.nanmin(t))
    mx, mn = np.array(mx), np.array(mn)
    i, j = np.unravel_index(np.nanargmax(T), T.shape)
    print(f'aile testi (uzun, {np.isfinite(T).sum()} test): en büyük basit t = {real_max:.2f} ({names[i]} | {Y.columns[j]}); '
          f'şansla ≥ olma olasılığı = {(np.sum(mx >= real_max) + 1) / (n_iter + 1):.3f}; sıfır dağılımında en büyük t: '
          f'medyan {np.median(mx):.2f}, %90 {np.percentile(mx, 90):.2f}, %95 {np.percentile(mx, 95):.2f}')
    print(f'en küçük basit t = {real_min:.2f}; şansla ≤ olma olasılığı = {(np.sum(mn <= real_min) + 1) / (n_iter + 1):.3f}; '
          f'sıfır %5 {np.percentile(mn, 5):.2f}')
    Tdf = pd.DataFrame(T, index=names, columns=[f'{a}|h{b}' for a, b in Y.columns])
    for q in (90, 95):
        thr = np.percentile(mx, q)
        hit = [(a, b, round(Tdf.loc[a, b], 2)) for a in Tdf.index for b in Tdf.columns if Tdf.loc[a, b] >= thr]
        print(f'aile düzeyi %{q} eşiğini (t ≥ {thr:.2f}) geçen testler: {hit}')
    return Tdf


def bh(scan):
    d = pd.read_csv(scan)
    p = elib.t_to_p(d['t_IS'].values)
    ok = elib.bh_fdr(p, 0.10)
    print(f'BH-FDR q=0,10 (iki yönlü, {np.isfinite(p).sum()} test): geçen = {int(ok.sum())}')
    if ok.sum():
        print(d.loc[ok, ['sinyal_tanimi', 't_IS', 'ort_fazla_IS_bps', 'net_temel_bps_IS']].round(2).to_string(index=False))
    lg = d[d.yon == 'long']
    okl = elib.bh_fdr(lg['p_tek_IS'].values, 0.10)
    print(f'BH-FDR q=0,10 (tek yönlü, yalnız uzun {len(lg)} test): geçen = {int(okl.sum())}')
    if okl.sum():
        print(lg.loc[okl, ['sinyal_tanimi', 't_IS', 'ort_fazla_IS_bps', 'net_temel_bps_IS']].round(2).to_string(index=False))


def adaylar(P, scan):
    d = pd.read_csv(scan).set_index('sinyal_tanimi')
    S = rules.signals(P)
    idx = P['ret_cc'].index
    cand = ['S3_zirve20|viop3|long|h3', 'S3_zirve20|viop3|long|h2', 'S3_zirve20|sepet|long|h3', 'S3_zirve20|likit10|long|h3',
            'S4_mom_ge1|sepet|long|h3', 'S4_mom_ge1|likit10|long|h3', 'S2_gecikme_yukari_1|viop3|long|h3',
            'S6_rel_1617_ge1p5|sepet|long|h1', 'S6_rel_1617_ge1p5|likit10|long|h3', 'S6_rel_1617_ge1p5|viop3|long|h3',
            'S6_rel_1417_le1p5|viop3|short|h1', 'S1_RS1_ge2|likit10|long|h3']
    c = ['n_gun_IS', 'n_bagimsiz_IS', 'ort_fazla_IS_bps', 't_IS', 'net_temel_bps_IS', 'net_muhafazakar_bps_IS', 'yari1_bps',
         'yari2_bps', 'top10_haric_bps', 'giris_acilis1_bps', 'giris_kapanis1_bps', 'gece_payi', 'en_yogun_pay',
         'yil_pozitif_orani', 'dolabilir_oran', 'eski_islem_bps', 'yeni_islem_bps', 'dol_mkt_IS_bps', 'maliyet_temel_bps']
    print(d.loc[cand, c].round(1).T.to_string())
    for k in cand:
        print(k, '|', d.loc[k, 'yillar_bps'])
    # XU030 ile korunmuş (β: 250 günlük, 1 gün gecikmeli; sektör AL + β × XU030 SAT), sinyal günü − bütün günler
    m30 = P['idx_ret']['XU030'].reindex(idx)
    for k in cand:
        sn, hedef, yon, hh = k.split('|'); h = int(hh[1:])
        if yon != 'long':
            continue
        sig, mn = rules.target_sig(P, S[sn], hedef)
        allsig, _ = rules.target_sig(P, pd.Series(True, index=idx), hedef)
        cols = list(sig.columns)
        f, fl, _ = elib.fwd_exec(P, h, 'long', cols)
        beta = elib.beta_lagged(P['ret_cc'][cols], m30)
        hed = f - beta.mul(elib.fwd_simple(m30.to_frame('m'), h)['m'], axis=0)
        ps, _, _ = elib.day_series(sig, hed, fl, mn)
        pa, _, _ = elib.day_series(allsig, hed, fl, mn)
        ps, pa = ps[ps.index <= elib.IS_END].dropna(), pa[pa.index <= elib.IS_END].dropna()
        x = pd.concat([pa.rename('y'), S[sn].astype(float).rename('d')], axis=1).dropna()
        rr = elib.ts_reg(1e4 * x['y'], x[['d']], lag=h)
        print(f"XU030-korumalı {k}: sinyal günü {1e4 * ps.mean():.0f} bps, bütün günler {1e4 * pa.mean():.0f} bps, "
              f"fark {rr.loc['d', 'katsayi']:.0f} (t={rr.loc['d', 't']:.1f})")
    # vadeli fiyatlarıyla
    if 'viop_front' in P:
        for sn, yon, h in [('S3_zirve20', 'long', 3), ('S2_gecikme_yukari_1', 'long', 3), ('S6_rel_1617_ge1p5', 'long', 3),
                           ('S6_rel_1617_ge1p5', 'long', 1), ('S6_rel_1417_le1p5', 'short', 1), ('S6_rel_1417_le2', 'short', 1),
                           ('S4_mom_le0', 'short', 1), ('S3_dip20_yalniz', 'short', 2)]:
            sig, _ = rules.target_sig(P, S[sn], 'viop3')
            rv = elib.evaluate_viop(sig, P, h=h, side=yon, name=sn)
            print(f"vadeli {sn}|{yon}|h{h}: n={rv['n_gun_IS']} fazla(kötüsü)={rv['ort_fazla_IS_bps']:.0f} t={rv['t_IS']:.1f} "
                  f"uzl={rv['settle_fazla_IS_bps']:.0f} son={rv['last_fazla_IS_bps']:.0f} net_uzl={rv['settle_net_temel_IS_bps']:.0f} "
                  f"| {rv['settle_yillar_bps']}")


if __name__ == '__main__':
    P = elib.load(sys.argv[1])
    bh(sys.argv[2])
    family_test(P)
    adaylar(P, sys.argv[2])
