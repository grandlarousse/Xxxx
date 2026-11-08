"""BIST BYF Yahoo JSON'larını bağımsız ayrıştır (yalnız JSON okunur)."""
import json, pandas as pd, numpy as np
from rc import S, OUT
for t in ["GLDTR.IS", "ZGOLD.IS", "ISGLK.IS"]:
    for iv in ["1h", "5m"]:
        j = json.load(open(f"{S}/dl_bist_byf/{t}_{iv}.json"))["chart"]["result"][0]
        meta = j["meta"]
        q = j["indicators"]["quote"][0]
        df = pd.DataFrame({k: q[k] for k in ["open", "high", "low", "close", "volume"]}, index=pd.to_datetime(j["timestamp"], unit="s", utc=True)).dropna(subset=["close"])
        df.to_parquet(f"{OUT}/bist_{t.split('.')[0]}_{iv}.parquet")
        hm = pd.Series(df.index.strftime("%H:%M")).value_counts().sort_index()
        print(t, iv, len(df), df.index[0], df.index[-1], "| tz:", meta.get("exchangeTimezoneName"), meta.get("gmtoffset"), "| period:", meta.get("currentTradingPeriod", {}).get("regular"))
        print("   bar başlangıç saatleri (UTC):", hm.to_dict() if iv == "1h" else dict(list(hm.items())[:3] + list(hm.items())[-4:]))
