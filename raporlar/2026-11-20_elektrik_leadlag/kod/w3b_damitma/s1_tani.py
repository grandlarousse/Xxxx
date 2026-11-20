"""Aşama 1 — A8 LightGBM üst beşte birliğinin çözümlenmesi (Soru 1–3 ve özellik önemi)."""
import os, sys, pickle, time
import numpy as np
import pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import elib, load_a8, feat_frames, bucket, Ev, fmt, per_stats

PANEL = sys.argv[1]
t0 = time.time()
P = elib.load(PANEL)
assert P['ret_cc'].index.max() <= elib.OOS1_END, 'kasa verisi yüklenemez'
a8 = load_a8()
fe = a8.features(P)
cache, imp = {}, []
pred = a8.predict_sec(P, fe, 1, a8._LGB, cache, collect=imp)
pred.to_pickle(os.path.join(HERE, 'out', 'pred_lgbm_h1.pkl'))
print('tahmin süresi', round(time.time() - t0, 1), 's; panel', P['ret_cc'].index.min().date(), P['ret_cc'].index.max().date(), 'hisse', len(fe['sc']))
sc, fill = fe['sc'], fe['fill']
ev = Ev(P)
top = a8.top_signal(pred, fill, 0.2, 5, False)
bot = a8.top_signal(pred, fill, 0.2, 5, True)

print('\n== S1: üst beşte birlik, kırılımlar')
r0 = ev(top, 'lgbm_ust20', soru='S1', note='A8 özgün kuralının yeniden üretimi')
print('yıllar(sec):', r0['yillar_bps'])
r = ev(top, 'lgbm_ust20_own', measure='own', soru='S1'); print('yıllar(own):', r['yillar_bps'])
first = P['ret_cc'][sc].apply(lambda s: s.first_valid_index())
old = [c for c in sc if first[c] < pd.Timestamp('2021-01-01')]
new = [c for c in sc if c not in old]
print('eski', len(old), 'yeni', len(new))
mo = pd.DataFrame(np.isin(sc, old)[None, :].repeat(len(fill), 0), index=fill.index, columns=sc)
ev(top & mo, 'lgbm_ust20_eski_hisseler', soru='S1')
ev(top & ~mo, 'lgbm_ust20_yeni_hisseler', soru='S1')
ev(fill & mo, 'TABAN_tum_eski_hisseler', soru='S1', note='modelsiz taban: 2021 öncesi listelenenlerin hepsi')
ev(fill & ~mo, 'TABAN_tum_yeni_hisseler', soru='S1', note='modelsiz taban: 2021 ve sonrası listelenenlerin hepsi')
# model yalnız eski / yalnız yeni hisseler içinde sıralanırsa
ev(a8.top_signal(pred, fill & mo, 0.2, 5), 'lgbm_ust20_eski_icinde_sirali', soru='S1')
ev(a8.top_signal(pred, fill & ~mo, 0.2, 5), 'lgbm_ust20_yeni_icinde_sirali', soru='S1')
adv = fe['adv']
lb = bucket(adv, fill, 3, 6)
for k, nm in enumerate(['dusuk', 'orta', 'yuksek']):
    ev(top & (lb == k), f'lgbm_ust20_lik_{nm}', soru='S1')
    ev(fill & (lb == k), f'TABAN_lik_{nm}', soru='S1', note='modelsiz taban')
    ev(a8.top_signal(pred, fill & (lb == k), 0.2, 3), f'lgbm_ust20_lik_{nm}_icinde_sirali', soru='S1', note='üçte birlik içinde yeniden sıralı')
p5 = fe['price'] >= 5.0
ev(a8.top_signal(pred, fill & p5, 0.2, 5), 'lgbm_ust20_fiyat5_icinde_sirali', soru='S1')
ev(fill & p5, 'TABAN_fiyat5', soru='S1', note='modelsiz taban')
ev(fill & ~p5, 'TABAN_fiyat_alti5', soru='S1', note='modelsiz taban')
# seçilenlerin olağan kayması (bench_own) evrene göre
M1, fl1 = elib.excess_measures(P, 1, 'long', sc)
B = M1['raw'] - M1['own']                       # hedefin t'den önceki 250 günlük ortalama f1'i
for nm, S in [('ust20', top), ('alt20', bot)]:
    for per, (a, b) in elib.periods_of(P).items():
        m = pd.Series(True, index=fill.index)
        if a is not None: m &= fill.index >= a
        if b is not None: m &= fill.index <= b
        sel = B.where(S & fill)[m]; uni = B.where(fill)[m]
        d = (sel.mean(axis=1) - uni.mean(axis=1)).dropna()
        cov = (B.where(S & fill)[m].notna().sum().sum() / max((S & fill)[m].sum().sum(), 1))
        yeni_pay = (S & fill & ~mo)[m].sum().sum() / max((S & fill)[m].sum().sum(), 1)
        yeni_evren = (fill & ~mo)[m].sum().sum() / max(fill[m].sum().sum(), 1)
        print(f'  kayma farkı {nm} {per}: seçilen − evren = {1e4 * d.mean():6.1f} bps/gün; own kıyası olan pay {cov:.2f}; yeni hisse payı seçilen {yeni_pay:.2f} / evren {yeni_evren:.2f}')

