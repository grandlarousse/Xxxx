"""A1 aday kurallar için ek sağlamlık denetimleri (yalnız IS): kaydırma sıfır dağılımı, tam 10 gün hariç ortalama,
bayat fiyat (hedef adv60 üçte birliği), öz-getiri ayrımı, eski/yeni hisseler. Kullanım: python3 -I check.py <panel_is> <çıktı>"""
import sys, os, json
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'ortak'))
sys.path.insert(0, HERE)
import elib   # noqa: E402
import rules  # noqa: E402

PANEL = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'out')
P = elib.load(PANEL)
assert P['ret_cc'].index.max() <= elib.IS_END
SEC = elib.sector_cols(P)
CAND = [
    ('A1_LN_W250_c2.0_th1.5_h1', rules.ln_signal, dict(W=250, c=2.0, theta=1.5), 1),
    ('A1_LN_W250_c2.0_th1.5_h2', rules.ln_signal, dict(W=250, c=2.0, theta=1.5), 2),
    ('A1_LN_W500_c1.5_th1.5_h2', rules.ln_signal, dict(W=500, c=1.5, theta=1.5), 2),
    ('A1_GP_abs0.03_asagi_h2', rules.gp_signal, dict(kind='abs', thr=0.03, up=False), 2),
    ('A1_GP_abs0.03_asagi_h3', rules.gp_signal, dict(kind='abs', thr=0.03, up=False), 3),
    ('A1_FL_th2.0_h1', rules.fl_signal, dict(theta=2.0), 1),
]
adv = elib.adv60(P)[SEC].where(P['tradable'][SEC])
rk = adv.rank(axis=1, pct=True)                      # t−1'e kadarki hacimle, o günkü kesit sırası (nedensel)
e = rules.sec_excess_today(P)
res = []
for ad, fn, kw, h in CAND:
    sig = fn(P, **kw)
    M, fl = elib.excess_measures(P, h, 'long', list(sig.columns))
    p, ntr, X = elib.day_series(sig, M['sec'], fl)
    d = p.dropna().sort_values()
    real, pv, null = elib.shift_null(sig, P, h=h, measure='sec', n=500, seed=7)
    r = {'ad': ad, 'n_gun': int(len(d)), 'ort_bps': 1e4 * d.mean(), 'en_iyi_10_gun_haric_bps': 1e4 * d.iloc[:-10].mean(),
         'en_iyi_yuzde5_haric_bps': 1e4 * d.iloc[:-max(10, int(np.ceil(0.05 * len(d))))].mean(),
         'en_kotu_ve_en_iyi_10_haric_bps': 1e4 * d.iloc[10:-10].mean(), 'medyan_gun_bps': 1e4 * d.median(),
         'kaydirma_p': pv, 'sifir_ort_bps': float(np.nanmean(null)), 'sifir_p95_bps': float(np.nanquantile(null, 0.95))}
    for lab, m in [('dusuk', rk <= 1 / 3), ('orta', (rk > 1 / 3) & (rk <= 2 / 3)), ('yuksek', rk > 2 / 3)]:
        x = elib.evaluate(sig & m.reindex_like(sig).fillna(False), P, h=h, measure='sec', name=ad + '_likidite_' + lab, family='A1')
        r[f'lik_{lab}_n'] = x['n_islem_IS']; r[f'lik_{lab}_bps'] = x['basabas_IS_bps']; r[f'lik_{lab}_t'] = x['t_IS']
    for lab, m in [('oz_fazla_poz', e > 0), ('oz_fazla_neg', e <= 0)]:
        x = elib.evaluate(sig & m.reindex_like(sig).fillna(False), P, h=h, measure='sec', name=ad + '_' + lab, family='A1')
        r[f'{lab}_n'] = x['n_islem_IS']; r[f'{lab}_bps'] = x['basabas_IS_bps']; r[f'{lab}_t'] = x['t_IS']
    x = elib.evaluate(sig, P, h=h, measure='sec', name=ad, family='A1')
    for k in ['eski_islem_bps', 'eski_n', 'yeni_islem_bps', 'yeni_n', 'yillar_bps', 'gece_payi', 'f1_gece_bps', 'f1_toplam_bps', 'giris_acilis1_bps', 'giris_kapanis1_bps',
              'net_dusuk_bps_IS', 'net_temel_bps_IS', 'net_muhafazakar_bps_IS', 'dol_own_IS_bps', 'dol_own_IS_t', 'dol_mkt_IS_bps', 'dol_raw_IS_bps', 'hepsi_sec_IS_bps']:
        r[k] = x.get(k)
    res.append(r)
# kontrol: aynı gün öz z >= 1,5 (lider bilgisi olmadan) -> sec fazla getirisi (LN'nin öz momentumdan farkı için kıyas)
Z = rules.zscore(P)[SEC]
for h in (1, 2):
    x = elib.evaluate((Z >= 1.5) & P['fill_long'][SEC], P, h=h, measure='sec', name=f'KONTROL_oz_z1.5_h{h}', family='A1')
    res.append({'ad': x['sinyal_tanimi'], 'n_gun': x['n_gun_IS'], 'ort_bps': x['ort_fazla_IS_bps'], 't': x['t_IS'], 'basabas': x['basabas_IS_bps']})
df = pd.DataFrame(res)
df.to_csv(os.path.join(OUT, 'aday_denetim.csv'), index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 60)
print(df.set_index('ad').T.to_string())
t1 = pd.read_csv(os.path.join(OUT, 't1_cift.csv')); t2 = pd.read_csv(os.path.join(OUT, 't2_olay.csv'))
print('\nT1 BH geçenler:'); print(t1[t1['bh']][['kaynak', 'hedef', 'h', 'n', 'b', 't', 't_sektorsuz', 't_yari1', 't_yari2']].round(2).to_string(index=False))
print('\nT2 BH geçenler:'); print(t2[t2['bh']].round(2).to_string(index=False))
print('T2 BH geçenlerde pozitif (AL yönünde) olan:', int((t2[t2['bh']]['t'] > 0).sum()), '/', int(t2['bh'].sum()))
