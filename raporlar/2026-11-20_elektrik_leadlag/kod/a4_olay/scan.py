"""A4 tarama: önceden yazılı ızgaranın tamamını IS'te elib.evaluate ile değerlendirir.
Kullanım: python3 -I scan.py <panel_is klasörü> <çıktı csv>"""
import os
import sys
import numpy as np
import pandas as pd

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(_HERE, '..', 'ortak'))
import elib  # noqa: E402
import rules  # noqa: E402

H1_END = pd.Timestamp('2019-12-31')
H2_START = pd.Timestamp('2020-01-01')


def halves(sig, P, h, side, measure='own', instrument='spot'):
    """IS'in iki yarısı (≤2019, 2020–2022): dolabilir gözlemlerde günlük kümelenmiş ortalama, t, bağımsız olay."""
    cols = [c for c in sig.columns if c in P['ret_cc'].columns]
    s = sig[cols].reindex(P['ret_cc'].index).fillna(False).astype(bool)
    if instrument == 'viop':
        cols = [c for c in cols if c in elib.VIOP]
        s = s[cols].copy()
        for c in cols:
            s.loc[s.index < pd.Timestamp(elib.VIOP_START[c]), c] = False
    M, fl = elib.excess_measures(P, h, side, cols)
    p, ntr, X = elib.day_series(s, M[measure], fl)
    out = {}
    for lab, a, b in [('y1', None, H1_END), ('y2', H2_START, elib.IS_END)]:
        st = elib.stats_block(p, ntr, X, h, a, b)
        out[f'{lab}_bps'] = st['ort_gun_bps']; out[f'{lab}_t'] = st['t']; out[f'{lab}_n_bagimsiz'] = st['n_bagimsiz']
    # f_1 gün içi payı (bilgi): r_oc(t+1) − kendi 250 günlük ortalaması
    g = P['ret_oc'][cols].shift(-1)
    gex = (g - g.shift(1).rolling(250, min_periods=120).mean()) * (1.0 if side == 'long' else -1.0)
    pg, _, _ = elib.day_series(s, gex, fl)
    out['f1_gunici_bps'] = 1e4 * pg[pg.index <= elib.IS_END].mean()
    return out


def run(panel_dir):
    P = elib.load(panel_dir)
    G, B = rules.grid(P)
    rows = []
    GX = rules.grid_extra(P, B)
    for ad, olay, sig, yon, arac in G + GX:
        for h in (1, 2, 3):
            ex = halves(sig, P, h, yon, 'own', arac)
            ex['olay'] = olay
            ex['izgara'] = 'komsu_kesif' if ad[2] == 'x' else 'on_yazili'
            rows.append(elib.evaluate(sig, P, h=h, side=yon, name=ad, family='A4', measure='own', instrument=arac, extra=ex))
    return P, G, B, rows


if __name__ == '__main__':
    panel, out = sys.argv[1], sys.argv[2]
    P, G, B, rows = run(panel)
    df = pd.DataFrame(rows)
    df['bh_gecti'] = elib.bh_fdr(df['p_tek_IS'].values, 0.10)      # tek yönlü (pozisyon yönü), bütün satırlar birlikte
    elib.to_csv(df.to_dict('records'), out)
    pd.set_option('display.width', 250); pd.set_option('display.max_rows', 500)
    show = df[['sinyal_tanimi', 'yon', 'h', 'n_bagimsiz_IS', 'n_islem_IS', 'ort_fazla_IS_bps', 't_IS', 'net_temel_bps_IS',
               'dol_sec_IS_bps', 'y1_bps', 'y1_n_bagimsiz', 'y2_bps', 'top10_haric_bps', 'giris_kapanis1_bps',
               'f1_gece_bps', 'f1_gunici_bps', 'en_yogun_pay', 'yil_pozitif_orani', 'bh_gecti']].copy()
    show.columns = ['ad', 'yon', 'h', 'nb', 'nis', 'own', 't', 'net', 'sec', 'y1', 'y1n', 'y2', 'top10x', 'k1', 'gece', 'gunici',
                    'yogun', 'yilpoz', 'bh']
    print(show[df['izgara'].eq('komsu_kesif') | (os.environ.get('A4_ALL') == '1')].round(2).to_string())
    print('test sayısı:', len(df))
