"""Ikinci kaynak: Nasdaq API'den duzeltilmemis gunluk OHLCV.
    from ikinci_kaynak import nasdaq_gunluk
    df = nasdaq_gunluk("SPY", "2026-10-01", "2026-11-20")   # index=tarih; open high low close volume (float)
assetclass verilmezse once 'etf' sonra 'stocks' denenir. Nasdaq kapanisi = resmi kapanis (temettu/bolunme duzeltmesi yok).
Tek istekte en cok ~5000 satir istenir; uzun aralik icin parca parca cagirin."""
import time, requests
import pandas as pd
H = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
     "Accept": "application/json, text/plain, */*", "Origin": "https://www.nasdaq.com", "Referer": "https://www.nasdaq.com/"}
def _sayi(s):
    return pd.to_numeric(s.astype(str).str.replace(r"[$,]", "", regex=True).replace({"N/A": None, "": None}), errors="coerce")
def nasdaq_gunluk(kod, bas, son, assetclass=None, deneme=3):
    siniflar = [assetclass] if assetclass else ["etf", "stocks"]
    limit = int((pd.Timestamp(son) - pd.Timestamp(bas)).days) + 10
    for ac in siniflar:
        for i in range(deneme):
            try:
                r = requests.get(f"https://api.nasdaq.com/api/quote/{kod}/historical",
                                 params=dict(assetclass=ac, fromdate=pd.Timestamp(bas).strftime("%Y-%m-%d"),
                                             todate=pd.Timestamp(son).strftime("%Y-%m-%d"), limit=limit), headers=H, timeout=30)
                d = r.json().get("data") if r.status_code == 200 else None
                if d and d.get("tradesTable") and d["tradesTable"].get("rows"):
                    df = pd.DataFrame(d["tradesTable"]["rows"])
                    df.index = pd.to_datetime(df.pop("date"), format="%m/%d/%Y"); df.index.name = "tarih"
                    df = df.rename(columns={"close": "close"})[["open", "high", "low", "close", "volume"]].apply(_sayi)
                    df.attrs["assetclass"] = ac
                    return df.sort_index()
                break   # yanit geldi ama bos: diger sinifi dene
            except Exception:
                time.sleep(1 + i)
    return pd.DataFrame(columns=["open", "high", "low", "close", "volume"])
if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from yukle import panel
    C = panel()["close"]
    son = C.index[-1]; bas = C.index[-20]
    for k in ["SPY", "NVDA"]:
        n = nasdaq_gunluk(k, bas, son)
        y = C.loc[bas:son, k]
        bps = (1e4 * (y / n.close.reindex(y.index) - 1)).round(2)
        print(k, n.attrs.get("assetclass"), "gun", int(bps.notna().sum()), "|bps| max", float(bps.abs().max()), "ort", round(float(bps.abs().mean()), 2))
        print(pd.DataFrame({"yahoo": y.round(4), "nasdaq": n.close.reindex(y.index), "bps": bps}).tail(5).to_string())
