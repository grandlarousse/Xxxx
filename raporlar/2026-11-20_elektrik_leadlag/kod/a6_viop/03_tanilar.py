"""Tanılar (yalnız IS): (a) kontrol regresyonları, (b) koşullu alt kümeler (keşif), (c) aile içi en yüksek t için yer değiştirme testi.
Çıktı: kod/a6_viop/_tanilar.txt"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from common import elib
import rules

P = elib.load(sys.argv[1])
idx = P['ret_cc'].index
trio = rules.trio_cols(P)
out = []


def pr(*a):
    s = ' '.join(str(x) for x in a); print(s); out.append(s)


def cl_ols(y, X, g):
    """Havuzlanmış OLS, tarihe göre kümelenmiş standart hata."""
    X = np.column_stack([np.ones(len(y))] + [X[c].values for c in X.columns]); yv = y.values
    b = np.linalg.lstsq(X, yv, rcond=None)[0]; u = yv - X @ b
    XtXi = np.linalg.inv(X.T @ X); S = np.zeros((X.shape[1],) * 2)
    for _, ii in pd.Series(np.arange(len(g))).groupby(g.values):
        s = X[ii.values].T @ u[ii.values]; S += np.outer(s, s)
    se = np.sqrt(np.diag(XtXi @ S @ XtXi))
    return b[1:], (b / se)[1:]


def stack(d):
    return pd.concat({k: v[trio].stack(future_stack=True) for k, v in d.items()}, axis=1)


xu = P['idx_ret']['XU100'].reindex(idx)
rz = rules.zlag(P['ret_cc'][trio], 60, 40)
svol = rules.spike(P['vol_tl'][trio])
G = {r['ad']: r for r in rules.grid(P)}
pr('== (a) kontrol regresyonları: fazla getiri (own, dolabilir) ~ sinyal + hedefin kendi r(t) + XU100 r(t) [+ ek]; t tarihe kümeli')
for ad, ek in [('V4_getiri_z1.0_yuk_spotAL_h2', None), ('V4_getiri_z1.0_yuk_spotAL_h3', None), ('V1_settle_z1.0_yuk_spotAL_h3', None),
               ('V1_settle_z1.5_yuk_spotAL_h2', None), ('V2_hacim_yuk_spotAL_h3', 'spot_hacim_sicrama')]:
    r = G[ad]; M, fl = elib.excess_measures(P, r['h'], 'long', trio)
    d = {'y': M['own'].where(fl), 'sinyal': r['sig'].astype(float), 'kendi_r': P['ret_cc'][trio],
         'xu100_r': pd.DataFrame({c: xu for c in trio})}
    if ek:
        d[ek] = svol.astype(float)
    S = stack(d).dropna()
    first = r['sig'].any(axis=1).idxmax(); S = S[S.index.get_level_values(0) >= first]
    b, t = cl_ols(S['y'], S.drop(columns='y'), pd.Series(S.index.get_level_values(0)))
    pr(f'{ad}: n={len(S)} ' + ' | '.join(f'{c}: {1e4 * bb if c in ("sinyal", ek) else bb:.2f} (t={tt:.2f})' for c, bb, tt in zip(S.columns[1:], b, t)))

pr('== (b) koşullu alt kümeler (KEŞİF; elib.evaluate, own, dolabilir): sinyal & hedefin kendi getirisi z<1 / z≥1')
nk = 0
for ad in ['V4_getiri_z1.0_yuk_spotAL_h2', 'V1_settle_z1.0_yuk_spotAL_h3', 'V2_hacim_yuk_spotAL_h3']:
    r = G[ad]
    for lab, m in [('kendi z<1', ~(rz >= 1)), ('kendi z≥1', rz >= 1), ('XU100 r(t)≤0', pd.DataFrame({c: xu <= 0 for c in trio})), ('XU100 r(t)>0', pd.DataFrame({c: xu > 0 for c in trio}))]:
        row = elib.evaluate(r['sig'] & m.fillna(False), P, h=r['h'], side='long', measure='own', name=ad + ' & ' + lab, family='kesif'); nk += 1
        pr(f"{row['sinyal_tanimi']}: n_bag={row['n_bagimsiz_IS']} fazla={row['ort_fazla_IS_bps']:.0f} bps t={row['t_IS']:.2f} net={row['net_temel_bps_IS']:.0f} mkt={row['dol_mkt_IS_bps']:.0f}")
# kaynak ayrımı (V4): ENJSA vadelisi kaynak vs ODAS vadelisi kaynak
z = rules.zlag(rules.front_wide(P, 'ret_settle', trio), 60, 40)
for src in trio:
    hit = (z[src] >= 1).fillna(False)
    sig = pd.DataFrame({c: (hit if c != src else False) for c in trio}, index=idx)
    for h in [2]:
        row = elib.evaluate(sig, P, h=h, side='long', measure='own', name=f'kaynak {src} vadelisi z≥1 → diğer ikisi spot AL h{h}', family='kesif'); nk += 1
        pr(f"{row['sinyal_tanimi']}: n_bag={row['n_bagimsiz_IS']} fazla={row['ort_fazla_IS_bps']:.0f} t={row['t_IS']:.2f} net={row['net_temel_bps_IS']:.0f} yıllar {row['yillar_bps']}")
# aynı kural spot getirisiyle kurulsa (vadeli bilgisi katkısı var mı?)
zs = rz
out_sig = pd.DataFrame(False, index=idx, columns=trio)
for c in trio:
    out_sig[c] = (zs[[o for o in trio if o != c]] >= 1).any(axis=1)
vstart = {c: pd.Timestamp(elib.VIOP_START[c]) for c in trio}
row = elib.evaluate(out_sig & (pd.DataFrame({c: idx >= pd.Timestamp('2019-03-01') for c in trio}, index=idx)), P, h=2, side='long', measure='own', name='(spot getirisiyle) diğer ikisinden biri z≥1 → hedef spot AL h2, 2019-03+', family='kesif'); nk += 1
pr(f"{row['sinyal_tanimi']}: n_bag={row['n_bagimsiz_IS']} fazla={row['ort_fazla_IS_bps']:.0f} t={row['t_IS']:.2f} net={row['net_temel_bps_IS']:.0f} yıllar {row['yillar_bps']}")
row = elib.evaluate(out_sig & (pd.DataFrame({c: idx < pd.Timestamp('2019-03-01') for c in trio}, index=idx)), P, h=2, side='long', measure='own', name='(spot getirisiyle) aynı kural, 2019-03 ÖNCESİ (vadeli yokken)', family='kesif'); nk += 1
pr(f"{row['sinyal_tanimi']}: n_bag={row['n_bagimsiz_IS']} fazla={row['ort_fazla_IS_bps']:.0f} t={row['t_IS']:.2f} net={row['net_temel_bps_IS']:.0f} yıllar {row['yillar_bps']}")
pr(f'keşif testi sayısı: {nk}')

pr('== (c) aile içi en yüksek t: dairesel kaydırma (her kural kendi etkin penceresinde, ortak oran u; 300 tekrar; basit t, viop için iki fiyatın kötüsü)')
items = []
for r in rules.grid(P):
    cols = [c for c in r['sig'].columns if c in P['ret_cc'].columns]
    if r['arac'] == 'viop':
        cols = [c for c in cols if c in elib.VIOP]
    S = r['sig'][cols].reindex(idx).fillna(False).values
    if not S.any():
        continue
    a = int(np.argmax(S.any(axis=1)))
    Fs = []
    if r['arac'] == 'spot':
        M, fl = elib.excess_measures(P, r['h'], r['yon'], cols)
        Fs.append(M['own'].where(fl).values[a:])
    else:
        sgn = 1.0 if r['yon'] == 'long' else -1.0
        vol = elib.viop_volume(P)[cols]
        for kind in ['settle', 'last']:
            rr = elib.viop_returns(P, kind)[cols]; L = elib.level(rr); f = L.shift(-r['h']) / L - 1
            own = (f - elib.bench_own(f, r['h'])) * sgn
            fill = (vol > 0) & rr.notna() & ~(rr.abs() >= 0.095) & (P['fill_long'] if r['yon'] == 'long' else P['fill_short'])[cols]
            Fs.append(own.where(fill).values[a:])
    items.append((r['ad'], S[a:], Fs, r.get('min_n', 1)))


def tstat(S, Fs, min_n):
    ts = []
    for F in Fs:
        X = np.where(S, F, np.nan)
        n = np.sum(np.isfinite(X), axis=1)
        with np.errstate(invalid='ignore'):
            p = np.nansum(X, axis=1) / np.where(n >= max(min_n, 1), n, np.nan)
        p = p[np.isfinite(p)]
        ts.append(p.mean() / (p.std(ddof=1) / np.sqrt(len(p))) if len(p) >= 15 else np.nan)
    return np.nanmin(ts) if np.isfinite(ts).any() else np.nan


import warnings; warnings.simplefilter('ignore')
real = np.array([tstat(S, Fs, m) for _, S, Fs, m in items])
rng = np.random.default_rng(0); null_max = []
for _ in range(300):
    u = rng.uniform(0.05, 0.95)
    tt = [tstat(np.roll(S, int(round(u * len(S))), axis=0), Fs, m) for _, S, Fs, m in items]
    null_max.append(np.nanmax(tt))
null_max = np.array(null_max)
i = int(np.nanargmax(real))
pr(f'gerçek en yüksek basit t = {real[i]:.2f} ({items[i][0]}); sıfır dağılımında en yüksek t: medyan {np.median(null_max):.2f}, %90 {np.quantile(null_max, .9):.2f}, %95 {np.quantile(null_max, .95):.2f}')
pr(f'aile düzeyi p (en yüksek t ≥ gerçek) = {(np.sum(null_max >= real[i]) + 1) / (len(null_max) + 1):.3f}; test sayısı {len(items)}; t>2 olan gerçek kural sayısı {int(np.nansum(real > 2))}, sıfır dağılımında ortalama {np.mean([0]):.0f}')
for ad in ['V4_getiri_z1.0_yuk_spotAL_h2', 'V4_getiri_z1.0_yuk_spotAL_h3', 'V1_settle_z1.5_yuk_spotAL_h2', 'V1_settle_z1.0_yuk_spotAL_h3', 'V2_hacim_yuk_spotAL_h3']:
    j = [k for k, it in enumerate(items) if it[0] == ad][0]
    pr(f'  {ad}: basit t={real[j]:.2f}; aile-düzeyi düzeltilmiş p={(np.sum(null_max >= real[j]) + 1) / (len(null_max) + 1):.3f}')
    rl, pv, _ = elib.shift_null(G[ad]['sig'], P, h=G[ad]['h'], side='long', measure='own', n=300, seed=1, start=idx[int(np.argmax(G[ad]['sig'].any(axis=1).values))])
    pr(f'     elib.shift_null (tek kural, etkin pencere): ortalama {rl:.0f} bps, p={pv:.3f}')
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_tanilar.txt'), 'w').write('\n'.join(out) + '\n')
