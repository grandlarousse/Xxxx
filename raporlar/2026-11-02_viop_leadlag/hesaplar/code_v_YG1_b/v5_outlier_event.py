"""v5: (a) olay-zamanı profili: hisseye özgü yukarı gap günü etrafında k=-10..+10 sepet-hedge'li gün-içi
(kalıcı 'gece yukarı / gün-içi aşağı' hisse özelliği mi, aynı güne özgü dönüş mü?)
(b) uç değer bağımlılığı: kırpma, en iyi günleri atma, |gap| kovaları, temettü günleri, hisse jackknife"""
import numpy as np, pandas as pd, vb
fr = pd.read_pickle('res/panel.pkl'); S = vb.S47
G = vb.wide(fr, 'gap')['2014':]; I = vb.wide(fr, 'intra')['2014':]; DV = vb.wide(fr, 'divday')['2014':]
gx, ix = G.pop('XU030'), I.pop('XU030'); G, I = G[S], I[S]; DV = DV[S].fillna(False).astype(bool)
B = pd.read_pickle('res/basket.pkl'); gbl, ibl = B['gbl'].reindex(G.index), B['ibl'].reindex(G.index)
IDG = G - gbl; HB = (I - ibl) * 1e4
print('(a) olay profili: idio-UP (>%1) günlerinde k gün sonraki sepet-hedge\'li gün-içi (bps; short yönü için işaret ters çevrilmemiş)')
for per, (a, b) in [('IS', ('2014', '2020')), ('OOS', ('2021', '2026'))]:
    ev = (IDG > 0.01)
    line = []
    for k in [-10, -5, -3, -2, -1, 0, 1, 2, 3, 5, 10]:
        x = HB.shift(-k).where(ev).loc[a:b].stack()
        line.append(f'k{k:+d}:{x.mean():.1f}')
    base = HB.loc[a:b].stack().mean()
    print(per, ' '.join(line), f'| tüm günler ort {base:.1f}')
    ev = (IDG < -0.01)
    line = []
    for k in [-10, -5, -3, -2, -1, 0, 1, 2, 3, 5, 10]:
        x = HB.shift(-k).where(ev).loc[a:b].stack()
        line.append(f'k{k:+d}:{x.mean():.1f}')
    print(per, 'DOWN', ' '.join(line))
# yerel taban: aynı hissenin t-20..t-1 ve t+1..t+20 ortalaması (gap günleri dahil) - aynı gün etkisinin artımı
def local_excess(sig, ret, a, b):
    r = ret
    m_before = r.shift(1).rolling(20, min_periods=10).mean()
    m_after = r[::-1].shift(1).rolling(20, min_periods=10).mean()[::-1]
    loc = (m_before + m_after) / 2
    x = (sig * (r - loc)).loc[a:b]
    d = x.mean(axis=1).dropna(); st = x.stack().dropna()
    m, t, n = vb.clus_t(st.values, st.index.get_level_values(0))
    return d.mean(), vb.tstat(d), m, t
sU = -np.sign(IDG).where(IDG > 0.01); sB = -np.sign(IDG).where(IDG.abs() > 0.01)
sRaw = -np.sign(G).where(G.abs() > 0.01)
for nm, s, r in [('idioB_up', sU, HB), ('idioB_both', sB, HB), ('raw_both', sRaw, I * 1e4)]:
    for per, (a, b) in [('IS', ('2014', '2020')), ('OOS', ('2021', '2026')), ('24-26', ('2024', '2026'))]:
        dm, dt, tm, tt = local_excess(s, r, a, b)
        print(f'{nm} {per}: yerel taban (±20g) çıkarılmış  DW {dm:.1f} (t {dt:.2f})  TW {tm:.1f} (t {tt:.2f})')
print('\n(b) uç değerler (OOS 2021-26; DW)')
def rep(nm, r):
    o = r.loc['2021':]; d = o.mean(axis=1).dropna()
    st = o.stack().dropna()
    srt = d.sort_values()
    out = dict(DW=d.mean(), t=vb.tstat(d), med_day=d.median(), pos_day=(d > 0).mean(), med_trade=st.median(), pos_trade=(st > 0).mean(),
               drop10best=srt.iloc[:-10].mean(), t_d10=vb.tstat(srt.iloc[:-10]), drop1pct=srt.iloc[:-int(len(d)*0.01)].mean(),
               drop5pct=srt.iloc[:-int(len(d)*0.05)].mean(),
               top5pct_share=srt.iloc[-int(len(d)*0.05):].sum() / d.sum())
    lo, hi = st.quantile([0.01, 0.99]); w = o.clip(lo, hi); dw = w.mean(axis=1).dropna()
    out['winsor1'] = dw.mean(); out['t_w'] = vb.tstat(dw)
    print(nm, {k: round(v, 2) for k, v in out.items()})
R = {'raw_both': sRaw * I * 1e4, 'raw_up': sRaw.where(G > 0) * I * 1e4, 'idioB_both': sB * HB, 'idioB_up': sU * HB}
for k, v in R.items(): rep(k, v)
print('\n|gap| kovaları (raw, OOS, DW ve TW)')
for lo, hi in [(0.01, 0.015), (0.015, 0.02), (0.02, 0.03), (0.03, 0.05), (0.05, 0.11)]:
    for leg, cond in [('up', G > 0), ('down', G < 0)]:
        s = -np.sign(G).where((G.abs() > lo) & (G.abs() <= hi) & cond)
        r = (s * I * 1e4)
        for per, (a, b) in [('IS', ('2014', '2020')), ('OOS', ('2021', '2026'))]:
            st = r.loc[a:b].stack().dropna(); m, t, n = vb.clus_t(st.values, st.index.get_level_values(0))
            print(f'  |gap| {lo:.3f}-{hi:.3f} {leg} {per}: TW {m:.1f} (t {t:.2f}) n {n}', end=';')
        print()
print('\ntemettü/kurumsal işlem günleri hariç (raw_both OOS DW):')
r = (sRaw.where(~DV) * I * 1e4).loc['2021':]; d = r.mean(axis=1).dropna(); print(d.mean(), vb.tstat(d), 'atılan işlem', int((sRaw.notna() & DV).loc['2021':].sum().sum()))
print('\nhisse jackknife (raw_both OOS DW): tek tek çıkarınca min/max; en çok katkı veren 5 hisse çıkınca')
base = R['raw_both'].loc['2021':]
jk = {c: base.drop(columns=c).mean(axis=1).mean() for c in S}
jk = pd.Series(jk).sort_values(); print('min', jk.head(3).round(1).to_dict(), 'max', jk.tail(3).round(1).to_dict())
contrib = base.sum().sort_values(ascending=False)
for k in [3, 5, 10]:
    d = base.drop(columns=contrib.index[:k]).mean(axis=1).dropna(); print(f'en iyi {k} hisse çıkınca: {d.mean():.1f} (t {vb.tstat(d):.2f})  çıkanlar {list(contrib.index[:k])}')
b2 = R['idioB_up'].loc['2021':]; contrib = b2.sum().sort_values(ascending=False)
for k in [3, 5, 10]:
    d = b2.drop(columns=contrib.index[:k]).mean(axis=1).dropna(); print(f'idioB_up en iyi {k} hisse çıkınca: {d.mean():.1f} (t {vb.tstat(d):.2f})  {list(contrib.index[:k])}')
