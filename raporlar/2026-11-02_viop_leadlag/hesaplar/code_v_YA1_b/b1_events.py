# olay siniflari + ertesi gun degiskenleri
import pandas as pd, numpy as np
from blib import *
P=pd.read_parquet(f'{OUT}/_panel.parquet')
xu=pd.read_parquet(f'{OUT}/_xu100.parquet')
xu['date']=pd.to_datetime(xu.index.tz_convert(None) if xu.index.tz is not None else xu.index).normalize()
xu=xu.reset_index(drop=True).drop_duplicates('date').set_index('date')
xc=xu.c
P=P.sort_values(['sym','date']).reset_index(drop=True)
g=P.groupby('sym',sort=False)
for k in [1,2,3,5]:
    for c in ['date','o','c','h','l','base','R','ca','consec','v']:
        P[f'{c}_{k}']=g[c].shift(-k)
# ertesi gun
P['gap1']=P.o_1/P.base_1-1
P['intra1']=P.c_1/P.o_1-1
P['cc1']=P.R_1-1
P['intra2']=P.c_2/P.o_2-1
P['intra3']=P.c_3/P.o_3-1
# t+1 kapanis -> t+5 kapanis (adj ile)
P['adj_1']=g['adj'].shift(-1); P['adj_5']=g['adj'].shift(-5)
P['r2_5']=P.adj_5/P.adj_1-1
x1=xc.reindex(P.date_1).values; x5=xc.reindex(P.date_5).values
P['x2_5']=x5/x1-1
xo=xu.o.reindex(P.date_1).values; P['xintra1']=xc.reindex(P.date_1).values/xo-1
ok1=(P.consec_1==True)&(P.ca_1==False)
lim=P.lim; tk=tick(P.c)/P.c
up=1+lim; dn=1-lim
nca=(P.ca==False)&P.reg.isin(['P10','P20'])
P['TC']=nca&(P.R>=up-0.0075)&(P.c>=0.999*P.h)
P['TCs']=nca&(P.R>=up-np.minimum(tk+0.001,0.0075))&(P.c>=P.h-1e-9)
P['TU_src']=nca&(P.Rh>=up-0.0075)&(P.R<up-0.0175)
P['TU_s']=nca&(P.Rh>=up-np.minimum(tk+0.001,0.0075))&(P.R<up-0.01)&~P.TC
P['NEAR']=nca&(P.Rh>=up-0.0075)&(P.Rh<up-np.minimum(tk+0.001,0.0075))&(P.R<up-0.0175)
P['BC']=nca&(P.R<=dn+0.0075)&(P.c<=1.001*P.l)
P['ok1']=ok1
# futures listesi
V=pd.read_parquet(f'{D}/viop_panel.parquet',columns=['date','und','segment'])
V=V[V.segment=='SSF']
first=V.groupby('und',observed=True).date.min()
P['fut_first']=P.sym.map(first)
P['fut_listed']=P.viop47&(P.date>=P.fut_first)
P['year']=P.date.dt.year
keep=['sym','date','reg','lim','viop47','fut_listed','year','o','h','l','c','v','R','Rh','dy','base','date_1','date_2','o_1','c_1','gap1','intra1','cc1','intra2','intra3','r2_5','x2_5','xintra1','R_1','Rl','ok1','TC','TCs','TU_src','TU_s','NEAR','BC','ca','consec','f']
P[keep].to_parquet(f'{OUT}/_full.parquet')
for c in ['TC','TCs','TU_src','TU_s','NEAR','BC']:
    s=P[P[c]&ok1]
    print(c, s.groupby('reg').size().to_dict(), 'viop47 P10', int((s.viop47&(s.reg=='P10')).sum()),
          'gap1 P10 bps', round(s[s.reg=='P10'].gap1.mean()*1e4,1), 'intra1', round(s[s.reg=='P10'].intra1.mean()*1e4,1))
print('fut_first', first.reindex(['BRSAN','CIMSA','DOAS','ASTOR','AKSEN','ALARK','HEKTS','ODAS','AEFES','TRALT','TRMET','SASA']).to_dict())
