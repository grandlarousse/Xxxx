import sys,json,time,urllib.request,os
out=sys.argv[1]
syms="SPY QQQ IWM DIA ^GSPC XLK SMH SOXX SOXL NVDA GLD SLV GDX GDXJ SIL USO XLE XOP TLT XLU CPER COPX FXI KWEB EEM EWZ EWT EWY IBIT MSTR COIN ETHA UDOW ASHR ARKK KBE JETS XME XLF VLO MPC PSX PBF HCA BDX TUR FMG.AX BHP.AX ^AXJO XU030.IS XU100.IS TUPRS.IS EREGL.IS KRDMD.IS SAHOL.IS AKBNK.IS GARAN.IS YKBNK.IS ISCTR.IS THYAO.IS PGSUS.IS KCHOL.IS TCELL.IS TTKOM.IS FROTO.IS TOASO.IS ASELS.IS BIMAS.IS SISE.IS PETKM.IS RYSAS.IS RYGYO.IS TRALT.IS TRMET.IS TRENJ.IS KOZAL.IS KOZAA.IS IPEKE.IS".split()
fail=[]
for s in syms:
    ok=False
    for a in range(5):
        try:
            u="https://query1.finance.yahoo.com/v8/finance/chart/%s?period1=1262304000&period2=1794268800&interval=1d&events=div%%2Csplits"%s.replace("^","%5E")
            req=urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"})
            d=urllib.request.urlopen(req,timeout=30).read()
            j=json.loads(d)
            if j["chart"]["result"]:
                open(os.path.join(out,s.replace("^","_")+".json"),"wb").write(d);ok=True;break
        except Exception as e:
            err=str(e)
        time.sleep(1)
    print(s,"OK" if ok else "FAIL "+err,flush=True)
    time.sleep(0.3)
