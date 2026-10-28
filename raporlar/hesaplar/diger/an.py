import json,sys,os,datetime as dt
D=sys.argv[1]
data={}
for f in os.listdir(D):
    j=json.load(open(os.path.join(D,f)))
    r=j['chart']['result'][0]
    ts=r['timestamp']; c=r['indicators']['quote'][0]['close']
    s={}
    for t,v in zip(ts,c):
        if v is None: continue
        d=dt.datetime.utcfromtimestamp(t+10800).date()
        s[d]=v
    data[f[:-5]]=s
for k,s in sorted(data.items()):
    ds=sorted(s); print(k, len(ds), ds[0], ds[-1], round(s[ds[-1]],2))
import math, statistics as st
idx=data['XU030.IS']
def common(a,b):
    return sorted(set(a)&set(b))
def rets(s,days):
    return [s[days[i]]/s[days[i-1]]-1 for i in range(1,len(days))]
def beta(a,b,n):
    days=common(a,b)[-(n+1):]
    ra=rets(a,days); rb=rets(b,days)
    ma=st.mean(ra); mb=st.mean(rb)
    cov=sum((x-ma)*(y-mb) for x,y in zip(ra,rb))/(len(ra)-1)
    vb=st.variance(rb); va=st.variance(ra)
    return cov/vb, cov/math.sqrt(va*vb), math.sqrt(va)*math.sqrt(252), math.sqrt(vb)*math.sqrt(252)
d14=dt.date(2026,9,14); d27=dt.date(2026,10,27); d28=dt.date(2026,10,28); d21=dt.date(2026,10,21)
print("ticker  14Sep  27Oct  28Oct  ret14Sep->28Oct  ret21Oct->28Oct  beta60 corr60 vol60 | beta250 corr250 vol250")
for k,s in sorted(data.items()):
    if k.startswith('USD'): continue
    try:
        r=s[d28]/s[d14]-1; r2=s[d28]/s[d21]-1
    except KeyError as e: print(k,'missing',e); continue
    b60=beta(s,idx,60); b250=beta(s,idx,245)
    print(f"{k:9s} {s[d14]:9.2f} {s.get(d27,float('nan')):9.2f} {s[d28]:9.2f} {r*100:7.1f}% {r2*100:6.1f}%  {b60[0]:.2f} {b60[1]:.2f} {b60[2]*100:.0f}% | {b250[0]:.2f} {b250[1]:.2f} {b250[2]*100:.0f}%")
print('XU030 vol60', beta(idx,idx,60)[2], 'vol250', beta(idx,idx,245)[2])
print("\n--- big daily moves (>12%) check")
for k,s in sorted(data.items()):
    ds=sorted(s)
    for i in range(1,len(ds)):
        r=s[ds[i]]/s[ds[i-1]]-1
        if abs(r)>0.12: print(k,ds[i],round(r*100,1))
def pair(a,b,h,n=120):
    A=data[a];B=data[b];days=common(A,B)[-(n+1):]
    ra=rets(A,days); rb=rets(B,days)
    sp=[x-h*y for x,y in zip(ra,rb)]
    sd=st.stdev(sp)
    # relative price ratio log
    lr=[math.log(A[d])-h*math.log(B[d]) for d in days]
    m=st.mean(lr); s=st.stdev(lr)
    # 20d spread vol
    return sd*math.sqrt(252), sd*math.sqrt(40), (lr[-1]-m)/s
for a,b,h in [('AKBNK.IS','XU030.IS',1.1),('YKBNK.IS','XU030.IS',1.1),('GARAN.IS','XU030.IS',1.0),('XBANK.IS','XU030.IS',1.1),('AKBNK.IS','GARAN.IS',1.0),('TUPRS.IS','THYAO.IS',1.0),('ASELS.IS','XU030.IS',1.3),('KCHOL.IS','XU030.IS',0.9),('YKBNK.IS','AKBNK.IS',1.0)]:
    for n in (60,120,245):
        v=pair(a,b,h,n)
        print(f"{a}/{b} h={h} n={n}: spread vol ann {v[0]*100:.1f}%  40d sd {v[1]*100:.1f}%  z(logratio) {v[2]:.2f}")
# relative perf windows
def rel(a,b,d0,d1):
    A=data[a];B=data[b]; return (A[d1]/A[d0])/(B[d1]/B[d0])-1
for d0 in [dt.date(2026,6,18),dt.date(2026,9,14),dt.date(2026,10,21),dt.date(2025,12,31)]:
    for a,b in [('AKBNK.IS','XU030.IS'),('XBANK.IS','XU030.IS'),('AKBNK.IS','GARAN.IS'),('TUPRS.IS','THYAO.IS'),('XU030.IS','XU030.IS')]:
        try: print(d0,a,b,round(rel(a,b,d0,d28)*100,1))
        except KeyError as e: print('miss',d0,e)
