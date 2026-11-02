"""v_YA1_a — zaman-tutarlı VİOP evreni: olay günü hissenin pay vadelisi bültende LİSTELİ mi (ilk SSF tarihi <= olay günü).
Bugünkü 47'lik listeyi 2020'ye geri taşımak (hayatta kalan/ileri bakışlı evren) yerine o gün işlenebilir olanlar.
"""
import numpy as np, pandas as pd, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from v0_panel import SCR
from v2_bt import nw_t
def st(x, dates, cost=0, tik=None):
    x = pd.Series(np.asarray(x, float)); d = pd.Series(np.asarray(dates))
    if tik is not None: x = x - np.asarray(tik, float)
    x = x - cost / 1e4; ok = x.notna().values; x = x[ok]; d = d[ok]
    if len(x) < 8: return f'n={len(x)}'
    gm = x.groupby(d.values).mean()
    return f'n={len(x)} işlem {1e4 * x.mean():.1f} (t_cl {gm.mean() / (gm.std() / np.sqrt(len(gm))):.2f}) gün {1e4 * gm.mean():.1f} (t_nw {nw_t(gm):.2f})'
V = pd.read_parquet(SCR + '/data/viop_panel.parquet', columns=['date', 'root', 'segment']); V = V[V.segment == 'SSF']
first = V.groupby('root').date.min()
E = pd.read_parquet(HERE + '/_ev_viop.parquet'); E['fx'] = E.date >= E.stock.map(first)
H = pd.read_parquet(HERE + '/_ev_h1.parquet')[['stock', 'date', 'p1030', 'open_match', 'f1030']]
E = E.merge(H, on=['stock', 'date'], how='left')
E['tik'] = np.minimum(0.01 / E.c_unadj, 0.02)
PER = [('2020-03..2026-10', '2020-03-13', '2027'), ('IS brif 2020', '2020-03-13', '2021'), ('OOS brif 2021-26', '2021', '2027'), ('IS 2020-22', '2020-03-13', '2023'), ('OOS 2023-26', '2023', '2027')]
for nm, m in [('TC (b)', E.TC), ('TU (c)', E.TU)]:
    s = E[m & E.fx]
    print(f'\n### {nm} — vadeli listeli olaylar n={len(s)}')
    for pn, a, b in PER:
        q = s[(s.date >= a) & (s.date < b)]
        print(f'  {pn:18s} spot açılış @15: {st(-q.intra_1, q.date, 15)} | @15+tik: {st(-q.intra_1, q.date, 15, q.tik)}')
        qf = q[q.f1_qty.fillna(0) > 0]
        print(f'  {"":18s} VADELİ açılış @15+tik: {st(-qf.fint1, qf.date, 15, qf.tikF1)} | @8+tik: {st(-qf.fint1, qf.date, 8, qf.tikF1)}')
    q = s[s.open_match.fillna(False) & s.p1030.notna()]
    print(f'  2023-11+ spot 10:30 giriş @15+tik: {st(-q.f1030, q.date, 15, q.tik)} | @30+tik: {st(-q.f1030, q.date, 30, q.tik)}')
s = E[E.BC & (E.BC_1 == False) & E.fx]
print(f'\n### BC dolum-uygun (d) — vadeli listeli n={len(s)}')
for pn, a, b in PER:
    q = s[(s.date >= a) & (s.date < b)]
    print(f'  {pn:18s} spot @19: {st(-q.dr2_5, q.date, 19)} | @19+tik: {st(-q.dr2_5, q.date, 19, q.tik)}')
D = pd.read_parquet(HERE + '/_div.parquet'); D = D[D.viop & (D.date >= '2017-03-06')]
D['fx'] = D.date >= D.stock.map(first)
print('\n### Temettü ex-gün (VİOP47, 2017-03+): vadeli listeli', D.fx.sum(), '/', len(D))
for pn, a, b in [('2017-03..2026', '2017', '2027'), ('2017-2020', '2017', '2021'), ('2021-2026', '2021', '2027')]:
    q = D[D.fx & (D.date >= a) & (D.date < b)]
    print(f'  {pn:14s} spot açılış SAT @15: {st(-q.intra0, q.date, 15)} | @15+tik {st(-q.intra0, q.date, 15, q.tik)}')
