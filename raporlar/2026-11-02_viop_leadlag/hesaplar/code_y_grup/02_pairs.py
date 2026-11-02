"""Ana-yavru / kardeş / pay grubu çiftleri: senkron + günlük lead-lag (gap/intra ayrışık, kontrollü) + FDR + plasebo (rastgele çift) null."""
from gx import *
import itertools, random
XU = R('XU100'); XD = DC('XU100') if False else None
xu_cc = XU
def sync_stats(a, b):
    A, B = R(a), R(b)
    df = pd.concat([A.rename('a'), B.rename('b'), xu_cc.rename('m')], axis=1).dropna()
    df = df[df.index >= pd.Timestamp('2010-01-01')]
    if len(df) < 250: return None
    last = df.index.max(); o = {}
    o['n'] = len(df); o['start'] = df.index[0].date()
    o['corr_full'] = df.a.corr(df.b)
    o['corr_3y'] = df[df.index >= last - pd.DateOffset(years=3)].pipe(lambda x: x.a.corr(x.b))
    o['corr_1y'] = df[df.index >= last - pd.DateOffset(years=1)].pipe(lambda x: x.a.corr(x.b))
    def pc(x):
        if len(x) < 120: return np.nan
        C = np.c_[np.ones(len(x)), x.m.values]
        ra = x.a.values - C @ np.linalg.lstsq(C, x.a.values, rcond=None)[0]; rb = x.b.values - C @ np.linalg.lstsq(C, x.b.values, rcond=None)[0]
        return np.corrcoef(ra, rb)[0, 1]
    o['pc_full'] = pc(df); o['pc_3y'] = pc(df[df.index >= last - pd.DateOffset(years=3)]); o['pc_1y'] = pc(df[df.index >= last - pd.DateOffset(years=1)])
    o['pc_IS'] = pc(df[(df.index >= '2014-01-01') & (df.index < SPLIT)]); o['pc_OOS'] = pc(df[df.index >= SPLIT])
    yrs = df.groupby(df.index.year).apply(pc).dropna(); o['pc_yr_pos'] = float((np.sign(yrs) == np.sign(o['pc_full'])).mean()); o['n_yr'] = len(yrs)
    # betalar: a ~ b + m ; b ~ a + m  (NW t)
    m1 = nwreg(df.a, df[['b', 'm']]); m2 = nwreg(df.b, df[['a', 'm']])
    o['beta_a_on_b'] = m1[0].params[1]; o['t_beta_ab'] = m1[0].tvalues[1]
    o['beta_b_on_a'] = m2[0].params[1]; o['t_beta_ba'] = m2[0].tvalues[1]
    o['beta_a_mkt'] = np.polyfit(df.m, df.a, 1)[0]; o['beta_b_mkt'] = np.polyfit(df.m, df.b, 1)[0]
    return o
def lead_stats(x, y, pre=''):
    """x lider, y takipçi. y_k,t ~ x_cc,t-1 + y_cc,t-1 + XU_t-1 (k=cc,gap,intra); y_intra,t ~ x_gap,t + y_gap,t + XU_gap,t (açılıştan sonra bilinir)."""
    X, Y = R(x), R(y); DY, DX = DC(y), DC(x); DM = DC('XU100')
    o = {}
    base = pd.concat([X.shift(1).rename('x1'), Y.shift(1).rename('y1'), xu_cc.shift(1).rename('m1')], axis=1)
    for k, tgt, st in [('cc', Y, '2010-01-01'), ('gap', DY['gap'], '2014-01-01'), ('intra', DY['intra'], '2014-01-01')]:
        yy = tgt[tgt.index >= pd.Timestamp(st)]
        for lab, lo, hi in [('', None, None), ('_IS', '2014-01-01', SPLIT), ('_OOS', SPLIT, None)]:
            if lab and k == 'cc': lo = lo if lo else None
            yv = yy
            if lo is not None: yv = yv[yv.index >= pd.Timestamp(lo)]
            if hi is not None: yv = yv[yv.index < pd.Timestamp(hi)]
            r = nwreg(yv, base)
            o[f'{pre}l1_{k}_b{lab}'] = r[0].params[1] if r else np.nan; o[f'{pre}l1_{k}_t{lab}'] = r[0].tvalues[1] if r else np.nan
            if not lab: o[f'{pre}l1_{k}_n'] = len(r[1]) if r else 0
    # aynı gün: x gap -> y intra (y gap ve XU gap kontrollü)
    base2 = pd.concat([DX['gap'].rename('xg'), DY['gap'].rename('yg'), DM['gap'].rename('mg')], axis=1)
    for lab, lo, hi in [('', '2014-01-01', None), ('_IS', '2014-01-01', SPLIT), ('_OOS', SPLIT, None)]:
        yv = DY['intra']; yv = yv[yv.index >= pd.Timestamp(lo)]
        if hi is not None: yv = yv[yv.index < pd.Timestamp(hi)]
        r = nwreg(yv, base2)
        o[f'{pre}g2i_b{lab}'] = r[0].params[1] if r else np.nan; o[f'{pre}g2i_t{lab}'] = r[0].tvalues[1] if r else np.nan
        if not lab: o[f'{pre}g2i_n'] = len(r[1]) if r else 0
    return o
if __name__ == '__main__':
    rows = []
    for a, b, g, typ in PAIRS:
        try:
            o = sync_stats(a, b)
            if o is None: print('skip', a, b); continue
            o.update(dict(ana=a, yavru=b, grup=g, tur=typ))
            o.update(lead_stats(b, a, 'Y2A_'))   # yavru lider -> ana
            o.update(lead_stats(a, b, 'A2Y_'))   # ana lider -> yavru
            rows.append(o); print(a, b, round(o['pc_full'], 3), round(o['Y2A_l1_intra_t'], 2), round(o['A2Y_l1_intra_t'], 2), round(o['Y2A_g2i_t'], 2), round(o['A2Y_g2i_t'], 2), flush=True)
        except Exception as e:
            print('ERR', a, b, e)
    df = pd.DataFrame(rows)
    # FDR: lead aileleri (her aile tüm çiftler x 2 yön)
    for fam in ['l1_cc', 'l1_gap', 'l1_intra', 'g2i']:
        ts = pd.concat([df[f'Y2A_{fam}_t'], df[f'A2Y_{fam}_t']]).values
        rej, padj = ll.fdr(ll.t_to_p(ts))
        n = len(df); df[f'Y2A_{fam}_fdr'] = rej[:n]; df[f'A2Y_{fam}_fdr'] = rej[n:]
    rej, _ = ll.fdr(ll.t_to_p(df['t_beta_ab'].values)); df['sync_fdr'] = rej
    cols = ['ana','yavru','grup','tur'] + [c for c in df.columns if c not in ('ana','yavru','grup','tur')]
    df[cols].to_csv(HERE + '/res_pairs.csv', index=False)
    print('n pairs', len(df), 'lead tests', 4 * 2 * len(df))
