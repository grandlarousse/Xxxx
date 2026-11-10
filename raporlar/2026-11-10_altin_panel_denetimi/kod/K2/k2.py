import pandas as pd, numpy as np, sys, math
V='/tmp/claude-0/-home-user-Xxxx/e31e33e0-f360-5bc6-a008-2cee330297de/scratchpad/veri'
OUT='/home/user/Xxxx/raporlar/2026-11-10_altin_panel_denetimi/hesap/K2/'
LOG=open(OUT+'k2.log','w')
def P(s='',show=False):
    LOG.write(str(s)+'\n')
    if show: print(s)
ARIFE=pd.to_datetime("2019-06-03 2019-10-28 2020-07-30 2020-10-28 2021-05-12 2021-07-19 2021-10-28 2022-07-08 2022-10-28 2023-04-20 2023-06-27 2024-04-09 2024-10-28 2025-06-05 2025-10-28 2026-03-19 2026-05-26 2026-10-28".split())
# ---------- VIOP
d=pd.read_csv(V+'/viop_filtre.csv',dtype=str,usecols=['TARIH','SOZLESME KODU','VADE TARIHI','UZLASMA FIYATI','ONCEKI UZLASMA FIYATI','ISLEM HACMI','ISLEM MIKTARI','ACIK POZISYON'])
d.columns=['date','code','vade','settle','prev','vol','qty','oi']
days=pd.DatetimeIndex(sorted(pd.to_datetime(d.date).unique())); N=len(days)
m=d.code.str.extract(r'^F_(XAUUSD|TRALT|KOZAL|XU030|USDTRY)(\d{4})$')
d=d[m[0].notna()].copy(); d['und']=m[0][m[0].notna()].replace({'KOZAL':'TRALT'})
for c in ['settle','prev','vol','qty','oi']: d[c]=pd.to_numeric(d[c],errors='coerce')
d['date']=pd.to_datetime(d.date); d['vade']=pd.to_datetime(d.vade)
d=d.sort_values('vol',ascending=False).drop_duplicates(['date','und','vade']).sort_values(['und','date','vade']).reset_index(drop=True)
d['r']=np.where((d.settle>0)&(d.prev>0),np.log(d.settle/d.prev.where(d.prev>0)),np.nan)
dd=days.values.astype('datetime64[D]'); last=dd[-1]
pos=np.searchsorted(dd,d.date.values.astype('datetime64[D]'))
vd=d.vade.values.astype('datetime64[D]')
j=np.searchsorted(dd,vd,'right')
dte=np.where(vd<=last,j-1-pos,(N-1-pos)+np.busday_count(last+np.timedelta64(1,'D'),vd+np.timedelta64(1,'D')))
d['dte']=dte
dq=d[d.dte>=4].sort_values(['und','date','vade'])
front={u:g.drop_duplicates('date').set_index('date').reindex(days) for u,g in dq.groupby('und')}
nxt2={u:g.groupby('date').nth(1).set_index('date').reindex(days) for u,g in dq.groupby('und')}
W={u:g.pivot_table(index='date',columns='code',values='r',aggfunc='first').reindex(days) for u,g in d.groupby('und')}
Wv={u:{c:w[c].values for c in w.columns} for u,w in W.items()}
FC={u:front[u]['code'].values for u in front}
def fwd(u,code,i,e):
    if not isinstance(code,str): return np.nan
    col=Wv[u].get(code)
    if col is None: return np.nan
    seg=col[i+1:e+1]
    if len(seg)<e-i or np.isnan(seg).any(): return np.nan
    return float(seg.sum())
def thr(dt): return 0.095 if dt>=pd.Timestamp('2020-03-13') else 0.195
THR=np.array([thr(x) for x in days])
rT=front['TRALT']['r']; gX=front['XAUUSD']['r']
lockT=(rT.abs().values>=THR)
# ---------- yahoo
def rd(s):
    y=pd.read_csv(V+f'/yahoo_daily/{s}.csv'); y['ld']=pd.to_datetime(y.ldate); return y.drop_duplicates('ld',keep='last').set_index('ld')['c']
