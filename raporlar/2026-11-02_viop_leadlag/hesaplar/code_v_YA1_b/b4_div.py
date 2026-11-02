# Temettu ex-gunu: curutme testleri
import pandas as pd, numpy as np, glob, os
from blib import *
rng=np.random.default_rng(11)
F=pd.read_parquet(f'{OUT}/_full.parquet')
F=F.sort_values(['sym','date'])
g=F.groupby('sym')
F['o_m1']=g.o.shift(1); F['c_m1']=g.c.shift(1)
F['intra0']=F.c/F.o-1
F['gap0']=F.o/F.base-1
F['tk']=0.01/F.px
thr=np.where(F.reg=='P10',0.105,0.205)
DV=F[(F.dy>0.003)&(F.dy<0.25)&(F.consec==True)&(F.date>='2014-01-01')&F.o.notna()&(np.abs(F.R-1)<thr)].copy()
DV['s']=-DV.intra0
print('olay sayisi',len(DV),'VIOP47',int(DV.viop47.sum()))
# veri artefakti kontrolleri
DV['o_eq_prevc']=np.isclose(DV.o,DV.c_m1,rtol=1e-6)
DV['o_eq_c']=np.isclose(DV.o,DV.c,rtol=1e-6)
print('acilis = onceki kapanis (duzeltmesiz) orani',round(DV.o_eq_prevc.mean(),3),' acilis=kapanis orani',round(DV.o_eq_c.mean(),3))
x=DV[['gap0','dy']].dropna(); b=np.polyfit(x.dy,x.gap0,1); print('gap0 = a + b*dy: b',round(b[0],3),' a bps',round(b[1]*1e4,1))
for lo,hi in [(0.003,0.01),(0.01,0.02),(0.02,0.04),(0.04,0.08),(0.08,0.25)]:
    q=DV[(DV.dy>=lo)&(DV.dy<hi)]; print(f'  dy {lo:.3f}-{hi:.3f}: n {len(q)} gap0 {q.gap0.mean()*1e4:.0f} medyan {q.gap0.median()*1e4:.0f} | gun-ici {q.intra0.mean()*1e4:.0f} | gap0/dy {np.nanmedian(q.gap0/q.dy):.3f}')
# h1 ilk bar acilisi ve 10:30
H=f'{D}/h1'
rows=[]
for s in DV[DV.date>='2023-11-30'].sym.unique():
    fn=f'{H}/{s}.IS.parquet'
    if not os.path.exists(fn): continue
    h=pd.read_parquet(fn); h['d']=pd.to_datetime(h.ldate).dt.normalize()
    hh=h.index.hour*60+h.index.minute
    h['hm']=hh
    for d in DV[(DV.sym==s)&(DV.date>='2023-11-30')].date:
        b_=h[h.d==d]
        if len(b_)<3: continue
        fb=b_[b_.hm==390]
        if len(fb)==0: continue
        pre=b_[b_.hm<900]
        rows.append(dict(sym=s,date=d,h_open=fb.o.iloc[0],h_1030=fb.c.iloc[0],h_pre=pre.c.iloc[-1]))
Hh=pd.DataFrame(rows)
DV=DV.merge(Hh,on=['sym','date'],how='left')
q=DV[DV.h_open.notna()]
print('h1 eslesme: n',len(q),' |gunluk acilis - h1 ilk bar acilis|<0.2% orani',round((np.abs(q.o/q.h_open-1)<0.002).mean(),3))
q=q[np.abs(q.o/q.h_open-1)<0.002]
DV['s_1030']=1-DV.c/DV.h_1030; DV['o_1030']=1-DV.h_1030/DV.o; DV['s_auc']=1-DV.c/DV.h_pre; DV['s_cont']=1-DV.h_pre/DV.h_1030
for nm,sub in [('tum',q),('VIOP47',q[q.viop47])]:
    sub=DV.loc[DV.h_open.notna()&(np.abs(DV.o/DV.h_open-1)<0.002)&(DV.viop47 if nm=='VIOP47' else True)]
    print(f' h1 {nm} n {len(sub)}: acilis->10:30 short {sub.o_1030.mean()*1e4:.0f} (t {cl_t(sub.o_1030,sub.date)[1]:.2f}) | 10:30->surekli son {sub.s_cont.mean()*1e4:.0f} (t {cl_t(sub.s_cont,sub.date)[1]:.2f}) | kapanis seansi {sub.s_auc.mean()*1e4:.0f} | 10:30->kapanis {sub.s_1030.mean()*1e4:.0f} (t {cl_t(sub.s_1030,sub.date)[1]:.2f})')
# alt donemler, VIOP47 spot @15 (+tik)
def rep(E,lab):
    out=[]
    for nm,a,b_ in [('2014-17','2014-01-01','2017-12-31'),('2018-20','2018-01-01','2020-12-31'),('2021-23','2021-01-01','2023-12-31'),('2024-26','2024-01-01','2026-12-31'),('TUM','2014-01-01','2026-12-31')]:
        q=E[(E.date>=a)&(E.date<=b_)]
        if len(q)<5: continue
        r=summ(q.assign(n1=q.s,n2=q.s-15e-4,n3=q.s-15e-4-q.tk),'n2',date='date')
        m3,t3,_=cl_t(q.s-15e-4-q.tk,q.date)
        mlog=np.log(q.o/q.c).mean()
        out.append(dict(donem=nm,n=r['n'],gap0=round(q.gap0.mean()*1e4,0),brut_log=round(mlog*1e4,1),brut=round(q.s.mean()*1e4,1),at15=r['trade_bps'],t15=r['trade_t'],at15tik=round(m3*1e4,1),t15tik=round(t3,2),med15=r['med_bps'],hit=r['hit']))
    print(f'--- {lab}'); print(pd.DataFrame(out).to_string(index=False))
