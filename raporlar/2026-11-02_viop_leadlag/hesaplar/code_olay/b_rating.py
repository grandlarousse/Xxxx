"""Kredi notu kararları (genelde Cuma ~20:30 UTC) -> Pazartesi gap / gün-içi / t+1..5."""
from olib import *
import json
ev = EV[EV.type == 'RATING'].copy()
ev['kind'] = ev['sub'].str.split('_').str[1]
cc, gp, it = comp('cc'), comp('gap'), comp('intra')
f15 = fwd_cc(cc, 1, 5); pre = sum(cc.shift(k) for k in range(1, 6))  # t-5..t-1
# baz: aynı haftanın günü ortalaması (pazartesi etkisi)
def base(T, c, d): 
    x = T[c]; return x[x.index.dayofweek == d.dayofweek].mean()
rows = []
for _, e in ev.iterrows():
    d = e.react_date
    if d not in cc.index or d < pd.Timestamp('2014-01-02'): continue
    r = dict(date=e.date.date(), react=d.date(), sub=e['sub'], kind=e.kind, dir=e.dir)
    for c in ['XU100', 'XBANK']:
        r[f'{c}_gap'] = gp.at[d, c] - base(gp, c, d); r[f'{c}_intra'] = it.at[d, c] - base(it, c, d)
        r[f'{c}_f1_5'] = f15.at[d, c]; r[f'{c}_pre5'] = pre.at[d, c]
    rows.append(r)
T = pd.DataFrame(rows); T.to_csv('res_rating_events.csv', index=False)
# işaretli özet
summ = []
for grp, m in [('not değişikliği', T.kind.isin(['downgrade', 'upgrade'])), ('görünüm/izleme', T.kind.isin(['outlook', 'review'])), ('hepsi', T.kind.notna())]:
    S = T[m]
    for col in [c for c in T.columns if c.startswith('X')]:
        v = S[col] * S['dir']; t, n = tstat(v)
        summ.append(dict(grp=grp, col=col, signed_mean_bps=1e4 * v.mean(), t=t, n=n, hit=(v > 0).mean()))
summ = pd.DataFrame(summ); summ.to_csv('res_rating_summary.csv', index=False)
print(summ[summ.grp != 'hepsi'].round(2).to_string(index=False))
# IS/OOS (2014-2020: neredeyse hepsi indirim; 2021-2026: çoğu artırım)
for lab, m in [('IS', T.react < pd.Timestamp('2021-01-01').date()), ('OOS', T.react >= pd.Timestamp('2021-01-01').date())]:
    S = T[m & T.kind.isin(['downgrade', 'upgrade'])]
    print(lab, 'not değişikliği n=', len(S), 'XBANK gap signed bps', round(1e4 * (S.XBANK_gap * S.dir).mean(), 1), 'intra', round(1e4 * (S.XBANK_intra * S.dir).mean(), 1), 'f1_5', round(1e4 * (S.XBANK_f1_5 * S.dir).mean(), 1))
# hisse kesiti: not değişikliği günü (react) aşırı cc, işaretli
chg = ev[ev.kind.isin(['downgrade', 'upgrade'])]
sign = dict(zip(chg.react_date, chg.dir))
xs = xsec(list(sign.keys()), sign, 'cc'); xs_g = xsec(list(sign.keys()), sign, 'gap')
xs['gap_mean_bps'] = xs_g['mean_bps']; xs.to_csv('res_rating_xsec.csv')
print(xs.round(1).iloc[list(range(4)) + list(range(-6, 0))].to_string())
# backtest (işlenebilir): olay sonrası Pazartesi açılışta dir yönünde gir, (a) kapanışta çık (b) 5 gün tut
sig = pd.Series(0.0, index=cc.index)
for d, s in sign.items():
    if d in sig.index: sig[d] = s
res = {}
for c in ['XBANK', 'XU100']:
    for nm, tgt in [('intra', it[c]), ('intra+f1_5', it[c] + f15[c])]:
        for cost in [8, 15]:
            r_, _ = ll.backtest(sig.replace(0, np.nan), tgt, cost_bps=cost)
            res[f'{c}_{nm}_{cost}'] = {k: r_[k] for k in ['IS', 'OOS', 'ALL']}
            print(c, nm, cost, {k: (round(r_[k].get('mean_bps', np.nan), 1), round(r_[k].get('t', np.nan), 2), r_[k]['n']) for k in ['IS', 'OOS', 'ALL']})
json.dump(res, open('res_rating_bt.json', 'w'), indent=1, default=str)
