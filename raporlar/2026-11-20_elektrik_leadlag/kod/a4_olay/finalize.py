"""A4 son adım: tarama çıktısına 'secim' ve 'not' sütunlarını ekler, öz-denetimi çalıştırır, dondurulmuş kuralları
elib.eval_rule ile yeniden üretir.  Kullanım: python3 -I finalize.py <panel_is> <tarama csv> <çıktı csv>"""
import os
import sys
import time
import numpy as np
import pandas as pd

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(_HERE, '..', 'ortak'))
import elib  # noqa: E402
import rules  # noqa: E402

panel, src, out = sys.argv[1:4]
P = elib.load(panel)
t0 = time.time()
R = rules.build(P)
print(f'build() süresi: {time.time() - t0:.1f} sn; kural sayısı {len(R)}; birincil {sum(r["birincil"] for r in R)}')
chk = elib.self_check_causal(rules.build, P)
print('self_check_causal:', chk)
assert all(v == 0 for v in chk.values()), 'NEDENSELLİK HATASI'
a = {r['ad']: r['sig'] for r in rules.build(P)}
assert all(a[r['ad']].equals(r['sig']) for r in R), 'build() deterministik değil'

df = pd.read_csv(src)
df['k'] = df['sinyal_tanimi'] + '_h' + df['h'].astype(str)
frozen = {f'{ad}_h{h}': ('birincil' if b else 'ikincil') for ad, h, b, _ in rules.FROZEN}
ELLE = {
    'E1_herhangi_h3': 'önceden yazılı hipotez; (vi) zayıf: n>=4 ve pay>=%5 komşularında kayboluyor, sepet getirisi '
                      'kontrol edilince ek etkisi yok (t=0,6); en iyi %5 gün hariç ~0; 2021 negatif',
    'E1x_herhangi_sepet_arti_h2': 'KEŞİF (ızgara dışı, aday olamaz): tavan + sektör sepeti artıda; t=2,6; aslında '
                                  'sektör momentumu',
    'E4_eks_SAT_h2': 'genişlik düşüşü sonrası zayıflığın devamı; işaret komşularda tutarlı ama en iyi günler hariç '
                     'negatif, ENJSA ağırlıklı, 2021 yoğun',
    'E6_degdi_kapanmadi_SAT_h1': 'spotta geri dönüş güçlü (AL satırı -99 bps, t=-2,5) ama satılabilir araçta '
                                 'IS\'te 7 olay; yalnız izleme',
    'E5_akran_AL_h3': 'ızgaradaki en yüksek t (2,5) ama temel maliyetin altında (net < 0); izleme',
}


def neden(r):
    if 'BILGI' in r['sinyal_tanimi']:
        return 'bilgi: tavanda kapanan hisse alınamaz (hepsi_own sütununa bak)'
    x = []
    if not (r['n_bagimsiz_IS'] >= 40):
        x.append('olay < 40')
    if not (r['ort_fazla_IS_bps'] > 0):
        x.append('IS fazla getiri <= 0')
    elif not (r['net_temel_bps_IS'] > 0):
        x.append('(i) maliyet sonrası <= 0')
    if not (np.sign(r['y1_bps']) == np.sign(r['y2_bps'])):
        x.append('(ii) yarılar farklı işaret ya da ilk yarıda olay yok')
    if not (r['top10_haric_bps'] > 0):
        x.append('(iii) en iyi günler hariç <= 0')
    if not (r['giris_kapanis1_bps'] > 0):
        x.append('(iv) t+1 kapanışı girişinde kayboluyor')
    if r['en_yogun_pay'] > 0.5:
        x.append('(v) tek hisse payı > %50')
    if not x:
        x.append('(vi)/(vii): komşularda tutarsız ya da t < 2 ve BH geçmiyor')
    return '; '.join(x)


df['secim'] = df['k'].map(frozen).fillna('elendi')
df['not'] = [ELLE.get(r['k'], '') + (' | ' if r['k'] in ELLE else '') + neden(r) for _, r in df.iterrows()]
df['n_IS'] = df['n_bagimsiz_IS']
df['aday_mi'] = df['secim'].eq('birincil')
df = df.drop(columns=['k'])
elib.to_csv(df.to_dict('records'), out)
print('yazıldı:', out, len(df), 'satır;', df['secim'].value_counts().to_dict(), '; BH geçen:', int(df['bh_gecti'].sum()))

# dondurulmuş kuralların eval_rule ile yeniden üretimi (tarama satırıyla aynı olmalı)
pd.set_option('display.width', 250)
rows = [x for r in R for x in elib.eval_rule(r, P, 'A4')]
fr = pd.DataFrame(rows)
c = ['sinyal_tanimi', 'arac', 'h', 'n_bagimsiz_IS', 'n_islem_IS', 'ort_fazla_IS_bps', 't_IS', 'basabas_IS_bps', 'net_temel_bps_IS',
     'top10_haric_bps', 'giris_kapanis1_bps', 'gece_payi', 'en_yogun_pay', 'yillar_bps']
print(fr[[x for x in c if x in fr.columns]].round(2).to_string())
vc = [x for x in fr.columns if x.startswith(('settle_', 'last_')) and ('fazla_IS' in x or 'n_bagimsiz_IS' in x or 't_IS' in x or 'net_temel_IS' in x)]
print(fr[fr['arac'] == 'viop_vadeli'][['sinyal_tanimi'] + vc].round(2).T.to_string())
