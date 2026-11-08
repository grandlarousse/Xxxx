"""Denetim: hayatta kalma yanlılığı testi için ex-ante evren (Kasım 2016'da piyasa değeri en büyük ABD hisseleri,
S1'in 7 hissesi hariç) + tek hisse kaldıraçlı ETF'i olan ama S1'e alınmamış hisseler.
Nasdaq tarihsel API (dl.py fetch_stock ile aynı kaynak), dürüst istemci adı. Çıktı: kod/denetim_tek_hisse_kaldiracli/veri/<SYM>.parquet
(paylaşılan data/stock dizinine YAZILMAZ)."""
import os, time, requests, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "veri"); os.makedirs(OUT, exist_ok=True)
EXANTE_2016 = ["XOM", "JNJ", "JPM", "GE", "WFC", "T", "PG", "CVX", "VZ", "PFE", "WMT", "KO", "BAC", "MRK", "ORCL",
               "INTC", "CSCO", "V", "HD", "CMCSA", "DIS", "PEP", "UNH", "PM", "IBM", "C", "MO", "AMGN", "MMM", "MA"]
LETF_OTHER = ["AMD", "NFLX", "BA", "PYPL", "NKE", "BABA", "LLY", "SMCI", "PLTR", "CRM", "ADBE", "QCOM", "MU", "UBER", "SHOP"]
def num(x):
    if x in (None, "", "N/A"): return np.nan
    return float(str(x).replace("$", "").replace(",", ""))
def fetch(sym):
    p = os.path.join(OUT, sym + ".parquet")
    if os.path.exists(p): return "cached"
    s = requests.Session(); s.headers["User-Agent"] = "etf-research-script/1.0"
    for a in range(4):
        try:
            r = s.get(f"https://api.nasdaq.com/api/quote/{sym}/historical",
                      params={"assetclass": "stocks", "fromdate": "2016-01-01", "todate": "2026-11-07", "limit": "99999"}, timeout=60)
            rows = r.json()["data"]["tradesTable"]["rows"]
            break
        except Exception as e:
            time.sleep(2 ** a); rows = None
    if not rows: return "nodata"
    df = pd.DataFrame(rows); df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")
    df = df.set_index("date").sort_index()
    df = pd.DataFrame({"o": df["open"].map(num), "h": df["high"].map(num), "l": df["low"].map(num),
                       "c": df["close"].map(num), "v": df["volume"].map(num)})
    df = df[~df.index.duplicated(keep="last")].dropna(subset=["c"])
    df.to_parquet(p); return f"ok n={len(df)}"
if __name__ == "__main__":
    for s in EXANTE_2016 + LETF_OTHER:
        print(s, fetch(s), flush=True); time.sleep(0.6)
