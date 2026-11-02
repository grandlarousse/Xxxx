"""Veri kalitesi çürütmeleri: (1) günlük C vs h1 ölçek uyumsuzluğu (bölünme/bedelsiz farkı) -> ay bazında medyan CA ve medyan log(P0730/O);
(2) Yahoo günlük C = resmi kapanış mı? VİOP vade sonu kesin uzlaşma (= spot kapanış seansı fiyatı) ile karşılaştır, tüm vadeler 2017+;
(3) CA=0 payı, CA dağılımı."""
import pandas as pd, numpy as np
RES='/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_YG2_b/res'
D='/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data'
A=pd.read_parquet(RES+'/panel.parquet'); A=A[A.sym!='XU030']
A['m']=A.date.dt.to_period('M')
g=A.groupby(['sym','m'])
M=pd.DataFrame({'medCA':g['CA'].median()*1e4,'medO730':g['r1_1'].median()*1e4,'medgap':g['gap1'].median()*1e4,'n':g['CA'].count()})
print('ay-hisse medyan CA (bps) dağılımı:'); print(M.loc[M.n>=5,'medCA'].describe().round(1))
print('|medCA|>30 bps olan ay-hisse:'); print(M[(M.n>=5)&(M.medCA.abs()>30)])
print('medyan O->07:30 |.|>60:'); print(M[(M.medO730.abs()>60)].head(20))
# CA=0 payı
print('CA==0 payı:', (A['CA'].abs()<1e-9).mean().round(3), ' CA mevcut:', A['CA'].notna().sum())
print((A.groupby('sym')['CA'].apply(lambda x:(x.abs()<1e-9).mean())).sort_values().round(2).to_string())
# (2) vade sonu uzlaşma
p=pd.read_parquet(D+'/viop_panel.parquet', columns=['date','root','segment','expiry','settle','close'])
p=p[(p.segment=='SSF')&(p.date==p.expiry)]
rows=[]
for s in A.sym.unique():
    d=pd.read_parquet(f'{D}/daily/{s}.IS.parquet'); d.index=pd.DatetimeIndex(d['ldate']); d=d[~d.index.duplicated(keep='last')]
    q=p[p.root==s].set_index('date')
    j=q.join(d[['c']],how='inner')
    j['diff_bps']=np.log(j['c']/j['settle'])*1e4; j['sym']=s; rows.append(j.reset_index())
E=pd.concat(rows)
E['h1per']=E.date>='2023-11-30'
print('Vade sonu: Yahoo C vs kesin uzlaşma, |fark| dağılımı (bps)')
for k,g in E.groupby('h1per'):
    ad=g.diff_bps.abs()
    print('h1 dönemi' if k else '2017-2023', len(g), 'tam eşit %', round((ad<0.5).mean()*100,1), ' |fark|>5bps %', round((ad>5).mean()*100,1), ' >50bps %', round((ad>50).mean()*100,1))
print(E[E.h1per&(E.diff_bps.abs()>5)][['date','sym','c','settle','diff_bps']].to_string())
E.to_csv(RES+'/w2_expiry_check.csv',index=False)
