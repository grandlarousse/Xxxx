"""v6lib — V6 (karar anı ve dolum gerçekçiliği) ortak yardımcıları.
Gün içi endeks değeri kuralı (VERI_NOTU_D2): İş Yatırım damgası = bar başlangıcı, değer = aralığın son değeri.
'saat T değeri' = damgası < T olan son bar (5 dk: en çok 15 dk bayat). 18:00 damgalı değer = resmi kapanış.
Yahoo barlarında da damga = bar başlangıcı, c = bar kapanışı: aynı kural."""
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
KOD = os.path.dirname(HERE)
for _p in (os.path.join(KOD, 'ortak'), os.path.join(KOD, 'a7_gunici'), os.path.join(KOD, 'a2_endeks')):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import elib  # noqa: E402
import vekil  # noqa: E402
import a2lib  # noqa: E402

BAS = pd.Timestamp('2017-01-02')
DONEM = {'IS17': (BAS, elib.IS_END), 'OOS1': (elib.OOS1_START, elib.OOS1_END), 'KASA': (elib.KASA_START, pd.Timestamp('2100-01-01')),
         'H2023': (elib.OOS1_START, pd.Timestamp('2100-01-01'))}
SAAT5 = ['1730', '1745', '1750', '1755', '1800']
ZWIN, ZMIN = 60, 40


def _bars(paths):
    """Bir ya da birkaç parquet (ts_tr,c | ts_utc,c) → (date, mn, c) sıralı, yinelenen damga tekil."""
    fr = []
    for p in paths:
        if not os.path.exists(p):
            continue
        d = pd.read_parquet(p)
        if 'ts_tr' not in d.columns:
            d['ts_tr'] = pd.to_datetime(d['ts_utc']) + pd.Timedelta(hours=3)
        fr.append(d[['ts_tr', 'c']])
    d = pd.concat(fr)
    d['ts_tr'] = pd.to_datetime(d['ts_tr']).astype('datetime64[ns]')
    d = d.dropna().drop_duplicates('ts_tr', keep='last').sort_values('ts_tr')
    d['date'] = d['ts_tr'].dt.normalize()
    d['mn'] = d['ts_tr'].dt.hour * 60 + d['ts_tr'].dt.minute
    return d


def at_times(d, saatler, bayat=15, tam_gun_mn=17 * 60):
    """saat etiketi 'HHMM' → o anda bilinen son değer (damga < T, en çok `bayat` dk eski). Yarım günler atılır."""
    out = {}
    for T in saatler:
        tm = int(T[:2]) * 60 + int(T[2:])
        out[T] = d[(d.mn < tm) & (d.mn >= tm - bayat)].groupby('date').c.last()
    df = pd.DataFrame(out)
    tam = d.groupby('date').mn.max() >= tam_gun_mn
    return df[tam.reindex(df.index).fillna(False)]


def endeks_gunici(P, raw_m5_xu030=None):
    """Dönen: dict
       E5   : XELKT 5 dk değerleri (1700, 1730, 1745, 1750, 1755, 1800) — İş Yatırım, 2017'den tam
       X    : {saat: XU030 değeri}, XS: {saat: kaynak etiketi} — bulunabilen en iyi kaynak (öncelik sırasıyla)
       vekil_hata: XU100 oranı vekilinin ölçülen hatası (bps)"""
    dr = str(P['dir'])
    saat = ['1700'] + SAAT5
    E5 = at_times(_bars([os.path.join(dr, 'm5_isy', 'XELKT.parquet')]), saat)
    x5 = at_times(_bars([os.path.join(dr, 'm5_isy', 'XU030.parquet')] + ([raw_m5_xu030] if raw_m5_xu030 else [])), saat)
    m5 = at_times(_bars([os.path.join(dr, 'm5_isy', 'XU100.parquet')]), saat)
    y5 = at_times(_bars([os.path.join(dr, 'm5', 'XU030.parquet')]), saat)
    xh = at_times(_bars([os.path.join(dr, 'h1_isy', 'XU030.parquet')]), ['1700', '1800'], bayat=60)
    yh = at_times(_bars([os.path.join(dr, 'h1', 'XU030.parquet')]), ['1730', '1800'], bayat=60)
    L = P['idx'][['XU030', 'XU100']]
    idx = P['idx'].index[P['idx'].index >= BAS]
    prox = m5.mul((L['XU030'] / L['XU100']).reindex(m5.index), axis=0)       # XU030_T ≈ XU030_kap × XU100_T / XU100_kap
    X, XS, hata = {}, {}, {}
    for T in saat:
        kay = [('isy_m5', x5[T]), ('yahoo_m5', y5[T]), ('xu100_vekil', prox[T])]
        if T in xh.columns:
            kay.append(('isy_h1', xh[T]))
        if T in yh.columns:
            kay.append(('yahoo_h1', yh[T]))
        v = pd.Series(np.nan, index=idx)
        s = pd.Series('', index=idx, dtype=object)
        for ad, x in kay:
            x = x.reindex(idx)
            m = v.isna() & x.notna()
            v[m] = x[m]
            s[m] = ad
        X[T], XS[T] = v, s
        o = pd.concat([x5[T], prox[T]], axis=1, keys=['a', 'b']).dropna()
        if len(o):
            e = (o.b / o.a - 1) * 1e4
            hata[T] = (len(o), float(e.abs().median()), float(e.abs().quantile(0.95)))
    return {'E5': E5.reindex(idx), 'X': X, 'XS': XS, 'vekil_hata': hata}


