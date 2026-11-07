"""TradingView sembol sayfasi kontrolu (varsayilan istek basliklari, istekler arasi 1,5 sn).
Sonuc: cikti/tv_kod_kontrol.csv (kod, http, sayfa basligi). 200 + basliktaki kod = sayfa var.
Not: sayfanin varligi kullanicinin planinda grafik acilacagini garanti etmez."""
import csv, os, re, sys, time, subprocess
import ortak as o

KODLAR = """NYSE:BDX NYSE:EHC NASDAQ:TW NASDAQ:ACGL NASDAQ:MAR NYSE:TMO NASDAQ:RPRX NASDAQ:CME NYSE:MRSH NYSE:HLT NYSE:SN
NYSE:MDT NYSE:SYK NYSE:BSX NASDAQ:ISRG NYSE:EW NYSE:ZBH NYSE:BAX NYSE:HCA NYSE:UHS NYSE:THC NYSE:SEM NYSE:UNH NYSE:DVA
NASDAQ:MKTX NYSE:ICE CBOE:CBOE NASDAQ:NDAQ NYSE:RNR NYSE:EG NYSE:CB NYSE:TRV NYSE:BRK.B NYSE:AON NYSE:AJG NASDAQ:WTW NYSE:BRO NYSE:MTG
NYSE:H NYSE:IHG NYSE:WH NASDAQ:BKNG NASDAQ:EXPE NYSE:DHR NYSE:A NYSE:WAT NYSE:MTD NYSE:IQV NASDAQ:VRTX NYSE:BBY NASDAQ:AMZN NASDAQ:HELE
AMEX:XLV AMEX:IHF AMEX:KIE NASDAQ:KBWP AMEX:IAI AMEX:XBI NASDAQ:IBB AMEX:XLY AMEX:PEJ AMEX:SPY
CBOE:VIX3M INDEX:S5FI INDEX:S5TH NASDAQ:NDX TVC:US02Y CME:SR31!
NASDAQ:HLT NASDAQ:SEM NASDAQ:WMT NYSE:TGT""".split()

out = os.path.join(o.CIKTI, "tv_kod_kontrol.csv")
tmp = os.path.join(o.D2, "tv_tmp.html")
rows = []
for k in KODLAR:
    url = "https://www.tradingview.com/symbols/" + k.replace(":", "-") + "/"
    r = subprocess.run(["curl", "-sS", "-o", tmp, "-w", "%{http_code}", url], capture_output=True, text=True)
    code = r.stdout.strip()
    title = ""
    try:
        m = re.search(r"<title>([^<]*)</title>", open(tmp, encoding="utf-8", errors="ignore").read())
        title = m.group(1).strip() if m else ""
    except OSError:
        pass
    ok = code == "200" and k.split(":")[1].replace(".", "") in title.replace(".", "").replace("-", "")
    rows.append((k, code, "VAR" if ok else "YOK/belirsiz", title[:90]))
    print(k, code, rows[-1][2], title[:70], flush=True)
    time.sleep(1.5)
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["kod", "http", "durum", "baslik"]); w.writerows(rows)
