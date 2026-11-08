"""E3-6 saldırısı (sıfır iddia): analistin denemediği 'beklenmeyen akış' (geçmiş getirilerle açıklanmayan pay değişimi, genişleyen pencere OLS),
madenci hedefleri (GDX/GDXJ), alt dönemler."""
import sys; sys.path.insert(0,"/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e3_etf_akis_prim")
from common import *
d=load_etf()
nh=pd.read_parquet(f"{P}/etf_gld_navhist.parquet"); nh.index=pd.to_datetime(nh.index)
S_=np.log(nh.shares.where(nh.shares>0)); f1=S_.diff()
nav=np.log(nh.nav); rn=nav.diff()
X=pd.concat([rn.rename("r0"),rn.shift(1).rename("r1"),rn.shift(2).rolling(4).sum().rename("r25"),rn.shift(6).rolling(15).sum().rename("r620"),f1.shift(1).rename("f_1")],axis=1)
res=pd.Series(np.nan,index=f1.index)
dd=pd.concat([f1.rename("y"),X],axis=1).dropna()
Y=dd.y.values; XX=np.column_stack([np.ones(len(dd)),dd.iloc[:,1:].values])
for i in range(500,len(dd)):
    b=np.linalg.lstsq(XX[:i],Y[:i],rcond=None)[0]; res.loc[dd.index[i]]=Y[i]-XX[i]@b
z=res/res.rolling(250,min_periods=120).std().shift(1)
def align(s, idx, lag):
    ss=s.shift(lag-1); pos=ss.index.searchsorted(idx,side="left")-1
    return pd.Series(np.where(pos>=0, ss.values[np.clip(pos,0,None)], np.nan), index=idx)
for lag in (1,2):
    A=align(z,d.index,lag)
    for tgt in ["GLD","IAU","GDX","GDXJ"]:
        r=lr(d[f"c_{tgt}"])
        for h in (1,5):
            st=split_stats(A,fwd(r,h),h)
            print(f"resid flow lag{lag} -> {tgt} h{h}: IC {st['ic']:.3f} t {st['t']:.2f} IS {st['t_is']:.2f} OOS {st['t_oos']:.2f} yrs {st['yrs_same_sign']}/{st['yrs']}")
# ham f1 -> madenciler
A=align(f1/f1.rolling(250,min_periods=120).std().shift(1),d.index,1)
for tgt in ["GDX","GDXJ"]:
    r=lr(d[f"c_{tgt}"]); st=split_stats(A,fwd(r,1),1); print(f"zf1 lag1 -> {tgt} h1: IC {st['ic']:.3f} t {st['t']:.2f} IS {st['t_is']:.2f} OOS {st['t_oos']:.2f}")
