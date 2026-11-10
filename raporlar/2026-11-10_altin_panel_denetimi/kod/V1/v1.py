import pandas as pd, numpy as np, os
S='/tmp/claude-0/-home-user-Xxxx/e31e33e0-f360-5bc6-a008-2cee330297de/scratchpad'
OUT='/home/user/Xxxx/raporlar/2026-11-10_altin_panel_denetimi/hesap/V1'
d=pd.read_csv(S+'/veri/viop_filtre.csv',dtype=str,usecols=['TARIH','SOZLESME KODU','VADE TARIHI','UZLASMA FIYATI','ONCEKI UZLASMA FIYATI','ISLEM MIKTARI'])
d.columns=['date','code','vade','u','p','vol']
for c in 'u','p','vol': d[c]=pd.to_numeric(d[c],errors='coerce')
d['date']=pd.to_datetime(d.date); d['vade']=pd.to_datetime(d.vade)
cal=pd.DatetimeIndex(sorted(d.date.unique())); N=len(cal); cpos={t:i for i,t in enumerate(cal)}
wd=pd.bdate_range(cal[0],cal[-1]); hol=list(wd.difference(cal).values.astype('datetime64[D]'))
D1=np.timedelta64(1,'D')
FAM={'XAU':r'^F_XAUUSD\d{4}$','TR':r'^F_(TRALT|KOZAL)\d{4}$','XU':r'^F_XU030\d{4}$'}
F={}
for f,rx in FAM.items():
    s=d[d.code.str.match(rx)].drop_duplicates(['date','code'],keep='last').copy()
    s['r']=np.log(s.u/s.p)
    R=s.pivot(index='date',columns='code',values='r').reindex(cal)
    V=s.pivot(index='date',columns='code',values='vol').reindex(cal)
    vd=s.groupby('code').vade.first(); codes=list(R.columns)
    front=np.full(N,-1)
    for i,t in enumerate(cal):
        best=None
        for j,c in enumerate(codes):
            if np.isnan(R.iat[i,j]): continue
            rem=np.busday_count((t+D1).to_datetime64().astype('datetime64[D]'),(vd[c]+D1).to_datetime64().astype('datetime64[D]'),holidays=hol)
            if rem>=4 and (best is None or vd[c]<vd[codes[best]]): best=j
        if best is not None: front[i]=best
    Rm=R.values; Vm=V.values
    r1=np.array([Rm[i,front[i]] if front[i]>=0 else np.nan for i in range(N)])
    vol=np.array([Vm[i,front[i]] if front[i]>=0 else np.nan for i in range(N)])
    F[f]=dict(R=Rm,front=front,r=r1,vol=vol)
def fwd(f,k):
    o=np.full(N,np.nan); Rm=F[f]['R']; fr=F[f]['front']
    for i in range(N-k):
        if fr[i]<0: continue
        o[i]=np.sum([Rm[i+j,fr[i]] for j in range(1,k+1)])  # nan propagates
    return o
g=pd.Series(F['XAU']['r'],index=cal); rT=pd.Series(F['TR']['r'],index=cal); rU=pd.Series(F['XU']['r'],index=cal)
dd=np.ones(N)
for i in range(1,N): dd[i]=max(1,np.busday_count((cal[i-1]+D1).to_datetime64().astype('datetime64[D]'),(cal[i]+D1).to_datetime64().astype('datetime64[D]')))
sd=lambda x:x.rolling(250,min_periods=60).std().shift(1)
z=(g/(sd(g)*np.sqrt(dd))); zT=(rT/(sd(rT)*np.sqrt(dd)))
def rb(y,x):
    return (y.rolling(250,min_periods=60).cov(x)/x.rolling(250,min_periods=60).var()).shift(1)
b=rb(rT,g)
def ly(n):
    x=pd.read_csv(f'{S}/veri/yahoo_daily/{n}.csv'); x['ldate']=pd.to_datetime(x.ldate); return x.drop_duplicates('ldate').set_index('ldate').sort_index()
sp=pd.concat([np.log(ly('TRALT.IS').c).diff().rename('t'),np.log(ly('XU030.IS').c).diff().rename('x')],axis=1).dropna()
beta=rb(sp.t,sp.x).reindex(cal.union(sp.index)).ffill().reindex(cal)
# eligibility
arife=pd.to_datetime("2019-06-03 2019-10-28 2020-07-30 2020-10-28 2021-05-12 2021-07-19 2021-10-28 2022-07-08 2022-10-28 2023-04-20 2023-06-27 2024-04-09 2024-10-28 2025-06-05 2025-10-28 2026-03-19 2026-05-26 2026-10-28".split())
thr=np.where(cal<pd.Timestamp('2020-03-13'),0.195,0.095)
ok=(np.abs(F['TR']['r'])<thr)&(F['TR']['vol']>0)&(~cal.isin(arife))&(cal>=pd.Timestamp('2018-12-17'))&(cal<=pd.Timestamp('2026-11-09'))
def tt(x):
    x=np.asarray(x,float); return x.mean()/(x.std(ddof=1)/np.sqrt(len(x))) if len(x)>2 else np.nan
def sim(leg,cl,ci,k,sigok=None):
    sig=(np.abs(z.values)>1)&ok&np.isfinite(leg)&np.isfinite(z.values)
    nf=0; rows=[]
    for i in range(N):
        if i>=nf and sig[i]:
            dr=np.sign(z.values[i]); br=dr*leg[i]*1e4
            rows.append((cal[i],dr,br,br-cl[i],br-ci[i])); nf=i+k
    return pd.DataFrame(rows,columns=['date','dir','brut','low','ind'])
def summ(name,t):
    s=f'{name}: n={len(t)} brut={t.brut.mean():.1f} low={t.low.mean():.1f} (t {tt(t.low):.2f}) ind={t.ind.mean():.1f} (t {tt(t.ind):.2f})'
    print(s); return s
