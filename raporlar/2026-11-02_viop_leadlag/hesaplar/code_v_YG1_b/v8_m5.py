"""v8: m5 (07.08-30.10.2026, 60 gün): açılış müzayedesi fiyatından sonraki ilk dakikalarda dönüşün hızı.
Müzayede (06:55 barı) c = O. 07:00 barı c = 10:05 fiyatı."""
import numpy as np, pandas as pd, vb
fr = pd.read_pickle('res/panel.pkl'); S = vb.S47
cols = {}
for s in S:
    m = pd.read_parquet(f'{vb.D}/m5/{s}.IS.parquet'); m['d'] = pd.to_datetime(m.ldate).dt.normalize()
    hm = m.index.hour * 60 + m.index.minute
    def at(t):
        x = m[hm == t].set_index('d'); return x[~x.index.duplicated()]
    a0 = at(415); a1 = at(425); a2 = at(445)  # 07:00 (10:00-10:05), 07:10 (->10:15), 07:30 (->10:35)
    v = m[(hm >= 420) & (hm < 450)].copy(); v['pv'] = (v.h + v.l + v.c) / 3 * v.v
    vw = (v.groupby('d').pv.sum() / v.groupby('d').v.sum())
    d = fr[s]
    x = pd.DataFrame({'O': d.o, 'C': d.c, 'gap': d.gap, 'P1005': at(420).c, 'P1015': at(430).c, 'P1030': at(445).o, 'VW30': vw}).loc['2026-08-07':].dropna()
    cols[s] = x
W = vb.wide(fr, 'tv')[S].rolling(250, min_periods=120).median().shift(1)
def wide(c): return pd.DataFrame({s: cols[s][c] for s in S})
O, C, G = wide('O'), wide('C'), wide('gap'); W = W.reindex(O.index); rk = W.rank(axis=1, ascending=False)
def bex(R):
    Wt = W.where(rk <= 25).where(R.notna()); sw = Wt.sum(axis=1); s_ = (R * Wt).sum(axis=1); w0 = Wt.fillna(0)
    return (-(R.fillna(0) * w0)).add(s_, axis=0).div((-w0).add(sw, axis=0), axis=0)
IDG = G - bex(G)
print('gün', len(O))
for nm, px in [('P1005', wide('P1005')), ('P1015', wide('P1015')), ('P1030', wide('P1030')), ('VW30', wide('VW30'))]:
    a = np.log(px / O); b = np.log(C / px)
    for fam, g, ra, rb in [('raw', G, a, b), ('idioB', IDG, a - bex(a), b - bex(b))]:
        for leg in ['both', 'up']:
            s = -np.sign(g).where(g.abs() > 0.01)
            if leg == 'up': s = s.where(g > 0)
            r1 = (s * ra * 1e4).stack().dropna(); r2 = (s * rb * 1e4).stack().dropna()
            m1, t1, n = vb.clus_t(r1.values, r1.index.get_level_values(0)); m2, t2, _ = vb.clus_t(r2.values, r2.index.get_level_values(0))
            print(f'{fam:5s} {leg:4s} O->{nm}: {m1:6.1f} (t {t1:5.2f}) | {nm}->C: {m2:6.1f} (t {t2:5.2f}) n {n}')
