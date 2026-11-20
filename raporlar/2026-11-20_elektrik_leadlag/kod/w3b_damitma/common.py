"""W3-B ortak yardımcılar: panel + A8 modeli (özellikler, LightGBM yürüyen pencere tahmini) + değerlendirme sarmalayıcıları.
Raporlanan her satır elib.evaluate() ile üretilir; yardımcı kırılımlar (gece/gün içi, medyan kıyası, devir) elib'in
excess_measures / day_series / stats_block fonksiyonlarıyla hesaplanır ve 'ek' diye etiketlenir."""
import os
import sys
import importlib.util
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'ortak'))
import elib  # noqa: E402


def load_a8():
    path = os.path.join(HERE, '..', 'a8_model', 'rules.py')
    spec = importlib.util.spec_from_file_location('a8rules', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def feat_frames(fe):
    """A8 özellik matrisini (satır biçimi) tarih×hisse çerçevelerine çevirir."""
    out = {}
    for j, nm in enumerate(fe['names']):
        A = np.full((fe['T'], fe['M']), np.nan)
        A[fe['pos'], fe['col']] = fe['X'][:, j]
        out[nm] = pd.DataFrame(A, index=fe['dates'], columns=fe['sc'])
    return out


def bucket(score, uni, nb=5, min_n=5):
    """Gün içi sıraya göre 0..nb-1 dilim (0 = en düşük). n < min_n ise NaN."""
    S = score.where(uni)
    n = S.notna().sum(axis=1)
    rk = S.rank(axis=1, method='first')
    b = np.floor((rk - 1).mul(nb).div(n.where(n > 0), axis=0))
    b[(n < min_n).values] = np.nan
    return b


KEEP = ['sinyal_tanimi', 'h', 'karar_olcusu', 'n_gun_IS', 'n_islem_IS', 'ort_fazla_IS_bps', 't_IS', 'basabas_IS_bps',
        'isabet_IS', 'net_dusuk_bps_IS', 'net_temel_bps_IS', 'net_muhafazakar_bps_IS', 'n_gun_OOS1', 'n_islem_OOS1',
        'ort_fazla_OOS1_bps', 't_OOS1', 'basabas_OOS1_bps', 'isabet_OOS1', 'net_dusuk_bps_OOS1', 'net_temel_bps_OOS1',
        'net_muhafazakar_bps_OOS1', 'dol_raw_IS_bps', 'dol_raw_OOS1_bps', 'dol_own_IS_bps', 'dol_own_IS_t',
        'dol_own_OOS1_bps', 'dol_own_OOS1_t', 'dol_sec_IS_bps', 'dol_sec_IS_t', 'dol_sec_OOS1_bps', 'dol_sec_OOS1_t',
        'maliyet_temel_bps', 'yil_pozitif_orani', 'yillar_bps', 'top10_haric_bps', 'kirpilmis_ort_bps', 'en_yogun_hisse',
        'en_yogun_pay', 'eski_islem_bps', 'eski_n', 'yeni_islem_bps', 'yeni_n', 'giris_acilis1_bps', 'giris_kapanis1_bps',
        'giris_kapanis0_bps', 'gece_payi']


class Ev:
    def __init__(self, P):
        self.P = P
        self.rows = []

    def __call__(self, sig, name, h=1, measure='sec', soru='', note='', show=True, min_n=1):
        r = elib.evaluate(sig, self.P, h=h, side='long', name=name, family='W3B', measure=measure, min_n=min_n)
        row = {k: r.get(k) for k in KEEP}
        row['soru'] = soru
        row['secim'] = ''
        row['not'] = note
        self.rows.append(row)
        if show:
            print(fmt(row))
        return row


def fmt(r):
    def g(k, d=1):
        v = r.get(k)
        return 'nan' if v is None or v != v else f'{v:.{d}f}'
    nd_is = r['n_islem_IS'] / max(r['n_gun_IS'], 1)
    nd_o = r['n_islem_OOS1'] / max(r['n_gun_OOS1'], 1)
    return (f"{r['sinyal_tanimi'][:44]:44s} h{r['h']} {r['karar_olcusu']} | IS n{r['n_gun_IS']:5d} x{nd_is:4.1f} {g('ort_fazla_IS_bps'):>7s} t{g('t_IS', 2):>6s} "
            f"isb{g('isabet_IS', 3)} net{g('net_temel_bps_IS'):>7s} | OOS n{r['n_gun_OOS1']:4d} x{nd_o:4.1f} {g('ort_fazla_OOS1_bps'):>7s} t{g('t_OOS1', 2):>6s} "
            f"isb{g('isabet_OOS1', 3)} net{g('net_temel_bps_OOS1'):>7s} | own {g('dol_own_IS_bps'):>6s}/{g('dol_own_OOS1_bps'):>6s} raw {g('dol_raw_IS_bps'):>6s}/{g('dol_raw_OOS1_bps'):>6s}")


def per_stats(P, p, ntr, X, h=1):
    return {k: elib.stats_block(p, ntr, X, h, a, b) for k, (a, b) in elib.periods_of(P).items()}
