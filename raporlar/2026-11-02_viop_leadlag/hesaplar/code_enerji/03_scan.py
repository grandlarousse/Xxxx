"""Veri güdümlü tarama: 6 hisse x paneldeki TÜM semboller (2014+).
Testler: (S) senkron corr, (PC) XU100 kontrollü kısmi corr, (G1) sürücü_{t-1}->gap_t, (I1) sürücü_{t-1}->intra_t, (H1) sürücü_{t-1}->(intra_t - XU100 intra_t).
t ~ r*sqrt(n) (iid), BH-FDR q=0.05 her test ailesi içinde. Sonra ilk adaylar için IS/OOS ve NW-t kontrolü."""
import pandas as pd, numpy as np, elib
from elib import ll
P = elib.panel(); P = P[P.index >= "2014-01-01"]
cat = pd.read_csv(elib.SCR + "/data/catalog.csv")
ok = cat[(cat.zero_frac <= 0.25) & (cat.n >= 750)].sym
cols = [c for c in P.columns if c in set(ok)]
X = P[cols]
xu = P["XU100.IS"]
STK = ["TUPRS", "PETKM", "SASA", "AKSEN", "ENJSA", "ODAS"]
D = elib.dpanel(); xud = D["XU100"]

def colcorr(y, M):
    """y: Series, M: DataFrame. pairwise-complete corr ve n (vektörize)."""
    m = M.notna() & y.notna().values[:, None]
    Y = np.where(m, y.values[:, None], np.nan); Z = np.where(m, M.values, np.nan)
    n = m.sum(0)
    Ym = Y - np.nanmean(Y, 0); Zm = Z - np.nanmean(Z, 0)
    c = np.nansum(Ym * Zm, 0) / np.sqrt(np.nansum(Ym ** 2, 0) * np.nansum(Zm ** 2, 0))
    return pd.Series(c, M.columns), pd.Series(n, M.columns)

def resid(s, ctrl):
    df = pd.concat([s, ctrl], axis=1).dropna()
    if len(df) < 100: return s * np.nan
    b = np.polyfit(df.iloc[:, 1], df.iloc[:, 0], 1)
    return s - (b[0] * ctrl + b[1])

Xr = X.apply(lambda c: resid(c, xu))
rows = []
for s in STK:
    y = P[s + ".IS"]; d = D[s]
    yr_ = resid(y, xu)
    tests = {"S": (y, X), "PC": (yr_, Xr), "G1": (d.gap.reindex(X.index), X.shift(1)), "I1": (d.intra.reindex(X.index), X.shift(1)),
             "H1": ((d.intra - xud.intra).reindex(X.index), X.shift(1)), "REV": (y.shift(1), X)}
    for k, (yy, M) in tests.items():
        c, n = colcorr(yy, M)
        for sym in M.columns:
            rows.append((s, k, sym, c[sym], int(n[sym])))
    print(s, flush=True)
R = pd.DataFrame(rows, columns=["stock", "test", "sym", "corr", "n"])
R = R[R.n >= 500]
R["t"] = R["corr"] * np.sqrt(R.n - 2) / np.sqrt(1 - R["corr"] ** 2)
R["p"] = ll.t_to_p(R.t)
R["fdr"] = False; R["padj"] = np.nan
for k, g in R.groupby("test"):
    rej, pa = ll.fdr(g.p.values); R.loc[g.index, "fdr"] = rej; R.loc[g.index, "padj"] = pa
R = R.merge(cat[["sym", "group", "name"]], on="sym", how="left")
R.to_csv(elib.RES + "/scan_all.csv", index=False)
print("Toplam test:", len(R), R.groupby("test").size().to_dict())
print("FDR geçen:", R[R.fdr].groupby(["test", "stock"]).size().unstack(fill_value=0).to_string())
