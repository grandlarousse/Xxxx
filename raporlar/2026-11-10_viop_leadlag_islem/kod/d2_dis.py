import pandas as pd, numpy as np, json, warnings
warnings.filterwarnings('ignore')
P='/tmp/claude-0/-home-user-Xxxx/b52fa442-3316-551a-bdd2-9e9f754166e0/scratchpad/veri/panel/'
OUT='/home/user/Xxxx/raporlar/2026-11-10_viop_leadlag_islem/ek/'
ns=lambda x: pd.DatetimeIndex(x).astype('datetime64[ns]')
fr=pd.read_parquet(P+'fut_ret.parquet'); fr.index=ns(fr.index); cal=fr.index; N=len(cal)
rd=lambda f: pd.read_parquet(P+f).set_axis(cal)
LIM=rd('fut_limit.parquet'); TRD=rd('fut_trades.parquet'); VAL=rd('fut_value_tl.parquet'); CODE=rd('fut_code.parquet')
spot=pd.read_parquet(P+'spot_gunluk.parquet'); spot['date']=ns(spot.date)
dis=pd.read_parquet(P+'dis_gunluk.parquet'); dis['date']=ns(dis.date)
spl=pd.read_csv(P+'bolunme_gunleri.csv'); spl['date']=ns(spl.date)
viop=pd.read_parquet(P+'viop_gunluk.parquet',columns=['date','code','close','settle']); viop['date']=ns(viop.date)
liq=pd.read_csv('/home/user/Xxxx/raporlar/2026-11-02_viop_leadlag/veri_ozet/y_viop_likidite.csv').set_index('und').rt_cost_retail_bps
def cost_of(u):
    if u=='XU030': return 6.
    if u in('USDTRY','XAUUSD','XAGUSD','XAUTRY'): return 8.
    return float(liq.get(u,22.)) if not np.isnan(liq.get(u,np.nan)) else 22.
years=cal.year.values
# ---------- spot returns
def sret(sym):
    d=spot[spot.sym==sym].drop_duplicates('date',keep='last').set_index('date').sort_index().reindex(cal)
    r=np.log(d.adj/d.adj.shift(1))
    sp=spl[spl.sym==sym].date
    r[r.index.isin(sp)]=np.nan
    m=np.where(cal<pd.Timestamp('2020-03-13'),np.log(1.205),np.log(1.105))
    r[(r.abs()>m)]=np.nan
    if sym in('XU030.IS','XBANK.IS','XU100.IS'): r[r.abs()>0.5]=np.nan
    r[(d.v==0)&(d.h==d.l)]=np.nan
    return r
def exdiv(sym):
    d=spot[spot.sym==sym].drop_duplicates('date',keep='last').set_index('date').sort_index().reindex(cal)
    x=np.log(d.adj/d.adj.shift(1))-np.log(d.c/d.c.shift(1))
    return np.where(x.abs()>0.003)[0]
def beta(y,x,w=250): return (y.rolling(w,min_periods=100).cov(x)/x.rolling(w,min_periods=100).var()).shift(1)
def sig(e,w=120): return e.rolling(w,min_periods=60).std().shift(1)
RX=sret('XU030.IS')
# ---------- foreign
def fs(sym):
    return dis[dis.sym==sym].drop_duplicates('date',keep='last').set_index('date').sort_index()['adj'].dropna()
def asofv(s,dates):
    pos=s.index.searchsorted(ns(dates),side='right')-1
    return pd.Series(np.where(pos>=0,np.log(s.values[np.clip(pos,0,None)]),np.nan),index=cal)
def lead(sym,mode):
    s=fs(sym); c=pd.Series(cal)
    if mode=='T1':
        p1=c.shift(1).fillna(pd.Timestamp('1900-01-01')); p2=c.shift(2).fillna(pd.Timestamp('1900-01-01'))
        return asofv(s,p1)-asofv(s,p2)
    p1=c.shift(1).fillna(pd.Timestamp('1900-01-01'))
    return asofv(s,cal)-asofv(s,p1)
def basket(syms,idx,mode):
    Li=lead(idx,mode); E=[]
    for s in syms:
        L=lead(s,mode); E.append(L-beta(L,Li)*Li)
    E=pd.concat(E,axis=1); b=E.mean(axis=1); b[E.notna().sum(axis=1)<len(syms)/2]=np.nan
    return b, b/sig(b)
