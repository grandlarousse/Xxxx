"""secim.py — tarama sonuçlarına seçim etiketlerini yazar, dondurulmuş kuralları elib ile yeniden değerlendirir,
nedensellik öz-denetimini çalıştırır. Kullanım: python3 -I secim.py <panel_is> <out klasörü> <ek klasörü>"""
import os, sys, time, warnings
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rules, a2lib
from a2lib import elib
warnings.filterwarnings('ignore')
PANEL, OUT, EK = sys.argv[1], sys.argv[2], sys.argv[3]
P = elib.load(PANEL)
assert P['ret_cc'].index.max() <= elib.IS_END
d = pd.concat([pd.read_csv(os.path.join(OUT, 'scan_raw.csv')), pd.read_csv(os.path.join(OUT, 'kesif_raw.csv'))], ignore_index=True)

# --- BH-FDR (q=0,10; iki yönlü; ızgara satırları, olay günü >= 30)
grid = (d.blok != 'KESIF') & (d.n_gun_IS >= 30)
d['bh_gecti'] = False
d.loc[grid, 'bh_gecti'] = elib.bh_fdr(elib.t_to_p(d.loc[grid, 't_IS'].values), 0.10)
d['n_IS'] = d['n_gun_IS']

SEC = {
    'T2a|XELKT|z>=1|all|-|h3|long|spot': ('birincil', 'A2_xelkt_z1_tum_h3: (i)-(vii) hepsi; aile içi BH geçen tek AL satırı; aile düzeltmeli yer değiştirme p=0,01. Zayıflık: 2020 ve 2021 negatif'),
    'T2b|XELKT|z>=1|lag|-|h3|long|spot': ('ikincil', 'A2_xelkt_z1_geciken_h3: birincil kuralın alt kümesi; gecikenler akranlarını geçmiyor (sec ~0), bağımsız kanıt değil'),
    'T2a|SPEC|z>=2|all|-|h3|long|spot': ('ikincil', 'A2_spec_z2_tum_h3: net en yüksek; en iyi 10 gün çıkınca +5 bps, z>=1,5 komşusu zayıf (sivri)'),
    'KESIF|XELKT z>=1 & XU100 z<1|all|h3': ('ikincil', 'A2_xelkt_z1_xu100alt_tum_h3: KEŞİF (ızgara dışı); iki yarıda da güçlü; aday olamaz, yalnız izleme'),
    'T2a|KOMSU|z>=1.5|all|-|h2|long|spot': ('ikincil', 'A2_komsu_z15_tum_h2: XELKT z<1 günlerinde net negatif (keşif ayrıştırması); bağımsız mekanizma zayıf'),
    'T2c|KOMSU|z>=2|AKSEN|-|h1|long|spot': ('ikincil', 'A2_komsu_z2_aksen_h1: tek hisse; 378 tek-hisse AL testi içinden seçildi, şans payı yüksek'),
    'KESIF|EWx z<=-1.5|lag∩VIOP3|h1|short|viop': ('ikincil', 'A2_ewx_zm15_geciken_viop_sat_h1: KEŞİF (ızgara dışı; T2b∩T2c); IS vadeli döneminde 37 olay günü: güç yetersiz'),
}


def neden(r):
    if r['sinyal_tanimi'] in SEC:
        return SEC[r['sinyal_tanimi']]
    kesif = 'keşif (ızgara dışı): aday olamaz; ' if r['blok'] == 'KESIF' else ''
    if not (r['n_gun_IS'] >= 30):
        return 'elendi', kesif + 'olay günü < 30'
    w = []
    if not (r['net_temel_bps_IS'] > 0): w.append('(i) temel maliyet sonrası <= 0')
    if not (r['y1_bps'] > 0 and r['y2_bps'] > 0): w.append('(ii) iki yarıda aynı pozitif işaret yok')
    if not (r['top10_haric_bps'] > 0): w.append('(iii) en iyi 10 gün çıkınca <= 0')
    if not (r['giris_kapanis1_bps'] > 0): w.append('(iv) t+1 kapanış girişinde kayboluyor')
    if r['hedef_tur'] in ('all', 'lag', 'liq10', 'sig', 'lagliq10', 'all_ex_src') and r['en_yogun_pay'] > 0.35: w.append('(v) tek hisse yoğun')
    if not (r['n_gun_IS'] >= 100): w.append('olay günü < 100')
    if not (r['t_IS'] >= 2): w.append('t < 2')
    pre = ''
    if r['yon'] == 'long' and r['t_IS'] <= -2:
        pre = 'AL yönünde anlamlı negatif (bilgi: bu günlerde alma; spotta açığa satış yok); '
    if not w:
        return 'elendi', kesif + pre + '(i)-(v) geçti, seçilmedi: seçilen kuralın komşusu/alt kümesi ya da aile içi çoklu testten sonra şanstan ayırt edilemiyor'
    return 'elendi', kesif + pre + '; '.join(w)


