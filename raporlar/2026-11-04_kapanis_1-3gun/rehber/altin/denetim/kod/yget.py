"""Denetim: bağımsız Yahoo indirici (ydl.fetch mantığı; yalnız denetim/veri altına yazar)."""
import os, sys, time, requests, pandas as pd
D = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/rehber/altin/denetim/veri"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}
P = {"daily": {"period1": 946684800, "interval": "1d"}, "h1": {"range": "730d", "interval": "60m"}, "m5": {"range": "60d", "interval": "5m"}}
def fetch(sym, kind):
    pr = dict(P[kind]); pr.update(includePrePost="false")
    if kind == "daily": pr["period2"] = int(time.time()) + 86400
    for a in range(5):
        r = requests.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}", params=pr, headers=UA, timeout=40)
        if r.status_code == 200: break
        time.sleep(2 * 2 ** a)
    res = r.json()["chart"]["result"][0]; q = res["indicators"]["quote"][0]
    adj = (res["indicators"].get("adjclose") or [{}])[0].get("adjclose")
    idx = pd.to_datetime(res["timestamp"], unit="s", utc=True)
    df = pd.DataFrame({"o": q["open"], "h": q["high"], "l": q["low"], "c": q["close"], "v": q["volume"], "adj": adj if adj else q["close"]}, index=idx)
    tz = res["meta"].get("exchangeTimezoneName")
    df["ldate"] = idx.tz_convert(tz).tz_localize(None).normalize()
    df = df.dropna(subset=["c"])
    df = df[~df["ldate"].duplicated(keep="last")] if kind == "daily" else df[~df.index.duplicated(keep="last")]
    os.makedirs(f"{D}/{kind}", exist_ok=True); df.to_parquet(f"{D}/{kind}/{sym}.parquet")
    return len(df), str(df.index[-1]), res["meta"].get("shortName")
if __name__ == "__main__":
    kind = sys.argv[1]
    for s in sys.argv[2:]: print(kind, s, fetch(s, kind)); time.sleep(0.3)
