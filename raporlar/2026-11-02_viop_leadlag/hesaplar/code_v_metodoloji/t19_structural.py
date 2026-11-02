# T19: Yapısal kırılmalar: (a) USDTRY rejimleri (oynaklık, sıfıra yakın gün oranı), (b) TL vs USD bazlı korelasyon yıllara göre, (c) en oynak %5 günün korelasyona katkısı, (d) nominal TL sürüklenmesinin işaret stratejilerine katkısı
import warnings; warnings.filterwarnings("ignore")
import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_metodoloji')
import vm, pandas as pd, numpy as np
c=vm.cal(); c=c[c>='2011-01-01']   # FX zaman damgası tutarlı dönem
fx=vm.ret('TRY=X',c=c)
print('(a) USDTRY günlük oynaklık (bps) ve |r|<5bp gün oranı:')
g=fx.groupby(fx.index.year); print(pd.DataFrame({'vol_bps':(g.std()*1e4).round(0),'kucuk_gun_pct':g.apply(lambda x:(x.abs()<5e-4).mean()*100).round(0)}).T.to_string())
xu=vm.ret('XU100.IS',c=c); xusd=xu-fx
print('\n(b) XU100 ~ sürücü senkron corr (TL vs USD bazlı) yıllara göre:')
out={}
for d in ['EEM','ES=F','^VIX','BZ=F']:
    r=vm.ret(d,c=c); r1=r.shift(1)
    D=pd.concat([xu.rename('tl'),xusd.rename('usd'),r.rename('d'),r1.rename('d1')],axis=1).dropna()
    yy=D.groupby(D.index.year).apply(lambda x: pd.Series({f'{d}_TL':x.tl.corr(x.d)+x.tl.corr(x.d1), f'{d}_USD':x.usd.corr(x.d)+x.usd.corr(x.d1)}))
    out[d]=yy
Y=pd.concat(out.values(),axis=1); print('(lag0+lag1 toplamı; eşzamansız kapanış düzeltmesi)'); print(Y.round(2).T.to_string())
print('\n(c) Korelasyonun en oynak günlere bağımlılığı (2011+, XU100 vs sürücü lag0+lag1 Dimson; THYAO~BZ, XBANK~TRY):')
pairs=[('XU100.IS','EEM'),('XU100.IS','ES=F'),('XBANK.IS','TRY=X'),('THYAO.IS','BZ=F'),('TUPRS.IS','BZ=F'),('EREGL.IS','SLX'),('TRALT.IS','GC=F')]
for st,d in pairs:
    y=vm.ret(st,c=c); r=vm.ret(d,c=c)
    D=pd.concat([y.rename('y'),r.rename('x')],axis=1).dropna()
    full=D.y.corr(D.x); sp=D.y.corr(D.x,method='spearman')
    z=(D.y/D.y.std())*(D.x/D.x.std()); top=z.abs().rank(pct=True)>0.99
    share=z[top].sum()/z.sum()
    calm=D[(D.y.abs()<D.y.abs().quantile(0.95))]
    ex=[('2018-08-01','2018-09-30'),('2021-11-15','2022-01-31'),('2023-05-15','2023-07-15'),('2025-03-15','2025-04-15'),('2026-09-01','2026-10-31'),('2020-02-20','2020-04-30')]
    m=pd.Series(True,index=D.index)
    for a,b in ex: m&=~((D.index>=a)&(D.index<=b))
    print(f'{st:9s}~{d:6s} Pearson={full:+.3f} Spearman={sp:+.3f} | en uç %1 günün kovaryans payı={share:.0%} | hisse |r| üst %5 hariç={calm.y.corr(calm.x):+.3f} | 6 kriz penceresi hariç={D[m].y.corr(D[m].x):+.3f}')
print('\n(d) Nominal TL sürüklenmesi: XU100 ortalama günlük cc / gap / gün-içi (bps) yıllara göre')
g=vm.decomp('XU100.IS',start='2014-01-01'); gg=g.groupby(g.index.year).mean()*1e4; print(gg.round(1).T.to_string())
# işaret stratejisi: pos=sign(EEM_{t-1}) -> XU100 gap_t ; pnl'in sürüklenme payı = mean(pos)*mean(gap)
e=vm.ret('EEM',c=c).shift(1); D=pd.concat([g['gap'],np.sign(e).rename('p')],axis=1).dropna(); D=D[D.p!=0]
pnl=D.p*D.gap; drift=D.p.mean()*D.gap.mean()
print(f"\nÖrnek: sign(EEM_t-1)->XU100 gap: ort pnl={1e4*pnl.mean():.1f} bps, pozisyon ort={D.p.mean():+.2f}, sürüklenme payı≈{1e4*drift:.1f} bps; sürüklenmeden arındırılmış (gap-ort) pnl={1e4*(D.p*(D.gap-D.gap.mean())).mean():.1f} bps")
