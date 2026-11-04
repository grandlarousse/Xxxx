"""1) Kaynağın kuralını aynen yeniden üret (spot, t+1 açılış girişi). (a) kaynak muhasebesi (09_bt.persistent + stats),
(b) v_YR1_b 'doğru muhasebe' (vb.pnl_open: çıkış günü gap'i + çıkış maliyeti). Ortak veri, son gün 30.10.2026."""
import sys; sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_y_grup')
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_k_sahol_a")
sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_YR1_b')
from gx import *
import kl
# --- 09_bt.py'den aynen (persistent, stats)
def stats(pnl, pos):
    out = {}
    for lab, lo, hi in [('ALL', '2014-01-01', '2027-01-01'), ('IS', '2014-01-01', SPLIT), ('OOS', SPLIT, '2027-01-01')]:
        p = pnl[(pnl.index >= pd.Timestamp(lo)) & (pnl.index < pd.Timestamp(hi))].dropna(); ps = pos.reindex(p.index).fillna(0)
        act = ps != 0; n = int(act.sum())
        m_, t_, _ = ll.nw_t(p[act], lags=5)
        out[lab] = {'n': n, 'mean_bps': round(1e4 * p[act].mean(), 1), 't': round(t_, 2)}
    return out
def persistent(z, gap, intra, cost_bps, legs, thr=1.0):
    df = pd.concat([z.rename('z'), gap.rename('g'), intra.rename('i')], axis=1).dropna(subset=['g', 'i'])
    pos = (-np.sign(df['z'])).where(df['z'].abs() > thr, 0.0).fillna(0.0)
    p1 = pos.shift(1).fillna(0); p2 = pos.shift(2).fillna(0)
    pnl = p2 * df['g'] + p1 * df['i'] - (cost_bps / 1e4) / 2 * legs * (p1 - p2).abs() * 2 / 2
    return pnl, p1
a, bb = 'SAHOL', 'AKBNK'
ra, rb = R(a), R(bb); da, db = DC(a), DC(bb)
beta = (ra.rolling(250, min_periods=120).cov(rb) / rb.rolling(250, min_periods=120).var()).shift(1)
s = (ra - beta * rb); S_ = s.fillna(0).cumsum()
z = (S_ - S_.rolling(60, min_periods=30).mean()) / S_.rolling(60, min_periods=30).std()
sg = da['gap'] - beta * db['gap']; si = da['intra'] - beta * db['intra']
print('(a) KAYNAK muhasebesi (09_bt BT3, z60>1,5, t+1 açılış):')
for c in [8, 15]:
    pnl, pos = persistent(z, sg, si, c, 2, thr=1.5); print('  ', c, 'bps', stats(pnl, pos))
src = pd.read_csv(HERE + '/res_bt.csv'); src = src[(src.bt == 'BT3') & (src.name == 'SAHOL/AKBNK') & (src.target.str.contains('z60'))]
print('   res_bt.csv:', src[['cost', 'n_IS', 'mean_IS', 't_IS', 'n_OOS', 'mean_OOS', 't_OOS']].round(2).to_dict('records'))
# kl.signal aynı z'yi veriyor mu?
K = kl.signal(last=kl.LAST_SHARED)
zz = pd.concat([z, K.z], axis=1).dropna(); print('   kl.signal z ile max fark:', float((zz.iloc[:, 0] - zz.iloc[:, 1]).abs().max()))
# --- (b) doğru muhasebe (vb)
import vb
P = vb.pair_inputs('SAHOL', 'AKBNK'); zb = vb.zscore(P['S'], 60); posb = vb.positions(zb, 1.5)
print('(b) v_YR1_b doğru muhasebe (bps/maruz gün, t):')
for c in [8, 15, 30]:
    d = vb.pnl_open(posb, P['A']['gap'], P['A']['intra'], P['B']['gap'], P['B']['intra'], P['beta'], c)
    tb = vb.table(d)
    print('  ', c, 'bps', {k: (round(tb.loc[k, 'bps'], 1), round(tb.loc[k, 't'], 2)) for k in ['IS', 'OOS']})
zc = pd.concat([zb.rename('vb'), K.z.rename('kl')], axis=1).dropna(); print('   vb z ile korelasyon', round(zc.corr().iloc[0, 1], 4), ' işaret uyumu |z|>1,5:', round(((zc.vb.abs() > 1.5) == (zc.kl.abs() > 1.5)).mean(), 4))
