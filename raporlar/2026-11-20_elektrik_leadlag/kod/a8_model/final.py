"""A8 son adım: rules.build() öz-denetimi, dondurulmuş kuralların elib ile değerlendirilmesi, sonuç CSV'si.
Kullanım: python3 -I final.py <panel_is> <çıktı_csv>"""
import os
import sys
import time
import pickle
import warnings
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'ortak'))
import elib  # noqa: E402
import rules as RU  # noqa: E402

warnings.filterwarnings('ignore')
P = elib.load(sys.argv[1])
assert P['ret_cc'].index.max() <= elib.IS_END
CSV = sys.argv[2]
OUT = os.path.join(HERE, 'out')
LOG = []


def say(*a):
    s = ' '.join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


t0 = time.time()
R1 = RU.build(P)
say(f'build(P) süresi: {time.time() - t0:.0f} sn; kural sayısı {len(R1)}; birincil {sum(r["birincil"] for r in R1)}')
R2 = RU.build(P)
det = all((a['sig'].values == b['sig'].values).all() for a, b in zip(R1, R2))
say('deterministik (iki build aynı):', det)
for cut in ('2021-06-30', '2018-09-14'):
    chk = elib.self_check_causal(RU.build, P, cut=cut)
    say(f'self_check_causal(cut={cut}):', {k: v for k, v in chk.items()})
    assert all(v == 0 for v in chk.values()), 'nedensellik öz-denetimi başarısız'
assert det

S = pickle.load(open(os.path.join(OUT, 'scan_rows.pkl'), 'rb'))
rows = S['rows'] + pickle.load(open(os.path.join(OUT, 'diag_rows.pkl'), 'rb'))
df = pd.DataFrame(rows)
df.loc[df.arac == 'viop', ['yari1_bps', 'yari2_bps']] = np.nan      # yarılar spot örneklemiyle hesaplanmıştı; viop'ta geçersiz
df['kaydirma_p'] = df.sinyal_tanimi.map(S['nulls'])
df['n_IS'] = df['n_gun_IS']
for c in ('n_OOS1', 'ort_fazla_OOS1_bps', 't_OOS1', 'net_temel_bps_OOS1'):
    df[c] = np.nan                                                  # kör protokol: OOS-1'i ana ajan hesaplar
aday = df.grup.isin(['izgara', 'zamanlama', 'tek_hisse']) & (df.get('dilim', '').fillna('') != 'alt')
df['bh_gecti'] = False
df.loc[aday, 'bh_gecti'] = elib.bh_fdr(df.loc[aday, 'p_tek_IS'].values, 0.10)
df['aday_mi'] = False
say(f'toplam değerlendirilen satır: {len(df)}; aday türü satır (ızgara üst dilim + zamanlama + tek hisse): {int(aday.sum())}; '
    f'BH(q=0,10) geçen: {int(df.bh_gecti.sum())} → {list(df[df.bh_gecti].sinyal_tanimi)}')
say('aday türü satırlarda net_temel_bps_IS > 0 olan:', list(df[aday & (df.net_temel_bps_IS > 0)].sinyal_tanimi))


def reason(r):
    out = []
    g = r['grup']
    if g in ('kiyas', 'zamanlama_kiyas'):
        out.append('kıyas modeli (aday değil)')
    if g == 'sahte_etki':
        out.append('sağlamlık sınaması')
    if g == 'kesif':
        out.append('keşif: ızgara dışı, aday olamaz')
    if r.get('dilim') == 'alt':
        out.append('bilgi: en alt beşte birlik uzun tarafta ölçüldü (negatif = kaçınma; spotta açığa satış yok)')
        return '; '.join(out)
    if not r['net_temel_bps_IS'] > 0:
        out.append(f"(i) temel maliyet sonrası ≤ 0 ({r['net_temel_bps_IS']:.0f} bps)")
    if r['yari1_bps'] == r['yari1_bps'] and r['yari2_bps'] == r['yari2_bps'] and r['yari1_bps'] * r['yari2_bps'] <= 0:
        out.append('(ii) iki yarıda işaret farklı')
    if not r['top10_haric_bps'] > 0:
        out.append('(iii) en iyi günler çıkınca ≤ 0')
    if not r['giris_kapanis1_bps'] > 0:
        out.append('(iv) t+1 kapanışı girişinde kayboluyor')
    if r['en_yogun_pay'] > 0.5:
        out.append(f"(v) tek hisse payı {r['en_yogun_pay']:.2f}")
    if r['n_gun_IS'] < 100:
        out.append('olay sayısı < 100')
    return '; '.join(out)


