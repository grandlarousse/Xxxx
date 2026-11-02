"""A2: Veri güdümlü tarama. 5 hisse x panel_ret_bistcal'deki TÜM semboller.
Testler (her biri ayrı FDR ailesi, BH q=0.05):
  sync   : corr(hisse_t, x_t)                       2010+
  pc     : kısmi corr | XU100_t                     2010+
  gap1   : corr(gap_t, x_{t-1})                     2014+
  intra1 : corr(intra_t, x_{t-1})   <- işlenebilir   2014+
  intra0 : corr(intra_t, x_t) yalnız açılış öncesi kapanan Asya/Avustralya sembolleri (işlenebilir)
  rev    : corr(x_t, hisse_{t-1})  (hisse önde)
p-değeri: basit t (r*sqrt((n-2)/(1-r^2))); FDR'den geçenler NW-t ve IS/OOS ile yeniden kontrol edilir.
Çıktı: res/scan_all.csv, res/scan_fdr.csv"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mh, ll, pandas as pd, numpy as np
from scipy import stats

P = pd.read_parquet(os.path.join(mh.SCR, "data", "panel_ret_bistcal.parquet"))
DEC = pd.read_parquet(os.path.join(mh.SCR, "data", "panel_decomp_bist.parquet"))
cat = pd.read_csv(os.path.join(mh.SCR, "data", "catalog.csv")).set_index("sym")
P = P.where(P != 0)  # tatil ffill sıfırları -> NaN
xu = P["XU100.IS"]

def cor_vec(y, X, min_n=250):
    """y Series, X DataFrame (aynı index). Her sütun için pairwise corr, n."""
    m = X.notna() & y.notna().values[:, None]
    Xv = X.where(m); yv = pd.DataFrame(np.repeat(y.values[:, None], X.shape[1], 1), index=X.index, columns=X.columns).where(m)
    n = m.sum()
    xm = Xv - Xv.mean(); ym = yv - yv.mean()
    r = (xm * ym).sum() / np.sqrt((xm ** 2).sum() * (ym ** 2).sum())
    r[n < min_n] = np.nan
    return r, n

def resid(y, x):
    df = pd.concat([y, x], axis=1).dropna()
    b = np.polyfit(df.iloc[:, 1], df.iloc[:, 0], 1)
    return y - (b[0] * x + b[1])

def pc_vec(y, X, ctrl):
    """kısmi corr: y ve her X sütunu ctrl'e regres edilir (sütun bazında ortak örneklemde yaklaşık: tüm örneklem beta)."""
    ry = resid(y, ctrl)
    RX = {}
    for c in X.columns:
        RX[c] = resid(X[c], ctrl) if X[c].notna().sum() > 250 else X[c] * np.nan
    return cor_vec(ry, pd.DataFrame(RX))

def pval(r, n):
    t = r * np.sqrt((n - 2) / (1 - r ** 2)); return pd.Series(2 * (1 - stats.norm.cdf(np.abs(t))), index=r.index), t

if __name__ == "__main__":
    rows = []
    syms = [c for c in P.columns]
    pre = [c for c in syms if mh.is_preopen(c)]
    for s in mh.STOCKS:
        y = P[s + ".IS"]; y = y[y.index >= mh.START]
        X = P.loc[y.index, [c for c in syms if c != s + ".IS"]]
        r, n = cor_vec(y, X); p, t = pval(r, n)
        rows.append(pd.DataFrame({"stock": s, "test": "sync", "sym": r.index, "r": r.values, "n": n.values, "t": t.values, "p": p.values}))
        rp, n2 = pc_vec(y, X, xu.loc[y.index]); p2, t2 = pval(rp, n2)
        rows.append(pd.DataFrame({"stock": s, "test": "pc", "sym": rp.index, "r": rp.values, "n": n2.values, "t": t2.values, "p": p2.values}))
        Xl = P.shift(1)
        for comp, tn in [("gap", "gap1"), ("intra", "intra1")]:
            yy = DEC[(s, comp)].dropna(); yy = yy[yy.index >= "2014-01-01"]
            XX = Xl.reindex(yy.index)[[c for c in syms if c != s + ".IS"]]
            r3, n3 = cor_vec(yy, XX); p3, t3 = pval(r3, n3)
            rows.append(pd.DataFrame({"stock": s, "test": tn, "sym": r3.index, "r": r3.values, "n": n3.values, "t": t3.values, "p": p3.values}))
        yy = DEC[(s, "intra")].dropna(); yy = yy[yy.index >= "2014-01-01"]
        XX = P.reindex(yy.index)[pre]
        r4, n4 = cor_vec(yy, XX); p4, t4 = pval(r4, n4)
        rows.append(pd.DataFrame({"stock": s, "test": "intra0_preopen", "sym": r4.index, "r": r4.values, "n": n4.values, "t": t4.values, "p": p4.values}))
        # ters: x_t ~ hisse_{t-1}
        yl = P[s + ".IS"].shift(1); yl = yl[yl.index >= mh.START]
        Xr = P.loc[yl.index, [c for c in syms if c != s + ".IS"]]
        r5, n5 = cor_vec(yl, Xr); p5, t5 = pval(r5, n5)
        rows.append(pd.DataFrame({"stock": s, "test": "rev", "sym": r5.index, "r": r5.values, "n": n5.values, "t": t5.values, "p": p5.values}))
    A = pd.concat(rows, ignore_index=True)
    A["group"] = A["sym"].map(cat["group"]); A["name"] = A["sym"].map(cat["name"]); A["zero_frac"] = A["sym"].map(cat["zero_frac"])
    A["rej"] = False; A["p_adj"] = np.nan
    for (s, tn), g in A.groupby(["stock", "test"]):
        rej, pa = ll.fdr(g["p"].values); A.loc[g.index, "rej"] = rej; A.loc[g.index, "p_adj"] = pa
    A.to_csv(os.path.join(mh.RES, "scan_all.csv"), index=False)
    F = A[A.rej]
    F.to_csv(os.path.join(mh.RES, "scan_fdr.csv"), index=False)
    print("toplam test:", len(A.dropna(subset=["p"])), "FDR geçen:", len(F))
    print(F.groupby(["stock", "test"]).size().unstack(fill_value=0))
