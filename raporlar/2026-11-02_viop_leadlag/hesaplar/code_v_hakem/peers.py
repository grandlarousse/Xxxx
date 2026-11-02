"""ÖN-KAYIT (02.11.2026, sonuçlara bakmadan sabitlendi) — v_hakem.
Kural (mekanik): her hisse için, o hisseyi kapsayan 1. tur SEKTÖR ajanının HİPOTEZ listesindeki (01_hyp/a1_hyp/a1_pairs/sv.py/a1_curated
kodlarındaki ÖNCEDEN yazılmış liste; FDR/tarama çıktısı DEĞİL) BIST-dışı tekil hisse + sektör ETF'leri alındı. Çıkarılanlar:
 - geniş endeks / ülke ETF'i (EEM, TUR, FXI, MCHI, KWEB, ASHR, EWZ...), FX, emtia vadelisi, faiz, oynaklık
 - aynı Türk şirketinin yurtdışı kotasyonu (TKC, AKBTY, TKGBY, YKBNY...)  [mekanik ayna]
 - hedef hisseyi İÇEREN ETF (CRAK ~%3,9 TUPRS)  [mekanik içerme]
 - Çin A-payı (.SS/.SZ) ve BIST seansı İÇİNDE kapanan borsalar (HK, Hindistan, Körfez, JSE, Atina, Tel Aviv, Kahire, Moskova, BKK, JK, KL, SI)
   -> bu kotasyonların t-1 bilgisi BIST t-1 seansında zaten görülür; 'açılışta yeni bilgi' hipotezine girmez
 - OTC ADR (bayat fiyat), aynı şirketin ikinci kotasyonu (STLA~STLAM.MI, BBVA~BBVA.MC, PKX~005490.KS, LPL~034220.KS, SONY~6758.T, TEN.MI~TS, BUD~ABI.BR, MT~MT.AS, LISP~LISN, ELD.TO~EGO)
   (aynı ajan listesinde tek kotasyon varsa o kalır)
 - ABD'de işlem gören ama ABD-dışı bölgeyi izleyen ETF (EUFN, GREK, CARZ)
Metal ajanı tek liste kullandığı için kendi kod yorumundaki alt gruplar kullanıldı: EREGL/KRDMD = 'çelik emsalleri' + 'madenciler';
TRALT/TRMET = 'altın madencileri'; BRSAN = 'petrol boru / OCTG'.
Bölge endeksi (artık için): ABD/ADR ^GSPC, Kanada ^GSPTSE, Meksika ^MXX, Brezilya ^BVSP, Avrupa ^STOXX (STOXX 600), Japonya ^N225,
Kore ^KS11, Tayvan ^TWII, Avustralya ^AXJO.
YURT İÇİ (DOM) emsalleri: BRIEF_YURTICI.md ve sektör raporlarındaki senkron kümeler (ikincil aile; t-1 bilgisi BIST kapanışında zaten biliniyor -> hipoteze göre ~0 beklenir).
"""
BANK = ["BBVA.MC", "SAN.MC", "UCG.MI", "ISP.MI", "BNP.PA", "DBK.DE", "KBE", "KRE", "XLF", "PKO.WA", "PEO.WA", "OTP.BD", "ITUB", "BBD"]
AIR = ["LHA.DE", "AF.PA", "IAG.L", "RYA.IR", "EZJ.L", "WIZZ.L", "JET2.L", "DAL", "UAL", "AAL", "LUV", "ALK", "JBLU"]
AIRPORT = ["ADP.PA", "FRA.DE", "AENA.MC", "FHZN.SW"]
STEEL = ["MT.AS", "TKA.DE", "SZG.DE", "VOE.VI", "SSAB-A.ST", "OUT1V.HE", "APAM.AS", "NUE", "STLD", "CLF", "CMC", "005490.KS", "5401.T", "GGB", "TX", "SLX"]
MINERS = ["VALE", "BHP", "RIO", "FMG.AX", "AAL.L", "GLEN.L", "FCX"]
GOLDM = ["GDX", "GDXJ", "NEM", "AEM", "B", "KGC", "SSRM", "EGO", "FRES.L", "CG.TO", "TXG.TO", "AU", "GFI", "HMY", "SIL"]
OCTG = ["TS", "OIH", "XOP", "XLE"]
US_REF = ["VLO", "MPC", "PSX", "PBF", "DK"]
EU_REF = ["PKN.WA", "MOL.BD", "NESTE.HE", "GALP.LS", "REP.MC", "OMV.VI"]
PETCHEM = ["LYB", "DOW", "BAS.DE", "WLK", "051910.KS", "011170.KS", "1301.TW", "1303.TW", "1326.TW"]
POLY = ["ALPEKA.MX", "1326.TW", "1303.TW", "3402.T", "LYB", "BAS.DE"]
UTIL = ["EOAN.DE", "RWE.DE", "ENEL.MI", "IBE.MC", "ENGI.PA", "EDP.LS", "PGE.WA", "CEZ.PR", "ICLN", "XLU"]
FERT = ["CF", "NTR", "MOS", "YAR.OL", "ICL", "IPI", "LXU", "OCI.AS", "SQM", "UAN", "CVR", "ATT.WA", "SDF.DE"]
AGRO = ["CTVA", "FMC", "BAYN.DE", "NUF.AX", "KWS.DE", "CF", "NTR", "MOS", "YAR.OL", "ICL", "IPI"]
EPC = ["FLR", "KBR", "J", "ACS.MC", "FER.MC", "HOT.DE", "SKA-B.ST"]
GLASS = ["SGO.PA", "OI", "VID.MC", "VRLA.PA", "5201.T", "GLW", "AMBP", "SOLB.BR", "SYENS.BR", "GEL", "NRP"]
CEM = ["HEI.DE", "HOLN.SW", "CX", "BZU.MI", "TITC.BR", "CRH", "VMC", "MLM", "EXP", "1101.TW", "SGO.PA"]
DEF = ["RHM.DE", "BA.L", "LDO.MI", "HO.PA", "SAAB-B.ST", "KOG.OL", "HAG.DE", "R3NK.DE", "LMT", "NOC", "RTX", "GD", "LHX",
       "012450.KS", "064350.KS", "079550.KS", "047810.KS", "ITA", "ESLT"]
