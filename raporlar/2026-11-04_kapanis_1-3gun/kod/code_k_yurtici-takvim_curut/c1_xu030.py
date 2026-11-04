"""(1) XU030 vadelisi kapanış bazı sıçraması — bağımsız yeniden hesap ve çürütme denemeleri."""
from curlib import *
cal = vcal(); F = fut('XU030')
fc, jc = F.front_series('close', min_dte=3)
fs, _ = F.front_series('settle', min_dte=3)
ftr, _ = F.front_series('trades', min_dte=3)
S_ = spot('XU030'); sc = S_['c'].reindex(cal)
scale = pd.Series(np.where(fc / sc < 0.5, 10.0, 1.0), index=cal)  # 2020-07-27 öncesi vadeli /10 kotasyon
fc = fc * scale; fs = fs * scale
b = np.log(fc / sc)
same = jc.eq(jc.shift(1)) & (jc >= 0)
db = (b - b.shift(1)).where(same)
db = db.where(ftr >= 5)
print('Δb std (bps) yıllara göre:', (db.groupby(db.index.year).std() * 1e4).round(1).to_dict())
out = []
def run(name, z, thr, h, entry, side=None, mask=None, cost=4.8, tag=''):
    on = (z.abs() > thr)
    if mask is not None: on &= mask
    d = z.index[on.fillna(False)]; sd = -np.sign(z.loc[d].values)
    if side == 'L': d = d[sd > 0]; sd = sd[sd > 0]
    if side == 'S': d = d[sd < 0]; sd = sd[sd < 0]
    x = sd * F.fwd(d, h, entry)
    o = summary(d, x, h, cost=cost)
    reg('xu030', name, h, entry, o, thr=thr, tag=tag)
    out.append(f'{name:42s} |z|>{thr} {entry} h{h}: {fmt(o)}')
    return d, sd, x, o

