"""W3-C — XU030 → elektrik gecikmesi: sinyal yardımcıları + dondurulmuş kurallar (YONTEM_EK E1 sözleşmesi).

- Bütün sinyaller TARİH düzeyindedir (XU030 ve XELKT endeks getirileri), yalnız t kapanışına kadarki bilgiyle kurulur
  (rolling + shift(1); tam örneklem istatistiği yok). Eşikler sayı olarak yazılıdır.
- z(x) = x(t) / std(x; t−win … t−1), en az 2/3·win gözlem (win = 60 → 40; A5 ile aynı).
- build(P) FROZEN listesindeki kuralları döndürür; her kural sözlüğünde ayrıca 'beklenen_isaret' vardır.
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ortak'))
import elib  # noqa: E402

ZWIN = 60
VIOP3 = ['AKSEN', 'ENJSA', 'ODAS']


def zscore(x, win=ZWIN):
    """x(t) / [x'in t−win…t−1 std'si] (1 gün gecikmeli; en az 2/3·win gözlem)."""
    return x / x.rolling(win, min_periods=max(int(win * 2 / 3), 20)).std().shift(1)


def index_z(P, win=ZWIN):
    """(zXU030, zXELKT): günlük kapanış getirilerinin z-skorları, index = P['ret_cc'].index."""
    idx = P['ret_cc'].index
    r = P['idx_ret'][['XELKT', 'XU030']].reindex(idx)
    return zscore(r['XU030'], win), zscore(r['XELKT'], win)


def lag_signal(P, thx=1.0, the=0.5, win=ZWIN, mode='lt'):
    """Tarih sinyali. mode='lt': zXU030 ≥ thx ve zXELKT < the (gecikme); 'ge': zXU030 ≥ thx ve zXELKT ≥ the;
    'none': yalnız zXU030 ≥ thx (koşulsuz piyasa momentumu)."""
    zx, ze = index_z(P, win)
    s = zx >= thx
    if mode == 'lt':
        s = s & (ze < the)
    elif mode == 'ge':
        s = s & (ze >= the)
    return s.fillna(False).astype(bool)


def liquid_mask(P, n=10, ex=None):
    """t günü dolabilir sektör hisseleri içinde adv60 (t−1'e kadar) sırasına göre en likit n hisse (ex: hariç)."""
    sc = [c for c in elib.sector_cols(P) if not ex or c not in ex]
    a = elib.adv60(P)[sc].where(P['fill_long'][sc])
    rk = a.rank(axis=1, ascending=False, method='first')
    return (rk <= n).fillna(False)


def spread(P, s, hedef):
    """Tarih sinyalini hedef matrisine yayar. Dönen: (bool DataFrame, min_n)."""
    idx = P['ret_cc'].index
    s = s.reindex(idx).fillna(False).astype(bool)

    def rep(cols):
        return pd.DataFrame(np.repeat(s.values[:, None], len(cols), axis=1), index=idx, columns=cols)
    if hedef == 'viop3':
        return rep([c for c in VIOP3 if c in P['ret_cc'].columns]), 1
    if hedef == 'sepet':
        return rep(elib.sector_cols(P)), 5
    if hedef == 'sepet_ex3':
        return rep([c for c in elib.sector_cols(P) if c not in VIOP3]), 5
    if hedef == 'likit10':
        return liquid_mask(P) & s.values[:, None], 5
    if hedef == 'likit10_ex3':
        return liquid_mask(P, ex=VIOP3) & s.values[:, None], 5
    if isinstance(hedef, (list, tuple)):
        return rep([c for c in hedef if c in P['ret_cc'].columns]), 1
    return rep([hedef]), 1


# ---------------------------------------------------------------------------------------------------------------
# DONDURULMUŞ KURALLAR: (ad, thx, the, mode, hedef, h, beklenen_isaret, açıklama)
# Çürütme taramasından (tara.py) sonra doldurulur; boşsa hiçbir kural dondurulmamıştır.
# ---------------------------------------------------------------------------------------------------------------
FROZEN = []


def build_tarama(P):
    """Dondurulmuş DEĞİL: taramada kullanılan ana sinyallerin nedensellik öz-denetimi için (denetim.py)."""
    out = []
    for ad, mode in (('T_a_kosulsuz', 'none'), ('T_b_sektor_da_guclu', 'ge'), ('T_c_ozgun_gecikme', 'lt')):
        for hedef in ('viop3', 'likit10', 'sepet'):
            sig, min_n = spread(P, lag_signal(P, 1.0, 0.5, ZWIN, mode), hedef)
            out.append({'ad': f'{ad}_{hedef}_h3', 'sig': sig, 'h': 3, 'yon': 'long', 'olcu': 'own', 'arac': 'spot',
                        'birincil': False, 'min_n': min_n, 'beklenen_isaret': +1, 'aciklama': 'tarama sinyali'})
    return out


def build(P):
    out = []
    for ad, thx, the, mode, hedef, h, isaret, acik in FROZEN:
        sig, min_n = spread(P, lag_signal(P, thx, the, ZWIN, mode), hedef)
        out.append({'ad': ad, 'sig': sig, 'h': h, 'yon': 'long', 'olcu': 'own', 'arac': 'spot', 'birincil': True,
                    'min_n': min_n, 'beklenen_isaret': isaret, 'aciklama': acik})
    return out