rep(DV,'tum evren ex-gunu acilis SAT -> kapanis')
rep(DV[DV.viop47],'VIOP47 ex-gunu')
# plasebo: ayni hisse rastgele gun; ex-1 ve ex+1 gun-ici
V47=DV[DV.viop47]
pool=F[F.viop47&(F.date>='2014-01-01')&(F.dy.abs()<1e-4)&F.intra0.notna()&(np.abs(F.R-1)<0.06)]
ps={k:(-gg.intra0).values for k,gg in pool.groupby('sym')}
cnt=V47.groupby('sym').size(); obs=V47.s.mean(); sims=[]
for i in range(2000):
    tot=0;n=0
    for s,k in cnt.items():
        a=ps.get(s);
        if a is None: continue
        tot+=a[rng.integers(0,len(a),k)].sum(); n+=k
    sims.append(tot/n)
sims=np.array(sims); print(f'plasebo VIOP47: gozlenen brut {obs*1e4:.1f}, ayni-hisse rastgele gun ort {sims.mean()*1e4:.1f} 95% {np.quantile(sims,.95)*1e4:.1f} p={(sims>=obs).mean():.4f}')
# ex-1, ex+1 gun-ici
F2=F.set_index(['sym','date'])
for k,lab in [(-1,'ex-1'),(1,'ex+1')]:
    vals=[]
    for s,d in zip(V47.sym,V47.date):
        gg=F[F.sym==s] if False else None
    idx=F.groupby('sym').cumcount()
F['i']=F.groupby('sym').cumcount()
key=V47.merge(F[['sym','date','i']],on=['sym','date'])
for k,lab in [(-1,'ex-1'),(1,'ex+1'),(2,'ex+2')]:
    kk=key[['sym','i']].assign(i=key.i+k).merge(F[['sym','i','intra0','date']],on=['sym','i'])
    m,t,n=cl_t(-kk.intra0,kk.date); print(f'  bayat/oncu sinyal {lab} gun-ici short brut {m*1e4:.1f} (t {t:.2f}, n {n})')
# uc deger, VIOP47 @15
E=V47.assign(net=V47.s-15e-4)
dm=E.groupby('date').net.sum().sort_values()
for lab,sub in [('tum',E),('en iyi 10 gun haric',E[~E.date.isin(dm.index[-10:])]),('simetrik 10+10',E[~E.date.isin(list(dm.index[:10])+list(dm.index[-10:]))]),('kirpilmis 5/95',E[(E.net>E.net.quantile(.05))&(E.net<E.net.quantile(.95))])]:
    m,t,n=cl_t(sub.net,sub.date); print(f'  VIOP47 @15 {lab}: {m*1e4:.1f} (t {t:.2f}, n {n})')
gg=E.groupby('sym').net.mean(); print('  hisse>0',int((gg>0).sum()),'/',len(gg))
# vadeli ex-gunu
V=pd.read_parquet(f'{D}/viop_panel.parquet')
V=V[V.segment=='SSF'][['date','und','expiry','settle','prev_settle','open','close','vwap','trades','value_tl']]; V['und']=V.und.astype(str)
m=V47[['sym','date','tk','s','gap0']].rename(columns={'sym':'und'}).merge(V,on=['und','date'])
m=m[m.expiry>m.date].sort_values('expiry').drop_duplicates(['und','date'])
m=m[(m.open>0)&(m.close>0)&(m.trades>0)]
m['f_oc']=1-m.close/m.open; m['f_vc']=1-m.close/m.vwap; m['f_open_rel']=m.open/m.prev_settle-1
print(f'VIOP vadeli ex-gunu n {len(m)}: vadeli acilis/onceki uzlasma medyan {m.f_open_rel.median()*1e4:.0f} bps (spot gap0 ayni olaylar medyan {m.gap0.median()*1e4:.0f})')
for col,lab in [('s','spot acilis->kapanis'),('f_oc','vadeli open->close'),('f_vc','vadeli VWAP->close')]:
    for c,cl in [(0,'brut'),(1,'@15+tik')]:
        x=m[col]-(15e-4+m.tk if c else 0); mm,tt,nn=cl_t(x,m.date)
        sub={}
        for a,b_ in [('2017','2020'),('2021','2023'),('2024','2026')]:
            qq=m[(m.date.dt.year>=int(a))&(m.date.dt.year<=int(b_))]; xx=qq[col]-(15e-4+qq.tk if c else 0); m2,t2,n2=cl_t(xx,qq.date); sub[a+'-'+b_[2:]]=f'{m2*1e4:.0f} (t {t2:.1f}, n {n2})'
        print(f'  {lab:22s} {cl:8s} {mm*1e4:6.1f} (t {tt:5.2f}) | {sub}')
DV.to_parquet(f'{OUT}/_div.parquet')
