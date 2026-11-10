import sys, json, os, math
import numpy as np, pandas as pd
from collections import Counter
DATA, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(20261110)
LOG = []
def log(*a):
    s=" ".join(str(x) for x in a); LOG.append(s); print(s)

def load(sym):
    j=json.load(open(f"{DATA}/{sym}.json")); res=j['chart']['result'][0]
    ts=pd.to_datetime(res['timestamp'],unit='s').normalize()
    q=res['indicators']['quote'][0]
    df=pd.DataFrame({k:q[k] for k in ['open','high','low','close','volume']},index=ts)
    try: df['adj']=res['indicators']['adjclose'][0]['adjclose']
    except Exception: df['adj']=df['close']
    df['adj']=df['adj'].fillna(df['close'])
    df=df[~df.index.duplicated(keep='last')].sort_index()
    return df.dropna(subset=['adj'])

def bist_df(sym):
    df=load(sym)
    if (df.volume>0).mean()>0.5: df=df[df.volume>0]
    return df
def bist_lp(sym):
    df=bist_df(sym); s=df.adj.astype(float).copy()
    r=np.log(s).diff(); bad=(r.abs()>0.25)
    if bad.sum(): log(f"  veri hatasi maskelendi {sym}: {int(bad.sum())} gun")
    s[bad]=np.nan
    return np.log(s)

cal=bist_df('XU030.IS').index
N=len(cal)
LP={}
def need(sym):
    if sym not in LP: LP[sym]=bist_lp(sym+'.IS').reindex(cal)
    return LP[sym]
for s in ['XU030','XU100']: need(s)
log("BIST takvim", cal[0].date(), cal[-1].date(), N)

def zs(lp, win, minp, idx=None):
    s=lp.dropna(); r=s.diff(); sd=r.rolling(win,min_periods=minp).std().shift(1)
    z=r/sd
    if idx is not None: z=z.reindex(idx); r=r.reindex(idx)
    return z,r
def fwd(lp, idx, h):
    s=lp.dropna(); v=s.values; pos=idx.get_indexer(s.index)
    ret=np.full(len(idx),np.nan); ex=np.full(len(idx),-1,int)
    if len(v)>h:
        ret[pos[:-h]]=v[h:]-v[:-h]; ex[pos[:-h]]=pos[h:]
    return ret,ex
def bret(stocks,h,minc):
    M=np.column_stack([(need(s).shift(-h)-need(s)).values for s in stocks])
    cnt=np.isfinite(M).sum(1); out=np.where(cnt>=minc,np.nanmean(np.where(np.isfinite(M),M,np.nan),axis=1),np.nan)
    return out, np.minimum(np.arange(N)+h,N-1)
def select(sig,ret,ex,start=260):
    out=[]; busy=-1
    for i in np.flatnonzero(sig & np.isfinite(ret)):
        if i<start or i<busy: continue
        out.append(i); busy=ex[i]
    return np.array(out,int)
def tstat(x):
    x=np.asarray(x,float); n=len(x)
    if n<3 or x.std(ddof=1)==0: return float('nan')
    return x.mean()/(x.std(ddof=1)/math.sqrt(n))
def stats(cfg, idx, c, ret, sign=1, costs=(10,44), show=True, test=''):
    ym=pd.Series(ret,index=c).groupby(c.year).mean()
    bench=ym.reindex(c.year).values
    g=sign*ret[idx]*1e4; b=sign*bench[idx]*1e4; ex=g-b; n=len(idx)
    row=dict(test=test,cfg=cfg,n=n,show=show)
    if n<3:
        return row,pd.DataFrame()
    d=c[idx]; yr=d.year
    row.update(g=g.mean(),ex=ex.mean(),tex=tstat(ex),tg=tstat(g))
    c1,c2=costs
    row.update(c1=c1,nC1=g.mean()-c1,tC1=tstat(g-c1),nex1=ex.mean()-c1,nC2=g.mean()-c2,tC2=tstat(g-c2),nex2=ex.mean()-c2)
    for nm,m in [('IS',d<=pd.Timestamp('2021-12-31')),('OOS',d>=pd.Timestamp('2022-01-01')),('SON',d>=pd.Timestamp('2024-01-01'))]:
        row[nm+'_n']=int(m.sum()); row[nm+'_ex']=ex[m].mean() if m.sum() else np.nan; row[nm+'_t']=tstat(ex[m]) if m.sum()>2 else np.nan
    y=pd.DataFrame({'y':yr,'g':g,'ex':ex}).groupby('y').agg(n=('g','size'),brut=('g','mean'),fazla=('ex','mean')).reset_index()
    yy=y[y.n>=3]; row['pos']=f"{(yy.fazla>0).sum()}/{len(yy)}"
    return row,y
