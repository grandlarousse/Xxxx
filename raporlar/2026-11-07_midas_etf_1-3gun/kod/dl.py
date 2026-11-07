"""Veri indirici (dürüst istemci adı ile, tarayıcı taklidi yok).
Kaynaklar:
  - Nasdaq API: ETF günlük OHLCV (~10 yıl, bölünme düzeltmeli), temettüler, listelendiği borsa.
  - Cboe CDN: VIX, VIX9D, VIX3M, VIX6M, VVIX, OVX, GVZ, SKEW, VXN geçmişi.
  - Coinbase Exchange: BTC-USD, ETH-USD günlük mumlar (UTC 00:00 kapanış).
  - FRED (erişilebilirse): DGS10, DGS2, DFII10, T10Y2Y, DTWEXBGS, DHHNGSP, DCOILWTICO, BAMLH0A0HYM2.
Çıktı: data/etf/<SYM>.parquet  (o,h,l,c,v, div, adjc = toplam getiri düzeltmeli kapanış)
       data/meta/etf_meta.json  (borsa, ad, ilk tarih, satır sayısı)
       data/vol/<IDX>.parquet, data/crypto/<PAIR>.parquet, data/fred/<ID>.parquet
Kullanım: python3 -I kod/dl.py etf | vol | crypto | fred | all
"""
import os, sys, json, time, random, datetime as dt
from concurrent.futures import ThreadPoolExecutor
import requests, pandas as pd, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import universe
BASE = os.path.join(os.path.dirname(HERE), "data")
UA = "etf-research-script/1.0"
TODAY = dt.date(2026, 11, 7)

def sess():
    s = requests.Session(); s.headers["User-Agent"] = UA; return s

def _get(s, url, params=None, tries=5, timeout=60):
    for a in range(tries):
        try:
            r = s.get(url, params=params, timeout=timeout)
            if r.status_code == 200:
                return r
            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep(2 ** a + random.random()); continue
            return r
        except Exception:
            time.sleep(2 ** a + random.random())
    return None

def _num(x):
    if x in (None, "", "N/A"): return np.nan
    return float(str(x).replace("$", "").replace(",", ""))

def fetch_etf(sym):
    out = os.path.join(BASE, "etf", sym + ".parquet")
    if os.path.exists(out): return sym, "cached", None
    s = sess()
    r = _get(s, f"https://api.nasdaq.com/api/quote/{sym}/historical",
             {"assetclass": "etf", "fromdate": "2006-01-01", "todate": TODAY.isoformat(), "limit": "99999"})
    if r is None: return sym, "neterr", None
    try:
        rows = r.json()["data"]["tradesTable"]["rows"]
    except Exception:
        return sym, "nodata", None
    if not rows: return sym, "empty", None
    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")
    df = df.set_index("date").sort_index()
    df = pd.DataFrame({"o": df["open"].map(_num), "h": df["high"].map(_num), "l": df["low"].map(_num),
                       "c": df["close"].map(_num), "v": df["volume"].map(_num)})
    df = df[~df.index.duplicated(keep="last")].dropna(subset=["c"])
    # temettüler
    div = pd.Series(0.0, index=df.index)
    rd = _get(s, f"https://api.nasdaq.com/api/quote/{sym}/dividends", {"assetclass": "etf"})
    nd = 0
    try:
        drows = (rd.json()["data"] or {}).get("dividends", {}).get("rows") or []
        for d in drows:
            if d.get("type") not in (None, "Cash"): continue
            try: ex = pd.to_datetime(d["exOrEffDate"], format="%m/%d/%Y")
            except Exception: continue
            amt = _num(d.get("amount"))
            if np.isnan(amt) or ex < df.index[0] or ex > df.index[-1]: continue
            pos = df.index.searchsorted(ex)
            if pos < len(df): div.iloc[pos] += amt; nd += 1
    except Exception:
        pass
    df["div"] = div
    # toplam getiri: r_t = (c_t + div_t)/c_{t-1} - 1
    tr = (df["c"] + df["div"]) / df["c"].shift(1)
    tr.iloc[0] = 1.0
    df["adjc"] = df["c"].iloc[-1] * tr.cumprod() / tr.cumprod().iloc[-1]
    # bilgi
    exch, name = None, None
    ri = _get(s, f"https://api.nasdaq.com/api/quote/{sym}/info", {"assetclass": "etf"})
    try:
        di = ri.json()["data"]; exch = di.get("exchange"); name = di.get("companyName")
    except Exception:
        pass
    os.makedirs(os.path.dirname(out), exist_ok=True)
    df.to_parquet(out)
    meta = {"sym": sym, "exchange": exch, "name": name, "n": len(df), "first": str(df.index[0].date()),
            "last": str(df.index[-1].date()), "n_div": nd, "cat": universe.CAT.get(sym)}
    return sym, f"ok n={len(df)}", meta

