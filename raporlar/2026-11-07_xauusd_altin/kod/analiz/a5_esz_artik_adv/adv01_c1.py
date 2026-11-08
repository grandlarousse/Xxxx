from adv_lib import *
sp=load_spot(); vp=load_viop(); days=sp.index
sig=pd.read_parquet(f"{S}/out/a5_esz_artik/signals_spot.parquet")
Y={h:fwd(vp.v_ret,h) for h in (1,2,3,4,5)}
assert np.allclose(Y[3].dropna(), vp.fwd3.reindex(Y[3].dropna().index), equal_nan=True)
V=lambda s: s.reindex(vp.index)
# independent recompute of C1
def c1_signal(start=12, W=60, facs=("DXY","TBOND","SPX"), end=15, q=0.8, return_parts=False):
    g=np.log(hsnap("XAUUSD",end,days)/hsnap("XAUUSD",start,days)) if end!=15 or start not in (12,7) else np.log(sp.xau_p15/sp[f"xau_p{start:02d}"])
    X=pd.DataFrame({k:np.log(hsnap(SYM[k],end,days)/hsnap(SYM[k],start,days)) for k in facs})
    rr=roll_ols(g,X,W); e=rr.e/rr.sig; f=rr.fit/rr.sig
    fv=V(f); thr=fv.abs()[fv.index<=IS_END].quantile(q)
    c=V(e).where(fv.abs()>thr)
    if return_parts: return c, V(e), fv, thr, V(g)
    return c
c1,e,f,thr,g12=c1_signal(return_parts=True)
print("thr",round(thr,3)," n",c1.notna().sum(), " first", c1.dropna().index.min())
a=V(sig.I12_MACRO3_W60); print("analyst vs mine e corr",a.corr(e).round(6), "max abs diff", (a-e).abs().max())
print("C1 h3 repro:", st(c1,Y[3],3))
print("C1 h3 pearson:", st(c1,Y[3],3,"pearson"))
# subperiods
print("subperiods h3:", sub_ic(c1,Y[3],3,PER))
for h in (1,2,3,4,5): print(f" h{h}", st(c1,Y[h],h))
c1.to_frame("c1").assign(e=e,f=f,g12=g12).to_parquet(f"{OUT}/c1_mine.parquet")
