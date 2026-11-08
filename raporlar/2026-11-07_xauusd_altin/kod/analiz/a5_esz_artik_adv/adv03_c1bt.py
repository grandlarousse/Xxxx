from adv_lib import *
import statsmodels.api as sm
vp=load_viop(); d=pd.read_parquet(f"{OUT}/c1_mine.parquet")
r=vp.v_ret; Y3=fwd(r,3)
c1=d.c1; pos=np.sign(c1).fillna(0)
tr=pd.DataFrame(dict(s=pos[pos!=0], y=Y3[pos!=0])).dropna()
tr["g"]=tr.s*tr.y
mu_all=r.mean()*3; mu_is=r[r.index<=IS_END].mean()*3; mu_oos=r[r.index>IS_END].mean()*3
print("drift 3d bps all/is/oos", round(mu_all*1e4,1), round(mu_is*1e4,1), round(mu_oos*1e4,1))
def trade_stats(T, cost_bps, mu=None, label=""):
    gg=T.g - cost_bps/1e4
    if mu is not None: gg=T.s*(T.y-mu) - cost_bps/1e4
    # NW t on trade series (overlap within 3 days among consecutive signals)
    m=sm.OLS(gg.values, np.ones(len(gg))).fit(cov_type="HAC",cov_kwds={"maxlags":3})
    return dict(lbl=label,n=len(gg),mean_bps=round(gg.mean()*1e4,1),t=round(m.tvalues[0],2),hit=round((gg>0).mean(),3))
out=[]
for per,msk in [("full",tr.index>=tr.index.min()),("is",tr.index<=IS_END),("oos",tr.index>IS_END)]:
    T=tr[msk]; mu={"full":mu_all,"is":mu_is,"oos":mu_oos}[per]
    for cost in (0,5,10):
        out.append(dict(per=per,cost=cost,**trade_stats(T,cost,label="raw")))
    out.append(dict(per=per,cost=5,**trade_stats(T,5,mu,label="demeaned")))
    for side,sm_ in [("long",T.s>0),("short",T.s<0)]:
        out.append(dict(per=per,cost=5,**trade_stats(T[sm_],5,label=side)))
        out.append(dict(per=per,cost=5,**trade_stats(T[sm_],5,mu,label=side+"_dm")))
O=pd.DataFrame(out); print(O.to_string())
# concentration: drop top-k trades
g=tr.g.sort_values(ascending=False)
for k in (0,3,5,10):
    rest=tr.drop(g.index[:k]); m=sm.OLS(rest.g.values,np.ones(len(rest))).fit(cov_type="HAC",cov_kwds={"maxlags":3})
    print(f"drop top{k}: mean {rest.g.mean()*1e4:.1f} bps t {m.tvalues[0]:.2f}")
# portfolio backtest (lib) 5/10 bps OOS, plus excl Mar2020 & Jan-Feb2026
for nm,rr in [("all",r.fillna(0))]:
    for per,msk in [("full",slice(None)),("is",r.index<=IS_END),("oos",r.index>IS_END)]:
        rr_=rr[msk] if not isinstance(msk,slice) else rr
        for cost in (5,10):
            b=backtest(pos.reindex(rr_.index),rr_,3,cost); bd=backtest(pos.reindex(rr_.index),rr_,3,cost,demean=True)
            print(per,cost,"SR",round(b["sharpe"],2),"t",round(b["t_daily"],2),"SRdm",round(bd["sharpe"],2),"ann%",round(b["ann_ret"]*100,2))
# rank IC excluding Mar 2020 and the 2026 crash, and excluding all of 2020
Yv=Y3
from adv_lib import st
ex=((c1.index>="2020-03-01")&(c1.index<="2020-04-30"))|((c1.index>="2026-01-01")&(c1.index<="2026-03-31"))
print("ex Mar-Apr2020 & Q1 2026:", st(c1.where(~ex),Yv,3))
print("2020 only:", sub_ic(c1,Yv,3,{"2020":("2020-01-01","2020-12-31"),"2020ex MarApr":("2020-05-01","2020-12-31")}))
# yearly trade P&L
tr["yr"]=tr.index.year; print(tr.groupby("yr").agg(n=("g","size"),mean_bps=("g",lambda x: round(x.mean()*1e4,1)),hit=("g",lambda x: round((x>0).mean(),2))))
