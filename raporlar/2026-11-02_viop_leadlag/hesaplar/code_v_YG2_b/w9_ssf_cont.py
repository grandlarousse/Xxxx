"""VİOP tarafı: SSF uzlaşma_t -> uzlaşma_{t+1} getirisi CA YÖNÜNDE (devam) mı? Eşik ve likidite kırılımı. Giriş = 18:05-18:15 VWAP (uzlaşma) vekili."""
import numpy as np, pandas as pd, vlib as v
D='/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data'
A=pd.read_parquet(v.RES+'/panel.parquet'); S=A[A.sym!='XU030'].sort_values(['sym','date']).copy()
S['liq']=S.groupby('sym')['TL'].transform(lambda z:z.shift(1).rolling(60,min_periods=20).median()); S['liqr']=S.groupby('date')['liq'].rank(pct=True)
P=pd.read_parquet(v.RES+'/w7_ssfpanel.parquet')[['date','sym','settle','expiry','trades']]
p=pd.read_parquet(D+'/viop_panel.parquet',columns=['date','root','segment','expiry','settle','trades','value_tl'])
p=p[p.segment=='SSF'].drop_duplicates(['root','expiry','date'],keep='last'); pd_={(a,b,c):x for a,b,c,x in zip(p.root,p.expiry,p.date,p.settle)}
vt={(a,b,c):x for a,b,c,x in zip(p.root,p.expiry,p.date,p.value_tl)}
cal=sorted(A.date.unique()); nx=dict(zip(cal[:-1],cal[1:]))
P=P.merge(S[['date','sym','CA','liqr']],on=['date','sym'],how='inner'); P=P[P.CA.notna()]
P['F_n']=[pd_.get((s,e,nx.get(d)),np.nan) for s,e,d in zip(P.sym,P.expiry,P.date)]
P['ssf_tl']=[vt.get((s,e,d),np.nan) for s,e,d in zip(P.sym,P.expiry,P.date)]
P['fr']=np.log(P.F_n.astype(float)/P.settle.astype(float)); P.loc[P.fr.abs()>0.105,'fr']=np.nan
P['fr_c']=-P['fr']   # port() -sign(CA) kullanır; devam için işareti çevir
P['ssfr']=P.groupby('date')['ssf_tl'].rank(pct=True)
for thr in [25,50,100]:
    for lab,m in [('tümü',P.CA.notna()),('SSF hacmi üst 1/3',P.ssfr>2/3),('SSF hacmi alt 2/3',P.ssfr<=2/3),('SSF işlem>=50',P.trades>=50)]:
        dd,x=v.port(P[m],'CA','fr_c',thr/1e4); s=v.summ(dd,x)
        print(f'SSF DEVAM +sign(CA) |CA|>{thr:3d} {lab:18s}',s)
d=P[['fr','CA','date']].dropna(); b,se=v.ols_cl(d['fr'],d[['CA']],d['date']); print('fr ~ CA %.3f (t %.1f)'%(b[1],b[1]/se[1]))
for yr in [2024,2025,2026]:
    dd,x=v.port(P[P.date.dt.year==yr],'CA','fr_c',0.0025); print(yr,v.summ(dd,x))