# ---------- target
def target(und):
    r=sret(und+'.IS'); b=beta(r,RX); e=r-b*RX; s=sig(e)
    z1=e/s; z2=(e.shift(1)+e)/(np.sqrt(2)*s)
    return dict(r=r,b=b,e=e,s=s,z1=z1,z2=z2,sraw=sig(r))
# ---------- engine
CLS={}
def e1arr(und):
    if und not in CLS:
        k=pd.DataFrame({'date':cal,'code':CODE[und].values}).merge(viop,how='left',on=['date','code'])
        CLS[und]=(k.close.values,k.settle.values)
    return CLS[und]
DI=pd.DatetimeIndex
PER={'TAM':lambda d:np.ones(len(d),bool),'IS':lambda d:DI(d).year<=2021,'OOS':lambda d:DI(d).year>=2022,
     'SON2Y':lambda d:np.asarray(DI(d)>=pd.Timestamp('2024-11-10')),'Y2026':lambda d:DI(d).year==2026,
     'P1723':lambda d:DI(d).year<=2023,'P2426':lambda d:DI(d).year>=2024}
def engine(und,mask,d,h,eo=0,hedge=None,e1=False,rule='fixed',fark=None,excl=None,freemode='auto',xalt=False):
    if freemode=='auto': freemode='entry' if eo>0 else 'exit'
    f=fr[und].values; lm=LIM[und].values; tr_=TRD[und].values; va=VAL[und].values; cd=CODE[und].values
    xu=fr['XU030'].values; cs,ss=e1arr(und)
    idx=np.where(np.asarray(mask,bool)&np.isfinite(d))[0]; free=0; rows=[]
    for i in idx:
        if i<free: continue
        ei=i+eo
        if ei+1>=N: continue
        if excl is not None and excl(i,ei): continue
        def leg(a,b): # day returns a..b inclusive
            x=f[a:b+1].copy()
            if hedge is not None:
                bt=hedge[ei]; x=x-bt*xu[a:b+1]
            return x
        if rule=='fixed': xi=(i+h if xalt else ei+h)
        else:
            xi=ei+3
            fk=fark[i]
            if np.isfinite(fk):
                for k in (1,2):
                    if ei+k>=N: break
                    c=d[i]*np.nansum(leg(ei+1,ei+k))
                    if c>=0.5*fk: xi=ei+k+1; break
        if xi>=N: continue
        if lm[ei]==1 or lm[xi]==1: continue
        if not(tr_[ei]>=20 and tr_[xi]>=20 and va[ei]>=1e6 and va[xi]>=1e6): continue
        w=leg(ei+1,xi)
        if np.isnan(w).any(): continue
        ret=d[i]*w.sum()*1e4
        if e1:
            if not(np.isfinite(cs[ei]) and np.isfinite(ss[ei])): continue
            ret+=d[i]*np.log(ss[ei]/cs[ei])*1e4
        roll=int(len(set(cd[ei:xi+1]))>1)
        c0=cost_of(und)*(1+roll)+(6. if hedge is not None else 0)
        rows.append((i,cal[i],d[i],ret,ret-c0,roll,xi)); free=(xi-eo if freemode=='entry' else xi)
    return pd.DataFrame(rows,columns=['i','date','d','ret','net','roll','xi'])
def summ(tr):
    n=len(tr)
    if n==0: return dict(n=0)
    r=tr.ret.values; m=r.mean(); sd=r.std(ddof=1) if n>2 else np.nan
    o=dict(n=n,brut=m,t=(m/(sd/np.sqrt(n)) if n>2 and sd>0 else np.nan),net=tr.net.mean(),hit=(r>0).mean(),med=np.median(r),long=(tr.d>0).mean(),roll=tr.roll.sum())
    if n>10: o['ex10']=np.sort(r)[:-10].mean()
    yl=tr.groupby(tr.date.dt.year).ret.mean(); o['poz_yil']=int((yl>0).sum()); o['yil_say']=len(yl)
    return o
RES={}; YIL={}
def run(key,und,mask,d,h,**kw):
    tr=engine(und,mask,d,h,**kw); RES[key]={p:summ(tr[np.asarray(PER[p](tr.date))]) if len(tr) else dict(n=0) for p in PER}
    YIL[key]=tr.groupby(tr.date.dt.year).ret.agg(['mean','count']).round(1).to_dict('index') if len(tr) else {}
    RES[key]['_tr']=tr
    return tr
