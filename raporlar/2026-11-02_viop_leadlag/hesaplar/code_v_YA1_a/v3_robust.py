"""v_YA1_a — sağlamlık: (1) koşulsuz gün-içi short tabanı (piyasa gün-içi sürüklenmesi), (2) TU tanım varyantları (gerçek dokunma vs 'yakın'),
(3) aynı gün olay sayısına göre ayrım (kriz kümeleri), (4) hisse yoğunlaşması / tek-hisse-dışarıda, (5) yıllara göre, (6) piyasa-nötr / koşulsuz-fazla.
"""
import numpy as np, pandas as pd, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from v1_events import VIOP
from v2_bt import nw_t
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 30); pd.set_option('display.max_rows', 300)

def st(x, dates, cost=15):
    x = pd.Series(np.asarray(x, float) - cost / 1e4); d = pd.Series(np.asarray(dates))
    ok = x.notna().values; x = x[ok]; d = d[ok]
    if len(x) < 10: return dict(n=len(x))
    gm = x.groupby(d.values).mean()
    return dict(n=len(x), trade=round(1e4 * x.mean(), 1), t_cl=round(gm.mean() / (gm.std() / np.sqrt(len(gm))), 2), day=round(1e4 * gm.mean(), 1), t_nw=round(nw_t(gm), 2))

F = pd.read_parquet(HERE + '/_full.parquet'); F = F[F.reg == 'P10'].copy()
ok = F.contig & ~F.ca
print('=== (1) Koşulsuz: her gün açılışta SAT, kapanışta KAPAT (brüt) ===')
base = {}
for lab, m in [('viop47', F.viop), ('all217', F.stock.notna())]:
    s = F[m & ok & F.intra.notna()]
    for a, b in [('2020-03-13', '2020-12-31'), ('2021-01-01', '2026-12-31'), ('2020-03-13', '2022-12-31'), ('2023-01-01', '2026-12-31'), ('2020-03-13', '2026-12-31')]:
        ss = s[(s.date >= a) & (s.date <= b)]
        r = st(-ss.intra, ss.date, 0); base[(lab, a, b)] = r; print(lab, a[:7], b[:7], r)
# hisse-gün bazında koşulsuz ortalama (aynı hisse, 2020-03+): ertesi gün-içi fade'in 'fazla' kısmı
mu = F[ok].groupby('stock').intra.mean()
F['intra_1_ex'] = F.intra_1 - F.stock.map(mu)
print('\n=== (2) TU varyantları: t+1 açılış SAT -> kapanış (15 bps) ===')
tol = np.minimum(np.maximum(F.tik_rel, 0.001) + 0.001, 0.0075); upx = 1 + F.lim - tol
var = {
    'TU_mine (h tavanda, R<1.09)': ok & (F.Rh >= upx) & (F.Rh <= 1.105) & (F.R < 1.09),
    'TU_src (h>=1.0925, R<1.0825)': ok & (F.Rh >= 1.0925) & (F.Rh <= 1.106) & (F.R < 1.0825),
    'NEAR (1.0925<=h<tavan, R<1.0825) = tavana DOKUNMADI': ok & (F.Rh >= 1.0925) & (F.Rh < upx) & (F.R < 1.0825),
    'PLACEBO h>=1.07 & h<1.0925, R<=h-0.01': ok & (F.Rh >= 1.07) & (F.Rh < 1.0925) & (F.R <= F.Rh - 0.01),
    'PLACEBO2 h>=1.05 & h<1.07, R<=h-0.01': ok & (F.Rh >= 1.05) & (F.Rh < 1.07) & (F.R <= F.Rh - 0.01),
}
for k, m in var.items():
    for lab, um in [('viop47', F.viop), ('all217', F.stock.notna())]:
        s = F[m & um]
        print(f'{k:55s} {lab:7s}', st(-s.intra_1, s.date), '| koşulsuz-fazla:', st(-s.intra_1_ex, s.date, 15).get('trade'))
print('\n=== (3) Aynı gün olay sayısı (TC fade, TU fade, BC dolum-uygun) — kriz kümesi etkisi ===')
E = pd.read_parquet(HERE + '/_ev.parquet'); E = E[E.reg == 'P10'].copy()
E['intra_1_ex'] = E.intra_1 - E.stock.map(mu)
for cls in ['TC', 'TU', 'BC']:
    E['n_' + cls] = E.groupby('date')[cls].transform('sum')
