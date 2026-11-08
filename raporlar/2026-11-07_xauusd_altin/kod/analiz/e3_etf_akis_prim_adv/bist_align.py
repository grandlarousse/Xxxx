"""BIST BYF Yahoo saatlik bar zaman hizası kalibrasyonu: BYF bar getirisi ile spot gram altın getirisinin farklı kaydırmalarda korelasyonu.
'has14' (14:30 barı olan gün) ve olmayan günler ayrı."""
import pandas as pd, numpy as np
S="/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"; P=f"{S}/panel"; O=f"{S}/out/e3_etf_akis_prim"
def dk(sym):
    x=pd.read_parquet(f"{P}/duka/{sym}.parquet")["c"]; x.index=x.index+pd.Timedelta(hours=1); return x[~x.index.duplicated()]
xau=dk("XAUUSD"); usd=dk("USDTRY")
g=np.log(xau*usd.reindex(xau.index).ffill()/31.1035)
for t in ["GLDTR","ZGOLD"]:
    h=pd.read_parquet(f"{O}/bist_{t}_1h.parquet")
    h["day"]=h.index.normalize(); has=h.groupby("day").apply(lambda q:(q.index.hour==14).any()); h["has"]=h.day.map(has)
    h=h[h.index< "2026-10-30"]
    h["r"]=np.log(h.close).groupby(h.day).diff()
    out={}
    for k in [-1,0,1,2]:
        # gold window [L-0.5+k, L+0.5+k] where L = bar label (start)
        a=h.index-pd.Timedelta(minutes=30)+pd.Timedelta(hours=k); b=a+pd.Timedelta(hours=1)
        gr=pd.Series(g.reindex(b).values-g.reindex(a).values,index=h.index)
        for hs in [True,False]:
            m=(h.has==hs)&h.r.notna()&gr.notna()
            out[(hs,k)]=round(np.corrcoef(h.r[m],gr[m])[0,1],3)
    print(t,out)
    # son bar fiyatı vs gram, 'close' ile gram 14:30 / 15:00 / 15:10 arasında günlük fark varyansı (has gruplarına göre)
    close=h.groupby("day").close.last(); last_lbl=h.groupby("day").apply(lambda q:q.index[-1])
    hs_=has.reindex(close.index)
    for T in ["14:00","15:00","16:00"]:
        ts=pd.DatetimeIndex([pd.Timestamp(f"{d.date()} {T}",tz="UTC") for d in close.index])
        gg=pd.Series(g.reindex(ts).values,index=close.index)
        dv=(np.log(close)-gg).diff()
        print(t,T,"std(Δ(ln close − ln gram_T)) bps has14:",round(dv[hs_.values].std()*1e4,1)," no14:",round(dv[~hs_.values].std()*1e4,1))
