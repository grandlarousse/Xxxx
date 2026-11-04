"""2) Kapanıştan kapanışa sürüm. Sinyal spot kapanışında (z_t), giriş/çıkış aynı gün VİOP uzlaşmasından (lag=0); lag=1 = bir gün gecikmeli uzlaşma.
IS vekili: spot adj kapanıştan kapanışa (2014–2020; aynı gün kapanış dolumu = iyimser). OOS: gerçek VİOP ön vade uzlaşması (2021–2026).
Maliyet: bacak başına gidiş-dönüş c bps + 1 tik/fiyat (VİOP tik 0,01 TL; spot BIST fiyat adımı tablosu). Devir: her bacakta tam gidiş-dönüş."""
import sys; sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_k_sahol_a')
import kl, numpy as np, pandas as pd
kl.use_new_data()
K = kl.signal()
FA, FB = {R: kl.cont('SAHOL', R) for R in [1, 2]}, {R: kl.cont('AKBNK', R) for R in [1, 2]}
pA, pB = kl.spot_px('SAHOL'), kl.spot_px('AKBNK')
EXITS = {'bant_ici(1,5)': dict(exit_z=1.5), 'z<0,5': dict(exit_z=0.5), 'z<0': dict(exit_z=0.0),
         'z<0,5|max5': dict(exit_z=0.5, maxN=5), 'z<0,5|max10': dict(exit_z=0.5, maxN=10), 'z<0,5|max20': dict(exit_z=0.5, maxN=20),
         'z<0|max10': dict(exit_z=0.0, maxN=10), 'bant_ici|max5': dict(exit_z=1.5, maxN=5),
         'sabit1': dict(hold=1), 'sabit2': dict(hold=2), 'sabit3': dict(hold=3), 'sabit5': dict(hold=5), 'sabit10': dict(hold=10)}
PER_S = [('IS spot 2014-20', '2014-01-01', '2021-01-01'), ('spot 2021-26', '2021-01-01', '2027-01-01')]
PER_F = [('VIOP 2017-20', '2017-03-01', '2021-01-01'), ('OOS VIOP 2021-26', '2021-01-01', '2027-01-01'), ('VIOP 2021-23', '2021-01-01', '2024-01-01'), ('VIOP 2024-26', '2024-01-01', '2027-01-01')]
def spot_inputs(c, tick=True):
    idx = K.index
    ta = 1e4 * kl.bist_tick(pA.c.reindex(idx).ffill()) / pA.c.reindex(idx).ffill() if tick else 0
    tb = 1e4 * kl.bist_tick(pB.c.reindex(idx).ffill()) / pB.c.reindex(idx).ffill() if tick else 0
    cA = pd.Series((c + ta) / 1e4, index=idx); cB = pd.Series((c + tb) / 1e4, index=idx)
    return K.z, K.rA, K.rB, K.beta, cA, cB, None
def fut_inputs(c, R=1, tick=True):
    fa, fb = FA[R], FB[R]; idx = fa.index.intersection(fb.index); fa, fb = fa.reindex(idx), fb.reindex(idx)
    z = K.z.reindex(idx); beta = K.beta.reindex(idx)
    ta = 1e4 * 0.01 / fa.F if tick else 0; tb = 1e4 * 0.01 / fb.F if tick else 0
    cA = pd.Series((c + ta) / 1e4, index=idx).ffill(); cB = pd.Series((c + tb) / 1e4, index=idx).ffill()
    return z, fa.r, fb.r, beta, cA, cB, (fa.roll | fb.roll)
if __name__ == '__main__':
    miss = K.index[(K.index >= '2017-03-06')].difference(FA[1].index); print('spot günü olup VİOP bülteni olmayan gün sayısı:', len(miss), list(miss[:8].date))
    rows = []
    for ename, ek in EXITS.items():
        for c in [8, 15, 30]:
            for tick in [True, False] if c == 8 else [True]:
                for lag in [0, 1]:
                    D, T = kl.run_rule(*spot_inputs(c, tick)[:6], roll=None, lag=lag, **ek)
                    for lab, lo, hi in PER_S: rows.append(dict(exit=ename, cost=c, tick=tick, lag=lag, R=None, src='spot', per=lab, **kl.summ(D, T, lo, hi)))
                    for R in ([1, 2] if (lag == 0 and c == 8 and tick) else [1]):
                        z, ra, rb, beta, cA, cB, rl = fut_inputs(c, R, tick)
                        D, T = kl.run_rule(z, ra, rb, beta, cA, cB, roll=rl, lag=lag, **ek)
                        for lab, lo, hi in PER_F: rows.append(dict(exit=ename, cost=c, tick=tick, lag=lag, R=R, src='viop', per=lab, **kl.summ(D, T, lo, hi)))
    G = pd.DataFrame(rows); G.to_csv(kl.HERE + '/res_grid.csv', index=False)
    pd.set_option('display.width', 250); pd.set_option('display.max_rows', 500)
    base = G[(G.tick) & (G.lag == 0) & ((G.R == 1) | G.R.isna())]
    for c in [8, 15, 30]:
        b = base[base.cost == c]
        print(f'\n=== maliyet {c} bps + tik, lag0, R=1: işlem başı net bps (t_işlem) ===')
        tab = b.assign(v=b.net_bps.round(1).astype(str) + ' (' + b.t_trade.round(2).astype(str) + ')').pivot_table(index='exit', columns='per', values='v', aggfunc='first')
        print(tab.reindex(list(EXITS)).to_string())
    b = base[base.cost == 8]
    print('\n=== 8 bps + tik: günlük NW t / yılda işlem / ort. tutma / isabet ===')
    for col in ['t_daily', 'per_yr', 'hold_mean', 'hit', 'ann_bps', 'mdd_bps', 'worst_bps']:
        print('--', col); print(b.pivot_table(index='exit', columns='per', values=col).reindex(list(EXITS)).round(2).to_string())
    print('\n=== lag=1 (bir gün gecikmeli uzlaşma), 8 bps + tik: net bps (t_işlem) ===')
    b = G[(G.tick) & (G.lag == 1) & (G.cost == 8) & ((G.R == 1) | G.R.isna())]
    print(b.assign(v=b.net_bps.round(1).astype(str) + ' (' + b.t_trade.round(2).astype(str) + ')').pivot_table(index='exit', columns='per', values='v', aggfunc='first').reindex(list(EXITS)).to_string())
    print('\n=== devir R=2 vs R=1 (8 bps + tik, lag0), OOS VİOP: net bps / t ===')
    b = G[(G.src == 'viop') & (G.cost == 8) & G.tick & (G.lag == 0) & (G.per == 'OOS VIOP 2021-26')]
    print(b.pivot_table(index='exit', columns='R', values=['net_bps', 't_trade']).reindex(list(EXITS)).round(2).to_string())
    print('\n=== tik etkisi (8 bps, lag0, R1): tiksiz vs tikli net bps ===')
    b = G[(G.cost == 8) & (G.lag == 0) & ((G.R == 1) | G.R.isna())]
    print(b.pivot_table(index='exit', columns=['per', 'tick'], values='net_bps').reindex(list(EXITS)).round(1).to_string())
