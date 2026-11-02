"""b1: bağımsız tekrar + plasebo (işaret çevirme, etiket permütasyonu, tarih kaydırma, sabit kaydırma) + veri madenciliği (grid max-t) testi."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vb import *
rng = np.random.default_rng(20261102)
cal = bist_cal()
IDX = ['XU100.IS', 'XU030.IS', 'XBANK.IS']
O = pd.DataFrame({s: load(s).o.reindex(cal) for s in IDX}); C = pd.DataFrame({s: load(s).c.reindex(cal) for s in IDX})
Ov, Cv = np.log(O.values), np.log(C.values)
N = len(cal)
ev = ev_load(('rating',)); post = ev[ev.period == 'post'].copy()
post['i0'] = [react_idx(cal, a, f) for a, f in zip(post.ann, post.after_close)]
post = post.drop_duplicates('i0').reset_index(drop=True)
print('post events', len(post)); print(post.assign(react=cal[post.i0].date)[['ann', 'agency', 'dir', 'react']].to_string(index=False))

def ret(i0, entry, h, j):
    """entry: 'open' o[i0]->c[i0+h]; 'close' c[i0]->c[i0+h]; 'pc' c[i0-1]->c[i0+h]"""
    i0 = np.asarray(i0); ok = (i0 + h < N) & (i0 >= 1)
    out = np.full(i0.shape, np.nan); ii = i0[ok]
    if entry == 'open': out[ok] = Cv[ii + h, j] - Ov[ii, j]
    elif entry == 'close': out[ok] = Cv[ii + h, j] - Cv[ii, j]
    else: out[ok] = Cv[ii + h, j] - Cv[ii - 1, j]
    return out

i0 = post.i0.values; dr = post.dir.values; yr = cal[i0].year
COST = 15e-4
print('\n=== (a) Bağımsız tekrar: Pazartesi açılış -> t+2 kapanış, kontraryen, 15 bps ===')
for j, s in enumerate(IDX):
    v = pd.Series(-dr * ret(i0, 'open', 2, j) - COST, index=cal[i0])
    print(fmt(v, s + ' ALL')); print(fmt(v[v.index.year <= 2020], '   IS 2014-20')); print(fmt(v[v.index.year >= 2021], '   OOS 2021-26'))
print('\n--- girişe göre (XU100, 15 bps) ---')
for entry in ['open', 'close', 'pc']:
    for h in [0, 1, 2, 3, 5, 10]:
        if entry == 'close' and h == 0: continue
        v = -dr * ret(i0, entry, h, 0) - COST
        print(fmt(v, f'{entry} -> t+{h}'))
print('\n--- günlük profil (XU100, işaretli brüt, bps) ---')
gap = -dr * (Ov[i0, 0] - Cv[i0 - 1, 0]); intra = -dr * (Cv[i0, 0] - Ov[i0, 0])
prof = {'gap t0': gap, 'intra t0': intra}
for k in range(1, 6): prof[f'cc t+{k}'] = -dr * (Cv[i0 + k, 0] - Cv[i0 + k - 1, 0])
for k, v in prof.items(): print(fmt(v, k))
print('corr(gap, intra) olay günleri:', np.corrcoef(gap, intra)[0, 1].round(2))
# tüm günler için gap-intra korelasyonu (mekanik bid-ask kontrolü)
g_all = Ov[1:, 0] - Cv[:-1, 0]; in_all = Cv[1:, 0] - Ov[1:, 0]; m = (cal[1:] >= '2014-01-01') & np.isfinite(g_all) & np.isfinite(in_all)
print('corr(gap, intra) tüm günler 2014+:', np.corrcoef(g_all[m], in_all[m])[0, 1].round(3))

base = (-dr * ret(i0, 'open', 2, 0)).mean()
print(f'\n=== (b) Plasebolar (XU100 open->t+2 brüt; gerçek ortalama {1e4*base:+.1f} bps) ===')
B = 100000
x = ret(i0, 'open', 2, 0)
sf = np.array([(-dr * rng.choice([-1, 1], len(dr)) * x).mean() for _ in range(B)])
print(f'işaret çevirme p (tek yönlü) = {(sf >= base).mean():.5f}')
lp = np.array([(-rng.permutation(dr) * x).mean() for _ in range(B)])
print(f'etiket permütasyonu p = {(lp >= base).mean():.5f}  (perm ort {1e4*lp.mean():+.1f})')
print('ham (işaretsiz) olay penceresi ort: indirimler', round(1e4 * x[dr < 0].mean(), 1), ' artırımlar', round(1e4 * x[dr > 0].mean(), 1))

wd_shift = lambda i, k: int(cal.searchsorted(cal[i] + pd.Timedelta(days=7 * k)))
ks = np.r_[-52:-2, 3:53]
def shifted_idx(kvec): return np.array([wd_shift(i, k) for i, k in zip(i0, kvec)])
# rastgele bağımsız kaydırma
D2 = 20000; pl = np.empty(D2); kk = rng.choice(ks, size=(D2, len(i0)))
pre_idx = {}
for k in ks: pre_idx[k] = np.array([wd_shift(i, k) for i in i0])
sh_all = np.stack([pre_idx[k] for k in ks])  # len(ks) x n
kpos = {k: p for p, k in enumerate(ks)}
kidx = np.vectorize(kpos.get)(kk)
I = sh_all[kidx, np.arange(len(i0))[None, :]]
okm = (I + 2 < N) & (I >= 1)
Xp = np.where(okm, Cv[np.minimum(I + 2, N - 1), 0] - Ov[np.minimum(I, N - 1), 0], np.nan)
pl = np.nanmean(-dr[None, :] * Xp, axis=1)
print(f'tarih kaydırma (±3..52 hf, bağımsız) p = {(pl >= base).mean():.5f}  plasebo ort {1e4*np.nanmean(pl):+.1f} sd {1e4*np.nanstd(pl):.1f}')
print('\n--- sabit kaydırma (bayat/erken sinyal), XU100 open->t+2, işaretli brüt ---')
for k in [-8, -4, -3, -2, -1, 1, 2, 3, 4, 8]:
    Ik = np.array([wd_shift(i, k) for i in i0]); v = -dr * ret(Ik, 'open', 2, 0)
    print(fmt(v, f'kaydırma {k:+d} hafta'))
# günlük kaydırma ±1..5 işlem günü
for k in [-5, -3, -1, 1, 3, 5]:
    v = -dr * ret(i0 + k, 'open', 2, 0); print(fmt(v, f'kaydırma {k:+d} işlem günü'))

print('\n=== (c) Veri madenciliği: grid max-t (gerçek vs plasebo) ===')
grid = [(e, h, j) for e in ['open', 'close'] for h in [0, 1, 2, 3, 5, 10] for j in range(3) if not (e == 'close' and h == 0)]
def grid_t(Iv):
    ts = []
    for e, h, j in grid:
        v = -dr * ret(Iv, e, h, j); v = v[np.isfinite(v)]
        ts.append(v.mean() / (v.std(ddof=1) / np.sqrt(len(v))))
    return np.array(ts)
tg = grid_t(i0); print('grid boyutu', len(grid), ' gerçek max|t|', np.abs(tg).max().round(2), ' gerçek t(open,2,XU100)', tg[[g == ('open', 2, 0) for g in grid].index(True)].round(2))
D3 = 3000; mx = np.empty(D3)
for b in range(D3): mx[b] = np.abs(grid_t(I[b])).max()
print(f'plasebo max|t| dağılımı: medyan {np.median(mx):.2f}, %95 {np.quantile(mx,.95):.2f}, %99 {np.quantile(mx,.99):.2f};  p(max|t|>=gerçek max) = {(mx >= np.abs(tg).max()).mean():.4f}')
print(f'p(max|t| >= 3.77) = {(mx >= 3.77).mean():.4f}')
pd.DataFrame({'grid': [str(g) for g in grid], 't': tg}).to_csv(HERE + '/res_b1_grid.csv', index=False)
np.save(HERE + '/placebo_I.npy', I[:D3])
