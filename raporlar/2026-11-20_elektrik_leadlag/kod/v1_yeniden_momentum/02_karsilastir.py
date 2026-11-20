"""V1 karşılaştırma (SON ADIM): bağımsız sonuçlar ile ana ajanın tabloları ve ortak kütüphane/panel yan yana.
elib ve panel_full yalnız burada, karşılaştırma için açılır.
Kullanım: python3 -I 02_karsilastir.py <v1_cikti> <panel_full> <rapor_klasoru>"""
import sys, os, importlib.util
import numpy as np
import pandas as pd

out, panel, rapor = sys.argv[1], sys.argv[2], sys.argv[3]
kod = os.path.join(rapor, 'kod')
sys.path.insert(0, os.path.join(kod, 'ortak'))
import elib


def mod(ad, yol):
    sp = importlib.util.spec_from_file_location(ad, yol); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m


ADLAR = {'S1': 'A5_zirve20_sepet_h3', 'S2': 'A2_xelkt_z1_tum_h3', 'S3': 'A5_gecikme1_viop3_h3'}
# ---- ana ajanın tabloları
ks = pd.read_csv(os.path.join(rapor, 'ek', 'kasa_sonuc.csv')).set_index('sinyal_tanimi')
to = pd.read_csv(os.path.join(rapor, 'ek', 'tum_oos_sonuc.csv')).set_index('sinyal_tanimi')
ana = {}
for k, ad in ADLAR.items():
    for dn, (tb, ek_) in {'IS': (ks, 'IS'), 'OOS1': (ks, 'OOS1'), 'KASA': (ks, 'KASA'), 'HAVUZ': (to, 'OOS')}.items():
        r = tb.loc[ad]
        ana[(k, dn)] = {'ana_n_gun': r[f'n_gun_{ek_}'], 'ana_n_bagimsiz': r[f'n_bagimsiz_{ek_}'], 'ana_n_islem': r[f'n_islem_{ek_}'],
                        'ana_fazla_bps': r[f'ort_fazla_{ek_}_bps'], 'ana_t': r[f't_{ek_}'], 'ana_ham_bps': r[f'dol_raw_{ek_}_bps'],
                        'ana_isabet': r[f'isabet_{ek_}']}
# ---- ana ajanın sinyal günleri (kütüphane + rules.py, panel_full)
P = elib.load(panel)
kurallar = {r['ad']: r for r in mod('a5rules', os.path.join(kod, 'a5_rotasyon', 'rules.py')).build(P)}
kurallar.update({r['ad']: r for r in mod('a2rules', os.path.join(kod, 'a2_endeks', 'rules.py')).build(P)})
ana_gun = {}
for k, ad in ADLAR.items():
    ru = kurallar[ad]
    cols = [c for c in ru['sig'].columns if c in P['ret_cc'].columns]
    M, fl = elib.excess_measures(P, 3, 'long', cols)
    p, ntr, X = elib.day_series(ru['sig'][cols], M['per'], fl, ru.get('min_n', 1))
    praw, _, _ = elib.day_series(ru['sig'][cols], M['raw'].where(M['per'].notna()), fl, ru.get('min_n', 1))
    ana_gun[k] = pd.DataFrame({'per': p, 'ham': praw}).dropna(subset=['per'])
# ---- benim günlerim
G = pd.read_csv(os.path.join(out, 'v1_gunluk.csv'), parse_dates=['date'])
R = pd.read_csv(os.path.join(out, 'v1_sonuc.csv'))
DON = {'IS': ('2010-01-04', '2022-12-30'), 'OOS1': ('2023-01-02', '2025-06-30'), 'KASA': ('2025-07-01', '2026-11-20'),
       'HAVUZ': ('2023-01-02', '2026-11-20')}