def spot_beta(a,b,mp):
    df=pd.concat([np.log(a).diff(),np.log(b).diff()],axis=1,keys=['a','b']).dropna()
    be=df.a.rolling(250,min_periods=mp).cov(df.b)/df.b.rolling(250,min_periods=mp).var()
    return be.reindex(days,method='ffill').shift(1)
tr_s,xu_s=rd('TRALT.IS'),rd('XU030.IS')
usdtry_last=float(rd('USDTRY_X').dropna().iloc[-1])
gap=np.array([1]+[max(1,int(np.busday_count(days[i-1].date(),days[i].date()))) for i in range(1,N)])
def make_S(mp):
    S=pd.DataFrame(index=days); S['g']=gX
    sig=gX.shift(1).rolling(250,min_periods=mp).std()
    S['z']=gX/(sig*np.sqrt(gap))
    S['beta']=spot_beta(tr_s,xu_s,mp)
    mask=gX.notna()&rT.notna(); x=gX.where(mask); y=rT.where(mask)
    S['b']=(y.rolling(250,min_periods=mp).cov(x)/x.rolling(250,min_periods=mp).var()).shift(1)
    return S
COST={'dusuk':(8,3,3),'bireysel':(23,10,8)}
def build(S,target,rule,k,strict=False,zc=1.0):
    z=S.z.values; beta=S.beta.values; bb=S.b.values
    rows=[]; nx=0
    qT=front['TRALT']['qty'].values; qX=front['XAUUSD']['qty'].values; qU=front['XU030']['qty'].values
    for i in range(N):
        if i<nx or not np.isfinite(z[i]): continue
        if days[i] in ARIFE: continue
        if rule=='a': dr=1 if z[i]>zc else (-1 if z[i]<-zc else 0)
        elif rule=='b': dr=-1 if z[i]>zc else (1 if z[i]<-zc else 0)
        else: dr=1
        if dr==0: continue
        usesT=target in('A1','A2','A3'); usesX=target in('A3','B1')
        if usesT:
            if not isinstance(FC['TRALT'][i],str) or not qT[i]>0 or lockT[i]: continue
        if usesX and not qX[i]>0: continue
        if target=='A2' and (not qU[i]>0 or not np.isfinite(beta[i])): continue
        if target=='A3' and not np.isfinite(bb[i]): continue
        e=i+k
        if usesT:
            cT=FC['TRALT'][i]
            while e<N and e<i+k+3 and np.isfinite(Wv['TRALT'][cT][e]) and abs(Wv['TRALT'][cT][e])>=THR[e]: e+=1
        nx=e+1 if strict else e
        fT=fwd('TRALT',FC['TRALT'][i],i,e) if usesT else 0.0
        fG=fwd('XAUUSD',FC['XAUUSD'][i],i,e) if usesX else 0.0
        if target=='A1': leg=fT; w=0.0
        elif target=='A2': w=beta[i]; leg=fT-w*fwd('XU030',FC['XU030'][i],i,e)
        elif target=='A3': w=bb[i]; leg=fT-w*fG
        else: leg=fG; w=0.0
        rows.append(dict(date=days[i],dir=dr,exit=days[e] if e<N else pd.NaT,gross=dr*leg*1e4,z=z[i],w=w))
    t=pd.DataFrame(rows)
    if len(t)==0: return t
    for nm,(T,X,U) in COST.items():
        aw=t.w.abs()
        t['c_'+nm]={'A1':T+0*aw,'A2':T+aw*U,'A3':T+aw*X,'B1':X+0*aw}[target]
    t['year']=t.date.dt.year; t['half']=t.date.dt.year.astype(str)+'H'+np.where(t.date.dt.month<=6,'1','2')
    return t
def tstat(x): 
    x=np.asarray(x); return np.nan if len(x)<3 or x.std(ddof=1)==0 else x.mean()/(x.std(ddof=1)/math.sqrt(len(x)))
