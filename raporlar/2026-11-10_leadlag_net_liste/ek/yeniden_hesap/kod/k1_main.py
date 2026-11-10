import sys, os, json, math
import numpy as np, pandas as pd
DATA, OUT = sys.argv[1], sys.argv[2]
START=260
issues=[]; outl={}
S={}; 
def load(sym):
    fn=os.path.join(DATA, sym.replace('^','_')+'.json')
    if not os.path.exists(fn): issues.append(sym+' yok'); return
    r=json.load(open(fn))['chart']['result'][0]
    ts=np.array(r['timestamp']); off=r['meta'].get('gmtoffset',0)
    q=r['indicators']['quote'][0]
    adj=r['indicators'].get('adjclose',[{}])[0].get('adjclose') or q['close']
    d=pd.to_datetime(ts+off,unit='s').normalize()
    df=pd.DataFrame({'o':q['open'],'h':q['high'],'l':q['low'],'c':q['close'],'v':q['volume'],'adj':adj},index=d).astype(float)
    df=df[~df.index.duplicated(keep='last')].sort_index().dropna(subset=['adj'])
    if sym.endswith('.IS') and not sym.startswith('XU'):
        z=(df.v.fillna(0)==0).sum(); df=df[df.v.fillna(0)>0]
        if z: issues.append(f'{sym}: hacim 0 {z} gun atildi')
    if sym.endswith('.IS'):
        lr=np.log(df.adj).diff(); bad=(lr.abs()>0.25).sum()
        if bad: issues.append(f'{sym}: |r|>0.25 {bad} gun NaN')
    S[sym]=df
for f in sorted(os.listdir(DATA)):
    load(f[:-5].replace('_','^',1) if f.startswith('_') else f[:-5])
def isbist(s): return s.endswith('.IS')
def ret_on(sym,dates):
    lr=np.log(S[sym].adj.reindex(dates)).diff()
    if isbist(sym): lr[lr.abs()>0.25]=np.nan
    return lr
def sd(x,w,mp=None): return x.rolling(w,min_periods=mp or int(w*0.8)).std().shift(1)
def beta(y,x,w):
    mp=int(w*0.8)
    return (y.rolling(w,min_periods=mp).cov(x)/x.rolling(w,min_periods=mp).var()).shift(1)
def fwd(r,h): return r.rolling(h,min_periods=h).sum().shift(-h)
def tt(x):
    x=np.asarray(x,float); n=len(x)
    if n<3: return np.nan
    s=x.std(ddof=1)
    return x.mean()/(s/math.sqrt(n)) if s>0 else np.nan
def mn(x): return float(np.mean(x)) if len(x) else np.nan
T_IS=pd.Timestamp('2021-12-31'); T_OOS=pd.Timestamp('2022-01-01'); T_SON=pd.Timestamp('2024-01-01')
def stats(dts,g,cl,ch,base):
    n=len(g); R={'n':n}
    if n==0: return R
    net=g-cl; d=pd.DatetimeIndex(dts)
    R.update(brut=g.mean(),net=net.mean(),t=tt(net),kaz=(net>0).mean(),worst=net.min())
    a=d<=T_IS; b=d>=T_OOS; c=d>=T_SON
    R.update(IS_net=mn(net[a]),IS_t=tt(net[a]),OOS_net=mn(net[b]),OOS_t=tt(net[b]),SON_net=mn(net[c]),SON_t=tt(net[c]),SON_n=int(c.sum()))
    yrs=pd.Series(net).groupby(d.year.values); ys=[v.mean()>0 for _,v in yrs if len(v)>=3]
    R['pos_yil']=np.mean(ys) if ys else np.nan
    R['t_ex5']=tt(np.sort(net)[:-5]) if n>=10 else np.nan
    R['fazla_bp']=g.mean()-base if base is not None else np.nan
    if ch is not None:
        nh=g-ch; R.update(net_hi=nh.mean(),t_hi=tt(nh),OOS_hi=mn(nh[b]),SON_hi=mn(nh[c]),IS_hi=mn(nh[a]),OOSt_hi=tt(nh[b]),tex5_hi=tt(np.sort(nh)[:-5]) if n>=10 else np.nan)
    def sag(R,sfx=''):
        if sfx:
            v=lambda k:R.get(k+sfx,np.nan)
            return bool(R['n']>=30 and v('t')>=2.5 and v('IS')>0 and v('OOS')>0 and v('OOSt')>=1.5 and v('tex5')>=1.5 and v('SON')>0)
    R['saglam']=bool(n>=30 and R['t']>=2.5 and R['IS_net']>0 and R['OOS_net']>0 and R['OOS_t']>=1.5 and R['t_ex5']>=1.5 and R['SON_net']>0)
    if ch is not None:
        R['saglam_hi']=bool(n>=30 and R['t_hi']>=2.5 and R['IS_hi']>0 and R['OOS_hi']>0 and R['OOSt_hi']>=1.5 and R['tex5_hi']>=1.5 and R['SON_hi']>0)
    return R
