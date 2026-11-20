"""Aşama 4 — dondurulmuş kuralların değerlendirmesi, sağlamlık, öz-denetim ve sonuç CSV'si."""
import os, sys, pickle, time, importlib.util
import numpy as np
import pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import elib, load_a8, feat_frames, bucket, Ev, fmt, per_stats, KEEP

PANEL, CSV = sys.argv[1], sys.argv[2]
P = elib.load(PANEL)
assert P['ret_cc'].index.max() <= elib.OOS1_END
spec = importlib.util.spec_from_file_location('w3b_rules', os.path.join(HERE, 'rules.py'))
rules = importlib.util.module_from_spec(spec); spec.loader.exec_module(rules)
t0 = time.time(); RL = rules.build(P); t_build = time.time() - t0
RL2 = rules.build(P)
print(f'build süresi {t_build:.1f} s; deterministik:', all((a['sig'].values == b['sig'].values).all() for a, b in zip(RL, RL2)))
for cut in ('2021-06-30', '2018-09-14', '2024-06-28'):
    print('self_check_causal kesim', cut, elib.self_check_causal(rules.build, P, cut))

a8 = load_a8(); fe = a8.features(P); F = feat_frames(fe)
pred = pd.read_pickle(os.path.join(HERE, 'out', 'pred_lgbm_h1.pkl'))
sc, fill = fe['sc'], fe['fill']
ev = Ev(P)
M1, fl1 = elib.excess_measures(P, 1, 'long', sc)
Mo, _ = elib.excess_measures(P, 1, 'long', sc, entry='open1')
raw = M1['raw'].where(fl1); med = raw.median(axis=1)
first = P['ret_cc'][sc].apply(lambda s: s.first_valid_index())
mo = pd.DataFrame(np.isin(sc, [c for c in sc if first[c] < pd.Timestamp('2021-01-01')])[None, :].repeat(len(fill), 0), index=fill.index, columns=sc)
lb = bucket(fe['adv'], fill, 3, 6)
vault_days = 4238 - len(fill)
print('kasa işlem günü (VERI_NOTU_D1: 4.238 − panel_dev gün sayısı):', vault_days)
full_rows = []
for r in RL:
    S = r['sig']; nm = r['ad']
    print('\n=====', nm)
    fr = elib.eval_rule(r, P, family='W3B')[0]; full_rows.append(fr)
    row = ev(S, nm, soru='DONDUR')
    row['secim'] = 'DONDURULDU'; row['not'] = r['aciklama']
    print('yıllar:', row['yillar_bps'], '| yıl + oranı', round(row['yil_pozitif_orani'], 2), '| top10 gün hariç', round(row['top10_haric_bps'], 1),
          '| kırpılmış', round(row['kirpilmis_ort_bps'], 1), '| en yoğun', row['en_yogun_hisse'], round(row['en_yogun_pay'], 3))
    print('giriş (IS+OOS1 birlikte): t kapanış', round(row['giris_kapanis0_bps'], 1), 't+1 açılış', round(row['giris_acilis1_bps'], 1),
          't+1 kapanış', round(row['giris_kapanis1_bps'], 1), '| net düşük/temel/muhafazakâr IS',
          [round(row[f'net_{s}_bps_IS'], 1) for s in ('dusuk', 'temel', 'muhafazakar')], 'OOS1', [round(row[f'net_{s}_bps_OOS1'], 1) for s in ('dusuk', 'temel', 'muhafazakar')])
    for lab, Fm in [('açılış(t+1) girişi', Mo['sec'])]:
        p, n, X = elib.day_series(S, Fm, fl1); st = per_stats(P, p, n, X)
        print(f'  ek {lab}: ' + '; '.join(f"{k} {v['ort_gun_bps']:.1f} (t {v['t']:.2f})" for k, v in st.items()))
    X = raw.where(S & fl1).sub(med, axis=0); st = per_stats(P, X.mean(axis=1), X.notna().sum(axis=1), X)
    print('  ek medyana karşı isabet: ' + '; '.join(f"{k} {v['isabet']:.3f}" for k, v in st.items()))
    for per, (a, b) in elib.periods_of(P).items():
        real, pv, null = elib.shift_null(S, P, 1, 'long', 'sec', n=300, seed=1, end=b, start=a)
        m = pd.Series(True, index=S.index)
        if a is not None: m &= S.index >= a
        if b is not None: m &= S.index <= b
        Sf = (S & fill)[m]; nday = (Sf.sum(axis=1) > 0)
        stay = ((Sf & Sf.shift(1, fill_value=False)).sum(axis=1) / Sf.sum(axis=1).where(Sf.sum(axis=1) > 0))[nday]
        print(f'  {per}: kaydırma sıfırı gerçek {real:.1f} bps, p = {pv:.3f} (sıfır ort {np.nanmean(null):.1f}); sinyalli gün payı {nday.mean():.2f}; '
              f'günde ort hisse {Sf.sum(axis=1)[nday].mean():.1f}; dünden kalan pay {stay.mean():.2f}; evren (dolabilir) {fill[m].sum(axis=1).mean():.1f}')
    ev(S & (fe['price'] >= 5), nm + '|fiyat>=5', soru='SAGLAMLIK')
    ev(S & mo, nm + '|eski_hisseler', soru='SAGLAMLIK'); ev(S & ~mo, nm + '|yeni_hisseler', soru='SAGLAMLIK')
    for k, lab in enumerate(['dusuk', 'orta', 'yuksek']):
        ev(S & (lb == k), nm + f'|lik_{lab}', soru='SAGLAMLIK')
    for h in (2, 3):
        ev(S, nm + f'|tut{h}', h=h, soru='SAGLAMLIK')
    ev(S, nm + '|own', measure='own', soru='SAGLAMLIK')
    ev(S, nm + '|gunde>=2hisse', min_n=2, soru='SAGLAMLIK')
