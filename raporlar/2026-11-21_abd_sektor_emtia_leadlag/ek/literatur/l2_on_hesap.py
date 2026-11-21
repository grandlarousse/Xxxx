import sys; sys.path.insert(0,'/home/user/Xxxx/raporlar/2026-11-21_abd_sektor_emtia_leadlag/kod')
import ortak as o, pandas as pd, numpy as np
pairs=[('USO','XLE'),('USO','XOP'),('USO','JETS'),('USO','SPY'),('GLD','GDX'),('SLV','SIL'),('CPER','COPX'),('CPER','FCX'),('UNG','EQT'),('BTC-USD','COIN'),('BTC-USD','MSTR'),('BTC-USD','MARA'),('HYG','SPY'),('HYG','IWM'),('TLT','XLU'),('TLT','KRE'),('UUP','EEM'),('FXI','KWEB'),('^VIX','SPY')]
sig=pd.DataFrame({a:o.hizali_getiri(a) for a,_ in pairs if a!='^VIX'})
v=np.log(o.oku('^VIX')['adjclose']).diff(); sig['^VIX']=v.reindex(o.takvim())
ts=o.panel('adjclose',['^VIX','^VIX3M']); sig['VIXR']=ts['^VIX']/ts['^VIX3M']
for (a,b) in pairs+[('VIXR','SPY')]:
  f=o.ileri_getiri([b],1)[b]
  for nm,bs,be in (('IS',None,'2018-12-31'),('OOS','2019-01-01',None),('SON','2024-01-01',None)):
    x=sig[a]; d=pd.concat([x,f],axis=1).dropna(); d=d.loc[bs:be]
    if len(d)<200: print(a,b,nm,'n',len(d)); continue
    c=d.iloc[:,0].corr(d.iloc[:,1]); print(f"{a:8s}->{b:5s} {nm:3s} n={len(d):5d} corr={c:+.3f} t~{c*np.sqrt(len(d)):+.1f}")
print('--- kismi (hedefin kendi gecikmeli getirisi kontrol, HAC t lag5)')
import statsmodels.api as sm
for (a,b) in [('HYG','SPY'),('USO','XLE'),('^VIX','SPY'),('TLT','XLU'),('GLD','GDX'),('CPER','FCX')]:
  f=o.ileri_getiri([b],1)[b]; own=o.hizali_getiri(b)
  for nm,bs,be in (('IS',None,'2018-12-31'),('OOS','2019-01-01',None)):
    d=pd.concat([f,sig[a],own],axis=1).dropna().loc[bs:be]
    m=sm.OLS(d.iloc[:,0],sm.add_constant(d.iloc[:,1:])).fit(cov_type='HAC',cov_kwds={'maxlags':5})
    print(f"{a}->{b} {nm} b_oncu={m.params.iloc[1]:+.4f} t={m.tvalues.iloc[1]:+.2f} | b_kendi={m.params.iloc[2]:+.4f} t={m.tvalues.iloc[2]:+.2f}")
