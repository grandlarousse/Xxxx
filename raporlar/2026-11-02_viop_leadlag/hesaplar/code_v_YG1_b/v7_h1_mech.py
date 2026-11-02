"""v7: açılış müzayedesi gürültüsü / bid-ask ayrıştırması (h1 2023-12..2026-10, m5 60 gün).
Sepet-hedge (kendi hariç, ciro ağırlıklı 25 hisse) her giriş anı için aynı anın fiyatlarıyla kurulur."""
import numpy as np, pandas as pd, vb
fr = pd.read_pickle('res/panel.pkl'); S = vb.S47
P = {}
for s in S:
    h = pd.read_parquet(f'{vb.D}/h1/{s}.IS.parquet'); h['d'] = pd.to_datetime(h.ldate).dt.normalize()
    hm = h.index.hour * 60 + h.index.minute
    b0 = h[hm == 390].set_index('d'); b1 = h[hm == 450].set_index('d')
    b0 = b0[~b0.index.duplicated()]; b1 = b1[~b1.index.duplicated()]
    d = fr[s]
    x = pd.DataFrame({'O': d.o, 'C': d.c, 'gap': d.gap, 'tv': d.tv, 'o0': b0.o, 'P1030': b0.c, 'TP0': (b0.h + b0.l + b0.c) / 3,
                      'P1130': b1.c, 'TP1': (b1.h + b1.l + b1.c) / 3}).loc['2023-11-30':]
    ok = (np.log(x.o0 / x.O).abs() < 0.003) & x.P1030.notna() & x.gap.notna()
    x = x[ok]
    P[s] = x
W = vb.wide(fr, 'tv')[S].rolling(250, min_periods=120).median().shift(1)
def wide(col): return pd.DataFrame({s: P[s][col] for s in S})
O, C, G, P1030, TP0, P1130, TP1 = [wide(c) for c in ['O', 'C', 'gap', 'P1030', 'TP0', 'P1130', 'TP1']]
W = W.reindex(O.index)
rk = W.rank(axis=1, ascending=False)
def basket_ex(R):
    Wt = W.where(rk <= 25).where(R.notna()); sw = Wt.sum(axis=1); s_ = (R * Wt).sum(axis=1); w0 = Wt.fillna(0)
    out = (-(R.fillna(0) * w0)).add(s_, axis=0).div((-w0).add(sw, axis=0), axis=0)
    return out.where(Wt.notna().sum(axis=1) >= 15, axis=0)
legs = {'O_C': np.log(C / O), 'O_1030': np.log(P1030 / O), '1030_C': np.log(C / P1030), 'TP0_C': np.log(C / TP0),
        '1130_C': np.log(C / P1130), 'TP1_C': np.log(C / TP1), 'O_TP0': np.log(TP0 / O)}
G1030 = G + np.log(P1030 / O)    # 10:30'a kadar gap (C_{t-1} -> P1030)
Hd = {k: (v - basket_ex(v)) for k, v in legs.items()}
gB = basket_ex(G); gB1 = basket_ex(G1030)
IDG0 = G - gB; IDG1 = G1030 - gB1
def sig(g, leg, thr=0.01):
    s = -np.sign(g).where(g.abs() > thr)
    if leg == 'up': s = s.where(g > 0)
    if leg == 'down': s = s.where(g < 0)
    return s
def summ(r, a='2023-11-30', b='2026-12-31'):
    r = r.loc[a:b] * 1e4; d = r.mean(axis=1).dropna(); st = r.stack().dropna()
    m, t, n = vb.clus_t(st.values, st.index.get_level_values(0))
    return f'DW {d.mean():6.1f} (t {vb.tstat(d):5.2f}) TW {m:6.1f} (t {t:5.2f}) n {n}'
print('Gün sayısı', len(O), O.index[0].date(), O.index[-1].date())
for fam, gsig, ret in [('raw', G, legs), ('idioB', IDG0, Hd)]:
    for leg in ['both', 'up', 'down']:
        s = sig(gsig, leg)
        print(f'--- {fam} {leg}: açılış gap sinyali')
        for k in ['O_C', 'O_1030', '1030_C', 'O_TP0', 'TP0_C', '1130_C', 'TP1_C']:
            print(f'   {k:7s}', summ(s * ret[k]))
# 10:30'da bilinen gap sinyali, giriş 10:30 veya 10:30-11:30 tipik fiyat
print('=== Sinyal = C_{t-1} -> 10:30 gap (müzayede fiyatı sinyalde YOK)')
for fam, gsig, ret in [('raw', G1030, legs), ('idioB', IDG1, Hd)]:
    for leg in ['both', 'up', 'down']:
        s = sig(gsig, leg)
        print(f'   {fam} {leg} 1030_C', summ(s * ret['1030_C']), '| TP1_C', summ(s * ret['TP1_C']), '| 1130_C', summ(s * ret['1130_C']))
# yarılar
print('=== yarılar (idioB up, açılış sinyali)')
s = sig(IDG0, 'up')
for a, b in [('2023-11-30', '2025-04-30'), ('2025-05-01', '2026-12-31')]:
    print(a, b, 'O_C', summ(s * Hd['O_C'], a, b), '| TP0_C', summ(s * Hd['TP0_C'], a, b), '| 1030_C', summ(s * Hd['1030_C'], a, b))
s = sig(IDG1, 'up')
for a, b in [('2023-11-30', '2025-04-30'), ('2025-05-01', '2026-12-31')]:
    print(a, b, 'sinyal 10:30 idio-up, 1030_C', summ(s * Hd['1030_C'], a, b), '| TP1_C', summ(s * Hd['TP1_C'], a, b))
pd.to_pickle({'legs': legs, 'Hd': Hd, 'G': G, 'G1030': G1030, 'IDG0': IDG0, 'IDG1': IDG1}, 'res/h1.pkl')
