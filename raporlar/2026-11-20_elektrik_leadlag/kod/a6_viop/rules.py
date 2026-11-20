"""a6_viop/rules.py — VİOP ailesi (A6) sinyal kurucuları ve dondurulmuş kurallar.
Sözleşme: YONTEM_EK E1. build(P) yalnız t ve öncesini kullanır (shift/rolling); eşikler sayı olarak yazılıdır.
Bağımlılık: yalnız numpy/pandas (elib gerekmez). P = elib.load(panel_klasoru)."""
import numpy as np
import pandas as pd

TRIO = ['AKSEN', 'ENJSA', 'ODAS']            # VİOP pay vadelisi olan XELKT üyeleri (çifte özgü: kontrat listesi)
KOMSU = ['ASTOR', 'ALARK', 'EUPWR', 'GESAN']  # sektör dışı komşular (hedef değildir)
Z_WIN, Z_MINP = 120, 60                       # Δbaz z-skoru: 120 günlük gecikmeli std
R_WIN, R_MINP = 60, 40                        # getiri z-skoru: 60 günlük gecikmeli std (YONTEM ortak ızgara)
SP_K, SP_WIN, SP_MINP = 3.0, 20, 15           # sıçrama: > 3 × 20 günlük gecikmeli medyan


# ---------------------------------------------------------------- yardımcılar
def _idx(P):
    return P['ret_cc'].index


def trio_cols(P):
    return [c for c in TRIO if c in P['ret_cc'].columns]


def sector_cols(P):
    return [c for c in P['ret_cc'].columns if c not in KOMSU]


def front_wide(P, col, unds):
    """viop_front (gün × dayanak; o gün hacmi en yüksek vade) → geniş matris, spot takviminde."""
    vf = P['viop_front']
    vf = vf[vf['und'].isin(unds)]
    W = vf.assign(date=pd.to_datetime(vf['date'])).pivot_table(index='date', columns='und', values=col, aggfunc='last')
    W.columns = [str(c) for c in W.columns]
    return W.reindex(index=_idx(P), columns=list(unds))


def ca_mask(P, cols):
    """t günü kurumsal işlem / temettü bayrağı (px.ca dolu)."""
    M = pd.DataFrame(False, index=_idx(P), columns=list(cols))
    if 'px' in P and 'ca' in P['px'].columns:
        px = P['px']
        x = px[px['ca'].notna() & (px['ca'].astype(str) != '') & px['sym'].isin(cols)]
        for d, s in zip(pd.to_datetime(x['date']), x['sym']):
            if d in M.index:
                M.loc[d, s] = True
    return M


def dbaz(P, kind='settle'):
    """Δbaz(t) = ln(1+vadeli getirisi(t)) − ln(1+spot r_cc(t)). Aynı kontrat (ret_settle/ret_last), düzeltilmiş spot.
    kind: 'settle' (uzlaşma) | 'last' (son fiyat). Sütunlar: üçlü + XU030. Kurumsal işlem günü boş."""
    col = 'ret_settle' if kind == 'settle' else 'ret_last'
    cols = trio_cols(P)
    F = front_wide(P, col, cols + ['XU030'])
    cm = ca_mask(P, cols)
    out = pd.DataFrame(index=_idx(P))
    for c in cols:
        out[c] = (np.log1p(F[c]) - np.log1p(P['ret_cc'][c])).where(~cm[c])
    out['XU030'] = np.log1p(F['XU030']) - np.log1p(P['idx_ret']['XU030'].reindex(_idx(P)))
    return out


def zlag(x, win, minp):
    """x(t) / std(x(t−win … t−1))."""
    return x / x.shift(1).rolling(win, min_periods=minp).std()


def spike(x, k=SP_K, win=SP_WIN, minp=SP_MINP):
    med = x.shift(1).rolling(win, min_periods=minp).median()
    return ((x > k * med) & (med > 0)).fillna(False)


