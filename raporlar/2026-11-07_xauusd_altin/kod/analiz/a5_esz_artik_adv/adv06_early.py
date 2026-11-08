from adv_lib import *
sp=load_spot(); vp=load_viop(); days=sp.index
sig=pd.read_parquet(f"{S}/out/a5_esz_artik/signals_spot.parquet")
skip3=sig.skip3; sf3=sig.sfwd3; Y3=fwd(vp.v_ret,3)
g=np.log(sp.xau_p15/sp.xau_p12)
d=pd.read_parquet(f"{OUT}/c1_mine.parquet")
def proxy(facs,W=60,q=0.8,start=12):
    gg=g if start==12 else np.log(sp.xau_p15/hsnap("XAUUSD",start,days))
    X=pd.DataFrame({k:np.log(hsnap(SYM[k],15,days)/hsnap(SYM[k],start,days)) for k in facs})
    rr=roll_ols(gg,X,W); e=rr.e/rr.sig; f=(rr.fit/rr.sig).abs()
    thr=f.expanding(120).quantile(q).shift(1)   # past-only threshold
    return e.where(f>thr), e, f
out=[]
for facs in [("EURUSD","USDJPY","SPX"),("EURUSD","SPX"),("USDJPY","SPX"),("DXY","SPX"),("DXY","TBOND","SPX")]:
    c,e,f=proxy(facs)
    for nm,(a,b) in {"pre 2016-01..2019-07":("2016-01-01","2019-07-31"),"pre 2016-01..2017-12":("2016-01-01","2017-12-31"),"C1 period 2019-08..2021":("2019-08-01","2021-12-31"),"OOS 2022+":("2022-01-01","2026-12-31")}.items():
        m=(c.index>=a)&(c.index<=b)
        r1=ic(c[m],skip3[m],5); r2=ic(c[m],sf3[m],5)
        cv=c.reindex(vp.index); mv=(cv.index>=a)&(cv.index<=b); r3=ic(cv[mv],Y3[mv],5)
        out.append(dict(facs="+".join(facs),period=nm,n=r1["n"],ic_skip=round(r1["ic"],3),t_skip=round(r1["t"],2),t_spot=round(r2["t"],2),n_viop=r3["n"],ic_viop=round(r3["ic"],3),t_viop=round(r3["t"],2)))
    if facs==("DXY","TBOND","SPX"):
        print("expanding-thr version vs C1 overlap:", (c.reindex(vp.index).notna() & d.c1.notna()).sum(), "of", d.c1.notna().sum(), c.reindex(vp.index).notna().sum())
O=pd.DataFrame(out); pd.set_option("display.width",250); print(O.to_string())
O.to_csv(f"{OUT}/c1_early_proxy.csv",index=False)
