"""A1: hipotez çiftleri -> standart metrik tablosu (out/code_kimya/res_hyp.csv)."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kc import *

FERT = ["CF", "NTR", "MOS", "YAR.OL", "ICL", "IPI", "LXU", "OCI.AS", "SQM", "UAN", "CVR", "2020.SR", "ABUK.CA", "MFPC.CA", "ATT.WA", "SDF.DE"]
GAS = ["TTF=F", "NG=F"]
GRAIN = ["ZW=F", "ZC=F", "ZS=F", "KE=F", "DBA", "MOO"]
AGRO = ["CTVA", "FMC", "BAYN.DE", "UPL.NS", "NUF.AX", "SUMICHEM.NS", "KWS.DE"]
EPC = ["FLR", "KBR", "J", "ACS.MC", "FER.MC", "HOT.DE", "SKA-B.ST"]
GLASS = ["SGO.PA", "OI", "VID.MC", "VRLA.PA", "5201.T", "GLW", "AMBP"]
SODA = ["SOLB.BR", "SYENS.BR", "GEL", "NRP", "TATACHEM.NS"]
CEM = ["HEI.DE", "HOLN.SW", "CX", "BZU.MI", "TITC.BR", "TITC.AT", "CRH", "VMC", "MLM", "EXP", "1101.TW"]
CEM_COST = ["MTF=F", "BTU", "BZ=F", "CL=F"]
CONSTR = ["XLB", "XHB", "ITB"]
TRCEM = ["AKCNS.IS", "NUHCM.IS", "BTCIM.IS", "AFYON.IS", "BUCIM.IS", "KONYA.IS"]
MACRO = ["TRY=X", "EURTRY=X", "EURUSD=X", "^STOXX", "^GDAXI", "^GSPC", "ACWI", "BZ=F", "GC=F", "^VIX"]
TRCHEM = ["BAGFS.IS", "EGGUB.IS", "ALKIM.IS"]

H = {
    "GUBRF": FERT + GAS + GRAIN + MACRO + ["HEKTS.IS", "TKFEN.IS", "BAGFS.IS", "EGGUB.IS", "^OVX"],
    "HEKTS": AGRO + FERT[:6] + GRAIN + MACRO + ["GUBRF.IS", "OYAKC.IS", "TKFEN.IS", "BTC-USD"],
    "TKFEN": ["CF", "YAR.OL", "NTR", "MOS", "OCI.AS"] + EPC + GAS + GRAIN[:3] + MACRO + ["ENKAI.IS", "GUBRF.IS", "HEKTS.IS", "KZT=X", "AZN=X"],
    "SISE": GLASS + SODA + GAS + MACRO + ["XLB", "ISCTR.IS", "XBANK.IS", "TRKCM.IS", "KCHOL.IS"],
    "CIMSA": CEM + CEM_COST + CONSTR + TRCEM + MACRO + ["OYAKC.IS", "SAHOL.IS", "EKGYO.IS", "SGO.PA", "TTF=F"],
    "OYAKC": CEM + CEM_COST + CONSTR + TRCEM + MACRO + ["CIMSA.IS", "HEKTS.IS", "EKGYO.IS", "SGO.PA", "TTF=F"],
}

if __name__ == "__main__":
    rows = []
    for s, drvs in H.items():
        for d in dict.fromkeys(drvs):
            try:
                o = pair(s, d)
            except Exception as e:
                print("skip", s, d, e); continue
            rows.append(o)
            print(f"{s:6s} {d:12s} c={o['corr_full']:+.2f} c3={o['corr_3y']:+.2f} c1={o['corr_1y']:+.2f} pc={o['pc_full']:+.2f} pcx={o['pc_ext']:+.2f} IS/OOS={o['pc_IS']:+.2f}/{o['pc_OOS']:+.2f} yrs={o['yrs_same_sign']:.2f} "
                  f"gap1={o['gap_l1']:+.2f} intra1={o['intra_l1']:+.3f}(t{o['intra_l1_t']:+.1f}) drift={o['drift_2_5']:+.3f}(t{o['drift_2_5_t']:+.1f}) rev={o['rev_l1']:+.3f}(t{o['rev_l1_t']:+.1f}) n={o['n']}", flush=True)
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "res_hyp.csv"), index=False)
