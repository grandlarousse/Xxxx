"""Uç değer, alt dönem, ex-ante likidite, tik, sahte-OOS parametre seçimi, kış vekili."""
import numpy as np, pandas as pd, vlib as v
rng=np.random.default_rng(11)
A=pd.read_parquet(v.RES+'/panel.parquet'); XU=A[A.sym=='XU030'].set_index('date')
S=A[A.sym!='XU030'].sort_values(['sym','date']).copy()
mu=S.groupby('date')['y'].transform('mean'); S['yx']=S['y']-mu
W=S[S.CA.notna()].copy()
base,x=v.port(W,'CA','y',0.0025); basex,xx=v.port(W,'CA','yx',0.0025)
print('BAZ ham',v.summ(base,x),' excess',v.summ(basex,xx))
# --- Uç değer
print('\n== Uç değer bağımlılığı ==')
for k in [5,10,20,40]:
    top=base.abs().sort_values().index[-k:]; topp=base.sort_values().index[-k:]
    print(f'en iyi {k} gün hariç: ham {v.summ(base.drop(topp))["bps"]} (t {v.summ(base.drop(topp))["t"]}); |pnl| en büyük {k} hariç {v.summ(base.drop(top))["bps"]}')
print('günlük P&L medyanı %.1f, kırpılmış (%%5) ort %.1f, isabet %.2f'%(1e4*base.median(),1e4*base.clip(base.quantile(.05),base.quantile(.95)).mean(),(base>0).mean()))
q=x['y'].quantile([.01,.99]); xw=x.assign(p=-np.sign(x.CA)*x.y.clip(*q)); print('getiri %1/%99 winsor:',v.summ(xw.groupby('date').p.mean()))
# hisse katkısı: en çok katkı veren 5/10 hisse hariç
cont=x.groupby('sym')['p'].sum().sort_values(ascending=False)
for k in [3,5,10]:
    drop=cont.index[:k]; dd,_=v.port(W[~W.sym.isin(drop)],'CA','y',0.0025); print(f'en çok katkı veren {k} hisse ({",".join(drop[:5])}...) hariç:',v.summ(dd))
