"""Yahoo gün içi indirici (60 dk: range=730d, 5 dk: range=60d). Ham JSON RAW/yahoo/{h1,m5}/<SYM>.json olarak saklanır,
sonra panel_full/{h1,m5}/<SYM>.parquet yazılır: ts_utc (bar başlangıcı, UTC, tz'siz), ts_tr (= ts_utc + 3 saat), o,h,l,c,v.
Ayrıca günlük (d) ham JSON: 05_snap.py resmi kapanış/açılış için okur.
Kaynak: https://query1.finance.yahoo.com/v8/finance/chart/<KOD>.IS?range=730d&interval=60m  (User-Agent: Mozilla/5.0)
Kullanım: python3 -I 03_yahoo_gunici.py indir | parse"""
import os, sys, json, time, random, subprocess
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from d2common import RAW, FULL, STOCKS, YIDX, UA
SYMS = STOCKS + YIDX
PAR = {"h1": "range=730d&interval=60m", "m5": "range=60d&interval=5m",
       "d": "period1=1483228800&period2=%d&interval=1d&events=div%%2Csplits" % (int(time.time()) + 86400)}   # d: günlük (resmi kapanış için)
# Yeni halka arzlarda range=730d HTTP 422 döndürüyor -> period1 = şimdi-729 gün ile yeniden denenir
ALT = {"h1": "period1=%d&period2=%d&interval=60m" % (int(time.time()) - 729 * 86400, int(time.time()) + 3600)}

def get(sym, kind, par=None):
    fn = f"{RAW}/yahoo/{kind}/{sym}.json"
    if os.path.exists(fn) and os.path.getsize(fn) > 2000: return "var"
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}.IS?{par or PAR[kind]}&includePrePost=false"
    for a in range(5):
        r = subprocess.run(["curl", "-sS", "-A", UA, "-o", fn + ".part", "-w", "%{http_code}", "--max-time", "60", url], capture_output=True, text=True)
        code = r.stdout.strip()
        if code == "200":
            try:
                j = json.load(open(fn + ".part")); res = j["chart"]["result"][0]
                n = len(res.get("timestamp") or [])
                os.rename(fn + ".part", fn); return f"ok n={n}"
            except Exception as e:
                code = f"bozuk:{type(e).__name__}"
        if code in ("404", "400", "422"):
            try: msg = json.load(open(fn + ".part"))["chart"]["error"]["description"][:120]
            except Exception: msg = ""
            os.remove(fn + ".part")
            if code == "422" and par is None and kind in ALT: return "alt:" + get(sym, kind, ALT[kind])
            return f"HTTP{code} {msg}"
        time.sleep(3 * 2 ** a + random.random())
    return f"basarisiz {code}"

def parse(sym, kind):
    fn = f"{RAW}/yahoo/{kind}/{sym}.json"
    if not os.path.exists(fn): return None
    res = json.load(open(fn))["chart"]["result"][0]
    ts = res.get("timestamp")
    if not ts: return None
    q = res["indicators"]["quote"][0]
    df = pd.DataFrame({"ts_utc": pd.to_datetime(ts, unit="s"), "o": q["open"], "h": q["high"], "l": q["low"], "c": q["close"], "v": q["volume"]})
    df = df.dropna(subset=["c"]).drop_duplicates("ts_utc", keep="last").sort_values("ts_utc")
    df.insert(1, "ts_tr", df["ts_utc"] + pd.Timedelta(hours=3))
    # Yahoo, verinin son gününe bar ızgarasına oturmayan tek satır ekliyor (18:00, o=h=l=c=resmi kapanış, v=0): bar değil, atılır.
    hm = df["ts_tr"].dt.hour * 60 + df["ts_tr"].dt.minute
    df = df[(hm % 60 == 30) if kind == "h1" else (hm < 18 * 60)]
    for c in "ohlc": df[c] = df[c].astype(float)
    df["v"] = df["v"].fillna(0).astype("int64")
    os.makedirs(f"{FULL}/{kind}", exist_ok=True)
    df.reset_index(drop=True).to_parquet(f"{FULL}/{kind}/{sym}.parquet", index=False)
    return len(df), df["ts_tr"].iloc[0], df["ts_tr"].iloc[-1], res["meta"].get("gmtoffset"), res["meta"].get("exchangeTimezoneName")

if __name__ == "__main__":
    mode = sys.argv[1]
    for kind in ("h1", "m5", "d"):
        os.makedirs(f"{RAW}/yahoo/{kind}", exist_ok=True)
        for s in SYMS + (["XELKT"] if kind == "d" else []):   # XELKT yalnız günlük (açılış için)
            if mode == "indir":
                r = get(s, kind); print(kind, s, r, flush=True)
                if r != "var": time.sleep(0.4)
            elif kind != "d":      # günlük ham JSON'u 05_snap.py okur
                print(kind, s, parse(s, kind), flush=True)