TEL = ["DTE.DE", "ORA.PA", "TEF.MC", "VOD.L", "TEL.OL", "TELIA.ST", "KPN.AS", "AMX", "TIMB", "OPL.WA", "MTELEKOM.BD", "VEON", "KYIV"]
RETAIL = ["JMT.LS", "DNP.WA", "CA.PA", "AD.AS", "TSCO.L", "SBRY.L", "WMT", "COST", "TGT", "KR", "DG", "WALMEX.MX", "CRFB3.SA", "ASAI3.SA",
          "AXFO.ST", "COLR.BR", "XRT"]
FOOD = ["MDLZ", "HSY", "NESN.SW", "BARN.SW", "LISN.SW", "GIS", "KHC", "ULVR.L", "BN.PA"]
BEV = ["KO", "PEP", "CCEP", "CCH.L", "KOF", "ABI.BR", "HEIA.AS", "CARL-B.CO", "TAP"]
AUTO_F = ["F", "GM", "STLAM.MI", "RNO.PA", "VOW3.DE", "MBG.DE", "BMW.DE", "DTG.DE", "VOLV-B.ST", "8TRA.DE", "IVG.MI", "PCAR", "CMI",
          "EXV5.DE", "7203.T", "005380.KS", "000270.KS", "CON.DE", "MT"]
