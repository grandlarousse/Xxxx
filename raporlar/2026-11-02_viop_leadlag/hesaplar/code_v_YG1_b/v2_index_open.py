"""v2: XU030 Yahoo açılışı bayat/gürültülü mü? Hedge'li (HX) ve hisseye özgü (idio) sonuçları kirletiyor mu?"""
import numpy as np, pandas as pd, vb
fr = pd.read_pickle('res/panel.pkl'); S = vb.S47
G = vb.wide(fr, 'gap')['2014':]; I = vb.wide(fr, 'intra')['2014':]; TV = vb.wide(fr, 'tv')['2014':]
gx, ix = G.pop('XU030'), I.pop('XU030')
# her yıl için o yılın önceki 250g ciro sıralamasına göre en büyük 25 hisse (XU030 vekili), ciro ağırlıklı
W = TV[S].rolling(250, min_periods=120).median().shift(1)
rk = W.rank(axis=1, ascending=False)
Wt = W.where(rk <= 25)
Wt = Wt.div(Wt.sum(axis=1), axis=0)
gb = (G[S] * Wt).sum(axis=1, min_count=15); ib = (I[S] * Wt).sum(axis=1, min_count=15)
df = pd.DataFrame({'gx': gx, 'ix': ix, 'gb': gb, 'ib': ib}).dropna()
df['dg'] = df.gx - df.gb; df['di'] = df.ix - df.ib
for y, g in df.groupby(df.index.year):
    bg = np.polyfit(g.gb, g.gx, 1)[0]; bi = np.polyfit(g.ib, g.ix, 1)[0]
    print(y, f'beta gapX~gapB {bg:.2f}  beta intraX~intraB {bi:.2f}  corr(dg,di) {g.dg.corr(g.di):+.2f}  sd(dg) {g.dg.std()*1e4:.1f} sd(di) {g.di.std()*1e4:.1f} bps  corr(gx,ix) {g.gx.corr(g.ix):+.2f} corr(gb,ib) {g.gb.corr(g.ib):+.2f}')
# Endeks açılışının bayatlık payı: dg'nin gb üzerine eğimi (k-1)
# h1 dönemi: XU030 10:30 değeri ile kontrol
h = pd.read_parquet(f'{vb.D}/h1/XU030.IS.parquet'); h['d'] = pd.to_datetime(h.ldate).dt.normalize()
b0 = h[h.index.hour * 60 + h.index.minute == 6 * 60 + 30].set_index('d')
x = vb.load_daily('XU030')
cmp = pd.DataFrame({'o_d': x.o, 'o_h1': b0.o, 'c1030': b0.c}).dropna()
print('h1 dönemi XU030: o_d==o_h1 oranı', np.isclose(cmp.o_d, cmp.o_h1, rtol=1e-5).mean(), 'n', len(cmp))
