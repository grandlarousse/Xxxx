"""E3-5 saldırısı: GLDTR prim -> göreli getiri. Yahoo saatlik barlarının bir kısmında (kış dönemleri) 14:30 barı yok;
o günlerde kesim fiyatı = 'kapanış' fiyatı (aynı gözlem) -> mekanik sıçrama (bounce). Günleri ayırıp test et; ayrıca bir bar erken kesim."""
import sys; sys.path.insert(0,"/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e3_etf_akis_prim")
import pandas as pd, numpy as np
S="/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"; P=f"{S}/panel"; O=f"{S}/out/e3_etf_akis_prim"
sys.path.insert(0,f"{S}/code")
from lib_altin import ic, fwd
def dk(sym):
    x=pd.read_parquet(f"{P}/duka/{sym}.parquet")["c"]; x.index=x.index+pd.Timedelta(hours=1); return x[~x.index.duplicated()]
xau=dk("XAUUSD"); usd=dk("USDTRY")
yu=pd.read_parquet(f"{P}/yahoo_h/USDTRY_X.parquet")["close"]; yu.index=yu.index+pd.Timedelta(hours=1)
usd=usd.combine_first(yu[yu.index>usd.index.max()])
sp=pd.read_parquet(f"{P}/panel_spot.parquet"); sp.index=pd.to_datetime(sp.index)
xp={}
for H in (12,13,14,15):
    s=sp[f"xau_p{H}"]; s.index=s.index+pd.Timedelta(hours=H); s.index=s.index.tz_localize("UTC"); xp[H]=s
xau=xau.combine_first(pd.concat(xp.values()).sort_index())
def at(series, ts):
    ts=pd.DatetimeIndex(ts); fl=ts.floor("h"); ce=ts.ceil("h")
    a=series.reindex(fl).values; b=series.reindex(ce).values
    return pd.Series(np.where(fl==ce,a,np.sqrt(a*b)),index=ts)
def at_floor(series, ts):  # yalnız geçmiş tam saat (ileriye bakmasız)
    ts=pd.DatetimeIndex(ts); return pd.Series(series.reindex(ts.floor("h")).values,index=ts)
for t in ["GLDTR","ZGOLD"]:
    h1=pd.read_parquet(f"{O}/bist_{t}_1h.parquet"); h1["day"]=h1.index.normalize().tz_localize(None)
    has=h1.groupby("day").apply(lambda g:(g.index.hour==14).any())
    close=h1.groupby("day")["close"].last()
    lastbar=h1.groupby("day").apply(lambda g:g.index[-1].hour*60+g.index[-1].minute)
    close=close[lastbar>=13*60+30]; days=close.index
    ts15=pd.DatetimeIndex([pd.Timestamp(f"{dd.date()} 15:00",tz="UTC") for dd in days])
    gram15=pd.Series((at(xau,ts15)*at(usd,ts15)/31.1035).values,index=days)
    ratio=close/gram15; rmed=ratio.rolling(20,min_periods=10).median().shift(1)
    r=np.log(close).diff(); rg=np.log(gram15).diff(); rel=r-rg
    res={}
    for lbl in [13*60+30, 12*60+30, 11*60+30]:
        cb=h1[(h1.index.hour*60+h1.index.minute)<=lbl]
        cutpx=cb.groupby("day")["close"].last().reindex(days)
        ce=pd.DatetimeIndex(cb.groupby("day").apply(lambda g:g.index[-1]+pd.Timedelta(hours=1)).reindex(days))
        for gname,fn in [("interp",at),("floor",at_floor)]:
            gcut=pd.Series((fn(xau,ce)*fn(usd,ce)/31.1035).values,index=days)
            pc=np.log(cutpx/(rmed*gcut))
            y=fwd(rel,1)
            for seg,msk in [("all",slice(None)),("has14",has.reindex(days).values),("no14",~has.reindex(days).values)]:
                x_=pc[msk] if not isinstance(msk,slice) else pc; y_=y[msk] if not isinstance(msk,slice) else y
                q=ic(x_,y_,5); res[(lbl,gname,seg)]=(round(q["ic"],3),round(q["t"],2),q["n"])
            if lbl==13*60+30 and gname=="interp":
                # h5
                for seg,msk in [("all",np.ones(len(days),bool)),("has14",has.reindex(days).values),("no14",~has.reindex(days).values)]:
                    q=ic(pc[msk],fwd(rel,5)[msk],5); res[(lbl,"interp_h5",seg)]=(round(q["ic"],3),round(q["t"],2),q["n"])
                # yalnız has14 günleri ve sonraki gün de has14 (çıkış da gerçek kapanışa yakın)
                both=has.reindex(days).values & np.roll(has.reindex(days).values,-1)
                q=ic(pc[both],y[both],5); res[(lbl,gname,"has14_both")]=(round(q["ic"],3),round(q["t"],2),q["n"])
    for k,v in res.items(): print(t,k,v)
