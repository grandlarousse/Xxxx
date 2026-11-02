"""v6: fiyat marjı (tavan/taban) kesilmesi — tavana yakın açılışta gün-içi getiri yukarıdan sınırlı -> mekanik pozitif fade.
Ham fiyatla: açılış / önceki kapanış oranı, limit L'ye 1 puandan yakın mı? Kapanış tavanda/tabanda kilitli mi (çıkış dolumu riski)?"""
import numpy as np, pandas as pd, vb
fr = pd.read_pickle('res/panel.pkl'); S = vb.S47
rows = []
for s in S:
    d = fr[s]['2014':]
    L = np.where(d.index < vb.REG, 0.20, 0.10)
    rg = d.o / d.c.shift() - 1  # ham açılış oranı (temettü günlerinde kayık ama az)
    rc = d.c / d.c.shift() - 1
    near = (rg.abs() >= L - 0.01)
    lockC = (rc.abs() >= L - 0.005)
    x = pd.DataFrame({'gap': d.gap, 'intra': d.intra, 'near': near, 'lockC': lockC, 'h': d.h, 'l': d.l, 'o': d.o, 'c': d.c, 'sym': s})
    x = x[x.gap.abs() > 0.01]
    rows.append(x)
X = pd.concat(rows); X['fade'] = -np.sign(X.gap) * X.intra * 1e4
X['oos'] = X.index >= '2021-01-01'
X['onlimit_all_day'] = X.near & (X.h == X.l)
print('|gap|>%1 işlemleri:', len(X))
for oos in [False, True]:
    Y = X[X.oos == oos]
    print('OOS' if oos else 'IS', 'tavan/tabana 1 puan yakın açılış oranı', round(Y.near.mean(), 4), 'n', int(Y.near.sum()),
          'bu işlemlerin fade ort', round(Y.loc[Y.near, 'fade'].mean(), 1), 'pozitif oranı', round((Y.loc[Y.near, 'fade'] >= 0).mean(), 2),
          '| kapanış kilitli (çıkış riski) oranı', round(Y.lockC.mean(), 4), 'gün boyu kilitli', int(Y.onlimit_all_day.sum()))
    tot = Y.fade.sum(); print('   limit-yakın işlemlerin toplam fade P&L payı', round(Y.loc[Y.near, 'fade'].sum() / tot, 3), '| ham TW tümü', round(Y.fade.mean(), 1), 'limit-yakın hariç', round(Y.loc[~Y.near, 'fade'].mean(), 1))
# DW, limit-yakın hariç
fr2 = {}
G = vb.wide(fr, 'gap')['2014':][S]; I = vb.wide(fr, 'intra')['2014':][S]
C = vb.wide(fr, 'c')['2014':][S]; O = vb.wide(fr, 'o')['2014':][S]
Lm = pd.Series(np.where(G.index < vb.REG, 0.20, 0.10), index=G.index)
near = (O / C.shift() - 1).abs().ge(Lm - 0.01, axis=0)
B = pd.read_pickle('res/basket.pkl'); gbl, ibl = B['gbl'].reindex(G.index), B['ibl'].reindex(G.index)
IDG = G - gbl; HB = (I - ibl) * 1e4
for nm, s, r in [('raw_both', -np.sign(G).where(G.abs() > 0.01), I * 1e4), ('raw_up', -np.sign(G).where(G > 0.01), I * 1e4),
                 ('idioB_up', -np.sign(IDG).where(IDG > 0.01), HB), ('idioB_both', -np.sign(IDG).where(IDG.abs() > 0.01), HB)]:
    for tag, ss in [('tüm', s), ('limit-yakın hariç', s.where(~near))]:
        for per in ['IS', 'OOS', '24-26']:
            a, b = vb.PERIODS[per]; d = (ss * r).loc[a:b].mean(axis=1).dropna()
            st = (ss * r).loc[a:b].stack().dropna(); m, t, n = vb.clus_t(st.values, st.index.get_level_values(0))
            print(f'{nm} {tag} {per}: DW {d.mean():.1f} (t {vb.tstat(d):.2f}) TW {m:.1f} (t {t:.2f}) n {n}')