ROWS=[]; YEARLY={}
def add(cfg,idx,c,ret,yearly=None,**kw):
    r,y=stats(cfg,idx,c,ret,**kw); ROWS.append(r)
    if yearly: YEARLY[yearly]=y
    return r

# ---------- sinyaller
zx,rx=zs(LP['XU030'],60,40,cal); zxv=zx.values
# dogrulama: saf python
def manual():
    j=json.load(open(f"{DATA}/XU030.IS.json")); res=j['chart']['result'][0]
    ts=res['timestamp']; q=res['indicators']['quote'][0]; adj=res['indicators']['adjclose'][0]['adjclose']; vol=q['volume']
    rows=[(t,a,v) for t,a,v in zip(ts,adj,vol) if a is not None]
    if sum(1 for t,a,v in rows if v and v>0)/len(rows)>0.5: rows=[x for x in rows if x[2] and x[2]>0]
    import datetime
    dts=[datetime.datetime.utcfromtimestamp(t).date() for t,a,v in rows]; a=[x[1] for x in rows]
    r=[None]+[math.log(a[i]/a[i-1]) for i in range(1,len(a))]
    r=[None if (x is not None and abs(x)>0.25) else x for x in r]
    out=[]; busy=-1
    for i in range(260,len(a)-2):
        w=[x for x in r[i-60:i] if x is not None]
        if len(w)<40 or r[i] is None: continue
        m=sum(w)/len(w); sd=math.sqrt(sum((x-m)**2 for x in w)/(len(w)-1)); z=r[i]/sd
        if z>=1 and i>=busy:
            out.append((dts[i],round(z,3),a[i],a[i+2],round(math.log(a[i+2]/a[i])*1e4,1))); busy=i+2
        if len(out)==3: break
    return out
man=manual()
sel=select(zxv>=1,*fwd(LP['XU030'],cal,2))
log("T1 elle dogrulama (saf python, ilk 3 islem k=1 h=2):")
for m,i in zip(man,sel[:3]):
    pr=fwd(LP['XU030'],cal,2)[0][i]*1e4
    log(f"  elle: {m[0]} z={m[1]} giris={m[2]:.2f} cikis={m[3]:.2f} getiri={m[4]} bps | pandas: {cal[i].date()} z={zxv[i]:.3f} getiri={pr:.1f} bps")

# ---------- T1
H=(1,2,3)
RET={}
for tgt in ['XU030','XU100']:
    for h in H: RET[(tgt,h)]=fwd(LP[tgt],cal,h)
for tgt in ['XU030','XU100']:
    for k in (1.0,1.5):
        for h in H:
            ret,ex=RET[(tgt,h)]
            idx=select(zxv>=k,ret,ex)
            show=(tgt=='XU030') or (k==1.0 and h in(2,3))
            add(f"T1 {tgt} k{k} h{h}",idx,cal,ret,costs=(5,5),show=show,test='T1',yearly=(f"T1_{tgt}_k1_h{h}" if k==1.0 and tgt=='XU030' and h in(2,3) else None))
