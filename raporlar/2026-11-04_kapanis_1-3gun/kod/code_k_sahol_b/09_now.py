import warnings; warnings.filterwarnings('ignore')
import numpy as np, pandas as pd, lb
from scipy.optimize import brentq
df = lb.pair_frame('SAHOL', 'AKBNK')
sig = lb.zsig(df)
print(sig[['ca', 'cb', 'pa', 'pb', 'beta', 'S', 'z']].tail(12).round(4).to_string())
last = df.index[-1]; nxt = pd.Timestamp('2026-11-04')
def z_next(pa_new, pb_new):
    d2 = df.copy()
    d2.loc[nxt] = [pa_new, pb_new, pa_new, pb_new, np.nan, np.nan]
    d2['ra'] = lb.clean_ret(d2.pa); d2['rb'] = lb.clean_ret(d2.pb)
    return lb.zsig(d2).z.iloc[-1]
sa, ak = df.ca.iloc[-1], df.cb.iloc[-1]
print('degismezse 04.11 z:', round(z_next(sa, ak), 3))
for thr in [1.5, -1.5]:
    ps = brentq(lambda p: z_next(p, ak) - thr, sa * 0.92, sa * 1.08)
    pb = brentq(lambda p: z_next(sa, p) - thr, ak * 0.92, ak * 1.08)
    print(f'z={thr:+.1f}: SAHOL {ps:.2f} ({(ps/sa-1)*100:+.2f}%) ya da AKBNK {pb:.2f} ({(pb/ak-1)*100:+.2f}%)')
# VIOP son uzlasmalar
p = lb.panel()
q = p[(p.date == p.date.max()) & p.code.isin(['F_SAHOL1126', 'F_AKBNK1126', 'F_SAHOL1226', 'F_AKBNK1226'])]
print(q[['date', 'code', 'settle', 'value_tl', 'oi']].to_string(index=False))
FS = q.set_index('code').settle
b = sig.beta.iloc[-1]
r = b * FS['F_SAHOL1126'] / FS['F_AKBNK1126']
print(f'beta {b:.4f}, kontrat orani N_AKBNK/N_SAHOL = {r:.3f}; 13 SAHOL -> {13*r:.2f} AKBNK; 1 SAHOL -> {max(1,round(r))}')
# basis/carry
print('baz SAHOL %.2f%%, AKBNK %.2f%% (spot 03.11 kapanis)' % ((FS['F_SAHOL1126'] / sa - 1) * 100, (FS['F_AKBNK1126'] / ak - 1) * 100))
