#!/usr/bin/env python3
"""T3 — KEŞİF (aday üretmez): günün son bölümünün getirisi → ertesi gün(ler).
(1) Zaman serisi: XU030 ve XELKT 17:00→kapanış, BIG sepeti 16:30→kapanış ve 17:30→kapanış  →  dolabilir üyelerin eşit
    ağırlıklı sepeti: gece (co1), gün içi (oc1), f1, f2, f3.   y = a + b·son_bolum + c·gunun_kalani  (Newey–West, gecikme h)
(2) Kesit (Fama–MacBeth + beşte birlik farkı): hissenin kendi 16:30→kapanış getirisi; kapanış seansı göreli sapması
    (p_close/p_1730 − 1 ve p_close/p_son − 1, eksi aynı gün sektör ortalaması) → aynı hedefler.
Not: saatlik hisse verisinde "17:00" yok; en yakın noktalar 16:30 ve 17:30'dur (VERI_NOTU_D2).
Kullanım: python3 -I t3_kesif.py <panel> <cikti.csv>
"""
import math
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import vekil  # noqa: E402
from vekil import elib  # noqa: E402

H1_BAS = pd.Timestamp('2023-12-21')
HEDEF = ['co1', 'oc1', 'f1', 'f2', 'f3']
LAG = {'co1': 1, 'oc1': 1, 'f1': 1, 'f2': 2, 'f3': 3}


def nw_ols(y, X, lag):
    df = pd.concat([y.rename('y'), X], axis=1).dropna()
    n = len(df)
    if n < X.shape[1] + 30:
        return None
    A = np.column_stack([np.ones(n), df.drop(columns='y').values])
    yv = df['y'].values
    b = np.linalg.lstsq(A, yv, rcond=None)[0]
    u = yv - A @ b
    Z = A * u[:, None]
    S = Z.T @ Z
    for k in range(1, lag + 1):
        G = Z[k:].T @ Z[:-k]
        S += (1 - k / (lag + 1)) * (G + G.T)
    Vi = np.linalg.inv(A.T @ A)
    V = Vi @ S @ Vi
    return b, b / np.sqrt(np.diag(V)), n


def mean_t(x, lag):
    x = x.dropna().values
    if len(x) < 20:
        return np.nan, np.nan, len(x)
    mu, t = elib._hac_mean(x, np.ones(len(x)), lag)
    return mu, t, len(x)


