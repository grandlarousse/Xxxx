import numpy as np, pandas as pd
from math import erf, sqrt, exp, log
exec(open('load.py').read())
Phi=lambda x:0.5*(1+erf(x/sqrt(2)))
F0=14644.0; S0=13960.9; rimp=0.279
def p_touch(b,days,sig=0.27,mu_ann=0.0,extra_var_days=1.0):
    # log-futures BM; drift = spot drift - carry decay; holiday adds variance
    s=sig/np.sqrt(252); T=days+extra_var_days
    mu=(mu_ann/252) - rimp/365*(days*365/252)/days  # per trading day approx carry decay
    mu=mu_ann/252 - rimp/252*1.45/1.0*0+ -rimp/365*1.45  # 1 trading day ~1.45 calendar days
    a=log(b/F0)
    st=s*sqrt(T)
    return Phi((-a+mu*T)/st)+exp(2*mu*a/s**2)*Phi((-a-mu*T)/st)
for b in (14900,15000,15050,15100):
    print(b, f'+{(b/F0-1)*100:.2f}%', ' 11g σ27:',round(p_touch(b,11),2),' σ22:',round(p_touch(b,11,0.22),2),' σ32:',round(p_touch(b,11,0.32),2),' | 6g(ilk hafta) σ27:',round(p_touch(b,6),2))
# Empirical: XU030 spot max high within 11 days >= barrier mapped to spot (~ +3.2% for 15,050; +2.2% for 14,900)
c=x30['c']; h=x30['h'].fillna(c)
def emp(th,N=11,start='2005-01-01',mask=None):
    idx=np.arange(len(c)-N)
    sel=[i for i in idx if c.index[i]>=pd.Timestamp(start) and (mask is None or mask.iloc[i])]
    hits=[(h.iloc[i+1:i+N+1].max()/c.iloc[i]-1)>=th for i in sel]
    return round(np.mean(hits),2), len(sel)
dd=c/c.rolling(60).max()-1; m=(dd<=-0.17)&(dd>=-0.30)&(c<c.rolling(50).mean())
for th,lab in [(0.022,'F14.900~spot+2,2%'),(0.032,'F15.050~spot+3,2%')]:
    print(lab,'koşulsuz 2005+',emp(th),' koşullu(durum) 1997+',emp(th,start='1997-01-01',mask=m),' koşullu 2005+',emp(th,mask=m))
