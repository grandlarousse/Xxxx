"""Dukascopy saatlik (BID) ve Yahoo günlük/saatlik JSON ayrıştırıcıları -> parquet."""
import glob, os, sys, json, lzma, struct, datetime as dt, numpy as np, pandas as pd
S = sys.argv[1]
POINT = {"XAUUSD": 1e3, "XAGUSD": 1e3, "DOLLARIDXUSD": 1e3, "USTBONDTRUSD": 1e3, "USA500IDXUSD": 1e3, "USDJPY": 1e3, "EURUSD": 1e5, "USDCNH": 1e5, "USDTRY": 1e5, "BRENTCMDUSD": 1e3, "COPPERCMDUSD": 1e4, "VOLIDXUSD": 1e2, "BTCUSD": 1e1}
def duka(sym):
    out = []
    for f in sorted(glob.glob(f"{S}/data/duka_h/{sym}/*.bi5")):
        b = open(f, "rb").read()
        if not b: continue
        y, m = os.path.basename(f)[:-4].split("_"); y, m = int(y), int(m) + 1
        base = dt.datetime(y, m, 1, tzinfo=dt.timezone.utc)
        raw = lzma.decompress(b)
        a = np.frombuffer(raw, dtype=">i4").reshape(-1, 6)
        vol = np.frombuffer(raw, dtype=">f4").reshape(-1, 6)[:, 5]
        t = pd.to_datetime(base) + pd.to_timedelta(a[:, 0], unit="s")
        d = pd.DataFrame({"t": t, "o": a[:, 1], "c": a[:, 2], "l": a[:, 3], "h": a[:, 4], "v": vol})
        out.append(d)
    if not out: return None
    d = pd.concat(out)
    p = POINT.get(sym, 1e3)
    for k in "oclh": d[k] = d[k] / p
    d = d[d.v > 0].drop_duplicates("t").set_index("t").sort_index()
    d.index.name = "bar_start_utc"
    return d
os.makedirs(f"{S}/panel/duka", exist_ok=True)
for sym in sorted(os.listdir(f"{S}/data/duka_h")):
    d = duka(sym)
    if d is not None and len(d):
        d.to_parquet(f"{S}/panel/duka/{sym}.parquet"); print("duka", sym, d.index.min(), d.index.max(), len(d), round(d.c.iloc[-1], 4))
def yahoo(fn):
    j = json.load(open(fn))["chart"]["result"][0]
    meta = j["meta"]; ts = j.get("timestamp")
    if not ts: return None, meta
    q = j["indicators"]["quote"][0]
    adj = j["indicators"].get("adjclose", [{}])[0].get("adjclose")
    d = pd.DataFrame({"ts_utc": pd.to_datetime(ts, unit="s", utc=True), "open": q["open"], "high": q["high"], "low": q["low"], "close": q["close"], "volume": q["volume"]})
    if adj: d["adjclose"] = adj
    tz = meta.get("exchangeTimezoneName", "UTC")
    d["date"] = d.ts_utc.dt.tz_convert(tz).dt.tz_localize(None).dt.normalize()
    return d, meta
os.makedirs(f"{S}/panel/yahoo", exist_ok=True); os.makedirs(f"{S}/panel/yahoo_h", exist_ok=True)
metas = {}
for fn in sorted(glob.glob(f"{S}/data/yahoo/*.json")):
    try:
        d, meta = yahoo(fn)
    except Exception as e:
        print("yahoo ERR", fn, e); continue
    k = os.path.basename(fn)[:-5]
    metas[k] = {x: meta.get(x) for x in ["symbol", "exchangeName", "exchangeTimezoneName", "currency", "instrumentType", "firstTradeDate"]}
    if d is None: print("yahoo empty", k); continue
    d = d.dropna(subset=["close"]).drop_duplicates("date", keep="last").set_index("date")
    d.to_parquet(f"{S}/panel/yahoo/{k}.parquet")
for fn in sorted(glob.glob(f"{S}/data/yahoo_h/*.json")):
    d, meta = yahoo(fn); k = os.path.basename(fn)[:-5]
    if d is None: continue
    d.dropna(subset=["close"]).set_index("ts_utc").to_parquet(f"{S}/panel/yahoo_h/{k}.parquet")
json.dump(metas, open(f"{S}/panel/yahoo/_meta.json", "w"), indent=1)
print("yahoo", len(metas))
