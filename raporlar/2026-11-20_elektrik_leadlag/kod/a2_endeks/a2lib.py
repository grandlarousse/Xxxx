"""a2lib.py — A2 (endeks <-> hisse) ailesinin girdi ve sinyal kurucuları.
Yalnız t kapanışına kadarki bilgi: bütün pencereler rolling + shift; tam örneklem istatistiği yok.
rules.py ve scan.py bu dosyayı kullanır (rules.py kendi klasörünü sys.path'e ekler)."""
import os, sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ortak'))
import elib

INPUTS = ['XELKT', 'EWx', 'BIG', 'XU030', 'XU100', 'SPEC', 'KOMSU']
ZWIN, ZMIN = 60, 40          # z: girdi / 60 günlük, 1 gün gecikmeli std
MIN_UNIV = 5                 # sepet kurallarında günde en az 5 dolabilir sektör hissesi (YONTEM_EK E6)


def _bc(s, cols):
    """Seriyi tarih×hisse matrisine yay."""
    return pd.DataFrame(np.repeat(s.values[:, None], len(cols), axis=1), index=s.index, columns=cols)


def _ex_mean(X, cols, min_n):
    """Her sütun için 'kendisi hariç' satır ortalaması (X: NaN = o gün yok). cols dışındaki hedefler için düz ortalama."""
    S, N = X.sum(axis=1, min_count=1).fillna(0.0), X.notna().sum(axis=1)
    out = {}
    for c in cols:
        if c in X.columns:
            s = S - X[c].fillna(0.0); n = N - X[c].notna().astype(int)
        else:
            s, n = S, N
        out[c] = (s / n.where(n > 0)).where(n >= min_n)
    return pd.DataFrame(out)


def context(P):
    """Bütün girdiler (tarih×hedef matrisi), z-skorları ve koşul serileri."""
    R = P['ret_cc']; sc = elib.sector_cols(P); T = P['tradable']
    ix = P['idx_ret'].reindex(R.index)
    C = {'sc': sc, 'R': R[sc], 'trad': T[sc]}
    raw = {}
    raw['XELKT'] = _bc(ix['XELKT'], sc)
    raw['XU030'] = _bc(ix['XU030'], sc)
    raw['XU100'] = _bc(ix['XU100'], sc)
    Xs = R[sc].where(T[sc])
    raw['EWx'] = _ex_mean(Xs, sc, 3)                               # = elib.ew_basket(P, ex=i)
    big = [c for c in elib.BIG if c in R.columns]
    raw['BIG'] = _ex_mean(R[big].where(T[big]), sc, 1)             # o gün mevcut olanlar, hedef hariç
    beta = elib.beta_lagged(ix[['XELKT']], ix['XU030'])['XELKT']   # 250 gün, 1 gün gecikmeli
    raw['SPEC'] = _bc(ix['XELKT'] - beta * ix['XU030'], sc)
    kom = [c for c in elib.KOMSU if c in R.columns]
    raw['KOMSU'] = _bc(R[kom].where(T[kom]).mean(axis=1), sc)
    C['raw'] = raw
    C['z'] = {k: v / v.rolling(ZWIN, min_periods=ZMIN).std().shift(1) for k, v in raw.items()}
    C['univ_ok'] = P['fill_long'][sc].sum(axis=1) >= MIN_UNIV
    adv = elib.adv60(P)[sc].where(T[sc])
    C['liq_rank'] = adv.rank(axis=1, ascending=False, method='first')
    # koşullar (XU030): 20 günlük getiri işareti; 20 günlük oynaklık > geçmiş 250 günün medyanı (gecikmeli)
    x30 = ix['XU030']
    L = (1 + x30.fillna(0)).cumprod()
    r20 = L / L.shift(20) - 1
    v20 = x30.rolling(20, min_periods=15).std()
    med = v20.rolling(250, min_periods=120).median().shift(1)
    C['kosul'] = {'tr_up': r20 > 0, 'tr_dn': r20 < 0, 'vol_hi': v20 > med, 'vol_lo': v20 <= med}
    # büyük hisselerin kendi z'si (T3 ters yön)
    C['own_z'] = (R[sc] / R[sc].rolling(ZWIN, min_periods=ZMIN).std().shift(1)).where(T[sc])
    return C


def laggard(C, inp):
    """'Geciken': o gün girdi yönünde hareket etmemiş hisse: |r_i| < 0,5·|girdi| ya da ters işaret."""
    r, g = C['R'], C['raw'][inp]
    return r.notna() & g.notna() & ((r.abs() < 0.5 * g.abs()) | (np.sign(r) != np.sign(g)))


def make_sig(C, inp, thr, hedef='all', kosul=None):
    """Eşikli sinyal. thr > 0: z >= thr; thr < 0: z <= thr.
    hedef: 'all' | 'lag' | 'liq10' | 'sig' (likidite sırası > 10) | 'lagliq10' | tek hisse kodu."""
    Z = C['z'][inp]
    s = (Z >= thr) if thr > 0 else (Z <= thr)
    s = s & C['trad']
    single = hedef in C['sc']
    if hedef not in C['sc'] and hedef not in ('all', 'lag', 'liq10', 'sig', 'lagliq10'):
        return pd.DataFrame(False, index=s.index, columns=[hedef])[[]]
    if single:
        s = s[[hedef]]
    else:
        s = s.mul(C['univ_ok'], axis=0).astype(bool)
        if hedef in ('lag', 'lagliq10'):
            s = s & laggard(C, inp)
        if hedef in ('liq10', 'lagliq10'):
            s = s & (C['liq_rank'] <= 10)
        if hedef == 'sig':
            s = s & (C['liq_rank'] > 10)
    if kosul:
        s = s.mul(C['kosul'][kosul], axis=0).astype(bool)
    return s.fillna(False).astype(bool)


def make_sig_src(C, src, thr):
    """T3: tek bir (büyük) hissenin kendi z'si eşiği aşınca sektörün geri kalanı hedef."""
    if src not in C['sc']:
        return None
    z = C['own_z'][src]
    hit = (z >= thr) if thr > 0 else (z <= thr)
    s = C['trad'].mul(hit.fillna(False), axis=0).mul(C['univ_ok'], axis=0).astype(bool)
    s[src] = False
    return s


def halves(sig, P, h, side='long', measure='own', split='2019-12-31'):
    """IS'in iki yarısı (<=2019, 2020–IS sonu) için elib ile aynı hesap."""
    cols = [c for c in sig.columns if c in P['ret_cc'].columns]
    M, fl = elib.excess_measures(P, h, side, cols)
    p, ntr, X = elib.day_series(sig[cols], M[measure], fl)
    out = {}
    for lab, a, b in [('y1', None, pd.Timestamp(split)), ('y2', pd.Timestamp(split) + pd.Timedelta(days=1), elib.IS_END)]:
        st = elib.stats_block(p, ntr, X, h, a, b)
        out[f'{lab}_bps'] = st['ort_gun_bps']; out[f'{lab}_t'] = st['t']; out[f'{lab}_n'] = st['n_gun']
    return out
