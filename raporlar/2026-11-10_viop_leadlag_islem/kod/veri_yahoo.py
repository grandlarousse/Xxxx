"""Yahoo indirici. python3 -I veri_yahoo.py <VERI_DIR> <ciftler_csv> <bulten_20261109.csv>
Cikti: raw/yahoo/{daily,h1,m5}/<SYM>.parquet (index UTC bar baslangici; o,h,l,c,adj,v) + raw/yahoo/events/<SYM>.json (div/split) + raw/yahoo/meta.json
Yeniden baslatilabilir (var olan dosya atlanir)."""
import os, sys, json, time, csv, random, requests, datetime as dt
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
V, CSV, BUL = sys.argv[1:4]
R = f"{V}/raw/yahoo"
for k in ("daily", "h1", "m5", "events"): os.makedirs(f"{R}/{k}", exist_ok=True)
S = requests.Session(); S.headers["User-Agent"] = "Mozilla/5.0"
# --- sembol listeleri
b = pd.read_csv(BUL, sep=";", encoding="cp1254", skiprows=[1], dtype=str)
b = b[(b["PAZAR SEGMENTI"] == "SSF")]
und47 = sorted({x[:-2] for x in b["DAYANAK VARLIK"].dropna().unique() if x.endswith(".E")})
assert len(und47) == 47, len(und47)
oncu = set()
for r in csv.DictReader(open(CSV, encoding="utf-8"), delimiter=";"):
    for x in r["oncu"].split("+"):
        x = x.strip()
        if x and not x.startswith("VIOP:"): oncu.add(x)
extra = ("AGHOL AKSA ALFAS ANSGR BERA BRYAT BTCIM CANTE CCOLA CWENE ECILC EGEEN ENERY EUPWR GESAN GLYHO GWIND ISMEN KARSN KCAER KONTR KONYA KORDS MAVI MIATK OTKAR QUAGR REEDR SMRTG SKBNK TABGD TMSN TTRAK TURSG YEOTK ZOREN ALBRK ANHYT AGESA AKFYE CLEBI LOGO NTHOL TUKAS SELEC ISDMR KRDMA KRDMB NUHCM AKCNS BUCIM AYGAZ BRISA TATGD BAGFS TRGYO ISGYO SNGYO AYDEM VESBE TRENJ SDTTR").split()
is_oncu = {x for x in oncu if x.endswith(".IS")}
foreign = {x for x in oncu if not x.endswith(".IS") and x not in ("XU030", "XLBNK", "XAUUSD", "XAGUSD", "XAUTRY", "USDTRY") and x not in und47} | {x for x in oncu if x in und47 and False}
# bare US ticker cakismasi: oncu'da cplak 'F','CF','DAL' vb. yabanci; und47 icindeki bare adlar (hedef) yabanci degil
foreign = {x for x in oncu if not x.endswith(".IS") and x not in und47 and not x.startswith("X")} | {x for x in oncu if x in ("XLBNK",) and False}
foreign |= {"^GSPC", "^STOXX50E", "^AXJO", "^N225", "^KS11"}
dis_only = foreign | {"SPY", "EXW1.DE", "BZ=F", "GC=F", "ES=F"}
idx = {"XU030.IS", "XU100.IS", "XBANK.IS"}
spot = {s + ".IS" for s in und47} | is_oncu | {s + ".IS" for s in extra} | idx
saatlik = {s + ".IS" for s in und47} | is_oncu | {"XU030.IS"} | dis_only
dk5 = {s + ".IS" for s in und47} | is_oncu | {"XU030.IS"}
json.dump({"und47": und47, "spot": sorted(spot), "dis": sorted(foreign), "saatlik": sorted(saatlik), "dk5": sorted(dk5)}, open(f"{R}/meta.json", "w"), indent=1)
jobs = [(s, "daily") for s in sorted(spot | foreign)] + [(s, "h1") for s in sorted(saatlik)] + [(s, "m5") for s in sorted(dk5)]
P = {"daily": {"period1": 1388534400, "period2": int(time.time()) + 86400, "interval": "1d"},
     "h1": {"range": "730d", "interval": "1h"}, "m5": {"range": "60d", "interval": "5m"}}
def run(j):
    sym, kind = j; p = f"{R}/{kind}/{sym}.parquet"
    if os.path.exists(p) or os.path.exists(p + ".yok"): return (sym, kind, "skip")
    prm = dict(P[kind]); prm.update({"includePrePost": "false", "events": "div,splits"})
    for a in range(3):
        try:
            r = S.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}", params=prm, timeout=40)
            if r.status_code == 404: open(p + ".yok", "w").write("404"); return (sym, kind, "404")
            if r.status_code != 200: time.sleep(3 * (a + 1)); continue
            res = (r.json().get("chart", {}).get("result") or [None])[0]
            if not res or not res.get("timestamp"): open(p + ".yok", "w").write("bos"); return (sym, kind, "bos")
            q = res["indicators"]["quote"][0]; ad = (res["indicators"].get("adjclose") or [{}])[0].get("adjclose")
            ix = pd.to_datetime(res["timestamp"], unit="s", utc=True)
            df = pd.DataFrame({"o": q["open"], "h": q["high"], "l": q["low"], "c": q["close"], "adj": ad if ad else q["close"], "v": q["volume"]}, index=ix)
            df = df.dropna(subset=["c"])
            tz = res["meta"].get("exchangeTimezoneName")
            if kind == "daily":
                df["ldate"] = ix[df.index.isin(ix)].tz_convert(tz).tz_localize(None).normalize()[:0].append(pd.DatetimeIndex([])) if False else pd.DatetimeIndex(ix.tz_convert(tz).tz_localize(None).normalize())[[i for i, t in enumerate(ix) if t in df.index]] if False else df.index.tz_convert(tz).tz_localize(None).normalize()
                df = df[~df["ldate"].duplicated(keep="last")]
            else:
                df = df[~df.index.duplicated(keep="last")]
            df.to_parquet(p)
            ev = res.get("events", {}) or {}
            if kind == "daily":
                json.dump({"tz": tz, "name": res["meta"].get("longName"), "first": res["meta"].get("firstTradeDate"), "currency": res["meta"].get("currency"),
                           "splits": {str(pd.to_datetime(int(k), unit="s").date()): v for k, v in (ev.get("splits") or {}).items()},
                           "div": {str(pd.to_datetime(int(k), unit="s").date()): v.get("amount") for k, v in (ev.get("dividends") or {}).items()}},
                          open(f"{R}/events/{sym}.json", "w"))
            return (sym, kind, f"ok {len(df)}")
        except Exception as e:
            time.sleep(3 * (a + 1))
    return (sym, kind, "fail")
with ThreadPoolExecutor(4) as ex:
    out = list(ex.map(run, jobs))
from collections import Counter
print(Counter(o[2].split()[0] for o in out))
print([o for o in out if o[2].split()[0] in ("404", "bos", "fail")])