x = d.apply(neden, axis=1, result_type='expand')
d['secim'], d['not'] = x[0], x[1]
d['aday_mi'] = d['secim'] == 'birincil'

# --- dondurulmuş kuralları elib.eval_rule ile yeniden değerlendir + öz-denetim
t0 = time.time(); R = rules.build(P); tb = time.time() - t0
fr = []
for r in R:
    fr += elib.eval_rule(r, P, family='A2')
F = pd.DataFrame(fr); F['blok'] = 'DONDURULMUS'
F['secim'] = np.where(F['birincil'], 'birincil', 'ikincil'); F['not'] = 'rules.py çıktısı (elib.eval_rule): ' + F['aciklama']
F['n_IS'] = F['n_gun_IS']
F.to_csv(os.path.join(OUT, 'dondurulmus_is.csv'), index=False)
chk = elib.self_check_causal(rules.build, P)
R2 = rules.build(P)
det = all(a['sig'].equals(b['sig']) for a, b in zip(R, R2))
with open(os.path.join(OUT, 'ozdenetim.txt'), 'w') as fh:
    fh.write(f'build süresi: {tb:.2f} s; deterministik: {det}\nself_check_causal (kesim 2021-06-30): {chk}\n')
    for cut in ['2016-12-30', '2019-12-31', '2022-06-30']:
        fh.write(f'self_check_causal (kesim {cut}): {elib.self_check_causal(rules.build, P, cut=cut)}\n')
print(open(os.path.join(OUT, 'ozdenetim.txt')).read())
K = ['sinyal_tanimi', 'arac', 'n_gun_IS', 'n_bagimsiz_IS', 'n_islem_IS', 'ort_fazla_IS_bps', 't_IS', 'basabas_IS_bps', 'net_temel_bps_IS',
     'net_muhafazakar_bps_IS', 'top10_haric_bps', 'giris_kapanis1_bps', 'gece_payi', 'en_yogun_pay', 'yil_pozitif_orani', 'dolabilir_oran', 'maliyet_temel_bps', 'yillar_bps']
pd.set_option('display.width', 330); pd.set_option('display.max_columns', 40); pd.set_option('display.max_colwidth', 130)
print(F[[k for k in K if k in F.columns]].round(2).to_string(index=False))
vv = F[F.arac == 'viop_vadeli']
if len(vv):
    print(vv[[c for c in vv.columns if c.startswith(('settle_', 'last_')) and 'IS' in c]].round(1).T.to_string())
out = pd.concat([d, F], ignore_index=True)
first = ['aile', 'blok', 'sinyal_tanimi', 'girdi', 'esik_z', 'hedef_tur', 'kosul', 'hedef', 'yon', 'h', 'arac', 'karar_olcusu', 'n_IS', 'n_bagimsiz_IS',
         'n_islem_IS', 'ort_fazla_IS_bps', 't_IS', 'p_tek_IS', 'basabas_IS_bps', 'net_temel_bps_IS', 'y1_bps', 'y1_t', 'y1_n', 'y2_bps', 'y2_t', 'y2_n',
         'dolabilir_oran', 'bh_gecti', 'yil_pozitif_orani', 'top10_haric_bps', 'giris_kapanis1_bps', 'gece_payi', 'en_yogun_pay', 'aday_mi', 'secim', 'not']
out = out[first + [c for c in out.columns if c not in first]]
elib.to_csv(out.to_dict('records'), os.path.join(EK, 'a2_endeks_sonuc.csv'))
rg = pd.concat([pd.read_csv(os.path.join(OUT, 'regresyon.csv')), pd.read_csv(os.path.join(OUT, 'regresyon_ek.csv'))], ignore_index=True)
rg.to_csv(os.path.join(EK, 'a2_endeks_regresyon.csv'), index=False)
g = d[d.blok != 'KESIF']
print('ızgara satırı:', len(g), '| olay günü>=30:', int((g.n_gun_IS >= 30).sum()), '| keşif satırı:', int((d.blok == 'KESIF').sum()),
      '| BH geçen:', int(d.bh_gecti.sum()), '(AL yönünde pozitif:', int((d.bh_gecti & (d.t_IS > 0) & (d.yon == 'long')).sum()), ')')
print('secim:', out.secim.value_counts().to_dict(), '| regresyon satırı:', len(rg))
ok = (g.n_gun_IS >= 100) & (g.net_temel_bps_IS > 0) & (g.y1_bps > 0) & (g.y2_bps > 0) & (g.top10_haric_bps > 0) & (g.giris_kapanis1_bps > 0) & (g.yon == 'long')
print('(i)-(v) ve n>=100 geçen AL satırı:', int(ok.sum()), '| bunlardan t>=2:', int((ok & (g.t_IS >= 2)).sum()))
print('IS ham kapanış >= 250 TL olan hisse-gün:', int((P['close_raw'] >= 250).sum().sum()))
