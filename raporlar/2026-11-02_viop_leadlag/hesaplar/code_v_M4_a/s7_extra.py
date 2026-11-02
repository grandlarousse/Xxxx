"""S7: (a) FMG.AX tek başına backtest (kaynakla aynı tanım: ham getiri -> z|>1), EREGL/KRDMD/BRSAN; (b) a-priori çelik+cevher kompoziti (Komatsu'suz);
(c) IS-only seçilmiş kompozitin OOS korelasyon t'si; (d) yıllık tablo (n, bps 8/15, hedge).
Çıktı: res_s7_*.csv"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v, numpy as np, pandas as pd
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 200)
JP_AU = ["5411.T", "5401.T", "6301.T", "FMG.AX", "BHP.AX"]
D = {s: v.decomp(s) for s in ["EREGL.IS", "KRDMD.IS", "BRSAN.IS", "XU100.IS"]}
rows = []
fmg = v.ret("FMG.AX")
for st in ["EREGL.IS", "KRDMD.IS", "BRSAN.IS"]:
    for cost in (8, 15):
        for mode, thr in [("sign", 0.0), ("z", 1.0)]:
            res, _, _ = v.bt(fmg, D[st]["intra"], cost=cost, mode=mode, thr=thr)
            rows.append({"test": "FMG.AX ham(t)", "stock": st, "cost": cost, "mode": f"{mode}{thr}", **v.flat(res)})
APR = ["5411.T", "5401.T", "005490.KS", "004020.KS", "FMG.AX", "BHP.AX", "RIO.AX"]
ap = v.composite(APR)
for st in ["EREGL.IS", "KRDMD.IS", "BRSAN.IS"]:
    for cost in (8, 15):
        res, _, _ = v.bt(ap, D[st]["intra"], cost=cost); rows.append({"test": "a-priori çelik+cevher (Komatsu yok, 7)", "stock": st, "cost": cost, "mode": "z1.0", **v.flat(res)})
    for nm, sel in [("IS-only top5 EREGL", ['6301.T', '5411.T', '4005.T', '7012.T', '7261.T']), ("IS-only top5 KRDMD", ['6301.T', '7012.T', 'IGO.AX', '7011.T', 'BHP.AX'])]:
        if nm.split()[-1] not in st: continue
        sig = v.composite(sel)
        for per, sub in [("IS", D[st]["intra"][D[st].index < v.SPLIT]), ("OOS", D[st]["intra"][D[st].index >= v.SPLIT])]:
            c, t, n = v.corr_t(sub, sig); print(f"{nm} {per}: corr={c:.3f} t={t:.2f} n={n}")
    for per, sub in [("IS", D[st]["intra"][D[st].index < v.SPLIT]), ("OOS", D[st]["intra"][D[st].index >= v.SPLIT])]:
        c, t, n = v.corr_t(sub, ap); print(f"a-priori 7 {st} {per}: corr={c:.3f} t={t:.2f} n={n}")
R = pd.DataFrame(rows); R.to_csv(os.path.join(v.OUT, "res_s7_extra.csv"), index=False)
print(R[["test", "stock", "cost", "mode", "IS_n", "IS_bps", "IS_t", "OOS_n", "OOS_bps", "OOS_t", "OOS_sh", "yrs_pos"]].round(2).to_string(index=False))
# yıllık tablo
comp = v.composite(JP_AU)
Y = []
for st in ["EREGL.IS", "KRDMD.IS"]:
    a = D[st]["intra"]; m = D["XU100.IS"]["intra"]
    df = pd.concat([a.rename("a"), m.rename("m")], axis=1).dropna()
    b = (df["a"].rolling(250, min_periods=120).cov(df["m"]) / df["m"].rolling(250, min_periods=120).var()).shift(1)
    hed = df["a"] - b * df["m"]
    _, p0, pos = v.bt(comp, a, cost=0)
    _, ph, posh = v.bt(comp, hed, cost=0)
    tr = p0[pos != 0]; trh = ph[posh != 0]
    for yr, g in tr.groupby(tr.index.year):
        mm, tt, nn = v.nw_mean_t(g); gh = trh[trh.index.year == yr]
        Y.append({"stock": st, "year": yr, "n": nn, "gross_bps": 1e4 * mm, "net8": 1e4 * mm - 8, "net15": 1e4 * mm - 15, "t_gross": tt,
                  "hedged_net15": 1e4 * gh.mean() - 15, "hit_net15": float((g - 0.0015 > 0).mean())})
Y = pd.DataFrame(Y); Y.to_csv(os.path.join(v.OUT, "res_s7_yearly.csv"), index=False)
print(Y.round(1).to_string(index=False))
