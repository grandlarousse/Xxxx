"""Aşama 2 — tek ve iki özellikli sıralamalar, bayraklar, 'temiz hisse' süzgeçleri (Soru 4)."""
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
R = P['ret_cc'][sc]
F['mom250'] = R.rolling(250, min_periods=120).mean()
F['mom60'] = R.rolling(60, min_periods=40).sum()
F['yas'] = P['ipo_n'][sc].astype(float)
ev = Ev(P)
is_m = fill.index <= elib.IS_END

print('== tahmin beşte birliklerinde özelliklerin gün içi yüzdelik sırası ortalaması (1 = en düşük dilim)')
bk = bucket(pred, fill, 5, 5)
rows = []
for nm in ['rel1', 'r0', 'r1', 'rel3', 'rel5', 'r20', 'volshock', 'vol20', 'liqrank', 'mom250', 'yas']:
    rk = F[nm].where(fill).rank(axis=1, pct=True)
    d = {'ozellik': nm}
    for lab, m in [('IS', is_m), ('OOS', ~is_m)]:
        for q in range(5):
            d[f'{lab}{q + 1}'] = float(np.nanmean(rk[m].where(bk[m] == q).values))
    rows.append(d)
print(pd.DataFrame(rows).set_index('ozellik').round(2).to_string())

print('\n== tek özellik: en üst / en alt beşte birlik (sec, h1)')
for nm in ['rel1', 'r0', 'r1', 'rel3', 'rel5', 'r20', 'volshock', 'vol20', 'liqrank', 'mom250', 'mom60', 'yas']:
    ev(a8.top_signal(F[nm], fill, 0.2, 5, False), f'tek_{nm}_ust20', soru='S4')
    ev(a8.top_signal(F[nm], fill, 0.2, 5, True), f'tek_{nm}_alt20', soru='S4')

print('\n== bayraklar')
lu, ld = P['lim_up'][sc], P['lim_dn'][sc]
tu = P['lim_up_touch'][sc] & ~lu
td = P['lim_dn_touch'][sc] & ~ld
ev(tu, 'bayrak_tavana_degdi_kapanmadi', soru='S4')
ev(td, 'bayrak_tabana_degdi_kapanmadi', soru='S4')
ev(ld, 'bayrak_tabanda_kapandi', soru='S4')
ev(lu.shift(1, fill_value=False) & ~lu, 'bayrak_dun_tavan_bugun_degil', soru='S4')
bayrak = tu | td | ld

print('\n== iki özellik (bağımsız üçte birlikler; 0 = düşük, 2 = yüksek)')
T3 = {nm: bucket(F[nm], fill, 3, 6) for nm in ['volshock', 'vol20', 'rel1', 'r20', 'liqrank']}
for a, ka, b, kb in [('volshock', 0, 'vol20', 0), ('volshock', 2, 'vol20', 2), ('volshock', 0, 'vol20', 2), ('volshock', 2, 'vol20', 0),
                     ('volshock', 0, 'rel1', 2), ('volshock', 0, 'rel1', 0), ('volshock', 2, 'rel1', 2), ('volshock', 2, 'rel1', 0),
                     ('vol20', 0, 'rel1', 2), ('vol20', 0, 'rel1', 0), ('vol20', 2, 'rel1', 2), ('vol20', 2, 'rel1', 0),
                     ('vol20', 0, 'r20', 2), ('vol20', 0, 'r20', 0), ('vol20', 2, 'r20', 2), ('vol20', 2, 'r20', 0)]:
    ev((T3[a] == ka) & (T3[b] == kb), f'iki_{a}{ka}_{b}{kb}', soru='S4')

print('\n== kaçınma süzgeçleri (kalan "temiz" hisselerin hepsi AL)')
q5 = {nm: bucket(F[nm], fill, 5, 5) for nm in ['rel1', 'volshock', 'vol20']}
kotu_rel = q5['rel1'] == 0
c1 = fill & ~bayrak
c2 = c1 & ~kotu_rel
c3 = c2 & ~(q5['volshock'] == 4)
c4 = c3 & ~(q5['vol20'] == 4)
ev(fill & bayrak, 'KACIN_bayrakli(tavan/taban temasi)', soru='S4')
ev(fill & (bayrak | kotu_rel), 'KACIN_bayrak_veya_rel1alt20', soru='S4')
ev(fill & (bayrak | kotu_rel | (q5['volshock'] == 4)), 'KACIN_bayrak|rel1alt20|hacimsokuust20', soru='S4')
ev(fill & (bayrak | kotu_rel | (q5['volshock'] == 4) | (q5['vol20'] == 4)), 'KACIN_bayrak|rel1alt20|hacim|oynaklikust20', soru='S4')
ev(c1, 'TEMIZ1_bayraksiz', soru='S4')
ev(c2, 'TEMIZ2_bayraksiz_rel1alt20degil', soru='S4')
ev(c3, 'TEMIZ3_+hacimsoku_ust20degil', soru='S4')
ev(c4, 'TEMIZ4_+oynaklik_ust20degil', soru='S4')
ev(a8.top_signal(pred, c4, 0.2, 5), 'lgbm_ust20_TEMIZ4_icinde_sirali', soru='S4', note='model temiz evrende ek değer katıyor mu')
ev(a8.top_signal(pred, c4, 0.2, 5, True), 'lgbm_alt20_TEMIZ4_icinde_sirali', soru='S4')
ev(a8.top_signal(pred, fill, 0.2, 5) & ~c4, 'lgbm_ust20_TEMIZ4_disi', soru='S4')
ev(a8.top_signal(pred, fill, 0.2, 5) & c4, 'lgbm_ust20_ve_TEMIZ4', soru='S4')
pickle.dump(ev.rows, open(os.path.join(HERE, 'out', 's2_rows.pkl'), 'wb'))
print('süre', round(time.time() - t0, 1))
