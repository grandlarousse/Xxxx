"""Kapanış/açılış fiyatı gürültüsü (bid-ask sıçraması) kontrolü: sinyali kapanış yerine tipik fiyat (h+l+c)/3 veya 17:30 TSİ saatlik fiyattan üret;
giriş t+1 10:30 (h1). Ayrıca evrende tam dönem t ve BH-FDR."""
import sys; HERE = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_YR1_a'; sys.path.insert(0, HERE)
exec(open(HERE + '/03_ratio_alt.py').read().split("if __name__ == '__main__':")[0])
from scipy import stats as sst
P = pair('SAHOL', 'AKBNK'); idx = P['idx']; beta = P['beta']
def sig_from_price(pa, pb, w=60, thr=1.5):
    ra = np.log(pa).diff().reindex(idx); rb = np.log(pb).diff().reindex(idx)
    ra[bad(ra.fillna(0))] = np.nan; rb[bad(rb.fillna(0))] = np.nan
    S = (ra - beta * rb).fillna(0).cumsum(); return positions(zscore(S, w), thr)
da, db = raw('SAHOL'), raw('AKBNK')
adjf_a, adjf_b = da['adj'] / da['c'], db['adj'] / db['c']
tp_a, tp_b = (da['h'] + da['l'] + da['c']) / 3 * adjf_a, (db['h'] + db['l'] + db['c']) / 3 * adjf_b
rows = []
def rec(lab, pos, g=P['g'], i=P['i'], pers=(('IS', '2014-01-01', SPLIT), ('OOS', SPLIT, '2027-01-01'), ('H1', '2023-12-01', '2027-01-01'))):
    sim = simulate(pos, g, i, P['c'], P['lw'], 'open', 8); o = dict(lab=lab)
    for p, lo, hi in pers:
        s = summarize(sim, lo, hi); o[f'{p}_m'] = s['mean_bps']; o[f'{p}_t'] = s['t_all']; o[f'{p}_n'] = s['n_act']
    rows.append(o)
pos_c = positions(zscore(P['S'], 60), 1.5)
pos_tp = sig_from_price(tp_a, tp_b)
rec('sinyal: kapanış (temel), giriş açılış', pos_c)
rec('sinyal: tipik fiyat (h+l+c)/3, giriş açılış', pos_tp)
# saatlik: 17:30 TSİ = 14:00 UTC bitişli bar (13:30 başlangıç)
h17a, h17b = h1_px('SAHOL', '14:30'), h1_px('AKBNK', '14:30')
p1030a, p1030b = h1_px('SAHOL', '07:30'), h1_px('AKBNK', '07:30')
ia = np.log(da['c'] / p1030a.reindex(da.index)).reindex(idx); ib = np.log(db['c'] / p1030b.reindex(db.index)).reindex(idx)
i2 = ia - beta * ib; g2 = P['c'] - i2; m = i2.notna()
# 17:00 sinyali: S'nin son gününü 17:00 fiyatıyla değiştir: z_t = (S_{t-1} + s17_t - mean)/std (pencere istatistikleri kapanış S'inden, t-1'e kadar)
S = P['S']; s17 = (np.log(h17a.reindex(idx) / da['adj'].reindex(idx).shift(1) * adjf_a.reindex(idx)) - beta * np.log(h17b.reindex(idx) / db['adj'].reindex(idx).shift(1) * adjf_b.reindex(idx)))
S17 = S.shift(1) + s17
mu = S.shift(1).rolling(59, min_periods=30).mean(); sd = S.shift(1).rolling(59, min_periods=30).std()
z17 = ((S17 - mu) / sd).where(s17.notna())
pos17 = positions(z17, 1.5)
H = (('H1', '2023-12-01', '2027-01-01'),)
rec('[H1] sinyal kapanış, giriş 10:30', pos_c.where(m.reindex(idx).fillna(False) | True), g2.where(m), i2.where(m), H)
rec('[H1] sinyal 17:30 TSİ, giriş kapanış t (close0)', pos17, pers=H)
sim17 = simulate(pos17, P['g'], P['i'], P['c'], P['lw'], 'close0', 8); s = summarize(sim17, '2023-12-01', '2027-01-01'); rows.append(dict(lab='[H1] sinyal 17:30, giriş aynı gün kapanış (gerçekçi: 17:30 sonrası VİOP)', H1_m=s['mean_bps'], H1_t=s['t_all'], H1_n=s['n_act']))
sim17b = simulate(pos17, g2.where(m), i2.where(m), P['c'], P['lw'], 'open', 8); s = summarize(sim17b, '2023-12-01', '2027-01-01'); rows.append(dict(lab='[H1] sinyal 17:30, giriş t+1 10:30', H1_m=s['mean_bps'], H1_t=s['t_all'], H1_n=s['n_act']))
pd.set_option('display.width', 250); print(pd.DataFrame(rows).round(2).to_string())
print('pozisyon uyumu kapanış vs tipik fiyat sinyali:', round(((pos_c != 0) == (pos_tp != 0))[idx >= '2014-01-01'].mean(), 3))
# evren: tam dönem t ve BH
U = pd.read_csv(HERE + '/res_ratio_universe.csv')
U = U[(U.IS_n >= 150) & (U.OOS_n >= 150)].copy()
U['t_full'] = (U.IS_t * np.sqrt(U.IS_n) + U.OOS_t * np.sqrt(U.OOS_n)) / np.sqrt(U.IS_n + U.OOS_n)  # yaklaşık birleşik t
U['p'] = 2 * (1 - sst.norm.cdf(U.t_full.abs()))
from statsmodels.stats.multitest import multipletests
U['rej'] = multipletests(U.p, alpha=0.05, method='fdr_bh')[0]
print('evren yönlü çift', len(U), ' BH q=0,05 geçen:', U[U.rej][['A', 'B', 'IS_t', 'OOS_t', 't_full']].round(2).to_string())
