#!/usr/bin/env python3
"""dogrula.py — sinyal.py'nin sinyal günlerini araştırmanın kural kodlarıyla (rules.py + panel) karşılaştırır.

Kullanım:
  python3 -I dogrula.py --panel <.../panel_full> --kod <.../kod> [--ham <ham klasörü>] [--canli] [--n 400]
    --ham    : sinyal.py'yi saklanmış ham İş Yatırım dosyalarıyla çalıştırır (isy_endeks/, isy_hisse/)
    --canli  : sinyal.py'yi şimdi İş Yatırım'dan indirdiği veriyle çalıştırır (panelin son gününe kadar)
    --kaydet : canlı indirmenin ham yanıtlarını bu klasöre yazar
Karşılaştırma: panelin son n işlem günü. Tarih düzeyi: S1, S2, S3. Hisse düzeyi: sepet (dolabilir), kaçınma
(5 puan geride; en kötü beşte birlik; tabana değen), T2. Ayrıca varsayılan kısa pencerenin (450 takvim günü)
uzun pencereyle aynı sonucu verdiği sınanır.
"""
import argparse
import importlib.util
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sinyal  # noqa: E402


def modul(yol, ad):
    spec = importlib.util.spec_from_file_location(ad, yol)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def referans(panel, kod):
    sys.path.insert(0, os.path.join(kod, 'ortak'))
    import elib
    P = elib.load(panel)
    a5 = {r['ad']: r for r in modul(os.path.join(kod, 'a5_rotasyon', 'rules.py'), 'a5rules').build(P)}
    a2 = {r['ad']: r for r in modul(os.path.join(kod, 'a2_endeks', 'rules.py'), 'a2rules').build(P)}
    a3 = {r['ad']: r for r in modul(os.path.join(kod, 'a3_kesit', 'rules.py'), 'a3rules').build(P)}
    w3a = {r['ad']: r for r in modul(os.path.join(kod, 'w3a_kacinma', 'rules.py'), 'w3arules').build(P)}
    w3b = modul(os.path.join(kod, 'w3b_damitma', 'rules.py'), 'w3brules')
    sc = elib.sector_cols(P)
    gun = {'S1': a5['A5_zirve20_sepet_h3']['sig'].any(axis=1),
           'S2': a2['A2_xelkt_z1_tum_h3']['sig'].any(axis=1),
           'S3': a5['A5_gecikme1_viop3_h3']['sig'].any(axis=1)}
    his = {'sepet': P['fill_long'][sc],
           'k5': w3a['W3A_sektorden_5puan_geride_KACIN_h1']['sig'],
           'kq': a3['A3_rel1_alt5_h1_RED']['sig'],
           'taban': P['lim_dn_touch'][sc] & P['tradable'][sc],
           't2': w3b.sade_sig(P)}
    return P, gun, his


def benim(endeks, hisse, son):
    Pm = sinyal.panel_kur(endeks, hisse, son)
    H = sinyal.hisse_sinyal(Pm)
    E = sinyal.endeks_sinyal(Pm['idx'], H['sepet_n'])
    return Pm, E, H


def karsilastir(etiket, P, gun, his, Pm, E, H, n, cikti):
    gunler = P['ret_cc'].index[-n:]
    cikti(f'--- {etiket}: son {n} işlem günü ({gunler[0].date()} → {gunler[-1].date()})')
    ortak = Pm['cal'][Pm['cal'].isin(gunler)]
    cikti(f'takvim: panel {len(gunler)} gün, sinyal.py {len(ortak)} gün, fark {len(gunler) - len(ortak)}')
    tamam = len(ortak) == len(gunler)
    for k in ['XELKT', 'XU030']:
        d = (Pm['idx'][k].reindex(gunler) / P['idx'][k].reindex(gunler) - 1).abs()
        kotu = d[d > 1e-9]
        cikti(f'endeks {k}: en büyük göreli fark {d.max():.2e}; farklı gün {len(kotu)}'
              + (': ' + ', '.join(f'{t.date()} ({Pm["idx"][k][t]:.2f} / {P["idx"][k][t]:.2f})' for t in kotu.index[:5]) if len(kotu) else ''))
    for k in ['S1', 'S2', 'S3']:
        a = gun[k].reindex(gunler).fillna(False).astype(bool)
        b = E[k].reindex(gunler).fillna(False).astype(bool)
        fark = gunler[(a != b).values]
        tamam &= len(fark) == 0
        cikti(f'{k}: kural kodu {int(a.sum())} gün, sinyal.py {int(b.sum())} gün, FARK {len(fark)}'
              + (': ' + ', '.join(str(t.date()) for t in fark[:8]) if len(fark) else ''))
    for k in ['sepet', 'k5', 'kq', 'taban', 't2']:
        a = his[k].reindex(index=gunler).fillna(False).astype(bool)
        b = H[k].reindex(index=gunler, columns=a.columns).fillna(False).astype(bool)
        f = (a != b)
        nf = int(f.values.sum())
        ornek = [f'{t.date()} {c}' for t, c in zip(*[x[:4] for x in (f.index[np.where(f.values)[0]], f.columns[np.where(f.values)[1]])])]
        cikti(f'{k}: kural kodu {int(a.values.sum())} hücre, sinyal.py {int(b.values.sum())} hücre, FARK {nf}'
              + (': ' + ', '.join(ornek) if nf else ''))
    return tamam


