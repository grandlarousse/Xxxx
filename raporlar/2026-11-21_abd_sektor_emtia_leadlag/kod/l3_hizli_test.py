import sys; sys.path.insert(0,'/home/user/Xxxx/raporlar/2026-11-21_abd_sektor_emtia_leadlag/kod')
import numpy as np, pandas as pd, ortak
vix=ortak.oku('^VIX')['close']
def rsi2(c):
    d=c.diff(); u=d.clip(lower=0); g=-d.clip(upper=0)
    au=u.ewm(alpha=1/2,adjust=False).mean(); ag=g.ewm(alpha=1/2,adjust=False).mean()
    return 100-100/(1+au/ag)
def stats(x):
    x=x.dropna(); n=len(x)
    if n<20: return f"n={n:4d}      -"
    return f"n={n:4d} {x.mean()*1e4:6.1f}bp t={x.mean()/x.std()*np.sqrt(n):4.1f}"
per=[('2005-14','2005','2014'),('2015-23','2015','2023'),('2024-26','2024','2026')]
syms=sys.argv[1].split(',')
rows=[]
for s in syms:
    d=ortak.oku(s); d=d[d.index>='2004-06-01']
    c=d['adjclose']; rng=(d['ah']-d['al'])
    ibs=((c-d['al'])/rng).where(rng>0)
    r1=c.shift(-1)/c-1; on=d['ao'].shift(-1)/c-1; intra=c.shift(-1)/d['ao'].shift(-1)-1
    r3=c.shift(-3)/c-1
    sig={'IBS<0.2':ibs<0.2,'RSI2<10':rsi2(c)<10,'3down':(c.diff()<0)&(c.diff().shift(1)<0)&(c.diff().shift(2)<0),
         'r5<-3%':(c/c.shift(5)-1)<-0.03,'IBS<0.2&VIX>25':(ibs<0.2)&(vix.reindex(d.index)>25),'ALL':pd.Series(True,index=d.index)}
    for k,m in sig.items():
        for p,a,b in per:
            mm=m[a:b]; idx=mm[mm].index
            rows.append((s,k,p,stats(r1[idx]),stats(on[idx]),stats(intra[idx]),stats(r3[idx])))
for r in rows: print(f"{r[0]:5s} {r[1]:15s} {r[2]} | c2c1 {r[3]} | ON {r[4]} | ID {r[5]} | c2c3 {r[6]}")