TRADES={}
def evalrule(dates,sig,fw,h,cl,ch,base=None,keep=None):
    sig=np.nan_to_num(np.asarray(sig,float)); f=np.asarray(fw,float)
    I=[];busy=-1
    for i in np.flatnonzero(sig!=0):
        if i<START or i<busy or np.isnan(f[i]): continue
        I.append(i); busy=i+h
    I=np.array(I,int)
    if len(I)==0: return {'n':0},I
    g=sig[I]*f[I]*1e4
    c1=cl[I] if hasattr(cl,'__len__') else cl
    c2=None if ch is None else (ch[I] if hasattr(ch,'__len__') else ch)
    if base is not None and not np.all(sig[I]>0): base=None
    return stats(dates[I],g,c1,c2,base),I
rowsA=[]; rowsB=[]
def costs(T):
    if isbist(T): return 10,44
    if T in('SOXL','UDOW'): return 30,None
    return 15,None
def addA(rule,variant,dates,sig,fwd_by_h,cl,ch,base_raw=None,hs=(1,2,3)):
    for h in hs:
        base=None if base_raw is None else base_raw[h]
        R,I=evalrule(dates,sig,fwd_by_h[h],h,cl,ch,base)
        R.update(blok='A',kural=rule,varyant=variant,h=h); rowsA.append(R)
def base_of(r): return {h:np.nanmean(fwd(r,h).values[START:])*1e4 for h in (1,2,3)}
def zpair(L,T,dates=None):
    d=S[L].index.intersection(S[T].index) if dates is None else dates
    rL=ret_on(L,d); rT=ret_on(T,d)
    return d,rL,rT
def feats(rL,rT):
    zL=rL/sd(rL,60); b=beta(rT,rL,60); art=rT-b*rL; za=art/sd(art,60)
    return zL,za
def cross_lead(rUS,tdates):
    idx=np.searchsorted(tdates.values,rUS.index.values,side='right')
    m=idx<len(tdates)
    s=pd.Series(rUS.values[m]).groupby(idx[m]).sum(min_count=1)
    out=np.full(len(tdates),np.nan); out[s.index.values]=s.values
    return pd.Series(out,index=tdates)
# ---------------- PART A ----------------
# A1
def A1(name,names):
    ds=S['^GSPC'].index
    for n in names: ds=ds.intersection(S[n].index)
    bk=pd.concat([ret_on(n,ds) for n in names],axis=1).mean(axis=1,skipna=False)
    sp=ret_on('^GSPC',ds); b=beta(bk,sp,250); P=bk-b*sp
    td=S['TUPRS.IS'].index; aggP=cross_lead(P.dropna(),td)
    z=aggP/sd(aggP,250); rT=ret_on('TUPRS.IS',td)
    F={h:fwd(rT,h).values for h in (1,2,3)}; base=base_of(rT)
    sig=np.where(z.abs()>1,np.sign(z),0)
    addA('A1 TUPRS<-'+name,'iki yon',td,sig,F,10,44,base)
    addA('A1 TUPRS<-'+name,'long',td,np.where(z>1,1,0),F,10,44,base)
