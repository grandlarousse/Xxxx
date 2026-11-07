import os, sys, time, json, urllib.request, urllib.parse
S = sys.argv[1]
def get(url, tries=5):
    for a in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            return urllib.request.urlopen(req, timeout=90).read()
        except Exception as e:
            err = e; time.sleep(2 * 2 ** a)
    print("FAIL", url, err, flush=True); return None
# Yahoo daily, full history
YT = ["GC=F","SI=F","HG=F","PL=F","PA=F","CL=F","BZ=F","NG=F","DX-Y.NYB","^TNX","^FVX","^IRX","^TYX","^VIX","^GSPC","^NDX","ES=F","NQ=F","ZN=F","ZB=F","ZT=F","GDX","GDXJ","GLD","IAU","SLV","TIP","TLT","UUP","FXI","EEM","BTC-USD","ETH-USD","NEM","AEM","GOLD","B","FNV","WPM","KGC","RGLD","^N225","^HSI","000001.SS","^KS11","^AXJO","^STOXX50E","^GDAXI","^FTSE","XU100.IS","XU030.IS","TUR","USDTRY=X","EURUSD=X","JPY=X","CNH=X","CNY=X","INR=X","ZAR=X","AUDUSD=X","CHF=X","GBPUSD=X","EURTRY=X","^GVZ","^OVX","^MOVE","HYG","LQD","SPY","XLE","COPX","SIL","RING","SGOL","PHYS","CEF","2840.HK","1818.HK","2899.HK","600547.SS","518880.SS","MCX.NS"]
os.makedirs(f"{S}/data/yahoo", exist_ok=True)
for t in YT:
    fn = f"{S}/data/yahoo/{t.replace('^','_').replace('=','_')}.json"
    if os.path.exists(fn): continue
    b = get(f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(t)}?period1=0&period2=1794000000&interval=1d&includeAdjustedClose=true&events=div%2Csplit")
    if b: open(fn, "wb").write(b)
    time.sleep(0.5)
print("yahoo daily done", flush=True)
# Yahoo hourly (730 days)
os.makedirs(f"{S}/data/yahoo_h", exist_ok=True)
for t in ["GC=F","SI=F","DX-Y.NYB","^TNX","ES=F","ZN=F","GDX","GLD","USDTRY=X","^VIX","CL=F","BTC-USD","XU030.IS","HG=F"]:
    fn = f"{S}/data/yahoo_h/{t.replace('^','_').replace('=','_')}.json"
    if os.path.exists(fn): continue
    b = get(f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(t)}?range=730d&interval=1h")
    if b: open(fn, "wb").write(b)
    time.sleep(0.5)
print("yahoo hourly done", flush=True)
# FRED
os.makedirs(f"{S}/data/fred", exist_ok=True)
for sid in ["DFII10","DFII5","T10YIE","T5YIE","T5YIFR","DGS10","DGS2","DGS3MO","DGS30","DTWEXBGS","DTWEXAFEGS","DTWEXEMEGS","VIXCLS","GVZCLS","OVXCLS","BAMLH0A0HYM2","BAMLC0A0CM","DFF","SOFR","USEPUINDXD","T10Y2Y","T10Y3M","DCOILBRENTEU","DCOILWTICO","NFCI","WALCL","RRPONTSYD","DEXCHUS","DEXINUS","DEXJPUS","DEXUSEU","DEXSZUS","DEXSFUS","DEXMXUS","SP500","NASDAQCOM","CPIAUCSL","CPILFESL","PCEPILFE","UNRATE","PAYEMS","ICSA","UMCSENT","M2SL","GFDEBTN","TEDRATE","STLFSI4","DTB3","EFFR"]:
    fn = f"{S}/data/fred/{sid}.csv"
    if os.path.exists(fn): continue
    b = get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}")
    if b: open(fn, "wb").write(b)
    time.sleep(0.4)
print("fred done", flush=True)
# CFTC disaggregated futures-only
os.makedirs(f"{S}/data/cftc", exist_ok=True)
for y in ["hist_2006_2016"] + [str(y) for y in range(2017, 2027)]:
    fn = f"{S}/data/cftc/fut_disagg_txt_{y}.zip"
    if os.path.exists(fn): continue
    b = get(f"https://www.cftc.gov/files/dea/history/fut_disagg_txt_{y}.zip")
    if b: open(fn, "wb").write(b)
    time.sleep(0.5)
# CFTC legacy + TFF not needed. Financial futures (TFF) skipped.
print("cftc done", flush=True)
# GPR daily
os.makedirs(f"{S}/data/misc", exist_ok=True)
for name, url in [("gpr_daily.xls", "https://www.matteoiacoviello.com/gpr_files/data_gpr_daily_recent.xls"),
                  ("sina_AU0.txt", "https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20_x=/InnerFuturesNewService.getDailyKLine?symbol=AU0"),
                  ("sina_AG0.txt", "https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20_x=/InnerFuturesNewService.getDailyKLine?symbol=AG0"),
                  ("fomc_calendar.html", "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm")]:
    fn = f"{S}/data/misc/{name}"
    if os.path.exists(fn): continue
    b = get(url)
    if b: open(fn, "wb").write(b)
    time.sleep(0.5)
print("ALL DONE", flush=True)
