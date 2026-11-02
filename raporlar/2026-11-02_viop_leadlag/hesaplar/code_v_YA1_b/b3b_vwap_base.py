# vadeli VWAP->kapanis short icin baz/plasebo: normal gunler, gap-eslesmeli, bayat sinyal
import pandas as pd, numpy as np
from blib import *
E=pd.read_parquet(f'{OUT}/_ev_fut.parquet')
ok=(E.f1_open>0)&(E.f1_close>0)&(E.f1_trades>0)&(E.f1_vwap>0)&E.ok1&E.date.ge('2020-03-13')
E=E[ok].copy()
E['fgap']=E.f1_vwap/E.f1_prev_settle-1   # bilinmez (VWAP gun sonu), sadece tanimlayici
E['net']=E.sf_vc-15e-4-E.tk
ev=E.TC|E.TCs|E.TU_src|E.TU_s|E.NEAR|E.BC|(E.R>1.06)|(E.R<0.94)
b=E[~ev]
print('kosulsuz (olay disi) vadeli VWAP->close short brut', summ(b.assign(n2=b.sf_vc),'n2'))
for a,c in [('2020-03-13','2020-12-31'),('2021-01-01','2023-12-31'),('2024-01-01','2026-12-31')]:
    q=b[(b.date>=a)&(b.date<=c)]; print('   ',a[:4],c[:4],round(q.sf_vc.mean()*1e4,1),'n',len(q))
tc=E[E.TC]
# gap-eslesmeli (spot gap1 kovalari) -- vadeli VWAP->close
bins=[-1,-0.02,-0.005,0.005,0.02,0.04,0.06,0.08,0.12,1]
tc=tc.assign(gb=pd.cut(tc.gap1,bins)); b2=b.assign(gb=pd.cut(b.gap1,bins))
pm=b2.groupby('gb',observed=True).sf_vc.mean()
d=tc.sf_vc-tc.gb.map(pm).astype(float)
m,t,n=cl_t(d,tc.date_1); print(f'TC vadeli VWAP->close: brut {tc.sf_vc.mean()*1e4:.1f}; gap-eslesmeli kontrole gore fazla {m*1e4:.1f} (t {t:.2f}, n {n})')
print(pd.DataFrame({'olay_n':tc.groupby('gb',observed=True).size(),'olay':tc.groupby('gb',observed=True).sf_vc.mean()*1e4,'kontrol_n':b2.groupby('gb',observed=True).size(),'kontrol':pm*1e4}).round(1).to_string())
# piyasa notr: ayni gun VIOP47 vadeli VWAP->close ortalamasi
xs=E.groupby('date_1').sf_vc.agg(['sum','count'])
tc=tc.join(xs,on='date_1'); tc['mn']=tc.sf_vc-(tc['sum']-tc.sf_vc)/(tc['count']-1)
r=summ(tc.assign(n2=tc.mn-15e-4-tc.tk),'n2'); print('TC vadeli VWAP->close piyasa-notr @15+tik',r)
# uc deger
dm=tc.groupby('date_1').net.sum().sort_values()
for lab,sub in [('tum',tc),('simetrik 10+10 gun haric',tc[~tc.date_1.isin(list(dm.index[:10])+list(dm.index[-10:]))]),('en iyi 10 gun haric',tc[~tc.date_1.isin(dm.index[-10:])])]:
    print('TC vadeli VWAP->close @15+tik',lab,summ(sub,'net'))
print('TC yillar @15+tik:',tc.groupby('year').net.agg(lambda x: round(x.mean()*1e4,1)).to_dict(), tc.groupby('year').size().to_dict())
# yol: vadeli open->VWAP, VWAP->close, high
print('TC t+1 vadeli yol (bps, ort/medyan): open->vwap', round((tc.f1_vwap/tc.f1_open-1).mean()*1e4,1),round((tc.f1_vwap/tc.f1_open-1).median()*1e4,1),
      '| open->high',round((tc.f1_high/tc.f1_open-1).median()*1e4,1),'| open->close',round((tc.f1_close/tc.f1_open-1).mean()*1e4,1))
# hisse dagilimi
g=tc.groupby('sym').net.agg(['mean','count']); print('hisse>0',int((g['mean']>0).sum()),'/',len(g),' LOSO aralik',round(min(tc[tc.sym!=s].net.mean() for s in g.index)*1e4,1),round(max(tc[tc.sym!=s].net.mean() for s in g.index)*1e4,1))
print(g.sort_values('count',ascending=False).head(10).assign(mean=lambda x:(x['mean']*1e4).round(0)).T.to_string())
