# T07: Yahoo 'adj' (temettü düzeltmeli) ile 'c' farkı: düzeltme adımı (k_t) doğru günde mi? Ham fiyat düşüşü hangi günde?
import warnings; warnings.filterwarnings("ignore")
import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_metodoloji'); sys.path.insert(0,'/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/code')
import vm, numpy as np, pandas as pd
from universe import VIOP
x=vm.raw('XU100.IS'); x=pd.Series(x['c'].values,index=pd.DatetimeIndex(x['ldate'].values)); x=x[~x.index.duplicated()]; mx=np.log(x).diff()
ev=[]
for s in VIOP:
    d=vm.raw(s+'.IS').copy(); d.index=pd.DatetimeIndex(d['ldate'].values); d=d[~d.index.duplicated(keep='last')]
    d=d[d.index>=pd.Timestamp('2010-01-01')]
    k=np.log(d['adj']/d['c']).diff()
    rc=np.log(d['c']).diff(); ex=rc-mx.reindex(rc.index)
    gap_raw=np.log(d['o']/d['c'].shift(1))
    for t in k.index[(k.abs()>0.002)]:
        i=d.index.get_loc(t)
        if i<2 or i>len(d)-3: continue
        ev.append(dict(sym=s,date=t,k=k.iloc[i],ex_m1=ex.iloc[i-1],ex_0=ex.iloc[i],ex_p1=ex.iloc[i+1],gap_m1=gap_raw.iloc[i-1],gap_0=gap_raw.iloc[i],gap_p1=gap_raw.iloc[i+1]))
E=pd.DataFrame(ev); print('olay sayısı (|k|>0,2%):',len(E), ' k>0 (temettü yönü):',(E.k>0).sum(),' k<0:',(E.k<0).sum())
import statsmodels.api as sm
for col in ['ex_m1','ex_0','ex_p1','gap_m1','gap_0','gap_p1']:
    m=sm.OLS(E[col],sm.add_constant(E['k'])).fit(); print(f'{col}: eğim={m.params["k"]:+.2f} (t={m.tvalues["k"]:+.1f})')
print('k çok büyük (>%10) olaylar (bedelsiz/hata adayı):'); print(E[E.k.abs()>0.10][['sym','date','k','ex_0','gap_0']].head(20).to_string(index=False))
# k'nin ex_0 ile eşleşme oranı: ham açılış gap'i ≈ -k (temettü düşüşü) mi?
E['dogru_gun']=(E['gap_0']<-0.5*E['k'])
print('Ham açılış gap_0 < -k/2 (düşüş aynı gün) oranı:',round(E['dogru_gun'].mean(),3), '| gap_p1 < -k/2 (düşüş ertesi gün):', round((E['gap_p1']<-0.5*E['k']).mean(),3), '| gap_m1:', round((E['gap_m1']<-0.5*E['k']).mean(),3))
E.to_csv('/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_metodoloji/t07_div_events.csv',index=False)
