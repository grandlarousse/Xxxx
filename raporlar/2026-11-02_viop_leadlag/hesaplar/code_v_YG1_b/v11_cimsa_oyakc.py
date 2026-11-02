"""v11: CIMSA / OYAKC çürütme testleri: alt dönemler, yön, sepet-hedge, uç değer, plasebo, seçim (IS sırası), h1 girişleri, SSF uzak-gün."""
import numpy as np, pandas as pd, vb
rng = np.random.default_rng(3)
fr = pd.read_pickle('res/panel.pkl'); S = vb.S47
G = vb.wide(fr, 'gap')['2014':][S]; I = vb.wide(fr, 'intra')['2014':][S]
B = pd.read_pickle('res/basket.pkl'); gbl, ibl = B['gbl'].reindex(G.index), B['ibl'].reindex(G.index)
HB = I - ibl
st = pd.read_csv('res/v1_stock.csv', index_col=0)
st['rkIS_t'] = st.tIS.rank(ascending=False); st['rkIS'] = st.IS.rank(ascending=False); st['rkOOS'] = st.OOS.rank(ascending=False)
print(st.loc[['CIMSA', 'OYAKC'], ['IS', 'tIS', 'rkIS', 'rkIS_t', 'OOS', 'tOOS', 'rkOOS']].round(2))
# IS'te seçilen hisselerin OOS performansı (seçim yanlılığı olmadan)
for k in [2, 5, 10, 14]:
    top = st.sort_values('tIS', ascending=False).index[:k]
    r = (-np.sign(G[top]).where(G[top].abs() > 0.01) * I[top] * 1e4).loc['2021':]
    d = r.mean(axis=1).dropna(); print(f'IS t sırasına göre ilk {k}: {list(top)[:5]}... OOS DW {d.mean():.1f} (t {vb.tstat(d):.2f})')
h1 = pd.read_pickle('res/h1.pkl')
def rep(s):
    g = G[s]; i = I[s] * 1e4; hb = HB[s] * 1e4
    sg = -np.sign(g).where(g.abs() > 0.01)
    r = (sg * i).dropna(); rh = (sg * hb).dropna()
    print(f'\n===== {s}: n {len(r)}')
    for p in ['14-17', '18-20', '21-23', '24-26', 'IS', 'OOS']:
        a, b = vb.PERIODS[p]; x = r.loc[a:b]; xh = rh.loc[a:b]
        up = x[g.reindex(x.index) > 0]; dn = x[g.reindex(x.index) < 0]
        print(f'  {p}: ham {x.mean():6.1f} (t {vb.tstat(x):5.2f}, n {len(x)}) | sepet-hedge {xh.mean():6.1f} (t {vb.tstat(xh):5.2f}) | up {up.mean():6.1f} (t {vb.tstat(up):4.1f}) down {dn.mean():6.1f} (t {vb.tstat(dn):4.1f}) | medyan {x.median():6.1f} pozitif %{100*(x>0).mean():.0f}')
    for p in ['IS', 'OOS']:
        a, b = vb.PERIODS[p]; x = r.loc[a:b].sort_values()
        print(f'  {p} uç: en iyi 5 hariç {x.iloc[:-5].mean():.1f} (t {vb.tstat(x.iloc[:-5]):.2f}) | en iyi 10 hariç {x.iloc[:-10].mean():.1f} (t {vb.tstat(x.iloc[:-10]):.2f}) | %1-99 winsor {x.clip(*x.quantile([.01,.99])).mean():.1f} | |gap|<=%3 {r.loc[a:b][g.loc[a:b].abs()<=0.03].mean():.1f} (t {vb.tstat(r.loc[a:b][g.loc[a:b].abs()<=0.03]):.2f}) | |gap|>%3 {r.loc[a:b][g.loc[a:b].abs()>0.03].mean():.1f} (n {(g.loc[a:b].abs()>0.03).sum()})')
    # plasebo: bayat sinyal
    out = []
    for lag in [1, 2, 3, 5]:
        x = (-np.sign(g.shift(lag)).where(g.shift(lag).abs() > 0.01) * i)
        out.append(f'L{lag}: IS {x.loc[:"2020"].mean():.1f} ({vb.tstat(x.loc[:"2020"]):.1f}) OOS {x.loc["2021":].mean():.1f} ({vb.tstat(x.loc["2021":]):.1f})')
    print('  bayat sinyal:', ' ; '.join(out))
    # dairesel kaydırma nulli (OOS ortalama)
    sv = sg.values; iv = i.values; N = len(sv); real = np.nanmean((sv * iv)[G.index >= '2021-01-01'])
    nul = [np.nanmean((np.roll(sv, rng.integers(21, N - 21)) * iv)[G.index >= '2021-01-01']) for _ in range(2000)]
    print(f'  kaydırma nulli OOS: gerçek {real:.1f}, null ort {np.mean(nul):.1f} sd {np.std(nul):.1f}, p {(np.array(nul) >= real).mean():.4f}')
    # h1
    L = h1['legs']; Hd = h1['Hd']; g0 = h1['G'][s]; g1 = h1['G1030'][s]
    s0 = -np.sign(g0).where(g0.abs() > 0.01); s1 = -np.sign(g1).where(g1.abs() > 0.01)
    for a, b in [('2023-11-30', '2025-04-30'), ('2025-05-01', '2026-12-31'), ('2023-11-30', '2026-12-31')]:
        parts = []
        for k in ['O_C', 'O_1030', 'TP0_C', '1030_C']:
            x = (s0 * L[k][s] * 1e4).loc[a:b].dropna(); parts.append(f'{k} {x.mean():.1f} ({vb.tstat(x):.1f})')
        x = (s1 * L['1030_C'][s] * 1e4).loc[a:b].dropna(); parts.append(f'sinyal@10:30 1030_C {x.mean():.1f} ({vb.tstat(x):.1f}, n {len(x)})')
        print(f'  h1 {a[:7]}..{b[:7]}: n {s0.loc[a:b].notna().sum()} | ' + ' | '.join(parts))
for s in ['CIMSA', 'OYAKC']: rep(s)
