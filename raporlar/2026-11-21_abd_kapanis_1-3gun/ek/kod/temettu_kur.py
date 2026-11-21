"""Ham Yahoo JSON events.dividends -> tarih x kod temettu tutari (hisse basina, bolunmeye gore duzeltilmis; Yahoo boyle verir).
Tarih = temettu kaydinin borsa yerel takvim gunu (Yahoo'da ex-date). Kullanim: python3 -I temettu_kur.py <ham_dizin> <panel_dizin>"""
import sys, os, json, urllib.parse
import pandas as pd
ham, pdz = sys.argv[1], sys.argv[2]
KOD = os.path.dirname(os.path.abspath(__file__)); VERI = os.path.join(os.path.dirname(KOD), "veri")
ev = pd.read_csv(os.path.join(VERI, "evren.csv"), dtype={"kod": str})
gun = pd.read_pickle(os.path.join(pdz, "close.pkl")).index
kayit, disari = [], 0
for k in ev.kod:
    p = os.path.join(ham, urllib.parse.quote(k, safe="") + ".json")
    if not os.path.exists(p): continue
    r = json.load(open(p))["chart"]["result"][0]
    tz = r["meta"].get("exchangeTimezoneName") or "America/New_York"
    for v in r.get("events", {}).get("dividends", {}).values():
        d = pd.Timestamp(int(v["date"]), unit="s", tz="UTC").tz_convert(tz).normalize().tz_localize(None)
        kayit.append((d, k, float(v["amount"])))
D = pd.DataFrame(kayit, columns=["tarih", "kod", "tutar"]).groupby(["tarih", "kod"]).tutar.sum().unstack()
disari = D.index.difference(gun)
print("kayit", len(kayit), "kod", D.shape[1], "panel disi tarih", len(disari), list(disari[:5]))
D = D.reindex(gun)
D.to_pickle(os.path.join(pdz, "temettu.pkl"))
print("panel icinde kayit", int(D.notna().sum().sum()), "ilk", D.dropna(how="all").index[0], "son", D.dropna(how="all").index[-1])
print(D[["SPY", "AAPL"]].dropna(how="all").tail(4))
