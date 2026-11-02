# T21: Bedelsiz (bonus) kalıntısı taraması: ham açılış gap'i ≈ -ln(1+k) (k tipik bedelsiz oranı), piyasa sakin, ertesi günlerde geri dönüş yok -> düzeltilmemiş bedelsiz adayı
import warnings; warnings.filterwarnings("ignore")
import sys, json; sys.path.insert(0,'/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_metodoloji'); sys.path.insert(0,'/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/code')
import vm, pandas as pd, numpy as np
from universe import VIOP
x=vm.raw('XU100.IS').copy(); x.index=pd.DatetimeIndex(x['ldate'].values); x=x[~x.index.duplicated()]; xg=np.log(x['o']/x['c'].shift(1))
ks=[0.05,0.1,0.15,0.2,0.25,0.3,0.4,0.5,0.6,0.75,1,1.5,2,3,4,5,9]
rows=[]; spl=0
for s in VIOP:
    m=json.load(open(f'{vm.B}/meta/{s}.IS.json')); spl+=len(m.get('splits') or {})
    d=vm.raw(s+'.IS').copy(); d.index=pd.DatetimeIndex(d['ldate'].values); d=d[~d.index.duplicated(keep='last')]; d=d[d.index>='2014-01-01']
    gap=np.log(d['o']/d['c'].shift(1)); cc=np.log(d['adj']).diff()
    for t in d.index[(gap<-0.04)]:
        k=[kk for kk in ks if abs(gap[t]+np.log(1+kk))<0.004]
        if not k: continue
        mk=xg.get(t,np.nan)
        if not (abs(mk)<0.01): continue
        rows.append(dict(sym=s,date=t.date(),gap=round(gap[t],4),k=k[0],cc=round(cc[t],4),xu_gap=round(mk,4),filtre_yakalar=abs(cc[t])>np.log(1.105) if t>=pd.Timestamp('2020-03-13') else abs(cc[t])>np.log(1.205)))
R=pd.DataFrame(rows)
print('Yahoo meta split olayı (47 hisse toplam):',spl)
print('Aday sayısı (2014+):',len(R),' filtrenin yakaladığı:',int(R.filtre_yakalar.sum()) if len(R) else 0,' kaçan:',int((~R.filtre_yakalar).sum()) if len(R) else 0)
if len(R): print(R[~R.filtre_yakalar].sort_values('date').to_string(index=False))
