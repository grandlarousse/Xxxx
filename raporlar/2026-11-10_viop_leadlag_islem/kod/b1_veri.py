import sys, requests, time, pandas as pd
V=sys.argv[1]; S=requests.Session(); S.headers["User-Agent"]="Mozilla/5.0"
def get(sym, prm):
    for a in range(4):
        r=S.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}",params=prm,timeout=40)
        if r.status_code==200:
            res=r.json()["chart"]["result"][0]; q=res["indicators"]["quote"][0]
            ad=(res["indicators"].get("adjclose") or [{}])[0].get("adjclose")
            ix=pd.to_datetime(res["timestamp"],unit="s",utc=True)
            df=pd.DataFrame({"o":q["open"],"h":q["high"],"l":q["low"],"c":q["close"],"adj":ad if ad else q["close"],"v":q["volume"]},index=ix).dropna(subset=["c"])
            return df,res["meta"].get("exchangeTimezoneName")
        time.sleep(3*(a+1))
    return None,None
d,tz=get("AKGRT.IS",{"period1":1388534400,"period2":int(time.time())+86400,"interval":"1d"})
if d is not None:
    d.to_parquet(f"{V}/raw/ek_b1/AKGRT.IS_daily.parquet")
    o=pd.DataFrame({"sym":"AKGRT.IS","date":d.index.tz_convert(tz).tz_localize(None).normalize(),"ts_utc":d.index,"o":d.o.values,"h":d.h.values,"l":d.l.values,"c":d.c.values,"adj":d.adj.values,"v":d.v.values})
    o=o[~o.date.duplicated(keep="last")]; o.to_parquet(f"{V}/panel/ek_b1_spot_AKGRT.parquet"); print("AKGRT",len(o),o.date.min())
else: print("AKGRT yok")
h,_=get("SI=F",{"range":"730d","interval":"1h","includePrePost":"false"})
if h is not None:
    h.to_parquet(f"{V}/raw/ek_b1/SI=F_h1.parquet")
    o=pd.DataFrame({"sym":"SI=F","ts_utc":h.index,"o":h.o.values,"h":h.h.values,"l":h.l.values,"c":h.c.values,"v":h.v.values}); o.to_parquet(f"{V}/panel/ek_b1_saatlik_SI.parquet"); print("SI",len(o),o.ts_utc.min())
else: print("SI yok")