def regime(y): return '19-20' if y<=2020 else ('21-23' if y<=2023 else '24-26')
def metr(t,cs,yrs):
    x=t.dropna(subset=['gross']); net=x.gross-x['c_'+cs]; n=len(x)
    o=dict(n=n,per_yr=n/yrs,brut=x.gross.mean(),net=net.mean(),t=tstat(net),hit=(net>0).mean(),std=net.std(ddof=1))
    rg=x.year.map(regime)
    for r in ['19-20','21-23','24-26']: o['net_'+r]=net[rg==r].mean(); o['n_'+r]=int((rg==r).sum())
    o['net_long']=net[x.dir>0].mean(); o['net_short']=net[x.dir<0].mean(); o['n_short']=int((x.dir<0).sum())
    k2=max(1,int(math.ceil(0.02*n))); o['net_ex2pct']=net.sort_values().iloc[:-k2].mean()
    o['worst']=net.min(); cum=net.cumsum().values; o['maxdd']=float((np.maximum.accumulate(cum)-cum).max())
    o['breakeven_cost']=x.gross.mean(); return o
SPEC=[('R1','A1','a'),('A1c','A1','c'),('R2','A3','a'),('A3c','A3','c'),('R3a','B1','a'),('R3b','B1','b'),('R3c','B1','c'),('A2','A2','a')]
# ---------- 1 saglama
sel=None
for mp in (250,120,90,60,30):
    S_=make_S(mp); t=build(S_,'A2','a',2); mm=metr(t,'dusuk',1)
    P(f'SAGLAMA min_periods={mp}: n={mm["n"]} net={mm["net"]:.1f} t={mm["t"]:.2f} brut={mm["brut"]:.1f}',True)
    if sel is None and 405<=mm['n']<=423: sel=(f'min_periods={mp}',S_)
P('SECILEN '+sel[0],True); S=sel[1]
first=S.z.first_valid_index(); yrs=(days[-1]-first).days/365.25
P(f'ilk z: {first.date()} yil={yrs:.2f}',True)
# ---------- 2 ana kurallar
T={}; rows=[]; ytab=[]
for lab,tg,ru in SPEC:
    for k in (1,2,3):
        t=build(S,tg,ru,k); T[(lab,k)]=t
for lab,tg,ru in SPEC:
    for k in (1,2,3):
        t=T[(lab,k)]
        for cs in COST:
            o=metr(t,cs,yrs); o.update(rule=lab,k=k,cost=cs); rows.append(o)
        if k==2:
            for cs in COST:
                x=t.dropna(subset=['gross']).copy(); x['net']=x.gross-x['c_'+cs]
                g=x.groupby('year').agg(n=('net','size'),net_mean=('net','mean'),net_sum=('net','sum')); g['rule']=lab; g['cost']=cs; ytab.append(g.reset_index())
M=pd.DataFrame(rows); base={'R1':'A1c','R2':'A3c','R3a':'R3c','R3b':'R3c','A2':'A1c'}
def bnet(r):
    b=base.get(r.rule); 
    return np.nan if b is None else M[(M.rule==b)&(M.k==r.k)&(M.cost==r.cost)].net.iloc[0]
M['baz_net']=M.apply(bnet,axis=1)
M['gecti_t2']=M.t>=2; M['gecti_ex2']=M.net_ex2pct>0; M['gecti_rejim']=(M[['net_19-20','net_21-23','net_24-26']]>0).sum(axis=1)>=2; M['gecti_taban']=M.net>M.baz_net
M['GECTI']=M.gecti_t2&M.gecti_ex2&M.gecti_rejim&M.gecti_taban
M.round(2).to_csv(OUT+'metrikler.csv',index=False); pd.concat(ytab).round(2).to_csv(OUT+'yil_tablosu_k2.csv',index=False)
cols=['rule','k','cost','n','per_yr','brut','net','t','hit','net_19-20','net_21-23','net_24-26','net_ex2pct','worst','maxdd','baz_net','GECTI']
P(M[M.k==2][cols].round(2).to_string(),True)
P('k=1,3 bireysel:',True); P(M[(M.k!=2)&(M.cost=='bireysel')&M.rule.isin(['R1','R2','R3a','A2'])][['rule','k','n','net','t','GECTI']].round(2).to_string(),True)
for lab in ['R1','R2','R3a']:
    P(M[(M.rule==lab)&(M.k==2)][['rule','cost','net_long','net_short','n_short','breakeven_cost']].round(1).to_string(),False)
