#!/usr/bin/env python3
"""V6 iş 1–2 — S1 / S2 / S3 sinyallerinin "kapanıştan önce bilinen" sürümleri (2017-01 → 2026-11).
Her (kural, saat, tampon) için: kapanış sinyaline göre yakalama / kesinlik, kaçan ve yanlış sinyallerin 3 günlük 'per'
fazla getirisi, kapanış sinyalinin ve "saatinde karar verenin" getirisi (giriş her iki durumda da t KAPANIŞ fiyatı;
dolum gerçek kapanış kilidine göre). Dönemler: IS17 (2017–2022), OOS1, KASA, H2023 (2023+; 'per' havuz kıyası).
Kullanım: python3 -I t1_endeks.py <panel_full> <cikti.csv> [raw_m5_xu030.parquet]"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # -I ile betik klasörü yola eklenmez
import v6lib as V  # noqa: E402
from v6lib import elib, vekil  # noqa: E402

TAMPON = {'S1': [-0.003, -0.0015, 0.0, 0.0015, 0.003, 0.005],
          'S2': [0.8, 0.9, 1.0, 1.1, 1.2, 1.3],
          'S3': [(0.8, 0.5), (0.9, 0.5), (1.0, 0.5), (1.1, 0.5), (1.2, 0.5), (1.0, 0.3), (1.0, 0.7), (0.9, 0.7)]}
TEMEL = {'S1': 0.0, 'S2': 1.0, 'S3': (1.0, 0.5)}
AD = {'S1': 'A5_zirve20_sepet_h3', 'S2': 'A2_xelkt_z1_tum_h3', 'S3': 'A5_gecikme1_viop3_h3'}


def main():
    panel, cikti = sys.argv[1], sys.argv[2]
    raw = sys.argv[3] if len(sys.argv) > 3 else None
    P = elib.load(panel)
    G = V.gunluk(P)
    I = V.endeks_gunici(P, raw)
    E5, X5, XS = I['E5'], I['X'], I['XS']
    kapE, kapX = G['L']['XELKT'], G['L']['XU030']
    print('XU100-oranı vekilinin hatası (n, medyan |bps|, %95):', {k: tuple(round(x, 1) for x in v) for k, v in I['vekil_hata'].items()})
    for T in ['1700'] + V.SAAT5:
        e = ((kapE.reindex(E5.index) / E5[T] - 1) * 1e4).dropna()
        x = ((kapX.reindex(X5[T].index) / X5[T] - 1) * 1e4).dropna()
        print(f'{T}: XELKT gün {len(e)}, kapanışa medyan |fark| {e.abs().median():.0f} bps; XU030 gün {len(x)}, '
              f'{x.abs().median():.0f} bps; kaynak {XS[T][X5[T].notna()].value_counts().to_dict()}')

    # --- dondurulmuş kurallarla eşleşme denetimi ve bilinen sonuçların yeniden üretimi
    gercek_kural = {}
    for aile in ('a5_rotasyon', 'a2_endeks'):
        for r in vekil.kural_yukle(f'{V.KOD}/{aile}/rules.py')(P):
            gercek_kural[r['ad']] = r
    hed, Xp, Fp, Xh, Fh, kap_sig = {}, {}, {}, {}, {}, {}
    for k in ('S1', 'S2', 'S3'):
        mask, mn = V.hedef(P, k)
        hed[k] = (mask, mn)
        cols = list(mask.columns)
        Xp[k], Fp[k] = V.olcu(P, 3, cols, 'uc_parca')
        Xh[k], Fh[k] = V.olcu(P, 3, cols, 'havuz')
        tb = TEMEL[k]
        s = V.sinyal(G, kapE, kapX, k, tb[0], tb[1]) if k == 'S3' else V.sinyal(G, kapE, kapX, k, tb)
        kap_sig[k] = s
        rs = gercek_kural[AD[k]]['sig']
        fark = int(((mask & s.reindex(mask.index).values[:, None]) != rs.reindex_like(mask).fillna(False)).values.sum())
        tum = [V.ozet(s, mask, Xp[k], Fp[k], mn, a, b) for a, b in
               ((pd.Timestamp('2000-01-01'), elib.IS_END), V.DONEM['OOS1'], V.DONEM['KASA'])]
        hv = V.ozet(s, mask, Xh[k], Fh[k], mn, *V.DONEM['H2023'])
        print(f'{k} {AD[k]}: dondurulmuş kuralla farklı hücre {fark}; IS/OOS1/KASA = ' +
              ' / '.join(f'{m:+.0f} (t {t:.1f}, {n} gün)' for m, t, n in tum) + f'; havuz 2023+ {hv[0]:+.0f} (t {hv[1]:.1f}, {hv[2]} gün)')

    rows = []

    def karsilastir(k, T, kaynak, vE, vX, tb, gunler):
        mask, mn = hed[k]
        A = kap_sig[k].reindex(gunler).fillna(False)
        B = (V.sinyal(G, vE, vX, k, tb[0], tb[1]) if k == 'S3' else V.sinyal(G, vE, vX, k, tb)).reindex(gunler).fillna(False)
        for dn, (a, b) in list(V.DONEM.items()) + [('TUM17', (V.BAS, pd.Timestamp('2100-01-01')))]:
            g = gunler[(gunler >= a) & (gunler <= b)]
            if len(g) == 0:
                continue
            Ag, Bg = A.reindex(g), B.reindex(g)
            X, F = (Xh[k], Fh[k]) if dn == 'H2023' else (Xp[k], Fp[k])
            st = {ad: V.ozet(s, mask, X, F, mn, a, b) for ad, s in
                  (('gercek', Ag), ('vekil', Bg), ('kacan', Ag & ~Bg), ('yanlis', Bg & ~Ag), ('ortak', Ag & Bg))}
            nA, nB, nT = int(Ag.sum()), int(Bg.sum()), int((Ag & Bg).sum())
            rows.append({'is': 'endeks_sinyali', 'kural': k, 'ad': AD[k], 'saat': T, 'kaynak': kaynak,
                         'tampon': (f'zX>={tb[0]:g};zE<{tb[1]:g}' if k == 'S3' else (f'{tb * 100:+.2f}%' if k == 'S1' else f'z>={tb:g}')),
                         'temel_esik': tb == TEMEL[k], 'donem': dn, 'n_gun_veri': len(g), 'n_gercek': nA, 'n_vekil': nB, 'n_ortak': nT,
                         'yakalama': nT / nA if nA else np.nan, 'kesinlik': nT / nB if nB else np.nan,
                         'gercek_bps': st['gercek'][0], 'gercek_t': st['gercek'][1], 'gercek_ngun': st['gercek'][2],
                         'vekil_bps': st['vekil'][0], 'vekil_t': st['vekil'][1], 'vekil_ngun': st['vekil'][2],
                         'fark_bps': st['vekil'][0] - st['gercek'][0],
                         'kacan_bps': st['kacan'][0], 'kacan_t': st['kacan'][1], 'kacan_ngun': st['kacan'][2],
                         'yanlis_bps': st['yanlis'][0], 'yanlis_t': st['yanlis'][1], 'yanlis_ngun': st['yanlis'][2]})

    # --- S1, S2: XELKT 5 dk (2017'den tam)
    for k in ('S1', 'S2'):
        for T in V.SAAT5:
            vE = E5[T].dropna()
            for tb in TAMPON[k]:
                karsilastir(k, T, 'isy_m5', vE, None, tb, vE.index)
    # --- S3: XU030 için bulunabilen en iyi kaynak; XELKT aynı saatin 5 dk değeri
    for T in ['1700'] + V.SAAT5:
        vX = X5[T].dropna()
        vE = E5[T].reindex(vX.index).dropna()
        vX = vX.reindex(vE.index)
        src = XS[T].reindex(vE.index)
        kay = '+'.join(f'{a}:{n}' for a, n in src.value_counts().items())
        for tb in TAMPON['S3']:
            karsilastir('S3', T, kay, vE, vX, tb, vE.index)
        if T not in ('1700', '1800'):       # yalnız gerçek XU030 gün içi verisi (vekilsiz) — duyarlılık
            m = src.isin(['isy_m5', 'yahoo_m5', 'yahoo_h1'])
            if m.sum():
                karsilastir('S3', T + '_vekilsiz', '+'.join(f'{a}:{n}' for a, n in src[m].value_counts().items()),
                            vE[m], vX[m], TEMEL['S3'], vE.index[m])
    R = pd.DataFrame(rows)
    R.to_csv(cikti, index=False)
    pd.set_option('display.width', 280, 'display.max_columns', 40, 'display.max_rows', 500)
    g = ['kural', 'saat', 'tampon', 'donem', 'n_gun_veri', 'n_gercek', 'n_vekil', 'yakalama', 'kesinlik', 'gercek_bps', 'gercek_t',
         'vekil_bps', 'vekil_t', 'fark_bps', 'kacan_bps', 'kacan_ngun', 'yanlis_bps', 'yanlis_ngun']
    print('\n== temel eşik, bütün saatler ve dönemler')
    print(R[R.temel_esik][g].round(2).to_string(index=False))
    print('\n== tampon ızgarası (TUM17 ve H2023)')
    print(R[R.donem.isin(['TUM17', 'H2023']) & ~R.saat.str.contains('vekilsiz')][g].round(2).to_string(index=False))


if __name__ == '__main__':
    main()
