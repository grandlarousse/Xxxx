"""v_YA1_a — backtestler (bağımsız). Maliyet: gidiş-dönüş C bps (8/15/30) + tik maliyeti (0,01 TL / gerçek fiyat; VİOP pay vadelisi tik=0,01 TL).
 b)  TC  -> t+1 açılışta SAT, t+1 kapanışta KAPAT     pnl = -intra_1
 c)  TU  -> aynı
 d)  BC  -> t+1 kapanışta SAT (yalnız t+1 taban DEĞİLSE = dolum uygun), t+5 kapanışta kapat; XU100'e göre fazla getiri (endeks vadelisi hedge +4 bps)
     d_naive: t+1 taban olsa da gir ; d_alt: t+1 taban ise t+2 taban değilse t+2 kapanışında gir (dr3_6)
 Çıktı: res_v2_bt.csv (+ yıllık)
İstatistik: (i) işlem başı ortalama, tarih-kümelemeli t ; (ii) olay-günü portföyü (aynı gün olayların eşit ağırlıklı ortalaması) Newey-West(5) t.
"""
import numpy as np, pandas as pd, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from v0_panel import SCR

def nw_t(x, L=5):
    x = np.asarray(pd.Series(x).dropna(), float); n = len(x)
    if n < 10: return np.nan
    m = x.mean(); e = x - m; s = (e @ e) / n
    for l in range(1, L + 1):
        w = 1 - l / (L + 1); s += 2 * w * (e[l:] @ e[:-l]) / n
    return m / np.sqrt(s / n)

def stat(df, col, cost_bps, tickmult=1.0):
    x = df[['date', col, 'tikc']].dropna(subset=[col])
    if len(x) < 10: return dict(n=len(x))
    pnl = x[col] - cost_bps / 1e4 - tickmult * x.tikc
    gm = pnl.groupby(x.date).mean()
    tcl = gm.mean() / (gm.std(ddof=1) / np.sqrt(len(gm))) if len(gm) > 2 else np.nan
    return dict(n=len(x), ndays=len(gm), mean_trade=round(1e4 * pnl.mean(), 1), med_trade=round(1e4 * pnl.median(), 1), t_cl=round(tcl, 2),
                mean_day=round(1e4 * gm.mean(), 1), t_nw=round(nw_t(gm), 2), hit=round((pnl > 0).mean(), 3), tick_bps=round(1e4 * tickmult * x.tikc.mean(), 1))

PERIODS = [('ALL', '2020-03-13', '2026-12-31'), ('IS_brief_2020', '2020-03-13', '2020-12-31'), ('OOS_brief_21_26', '2021-01-01', '2026-12-31'),
           ('IS_20_22', '2020-03-13', '2022-12-31'), ('OOS_23_26', '2023-01-01', '2026-12-31')]

def main():
    E = pd.read_parquet(HERE + '/_ev.parquet')
    S177 = set(pd.read_parquet(SCR + '/out/code_y_akis/res_limit_events.parquet', columns=['stock']).stock)
    # tik maliyeti: VİOP tik 0,01 TL / gerçek fiyat (c_unadj; meta eksikliği için %2 tavan)
    E['tikc'] = np.minimum(0.01 / E.c_unadj, 0.02)
    E['s_fade'] = -E.intra_1
    E['s_fade_x'] = -(E.intra_1 - E.xintra_1)
    E['s_long'] = E.intra_1
    E['s_dr'] = -E.dr2_5 - 4e-4 * 0      # hedge maliyeti ayrıca maliyete eklenecek
    E['s_dr3'] = -E.dr3_6
    E['s_gap'] = E.gap_1
    rows = []; yrows = []
    unis = {'viop47': E.viop, 'all217': E.stock.notna(), 'src177': E.stock.isin(S177), 'liqH': E.liq == 'H', 'all_noIPO': E.age >= 40}
    strat = {
        'b_TC_fade': (E.TC, 's_fade', 0), 'b_TC_fade_xu': (E.TC, 's_fade_x', 4), 'b_TCB_fade': (E.TC_B, 's_fade', 0), 'b_TCS_fade': (E.TC_S, 's_fade', 0),
        'b_TC_notTCL_fade': (E.TC & ~E.TCL, 's_fade', 0), 'b_TCL_fade': (E.TCL, 's_fade', 0),
        'b_TC_openNotLim_fade': (E.TC & (E.Ro_1 < 1.09), 's_fade', 0),
        'c_TU_fade': (E.TU, 's_fade', 0),
        'd_BC_short_fill': (E.BC & (E.BC_1 == False), 's_dr', 4), 'd_BC_short_naive': (E.BC, 's_dr', 4),
        'd_BC_short_alt_t2': (E.BC & (E.BC_1 == True) & (E.BC_2 == False), 's_dr3', 4),
        'd_BCB_short_fill': (E.BC_B & (E.BC_1 == False), 's_dr', 4),
        'ctl_UP6_fade': (E.UP6, 's_fade', 0), 'ctl_DN6_long': (E.DN6, 's_long', 0), 'e_BCL_long': (E.BCL, 's_long', 0),
    }
    for reg in ['P10', 'P20']:
        Er = E[E.reg == reg]
        for un, um in unis.items():
            um = um.reindex(Er.index)
            for sn, (sm, col, hc) in strat.items():
                sub = Er[um & sm.reindex(Er.index).fillna(False)]
                pers = PERIODS if reg == 'P10' else [('P20_ALL', '2015-12-01', '2020-03-10')]
                for pn, a, b in pers:
                    ss = sub[(sub.date >= a) & (sub.date <= b)]
                    for cst in [0, 8, 15, 30]:
                        for tm in ([0, 1] if cst > 0 else [0]):
                            rows.append(dict(reg=reg, uni=un, strat=sn, per=pn, cost=cst + hc, tick=tm, **stat(ss, col, cst + hc, tm)))
                if reg == 'P10':
                    for y, ss in sub.groupby('yr'):
                        r = stat(ss, col, 15 + hc, 0); yrows.append(dict(uni=un, strat=sn, yr=y, cost=15 + hc, **r))
    R = pd.DataFrame(rows); R.to_csv(HERE + '/res_v2_bt.csv', index=False)
    Y = pd.DataFrame(yrows); Y.to_csv(HERE + '/res_v2_byyear.csv', index=False)
    return R, Y

if __name__ == '__main__':
    R, Y = main()
    pd.set_option('display.width', 250); pd.set_option('display.max_columns', 30); pd.set_option('display.max_rows', 500)
    show = R[(R.reg == 'P10') & R.uni.isin(['viop47', 'all217']) & (((R.cost % 100).isin([15, 19])) & (R.tick == 0) | (R.cost == 0))]
    print(show.to_string())
    print(R[(R.reg == 'P20') & (R.cost.isin([0, 15, 19])) & (R.tick == 0) & R.uni.isin(['all217', 'viop47'])].to_string())
