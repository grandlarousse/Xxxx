"""Aşama 3 — sade kural adayları (oynaklık × günlük göreli güç) ve model dilimleri; komşu parametreler."""
import os, sys, pickle, time
import numpy as np
import pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import elib, load_a8, feat_frames, bucket, Ev, fmt, per_stats

PANEL = sys.argv[1]
t0 = time.time()
P = elib.load(PANEL)
assert P['ret_cc'].index.max() <= elib.OOS1_END
a8 = load_a8()
fe = a8.features(P)
pred = pd.read_pickle(os.path.join(HERE, 'out', 'pred_lgbm_h1.pkl'))
sc, fill = fe['sc'], fe['fill']
F = feat_frames(fe)
ev = Ev(P)
lu, ld = P['lim_up'][sc], P['lim_dn'][sc]
bayrak = (P['lim_up_touch'][sc] & ~lu) | (P['lim_dn_touch'][sc] & ~ld) | ld
nf = fill & ~bayrak
xe = P['idx_ret']['XELKT'].reindex(fill.index)
relx = P['ret_cc'][sc].sub(xe, axis=0)                       # XELKT endeksine göre günlük fark (TradingView'de doğrudan görülür)
print('işlem günü (panel_dev):', len(fill), '; OOS-1 günü:', int((fill.index > elib.IS_END).sum()))

print('== 3×3: vol20 üçte birliği × rel1 üçte birliği (bayraksız evren)')
v3 = bucket(F['vol20'], fill, 3, 6); r3 = bucket(F['rel1'], fill, 3, 6)
for a in range(3):
    for b in range(3):
        ev(nf & (v3 == a) & (r3 == b), f'3x3_vol{a}_rel{b}_bayraksiz', soru='S4')

print('\n== sade kural ızgarası: düşük oynaklık × bugünkü göreli güç (bayraksız)')
vol = {'V25': bucket(F['vol20'], fill, 4, 6) == 0, 'V33': v3 == 0, 'V50': bucket(F['vol20'], fill, 2, 6) == 0}
guc = {'R33': r3 == 2, 'R50': bucket(F['rel1'], fill, 2, 6) == 1, 'Rpoz': F['rel1'] > 0, 'Rpoz1': F['rel1'] > 0.01, 'RXpoz': relx > 0, 'RXpoz1': relx > 0.01}
for vk, vm in vol.items():
    for gk, gm in guc.items():
        ev(nf & vm & gm, f'sade_{vk}_{gk}', soru='S4')
print('\n== ek koşullar / gevşetmeler')
base = vol['V33'] & guc['Rpoz']
ev(fill & base, 'sade_V33_Rpoz_bayrakDAHIL', soru='S4')
ev(nf & base & (F['volshock'] < np.log(2.0)), 'sade_V33_Rpoz_hacim<2x', soru='S4')
ev(nf & base & (F['volshock'] < 0), 'sade_V33_Rpoz_hacim<1x', soru='S4')
ev(nf & base & (F['volshock'] >= 0), 'sade_V33_Rpoz_hacim>=1x', soru='S4')
ev(nf & base & (F['rel1'] < 0.03), 'sade_V33_Rpoz_rel<3%', soru='S4')
ev(nf & vol['V33'] & (F['rel1'] > 0) & (F['r0'] > 0), 'sade_V33_Rpoz_ve_gun_arti', soru='S4')
ev(nf & vol['V33'] & (F['rel1'] <= 0), 'sade_V33_Rneg (karşıt)', soru='S4')
ev(nf & ~vol['V50'] & (F['rel1'] > 0), 'sade_Vust50_Rpoz (karşıt)', soru='S4')
ev(nf & (F['rel1'] > 0), 'sade_yalniz_Rpoz', soru='S4')
ev(nf & vol['V33'], 'sade_yalniz_V33', soru='S4')
for h in (2, 3):
    ev(nf & base, f'sade_V33_Rpoz_tut{h}', h=h, soru='S2')

print('\n== model dilimleri')
q = pred[fill.index <= elib.IS_END].where(fill).stack().quantile([.5, .8, .9, .95]).round(5).to_dict(); print('IS tahmin yüzdelikleri:', q)
q5 = {nm: bucket(F[nm], fill, 5, 5) for nm in ['rel1', 'volshock', 'vol20']}
c2 = nf & ~(q5['rel1'] == 0)
c4 = c2 & ~(q5['volshock'] == 4) & ~(q5['vol20'] == 4)
top20 = a8.top_signal(pred, fill, 0.2, 5); top10 = a8.top_signal(pred, fill, 0.1, 5)
ev(top10, 'lgbm_ust10', soru='DONDUR')
ev(top10 & c4, 'lgbm_ust10_ve_TEMIZ4', soru='DONDUR')
ev(a8.top_signal(pred, c4, 0.1, 5), 'lgbm_ust10_TEMIZ4_icinde_sirali', soru='DONDUR')
ev(top20 & nf, 'lgbm_ust20_ve_bayraksiz', soru='DONDUR')
ev(top20 & c2, 'lgbm_ust20_ve_TEMIZ2', soru='DONDUR')
ev(top20 & c4, 'lgbm_ust20_ve_TEMIZ4', soru='DONDUR')
for thr in (0.001, 0.002, 0.003):
    ev(fill & (pred > thr), f'lgbm_tahmin>{int(thr * 1e4)}bps', soru='DONDUR')
    ev(c4 & (pred > thr), f'lgbm_tahmin>{int(thr * 1e4)}bps_ve_TEMIZ4', soru='DONDUR')
rk = pred.where(fill).rank(axis=1, ascending=False, method='first')
ok5 = (pred.where(fill).notna().sum(axis=1) >= 5).values[:, None]
ev((rk <= 1) & ok5, 'lgbm_en_ust_1_hisse', soru='S5'); ev((rk <= 3) & ok5, 'lgbm_en_ust_3_hisse', soru='S5')
ev(top20 & nf & base, 'lgbm_ust20_ve_sade_V33_Rpoz', soru='DONDUR')
ev(nf & base & ~top20, 'sade_V33_Rpoz_lgbm_ust20_DISI', soru='DONDUR')
ev(top20 & ~(nf & base), 'lgbm_ust20_sade_DISI', soru='DONDUR')
pickle.dump(ev.rows, open(os.path.join(HERE, 'out', 's3_rows.pkl'), 'wb'))
print('süre', round(time.time() - t0, 1))
