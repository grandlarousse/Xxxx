"""Tavan/taban günleri bağımlılığı, dolum fizibilitesi, bayatlatılmış sinyal, 10:30 giriş/çıkış, ilk gün katkısı."""
import vb, numpy as np, pandas as pd
P = vb.pair_inputs('SAHOL', 'AKBNK'); A, B, beta = P['A'], P['B'], P['beta']
z = vb.zscore(P['S'], 60); pos = vb.positions(z, 1.5)
df = vb.pnl_open(pos, A['gap'], A['intra'], B['gap'], B['intra'], beta, 8)
sA = np.expm1(A['cc']); sB = np.expm1(B['cc']); gA = np.expm1(A['gap']); gB = np.expm1(B['gap'])
lim = pd.Series(np.where(df.index < vb.REG, 0.19, 0.095), index=df.index)
limday = (sA.abs() >= lim) | (sB.abs() >= lim)
print('limit (>=%9,5 / %19) gün sayısı 2014+:', int(limday[df.index >= '2014'].sum()), ' maruz olanlar:', int((limday & df.exp)[df.index >= '2014'].sum()))
for lab, lo, hi in [('IS', '2014', '2021'), ('OOS', '2021', '2027'), ('2021-23', '2021', '2024'), ('2024-26', '2024', '2027')]:
    x = df[(df.index >= lo) & (df.index < hi)]; tot = x.net.sum(); l = x[limday.reindex(x.index)].net.sum()
    d2 = x.copy(); d2.loc[limday.reindex(x.index).values, ['net']] = 0
    print(f'{lab}: limit günlerinin net pnl payı {l / tot:.2f}; limit günleri sıfırlanınca', {k: round(v, 2) for k, v in vb.summ(d2, lo, hi).items()})
# Limit günleri listesi (maruz)
L = df[limday & df.exp & (df.index >= '2014')][['Pg', 'Pi', 'net']].copy(); L['sA'] = sA; L['sB'] = sB; L['gA'] = gA; L['gB'] = gB
print((L.assign(net_bps=lambda x: (1e4 * x.net).round(0))[['Pg', 'Pi', 'sA', 'sB', 'gA', 'gB', 'net_bps']].round(3)).to_string())
# Dolum fizibilitesi: açılışta pozisyon değişimi gereken günlerde açılış tavan/taban kilitli mi?
ch = df[(df.Pi != df.Pg) & (df.index >= '2014')].copy()
dA = ch.Pi - ch.Pg  # SAHOL alım(+)/satım(-)
dB = -dA
oA_lock_up = (gA.reindex(ch.index) >= lim.reindex(ch.index) - 0.003) & (A['o'] == A['h']).reindex(ch.index)
oA_lock_dn = (gA.reindex(ch.index) <= -lim.reindex(ch.index) + 0.003) & (A['o'] == A['l']).reindex(ch.index)
oB_lock_up = (gB.reindex(ch.index) >= lim.reindex(ch.index) - 0.003) & (B['o'] == B['h']).reindex(ch.index)
oB_lock_dn = (gB.reindex(ch.index) <= -lim.reindex(ch.index) + 0.003) & (B['o'] == B['l']).reindex(ch.index)
inf = ((dA > 0) & oA_lock_up) | ((dA < 0) & oA_lock_dn) | ((dB > 0) & oB_lock_up) | ((dB < 0) & oB_lock_dn)
print('açılışta işlem gereken gün:', len(ch), ' kilitli (dolum imkansız):', int(inf.sum()), list(ch.index[inf].date))
# kilitli açılışlarda girişi ertesi güne kaydır (yaklaşık): o günlerde pozisyonu bir önceki değerde tut
pos2 = pos.copy()
# pos_t (karar) -> Pi_{t+1}; Pi'nin değişemediği gün d ise karar günü d-1: pos[d-1] = pos[d-2]
for d in ch.index[inf]:
    i = pos.index.get_loc(d)
    pos2.iloc[i - 1] = pos2.iloc[i - 2]
