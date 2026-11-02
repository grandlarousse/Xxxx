"""cin ajanı - Adım 1: Yahoo'dan Çin/Asya orijinal seriler + alternatif adayları indir (ydl.fetch, eksikse).
Kullanım: python3 c01_fetch_yahoo.py
Çıktı: data/daily/<SYM>.parquet (ortak veri dizini; ydl standart) + out/code_cin/yahoo_fetch_status.csv
"""
import sys, os, time
SCR = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
sys.path.insert(0, SCR + "/code")
import ydl, pandas as pd

SYMS = {
 # --- Çin / HK endeksleri (orijinal) ---
 "000001.SS": "SSE Composite", "000300.SS": "CSI 300", "399001.SZ": "Shenzhen Component", "000016.SS": "SSE 50",
 "000905.SS": "CSI 500", "399006.SZ": "ChiNext", "^HSI": "Hang Seng", "^HSCE": "HSCEI", "XIN9.FGI": "FTSE China A50 (Yahoo?)",
 "^HSTECH": "HS Tech?", "HSTECH.HK": "HS Tech?",
 # --- FX ---
 "CNY=X": "USD/CNY", "CNH=X": "USD/CNH", "AUDUSD=X": "AUD/USD", "HKD=X": "USD/HKD",
 # --- ABD ETF alternatifleri ---
 "ASHR": "CSI300 A ETF", "CNYA": "MSCI China A ETF", "KBA": "MSCI China A50 Connect ETF", "FXI": "China Large-Cap (H)", "MCHI": "MSCI China",
 "GXC": "S&P China", "KWEB": "China Internet", "CQQQ": "China Tech", "CHIQ": "China Consumer Disc.", "CXSE": "China ex-SOE",
 "EWH": "MSCI Hong Kong", "FLCH": "FTSE China", "CNXT": "ChiNext ETF", "PGJ": "Golden Dragon", "YINN": "3x China (kaldıraçlı)",
 # --- Emtia (ABD/diğer) ---
 "TIO=F": "COMEX demir cevheri 62% CFR China", "HG=F": "COMEX bakır", "ALI=F": "COMEX alüminyum", "HRC=F": "COMEX ABD HRC",
 "CL=F": "WTI", "BZ=F": "Brent", "GC=F": "Altın", "MTF=F": "Rotterdam kömür", "SLX": "Çelik ETF", "PICK": "Metal madencileri ETF",
 "CPER": "Bakır ETF", "COPX": "Bakır madenci ETF",
 # --- Demir cevheri madencileri / AUD ---
 "BHP": "BHP ADR", "RIO": "Rio ADR", "VALE": "Vale ADR", "FMG.AX": "Fortescue", "BHP.AX": "BHP ASX", "RIO.AX": "Rio ASX", "MIN.AX": "Mineral Resources",
 "CIA.AX": "Champion Iron", "^AXJO": "ASX200", "^KS11": "KOSPI", "^N225": "Nikkei", "005490.KS": "POSCO", "PKX": "POSCO ADR",
 # --- Çin hisseleri: A ve H (orijinal) ---
 "600019.SS": "Baosteel", "000898.SZ": "Ansteel A", "0347.HK": "Ansteel H", "0323.HK": "Maanshan Steel H", "000709.SZ": "HBIS",
 "000333.SZ": "Midea A", "0300.HK": "Midea H", "600690.SS": "Haier A", "6690.HK": "Haier H", "000651.SZ": "Gree", "000921.SZ": "Hisense HA A",
 "0921.HK": "Hisense HA H", "000100.SZ": "TCL Tech", "1070.HK": "TCL Electronics", "0751.HK": "Skyworth",
 "002594.SZ": "BYD A", "1211.HK": "BYD H", "0175.HK": "Geely", "2333.HK": "Great Wall Motor H", "600104.SS": "SAIC", "9863.HK": "Leapmotor",
 "300750.SZ": "CATL A", "3750.HK": "CATL H",
 "600028.SS": "Sinopec A", "0386.HK": "Sinopec H", "601857.SS": "PetroChina A", "0857.HK": "PetroChina H", "0883.HK": "CNOOC H",
 "601899.SS": "Zijin A", "2899.HK": "Zijin H", "603993.SS": "CMOC A", "3993.HK": "CMOC H", "600547.SS": "Shandong Gold A", "1787.HK": "Shandong Gold H",
 "1818.HK": "Zhaojin H", "600585.SS": "Conch A", "0914.HK": "Conch H", "601600.SS": "Chalco A", "2600.HK": "Chalco H", "1378.HK": "Hongqiao",
 "600362.SS": "Jiangxi Copper A", "0358.HK": "Jiangxi Copper H",
 "600346.SS": "Hengli Petrochem", "002493.SZ": "Rongsheng", "601233.SS": "Tongkun", "000703.SZ": "Hengyi", "603225.SS": "Xin Feng Ming",
 "000822.SZ": "Shandong Haihua (soda)", "600409.SS": "Sanyou Chem (soda)", "000683.SZ": "Yuanxing (dogal soda)", "601636.SS": "Kibing Glass",
 "0868.HK": "Xinyi Glass", "3606.HK": "Fuyao H", "600660.SS": "Fuyao A", "600740.SS": "Shanxi Coking", "601088.SS": "Shenhua A", "1088.HK": "Shenhua H",
 "600089.SS": "TBEA", "601179.SS": "XD Electric", "002028.SZ": "Sieyuan Electric", "518880.SS": "Huaan Gold ETF",
 # --- ABD ADR / OTC ---
 "BABA": "Alibaba ADR", "PDD": "PDD", "JD": "JD ADR", "BIDU": "Baidu ADR", "NIO": "NIO", "XPEV": "XPeng", "LI": "Li Auto",
 "BYDDY": "BYD ADR (OTC)", "BYDDF": "BYD H OTC", "ZIJMY": "Zijin ADR OTC", "ZIJMF": "Zijin H OTC", "AHCHY": "Conch ADR OTC",
 "SNPMF": "Sinopec H OTC", "PCCYF": "PetroChina H OTC", "CMCLF": "CMOC H OTC", "JIAXF": "Jiangxi Copper H OTC", "GELYY": "Geely ADR OTC",
 "GWLLY": "Great Wall ADR OTC", "HSHCY": "Haier ADR OTC?", "CICHY": "CCB ADR OTC", "TCEHY": "Tencent ADR OTC", "ALMMF": "Chalco H OTC",
 "SHZHY": "Shenzhou Intl ADR", "IVL.BK": "Indorama (PTA)", "TATACHEM.NS": "Tata Chemicals (soda)", "WHR": "Whirlpool", "ELUX-B.ST": "Electrolux",
 "CF": "CF Industries (üre)", "NTR": "Nutrien", "YAR.OL": "Yara", "2010.SR": "SABIC", "LYB": "LyondellBasell", "011170.KS": "Lotte Chem",
 "051910.KS": "LG Chem", "1301.TW": "Formosa Plastics", "1326.TW": "Formosa Chem&Fibre", "1303.TW": "Nan Ya",
 "EH": "eHang", "TSLA": "Tesla",
}

if __name__ == "__main__":
    rows = []
    for s, d in SYMS.items():
        p = os.path.join(SCR, "data/daily", s.replace("/", "_") + ".parquet")
        force = False
        if os.path.exists(p):
            try:
                n = len(pd.read_parquet(p)); force = n < 50
            except Exception: force = True
        r = ydl.fetch(s, "daily", force=force)
        n = len(pd.read_parquet(p)) if os.path.exists(p) else 0
        first = str(pd.read_parquet(p)["ldate"].min().date()) if n else ""
        last = str(pd.read_parquet(p)["ldate"].max().date()) if n else ""
        rows.append({"sym": s, "desc": d, "status": r, "n": n, "first": first, "last": last})
        print(s, r, n, first, last, flush=True)
        if r != "cached": time.sleep(0.25)
    pd.DataFrame(rows).to_csv(os.path.join(SCR, "out/code_cin/yahoo_fetch_status.csv"), index=False)