rows = []
print('--- sinyal tarihleri örtüşmesi ve gün düzeyi fark (bps) ---')
for k in ADLAR:
    for dn, (a, b) in DON.items():
        ag = ana_gun[k].loc[a:b]
        for su in ['A', 'B']:
            g = G[(G.surum == su) & (G.kural == k) & (G.date >= a) & (G.date <= b)].set_index('date')
            ort = ag.index.intersection(g.index)
            jac = len(ort) / max(len(ag.index.union(g.index)), 1)
            dper = (g.per.reindex(ort) - ag.per.reindex(ort)) * 1e4
            dham = (g.ham.reindex(ort) - ag.ham.reindex(ort)) * 1e4
            if su == 'A':
                A = R[(R.surum == 'A') & (R.kural == k) & (R.donem == dn)].iloc[0]
                B = R[(R.surum == 'B') & (R.kural == k) & (R.donem == dn)].iloc[0]
                C = R[(R.surum == 'C') & (R.kural == k) & (R.donem == dn)].iloc[0]
                m = ana[(k, dn)]
                rows.append({'kural': k, 'kural_adi': ADLAR[k], 'donem': dn,
                             'ana_n_gun': int(m['ana_n_gun']), 'v1_n_gun': int(A.n_gun),
                             'ana_n_bagimsiz': int(m['ana_n_bagimsiz']), 'v1_n_bagimsiz': int(A.n_bagimsiz),
                             'ana_n_islem': int(m['ana_n_islem']), 'v1_n_islem': int(A.n_islem),
                             'ana_fazla_bps': m['ana_fazla_bps'], 'v1_fazla_bps': A.fazla_bps, 'fark_bps': A.fazla_bps - m['ana_fazla_bps'],
                             'v1B_kutuphane_taklidi_bps': B.fazla_bps, 'farkB_bps': B.fazla_bps - m['ana_fazla_bps'],
                             'ana_t': m['ana_t'], 'v1_t_nw2': A.t_nw2, 'v1_t_blok': A.t_blok,
                             'ana_ham_bps': m['ana_ham_bps'], 'v1_ham_bps': A.ham_bps,
                             'ana_isabet': m['ana_isabet'], 'v1_isabet_islem': A.isabet_islem_per, 'v1_isabet_gun': A.isabet_gun_per,
                             'tarih_ortusme_jaccard': jac, 'yalniz_ana_gun': len(ag.index.difference(g.index)),
                             'yalniz_v1_gun': len(g.index.difference(ag.index)),
                             'gun_fark_per_ort_mutlak_bps': dper.abs().mean(), 'gun_fark_ham_ort_mutlak_bps': dham.abs().mean(),
                             'bs_ga90_alt_bps': A.bs_ga90_alt, 'bs_ga90_ust_bps': A.bs_ga90_ust, 'bs_pay_negatif': A.bs_pay_negatif,
                             'kaydirma_p': A.kaydirma_p, 'kaydirma_p_tum': A.kaydirma_p_tum, 'sifir_ort_bps': A.sifir_ort_bps,
                             'sifir_q95_bps': A.sifir_q95_bps,
                             'v1C_cokus3_haric_bps': C.fazla_bps, 'v1C_t_nw2': C.t_nw2, 'v1C_ham_bps': C.ham_bps,
                             'v1_sinyal_disi_gun_ham_bps': A.sinyal_disi_gun_ham_bps})
            print(k, dn, su, 'ana', len(ag), 'v1', len(g), 'ortak', len(ort), 'jaccard %.4f' % jac,
                  '| per fark ort|.| %.2f maks %.1f | ham fark ort|.| %.2f maks %.1f' % (dper.abs().mean(), dper.abs().max(), dham.abs().mean(), dham.abs().max()),
                  '| yalnız ana:', [str(d.date()) for d in ag.index.difference(g.index)][:6],
                  '| yalnız v1:', [str(d.date()) for d in g.index.difference(ag.index)][:6])
T = pd.DataFrame(rows)


