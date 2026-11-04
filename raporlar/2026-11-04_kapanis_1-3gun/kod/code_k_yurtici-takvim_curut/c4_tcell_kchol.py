"""(4) TCELL–TTKOM göreli dönüş ve (5) KCHOL NAV sapması — bağımsız yeniden hesap."""
from curlib import *
cal = vcal()
FW = pd.read_parquet(RES + '/_fwd_cache.parquet')
def fw(u, h, e): return FW[f'{u}|{h}|{e}']
out = []
def beta(y, x, w=250, mp=120):
    return (y.rolling(w, min_periods=mp).cov(x) / x.rolling(w, min_periods=mp).var()).shift(1)
def run(block, name, d, sd, xfun, h, e, cost=0.0, tag='', is_end='2021-12-31'):
    x = sd * xfun(d, h, e)
    o = summary(d, x, h, cost=cost, is_end=is_end); reg(block, name, h, e, o, tag=tag)
    out.append(f'{name:44s} {e} h{h}: {fmt(o)}'); return x, o
# ================= TCELL–TTKOM =================
A = spot('TCELL'); B = spot('TTKOM')
la = np.log(A['adj']).reindex(cal).ffill(limit=2); lb = np.log(B['adj']).reindex(cal).ffill(limit=2)
ra = la.diff(); rb = lb.diff()
for bname, bb in [('β250', beta(ra, rb).clip(0.2, 2.0)), ('β=1', pd.Series(1.0, index=cal)), ('β=0,61 sabit', pd.Series(0.61, index=cal))]:
    sp = la - bb * lb
    for W in [20, 60]:
        z = (sp - sp.rolling(W, min_periods=W).mean()) / sp.rolling(W, min_periods=W).std()
        for thr in [1.5, 2.0]:
            on = (z.abs() > thr).fillna(False).values
            d = cal[on]; sd = -np.sign(z.values[on]); bv = bb.reindex(d).fillna(1.0).values
            xf = lambda dd, h, e, bv=bv: (fw('TCELL', h, e).reindex(dd).values - bv * fw('TTKOM', h, e).reindex(dd).values) / (1 + bv)
            for h in [1, 2, 3, 5]:
                for e in ['E0', 'E2']:
                    tg = 'ana' if (bname == 'β250' and W == 20 and thr == 2.0) else 'grid'
                    run('tcell', f'TCELL–TTKOM Z{W}>{thr} {bname} dönüş', d, sd, xf, h, e, tag=tg)
# yeni giriş sayısı ve yalnız ilk gün
bb = beta(ra, rb).clip(0.2, 2.0); sp = la - bb * lb
z = (sp - sp.rolling(20, min_periods=20).mean()) / sp.rolling(20, min_periods=20).std()
on = (z.abs() > 2).fillna(False)
first = on & ~on.shift(1, fill_value=False)
print('TCELL–TTKOM Z20>2: sinyal günü', int(on.sum()), 'yeni giriş', int(first.sum()))
d = cal[first.values]; sd = -np.sign(z.reindex(d).values); bv = bb.reindex(d).fillna(1.0).values
xf = lambda dd, h, e: (fw('TCELL', h, e).reindex(dd).values - bv * fw('TTKOM', h, e).reindex(dd).values) / (1 + bv)
for h in [2, 3]:
    for e in ['E0', 'E2']:
        run('tcell', 'TCELL–TTKOM Z20>2 yalnız yeni giriş', d, sd, xf, h, e, tag='ilk')
