"""Ortak Yahoo indirici. Kullanım:
  python3 -I ydl.py daily SYM1 SYM2 ...      -> data/daily/<SYM>.parquet
  python3 -I ydl.py h1 SYM...                 -> data/h1/<SYM>.parquet (60m, ~730g)
  python3 -I ydl.py m5 SYM...                 -> data/m5/<SYM>.parquet (5m, 60g)
Kütüphane olarak: from ydl import fetch; fetch('THYAO.IS','daily')
Parquet sütunları: o,h,l,c,adj,v ; index = UTC zaman damgası (bar başlangıcı); 'ldate' = borsa yerel tarihi.
Meta: data/meta/<SYM>.json (timezone, gmtoffset, currency, name, exchange, type)
Not: BIST hisselerinde Yahoo 'c' bölünme düzeltmeli, 'adj' temettü+bölünme düzeltmeli. Bedelsiz kaynaklı sıçramalar kalabilir -> temizlik ayrı (clean.py).
"""
import os, sys, json, time, random, requests, datetime as dt
import pandas as pd
BASE = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/dl_k_sahol_a"
S = requests.Session(); S.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64)"
def _path(kind, sym):
    safe = sym.replace("/", "_")
    return os.path.join(BASE, kind, safe + ".parquet")
def fetch(sym, kind="daily", force=False, retries=5):
    p = _path(kind, sym); os.makedirs(os.path.dirname(p), exist_ok=True)
    os.makedirs(os.path.join(BASE, "meta"), exist_ok=True)
    if os.path.exists(p) and not force: return "cached"
    if kind == "daily": params = {"period1": 946684800, "period2": int(time.time()) + 86400, "interval": "1d"}
    elif kind == "h1": params = {"range": "730d", "interval": "60m"}
    elif kind == "m5": params = {"range": "60d", "interval": "5m"}
    elif kind == "m15": params = {"range": "60d", "interval": "15m"}
    else: raise ValueError(kind)
    params.update({"includePrePost": "false", "events": "div,splits"})
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}"
    for a in range(retries):
        try:
            r = S.get(url, params=params, timeout=40)
        except Exception as e:
            time.sleep(2 ** a + random.random()); continue
        if r.status_code == 429 or r.status_code >= 500:
            time.sleep(3 * 2 ** a + random.random()); continue
        if r.status_code != 200: return f"HTTP{r.status_code}"
        j = r.json().get("chart", {})
        if j.get("error") or not j.get("result"): return f"err:{j.get('error')}"
        res = j["result"][0]; ts = res.get("timestamp")
        if not ts: return "empty"
        q = res["indicators"]["quote"][0]
        adj = res["indicators"].get("adjclose", [{}])
        adj = adj[0].get("adjclose") if adj else None
        idx = pd.to_datetime(ts, unit="s", utc=True)
        df = pd.DataFrame({"o": q.get("open"), "h": q.get("high"), "l": q.get("low"), "c": q.get("close"),
                           "adj": adj if adj else q.get("close"), "v": q.get("volume")}, index=idx)
        m = res["meta"]; off = m.get("gmtoffset", 0)
        tzname = m.get("exchangeTimezoneName")
        try:
            df["ldate"] = idx.tz_convert(tzname).tz_localize(None).normalize() if tzname else (idx + pd.Timedelta(seconds=off)).tz_localize(None).normalize()
        except Exception:
            df["ldate"] = (idx + pd.Timedelta(seconds=off)).tz_localize(None).normalize()
        df = df.dropna(subset=["c"])
        if kind == "daily":
            df = df[~df["ldate"].duplicated(keep="last")]
        else:
            df = df[~df.index.duplicated(keep="last")]
        df.to_parquet(p)
        meta = {k: m.get(k) for k in ["symbol", "currency", "exchangeName", "fullExchangeName", "instrumentType", "exchangeTimezoneName", "gmtoffset", "longName", "shortName", "firstTradeDate"]}
        ev = res.get("events", {})
        meta["splits"] = {str(pd.to_datetime(int(k), unit='s').date()): v.get("splitRatio") for k, v in ev.get("splits", {}).items()} if ev else {}
        meta["n_" + kind] = len(df); meta["first_" + kind] = str(df.index[0]); meta["last_" + kind] = str(df.index[-1])
        mp = os.path.join(BASE, "meta", sym.replace("/", "_") + ".json")
        old = json.load(open(mp)) if os.path.exists(mp) else {}
        old.update(meta); json.dump(old, open(mp, "w"), ensure_ascii=False, indent=1)
        return f"ok n={len(df)}"
    return "fail-retries"
def load(sym, kind="daily"):
    return pd.read_parquet(_path(kind, sym))
if __name__ == "__main__":
    kind = sys.argv[1]; syms = sys.argv[2:]
    for s_ in syms:
        print(s_, fetch(s_, kind), flush=True); time.sleep(0.15)
