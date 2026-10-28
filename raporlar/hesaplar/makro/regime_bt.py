import json,datetime as dt,sys,statistics as st
d=json.load(open(sys.argv[1]))['chart']['result'][0]
ser=[(dt.datetime.fromtimestamp(t,dt.UTC).date(),x) for t,x in zip(d['timestamp'],d['indicators']['quote'][0]['close']) if x and x>0]
# approx policy path (TCMB) and USD rate [V]
pol=[(dt.date(2023,8,24),.25),(dt.date(2023,9,21),.30),(dt.date(2023,10,26),.35),(dt.date(2023,11,23),.40),(dt.date(2023,12,21),.425),(dt.date(2024,1,25),.45),(dt.date(2024,3,21),.50),
     (dt.date(2024,12,26),.475),(dt.date(2025,1,23),.45),(dt.date(2025,3,6),.425),(dt.date(2025,4,17),.46),(dt.date(2025,7,24),.43),(dt.date(2025,9,11),.405),(dt.date(2025,10,23),.395),(dt.date(2025,12,11),.38),(dt.date(2026,1,22),.37),(dt.date(2026,10,22),.36)]
usd=[(dt.date(2023,1,1),.053),(dt.date(2024,9,18),.049),(dt.date(2024,12,18),.044),(dt.date(2025,9,17),.042),(dt.date(2025,10,29),.039),(dt.date(2025,12,10),.036),(dt.date(2026,9,16),.039)]
def lk(tbl,D):
    v=tbl[0][1]
    for a,b in tbl:
        if D>=a: v=b
    return v
n=64; res=[]; res_stop=[]
idx={D:i for i,(D,x) in enumerate(ser)}
for i,(D0,S0) in enumerate(ser):
    if D0<dt.date(2023,8,24) or D0>dt.date(2026,8,24): continue
    diff=lk(pol,D0)-lk(usd,D0)-0.02  # forward implied usually ~2pp below policy [V]
    F0=S0*(1+diff*n/365); end=D0+dt.timedelta(days=n)
    path=[(D,x) for D,x in ser[i+1:] if D<=end]
    ST=path[-1][1]; r=(F0-ST)/F0; res.append((D0,r))
    rs=r
    for D,x in path:
        Ft=x*(1+diff*(end-D).days/365)
        if Ft>F0*1.014: rs=(F0-Ft)/F0; break
    res_stop.append(rs)
r=[x for _,x in res]
def q(a,p): a=sorted(a); return a[int(p*(len(a)-1))]
print("N",len(r),"mean %.2f%% median %.2f%% p5 %.2f%% min %.2f%% pos %.0f%%"%(st.mean(r)*100,st.median(r)*100,q(r,.05)*100,min(r)*100,100*sum(x>0 for x in r)/len(r)))
print("with stop: mean %.2f%% p5 %.2f%% min %.2f%% pos %.0f%%"%(st.mean(res_stop)*100,q(res_stop,.05)*100,min(res_stop)*100,100*sum(x>0 for x in res_stop)/len(res_stop)))
w=min(res,key=lambda t:t[1]); print("worst start",w)
# by year
for y in (2023,2024,2025,2026):
    a=[x for D,x in res if D.year==y]; print(y,len(a),"mean %.2f%% min %.2f%%"%(st.mean(a)*100,min(a)*100))
