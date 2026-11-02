"""A1: Hipotez listesindeki tüm sürücüler x 5 hisse, TL ve USD bazında brief standardı istatistikler.
Çıktı: res/hyp_pairs.csv"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mh, ll, pandas as pd, numpy as np
from multiprocessing import Pool

DRV = {
 # demir cevheri / çelik emtiası / enerji / kur
 "TIO=F": "Demir cevheri 62% Fe CFR Çin (CME/SGX TSI)", "HRC=F": "ABD Midwest HRC (CME, illikit)", "BUS=F": "ABD Busheling hurda (CME, çok illikit)",
 "MTF=F": "Kömür API2 CIF ARA (2025-12'de bitiyor)", "HG=F": "Bakır COMEX", "ALI=F": "Alüminyum COMEX (illikit)", "GC=F": "Altın COMEX",
 "SI=F": "Gümüş COMEX", "PL=F": "Platin NYMEX", "CL=F": "WTI ham petrol", "BZ=F": "Brent", "NG=F": "Doğal gaz HH",
 "TRY=X": "USDTRY", "DX-Y.NYB": "Dolar endeksi", "AUDUSD=X": "AUDUSD (Çin/demir proxy)", "ZAR=X": "USDZAR", "^GSPC": "S&P 500", "^TNX": "ABD 10y faiz",
 # çelik emsalleri
 "MT": "ArcelorMittal (NYSE)", "MT.AS": "ArcelorMittal (Amsterdam)", "TKA.DE": "thyssenkrupp", "SZG.DE": "Salzgitter", "VOE.VI": "voestalpine",
 "SSAB-A.ST": "SSAB", "OUT1V.HE": "Outokumpu", "APAM.AS": "Aperam", "NUE": "Nucor", "STLD": "Steel Dynamics", "CLF": "Cleveland-Cliffs",
 "CMC": "Commercial Metals (ABD inşaat demiri)", "TATASTEEL.NS": "Tata Steel", "JSWSTEEL.NS": "JSW Steel", "PKX": "POSCO ADR", "005490.KS": "POSCO Seul",
 "5401.T": "Nippon Steel", "GGB": "Gerdau", "TX": "Ternium", "SLX": "VanEck Çelik ETF", "XME": "SPDR Metal&Madencilik ETF", "PICK": "iShares küresel metal üreticileri",
 # madenciler / Çin proxy
 "VALE": "Vale", "BHP": "BHP", "RIO": "Rio Tinto", "FMG.AX": "Fortescue (ASX)", "AAL.L": "Anglo American", "GLEN.L": "Glencore", "FCX": "Freeport",
 "ASHR": "CSI300 A-pay ETF (ABD)", "FXI": "Çin büyük şirket ETF", "MCHI": "MSCI Çin ETF", "^HSI": "Hang Seng", "000001.SS": "Şanghay Bileşik (TV'de AÇILMAZ)",
 # altın madencileri
 "GLD": "SPDR Gold", "GDX": "Altın madencileri ETF", "GDXJ": "Küçük altın madencileri ETF", "NEM": "Newmont", "AEM": "Agnico Eagle", "B": "Barrick",
 "KGC": "Kinross", "SSRM": "SSR Mining (Çöpler)", "EGO": "Eldorado (Türkiye: Kışladağ/Efemçukuru)", "ELD.TO": "Eldorado (TSX)", "FRES.L": "Fresnillo",
 "CG.TO": "Centerra (eski Öksüt sahibi)", "TXG.TO": "Torex", "AU": "AngloGold", "GFI": "Gold Fields", "HMY": "Harmony", "2899.HK": "Zijin (HKEX)", "SIL": "Gümüş madencileri ETF",
 # petrol boru / OCTG
 "TS": "Tenaris (NYSE)", "TEN.MI": "Tenaris (Milano)", "OIH": "Petrol servis ETF", "XOP": "E&P ETF", "XLE": "Enerji ETF",
 # Türkiye / BIST ilişkili
 "TUR": "iShares MSCI Türkiye ETF", "XUSIN.IS": "BIST Sınai", "ISDMR.IS": "İsdemir (Erdemir bağlı ort.)", "KRDMA.IS": "Kardemir A", "KRDMB.IS": "Kardemir B",
 "TRENJ.IS": "TR Doğal Enerji (eski İpek, Koza grubu)", "EREGL.IS": "Ereğli", "KRDMD.IS": "Kardemir D", "TRALT.IS": "Türk Altın", "TRMET.IS": "TR Anadolu Metal", "BRSAN.IS": "Borusan Boru",
}

def one(stock, drv, usd):
    try:
        if drv == "ONS_TL":
            s = mh.pair_stats(stock, drv, usd=usd, drv_series=mh.onsTL(), drv_name="ONS_TL")
        else:
            if drv.replace(".IS", "") == stock: return None
            s = mh.pair_stats(stock, drv, usd=usd)
        s["driver_desc"] = DRV.get(drv, "Ons altın TL (GC=F+USDTRY)")
        return s
    except Exception as e:
        print("ERR", stock, drv, e); return None

if __name__ == "__main__":
    jobs = [(s, d, u) for s in mh.STOCKS for d in list(DRV) + ["ONS_TL"] for u in (False, True)]
    # USD bazı sadece BIST dışı sürücüler için anlamlı; BIST içi çiftlerde de hesaplanır ama TL esas
    with Pool(4) as pool: rows = pool.starmap(one, jobs, chunksize=4)
    df = pd.DataFrame([r for r in rows if r])
    df.to_csv(os.path.join(mh.RES, "hyp_pairs.csv"), index=False)
    print(df.shape)
