"""Veri madenciliği: 105'lik ızgara (pencere x eşik x β) SAHOL/AKBNK ve korelasyon-eşli 42 plasebo çiftte.
IS'te en iyi parametreyi seç -> OOS t (dürüst seçim). Histerezisli çıkış alt ızgarası."""
import vb, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
WINS = [20, 30, 40, 60, 90, 120, 250]; THRS = [1.0, 1.25, 1.5, 1.75, 2.0]; BETAS = ['b1', 'b120', 'b250']
def grid(a, b, cost=8):
    out = []
    for bt in BETAS:
        P = vb.pair_inputs(a, b, betawin=120 if bt == 'b120' else 250, beta1=(bt == 'b1'))
        for w in WINS:
            z = vb.zscore(P['S'], w)
            for th in THRS:
                d = vb.pnl_open(vb.positions(z, th), P['A']['gap'], P['A']['intra'], P['B']['gap'], P['B']['intra'], P['beta'], cost)
                tb = vb.table(d)
                out.append(dict(a=a, b=b, beta=bt, win=w, thr=th, IS_t=tb.loc['IS', 't'], OOS_t=tb.loc['OOS', 't'], IS_bps=tb.loc['IS', 'bps'], OOS_bps=tb.loc['OOS', 'bps'],
                                t1417=tb.loc['2014-17', 't'], t1820=tb.loc['2018-20', 't'], t2123=tb.loc['2021-23', 't'], t2426=tb.loc['2024-26', 't']))
    return pd.DataFrame(out)
if __name__ == '__main__':
    g = grid('SAHOL', 'AKBNK'); g.to_csv('res_grid_sahol.csv', index=False)
    print('SAHOL/AKBNK 105 spesifikasyon: OOS t medyan', g.OOS_t.median().round(2), ' %>2', (g.OOS_t > 2).mean().round(2), ' %>0', (g.OOS_t > 0).mean().round(2), ' IS t medyan', g.IS_t.median().round(2), ' %IS>2', (g.IS_t > 2).mean().round(2))
    print(g.pivot_table(index='win', columns='beta', values='OOS_t', aggfunc='median').round(2).to_string())
    print(g.pivot_table(index='win', columns='beta', values='IS_t', aggfunc='median').round(2).to_string())
    print('alt dönem t medyanları (105 spes.):', g[['t1417', 't1820', 't2123', 't2426']].median().round(2).to_dict(), ' >0 oranı', (g[['t1417', 't1820', 't2123', 't2426']] > 0).mean().round(2).to_dict())
    bi = g.loc[g.IS_t.idxmax()]; print('IS-en iyi spes.:', bi[['beta', 'win', 'thr', 'IS_t', 'OOS_t', 'OOS_bps']].to_dict())
    top5 = g.nlargest(5, 'IS_t'); print('IS ilk 5 spes. OOS t:', top5[['beta', 'win', 'thr', 'IS_t', 'OOS_t']].round(2).to_string())
    # korelasyon eşli plasebo çiftleri
    U = pd.read_csv('res_universe.csv'); cs = U[(U.a == 'SAHOL') & (U.b == 'AKBNK')]['corr'].iloc[0]
    M = U[(U['corr'] > cs - 0.1) & (U['corr'] < cs + 0.1) & ~((U.a.isin(['SAHOL', 'AKBNK'])) & (U.b.isin(['SAHOL', 'AKBNK'])))]
    rows = []
    for a, b in zip(M.a, M.b):
        gg = grid(a, b); bi2 = gg.loc[gg.IS_t.idxmax()]
        rows.append(dict(a=a, b=b, med_OOS=gg.OOS_t.median(), frac_OOS2=(gg.OOS_t > 2).mean(), med_IS=gg.IS_t.median(), ISbest_IS=bi2.IS_t, ISbest_OOS=bi2.OOS_t, max_OOS=gg.OOS_t.max()))
    Rr = pd.DataFrame(rows); Rr.to_csv('res_grid_placebo.csv', index=False)
    print(f'plasebo {len(Rr)} çift: medyan OOS t (ızgara medyanı) ort {Rr.med_OOS.mean():.2f}, en yüksek {Rr.med_OOS.max():.2f};  %OOS>2 ort {Rr.frac_OOS2.mean():.2f}, en yüksek {Rr.frac_OOS2.max():.2f}')
    print(f'   IS-seçimli OOS t: ort {Rr.ISbest_OOS.mean():.2f}, sd {Rr.ISbest_OOS.std():.2f}, max {Rr.ISbest_OOS.max():.2f};  ızgara max OOS t ort {Rr.max_OOS.mean():.2f}, en yüksek {Rr.max_OOS.max():.2f}')
    print(Rr.sort_values('med_OOS', ascending=False).head(6).round(2).to_string())
    # histerezisli çıkış (SAHOL/AKBNK, seçili alt ızgara)
    rows = []
    for bt in ['b1', 'b250']:
        P = vb.pair_inputs('SAHOL', 'AKBNK', beta1=(bt == 'b1'))
        for w in [20, 40, 60, 120]:
            z = vb.zscore(P['S'], w)
            for th in [1.5, 2.0]:
                for ex in [0.0, 0.5]:
                    d = vb.pnl_open(vb.positions(z, th, exit_=ex), P['A']['gap'], P['A']['intra'], P['B']['gap'], P['B']['intra'], P['beta'], 8); tb = vb.table(d)
                    rows.append(dict(beta=bt, win=w, thr=th, exit=ex, IS_t=tb.loc['IS', 't'], OOS_t=tb.loc['OOS', 't'], OOS_bps=tb.loc['OOS', 'bps']))
    H = pd.DataFrame(rows); print('histerezis alt ızgarası (16x2):'); print(H.round(2).to_string()); H.to_csv('res_grid_hyst.csv', index=False)
