import os, sys, time, urllib.request, urllib.parse
S = sys.argv[1]
def get(url, tries=5):
    for a in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            return urllib.request.urlopen(req, timeout=90).read()
        except Exception as e:
            err = e; time.sleep(2 * 2 ** a)
    print("FAIL", url, err, flush=True); return None
D = ["GLDM","AAAU","BAR","OUNZ","SIVR","PSLV","SGDM","GOAU","UGL","AGQ","NUGT","JNUG","GDXU","GLL","DZZ","DUST","JDST","ZSL","DGP","SHNY","GDE","SPPP","PPLT","PALL","BITO","IBIT","SLVP","SILJ","USLV","GOEX","GLTR","EGO","AU","HMY","GFI","PAAS","AG","CDE","HL","SSRM","IAG","OR","SAND","NGD","EQX","BTG","AGI","KGC","GOLD.TO","ABX.TO","XGD.TO","CGL.TO","GLDTR.IS","ZGOLD.IS","GMSTR.IS","ALTIN.IS","ZGLD.IS","QNBTR.IS","USDTRY=X","2840.HK","1328.T","SGLN.L","PHAU.L","4GLD.DE","XAD5.MI","GBSE.MI","SGOL","GLD","IAU","GDX","GDXJ","SLV","SIL","RING","PHYS","CEF"]
os.makedirs(f"{S}/data/yahoo", exist_ok=True)
for t in D:
    fn = f"{S}/data/yahoo/{t.replace('^','_').replace('=','_')}.json"
    if os.path.exists(fn): continue
    b = get(f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(t)}?period1=0&period2=1794000000&interval=1d&includeAdjustedClose=true&events=div%2Csplit")
    if b: open(fn, "wb").write(b)
    time.sleep(0.4)
print("daily done", flush=True)
for t in ["GLD","IAU","GLDM","GDX","GDXJ","SLV","NUGT","UGL","GLL","DUST","PHYS","SIL","RING","SPY"]:
    fn = f"{S}/data/yahoo_h/{t}.json"
    if os.path.exists(fn): continue
    b = get(f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=730d&interval=1h&includePrePost=true")
    if b: open(fn, "wb").write(b)
    time.sleep(0.4)
# 5 dakikalık son 60 gün (gün sonu dinamiği için)
os.makedirs(f"{S}/data/yahoo_5m", exist_ok=True)
for t in ["GLD","GDX","GDXJ","NUGT","SLV","IAU","GC=F"]:
    fn = f"{S}/data/yahoo_5m/{t.replace('=','_')}.json"
    if os.path.exists(fn): continue
    b = get(f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(t)}?range=60d&interval=5m&includePrePost=true")
    if b: open(fn, "wb").write(b)
    time.sleep(0.4)
print("ALL DONE", flush=True)
