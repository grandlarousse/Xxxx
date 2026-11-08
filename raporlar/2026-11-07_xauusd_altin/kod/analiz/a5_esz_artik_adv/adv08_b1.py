from adv_lib import *
import statsmodels.api as sm
sp=load_spot(); vp=load_viop(); days=sp.index; V=lambda s:s.reindex(vp.index)
sig=pd.read_parquet(f"{S}/out/a5_esz_artik/signals_spot.parquet")
r=vp.v_ret; Y={h:fwd(r,h) for h in (1,2,3,5)}
x=V(sig.GSRD_k5)
print("B1 repro", st(x,Y[1],1)); print("B1 pearson", st(x,Y[1],1,"pearson"))
PER2={"2017-19":("2017-01-01","2019-12-31"),"2020-21":("2020-01-01","2021-12-31"),"2022-23":("2022-01-01","2023-12-31"),"2024-26":("2024-01-01","2026-12-31")}
print("B1 subper", sub_ic(x,Y[1],1,PER2))
# independent recompute
lr=np.log(sp.xau_p15/sp.dk_XAGUSD_p15); dlr=lr.diff(); sd=dlr.rolling(120,min_periods=96).std().shift(1)
rows=[]
for k in (1,2,3,4,5,6,7,8,10,15,20):
    z=V(dlr.rolling(k).sum()/(sd*np.sqrt(k)))
    if k==5: print("indep vs analyst corr", z.corr(x).round(6))
    for h in (1,2,3,5):
        s_=st(z,Y[h],h); rows.append(dict(k=k,h=h,t=s_["t"],t_is=s_["t_is"],t_oos=s_["t_oos"]))
R=pd.DataFrame(rows); pd.set_option("display.width",250)
for c in ("t","t_is","t_oos"): print(c); print(R.pivot(index="k",columns="h",values=c))
# backtests sign rule h1
def bt(pos,h=1,cost=5,per="oos",demean=False):
    rr=r.fillna(0); msk={"full":rr.index>=rr.index.min(),"is":rr.index<=IS_END,"oos":rr.index>IS_END}[per]
    b=backtest(pos[msk],rr[msk],h,cost,demean=demean); return round(b["sharpe"],2),round(b["t_daily"],2),round(b["ann_ret"]*100,1)
pos=-np.sign(x).fillna(0)
for per in ("is","oos","full"):
    print(per,"5bps",bt(pos,per=per),"10bps",bt(pos,cost=10,per=per),"dm",bt(pos,per=per,demean=True),"long",bt(pos.clip(lower=0),per=per,demean=True),"short",bt(pos.clip(upper=0),per=per,demean=True))
# B&H OOS for reference
print("BH oos", bt(pd.Series(1.0,index=r.index),cost=0))
# yearly pnl of B1
rr=r.fillna(0); b=backtest(pos,rr,1,5); pnl=b["pnl"]; print((pnl.groupby(pnl.index.year).sum()*100).round(1).to_dict())
print("demeaned yearly", ((backtest(pos,rr,1,5,demean=True)["pnl"]).groupby(pnl.index.year).sum()*100).round(1).to_dict())
# drift-trap check: correlation of signal with trend; long fraction OOS
print("OOS long frac", (pos[pos.index>IS_END]>0).mean().round(3), " IS long frac",(pos[pos.index<=IS_END]>0).mean().round(3))
# control for gold's own 5d return (time-series momentum) and silver 5d
g5=V(np.log(sp.xau_p15).diff().rolling(5).sum()); s5=V(np.log(sp.dk_XAGUSD_p15).diff().rolling(5).sum())
d=pd.concat([Y[1].rename("y"),x.rename("x"),g5.rename("g5"),s5.rename("s5")],axis=1).dropna()
for sub,nm in [(d,"full"),(d[d.index>IS_END],"oos")]:
    Z=(sub-sub.mean())/sub.std(); m=sm.OLS(Z.y,sm.add_constant(Z[["x","g5"]])).fit(cov_type="HAC",cov_kwds={"maxlags":5})
    print(nm,"y~x+g5 t",m.tvalues.round(2).to_dict())
    m=sm.OLS(Z.y,sm.add_constant(Z[["g5","s5"]])).fit(cov_type="HAC",cov_kwds={"maxlags":5}); print(nm,"y~g5+s5 t",m.tvalues.round(2).to_dict())
# own 5-day gold return as predictor alone (OOS)
print("gold5 alone h1", st(g5,Y[1],1)); print("silver5 alone h1", st(s5,Y[1],1))
# winsorize / exclude extremes
ext=((x.index>="2020-03-01")&(x.index<="2020-03-31"))|((x.index>="2026-01-01")&(x.index<="2026-02-28"))|((x.index>="2021-01-25")&(x.index<="2021-02-15"))
print("B1 ex extremes", st(x.where(~ext),Y[1],1))
