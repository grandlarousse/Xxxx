"""A5 — XELKT / XU030 rotasyonu ve sektör zamanlaması: sinyal kütüphanesi + dondurulmuş kurallar.

Sözleşme: YONTEM_EK E1. build(P) herhangi bir panelde çalışır (P = elib.load(klasör)).
- Bütün sinyaller TARİH düzeyindedir (endeks serilerinden), yalnız t kapanışına kadarki bilgiyle kurulur
  (rolling + shift; tam örneklem istatistiği yok). Eşikler sayı olarak yazılıdır.
- Hedefler: 'sepet' (dolabilir bütün sektör hisseleri), 'likit10' (t−1'e kadarki 60 günlük medyan TL hacme göre
  o gün dolabilir en likit 10 sektör hissesi), 'viop3' (AKSEN, ENJSA, ODAS).
- S6 (gün içi) sinyalleri P['dir']/h1_isy/{XELKT,XU030}.parquet dosyalarını okur; klasör yoksa sinyal üretmez.
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ortak'))
import elib  # noqa: E402

ZWIN, ZMIN = 60, 40          # z-skoru: 60 günlük std, 1 gün gecikmeli
THR = [1.0, 1.5, 2.0]
KS = [1, 3, 5, 10]
VIOP3 = ['AKSEN', 'ENJSA', 'ODAS']


def _z(x):
    """x(t) / [x'in t−60…t−1 std'si]."""
    return x / x.rolling(ZWIN, min_periods=ZMIN).std().shift(1)


def _t(v):
    return ('%g' % v).replace('.', 'p')


def hourly(P):
    """Saatlik İş Yatırım endeks verisinden gün içi getiri pencereleri (tarih × pencere), XELKT ve XU030.
    Damga = bar başlangıcı, değer = aralığın son değeri: 'saat HH:00 değeri' = damgası < HH olan son bar.
    18:00 damgalı değer resmi kapanış; o bar yoksa (yarım gün) gün kullanılmaz."""
    out = {}
    base = os.path.join(str(P.get('dir', '')), 'h1_isy')
    for s in ['XELKT', 'XU030']:
        f = os.path.join(base, s + '.parquet')
        if not os.path.exists(f):
            return None
        d = pd.read_parquet(f)[['ts_tr', 'c']].copy()
        d['ts_tr'] = pd.to_datetime(d['ts_tr'])
        d = d.sort_values('ts_tr')
        d['date'] = d['ts_tr'].dt.normalize()
        d['hr'] = d['ts_tr'].dt.hour
        v14 = d[d.hr <= 13].groupby('date').c.last()      # 14:00'te bilinen değer
        v16 = d[d.hr <= 15].groupby('date').c.last()      # 16:00
        v17 = d[d.hr <= 16].groupby('date').c.last()      # 17:00
        n14 = d[d.hr <= 13].groupby('date').c.size()
        has16 = d[d.hr == 15].groupby('date').c.size()
        has17 = d[d.hr == 16].groupby('date').c.size()
        cl = d[d.hr == 18].groupby('date').c.last()       # resmi kapanış
        W = pd.DataFrame({'16K': cl / v16 - 1, '14K': cl / v14 - 1, '1617': v17 / v16 - 1, '1417': v17 / v14 - 1})
        ok = (n14.reindex(W.index).fillna(0) >= 2) & (has16.reindex(W.index).fillna(0) > 0) & \
             (has17.reindex(W.index).fillna(0) > 0) & cl.reindex(W.index).notna()
        out[s] = W.where(ok, np.nan).dropna(how='all')
    return out


def signals(P):
    """Önceden yazılı ızgaranın bütün tarih düzeyi sinyalleri: {ad: bool Series (index = P['ret_cc'].index)}."""
    idx = P['ret_cc'].index
    L = P['idx'][['XELKT', 'XU030']].reindex(idx)
    r = P['idx_ret'][['XELKT', 'XU030']].reindex(idx)
    S = {}
    # S1 göreli güç
    for k in KS:
        rs = L['XELKT'].pct_change(k, fill_method=None) - L['XU030'].pct_change(k, fill_method=None)
        z = _z(rs)
        for th in THR:
            S[f'S1_RS{k}_ge{_t(th)}'] = z >= th
            S[f'S1_RS{k}_le{_t(th)}'] = z <= -th
    zE, zX = _z(r['XELKT']), _z(r['XU030'])
    # S2 gecikme
    for th in THR:
        S[f'S2_gecikme_yukari_{_t(th)}'] = (zX >= th) & (zE < 0.5)
        S[f'S2_gecikme_asagi_{_t(th)}'] = (zX <= -th) & (zE > -0.5)
    # S3 kırılım (20 günlük en yüksek / en düşük kapanış; pencere t dâhil)
    hiE = L['XELKT'] >= L['XELKT'].rolling(20, min_periods=20).max()
    hiX = L['XU030'] >= L['XU030'].rolling(20, min_periods=20).max()
    loE = L['XELKT'] <= L['XELKT'].rolling(20, min_periods=20).min()
    loX = L['XU030'] <= L['XU030'].rolling(20, min_periods=20).min()
    S['S3_zirve20'] = hiE
    S['S3_zirve20_yalniz'] = hiE & ~hiX
    S['S3_dip20'] = loE
    S['S3_dip20_yalniz'] = loE & ~loX
    # S4 sektör momentumu (XELKT r_cc(t) işareti / büyüklüğü)
    S['S4_mom_ge0'] = r['XELKT'] > 0
    S['S4_mom_le0'] = r['XELKT'] < 0
    for th in THR:
        S[f'S4_mom_ge{_t(th)}'] = zE >= th
        S[f'S4_mom_le{_t(th)}'] = zE <= -th
    # S5 ortalamaya dönüş: ln(XELKT/XU030) − 20 günlük ortalama, 20 günlük std ile
    lr = np.log(L['XELKT'] / L['XU030'])
    z5 = (lr - lr.rolling(20, min_periods=20).mean()) / lr.rolling(20, min_periods=20).std()
    for th in THR:
        S[f'S5_oran_ge{_t(th)}'] = z5 >= th
        S[f'S5_oran_le{_t(th)}'] = z5 <= -th
    # S6 gün sonu hareketi (saatlik)
    H = hourly(P)
    for w in ['16K', '14K', '1617', '1417']:
        for typ in ['abs', 'rel']:
            if H is None:
                x = pd.Series(np.nan, index=idx)
            else:
                x = H['XELKT'][w] if typ == 'abs' else H['XELKT'][w] - H['XU030'][w].reindex(H['XELKT'].index)
                x = x.dropna()
                x = _z(x).reindex(idx)        # std yalnız saatlik verisi olan günler üzerinden, 1 gün gecikmeli
            for th in THR:
                S[f'S6_{typ}_{w}_ge{_t(th)}'] = x >= th
                S[f'S6_{typ}_{w}_le{_t(th)}'] = x <= -th
    return {k: v.reindex(idx).fillna(False).astype(bool) for k, v in S.items()}


def liquid_mask(P, n=10):
    """t günü dolabilir (fill_long) sektör hisseleri içinde adv60 (t−1'e kadar) sırasına göre en likit n hisse."""
    sc = elib.sector_cols(P)
    a = elib.adv60(P)[sc].where(P['fill_long'][sc])
    rk = a.rank(axis=1, ascending=False, method='first')
    return (rk <= n).fillna(False)


def target_sig(P, s, hedef):
    """Tarih sinyalini hedef matrisine yayar. Dönen: (bool DataFrame, min_n)."""
    idx = P['ret_cc'].index
    s = s.reindex(idx).fillna(False).astype(bool)
    if hedef == 'sepet':
        sc = elib.sector_cols(P)
        return pd.DataFrame(np.repeat(s.values[:, None], len(sc), axis=1), index=idx, columns=sc), 5
    if hedef == 'likit10':
        m = liquid_mask(P)
        return m & s.values[:, None], 5
    if hedef == 'viop3':
        cols = [c for c in VIOP3 if c in P['ret_cc'].columns]
        return pd.DataFrame(np.repeat(s.values[:, None], len(cols), axis=1), index=idx, columns=cols), 1
    raise ValueError(hedef)


# ---------------------------------------------------------------------------------------------------------------
# DONDURULMUŞ KURALLAR  (ad, sinyal, hedef, h, yön, araç, birincil, açıklama) — IS taramasından sonra doldurulur
# ---------------------------------------------------------------------------------------------------------------
FROZEN = [
    # --- BİRİNCİL (3)
    ('A5_zirve20_viop3_h3', 'S3_zirve20', 'viop3', 3, 'long', 'spot', True,
     'XELKT kapanışı son 20 günün (t dâhil) en yüksek kapanışı → AKSEN, ENJSA, ODAS spot AL, 3 gün tut'),
    ('A5_zirve20_sepet_h3', 'S3_zirve20', 'sepet', 3, 'long', 'spot', True,
     'XELKT kapanışı son 20 günün en yüksek kapanışı → dolabilir bütün sektör hisseleri eşit ağırlık AL, 3 gün tut'),
    ('A5_mom1_sepet_h3', 'S4_mom_ge1', 'sepet', 3, 'long', 'spot', True,
     'XELKT r_cc(t) / 60 günlük gecikmeli std ≥ 1 → dolabilir bütün sektör hisseleri eşit ağırlık AL, 3 gün tut'),
    # --- İKİNCİL (6)
    ('A5_zirve20_likit10_h3', 'S3_zirve20', 'likit10', 3, 'long', 'spot', False,
     'XELKT 20 günlük en yüksek kapanış → adv60 sırasına göre en likit 10 dolabilir sektör hissesi AL, 3 gün'),
    ('A5_mom1_likit10_h3', 'S4_mom_ge1', 'likit10', 3, 'long', 'spot', False,
     'XELKT z(r_cc) ≥ 1 → en likit 10 dolabilir sektör hissesi AL, 3 gün'),
    ('A5_gecikme1_viop3_h3', 'S2_gecikme_yukari_1', 'viop3', 3, 'long', 'spot', False,
     'XU030 z(r_cc) ≥ 1 ve XELKT z(r_cc) < 0,5 (sektör geride) → AKSEN, ENJSA, ODAS spot AL, 3 gün'),
    ('A5_gunsonu1617_sepet_h1', 'S6_rel_1617_ge1p5', 'sepet', 1, 'long', 'spot', False,
     '16:00→17:00 (XELKT − XU030) getirisi / 60 günlük gecikmeli std ≥ 1,5 → sektör sepeti AL, 1 gün'),
    ('A5_gunsonu1617_viop3_h3', 'S6_rel_1617_ge1p5', 'viop3', 3, 'long', 'spot', False,
     '16:00→17:00 (XELKT − XU030) getirisi z ≥ 1,5 → AKSEN, ENJSA, ODAS spot AL, 3 gün'),
    ('A5_gunsonu1417_asagi_viop3_sat_h1', 'S6_rel_1417_le1p5', 'viop3', 1, 'short', 'viop', False,
     '14:00→17:00 (XELKT − XU030) getirisi z ≤ −1,5 → AKSEN, ENJSA, ODAS vadeli SAT, 1 gün (aynı zamanda AL\'dan kaçın)'),
]


def build(P):
    S = signals(P)
    out = []
    for ad, sn, hedef, h, yon, arac, birincil, acik in FROZEN:
        sig, min_n = target_sig(P, S[sn], hedef)
        out.append({'ad': ad, 'sig': sig, 'h': h, 'yon': yon, 'olcu': 'own', 'arac': arac, 'birincil': birincil,
                    'min_n': min_n, 'aciklama': acik})
    return out
