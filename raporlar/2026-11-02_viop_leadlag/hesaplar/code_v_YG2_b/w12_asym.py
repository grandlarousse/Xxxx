"""Asimetri: CA>0 (alış dengesizliği, fiyat yukarı) ve CA<0 için ayrı eğimler ve bacaklar (excess / XU030 hedge'li)."""
import numpy as np, pandas as pd, vlib as v
A=pd.read_parquet(v.RES+'/panel.parquet'); XU=A[A.sym=='XU030'].set_index('date')
S=A[A.sym!='XU030'].copy(); S['yx']=S['y']-S.groupby('date')['y'].transform('mean'); S['yh']=S['y']-S['date'].map(XU['y'])
W=S[S.CA.notna()].copy(); W['CAp']=W.CA.clip(lower=0); W['CAm']=W.CA.clip(upper=0)
for y in ['y','yx','yh']:
    d=W[[y,'CAp','CAm','date','sym']].dropna(); Z=v.demean2(d,[y,'CAp','CAm'])
    b,se=v.ols_cl(d[y],d[['CAp','CAm']],d['date']); b2,se2=v.ols_cl(Z[y],Z[['CAp','CAm']],d['date'])
    print(f'{y}: CA+ {b[1]:+.3f} (t {b[1]/se[1]:+.1f}) CA- {b[2]:+.3f} (t {b[2]/se[2]:+.1f}) | FE: CA+ {b2[1]:+.3f} ({b2[1]/se2[1]:+.1f}) CA- {b2[2]:+.3f} ({b2[2]/se2[2]:+.1f})')
for thr in [25,50,100]:
    for side in ['long','short']:
        print(thr,side,'yx',v.summ(*v.port(W,'CA','yx',thr/1e4,side=side)),' yh',v.summ(v.port(W,'CA','yh',thr/1e4,side=side)[0]))
print('CA>0 payı (|CA|>50):',(W[W.CA.abs()>0.005].CA>0).mean().round(2))
