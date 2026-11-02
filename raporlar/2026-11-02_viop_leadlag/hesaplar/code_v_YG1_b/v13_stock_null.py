"""v13: '%87 hisse pozitif' iddiasının null'u (dairesel kaydırma) ve sepet-hedge'li hisse bazında medyan/pozitif/FDR."""
import numpy as np, pandas as pd, vb
from scipy import stats
rng = np.random.default_rng(5)
fr = pd.read_pickle('res/panel.pkl'); S = vb.S47
G = vb.wide(fr, 'gap')['2014':][S]; I = vb.wide(fr, 'intra')['2014':][S]
B = pd.read_pickle('res/basket.pkl'); gbl, ibl = B['gbl'].reindex(G.index), B['ibl'].reindex(G.index)
oos = G.index >= '2021-01-01'; N = len(G)
for nm, g, r in [('ham', G, I), ('sepet-hedge (ham gap sinyali)', G, I - ibl), ('idio sinyal + sepet-hedge', G - gbl, I - ibl)]:
    sv = (-np.sign(g).where(g.abs() > 0.01)).values; rv = r.values * 1e4
    x = sv * rv
    m = np.nanmean(x[oos], axis=0); sd = np.nanstd(x[oos], axis=0, ddof=1); n = np.sum(~np.isnan(x[oos]), axis=0)
    t = m / (sd / np.sqrt(n)); p = 2 * stats.t.sf(np.abs(t), n - 1)
    mi = np.nanmean(x[~oos], axis=0)
    nul_med, nul_pos = [], []
    for it in range(300):
        sh = np.column_stack([np.roll(sv[:, j], rng.integers(21, N - 21)) for j in range(len(S))])
        y = sh * rv; mm = np.nanmean(y[oos], axis=0)
        nul_med.append(np.nanmedian(mm)); nul_pos.append(np.nanmean(mm > 0))
    print(f'{nm}: OOS hisse medyanı {np.nanmedian(m):.1f}, pozitif %{100*np.nanmean(m>0):.0f}, FDR(OOS) {vb.bh(p).sum()}/47, |t|>2 {int((t>2).sum())} | IS&OOS ikisi de >0: {int(((m>0)&(mi>0)).sum())} | null: medyan {np.mean(nul_med):.1f} (p95 {np.quantile(nul_med,.95):.1f}), pozitif %{100*np.mean(nul_pos):.0f} (p95 %{100*np.quantile(nul_pos,.95):.0f})')
