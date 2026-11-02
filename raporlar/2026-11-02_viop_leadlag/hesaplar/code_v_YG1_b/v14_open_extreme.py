"""v14: açılış fiyatı günün uç noktası mı? (short için O==H, long için O==L) — sürekli işlemde O'dan ya da daha iyisinden hiç işlem olmamış.
Bu günlerin fade P&L payı ve hariç tutulunca kalan."""
import numpy as np, pandas as pd, vb
fr = pd.read_pickle('res/panel.pkl'); S = vb.S47
G = vb.wide(fr, 'gap')['2014':][S]; I = vb.wide(fr, 'intra')['2014':][S]
O = vb.wide(fr, 'o')['2014':][S]; H = vb.wide(fr, 'h')['2014':][S]; Lw = vb.wide(fr, 'l')['2014':][S]
B = pd.read_pickle('res/basket.pkl'); gbl, ibl = B['gbl'].reindex(G.index), B['ibl'].reindex(G.index)
tick = 0.0
for nm, g, r in [('ham both', G, I), ('idio-UP sepet-hedge', (G - gbl).where((G - gbl) > 0), I - ibl), ('ham up', G.where(G > 0), I), ('ham down', G.where(G < 0), I)]:
    s = -np.sign(g).where(g.abs() > 0.01)
    ext = ((s < 0) & (O >= H * (1 - 1e-6))) | ((s > 0) & (O <= Lw * (1 + 1e-6)))
    x = s * r * 1e4
    for per in ['IS', 'OOS', '24-26']:
        a, b = vb.PERIODS[per]
        xx = x.loc[a:b]; ee = ext.loc[a:b]
        st = xx.stack().dropna(); e = ee.stack().reindex(st.index).fillna(False).astype(bool)
        d_all = xx.mean(axis=1).dropna(); d_ex = xx.where(~ee).mean(axis=1).dropna()
        print(f'{nm} {per}: açılış=uç oranı %{100*e.mean():.1f}, bu işlemlerin ort {st[e].mean():.0f} bps, P&L payı %{100*st[e].sum()/st.sum():.0f} | DW tümü {d_all.mean():.1f} (t {vb.tstat(d_all):.2f}) -> açılış=uç hariç {d_ex.mean():.1f} (t {vb.tstat(d_ex):.2f}) | TW hariç {st[~e].mean():.1f}')

print('\n--- null (dairesel kaydırılmış sinyal, 200 tekrar): aynı "açılış=uç hariç" filtresi rastgele günlerde ne verir?')
rng = np.random.default_rng(9); N = len(G); oos = G.index >= '2021-01-01'
Ov, Hv, Lv = O.values, H.values, Lw.values
for nm, g, r in [('ham both', G, I), ('idio-UP sepet-hedge', (G - gbl).where((G - gbl) > 0), I - ibl)]:
    sv = (-np.sign(g).where(g.abs() > 0.01)).values; rv = r.values * 1e4
    def stat(s):
        ext = ((s < 0) & (Ov >= Hv * (1 - 1e-6))) | ((s > 0) & (Ov <= Lv * (1 + 1e-6)))
        x = s * rv; xe = np.where(ext, np.nan, x)
        with np.errstate(all='ignore'):
            out = []
            for msk in [~oos, oos]:
                d1 = np.nanmean(x[msk], axis=1); d2 = np.nanmean(xe[msk], axis=1)
                out += [np.nanmean(d1), np.nanmean(d2), np.nanmean(ext[msk][~np.isnan(x[msk])])]
        return out
    real = stat(sv)
    nul = np.array([stat(np.column_stack([np.roll(sv[:, j], rng.integers(21, N - 21)) for j in range(len(S))])) for _ in range(200)])
    print(f'{nm}: IS gerçek {real[0]:.1f} -> hariç {real[1]:.1f} (uç oranı %{100*real[2]:.1f}) | null {nul[:,0].mean():.1f} -> hariç {nul[:,1].mean():.1f} (uç %{100*nul[:,2].mean():.1f}); hariç fark {real[1]-nul[:,1].mean():.1f} (null sd {nul[:,1].std():.1f})')
    print(f'      OOS gerçek {real[3]:.1f} -> hariç {real[4]:.1f} (uç %{100*real[5]:.1f}) | null {nul[:,3].mean():.1f} -> hariç {nul[:,4].mean():.1f} (uç %{100*nul[:,5].mean():.1f}); hariç fark {real[4]-nul[:,4].mean():.1f} (null sd {nul[:,4].std():.1f})')
