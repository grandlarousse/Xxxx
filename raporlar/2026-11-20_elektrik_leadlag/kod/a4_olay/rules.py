"""A4 (olaylar) — sinyal kurucuları, önceden yazılı ızgara ve dondurulmuş kurallar.

Sözleşme: YONTEM_EK E1. Bütün sinyaller yalnız t kapanışına kadarki bilgiyle kurulur (aynı gün bayrakları, geçmişe
bakan rolling/shift). Tam örneklem istatistiği yok; eşikler sayı olarak yazılı; hisse listesi panelden okunur
(yalnız VİOP üçlüsü elib.VIOP'tan gelir). Ana faaliyet kümesi sabit niteliktir (ek/xelkt_uyeler.csv, yalnız
'ana_faaliyet' sütunu).
"""
import os
import sys
import numpy as np
import pandas as pd

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, '..', 'ortak'))
import elib  # noqa: E402

LIM0 = pd.Timestamp('2015-12-01')      # çift seans bitti; öncesinde tavan/taban bayrakları güvenilmez
UYE_CSV = os.path.join(_HERE, '..', '..', 'ek', 'xelkt_uyeler.csv')


def _kume():
    try:
        m = pd.read_csv(UYE_CSV, usecols=['sym', 'ana_faaliyet'])
        return {s: str(a).replace('?', '').strip() for s, a in zip(m['sym'], m['ana_faaliyet'])}
    except Exception:
        return {}


def _others(X, cond=None):
    """Her hisse için: kendisi hariç X'i sağlayan hisse sayısı (tarih×hisse)."""
    cnt = X.sum(axis=1).values[:, None] - X.values.astype(int)
    return pd.DataFrame(cnt, index=X.index, columns=X.columns)


def _streak(B):
    """Art arda True sayısı (t dâhil), sütun bazında."""
    b = B.astype(int)
    out = {}
    for c in B.columns:
        out[c] = b[c].groupby((~B[c]).cumsum()).cumsum()
    return pd.DataFrame(out, index=B.index, columns=B.columns)


def blocks(P):
    """Olay yapı taşları (hepsi nedensel)."""
    sc = elib.sector_cols(P)
    R = P['ret_cc'][sc]
    idx = R.index
    late = pd.Series(idx >= LIM0, index=idx)
    tr = P['tradable'][sc]
    lu_raw = P['lim_up'][sc].where(late, False).astype(bool)
    ld_raw = P['lim_dn'][sc].where(late, False).astype(bool)
    tu = P['lim_up_touch'][sc].where(late, False).astype(bool)
    td = P['lim_dn_touch'][sc].where(late, False).astype(bool)
    up, dn = lu_raw & tr, ld_raw & tr
    ntr = tr.sum(axis=1)
    B = dict(sc=sc, R=R, tr=tr, up=up, dn=dn, lu_raw=lu_raw, ld_raw=ld_raw, tu=tu, td=td, ntr=ntr)
    B['nup_o'] = _others(up)
    B['ndn_o'] = _others(dn)
    ntr_o = _others(tr).clip(lower=1)
    B['fup_o'] = B['nup_o'] / ntr_o
    B['fdn_o'] = B['ndn_o'] / ntr_o
    # kaynak likiditesi: adv60, o gün tradable sektör üyelerinin kesit medyanına göre
    adv = elib.adv60(P)[sc].where(tr)
    med = adv.median(axis=1)
    hi = adv.ge(med, axis=0) & adv.notna()
    B['up_hi'], B['up_lo'] = up & hi, up & ~hi
    st = _streak(lu_raw)
    B['streak'] = st
    B['up_first'], B['up_cont'] = up & (st == 1), up & (st >= 2)
    # ana faaliyet kümesi
    km = _kume()
    same = pd.DataFrame(0, index=idx, columns=sc)
    B['km'] = km
    for k in sorted(set(km.get(c, 'bilinmiyor') for c in sc)):
        cc = [c for c in sc if km.get(c, 'bilinmiyor') == k]
        if len(cc) >= 2 and k != 'bilinmiyor':
            same[cc] = _others(up[cc])
    B['same_o'] = same
    # sektör günü
    x = P['idx_ret']['XELKT'].reindex(idx)
    z = x / x.rolling(60, min_periods=40).std().shift(1)
    B['x'], B['z'] = x, z
    # genişlik
    Rt = R.where(tr)
    B['b_up'] = (Rt > 0.02).sum(axis=1) / ntr.clip(lower=1)
    B['b_dn'] = (Rt < -0.02).sum(axis=1) / ntr.clip(lower=1)
    # hacim patlaması
    V = P['vol_tl'][sc]
    B['vratio'] = V / V.rolling(20, min_periods=15).median().shift(1)
    # halka arz
    ipo = P['ipo_n'].reindex(index=idx, columns=sc)
    first_row = pd.Series(idx == idx[0], index=idx)
    B['ipo'] = ipo
    B['ipo1'] = ((ipo == 1).any(axis=1)) & ~first_row
    B['ipo5'] = (((ipo >= 1) & (ipo <= 5)).any(axis=1)) & ~first_row
    return B


