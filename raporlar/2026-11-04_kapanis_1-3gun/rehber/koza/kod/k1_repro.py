"""(1) Araştırma kuralının birebir yeniden üretimi (c2_koza.py) — yalnız okuma; araştırma dizinine yazmaz.
İki yol: (a) araştırmanın _fwd_cache.parquet önbelleği, (b) curlib.Fut ile önbelleksiz yeniden hesap. İkisi aynı sonucu vermeli."""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_k_yurtici-takvim_curut')
import curlib as C
import numpy as np, pandas as pd
cal = C.vcal()
FW = pd.read_parquet(C.RES + '/_fwd_cache.parquet'); SR = pd.read_parquet(C.RES + '/_spot_ret.parquet')
SR['TRENJ'] = C.spot_ret('TRENJ')


def beta(y, x, w=250, mp=120):
    return (y.rolling(w, min_periods=mp).cov(x) / x.rolling(w, min_periods=mp).var()).shift(1)


def zk(u, k, sdw=60):
    return u.rolling(k, min_periods=k).sum() / (u.rolling(sdw, min_periods=40).std() * np.sqrt(k))


r = SR[['TRMET', 'TRALT', 'TRENJ', 'XU030']].dropna(how='all')
grp = r[['TRALT', 'TRENJ']].mean(axis=1, skipna=False)
b_g = beta(r.TRMET, grp).clip(0.2, 2.0)
u = r.TRMET - b_g * grp
bTA = beta(r.TRMET, r.TRALT).clip(0.3, 2.0)
z3 = zk(u, 3)
FM, FA = C.fut('TRMET'), C.fut('TRALT')


def run(z, thr, h, e, src='cache', bb_ser=bTA, legs=('TRMET', 'TRALT')):
    zz = z.reindex(cal); on = (zz.abs() > thr).fillna(False).values
    d = cal[on]; sd = np.sign(zz.loc[d].values); bb = bb_ser.reindex(d).fillna(1.0).values
    if src == 'cache':
        a = FW[f'{legs[0]}|{h}|{e}'].reindex(d).values; b = FW[f'{legs[1]}|{h}|{e}'].reindex(d).values
    else:
        a = C.fut(legs[0]).fwd(d, h, e); b = C.fut(legs[1]).fwd(d, h, e)
    x = sd * (a - bb * b) / (1 + bb)
    return d, sd, x, C.summary(d, x, h)


print('Veri: VİOP paneli', cal.min().date(), '→', cal.max().date(), '| spot son', r.index.max().date())
print('Son β_g', round(float(b_g.dropna().iloc[-1]), 3), 'son β_TA', round(float(bTA.dropna().iloc[-1]), 3),
      'σ60(u) bps', round(float(u.rolling(60, min_periods=40).std().iloc[-1] * 1e4), 1))
for src in ['cache', 'fut']:
    for e in ['E0', 'E1', 'E2']:
        for h in [1, 2, 3]:
            d, sd, x, o = run(z3, 1.5, h, e, src)
            print(f'[{src}] ANA k3 |z|>1,5 {e} h{h}: n={o["n"]} brüt {o["gross"]:+.1f} t {o["t"]:.2f} isabet {o["hit"]:.2f} '
                  f'IS {o["IS"]:+.1f} OOS {o["OOS"]:+.1f} 2024-26 {o["2024-26"]:+.1f} (t {o["2024-26_t"]:.2f}) top10 hariç {o["ex_top10"]:+.1f} (t {o["ex_top10_t"]:.2f})')
# TERS (TRALT artığı; TRALT1! − β·TRMET1!)
grp2 = r[['TRMET', 'TRENJ']].mean(axis=1, skipna=False)
uA = r.TRALT - beta(r.TRALT, grp2).clip(0.2, 2.0) * grp2
bAT = beta(r.TRALT, r.TRMET).clip(0.3, 2.0)
for e in ['E0', 'E2']:
    for h in [1, 2, 3]:
        d, sd, x, o = run(zk(uA, 3), 1.5, h, e, 'cache', bb_ser=bAT, legs=('TRALT', 'TRMET'))
        print(f'TERS k3 |z|>1,5 {e} h{h}: n={o["n"]} brüt {o["gross"]:+.1f} t {o["t"]:.2f} 2024-26 {o["2024-26"]:+.1f} (t {o["2024-26_t"]:.2f})')
# bağımsız olay sayısı
d, sd, x, o = run(z3, 1.5, 2, 'E0')
T = pd.DataFrame({'date': d, 'x': x}).dropna()
pos = cal.get_indexer(pd.DatetimeIndex(T.date)); newev = np.r_[True, np.diff(pos) > 3]
print('Sinyal günü', len(T), '| bağımsız olay (3 günden uzak)', int(newev.sum()))
# z3 serisini sakla (sinyal betiğinin karşılaştırması için)
pd.DataFrame({'u': u, 'b_g': b_g, 'bTA': bTA, 'z3': z3}).to_parquet(
    '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/dl_rehber_koza/z3_arastirma.parquet')