def kisa_pencere(etiket, endeks, hisse, son, E, H, cikti, gun=450, m=150):
    bas = son - pd.Timedelta(days=gun)
    e2 = {k: v.loc[bas:] for k, v in endeks.items()}
    h2 = {k: v.loc[bas:] for k, v in hisse.items()}
    _, Ek, Hk = benim(e2, h2, son)
    gunler = Ek.index[-m:]
    out = []
    for k in ['S1', 'S2', 'S3']:
        out.append(f'{k} {int((Ek[k].reindex(gunler) != E[k].reindex(gunler)).sum())}')
    for k in ['sepet', 'k5', 'kq', 'taban', 't2']:
        out.append(f'{k} {int((Hk[k].reindex(gunler) != H[k].reindex(index=gunler, columns=Hk[k].columns)).values.sum())}')
    for k in ['yS1', 'ysdE', 'ysdX', 'zE', 'zX']:
        d = (Ek[k].reindex(gunler) - E[k].reindex(gunler)).abs().max()
        out.append(f'{k} {d:.1e}')
    cikti(f'--- {etiket}: kısa pencere ({gun} takvim günü) ile uzun pencere, son {m} gün; fark sayıları / en büyük fark: '
          + '; '.join(out))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--panel', required=True)
    ap.add_argument('--kod', required=True)
    ap.add_argument('--ham')
    ap.add_argument('--canli', action='store_true')
    ap.add_argument('--kaydet')
    ap.add_argument('--n', type=int, default=400)
    ap.add_argument('--yaz', help='sonuç metnini bu dosyaya da yazar')
    a = ap.parse_args()
    satirlar = []

    def cikti(s):
        print(s, flush=True)
        satirlar.append(s)

    P, gun, his = referans(a.panel, a.kod)
    son = P['ret_cc'].index[-1]
    cikti(f'DOĞRULAMA | panel son günü {son.date()} | kural kodları: a5_rotasyon, a2_endeks, a3_kesit, w3a_kacinma, w3b_damitma')
    sonuc = {}
    if a.ham:
        endeks, hisse, _ = sinyal.veri_yukle(None, None, ham=a.ham, sessiz=True)
        Pm, E, H = benim(endeks, hisse, son)
        sonuc['ham'] = karsilastir('HAM DOSYALAR (panelle aynı indirme)', P, gun, his, Pm, E, H, a.n, cikti)
        kisa_pencere('HAM DOSYALAR', endeks, hisse, son, E, H, cikti)
    if a.canli:
        bas = son - pd.Timedelta(days=int(a.n * 1.47) + 260)
        endeks, hisse, eksik = sinyal.veri_yukle(bas, son, kaydet=a.kaydet, sessiz=True)
        if eksik:
            cikti('canlı indirmede eksik: ' + ', '.join(eksik))
        Pm, E, H = benim(endeks, hisse, son)
        sonuc['canli'] = karsilastir(f'CANLI İNDİRME ({bas.date()} → {son.date()})', P, gun, his, Pm, E, H, a.n, cikti)
        kisa_pencere('CANLI İNDİRME', endeks, hisse, son, E, H, cikti)
    for k, v in sonuc.items():
        cikti(f'SONUÇ {k}: S1/S2/S3 sinyal günleri ' + ('BİREBİR AYNI' if v else 'FARKLI'))
    if a.yaz:
        with open(a.yaz, 'w', encoding='utf-8') as f:
            f.write('\n'.join(satirlar) + '\n')


if __name__ == '__main__':
    main()
