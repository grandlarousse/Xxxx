"""Veri indirme (bir kez). Kullanım: python3 00_indir.py <veri_klasoru>"""
import sys, time, pandas as pd, yfinance as yf
out = sys.argv[1]
DAILY = ["UNG","BOIL","KOLD","UNL","NG=F","EQT","AR","RRC","EXE","CNX","CRK","GPOR","CTRA","BKV","NFG","INR","SWN","DVN",
         "LNG","VG","NEXT","NFE","CQP","GLNG","FLNG","EE","KMI","WMB","ET","DTM","TRGP","AM","AROC","KGS",
         "FCG","XOP","XLE","SPY","USO","GUSH","DRIP","XLU","VST","CEG","NRG","TLN","GEV","TTF=F","CL=F","BZ=F","HO=F","^VIX"]
HOURLY = ["UNG","BOIL","KOLD","NG=F","EQT","AR","RRC","EXE","CRK","CNX","XOP","SPY","LNG","TTF=F"]
def get(t, **kw):
    for i in range(3):
        try:
            d = yf.Ticker(t).history(auto_adjust=True, **kw)
            if len(d): return d
        except Exception as e:
            err = e
        time.sleep(1.5)
    return pd.DataFrame()
rows = []
for t in DAILY:
    d = get(t, start="2007-01-01", interval="1d")
    if len(d):
        d.index = d.index.tz_localize(None).normalize()
        d[["Open","High","Low","Close","Volume"]].to_csv(f"{out}/d_{t.replace('=','_').replace('^','')}.csv")
        rows.append((t, "1d", len(d), str(d.index[0].date()), str(d.index[-1].date()), round(float(d.Close.iloc[-1]),3)))
    else: rows.append((t, "1d", 0, "", "", None))
for t in HOURLY:
    d = get(t, period="730d", interval="60m")
    if len(d):
        d[["Open","High","Low","Close","Volume"]].to_csv(f"{out}/h_{t.replace('=','_')}.csv")
        rows.append((t, "60m", len(d), str(d.index[0]), str(d.index[-1]), round(float(d.Close.iloc[-1]),3)))
    else: rows.append((t, "60m", 0, "", "", None))
cov = pd.DataFrame(rows, columns=["ticker","aralik","n","ilk","son","son_kapanis"])
cov.to_csv(f"{out}/_kapsam.csv", index=False)
print(cov.to_string(index=False))
