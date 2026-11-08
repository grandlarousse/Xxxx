"""BIST altın BYF'leri: Yahoo saatlik/5dk JSON -> parquet (indirme dizini dl_bist_byf, güvenilmez veri olarak yalnız JSON okunur)."""
import json, sys, pandas as pd, numpy as np
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
DL = f"{S}/dl_bist_byf"; OUT = f"{S}/out/e3_etf_akis_prim"
for t in ["GLDTR.IS", "ZGOLD.IS", "ISGLK.IS", "GMSTR.IS"]:
    for iv in ["1h", "5m"]:
        j = json.load(open(f"{DL}/{t}_{iv}.json"))["chart"]["result"][0]
        q = j["indicators"]["quote"][0]
        df = pd.DataFrame({k: q[k] for k in ["open", "high", "low", "close", "volume"]}, index=pd.to_datetime(j["timestamp"], unit="s", utc=True))
        df.index.name = "ts_utc"; df = df.dropna(subset=["close"])
        df.to_parquet(f"{OUT}/bist_{t.split('.')[0]}_{iv}.parquet")
        print(t, iv, len(df), df.index[0], df.index[-1], df.index.minute.unique()[:5].tolist(), sorted(df.index.hour.unique().tolist()))
