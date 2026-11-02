"""6) Backtestler (look-ahead yok; maliyet 8/15 bps gidiş-dönüş; IS/OOS).
BT1 tavan/taban (P10 rejimi, 2020-03-13+; IS=2020-03..2022-12, OOS=2023-01..2026-10; ayrıca brif ayrımı 2021):
   a) TC -> ertesi gün açılışta SAT, kapanışta kapat (gün-içi geri dönüş). b) TU (dokunup geri dönen) -> aynı. c) BCL (kilitli taban) -> ertesi gün açılışta AL, kapanışta sat.
   d) BC -> t+1 kapanışında SAT, t+5 kapanışında kapat (sürüklenme; XU100'e göre fazla getiri, endeks vadelisiyle hedge varsayımı).
   Günlük PnL = o gün açık olayların eşit ağırlıklı ortalaması. Evren: 'viop47' (VİOP pay vadelisiyle işlenebilir) ve 'all' (spot; açığa satış kısıtı/spread notu).
BT5 Ay dönümü: XU030 (VİOP F_XU030) ayın son iş günü kapanışında AL, ilk iş günü kapanışında SAT (d1) ve son-1 kapanış -> 3. gün kapanışı (TOM).
BT6 Temettü: a) ex-5 kapanışında AL, ex-1 kapanışında SAT (fazla getiri, XU100 hedge) b) ex-günü açılışta SAT, kapanışta kapat.
"""
import numpy as np, pandas as pd, json, alib
from alib import ll
E = pd.read_parquet('res_limit_events.parquet'); E = E[E.reg == 'P10']
res = {}
def stats(pnl_by_day, lab):
    p = pnl_by_day.dropna()
    if len(p) < 20: return {'n_days': len(p)}
    m, t, n = alib.nw(p, 5)
    return {'n_days': n, 'mean_bps': round(1e4 * p.mean(), 1), 't': round(t, 2), 'hit': round((p > 0).mean(), 3),
            'sharpe_ann_active': round(p.mean() / p.std() * np.sqrt(252), 2)}
def run(sub, col, sign, cost, lab):
    x = sub[['date', col]].dropna()
    pnl = sign * x[col] - cost / 1e4
    g = pnl.groupby(x.date).mean()
    out = {'n_trades': len(x)}
    for per, a, b in [('ALL', '2020', '2027'), ('IS_20_22', '2020', '2022-12-31'), ('OOS_23_26', '2023', '2027'), ('IS_brief_2020', '2020', '2020-12-31'), ('OOS_brief_21_26', '2021', '2027')]:
        out[per] = stats(g.loc[a:b], per)
    out['by_year_bps'] = (1e4 * g.groupby(g.index.year).mean()).round(1).to_dict()
    return out
for uni, mask in [('viop47', E.viop), ('all', E.stock.notna()), ('all_liqH', E.liq == 'H')]:
    for cost in [8, 15]:
        res[f'BT1a_TC_fade_intra_{uni}_c{cost}'] = run(E[mask & E.TC], 'intra1', -1, cost, '')
        res[f'BT1b_TU_fade_intra_{uni}_c{cost}'] = run(E[mask & E.TU], 'intra1', -1, cost, '')
        res[f'BT1c_BCL_long_intra_{uni}_c{cost}'] = run(E[mask & E.BCL], 'intra1', +1, cost, '')
        res[f'BT1d_BC_short_t2_5x_{uni}_c{cost}'] = run(E[mask & E.BC], 'cc2_5x', -1, cost, '')
        res[f'BT1e_TC_short_t2_5x_{uni}_c{cost}'] = run(E[mask & E.TC & ~E.ipo], 'cc2_5x', -1, cost, '')
# --- BT5 ay dönümü
D = pd.read_parquet('_cal_flags.parquet')
x30 = ll.ret('XU030.IS'); x30 = x30[x30.index >= '2005-01-01']
cal = x30.index
flags = D.reindex(cal)
def cal_bt(mask_hold, cost, lab):
    pos = mask_hold.astype(float)
    entries = (pos.diff().fillna(pos) > 0).astype(float)
    pnl = pos * x30 - entries * cost / 1e4
    o = {}
    for per, a, b in [('ALL', '2005', '2027'), ('IS', '2005', '2020-12-31'), ('OOS', '2021', '2027')]:
        p = pnl.loc[a:b]; ps = pos.loc[a:b]
        tr = p[ps > 0]
        o[per] = dict(days_in=int(ps.sum()), mean_bps_per_day_in=round(1e4 * tr.mean(), 1), t=round(alib.nw(tr, 5)[1], 2), ann_ret_pct=round(100 * p.mean() * 252, 2),
                      sharpe=round(p.mean() / p.std() * np.sqrt(252), 2), bh_mean_bps=round(1e4 * x30.loc[a:b].mean(), 1))
    o['by_year_bps_in'] = (1e4 * pnl[pos > 0].groupby(pnl[pos > 0].index.year).mean()).round(1).to_dict()
    return o
for cost in [8, 15]:
    res[f'BT5_d1_XU030_c{cost}'] = cal_bt(flags.d1.fillna(False), cost, 'd1')
    res[f'BT5_TOM_XU030_c{cost}'] = cal_bt(flags.tom.fillna(False), cost, 'tom')
# --- BT6 temettü
T = pd.read_csv('res_div_events.csv', parse_dates=['date']); T = T[(T.dy > 0.003) & (T.dy < 0.25)]
for uni, m in [('viop47', T.viop), ('all', T.stock.notna())]:
    for cost in [8, 15]:
        for nm, col, sg in [('BT6a_pre5_long', 'pre5', 1), ('BT6b_exday_short_intra', 'intra0', -1)]:
            x = T[m][['date', col]].dropna(); pnl = sg * x[col] - cost / 1e4
            o = {}
            for per, a, b in [('ALL', '2010', '2027'), ('IS', '2010', '2020-12-31'), ('OOS', '2021', '2027')]:
                pp = pnl[(x.date >= a) & (x.date <= b)]
                o[per] = dict(n=len(pp), mean_bps=round(1e4 * pp.mean(), 1), t=round(alib.tstat(pp)[0], 2), hit=round((pp > 0).mean(), 3))
            o['by_year_bps'] = (1e4 * pnl.groupby(x.date.dt.year).mean()).round(0).to_dict()
            res[f'{nm}_{uni}_c{cost}'] = o
json.dump(res, open('res_bt_all.json', 'w'), indent=1, default=str)
for k, v in res.items():
    print(k, {kk: vv for kk, vv in v.items() if kk not in ('by_year_bps', 'by_year_bps_in')})
