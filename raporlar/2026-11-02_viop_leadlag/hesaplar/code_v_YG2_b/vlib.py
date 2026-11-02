# Çalıştırma: nice -n 10 python3 w1_panel.py && w2_dataq.py && w3_core.py && w4_placebo.py && w5_lags.py && w6_robust.py && w6b_winter.py && w7_ssf_proxy.py && w8_oos_cost.py && w9_ssf_cont.py && w10_misc.py && w11_extra.py && w12_asym.py
"""v_YG2_b ortak istatistik araçları (ll.py'den bağımsız)."""
import numpy as np, pandas as pd
RES='/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_YG2_b/res'
def ols_cl(y, X, g):
    y=np.asarray(y,float); X=np.column_stack([np.ones(len(y)),np.asarray(X,float)])
    iXX=np.linalg.pinv(X.T@X); b=iXX@X.T@y; u=y-X@b
    gi=pd.factorize(np.asarray(g))[0]; G=gi.max()+1
    S=np.zeros((G,X.shape[1])); np.add.at(S,gi,X*u[:,None])
    V=iXX@(S.T@S)@iXX*G/(G-1)*(len(y)-1)/(len(y)-X.shape[1])
    se=np.sqrt(np.clip(np.diag(V),0,None)); return b, se
def demean2(df, cols, a='sym', b='date', it=20):
    Z=df[cols].copy()
    for _ in range(it):
        Z=Z-Z.groupby(df[a]).transform('mean'); Z=Z-Z.groupby(df[b]).transform('mean')
    return Z
def nw(x, L=5):
    x=pd.Series(x).dropna().values; n=len(x)
    if n<10: return np.nan,np.nan,n
    m=x.mean(); e=x-m; v=e@e/n
    for l in range(1,L+1): v+=2*(1-l/(L+1))*(e[l:]@e[:-l])/n
    return m, m/np.sqrt(v/n), n
def port(df, sig='CA', y='y', thr=0.0025, excess=False, side='both'):
    """günlük eşit ağırlıklı portföy: |sig|>thr olan hisselerde -sign(sig)*y. excess=True: y - günün kesit ortalaması (tüm hisseler)."""
    d=df[[sig,y,'date','sym']].dropna()
    if excess:
        mu=df.groupby('date')[y].transform('mean'); d=d.assign(**{y:d[y]-mu.loc[d.index]})
    d=d[d[sig].abs()>thr]
    if side=='long': d=d[d[sig]<0]
    if side=='short': d=d[d[sig]>0]
    d=d.assign(p=-np.sign(d[sig])*d[y])
    daily=d.groupby('date')['p'].mean()
    return daily, d
def summ(daily, d=None):
    m,t,n=nw(daily); return dict(bps=round(1e4*m,1), t=round(t,2), ndays=n, ntr=(len(d) if d is not None else np.nan))
