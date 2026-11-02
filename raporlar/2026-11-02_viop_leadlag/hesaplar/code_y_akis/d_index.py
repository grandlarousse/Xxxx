"""Endeks dönem değişikliği: duyuru -> tepki -> yürürlük arifesi kapanışı -> sonrası. İşaret: giren +1, çıkan -1. Fazla getiri = hisse - XU100 (adj, log).
Pencereler: R0 = tepki (duyuru seans sonrasıysa ertesi gün cc; seans içiyse duyuru günü+ertesi gün), RUN = R0 sonrası kapanış -> eff_eve kapanışı,
EVE = eff_eve günü cc (kapanış dengelemesi dahil), POST5 = eff_eve sonrası 5 gün, POST20.
BT: R0 kapanışında işaret yönünde gir, eff_eve kapanışında çık (RUN). Maliyet 15 bps (küçük hisselerde gerçek spread daha yüksek)."""
import numpy as np, pandas as pd, alib, index_events as I
from alib import ll
X = alib.xu('XU100'); xcc = X['cc']
def series(sym):
    d = ll.raw(sym + '.IS').copy(); d.index = pd.DatetimeIndex(d['ldate'].values); d = d[~d.index.duplicated(keep='last')]; d = d[d.v.fillna(0) > 0]
    r = np.log(d.adj).diff(); r[(r > ll.LIM_UP) | (r < ll.LIM_DN)] = np.nan
    return r, (d.c * d.v).rolling(60, min_periods=10).median()
rows = []
for e in I.EV:
    for key in ['BIST30_in', 'BIST30_out', 'BIST50_in', 'BIST50_out', 'BIST100_in', 'BIST100_out']:
        for s in e.get(key, []):
            try: r, tv = series(s)
            except Exception as ex: print('yok', s, ex); continue
            exr = (r - xcc.reindex(r.index)).dropna()
            idx = exr.index
            rc = pd.Timestamp(e['react']); eve = pd.Timestamp(e['eff_eve'])
            if rc not in idx or eve not in idx: print('tarih yok', s, e['q']); continue
            i0 = idx.get_loc(rc); ie = idx.get_loc(eve)
            if e['intra_ann']: R0 = exr.iloc[i0:i0 + 2].sum(); ient = i0 + 1
            else: R0 = exr.iloc[i0]; ient = i0
            sign = 1 if key.endswith('_in') else -1
            rows.append(dict(q=e['q'], idx=key.split('_')[0], dir=key.split('_')[1], sign=sign, stock=s, viop=s in alib.VIOP,
                             pre5=exr.iloc[max(0, i0 - 5):i0].sum(), R0=R0, RUN=exr.iloc[ient + 1:ie + 1].sum() if ie > ient else np.nan,
                             RUN_ex_eve=exr.iloc[ient + 1:ie].sum() if ie - 1 > ient else np.nan, EVE=exr.iloc[ie],
                             POST5=exr.iloc[ie + 1:ie + 6].sum() if ie + 6 <= len(exr) else np.nan, POST20=exr.iloc[ie + 1:ie + 21].sum() if ie + 21 <= len(exr) else np.nan,
                             n_run=ie - ient, tv_mn=tv.reindex([rc]).iloc[0] / 1e6 if rc in tv.index else np.nan))
E = pd.DataFrame(rows); E.to_csv('res_index_events.csv', index=False)
for c in ['pre5', 'R0', 'RUN', 'RUN_ex_eve', 'EVE', 'POST5', 'POST20']: E['s_' + c] = E[c] * E.sign
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 40)
out = []
for lab, sub in [('all', E), ('BIST30', E[E.idx == 'BIST30']), ('BIST50', E[E.idx == 'BIST50']), ('BIST100', E[E.idx == 'BIST100']), ('in', E[E.sign > 0]), ('out', E[E.sign < 0]),
                 ('viop47', E[E.viop]), ('excl_2026Q4', E[E.q != '2026Q4']), ('BIST30+50', E[E.idx != 'BIST100'])]:
    r = dict(set=lab, n=len(sub))
    for c in ['pre5', 'R0', 'RUN', 'EVE', 'POST5', 'POST20']:
        v = sub['s_' + c].dropna(); r[c + '_bps'] = round(1e4 * v.mean(), 1); r[c + '_t'] = round(alib.tstat(v)[0], 2)
        r[c + '_qpos'] = f"{int((sub.groupby('q')['s_' + c].mean() > 0).sum())}/{sub.q.nunique()}"
    # BT: R0 kapanışında işaret yönünde gir, eff_eve kapanışında çık
    for cost in [8, 15]:
        p = sub.s_RUN.dropna() - cost / 1e4; r[f'bt_run_c{cost}_bps'] = round(1e4 * p.mean(), 1)
    out.append(r)
S = pd.DataFrame(out); print(S.to_string()); S.to_csv('res_index_summary.csv', index=False)
print(E.groupby(['q', 'idx', 'dir'])[['s_R0', 's_RUN', 's_EVE', 's_POST5']].mean().mul(1e4).round(0).to_string())
