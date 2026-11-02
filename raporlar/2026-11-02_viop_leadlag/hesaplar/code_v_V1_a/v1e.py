"""Yerel plasebo (±3..8 hafta), uzun ön-trend (pre20) kontrolü, bağımsız veri: TUR ETF (ABD, USD)."""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_V1_a')
from v1 import *
rat = EV[EV.kind == 'rating'].copy()
for sym in ['XU100.IS', 'XBANK.IS']:
    for entry in ['open', 'close0']:
        act = np.mean([-e.dir * trade(sym, int(e.react_i), entry, 2) for _, e in rat.iterrows()])
        pl = []
        for w in [-8, -7, -6, -5, -4, -3, 3, 4, 5, 6, 7, 8]:
            v = [ -e.dir * trade(sym, CAL.searchsorted(e.react + pd.Timedelta(weeks=w)), entry, 2) for _, e in rat.iterrows()]
            pl.append(np.nanmean(v))
        pl = np.array(pl)
        print(f'yerel plasebo ±3..8 hafta {sym} {entry}: gerçek {1e4*act:.0f} | plasebo {np.round(1e4*pl).astype(int).tolist()} | max {1e4*pl.max():.0f}')
# pre20 kontrolü
xu = DLY['XU100.IS']; c = xu['c'].values; o = xu['o'].values
tb = pd.DataFrame({'react': rat.react.values, 'dir': rat.dir.values, 'i': rat.react_i.values})
tb['pre20'] = [np.log(c[i - 1] / c[i - 21]) for i in tb.i]
tb['strat'] = [-d * np.log(c[i + 2] / o[i]) for d, i in zip(tb.dir, tb.i)]
print('pre20 not yönünde (signed):', summarize(tb.dir * tb.pre20, 0))
X = np.c_[np.ones(len(tb)), -tb.dir * tb.pre20]; y = tb.strat.values
b = np.linalg.lstsq(X, y, rcond=None)[0]; r = y - X @ b; s2 = r @ r / (len(y) - 2); se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
print('strat = a + b*(-dir*pre20): a=%.0f bps (t %.2f), b=%.3f (t %.2f)' % (1e4 * b[0], b[0] / se[0], b[1], b[1] / se[1]))
i_all = np.arange(21, len(CAL) - 2); m = (CAL[i_all] >= '2014-01-01') & (CAL[i_all].dayofweek == 0)
pre20 = np.log(c[i_all - 1] / c[i_all - 21])[m]; fwd = np.log(c[i_all + 2] / o[i_all])[m]
bg = np.polyfit(-pre20, fwd, 1)[0]
print('tüm Pazartesiler fwd ~ -pre20 eğimi: %.3f -> olaylarda beklenen katkı %.0f bps' % (bg, 1e4 * bg * (tb.dir * tb.pre20).mean()))
# TUR ETF (iShares MSCI Turkey, NYSE/Cboe, USD) : Pazartesi ABD açılışı (13:30/14:30 UTC) -> Çarşamba ABD kapanışı
def ld(sym):
    d = pd.read_parquet(f'{D}/daily/{sym}.parquet'); d.index = pd.DatetimeIndex(pd.to_datetime(d['ldate'].astype(str))).normalize()
    return d[~d.index.duplicated(keep='last')].sort_index()
for sym in ['TUR']:
    d = ld(sym); cal = d.index
    out = {}
    for _, e in rat.iterrows():
        p = cal.searchsorted(e.ann, side='right')  # ilk ABD seansı > açıklama günü
        if p + 2 >= len(cal): continue
        r_open = np.log(d['c'].iloc[p + 2] / d['o'].iloc[p]); r_close = np.log(d['c'].iloc[p + 2] / d['c'].iloc[p])
        out[cal[p]] = (-e.dir * r_open, -e.dir * r_close, (cal[p] - e.ann).days)
    O = pd.DataFrame(out, index=['open_t2', 'close0_t2', 'gun']).T
    print(sym, 'açılış->t+2:', summarize(O.open_t2, 15), '| IS', summarize(O.open_t2[O.index < '2021'], 15)['mean_bps'], 'OOS', summarize(O.open_t2[O.index >= '2021'], 15)['mean_bps'])
    print(sym, 'kapanış0->t+2:', summarize(O.close0_t2, 15))
