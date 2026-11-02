# (d) Taban sonrasi suruklenme: curutme testleri
import pandas as pd, numpy as np
from blib import *
rng=np.random.default_rng(5)
P=pd.read_parquet(f'{OUT}/_panel.parquet').sort_values(['sym','date'])
F=pd.read_parquet(f'{OUT}/_full.parquet').sort_values(['sym','date'])
g=P.groupby('sym')
P['date_5']=g.date.shift(-5); P['adj_1']=g.adj.shift(-1); P['adj_5']=g.adj.shift(-5)
P['ca_any']=sum(g.ca.shift(-k).fillna(True).astype(bool) for k in range(1,6))>0
F=F.merge(P[['sym','date','date_5','ca_any']],on=['sym','date'],how='left')
F['Rl_1']=F.groupby('sym').Rl.shift(-1)
# (XU100 getirisi _full.parquet icindeki x2_5'ten)
# t+1 tabanda kilitli mi (spot): R_1 <= 0.9075 ve kapanis ~ dusuk
F['lock1']=(F.R_1<=0.9075)
B=F[F.BC&(F.reg=='P10')&F.ok1&(F.ca_any==False)&F.r2_5.notna()].copy()
B['feas']=~B.lock1
B['s']=-(B.r2_5-B.x2_5)          # basit, XU100 hedge
B['s_log']=-(np.log1p(B.r2_5)-np.log1p(B.x2_5))
B['s_raw']=-B.r2_5
B['tk']=0.01/B.px
cnt=B.groupby('date').size(); B['crowd']=B.date.map(cnt)
C=19e-4
def show(E,lab,date='date_1'):
    E=E.assign(net=E.s-C)
    r=summ(E,'net',date=date)
    rl=summ(E.assign(n2=E.s_log-C),'n2',date=date)
    print(f'{lab:55s} n {r["n"]:5d} trade {r["trade_bps"]:7.1f} (t {r["trade_t"]:5.2f}) day {r["day_bps"]:7.1f} (t {r["day_t"]:5.2f}) med {r["med_bps"]:7.1f} | log-trade {rl["trade_bps"]:7.1f} log-day {rl["day_bps"]:7.1f}')
for uni,mask in [('tum 217',B.sym.notna()),('VIOP47',B.viop47),('VIOP47 vadeli-listeli',B.fut_listed)]:
    E=B[mask&B.feas]
    print(f'\n=== {uni}: dolum-uygun (t+1 taban kilidi yok) short t+1 kapanis -> t+5, XU100 hedge, @19 ===')
    show(E,'tumu')
    for a,b in [('2020-03-13','2020-12-31'),('2021-01-01','2023-12-31'),('2024-01-01','2026-12-31')]:
        show(E[(E.date>=a)&(E.date<=b)],f'  {a[:7]}..{b[:7]}')
    show(E[E.crowd<5],'  kalabalik degil (ayni gun <5 taban)')
    show(E[E.crowd>=5],'  kalabalik (>=5 taban)')
    show(E[E.crowd==1],'  tekil (ayni gun 1 taban)')
    En=E.assign(net=E.s-C); dm=En.groupby('date_1').net.sum().sort_values()
    show(E[~E.date_1.isin(list(dm.index[:10])+list(dm.index[-10:]))],'  simetrik 10+10 gun haric')
    show(E[~E.date_1.isin(dm.index[-10:])],'  en iyi 10 gun haric')
    print('  yillar (islem basi @19):',En.groupby('year').net.agg(lambda x: round(x.mean()*1e4)).to_dict(),' n',En.groupby('year').size().to_dict())
