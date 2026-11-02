# Yahoo c bolunme/bedelsiz-duzeltilmis -> gercek fiyat seviyesi VIOP vadeli uzlasmasindan (tik maliyeti icin)
import pandas as pd, numpy as np
from blib import *
V=pd.read_parquet(f'{D}/viop_panel.parquet',columns=['date','und','segment','expiry','settle','value_tl'])
V=V[(V.segment=='SSF')&(V.settle>0)]
V=V.sort_values('value_tl').drop_duplicates(['date','und'],keep='last')
F=pd.read_parquet(f'{OUT}/_full.parquet')
m=F[['sym','date','c']].merge(V.rename(columns={'und':'sym'})[['sym','date','settle']],on=['sym','date'],how='left')
m['ratio']=m.settle/m.c
m=m.sort_values(['sym','date'])
m['rmed']=m.groupby('sym').ratio.transform(lambda s:s.rolling(21,min_periods=5,center=True).median())
m['k']=np.where(m.rmed<1.25,1.0,m.rmed/1.015)
m['k']=m.groupby('sym').k.transform(lambda s:s.bfill().ffill())
m['k']=m.k.fillna(1.0)
F=F.merge(m[['sym','date','k']],on=['sym','date'],how='left')
F['px']=F.c*F.k
F.to_parquet(f'{OUT}/_full.parquet')
v=F[F.viop47&F.TC&(F.reg=='P10')]
print('VIOP47 TC: Yahoo-c tik maliyeti ort bps',round((0.01/v.c).mean()*1e4,1),' gercek fiyatla',round((0.01/v.px).mean()*1e4,1),' medyan',round((0.01/v.px).median()*1e4,1), ' >15bps oran',round(((0.01/v.px)>15e-4).mean(),3))