A1('ABD rafineri 4',['VLO','MPC','PSX','PBF']); A1('ABD rafineri PBFsiz',['VLO','MPC','PSX'])
# A2
ds=S['FMG.AX'].index.intersection(S['BHP.AX'].index).intersection(S['^AXJO'].index)
bk=(ret_on('FMG.AX',ds)+ret_on('BHP.AX',ds))/2; ax=ret_on('^AXJO',ds)
art=bk-beta(bk,ax,60)*ax; zasx=art/sd(art,60)
for hedge in (0,1):
    if hedge:
        td=S['EREGL.IS'].index.intersection(S['XU030.IS'].index)
    else: td=S['EREGL.IS'].index
    rT=ret_on('EREGL.IS',td); z=zasx.reindex(td)
    if hedge:
        rX=ret_on('XU030.IS',td); bt=beta(rT,rX,60)
        F={h:(fwd(rT,h)-bt*fwd(rX,h)).values for h in (1,2,3)}; cl=(10*(1+bt.abs())).values; ch=(44*(1+bt.abs())).values; base=None
    else:
        F={h:fwd(rT,h).values for h in (1,2,3)}; cl,ch=10,44; base=base_of(rT)
    nm='A2 EREGL<-FMG+BHP '+('hedgeli(XU030)' if hedge else 'ham')
    addA(nm,'iki yon',td,np.where(z.abs()>1,np.sign(z),0),F,cl,ch,base)
    addA(nm,'long',td,np.where(z>1,1,0),F,cl,ch,base)
# A3
d,rG,rY=zpair('RYGYO.IS','RYSAS.IS')
z=(rG/sd(rG,250)).clip(-5,5); F={h:fwd(rY,h).values for h in (1,2,3)}; base=base_of(rY)
addA('A3 RYSAS<-RYGYO','iki yon',d,np.where(z.abs()>1,np.sign(z),0),F,10,44,base)
addA('A3 RYSAS<-RYGYO','long',d,np.where(z>1,1,0),F,10,44,base)
# A4
d=S['TRMET.IS'].index.intersection(S['TRALT.IS'].index).intersection(S['TRENJ.IS'].index)
rM,rA,rE=[ret_on(x,d) for x in ('TRMET.IS','TRALT.IS','TRENJ.IS')]
gr=(rA+rE)/2; u=rM-beta(rM,gr,60)*gr
z3=u.rolling(3,min_periods=3).sum()/(sd(u,60)*math.sqrt(3))
F={h:(fwd(rM,h)-0.7*fwd(rA,h)).values for h in (1,2,3)}
sig=np.where(z3>1.5,1,np.where(z3<-1.5,-1,0))
addA('A4 Koza goreli (TRMET-0.7TRALT)','iki yon',d,sig,F,17,74.8)
addA('A4 Koza goreli (TRMET-0.7TRALT)','long TRMET',d,np.where(z3>1.5,1,0),F,17,74.8)
# A5
d,rS,rK=zpair('SAHOL.IS','AKBNK.IS')
spr=rS-beta(rS,rK,250)*rK; Sc=spr.fillna(0).cumsum()
zz=(Sc-Sc.rolling(60,min_periods=48).mean())/Sc.rolling(60,min_periods=48).std()
F={h:(fwd(rK,h)-fwd(rS,h)).values for h in (1,2,3)}
addA('A5 SAHOL/AKBNK','iki yon',d,np.where(zz>1.5,1,np.where(zz<-1.5,-1,0)),F,20,88)
addA('A5 SAHOL/AKBNK','z>+1.5 (SAHOL sat/AKBNK al)',d,np.where(zz>1.5,1,0),F,20,88)
addA('A5 SAHOL/AKBNK','z<-1.5 (SAHOL al/AKBNK sat)',d,np.where(zz<-1.5,-1,0),F,20,88)
# A6
for L,T,kind in [('XLK','SMH','ONDE'),('QQQ','SOXL','ONDE'),('IWM','UDOW','GERIDE'),('SMH','EWT','GERIDE'),('TLT','ASHR','L_UP')]:
    d,rL,rT=zpair(L,T); zL,za=feats(rL,rT)
    sg={'ONDE':za>=2,'GERIDE':za<=-2,'L_UP':zL>=2}[kind]
    F={h:fwd(rT,h).values for h in (1,2,3)}; c=costs(T)[0]
    addA(f'A6 {L}->{T} {kind}','long',d,np.where(sg,1,0),F,c,None,base_of(rT))
