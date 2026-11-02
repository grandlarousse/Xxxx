"""S6: Regresyon kontrolleri, yoğunlaşma, mevsim/zaman marjı, tik (o==önceki kapanış) günleri, 47 VİOP hissesinde genişlik.
Çıktı: res_s6_*.csv"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v, numpy as np, pandas as pd
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 200)
JP_AU = ["5411.T", "5401.T", "6301.T", "FMG.AX", "BHP.AX"]
ST = ["EREGL.IS", "KRDMD.IS"]
comp = v.composite(JP_AU)
xu = v.decomp("XU100.IS")
spx = v.ret("^GSPC").shift(1)      # ABD kapanışı t-1 (BIST açılışından önce bilinir)
slx = v.ret("SLX").shift(1)
n225 = v.zpast(v.ret("^N225"))
# (1) regresyon kontrolleri (standardize edilmiş)
reg = []
for st in ST:
    d = v.decomp(st)
    X = pd.DataFrame({"comp_t": comp, "gap_t": d["gap"], "own_intra_t1": d["intra"].shift(1), "own_cc_t1": d["cc"].shift(1),
                      "xu_intra_t1": xu["intra"].shift(1), "spx_t1": spx, "slx_t1": slx, "n225z_t": n225})
    y = d["intra"]
    for spec, cols in [("yalın", ["comp_t"]), ("+gap", ["comp_t", "gap_t"]), ("+gap+gecikmeler", ["comp_t", "gap_t", "own_intra_t1", "own_cc_t1", "xu_intra_t1"]),
                       ("+ABD t-1 (SPX,SLX)", ["comp_t", "gap_t", "own_intra_t1", "own_cc_t1", "xu_intra_t1", "spx_t1", "slx_t1"]),
                       ("+N225 z_t", ["comp_t", "gap_t", "own_intra_t1", "own_cc_t1", "xu_intra_t1", "spx_t1", "slx_t1", "n225z_t"])]:
        for per, msk in [("ALL", None), ("IS", "IS"), ("OOS", "OOS")]:
            df = pd.concat([y.rename("y"), X[cols]], axis=1).dropna()
            if msk == "IS": df = df[df.index < v.SPLIT]
            if msk == "OOS": df = df[df.index >= v.SPLIT]
            df = (df - df.mean()) / df.std()
            p, t, n = v.nw_ols(df["y"], df[cols])
            reg.append({"stock": st, "spec": spec, "period": per, "b_comp": p["comp_t"], "t_comp": t["comp_t"], "n": n,
                        **({"t_gap": t["gap_t"]} if "gap_t" in cols else {}), **({"t_n225": t["n225z_t"]} if "n225z_t" in cols else {})})
REG = pd.DataFrame(reg); REG.to_csv(os.path.join(v.OUT, "res_s6_reg.csv"), index=False)
print(REG.round(3).to_string(index=False))

# (2) yoğunlaşma + mevsim/zaman marjı + tik günleri
conc = []
for st in ST:
    d = v.decomp(st)
    res, pnl, pos = v.bt(comp, d["intra"], cost=15, mode="z", thr=1.0)
    tr = pnl[pos != 0]
    for per, x in [("ALL", tr), ("OOS", tr[tr.index >= v.SPLIT]), ("IS", tr[tr.index < v.SPLIT])]:
        srt = x.sort_values(ascending=False)
        top10 = srt.iloc[:10].sum(); tot = x.sum()
        trim = x.clip(x.quantile(0.01), x.quantile(0.99))
        conc.append({"stock": st, "period": per, "n": len(x), "mean_bps": 1e4 * x.mean(), "median_bps": 1e4 * x.median(),
                     "trim1pct_mean_bps": 1e4 * trim.mean(), "sum_pct": 100 * tot, "top10_sum_pct": 100 * top10,
                     "mean_ex_top10_bps": 1e4 * srt.iloc[10:].mean(), "long_n": int((pos[x.index] > 0).sum()), "short_n": int((pos[x.index] < 0).sum()),
                     "long_bps": 1e4 * x[pos[x.index] > 0].mean(), "short_bps": 1e4 * x[pos[x.index] < 0].mean()})
    # mevsim: Avustralya yaz saati (Eki-Nis: ASX kapanış ~05:10 UTC) vs kış (Nis-Eki: ~06:10 UTC); Tokyo 2024-11-05 sonrası 06:30
    m = tr.index.month
    for lab, msk in [("ASX yaz saati (Kas-Mar) kapanış ~05:10 UTC", np.isin(m, [11, 12, 1, 2, 3])), ("ASX kış (May-Eyl) kapanış ~06:10 UTC", np.isin(m, [5, 6, 7, 8, 9])),
                     ("2014-2016-09 (TR yaz/kış saati, açılış daha geç UTC)", tr.index < "2016-09-08"), ("Tokyo 06:30 kapanış dönemi (2024-11-05+)", tr.index >= "2024-11-05")]:
        x = tr[msk]; mm, tt, nn = v.nw_mean_t(x)
        conc.append({"stock": st, "period": lab, "n": nn, "mean_bps": 1e4 * mm, "t": tt})
    # tik: o == önceki kapanış günleri
    oeq = np.isclose(d["o"], d["pc"], rtol=1e-6)
    oeq = pd.Series(oeq, index=d.index).reindex(tr.index)
    for lab, msk in [("o==önceki c (açılış=önceki kapanış)", oeq.values), ("o!=önceki c", ~oeq.values)]:
        x = tr[msk]; mm, tt, nn = v.nw_mean_t(x)
        conc.append({"stock": st, "period": lab, "n": nn, "mean_bps": 1e4 * mm, "t": tt})
C = pd.DataFrame(conc); C.to_csv(os.path.join(v.OUT, "res_s6_conc.csv"), index=False)
print(C.round(2).to_string(index=False))

# (3) 47 VİOP hissesinde genişlik: kompozit(t) -> intra_t
VIOP = "AEFES AKBNK AKSEN ALARK ARCLK ASELS ASTOR BIMAS BRSAN CIMSA DOAS DOHOL EKGYO ENJSA ENKAI EREGL FROTO GARAN GUBRF HALKB HEKTS ISCTR KCHOL KRDMD MGROS ODAS OYAKC PETKM PGSUS SAHOL SASA SISE SOKM TAVHL TCELL THYAO TKFEN TOASO TRALT TRMET TSKB TTKOM TUPRS ULKER VAKBN VESTL YKBNK".split()
br = []
for s in VIOP + ["XU100", "XU030", "XUSIN", "XBANK"]:
    sym = s + ".IS"
    try: d = v.decomp(sym)
    except Exception as e: print("atla", s, e); continue
    c, t, n = v.corr_t(d["intra"], comp)
    cO, tO, nO = v.corr_t(d["intra"][d.index >= v.SPLIT], comp); cI, tI, nI = v.corr_t(d["intra"][d.index < v.SPLIT], comp)
    res, pnl, pos = v.bt(comp, d["intra"], cost=15, mode="z", thr=1.0)
    br.append({"sym": s, "corr": c, "t": t, "n": n, "t_IS": tI, "t_OOS": tO, "IS_bps15": res["IS"]["bps"], "OOS_bps15": res["OOS"]["bps"], "OOS_t15": res["OOS"]["t"]})
B = pd.DataFrame(br).sort_values("t", ascending=False)
from scipy import stats
B["p"] = 2 * (1 - stats.norm.cdf(B["t"].abs()))
# BH-FDR (yalnız 47 hisse)
bb = B[B.sym.isin(VIOP)].copy(); bb = bb.sort_values("p"); m = len(bb); bb["bh_thr"] = 0.05 * np.arange(1, m + 1) / m
k = np.where(bb["p"].values <= bb["bh_thr"].values)[0]; kmax = k.max() + 1 if len(k) else 0
B["fdr_pass"] = B.sym.isin(bb.sym.iloc[:kmax])
B.to_csv(os.path.join(v.OUT, "res_s6_breadth.csv"), index=False)
print(B.round(2).to_string(index=False))
print("FDR geçen (47 hisse):", B[B.fdr_pass].sym.tolist())
