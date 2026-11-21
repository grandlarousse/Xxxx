"""Evren tanımı: grup -> semboller (Yahoo kodlarıyla).

Her grup bir araştırma rolünü taşır (hedef, öncü aday, araç). Aynı sembol birden çok grupta olabilir.
Tek kaynak budur: indirme betiği ve bütün backtest betikleri buradan okur.
"""

EVREN = {
    # ---------- Geniş piyasa ----------
    "genis_etf": "SPY QQQ IWM DIA MDY RSP VTI IJR IWF IWD IWO IWN MTUM VLUE QUAL USMV SPHB SPLV COWZ IPO ARKK",
    "endeks_abd": "^GSPC ^NDX ^RUT ^DJI ^SOX ^XAU ^HUI ^BKX ^NBI ^DJT ^DJU",
    # ---------- 11 GICS sektörü ----------
    "sektor_etf": "XLK XLF XLE XLV XLI XLY XLP XLU XLB XLRE XLC",
    # ---------- Alt sektör / tema ETF'leri ----------
    "alt_teknoloji": "SMH SOXX XSD IGV SKYY HACK CIBR FDN BOTZ ROBO AIQ QTUM",
    "alt_finans": "KRE KBE KIE IAI REM BLOK WGMI BITQ",
    "alt_saglik": "XBI IBB IHI XPH IHF PJP XHE XHS ARKG",
    "alt_tuketim": "XRT XHB ITB PEJ BETZ IBUY JETS DRIV IDRV",
    "alt_sanayi": "XAR ITA PPA IYT XTN PAVE GRID UFO SEA BOAT BDRY",
    "alt_enerji": "XOP OIH XES AMLP CRAK FCG IEO IEZ VDE PSCE URA URNM NLR TAN ICLN FAN PBW",
    "alt_malzeme": "XME GDX GDXJ SIL SILJ COPX PICK SLX LIT REMX MOO VEGI WOOD CUT RING SLVP GOAU BATT",
    "alt_gayrimenkul_altyapi": "IYR VNQ IYZ PHO",
    "ulke_etf": "EEM EFA EWJ EWZ EWW EWG EWU INDA EWY EWT VGK EZU FXI MCHI KWEB ASHR TUR EWC EWA ARGT",
    # ---------- Kaldıraçlı / ters araçlar ----------
    "kaldiracli": (
        "TQQQ SQQQ UPRO SPXU SPXL SPXS TNA TZA SOXL SOXS TECL TECS FNGU LABU LABD FAS FAZ DPST NAIL DFEN "
        "ERX ERY GUSH DRIP NUGT DUST JNUG JDST UCO SCO BOIL KOLD UGL GLL AGQ ZSL YINN YANG TMF TMV "
        "UVXY SVXY VXX VIXY UVIX SVIX NVDL TSLL CONL BITX"
    ),
    # ---------- Emtia: ETF/ETN ----------
    "emtia_etf": (
        "USO BNO UNG UGA DBO USL DBE UNL GLD IAU GLDM SGOL SLV SIVR PPLT PALL CPER DBB DBA CORN WEAT SOYB CANE "
        "DBC PDBC GSG COMT BCI FTGC TAGS KRBN SRUUF COPJ COPP LITP SETM"
    ),
    # ---------- Emtia ve finansal vadeliler (Yahoo sürekli kontrat) ----------
    "vadeli_emtia": (
        "CL=F BZ=F NG=F RB=F HO=F GC=F SI=F PL=F PA=F HG=F ALI=F ZC=F ZW=F KE=F ZS=F ZL=F ZM=F ZO=F ZR=F "
        "SB=F KC=F CC=F CT=F OJ=F LE=F HE=F GF=F LBS=F LBR=F HRC=F TIO=F MTF=F"
    ),
    "vadeli_finans": "ES=F NQ=F RTY=F YM=F ZN=F ZB=F ZT=F ZF=F DX=F 6E=F 6J=F BTC=F",
    # ---------- Kur, kripto, faiz, volatilite, kredi ----------
    "kur": "DX-Y.NYB EURUSD=X USDJPY=X CNH=X MXN=X AUDUSD=X CAD=X BRL=X GBPUSD=X CHF=X",
    "kur_etf": "UUP FXE FXY FXA FXC FXB CEW",
    "kripto": "BTC-USD ETH-USD SOL-USD IBIT GBTC ETHA ETHE BITO",
    "faiz_vol": "^TNX ^IRX ^FVX ^TYX ^VIX ^VIX3M ^VIX9D ^VVIX ^SKEW ^MOVE ^OVX ^GVZ ^VXN ^RVX",
    "tahvil_kredi": "TLT IEF SHY HYG LQD JNK TIP EMB BKLN MUB",
    # ---------- Yurt dışı endeksler ve öncü yabancı hisseler (yerel seans, ABD kapanışından önce biter) ----------
    "endeks_dis": (
        "^N225 ^HSI 000001.SS 399001.SZ ^KS11 ^TWII ^AXJO ^BSESN ^GDAXI ^FTSE ^FCHI ^STOXX50E ^STOXX ^BVSP ^MXX ^GSPTSE"
    ),
    "dis_hisse": (
        "2330.TW 005930.KS 000660.KS 8035.T 6857.T 9984.T 6920.T 6758.T 7203.T ASML.AS ASM.AS BESI.AS SAP.DE IFX.DE "
        "SIE.DE RHM.DE MC.PA AIR.PA STMPA.PA NOVO-B.CO MAERSK-B.CO SHEL.L BP.L RIO.L GLEN.L AZN.L HSBA.L "
        "BHP.AX FMG.AX RIO.AX 0700.HK 9988.HK 1211.HK 300750.SZ NESN.SW ROG.SW"
    ),
    # ---------- ABD hisseleri (alt sektöre göre; öncüler ve yüksek betalı takipçiler) ----------
    "h_yariiletken": (
        "NVDA AMD AVGO TSM ASML INTC MU QCOM TXN AMAT LRCX KLAC MRVL ON NXPI ADI MCHP MPWR TER ENTG SMCI ARM AMKR "
        "COHR LITE CRDO ALAB ONTO ACLS WOLF SWKS QRVO STM GFS UMC ASX CAMT NVMI ACMR FORM MKSI AEHR RMBS SITM MTSI "
        "POWI LSCC SLAB SYNA"
    ),
    "h_donanim_ag": "AAPL CSCO ANET CIEN VRT DELL HPE HPQ WDC STX SNDK PSTG NTAP CLS FN AAOI IBM GLW APH TEL JBL FLEX",
    "h_yazilim": (
        "MSFT ORCL CRM ADBE NOW PLTR SNOW DDOG MDB NET CRWD PANW ZS FTNT S OKTA TEAM WDAY INTU HUBS ZM DOCU TWLO "
        "PATH AI ACN SNPS CDNS ADSK ROP APP U"
    ),
    "h_internet_medya": (
        "GOOGL META AMZN NFLX DIS SPOT RBLX TTD PINS SNAP RDDT SHOP UBER LYFT ABNB BKNG DASH EXPE EBAY ETSY CHWY W "
        "CVNA T VZ TMUS CMCSA CHTR WBD EA TTWO"
    ),
    "h_fintech_kripto": "PYPL XYZ COIN HOOD SOFI AFRM UPST MSTR MARA RIOT CLSK IREN CIFR WULF HUT CORZ BTDR CRWV NBIS APLD",
    "h_tematik_yuksek_beta": "IONQ RGTI QBTS QUBT RKLB ASTS LUNR JOBY ACHR OKLO SMR NNE TEM RXRX",
    "h_nukleer_guc": "LEU CCJ UEC UUUU DNN NXE BWXT CEG VST TLN NRG GEV ETN PWR BE FLNC",
    "h_temiz_enerji": "PLUG FCEL ENPH SEDG FSLR RUN NXT ARRY",
    "h_oto_ev": "TSLA GM F RIVN LCID NIO XPEV LI STLA TM HMC APTV BWA",
    "h_lityum_nadir": "ALB SQM LAC MP PLL SGML TMC",
    "h_perakende_tuketim": (
        "HD LOW NKE LULU SBUX MCD CMG TGT WMT COST TJX ROST DG DLTR BBY DKS ULTA RH WSM DECK ONON CROX"
    ),
    "h_konut": "DHI LEN PHM TOL KBH NVR BLDR Z OPEN RKT UWMC",
    "h_seyahat": "RCL CCL NCLH MAR HLT LVS WYNN MGM DKNG AAL DAL UAL LUV ALK JBLU",
    "h_temel_tuketim": "PG KO PEP PM MO MDLZ CL KMB GIS KHC HSY STZ KR ADM BG TSN CAG MNST EL CELH",
    "h_ilac_biyotek": (
        "LLY NVO JNJ MRK ABBV PFE AMGN GILD BMY VRTX REGN MRNA BNTX BIIB ZTS HIMS VKTX CRSP NTLA BEAM ALNY ARGX "
        "INSM AZN NVS SNY GSK"
    ),
    "h_medikal_hizmet": "UNH CVS CI ELV HUM CNC HCA ISRG TMO DHR ABT MDT SYK BSX DXCM ILMN EXAS NTRA IQV",
    "h_banka_buyuk": "JPM BAC C WFC GS MS SCHW BLK BX KKR APO CG ARES AXP COF V MA BRK-B IBKR LPLA",
    "h_banka_bolgesel": "USB PNC TFC FITB KEY RF HBAN CFG ZION WAL CMA MTB FLG",
    "h_sigorta_borsa": "PGR ALL AIG MET PRU CB TRV ICE CME NDAQ CBOE SPGI MCO MSCI",
    "h_gyo": "PLD AMT CCI EQIX DLR SPG O PSA WELL AVB EQR VICI IRM SBAC CBRE AGNC NLY",
    "h_savunma_havacilik": "BA GE RTX LMT NOC GD LHX HII TDG HWM AXON KTOS AVAV LDOS BAH",
    "h_makine_sanayi": (
        "CAT DE HON MMM URI PCAR CMI EMR ROK PH ITW WM RSG FAST GWW CARR TT JCI LII FIX EME MTZ DY STRL PRIM"
    ),
    "h_tasimacilik": "UNP CSX NSC UPS FDX ODFL JBHT XPO SAIA KNX CHRW EXPD",
    "h_denizcilik": "ZIM MATX SBLK GOGL DAC STNG FRO TNK INSW DHT GNK FLNG",
    "h_petrol_entegre_ep": (
        "XOM CVX COP EOG OXY DVN FANG APA KOS TTE SHEL BP EQNR PBR CNQ SU CVE IMO"
    ),
    "h_petrol_hizmet": "SLB HAL BKR NOV FTI RIG VAL NE HP PTEN LBRT",
    "h_rafineri": "VLO MPC PSX PBF DK DINO PARR CVI",
    "h_boru_lng": "KMI WMB ET EPD OKE TRGP LNG CQP ENB TRP",
    "h_dogalgaz": "EQT AR RRC CTRA CNX EXE",
    "h_komur": "BTU CNR AMR HCC ARLP",
    "h_kimya_gubre": "LIN APD SHW ECL DOW LYB DD CTVA FMC MOS NTR CF IPI",
    "h_bakir_celik_aluminyum": "FCX SCCO TECK BHP RIO VALE HBM ERO CLF NUE STLD CMC RS AA CENX KALU",
    "h_altin_gumus": (
        "NEM B AEM KGC AU GFI HMY WPM FNV RGLD PAAS AG HL CDE EXK SSRM AGI EGO IAG NGD BTG SBSW PLG"
    ),
    "h_yapi_orman": "VMC MLM CRH EXP IP PKG BALL WY PCH RYN LPX",
    "h_kamu_hizmet": "NEE DUK SO D AEP EXC SRE XEL PCG EIX ED PEG AWK AES",
    "h_cin_adr": "BABA PDD JD BIDU NTES TCOM BILI FUTU TME",
    "h_diger_adr": "SAP SONY SE MELI NU GRAB INFY HDB ITUB",
    # ---------- 1. dalga ajanlarının istediği ek semboller (kaldıraçlı/ters sektör ETF'leri, yabancı öncüler, emsaller) ----------
    "ek_kaldiracli": "DUSL UTSL UXI SIJ SDP CURE RXL DRN DRV RETL WANT SKF TSLQ MSTU BITI CWEB USD UPLT UPAL CPXR UCOP COPZ",
    "ek_etf": "SOXQ PSI BIZD KBWB MBB EWH EWS BWET EUAD SHLD AAAU PSLV CEF SPPP IHE VHT WCLD BUG KCCA KEUA WXET CXRN",
    "ek_hisse": (
        "ARCC OBDC OWL GLXY CRCL ANT AGCO ANDE CALM DAR GPRE HRL INGR KDP PPC SFD TILL UAN ICL BCC UFPI CX MT OLN PPG "
        "WLK USAR BJ BURL ZBH IMPUY CNH AXT"
    ),
    "ek_dis": (
        "BA.L LDO.MI SAAB-B.ST HAG.DE U-UN.TO CCO.TO FM.TO ANTO.L LYC.AX PLS.AX 002460.SZ 0027.HK 1928.HK 2015.HK "
        "2899.HK 3033.HK 9618.HK 9866.HK 9868.HK"
    ),
    "ek_diger": "KRW=X TWD=X TTF=F ^VXEEM ^VXGDX",
}



def tum_semboller():
    """Tekrarsız, sıralı sembol listesi."""
    s = set()
    for v in EVREN.values():
        s.update(v.split())
    return sorted(s)


def grup_haritasi():
    """sembol -> [gruplar]."""
    h = {}
    for g, v in EVREN.items():
        for t in v.split():
            h.setdefault(t, []).append(g)
    return h


if __name__ == "__main__":
    print(len(tum_semboller()), "sembol,", len(EVREN), "grup")