# P20 rejimi
E=B0=F[F.BC&(F.reg=='P20')&F.ok1&(F.ca_any==False)&F.r2_5.notna()].copy()
E['s']=-(E.r2_5-E.x2_5); E['s_log']=-(np.log1p(E.r2_5)-np.log1p(E.x2_5)); E=E[~(E.R_1<=0.8075)]
print('\n=== P20 (2015-12..2020-03, +-%20) BC dolum-uygun ==='); show(E,'tum 217'); show(E[E.viop47],'VIOP47')
# plasebo: ayni hisse rastgele gun (P10), ayni short t+1->t+5 hedge
pool=F[(F.reg=='P10')&F.ok1&F.r2_5.notna()&(np.abs(F.R-1)<0.05)].copy(); pool['s']=-(pool.r2_5-pool.x2_5)
for uni,mask in [('tum 217',B.sym.notna()),('VIOP47',B.viop47)]:
    E=B[mask&B.feas]; obs=E.s.mean()
    ps={k:gg.s.values for k,gg in pool.groupby('sym')}; cn=E.groupby('sym').size(); sims=[]
    for i in range(1000):
        tot=0;n=0
        for s,k in cn.items():
            a=ps.get(s)
            if a is None: continue
            tot+=a[rng.integers(0,len(a),k)].sum(); n+=k
        sims.append(tot/n)
    sims=np.array(sims)
    # ayni gun rastgele hisse
    pd_={k:gg.s.values for k,gg in pool.groupby('date')}; cd=E.groupby('date').size(); sims2=[]
    for i in range(1000):
        tot=0;n=0
        for d,k in cd.items():
            a=pd_.get(d)
            if a is None or len(a)==0: continue
            tot+=a[rng.integers(0,len(a),k)].sum(); n+=k
        sims2.append(tot/n)
    sims2=np.array(sims2)
    print(f'plasebo {uni}: gozlenen brut islem-basi {obs*1e4:.1f} | ayni-hisse rastgele gun ort {sims.mean()*1e4:.1f} 95% {np.quantile(sims,.95)*1e4:.1f} p={(sims>=obs).mean():.3f} | ayni-gun rastgele hisse ort {sims2.mean()*1e4:.1f} 95% {np.quantile(sims2,.95)*1e4:.1f} p={(sims2>=obs).mean():.3f}')
# vadeli versiyonu: t+1 uzlasmada SAT, t+5 uzlasmada kapat (vade > t+5), XU100 hedge
V=pd.read_parquet(f'{D}/viop_panel.parquet')
V=V[V.segment=='SSF'][['date','und','expiry','settle','close','low','prev_settle','trades','value_tl']]; V['und']=V.und.astype(str)
E=B[B.viop47&B.feas&(B.date>='2020-03-13')].copy()
a=E[['sym','date','date_1','date_5']].rename(columns={'sym':'und'})
m1=a.merge(V.rename(columns={'date':'date_1'}),on=['und','date_1'])
m1=m1[m1.expiry>m1.date_5].sort_values('expiry').drop_duplicates(['und','date'])
m5=V.rename(columns={'date':'date_5','settle':'settle5','close':'close5','trades':'tr5'})[['und','date_5','expiry','settle5','close5','tr5']]
m=m1.merge(m5,on=['und','date_5','expiry'])
m=m.rename(columns={'und':'sym'}).merge(E[['sym','date','x2_5','tk','s','crowd','year']],on=['sym','date'])
m=m[(m.settle>0)&(m.settle5>0)]
m['f_lock1']=m.close<=m.prev_settle*0.9005+0.011
m['sf']=-(m.settle5/m.settle-1-m.x2_5)
print(f'\nVADELI BC short (t+1 uzlasma -> t+5 uzlasma, XU100 hedge) n {len(m)}, t+1 vadeli taban kilit orani {m.f_lock1.mean():.3f}, t+1 islem sayisi medyan {m.trades.median()}')
mm=m[~m.f_lock1]
for lab,sub in [('tumu',mm),('2020',mm[mm.year==2020]),('2021-23',mm[(mm.year>=2021)&(mm.year<=2023)]),('2024-26',mm[mm.year>=2024]),('kalabalik<5',mm[mm.crowd<5]),('kalabalik>=5',mm[mm.crowd>=5])]:
    for c,cl in [(19e-4,'@19'),(None,'@19+tik')]:
        x=sub.sf-(19e-4 if c else 19e-4+sub.tk)
        r=summ(sub.assign(net=x),'net')
        print(f'  {lab:12s} {cl:8s} trade {r["trade_bps"]:7.1f} (t {r["trade_t"]:5.2f}) day {r["day_bps"]:7.1f} (t {r["day_t"]:5.2f}) med {r["med_bps"]:7.1f} n {r["n"]}')
print('  spot ayni olaylar @19 trade',round((mm.s.mean()-19e-4)*1e4,1))
