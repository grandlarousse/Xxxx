"""Kontrol: USDTRY_{t-1} -> ENKAI intra ilişkisinde uç günlerin katkısı."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vlib as V, numpy as np, pandas as pd
pd.set_option('display.width', 200)
E=V.decomp('ENKAI'); X=V.decomp('XU100'); U=V.fx_prev('TRY=X'); T,_=V.us_prev('TUR')
d=pd.concat([U.rename('USD'),T.rename('TUR'),E['gap'].rename('Egap'),E['intra'].rename('Eintra'),X['gap'].rename('Xgap'),X['intra'].rename('Xintra')],axis=1).dropna(subset=['USD','Eintra']).loc['2014':]
d['absU']=d.USD.abs()
top=d.sort_values('absU',ascending=False).head(25)
print(top.round(4).to_string())
for k in [0,4,10,20,32,60]:
    dd=d.drop(d.sort_values('absU',ascending=False).index[:k])
    print(k, 'en büyük |USD| günü atıldı:', [(round(a,3),round(b,2)) for a,b,_ in [V.corr_t(dd.Eintra,dd.USD),V.corr_t(dd.Eintra,dd.USD,V.IS0,V.SPLIT),V.corr_t(dd.Eintra,dd.USD,V.SPLIT)]])
# Spearman (sıra) korelasyonu
from scipy.stats import spearmanr
for lab,m in [('ALL',d.index>='2014'),('IS',d.index<V.SPLIT),('OOS',d.index>=V.SPLIT)]:
    print('Spearman', lab, round(spearmanr(d.USD[m], d.Eintra[m]).correlation,3), ' TUR:', round(spearmanr(d.TUR[m].fillna(0), d.Eintra[m]).correlation,3))