def sgn(z): return np.sign(z.values)
def M(z,thr=1.0): return (z.abs()>=thr).fillna(False).values
# ================= A
US=['VLO','MPC','PSX','PBF']
bA,zA=basket(US,'^GSPC','T1'); bA3,zA3=basket(US[:3],'^GSPC','T1')
TT=target('TUPRS'); dA=sgn(zA)
kulA=lambda z,T,d: ((d*T['z2'].values)<=0.25)
run('A_ONCU_h2_E0','TUPRS',M(zA),dA,2)
run('A_ONCU_h2_E2','TUPRS',M(zA),dA,2,eo=1)
run('A_KUL_h2_E0','TUPRS',M(zA)&kulA(zA,TT,dA),dA,2)
run('A_IKISI_h2_E0','TUPRS',M(zA)&~kulA(zA,TT,dA)&np.isfinite(TT['z2'].values),dA,2)
# ================= A basit kural
def pct(sym):
    return np.exp(lead(sym,'T1'))-1
dg=(sum(pct(s) for s in US)/4)-pct('^GSPC'); dg3=(sum(pct(s) for s in US[:3])/3)-pct('^GSPC')
thr=dg.rolling(250,min_periods=100).std().shift(1); thr3=dg3.rolling(250,min_periods=100).std().shift(1)
def simple(name,dd,th,hs=(1,2,3)):
    sg=((dd.abs()>=th)&dd.notna()&th.notna() if isinstance(th,pd.Series) else (dd.abs()>=th)&dd.notna()).values
    d=np.sign(dd.values)
    for h in hs:
        run(f'{name}_h{h}','TUPRS',sg,d,h)
        if h==2:
            run(f'{name}_h2_sadeceAL','TUPRS',sg&(d>0),d,2); run(f'{name}_h2_sadeceSAT','TUPRS',sg&(d<0),d,2)
simple('Asade',dg,thr); simple('Asade_PBFsiz',dg3,thr3,(2,))
simple('Asade_kesif2pct',dg,0.02); simple('Asade_kesif3pct',dg,0.03)
# ---- zaman dilimi ayrisimi
sp=spot[spot.sym=='TUPRS.IS'].drop_duplicates('date',keep='last').set_index('date').sort_index().reindex(cal)
spx=spl[spl.sym=='TUPRS.IS'].date; o_=sp.o.copy(); c_=sp.c.copy()
bad=cal.isin(spx); o_[bad]=np.nan; c_[bad]=np.nan
sl={'i_oncekiKap_Acilis':np.log(o_/c_.shift(1)),'ii_Acilis_Kapanis':np.log(c_/o_),'iii_Kap_t_Kap_t1':np.log(c_.shift(-1)/c_),'iv_Kap_t1_Kap_t2':np.log(c_.shift(-2)/c_.shift(-1)),
    'fut_t(bilgi)':fr['TUPRS']}
DIL=[]
for nm,mk,dd in [('S_ONCU',M(zA),dA),('S_KUL',M(zA)&kulA(zA,TT,dA),dA),('Asade',((dg.abs()>=thr)&thr.notna()).values,np.sign(dg.values))]:
    for per in ['TAM','OOS','SON2Y','Y2026']:
        pm=PER[per](cal)
        for k,s in sl.items():
            x=(s.values*dd*1e4)[mk&pm&np.isfinite(s.values)]
            if len(x)>2: DIL.append(dict(kural=nm,donem=per,dilim=k,n=len(x),ort_bps=x.mean(),t_naif=x.mean()/(x.std(ddof=1)/np.sqrt(len(x)))))
pd.DataFrame(DIL).to_csv(OUT+'d2_A_dilim.csv',index=False)
# ---- esik / cikis / E1  (A, C, D)
bC,zC=basket(['BHP.AX','FMG.AX'],'^AXJO','ASYA'); dC=sgn(zC); TE=target('EREGL')
zD=fr['XAUUSD']/sig(fr['XAUUSD']); dD=sgn(zD); TR=target('TRALT')
CASES={'A':('TUPRS',zA,TT,dA,TT['sraw']),'C':('EREGL',zC,TE,dC,TE['sraw']),'D':('TRALT',zD,TR,dD,TR['sraw'])}
def farkarr(z,T,d,hedged):
    s=(T['s'] if hedged else T['sraw']).values
    zt=(T['z2'] if False else T['z1']).values
    return np.maximum(0,np.abs(z.values)-d*zt)*s