# sinyalin tarama sürümüyle aynılığı
lu, ld = P['lim_up'][sc], P['lim_dn'][sc]
bayrak = (P['lim_up_touch'][sc] & ~lu) | (P['lim_dn_touch'][sc] & ~ld) | ld
nf = fill & ~bayrak
s1 = nf & (bucket(F['vol20'], fill, 2, 6) == 0) & (bucket(F['rel1'], fill, 3, 6) == 2)
q5 = {k: bucket(F[k], fill, 5, 5) for k in ['rel1', 'volshock', 'vol20']}
s2 = nf & ~(q5['rel1'] == 0) & ~(q5['volshock'] == 4) & ~(q5['vol20'] == 4) & (pred > 0.002)
print('\ntarama sürümüyle fark (hücre):', int((s1 != RL[0]['sig']).values.sum()), int((s2 != RL[1]['sig']).values.sum()), '; sinyal sayısı', int(RL[0]['sig'].values.sum()), int(RL[1]['sig'].values.sum()))
ev(RL[0]['sig'] & RL[1]['sig'], 'iki_kural_birlikte', soru='SAGLAMLIK'); ev(RL[0]['sig'] & ~RL[1]['sig'], 'sade_var_model_yok', soru='SAGLAMLIK'); ev(RL[1]['sig'] & ~RL[0]['sig'], 'model_var_sade_yok', soru='SAGLAMLIK')
pickle.dump(ev.rows, open(os.path.join(HERE, 'out', 's4_rows.pkl'), 'wb'))
pd.DataFrame(full_rows).to_csv(os.path.join(HERE, 'out', 'dondurulan_tam_satir.csv'), index=False)

# ---- sonuç CSV'si: bütün aşamaların satırları
allr = []
for k in ('s1', 's2', 's3', 's4'):
    allr += pickle.load(open(os.path.join(HERE, 'out', f'{k}_rows.pkl'), 'rb'))
df = pd.DataFrame(allr)
def tag(r):
    n = r['sinyal_tanimi']
    if r['secim']:
        return r['secim']
    if n.startswith('W3B_') or n.startswith('iki_kural') or n.endswith('_yok'):
        return 'sağlamlık (dondurulan kuralın kırılımı)'
    if n in ('sade_V50_R33',):
        return 'seçildi → W3B_sade_sakin_guclu_h1'
    if n == 'lgbm_tahmin>20bps_ve_TEMIZ4':
        return 'seçildi → W3B_lgbm_tahmin20_temiz_h1'
    if n.startswith('sade_') or n.startswith('3x3_') or n.startswith('lgbm_tahmin') or 'TEMIZ' in n:
        return 'komşu / aday (dondurulmadı)'
    if n.startswith('KACIN') or n.startswith('bayrak') or n.endswith('alt20') or 'alt20' in n or 'dilim1' in n or 'ondalik1/' in n:
        return 'kaçınma tanısı (AL kuralı değil)'
    if n.startswith('TABAN'):
        return 'taban (modelsiz kıyas)'
    return 'tanı'
df['secim'] = df.apply(tag, axis=1)
same = (np.sign(df['ort_fazla_IS_bps']) == np.sign(df['ort_fazla_OOS1_bps']))
df['iki_donem_ayni_yon'] = same
df['not'] = df['not'].where(df['not'] != '', '')
cols = ['soru', 'sinyal_tanimi', 'secim'] + [c for c in KEEP if c != 'sinyal_tanimi'] + ['iki_donem_ayni_yon', 'not']
os.makedirs(os.path.dirname(CSV), exist_ok=True)
df[cols].to_csv(CSV, index=False)
print('CSV satır', len(df), '→', CSV)