def _bc(day_cond, like):
    """Günlük koşulu (Series) tarih×hisse matrisine yay."""
    v = np.asarray(day_cond, dtype=bool)
    return pd.DataFrame(np.repeat(v[:, None], like.shape[1], axis=1), index=like.index, columns=like.columns)


def spike(B, mult=3.0, rmin=0.03):
    return (B['vratio'] > mult) & (B['R'] > rmin) & B['tr']


def sector_day(B, kind, thr):
    """kind: 'abs' (XELKT getirisi) | 'z' (60 günlük gecikmeli std'ye oran); thr işaretli."""
    s = B['x'] if kind == 'abs' else B['z']
    return (s >= thr) if thr > 0 else (s <= thr)


def breadth(B, side, share=0.5, min_n=5):
    f = B['b_up'] if side == 'up' else B['b_dn']
    return (f >= share) & (B['ntr'] >= min_n)


def grid(P):
    """Önceden yazılı ızgara: [(ad, olay, sig, yon, arac)] — h ∈ {1,2,3} tarama betiğinde eklenir."""
    B = blocks(P)
    R, tr, up, sc = B['R'], B['tr'], B['up'], B['sc']
    V3 = [c for c in elib.VIOP if c in sc]
    G = []

    def add(ad, olay, sig, yon='long', arac='spot'):
        if arac == 'viop' or ad.endswith('_viop3'):
            sig = sig[V3]
        G.append((ad, olay, sig.fillna(False).astype(bool), yon, arac))

    # ---------------- E1 tavan bulaşması (hedef: tavanda kapanmamış diğer üyeler)
    n = B['nup_o']
    tgt = tr & ~B['lu_raw']
    add('E1_herhangi', 'E1', (n >= 1) & tgt)
    add('E1_n1', 'E1', (n == 1) & tgt)
    add('E1_n2_3', 'E1', (n >= 2) & (n <= 3) & tgt)
    add('E1_n4p', 'E1', (n >= 4) & tgt)
    add('E1_pay10', 'E1', (B['fup_o'] >= 0.10) & tgt)
    add('E1_pay20', 'E1', (B['fup_o'] >= 0.20) & tgt)
    hi_o, lo_o = _others(B['up_hi']), _others(B['up_lo'])
    add('E1_kaynak_likit', 'E1', (hi_o >= 1) & tgt)
    add('E1_kaynak_yalniz_sig', 'E1', (lo_o >= 1) & (hi_o == 0) & tgt)
    f_o, c_o = _others(B['up_first']), _others(B['up_cont'])
    add('E1_kaynak_ilk_gun', 'E1', (f_o >= 1) & tgt)
    add('E1_kaynak_yalniz_seri', 'E1', (c_o >= 1) & (f_o == 0) & tgt)
    add('E1_hedef_hareketli', 'E1', (n >= 1) & (R >= 0.03) & tgt)
    add('E1_hedef_hareketsiz', 'E1', (n >= 1) & (R < 0.03) & tgt)
    add('E1_ayni_kume', 'E1', (B['same_o'] >= 1) & tgt)
    add('E1_yalniz_farkli_kume', 'E1', (n >= 1) & (B['same_o'] == 0) & tgt)
    add('E1_n4p_hareketsiz', 'E1', (n >= 4) & (R < 0.03) & tgt)
    add('E1_n4p_hareketli', 'E1', (n >= 4) & (R >= 0.03) & tgt)
    # ---------------- E2 taban bulaşması
    m = B['ndn_o']
    tgd = tr & ~B['ld_raw']
    add('E2_herhangi_AL', 'E2', (m >= 1) & tgd)
    add('E2_n2p_AL', 'E2', (m >= 2) & tgd)
    add('E2_pay10_AL', 'E2', (B['fdn_o'] >= 0.10) & tgd)
    add('E2_herhangi_SAT', 'E2', (m >= 1) & tgd, 'short', 'viop')
    add('E2_n2p_SAT', 'E2', (m >= 2) & tgd, 'short', 'viop')
    # ---------------- E3 sektör günü
    for lab, kind, thr in [('art3', 'abs', 0.03), ('eks3', 'abs', -0.03), ('zart2', 'z', 2.0), ('zeks2', 'z', -2.0)]:
        d = _bc(sector_day(B, kind, thr), R) & tr
        add(f'E3_{lab}_sektor_AL', 'E3', d)
        add(f'E3_{lab}_AL_viop3', 'E3', d)
        add(f'E3_{lab}_SAT', 'E3', d, 'short', 'viop')
    # ---------------- E4 genişlik
    for lab, side in [('art', 'up'), ('eks', 'dn')]:
        d = _bc(breadth(B, side), R) & tr
        add(f'E4_{lab}_sektor_AL', 'E4', d)
        add(f'E4_{lab}_SAT', 'E4', d, 'short', 'viop')
    # ---------------- E5 hacim patlaması
    sp = spike(B)
    add('E5_kendi_AL', 'E5', sp)
    add('E5_kendi_tavansiz_AL', 'E5', sp & ~B['tu'])
    so = _others(sp)
    add('E5_akran_AL', 'E5', (so >= 1) & ~sp & tr)
    same_sp = pd.DataFrame(0, index=R.index, columns=sc)
    km = B['km']
    for k in sorted(set(km.get(c, 'bilinmiyor') for c in sc)):
        cc = [c for c in sc if km.get(c, 'bilinmiyor') == k]
        if len(cc) >= 2 and k != 'bilinmiyor':
            same_sp[cc] = _others(sp[cc])
    add('E5_akran_ayni_kume_AL', 'E5', (same_sp >= 1) & ~sp & tr)
    add('E5_kendi_SAT', 'E5', sp, 'short', 'viop')
    # ---------------- E6 kendi tavanı / tabanı
    touch = B['tu'] & ~B['lu_raw'] & tr
    add('E6_degdi_kapanmadi_AL', 'E6', touch)
    add('E6_degdi_kapanmadi_SAT', 'E6', touch, 'short', 'viop')
    add('E6_tavanda_kapandi_BILGI', 'E6', up)
    add('E6_tabana_degdi_kapanmadi_AL', 'E6', B['td'] & ~B['ld_raw'] & tr)
    # ---------------- E7 tavan serisinin bitişi
    st = B['streak']
    end_raw = (~B['lu_raw']) & (st.shift(1) >= 2) & R.notna()
    end_tr = end_raw & tr
    add('E7_kendi_AL', 'E7', end_tr)
    add('E7_akran_AL', 'E7', (_others(end_tr) >= 1) & ~end_tr & tr)
    add('E7_akran_halkaarz_dahil_AL', 'E7', (_others(end_raw) >= 1) & ~end_raw & tr)
    add('E7_kendi_SAT', 'E7', end_tr, 'short', 'viop')
    # ---------------- E8 yeni halka arz
    add('E8_ilk_gun_AL', 'E8', _bc(B['ipo1'], R) & tr)
    add('E8_ilk5_gun_AL', 'E8', _bc(B['ipo5'], R) & tr)
    return G, B


