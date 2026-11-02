"""tv_map.csv'de olmayan BIST endeks kodlarını TradingView sembol sayfasıyla (HTTP 200 + başlık) doğrula. Çıktı: results/tv_check.csv"""
import subprocess, time, re, pandas as pd
codes = ["XYUZO","XTUMY","XKTUM","XK030","XK050","XK100","XTMTU","XHARZ","XSD25","XMESY","XKURY","XUSRD","XKOBI","XU050","XSIST","XYLDZ","XBANA","XAKUR","XFINK","XSRDK","XU500","XUTUM","XUSIN"]
rows = []
for c in codes:
    out = subprocess.run(["curl", "-s", "-m", "30", "-A", "Mozilla/5.0", "-w", "\n%{http_code}", f"https://www.tradingview.com/symbols/BIST-{c}/"], capture_output=True, text=True).stdout
    code = out.strip().split("\n")[-1]; t = re.search(r"<title>([^<]*)", out); title = t.group(1) if t else ""
    rows.append({"code": c, "http": code, "title": title, "ok": int(code == "200" and "not found" not in title.lower())}); time.sleep(1.0)
    print(rows[-1], flush=True)
pd.DataFrame(rows).to_csv("results/tv_check.csv", index=False)