AUTO_T = ["STLAM.MI", "RNO.PA", "VOW3.DE", "F", "EXV5.DE", "7203.T", "005380.KS"]
AUTO_D = ["VOW3.DE", "P911.DE", "PAH3.DE", "MBG.DE", "BMW.DE", "EXV5.DE"]
WHITE = ["WHR", "ELUX-B.ST", "6752.T", "066570.KS", "MT", "SLX", "XHB", "ITB"]
TV = ["034220.KS", "066570.KS", "005930.KS", "6758.T", "6752.T", "2409.TW", "3481.TW", "SMH", "GLW", "WHR", "ELUX-B.ST"]
GRIDEQ = ["ENR.DE", "GEV", "ETN", "HUBB", "VRT", "POWL", "NVT", "AYI", "267260.KS", "298040.KS", "010120.KS", "103590.KS", "006260.KS",
          "SIE.DE", "ABBN.SW", "SU.PA", "PRY.MI", "NKT.CO", "6501.T", "6503.T", "6504.T", "HPS-A.TO", "GRID", "NVDA", "SMH"]

PEERS = {
 # banka ajanı (01_hyp.py DRV; Atina/JSE/OTC/EUFN çıkarıldı)
 **{s: BANK for s in ["AKBNK", "GARAN", "YKBNK", "ISCTR", "HALKB", "VAKBN", "TSKB"]},
 # holding ajanı (01_hyp.py H)
 "KCHOL": ["VLO", "F", "STLAM.MI", "VOW3.DE", "RNO.PA", "WHR", "ELUX-B.ST"],
 "SAHOL": ["KBE", "BBVA.MC", "PKO.WA", "OTP.BD", "ITUB", "HEI.DE"],
 "DOHOL": ["GDX", "ICLN"],
 "ALARK": ["BTU", "ARCH", "WHC.AX", "YAL.AX", "ACS.MC", "FER.MC", "HOT.DE", "SKA-B.ST", "VIE.PA", "STR.VI", "BBY.L", "PAVE", "TUI1.DE"],
 "ENKAI": ["FLR", "KBR", "J", "ACS.MC", "HOT.DE", "SKA-B.ST", "XLE"],
 "EKGYO": ["XHB", "ITB", "VNA.DE", "LEG.DE", "VNQ"],
 # enerji ajanı (01_sync.py)
 "TUPRS": US_REF + EU_REF + ["XLE"],
 "PETKM": PETCHEM,
 "SASA": POLY,
 "AKSEN": UTIL + ["TAN", "VWS.CO", "ORSTED.CO"],
 "ENJSA": UTIL,
 "ODAS": ["GDX", "BTU", "EOAN.DE", "RWE.DE", "PGE.WA", "CEZ.PR", "ICLN"],
 # havacılık ajanı (a3_multi.py)
 "THYAO": AIR, "PGSUS": AIR, "TAVHL": AIRPORT,
 # metal ajanı (a1_hyp.py alt grupları)
 "EREGL": STEEL + MINERS, "KRDMD": STEEL + MINERS, "BRSAN": OCTG, "TRALT": GOLDM, "TRMET": GOLDM,
 # kimya ajanı (a1_hyp.py)
 "GUBRF": FERT, "HEKTS": AGRO, "TKFEN": ["CF", "YAR.OL", "NTR", "MOS", "OCI.AS"] + EPC, "SISE": GLASS, "CIMSA": CEM, "OYAKC": CEM,
 # otomotiv ajanı (01_hyp.py)
 "FROTO": AUTO_F, "TOASO": AUTO_T, "DOAS": AUTO_D, "ARCLK": WHITE, "VESTL": TV, "ASTOR": GRIDEQ,
 # savunma-telekom ajanı (sv.py; TKC ayna olarak çıkarıldı)
 "ASELS": DEF, "TCELL": TEL, "TTKOM": TEL,
 # tüketim ajanı (a1_curated.py)
 "BIMAS": RETAIL, "MGROS": RETAIL, "SOKM": RETAIL, "ULKER": FOOD, "AEFES": BEV,
}
SECTOR = {**{s: "banka" for s in ["AKBNK", "GARAN", "YKBNK", "ISCTR", "HALKB", "VAKBN", "TSKB"]},
          **{s: "holding" for s in ["KCHOL", "SAHOL", "DOHOL", "ALARK", "ENKAI", "EKGYO"]},
          **{s: "enerji" for s in ["TUPRS", "PETKM", "SASA", "AKSEN", "ENJSA", "ODAS"]},
          **{s: "havacilik" for s in ["THYAO", "PGSUS", "TAVHL"]},
          **{s: "metal" for s in ["EREGL", "KRDMD", "BRSAN", "TRALT", "TRMET"]},
          **{s: "kimya" for s in ["GUBRF", "HEKTS", "TKFEN", "SISE", "CIMSA", "OYAKC"]},
          **{s: "otomotiv" for s in ["FROTO", "TOASO", "DOAS", "ARCLK", "VESTL", "ASTOR"]},
          **{s: "savunma_tel" for s in ["ASELS", "TCELL", "TTKOM"]},
          **{s: "tuketim" for s in ["BIMAS", "MGROS", "SOKM", "ULKER", "AEFES"]}}
