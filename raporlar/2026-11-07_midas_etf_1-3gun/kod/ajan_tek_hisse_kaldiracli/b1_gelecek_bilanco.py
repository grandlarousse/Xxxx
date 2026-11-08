"""Yaklaşan bilanço tarihleri (Nasdaq: https://api.nasdaq.com/api/analyst/<SYM>/earnings-date; UA 'etf-research-script/1.0').
Çıktı: sonuclar/aile_tek_hisse_kaldiracli/gelecek_bilanco.csv (ham metin + ayrıştırılmış tarih). 'expected*' = Nasdaq/Zacks tahmini.
Çalıştırma: python3 -I kod/ajan_tek_hisse_kaldiracli/b1_gelecek_bilanco.py"""
import os, sys, re, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd, requests
import thk

S = requests.Session(); S.headers["User-Agent"] = "etf-research-script/1.0"; S.headers["Accept"] = "application/json"
rows = []
for s in thk.STOCKS:
    txt = ""; ann = ""
    try:
        r = S.get(f"https://api.nasdaq.com/api/analyst/{s}/earnings-date", timeout=40)
        if r.status_code == 200:
            d = (r.json() or {}).get("data") or {}
            txt = d.get("reportText") or ""; ann = d.get("announcement") or ""
    except Exception as e:
        txt = f"hata: {e}"
    m = re.search(r"(\d{1,2}/\d{1,2}/\d{4})", txt)
    when = "seans_sonrasi" if "after market close" in txt else ("seans_oncesi" if "before market open" in txt else "")
    rows.append({"sym": s, "tarih": pd.to_datetime(m.group(1)).date() if m else None, "zaman": when,
                 "tahmini_mi": "expected" in txt.lower(), "ham": txt[:300], "duyuru": ann})
    time.sleep(1.0)
R = pd.DataFrame(rows); R.to_csv(os.path.join(thk.OUT, "gelecek_bilanco.csv"), index=False)
print(R[["sym", "tarih", "zaman", "tahmini_mi", "duyuru"]].to_string(index=False))
