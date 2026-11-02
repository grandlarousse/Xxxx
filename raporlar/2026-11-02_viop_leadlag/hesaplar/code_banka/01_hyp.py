"""Hipotez sürücüleri x 7 banka + XBANK: standart metrik seti -> res/hyp.csv (TL) ve res/hyp_usd.csv (USD bazlı banka getirisi)."""
import bk, pandas as pd, numpy as np, sys
DRV = {
 # BBVA / Avrupa bankaları
 "BBVA.MC": "BBVA Madrid", "BBVA": "BBVA ADR (NYSE)", "SAN.MC": "Santander", "UCG.MI": "UniCredit", "ISP.MI": "Intesa", "BNP.PA": "BNP", "DBK.DE": "Deutsche Bank",
 "EUFN": "MSCI Europe Financials ETF", "KBE": "S&P Bank ETF", "KRE": "S&P Regional Bank ETF", "XLF": "US Financials ETF",
 # Yunan / CEE / EM bankaları
 "ETE.AT": "NBG", "EUROB.AT": "Eurobank", "TPEIR.AT": "Piraeus", "ALBKY": "Alpha Bank ADR(OTC)", "PKO.WA": "PKO BP", "PEO.WA": "Pekao", "OTP.BD": "OTP",
 "SBK.JO": "Standard Bank", "FSR.JO": "FirstRand", "ITUB": "Itau ADR", "BBD": "Bradesco ADR",
 # Türk varlıkları ABD'de
 "TUR": "iShares MSCI Turkey ETF", "AKBTY": "Akbank ADR (OTC)", "TKGBY": "Garanti ADR (OTC)",
 # faiz / risk
 "^TNX": "UST10Y (fark)", "^FVX": "UST5Y (fark)", "2YY=F": "UST2Y vadeli (fark)", "^IRX": "UST3M (fark)", "DX-Y.NYB": "DXY", "^VIX": "VIX", "^MOVE": "MOVE",
 "EMB": "EM USD tahvil ETF", "EMLC": "EM yerel tahvil ETF", "HYG": "US HY ETF", "TLT": "UST 20y+ ETF", "CEW": "EM kur sepeti ETF", "EEM": "EM hisse ETF",
 "ZAR=X": "USDZAR", "BRL=X": "USDBRL", "MXN=X": "USDMXN", "HUF=X": "USDHUF", "PLN=X": "USDPLN", "TRY=X": "USDTRY", "EURTRY=X": "EURTRY", "EURUSD=X": "EURUSD",
 "GC=F": "Altın vadeli", "BZ=F": "Brent", "ES=F": "S&P500 vadeli", "^STOXX50E": "EuroStoxx50", "^GDAXI": "DAX", "GD.AT": "Atina genel", "EZA": "G.Afrika ETF", "EWZ": "Brezilya ETF", "EPOL": "Polonya ETF", "GREK": "Yunanistan ETF",
}
def run(usd=False):
    rows = []
    for st in bk.ALL:
        for d, desc in DRV.items():
            try:
                o = bk.pair(st, d, usd=usd); o["desc"] = desc; rows.append(o)
            except Exception as e:
                print("ERR", st, d, e, file=sys.stderr)
    df = pd.DataFrame(rows); df.to_csv(bk.RES + ("/hyp_usd.csv" if usd else "/hyp.csv"), index=False); return df
if __name__ == "__main__":
    df = run(False); dfu = run(True)
    cols = ["corr_full", "corr_3y", "corr_1y", "pcorr_xu100", "is_pc", "oos_pc", "gap_t", "gap_pc_xugap", "intra_t", "intra_is_t", "intra_oos_t", "rev_t", "rev_pc", "drift_t"]
    x = df[df.stock == "XBANK"].set_index("driver")[cols].round(2)
    x.to_csv(bk.RES + "/hyp_xbank_summary.csv"); print(x.to_string())