# A7
for T,thr,dn in [('QQQ',0.10,True),('SMH',0.20,False)]:
    df=S[T]; d=df.index; r=np.log(df.adj).diff(); ibs=(df.c-df.l)/(df.h-df.l)
    sg=(ibs<thr)&((r<0) if dn else True)
    F={h:fwd(r,h).values for h in (1,2,3)}
    addA(f'A7 {T} IBS<{thr}'+(' & dusus' if dn else ''),'long',d,np.where(sg,1,0),F,15,None,base_of(r))
# A8
def ols2(y,x1,x2,w=250):
    Y=y.values;X1=x1.values;X2=x2.values;n=len(Y);b=np.full(n,np.nan);c=np.full(n,np.nan)
    for i in range(w,n):
        sl=slice(i-w,i); A=np.column_stack([np.ones(w),X1[sl],X2[sl]]); yy=Y[sl]
        ok=~np.isnan(A).any(1)&~np.isnan(yy)
        if ok.sum()<200: continue
        co=np.linalg.lstsq(A[ok],yy[ok],rcond=None)[0]; b[i]=co[1];c[i]=co[2]
    return pd.Series(b,index=y.index),pd.Series(c,index=y.index)
d=S['GDXJ'].index.intersection(S['GDX'].index).intersection(S['GLD'].index).intersection(S['SPY'].index)
r={x:ret_on(x,d) for x in ('GDXJ','GDX','GLD','SPY')}
def resid(y):
    b,c=ols2(r[y],r['GLD'],r['SPY']); return r[y]-b*r['GLD']-c*r['SPY']
eJ=resid('GDXJ'); eG=resid('GDX')
for nm,sg,tg in [('A8 E2-C2j GDXJ artik>0.667%',eJ>0.00667,'GDXJ'),('A8 E2-C2 GDX 3g artik>0.806%',eG.rolling(3,min_periods=3).sum()>0.00806,'GDX'),('A8 E2-C1 GDX 10g artik>2.515% -> GLD',eG.rolling(10,min_periods=10).sum()>0.02515,'GLD')]:
    F={h:fwd(r[tg],h).values for h in (1,2,3)}
    addA(nm,'long (ayni kapanis girisi)',d,np.where(sg,1,0),F,15,None,base_of(r[tg]))
# E1-C2 tatil oncesi GDX
sp=S['SPY'].index; allw=pd.bdate_range(sp[0],sp[-1]); miss=allw.difference(sp)
sig=pd.Series(0,index=sp); ev=0
for m in miss:
    j=sp.searchsorted(m)-1   # tatilden onceki son islem gunu
    if j>=1 and (m-sp[j]).days<=4: sig.iloc[j-1]=1; ev+=1