for k,(und,z,T,d,_) in CASES.items():
    for hedged in ([False] if k=='A' else [False,True]):
        hg=T['b'].values if hedged else None; tag=k+('H' if hedged else 'T')
        zt=T['z2'] if k=='A' else T['z1']
        fa=np.maximum(0,np.abs(z.values)-d*zt.values)*(T['s'] if hedged else T['sraw']).values
        for h in (1,2,3): run(f'{tag}_ONCU_h{h}',und,M(z),d,h,hedge=hg)
        run(f'{tag}_ONCU_DOYGUN_K1',und,M(z),d,3,hedge=hg,rule='doygun',fark=fa)
        run(f'{tag}_ONCU_h2_E1',und,M(z),d,2,hedge=hg,e1=True)
        run(f'{tag}_ONCU_h3_E1',und,M(z),d,3,hedge=hg,e1=True)
        for h in (2,3): run(f'{tag}_ONCU_h{h}_E2',und,M(z),d,h,hedge=hg,eo=1)
        for th in (0.75,1.0,1.5,2.0):
            for h in (2,3): run(f'{tag}_ESIK{th}_h{h}',und,M(z,th),d,h,hedge=hg)
# kutu: C ve D hedge'li S_KUL degil (S_ONCU) -- yeniden uretim icin h:C h3, D h2
# ================= B
u=fr['USDTRY']-fr['USDTRY'].rolling(20).mean().shift(1); zB=u/sig(u); dB=sgn(zB)
raw=fr['USDTRY'].values*1e4
CRIS=[('2018-08-01','2018-09-30'),('2020-03-01','2020-04-30'),('2021-11-01','2022-01-31'),('2023-05-01','2023-06-30'),('2025-03-01','2025-04-30'),('2026-09-01','2026-10-31')]
crm=np.zeros(N,bool)
for a,b in CRIS: crm|=(cal>=a)&(cal<=b)
TB={u_:target(u_) for u_ in ['FROTO','ENKAI','VESTL','TOASO','BIMAS','TCELL','TTKOM','EKGYO']}
# XU030 hedefi: ham spot
rx=RX; sx=sig(rx); TB['XU030']=dict(z1=rx/sx,b=pd.Series(1.0,index=cal),s=sx,r=rx)
def B(key,und,kul=True,eo=1,h=2,mask_extra=None,hedge=False,excl=None):
    T=TB[und]; kk=((dB*T['z1'].values)<=0.25) if kul else np.ones(N,bool)
    m=M(zB)&kk
    if mask_extra is not None: m=m&mask_extra
    run(key,und,m,dB,h,eo=eo,hedge=(TB[und]['b'].values if hedge else None),excl=excl)
for t_ in ['FROTO','ENKAI','VESTL','TOASO']:
    for kul in (True,False):
        B(f'B_{t_}_{"KUL" if kul else "ONCU"}_E2',t_,kul)
        B(f'B_{t_}_{"KUL" if kul else "ONCU"}_E0',t_,kul,eo=0)
for kul in (True,False):
    s='KUL' if kul else 'ONCU'
    B(f'B_FROTO_{s}_E3','FROTO',kul,eo=2)
    B(f'B_FROTO_{s}_E2_ham50','FROTO',kul,mask_extra=np.abs(raw)>=50)
    B(f'B_FROTO_{s}_E2_krizsiz','FROTO',kul,mask_extra=~crm)
    B(f'B_FROTO_{s}_E2_hedgeli','FROTO',kul,hedge=True)
    ed=exdiv('FROTO.IS')
    ex=lambda i,ei,ed=ed: bool(((ed>=i-2)&(ed<=ei+5)).any())
    B(f'B_FROTO_{s}_E2_exdivsiz','FROTO',kul,excl=ex)
    for pl in ['XU030','BIMAS','TCELL','TTKOM','EKGYO']:
        B(f'B_{pl}_{s}_E2_plasebo',pl,kul)
# B: sinyal gunlerinde ham USDTRY degisimi medyani
BX=[]
Tf=TB['FROTO']; kf=(dB*Tf['z1'].values)<=0.25
for nm,mk in [('FROTO_KUL_sinyal',M(zB)&kf),('ONCU_sinyal',M(zB)&np.isfinite(zB.values))]:
    for per in ['TAM','P1723','P2426','Y2026']:
        pm=PER[per](cal)&(cal>=pd.Timestamp('2019-11-18'))
        x=raw[mk&pm]
        if len(x): BX.append(dict(sinyal=nm,donem=per,n=len(x),medyan_ham_bps=np.median(x),medyan_yonlu_bps=np.median(x*dB[mk&pm]),medyan_mutlak_bps=np.median(np.abs(x)),pay_mutlak_lt20=(np.abs(x)<20).mean()))
