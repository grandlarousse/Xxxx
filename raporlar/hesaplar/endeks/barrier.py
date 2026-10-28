import pandas as pd, numpy as np
exec(open('load.py').read())
df=x30.copy(); c=df['c']; h=df['h'].fillna(c); l=df['l'].fillna(c)
dd=c/c.rolling(60).max()-1; sma50=c.rolling(50).mean()
cond=(dd<=-0.17)&(dd>=-0.30)&(c<sma50)
idx=np.where(cond.values)[0]
# episode clustering: keep days, but weight by episode (gap>20 days = new episode)
eps=[]; cur=[]
for i in idx:
    if cur and i-cur[-1]>20: eps.append(cur); cur=[]
    cur.append(i)
if cur: eps.append(cur)
print('gün sayısı',len(idx),'epizot',len(eps))
def first_pass(i,up,dn,N):
    p0=c.iloc[i]
    for j in range(i+1,min(i+N+1,len(c))):
        if h.iloc[j]>=p0*(1+up) and l.iloc[j]<=p0*(1-dn): return 'both'
        if h.iloc[j]>=p0*(1+up): return 'up'
        if l.iloc[j]<=p0*(1-dn): return 'dn'
    return 'none' if i+N<len(c) else 'na'
def stats(up,dn,N,label):
    res=[]
    for e in eps:
        r=[first_pass(i,up,dn,N) for i in e]; r=[x for x in r if x!='na']
        if not r: continue
        s=pd.Series(r).value_counts(normalize=True); res.append(s)
    R=pd.DataFrame(res).fillna(0).mean()  # episode-weighted
    print(f'{label}: up+{up*100:.1f}% / dn-{dn*100:.1f}% / {N}g ->', {k:round(v,2) for k,v in R.items()})
# Long-now: spot up to 14,700 (+5.3%) vs down to 13,330 (-4.5%) in 20 days
stats(0.053,0.045,20,'LONG şimdi (hedef SMA20 / stop Eki23 dip altı)')
# Short-now
stats(0.053,0.045,20,'(aynı bariyer simetrik okuma)')
# rally +3% first within 10 days (short entry fill)
stats(0.03,0.08,10,'+%3 tepki (short girişi dolar mı) vs -%8, 10g')
# Short from rally: entry at +3% (14,380): stop +4% above entry (14,950), target -6.5% below entry (13,450) 25 days
stats(0.04,0.065,25,'SHORT tepkiden: stop +%4 / hedef -%6,5, 25g')
# Long on retest: entry at -4% (13,400): stop -3.5% (12,930), target +6.5% (14,270)
stats(0.065,0.035,25,'LONG retestten: hedef +%6,5 / stop -%3,5, 25g')
# forward 21d/42d returns distribution in cond (episode-weighted)
for N in (10,21,42):
    v=[]
    for e in eps:
        r=[(c.iloc[i+N]/c.iloc[i]-1) for i in e if i+N<len(c)]
        if r: v.append(np.median(r))
    v=np.array(v); print(f'{N}g ileri getiri (epizot medyanları): medyan {np.median(v)*100:.1f}% ort {v.mean()*100:.1f}% poz {np.mean(v>0):.2f} n={len(v)}')
for e in eps:
    d0=c.index[e[0]].date(); d1=c.index[e[-1]].date(); print('  ',d0,'->',d1,len(e))