def bcast(flag, cols, P):
    f = flag.reindex(_idx(P)).fillna(False).astype(bool)
    return pd.DataFrame({c: f.values for c in cols}, index=_idx(P))


def _thr(z, thr, up):
    return ((z >= thr) if up else (z <= -thr)).fillna(False)


# ---------------------------------------------------------------- sinyal aileleri
def v1_sig(P, kind, thr, up):
    """V1: kendi baz sıçraması. z(Δbaz) ≥ thr (up) ya da ≤ −thr. Hedef: aynı dayanak (üçlü)."""
    z = zlag(dbaz(P, kind)[trio_cols(P)], Z_WIN, Z_MINP)
    return _thr(z, thr, up)


def v2_sig(P, tur, up):
    """V2: vadeli hacim (bütün vadeler, TL) ya da açık pozisyon artışı sıçraması; yön = o günkü vadeli uzlaşma getirisi işareti.
    hacim: V(t) > 3 × medyan20(V).  ap: ΔAP(t) > 3 × medyan20(|ΔAP|)."""
    cols = trio_cols(P)
    r = front_wide(P, 'ret_settle', cols)
    if tur == 'hacim':
        s = spike(front_wide(P, 'toplam_hacim_tl', cols))
    else:
        d = front_wide(P, 'toplam_acik_poz', cols).diff()
        med = d.abs().shift(1).rolling(SP_WIN, min_periods=SP_MINP).median()
        s = ((d > SP_K * med) & (med > 0)).fillna(False)
    return s & ((r > 0) if up else (r < 0)).fillna(False)


def v3_flag(P, kind, thr, up):
    """V3: XU030 vadelisi baz sıçraması (zaman serisi bayrağı)."""
    z = zlag(dbaz(P, kind)['XU030'], Z_WIN, Z_MINP)
    return _thr(z, thr, up)


def v3_sig(P, kind, thr, up, hedef):
    cols = trio_cols(P) if hedef == 'trio' else sector_cols(P)
    return bcast(v3_flag(P, kind, thr, up), cols, P)


def v4_sig(P, kaynak, thr, up):
    """V4: üçlüden bir BAŞKASININ vadeli getirisi (z60) ya da Δbaz'ı (uzlaşma, z120) eşiği aştı → hedef = diğerleri."""
    cols = trio_cols(P)
    if kaynak == 'getiri':
        z = zlag(front_wide(P, 'ret_settle', cols), R_WIN, R_MINP)
    else:
        z = zlag(dbaz(P, 'settle')[cols], Z_WIN, Z_MINP)
    hit = _thr(z, thr, up)
    out = pd.DataFrame(False, index=_idx(P), columns=cols)
    for c in cols:
        others = [o for o in cols if o != c]
        if others:
            out[c] = hit[others].any(axis=1)
    return out