print('hisse bazında pozitif ortalama P&L oranı: %.2f (%d hisse)'%((x.groupby('sym')['p'].mean()>0).mean(),x.sym.nunique()))
# blok bootstrap (10 günlük bloklar) %95 GA
b=base.values; n=len(b); L=10; bs=[]
for _ in range(2000):
    st=rng.integers(0,n-L,size=n//L+1); idx=(st[:,None]+np.arange(L)).ravel()[:n]; bs.append(b[idx].mean())
print('blok bootstrap %%95 GA: [%.1f, %.1f] bps'%(1e4*np.percentile(bs,2.5),1e4*np.percentile(bs,97.5)))
# --- Alt dönemler
print('\n== Alt dönem ==')
W['yr']=W.date.dt.year; W['mo']=W.date.dt.month
for yr in [2024,2025,2026]:
    for lab,m in [('Nis-Haz',W.mo.isin([3,4,5,6])),('Tem-Ağu',W.mo.isin([7,8])),('Eyl-Eki',W.mo.isin([9,10]))]:
        sel=W[(W.yr==yr)&m]; dd,_=v.port(sel,'CA','y',0.0025); ddx,_=v.port(sel,'CA','yx',0.0025)
        d=sel[['y','CA','date']].dropna(); b_,se_=v.ols_cl(d['y'],d[['CA']],d['date'])
        print(yr,lab,'ham',v.summ(dd),' excess',v.summ(ddx)['bps'],v.summ(ddx)['t'],'  b %.2f (t %.1f)'%(b_[1],b_[1]/se_[1]))
# --- Ex-ante likidite (geçmiş 60 gün medyan TL hacim, t-1'e kadar) ve tik
S['liq']=S.groupby('sym')['TL'].transform(lambda z:z.shift(1).rolling(60,min_periods=20).median())
S['liqr']=S.groupby('date')['liq'].rank(pct=True)
def tick(p):
    p=np.asarray(p,float); return np.select([p<20,p<50,p<100,p<250,p<500,p<1000,p<2500],[0.01,0.02,0.05,0.10,0.25,0.50,1.00],2.50)
S['tick_bps']=1e4*tick(S['C'])/S['C']; S['CA_ticks']=np.abs(S['C']-S['P1500'])/tick(S['C'])
W=S[S.CA.notna()].copy()
print('\n== Ex-ante likidite (günlük kesit sıralaması, geçmiş 60g TL hacim) ==')
for lab,m in [('alt üçte bir',W.liqr<=1/3),('orta',(W.liqr>1/3)&(W.liqr<=2/3)),('üst üçte bir',W.liqr>2/3)]:
    dd,xx=v.port(W[m],'CA','y',0.0025); ddx,_=v.port(W[m],'CA','yx',0.0025); print(lab,'ham',v.summ(dd,xx),' excess',v.summ(ddx))
print('\n== Tik ==')
for lab,m in [('tik<=5bps',W.tick_bps<=5),('tik 5-10',(W.tick_bps>5)&(W.tick_bps<=10)),('tik>10',W.tick_bps>10),('CA>=3 tik',W.CA_ticks>=2.5),('CA 1-2 tik',W.CA_ticks<2.5)]:
    dd,xx=v.port(W[m],'CA','y',0.0025); print(lab,v.summ(dd,xx))
# --- Sahte-OOS: parametreleri yalnız 2024 yazında seç, 2025-26'da sına
print('\n== Sahte-OOS parametre seçimi ==')
cand=[(thr,y) for thr in [0,10,25,50,75,100] for y in ['gap1','y','y0830','y0930','y1430','cc1']]
IS=W[W.date<'2025-01-01']; OOS=W[W.date>='2025-01-01']
sc=[]
for thr,y in cand:
    dd,_=v.port(IS,'CA',y,thr/1e4); s=v.summ(dd); sc.append((s['t'],thr,y,s['bps']))
sc.sort(reverse=True); print('IS(2024) en iyi 5:',sc[:5])
for t_,thr,y,b_ in sc[:3]:
    dd,_=v.port(OOS,'CA',y,thr/1e4); print(f'  seçilen thr={thr} çıkış={y}: IS {b_:.1f} (t {t_:.1f}) -> OOS 2025-26',v.summ(dd))
print('  medyan IS-sırası parametre OOS:', np.median([v.summ(v.port(OOS,'CA',y,thr/1e4)[0])['bps'] for _,thr,y,_ in sc]))
# --- Kış vekili: LH (14:30->C) yıl boyu
print('\n== Kış vekili LH = log(C/P14:30) ==')
S['season']=np.where(S.summer,'yaz','kış')
for se in ['yaz','kış']:
    sel=S[(S.season==se)&S.LH.notna()]
    d=sel[['y','LH','DAY','date']].dropna(); b_,s_=v.ols_cl(d['y'],d[['LH','DAY']],d['date'])
    for thr in [25,50]:
        dd,_=v.port(sel,'LH','y',thr/1e4); ddx,_=v.port(sel,'LH','yx',thr/1e4)
        print(se,f'|LH|>{thr}','ham',v.summ(dd),' excess',v.summ(ddx)['bps'],v.summ(ddx)['t'],' b_LH %.3f (t %.1f) n_gün %d'%(b_[1],b_[1]/s_[1],d.date.nunique()))
# Yazın LH'yi CA ve L30'a ayır: beklenen kış katsayısı
sel=S[S.summer&S.CA.notna()]; d=sel[['y','LH','CA','L30','date']].dropna()
cv=np.cov(d.CA,d.LH)[0,1]/d.LH.var(); print('yaz: cov(CA,LH)/var(LH)=%.3f, var(CA)/var(LH)=%.3f -> b_LH beklenen ≈ -0.35*%.3f = %.3f'%(cv,d.CA.var()/d.LH.var(),cv,-0.35*cv))
