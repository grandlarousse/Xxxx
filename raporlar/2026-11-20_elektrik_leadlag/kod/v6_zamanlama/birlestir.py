#!/usr/bin/env python3
"""V6 — ara tabloları tek dosyada birleştirir: <ara_klasor>/{t1_endeks,t3_dolum,t5_hisse}.csv → ek/v6_zamanlama.csv
Sütun 'is': endeks_sinyali (iş 1–2) | dolum (iş 3) | hisse_kurali (iş 5). Kullanım: python3 -I birlestir.py <ara_klasor> <cikti.csv>"""
import os
import sys

import pandas as pd

ara, cikti = sys.argv[1], sys.argv[2]
fr = []
for f in ('t1_endeks.csv', 't3_dolum.csv'):
    p = os.path.join(ara, f)
    if os.path.exists(p):
        fr.append(pd.read_csv(p))
p = os.path.join(ara, 't5_hisse.csv')
if os.path.exists(p):
    t = pd.read_csv(p)
    saat = {'p_1730': '1730', 'p_son': '1800', 'p_1750': '1750'}
    kay = {'p_1730': 'yahoo_h1 (16:30 barı kapanışı)', 'p_son': 'yahoo_h1/m5 (18:00 son sürekli işlem; 17:30 barı olan günler)',
           'p_1750': 'yahoo_m5 (17:45 barı kapanışı; son ~60 gün)'}
    fr.append(pd.DataFrame({
        'is': 'hisse_kurali', 'kural': t['kural'], 'ad': t['ad'], 'saat': t['nokta'].map(saat), 'kaynak': t['nokta'].map(kay),
        'tampon': 'yok', 'temel_esik': True, 'donem': t['bas'] + '→' + t['son'], 'n_gun_veri': t['n_gun'],
        'n_gercek': t['n_gercek'], 'n_vekil': t['n_vekil'], 'n_ortak': t['n_ortak'], 'yakalama': t['yakalama'], 'kesinlik': t['kesinlik'],
        'gercek_bps': t['ort_gercek_bps'], 'gercek_t': t['t_gercek'], 'vekil_bps': t['ort_vekil_bps'], 'vekil_t': t['t_vekil'],
        'fark_bps': t['fark_bps'], 'kacan_bps': t['ort_kacan_bps'], 'yanlis_bps': t['ort_yanlis_bps'],
        'not': 'ölçü sec, h=1, hisse-gün sayıları; vekil sinyali kapanışta kilitli (dolmaz): ' + t['n_vekil_dolmaz'].astype(str)}))
R = pd.concat(fr, ignore_index=True)
for c in R.columns:
    if R[c].dtype == float:
        R[c] = R[c].round(4)
R.to_csv(cikti, index=False)
print(cikti, len(R), 'satır;', R['is'].value_counts().to_dict())