for h in H:
    ret,ex=RET[('XU030',h)]
    for k in (1.0,1.5):
        idx=select(zxv<=-k,ret,ex)
        add(f"T1 AYNA kisa XU030 z<=-{k} h{h}",idx,cal,ret,sign=-1,costs=(5,5),show=(k==1.0 and h in (2,3)),test='T1')
        if k==1.0 and h in(2,3):
            r=stats('x',idx,cal,ret,costs=(5,5))[0]
            r2=ROWS[-1]; log(f"  ayna long-yonlu ort (ham getiri sonrasi) h{h}: {-r2['g']:.1f} bps n{r2['n']}")

# ---------- T2
BASK=['AKBNK','GARAN','YKBNK','ISCTR','SAHOL','KCHOL','THYAO','PGSUS','TUPRS','EREGL','ASELS','BIMAS','TCELL','FROTO','SISE']
for s in BASK: need(s)
BR={}; DIFF={}
for h in H:
    br,bex=bret(BASK,h,10); BR[h]=(br,bex)
    DIFF[h]=(br-RET[('XU030',h)][0],bex)
for k in (1.0,1.5):
    for h in H:
        br,bex=BR[h]
        idx=select(zxv>=k,br,bex)
        add(f"T2 sepet k{k} h{h}",idx,cal,br,show=(k==1.0 or h==3),test='T2',yearly=(f"T2_sepet_k1_h{h}" if k==1.0 else None))
        d,_=DIFF[h]
        add(f"T2 sepet-XU030 k{k} h{h}",idx,cal,d,show=(k==1.0 or h==3),test='T2')

# ---------- T3 plasebo
def placebo(real_idx,ret,h,nsim=2000):
    ok=np.isfinite(ret)&(np.arange(N)>=260); el=np.flatnonzero(ok)
    byy={y:el[cal.year[el]==y] for y in set(cal.year[el])}
    cnt=Counter(cal.year[real_idx]); real=ret[real_idx].mean()*1e4
    means=np.empty(nsim)
    for s in range(nsim):
        blocked=np.zeros(N+2*h+2,bool); vals=[]
        for y,cn in cnt.items():
            cand=rng.permutation(byy[y]); p=0
            for c in cand:
                if blocked[c]: continue
                vals.append(ret[c]); blocked[max(0,c-h+1):c+h]=True; p+=1
                if p==cn: break
        means[s]=np.mean(vals)*1e4
    return real,means.mean(),(means>=real).mean(),means.std()
PL=[]
for nm,ret,ex,h,k in [('T1 XU030 k1 h2',*RET[('XU030',2)],2,1.0),('T1 XU030 k1 h3',*RET[('XU030',3)],3,1.0),('T2 sepet k1 h3',*BR[3],3,1.0)]:
    idx=select(zxv>=k,ret,ex); r,m,p,sd=placebo(idx,ret,h)
    PL.append((nm,len(idx),r,m,sd,p)); log(f"T3 {nm}: n{len(idx)} gercek {r:.1f} plasebo ort {m:.1f} sd {sd:.1f} p={p:.4f}")

# ---------- T4
def beta60(stock):
    s,r=zs(need(stock),60,40,cal)[1],None
    rs=zs(need(stock),60,40,cal)[1]
    cov=rs.rolling(60,min_periods=40).cov(rx); var=rx.rolling(60,min_periods=40).var()
    return (cov/var).shift(1).values
for st in ['KCHOL','TUPRS','ASELS','EREGL']:
    b=beta60(st)
    for k in (1.0,1.5):
        for h in (2,3):
            ret,ex=fwd(need(st),cal,h)
            xr=np.full(N,np.nan); v=ex>=0; xr[v]=LP['XU030'].values[ex[v]]-LP['XU030'].values[v]
            res=ret-b*xr
            idx=select(zxv>=k,ret,ex)
            add(f"T4 {st} ham k{k} h{h}",idx,cal,ret,show=False,test='T4')
            add(f"T4 {st} ARTIK k{k} h{h}",idx,cal,res,show=(k==1.0 or h==3 or st=='KCHOL'),test='T4')
            if len(idx): ROWS[-1]['nb']=np.nanmean(b[idx])

# ---------- ABD -> BIST
def map_sig(sigser):
    d=sigser.index[sigser.values.astype(bool)]
    t=cal.searchsorted(d,side='right'); t=t[t<N]
    a=np.zeros(N,bool); a[t]=True; return a
