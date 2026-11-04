"""(2) Koza grubu göreli momentum (TRMET artığı) — bağımsız yeniden hesap, plasebo evreni, limit kilidi, en iyi 10 işlem."""
from curlib import *
cal = vcal()
FW = pd.read_parquet(RES + '/_fwd_cache.parquet'); SR = pd.read_parquet(RES + '/_spot_ret.parquet')
SR['TRENJ'] = spot_ret('TRENJ')
def fw(u, h, e): return FW[f'{u}|{h}|{e}']
rS = SR.reindex(cal)  # spot getiriler VİOP takviminde (VİOP günü olmayan spot günleri düşer)
# NOT: spot takvimi ile VİOP takvimi farklı olabilir; artığı spot takviminde hesaplayıp VİOP takvimine eşleriz
def beta(y, x, w=250, mp=120):
    return (y.rolling(w, min_periods=mp).cov(x) / x.rolling(w, min_periods=mp).var()).shift(1)
def zk(u, k, sdw=60):
    return u.rolling(k, min_periods=k).sum() / (u.rolling(sdw, min_periods=40).std() * np.sqrt(k))
r = SR[['TRMET', 'TRALT', 'TRENJ', 'XU030']].dropna(how='all')
grp = r[['TRALT', 'TRENJ']].mean(axis=1, skipna=False)
b_g = beta(r.TRMET, grp).clip(0.2, 2.0)
u = r.TRMET - b_g * grp
bTA = beta(r.TRMET, r.TRALT).clip(0.3, 2.0)
lock = FW['TRMET|0|r_front'].abs() > np.log(1.095)  # sinyal günü TRMET vadelisi limitte (±%10 rejimi)
lockA = FW['TRALT|0|r_front'].abs() > np.log(1.095)
out = []
def pair_ret(dates, h, e, bb):
    return (fw('TRMET', h, e).reindex(dates).values - bb * fw('TRALT', h, e).reindex(dates).values) / (1 + bb)
def run(name, z, thr, h, e, mode='mom', excl=None, cost=0.0, tag='', ret_fun=None):
    zz = z.reindex(cal)
    on = zz.abs() > thr
    if excl is not None: on &= ~excl.reindex(cal).fillna(False)
    d = cal[on.fillna(False).values]
    sd = np.sign(zz.loc[d].values) * (1 if mode == 'mom' else -1)
    bb = bTA.reindex(d).fillna(1.0).values
    x = sd * (pair_ret(d, h, e, bb) if ret_fun is None else ret_fun(d, h, e))
    o = summary(d, x, h, cost=cost); reg('koza', name, h, e, o, thr=thr, tag=tag)
    out.append(f'{name:40s} |z|>{thr} {e} h{h}: {fmt(o)}')
    return d, sd, x, o
# ---- ana kural + ızgara (k, eşik) ----
for k in [1, 2, 3, 5]:
    z = zk(u, k)
    for thr in [1.0, 1.5, 2.0]:
        for h in [1, 2, 3]:
            for e in ['E0', 'E2']:
                run(f'TRMET artığı k{k} momentum', z, thr, h, e, tag='grid')
z3 = zk(u, 3)
for e in ['E0', 'E1', 'E2']:
    for h in [1, 2, 3]:
        run('ANA k3 momentum', z3, 1.5, h, e, tag='ana', cost=2 * 7.5)
# ---- limit kilidi: sinyal günü vadeli limitteyse dolum yok ----
for h in [1, 2, 3]:
    run('ANA kilitli günler hariç', z3, 1.5, h, 'E0', excl=(lock | lockA), tag='lim')
print('Sinyal günlerinin kilitli oranı:', round(float((lock | lockA).reindex(cal[(z3.reindex(cal).abs() > 1.5).fillna(False).values]).mean()), 3))
# ---- XU030 hedge'li (tek bacak TRMET) ----
bX = beta(r.TRMET, r.XU030).clip(0.3, 2.0)
def xu_ret(d, h, e):
    bb = bX.reindex(d).fillna(1.0).values
    return (fw('TRMET', h, e).reindex(d).values - bb * fw('XU030', h, e).reindex(d).values) / (1 + bb)
for h in [1, 2, 3]:
    for e in ['E0', 'E2']:
        run('ANA TRMET−β·XU030', z3, 1.5, h, e, ret_fun=xu_ret, tag='alt')
