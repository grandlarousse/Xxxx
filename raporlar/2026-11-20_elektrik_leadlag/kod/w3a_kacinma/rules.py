"""W3-A (kaçınma ve SAT sinyalleri) — özellikler, tetikler ve DONDURULMUŞ kurallar (YONTEM_EK E1 sözleşmesi).

Bütün girdiler yalnız t kapanışına kadarki bilgiyle kurulur (aynı gün bayrakları ve kesiti; geçmişe bakan
rolling + shift). Tam örneklem istatistiği yok; eşikler sayı olarak yazılı. Hisse listesi panelden okunur
(evren = elib.sector_cols(P)); VİOP üçlüsü elib.VIOP.

Kural sözlüklerinde ek alan: "beklenen_isaret" = −1 (kaçınma: AL pozisyonunun fazla getirisi EKSİ beklenir) ya da
+1 (pozisyon kazandırır).
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

LIM0 = pd.Timestamp('2015-12-01')       # çift seans bitti; öncesinde tavan/taban bayrakları güvenilmez
MARJ10 = pd.Timestamp('2020-03-13')     # bu tarihten itibaren günlük marj ±%10, öncesi ±%20
MIN_N = 8                               # göreli getiri (rel_k) için gün içi en az tradable üye
Z_WIN, Z_MINP = 60, 40                  # sektör sepeti z'si: 60 günlük std, 1 gün gecikmeli


def bcast(s, like):
    """Günlük (bool) seriyi tarih×hisse matrisine yayar."""
    v = s.reindex(like.index).fillna(False).astype(bool).values
    return pd.DataFrame(np.repeat(v[:, None], like.shape[1], axis=1), index=like.index, columns=like.columns)


def qmask(X, frac, side, min_n):
    """Gün içi sıralamada en alt ('bottom') / en üst ('top') frac'lık dilim (floor(n·frac), en az 1; n ≥ min_n)."""
    n = X.notna().sum(axis=1)
    kq = np.floor(n * frac).clip(lower=1)
    r = X.rank(axis=1, method='first', ascending=(side == 'bottom'))
    m = r.le(kq, axis=0) & X.notna()
    return m & bcast(n >= min_n, X)


def feats(P):
    sc = elib.sector_cols(P)
    R = P['ret_cc'][sc]
    idx = R.index
    late = pd.Series(idx >= LIM0, index=idx)
    tr = P['tradable'][sc]
    F = {'sc': sc, 'R': R, 'tr': tr}
    for k in ('lim_up', 'lim_dn', 'lim_up_touch', 'lim_dn_touch'):
        F[k] = P[k][sc].where(late, False).astype(bool)
    marj = pd.Series(np.where(idx >= MARJ10, 0.10, 0.20), index=idx)
    # kapanışın tavan fiyatına uzaklığı: (1 + marj) / (1 + r_cc) − 1   (taban için simetrik)
    F['tavan_uzak'] = (1.0 / (1 + R)).mul(1 + marj, axis=0) - 1
    F['taban_uzak'] = (1 + R).div(1 - marj, axis=0) - 1
    lr = np.log1p(R)
    for k in (1, 3):
        rk = np.expm1(lr.rolling(k, min_periods=k).sum()).where(tr)
        n = rk.notna().sum(axis=1)
        F[f'rel{k}'] = rk.sub(rk.mean(axis=1).where(n >= MIN_N), axis=0)      # hisse − EW sektör (k gün)
    ew = elib.ew_basket(P, cols=sc, min_n=5)                                   # tradable üyelerin EW r_cc(t)'si
    F['ew'] = ew
    F['z'] = ew / ew.rolling(Z_WIN, min_periods=Z_MINP).std().shift(1)
    V = P['vol_tl'][sc]
    Vp = V.where(V > 0)
    F['vratio'] = Vp / Vp.rolling(20, min_periods=10).median().shift(1)        # hacim / önceki 20 günün medyanı
    adv = elib.adv60(P)[sc].where(tr)
    F['likit'] = qmask(adv, 1 / 3, 'top', 9)
    F['sig'] = qmask(adv, 1 / 3, 'bottom', 9)
    F['orta'] = adv.notna() & ~F['likit'] & ~F['sig'] & bcast(adv.notna().sum(axis=1) >= 9, adv)
    F['px5'] = P['close_raw'][sc] >= 5.0
    return F


