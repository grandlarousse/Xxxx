"""ETF evreni (kategori -> semboller). Midas'ta işlem gören ABD ETF'lerinin geniş bir kesiti.
Midas'ta bulunurluk ayrıca doğrulanır (bkz. notlar/midas_kosullari.md)."""
U = {
 "abd_genis": ["SPY","VOO","IVV","QQQ","QQQM","DIA","IWM","MDY","RSP","VTI","SPLG"],
 "abd_kaldiracli": ["TQQQ","SQQQ","UPRO","SPXU","SPXL","SPXS","SSO","SDS","QLD","QID","UDOW","SDOW","TNA","TZA","SH","PSQ","URTY","SRTY"],
 "sektor": ["XLK","XLF","XLE","XLV","XLI","XLY","XLP","XLU","XLB","XLRE","XLC","SMH","SOXX","KRE","KBE","XBI","IBB","XOP","OIH","XME","ITB","XHB","XRT","JETS","IGV","CIBR","ITA","XAR","PAVE","IYT","VNQ","KIE","IYR","FDN"],
 "sektor_kaldiracli": ["SOXL","SOXS","TECL","TECS","FAS","FAZ","LABU","LABD","ERX","ERY","GUSH","DRIP","NAIL","DFEN","FNGU","FNGD","CURE","RETL","UTSL"],
 "tematik": ["ARKK","ARKG","ARKW","TAN","ICLN","URA","URNM","LIT","REMX","COPX","BOTZ","ROBO","QTUM","KWEB","BLOK","NLR","UFO","HACK","SKYY","MOO","WCLD","DRIV"],
 "tek_hisse_kaldiracli": ["NVDL","TSLL","MSTU","CONL","NVDU","TSLQ","NVDS","AAPU","AMZU","METU","MSFU","GGLL"],
 "altin_gumus_metal": ["GLD","IAU","GLDM","SLV","SIVR","PPLT","PALL","CPER","DBB","UGL","GLL","AGQ","ZSL"],
 "madenci": ["GDX","GDXJ","NUGT","DUST","JNUG","JDST","SIL","SILJ","RING"],
 "enerji_emtia": ["USO","BNO","USL","UCO","SCO","UNG","UNL","BOIL","KOLD","UGA","DBO","XLE"],
 "tarim_genis_emtia": ["DBC","PDBC","GSG","DBA","CORN","WEAT","SOYB","CANE","COMT","BCI"],
 "tahvil": ["TLT","TMF","TMV","TBT","UBT","IEF","SHY","BIL","SGOV","AGG","BND","LQD","HYG","JNK","TIP","EMB","MUB","ZROZ","EDV","GOVT","VCIT","IEI","TLH","SCHP","USHY","BKLN","STIP"],
 "doviz": ["UUP","UDN","FXE","FXY","FXB","FXA","FXC","FXF","CEW","YCS","YCL","EUO","ULE"],
 "volatilite": ["VXX","UVXY","SVXY","VIXY","UVIX","SVIX","VIXM"],
 "kripto": ["IBIT","FBTC","GBTC","BITB","ARKB","BITO","ETHA","ETHE","BITX","BITI","ETHU","SBIT","BITU"],
 "uluslararasi": ["EEM","VWO","IEMG","EFA","VEA","IEFA","VGK","EZU","FXI","MCHI","ASHR","EWJ","DXJ","EWZ","EWW","INDA","EPI","EWT","EWY","EWG","EWU","EWQ","EWI","EWP","EWC","EWA","EWH","EWS","EIDO","EPHE","THD","EZA","TUR","ARGT","EPOL","ILF","EWM","VNM","ECH","EPU","KSA","EWL","EWN","EWD","GREK","EWK","EIS","QAT","UAE","EWO","NORW","EDEN","EFNL","ENZL","PAK","FM","GXG","EGPT","KEMQ","CQQQ","CHIQ"],
 "uluslararasi_kaldiracli": ["YINN","YANG","EDC","EDZ","EURL","BRZU","INDL","MEXX","KORU","CHAU","CWEB"],
 "faktor_temettu": ["MTUM","QUAL","USMV","VLUE","IWF","IWD","IWO","IWN","SCHD","JEPI","JEPQ","VUG","VTV","SPLV","SPHB","VIG","DGRO","DVY","NOBL","QYLD","XYLD","SPYD","COWZ","AVUV","SCHG","MGK","VYM"],
}
ALL = sorted({s for v in U.values() for s in v})
CAT = {}
for k, v in U.items():
    for s in v:
        CAT.setdefault(s, k)

# Analiz aileleri (iş akışında her aile ayrı ajan tarafından incelenir)
FAMILIES = {
 "abd_endeks": U["abd_genis"] + U["abd_kaldiracli"] + U["faktor_temettu"],
 "sektor_tematik": U["sektor"] + U["sektor_kaldiracli"] + U["tematik"],
 "tek_hisse_kaldiracli": U["tek_hisse_kaldiracli"],
 "enerji_tarim": U["enerji_emtia"] + U["tarim_genis_emtia"] + ["XOP", "OIH", "GUSH", "DRIP", "ERX", "ERY"],
 "metal_madenci": U["altin_gumus_metal"] + U["madenci"] + ["COPX", "XME", "URA", "URNM", "LIT", "REMX"],
 "tahvil_doviz": U["tahvil"] + U["doviz"],
 "volatilite": U["volatilite"],
 "kripto": U["kripto"] + ["BLOK", "MSTU", "CONL"],
 "uluslararasi": U["uluslararasi"] + U["uluslararasi_kaldiracli"],
}
