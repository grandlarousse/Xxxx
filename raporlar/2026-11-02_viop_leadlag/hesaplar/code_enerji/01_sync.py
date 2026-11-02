"""Hipotez güdümlü çift testleri: 6 hisse x sürücü listesi. Senkron (günlük+haftalık), kısmi (XU100), lag1 gap/intra, ters yön, stabilite.
TL ve USD bazlı (hisse - USDTRY) iki versiyon."""
import pandas as pd, numpy as np, elib
from elib import R, summary

cr = elib.crack_ret()
ptf = elib.ptf_daily()

def ptf_series(col="tl"):
    """L_t = log PTF'nin (t-5..t+1) 7 günlük ortalaması; t+1 PTF'si t günü ~11:00 UTC'de ilan edilir -> L_t BIST seansı t sırasında bilinir.
    Hafta içi/sonu mevsimselliği 7 gün ortalamasıyla yok olur. Getiri = L_t - L_{t-1} (BIST takviminde)."""
    lp = np.log(ptf[col].clip(lower=1))
    m7 = lp.rolling(7).mean()              # index d: (d-6..d) ortalaması
    m7_known = m7.shift(-1)                 # BIST günü t'de bilinen: (t-5..t+1)
    cal = elib.ll.bist_cal()
    s = m7_known.reindex(m7_known.index.union(cal)).ffill().reindex(cal)
    s = s[s.index <= ptf.index.max() - pd.Timedelta(days=1)]
    return s.diff()

DRV = {}
def add(k, s, desc, tv): DRV[k] = (s, desc, tv)
for s, d, tv in [
    ("BZ=F", "Brent vadeli", "ICEEUR:BRN1! / TVC:UKOIL"), ("CL=F", "WTI vadeli", "NYMEX:CL1!"),
    ("HO=F", "NY ULSD (dizel/ısınma yakıtı) vadeli", "NYMEX:HO1!"), ("RB=F", "RBOB benzin vadeli", "NYMEX:RB1!"),
    ("NG=F", "Henry Hub doğalgaz", "NYMEX:NG1!"), ("TTF=F", "Hollanda TTF gaz", "ICEENDEX:TFM1!"), ("MTF=F", "Rotterdam kömür (API2)", "ICEEUR:ATW1! ?"),
    ("KRBN", "Küresel karbon ETF", "AMEX:KRBN"), ("GC=F", "Altın vadeli", "COMEX:GC1!"), ("TRY=X", "USDTRY", "FX:USDTRY"), ("EURUSD=X", "EURUSD", "FX:EURUSD"),
    ("CRAK", "Rafineri ETF", "AMEX:CRAK"), ("VLO", "Valero", "NYSE:VLO"), ("MPC", "Marathon Petroleum", "NYSE:MPC"), ("PSX", "Phillips 66", "NYSE:PSX"),
    ("PBF", "PBF Energy", "NYSE:PBF"), ("DK", "Delek US", "NYSE:DK"), ("PKN.WA", "Orlen", "GPW:PKN"), ("MOL.BD", "MOL", "BET:MOL"),
    ("MOH.AT", "Motor Oil Hellas", "ATHEX:MOH"), ("ELPE.AT", "Helleniq Energy", "ATHEX:ELPE"), ("NESTE.HE", "Neste", "OMXHEX:NESTE"),
    ("GALP.LS", "Galp", "EURONEXT:GALP"), ("REP.MC", "Repsol", "BME:REP"), ("OMV.VI", "OMV", "VIE:OMV"), ("XLE", "ABD enerji ETF", "AMEX:XLE"),
    ("LYB", "LyondellBasell", "NYSE:LYB"), ("DOW", "Dow", "NYSE:DOW"), ("BAS.DE", "BASF", "XETR:BAS"), ("WLK", "Westlake", "NYSE:WLK"),
    ("051910.KS", "LG Chem", "KRX:051910"), ("011170.KS", "Lotte Chemical", "KRX:011170"), ("2010.SR", "SABIC", "TADAWUL:2010"),
    ("PTTGC.BK", "PTT Global Chemical", "SET:PTTGC"), ("1301.TW", "Formosa Plastics", "TWSE:1301"), ("1303.TW", "Nan Ya Plastics", "TWSE:1303"),
    ("1326.TW", "Formosa Chemicals & Fibre", "TWSE:1326"), ("IVL.BK", "Indorama Ventures", "SET:IVL"), ("ALPEKA.MX", "Alpek", "BMV:ALPEKA"),
    ("RELIANCE.NS", "Reliance Industries", "NSE:RELIANCE"), ("3402.T", "Toray", "TSE:3402"), ("CT=F", "Pamuk vadeli (polyester ikamesi)", "ICEUS:CT1!"),
    ("EOAN.DE", "E.ON", "XETR:EOAN"), ("RWE.DE", "RWE", "XETR:RWE"), ("ENEL.MI", "Enel", "MIL:ENEL"), ("IBE.MC", "Iberdrola", "BME:IBE"),
    ("ENGI.PA", "Engie", "EURONEXT:ENGI"), ("EDP.LS", "EDP", "EURONEXT:EDP"), ("PGE.WA", "PGE", "GPW:PGE"), ("CEZ.PR", "CEZ", "PSECZ:CEZ ?"),
    ("PPC.AT", "PPC (DEI)", "ATHEX:PPC"), ("ICLN", "Temiz enerji ETF", "NASDAQ:ICLN"), ("TAN", "Güneş ETF", "AMEX:TAN"), ("VWS.CO", "Vestas", "OMXCOP:VWS"),
    ("ORSTED.CO", "Orsted", "OMXCOP:ORSTED"), ("BTU", "Peabody (kömür)", "NYSE:BTU"), ("XLU", "ABD utilities ETF", "AMEX:XLU"), ("GDX", "Altın madencileri ETF", "AMEX:GDX"),
    ("^STOXX", "STOXX 600", "TVC:SXXP ?"), ("ES=F", "S&P500 vadeli", "CME_MINI:ES1!"), ("EEM", "Gelişen piyasalar ETF", "AMEX:EEM"), ("TUR", "iShares Türkiye ETF", "NASDAQ:TUR"),
]:
    try: add(s, R(s), d, tv)
    except Exception as e: print("yok", s, e)