# T5
kb=load('KBE'); lpk=np.log(kb.adj); zk,_=zs(lpk,60,40)
bank=['AKBNK','GARAN','YKBNK','ISCTR']
for s in bank: need(s)
TG={}
for h in H:
    TG[('AKBNK',h)]=fwd(need('AKBNK'),cal,h); TG[('XU030',h)]=RET[('XU030',h)]
    TG[('BANKA4',h)]=bret(bank,h,3)
for k in (1.0,1.5):
    sg=map_sig(zk>=k)
    for h in H:
        for tg in ['AKBNK','XU030','BANKA4']:
            ret,ex=TG[(tg,h)]
            idx=select(sg,ret,ex)
            main=(tg=='AKBNK') or (k==1.5 and h==2) or (k==1.0 and h==2)
            r=add(f"T5 KBE z>={k} -> {tg} h{h}",idx,cal,ret,show=main,test='T5',yearly=(f"T5_AKBNK_k{k}_h{h}" if tg=='AKBNK' and h==2 else None))
            if tg=='AKBNK' and len(idx):
                ov=(zxv[idx]>=1); ROWS[-1]['ov']=ov.mean()
                if k==1.5 and h==2 or (k==1.0 and h==2):
                    log(f"T5 AKBNK k{k} h{h}: n{len(idx)} ayni gun z_XU030>=1 orani {ov.mean():.3f}")
                    for nm,m in [('XU030z<1',~ov),('XU030z>=1',ov)]:
                        if m.sum()>=3:
                            add(f"T5 AKBNK k{k} h{h} | {nm}",idx[m],cal,ret,show=True,test='T5')
# T6
us={}
for s in ['VLO','MPC','PSX','PBF','_GSPC']:
    d=load(s); us[s]=np.log(d.adj).diff()
R=pd.concat([us[s] for s in ['VLO','MPC','PSX','PBF']],axis=1).dropna().mean(axis=1)
S=us['_GSPC']; J=pd.concat([R.rename('R'),S.rename('S')],axis=1).dropna()
beta=(J.R.rolling(250,min_periods=150).cov(J.S)/J.S.rolling(250,min_periods=150).var()).shift(1)
P=J.R-beta*J.S; zP=P/P.rolling(250,min_periods=150).std().shift(1)
log("T6 z P: n",int(zP.notna().sum()),"z>1:",int((zP>1).sum()),"z<-1:",int((zP<-1).sum()))
sgl=map_sig(zP>1); sgs=map_sig(zP<-1)
trl=need('TUPRS'); rtu=zs(trl,60,40,cal)[1].values; rxv=rx.values
for h in (2,3):
    ret,ex=fwd(trl,cal,h)
    il=select(sgl,ret,ex)
    add(f"T6 TUPRS UZUN z>1 h{h}",il,cal,ret,show=True,test='T6',yearly=f"T6_long_h{h}")
    ish=select(sgs,ret,ex)
    add(f"T6 TUPRS KISA z<-1 h{h}",ish,cal,ret,sign=-1,show=True,test='T6',yearly=f"T6_short_h{h}")
    a=rtu[il]; rel=rtu[il]-rxv[il]; med=np.nanmedian(rel)
    for nm,m in [('(a) TUPRS_t<=0',a<=0),('(b) TUPRS_t>0',a>0),('(c) goreli<=medyan',rel<=med),('(c) goreli>medyan',rel>med)]:
        add(f"T6 uzun h{h} | {nm}",il[m],cal,ret,show=True,test='T6')
