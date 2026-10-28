import pandas as pd, numpy as np
exec(open('load.py').read())
c=x30['c']; h=x30['h'].fillna(c); l=x30['l'].fillna(c)
f=fx['c'].reindex(c.index).ffill()
dd=c/c.rolling(60).max()-1
# episode start = first day dd<=-0.17 after >=60 days w/o; sample = start+7 trading days
starts=[]; last=-999
for i,v in enumerate(dd.values):
    if v<=-0.17 and i-last>60: starts.append(i)
    if v<=-0.17: last=i
def fp(i,up,dn,N):
    p0=c.iloc[i]
    for j in range(i+1,min(i+N+1,len(c))):
        if h.iloc[j]>=p0*(1+up): return 1
        if l.iloc[j]<=p0*(1-dn): return 0
    return np.nan
rows=[]
for s in starts:
    i=s+7
    if i+42>=len(c): continue
    rows.append(dict(start=c.index[s].date(),t=c.index[i].date(),dd_t=round(dd.iloc[i]*100,1),
        r21=round((c.iloc[i+21]/c.iloc[i]-1)*100,1),r42=round((c.iloc[i+42]/c.iloc[i]-1)*100,1),
        min42=round((l.iloc[i+1:i+43].min()/c.iloc[i]-1)*100,1),
        usd42=round(((c.iloc[i+42]/f.iloc[i+42])/(c.iloc[i]/f.iloc[i])-1)*100,1) if c.index[i]>=pd.Timestamp('2005-02-01') else np.nan,
        L=fp(i,0.053,0.045,20)))
R=pd.DataFrame(rows); print(R.to_string())
print(R[['r21','r42','min42','usd42','L']].describe().loc[['count','mean','50%','min']].round(2))
print('poz oran r21',(R.r21>0).mean().round(2),'r42',(R.r42>0).mean().round(2))
R2=R[R.t>=pd.Timestamp('2005-01-01').date()]
print('2005+: n',len(R2),'r21 med',R2.r21.median(),'r42 med',R2.r42.median(),'L(+5.3 önce)',R2.L.mean().round(2),'min42 med',R2.min42.median())
