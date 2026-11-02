"""b2: rejim mi olay mı? Hafta kaydırma profili, yerel taban (±1..6 hafta aynı gün pencereleri) çıkarılmış anormal getiri,
kümeleme (yıl/epizot) düzeyinde t, uç değer bağımlılığı."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vb import *
from scipy import stats
cal = bist_cal(); N = len(cal)
X = load('XU100.IS'); O = np.log(X.o.reindex(cal).values); C = np.log(X.c.reindex(cal).values)
ev = ev_load(('rating',)); post = ev[ev.period == 'post'].copy()
post['i0'] = [react_idx(cal, a, f) for a, f in zip(post.ann, post.after_close)]
post = post.drop_duplicates('i0').reset_index(drop=True)
i0 = post.i0.values; dr = post.dir.values
wd = lambda i, k: int(cal.searchsorted(cal[i] + pd.Timedelta(days=7 * k)))
def w(I, h=2): I = np.asarray(I); return C[I + h] - O[I]
real = -dr * w(i0)
print('=== hafta kaydırma profili (XU100 açılış->t+2, işaretli brüt) ===')
rows = []
for k in range(-26, 27):
    Ik = np.array([wd(i, k) for i in i0]); v = -dr * w(Ik); t, n = tstat(v)
    rows.append(dict(k=k, mean=1e4 * v.mean(), t=t))
P = pd.DataFrame(rows).set_index('k'); P.to_csv(HERE + '/res_b2_shift_profile.csv')
print(P.round(2).T.to_string())
nz = P.drop(0)
print(f'k≠0 ortalama {nz["mean"].mean():+.1f} bps; |k|<=4 (k≠0) ort {nz.loc[[-4,-3,-2,-1,1,2,3,4],"mean"].mean():+.1f}; |k| 5..26 ort {nz[nz.index.map(abs)>=5]["mean"].mean():+.1f}')
print('k≠0 içinde gerçek değerden (+%.0f) büyük olan sayısı: %d / %d' % (P.loc[0, 'mean'], (nz['mean'] >= P.loc[0, 'mean']).sum(), len(nz)))

print('\n=== yerel taban çıkarılmış anormal getiri ===')
for lo, hi in [(1, 4), (1, 6), (2, 8), (5, 26)]:
    ks = [k for k in range(-hi, hi + 1) if lo <= abs(k) <= hi]
    basem = np.array([np.mean([w([wd(i, k)])[0] for k in ks]) for i in i0])
    ab = -dr * (w(i0) - basem)
    print(fmt(ab, f'taban ±{lo}..{hi} hafta'))
# trend: olay öncesi 60 gün ve sonrası 60 gün (merkezli) günlük ortalama x 3 gün
for L in [20, 60, 120]:
    cc = np.diff(C, prepend=np.nan)
    mu = np.array([np.nanmean(np.r_[cc[i - L:i - 5], cc[i + 6:i + L]]) for i in i0])
    ab = -dr * (w(i0) - 3 * mu); print(fmt(ab, f'merkezli ±{L}g sürüklenme çıkarılmış (olay ±5g hariç)'))

print('\n=== kümeleme: yıl ve epizot düzeyi ===')
T = pd.DataFrame({'d': cal[i0], 'v': real - 15e-4, 'dir': dr, 'ag': post.agency.values})
T['yr'] = T.d.dt.year
ep = {2016: '2016-17 IG kaybı', 2017: '2016-17 IG kaybı', 2018: '2018 kur krizi', 2019: '2019-20', 2020: '2019-20', 2022: '2022 heterodoks', 2024: '2024-25 artırımlar', 2025: '2024-25 artırımlar'}
T['ep'] = T.yr.map(ep)
g = T.groupby('yr').v.mean(); t, n = tstat(g); print(f'yıl ortalamaları: {(1e4*g).round(0).to_dict()}  -> t {t:.2f} (n={n})')
g = T.groupby('ep').v.mean(); t, n = tstat(g); print(f'epizot ortalamaları: {(1e4*g).round(0).to_dict()}  -> t {t:.2f} (n={n})')
print('\n=== uç değer bağımlılığı ===')
v = T.v.sort_values(ascending=False)
for k in [0, 1, 2, 3, 5]: print(fmt(v.iloc[k:], f'en iyi {k} olay hariç'))
print(fmt(stats.trimboth(T.v.values, 0.1), 'kırpılmış %10 (her iki uç)'))
print('Wilcoxon p (tek yönlü):', round(stats.wilcoxon(T.v, alternative='greater').pvalue, 5), ' işaret testi p:', round(stats.binomtest(int((T.v > 0).sum()), len(T), 0.5, alternative='greater').pvalue, 5))
print('olay tablosu:'); print(T.assign(v=(1e4 * T.v).round(0)).to_string(index=False))
T.to_csv(HERE + '/res_b2_events.csv', index=False)