for lab in ['R1','A1c','R2','R3a','R3b','A2']:
    t=T[(lab,2)].copy(); t['exit']=t.exit.dt.date; t['date']=t.date.dt.date
for grp,labs in [('tralt',['R1','A1c','R2','A3c','A2']),('xau',['R3a','R3b','R3c'])]:
    out=[]
    for lab in labs:
        t=T[(lab,2)][['date','exit','dir','gross','z','w','c_dusuk','c_bireysel']].copy(); t.insert(0,'rule',lab); out.append(t)
    pd.concat(out).round(3).to_csv(OUT+f'islemler_k2_{grp}.csv',index=False)
# hedge kontrat sayisi
lastb=S.b.dropna().iloc[-1]; med_b=S.b[S.index>='2025-11-10'].median(); gold=float(front['XAUUSD'].settle.dropna().iloc[-1]); trp=float(front['TRALT'].settle.dropna().iloc[-1])
hr=[]
for nom in (10000,20000,30000):
    for bn,bv in (('son_b',lastb),('medyan12ay_b',med_b)):
        x=abs(bv)*nom/gold; rr=round(x); hr.append(dict(nominal=nom,b=bn,bdeg=bv,ons_kontrat=x,yuvarlak=rr,yuvarlama_hata_pct=(abs(rr-x)/x*100 if x>0 else np.nan)))
HR=pd.DataFrame(hr); HR.round(3).to_csv(OUT+'hedge_kontrat.csv',index=False); P(f'altin {gold} TRALT {trp} USDTRY {usdtry_last}',True); P(HR.round(2).to_string(),True)
# ---------- 3 bootstrap
rng=np.random.default_rng(12345)
def hys(lo,hi):
    return [f'{y}H{h}' for y in range(lo,hi+1) for h in (1,2)]
SCEN={'tam':(2019,2026),'2019-20':(2019,2020),'2021-23':(2021,2023),'2024-26':(2024,2026)}
brow=[]
for lab in ['R1','R2','R3a','A2']:
    t=T[(lab,2)].dropna(subset=['gross']).copy(); t['net']=t.gross-t.c_bireysel
    for sc in list(SCEN)+['en_iyi2pct_cikarilmis']:
        if sc=='en_iyi2pct_cikarilmis':
            kk=max(1,int(math.ceil(0.02*len(t)))); tt=t.sort_values('net').iloc[:-kk]; pool=hys(*SCEN['tam']); first_h=t.half.min()
        else:
            tt=t; pool=hys(*SCEN[sc])
        pool=[h for h in pool if h>=(tt.half.min() if sc!='tam' and sc!='en_iyi2pct_cikarilmis' else first_h if sc=='en_iyi2pct_cikarilmis' else t.half.min()) and h<=t.half.max()] if sc in('tam','en_iyi2pct_cikarilmis') else [h for h in pool if h<=t.half.max()]
        H=np.array([tt[tt.half==h].net.sum() for h in pool])
        if len(H)<2: continue
        ann=H[rng.integers(0,len(H),(5000,2))].sum(1)
        brow.append(dict(rule=lab,senaryo=sc,n_yarıyıl=len(H),ort_bps=ann.mean(),medyan_bps=np.median(ann),p5_bps=np.percentile(ann,5),p95_bps=np.percentile(ann,95),
            ort_usd20k=ann.mean()/1e4*20000,medyan_usd20k=np.median(ann)/1e4*20000,p5_usd20k=np.percentile(ann,5)/1e4*20000,p95_usd20k=np.percentile(ann,95)/1e4*20000,zarar_olas=(ann<0).mean()))
