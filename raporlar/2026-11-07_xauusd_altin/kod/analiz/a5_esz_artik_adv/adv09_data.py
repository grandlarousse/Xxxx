from adv_lib import *
vp=load_viop(); sp=load_spot()
d=pd.read_parquet(f"{OUT}/c1_mine.parquet")
stale=(vp.v_ret==0); print("v_ret==0 days", stale.sum(), " v_volume<=5:", (vp.v_volume<=5).sum(), " v_volume==0:", (vp.v_volume==0).sum())
# settlement vs spot 15:10 approx: compare v_settle with xau_p15 basis jump
basis=np.log(vp.v_settle/vp.xau_p15); jb=basis.diff()
print("basis daily change abs>0.5%:", (jb.abs()>0.005).sum(), "dates:", list(jb[jb.abs()>0.005].index.date)[:20])
# are C1 trade days / next 3 days affected by stale or basis jumps
c1d=d.c1.dropna().index
bad=set(jb[jb.abs()>0.005].index)|set(vp.index[stale])
aff=[t for t in c1d if any(vp.index[min(vp.index.get_loc(t)+j,len(vp)-1)] in bad for j in range(0,4))]
print("C1 trades touching basis jump/stale:", len(aff), aff[:10])
Y3=fwd(vp.v_ret,3)
c=d.c1.copy(); c[c.index.isin(aff)]=np.nan
print("C1 excl affected:", st(c,Y3,3))
# compare VIOP fwd3 vs spot skip3 on C1 days
sig=pd.read_parquet(f"{S}/out/a5_esz_artik/signals_spot.parquet")
z=pd.concat([Y3.rename("v"),sig.skip3.reindex(vp.index).rename("s")],axis=1).loc[c1d].dropna(); print("corr viop fwd3 vs spot skip3 on C1 days", z.corr().iloc[0,1].round(3), len(z))
# DST check: does effect differ between US summer/winter time (12:30 vs 13:30 UTC data releases)
idx=d.c1.dropna().index
from zoneinfo import ZoneInfo
dst=pd.Series([bool(pd.Timestamp(t).replace(hour=12).tz_localize("UTC").tz_convert(ZoneInfo("America/New_York")).dst()) for t in d.index],index=d.index)
for nm,m in [("US summer (EDT)",dst),("US winter (EST)",~dst)]:
    print(nm, st(d.c1.where(m),Y3,3))
