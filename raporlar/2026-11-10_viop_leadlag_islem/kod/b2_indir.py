"""b2: eksik Yahoo semboller (RB=F, HO=F, HRC=F) gunluk 2014+ ve saatlik 730g. python3 -I b2_indir.py <VERI_DIR>"""
import sys, time, requests, pandas as pd
V = sys.argv[1]; S = requests.Session(); S.headers["User-Agent"] = "Mozilla/5.0"
D, H = [], []
for sym in ["RB=F", "HO=F", "HRC=F"]:
    for kind, prm in (("d", {"period1": 1388534400, "period2": int(time.time()) + 86400, "interval": "1d"}), ("h", {"range": "730d", "interval": "1h"})):
        res = None
        for a in range(5):
            try:
                r = S.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}", params=dict(prm, includePrePost="false"), timeout=40)
                if r.status_code == 200:
                    res = (r.json()["chart"]["result"] or [None])[0]; break
                time.sleep(3)
            except Exception as e:
                time.sleep(3)
        if not res or not res.get("timestamp"): print(sym, kind, "YOK"); continue
        q = res["indicators"]["quote"][0]; ix = pd.to_datetime(res["timestamp"], unit="s", utc=True)
        df = pd.DataFrame({"o": q["open"], "h": q["high"], "l": q["low"], "c": q["close"], "v": q["volume"]}, index=ix).dropna(subset=["c"])
        tz = res["meta"].get("exchangeTimezoneName")
        if kind == "d":
            df["adj"] = df["c"]; df["date"] = df.index.tz_convert(tz).tz_localize(None).normalize()
            df = df[~df["date"].duplicated(keep="last")]
            D.append(df.assign(sym=sym, ts_utc=df.index).reset_index(drop=True))
        else:
            df = df[~df.index.duplicated(keep="last")]
            H.append(df.assign(sym=sym, ts_utc=df.index).reset_index(drop=True))
        print(sym, kind, len(df), df.index.min() if kind=="h" else df["date"].min(), "vol0 payi", round(float((df.v.fillna(0) == 0).mean()), 3), "ayni_kapanis payi", round(float((df.c.diff() == 0).mean()), 3))
if D: pd.concat(D).to_parquet(f"{V}/panel/ek_b2_dis_gunluk.parquet")
if H: pd.concat(H).to_parquet(f"{V}/panel/ek_b2_saatlik.parquet")
