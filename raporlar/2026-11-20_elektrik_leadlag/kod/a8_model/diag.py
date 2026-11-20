"""A8 tanı (IS): en alt beşte birlik, üst−alt farkı, zamanlama katsayıları ve ızgara dışı KEŞİF satırları (aday olamaz).
Çıktı: out/diag_rows.pkl (keşif satırları) + ekrana özet."""
import os
import sys
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
OUT = os.path.join(HERE, 'out')
S = pickle.load(open(os.path.join(OUT, 'scan_rows.pkl'), 'rb'))
df = pd.DataFrame(S['rows'])
k = df[(df.karar_olcusu == 'sec') & (df.filtre == '') & df.sinyal_tanimi.str.endswith('20')].copy()
k['anahtar'] = k.model + '_h' + k.h.astype(str)
u = k[k.dilim == 'ust'].set_index('anahtar')
a = k[k.dilim == 'alt'].set_index('anahtar')
t = pd.DataFrame({'ust_bps': u.ort_fazla_IS_bps, 'ust_t': u.t_IS, 'alt_bps': a.ort_fazla_IS_bps, 'alt_t': a.t_IS,
                  'alt_y1': a.yari1_bps, 'alt_y2': a.yari2_bps, 'alt_top10': a.top10_haric_bps, 'alt_kap1': a.giris_kapanis1_bps,
                  'alt_own': a.dol_own_IS_bps, 'alt_gece': a.gece_sec_bps, 'ic': u.ic_ort})
t['fark'] = t.ust_bps - t.alt_bps
print(t.round(1).to_string())

fe = RU.features(P)
cache = {}
print('\nzamanlama ridge lam=1 standart katsayılar (bps; parantez: pozitif işaret payı)')
names = RU.DAY_FEATS + RU.DAY_EXTRA
for h in (1, 2, 3):
    col = []
    RU.predict_day(P, fe, h, {'model': 'ridge', 'lam': 1}, {}, col)
    A = np.array(col)
    print(f'h={h}', ' '.join(f"{n}:{1e4 * A[:, j].mean():.1f}({(A[:, j] > 0).mean():.2f})" for j, n in enumerate(names)))

# ---- KEŞİF (ızgara dışı): AKSEN/ENJSA/ODAS kesit tahmininin en alt beşte birliğindeyse SAT, en üstündeyse AL
rows = []
H1, H2 = pd.Timestamp('2019-12-31'), pd.Timestamp('2020-01-01')
cfg = S['lg_best']
for bottom, side in ((True, 'short'), (False, 'long')):
    sp = {'kind': 'sec', 'cfg': cfg, 'h': 1, 'frac': 0.2, 'bottom': bottom}
    sig = RU.rule_sig(P, fe, sp, cache)
    cols = [c for c in elib.VIOP if c in sig.columns]
    s3 = sig[cols]
    if side == 'short':
        s3 = s3 & P['fill_short'][cols]
    for arac, olcu in (('spot', 'sec'), ('spot', 'own'), ('viop', 'own')):
        if arac == 'spot' and side == 'long' and olcu == 'own':
            continue
        Mx, fl = elib.excess_measures(P, 1, side, cols)
        p, _, _ = elib.day_series(s3, Mx[olcu], fl)
        ex = {'grup': 'kesif', 'model': RU.cfg_tag(cfg), 'yari1_bps': 1e4 * p[p.index <= H1].mean(), 'yari2_bps': 1e4 * p[p.index >= H2].mean()}
        nm = f"A8_kesif_3hisse_{RU.cfg_tag(cfg)}_h1_{'alt' if bottom else 'ust'}20_{side}_{arac}_{olcu}"
        r = elib.evaluate(s3, P, h=1, side=side, measure=olcu, instrument=arac, name=nm, family='A8', extra=ex)
        rows.append(r)
        print(f"{nm:62s} n={r['n_gun_IS']:4d} fz={r['ort_fazla_IS_bps']:6.1f} t={r['t_IS']:5.2f} net={r['net_temel_bps_IS']:6.1f} "
              f"y1={r['yari1_bps']:6.1f} y2={r['yari2_bps']:6.1f} top10={r['top10_haric_bps']:6.1f} kap1={r['giris_kapanis1_bps']:6.1f} "
              f"pay={r['en_yogun_pay']:.2f} yıllar={r['yillar_bps']}")
pickle.dump(rows, open(os.path.join(OUT, 'diag_rows.pkl'), 'wb'))
print('keşif satırı:', len(rows))