add("HO_CRACK", cr["d_ho_crack"], "Dizel crack (HO*42-BZ) değişimi / Brent", "NYMEX:HO1!*42-ICEEUR:BRN1!")
add("RB_CRACK", cr["d_rb_crack"], "Benzin crack (RB*42-BZ) değişimi / Brent", "NYMEX:RB1!*42-ICEEUR:BRN1!")
add("C321", cr["d_c321"], "3-2-1 crack değişimi / Brent", "(2*RB1!*42+HO1!*42-3*BRN1!)/3")
add("HOxBZ", cr["hoxbz"], "log(HO/BZ) değişimi", "NYMEX:HO1!/ICEEUR:BRN1!")
add("PTF_TL", ptf_series("tl"), "Türkiye PTF 7g ort. değişimi (TL)", "yok (EPİAŞ)")
add("PTF_USD", ptf_series("usd"), "Türkiye PTF 7g ort. değişimi (USD)", "yok (EPİAŞ)")
for s in ["TUPRS", "PETKM", "SASA", "AKSEN", "ENJSA", "ODAS", "XU100", "XBANK", "AYGAZ", "AKSA", "ZOREN"]:
    if s not in ["XU100"]:
        try: add(s + ".IS", R(s), "BIST " + s, "BIST:" + s)
        except Exception as e: print("yok", s, e)

