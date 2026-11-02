"""VİOP vadeli fiyatlarıyla (bülten) bağımsız backtest: kendi sürekli seri kurgum (ön ay, vadeye <=3 iş günü kala devir),
dolum = t+1 ilk işlem / t+1 tüm gün VWAP / t+1 uzlaşma; DEVİR MALİYETİ dahil. Sinyal spot kapanıştan (z60, β250). Likidite yıllık."""
import vb, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
PP = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data/viop_panel.parquet'
p = pd.read_parquet(PP, columns=['date', 'code', 'root', 'ctype', 'expiry', 'settle', 'prev_settle', 'open', 'close', 'vwap', 'value_tl', 'qty', 'trades', 'oi'])
p = p[p.ctype.astype(str).isin(['D_EQ_FPD', 'D_IX_FUT'])].copy(); p['root'] = p.root.astype(str); p['date'] = pd.to_datetime(p.date); p['expiry'] = pd.to_datetime(p.expiry)
DATES = np.array(sorted(p.date.unique()))
def cont(root, roll_bd=3):
    d = p[(p.root == root) & (p.expiry >= p.date)].copy()
    d['bdl'] = np.searchsorted(DATES, d.expiry.values) - np.searchsorted(DATES, d.date.values)
    d = d[d.bdl > roll_bd].sort_values(['date', 'expiry'])
    f = d.groupby('date').head(1).set_index('date')
    f['r'] = np.log(f.settle / f.prev_settle); f.loc[(f.settle <= 0) | (f.prev_settle <= 0), 'r'] = np.nan
    f.loc[np.expm1(f.r).abs() > 0.105, 'r'] = np.nan   # 2017+ hepsi yeni rejim değil: 2020-03 öncesi spot ±%20 idi; vadeli marjı aynı mantık
    f['X_open'] = np.where((f.trades > 0) & (f.open > 0), f.open, np.nan)
    f['X_vwap'] = np.where((f.trades > 0) & (f.vwap > 0), f.vwap, np.nan)
    f['X_settle'] = f.settle
    f['roll'] = f.code != f.code.shift()
    return f
def bt(pos, beta, FA, FB, X='X_open', cost=8, roll=True):
    idx = FA.index.intersection(FB.index); FA = FA.reindex(idx); FB = FB.reindex(idx)
    pos = pos.reindex(idx).fillna(0); b = beta.reindex(idx).ffill()
    Q = pos.shift(1).fillna(0); Q0 = Q.shift(1).fillna(0)  # Q_t: t'de X_t ile yürütülen hedef
    def leg(F):
        xa = F[X].fillna(F['settle'])   # dolum yoksa uzlaşmadan (yaklaşık)
        pre = np.log(xa / F.prev_settle); post = np.log(F.settle / xa)
        return pre, post
    preA, postA = leg(FA); preB, postB = leg(FB)
    gross = Q0 * (preA - b * preB).fillna(0) + Q * (postA - b * postB).fillna(0)
    c = cost / 1e4
    tc = c / 2 * (1 + b.abs()) * (Q - Q0).abs()
    if roll: tc += c * (1 + b.abs()) * Q0.abs() * (FA.roll | FB.roll).astype(float) * (Q != 0)   # pozisyon devir gününde tutuluyorsa
    net = gross - tc
    exp = (Q != 0) | (Q0 != 0)
    return pd.DataFrame({'net': net, 'gross': gross, 'cost': tc, 'exp': exp, 'valid': (FA.r.notna() & FB.r.notna()), 'Pi': Q, 'Pg': Q0})
PER = [('2017-20', '2017-03-01', '2021-01-01'), ('2021-23', '2021-01-01', '2024-01-01'), ('2024-26', '2024-01-01', '2027-01-01'), ('OOS 2021-26', '2021-01-01', '2027-01-01')]
if __name__ == '__main__':
    FA, FB = cont('SAHOL'), cont('AKBNK')
    P = vb.pair_inputs('SAHOL', 'AKBNK'); z = vb.zscore(P['S'], 60); pos = vb.positions(z, 1.5)
    # likidite (ön ay günlük işlem değeri medyanı, mn TL) ve işlem sayısı
    for nm, F in [('SAHOL', FA), ('AKBNK', FB)]:
        g = F.groupby(F.index.year); print(nm, 'ön ay medyan günlük değer (mn TL):', (g.value_tl.median() / 1e6).round(1).to_dict(), ' medyan işlem adedi:', g.trades.median().to_dict())
    rows = []
    for X in ['X_open', 'X_vwap', 'X_settle']:
        for c in [8, 15, 30]:
            for rl in [True, False]:
                d = bt(pos, P['beta'], FA, FB, X, c, rl)
                for lab, lo, hi in PER:
                    s = vb.summ(d, lo, hi); rows.append(dict(fill=X, cost=c, roll=rl, per=lab, bps=s['bps'], t=s['t'], n=s['n']))
    R = pd.DataFrame(rows); R.to_csv('res_fut.csv', index=False)
    print(R.pivot_table(index=['fill', 'cost', 'roll'], columns='per', values='t').round(2).to_string())
    print(R[R.roll].pivot_table(index=['fill', 'cost'], columns='per', values='bps').round(1).to_string())
    # spot-vadeli aynı günler karşılaştırması (spot açılış, 8 bps)
    ds = vb.pnl_open(pos, P['A']['gap'], P['A']['intra'], P['B']['gap'], P['B']['intra'], P['beta'], 8)
    print('spot aynı dönem:', {lab: round(vb.summ(ds, lo, hi)['t'], 2) for lab, lo, hi in PER})
    # devir sayısı / işlem
    d = bt(pos, P['beta'], FA, FB, 'X_open', 8, True); d = d[d.index >= '2021']
    print('OOS devir gününde açık pozisyon:', int(((FA.roll | FB.roll).reindex(d.index) & (d.Pg != 0) & (d.Pi != 0)).sum()), ' giriş sayısı', int(((d.Pi != 0) & (d.Pi != d.Pg)).sum()))