# 1. turda öne çıkan 'ünlü' örnekler (genel-anomali testinde dışarıda bırakılıp tekrar edilecek)
FAMOUS = ["TUPRS", "THYAO", "PGSUS", "TAVHL", "EREGL", "KRDMD"]
BANKS = ["AKBNK", "GARAN", "YKBNK", "ISCTR", "HALKB", "VAKBN", "TSKB"]
DOM = {
 **{s: [b for b in BANKS if b != s] for s in BANKS},
 "EREGL": ["ISDMR", "KRDMD"], "KRDMD": ["EREGL", "ISDMR"], "BRSAN": ["EREGL", "KRDMD"],
 "TRALT": ["TRMET", "TRENJ"], "TRMET": ["TRALT", "TRENJ"],
 "CIMSA": ["OYAKC", "AKCNS", "NUHCM", "AFYON", "BUCIM", "KONYA"], "OYAKC": ["CIMSA", "AKCNS", "NUHCM", "AFYON", "BUCIM", "KONYA"],
 "ASTOR": ["EUPWR", "GESAN"], "MGROS": ["SOKM", "BIMAS"], "SOKM": ["MGROS", "BIMAS"], "BIMAS": ["MGROS", "SOKM"], "ULKER": ["BIMAS", "MGROS", "SOKM"],
 "THYAO": ["PGSUS", "TAVHL"], "PGSUS": ["THYAO", "TAVHL"], "TAVHL": ["THYAO", "PGSUS"],
 "SAHOL": ["AKBNK"], "KCHOL": ["TUPRS", "FROTO", "YKBNK", "ARCLK", "TOASO"], "AEFES": ["CCOLA"],
 "GUBRF": ["BAGFS", "EGGUB", "HEKTS"], "HEKTS": ["GUBRF", "BAGFS"], "TKFEN": ["ENKAI"], "ENKAI": ["TKFEN"],
 "FROTO": ["TOASO", "DOAS"], "TOASO": ["FROTO", "DOAS"], "DOAS": ["FROTO", "TOASO"], "ARCLK": ["VESTL"], "VESTL": ["ARCLK"],
 "TCELL": ["TTKOM"], "TTKOM": ["TCELL"], "TUPRS": ["AYGAZ", "PETKM"], "PETKM": ["TUPRS", "AKSA"],
 "SASA": ["HEKTS", "KONTR", "ASTOR", "SMRTG", "EUPWR", "GESAN", "CWENE", "YEOTK", "ALFAS"],
 "AKSEN": ["ZOREN", "ODAS", "ENJSA"], "ODAS": ["ZOREN", "AKSEN"], "ENJSA": ["AKSEN", "ODAS", "ZOREN"],
 "ASELS": ["OTKAR"], "ALARK": ["ALCAR"], "EKGYO": ["PSGYO", "RYGYO"],
}
