"""A1: hipotez güdümlü çift testleri: 3 hisse x ~60 sürücü. Çıktı: res/a1_pairs.csv"""
from h import *

DRV = {
 # yakıt
 "BZ=F": "Brent vadeli", "CL=F": "WTI vadeli", "HO=F": "Heating oil (jet proxy)", "RB=F": "RBOB benzin", "^OVX": "Petrol vol endeksi",
 # Avrupa havayolu
 "LHA.DE": "Lufthansa", "AF.PA": "Air France-KLM", "IAG.L": "IAG", "RYA.IR": "Ryanair (Dublin)", "RYAAY": "Ryanair ADR (ABD)",
 "WIZZ.L": "Wizz Air", "EZJ.L": "easyJet", "JET2.L": "Jet2", "AEGN.AT": "Aegean", "NAS.OL": "Norwegian", "FIA1S.HE": "Finnair",
 # ABD/Asya havayolu
 "DAL": "Delta", "UAL": "United", "AAL": "American", "LUV": "Southwest", "ALK": "Alaska Air", "JBLU": "JetBlue", "JETS": "US Global Jets ETF",
 "CPA": "Copa", "9201.T": "Japan Airlines", "9202.T": "ANA", "ELAL.TA": "El Al",
 # havalimanı
 "ADP.PA": "Groupe ADP", "FRA.DE": "Fraport", "AENA.MC": "Aena", "FHZN.SW": "Flughafen Zürich",
 # turizm
 "TUI1.DE": "TUI", "BKNG": "Booking", "EXPE": "Expedia", "ABNB": "Airbnb", "TCOM": "Trip.com ADR", "CCL": "Carnival", "RCL": "Royal Caribbean",
 "MAR": "Marriott", "AC.PA": "Accor", "MEL.MC": "Melia",
 # üretici / kiralama
 "BA": "Boeing", "AIR.PA": "Airbus", "SAF.PA": "Safran", "MTX.DE": "MTU Aero", "EMBJ": "Embraer", "AER": "AerCap",
 # kur / risk / endeks
 "EURUSD=X": "EURUSD", "TRY=X": "USDTRY", "EURTRY=X": "EURTRY", "DX-Y.NYB": "DXY", "^VIX": "VIX", "^TA125.TA": "TA-125 İsrail",
 "^STOXX": "STOXX600", "^GSPC": "S&P500", "ES=F": "S&P500 vadeli", "TUR": "iShares Türkiye ETF (ABD)", "TKC": "Turkcell ADR",
 "GC=F": "Altın", "^TNX": "ABD 10y faiz",
 # yurt içi
 "THYAO.IS": "THYAO", "PGSUS.IS": "PGSUS", "TAVHL.IS": "TAVHL", "CLEBI.IS": "Çelebi Hava Servisi", "XU100.IS": "BIST100",
}

if __name__ == "__main__":
    rows = []
    jc = jet_crack()
    for st in STOCKS:
        for d, desc in list(DRV.items()) + [("JETCRACK", "Jet crack (HO*42-Brent)/Brent")]:
            if d == st + ".IS": continue
            try:
                o = stat_block(st, jc if d == "JETCRACK" else d, drv_name=d)
                o["desc"] = desc; rows.append(o)
            except Exception as e:
                print("ERR", st, d, e)
        # USD bazlı tekrar (yalnız seçili)
        for d in ["BZ=F", "HO=F", "LHA.DE", "AF.PA", "RYAAY", "JETS", "DAL", "ADP.PA", "EURUSD=X", "TRY=X", "^VIX", "^STOXX", "^GSPC"]:
            o = stat_block(st, d, usd=True); o["desc"] = DRV.get(d, d) + " [hisse USD]"; rows.append(o)
    df = pd.DataFrame(rows)
    df.to_csv(RES + "/a1_pairs.csv", index=False)
    pd.set_option("display.width", 250); pd.set_option("display.max_rows", 500)
    cols = ["stock", "driver", "n", "corr_full", "corr_3y", "corr_1y", "pcorr_xu100", "pc_IS", "pc_OOS", "yrs_pc_same_sign", "beta", "corr_lag1", "t_lag1", "gap_corr", "gap_t", "intra_corr", "intra_t", "xintra_corr", "xintra_t", "drift5_corr", "drift5_t", "rev_corr", "rev_t"]
    print(df[cols].round(3).to_string())
