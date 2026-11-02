"""KCHOL NAV iskontosu: kendi NAV inşam (al-tut 2010 başlangıç, kaynak referans ağırlıkları = model girdisi), z250>1, KCHOL - β·XU030, t+1 açılış.
Alt dönemler, bayat sinyal, dairesel kaydırma / rastgele yön plasebosu, uç işlemler, kriz hariç, NAV varyantları."""
import vb, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore'); rng = np.random.default_rng(11)
W = {'TUPRS': .33, 'FROTO': .20, 'YKBNK': .24, 'ARCLK': .07, 'TOASO': .04, 'AYGAZ': .03, 'OTKAR': .02, 'TTRAK': .03}
idx = vb.cal(); idx = idx[idx >= '2010-01-01']
def nav_ret(W, start='2010-01-01', rebal=None):
    R = pd.DataFrame({k: vb.load(k)['cc'] for k in W}).reindex(idx); R = R[R.index >= start]
    w0 = pd.Series(W) / sum(W.values())
    if rebal is None:
        lvl = np.exp(R.fillna(0).cumsum()); val = lvl * w0
    else:  # yıllık yeniden dengeleme
        val = pd.DataFrame(index=R.index, columns=R.columns, dtype=float); cur = w0.copy()
        for y, g in R.groupby(R.index.year):
            l = np.exp(g.fillna(0).cumsum()); val.loc[g.index] = (l * cur).values; cur = w0.copy()
        val = val.astype(float)
    wt = val.shift(1).div(val.shift(1).sum(axis=1), axis=0).fillna(w0)
    if rebal is not None:
        first = ~R.index.year.to_series(index=R.index).duplicated(); wt.loc[first.values] = w0.values
    return (wt * R.fillna(0)).sum(axis=1).reindex(idx)
H = vb.load('KCHOL').reindex(idx); X = vb.load('XU030').reindex(idx)
bm = (H['cc'].rolling(250, min_periods=120).cov(X['cc']) / X['cc'].rolling(250, min_periods=120).var()).shift(1)
def run(navr, win=250, thr=1.0, cost=8, costX=None, lag=0, pos=None):
    D = (H['cc'] - navr).fillna(0).cumsum(); D[navr.isna()] = np.nan
    z = vb.zscore(D, win)
    if pos is None: pos = vb.positions(z, thr).shift(lag).fillna(0)
    Pg = pos.shift(2).fillna(0); Pi = pos.shift(1).fillna(0); b = bm.shift(1)
    sg = H['gap'] - b * X['gap']; si = H['intra'] - b * X['intra']
    gross = Pg * sg.fillna(0) + Pi * si.fillna(0)
    cx = cost if costX is None else costX
    tc = (cost / 2 + b.abs() * cx / 2) / 1e4 * (Pi - Pg).abs()
    return pd.DataFrame({'net': gross - tc, 'exp': (Pg != 0) | (Pi != 0), 'valid': sg.notna() | si.notna(), 'Pi': Pi, 'Pg': Pg}), pos, z
nav = nav_ret(W)
base, pos, z = run(nav)
print('KCHOL NAV z250>1, 8 bps:'); print(vb.table(base)[['n', 'bps', 't', 'frac']].round(2).T.to_string())
for c, cx in [(15, None), (30, None), (8, 3), (15, 3)]:
    print(f'maliyet KCHOL {c} / XU030 {cx or c}:', {k: (round(v['bps'], 1), round(v['t'], 2)) for k, v in vb.table(run(nav, cost=c, costX=cx)[0]).T.to_dict().items() if k in ['IS', 'OOS', '2021-23', '2024-26']})
e = base[base.exp & (base.index >= '2014')]; yr = 1e4 * e.net.groupby(e.index.year).mean(); print('yıllık:', yr.round(1).to_dict(), 'pozitif', int((yr > 0).sum()), '/', len(yr))
# bayat sinyal
print('bayat sinyal (gün, IS t, OOS t):', [(k, round(vb.table(run(nav, lag=k)[0]).loc['IS', 't'], 2), round(vb.table(run(nav, lag=k)[0]).loc['OOS', 't'], 2)) for k in [0, 1, 2, 5, 10, 20, 40]])
# plasebolar
bt_ = vb.table(base); real = (bt_.loc['IS', 't'], bt_.loc['OOS', 't'])
pz = pos.values; n = len(pz); rr = []
for _ in range(300):
    k = int(rng.integers(250, n - 250)); ps = pd.Series(np.roll(pz, k), index=pos.index)
    tb = vb.table(run(nav, pos=ps)[0]); rr.append((tb.loc['IS', 't'], tb.loc['OOS', 't']))
R = pd.DataFrame(rr, columns=['IS', 'OOS']); print('dairesel kaydırma 300: ort', R.mean().round(2).to_dict(), 'sd', R.std().round(2).to_dict(), ' p(OOS>=gerçek)', (R.OOS >= real[1]).mean().round(3), ' p(IS>=)', (R.IS >= real[0]).mean().round(3))
blk = (pos != pos.shift()).cumsum(); rr = []
for _ in range(300):
    sg = pd.Series(rng.choice([-1.0, 1.0], size=blk.max() + 1)); ps = pd.Series(pos.abs().values * sg.reindex(blk.values).values, index=pos.index)
    tb = vb.table(run(nav, pos=ps)[0]); rr.append((tb.loc['IS', 't'], tb.loc['OOS', 't']))
