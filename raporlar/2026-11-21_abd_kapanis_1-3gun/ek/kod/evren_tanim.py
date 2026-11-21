GRUPLAR = {
"genis_endeks":"SPY QQQ IWM DIA MDY RSP VTI",
"sektor":"XLK XLF XLE XLV XLY XLP XLI XLB XLU XLRE XLC",
"tema_etf":"SMH SOXX XSD IGV SKYY CIBR HACK FDN XBI IBB IHI XPH KRE KBE KIE IAI XHB ITB XRT XOP OIH XME GDX GDXJ SIL COPX URA URNM NLR IYT JETS ITA XAR PPA ARKK ARKW ARKG TAN ICLN LIT IPO MAGS QTUM BOTZ ROBO UFO BLOK BITQ WGMI PAVE VNQ IYR",
"faktor":"MTUM SPMO QUAL USMV SPLV SPHB IWF IWD VUG VTV IWO IWN AVUV SCHD VYM",
"kaldirac_ters":"TQQQ SQQQ UPRO SPXU SPXL SPXS SSO SDS QLD QID SOXL SOXS TECL TECS TNA TZA FAS FAZ LABU LABD NUGT DUST JNUG GUSH DRIP ERX ERY YINN YANG TMF TMV UDOW SDOW NVDL TSLL TSLQ CONL MSTU MSTX BITX UVXY SVXY VXX VIXY UCO SCO BOIL KOLD AGQ ZSL UGL GLL",
"capraz_varlik":"TLT IEF SHY TIP HYG JNK LQD EMB BKLN UUP FXE FXY FXB FXA GLD SLV PPLT PALL USO BNO UNG DBC DBA CPER IBIT ETHA GBTC BITO",
"ulke_etf":"EFA EEM VGK EZU EWJ EWG EWU EWQ EWI EWP EWL FXI MCHI KWEB ASHR EWT EWY INDA EWZ EWW TUR EZA EWA EWC EWH EWS ARGT ILF",
"gosterge":"^GSPC ^IXIC ^NDX ^RUT ^DJI ^SOX ^VIX ^VIX3M ^VIX9D ^VVIX ^SKEW ^TNX ^FVX ^TYX ^IRX ^MOVE",
"vadeli_doviz_kripto":"ES=F NQ=F RTY=F CL=F BZ=F NG=F GC=F SI=F HG=F ZN=F ZB=F DX-Y.NYB EURUSD=X JPY=X TRY=X BTC-USD ETH-USD SOL-USD",
"dis_endeks":"^N225 ^HSI 000001.SS ^KS11 ^TWII ^GDAXI ^FTSE ^FCHI ^STOXX50E ^BVSP ^NSEI XU100.IS",
"h_yari_iletken":"NVDA AMD AVGO TSM MU INTC QCOM TXN AMAT LRCX KLAC ASML MRVL ARM ON MCHP ADI NXPI MPWR ALAB CRDO COHR LITE WDC STX",
"h_ai_altyapi":"SMCI DELL HPE ANET VRT CLS ETN PWR CRWV NBIS APLD ORCL",
"h_mega":"AAPL MSFT GOOGL AMZN META TSLA NFLX",
"h_yazilim":"CRM ADBE NOW PLTR APP CRWD PANW ZS NET SNOW DDOG MDB SHOP RDDT DUOL TTD U RBLX SNAP PINS UBER DASH ABNB SPOT FIG INTU WDAY TEAM HUBS AI SOUN BBAI",
"h_kripto":"MSTR COIN HOOD MARA RIOT CLSK IREN CIFR HUT WULF BITF CORZ GLXY CRCL",
"h_fintech":"V MA PYPL XYZ AFRM SOFI UPST NU KLAR TOST",
"h_banka":"JPM BAC C WFC GS MS SCHW BX KKR APO AXP COF",
"h_enerji":"XOM CVX COP OXY EOG DVN SLB HAL VLO MPC PSX PBF FANG",
"h_elektrik_nukleer":"VST CEG GEV TLN NRG BE CCJ UEC LEU OKLO SMR NNE BWXT NEE",
"h_kuantum":"IONQ RGTI QBTS QUBT",
"h_uzay_savunma":"RKLB ASTS LUNR PL KTOS AVAV LMT RTX NOC GD BA AXON",
"h_ev_cin":"RIVN LCID NIO XPEV LI BABA PDD JD BIDU",
"h_seyahat":"DAL UAL AAL LUV CCL RCL NCLH BKNG MAR",
"h_konut":"DHI LEN PHM TOL",
"h_tuketici":"WMT TGT COST HD LOW NKE LULU SBUX MCD CMG CVNA DIS",
"h_saglik":"LLY NVO UNH JNJ PFE MRK ABBV AMGN VRTX REGN ISRG MRNA HIMS TEM CRSP VKTX",
"h_maden_metal":"NEM AEM B FCX SCCO NUE CLF AA MP ALB",
"h_gunes":"FSLR ENPH RUN",
"h_meme":"GME AMC",
"h_sanayi_diger":"CAT DE GE HON UNP FDX UPS BRK-B KO PEP PG",
}
KODLAR = [(k, g) for g, s in GRUPLAR.items() for k in s.split()]
KALDIRAC = {"TQQQ":(3,"QQQ"),"SQQQ":(-3,"QQQ"),"UPRO":(3,"SPY"),"SPXU":(-3,"SPY"),"SPXL":(3,"SPY"),"SPXS":(-3,"SPY"),
"SSO":(2,"SPY"),"SDS":(-2,"SPY"),"QLD":(2,"QQQ"),"QID":(-2,"QQQ"),"SOXL":(3,"SOXX"),"SOXS":(-3,"SOXX"),
"TECL":(3,"XLK"),"TECS":(-3,"XLK"),"TNA":(3,"IWM"),"TZA":(-3,"IWM"),"FAS":(3,"XLF"),"FAZ":(-3,"XLF"),
"LABU":(3,"XBI"),"LABD":(-3,"XBI"),"NUGT":(2,"GDX"),"DUST":(-2,"GDX"),"JNUG":(2,"GDXJ"),"GUSH":(2,"XOP"),"DRIP":(-2,"XOP"),
"ERX":(2,"XLE"),"ERY":(-2,"XLE"),"YINN":(3,"FXI"),"YANG":(-3,"FXI"),"TMF":(3,"TLT"),"TMV":(-3,"TLT"),
"UDOW":(3,"DIA"),"SDOW":(-3,"DIA"),"NVDL":(2,"NVDA"),"TSLL":(2,"TSLA"),"TSLQ":(-2,"TSLA"),"CONL":(2,"COIN"),
"MSTU":(2,"MSTR"),"MSTX":(2,"MSTR"),"BITX":(2,"IBIT"),"UVXY":(1.5,"VXX"),"SVXY":(-0.5,"VXX"),"VXX":(1,"^VIX"),"VIXY":(1,"^VIX"),
"UCO":(2,"USO"),"SCO":(-2,"USO"),"BOIL":(2,"UNG"),"KOLD":(-2,"UNG"),"AGQ":(2,"SLV"),"ZSL":(-2,"SLV"),"UGL":(2,"GLD"),"GLL":(-2,"GLD")}
# VXX/VIXY: kaldiracsiz VIX vadeli (S&P 500 VIX Short-Term Futures) ETN/ETF; dayanak ^VIX yalnizca yaklasik.
# Emtia urunleri Bloomberg vadeli alt endekslerini izler; dayanak olarak evrendeki ETF (USO/UNG/SLV/GLD) verildi.
ONCE = set("^N225 ^HSI 000001.SS ^KS11 ^TWII ^GDAXI ^FTSE ^FCHI ^STOXX50E ^NSEI XU100.IS ^TNX ^FVX ^TYX ^IRX".split())
VIX1615 = set("^VIX ^VIX3M ^VIX9D ^VVIX ^SKEW".split())
def sinif(k):
    if k in ONCE: return "ONCE"
    if k in VIX1615: return "VIX1615"
    if k.endswith("-USD") or k.endswith("=X") or k=="DX-Y.NYB" or k.endswith("=F") or k in ("^BVSP","^MOVE"): return "SONRA"
    return "ABD16"
def tur(k, g):
    if k.endswith("-USD"): return "kripto"
    if k.endswith("=X") or k=="DX-Y.NYB": return "doviz"
    if k.endswith("=F"): return "vadeli"
    if k.startswith("^") or k in ("000001.SS","XU100.IS"): return "endeks"
    if g.startswith("h_"): return "hisse"
    return "ETF"

# Gelmeyen kod -> yeni kod (veri_indir sonrasi doldurulur)
YENI_KOD = {"BITF": "KEEL"}   # Bitfarms -> Keel Infrastructure Corp. (Yahoo BITF bos donuyor)
