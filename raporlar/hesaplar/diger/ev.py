import json,sys,os,datetime as dt,math,statistics as st
D=sys.argv[1]; data={}
for f in os.listdir(D):
    r=json.load(open(os.path.join(D,f)))['chart']['result'][0]
    s={}
    for t,v in zip(r['timestamp'],r['indicators']['quote'][0]['close']):
        if v is not None: s[dt.datetime.fromtimestamp(t+10800,dt.timezone.utc).date()]=v
    data[f[:-8]]=s
G,Y,A,X,B,S=[data[k] for k in ['GARAN','YKBNK','AKBNK','XU030','XBANK','SAHOL']]
days=sorted(set(G)&set(Y)&set(X)&set(B)&set(A)&set(S))
print('range',days[0],days[-1],len(days))
def ret(s,d):
    i=days.index(d); return s[d]/s[days[i-1]]-1
h=0.85
ev=[('2024-12-26','cut 250'),('2025-01-23','cut 250'),('2025-03-06','cut 250'),('2025-03-19','sok/imamoglu'),('2025-03-20','gece faizi 46 (sok)'),('2025-04-17','hike 350'),('2025-06-19','hold'),('2025-07-24','cut 300'),('2025-09-11','cut 250'),('2025-10-23','cut 100'),('2025-12-11','cut 150'),('2026-01-22','cut 100'),('2026-03-12','hold'),('2026-04-22','hold'),('2026-06-11','hold'),('2026-07-23','hold'),('2026-09-10','hold'),('2026-10-22','cut 100')]
print('date        event            GARAN   YKBNK   AKBNK   XBANK   XU030   G-0.85Y  G-A')
cuts=[]
for d,e in ev:
    d=dt.date.fromisoformat(d)
    if d not in days: print(d,'missing'); continue
    g,y,a,x,b=ret(G,d),ret(Y,d),ret(A,d),ret(X,d),ret(B,d)
    p=g-h*y
    print(f"{d} {e:16s} {g*100:6.2f} {y*100:6.2f} {a*100:6.2f} {b*100:6.2f} {x*100:6.2f}  {p*100:6.2f}  {(g-a)*100:6.2f}")
    if e.startswith('cut'): cuts.append(p)
print('cut days n',len(cuts),'mean pair',round(st.mean(cuts)*100,2),'median',round(st.median(cuts)*100,2),'neg count',sum(1 for c in cuts if c<0))
# CPI release days: 3rd of month (or next business day) 2024-11..2026-10
cpi=[]
for yv in (2024,2025,2026):
    for m in range(1,13):
        d=dt.date(yv,m,3)
        if d<days[0] or d>days[-1]: continue
        while d not in days: d+=dt.timedelta(1)
        cpi.append(d)
xs=[];ps=[]
for d in cpi:
    b=ret(B,d)-1.1*ret(X,d); p=ret(G,d)-h*ret(Y,d); xs.append(ret(B,d)); ps.append(p)
def ols(x,y):
    mx,my=st.mean(x),st.mean(y); c=sum((a-mx)*(b-my) for a,b in zip(x,y)); v=sum((a-mx)**2 for a in x); 
    beta=c/v; r=c/math.sqrt(v*sum((b-my)**2 for b in y)); return beta,r
print('CPI days n',len(cpi),'pair~XBANK beta,corr',[round(v,2) for v in ols(xs,ps)])
# all days: pair on XBANK, and on bank factor (XBANK - beta*XU030)
for n in (250,500,len(days)-1):
    dd=days[-(n+1):]
    rb=[B[dd[i]]/B[dd[i-1]]-1 for i in range(1,len(dd))]
    rx=[X[dd[i]]/X[dd[i-1]]-1 for i in range(1,len(dd))]
    rp=[(G[dd[i]]/G[dd[i-1]]-1)-h*(Y[dd[i]]/Y[dd[i-1]]-1) for i in range(1,len(dd))]
    bb,_=ols(rx,rb); fac=[b-bb*x for b,x in zip(rb,rx)]
    print('n',n,'pair~XBANK',[round(v,2) for v in ols(rb,rp)],'pair~bankfactor(XBANK-',round(bb,2),'*XU030)',[round(v,2) for v in ols(fac,rp)])
    for nm,s in (('GARAN',G),('YKBNK',Y)):
        rs=[s[dd[i]]/s[dd[i-1]]-1 for i in range(1,len(dd))]
        print('   ',nm,'beta to XBANK',round(ols(rb,rs)[0],2),'to XU030',round(ols(rx,rs)[0],2))
