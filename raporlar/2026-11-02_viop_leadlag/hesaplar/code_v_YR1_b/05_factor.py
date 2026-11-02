"""Ortak faktör: SAHOL/AKBNK pnl'ini benzer kurallı faktör stratejileri + kesitsel kısa vade dönüş faktörü + piyasa üzerinde regres et (NW alfa).
Bacak ayrıştırması ve sapmanın kaynağı (SAHOL mu AKBNK mı hareket etti)."""
import vb, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
def strat(a, b, cost=8, win=60, thr=1.5):
    P = vb.pair_inputs(a, b); z = vb.zscore(P['S'], win); pos = vb.positions(z, thr)
    return vb.pnl_open(pos, P['A']['gap'], P['A']['intra'], P['B']['gap'], P['B']['intra'], P['beta'], cost), pos, P
base, pos, P = strat('SAHOL', 'AKBNK')
y = base['net']
F = {}
for a, b in [('SAHOL', 'XU030'), ('AKBNK', 'XBANK'), ('XBANK', 'XU030'), ('SAHOL', 'XBANK'), ('SAHOL', 'GARAN'), ('SAHOL', 'YKBNK'), ('KCHOL', 'AKBNK'), ('GARAN', 'AKBNK'), ('KCHOL', 'XU030')]:
    d, _, _ = strat(a, b); F[f'{a}/{b}'] = d['net']; tb = vb.table(d)
    print(f'{a}/{b}: IS t {tb.loc["IS", "t"]:.2f}  OOS t {tb.loc["OOS", "t"]:.2f}  corr(pnl, SAHOL/AKBNK) {d["net"][d.index >= "2014"].corr(y[y.index >= "2014"]):.2f}')
# kesitsel kısa vade dönüş faktörü (47 hisse, 5g XU100 artık getirisi, alt-üst beşte birlik, t+1 açılış, günlük yeniden dengeleme)
U = 'AEFES AKBNK AKSEN ALARK ARCLK ASELS BIMAS BRSAN CIMSA DOAS DOHOL EKGYO ENJSA ENKAI EREGL FROTO GARAN GUBRF HALKB HEKTS ISCTR KCHOL KRDMD MGROS ODAS OYAKC PETKM PGSUS SAHOL SASA SISE SOKM TAVHL TCELL THYAO TKFEN TOASO TRALT TRMET TSKB TTKOM TUPRS ULKER VAKBN VESTL YKBNK'.split()
idx = vb.cal()
C = pd.DataFrame({s: vb.load(s)['cc'] for s in U}).reindex(idx); G = pd.DataFrame({s: vb.load(s)['gap'] for s in U}).reindex(idx); I = pd.DataFrame({s: vb.load(s)['intra'] for s in U}).reindex(idx)
m = vb.load('XU100')['cc'].reindex(idx)
bm = C.rolling(250, min_periods=120).cov(m).div(m.rolling(250, min_periods=120).var(), axis=0).shift(1)
res = C - bm.mul(m, axis=0); r5 = res.rolling(5).sum()
rk = r5.rank(axis=1, pct=True); w = (rk <= 0.2).astype(float) - (rk >= 0.8).astype(float); w = w.div(w.abs().sum(axis=1) / 2, axis=0).fillna(0)
rev = (w.shift(2) * (G - bm.mul(vb.load('XU100')['gap'].reindex(idx), axis=0)).fillna(0)).sum(axis=1) + (w.shift(1) * (I - bm.mul(vb.load('XU100')['intra'].reindex(idx), axis=0)).fillna(0)).sum(axis=1)
F['REV5_xs'] = rev
F['XU100'] = m; F['absXU100'] = m.abs()
X = pd.DataFrame(F).reindex(y.index)
def ols_nw(yv, Xv, lags=5):
    Xc = np.column_stack([np.ones(len(Xv)), Xv]); b = np.linalg.lstsq(Xc, yv, rcond=None)[0]; e = yv - Xc @ b
    n = len(yv); XtXi = np.linalg.inv(Xc.T @ Xc); S = (Xc * e[:, None]).T @ (Xc * e[:, None]) / n
    for L in range(1, lags + 1):
        G_ = (Xc[L:] * e[L:, None]).T @ (Xc[:-L] * e[:-L, None]) / n; S += (1 - L / (lags + 1)) * (G_ + G_.T)
    V = n * XtXi @ S @ XtXi; return b, b / np.sqrt(np.diag(V))
for lab, lo, hi in [('IS', '2014', '2021'), ('OOS', '2021', '2027'), ('ALL', '2014', '2027')]:
    mm = (y.index >= lo) & (y.index < hi)
    Z = X[mm].fillna(0).copy(); Z['absXU100'] -= Z['absXU100'].mean(); yy = y[mm].fillna(0)
    b, t = ols_nw(yy.values, Z.values)
    print(f'{lab} [SAHOL/banka varyantları DAHİL]: alfa {1e4 * b[0]:.2f} bps/gün (tüm günler) t {t[0]:.2f}; ham ort {1e4 * yy.mean():.2f} t {vb.nw_t(yy)[1]:.2f}')
    print('   katsayı t:', dict(zip(Z.columns, np.round(t[1:], 2))))