def run_etf():
    os.makedirs(os.path.join(BASE, "meta"), exist_ok=True)
    mp = os.path.join(BASE, "meta", "etf_meta.json")
    meta = json.load(open(mp)) if os.path.exists(mp) else {}
    syms = universe.ALL
    status = {}
    def job(sym):
        res = fetch_etf(sym); time.sleep(0.3 + random.random() * 0.3); return res
    with ThreadPoolExecutor(3) as ex:
        for sym, st, m in ex.map(job, syms):
            status[sym] = st
            if m: meta[sym] = m
            print(sym, st, flush=True)
    json.dump(meta, open(mp, "w"), indent=1)
    json.dump(status, open(os.path.join(BASE, "meta", "dl_status_etf.json"), "w"), indent=0)
    bad = {k: v for k, v in status.items() if not (v.startswith("ok") or v == "cached")}
    print("total", len(status), "bad", len(bad), bad)

def run_vol():
    s = sess(); os.makedirs(os.path.join(BASE, "vol"), exist_ok=True)
    for c in ["VIX", "VIX9D", "VIX3M", "VIX6M", "VVIX", "OVX", "GVZ", "SKEW", "VXN"]:
        r = _get(s, f"https://cdn.cboe.com/api/global/us_indices/daily_prices/{c}_History.csv")
        if r is None or r.status_code != 200: print(c, "fail"); continue
        from io import StringIO
        df = pd.read_csv(StringIO(r.text))
        df.columns = [x.strip().lower() for x in df.columns]
        df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")
        df = df.set_index("date").sort_index()
        if "close" not in df.columns:
            df = df.rename(columns={df.columns[-1]: "close"})
        df.to_parquet(os.path.join(BASE, "vol", c + ".parquet")); print(c, len(df), df.index[-1].date())

def run_crypto():
    s = sess(); os.makedirs(os.path.join(BASE, "crypto"), exist_ok=True)
    for pair in ["BTC-USD", "ETH-USD", "SOL-USD"]:
        rows = []; end = dt.datetime(2026, 11, 8)
        start_lim = dt.datetime(2015, 1, 1)
        while end > start_lim:
            st = end - dt.timedelta(days=300)
            r = _get(s, f"https://api.exchange.coinbase.com/products/{pair}/candles",
                     {"granularity": 86400, "start": st.isoformat(), "end": end.isoformat()})
            if r is None or r.status_code != 200: break
            j = r.json()
            if not j: break
            rows += j; end = st; time.sleep(0.4)
        if not rows: print(pair, "fail"); continue
        df = pd.DataFrame(rows, columns=["t", "l", "h", "o", "c", "v"])
        df["date"] = pd.to_datetime(df["t"], unit="s"); df = df.drop_duplicates("date").set_index("date").sort_index()
        df = df[["o", "h", "l", "c", "v"]]
        df.to_parquet(os.path.join(BASE, "crypto", pair + ".parquet")); print(pair, len(df), df.index[0].date(), df.index[-1].date())

def run_crypto_hourly():
    """BTC/ETH saatlik (son ~3 yıl): ABD kapanışı (16:00 ET) anındaki fiyatı bulmak için."""
    s = sess(); os.makedirs(os.path.join(BASE, "crypto"), exist_ok=True)
    for pair in ["BTC-USD", "ETH-USD"]:
        rows = []; end = dt.datetime(2026, 11, 8)
        start_lim = dt.datetime(2023, 6, 1)
        while end > start_lim:
            st = end - dt.timedelta(hours=300)
            r = _get(s, f"https://api.exchange.coinbase.com/products/{pair}/candles",
                     {"granularity": 3600, "start": st.isoformat(), "end": end.isoformat()})
            if r is None or r.status_code != 200: break
            j = r.json()
            if not j: break
            rows += j; end = st; time.sleep(0.35)
        df = pd.DataFrame(rows, columns=["t", "l", "h", "o", "c", "v"])
        df["ts"] = pd.to_datetime(df["t"], unit="s", utc=True); df = df.drop_duplicates("ts").set_index("ts").sort_index()
        df[["o", "h", "l", "c", "v"]].to_parquet(os.path.join(BASE, "crypto", pair + "_h1.parquet")); print(pair, "h1", len(df))