STK = {
 "TUPRS": ["BZ=F", "CL=F", "HO=F", "RB=F", "HO_CRACK", "RB_CRACK", "C321", "HOxBZ", "CRAK", "VLO", "MPC", "PSX", "PBF", "DK", "PKN.WA", "MOL.BD", "MOH.AT", "ELPE.AT", "NESTE.HE", "GALP.LS", "REP.MC", "OMV.VI", "XLE", "TRY=X", "EURUSD=X", "NG=F", "TTF=F", "AYGAZ.IS", "PETKM.IS", "ES=F", "^STOXX", "EEM", "TUR"],
 "PETKM": ["BZ=F", "CL=F", "HO_CRACK", "NG=F", "TTF=F", "LYB", "DOW", "BAS.DE", "WLK", "051910.KS", "011170.KS", "2010.SR", "PTTGC.BK", "1301.TW", "1303.TW", "1326.TW", "IVL.BK", "TRY=X", "EURUSD=X", "TUPRS.IS", "SASA.IS", "AKSA.IS", "ES=F", "^STOXX", "EEM", "TUR"],
 "SASA": ["BZ=F", "CL=F", "IVL.BK", "ALPEKA.MX", "RELIANCE.NS", "1326.TW", "1303.TW", "3402.T", "CT=F", "LYB", "BAS.DE", "TRY=X", "EURUSD=X", "PETKM.IS", "AKSA.IS", "ES=F", "EEM", "TUR"],
 "AKSEN": ["TTF=F", "NG=F", "MTF=F", "KRBN", "BZ=F", "PTF_TL", "PTF_USD", "EOAN.DE", "RWE.DE", "ENEL.MI", "IBE.MC", "ENGI.PA", "EDP.LS", "PGE.WA", "CEZ.PR", "PPC.AT", "ICLN", "TAN", "VWS.CO", "ORSTED.CO", "XLU", "TRY=X", "EURUSD=X", "ENJSA.IS", "ODAS.IS", "ZOREN.IS", "ES=F", "^STOXX", "EEM", "TUR"],
 "ENJSA": ["TTF=F", "NG=F", "MTF=F", "KRBN", "BZ=F", "PTF_TL", "PTF_USD", "EOAN.DE", "RWE.DE", "ENEL.MI", "IBE.MC", "ENGI.PA", "EDP.LS", "PGE.WA", "CEZ.PR", "PPC.AT", "ICLN", "XLU", "TRY=X", "EURUSD=X", "AKSEN.IS", "ODAS.IS", "XBANK.IS", "ES=F", "^STOXX", "EEM", "TUR"],
 "ODAS": ["GC=F", "GDX", "MTF=F", "BTU", "TTF=F", "NG=F", "KRBN", "BZ=F", "PTF_TL", "PTF_USD", "EOAN.DE", "RWE.DE", "PGE.WA", "CEZ.PR", "PPC.AT", "ICLN", "TRY=X", "EURUSD=X", "AKSEN.IS", "ENJSA.IS", "ZOREN.IS", "ES=F", "EEM", "TUR"],
}
ASIA0 = {"051910.KS", "011170.KS", "1301.TW", "1303.TW", "1326.TW", "3402.T"}  # BIST açılışı (07:00 UTC) öncesi kapanır
rows = []
for stk, drvs in STK.items():
    for dk in drvs:
        s, desc, tv = DRV[dk]
        for usd in [False, True]:
            o = summary(stk, s, name=dk, usd=usd, lag_asia0=dk in ASIA0)
            o.update({"driver_desc": desc, "tv_ticker": tv, "base": "USD" if usd else "TL"})
            rows.append(o)
    print(stk, "ok", flush=True)
df = pd.DataFrame(rows)
df.to_csv(elib.RES + "/sync_pairs.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 500)
cols = ["stock", "driver_yahoo", "base", "corr_full", "corr_3y", "corr_1y", "pcorr_xu100", "corr_lag1", "corr_w", "pcorr_w_xu100", "beta", "gap_lag1_corr", "gap_lag1_t", "intra_lag1_corr", "intra_lag1_t", "reverse_corr", "yr_same_sign", "is_corr", "oos_corr", "pc_is", "pc_oos", "n"]
print(df[df.base == "TL"][cols].round(3).to_string())