# Bacak ayrıştırması (piyasa-hedge'li): SAHOL - bA*XU030 ve -(β)(AKBNK - bB*XU030), +market kalıntısı
A, B, beta = P['A'], P['B'], P['beta']; Xu = vb.load('XU030').reindex(idx)
bA = A['cc'].rolling(250, min_periods=120).cov(Xu['cc']) / Xu['cc'].rolling(250, min_periods=120).var(); bA = bA.shift(1)
bB = B['cc'].rolling(250, min_periods=120).cov(Xu['cc']) / Xu['cc'].rolling(250, min_periods=120).var(); bB = bB.shift(1)
Pg = pos.shift(2).fillna(0); Pi = pos.shift(1).fillna(0); bi = beta.shift(1)
legA = Pg * (A['gap'] - bA * Xu['gap']).fillna(0) + Pi * (A['intra'] - bA * Xu['intra']).fillna(0)
legB = -(Pg * bi * (B['gap'] - bB * Xu['gap']).fillna(0) + Pi * bi * (B['intra'] - bB * Xu['intra']).fillna(0))
mkt = Pg * ((bA - bi * bB) * Xu['gap']).fillna(0) + Pi * ((bA - bi * bB) * Xu['intra']).fillna(0)
ex = base['exp']
for lab, lo, hi in [('IS', '2014', '2021'), ('OOS', '2021', '2027')]:
    mm = (idx >= lo) & (idx < hi)
    print(lab, 'brüt bps/maruz gün: SAHOL bacağı', round(1e4 * legA[mm & ex].mean(), 1), '(t', round(vb.nw_t(legA[mm])[1], 2), ') AKBNK bacağı', round(1e4 * legB[mm & ex].mean(), 1), '(t', round(vb.nw_t(legB[mm])[1], 2), ') piyasa kalıntısı', round(1e4 * mkt[mm & ex].mean(), 1))
# Sapmanın kaynağı: giriş öncesi 10 gün SAHOL ve AKBNK piyasa artık getirisi
eA = (A['cc'] - bA * Xu['cc']).rolling(10).sum(); eB = (B['cc'] - bB * Xu['cc']).rolling(10).sum() * beta
T = vb.trades(base[base.index >= '2014-01-01'])
dec = pos.index  # karar günü = giriş günü - 1
T['dec'] = [pos.index[pos.index.get_loc(e) - 1] for e in T.entry]
T['eA'] = eA.reindex(T['dec']).values; T['eB'] = eB.reindex(T['dec']).values
T['src'] = np.where(T.eA.abs() > T.eB.abs(), 'SAHOL hareketi', 'AKBNK hareketi')
T['per'] = np.where(pd.DatetimeIndex(T.entry) < '2021', 'IS', 'OOS')
print(T.groupby(['per', 'src']).net.agg(['count', 'mean', lambda s: s.mean() / s.std() * np.sqrt(len(s))]).assign(mean=lambda d: (1e4 * d['mean']).round(1)).round(2).to_string())
print('\n--- yalnız GENEL faktörler (SAHOL/banka varyantları hariç) ---')
gen = ['SAHOL/XU030', 'AKBNK/XBANK', 'XBANK/XU030', 'KCHOL/XU030', 'REV5_xs', 'XU100', 'absXU100']
for lab, lo, hi in [('IS', '2014', '2021'), ('OOS', '2021', '2027'), ('ALL', '2014', '2027')]:
    mm = (y.index >= lo) & (y.index < hi); Z = X[gen][mm].fillna(0); yy = y[mm].fillna(0)
    b, t = ols_nw(yy.values, Z.values)
    print(f'{lab}: alfa {1e4 * b[0]:.2f} bps/gün t {t[0]:.2f} (ham {1e4 * yy.mean():.2f}, t {vb.nw_t(yy)[1]:.2f}); katsayı t', dict(zip(gen, np.round(t[1:], 2))))
print('\n--- genel faktörler; |XU100| (işlenemeyen kontrol) demean edildi; her faktörün kendi ort. katkısı ---')
for lab, lo, hi in [('IS', '2014', '2021'), ('OOS', '2021', '2027'), ('ALL', '2014', '2027')]:
    mm = (y.index >= lo) & (y.index < hi); Z = X[gen][mm].fillna(0).copy(); Z['absXU100'] -= Z['absXU100'].mean(); yy = y[mm].fillna(0)
    b, t = ols_nw(yy.values, Z.values)
    contrib = {k: round(1e4 * bb * Z[k].mean(), 2) for k, bb in zip(gen, b[1:])}
    print(f'{lab}: alfa {1e4 * b[0]:.2f} bps/gün t {t[0]:.2f} (ham {1e4 * yy.mean():.2f}); b:', dict(zip(gen, np.round(b[1:], 3))), ' ort katkı bps:', contrib)