def grid_extra(P, B=None):
    """Komşu parametre / keşif denemeleri (ızgara dışı; test sayısına dâhil, aday seçiminde yalnız (vi) için)."""
    B = B or blocks(P)
    R, tr, sc = B['R'], B['tr'], B['sc']
    V3 = [c for c in elib.VIOP if c in sc]
    G = []

    def add(ad, olay, sig, yon='long', arac='spot'):
        if arac == 'viop':
            sig = sig[V3]
        G.append((ad, olay, sig.fillna(False).astype(bool), yon, arac))
    n = B['nup_o']
    tgt = tr & ~B['lu_raw']
    add('E1x_pay05', 'E1', (B['fup_o'] >= 0.05) & tgt)
    add('E1x_n2p', 'E1', (n >= 2) & tgt)
    ew = elib.ew_basket(P, cols=sc)
    add('E1x_herhangi_sepet_arti', 'E1', (n >= 1) & tgt & _bc(ew > 0, R))
    add('E1x_herhangi_sepet_eksi', 'E1', (n >= 1) & tgt & _bc(ew <= 0, R))
    Rt = R.where(tr)
    for lab, thr, share in [('pay40', 0.02, 0.4), ('pay60', 0.02, 0.6), ('esik15', 0.015, 0.5), ('esik30', 0.03, 0.5)]:
        f = (Rt < -thr).sum(axis=1) / B['ntr'].clip(lower=1)
        d = _bc((f >= share) & (B['ntr'] >= 5), R) & tr
        add(f'E4x_eks_{lab}_SAT', 'E4', d, 'short', 'viop')
        add(f'E4x_eks_{lab}_sektor_AL', 'E4', d)
    for lab, share in [('pay40', 0.4), ('pay60', 0.6)]:
        add(f'E4x_art_{lab}_sektor_AL', 'E4', _bc(breadth(B, 'up', share), R) & tr)
    touch = B['tu'] & ~B['lu_raw'] & tr
    add('E6x_degdi_kapanis_guclu', 'E6', touch & (R >= 0.05))
    add('E6x_degdi_kapanis_zayif', 'E6', touch & (R < 0.05))
    return G


