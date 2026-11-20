"""A3 sonlandırma: dondurulmuş kuralları kur, tarama satırlarıyla eşle, nedensellik öz-denetimi, sonuç CSV'si.
Kullanım: python3 -I finalize.py <panel_is> <ara_cikti_klasoru> <ek_klasoru>"""
import os
import shutil
import sys
import time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'ortak'))
import elib  # noqa: E402
import rules as RL  # noqa: E402

panel, out, ek = sys.argv[1], sys.argv[2], sys.argv[3]
P = elib.load(panel)
assert P['ret_cc'].index.max() <= elib.IS_END
t0 = time.time()
rules = RL.build(P)
t_build = time.time() - t0
a = pd.read_csv(os.path.join(out, 'scan_rows.csv'))
b = pd.read_csv(os.path.join(out, 'scan_rows2.csv'))
b = b[~b['sinyal_tanimi'].str.endswith('_tani')]
df = pd.concat([a, b], ignore_index=True)
log = [f'build() süresi: {t_build:.1f} s; kural sayısı: {len(rules)}; birincil: {sum(r["birincil"] for r in rules)}']

frozen = {}
for r in rules:
    row = elib.eval_rule(r, P, family='A3')[0]
    m = df[(df['sinyal_tanimi'] == r['izgara_adi']) & (df['arac'] == r['arac'])]
    assert len(m) == 1, r['izgara_adi']
    d = abs(row['ort_fazla_IS_bps'] - m['ort_fazla_IS_bps'].iloc[0])
    assert d < 1e-6 and row['n_gun_IS'] == m['n_gun_IS'].iloc[0], (r['ad'], d)
    frozen[m.index[0]] = r
    log.append(f"{r['ad']}: h={r['h']} {r['yon']} {r['olcu']} {r['arac']} | n_gun {row['n_gun_IS']} bağımsız {row['n_bagimsiz_IS']} | "
               f"fazla {row['ort_fazla_IS_bps']:.1f} bps t {row['t_IS']:.2f} | net temel {row['net_temel_bps_IS']:.1f} | tarama satırıyla fark {d:.1e}")


def note(r):
    f = []
    g = lambda k: r[k] if k in r and r[k] == r[k] else np.nan
    tar = str(r.get('tarama', ''))
    if 'vadeli' in tar:
        return 'vadeli fiyatıyla tekrar (bilgi)'
    if g('net_temel_bps_IS') <= 0:
        f.append('i: temel maliyet sonrası ≤ 0')
    if g('yari1_bps') * g('yari2_bps') <= 0:
        f.append('ii: iki yarıda işaret farklı')
    if g('top10gun_haric_bps') <= 0:
        f.append('iii: en iyi 10 gün çıkınca ≤ 0')
    if g('giris_kapanis1_bps') <= 0:
        f.append('iv: t+1 kapanışı girişinde ≤ 0')
    if g('en_yogun_pay') > 0.5:
        f.append('v: tek hisse payı > %50')
    if abs(g('t_IS')) < 2:
        f.append('|t| < 2')
    pre = {'kontrol_c_px5': 'kontrol (c): ham fiyat ≥ 5 TL', 'kontrol_d_lik15': 'kontrol (d): en likit 15', 'tani': 'tanılama',
           'kesif': 'KEŞİF (ızgara dışı)', 'kesif_viop': 'KEŞİF (ızgara dışı)', 'T2_viop_kisa': 'yön tamamlayıcı (VİOP SAT)',
           'T3_asagi': 'aşağı yön (bilgi)', 'T4_asagi': 'aşağı yön (bilgi)'}.get(tar, '')
    return (pre + ' | ' if pre else '') + ('; '.join(f) if f else 'ölçütleri sayıca karşılıyor')


df['secim'] = 'elendi'
df['kural_adi'] = ''
df['not'] = [note(r) for _, r in df.iterrows()]
for i, r in frozen.items():
    df.loc[i, 'secim'] = 'birincil' if r['birincil'] else 'ikincil'
    df.loc[i, 'kural_adi'] = r['ad']
    df.loc[i, 'not'] = 'DONDURULDU (ikincil, bilgi amaçlı) | ' + df.loc[i, 'not']
elib.to_csv(df.to_dict('records'), os.path.join(ek, 'a3_kesit_sonuc.csv'))

chk = elib.self_check_causal(RL.build, P)
log.append('self_check_causal (kesim 2021-06-30): ' + str(chk))
assert all(v == 0 for v in chk.values()), chk
r2 = RL.build(P)
same = all(x['sig'].equals(y['sig']) for x, y in zip(rules, r2))
log.append(f'deterministik (iki build aynı): {same}')
# BH (q=0,10) — ana ızgara satırları, tek yönlü (pozitif)
g = df[df['tarama'].isin(['T2', 'T2_kosullu', 'T3', 'T4', 'T3_asagi', 'T4_asagi'])]
log.append(f'ana ızgara satırı: {len(g)}; BH(q=0,10) geçen (pozitif yön): {int(elib.bh_fdr(g["p_tek_IS"].values).sum())}; '
           f'en büyük t: {g["t_IS"].max():.2f}; en küçük t: {g["t_IS"].min():.2f}')
log.append(f'toplam satır: {len(df)}; tarama dağılımı: {df["tarama"].value_counts().to_dict()}')
log.append(f'secim dağılımı: {df["secim"].value_counts().to_dict()}')
shutil.copy(os.path.join(out, 'regresyon.csv'), os.path.join(ek, 'a3_kesit_regresyon.csv'))
txt = open(os.path.join(out, 'tanilama.txt')).read() + '\n--- sonlandırma ---\n' + '\n'.join(log) + '\n'
open(os.path.join(ek, 'a3_kesit_tanilama.txt'), 'w').write(txt)
print('\n'.join(log))
