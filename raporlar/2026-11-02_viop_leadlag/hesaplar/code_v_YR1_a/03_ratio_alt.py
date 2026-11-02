"""YR1-A alternatif tanımlar: beta=1 log oran, histerezis çıkış, parametre ızgarası, bacak ayrıştırması (XU030 hedge)."""
import sys; sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_YR1_a')
from vlib import *
def pair(A, B, beta_mode='roll'):
    da, db = dec(A), dec(B)
    idx = da.index.union(db.index); idx = idx[idx >= pd.Timestamp('2010-01-01')]
    da, db = da.reindex(idx), db.reindex(idx)
    beta = roll_beta(da['cc'], db['cc']) if beta_mode == 'roll' else pd.Series(1.0, index=idx)
    if beta_mode == 'logratio':
        S = np.log(raw(A)['adj']).reindex(idx).ffill() - np.log(raw(B)['adj']).reindex(idx).ffill()  # literal log fiyat oranı (temizlik yok)
    else:
        S = (da['cc'] - beta * db['cc']).fillna(0).cumsum()
    return dict(da=da, db=db, beta=beta, S=S, g=da['gap'] - beta * db['gap'], i=da['intra'] - beta * db['intra'], c=da['cc'] - beta * db['cc'], lw=1 + beta.abs(), idx=idx)
def run(P, w, thr, cost=8, entry='open', mode='band', exit_thr=None, tgt=None):
    z = zscore(P['S'], w); pos = positions(z, thr, mode, exit_thr)
    g, i, c, lw = (P['g'], P['i'], P['c'], P['lw']) if tgt is None else tgt
    sim = simulate(pos, g, i, c, lw, entry, cost)
    o = {}
    for per, lo, hi in [('IS', '2014-01-01', SPLIT), ('OOS', SPLIT, '2027-01-01')]:
        st = summarize(sim, lo, hi); o[f'{per}_m'] = st['mean_bps']; o[f'{per}_t'] = st['t_all']; o[f'{per}_sh'] = st['sharpe']; o[f'{per}_tr'] = st['entries']; o[f'{per}_hold'] = st['hold_d']
    yb = by_year(sim[sim.index >= '2014-01-01']); o['yrs'] = f'{int((yb > 0).sum())}/{len(yb)}'
    return o, sim, pos
if __name__ == '__main__':
    pd.set_option('display.width', 250); pd.set_option('display.max_rows', 300)
    P = pair('SAHOL', 'AKBNK'); P1 = pair('SAHOL', 'AKBNK', 'one'); PL = pair('SAHOL', 'AKBNK', 'logratio')
    rows = []
    for lab, PP in [('beta250', P), ('beta=1 cumsum', P1), ('log fiyat oranı (adj)', PL)]:
        for mode, ex in [('band', None), ('hyst', 0.0), ('hyst', 0.5)]:
            o, _, _ = run(PP, 60, 1.5, mode=mode, exit_thr=ex); rows.append(dict(tanim=lab, kural=f'{mode}{"" if ex is None else ex}', **o))
    print(pd.DataFrame(rows).round(2).to_string())
    # ızgara
    G = []
    for w in [20, 40, 60, 90, 120, 250]:
        for thr in [1.0, 1.5, 2.0, 2.5]:
            o, _, _ = run(P, w, thr); G.append(dict(w=w, thr=thr, **o))
    G = pd.DataFrame(G); G.to_csv(HERE + '/res_ratio_grid.csv', index=False)
    print(G.round(2).to_string())
    print('ızgara: IS t>2 oranı', (G.IS_t > 2).mean().round(2), ' OOS t>2 oranı', (G.OOS_t > 2).mean().round(2), ' min/medyan IS t', G.IS_t.min().round(2), G.IS_t.median().round(2), ' OOS', G.OOS_t.min().round(2), G.OOS_t.median().round(2))
    # bacak ayrıştırması: aynı pozisyon, hedef = SAHOL - bX*XU030 ve -(beta)*(AKBNK - bY*XU030)
    dx = dec('XU030').reindex(P['idx'])
    bA = roll_beta(P['da']['cc'], dx['cc']); bB = roll_beta(P['db']['cc'], dx['cc'])
    z = zscore(P['S'], 60); pos = positions(z, 1.5)
    L = []
    for lab, g, i, c, lw in [('tam spread', P['g'], P['i'], P['c'], P['lw']),
                             ('SAHOL - b*XU030', P['da']['gap'] - bA * dx['gap'], P['da']['intra'] - bA * dx['intra'], P['da']['cc'] - bA * dx['cc'], 1 + bA.abs()),
                             ('-beta*(AKBNK - b*XU030)', -P['beta'] * (P['db']['gap'] - bB * dx['gap']), -P['beta'] * (P['db']['intra'] - bB * dx['intra']), -P['beta'] * (P['db']['cc'] - bB * dx['cc']), P['beta'].abs() * (1 + bB.abs())),
                             ('SAHOL çıplak', P['da']['gap'], P['da']['intra'], P['da']['cc'], pd.Series(1.0, index=P['idx'])),
                             ('-beta*AKBNK çıplak', -P['beta'] * P['db']['gap'], -P['beta'] * P['db']['intra'], -P['beta'] * P['db']['cc'], P['beta'].abs())]:
        sim = simulate(pos, g, i, c, lw, 'open', 0)
        o = dict(bacak=lab)
        for per, lo, hi in [('IS', '2014-01-01', SPLIT), ('OOS', SPLIT, '2027-01-01')]:
            st = summarize(sim, lo, hi); o[f'{per}_brut_m'] = st['mean_bps']; o[f'{per}_t'] = st['t_all']
        L.append(o)
    print(pd.DataFrame(L).round(2).to_string())
    # Yön ayrıştırması: spread uzun (SAHOL al) vs kısa
    sim = simulate(pos, P['g'], P['i'], P['c'], P['lw'], 'open', 8)
    for per, lo, hi in [('IS', '2014-01-01', SPLIT), ('OOS', SPLIT, '2027-01-01')]:
        ss = sim[(sim.index >= lo) & (sim.index < hi) & sim.expo]
        side = np.sign(ss['p1'].where(ss['p1'] != 0, pos.reindex(ss.index).shift(2).fillna(0)))
        print(per, 'yön: +1=SAHOL uzun', (1e4 * ss['pnl'].groupby(side).agg(['count', 'mean'])).round(1).to_dict())
