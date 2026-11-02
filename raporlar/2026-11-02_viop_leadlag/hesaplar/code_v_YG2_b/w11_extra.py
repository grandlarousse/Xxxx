"""Excess versiyonda uç gün bağımlılığı; yalnız-uzun (açığa satışsız) + XU030 hedge'li net."""
import numpy as np, pandas as pd, vlib as v
A=pd.read_parquet(v.RES+'/panel.parquet'); XU=A[A.sym=='XU030'].set_index('date')
S=A[A.sym!='XU030'].sort_values(['sym','date']).copy()
S['yx']=S['y']-S.groupby('date')['y'].transform('mean'); S['yh']=S['y']-S['date'].map(XU['y'])
S['liq']=S.groupby('sym')['TL'].transform(lambda z:z.shift(1).rolling(60,min_periods=20).median()); S['liqr']=S.groupby('date')['liq'].rank(pct=True)
W=S[S.CA.notna()].copy()
bx,_=v.port(W,'CA','yx',0.0025)
for k in [10,20,40]:
    print(f'excess: en iyi {k} gün hariç', v.summ(bx.drop(bx.sort_values().index[-k:])))
def tick(p_):
    p_=np.asarray(p_,float); return np.select([p_<20,p_<50,p_<100,p_<250,p_<500,p_<1000,p_<2500],[0.01,0.02,0.05,0.10,0.25,0.50,1.00],2.50)
W['tickb']=1e4*tick(W['C'])/W['C']
print('\nYalnız uzun (CA<0, C\'den al, ertesi 07:30 sat), XU030 vadelisiyle hedge (yh); maliyet 4 + 0.5*tik + 3 (hedge)')
for thr in [25,50,100]:
    for lab,m in [('tümü',W.CA.notna()),('liq alt 2/3',W.liqr<=2/3)]:
        X=W[m&(W.CA< -thr/1e4)][['date','yh','tickb','y']].dropna()
        g=(X.yh*1e4).groupby(X.date).mean(); n=(X.yh*1e4-4-0.5*X.tickb-3).groupby(X.date).mean()
        print(f'  |CA|>{thr} {lab}: brüt hedge\'li {v.summ(g/1e4)}  net {v.summ(n/1e4)}  işlem/gün {X.groupby("date").size().mean():.1f}')
