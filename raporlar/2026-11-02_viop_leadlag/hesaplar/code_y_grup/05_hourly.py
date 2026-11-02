"""Saatlik (h1) lead-lag: y_h ~ x_{h-1} + y_{h-1} + XU100_{h-1}; yalnız gün-içi barlar (günün ilk barı = gece gap'i hariç).
Bayat fiyat kontrolü: takipçinin sıfır hacimli bar oranı; ayrıca 'likit alt örneklem' (her iki barda da hacim>0)."""
from gx import *
H1 = SCR + '/data/h1/'
_h = {}
def hb(sym):
    s = S(sym)
    if s not in _h:
        d = pd.read_parquet(H1 + s + '.parquet'); d = d[d.index.minute.isin([30]) | ((d.index.hour == 15) & (d.index.minute == 0))]
        d = d[d['ldate'] <= LAST]
        r = np.log(d['c']).diff(); day = d['ldate']; first = day != day.shift(1)
        r[first] = np.nan; r[(r > np.log(1.105)) | (r < np.log(0.895))] = np.nan
        _h[s] = pd.DataFrame({'r': r, 'v': d['v'], 'day': day})
    return _h[s]
def hstats(x, y):
    X, Y, M = hb(x), hb(y), hb('XU100')
    df = pd.concat([Y['r'].rename('y'), X['r'].shift(1).rename('x1'), Y['r'].shift(1).rename('y1'), M['r'].shift(1).rename('m1'),
                    Y['v'].rename('vy'), Y['v'].shift(1).rename('vy1'), Y['day'].rename('d'), Y['day'].shift(1).rename('d1')], axis=1)
    df = df[df['d'] == df['d1']].dropna(subset=['y', 'x1', 'y1', 'm1'])
    o = {'x': x, 'y': y, 'n_h': len(df), 'zero_vol_y': float((df['vy'] <= 0).mean()), 'start_h': str(df.index.min())[:10] if len(df) else None}
    if len(df) < 500: return o
    r = nwreg(df['y'], df[['x1', 'y1', 'm1']], lags=8)
    o['h_b'] = r[0].params[1]; o['h_t'] = r[0].tvalues[1]
    sd = df[['y', 'x1']].std(); o['h_bstd'] = o['h_b'] * sd['x1'] / sd['y']
    L = df[(df['vy'] > 0) & (df['vy1'] > 0)]; r2 = nwreg(L['y'], L[['x1', 'y1', 'm1']], lags=8)
    o['h_t_liq'] = r2[0].tvalues[1] if r2 else np.nan
    # yarı örneklem istikrarı
    mid = df.index[len(df) // 2]
    for lab, sub in [('h1', df[df.index < mid]), ('h2', df[df.index >= mid])]:
        rr = nwreg(sub['y'], sub[['x1', 'y1', 'm1']], lags=8); o[f't_{lab}'] = rr[0].tvalues[1] if rr else np.nan
    # eşzamanlı saatlik korelasyon (XU100 kontrollü)
    df2 = pd.concat([Y['r'].rename('y'), X['r'].rename('x'), M['r'].rename('m')], axis=1).dropna()
    o['h_pc0'] = ll.partial_corr(df2['y'], df2['x'], [df2['m']])[0]
    return o
if __name__ == '__main__':
    import os
    pe = pd.read_csv(HERE + '/res_peers.csv')[['x', 'y']].drop_duplicates()
    todo = [(a, b, g) for a, b, g, t in PAIRS] + [(r.x, r.y, 'PEER') for r in pe.itertuples() if r.x < r.y]
    rows = []
    for a, b, g in todo:
        if not (os.path.exists(H1 + S(a) + '.parquet') and os.path.exists(H1 + S(b) + '.parquet')): continue
        for x, y, d in [(b, a, 'Y2A'), (a, b, 'A2Y')]:
            try:
                o = hstats(x, y); o.update(dict(ana=a, yavru=b, grup=g, yon=d)); rows.append(o)
            except Exception as e: print('ERR', x, y, e)
    D = pd.DataFrame(rows)
    rej, padj = ll.fdr(ll.t_to_p(D['h_t'].values)); D['fdr'] = rej
    D.to_csv(HERE + '/res_hourly.csv', index=False)
    pd.set_option('display.width', 250); pd.set_option('display.max_rows', 300)
    print(D[['ana','yavru','grup','yon','x','y','n_h','zero_vol_y','h_pc0','h_bstd','h_t','h_t_liq','t_h1','t_h2','fdr']].round(3).to_string())
    for g in ['grp', 'PEER']:
        v = D[(D.grup == 'PEER') == (g == 'PEER')]['h_t']; print(g, 'n', len(v), 'mean t', round(v.mean(), 2), '%t>2', round((v > 2).mean(), 3), '%t<-2', round((v < -2).mean(), 3))
