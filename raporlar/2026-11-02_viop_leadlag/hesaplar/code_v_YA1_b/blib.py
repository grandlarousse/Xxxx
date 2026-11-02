import numpy as np, pandas as pd
OUT='/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_YA1_b'
D='/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data'

def tick(p):
    p=np.asarray(p,float)
    return np.select([p<20,p<50,p<100,p<250,p<500,p<1000,p<2500],[0.01,0.02,0.05,0.10,0.25,0.50,1.0],2.5)

def cl_t(x,g):
    """ortalama ve tarih-kumelemeli t"""
    x=np.asarray(x,float); g=np.asarray(g); m=np.isfinite(x); x=x[m]; g=g[m]
    n=len(x)
    if n<3: return np.nan,np.nan,n
    mu=x.mean(); e=x-mu
    s=pd.Series(e).groupby(g).sum().values
    G=len(s)
    v=(s**2).sum()/n**2*G/(G-1) if G>1 else np.nan
    return mu, mu/np.sqrt(v) if v>0 else np.nan, n

def nw_t(x,L=5):
    x=np.asarray(x,float); x=x[np.isfinite(x)]; n=len(x)
    if n<5: return np.nan,np.nan,n
    mu=x.mean(); e=x-mu; g0=(e@e)/n; s=g0
    for l in range(1,L+1):
        s+=2*(1-l/(L+1))*(e[l:]@e[:-l])/n
    return mu, mu/np.sqrt(s/n), n

def summ(df,col,date='date_1',bps=True):
    k=1e4 if bps else 1
    m,t,n=cl_t(df[col],df[date])
    dm=df.groupby(date)[col].mean()
    md,td,nd=nw_t(dm.sort_index().values)
    return dict(n=n,days=nd,trade_bps=round(m*k,1),trade_t=round(t,2),day_bps=round(md*k,1),day_t=round(td,2),
                med_bps=round(np.nanmedian(df[col])*k,1),hit=round((df[col]>0).mean(),3))
