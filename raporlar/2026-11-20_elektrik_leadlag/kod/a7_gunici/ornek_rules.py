"""ornek_rules.py — vekil.py'yi sınamak için ÖRNEK kurallar (YONTEM §6 ortak ızgarasından genel eşikler).
Aday DEĞİLDİR (A7 aday üretmez); yalnız aracın farklı girdi türleriyle (öz getiri, z, endeks, çok günlük birikim,
tavan kilidi) doğru çalıştığını göstermek içindir."""
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ortak'))
import elib  # noqa: E402


def build(P):
    sc = elib.sector_cols(P)
    R = P['ret_cc'][sc]
    tr = P['tradable'][sc]
    z = R / R.rolling(60, min_periods=30).std().shift(1)
    xel = P['idx_ret']['XELKT'].reindex(R.index)
    bas = elib.ew_basket(P)
    L = elib.level(R)
    r3 = L / L.shift(3) - 1
    b = (1 + bas.fillna(0)).cumprod()
    b3 = b / b.shift(3) - 1
    lu = P['lim_up'][sc]
    diger_tavan = (-lu.astype(int)).add(lu.sum(axis=1), axis=0) >= 1
    gun = pd.DataFrame(True, index=R.index, columns=sc)
    return [
        {'ad': 'ORN_oz_up5_h1', 'sig': (R >= 0.05) & tr, 'h': 1, 'yon': 'long', 'olcu': 'sec', 'arac': 'spot',
         'birincil': False, 'aciklama': 'hissenin kendi günlük getirisi ≥ +%5'},
        {'ad': 'ORN_oz_z2_h1', 'sig': (z >= 2) & tr, 'h': 1, 'yon': 'long', 'olcu': 'sec', 'arac': 'spot',
         'birincil': False, 'aciklama': 'öz getiri z ≥ 2 (60 gün, 1 gün gecikmeli std)'},
        {'ad': 'ORN_xelkt_up3_h1', 'sig': gun.mul(xel >= 0.03, axis=0) & tr, 'h': 1, 'yon': 'long', 'olcu': 'own',
         'arac': 'spot', 'birincil': False, 'aciklama': 'XELKT ≥ +%3 günü bütün üyeler'},
        {'ad': 'ORN_geride3_h2', 'sig': (r3.sub(b3, axis=0) <= -0.05) & tr, 'h': 2, 'yon': 'long', 'olcu': 'sec',
         'arac': 'spot', 'birincil': False, 'aciklama': '3 günlük getiri sektör sepetinin ≥ 5 puan gerisinde'},
        {'ad': 'ORN_tavan_bulasma_h1', 'sig': diger_tavan & ~lu & tr, 'h': 1, 'yon': 'long', 'olcu': 'own',
         'arac': 'spot', 'birincil': False, 'aciklama': 'başka bir üye tavanda kapandı; kendisi tavanda değil'},
    ]