def gunluk(P):
    """Günlük girdiler: XELKT/XU030 kapanış düzeyi, dünkü kapanış, 60 günlük gecikmeli std, önceki 19 kapanışın en yükseği."""
    L = P['idx'][['XELKT', 'XU030']]
    r = P['idx_ret'][['XELKT', 'XU030']].reindex(L.index)
    sd = r.rolling(ZWIN, min_periods=ZMIN).std().shift(1)
    return {'L': L, 'r': r, 'sd': sd, 'onceki': L.shift(1), 'zirve19': L['XELKT'].shift(1).rolling(19, min_periods=19).max()}


def sinyal(G, vE, vX=None, kural='S1', tampon=0.0, capE=0.5):
    """vE, vX: karar anındaki endeks değeri (tarih serisi; kapanış sürümü için resmi kapanış).
    S1: vE ≥ zirve19 × (1 + tampon).  S2: z(XELKT) ≥ tampon.  S3: z(XU030) ≥ tampon ve z(XELKT) < capE."""
    zE = (vE / G['onceki']['XELKT'].reindex(vE.index) - 1) / G['sd']['XELKT'].reindex(vE.index)
    if kural == 'S1':
        return (vE >= G['zirve19'].reindex(vE.index) * (1 + tampon)).fillna(False)
    if kural == 'S2':
        return (zE >= tampon).fillna(False)
    zX = (vX / G['onceki']['XU030'].reindex(vX.index) - 1) / G['sd']['XU030'].reindex(vX.index)
    return ((zX >= tampon) & (zE < capE)).fillna(False)


def hedef(P, kural):
    """Kuralın hedef maskesi (tarih × hisse) ve günde en az pozisyon sayısı — dondurulmuş kurallardaki gibi."""
    sc = elib.sector_cols(P)
    idx = P['ret_cc'].index
    if kural == 'S1':
        return pd.DataFrame(True, index=idx, columns=sc), 5
    if kural == 'S2':
        C = a2lib.context(P)
        return (C['trad'].mul(C['univ_ok'], axis=0)).astype(bool), 1
    return pd.DataFrame(True, index=idx, columns=[c for c in elib.VIOP if c in P['ret_cc'].columns]), 1


def olcu(P, h, cols, mod):
    """'per' fazla getirisi (bps) ve dolabilir maskesi. mod: 'uc_parca' (IS/OOS-1/kasa ayrı) | 'havuz' (2023+ tek dönem)."""
    eski = elib.PERIOD_MODE
    elib.PERIOD_MODE = mod
    P['_cache'] = {}
    M, F = elib.excess_measures(P, h, 'long', cols)
    X = M['per'] * 1e4
    elib.PERIOD_MODE = eski
    P['_cache'] = {}
    return X, F


def ozet(s, mask, X, F, min_n, a, b, h=3):
    """Tarih sinyali s → hedef matrisi → günlük eşit ağırlıklı portföy; [a, b] içinde ortalama bps, HAC t, gün sayısı."""
    s = s.reindex(mask.index).fillna(False).astype(bool)
    S = mask & s.values[:, None]
    p, n, _ = elib.day_series(S, X, F, min_n)
    m = (p.index >= a) & (p.index <= b)
    p2 = p[m]
    d = p2.notna().values.astype(float)
    if d.sum() == 0:
        return np.nan, np.nan, 0
    x = p2.fillna(0).values
    mu, t = elib._hac_mean(x, d, max(h - 1, 0))
    if not np.isfinite(mu):
        mu = x.sum() / d.sum()
    return float(mu), (float(t) if np.isfinite(t) else np.nan), int(d.sum())
