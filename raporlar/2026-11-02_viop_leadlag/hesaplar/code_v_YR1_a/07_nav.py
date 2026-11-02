"""YR1-B: KCHOL NAV iskontosu — bağımsız yeniden üretim + zamanlama + maliyet + alternatif NAV + plasebo."""
import sys; sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_YR1_a')
from vlib import *
W0 = {'TUPRS': .33, 'FROTO': .20, 'YKBNK': .24, 'ARCLK': .07, 'TOASO': .04, 'AYGAZ': .03, 'OTKAR': .02, 'TTRAK': .03}
cal = raw('XU100').index; cal = cal[cal >= pd.Timestamp('2010-01-01')]
K = dec('KCHOL').reindex(cal); X = dec('XU030').reindex(cal)
def nav_ret(W, start='2010-01-01', rebal=None):
    rr = pd.DataFrame({k: dec(k)['cc'].reindex(cal) for k in W}); rr = rr[rr.index >= pd.Timestamp(start)]
    w0 = pd.Series(W, dtype=float); w0 /= w0.sum()
    avail = rr.notna().cumsum() > 0
    if rebal is None:
        lvl = np.exp(rr.fillna(0).cumsum()); val = (lvl * w0).where(avail, 0.0)
        wt = val.shift(1).div(val.shift(1).sum(axis=1), axis=0)
    else:  # yıllık yeniden dengeleme (sabit ağırlık her yıl başı)
        grp = rr.index.year
        lvl = np.exp(rr.fillna(0).groupby(grp).cumsum()); val = (lvl * w0).where(avail, 0.0)
        wt = val.shift(1).div(val.shift(1).sum(axis=1), axis=0)
        first = pd.Series(grp, index=rr.index).diff().fillna(1) != 0
        wt.loc[first] = (w0 * avail.loc[first]).div((w0 * avail.loc[first]).sum(axis=1), axis=0)
    out = (wt * rr.fillna(0)).sum(axis=1); out[wt.sum(axis=1) == 0] = np.nan
    return out.reindex(cal)
bm = roll_beta(K['cc'], X['cc'])
tg, ti, tc = K['gap'] - bm * X['gap'], K['intra'] - bm * X['intra'], K['cc'] - bm * X['cc']
lw = 1 + bm.abs()
tick = 1e4 * (0.01 / K['px'])  # XU030 vadelisi tik maliyeti ihmal (0,025 puan / ~10.000+)
def signal(navr, win=250, thr=1.0, Dmode='raw'):
    d = (K['cc'] - navr)
    D = d.fillna(0).cumsum().where(navr.notna().cumsum() > 0)
    z = zscore(D, win); return positions(z, thr), z
def stat(sim, lo0='2014-01-01'):
    o = {}
    for per, lo, hi in [('IS', lo0, SPLIT), ('OOS', SPLIT, '2027-01-01'), ('23-26', '2023-01-01', '2027-01-01')]:
        st = summarize(sim, lo, hi); o[f'{per}_m'] = st['mean_bps']; o[f'{per}_t'] = st['t_all']; o[f'{per}_n'] = st['n_act']; o[f'{per}_sh'] = st['sharpe']; o[f'{per}_hold'] = st['hold_d']; o[f'{per}_in'] = st['pct_in']
    yb = by_year(sim[sim.index >= lo0]); o['yrs'] = f'{int((yb > 0).sum())}/{len(yb)}'; o['by_year'] = yb.to_dict()
    return o
if __name__ == '__main__':
    pd.set_option('display.width', 260); pd.set_option('display.max_rows', 300); pd.set_option('display.max_colwidth', 160)
    navr = nav_ret(W0); pos, z = signal(navr)
    rows = []
    sim0 = simulate(pos, tg, ti, tc, pd.Series(2.0, index=cal), 'open', 8)
    o = dict(lab='kaynak-taklit (aktif=p1, legs=2, 8bps)')
    for per, lo, hi in [('IS', '2014-01-01', SPLIT), ('OOS', SPLIT, '2027-01-01')]:
        st = summarize(sim0, lo, hi, active='act_p1'); o[f'{per}_m'] = st['mean_bps']; o[f'{per}_t'] = st['t_act']; o[f'{per}_n'] = st['n_act']
    rows.append(o)
    for entry in ['close0', 'open', 'close1']:
        for cost in [0, 8, 15, 30]:
            rows.append(dict(lab=f'{entry} {cost}bps', **stat(simulate(pos, tg, ti, tc, lw, entry, cost))))
        rows.append(dict(lab=f'{entry} 8bps+tik', **stat(simulate(pos, tg, ti, tc, lw, entry, 8, tick))))
        rows.append(dict(lab=f'{entry} 15bps+tik', **stat(simulate(pos, tg, ti, tc, lw, entry, 15, tick))))
    # 10:30 girişi (h1 dönemi)
    pk, px_ = h1_px('KCHOL'), h1_px('XU030')
    # XU030 h1 ilk barının kapanışı (10:30) kullanılabilir; açılışı günlük veriden. intra' = log(c/p1030)
    ik = np.log(raw('KCHOL')['c'] / pk.reindex(raw('KCHOL').index)).reindex(cal); ix = np.log(raw('XU030')['c'] / px_.reindex(raw('XU030').index)).reindex(cal)
    i2 = ik - bm * ix; g2 = tc - i2; m = i2.notna()
    for cost in [0, 8, 15]:
        for lab, g_, i_ in [('10:30 girişi', g2, i2), ('açılış (aynı günler)', tg, ti)]:
            ss = simulate(pos, g_.where(m), i_.where(m), tc, lw, 'open', cost); ss = ss[ss.index >= '2023-12-01']
            st = summarize(ss, '2023-12-01', '2027-01-01'); rows.append(dict(lab=f'{lab} {cost}bps [2023-12..]', **{'23-26_m': st['mean_bps'], '23-26_t': st['t_all'], '23-26_n': st['n_act']}))
    D = pd.DataFrame(rows); D.to_csv(HERE + '/res_nav_timing.csv', index=False)
    print(D.drop(columns=['by_year']).round(2).to_string())
    for r in rows:
        if r['lab'] in ['open 8bps', 'close1 8bps', 'open 30bps']: print(r['lab'], r['by_year'])
    # yön ayrıştırması
    sim = simulate(pos, tg, ti, tc, lw, 'open', 8)
    for per, lo, hi in [('IS', '2014-01-01', SPLIT), ('OOS', SPLIT, '2027-01-01')]:
        ss = sim[(sim.index >= lo) & (sim.index < hi)]
        side = pos.reindex(ss.index).shift(1).fillna(0)
        print(per, 'yön (+1 = iskonto geniş, KCHOL uzun):', {k: (len(v), round(1e4 * v.mean(), 1)) for k, v in ss['pnl'].groupby(side) if k != 0}, ' gün oranı uzun/kısa:', round((side > 0).mean(), 2), round((side < 0).mean(), 2))