def grid(P):
    """Önceden yazılı ızgara (YONTEM §6 A6 + görev tanımı). Her öğe rules.py sözleşmesinde bir kural sözlüğü + 'aile'."""
    R = []

    def add(ad, sig, h, yon, arac, aile, acik, min_n=1):
        R.append({'ad': ad, 'sig': sig, 'h': h, 'yon': yon, 'olcu': 'own', 'arac': arac, 'birincil': False,
                  'aciklama': acik, 'aile': aile, 'min_n': min_n})
    for kind in ['settle', 'last']:
        for thr in [1.0, 1.5, 2.0]:
            for up in [True, False]:
                s = v1_sig(P, kind, thr, up)
                d = 'yuk' if up else 'asg'
                for h in [1, 2, 3]:
                    add(f'V1_{kind}_z{thr}_{d}_spotAL_h{h}', s, h, 'long', 'spot', 'V1', f'kendi Δbaz({kind}) z {"≥" if up else "≤−"}{thr} → spot AL')
                    add(f'V1_{kind}_z{thr}_{d}_viop{"SAT" if up else "AL"}_h{h}', s, h, 'short' if up else 'long', 'viop', 'V1',
                        f'kendi Δbaz({kind}) z {"≥" if up else "≤−"}{thr} → vadeli {"SAT" if up else "AL"} (bazın geri dönmesi)')
    for tur in ['hacim', 'ap']:
        for up in [True, False]:
            s = v2_sig(P, tur, up)
            for h in [1, 2, 3]:
                if up:
                    add(f'V2_{tur}_yuk_spotAL_h{h}', s, h, 'long', 'spot', 'V2', f'vadeli {tur} sıçraması + gün yukarı → spot AL')
                    add(f'V2_{tur}_yuk_viopAL_h{h}', s, h, 'long', 'viop', 'V2', f'vadeli {tur} sıçraması + gün yukarı → vadeli AL')
                else:
                    add(f'V2_{tur}_asg_viopSAT_h{h}', s, h, 'short', 'viop', 'V2', f'vadeli {tur} sıçraması + gün aşağı → vadeli SAT')
    for kind in ['settle', 'last']:
        for thr in [1.0, 1.5, 2.0]:
            for up in [True, False]:
                d = 'yuk' if up else 'asg'
                ss = v3_sig(P, kind, thr, up, 'sektor'); st = v3_sig(P, kind, thr, up, 'trio')
                for h in [1, 2, 3]:
                    add(f'V3_{kind}_z{thr}_{d}_sektorAL_h{h}', ss, h, 'long', 'spot', 'V3', f'XU030 vadelisi Δbaz({kind}) z {"≥" if up else "≤−"}{thr} → dolabilir sektör hisseleri spot AL', 5)
                    add(f'V3_{kind}_z{thr}_{d}_viop{"AL" if up else "SAT"}_h{h}', st, h, 'long' if up else 'short', 'viop', 'V3',
                        f'XU030 vadelisi Δbaz({kind}) z {"≥" if up else "≤−"}{thr} → üçlü vadeli {"AL" if up else "SAT"}')
    for kaynak in ['getiri', 'dbaz']:
        for thr in [1.0, 1.5, 2.0]:
            for up in [True, False]:
                d = 'yuk' if up else 'asg'
                s = v4_sig(P, kaynak, thr, up)
                for h in [1, 2, 3]:
                    add(f'V4_{kaynak}_z{thr}_{d}_spotAL_h{h}', s, h, 'long', 'spot', 'V4', f'üçlüden diğerinin vadeli {kaynak} z {"≥" if up else "≤−"}{thr} → hedef spot AL')
                    add(f'V4_{kaynak}_z{thr}_{d}_viop{"AL" if up else "SAT"}_h{h}', s, h, 'long' if up else 'short', 'viop', 'V4',
                        f'üçlüden diğerinin vadeli {kaynak} z {"≥" if up else "≤−"}{thr} → hedef vadeli {"AL" if up else "SAT"}')
    return R


# ---------------------------------------------------------------- dondurulmuş kurallar (IS: → 2022-12-30)
def v4k_sig(P):
    """KEŞİF (ızgara dışı): V4 getiri z≥1 sinyali VE hedefin kendi spot getirisi o gün 1σ'nın altında (hedef henüz hareket etmemiş)."""
    cols = trio_cols(P)
    own_z = zlag(P['ret_cc'][cols], R_WIN, R_MINP)
    return v4_sig(P, 'getiri', 1.0, True) & ~(own_z >= 1.0).fillna(False)


# ızgara adı → (dondurulmuş ad, birincil mi)
FROZEN = {
    'V4_getiri_z1.0_yuk_spotAL_h2': ('A6_V4_akran_vadeli_getiri_z1_spotAL_h2', True),
    'V4_getiri_z1.0_yuk_spotAL_h3': ('A6_V4_akran_vadeli_getiri_z1_spotAL_h3', False),
    'V4_getiri_z1.0_yuk_viopAL_h2': ('A6_V4_akran_vadeli_getiri_z1_viopAL_h2', False),
    'V1_settle_z1.5_yuk_spotAL_h2': ('A6_V1_dbaz_uzl_z1.5_yuk_spotAL_h2', False),
    'V1_settle_z1.0_yuk_spotAL_h3': ('A6_V1_dbaz_uzl_z1_yuk_spotAL_h3', False),
    'V2_hacim_yuk_spotAL_h3': ('A6_V2_vadeli_hacim3x_yuk_spotAL_h3', False),
    'V4K_getiri_z1.0_yuk_kendiz_lt1_spotAL_h2': ('A6_V4K_kesif_akran_z1_kendi_lt1_spotAL_h2', False),
}