# spot uzun geçmiş
la_s = np.log(A['adj']); lb_s = np.log(B['adj']); J = pd.concat([la_s.rename('a'), lb_s.rename('b')], axis=1).ffill(limit=2).dropna()
ras = J.a.diff(); rbs = J.b.diff(); bbs = beta(ras, rbs).clip(0.2, 2.0); sps = J.a - bbs * J.b
zs = (sps - sps.rolling(20, min_periods=20).mean()) / sps.rolling(20, min_periods=20).std()
for h in [2, 3]:
    ons = (zs.abs() > 2).fillna(False).values; ds = J.index[ons]; sds = -np.sign(zs.values[ons]); bvs = bbs.reindex(ds).fillna(1).values
    fa = spot_fwd(ras, h).reindex(ds).values; fb = spot_fwd(rbs, h).reindex(ds).values
    x = sds * (fa - bvs * fb) / (1 + bvs); o = summary(ds, x, h, is_end='2020-12-31'); reg('tcell', 'SPOT TCELL–TTKOM Z20>2', h, 'S', o, tag='spot')
    out.append(f'SPOT TCELL–TTKOM Z20>2 (2009+) h{h}: {fmt(o)}')
# ================= KCHOL NAV =================
W_ = {'TUPRS': .33, 'YKBNK': .24, 'FROTO': .20, 'ARCLK': .07, 'TOASO': .04, 'AYGAZ': .03, 'TTRAK': .03, 'OTKAR': .02}
lp = {}
for s in ['KCHOL'] + list(W_):
    try: lp[s] = np.log(spot(s)['adj'])
    except Exception as ex: print('yok', s, ex)
LP = pd.DataFrame(lp).ffill(limit=2)
RP = LP.diff()
wsum = sum(W_[s] for s in W_ if s in RP)
nav_r = sum(RP[s].fillna(0) * W_[s] for s in W_ if s in RP) / wsum  # günlük yeniden dengelenen sepet (sabit ağırlık)
Dv = (RP['KCHOL'] - nav_r).cumsum()  # log KCHOL − log NAV (sabit ağırlıklı sepet, kümülatif)
dev = Dv - Dv.rolling(60, min_periods=60).mean()
zdev = dev / dev.rolling(250, min_periods=120).std().shift(1)
rk = RP['KCHOL'].reindex(cal); rx = spot_ret('XU030').reindex(cal)
bK = beta(rk, rx).clip(0.3, 2.0)
zc = zdev.reindex(cal)
for thr in [0.5, 1.0, 1.5]:
    on = (zc.abs() > thr).fillna(False).values; d = cal[on]; sd = -np.sign(zc.values[on]); bv = bK.reindex(d).fillna(1.0).values
    xf = lambda dd, h, e, bv=bv: (fw('KCHOL', h, e).reindex(dd).values - bv * fw('XU030', h, e).reindex(dd).values) / (1 + bv)
    for h in [1, 2, 3, 5]:
        for e in ['E0', 'E2']:
            run('kchol', f'KCHOL NAV zdev>{thr} (KCHOL1!−β·XU030D1!)', d, sd, xf, h, e, tag='ana' if thr == 0.5 else 'grid')
on = (zc.abs() > 0.5).fillna(False)
print('KCHOL zdev>0,5 sinyal günü oranı', round(float(on.mean()), 3), 'yeni giriş/yıl', round(float((on & ~on.shift(1, fill_value=False)).sum()) / 9.6, 1))
# spot uzun geçmiş KCHOL − β XU030
rxs = spot_ret('XU030'); J2 = pd.concat([RP['KCHOL'].rename('k'), rxs.rename('x'), zdev.rename('z')], axis=1).dropna(subset=['k', 'x'])
bKs = beta(J2.k, J2.x).clip(0.3, 2.0)
for h in [3]:
    on = (J2.z.abs() > 0.5).fillna(False).values; ds = J2.index[on]; sds = -np.sign(J2.z.values[on]); bv = bKs.reindex(ds).fillna(1).values
    x = sds * (spot_fwd(J2.k, h).reindex(ds).values - bv * spot_fwd(J2.x, h).reindex(ds).values) / (1 + bv)
    o = summary(ds, x, h, is_end='2020-12-31'); reg('kchol', 'SPOT KCHOL NAV zdev>0,5', h, 'S', o, tag='spot'); out.append(f'SPOT KCHOL NAV zdev>0,5 h{h}: {fmt(o)}')
for o_ in out: print(o_)
save('tcell'); save('kchol'); print('test sayısı', sum(1 for r in REGISTRY))