# T7
d1=bist_lp('RYGYO.IS').reindex(cal); LP['RYGYO']=d1; LP['RYSAS']=bist_lp('RYSAS.IS').reindex(cal)
zr,_=zs(LP['RYGYO'],250,150,cal); zr=zr.clip(-5,5).values
ret,ex=fwd(LP['RYSAS'],cal,1)
sg=zr>1
i0=select(sg,ret,ex); add("T7 RYGYO z>1 -> RYSAS h1",i0,cal,ret,show=True,test='T7',yearly='T7_h1')
sg2=np.zeros(N,bool); sg2[1:]=sg[:-1]
i1=select(sg2,ret,ex); add("T7 1 gun gec giris",i1,cal,ret,show=True,test='T7',yearly='T7_gec')
ok=(zr<-1); 
add("T7 (ayna) z<-1 -> RYSAS h1 (bilgi)",select(zr<-1,ret,ex),cal,ret,show=False,test='T7')
for sym in ['RYSAS','RYGYO']:
    d=bist_df(sym+'.IS') if False else load(sym+'.IS'); t=d.tail(250); tl=(t.close*t.volume)
    log(f"T7 {sym} son 250 gun medyan gunluk TL hacim: tum {tl.median():,.0f} | hacim>0 gunler {tl[t.volume>0].median():,.0f}; hacim0 gun {(t.volume==0).sum()}; son tarih {d.index[-1].date()}")

# T8
def t8(sym,rule,hs):
    d=load(sym); d=d[(d.high>d.low)]; c=d.index; n=len(c)
    ibs=((d.close-d.low)/(d.high-d.low)).values
    sig=rule(d,ibs); lp=np.log(d.adj)
    log(f"T8 {sym}: veri {c[0].date()}..{c[-1].date()} n{n}")
    for h in hs:
        ret=np.full(n,np.nan); v=lp.values; ret[:-h]=v[h:]-v[:-h]; ex=np.minimum(np.arange(n)+h,n-1)
        for nm,m in [('tum',np.ones(n,bool)),('2016+',c>=pd.Timestamp('2016-01-01')),('2011-15',c<pd.Timestamp('2016-01-01'))]:
            idx=select(sig&m,ret,ex)
            r=add(f"T8 {sym} h{h} {nm}",idx,c,ret,costs=(13,13),show=True,test='T8',yearly=(f"T8_{sym}_h{h}_tum" if nm=='tum' else None))
t8('QQQ',lambda d,ibs:(ibs<0.10)&(d.close.values<d.close.shift(1).values),(2,3))
t8('SMH',lambda d,ibs:(ibs<0.20),(1,2,3))

# ---------- cikti
df=pd.DataFrame(ROWS); df.to_csv(f"{OUT}/K2_tum_sonuc.csv",index=False)
for k,y in YEARLY.items(): y.to_csv(f"{OUT}/yil_{k}.csv",index=False)
pd.DataFrame(PL,columns=['test','n','gercek','plasebo_ort','plasebo_sd','p']).to_csv(f"{OUT}/T3_plasebo.csv",index=False)
f=lambda x:'-' if x is None or (isinstance(x,float) and np.isnan(x)) else f"{x:.0f}"
ft=lambda x:'-' if x is None or (isinstance(x,float) and np.isnan(x)) else f"{x:.1f}"
L=["| test | n | brut | fazla(t) | net c1 (t) | netfazla c1 | net c2 (t) | IS | OOS | SON | +yil |","|---|--:|--:|--|--|--:|--|--|--|--|--|"]
for r in ROWS:
    if not r.get('show') or 'g' not in r or pd.isna(r.get('g')): 
        if r.get('show'): L.append(f"| {r['cfg']} | {r['n']} | - |")
        continue
    L.append(f"| {r['cfg']} | {r['n']} | {f(r['g'])} | {f(r['ex'])}({ft(r['tex'])}) | {f(r['nC1'])}({ft(r['tC1'])}) | {f(r['nex1'])} | {f(r['nC2'])}({ft(r['tC2'])}) | {f(r['IS_ex'])}({ft(r['IS_t'])}) | {f(r['OOS_ex'])}({ft(r['OOS_t'])}) | {f(r['SON_ex'])}({ft(r['SON_t'])}) | {r['pos']} |")
open(f"{OUT}/tablo_ana.md","w").write("\n".join(L)+"\n")
open(f"{OUT}/log.txt","w").write("\n".join(LOG)+"\n")
print("\n".join(L)); print(len(L),"satir")
