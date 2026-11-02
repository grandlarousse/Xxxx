"""v4: plasebolar — (a) bayatlatılmış sinyal gap_{t-k}, (b) hisse içi dairesel kaydırma (tarih karıştırma) nulli,
(c) rastgele çift: başka hissenin gap'iyle bu hissenin gün-içini fade, (d) çapraz/ortak faktör: kendi vs diğerleri."""
import numpy as np, pandas as pd, vb
rng = np.random.default_rng(7)
fr = pd.read_pickle('res/panel.pkl'); S = vb.S47
G = vb.wide(fr, 'gap')['2014':]; I = vb.wide(fr, 'intra')['2014':]
gx, ix = G.pop('XU030'), I.pop('XU030'); G, I = G[S], I[S]
B = pd.read_pickle('res/basket.pkl'); gbl, ibl = B['gbl'].reindex(G.index), B['ibl'].reindex(G.index)
IDG = G - gbl; HB = I - ibl
XS = I.sub(I.mean(axis=1), axis=0)
def sig(gs, leg='both', thr=0.01):
    s = -np.sign(gs).where(gs.abs() > thr)
    if leg == 'up': s = s.where(gs > 0)
    if leg == 'down': s = s.where(gs < 0)
    return s
def dw(r, a, b):
    x = r.loc[a:b].mean(axis=1).dropna(); return x.mean(), vb.tstat(x)
def tw(r, a, b):
    st = r.loc[a:b].stack().dropna(); m, t, n = vb.clus_t(st.values, st.index.get_level_values(0)); return m, t
cases = {'raw_both': (G, I, 'both'), 'raw_up': (G, I, 'up'), 'raw_down': (G, I, 'down'),
         'idioB_both': (IDG, HB, 'both'), 'idioB_up': (IDG, HB, 'up')}
print('(a) bayatlatılmış sinyal: gap_{t-k} -> intra_t (DW bps, t) IS | OOS')
for k, (gs, ret, leg) in cases.items():
    out = []
    for lag in [0, 1, 2, 3, 5, 10]:
        r = sig(gs.shift(lag), leg) * ret * 1e4
        a = dw(r, '2014', '2020'); b = dw(r, '2021', '2026')
        out.append(f'L{lag}: {a[0]:.1f}({a[1]:.1f}) | {b[0]:.1f}({b[1]:.1f})')
    print(k, ' ; '.join(out))
print('\n(b) hisse içi dairesel kaydırma nulli (offset 21..N-21, 500 tekrar), OOS ve IS DW ortalaması')
Gv, Iv = {}, {}
for k in ['raw_both', 'raw_up', 'idioB_up']:
    gs, ret, leg = cases[k]
    S0 = sig(gs, leg)
    real_is = dw(S0 * ret * 1e4, '2014', '2020')[0]; real_oos = dw(S0 * ret * 1e4, '2021', '2026')[0]
    sv = S0.values; rv = ret.values * 1e4; N = sv.shape[0]
    idx_oos = G.index >= '2021-01-01'
    nul_is, nul_oos = [], []
    for it in range(500):
        sh = np.empty_like(sv)
        for j in range(sv.shape[1]):
            sh[:, j] = np.roll(sv[:, j], rng.integers(21, N - 21))
        pr = sh * rv
        with np.errstate(all='ignore'):
            d = np.nanmean(pr, axis=1)
        nul_is.append(np.nanmean(d[~idx_oos])); nul_oos.append(np.nanmean(d[idx_oos]))
    nul_is, nul_oos = np.array(nul_is), np.array(nul_oos)
    print(f'{k}: gerçek IS {real_is:.1f} null ort {nul_is.mean():.1f} sd {nul_is.std():.1f} p {(nul_is>=real_is).mean():.3f} | gerçek OOS {real_oos:.1f} null ort {nul_oos.mean():.1f} sd {nul_oos.std():.1f} p {(nul_oos>=real_oos).mean():.3f}')
print('\n(c) rastgele çift: hisse j\'nin gap sinyaliyle hisse i\'nin gün-içi (i!=j), 300 rastgele eşleme; OOS DW')
for retname, ret in [('raw', I), ('XS', XS)]:
    for leg in ['both', 'up']:
        S0 = sig(G, leg); own = dw(S0 * ret * 1e4, '2021', '2026')[0]; own_is = dw(S0 * ret * 1e4, '2014', '2020')[0]
        vals, vals_is = [], []
        for it in range(300):
            perm = rng.permutation(len(S))
            while np.any(perm == np.arange(len(S))): perm = rng.permutation(len(S))
            Sp = pd.DataFrame(S0.values[:, perm], index=S0.index, columns=S)
            r = Sp * ret * 1e4
            vals.append(dw(r, '2021', '2026')[0]); vals_is.append(dw(r, '2014', '2020')[0])
        vals = np.array(vals); vals_is = np.array(vals_is)
        print(f'{retname} {leg}: kendi IS {own_is:.1f} çift-ort IS {vals_is.mean():.1f} (sd {vals_is.std():.1f}) | kendi OOS {own:.1f} çift-ort OOS {vals.mean():.1f} (sd {vals.std():.1f}, max {vals.max():.1f})')
print('\n(d) TW (gün kümelenmiş t): kendi vs bayat L1, L2')
for k, (gs, ret, leg) in cases.items():
    for lag in [0, 1, 2]:
        r = sig(gs.shift(lag), leg) * ret * 1e4
        a = tw(r, '2014', '2020'); b = tw(r, '2021', '2026')
        print(f'{k} L{lag}: IS {a[0]:.1f} ({a[1]:.2f}) OOS {b[0]:.1f} ({b[1]:.2f})')
