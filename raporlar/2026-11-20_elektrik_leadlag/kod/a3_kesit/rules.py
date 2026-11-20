"""A3 kesit ailesi — özellikler ve dondurulmuş kurallar (YONTEM_EK E1 sözleşmesi).

Bütün özellikler yalnız t kapanışına kadarki veriden kurulur (rolling/shift; gün içi kesit sırası).
Hisse listesi koda gömülü değildir: evren = elib.sector_cols(P) (panelde bulunan XELKT üyeleri).
Eşikler sayı olarak yazılıdır; P'den yeniden kestirilmez.
"""
import os
import sys

import numpy as np
import pandas as pd

_HERE = os.path.dirname(os.path.abspath(__file__))
_ORTAK = os.path.join(os.path.dirname(_HERE), 'ortak')
if _ORTAK not in sys.path:
    sys.path.insert(0, _ORTAK)
import elib  # noqa: E402

MIN_N = 8          # sıralama için gün içi en az geçerli (tradable) üye
MIN_N3 = 9         # üçte birlikler için en az üye
VOL_WIN = 20       # hacim şoku: log(hacim / t−1'e kadarki 20 günlük medyan)
Z_WIN = 60         # sepet getirisi z'si: 60 günlük std, 1 gün gecikmeli


def qmask(X, frac, side, min_n):
    """Gün içi sıralamada en alt ('bottom') ya da en üst ('top') frac'lık dilim. X: NaN = evren dışı.
    Dilim büyüklüğü floor(n·frac), en az 1. Eşitlikte sütun sırası (deterministik)."""
    n = X.notna().sum(axis=1)
    kq = np.floor(n * frac).clip(lower=1)
    r = X.rank(axis=1, method='first', ascending=(side == 'bottom'))
    m = r.le(kq, axis=0) & X.notna()
    return m & pd.DataFrame(np.repeat((n >= min_n).values[:, None], X.shape[1], axis=1), index=X.index, columns=X.columns)


def bcast(s, like):
    """Tarih serisini (bool) tarih×hisse matrisine yayar."""
    v = s.reindex(like.index).fillna(False).astype(bool).values
    return pd.DataFrame(np.repeat(v[:, None], like.shape[1], axis=1), index=like.index, columns=like.columns)


def feats(P, univ=None):
    """A3 özellikleri. univ: (isteğe bağlı) bool tarih×hisse evren kısıtı (t'de bilinen)."""
    sc = elib.sector_cols(P)
    R = P['ret_cc'][sc]
    T = P['tradable'][sc]
    if univ is not None:
        T = T & univ.reindex_like(T).fillna(False)
    V = P['vol_tl'][sc]
    lr = np.log1p(R)
    F = {'sc': sc, 'R': R, 'T': T}
    for k in (1, 3, 5):
        rk = np.expm1(lr.rolling(k, min_periods=k).sum()).where(T)
        n = rk.notna().sum(axis=1)
        sec = rk.mean(axis=1).where(n >= MIN_N)
        F[f'rk{k}'] = rk
        F[f'sec{k}'] = sec                       # EW sektörün k günlük getirisi
        F[f'rel{k}'] = rk.sub(sec, axis=0)       # hisse − sektör
    Vp = V.where(V > 0)
    vmed = Vp.rolling(VOL_WIN, min_periods=10).median().shift(1)
    F['vs'] = np.log(Vp / vmed).where(T)         # hacim şoku
    adv = elib.adv60(P)[sc].where(T)
    F['adv'] = adv
    # büyüklük üçte birlikleri (t−1'e kadarki 60 günlük medyan TL hacim)
    F['big'] = qmask(adv, 1 / 3, 'top', MIN_N3)
    F['small'] = qmask(adv, 1 / 3, 'bottom', MIN_N3)
    # hacim şoku üçte birlikleri (t günü)
    F['vhi'] = qmask(F['vs'], 1 / 3, 'top', MIN_N3)
    F['vlo'] = qmask(F['vs'], 1 / 3, 'bottom', MIN_N3)
    for g in ('big', 'small', 'vhi', 'vlo'):
        X = R.where(F[g])
        rg = X.mean(axis=1).where(X.notna().sum(axis=1) >= 2)
        F['R_' + g] = rg
        F['z_' + g] = rg / rg.rolling(Z_WIN, min_periods=40).std().shift(1)
    F['px'] = P['close_raw'][sc]
    return F