def neden(r):
    if abs(r.fark_bps) < 5:
        return 'fark < 5 bps'
    if abs(r.farkB_bps) < 1:
        return ('kıyas farkı: ortak kütüphane çıkış kaymasını 5 günle sınırlıyor (uzun taban serileri: BIGEN, LYDYE, MAGEN, ESEN); '
                'V1 ilk kilitsiz kapanışı kullanıyor; kütüphane taklidi (B) farkı kapatıyor; sinyal günleri aynı')
    return 'açıklanamadı'


T['fark_nedeni'] = T.apply(neden, axis=1)
T.to_csv(os.path.join(rapor, 'ek', 'v1_yeniden_momentum.csv'), index=False, float_format='%.4f')
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 50)
print(T[['kural', 'donem', 'ana_n_gun', 'v1_n_gun', 'ana_n_islem', 'v1_n_islem', 'ana_fazla_bps', 'v1_fazla_bps', 'fark_bps',
         'v1B_kutuphane_taklidi_bps', 'farkB_bps', 'ana_t', 'v1_t_nw2', 'v1_t_blok', 'ana_ham_bps', 'v1_ham_bps', 'ana_isabet',
         'v1_isabet_islem']].round(2).to_string())
print(T[['kural', 'donem', 'bs_ga90_alt_bps', 'bs_ga90_ust_bps', 'bs_pay_negatif', 'kaydirma_p', 'kaydirma_p_tum', 'sifir_ort_bps',
         'sifir_q95_bps', 'v1C_cokus3_haric_bps', 'v1C_t_nw2', 'v1C_ham_bps', 'v1_sinyal_disi_gun_ham_bps']].round(3).to_string())

# ---- panel düzeyi karşılaştırma (bayraklar, getiri)
print('--- panel düzeyi ---')
sc = [c for c in pd.read_pickle(os.path.join(out, 'v1_fill.pkl')).columns]
my = {k: pd.read_pickle(os.path.join(out, f'v1_{k}.pkl')) for k in ['fill', 'tavan', 'taban', 'tradable', 'cadj']}
idx = P['ret_cc'].index
print('takvim aynı mı:', idx.equals(my['fill'].index), len(idx), len(my['fill'].index))
for a, b in [('tradable', 'tradable'), ('fill', 'fill_long')]:
    x, y = my[a].reindex(idx)[sc].values, P[b][sc].values
    print(f'{a}: v1 {x.sum()} ana {y.sum()} yalnız v1 {(x & ~y).sum()} yalnız ana {(~x & y).sum()}')
tr = (my['tradable'].reindex(idx)[sc] | P['tradable'][sc]).values
for a, b in [('tavan', 'lim_up'), ('taban', 'lim_dn')]:
    x, y = my[a].reindex(idx)[sc].values & tr, P[b][sc].values & tr
    print(f'{a} (dolabilir evrende): v1 {x.sum()} ana {y.sum()} yalnız v1 {(x & ~y).sum()} yalnız ana {(~x & y).sum()}')
    for lab, mm in [('2020-03-13 sonrası', idx >= pd.Timestamp('2020-03-13')), ('2023+', idx >= pd.Timestamp('2023-01-02'))]:
        print(f'   {lab}: v1 {x[mm].sum()} ana {y[mm].sum()} yalnız v1 {(x & ~y)[mm].sum()} yalnız ana {(~x & y)[mm].sum()}')
r_my = my['cadj'].reindex(idx)[sc].pct_change(fill_method=None)
d = (r_my - P['ret_cc'][sc]).where(P['tradable'][sc] & my['tradable'].reindex(idx)[sc])
dv = d.abs().values
print('günlük getiri farkı (ortak dolabilir hücreler): n', int(np.isfinite(dv).sum()), 'maks %.6f' % np.nanmax(dv),
      '>1e-4:', int((dv > 1e-4).sum()), '>1e-3:', int((dv > 1e-3).sum()), '>1e-2:', int((dv > 1e-2).sum()))
big = d.abs().stack().sort_values(ascending=False).head(8)
print(big.to_string())