B=pd.DataFrame(brow); B.round(3).to_csv(OUT+'bootstrap.csv',index=False)
P(B[['rule','senaryo','n_yarıyıl','ort_bps','medyan_bps','p5_bps','p95_bps','ort_usd20k','p5_usd20k','p95_usd20k','zarar_olas']].round(2).to_string(),True)
# ---------- 4 risk/likidite
w12=days>=pd.Timestamp('2025-11-10'); rk=[]
for u,nm in (('TRALT','F_TRALT'),('XAUUSD','F_XAUUSD')):
    for k in (1,2,3):
        v=[]
        for i in np.where(w12)[0]:
            c=FC[u][i]
            if isinstance(c,str): v.append(fwd(u,c,i,i+k))
        v=np.array([a for a in v if np.isfinite(a)])*1e4
        rk.append(dict(arac=nm,k=k,n=len(v),std_bps=v.std(ddof=1),q01=np.percentile(v,1),q05=np.percentile(v,5),q95=np.percentile(v,95),q99=np.percentile(v,99),std_usd20k=v.std(ddof=1)/1e4*20000,q01_usd20k=np.percentile(v,1)/1e4*20000,q05_usd20k=np.percentile(v,5)/1e4*20000))
RK=pd.DataFrame(rk); RK.round(2).to_csv(OUT+'risk_12ay.csv',index=False); P(RK.round(1).to_string(),True)
lk=pd.DataFrame({'yil':days.year,'kilit':lockT&rT.notna().values,'gun':rT.notna().values}).groupby('yil').sum(); lk.to_csv(OUT+'kilit_gunleri.csv'); P('kilit gunleri:\n'+lk.T.to_string(),True)
lq=[]
for u,nm,mult in (('TRALT','F_TRALT',100),('XAUUSD','F_XAUUSD',1)):
    f=front[u][w12]; px=float(f.settle.dropna().iloc[-1])
    for nom in (10000,20000,30000):
        kon=nom*usdtry_last/(px*mult) if u=='TRALT' else nom/px
        lq.append(dict(arac=nm,nominal=nom,fiyat=px,kontrat=kon,medyan_hacim_TL=f.vol.median(),medyan_miktar=f.qty.median(),medyan_acik_poz=f.oi.median(),gunluk_miktar_yuzde=kon/f.qty.median()*100,sifir_islem_gun=int((f.qty.fillna(0)==0).sum())))
LQ=pd.DataFrame(lq); LQ.round(2).to_csv(OUT+'likidite.csv',index=False); P(LQ.round(1).to_string(),True)
fx=front['XAUUSD']; nx=nxt2['XAUUSD']
car=(np.log(nx.settle/fx.settle)/((nx.vade-fx.vade).dt.days)*365)[w12].dropna()
P(f'XAUUSD tasima yillik medyan (son12ay) {car.median():.4f} n={len(car)}; 2gun bps={car.median()*2/365*1e4:.2f}',True)
# ---------- 5 guncel
win=(days>=pd.Timestamp('2026-10-26'))
cur=pd.DataFrame({'date':days[win].date,'g_pct':S.g[win].values*100,'z':S.z[win].values,'gap':gap[win],'TRALT_r_pct':rT[win].values*100,'kilit':lockT[win],'arife':[x in ARIFE for x in days[win]]}); cur.round(3).to_csv(OUT+'guncel_gunler.csv',index=False)
P(cur.round(2).to_string(),True)
for lab in ['R1','R2','A2']:
    t=T[(lab,2)]; t=t[t.date>=pd.Timestamp('2026-10-26')].copy(); t['net_bireysel']=t.gross-t.c_bireysel
    t.round(2).to_csv(OUT+f'guncel_islem_{lab}.csv',index=False)
    P(f'{lab} guncel islemler:\n'+t[['date','dir','exit','gross','z','net_bireysel']].round(2).to_string(),True)
    P(f'{lab} 05.11 sonrasi giris: {int((t.date>pd.Timestamp("2026-11-05")).sum())}; sonucu belli: {int(t[t.date>pd.Timestamp("2026-11-05")].gross.notna().sum())}',True)
