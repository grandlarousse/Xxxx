"""Yahoo gün içi indirici (D2): 60 dk (730 gün) ve 5 dk (60 gün). Ham: $S/data/yahoo_raw/{h1,m5}/<SYM>.parquet
Sütunlar: o,h,l,c,v ; index = UTC bar başlangıcı. Yalnız v8/finance/chart uç noktası. UA: Mozilla/5.0.
Kullanım: python3 -I 02_yahoo_indir.py"""
import os, time, json, random, requests, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/4917622c-a1fc-5288-a182-a19cca9a4438/scratchpad/el"
BASE = f"{S}/data/yahoo_raw"
SYMS = ("A1YEN AHGAZ AKENR AKFYE AKSEN AKSUE ALFAS ARFYE AYDEM AYEN BESTE BIOEN BIGEN CONSE CWENE CANTE CATES ARASE ECOGR ENDAE "
        "ENJSA ENERY ESEN GWIND HUNER ENTRA IZENR KLYPV LYDYE MAGEN MASFN METEN MOGAN NTGAZ NATEN ODAS PAMEL SMRTG TATEN VEYAS "
        "ZEDUR ZOREN ASTOR ALARK EUPWR GESAN").split()
ALLS = [s + ".IS" for s in SYMS] + ["XU030.IS", "XU100.IS"]
FALL = ["730d", "600d", "500d", "400d", "365d", "6mo"]
PARAMS = {"d": {"range": "6y", "interval": "1d"}, "h1": {"range": "730d", "interval": "60m"}, "m5": {"range": "60d", "interval": "5m"}}
ses = requests.Session(); ses.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64)"
def fetch(sym, kind):
    p = f"{BASE}/{kind}/{sym.replace('.IS','')}.parquet"; os.makedirs(os.path.dirname(p), exist_ok=True)
    if os.path.exists(p): return "have"
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}"
    prm = dict(PARAMS[kind]); prm.update({"includePrePost": "false", "events": "div,splits"})
    rng_i = 0
    for a in range(8):
        try: r = ses.get(url, params=prm, timeout=60)
        except Exception: time.sleep(2 ** a); continue
        if r.status_code == 429 or r.status_code >= 500: time.sleep(3 * 2 ** a + random.random()); continue
        if r.status_code == 422 and kind == "h1" and rng_i < len(FALL) - 1:  # bazı hisselerde 730d reddediliyor -> daha kısa aralık
            rng_i += 1; prm["range"] = FALL[rng_i]; continue
        if r.status_code != 200: return f"HTTP{r.status_code}"
        res = (r.json().get("chart", {}).get("result") or [None])[0]
        if not res or not res.get("timestamp"): return "empty"
        q = res["indicators"]["quote"][0]
        df = pd.DataFrame({k: q.get(n) for k, n in [("o", "open"), ("h", "high"), ("l", "low"), ("c", "close"), ("v", "volume")]},
                          index=pd.to_datetime(res["timestamp"], unit="s", utc=True))
        df.index.name = "ts_utc"
        df = df.dropna(subset=["c"]); df = df[~df.index.duplicated(keep="last")]
        df.to_parquet(p)
        return f"ok range={prm['range']} n={len(df)} {df.index[0]}..{df.index[-1]} tz={res['meta'].get('exchangeTimezoneName')} off={res['meta'].get('gmtoffset')}"
    return "fail"
if __name__ == "__main__":
    for kind in ("h1", "m5", "d"):
        for s in ALLS:
            print(kind, s, fetch(s, kind), flush=True); time.sleep(0.25)
