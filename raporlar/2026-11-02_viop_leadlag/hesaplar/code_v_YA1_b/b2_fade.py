# (b) TC fade ve (c) TU fade: curutme testleri (spot acilis girisi)
import pandas as pd, numpy as np, sys
from blib import *
rng=np.random.default_rng(7)
F=pd.read_parquet(f'{OUT}/_full.parquet')
F=F[F.ok1&F.intra1.notna()].copy()
F['tk']=0.01/F.px  # VIOP pay vadelisi tik 0.01 TL; gercek fiyat seviyesi (b1b_price)
F['s']=-F.intra1                       # gercek short PnL (basit getiri)
F['s_log']=np.log(F.o_1/F.c_1)         # kaynak/1.asama: -log(c/o)
# piyasa notr: ayni gun VIOP47 esit agirlikli gun-ici (olay hissesi haric yaklasik: tum VIOP47)
v=F[F.viop47&F.ok1]
xs=v.groupby('date_1').intra1.agg(['sum','count'])
F=F.join(xs,on='date_1')
F['xs_ex']=np.where(F.viop47,(F['sum']-F.intra1)/(F['count']-1),F['sum']/F['count'])
F['s_mn']=-(F.intra1-F.xs_ex)
F['s_x']=-(F.intra1-F.xintra1)
C=15e-4
def per(sub):
    if sub.year.nunique()==0: return {}
    return summ(sub,'net')
def table(E,label):
    E=E.copy(); E['net']=E.s-C
    out=[]
    def add(nm,sub,col='net'):
        r=summ(sub.assign(net=sub[col]),'net') if len(sub)>2 else dict(n=len(sub))
        r['set']=nm; out.append(r)
    add('gross_log',E.assign(net=E.s_log))
    add('gross_simple',E.assign(net=E.s))
    add('@15',E)
    add('@15+tik',E.assign(net=E.s-C-E.tk))
    add('@30+tik',E.assign(net=E.s-30e-4-E.tk))
    add('@15 piyasa-notr(VIOP47 xs)',E.assign(net=E.s_mn-C))
    add('@15 XU100-notr',E.assign(net=E.s_x-C))
    for a,b,nm in [('2015-12-01','2017-12-31','2015-12..17 (P20)'),('2018-01-01','2020-03-10','2018..2020-03 (P20)'),('2020-03-13','2020-12-31','2020-03..12 (P10)'),('2021-01-01','2023-12-31','2021-23'),('2024-01-01','2026-12-31','2024-26')]:
        add('@15 '+nm,E[(E.date>=a)&(E.date<=b)])
    # uc deger
    q1,q99=E.net.quantile([.01,.99])
    add('@15 winsor1%',E.assign(net=E.net.clip(q1,q99)))
    dm=E.groupby('date_1').net.sum().sort_values()
    add('@15 en iyi 10 gun haric',E[~E.date_1.isin(dm.index[-10:])])
    add('@15 en iyi 5% gun haric',E[~E.date_1.isin(dm.index[-max(1,int(len(dm)*.05)):])])
    add('@15 simetrik: en iyi+en kotu 10 gun haric',E[~E.date_1.isin(list(dm.index[-10:])+list(dm.index[:10]))])
    k=max(1,int(len(dm)*.05)); add('@15 simetrik 5%+5% gun haric',E[~E.date_1.isin(list(dm.index[-k:])+list(dm.index[:k]))])
    q5,q95=E.net.quantile([.05,.95]); add('@15 islem kirpilmis 5/95',E[(E.net>q5)&(E.net<q95)])
    df=pd.DataFrame(out).set_index('set')
    print(f'\n==== {label} ====')
    print(df[['n','days','trade_bps','trade_t','day_bps','day_t','med_bps','hit']].to_string())
    # LOYO / LOSO
    yy={y:round(E[E.year!=y].net.mean()*1e4,1) for y in sorted(E.year.unique())}
    by={y:(round(E[E.year==y].net.mean()*1e4,1),int((E.year==y).sum())) for y in sorted(E.year.unique())}
    ss=E.groupby('sym').net.agg(['mean','count'])
    loso=[E[E.sym!=s].net.mean()*1e4 for s in ss.index]
    print('yil (ort, n):',by)
    print('LOYO aralik:',min(yy.values()),max(yy.values()),'| LOSO aralik:',round(min(loso),1),round(max(loso),1),'| hisse>0:',int((ss['mean']>0).sum()),'/',len(ss))
    return E

