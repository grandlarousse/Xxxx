"""Ek denetimler: uzatma segmentleri 2024+, 2026 toplamı, betik replay() ile P0L uyumu, lead-lag (bağımsız OLS+NW)."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/denetim_koza/kod')
import bag, d2_bt as BT
SIG, D = bag.signal(upto='2026-11-03')
T, op = BT.simulate(SIG)
later = [(T.entry[k], v) for k, s in enumerate(T.segs) for v in s[1:]]
L = pd.DataFrame(later, columns=['entry', 'r'])
for a in ['2019', '2024']:
    x = L[L.entry >= a].r
    print(f'uzatma sonrası segmentler {a}+: ort {x.mean():+.1f} n {len(x)} t {BT.tt(x):.2f}')
y26 = T[T.entry >= '2026-01-01']
print(f'2026: n {len(y26)} brüt toplam {y26.gross.sum():+.0f} net15t toplam {y26.net15t.sum():+.0f} ort {y26.net15t.mean():+.1f}')
print('2026 işlemleri:\n', y26[['entry', 'exit', 'days', 'side', 'gross', 'net15t']].round(1).to_string(index=False))
# betik replay ile karşılaştırma (betik kendi verisiyle; S betik_sig.parquet)
sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/rehber/koza')
import sinyal_koza as K
S = pd.read_parquet('/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/denetim_koza/betik_sig.parquet')
Rb = pd.DataFrame({s: bag.rets(D[s], s) for s in ['TRMET', 'TRALT', 'TRENJ', 'XU030']})
idx, tr, pos = K.replay(S.dropna(subset=['z3', 'bH'], how='all'), Rb, ndays=400)
RP = pd.DataFrame([dict(entry=idx[p['i0']], exit=idx[p['out']], side=p['s']) for p in tr])
RP = RP[RP.entry >= RP.entry.iloc[0] + pd.Timedelta(days=30)]
m = RP.merge(T[['entry', 'exit', 'side']], on=['entry', 'exit', 'side'], how='outer', indicator=True)
m = m[m.entry >= RP.entry.min()]
print('betik replay (spot kilit vekili) vs P0L (VİOP kilit vekili), son ~400 gün:', m._merge.value_counts().to_dict())
print(m[m._merge != 'both'])
# lead-lag: y_t ~ c + x_{t-1..3} + y_{t-1..3} + XU_{t-1..3}; NW(5)
R = pd.DataFrame({s: bag.rets(D[s], s) for s in ['TRMET', 'TRALT', 'TRENJ', 'XU030']}).dropna(how='all')
def nw_ols(Y, X, L=5):
    b = np.linalg.lstsq(X, Y, rcond=None)[0]; e = Y - X @ b; n = len(Y)
    XtXi = np.linalg.inv(X.T @ X); S = (X * e[:, None]).T @ (X * e[:, None])
    for l in range(1, L + 1):
        w = 1 - l / (L + 1); G = (X[l:] * e[l:, None]).T @ (X[:-l] * e[:-l, None]); S += w * (G + G.T)
    V = XtXi @ S @ XtXi; return b, b / np.sqrt(np.diag(V))
for yv, xv in [('TRMET', 'TRALT'), ('TRALT', 'TRMET')]:
    for lab, a, b_ in [('2017–21', '2017', '2021-12-31'), ('2022–26', '2022', '2026-12-31'), ('2024–26', '2024', '2026-12-31')]:
        df = pd.DataFrame({'y': R[yv]})
        for k in (1, 2, 3):
            df[f'x{k}'] = R[xv].shift(k); df[f'y{k}'] = R[yv].shift(k); df[f'm{k}'] = R.XU030.shift(k)
        df = df.loc[a:b_].dropna()
        X = np.column_stack([np.ones(len(df))] + [df[c].values for c in ['x1', 'x2', 'x3', 'y1', 'y2', 'y3', 'm1', 'm2', 'm3']])
        bb, tt_ = nw_ols(df.y.values, X)
        print(f'{xv}(t−k) → {yv}(t) {lab}: n {len(df)} b1 {bb[1]:+.3f} (t {tt_[1]:+.2f}) b2 {bb[2]:+.3f} (t {tt_[2]:+.2f}) b3 {bb[3]:+.3f} (t {tt_[3]:+.2f}) | Σb {bb[1:4].sum():+.3f}')