# ------------------------------------------------------------------------------------------------------------------
# Dondurulmuş kurallar (IS taramasından sonra doldurulur)
# ------------------------------------------------------------------------------------------------------------------
def build(P):
    """YONTEM_EK E1 sözleşmesi. Birincil kural YOK (IS'te ölçütleri karşılayan çıkmadı); 5 ikincil (izleme) kuralı."""
    G, B = grid(P)
    G = G + grid_extra(P, B)
    S = {ad: (sig, yon, arac) for ad, olay, sig, yon, arac in G}
    out = []
    for ad, h, birincil, acik in FROZEN:
        sig, yon, arac = S[ad]
        out.append({'ad': f'A4_{ad}_h{h}', 'sig': sig, 'h': h, 'yon': yon, 'olcu': 'own', 'arac': arac,
                    'birincil': birincil, 'aciklama': acik})
    return out


# (ızgara adı, h, birincil mi, açıklama) — eşikler grid()/grid_extra() içinde sayı olarak yazılıdır
FROZEN = [
    ('E1_herhangi', 3, False,
     'XELKT üyelerinden en az biri (hedef hariç, tradable) t günü tavanda kapandı -> tavanda kapanmamış diğer '
     'tradable üyeler AL, 3 gün (2015-12-01 sonrası bayraklar)'),
    ('E1x_herhangi_sepet_arti', 2, False,
     'KEŞİF: E1 koşulu VE aynı gün tradable üyelerin eşit ağırlıklı getirisi > 0 -> tavanda kapanmamış diğer '
     'üyeler AL, 2 gün'),
    ('E4_eks_SAT', 2, False,
     'Tradable XELKT üyelerinin >= %50\'si t günü < -%2 (en az 5 üye) -> AKSEN/ENJSA/ODAS vadelisinde SAT, 2 gün'),
    ('E6_degdi_kapanmadi_SAT', 1, False,
     'AKSEN/ENJSA/ODAS t günü tavana değdi ama tavanda kapanmadı -> aynı hissenin vadelisinde SAT, 1 gün '
     '(IS\'te yalnız 7 olay)'),
    ('E5_akran_AL', 3, False,
     'Başka bir tradable üyede hacim > 3 x önceki 20 günün medyanı ve getiri > +%3 -> kendisi patlama yapmamış '
     'diğer tradable üyeler AL, 3 gün (IS\'te temel maliyetin altında)'),
]