df2 = vb.pnl_open(pos2, A['gap'], A['intra'], B['gap'], B['intra'], beta, 8)
print('kilitli açılışlar ertelenince:'); print(vb.table(df2).loc[['IS', 'OOS', '2021-23', '2024-26'], ['bps', 't']].round(2).to_string())
# Bayatlatılmış sinyal: karar pos_{t-k}
print('\n--- bayat sinyal (k gün gecikmeli karar, açılış girişi, 8 bps) ---')
rows = []
for k in [0, 1, 2, 3, 5, 10, 20, 40]:
    d = vb.pnl_open(pos.shift(k).fillna(0), A['gap'], A['intra'], B['gap'], B['intra'], beta, 8)
    tb = vb.table(d); rows.append(dict(k=k, IS_bps=tb.loc['IS', 'bps'], IS_t=tb.loc['IS', 't'], OOS_bps=tb.loc['OOS', 'bps'], OOS_t=tb.loc['OOS', 't']))
print(pd.DataFrame(rows).round(2).to_string())
# 0 maliyet brüt bayatlama eğrisi
rows = []
for k in [0, 1, 2, 3, 5, 10, 20, 40]:
    d = vb.pnl_open(pos.shift(k).fillna(0), A['gap'], A['intra'], B['gap'], B['intra'], beta, 0)
    tb = vb.table(d); rows.append(dict(k=k, IS_bps=tb.loc['IS', 'bps'], IS_t=tb.loc['IS', 't'], OOS_bps=tb.loc['OOS', 'bps'], OOS_t=tb.loc['OOS', 't']))
print('brüt:'); print(pd.DataFrame(rows).round(2).to_string())
# İlk gün katkısı: giriş günü gün içi / sonraki günler
first = (df.Pi != 0) & (df.Pg != df.Pi)
for lab, lo, hi in [('IS', '2014', '2021'), ('OOS', '2021', '2027')]:
    x = df[(df.index >= lo) & (df.index < hi)]; f = first.reindex(x.index)
    print(lab, 'brüt pnl payı: giriş günü', round(x[f].gross.sum() / x.gross.sum(), 2), ' sonraki günler', round(x[~f].gross.sum() / x.gross.sum(), 2))
# 10:30 TSİ giriş ve çıkış (h1: 2023-12+); sinyal t kapanışı
pA, pB = vb.p1030('SAHOL'), vb.p1030('AKBNK')
fA = (A['adj'] / A['c']); fB = (B['adj'] / B['c'])
idx = df.index[(df.index >= '2023-12-01')]
qA = np.log(pA.reindex(idx) * fA.reindex(idx)); qB = np.log(pB.reindex(idx) * fB.reindex(idx))
lA = np.log(A['adj']).reindex(idx); lB = np.log(B['adj']).reindex(idx); lA0 = np.log(A['adj'].ffill()).shift().reindex(idx); lB0 = np.log(B['adj'].ffill()).shift().reindex(idx)
g1A = qA - lA0; i1A = lA - qA; g1B = qB - lB0; i1B = lB - qB   # prevclose->10:30, 10:30->close
for c in [8, 15]:
    d_o = vb.pnl_open(pos, A['gap'], A['intra'], B['gap'], B['intra'], beta, c).reindex(idx)
    d_q = vb.pnl_open(pos, g1A.reindex(df.index), i1A.reindex(df.index), g1B.reindex(df.index), i1B.reindex(df.index), beta, c).reindex(idx)
    m = d_q[['gross']].notna().all(axis=1) & g1A.notna() & g1B.notna()
    print(f'2023-12+ {c} bps: açılış girişi', {k: round(v, 2) for k, v in vb.summ(d_o[m], '2023-12-01').items()}, '\n            10:30 giriş/çıkış', {k: round(v, 2) for k, v in vb.summ(d_q[m], '2023-12-01').items()})