def placebo(E,pool,label,nperm=2000):
    """(i) ayni hisse, rastgele tarih (P10); (ii) ayni gun rastgele hisse; (iii) gap-eslesmeli kontrol"""
    E=E.copy();
    obs=(E.s.mean())
    # (i) ayni hisse rastgele gun
    pool_s={k:g.s.values for k,g in pool.groupby('sym')}
    cnt=E.groupby('sym').size()
    sims=np.empty(nperm)
    for i in range(nperm):
        tot=0; n=0
        for s,k in cnt.items():
            a=pool_s.get(s)
            if a is None or len(a)==0: continue
            tot+=a[rng.integers(0,len(a),k)].sum(); n+=k
        sims[i]=tot/n
    p1=(sims>=obs).mean()
    # (ii) ayni gun rastgele hisse (olay olmayan)
    pool_d={k:g.s.values for k,g in pool.groupby('date_1')}
    cntd=E.groupby('date_1').size()
    sims2=np.empty(nperm)
    for i in range(nperm):
        tot=0; n=0
        for d,k in cntd.items():
            a=pool_d.get(d)
            if a is None or len(a)==0: continue
            tot+=a[rng.integers(0,len(a),k)].sum(); n+=k
        sims2[i]=tot/n
    p2=(sims2>=obs).mean()
    print(f'-- plasebo {label}: gozlenen brut {obs*1e4:.1f} bps | ayni-hisse rastgele gun: ort {sims.mean()*1e4:.1f} [95% {np.quantile(sims,.95)*1e4:.1f}] p={p1:.4f} | ayni-gun rastgele hisse: ort {sims2.mean()*1e4:.1f} [95% {np.quantile(sims2,.95)*1e4:.1f}] p={p2:.4f}')
    # (iii) gap eslesmeli
    bins=[-1,-0.02,-0.005,0.005,0.02,0.04,0.06,0.08,0.12,1]
    E['gb']=pd.cut(E.gap1,bins); pool=pool.copy(); pool['gb']=pd.cut(pool.gap1,bins)
    pm=pool.groupby('gb',observed=True).s.mean()
    exp=E.gb.map(pm).astype(float)
    d=E.s-exp
    m,t,n=cl_t(d,E.date_1)
    print(f'   gap-eslesmeli kontrole gore fazla brut: {m*1e4:.1f} bps (t {t:.2f}, n {n}); kontrol beklenen {exp.mean()*1e4:.1f}')
    tab=pd.DataFrame({'olay_n':E.groupby('gb',observed=True).size(),'olay_s':E.groupby('gb',observed=True).s.mean()*1e4,'kontrol_n':pool.groupby('gb',observed=True).size(),'kontrol_s':pm*1e4}).round(1)
    print(tab.to_string())
    # (iv) bayatlatilmis sinyal: t+2, t+3 gun-ici short
    for k in [2,3]:
        x=-E[f'intra{k}']; m,t,n=cl_t(x,E.date_1)
        print(f'   bayat sinyal t+{k} gun-ici short brut: {m*1e4:.1f} (t {t:.2f}, n {n})')

P10=F[F.reg=='P10']
evt=P10.TC|P10.TCs|P10.TU_src|P10.TU_s|P10.NEAR|P10.BC|(P10.R>1.06)|(P10.R<0.94)
pool_v=P10[P10.viop47&~evt]
pool_a=P10[~evt]
for nm,mask,pool in [('TC VIOP47 (P10)',F.TC&F.viop47,pool_v),('TC VIOP47 vadeli-listeli (P10)',F.TC&F.fut_listed,pool_v),('TC tum 217 (P10)',F.TC,pool_a),
                     ('TU_src VIOP47',F.TU_src&F.viop47,pool_v),('TU_s (sik) VIOP47',F.TU_s&F.viop47,pool_v),('TU_s (sik) vadeli-listeli',F.TU_s&F.fut_listed,pool_v),('TU_src tum',F.TU_src,pool_a),('TU_s tum',F.TU_s,pool_a)]:
    allreg=F[mask]
    if nm.startswith('TC VIOP47 (P10)') or nm.startswith('TC tum'):
        E=table(allreg,nm+' [P20 dahil alt donemler]')
    E=allreg[allreg.reg=='P10']
    if not (nm.startswith('TC VIOP47 (P10)') or nm.startswith('TC tum')):
        table(E,nm)
    placebo(E,pool,nm,nperm=1000)
# koşulsuz gun-ici short (piyasa suruklenmesi)
for nm,pool in [('VIOP47',P10[P10.viop47]),('tum',P10)]:
    r=summ(pool.assign(net=pool.s),'net'); print('kosulsuz gun-ici short brut',nm,r)
    for a,b in [('2020-03-13','2020-12-31'),('2021-01-01','2023-12-31'),('2024-01-01','2026-12-31')]:
        q=pool[(pool.date>=a)&(pool.date<=b)]; print('   ',a[:4],b[:4],round(q.s.mean()*1e4,1))
