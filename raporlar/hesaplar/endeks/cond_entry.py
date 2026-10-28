import pandas as pd, numpy as np
exec(open('load.py').read())
c=x30['c']; h=x30['h'].fillna(c); l=x30['l'].fillna(c)
dd=c/c.rolling(60).max()-1
starts=[]; last=-999
for i,v in enumerate(dd.values):
    if v<=-0.17 and i-last>60: starts.append(i)
    if v<=-0.17: last=i
def sim(t, trig, side, stop, tgt, wait=12, hold=25):
    p0=c.iloc[t]; e=p0*(1+trig)
    for j in range(t+1, min(t+wait+1,len(c))):
        hit = h.iloc[j]>=e if trig>0 else l.iloc[j]<=e
        if hit:
            for k in range(j+1, min(j+hold+1,len(c))):
                if side=='S':
                    if h.iloc[k]>=e*(1+stop): return 'stop'
                    if l.iloc[k]<=e*(1-tgt): return 'tgt'
                else:
                    if l.iloc[k]<=e*(1-stop): return 'stop'
                    if h.iloc[k]>=e*(1+tgt): return 'tgt'
            return 'time'
    return 'nofill'
for label,args in [('SHORT tepki: +%3 dolum, stop +%3, hedef -%7',(0.03,'S',0.03,0.07)),
                   ('SHORT tepki: +%3.5 dolum, stop +%3.5, hedef -%6',(0.035,'S',0.035,0.06)),
                   ('LONG retest: -%3.5 dolum, stop -%3.5, hedef +%6',(-0.035,'L',0.035,0.06)),
                   ('LONG şimdi(dolum 0): stop -%4.5, hedef +%5.3',(0.0001,'L',0.045,0.053))]:
    res=[]
    for s in starts:
        t=s+7
        if t+40>=len(c): continue
        res.append(sim(t,*args))
    s=pd.Series(res).value_counts(); n=len(res)
    filled=n-s.get('nofill',0)
    print(label,'| n',n,dict(s), '| dolum oranı',round(filled/n,2),'| dolunca hedef oranı', round(s.get('tgt',0)/max(filled,1),2))