def kesif(P):
    """Izgara dışı (keşif) dondurulan tek kural; ızgara sözlüğüyle aynı biçimde."""
    return [{'ad': 'V4K_getiri_z1.0_yuk_kendiz_lt1_spotAL_h2', 'sig': v4k_sig(P), 'h': 2, 'yon': 'long', 'olcu': 'own', 'arac': 'spot',
             'birincil': False, 'aile': 'V4-kesif', 'min_n': 1,
             'aciklama': 'KEŞİF: üçlüden diğerinin vadeli getirisi z ≥ 1 ve hedefin kendi getirisi z < 1 → hedef spot AL'}]


def build(P):
    """Dondurulmuş kurallar: 1 birincil + 6 ikincil. Hedef sütunları: AKSEN/ENJSA/ODAS'tan panelde olanlar.
    Girdi: viop_front (ret_settle, toplam_hacim_tl), ret_cc, px.ca. Bütün pencereler gecikmeli (shift(1).rolling)."""
    v4 = v4_sig(P, 'getiri', 1.0, True)      # başka bir üçlü üyesinin vadeli uzlaşma getirisi / std60(t−1) ≥ 1
    R = [
        ('A6_V4_akran_vadeli_getiri_z1_spotAL_h2', v4, 2, 'long', 'spot', True,
         'AKSEN/ENJSA/ODAS içinde hedef dışındaki bir üyenin yakın vade vadeli uzlaşma getirisi, kendi 60 günlük gecikmeli std\'sinin ≥ 1 katı → hedef spot AL, 2 gün'),
        ('A6_V4_akran_vadeli_getiri_z1_spotAL_h3', v4, 3, 'long', 'spot', False, 'aynı sinyal → hedef spot AL, 3 gün'),
        ('A6_V4_akran_vadeli_getiri_z1_viopAL_h2', v4, 2, 'long', 'viop', False, 'aynı sinyal → hedef pay vadelisi AL, 2 gün'),
        ('A6_V1_dbaz_uzl_z1.5_yuk_spotAL_h2', v1_sig(P, 'settle', 1.5, True), 2, 'long', 'spot', False,
         'kendi Δbaz (ln(1+vadeli uzlaşma getirisi) − ln(1+spot getirisi)) / std120(t−1) ≥ 1,5 → aynı hisse spot AL, 2 gün'),
        ('A6_V1_dbaz_uzl_z1_yuk_spotAL_h3', v1_sig(P, 'settle', 1.0, True), 3, 'long', 'spot', False,
         'kendi Δbaz z ≥ 1 → aynı hisse spot AL, 3 gün'),
        ('A6_V2_vadeli_hacim3x_yuk_spotAL_h3', v2_sig(P, 'hacim', True), 3, 'long', 'spot', False,
         'vadeli toplam TL hacmi > 3 × 20 günlük gecikmeli medyan ve vadeli uzlaşma getirisi > 0 → aynı hisse spot AL, 3 gün'),
        ('A6_V4K_kesif_akran_z1_kendi_lt1_spotAL_h2', v4k_sig(P), 2, 'long', 'spot', False,
         'KEŞİF (ızgara dışı): birincil sinyal ve hedefin kendi spot getirisi / std60(t−1) < 1 → hedef spot AL, 2 gün'),
    ]
    return [{'ad': ad, 'sig': sig.astype(bool), 'h': h, 'yon': yon, 'olcu': 'own', 'arac': arac, 'birincil': b, 'aciklama': ac}
            for ad, sig, h, yon, arac, b, ac in R]
