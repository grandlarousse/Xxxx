"""0) Eksik dağıtım (temettü/faiz) verisi: Nasdaq API NYSE Arca / Cboe listeli ETF'ler için temettü geçmişi vermiyor
("Dividend History for Non-Nasdaq symbols is not available"). Bu yüzden data/etf/*.parquet'te HYG, AGG, LQD, TIP, MUB,
BIL, SGOV, JNK, EDV, ZROZ, GOVT, TLH, SCHP, USHY, BKLN, STIP, TMF/TMV/TBT/UBT ve tüm döviz ETF'lerinin dağıtımları YOK
-> toplam getiri eksik, ex-date (çoğunlukla ayın ilk işlem günü) getirileri aşağı yanlı (-16..-34 bp).
Bu betik Yahoo Finance chart API'sinden (dürüst istemci adı) dağıtım olaylarını indirir; ham JSON ayrı klasöre,
ayrıştırılmış tablo sonuclar/aile_tahvil_doviz/temettu_yahoo.csv'ye yazılır. lib.py değiştirilmez; düzeltme td.load()'da.
Çalıştır: python3 -I kod/ajan_tahvil_doviz/00_temettu_indir.py"""
import os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import requests, pandas as pd
import td

RAW = os.path.join(td.OUT, "temettu_yahoo_ham")
os.makedirs(RAW, exist_ok=True)
s = requests.Session(); s.headers["User-Agent"] = "etf-research-script/1.0"
rows = []
for sym in td.FAM + ["SPY"]:
    fn = os.path.join(RAW, sym + ".json")
    if not os.path.exists(fn):
        r = s.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}",
                  params={"period1": "1451606400", "period2": "1794096000", "interval": "1d", "events": "div,split"}, timeout=40)
        if r.status_code != 200:
            print(sym, "HTTP", r.status_code); continue
        open(fn, "w").write(r.text); time.sleep(1.0)
    j = json.load(open(fn))
    try:
        res = j["chart"]["result"][0]
    except Exception:
        print(sym, "veri yok"); continue
    ev = (res.get("events") or {})
    for k, v in (ev.get("dividends") or {}).items():
        d = pd.to_datetime(int(v["date"]), unit="s", utc=True).tz_convert("America/New_York").tz_localize(None).normalize()
        rows.append({"sym": sym, "date": d, "amount": float(v["amount"]), "kind": "div"})
    for k, v in (ev.get("splits") or {}).items():
        d = pd.to_datetime(int(v["date"]), unit="s", utc=True).tz_convert("America/New_York").tz_localize(None).normalize()
        rows.append({"sym": sym, "date": d, "amount": float(v["numerator"]) / float(v["denominator"]), "kind": "split"})
out = pd.DataFrame(rows).sort_values(["sym", "date"])
out.to_csv(os.path.join(td.OUT, "temettu_yahoo.csv"), index=False)
print(out.groupby(["sym", "kind"]).size().unstack(fill_value=0).to_string())
