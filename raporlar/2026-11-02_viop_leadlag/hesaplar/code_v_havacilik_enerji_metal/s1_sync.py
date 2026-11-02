"""S1: senkron iddialar — corr / XU100 kısmi / ortak faktör (XU100+USDTRY+EEM [+bölge/sektör]) / yıl işareti / haftalık / gecikme tanısı."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_havacilik_enerji_metal")
import vlib as V
RES = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_havacilik_enerji_metal/res"
R = {}
def r(s):
    if s not in R:
        if s == "EUSTEEL4":
            R[s] = pd.concat([r(x) for x in ["MT.AS", "SSAB-A.ST", "VOE.VI", "SZG.DE"]], axis=1).mean(axis=1, skipna=False)
        elif s == "EUSTEEL3":
            R[s] = pd.concat([r(x) for x in ["MT.AS", "SSAB-A.ST", "VOE.VI"]], axis=1).mean(axis=1, skipna=False)
        else: R[s] = V.ret(s)
    return R[s]
XU, FX, EEM, ES, SX = "XU100.IS", "TRY=X", "EEM", "ES=F", "^STOXX"
# (claim, stock, driver, iddia_pc, ek kontroller (bölge/sektör))
PAIRS = [
 ("A1", "THYAO.IS", "LHA.DE", 0.18, [SX]), ("A1", "THYAO.IS", "EZJ.L", 0.16, [SX]), ("A1", "THYAO.IS", "IAG.L", 0.15, [SX]),
 ("A1", "PGSUS.IS", "EZJ.L", 0.17, [SX]), ("A1x", "PGSUS.IS", "IAG.L", 0.15, [SX]), ("A1x", "PGSUS.IS", "LHA.DE", 0.14, [SX]),
 ("A2", "THYAO.IS", "PGSUS.IS", 0.51, ["XBANK.IS", "XUSIN.IS"]),
 ("A3", "TAVHL.IS", "ADP.PA", 0.13, [SX]),
 ("E1", "TUPRS.IS", "CRAK", 0.17, [ES]), ("E1b", "TUPRS.IS", "CRAK", 0.17, [ES, "BZ=F"]),
 ("E2", "TUPRS.IS", "BZ=F", 0.16, [ES]),
 ("M1", "EREGL.IS", "ISDMR.IS", 0.45, ["XBANK.IS", "XUSIN.IS"]), ("M1", "EREGL.IS", "KRDMD.IS", 0.34, ["XBANK.IS", "XUSIN.IS"]),
 ("M2", "TRALT.IS", "GC=F", 0.22, [ES]),
 ("M5", "EREGL.IS", "EUSTEEL4", 0.12, [SX]), ("M5", "EREGL.IS", "EUSTEEL3", 0.12, [SX]),
 ("M5", "EREGL.IS", "MT.AS", 0.12, [SX]), ("M5", "EREGL.IS", "SSAB-A.ST", 0.12, [SX]), ("M5", "EREGL.IS", "VOE.VI", None, [SX]), ("M5", "EREGL.IS", "SZG.DE", None, [SX]),
]
rows = []
for cid, st, dr, claim, extra in PAIRS:
    a, b = r(st), r(dr)
    c1 = [r(XU)]; c3 = [r(XU), r(FX), r(EEM)]; c4 = c3 + [r(x) for x in extra]
    row = {"claim": cid, "stock": st, "driver": dr, "iddia_pc": claim, "ek_kontrol": "+".join(extra)}
    for k, (s, e) in V.PER.items():
        c, n, _ = V.pcorr(a, b, None, s, e); row[f"c_{k}"] = c; row[f"n_{k}"] = n
        row[f"pc1_{k}"] = V.pcorr(a, b, c1, s, e)[0]
        row[f"pc3_{k}"] = V.pcorr(a, b, c3, s, e)[0]
        row[f"pc4_{k}"] = V.pcorr(a, b, c4, s, e)[0]
    row["pc1_nwt"] = V.pc_nwt(a, b, c1, "2010-01-01")
    row["pc4_nwt"] = V.pc_nwt(a, b, c4, "2010-01-01")
    y = V.byyear(a, b, c1); sgn = np.sign(row["pc1_tam"])
    row["yil_ayni_isaret"] = f"{int((np.sign(y) == sgn).sum())}/{len(y)}"; row["yil_min"] = y.min(); row["yil_max"] = y.max()
    y4 = V.byyear(a, b, c4); row["yil4_ayni_isaret"] = f"{int((np.sign(y4) == np.sign(row['pc4_tam'])).sum())}/{len(y4)}"
    # gecikme tanısı (2010+): sürücü önde / hisse önde, XU100 kontrollü
    row["pc1_drv_lag1"] = V.pcorr(a, b.shift(1), [r(XU)], "2010-01-01")[0]
    row["pc1_stk_lag1"] = V.pcorr(a.shift(1), b, [r(XU)], "2010-01-01")[0]
    # haftalık
    W = {k: V.wk(v) for k, v in {"a": a, "b": b, "xu": r(XU), "fx": r(FX), "eem": r(EEM)}.items()}
    for k, (s, e) in [("tam", ("2010-01-01", None)), ("IS", ("2014-01-01", "2020-12-31")), ("OOS", ("2021-01-01", None))]:
        row[f"w_c_{k}"] = V.pcorr(W["a"], W["b"], None, s, e)[0]
        row[f"w_pc1_{k}"] = V.pcorr(W["a"], W["b"], [W["xu"]], s, e)[0]
        row[f"w_pc3_{k}"] = V.pcorr(W["a"], W["b"], [W["xu"], W["fx"], W["eem"]], s, e)[0]
    row["w_n"] = V.pcorr(W["a"], W["b"], [W["xu"]], "2010-01-01")[1]
    wy = V.byyear(W["a"], W["b"], [W["xu"]], minn=30)
    row["w_yil_ayni"] = f"{int((np.sign(wy) == np.sign(row['w_pc1_tam'])).sum())}/{len(wy)}"
    rows.append(row)
    if cid in ("M2",):
        wy.to_csv(f"{RES}/s1_M2_weekly_pc_byyear.csv")
        print("M2 haftalık yıllık pc(XU100):", wy.round(2).to_dict())
        wy3 = V.byyear(W["a"], W["b"], [W["xu"], W["fx"]], minn=30); print("M2 haftalık yıllık pc(XU100+USDTRY):", wy3.round(2).to_dict())
    print(cid, st, dr, "pc1 tam %.3f IS %.3f OOS %.3f 1y %.3f | pc3 %.3f | pc4 %.3f | yıl %s | w_pc1 %.3f" % (row["pc1_tam"], row["pc1_IS"], row["pc1_OOS"], row["pc1_1y"], row["pc3_tam"], row["pc4_tam"], row["yil_ayni_isaret"], row["w_pc1_tam"]), flush=True)
D = pd.DataFrame(rows); D.to_csv(f"{RES}/s1_sync.csv", index=False)
pd.set_option("display.width", 250)
print(D[["claim", "stock", "driver", "iddia_pc", "n_tam", "c_tam", "c_1y", "pc1_tam", "pc1_IS", "pc1_OOS", "pc1_1y", "pc1_nwt", "pc3_tam", "pc3_IS", "pc3_OOS", "pc4_tam", "pc4_IS", "pc4_OOS", "pc4_nwt", "yil_ayni_isaret", "yil4_ayni_isaret", "pc1_drv_lag1", "pc1_stk_lag1"]].round(3).to_string())
print(D[["claim", "stock", "driver", "w_n", "w_c_tam", "w_pc1_tam", "w_pc1_IS", "w_pc1_OOS", "w_pc3_tam", "w_pc3_IS", "w_pc3_OOS", "w_yil_ayni"]].round(3).to_string())