R = pd.DataFrame(rr, columns=['IS', 'OOS']); print('rastgele yön 300: ort', R.mean().round(2).to_dict(), 'sd', R.std().round(2).to_dict(), ' p(OOS>=gerçek)', (R.OOS >= real[1]).mean().round(3))
# uç işlemler
T = vb.trades(base[base.index >= '2014']); T['yr'] = pd.DatetimeIndex(T.entry).year
for lab, m in [('IS', T.yr < 2021), ('OOS', T.yr >= 2021)]:
    t = T[m].sort_values('net', ascending=False); tot = t.net.sum()
    print(lab, 'işlem', len(t), 'ort gün', round(t.ndays.mean(), 1), 'isabet', round((t.net > 0).mean(), 2), ' trade-t', round(t.net.mean() / t.net.std() * np.sqrt(len(t)), 2),
          ' en iyi 3 hariç trade-t', round(t.net.iloc[3:].mean() / t.net.iloc[3:].std() * np.sqrt(len(t) - 3), 2), ' en iyi 3 payı', round(t.net.iloc[:3].sum() / tot, 2))
CR = [('2018-08-01', '2018-09-30'), ('2020-03-01', '2020-04-30'), ('2021-11-15', '2022-01-31'), ('2023-02-06', '2023-03-15'), ('2023-05-01', '2023-06-30'), ('2025-03-17', '2025-04-30'), ('2026-09-01', '2026-10-31')]
d3 = base.copy(); m = pd.Series(False, index=d3.index)
for a, b in CR: m |= (d3.index >= a) & (d3.index <= b)
d3.loc[m, 'net'] = 0; d3.loc[m, 'exp'] = False; d3.loc[m, 'valid'] = False
print('kriz hariç:', {k: (round(v['bps'], 1), round(v['t'], 2)) for k, v in vb.table(d3).T.to_dict().items()})
# parametre / NAV varyantları
rows = []
for nm, nv in [('al-tut 2010', nav), ('al-tut 2014', nav_ret(W, '2014-01-01')), ('yıllık dengeleme', nav_ret(W, rebal='Y')), ('eşit ağırlık 8', nav_ret({k: 1 for k in W})),
               ('ilk 4 (TUPRS/FROTO/YKBNK/ARCLK)', nav_ret({k: W[k] for k in ['TUPRS', 'FROTO', 'YKBNK', 'ARCLK']}))]:
    for win in [120, 250, 500]:
        for thr in [0.75, 1.0, 1.5]:
            tb = vb.table(run(nv, win=win, thr=thr)[0]); rows.append(dict(nav=nm, win=win, thr=thr, IS_t=tb.loc['IS', 't'], OOS_t=tb.loc['OOS', 't'], t2123=tb.loc['2021-23', 't'], t2426=tb.loc['2024-26', 't'], OOS_bps=tb.loc['OOS', 'bps']))
V = pd.DataFrame(rows); V.to_csv('res_kchol_grid.csv', index=False)
print('NAV x pencere x eşik (45): OOS t medyan', V.OOS_t.median().round(2), ' %>2', (V.OOS_t > 2).mean().round(2), ' %>0', (V.OOS_t > 0).mean().round(2), ' IS t medyan', V.IS_t.median().round(2), ' %IS>2', (V.IS_t > 2).mean().round(2))
print(V.pivot_table(index='nav', columns='win', values='OOS_t', aggfunc='median').round(2).to_string())
print('alt dönem medyan t:', V[['t2123', 't2426']].median().round(2).to_dict())
# 10:30 giriş (2023-12+)
pK, pX = vb.p1030('KCHOL'), vb.p1030('XU030')
fK = H['adj'] / H['c']
q = np.log(pK.reindex(idx) * fK); qx = np.log(pX.reindex(idx))
gK = q - np.log(H['adj'].ffill()).shift(); iK = np.log(H['adj']) - q; gX = qx - np.log(X['c'].ffill()).shift(); iX = np.log(X['c']) - qx
Pg = pos.shift(2).fillna(0); Pi = pos.shift(1).fillna(0); b = bm.shift(1)
for nm, sg, si in [('açılış', H['gap'] - b * X['gap'], H['intra'] - b * X['intra']), ('10:30', gK - b * gX, iK - b * iX)]:
    msk = (idx >= '2023-12-01') & gK.notna() & gX.notna()
    gross = Pg * sg.fillna(0) + Pi * si.fillna(0); tc = 8 / 1e4 / 2 * (1 + b.abs()) * (Pi - Pg).abs()
    d = pd.DataFrame({'net': gross - tc, 'exp': (Pg != 0) | (Pi != 0), 'valid': True}, index=idx)[msk]
    print('2023-12+ giriş', nm, {k: round(v, 2) for k, v in vb.summ(d, '2023-12-01').items()})
