"""v10: veri madenciliği — 72 spesifikasyon yüzeyi (eşik 0/0,5/1/1,5/2/3% x sinyal raw/idio(sepet) x bacak both/up/down x getiri ham/sepet-hedge)
ve dairesel kaydırma nulli altında max-t (White reality check benzeri), 200 tekrar."""
import numpy as np, pandas as pd, vb, itertools
rng = np.random.default_rng(11)
fr = pd.read_pickle('res/panel.pkl'); S = vb.S47
G = vb.wide(fr, 'gap')['2014':]; I = vb.wide(fr, 'intra')['2014':]
G.pop('XU030'); I.pop('XU030'); G, I = G[S], I[S]
B = pd.read_pickle('res/basket.pkl'); gbl, ibl = B['gbl'].reindex(G.index), B['ibl'].reindex(G.index)
sigs = {'raw': G.values, 'idio': (G - gbl).values}
rets = {'unh': I.values * 1e4, 'hedB': (I - ibl).values * 1e4}
oos = (G.index >= '2021-01-01'); N = len(G)
thrs = [0, 0.005, 0.01, 0.015, 0.02, 0.03]
specs = list(itertools.product(thrs, ['raw', 'idio'], ['both', 'up', 'down'], ['unh', 'hedB']))
def evalall(sg_shift=None):
    out = []
    cache = {}
    for thr, sn, leg, rn in specs:
        g = sigs[sn] if sg_shift is None else sg_shift[sn]
        with np.errstate(invalid='ignore'):
            s = -np.sign(g) * (np.abs(g) > thr)
            if leg == 'up': s = s * (g > 0)
            if leg == 'down': s = s * (g < 0)
            s = np.where((s == 0) | np.isnan(g), np.nan, s)
            r = s * rets[rn]
            cnt = np.sum(~np.isnan(r), axis=1)
            d = np.where(cnt > 0, np.nansum(r, axis=1) / np.maximum(cnt, 1), np.nan)
        res = []
        for msk in [~oos, oos]:
            x = d[msk]; x = x[~np.isnan(x)]
            res += [x.mean(), x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))]
        out.append(res)
    return np.array(out)
A = evalall()
T = pd.DataFrame(A, columns=['IS', 'tIS', 'OOS', 'tOOS'], index=pd.MultiIndex.from_tuples(specs, names=['thr', 'sig', 'leg', 'ret']))
T.round(2).to_csv('res/v10_surface.csv')
pd.set_option('display.width', 220); pd.set_option('display.max_rows', 100)
print(T.round(1).unstack('thr')['OOS'])
print(T.round(2).unstack('thr')['tOOS'])
print(T.round(1).unstack('thr')['IS'])
print('OOS t>2 olan spec sayısı', int((T.tOOS > 2).sum()), '/', len(T), '; IS t>2', int((T.tIS > 2).sum()))
print('IS ve OOS ikisinde t>2:', int(((T.tIS > 2) & (T.tOOS > 2)).sum()))
# null
Gv = {k: v for k, v in sigs.items()}
mx_oos, mx_is, mh_oos, mh_is = [], [], [], []
hed = np.array([r == 'hedB' for (_, _, _, r) in specs])
for it in range(200):
    offs = rng.integers(21, N - 21, size=len(S))
    sh = {k: np.column_stack([np.roll(v[:, j], offs[j]) for j in range(len(S))]) for k, v in Gv.items()}
    Z = evalall(sh)
    mx_is.append(np.nanmax(Z[:, 1])); mx_oos.append(np.nanmax(Z[:, 3])); mh_is.append(np.nanmax(Z[hed, 1])); mh_oos.append(np.nanmax(Z[hed, 3]))
mx_is, mx_oos, mh_is, mh_oos = map(np.array, [mx_is, mx_oos, mh_is, mh_oos])
print('null max-t (72 spec) IS: medyan %.2f p95 %.2f | OOS: medyan %.2f p95 %.2f' % (np.median(mx_is), np.quantile(mx_is, .95), np.median(mx_oos), np.quantile(mx_oos, .95)))
print('null max-t (yalnız 36 sepet-hedge spec) IS: medyan %.2f p95 %.2f | OOS: medyan %.2f p95 %.2f' % (np.median(mh_is), np.quantile(mh_is, .95), np.median(mh_oos), np.quantile(mh_oos, .95)))
for key in [(0.01, 'raw', 'both', 'unh'), (0.01, 'raw', 'both', 'hedB'), (0.01, 'idio', 'up', 'hedB'), (0.01, 'idio', 'both', 'hedB')]:
    hl = T.loc[key]
    print(key, 'tIS %.2f tOOS %.2f | p(72 max) IS %.3f OOS %.3f | p(36 hedge max) IS %.3f OOS %.3f' % (hl.tIS, hl.tOOS, (mx_is >= hl.tIS).mean(), (mx_oos >= hl.tOOS).mean(), (mh_is >= hl.tIS).mean(), (mh_oos >= hl.tOOS).mean()))
