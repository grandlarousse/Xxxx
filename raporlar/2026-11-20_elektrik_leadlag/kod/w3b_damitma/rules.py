"""W3-B damıtma — dondurulmuş kurallar (en çok 2). Sözleşme: YONTEM_EK E1; ayrıca 'beklenen_isaret'.

Kurallar IS (→ 2022-12-30) ve OOS-1 (2023-01 → 2025-06) birlikte görülerek seçildi (ikisi de geliştirme verisi);
tek geçerli sınama kasadır (2025-07-01 →). Bütün sabitler sayı olarak yazılıdır; P'den yeniden kestirilmez.

Ortak tanımlar (hepsi t günü kapanışında bilinir):
  evren      = paneldeki XELKT üyeleri; "dolabilir" = elib fill_long (tradable ve t günü tavanda kapanmamış)
  r(t)       = günlük kapanış getirisi (1 bps'e yuvarlanmış)
  oynaklık20 = r'nin son 20 işlem günündeki standart sapması (en az 10 gözlem; t dâhil)
  hacim şoku = ln(TL hacim(t) / önceki 20 günün medyan TL hacmi), [0,05; 20] aralığına kırpılmış oran
  bayrak     = gün içinde tavana değdi ama tavanda kapanmadı | tabana değdi | tabanda kapandı
  dilim(x,n) = dolabilir hisseler içinde x'in gün içi sırası n eşit parçaya bölünür (0 = en düşük; eşitlikte sütun sırası)

KURAL 1  W3B_sade_sakin_guclu_h1   (model yok)
  AL: dolabilir & bayraksız & oynaklık20 sektörün alt yarısında (dilim(·,2)=0; en az 6 hisse)
      & r(t) sektörün en üst üçte birliğinde (dilim(·,3)=2; en az 6 hisse). Giriş t kapanışı, çıkış t+1 kapanışı.
KURAL 2  W3B_lgbm_tahmin20_temiz_h1  (A8 LightGBM h1 kesit tahmini; kod/a8_model/rules.py)
  AL: dolabilir & bayraksız & r(t) en alt beşte birlikte değil & hacim şoku en üst beşte birlikte değil
      & oynaklık20 en üst beşte birlikte değil (beşte birlikler en az 5 hisseyle) & model tahmini > +20 bps.
"""
import os
import sys
import importlib.util
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'ortak'))
import elib  # noqa: E402

VOL_WIN, VOL_MINP = 20, 10
PRED_THR = 0.0020            # +20 bps (IS'te tahminlerin yaklaşık 87. yüzdeliği; komşular 10 ve 30 bps aynı yönde)


def _load_a8():
    spec = importlib.util.spec_from_file_location('a8rules_w3b', os.path.join(HERE, '..', 'a8_model', 'rules.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def bucket(score, uni, nb, min_n):
    """Gün içi sıraya göre 0..nb-1 dilim (0 = en düşük); n < min_n ise NaN (koşul sağlanmaz)."""
    S = score.where(uni)
    n = S.notna().sum(axis=1)
    rk = S.rank(axis=1, method='first')
    b = np.floor((rk - 1).mul(nb).div(n.where(n > 0), axis=0))
    b[(n < min_n).values] = np.nan
    return b


def flags(P, sc):
    lu, ld = P['lim_up'][sc], P['lim_dn'][sc]
    tu = P['lim_up_touch'][sc] if 'lim_up_touch' in P else lu
    td = P['lim_dn_touch'][sc] if 'lim_dn_touch' in P else ld
    return (tu & ~lu) | (td & ~ld) | ld


def sade_sig(P):
    sc = sorted(elib.sector_cols(P))
    R = P['ret_cc'][sc].round(4)
    fill = P['fill_long'][sc]
    valid = P['tradable'][sc] & R.notna()
    vol20 = R.rolling(VOL_WIN, min_periods=VOL_MINP).std().round(8).where(valid)
    low_vol = bucket(vol20, fill, 2, 6) == 0
    strong = bucket(R.where(valid), fill, 3, 6) == 2
    return (fill & ~flags(P, sc) & low_vol & strong).astype(bool)


def model_sig(P):
    a8 = _load_a8()
    fe = a8.features(P)
    pred = a8.predict_sec(P, fe, 1, a8._LGB, {})
    sc, fill = fe['sc'], fe['fill']

    def frame(nm):
        A = np.full((fe['T'], fe['M']), np.nan)
        A[fe['pos'], fe['col']] = fe['X'][:, fe['names'].index(nm)]
        return pd.DataFrame(A, index=fe['dates'], columns=sc)
    clean = (fill & ~flags(P, sc) & ~(bucket(frame('rel1'), fill, 5, 5) == 0)
             & ~(bucket(frame('volshock'), fill, 5, 5) == 4) & ~(bucket(frame('vol20'), fill, 5, 5) == 4))
    return (clean & (pred > PRED_THR)).astype(bool)


def build(P):
    return [
        {'ad': 'W3B_sade_sakin_guclu_h1', 'sig': sade_sig(P), 'h': 1, 'yon': 'long', 'olcu': 'sec', 'arac': 'spot',
         'birincil': True, 'beklenen_isaret': +1,
         'aciklama': 'Sade kural: dolabilir, gün içinde tavana/tabana değmemiş, 20 günlük oynaklığı sektörün alt yarısında ve '
                     'günlük getirisi sektörün en üst üçte birliğinde olan XELKT hissesi AL, 1 gün'},
        {'ad': 'W3B_lgbm_tahmin20_temiz_h1', 'sig': model_sig(P), 'h': 1, 'yon': 'long', 'olcu': 'sec', 'arac': 'spot',
         'birincil': True, 'beklenen_isaret': +1,
         'aciklama': 'A8 LightGBM(d3, yaprak≥500) h1 kesit tahmini > +20 bps ve hisse "temiz" (bayraksız; günlük getiride en alt, '
                     'hacim şokunda ve 20 günlük oynaklıkta en üst beşte birlikte değil) ise AL, 1 gün'},
    ]