print('\n== S3: beşte birlikler (tahmine göre; 0 = en düşük)')
bk = bucket(pred, fill, 5, 5)
for q in range(5):
    ev(bk == q, f'lgbm_dilim{q + 1}/5', soru='S3')
bk10 = bucket(pred, fill, 10, 10)
for q in [0, 1, 8, 9]:
    ev(bk10 == q, f'lgbm_ondalik{q + 1}/10', soru='S3')
ev(bot, 'lgbm_alt20', soru='S3')
raw = M1['raw'].where(fl1)
med = raw.median(axis=1); mean_all = raw.mean(axis=1)
for nm, S in [('ust20', top), ('alt20', bot)]:
    for lab, ref in [('medyan', med), ('ortalama', mean_all)]:
        X = raw.where(S).sub(ref, axis=0)
        st = per_stats(P, X.mean(axis=1), X.notna().sum(axis=1), X)
        print(f'  ek: {nm} − evren {lab}: ' + '; '.join(f"{k} {v['ort_gun_bps']:.1f} bps (t {v['t']:.2f}), isabet {v['isabet']:.3f}" for k, v in st.items()))

print('\n== S2: gece / gün içi, tutma süresi, devir')
Mo, _ = elib.excess_measures(P, 1, 'long', sc, entry='open1')
g = P['ret_co'][sc].shift(-1)
gf = g.where(fl1)
gs = pd.DataFrame({c: g[c] - (gf.sum(axis=1) - gf[c].fillna(0)) / (gf.notna().sum(axis=1) - gf[c].notna().astype(int)).where(lambda n: n >= 4) for c in sc})
for nm, S in [('ust20', top), ('alt20', bot)]:
    for lab, F in [('kapanış→kapanış(sec)', M1['sec']), ('açılış(t+1)→kapanış(t+1)(sec)', Mo['sec']), ('gece kapanış→açılış(sec)', gs)]:
        p, n, X = elib.day_series(S, F, fl1)
        st = per_stats(P, p, n, X)
        print(f'  ek: {nm} {lab}: ' + '; '.join(f"{k} {v['ort_gun_bps']:.1f} bps (t {v['t']:.2f})" for k, v in st.items()))
for h in (2, 3):
    ev(top, f'lgbm_ust20_tut{h}', h=h, soru='S2', note='h1 tahmini, h gün tutma')
S = (top & fill)
prev = S.shift(1, fill_value=False)
for per, (a, b) in elib.periods_of(P).items():
    m = pd.Series(True, index=S.index)
    if a is not None: m &= S.index >= a
    if b is not None: m &= S.index <= b
    m &= S.sum(axis=1) > 0
    stay = ((S & prev).sum(axis=1) / S.sum(axis=1).where(S.sum(axis=1) > 0))[m]
    print(f'  devir {per}: bugünkü üst dilimin dün de üst dilimde olan payı {stay.mean():.3f} → günlük yeni pozisyon payı {1 - stay.mean():.3f}')

print('\n== S4: özellik önemi (LightGBM kazanç payı; son 30 aylık model = OOS-1)')
I = np.array(imp, dtype=float); I = I / I.sum(axis=1, keepdims=True)
df = pd.DataFrame({'IS': I[:-30].mean(0), 'OOS1': I[-30:].mean(0)}, index=fe['names']).sort_values('OOS1', ascending=False)
print(df.round(3).to_string()); print('model sayısı', len(I))
df.to_csv(os.path.join(HERE, 'out', 'onem.csv'))
pickle.dump(ev.rows, open(os.path.join(HERE, 'out', 's1_rows.pkl'), 'wb'))
print('süre', round(time.time() - t0, 1))