def triggers(F):
    """Temel tetikler (bool tarih×hisse; True = t günü işaretli). Hepsi t kapanışında bilinir."""
    R, tr = F['R'], F['tr']
    lu, ld, tu, td = F['lim_up'], F['lim_dn'], F['lim_up_touch'], F['lim_dn_touch']
    T = {}
    T['K1'] = tu & ~lu & tr                                  # tavana değdi, tavanda kapanmadı
    T['K2'] = td & ~ld & tr                                  # tabana değdi, tabanda kapanmadı
    T['K3'] = ld & tr                                        # tabanda kapandı
    T['K4q'] = qmask(F['rel1'], 0.2, 'bottom', MIN_N)        # günün sektöre göre en kötü beşte birliği
    T['K4a3'] = (F['rel1'] <= -0.03) & tr                    # sektörden ≥ %3 geride
    T['K4a5'] = (F['rel1'] <= -0.05) & tr                    # sektörden ≥ %5 geride
    T['K4q_k3'] = qmask(F['rel3'], 0.2, 'bottom', MIN_N)
    T['K4a5_k3'] = (F['rel3'] <= -0.05) & tr
    T['K4a8_k3'] = (F['rel3'] <= -0.08) & tr
    dn, up = bcast(F['z'] <= -1.5, R), bcast(F['z'] >= 1.5, R)
    diren = R.gt(0.5 * F['ew'], axis=0)                      # sepetin düşüşünün yarısından az düştü / yükseldi
    T['K5'] = dn & diren & tr                                # sektör sert düşerken direnen
    T['K5tum'] = dn & tr
    T['K5dusen'] = dn & ~diren & tr
    T['K6'] = up & tr                                        # sektör sert yükseldi: bütün hisseler
    T['K6geciken'] = up & R.lt(0.5 * F['ew'], axis=0) & tr
    T['K6onde'] = up & ~R.lt(0.5 * F['ew'], axis=0) & tr
    T['K5abs3'] = bcast(F['ew'] <= -0.03, R) & diren & tr
    T['K6abs3'] = bcast(F['ew'] >= 0.03, R) & tr
    # ---- komşu parametreler (duyarlılık sınaması)
    T['K23'] = td & tr                                       # tabana değdi (tabanda kapansın ya da kapanmasın)
    T['K4a4'] = (F['rel1'] <= -0.04) & tr
    T['K4a7'] = (F['rel1'] <= -0.07) & tr
    T['K5z10'] = bcast(F['z'] <= -1.0, R) & diren & tr
    T['K5z20'] = bcast(F['z'] <= -2.0, R) & diren & tr
    T['K5arti'] = dn & (R > 0) & tr                          # sert düşüş günü artıda kapanan
    T['K5yarim_ustu'] = dn & R.gt(F['ew'], axis=0) & tr      # sert düşüş günü sektörden iyi (rel > 0)
    return {k: v.fillna(False).astype(bool) for k, v in T.items()}


def build(P):
    """Dondurulmuş kurallar (geliştirme verisi: IS + OOS-1, 2010-01-04 → 2025-06-30). Kasada bir kez sınanır."""
    F = feats(P)
    T = triggers(F)
    return frozen(F, T)


def frozen(F, T):
    """En çok 4 kural. Eşikler sabit sayılardır (0,05; −1,0; 0,5); P'den hiçbir şey kestirilmez."""
    sc = F['sc']
    v3 = [c for c in elib.VIOP if c in sc]
    return [
        {"ad": "W3A_tavana_degdi_kapanmadi_KACIN_h1", "sig": T['K1'], "h": 1, "yon": "long", "olcu": "own",
         "arac": "spot", "birincil": True, "beklenen_isaret": -1,
         "aciklama": "KAÇINMA: hisse t günü tavan fiyatına değdi ama tavanda kapanmadı (lim_up_touch & ~lim_up; tradable; "
                     "2015-12-01 sonrası) -> t kapanışında ALMA; AL pozisyonunun 1 günlük fazla getirisi (own) EKSİ beklenir"},
        {"ad": "W3A_sektorden_5puan_geride_KACIN_h1", "sig": T['K4a5'], "h": 1, "yon": "long", "olcu": "sec",
         "arac": "spot", "birincil": True, "beklenen_isaret": -1,
         "aciklama": "KAÇINMA: hissenin t günü getirisi − tradable XELKT üyelerinin eşit ağırlıklı getirisi <= −%5 (n >= 8; "
                     "tabanda kapananlar dâhil) -> t kapanışında ALMA; AL pozisyonunun 1 günlük sektöre göre getirisi (sec) EKSİ beklenir"},
        {"ad": "W3A_sektor_dustu_direnen_VIOP_SAT_h1", "sig": T['K5z10'][v3], "h": 1, "yon": "short", "olcu": "own",
         "arac": "viop", "birincil": True, "beklenen_isaret": 1,
         "aciklama": "SAT: tradable XELKT üyelerinin eşit ağırlıklı getirisi / 60 günlük gecikmeli std <= −1 ve AKSEN/ENJSA/ODAS "
                     "o gün sepetin düşüşünün yarısından az düştü ya da yükseldi (r_i > 0,5·sepet) -> aynı hissenin vadelisinde SAT, 1 gün"},
    ]
