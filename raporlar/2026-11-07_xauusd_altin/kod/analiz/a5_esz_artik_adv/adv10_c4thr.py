from adv_lib import *
sp=load_spot(); vp=load_viop(); days=sp.index; V=lambda s:s.reindex(vp.index)
sig=pd.read_parquet(f"{S}/out/a5_esz_artik/signals_spot.parquet"); skip1=sig.skip1; Y1=fwd(vp.v_ret,1)
e07=V(sig.I07_MACRO3_W60)
P3={"2019-21":("2019-01-01","2021-12-31"),"2022-23":("2022-01-01","2023-12-31"),"2024-26":("2024-01-01","2026-12-31")}
for thr in (0.5,1.0,1.5): print("C4 |e|>",thr, sub_ic(e07.where(e07.abs()>thr),Y1,1,P3))
for facs in [("EURUSD","SPX"),("DXY","SPX"),("EURUSD","USDJPY","SPX"),("SPX",)]:
    g=np.log(sp.xau_p15/sp.xau_p07); X=pd.DataFrame({k:np.log(hsnap(SYM[k],15,days)/hsnap(SYM[k],7,days)) for k in facs})
    rr=roll_ols(g,X,60); x=(rr.e/rr.sig); xc=x.where(x.abs()>1)
    out=[]
    for nm,(a,b) in {"pre..2019-07":("2016-01-01","2019-07-31"),"2019-08..2021":("2019-08-01","2021-12-31"),"2022+":("2022-01-01","2026-12-31")}.items():
        mm=(xc.index>=a)&(xc.index<=b); r1=ic(xc[mm],skip1[mm],5); xv=V(xc); mv=(xv.index>=a)&(xv.index<=b); r3=ic(xv[mv],Y1[mv],5)
        out.append(f"{nm}: skip t {r1['t']:.2f} (n{r1['n']}) viop t {r3['t']:.2f} (n{r3['n']})")
    print("I07|e|>1 proxy","+".join(facs)," | ".join(out))
# trade-level t for thr1 OOS (h1) with 5/10 bps
pos=np.sign(e07).where(e07.abs()>1,0).fillna(0); tr=(pos*Y1)[pos!=0].dropna()
for per,m in [("is",tr.index<=IS_END),("oos",tr.index>IS_END)]:
    t_=tr[m]; 
    for c in (5,10): g=t_-c/1e4; print(per,c,"bps n",len(g),"mean bps",round(g.mean()*1e4,1),"t",round(g.mean()/g.std()*np.sqrt(len(g)),2))