print("\n--- extra pairs")
for a,b,h in [('GARAN.IS','YKBNK.IS',1.0),('GARAN.IS','AKBNK.IS',1.0),('GARAN.IS','ISCTR.IS',1.0)]:
    for n in (60,120,245):
        v=pair(a,b,h,n); print(f"{a}/{b} n={n}: spread vol {v[0]*100:.1f}% 40d sd {v[1]*100:.1f}% z {v[2]:.2f}")
    for n in (60,120,245):
        bb=beta(data[a],data[b],n); print(f"   beta {a} on {b} n={n}: {bb[0]:.2f} corr {bb[1]:.2f}")
for d0 in [dt.date(2025,12,31),dt.date(2026,6,18),dt.date(2026,9,14),dt.date(2026,10,21)]:
    print(d0, 'GARAN/YKBNK', round(rel('GARAN.IS','YKBNK.IS',d0,d28)*100,1), 'YKBNK/AKBNK', round(rel('YKBNK.IS','AKBNK.IS',d0,d28)*100,1))
# daily moves 20-28 oct for banks and index
ds=[d for d in sorted(idx) if d>=dt.date(2026,10,19)]
for d in ds:
    print(d, ' '.join(f"{k[:5]}:{data[k][d]:.2f}" for k in ['XU030.IS','XBANK.IS','AKBNK.IS','GARAN.IS','YKBNK.IS','ISCTR.IS'] if d in data[k]))
print("\n--- holding pair")
for a,b,h in [('KCHOL.IS','SAHOL.IS',1.0),('ASELS.IS','THYAO.IS',1.0),('BIMAS.IS','XU030.IS',0.8)]:
    for n in (60,120,245):
        v=pair(a,b,h,n); bb=beta(data[a],data[b],n); print(f"{a}/{b} n={n}: spread vol {v[0]*100:.1f}% 40d sd {v[1]*100:.1f}% z {v[2]:.2f} beta {bb[0]:.2f} corr {bb[1]:.2f}")
    for d0 in [dt.date(2025,12,31),dt.date(2026,6,18),dt.date(2026,9,14),dt.date(2026,10,21)]:
        print('  ',d0, round(rel(a,b,d0,d28)*100,1))
print('XU030 31Dec', data['XU030.IS'][dt.date(2025,12,31)], 'XBANK 31Dec', data['XBANK.IS'][dt.date(2025,12,31)])
# max drawdown style: 40-day realized pair move distribution for GARAN/YKBNK and GARAN/AKBNK with h
for a,b,h in [('GARAN.IS','YKBNK.IS',0.8),('GARAN.IS','AKBNK.IS',0.85),('GARAN.IS','YKBNK.IS',1.0)]:
    days=common(data[a],data[b])
    moves=[]
    for i in range(40,len(days)):
        ra=data[a][days[i]]/data[a][days[i-40]]-1; rb=data[b][days[i]]/data[b][days[i-40]]-1
        moves.append(ra-h*rb)
    moves.sort(); n=len(moves)
    print(a,b,h,'40d pair ret pctiles 5/25/50/75/95:', [round(moves[int(p*n)]*100,1) for p in (0.05,0.25,0.5,0.75,0.95)])
print("\n--- SAHOL/AKBNK")
for h in (0.6,0.76,0.9):
    for n in (60,120,245):
        v=pair('SAHOL.IS','AKBNK.IS',h,n); print(f"h={h} n={n}: spread vol {v[0]*100:.1f}% 40d sd {v[1]*100:.1f}% z {v[2]:.2f}")
for n in (60,120,245):
    bb=beta(data['SAHOL.IS'],data['AKBNK.IS'],n); print('beta SAHOL on AKBNK',n,round(bb[0],2),'corr',round(bb[1],2))
for d0 in [dt.date(2025,12,31),dt.date(2026,6,18),dt.date(2026,9,14),dt.date(2026,10,15),dt.date(2026,10,21)]:
    print('  ',d0, 'SAHOL/AKBNK', round(rel('SAHOL.IS','AKBNK.IS',d0,d28)*100,1))
S=data['SAHOL.IS'];A=data['AKBNK.IS']
for d in sorted(S):
    if d>=dt.date(2026,10,12): print(d, S[d], A.get(d))
days=common(S,A)
moves=[]
for i in range(40,len(days)):
    moves.append(S[days[i]]/S[days[i-40]]-1-0.76*(A[days[i]]/A[days[i-40]]-1))
moves.sort(); n=len(moves); print('40d pair pctiles', [round(moves[int(p*n)]*100,1) for p in (0.05,0.25,0.5,0.75,0.95)])
# ratio history of SAHOL mcap / AKBNK stake value (shares SAHOL 2.1004bn, AKBNK 5.2bn, stake 40.75%)
r=[(d, S[d]*2.1004/(A[d]*5.2*0.4075)) for d in days]
vals=[x for _,x in r]; print('SAHOL mcap / Akbank stake: now', round(vals[-1],3),'1y min',round(min(vals),3),'max',round(max(vals),3),'median',round(st.median(vals),3))