# ---- ters hisse: TRALT artığı (TRMET+TRENJ grubuna göre), TRALT1!−β·TRMET1! ----
grp2 = r[['TRMET', 'TRENJ']].mean(axis=1, skipna=False)
uA = r.TRALT - beta(r.TRALT, grp2).clip(0.2, 2.0) * grp2
bAT = beta(r.TRALT, r.TRMET).clip(0.3, 2.0)
def alt_ret(d, h, e):
    bb = bAT.reindex(d).fillna(1.0).values
    return (fw('TRALT', h, e).reindex(d).values - bb * fw('TRMET', h, e).reindex(d).values) / (1 + bb)
for h in [1, 2, 3]:
    for e in ['E0', 'E2']:
        run('TERS: TRALT artığı momentum', zk(uA, 3), 1.5, h, e, ret_fun=alt_ret, tag='ters')
# ---- spot uzun geçmiş (2010+) — bilgi ----
def spot_pair(d, h, e):
    f = lambda s: spot_fwd(r[s], h).reindex(d).values
    bb = bTA.reindex(d).fillna(1.0).values
    return (f('TRMET') - bb * f('TRALT')) / (1 + bb)
zs = z3.dropna(); ds = zs.index[zs.abs() > 1.5]
for h in [1, 2, 3]:
    x = np.sign(zs.loc[ds].values) * spot_pair(ds, h, 'S')
    o = summary(ds, x, h, is_end='2020-12-31'); reg('koza', 'SPOT ANA k3 momentum', h, 'S', o, tag='spot')
    out.append(f'SPOT ANA k3 momentum (2011+) h{h}: {fmt(o)}')
# ---- en büyük işlemler ----
d, sd, x, o = run('ANA k3 momentum (liste)', z3, 1.5, 2, 'E0', tag='ana2')
T = pd.DataFrame({'date': d, 'side': sd, 'ret_bps': x * 1e4, 'lockM': lock.reindex(d).values, 'lockA': lockA.reindex(d).values,
                  'z3': z3.reindex(d).values}).dropna(subset=['ret_bps']).sort_values('ret_bps')
print('En iyi 12 işlem (h2 E0):'); print(T.tail(12).round(1).to_string())
print('En kötü 5:'); print(T.head(5).round(1).to_string())
# örtüşme: ardışık sinyal günleri (aynı olay) -> bağımsız olay sayısı
dd = pd.DatetimeIndex(T.date.sort_values()); pos = cal.get_indexer(dd); newev = np.r_[True, np.diff(pos) > 3]
print('Sinyal günü', len(dd), 'bağımsız olay (3 günden uzak)', newev.sum())
# yalnız ilk gün (yeni olay) girişleri
first = dd[newev]
for h in [1, 2, 3]:
    for e in ['E0', 'E2']:
        zz = z3.reindex(first); sdf = np.sign(zz.values); bb = bTA.reindex(first).fillna(1).values
        xf = sdf * pair_ret(first, h, e, bb); o = summary(first, xf, h); reg('koza', 'ANA yalnız ilk gün', h, e, o, tag='ilk')
        out.append(f'ANA yalnız yeni olay ilk günü {e} h{h}: {fmt(o)}')
# ---- plasebo: rastgele tarih ----
pool = cal[(cal >= '2019-01-01') & z3.reindex(cal).notna().values]
d2, sd2, x2, o2 = run('ANA (plasebo için)', z3, 1.5, 2, 'E2', tag='pl')
for e, h in [('E0', 2), ('E2', 2)]:
    dd_, sd_, xx_, _ = run('ANA (plasebo için)', z3, 1.5, h, e, tag='pl')
    yy = pd.Series(pair_ret(cal, h, e, bTA.reindex(cal).fillna(1.0).values), index=cal)
    pb = placebo_dates(dd_, sd_, lambda q: yy.reindex(q).values, pool, nrep=1000, seed=3)
    print(f'Plasebo rastgele tarih {e} h{h}: %95 {np.percentile(pb, 95):+.1f} %99 {np.percentile(pb, 99):+.1f}; gerçek {np.nanmean(xx_) * 1e4:+.1f}; p={np.mean(pb >= np.nanmean(xx_) * 1e4):.3f}')
for o_ in out: print(o_)
D = save('koza'); print('test sayısı (bu blok):', len(D))
