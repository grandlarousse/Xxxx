"""Ham Yahoo JSON meta'sindan kapanis saati tablosu. Kullanim: python3 -I kapanis_saatleri.py <ham_dizin>
Kural: ET 15:45'ten sonra kapanan seri SONRA; ABD16 ise 15:45-16:05 arasi ve ABD borsasi; VIX1615 korunur ama sinif SONRA olarak raporlanir."""
import sys, os, json, urllib.parse
import pandas as pd
from zoneinfo import ZoneInfo
KOD = os.path.dirname(os.path.abspath(__file__)); VERI = os.path.join(os.path.dirname(KOD), "veri")
ham = sys.argv[1]
ET = ZoneInfo("America/New_York")
ev = pd.read_csv(os.path.join(VERI, "evren.csv"), dtype={"kod": str})
rows = []
for k in ev.kod:
    p = os.path.join(ham, urllib.parse.quote(k, safe="") + ".json")
    if not os.path.exists(p):
        rows.append(dict(kod=k)); continue
    m = json.load(open(p))["chart"]["result"][0]["meta"]
    reg = m["currentTradingPeriod"]["regular"]; tz = m.get("exchangeTimezoneName")
    s = pd.Timestamp(reg["start"], unit="s", tz="UTC"); e = pd.Timestamp(reg["end"], unit="s", tz="UTC")
    rows.append(dict(kod=k, borsa=m.get("exchangeName"), exchangeTimezoneName=tz, instrumentType=m.get("instrumentType"),
                     yerel_acilis=s.tz_convert(tz).strftime("%H:%M"), yerel_kapanis=e.tz_convert(tz).strftime("%H:%M"),
                     et_kapanis=e.tz_convert(ET).strftime("%H:%M"), ornek_gun_utc=e.strftime("%Y-%m-%d"),
                     sure_saat=round((e - s).total_seconds() / 3600, 2)))
T = pd.DataFrame(rows)
T.to_csv(os.path.join(VERI, "kapanis_saatleri.csv"), index=False)
print(T.drop(columns=["ornek_gun_utc"]).merge(ev[["kod", "tur", "kapanis_sinifi"]], on="kod").query("tur not in ['ETF','hisse'] or et_kapanis!='16:00'").to_string())
print(T.et_kapanis.value_counts())
