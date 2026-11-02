"""Plasebo: (a) sinyal-getiri dairesel kaydırma, (b) işlem bazında rastgele yön, (c) rastgele giriş tarihleri (aynı süre profili)."""
import vb, numpy as np, pandas as pd
rng = np.random.default_rng(7)
P = vb.pair_inputs('SAHOL', 'AKBNK'); A, B, beta = P['A'], P['B'], P['beta']
z = vb.zscore(P['S'], 60); pos = vb.positions(z, 1.5)
base = vb.table(vb.pnl_open(pos, A['gap'], A['intra'], B['gap'], B['intra'], beta, 8))
print('gerçek:', base.loc[['IS', 'OOS'], ['bps', 't']].round(2).to_dict())
idx = pos.index; m14 = idx >= '2010-01-01'
pz = pos[m14]; n = len(pz)
# (a) dairesel kaydırma: pozisyon serisini 250..n-250 gün kaydır
res = []
for _ in range(400):
    k = int(rng.integers(250, n - 250))
    ps = pd.Series(np.roll(pz.values, k), index=pz.index).reindex(idx).fillna(0)
    tb = vb.table(vb.pnl_open(ps, A['gap'], A['intra'], B['gap'], B['intra'], beta, 8)); res.append((tb.loc['IS', 't'], tb.loc['OOS', 't']))
R = pd.DataFrame(res, columns=['IS', 'OOS'])
print('(a) dairesel kaydırma, 400 çekiliş: ort', R.mean().round(2).to_dict(), 'sd', R.std().round(2).to_dict(), ' p(IS>=gerçek)', (R.IS >= base.loc['IS', 't']).mean(), ' p(OOS>=gerçek)', (R.OOS >= base.loc['OOS', 't']).mean(), ' p(ikisi)', ((R.IS >= base.loc['IS', 't']) & (R.OOS >= base.loc['OOS', 't'])).mean())
# (b) işlem bazında rastgele yön (aynı zamanlama)
blk = (pos != pos.shift()).cumsum()
res = []
for _ in range(400):
    sg = pd.Series(rng.choice([-1.0, 1.0], size=blk.max() + 1))
    ps = pos.abs() * sg.reindex(blk.values).values
    tb = vb.table(vb.pnl_open(pd.Series(ps, index=idx), A['gap'], A['intra'], B['gap'], B['intra'], beta, 8)); res.append((tb.loc['IS', 't'], tb.loc['OOS', 't']))
R = pd.DataFrame(res, columns=['IS', 'OOS'])
print('(b) rastgele yön, 400: ort', R.mean().round(2).to_dict(), 'sd', R.std().round(2).to_dict(), ' p(IS>=)', (R.IS >= base.loc['IS', 't']).mean(), ' p(OOS>=)', (R.OOS >= base.loc['OOS', 't']).mean())
# (c) rastgele giriş tarihleri: gerçek işlem sürelerini koru, rastgele yön, rastgele başlangıç (çakışmasız yaklaşık)
T = []
cur = 0
for i, v in enumerate(pos.values):
    if v != 0 and (i == 0 or v != pos.values[i - 1]): T.append([i, 1])
    elif v != 0: T[-1][1] += 1
durs = np.array([d for _, d in T]); N = len(idx); st0 = np.searchsorted(idx, pd.Timestamp('2014-01-01'))
res = []
for _ in range(300):
    ps = np.zeros(N)
    starts = np.sort(rng.integers(st0, N - 30, size=len(durs)))
    for s, d in zip(starts, rng.permutation(durs)): ps[s:s + d] = rng.choice([-1.0, 1.0])
    tb = vb.table(vb.pnl_open(pd.Series(ps, index=idx), A['gap'], A['intra'], B['gap'], B['intra'], beta, 8)); res.append((tb.loc['IS', 't'], tb.loc['OOS', 't']))
R = pd.DataFrame(res, columns=['IS', 'OOS'])
print('(c) rastgele tarih+yön, 300: ort', R.mean().round(2).to_dict(), 'sd', R.std().round(2).to_dict(), ' p(IS>=)', (R.IS >= base.loc['IS', 't']).mean(), ' p(OOS>=)', (R.OOS >= base.loc['OOS', 't']).mean())
