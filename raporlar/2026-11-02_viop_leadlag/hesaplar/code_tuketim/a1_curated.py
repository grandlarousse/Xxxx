"""A1: hipotez güdümlü sürücü tablosu (5 hisse x seçilmiş sürücüler). Çıktı: a1_curated.csv"""
from common import *
COMMON = ["XU100", "XU030", "TRY=X", "EURTRY=X", "^GSPC", "ES=F", "^VIX", "EEM", "TUR", "^STOXX50E", "XLP", "DBA", "ZW=F", "BZ=F", "GC=F", "DX-Y.NYB"]
PEERS_BIST = ["BIMAS", "MGROS", "SOKM", "ULKER", "AEFES", "CCOLA"]
D = {
 "ULKER": ["CC=F", "ZW=F", "KE=F", "SB=F", "ZL=F", "KC=F", "ZC=F", "DBA", "MDLZ", "HSY", "NESN.SW", "BARN.SW", "LISN.SW", "LISP.SW", "GIS", "KHC", "ULVR.L", "BN.PA", "EGP=X", "KZT=X", "SAR=X"],
 "AEFES": ["CCOLA", "KO", "PEP", "CCEP", "CCH.L", "KOF", "BUD", "ABI.BR", "HEIA.AS", "CARL-B.CO", "TAP", "ALI=F", "HG=F", "RUB=X", "KZT=X", "PKR=X", "UZS=X", "GEL=X", "UAH=X", "ZC=F", "KE=F", "SB=F", "DBA"],
 "BIMAS": ["JMT.LS", "DNP.WA", "CA.PA", "AD.AS", "TSCO.L", "SBRY.L", "WMT", "COST", "TGT", "KR", "DG", "SHP.JO", "PIK.JO", "WALMEX.MX", "CRFB3.SA", "ASAI3.SA", "CPALL.BK", "AXFO.ST", "COLR.BR", "XRT", "EGP=X", "MAD=X", "ZW=F", "SB=F"],
}
D["MGROS"] = [x for x in D["BIMAS"] if x not in ("EGP=X", "MAD=X")] + ["KZT=X"]  # Migros: eski Kazakistan/Ramstore geçmişi (2019 çıkış)
D["SOKM"] = [x for x in D["BIMAS"] if x not in ("EGP=X", "MAD=X")]
rows = []
for s in STOCKS:
    drv = COMMON + [p for p in PEERS_BIST if p != s] + D[s]
    for d in drv:
        if ll.T(d) == ll.T(s): continue
        try:
            o = pair_stats(s, d)
            # USD bazlı (global sürücüler için TL kirlenmesi kontrolü)
            if not ll.is_bist(ll.T(d)) and d not in ("TRY=X", "EURTRY=X"):
                ou = pair_stats(s, d, usd=True)
                o["corr_full_usd"] = ou["corr_full"]; o["pcorr_usd"] = ou["pcorr_xu100"]
            rows.append(o); print(s, d, round(o["corr_full"], 3), round(o["pcorr_xu100"], 3), round(o.get("intra_corr", np.nan), 3), flush=True)
        except Exception as e:
            print("ERR", s, d, e)
df = pd.DataFrame(rows); df.to_csv(CODE + "/a1_curated.csv", index=False)
print(df.shape)