def main():
    panel, out = sys.argv[1], sys.argv[2]
    P = elib.load(panel)
    R = P['ret_cc']
    sc = elib.sector_cols(P)
    idx_all = R.index
    # hedefler (hisse düzeyi)
    Y = {'co1': P['ret_co'][sc].shift(-1), 'oc1': P['ret_oc'][sc].shift(-1)}
    for h in (1, 2, 3):
        M, fill = elib.excess_measures(P, h, 'long', sc)
        Y[f'f{h}'] = M['raw']
    U = (P['fill_long'] & P['fill_short'])[sc]                    # t günü ne tavanda ne tabanda kapanmış, işlem görür
    YB = {}
    for k, v in Y.items():
        x = v.where(U)
        YB[k] = x.mean(axis=1).where(x.notna().sum(axis=1) >= 5)
    pc = vekil.snap_fiyat(P, 'p_close').reindex(idx_all)
    p1700 = vekil.snap_fiyat(P, 'p_1700').reindex(idx_all)
    p1730 = vekil.snap_fiyat(P, 'p_1730').reindex(idx_all)
    pson = vekil.snap_fiyat(P, 'p_son').reindex(idx_all)
    I = P['idx_ret']
    h1 = idx_all[idx_all >= H1_BAS]
    mid = h1[len(h1) // 2]
    per_h1 = {'tum': (h1[0], h1[-1]), 'yari1': (h1[0], mid - pd.Timedelta(days=1)), 'yari2': (mid, h1[-1])}
    per_uzun = {'IS_2017_2022': (pd.Timestamp('2017-01-02'), elib.IS_END), 'OOS1_2023_2025H1': (elib.OOS1_START, idx_all[-1])}
    rows = []
    # ---------------- (1) zaman serisi
    sinyal = {}
    for s in ('XU030', 'XELKT'):
        lh = pc[s] / p1700[s] - 1
        sinyal[f'{s}_1700_kapanis'] = (lh, (1 + I[s]) / (1 + lh) - 1, {**per_h1, **per_uzun})
    big = [c for c in elib.BIG if c in sc]
    tb = P['tradable'][big]
    rb = R[big].where(tb).mean(axis=1)
    for ad, px in (('BIG_1630_kapanis', p1700), ('BIG_1730_kapanis', p1730)):
        lh = (pc[big] / px[big] - 1).where(tb).mean(axis=1)
        sinyal[ad] = (lh, rb - lh, per_h1)
    for ad, (lh, rest, per) in sinyal.items():
        for dn, (a, b) in per.items():
            sl = slice(a, b)
            X = pd.concat([lh.rename('son'), rest.rename('kalan')], axis=1)[sl]
            esik = 0.005
            for hd in HEDEF:
                y = YB[hd][sl]
                res = nw_ols(y, X, LAG[hd])
                if res is None:
                    continue
                bb, tt, n = res
                ok = y.notna() & X['son'].notna()
                ust, alt = ok & (X['son'] >= esik), ok & (X['son'] <= -esik)
                rows.append({'tur': 'zaman_serisi', 'girdi': ad, 'hedef': 'sepet_' + hd, 'donem': dn, 'n': n,
                             'katsayi': bb[1], 't': tt[1], 'katsayi_kalan': bb[2], 't_kalan': tt[2],
                             'girdi_std_bps': X['son'][ok].std() * 1e4,
                             'ust_n': int(ust.sum()), 'ust_fazla_bps': (y[ust].mean() - y[ok].mean()) * 1e4,
                             'alt_n': int(alt.sum()), 'alt_fazla_bps': (y[alt].mean() - y[ok].mean()) * 1e4})
    # ---------------- (2) kesit
    def demean(D):
        D = D.where(U)
        return D.sub(D.mean(axis=1), axis=0)

    own = (pc[sc] / p1700[sc] - 1)
    d1730 = (pc[sc] / p1730[sc] - 1)
    dson = (pc[sc] / pson[sc] - 1)
    kesit = {
        'oz_1630_kapanis': (demean(own), demean((1 + R[sc]) / (1 + own) - 1)),
        'kapanis_sapma_1730_goreli': (demean(d1730), demean((1 + R[sc]) / (1 + d1730) - 1)),
        'kapanis_sapma_1800son_goreli': (demean(dson), demean((1 + R[sc]) / (1 + dson) - 1)),
    }
    for ad, (x, ctrl) in kesit.items():
        for dn, (a, b) in per_h1.items():
            sl = slice(a, b)
            xx, cc = x[sl], ctrl[sl]
            xx = xx.where(xx.std(axis=1) > 5e-4, axis=0)          # yarım günler: nokta = kapanış, kesit farkı yok → atla
            rk = xx.rank(axis=1, pct=True)
            nn = xx.notna().sum(axis=1)
            for hd in HEDEF:
                y = Y[hd].where(U)[sl]
                fm, _ = elib.fama_macbeth(y, {'x': xx, 'kalan': cc}, min_n=8, lag=LAG[hd] - 1)
                top = y.where(rk > 0.8).mean(axis=1).where(nn >= 10)
                bot = y.where(rk <= 0.2).mean(axis=1).where(nn >= 10)
                mu, t, n = mean_t(top - bot, LAG[hd] - 1)
                xs = xx.where(rk > 0.8).mean(axis=1) - xx.where(rk <= 0.2).mean(axis=1)
                rows.append({'tur': 'kesit', 'girdi': ad, 'hedef': 'hisse_' + hd, 'donem': dn,
                             'n': int(fm.loc['x', 'n_gun']) if 'x' in fm.index else 0,
                             'katsayi': fm.loc['x', 'katsayi'], 't': fm.loc['x', 't'],
                             'katsayi_kalan': fm.loc['kalan', 'katsayi'], 't_kalan': fm.loc['kalan', 't'],
                             'girdi_std_bps': xx.stack().std() * 1e4,
                             'ceyrek_fark_bps': mu * 1e4 if np.isfinite(mu) else np.nan, 't_ceyrek_fark': t, 'n_ceyrek_gun': n,
                             'girdi_ceyrek_fark_bps': xs.mean() * 1e4})
    df = pd.DataFrame(rows)
    # çoklu test: 'tum' dönemi (saatlik) birincil test kümesi — BH q=0,10
    m = df.donem == 'tum'
    p = df.loc[m, 't'].abs().map(lambda t: math.erfc(t / math.sqrt(2)) if np.isfinite(t) else 1.0)
    order = p.sort_values()
    k = len(order)
    passed = order <= 0.10 * (np.arange(1, k + 1) / k)
    cut = order[passed].max() if passed.any() else -1
    df['p_iki_yonlu'] = np.nan
    df.loc[m, 'p_iki_yonlu'] = p
    df['bh_gecti_q10'] = False
    df.loc[m, 'bh_gecti_q10'] = p <= cut
    df['etiket'] = 'keşif'
    os.makedirs(os.path.dirname(out), exist_ok=True)
    df.round(4).to_csv(out, index=False)
    pd.set_option('display.width', 280, 'display.max_rows', 400, 'display.max_columns', 40)
    print('test sayısı (tum dönemi):', int(m.sum()), '| BH geçen:', int(df.bh_gecti_q10.sum()), '| toplam satır:', len(df))
    zs = df[df.tur == 'zaman_serisi']
    print(zs[['girdi', 'hedef', 'donem', 'n', 'katsayi', 't', 't_kalan', 'ust_n', 'ust_fazla_bps', 'alt_n', 'alt_fazla_bps', 'bh_gecti_q10']].round(2).to_string(index=False))
    ks = df[df.tur == 'kesit']
    print(ks[['girdi', 'hedef', 'donem', 'n', 'katsayi', 't', 't_kalan', 'ceyrek_fark_bps', 't_ceyrek_fark', 'girdi_ceyrek_fark_bps', 'bh_gecti_q10']].round(2).to_string(index=False))


if __name__ == '__main__':
    main()
