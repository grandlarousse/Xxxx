import pandas as pd, numpy as np
exec(open('load.py').read())
df=x30.copy(); c=df['c']; h=df['h'].fillna(c); l=df['l'].fillna(c)
dd=c/c.rolling(60).max()-1; sma50=c.rolling(50).mean()
def first_pass(i,up,dn,N):
    p0=c.iloc[i]
    for j in range(i+1,min(i+N+1,len(c))):
        hu=h.iloc[j]>=p0*(1+up); ld=l.iloc[j]<=p0*(1-dn)
        if hu and ld: return 'both'
        if hu: return 'up'
        if ld: return 'dn'
    return 'none' if i+N<len(c) else 'na'
def run(mask,label,start):
    m=mask & (c.index>=pd.Timestamp(start)) & (c.index<=pd.Timestamp('2026-09-01'))
    idx=np.where(m.values)[0]
    eps=[]; cur=[]
    for i in idx:
        if cur and i-cur[-1]>20: eps.append(cur); cur=[]
        cur.append(i)
    if cur: eps.append(cur)
    out={'n_ep':len(eps)}
    for (up,dn,N,k) in [(0.053,0.045,20,'L_simdi'),(0.04,0.065,25,'S_tepki'),(0.065,0.035,25,'L_retest')]:
        res=[]
        for e in eps:
            r=[first_pass(i,up,dn,N) for i in e]; r=[x for x in r if x!='na']
            if r: res.append(np.mean([x=='up' for x in r]))
        out[k+'_Pup']=round(np.mean(res),2)
    for N in (21,42):
        v=[np.median([c.iloc[i+N]/c.iloc[i]-1 for i in e if i+N<len(c)]) for e in eps if any(i+N<len(c) for i in e)]
        out[f'r{N}_med']=round(np.median(v)*100,1); out[f'r{N}_pos']=round(np.mean(np.array(v)>0),2)
    print(label,start,out)
cond=(dd<=-0.17)&(dd>=-0.30)&(c<sma50)
allm=pd.Series(True,index=c.index)
for st in ['1997-01-01','2005-01-01','2010-01-01']:
    run(cond,'KOŞULLU ',st)
    # unconditional: sample every 21st day to make 'episodes'
    m=pd.Series(False,index=c.index); m.iloc[::25]=True
    run(m,'KOŞULSUZ',st)
# USD-based 2005+
f=fx['c'].reindex(c.index).ffill(); u=(c/f).loc['2005':].dropna()
du=u/u.rolling(60).max()-1
cu=(du<=-0.17)&(du>=-0.35)&(u<u.rolling(50).mean())
idx=np.where(cu.values)[0]; eps=[]; cur=[]
for i in idx:
    if cur and i-cur[-1]>20: eps.append(cur); cur=[]
    cur.append(i)
if cur: eps.append(cur)
for N in (21,42,63):
    v=[np.median([u.iloc[i+N]/u.iloc[i]-1 for i in e if i+N<len(u)]) for e in eps if any(i+N<len(u) for i in e)]
    uu=(u.shift(-N)/u-1).dropna()
    print(f'USD bazlı XU030 2005+ koşullu {N}g: medyan {np.median(v)*100:.1f}% poz {np.mean(np.array(v)>0):.2f} n={len(v)} | koşulsuz medyan {uu.median()*100:.1f}% poz {(uu>0).mean():.2f}')