def top_liquid(P, n=15):
    """t−1'e kadarki adv60'a göre en likit n tradable sektör üyesi."""
    sc = elib.sector_cols(P)
    a = elib.adv60(P)[sc].where(P['tradable'][sc])
    return a.rank(axis=1, ascending=False, method='first') <= n


# ---------------------------------------------------------------------------------------------------
# Tarama ızgarasındaki kural üreticileri (scan.py ve build() aynı işlevleri kullanır)
# ---------------------------------------------------------------------------------------------------
def sig_quint(F, k, side, cond=None, thr=0.02):
    """rel_k beşte birliği. cond: None | 'up' (sektör k günlük > +thr) | 'dn' (< −thr)."""
    s = qmask(F[f'rel{k}'], 0.2, side, MIN_N)
    if cond == 'up':
        s = s & bcast(F[f'sec{k}'] > thr, s)
    elif cond == 'dn':
        s = s & bcast(F[f'sec{k}'] < -thr, s)
    return s


def sig_xgroup(F, src, dst, z, sign=1):
    """Kaynak sepetin (src) t günü getirisi z-eşiğini aşınca hedef sepet (dst) üyeleri."""
    zz = F['z_' + src]
    cond = (zz >= z) if sign > 0 else (zz <= -z)
    return F[dst] & bcast(cond, F[dst])


def build(P):
    """Dondurulmuş kurallar (IS: 2010-01-04 → 2022-12-30). BİRİNCİL KURAL YOK: ızgarada hiçbir satır seçim ölçütlerini
    karşılamadı. Aşağıdakiler yalnız bilgi amaçlı İKİNCİL kurallardır; eşikler sabittir."""
    F = feats(P)
    sc = F['sc']
    vcols = [c for c in elib.VIOP if c in sc]
    rules = [
        {"ad": "A3_rel5_ust5_h3", "sig": sig_quint(F, 5, 'top'), "h": 3, "yon": "long", "olcu": "sec", "arac": "spot",
         "birincil": False, "izgara_adi": "T2_rel5_ust5_h3",
         "aciklama": "5 günlük (hisse − EW sektör) getirisinde en üst beşte birlik (floor(n/5) hisse, n ≥ 8) → t kapanışında AL, 3 gün tut"},
        {"ad": "A3_vhi_z15_vlo_h3", "sig": sig_xgroup(F, 'vhi', 'vlo', 1.5, +1), "h": 3, "yon": "long", "olcu": "own", "arac": "spot",
         "birincil": False, "izgara_adi": "T4_vhi_z15_yukari_vlo_h3_own",
         "aciklama": "Hacim şoku en yüksek üçte birliğin EW getirisi z ≥ 1,5 (60 g std, 1 g gecikmeli) → hacim şoku en düşük üçte birliği AL, 3 gün tut"},
        {"ad": "A3_big_z10_small_h3", "sig": sig_xgroup(F, 'big', 'small', 1.0, +1), "h": 3, "yon": "long", "olcu": "own", "arac": "spot",
         "birincil": False, "izgara_adi": "T3_big_z10_yukari_small_h3_own",
         "aciklama": "adv60'a göre en büyük üçte birliğin EW getirisi z ≥ 1 → en küçük üçte birliği AL, 3 gün tut"},
        {"ad": "A3_rel1_alt5_viop_al_h1", "sig": sig_quint(F, 1, 'bottom')[vcols], "h": 1, "yon": "long", "olcu": "sec", "arac": "viop",
         "birincil": False, "izgara_adi": "K_rel1_alt5_viop_al_h1",
         "aciklama": "KEŞİF: 1 günlük göreli getiride en alt beşte birliğe düşen AKSEN/ENJSA/ODAS → vadelide AL, 1 gün tut"},
        {"ad": "A3_rel1_alt5_h1_RED", "sig": sig_quint(F, 1, 'bottom'), "h": 1, "yon": "long", "olcu": "sec", "arac": "spot",
         "birincil": False, "izgara_adi": "T2_rel1_alt5_h1",
         "aciklama": "HİPOTEZ REDDİ (beklenen işaret NEGATİF; alım kuralı değil): 1 günlük göreli getiride en alt beşte birlik → AL, 1 gün tut"},
    ]
    return rules
