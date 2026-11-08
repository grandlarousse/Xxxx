"""Tüm ETF'ler için dağıtım (temettü/faiz/sermaye kazancı) ve bölünme olaylarını Yahoo Finance chart API'sinden indirir.
Neden: Nasdaq API, NYSE Arca (PSE) ve Cboe (BATS) listeli ETF'lerin dağıtım geçmişini vermiyor (313 ETF'in 267'si).
Dürüst istemci adı ('etf-research-script/1.0'), istekler arası 1 sn. Ham JSON: data/yahoo_div/<SYM>.json
Tablo: sonuclar/temettu_yahoo_tum.csv (sym,date,amount,kind) — date = ex-date (New York tarihi).
Kullanım: python3 -I kod/temettu_yahoo.py"""
import os, sys, json, time, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import requests, pandas as pd
import lib

RAW = os.path.join(lib.DATA, "yahoo_div"); os.makedirs(RAW, exist_ok=True)
s = requests.Session(); s.headers["User-Agent"] = "etf-research-script/1.0"
rows = []; bad = {}
for sym in lib.available():
    fn = os.path.join(RAW, sym + ".json")
    if not os.path.exists(fn):
        ok = False
        for a in range(5):
            try:
                r = s.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}",
                          params={"period1": "1451606400", "period2": "1794096000", "interval": "1mo", "events": "div,split"}, timeout=40)
            except Exception:
                time.sleep(2 ** a); continue
            if r.status_code == 429: time.sleep(5 * 2 ** a); continue
            if r.status_code == 200:
                open(fn, "w").write(r.text); ok = True
            else:
                bad[sym] = r.status_code
            break
        time.sleep(1.0 + random.random() * 0.5)
        if not ok: continue
    try:
        res = json.load(open(fn))["chart"]["result"][0]
    except Exception:
        bad[sym] = "parse"; continue
    ev = res.get("events") or {}
    for v in (ev.get("dividends") or {}).values():
        d = pd.to_datetime(int(v["date"]), unit="s", utc=True).tz_convert("America/New_York").tz_localize(None).normalize()
        rows.append({"sym": sym, "date": d.date(), "amount": float(v["amount"]), "kind": "div"})
    for v in (ev.get("splits") or {}).values():
        d = pd.to_datetime(int(v["date"]), unit="s", utc=True).tz_convert("America/New_York").tz_localize(None).normalize()
        rows.append({"sym": sym, "date": d.date(), "amount": float(v["numerator"]) / float(v["denominator"]), "kind": "split"})
    rows.append({"sym": sym, "date": None, "amount": None, "kind": "fetched"})
out = pd.DataFrame(rows)
out.to_csv(os.path.join(lib.ROOT, "sonuclar", "temettu_yahoo_tum.csv"), index=False)
print("satır", len(out), "ETF", out.sym.nunique(), "hatalı", bad)
print(out[out.kind == "div"].groupby("sym").size().describe())