rg=r['GDX']; dd=d; sg=sig.reindex(dd).fillna(0)
START_bak=START
F={1:fwd(rg,1).values}
# E1 yillik ~9 olay oldugundan START filtresi 260 gunluk isinma gerektirmez
START=0
R,I=evalrule(dd,sg.values,F[1],1,15,None,base_of(rg)[1] if False else None); START=START_bak
R.update(blok='A',kural='A8 E1-C2 tatil oncesi GDX',varyant='long (tatil_olay=%d)'%ev,h=1); rowsA.append(R)
# ---------------- PART B ----------------
UP=[('GLD','GDX'),('GLD','GDXJ'),('GLD','SLV'),('SLV','SIL'),('GDX','GDXJ'),('SPY','IWM'),('QQQ','IWM'),('SPY','QQQ'),('QQQ','SPY'),('QQQ','SMH'),('XLK','SMH'),('SMH','NVDA'),('NVDA','SMH'),('SMH','SOXX'),('USO','XLE'),('XLE','XOP'),('TLT','XLU'),('CPER','COPX'),('FXI','KWEB'),('EEM','EWZ'),('SMH','EWT'),('SMH','EWY'),('IBIT','MSTR'),('IBIT','COIN'),('IBIT','ETHA'),('QQQ','ARKK')]
BP=[('XU030',t) for t in 'AKBNK GARAN YKBNK ISCTR SAHOL KCHOL THYAO PGSUS TUPRS EREGL ASELS BIMAS TCELL FROTO SISE'.split()]
for a,b in [('AKBNK','GARAN'),('GARAN','YKBNK'),('AKBNK','SAHOL'),('THYAO','PGSUS'),('KCHOL','SAHOL'),('TCELL','TTKOM'),('EREGL','KRDMD'),('FROTO','TOASO'),('TRALT','TRMET')]:
    BP+= [(a,b),(b,a)]
BP=[(a+'.IS',b+'.IS') for a,b in BP]
CP=[('SPY','XU030.IS'),('TUR','XU030.IS'),('KBE','AKBNK.IS'),('KBE','GARAN.IS'),('JETS','THYAO.IS'),('JETS','PGSUS.IS'),('XME','EREGL.IS'),('XLE','TUPRS.IS'),('GDX','TRALT.IS'),('GLD','TRALT.IS')]
def partB(L,T,mk):
    if mk=='CAPRAZ':
        td=S[T].index; rT=ret_on(T,td); rUS=ret_on(L,S[L].index); rL=cross_lead(rUS.dropna(),td); d=td
    else: d,rL,rT=zpair(L,T)
    zL,za=feats(rL,rT); cl,ch=costs(T)
    F={h:fwd(rT,h).values for h in (1,2,3)}; base=base_of(rT)
    for k in (1.0,1.5,2.0):
        rules={'YETISME_LONG':np.where((zL>=k)&(za<=-k),1,0),'SADE_LONG':np.where(zL>=k,1,0)}
        if mk!='ABD': rules['YETISME_SHORT']=np.where((zL<=-k)&(za>=k),-1,0)
        for rn,sg in rules.items():
            for h in (1,2,3):
                R,I=evalrule(d,sg,F[h],h,cl,ch,base[h] if rn!='YETISME_SHORT' else None)
                R.update(blok='B',kural=rn,L=L,T=T,piyasa=mk,k=k,h=h); rowsB.append(R)
for L,T in UP: partB(L,T,'ABD')
for L,T in BP: partB(L,T,'BIST')
for L,T in CP: partB(L,T,'CAPRAZ')
A=pd.DataFrame(rowsA); Bd=pd.DataFrame(rowsB)
# BH
def pone(t): return 1.0 if (t is None or np.isnan(t)) else 0.5*math.erfc(t/math.sqrt(2))
Bd['p']=[pone(t) for t in Bd.t]
m=len(Bd); order=Bd.p.sort_values().index
Bd['rank']=0; 
ps=Bd.p.loc[order].values
for q in (0.10,0.05):
    kmax=0
    for i,p in enumerate(ps,1):
        if p<=q*i/m: kmax=i
    Bd[f'fdr{int(q*100):02d}']=False
    Bd.loc[order[:kmax],f'fdr{int(q*100):02d}']=True
A.to_csv(os.path.join(OUT,'partA.csv'),index=False); Bd.to_csv(os.path.join(OUT,'partB.csv'),index=False)
pd.to_pickle((A,Bd,issues),os.path.join(OUT,'res.pkl'))
print('A rows',len(A),'B rows',len(Bd),'m',m,'fdr10',Bd.fdr10.sum(),'fdr05',Bd.fdr05.sum(),'saglam',Bd.saglam.sum())
print('issues',issues)
