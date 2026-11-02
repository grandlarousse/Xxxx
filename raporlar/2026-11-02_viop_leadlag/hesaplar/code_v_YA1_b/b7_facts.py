# (a) ve (d) olgularinin basit vs log getiriyle kontrolu + TC sonrasi t+2 gap
import pandas as pd, numpy as np
from blib import *
F=pd.read_parquet(f'{OUT}/_full.parquet').sort_values(['sym','date'])
g=F.groupby('sym'); F['gap2']=g.gap1.shift(-1)
P=pd.read_parquet(f'{OUT}/_panel.parquet').sort_values(['sym','date'])
gp=P.groupby('sym'); P['ca_any']=sum(gp.ca.shift(-k).fillna(True).astype(bool) for k in range(1,6))>0
F=F.merge(P[['sym','date','ca_any']],on=['sym','date'],how='left')
for cls in ['TC','BC']:
    for uni,m in [('tum',F.sym.notna()),('VIOP47',F.viop47)]:
        E=F[F[cls]&m&(F.reg=='P10')&F.ok1]
        gm,gt,gn=cl_t(E.gap1,E.date_1)
        e=E[(E.ca_any==False)&E.r2_5.notna()]
        xs=e.r2_5-e.x2_5; xl=np.log1p(e.r2_5)-np.log1p(e.x2_5)
        sm,st,_=cl_t(xs,e.date_1); lm,lt,_=cl_t(xl,e.date_1)
        dm=xs.groupby(e.date_1).mean(); dl=xl.groupby(e.date_1).mean()
        print(f'{cls} {uni:6s} n {gn}: gap1 {gm*1e4:.0f} (t {gt:.1f}) | t+2..5 XU100-fazla: basit islem {sm*1e4:.0f} (t {st:.1f}) gun {dm.mean()*1e4:.0f} | log islem {lm*1e4:.0f} (t {lt:.1f}) gun {dl.mean()*1e4:.0f} | medyan basit {xs.median()*1e4:.0f}')
E=F[F.TC&(F.reg=='P10')&F.ok1]
for uni,m in [('tum',E.sym.notna()),('VIOP47',E.viop47)]:
    q=E[m]; a,t,n=cl_t(q.gap2,q.date_1); b,tb,_=cl_t(-q.intra2,q.date_1)
    print(f'TC {uni}: t+2 gap {a*1e4:.0f} (t {t:.1f}) ; t+2 gun-ici short {b*1e4:.0f} (t {tb:.1f}); n {n}')