pd.DataFrame(BX).to_csv(OUT+'d2_B_ham_kur.csv',index=False)
# ---- yeniden uretim tanilari (en cok 3 deneme)
for t_ in ['FROTO','ENKAI','VESTL','TOASO']:
    for kul in (True,False):
        T=TB[t_]; kk=((dB*T['z1'].values)<=0.25) if kul else np.ones(N,bool); s_='KUL' if kul else 'ONCU'
        run(f'TANI1_B_{t_}_{s_}_E2_girisbazli',t_,M(zB)&kk,dB,2,eo=1,freemode='entry')
        run(f'TANI3_B_{t_}_{s_}_E2_zT2gun',t_,M(zB)&(((dB*T['z2'].values)<=0.25) if kul else np.ones(N,bool)),dB,2,eo=1)
for k,(und,z,T,d,_) in CASES.items():
    for hedged in ([False] if k=='A' else [False,True]):
        hg=T['b'].values if hedged else None; tag=k+('H' if hedged else 'T')
        run(f'TANI2_{tag}_h2_E2_cikis_t+h',und,M(z),d,2,hedge=hg,eo=1,xalt=True)
        run(f'TANI1_{tag}_h2_E2_girisbazli',und,M(z),d,2,hedge=hg,eo=1,freemode='entry')
# ================= bugun
last=cal[-10:]; BU=[]
for dt in last:
    i=cal.get_loc(dt)
    BU.append(dict(tarih=dt.date(),A_z=zA.iloc[i],A_basit_fark_pct=dg.iloc[i]*100,A_basit_esik_pct=thr.iloc[i]*100,A_tetik=abs(zA.iloc[i])>=1,
        B_usdtry_z=zB.iloc[i],B_froto_zT=Tf['z1'].iloc[i],B_ONCU=abs(zB.iloc[i])>=1,B_KUL=(abs(zB.iloc[i])>=1) and dB[i]*Tf['z1'].iloc[i]<=0.25,
        C_z=zC.iloc[i],C_tetik=abs(zC.iloc[i])>=1,D_z=zD.iloc[i],D_tetik=abs(zD.iloc[i])>=1))
pd.DataFrame(BU).to_csv(OUT+'d2_bugun.csv',index=False)
# bugun: ABD kapanis tarihleri
t=cal[-1]; p1=cal[-2]; p2=cal[-3]
info=[]
for s in US+['^GSPC']:
    x=fs(s); a=x[x.index<=p1]; b=x[x.index<=p2]
    info.append((s,a.index[-1].date(),b.index[-1].date(),round(100*(a.iloc[-1]/b.iloc[-1]-1),3)))
json.dump(dict(t=str(t.date()),p1=str(p1.date()),p2=str(p2.date()),abd=info,sepet_artik_z=float(zA.iloc[-1]),sepet_artik=float(bA.iloc[-1]),sigma=float(sig(bA).iloc[-1]),
    C_z=float(zC.iloc[-1]),D_z=float(zD.iloc[-1]),B_z=float(zB.iloc[-1]),B_u_bps=float(u.iloc[-1]*1e4),B_froto_zT=float(Tf['z1'].iloc[-1]),
    A_dsign=float(dA[-1]),A_zT2=float(TT['z2'].iloc[-1])),open(OUT+'d2_bugun_abd.json','w'),default=str,indent=1)
# ================= cikti
rows=[]
for k,v in RES.items():
    for p in PER:
        s=v[p]
        if s.get('n',0)>0: rows.append(dict(anahtar=k,donem=p,**s,yillar=json.dumps(YIL[k]) if p=='TAM' else ''))
pd.DataFrame(rows).round(2).to_csv(OUT+'d2_tum_sonuclar.csv',index=False)
for k in ['A_ONCU_h2_E0','A_KUL_h2_E0','B_FROTO_KUL_E2','CT_ONCU_h3','DH_ONCU_h2']:
    if k in RES: RES[k]['_tr'].to_csv(OUT+f'd2_islemler_{k}.csv',index=False)
print('ok',len(rows))