one=np.ones(N)
fT={k:fwd('TR',k) for k in (1,2,3)}; fX={k:fwd('XU',k) for k in (1,2,3)}; fG={k:fwd('XAU',k) for k in (1,2,3)}
bt=beta.values; bb=b.values
res={}
k=2
tA2=sim(fT[k]-bt*fX[k],8+np.abs(bt)*3,23+np.abs(bt)*8,k); summ('1 A2 k2',tA2)
tA1=sim(fT[k],8*one,23*one,k); summ('2 A1 k2',tA1)
ti=tA1.ind.values
for cut in (int(0.02*len(ti)),int(np.ceil(0.02*len(ti)))):
    print('2 A1 en iyi 2pct, cikarilan=%d: ind %.1f'%(cut,np.sort(ti)[:-cut].mean()))
for nm,(a,bq) in {'2019-20':('2019','2020'),'2021-23':('2021','2023'),'2024-26':('2024','2026')}.items():
    m=(tA1.date.dt.year>=int(a))&(tA1.date.dt.year<=int(bq)); print('  rejim',nm,'n',m.sum(),'ind %.1f'%tA1.ind[m].mean())
tA3=sim(fT[k]-bb*fG[k],8+np.abs(bb)*3,23+np.abs(bb)*10,k); summ('3 A3 k2',tA3)
tB1=sim(fG[k],3*one,10*one,k); summ('4 B1 k2',tB1)
for n_,t_ in [('A2',tA2),('A1',tA1),('A3',tA3),('B1',tB1)]: t_.to_csv(f'{OUT}/trades_{n_}_k2.csv',index=False)
# ---- eGDXJ
U=pd.concat([np.log(ly(n).adj).diff().rename(n) for n in ('GDXJ','GDX','GLD')],axis=1).dropna()
eJ=U.GDXJ-rb(U.GDXJ,U.GDX)*U.GDX; eJ=eJ/eJ.rolling(250,min_periods=60).std().shift(1)
eX=U.GDX-rb(U.GDX,U.GLD)*U.GLD; eX=eX/eX.rolling(250,min_periods=60).std().shift(1)
ud=U.index; p=np.searchsorted(ud.values,cal.values,side='left')-1
dup=np.r_[False,p[1:]==p[:-1]]
def emap(e,off):
    q=p+off; v=np.full(N,np.nan); m=(q>=0)&(q<len(ud))&(~dup); v[m]=e.values[q[m]]; return v
E={'eJ':emap(eJ,0),'eJ+1':emap(eJ,1),'eJ-1':emap(eJ,-1),'eX':emap(eX,0)}
chk=[(cal[i].date(),ud[p[i]].date()) for i in range(1000,1006)]; print('d* esleme ornek',chk, 'NA oran',dup.mean())
def nw(y,X,L=4):
    n,kx=X.shape; XtXi=np.linalg.inv(X.T@X); be=XtXi@X.T@y; u=y-X@be; Xu=X*u[:,None]
    Sg=Xu.T@Xu
    for l in range(1,L+1):
        w=1-l/(L+1); G=Xu[l:].T@Xu[:-l]; Sg+=w*(G+G.T)
    V=XtXi@Sg@XtXi; return be,be/np.sqrt(np.diag(V))
def reg(y,e,mask,tr=None):
    m=ok&mask&np.isfinite(y)&np.isfinite(z.values)&np.isfinite(zT.values)&np.isfinite(e)
    yy=y[m]*1e4; 
    if tr=='w': lo,hi=np.percentile(yy,[1,99]); yy=np.clip(yy,lo,hi)
    X=np.c_[np.ones(m.sum()),z.values[m],zT.values[m],e[m]]
    if tr=='t10':
        keep=np.ones(len(yy),bool); keep[np.argsort(-np.abs(yy))[:10]]=False; yy=yy[keep]; X=X[keep]
    be,t=nw(yy,X); return be[3],t[3],len(yy)
allm=np.ones(N,bool); yr=cal.year.values
per={'tum':allm,'<2022':cal<pd.Timestamp('2022-01-01'),'>=2022':cal>=pd.Timestamp('2022-01-01'),'>=2024':cal>=pd.Timestamp('2024-01-01')}
y3=fT[3]-bb*fG[3]
cases=[('0 K1 baz (A3 k3, eJ)',y3,'eJ',allm,None),('a plasebo eJ+1 (t gunu seansi)',y3,'eJ+1',allm,None),('a plasebo eJ-1',y3,'eJ-1',allm,None),
('b 2019 at',y3,'eJ',yr!=2019,None),('b yalniz 2020-07+',y3,'eJ',cal>=pd.Timestamp('2020-07-01'),None),
('c winsor 1-99',y3,'eJ',allm,'w'),('c ilk10|y| at',y3,'eJ',allm,'t10'),
('d A1 k1',fT[1],'eJ',allm,None),('d A1 k2',fT[2],'eJ',allm,None),('d A1 k3',fT[3],'eJ',allm,None),('d A3 k3 e_GDX',y3,'eX',allm,None),('d A1 k3 e_GDX',fT[3],'eX',allm,None),
('e hedef F_XU030 k3',fX[3],'eJ',allm,None)]
rows=[]
for nm,y,e,m,tr in cases:
    line=nm.ljust(34)
    for pn,pm in per.items():
        c,t,n=reg(y,E[e],m&pm,tr); line+=f' | {pn}: {c:6.1f} t{t:5.2f} n{n}'; rows.append((nm,pn,c,t,n))
    print(line)
pd.DataFrame(rows,columns=['case','period','d_bps','t','n']).to_csv(f'{OUT}/reg_cases.csv',index=False)
