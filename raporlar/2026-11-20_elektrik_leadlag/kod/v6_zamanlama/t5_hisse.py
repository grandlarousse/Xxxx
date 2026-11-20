#!/usr/bin/env python3
"""V6 iş 5 — T2 / K1 / K2 (hisse düzeyi kesit kuralları): 17:30 fiyatıyla (ve üst sınır olarak 18:00 son sürekli işlem
fiyatıyla) kurulan sürümün kapanış sürümüyle örtüşmesi. Araç: kod/a7_gunici/vekil.py (mod='tam').
Kullanım: python3 -I t5_hisse.py <panel_full> <cikti.csv> [bas=2023-12-21]"""
import importlib.util
import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
KOD = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(KOD, 'ortak'))
sys.path.insert(0, os.path.join(KOD, 'a7_gunici'))
import elib  # noqa: E402
import vekil  # noqa: E402

SEC = {'W3B_sade_sakin_guclu_h1': 'T2', 'A3_rel1_alt5_h1_RED': 'K1', 'W3A_sektorden_5puan_geride_KACIN_h1': 'K2'}


def _mod(yol, ad):
    spec = importlib.util.spec_from_file_location(ad, yol)
    m = importlib.util.module_from_spec(spec)
    sys.path.insert(0, os.path.dirname(yol))
    try:
        spec.loader.exec_module(m)
    finally:
        sys.path.pop(0)
    return m


def builds():
    w3b = _mod(os.path.join(KOD, 'w3b_damitma', 'rules.py'), 'w3b_v6')

    def b_w3b(P):   # yalnız sade kural (model kuralı 11 sn/kurulum; burada gerekmez)
        return [{'ad': 'W3B_sade_sakin_guclu_h1', 'sig': w3b.sade_sig(P), 'h': 1, 'yon': 'long', 'olcu': 'sec', 'arac': 'spot'}]

    def only(build):
        return lambda P: [r for r in build(P) if r['ad'] in SEC]
    return [b_w3b, only(vekil.kural_yukle(os.path.join(KOD, 'a3_kesit', 'rules.py'))),
            only(vekil.kural_yukle(os.path.join(KOD, 'w3a_kacinma', 'rules.py')))]


def main():
    panel, cikti = sys.argv[1], sys.argv[2]
    kw = dict(a.split('=') for a in sys.argv[3:] if '=' in a)
    bas = kw.get('bas', '2023-12-21')
    P = elib.load(panel)
    out = []
    # p_1730: 17:30 fiyatı (saatlik 16:30 barının kapanışı; 2023-12-21'den beri)
    # p_son : 18:00 son sürekli işlem fiyatı (yalnız 17:30 barının olduğu günler)
    # p_1750 (bas=2026-08-28): gerçek 17:50 (5 dk verisi, son ~60 gün)
    for nokta, b in (('p_1730', bas), ('p_son', bas), ('p_1750', '2026-08-28')):
        for build in builds():
            t, _ = vekil.karsilastir(build, P, nokta=nokta, bas=b, mod='tam')
            t['kural'] = t['ad'].map(SEC)
            out.append(t)
            print(t[['kural', 'ad', 'nokta', 'n_gun', 'n_gercek', 'n_vekil', 'kesinlik', 'yakalama', 'ort_gercek_bps', 't_gercek',
                     'ort_vekil_bps', 't_vekil', 'ort_kacan_bps', 'ort_yanlis_bps', 'n_vekil_dolmaz']].round(3).to_string(index=False),
                  flush=True)
            pd.concat(out).to_csv(cikti, index=False)


if __name__ == '__main__':
    main()
