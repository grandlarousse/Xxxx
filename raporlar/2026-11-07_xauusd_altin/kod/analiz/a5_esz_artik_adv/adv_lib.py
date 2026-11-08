import sys, numpy as np, pandas as pd
S="/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
sys.path.insert(0,f"{S}/code")
from lib_altin import load_spot, load_viop, hourly, split_stats, ic, IS_END, backtest, fwd, bh_fdr
OUT=f"{S}/out/a5_esz_artik_adv"
SYM=dict(DXY="DOLLARIDXUSD",TBOND="USTBONDTRUSD",SPX="USA500IDXUSD",XAG="XAGUSD",USDJPY="USDJPY",EURUSD="EURUSD",USDCNH="USDCNH")
_H={}
def hsnap(sym, hour, days):
    """price at hour:00 UTC = close of bar starting hour-1 (exact bar only)"""
    if sym not in _H:
        h=hourly(sym); h.index=h.index.tz_convert(None); _H[sym]=h["c"]
    c=_H[sym]; s=c[c.index.hour==(hour-1)%24].copy(); s.index=s.index.normalize()
    if hour==0: s.index=s.index+pd.Timedelta(days=1)
    return s.reindex(days)
def roll_ols(y, X, W, minp=None):
    minp=minp or int(0.8*W); X=pd.DataFrame(X); Y=y.values.astype(float); Xv=X.values.astype(float)
    n,p=Xv.shape; ok=np.isfinite(Y)&np.isfinite(Xv).all(1)
    e=np.full(n,np.nan); fit=np.full(n,np.nan); sg=np.full(n,np.nan)
    okidx=np.where(ok)[0]
    for t in range(n):
        if not ok[t]: continue
        idx=okidx[(okidx>=t-W)&(okidx<t)]
        if len(idx)<minp: continue
        A=np.column_stack([np.ones(len(idx)),Xv[idx]]); b=np.linalg.lstsq(A,Y[idx],rcond=None)[0]
        r=Y[idx]-A@b; sg[t]=r.std(ddof=p+1); fit[t]=Xv[t]@b[1:]; e[t]=Y[t]-b[0]-fit[t]
    return pd.DataFrame(dict(e=e,fit=fit,sig=sg),index=y.index)
def st(x,y,h,method="spearman"):
    r=split_stats(x,y,h,method); return {k:(round(v,3) if isinstance(v,float) else v) for k,v in r.items() if k!="by_year"}
def sub_ic(x,y,h,periods):
    out={}
    for nm,(a,b) in periods.items():
        m=(x.index>=a)&(x.index<=b); r=ic(x[m],y[m],max(h,5)); out[nm]=(round(r["ic"],3),round(r["t"],2),r["n"])
    return out
PER={"2019-21":("2017-01-01","2021-12-31"),"2020-21":("2020-01-01","2021-12-31"),"2019":("2019-01-01","2019-12-31"),"2022-23":("2022-01-01","2023-12-31"),"2024-26":("2024-01-01","2026-12-31")}
