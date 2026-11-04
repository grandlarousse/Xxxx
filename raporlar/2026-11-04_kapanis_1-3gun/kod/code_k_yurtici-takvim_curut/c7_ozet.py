"""Özet: ana adaylarda simetrik budama (en iyi 10 + en kötü 10 çıkar), %1 winsor, en büyük işlemler; tüm testlerde BH-FDR."""
from curlib import *
import glob
cal = vcal(); FW = pd.read_parquet(RES + '/_fwd_cache.parquet'); SR = pd.read_parquet(RES + '/_spot_ret.parquet')
def fw(u, h, e): return FW[f'{u}|{h}|{e}']
def beta(y, x, w=250, mp=120): return (y.rolling(w, min_periods=mp).cov(x) / x.rolling(w, min_periods=mp).var()).shift(1)
def trims(name, d, x, h):
    d = pd.DatetimeIndex(d); x = np.asarray(x, float); ok = np.isfinite(x); d = d[ok]; x = x[ok]
    o = np.argsort(x); keep = o[10:-10]
    m0, t0, n0 = clnw(d, x, h); m1, t1, _ = clnw(d[keep], x[keep], h)
    lo, hi = np.percentile(x, [1, 99]); xw = np.clip(x, lo, hi); m2, t2, _ = clnw(d, xw, h)
    med = np.median(x) * 1e4
    print(f'{name:44s} n={n0} ort {m0:+.1f} (t {t0:.2f}) | simetrik budama ±10: {m1:+.1f} (t {t1:.2f}) | winsor %1: {m2:+.1f} (t {t2:.2f}) | medyan {med:+.1f}')
    return d, x
# --- XU030 ---
F = fut('XU030'); fc, jc = F.front_series('close', 3); sc = spot('XU030')['c'].reindex(cal)
scale = pd.Series(np.where(fc / sc < 0.5, 10.0, 1.0), index=cal); fc = fc * scale
b = np.log(fc / sc); tr_, _ = F.front_series('trades', 3)
db = (b - b.shift(1)).where(jc.eq(jc.shift(1)) & (jc >= 0)).where(tr_ >= 5)
z = db / db.rolling(120, min_periods=60).std().shift(1)
d = z.index[(z.abs() > 1).fillna(False)]; sd = -np.sign(z.loc[d].values)
for e in ['E1', 'E0']:
    dd, xx = trims(f'XU030 Δb z120>1 {e} h1', d, sd * F.fwd(d, 1, e), 1)
x1 = sd * F.fwd(d, 1, 'E1'); T = pd.DataFrame({'d': d, 'side': sd, 'bps': x1 * 1e4, 'db_bps': db.reindex(d).values * 1e4}).dropna().sort_values('bps')
print('XU030 en iyi 10 işlem:'); print(T.tail(10).round(1).to_string(index=False))
# --- Koza ---
r = SR[['TRMET', 'TRALT', 'XU030']].copy(); r['TRENJ'] = spot_ret('TRENJ')
grp = r[['TRALT', 'TRENJ']].mean(axis=1, skipna=False); u = r.TRMET - beta(r.TRMET, grp).clip(0.2, 2.0) * grp
z3 = (u.rolling(3, min_periods=3).sum() / (u.rolling(60, min_periods=40).std() * np.sqrt(3))).reindex(cal)
bTA = beta(r.TRMET, r.TRALT).clip(0.3, 2.0).reindex(cal).fillna(1.0)
d = cal[(z3.abs() > 1.5).fillna(False).values]; sd = np.sign(z3.loc[d].values); bv = bTA.reindex(d).values
for e in ['E0', 'E2']:
    for h in [2, 3]:
        trims(f'Koza momentum k3>1,5 {e} h{h}', d, sd * (fw('TRMET', h, e).reindex(d).values - bv * fw('TRALT', h, e).reindex(d).values) / (1 + bv), h)
# maliyet: iki bacak, sermaye başına ≈ (c_TRMET + β c_TRALT)/(1+β)
L = pd.read_csv(S + '/out/y_viop_likidite.csv').set_index('und')
for col in ['rt_cost_small_bps', 'rt_cost_cons_bps', 'rt_cost_1m_bps']:
    c = (L.at['TRMET', col] + 0.7 * L.at['TRALT', col]) / 1.7; print(f'Koza çifti sermaye başına maliyet {col}: {c:.1f} bps')
# --- Ay sonu ---
c_ = cal.to_series(); me = pd.DatetimeIndex(c_.groupby([c_.index.year, c_.index.month]).max().values); me = me[me < cal[-1]]
trims('Ay sonu XU030D1! E0 h1', me, fw('XU030', 1, 'E0').reindex(me).values, 1)
# --- TCELL–TTKOM (tarayıcı kurgusu: vadeli-sinyal Z20>2) ---
ra_s = spot_ret('TCELL').reindex(cal); rb_s = spot_ret('TTKOM').reindex(cal); bb = beta(ra_s, rb_s).clip(0.3, 2.0)
for src, ra, rb in [('vadeli-sinyal', FW['TCELL|0|r_front'], FW['TTKOM|0|r_front']), ('spot-sinyal', ra_s, rb_s)]:
    uu = ra - bb * rb; Sx = uu.fillna(0).cumsum().where(uu.notna())
    zz = (Sx - Sx.rolling(20, min_periods=16).mean()) / Sx.rolling(20, min_periods=16).std()
    d = cal[(zz.abs() > 2).fillna(False).values]; sd = -np.sign(zz.loc[d].values); bv = bb.reindex(d).fillna(1).values
    for e in ['E0', 'E2']:
        trims(f'TCELL–TTKOM {src} Z20>2 {e} h3', d, sd * (fw('TCELL', 3, e).reindex(d).values - bv * fw('TTKOM', 3, e).reindex(d).values) / (1 + bv), 3)
# --- BH-FDR tüm testler ---
D = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(RES + '/tests_*.csv'))], ignore_index=True)
D['q'] = bh_q(D['p'].values)
print('Toplam test:', len(D), '| BH q<0,05 geçen:', int((D.q < 0.05).sum()))
thr = D.loc[D.q < 0.05, 't'].abs().min() if (D.q < 0.05).any() else np.nan
print('Geçiş eşiği |t| ≈', round(float(thr), 2))
D.to_csv(RES + '/tests_all_curut.csv', index=False)
for blk, pat in [('xu030', 'ANA db z120'), ('koza', 'ANA k3 momentum'), ('ay', 'Ay sonu AL'), ('tcell2', 'Z20>2.0'), ('kchol', 'zdev>0.5'), ('baz', 'Kesitsel L/S 2022-09-23+ A'), ('tem', 'VİOP')]:
    s = D[(D.block == blk) & D.name.astype(str).str.contains(pat, regex=False)]
    print(blk, '|', s[['name', 'h', 'entry', 'n', 'gross', 't', 'q']].round(3).to_string(index=False).replace('\n', '\n   '))
