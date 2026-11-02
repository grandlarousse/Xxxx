# TC/TU ertesi gun: saatlik veriyle acilis gurultusu ayristirmasi (2023-11-30+)
import pandas as pd, numpy as np, os
from blib import *
F=pd.read_parquet(f'{OUT}/_full.parquet')
F=F[(F.date_1>='2023-11-30')&F.ok1&F.intra1.notna()&(F.reg=='P10')]
H=f'{D}/h1'
rows=[]
for s in F.sym.unique():
    fn=f'{H}/{s}.IS.parquet'
    if not os.path.exists(fn): continue
    h=pd.read_parquet(fn); h['d']=pd.to_datetime(h.ldate).dt.normalize(); h['hm']=h.index.hour*60+h.index.minute
    cont=h[h.hm<900]
    a=cont.groupby('d').agg(h_open=('o','first'),h_1030=('c','first'),h_pre=('c','last'),twap=('c','mean'),nb=('c','size'),hm0=('hm','first'))
    a['sym']=s; rows.append(a.reset_index().rename(columns={'d':'date_1'}))
Hh=pd.concat(rows)
Hh=Hh[(Hh.hm0==390)&(Hh.nb>=6)]
E=F.merge(Hh,on=['sym','date_1'],how='inner')
E=E[np.abs(E.o_1/E.h_open-1)<0.002]
E['s_o1030']=1-E.h_1030/E.o_1
E['s_1030c']=1-E.c_1/E.h_1030
E['s_cont']=1-E.h_pre/E.h_1030
E['s_auc']=1-E.c_1/E.h_pre
E['s_twapc']=1-E.c_1/E.twap
E['s_oc']=-E.intra1
E['tk']=0.01/E.px
ev=E.TC|E.TCs|E.TU_src|E.TU_s|E.NEAR|E.BC|(E.R>1.06)|(E.R<0.94)
base=E[~ev]
print('h1 eslesen gun:',len(E),' hisse',E.sym.nunique())
cols=['s_oc','s_o1030','s_1030c','s_cont','s_auc','s_twapc']
def row(sub,lab):
    out={'set':lab,'n':len(sub)}
    for c in cols:
        m,t,n=cl_t(sub[c],sub.date_1); out[c]=f'{m*1e4:.0f} ({t:.1f})'
    m,t,n=cl_t(sub.s_1030c-15e-4-sub.tk,sub.date_1); out['1030c@15+tik']=f'{m*1e4:.0f} ({t:.1f})'
    m,t,n=cl_t(sub.s_twapc-15e-4-sub.tk,sub.date_1); out['twapc@15+tik']=f'{m*1e4:.0f} ({t:.1f})'
    return out
R=[row(base[base.viop47],'baz VIOP47 (olay disi)'),row(base,'baz tum h1')]
for nm,m in [('TC',E.TC),('TU_s',E.TU_s),('TU_src',E.TU_src),('NEAR',E.NEAR)]:
    R.append(row(E[m&E.viop47],nm+' VIOP47')); R.append(row(E[m&E.fut_listed],nm+' VIOP47 vadeli-listeli')); R.append(row(E[m],nm+' tum h1'))
print(pd.DataFrame(R).set_index('set').to_string())
# gap-eslesmeli 10:30->kapanis (TC, tum h1)
bins=[-1,-0.005,0.005,0.02,0.04,0.06,0.08,1]
for nm,m in [('TC tum h1',E.TC),('TC VIOP47',E.TC&E.viop47)]:
    t_=E[m].assign(gb=lambda x:pd.cut(x.gap1,bins)); b=base.assign(gb=pd.cut(base.gap1,bins))
    pm=b.groupby('gb',observed=True).s_1030c.mean(); d=t_.s_1030c-t_.gb.map(pm).astype(float)
    mm,tt,nn=cl_t(d,t_.date_1); print(f'{nm}: 10:30->kapanis gap-eslesmeli fazla {mm*1e4:.1f} (t {tt:.2f}, n {nn})')
# piyasa notr 10:30->kapanis (ayni gun h1 VIOP47 ortalamasi)
xs=E[E.viop47].groupby('date_1').s_1030c.mean()
t_=E[E.TC&E.viop47].copy(); t_['mn']=t_.s_1030c-t_.date_1.map(xs)
mm,tt,nn=cl_t(t_.mn,t_.date_1); print(f'TC VIOP47 10:30->kapanis piyasa-notr brut {mm*1e4:.1f} (t {tt:.2f}, n {nn})')
dm=(t_.s_1030c-15e-4-t_.tk).groupby(t_.date_1).sum().sort_values()
q=t_[~t_.date_1.isin(dm.index[-10:])]; mm,tt,nn=cl_t(q.s_1030c-15e-4-q.tk,q.date_1); print(f'TC VIOP47 10:30->kapanis @15+tik en iyi 10 gun haric {mm*1e4:.1f} (t {tt:.2f}, n {nn})')
q=t_[~t_.date_1.isin(list(dm.index[-10:])+list(dm.index[:10]))]; mm,tt,nn=cl_t(q.s_1030c-15e-4-q.tk,q.date_1); print(f'TC VIOP47 10:30->kapanis @15+tik simetrik 10+10 haric {mm*1e4:.1f} (t {tt:.2f}, n {nn})')
# vadeli VWAP vs spot TWAP ayni olaylar
FE=pd.read_parquet(f'{OUT}/_ev_fut.parquet')[['sym','date','sf_vc','sf_oc','f1_trades']]
j=t_.merge(FE,on=['sym','date'],how='inner'); j=j[j.f1_trades>0]
print(f'ayni TC VIOP47 olaylari (n {len(j)}): spot TWAP->kapanis {j.s_twapc.mean()*1e4:.0f} | vadeli VWAP->kapanis {j.sf_vc.mean()*1e4:.0f} | spot 10:30->kapanis {j.s_1030c.mean()*1e4:.0f} | vadeli open->close {j.sf_oc.mean()*1e4:.0f} | spot open->close {j.s_oc.mean()*1e4:.0f}')