# ---- ana kural ve ızgara (kaç varyant) ----
grid = []
for L in [60, 120, 250]:
    z = db / db.rolling(L, min_periods=L // 2).std().shift(1)
    for thr in [0.75, 1.0, 1.25, 1.5]:
        for h in [1, 2, 3]:
            for e in ['E1', 'E0', 'E2']:
                _, _, _, o = run(f'db z{L}', z, thr, h, e, tag='grid')
                grid.append(dict(L=L, thr=thr, h=h, e=e, n=o['n'], g=o['gross'], t=o['t']))
G = pd.DataFrame(grid)
print('Izgara (h1):'); print(G[G.h == 1].pivot_table(index=['L', 'thr'], columns='e', values='t').round(2))
print(G[G.h == 1].pivot_table(index=['L', 'thr'], columns='e', values='g').round(1))
z = db / db.rolling(120, min_periods=60).std().shift(1)
d, sd, x, o = run('ANA db z120', z, 1.0, 1, 'E1', tag='ana')
run('ANA db z120 yalnız AL', z, 1.0, 1, 'E1', side='L', tag='yan'); run('ANA db z120 yalnız SAT', z, 1.0, 1, 'E1', side='S', tag='yan')
# ---- ayrıştırma: Δb = r_F(kapanış) − r_S(kapanış). Hangisi öngörüyor? ----
rF = np.log(fc / fc.shift(1)).where(same); rS = np.log(sc / sc.shift(1))
y1 = pd.Series(F.fwd(cal, 1, 'E1'), index=cal); y0 = pd.Series(F.fwd(cal, 1, 'E0'), index=cal)
J = pd.concat([db.rename('db'), rF.rename('rF'), rS.rename('rS'), y1.rename('y1'), y0.rename('y0'),
               np.log(fs / fc).rename('st_cl')], axis=1).dropna()
import numpy.linalg as la
for per in [('2017', '2019'), ('2020', '2022'), ('2023', '2026'), ('2017', '2026')]:
    s = J.loc[per[0]:per[1]]
    X = np.column_stack([np.ones(len(s)), s.rF, s.rS]); bb = la.lstsq(X, s.y1, rcond=None)[0]
    b1 = np.polyfit(s.db, s.y1, 1)[0]; b0 = np.polyfit(s.db, s.y0, 1)[0]
    print(f'{per}: y1~db eğim {b1:.3f} | y0~db eğim {b0:.3f} | y1 ~ rF {bb[1]:.3f} + rS {bb[2]:.3f} | corr(db, settle_t/close_t) {s.db.corr(s.st_cl):.2f} n {len(s)}')
# E1 getirisinin bileşenleri: log(settle_t/close_t) (gün t içinde, son 10 dk VWAP − son fiyat) + E0
dd = pd.DatetimeIndex(d)
comp = pd.DataFrame({'E1': x, 'stcl': sd * np.log(fs.reindex(dd).values / fc.reindex(dd).values), 'E0': sd * F.fwd(dd, 1, 'E0')})
print('Ana kural bileşenleri (bps):', (comp.mean() * 1e4).round(1).to_dict())
# ---- saatlik müzayede (2023-11+): S_kapanış / S_18:00 ----
h1 = pd.read_parquet(S + '/data/h1/XU030.IS.parquet'); h1.index = pd.DatetimeIndex(h1.index)
h1['ld'] = pd.DatetimeIndex(h1.ldate).astype('datetime64[ns]')
pre = h1[h1.index.time == pd.Timestamp('14:30').time()].groupby('ld').c.last()  # yaz ızgarası: 14:30 barının kapanışı = 18:00 TSİ (müzayede öncesi)
CA = np.log(sc.reindex(pre.index) / pre).rename('CA')
K = pd.concat([CA, db.rename('db'), z.rename('z'), y1.rename('y1'), y0.rename('y0')], axis=1).dropna()
print('2023-11+ CA ile Δb korelasyonu', round(K.CA.corr(K.db), 3), 'n', len(K), '| CA std bps', round(K.CA.std() * 1e4, 1))
kk = K[K.z.abs() > 1]
print('  sinyal günlerinde corr(CA, Δb)', round(kk.CA.corr(kk.db), 3), ' | y1 ~ CA eğim', round(np.polyfit(K.CA, K.y1, 1)[0], 3),
      ' | y1 ~ db | CA kontrol:', np.round(la.lstsq(np.column_stack([np.ones(len(K)), K.db, K.CA]), K.y1, rcond=None)[0][1:], 3))
# Sinyalin CA dışındaki kısmı: Δb'nin CA'ya ortogonal artığı
bcoef = np.polyfit(K.CA, K.db, 1); K['db_res'] = K.db - np.polyval(bcoef, K.CA)
for col in ['db', 'db_res']:
    zz = K[col] / K[col].std()
    m = zz.abs() > 1; xx = -np.sign(zz[m]) * K.y1[m]
    o2 = summary(K.index[m], xx.values, 1); out.append(f'2023-11+ {col} |z|>1 E1 h1: {fmt(o2)}'); reg('xu030', f'2023+ {col}', 1, 'E1', o2, tag='mek')
# ---- plasebo: rastgele tarih (yön korunur), 1000 tekrar ----
pool = z.dropna().index
yy = pd.Series(F.fwd(cal, 1, 'E1'), index=cal)
pb = placebo_dates(dd, sd, lambda q: yy.reindex(q).values, pool, nrep=1000, seed=1)
print(f'Plasebo rastgele tarih: ort {pb.mean():+.1f}, %95 {np.percentile(pb, 95):+.1f}, %99 {np.percentile(pb, 99):+.1f}; gerçek {np.nanmean(x) * 1e4:+.1f}; p={np.mean(pb >= np.nanmean(x) * 1e4):.3f}')
# Plasebo 2: rastgele yön
rng = np.random.default_rng(2); pr = []
for _ in range(1000):
    s2 = rng.choice([-1, 1], len(dd)); pr.append(np.nanmean(s2 * yy.reindex(dd).values) * 1e4)
pr = np.array(pr); print(f'Plasebo rastgele yön: %95 {np.percentile(pr, 95):+.1f}; p={np.mean(pr >= np.nanmean(x) * 1e4):.3f}')
# ---- işlem sayısı / likidite filtresi ve maliyet ----
for c in [3, 4.8, 5.3, 8, 21.6]:
    print(f'  maliyet {c} bps -> net {o["gross"] - c:+.1f}')
# ---- vade ayı / vade haftası hariç ----
dte = pd.Series(F.exps[np.maximum(jc.values, 0)], index=cal) - cal.to_series()
run('ANA, vadeye ≥10 gün', z, 1.0, 1, 'E1', mask=(dte.dt.days >= 10), tag='yan')
run('ANA, vadeye <10 gün', z, 1.0, 1, 'E1', mask=(dte.dt.days < 10), tag='yan')
for o_ in out: print(o_)
D = save('xu030'); print('test sayısı (bu blok):', len(D))