CR = [('2020-03-13', '2020-04-30'), ('2021-12-01', '2021-12-31'), ('2023-02-06', '2023-03-15'), ('2025-03-19', '2025-04-30'), ('2026-09-01', '2026-10-31')]
cris = pd.Series(False, index=E.index)
for a, b in CR: cris |= (E.date >= a) & (E.date <= b)
E['crisis'] = cris
for name, m, col, sg, cst in [('TC fade', E.TC, 'intra_1', -1, 15), ('TU fade', E.TU, 'intra_1', -1, 15), ('BC short dolum-uygun', E.BC & (E.BC_1 == False), 'dr2_5', -1, 19)]:
    cls = name.split()[0]
    for lab, um in [('viop47', E.viop), ('all217', E.stock.notna())]:
        s = E[m & um]
        ncol = 'n_' + cls
        print(name, lab, 'tümü', st(sg * s[col], s.date, cst), '| gün olay<5:', st(sg * s[s[ncol] < 5][col], s[s[ncol] < 5].date, cst),
              '| >=5:', st(sg * s[s[ncol] >= 5][col], s[s[ncol] >= 5].date, cst), '| kriz hariç:', st(sg * s[~s.crisis][col], s[~s.crisis].date, cst))
print('\n=== (4) Hisse yoğunlaşması (VİOP47 TC fade @15 / BC dolum-uygun @19) ===')
for name, m, col, cst in [('TC fade', E.TC & E.viop, 'intra_1', 15), ('TU fade', E.TU & E.viop, 'intra_1', 15), ('BC fill', E.BC & (E.BC_1 == False) & E.viop, 'dr2_5', 19)]:
    s = E[m].copy(); s['p'] = -s[col] - cst / 1e4
    bys = s.groupby('stock').p.agg(['count', 'mean', 'sum']).sort_values('sum')
    bys['mean'] = (1e4 * bys['mean']).round(0); bys['sum'] = (1e4 * bys['sum']).round(0)
    print(name, 'hisse sayısı', len(bys), 'pozitif ort. hisse', (bys['mean'] > 0).sum(), '| en çok katkı:', bys.tail(5).to_dict('index'), '| en kötü:', bys.head(3).to_dict('index'))
    tot = s.p.sum(); top = bys['sum'].tail(3).sum() / 1e4
    print('   toplam katkı %.0f bps-işlem; ilk 3 hisse payı %.0f%%' % (1e4 * tot, 100 * top / tot if tot != 0 else np.nan))
    lo = []
    for k in bys.index:
        ss = s[s.stock != k]; lo.append(1e4 * ss.p.mean())
    print('   tek-hisse-dışarıda ortalama (işlem başı) min/max: %.1f / %.1f' % (min(lo), max(lo)))
print('\n=== (5) Yıllara göre (15 bps; BC 19) ===')
for name, m, col, cst in [('TC fade', E.TC, 'intra_1', 15), ('TU fade', E.TU, 'intra_1', 15), ('BC fill', E.BC & (E.BC_1 == False), 'dr2_5', 19)]:
    for lab, um in [('viop47', E.viop), ('all217', E.stock.notna())]:
        s = E[m & um]
        yy = {int(y): st(-g[col], g.date, cst).get('trade') for y, g in s.groupby('yr')}
        yd = {int(y): st(-g[col], g.date, cst).get('day') for y, g in s.groupby('yr')}
        print(f'{name:8s} {lab:7s} işlem:', yy, ' gün:', yd)
print('\n=== (6) Koşulsuz hisse gün-içi ortalaması düşülmüş fade (VİOP47 / all, 15 bps) ===')
for name, m in [('TC', E.TC), ('TU', E.TU)]:
    for lab, um in [('viop47', E.viop), ('all217', E.stock.notna())]:
        s = E[m & um]
        for a, b in [('2020-03-13', '2026-12-31'), ('2020-03-13', '2020-12-31'), ('2021-01-01', '2026-12-31'), ('2020-03-13', '2022-12-31'), ('2023-01-01', '2026-12-31')]:
            ss = s[(s.date >= a) & (s.date <= b)]
            print(name, lab, a[:4], b[:4], 'ham', st(-ss.intra_1, ss.date), 'XU100-nötr', st(-(ss.intra_1 - ss.xintra_1), ss.date, 19), 'hisse-koşulsuz-fazla', st(-ss.intra_1_ex, ss.date))
