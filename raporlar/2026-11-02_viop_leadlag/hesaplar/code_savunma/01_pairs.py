"""01: Hipotez sürücüleri için standart metrikler (senkron, kısmi, lag1 gap/intra, IS/OOS, ters yön)."""
from sv import *

DEF_LIST = ["XU100", "EU_DEF", "US_DEF", "KR_DEF", "RHM.DE", "BA.L", "LDO.MI", "HO.PA", "SAAB-B.ST", "HAG.DE", "R3NK.DE", "KOG.OL",
            "CSG.AS", "EUAD", "AIR.DE", "AM.PA", "QQ.L", "CHG.L", "BAB.L", "IDR.MC", "EXA.PA", "MTX.DE",
            "ITA", "XAR", "PPA", "LMT", "NOC", "RTX", "GD", "LHX", "HII", "KTOS", "AVAV", "PLTR",
            "012450.KS", "064350.KS", "079550.KS", "047810.KS", "7011.T", "7012.T", "7013.T", "ESLT",
            "OTKAR.IS", "TUR", "FXAL", "^GDAXI", "^STOXX", "ES=F", "GC=F", "BZ=F", "^VIX"]
TEL_LIST = ["XU100", "TKC", "TUR", "FXAL", "EURTRY_AL", "VEON", "KYIV", "VOD", "VOD.L", "MTN.JO", "VOD.JO", "DTE.DE", "ORA.PA", "TEF.MC",
            "OPL.WA", "TEL.OL", "TELIA.ST", "KPN.AS", "HTO.AT", "MTELEKOM.BD", "AMX", "TIMB", "IHS", "7010.SR", "BHARTIARTL.NS",
            "EU_TEL", "EM_TEL", "EEM", "^STOXX", "ES=F", "^VIX"]
rows = []
for d in DEF_LIST: rows.append(pair("ASELS", d))
for st in ["TCELL", "TTKOM"]:
    lst = TEL_LIST + (["TTKOM.IS"] if st == "TCELL" else ["TCELL.IS"]) + ["ASELS.IS"]
    for d in lst: rows.append(pair(st, d))
df = pd.DataFrame(rows)
df.to_csv(RES + "/01_pairs.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40); pd.set_option("display.max_rows", 300)
cols = ["stock", "driver", "n", "corr_full", "corr_3y", "corr_1y", "pcorr_xu100", "pc_is", "pc_oos", "beta", "yr_same_sign",
        "lag1_cc", "lag1_cc_t", "gap_l1", "gap_l1_t", "intra_l1", "intra_l1_t", "intra_l1_is", "intra_l1_oos", "gap_l0", "intra_l0", "intra_l0_t", "lag2_5_t", "rev_l1", "rev_l1_t"]
print(fmt(df[cols], nd=3).to_string())