def run_fred():
    s = sess(); os.makedirs(os.path.join(BASE, "fred"), exist_ok=True)
    ids = ["DGS10", "DGS2", "DFII10", "T10Y2Y", "DTWEXBGS", "DHHNGSP", "DCOILWTICO", "DCOILBRENTEU",
           "BAMLH0A0HYM2", "DEXJPUS", "DEXUSEU", "DEXCHUS", "NIKKEI225", "SP500", "VIXCLS", "DFF", "T10YIE"]
    from io import StringIO
    for i in ids:
        p = os.path.join(BASE, "fred", i + ".parquet")
        if os.path.exists(p): continue
        r = _get(s, "https://fred.stlouisfed.org/graph/fredgraph.csv", {"id": i, "cosd": "2006-01-01"}, tries=6, timeout=90)
        if r is None or r.status_code != 200: print(i, "fail"); continue
        df = pd.read_csv(StringIO(r.text)); df.columns = ["date", "value"]
        df["date"] = pd.to_datetime(df["date"]); df["value"] = pd.to_numeric(df["value"], errors="coerce")
        df.set_index("date").to_parquet(p); print(i, len(df)); time.sleep(1)

def fetch_stock(sym):
    """Tek hisse (ör. tek hisse kaldıraçlı ETF'lerin dayanak hissesi) -> data/stock/<SYM>.parquet (o,h,l,c,v; temettüsüz)."""
    out = os.path.join(BASE, "stock", sym + ".parquet")
    if os.path.exists(out): return "cached"
    s = sess()
    r = _get(s, f"https://api.nasdaq.com/api/quote/{sym}/historical",
             {"assetclass": "stocks", "fromdate": "2006-01-01", "todate": TODAY.isoformat(), "limit": "99999"})
    try:
        rows = r.json()["data"]["tradesTable"]["rows"]
    except Exception:
        return "nodata"
    df = pd.DataFrame(rows); df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")
    df = df.set_index("date").sort_index()
    df = pd.DataFrame({"o": df["open"].map(_num), "h": df["high"].map(_num), "l": df["low"].map(_num),
                       "c": df["close"].map(_num), "v": df["volume"].map(_num)})
    os.makedirs(os.path.dirname(out), exist_ok=True); df.to_parquet(out)
    return f"ok n={len(df)}"

def run_treasury():
    """ABD Hazinesi günlük getiri eğrisi (nominal ve reel). FRED erişilemezse yedek kaynak.
    Hazine verisi ~15:30 ET kapanış teklif fiyatlarına dayanır -> t kapanışında bilinir kabul edilir."""
    from io import StringIO
    s = sess(); os.makedirs(os.path.join(BASE, "treasury"), exist_ok=True)
    for typ, fn in (("daily_treasury_yield_curve", "nominal"), ("daily_treasury_real_yield_curve", "real")):
        parts = []
        for y in range(2015, 2027):
            u = (f"https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/{y}/all"
                 f"?type={typ}&field_tdr_date_value={y}&page&_format=csv")
            r = _get(s, u, timeout=60)
            if r is None or r.status_code != 200: print(typ, y, "fail"); continue
            parts.append(pd.read_csv(StringIO(r.text))); time.sleep(0.5)
        df = pd.concat(parts); df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y")
        df = df.drop_duplicates("Date").set_index("Date").sort_index()
        df.to_parquet(os.path.join(BASE, "treasury", fn + ".parquet")); print(fn, df.shape, df.index[-1].date())

if __name__ == "__main__":
    w = sys.argv[1]
    if w == "treasury": run_treasury()
    if w in ("etf", "all"): run_etf()
    if w in ("vol", "all"): run_vol()
    if w in ("crypto", "all"): run_crypto(); run_crypto_hourly()
    if w in ("fred", "all"): run_fred()
