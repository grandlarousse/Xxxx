"""S1: M4 iddiasının birebir yeniden üretimi (kendi kodumla). JP/AU z-kompoziti (t) -> EREGL/KRDMD intra_t; FMG.AX (t) -> intra korelasyonu.
Çıktı: res_s1.csv"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v, numpy as np, pandas as pd
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 50)
JP_AU = ["5411.T", "5401.T", "6301.T", "FMG.AX", "BHP.AX"]
rows = []
comp = v.composite(JP_AU)
xu = v.decomp("XU100.IS")
for st in ["EREGL.IS", "KRDMD.IS", "BRSAN.IS", "XU100.IS"]:
    d = v.decomp(st)
    a = d["intra"]; m = xu["intra"]
    df = pd.concat([a, m], axis=1).dropna(); beta = np.polyfit(df.iloc[:, 1], df.iloc[:, 0], 1)[0]
    hed = a - beta * m
    for tgt_name, tgt in [("intra", a), ("hedged_fullbeta", hed)]:
        for cost in (8, 15):
            for mode, thr in [("sign", 0.0), ("z", 1.0)]:
                res, pnl, pos = v.bt(comp, tgt, cost=cost, mode=mode, thr=thr)
                rows.append({"stock": st, "signal": "JP_AU_comp", "target": tgt_name, "cost": cost, "mode": f"{mode}{thr}", **v.flat(res)})
R = pd.DataFrame(rows); R.to_csv(os.path.join(v.OUT, "res_s1.csv"), index=False)
print(R[["stock", "target", "cost", "mode", "IS_n", "IS_bps", "IS_t", "OOS_n", "OOS_bps", "OOS_t", "OOS_sh", "yrs_pos"]].round(2).to_string())
for _, r in R[(R["mode"] == "z1.0") & (R.cost == 15)].iterrows(): print(r.stock, r.target, r.by_year)
# FMG.AX korelasyon / NW t (Çin ajanı iddiası t 4,4/3,9/3,5)
fmg = v.ret("FMG.AX")
print("\nFMG.AX(t) -> intra_t corr, NW t (tam / IS / OOS)")
for st in ["KRDMD.IS", "EREGL.IS", "BRSAN.IS", "XU100.IS", "TRALT.IS", "TRMET.IS"]:
    i = v.decomp(st)["intra"]
    c, t, n = v.corr_t(i, fmg); cI, tI, nI = v.corr_t(i[i.index < v.SPLIT], fmg); cO, tO, nO = v.corr_t(i[i.index >= v.SPLIT], fmg)
    print(f"{st:10s} r={c:.3f} t={t:.2f} n={n} | IS r={cI:.3f} t={tI:.2f} | OOS r={cO:.3f} t={tO:.2f} n={nO}")
print("\nKompozit(t) -> intra_t corr")
for st in ["KRDMD.IS", "EREGL.IS", "BRSAN.IS", "XU100.IS"]:
    i = v.decomp(st)["intra"]; g = v.decomp(st)["gap"]
    c, t, n = v.corr_t(i, comp); cg, tg, _ = v.corr_t(g, comp)
    print(f"{st:10s} intra r={c:.3f} t={t:.2f} n={n} | gap r={cg:.3f} t={tg:.2f}")
