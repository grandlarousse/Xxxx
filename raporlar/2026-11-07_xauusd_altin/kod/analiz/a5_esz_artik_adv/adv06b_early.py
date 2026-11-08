from adv_lib import *
sp=load_spot(); vp=load_viop(); days=sp.index
sig=pd.read_parquet(f"{S}/out/a5_esz_artik/signals_spot.parquet"); skip3=sig.skip3; Y3=fwd(vp.v_ret,3)
g=np.log(sp.xau_p15/sp.xau_p12)
for facs in [("DXY","SPX"),("EURUSD","SPX"),("EURUSD","USDJPY","SPX"),("SPX",),("EURUSD",)]:
  for W in (60,120):
    X=pd.DataFrame({k:np.log(hsnap(SYM[k],15,days)/hsnap(SYM[k],12,days)) for k in facs})
    rr=roll_ols(g,X,W); e=rr.e/rr.sig; f=(rr.fit/rr.sig).abs()
    res=[]
    for nm,(a,b) in {"pre..2019-07":("2016-01-01","2019-07-31"),"2019-08..2021":("2019-08-01","2021-12-31"),"2022+":("2022-01-01","2026-12-31")}.items():
        m=(f.index>=a)&(f.index<=b); thr=f[m].quantile(0.8); c=e.where(m&(f>thr))
        r1=ic(c,skip3,5); cv=c.reindex(vp.index); r3=ic(cv,Y3,5)
        res.append(f"{nm}: skip t {r1['t']:.2f} (n{r1['n']}) viop t {r3['t']:.2f} (n{r3['n']})")
    print("+".join(facs),W," | ".join(res))
