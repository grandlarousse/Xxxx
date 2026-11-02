# T08: (a) Yahoo bölünme/bedelsiz olaylarında 'c' düzeltilmiş mi? (b) ±%10,5 filtresinden kaçan bedelsiz kalıntıları (c) açılış fiyatı kalitesi: o==önceki c oranı (2014+)
import warnings; warnings.filterwarnings("ignore")
import sys, json, os; sys.path.insert(0,'/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_metodoloji'); sys.path.insert(0,'/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/code')
import vm, numpy as np, pandas as pd
from universe import VIOP
B=vm.B
x=vm.raw('XU100.IS'); xs=pd.Series(x['c'].values,index=pd.DatetimeIndex(x['ldate'].values)); xs=xs[~xs.index.duplicated()]; mx=np.log(xs).diff()
rows=[]; sus=[]
for s in VIOP:
    m=json.load(open(f'{B}/meta/{s}.IS.json')); sp=m.get('splits',{}) or {}
    d=vm.raw(s+'.IS').copy(); d.index=pd.DatetimeIndex(d['ldate'].values); d=d[~d.index.duplicated(keep='last')]
    r=np.log(d['adj']).diff(); ex=r-mx.reindex(r.index)
    unadj=0
    for ds,ratio in sp.items():
        t=pd.Timestamp(ds); w=r[(r.index>=t-pd.Timedelta(days=3))&(r.index<=t+pd.Timedelta(days=3))]
        if len(w) and w.abs().max()>0.15: unadj+=1
    post=d.index>=pd.Timestamp('2014-01-01')
    dp=d[post]; o_eq=(dp['o']==dp['c'].shift(1)).mean(); o_eq_hl=((dp['o']==dp['c'].shift(1))&(dp['h']==dp['l'])).mean()
    o_eq_y={y:round(((g['o']==g['c'].shift(1)).mean())*100,1) for y,g in dp.groupby(dp.index.year)}
    # 2020-03-13 sonrası -%10,5..-%5 arası, piyasa sakin, ertesi 5 gün toparlanma yok, büyük hacim yok -> bedelsiz kalıntı adayı (kaba)
    cand=r[(r<-0.07)&(r>=np.log(0.895))&(mx.reindex(r.index).abs()<0.015)]
    for t in cand.index:
        sus.append((s,t.date(),round(r[t],3)))
    rows.append(dict(sym=s,n_split=len(sp),split_unadj_suspect=unadj,o_eq_prevc_pct=round(o_eq*100,1),o_eq_prevc_and_hl_pct=round(o_eq_hl*100,2),
                     o_eq_2014=o_eq_y.get(2014),o_eq_2016=o_eq_y.get(2016),o_eq_2020=o_eq_y.get(2020),o_eq_2023=o_eq_y.get(2023),o_eq_2026=o_eq_y.get(2026)))
T=pd.DataFrame(rows); print(T.to_string(index=False))
print('Ortalama o==önceki c oranı (2014+):', T.o_eq_prevc_pct.mean().round(2),'%')
for idx in ['XU030.IS','XU100.IS','XBANK.IS','XUSIN.IS','XHOLD.IS','XLBNK.IS']:
    d=vm.raw(idx).copy(); d.index=pd.DatetimeIndex(d['ldate'].values); d=d[d.index>=pd.Timestamp('2014-01-01')]
    print(idx,'o==önceki c %:', round((d['o']==d['c'].shift(1)).mean()*100,1), ' |o/önceki c -1|<1bp %:', round(((d['o']/d['c'].shift(1)-1).abs()<1e-4).mean()*100,1))
print('Sessiz günde -%7..-%10,5 düşüş (bedelsiz kalıntı/haber adayı) sayısı:',len(sus)); print(sus[:30])
