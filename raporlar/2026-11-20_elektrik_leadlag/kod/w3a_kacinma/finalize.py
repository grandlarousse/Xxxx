"""W3-A sonlandırma: öz-denetim, dondurulmuş kuralların değerlendirmesi, kasa beklentisi ve güç, sonuç tablosu.
Kullanım: python3 -I finalize.py <panel_dev> <scan.csv> <çıktı csv>"""
import os
import sys
import time
from math import erf, sqrt

import numpy as np
import pandas as pd

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(os.path.dirname(_HERE), 'ortak'))
import elib  # noqa: E402
import rules  # noqa: E402

KASA_GUN = 350          # kasa dönemi yaklaşık işlem günü (2025-07-01 → 2026-11-20)
Phi = lambda x: 0.5 * (1 + erf(x / sqrt(2)))


def guc(delta, sigma, n, z):
    return float(Phi(delta * sqrt(max(n, 0)) / sigma - z)) if sigma and sigma == sigma and sigma > 0 else np.nan


def etiket(r):
    """Tarama satırı için otomatik 'not': iki dönemde işaret ve |t|."""
    a, b, ta, tb = r.get('ort_fazla_IS_bps'), r.get('ort_fazla_OOS1_bps'), r.get('t_IS'), r.get('t_OOS1')
    if not (a == a and b == b):
        return 'olay yok / yetersiz'
    want = 1 if r['yon'] == 'short' else -1          # spot AL satırlarında beklenen işaret eksi (kaçınma); SAT'ta artı
    if a * want > 0 and b * want > 0:
        if abs(ta) >= 2 and abs(tb) >= 2:
            return 'iki dönemde aynı yön, ikisinde de |t| >= 2'
        return 'iki dönemde aynı yön, en az birinde |t| < 2'
    if a * want <= 0 and b * want <= 0:
        return 'iki dönemde de beklenenin tersi'
    return 'işaret dönemler arasında tutarsız'


def main(panel, scan_csv, out):
    P = elib.load(panel)
    t0 = time.time()
    R = rules.build(P)
    print(f'build: {time.time() - t0:.2f} sn, {len(R)} kural')
    for cut in ('2019-06-28', '2021-06-30', '2022-12-30', '2024-06-28'):
        print('self_check_causal', cut, elib.self_check_causal(rules.build, P, cut=cut))
    a = rules.build(P)
    print('deterministik:', all((x['sig'].values == y['sig'].values).all() for x, y in zip(R, a)))
    n_oos = int(((P['ret_cc'].index >= elib.OOS1_START) & (P['ret_cc'].index <= elib.OOS1_END)).sum())
    oran = KASA_GUN / n_oos
    rows = []
    for r in R:
        for row in elib.eval_rule(r, P, family='W3A'):
            row['grup'] = 'DONDURULMUS'; row['tetik'] = r['ad']; row['beklenen_isaret'] = r['beklenen_isaret']
            vad = row['arac'] == 'viop_vadeli'
            if r['arac'] == 'spot' or vad:          # karar satırı: spot kuralda spot, VİOP kuralında vadeli fiyatlı satır
                n1 = row['n_gun_OOS1']; m1 = abs(row['ort_fazla_OOS1_bps']); t1 = abs(row['t_OOS1'])
                sig = m1 / t1 * sqrt(n1)
                d = min(abs(row['ort_fazla_IS_bps']), m1)
                nk = n1 * oran
                row.update({'kasa_beklenen_olay': round(nk, 1), 'sigma_gun_bps': round(sig, 0), 'etki_varsayim_bps': round(d, 1),
                            'guc_a05': round(guc(d, sig, nk, 1.645), 2), 'guc_holm10': round(guc(d, sig, nk, 2.326), 2),
                            'guc_yarim_etki_a05': round(guc(d / 2, sig, nk, 1.645), 2)})
                # yer değiştirme (dairesel kaydırma) sınaması: geliştirme döneminin tamamı, spot fiyatla
                real, p_hi, null = elib.shift_null(r['sig'], P, h=r['h'], side=r['yon'], measure=r['olcu'], n=300,
                                                   end=elib.OOS1_END)
                p = p_hi if r['beklenen_isaret'] > 0 else float((np.sum(null <= real) + 1) / (np.isfinite(null).sum() + 1))
                row['yer_degistirme_p'] = round(p, 4); row['yer_degistirme_gercek_bps'] = round(real, 1)
                row['secim'] = 'DONDURULDU (karar satırı)'
            else:
                row['secim'] = 'DONDURULDU (bilgi: spot fiyatla, vadeli dönemi)'
            row['not'] = r['aciklama']
            rows.append(row)
    F = pd.DataFrame(rows)
    S = pd.read_csv(scan_csv)
    S['secim'] = 'tarama'
    S['not'] = S.apply(etiket, axis=1)
    dond = {'K1_AL_h1_own': 'W3A_tavana_degdi_kapanmadi_KACIN_h1', 'K4a5_AL_h1_sec': 'W3A_sektorden_5puan_geride_KACIN_h1',
            'K5z10_VIOP_SAT_h1': 'W3A_sektor_dustu_direnen_VIOP_SAT_h1'}
    for k, v in dond.items():
        S.loc[S['sinyal_tanimi'] == k, 'secim'] = 'tarama (dondurulan kuralın kaynağı: ' + v + ')'
    D = pd.concat([F, S], ignore_index=True)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    D.to_csv(out, index=False)
    print(f'{len(S)} tarama satırı + {len(F)} dondurulmuş satır -> {out}')
    print(S['not'].groupby([S['grup'].isin(['viop_sat']), S['not']]).size().to_string())
    pd.set_option('display.width', 250); pd.set_option('display.max_columns', 60)
    c = ['sinyal_tanimi', 'arac', 'karar_olcusu', 'n_bagimsiz_IS', 'ort_fazla_IS_bps', 't_IS', 'n_bagimsiz_OOS1', 'ort_fazla_OOS1_bps',
         't_OOS1', 'net_temel_bps_IS', 'net_temel_bps_OOS1', 'kasa_beklenen_olay', 'sigma_gun_bps', 'etki_varsayim_bps', 'guc_a05',
         'guc_holm10', 'guc_yarim_etki_a05', 'yer_degistirme_p', 'gece_payi', 'giris_acilis1_bps', 'giris_kapanis1_bps',
         'kirpilmis_ort_bps', 'en_yogun_hisse', 'en_yogun_pay', 'yil_pozitif_orani']
    print(F[[k for k in c if k in F.columns]].round(2).T.to_string())
    for _, r in F.iterrows():
        print(r['sinyal_tanimi'], r['arac'], '|', r.get('yillar_bps', ''), '|', r.get('settle_yillar_bps', ''))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