df['secim'] = 'elendi'
df['not'] = df.apply(reason, axis=1)
extra_rows = []
for r in R1:
    ev = elib.eval_rule(r, P, 'A8')
    m = df.sinyal_tanimi == r['ad']
    assert m.sum() == 1, r['ad']
    i = df.index[m][0]
    assert abs(df.at[i, 'ort_fazla_IS_bps'] - ev[0]['ort_fazla_IS_bps']) < 1e-9, (r['ad'], df.at[i, 'ort_fazla_IS_bps'], ev[0]['ort_fazla_IS_bps'])
    df.at[i, 'secim'] = 'birincil' if r['birincil'] else 'ikincil'
    df.at[i, 'not'] = 'DONDURULMUŞ (rules.py); ' + df.at[i, 'not']
    e0 = ev[0]
    say(f"{r['ad']}: h={r['h']} olcu={r['olcu']} arac={r['arac']} n_gun={e0['n_gun_IS']} n_bagimsiz={e0['n_bagimsiz_IS']} fazla={e0['ort_fazla_IS_bps']:.1f} "
        f"t={e0['t_IS']:.2f} basabas={e0['basabas_IS_bps']:.1f} maliyet={e0['maliyet_temel_bps']:.1f} net={e0['net_temel_bps_IS']:.1f} "
        f"yil+={e0['yil_pozitif_orani']:.2f} top10={e0['top10_haric_bps']:.1f} kap1={e0['giris_kapanis1_bps']:.1f} acilis1={e0['giris_acilis1_bps']:.1f} "
        f"gece_payi={e0['gece_payi']:.2f} pay={e0['en_yogun_pay']:.2f}({e0['en_yogun_hisse']}) eski={e0['eski_islem_bps']:.1f} yeni={e0['yeni_islem_bps']:.1f} "
        f"yari=[{df.at[i, 'yari1_bps']:.1f},{df.at[i, 'yari2_bps']:.1f}] ic={df.at[i, 'ic_ort']:.4f}/{df.at[i, 'ic_t']:.2f} yıllar={e0['yillar_bps']}")
    for x in ev[1:]:
        x.update({'secim': 'ikincil', 'grup': 'kesif', 'not': 'DONDURULMUŞ kuralın vadeli fiyatlarıyla (uzlaşma/son fiyat kötüsü) değerlendirmesi', 'aday_mi': False})
        extra_rows.append(x)
        say(f"   vadeli fiyatlarıyla: n={x['n_gun_IS']} fazla={x['ort_fazla_IS_bps']:.1f} t={x['t_IS']:.2f} "
            f"uzlaşma net={x['settle_net_temel_IS_bps']:.1f} son fiyat net={x['last_net_temel_IS_bps']:.1f} yıllar(uzlaşma)={x['settle_yillar_bps']}")
df = pd.concat([df, pd.DataFrame(extra_rows)], ignore_index=True)
front = ['aile', 'sinyal_tanimi', 'secim', 'grup', 'hedef', 'yon', 'h', 'arac', 'karar_olcusu', 'n_IS', 'ort_fazla_IS_bps', 't_IS',
         'n_OOS1', 'ort_fazla_OOS1_bps', 't_OOS1', 'dolabilir_oran', 'net_temel_bps_IS', 'net_temel_bps_OOS1', 'bh_gecti',
         'yil_pozitif_orani', 'top10_haric_bps', 'aday_mi', 'not']
df = df[front + [c for c in df.columns if c not in front]]
elib.to_csv(df.to_dict('records'), CSV)
say('yazıldı:', CSV, df.shape, dict(df.secim.value_counts()))
open(os.path.join(OUT, 'final_ozet.txt'), 'w').write('\n'.join(LOG) + '\n')
