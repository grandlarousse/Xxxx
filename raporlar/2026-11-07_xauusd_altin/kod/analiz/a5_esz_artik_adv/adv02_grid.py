from adv_lib import *
exec(open("adv01_c1.py").read().split("# independent recompute of C1")[0].split("from adv_lib import *")[1])
import itertools
def build(start,W,facs,end=15):
    if end==15 and start in (7,12,13,14,0): g=np.log(sp.xau_p15/sp[f"xau_p{start:02d}"])
    else: g=np.log(hsnap("XAUUSD",end,days)/hsnap("XAUUSD",start,days))
    X=pd.DataFrame({k:np.log(hsnap(SYM[k],end,days)/hsnap(SYM[k],start,days)) for k in facs})
    rr=roll_ols(g,X,W); return V(rr.e/rr.sig), V(rr.fit/rr.sig)
rows=[]
cache={}
for start in (10,11,12,13,14):
    for W in (40,60,90,120,250):
        e,f=build(start,W,("DXY","TBOND","SPX")); cache[(start,W)]=(e,f)
        for q in (0.6,0.7,0.75,0.8,0.85,0.9):
            thr=f.abs()[f.index<=IS_END].quantile(q); c=e.where(f.abs()>thr)
            for h in (1,3,5):
                r=st(c,Y[h],h); rows.append(dict(start=start,W=W,q=q,h=h,**r))
G=pd.DataFrame(rows); G.to_csv(f"{OUT}/c1_neighbors.csv",index=False)
pd.set_option("display.width",250)
for h in (3,1,5):
    print(f"\n=== h{h} t_full (rows start, cols W) at q=0.8"); print(G[(G.h==h)&(G.q==0.8)].pivot(index="start",columns="W",values="t").round(2))
    print(f"=== h{h} t_oos q=0.8"); print(G[(G.h==h)&(G.q==0.8)].pivot(index="start",columns="W",values="t_oos").round(2))
print("\n=== h3 start=12: t by W x q"); print(G[(G.h==3)&(G.start==12)].pivot(index="W",columns="q",values="t").round(2))
print("=== h3 start=12: t_oos by W x q"); print(G[(G.h==3)&(G.start==12)].pivot(index="W",columns="q",values="t_oos").round(2))
print("=== h3 start=12: t_is by W x q"); print(G[(G.h==3)&(G.start==12)].pivot(index="W",columns="q",values="t_is").round(2))
h3=G[G.h==3]; print("\nh3 all", len(h3), "frac t>2", (h3.t>2).mean().round(2), "frac t_oos>1.96", (h3.t_oos>1.96).mean().round(2), "median t", h3.t.median().round(2), "median t_oos", h3.t_oos.median().round(2))
