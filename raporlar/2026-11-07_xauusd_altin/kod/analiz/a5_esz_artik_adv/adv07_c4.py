from adv_lib import *
import statsmodels.api as sm
sp=load_spot(); vp=load_viop(); days=sp.index; V=lambda s:s.reindex(vp.index)
sig=pd.read_parquet(f"{S}/out/a5_esz_artik/signals_spot.parquet")
G=pd.read_csv(f"{S}/out/a5_esz_artik/grid_viop.csv")
u=G[(G.fam=='C_intraday')&(~G.test_id.str.contains('I12c|I12F'))]; print("neg uncond:",u[u.t<0][["test_id","t"]].to_string())
r=vp.v_ret; Y={h:fwd(r,h) for h in (1,2,3,5)}
e07=V(sig.I07_MACRO3_W60)
print("C4 repro h1", st(e07,Y[1],1))
print("C4 subper h1", sub_ic(e07,Y[1],1,PER))
def bt_thr(x,thr,h=1,cost=5,per="oos",demean=False,side=None):
    pos=np.sign(x).where(x.abs()>thr,0).fillna(0)
    if side=="long": pos=pos.clip(lower=0)
    if side=="short": pos=pos.clip(upper=0)
    rr=r.fillna(0); msk={"full":rr.index>=rr.index.min(),"is":rr.index<=IS_END,"oos":rr.index>IS_END}[per]
    b=backtest(pos[msk],rr[msk],h,cost,demean=demean); return round(b["sharpe"],2), round(b["t_daily"],2)
for thr in (0,0.5,0.75,1.0,1.25,1.5,2.0):
    print(f"thr {thr}: IS {bt_thr(e07,thr,per='is')} OOS {bt_thr(e07,thr)} OOS10 {bt_thr(e07,thr,cost=10)} OOSdm {bt_thr(e07,thr,demean=True)} full {bt_thr(e07,thr,per='full')}")
print("thr1 OOS long dm", bt_thr(e07,1,demean=True,side="long"), "short dm", bt_thr(e07,1,demean=True,side="short"))
# IC on |e|>1 subset
m=e07.abs()>1; print("IC on |e07|>1 days h1", st(e07.where(m),Y[1],1))
# neighbors: start hour 6,7,8,9,10 and W 40/60/120/250
def build(start,W,facs=("DXY","TBOND","SPX")):
    g=np.log(sp.xau_p15/(sp[f"xau_p{start:02d}"] if start in (7,12,13,14) else hsnap("XAUUSD",start,days)))
    X=pd.DataFrame({k:np.log(hsnap(SYM[k],15,days)/hsnap(SYM[k],start,days)) for k in facs})
    rr=roll_ols(g,X,W); return V(rr.e/rr.sig)
rows=[]
for start in (6,7,8,9,10):
    for W in (40,60,120,250):
        x=build(start,W); s1=st(x,Y[1],1); sh=bt_thr(x,1); sh_is=bt_thr(x,1,per="is")
        rows.append(dict(start=start,W=W,t=s1["t"],t_is=s1["t_is"],t_oos=s1["t_oos"],sr_is=sh_is[0],sr_oos=sh[0],sr_oos10=bt_thr(x,1,cost=10)[0]))
R=pd.DataFrame(rows); pd.set_option("display.width",250)
for c in ("t","t_oos","sr_oos","sr_oos10"): print(c); print(R.pivot(index="start",columns="W",values=c))
R.to_csv(f"{OUT}/c4_neighbors.csv",index=False)
# early proxy 2016-01..2019-07 with EURUSD+SPX, DXY+SPX
skip1=sig.skip1
for facs in [("EURUSD","SPX"),("DXY","SPX"),("EURUSD","USDJPY","SPX")]:
    g=np.log(sp.xau_p15/sp.xau_p07); X=pd.DataFrame({k:np.log(hsnap(SYM[k],15,days)/hsnap(SYM[k],7,days)) for k in facs})
    rr=roll_ols(g,X,60); x=rr.e/rr.sig
    out=[]
    for nm,(a,b) in {"pre..2019-07":("2016-01-01","2019-07-31"),"2019-08..2021":("2019-08-01","2021-12-31"),"2022+":("2022-01-01","2026-12-31")}.items():
        mm=(x.index>=a)&(x.index<=b); r1=ic(x[mm],skip1[mm],5); xv=V(x); mv=(xv.index>=a)&(xv.index<=b); r3=ic(xv[mv],Y[1][mv],5)
        out.append(f"{nm}: skip t {r1['t']:.2f} (n{r1['n']}) viop t {r3['t']:.2f}")
    print("I07 proxy","+".join(facs)," | ".join(out))
