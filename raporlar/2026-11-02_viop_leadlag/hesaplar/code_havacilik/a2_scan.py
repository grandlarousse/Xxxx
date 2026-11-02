"""A2: veri güdümlü tarama. 3 hisse x panel_ret_bistcal'daki TÜM semboller.
Testler: (1) senkron kısmi korelasyon | XU100 (2010+), (2) x_{t-1} -> gap_t, (3) x_{t-1} -> intra_t, (4) x_{t-1} -> hisseye özgü intra (XU100 intra'dan arındırılmış),
(5) ters yön: hisse_{t-1} -> x_t.  Her test ailesi için BH-FDR (q=0.05). Hayatta kalanlar NW-t ile yeniden hesaplanır.
Çıktı: res/a2_scan.csv, res/a2_top.txt"""
from h import *
from scipy import stats

def colcorr(y, X):
    """y: Series, X: DataFrame. NaN-çiftli korelasyon (vektörize)."""
    Y = np.broadcast_to(y.values[:, None], X.shape).astype(float)
    Xv = X.values.astype(float)
    M = ~np.isnan(Y) & ~np.isnan(Xv)
    n = M.sum(0)
    Yz = np.where(M, Y, 0.0); Xz = np.where(M, Xv, 0.0)
    my = Yz.sum(0) / np.maximum(n, 1); mx = Xz.sum(0) / np.maximum(n, 1)
    Yc = np.where(M, Y - my, 0.0); Xc = np.where(M, Xv - mx, 0.0)
    r = (Yc * Xc).sum(0) / np.sqrt((Yc ** 2).sum(0) * (Xc ** 2).sum(0))
    return pd.Series(r, X.columns), pd.Series(n, X.columns)

def resid_on(X, m):
    """Her sütunu m üzerine (kendi örneklemiyle) regresle, artıkları döndür."""
    out = {}
    for c in X.columns:
        df = pd.concat([X[c], m], axis=1).dropna()
        if len(df) < 100: continue
        b = np.polyfit(df.iloc[:, 1], df.iloc[:, 0], 1)
        out[c] = X[c] - (b[0] * m + b[1])
    return pd.DataFrame(out)

if __name__ == "__main__":
    P = pd.read_parquet(S + "/data/panel_ret_bistcal.parquet")
    cat = pd.read_csv(S + "/data/catalog.csv").set_index("sym")
    keep = [c for c in P.columns if c in cat.index and cat.loc[c, "zero_frac"] <= 0.30 and cat.loc[c, "n"] >= 750]
    P = P[keep]
    isb = [c.endswith(".IS") for c in P.columns]
    # BIST-dışı sembollerde ffill sıfırlarını NaN yap
    for c, b in zip(P.columns, isb):
        if not b: P.loc[P[c] == 0, c] = np.nan
    P = P[P.index >= "2010-01-01"]
    m = P["XU100.IS"]
    Pr = resid_on(P, m)
    rows = []
    for st in STOCKS:
        y = R(st).reindex(P.index); dd = D(st).reindex(P.index)
        ym = (y - np.polyval(np.polyfit(pd.concat([y, m], axis=1).dropna().iloc[:, 1], pd.concat([y, m], axis=1).dropna().iloc[:, 0], 1), m))
        xi = D("XU100")["intra"].reindex(P.index)
        dfi = pd.concat([dd["intra"], xi], axis=1).dropna(); bi = np.polyfit(dfi.iloc[:, 1], dfi.iloc[:, 0], 1)[0]
        exintra = dd["intra"] - bi * xi
        cols = [c for c in P.columns if c != st + ".IS"]
        Xs = P[cols]; Xl = Xs.shift(1)
        res = {}
        res["sync_pc"], n1 = colcorr(ym, Pr[[c for c in cols if c in Pr.columns]])
        res["sync_raw"], _ = colcorr(y, Xs)
        sub = P.index >= "2014-01-01"
        res["gap_l1"], n2 = colcorr(dd["gap"][sub], Xl[sub])
        res["intra_l1"], n3 = colcorr(dd["intra"][sub], Xl[sub])
        res["xintra_l1"], n4 = colcorr(exintra[sub], Xl[sub])
        # IS / OOS ayrımı intra için
        isx = sub & (P.index < SPLIT); oos = P.index >= SPLIT
        res["intra_l1_IS"], _ = colcorr(dd["intra"][isx], Xl[isx])
        res["intra_l1_OOS"], _ = colcorr(dd["intra"][oos], Xl[oos])
        res["sync_pc_IS"], _ = colcorr(ym[P.index < SPLIT], Pr.loc[P.index < SPLIT, [c for c in cols if c in Pr.columns]])
        res["sync_pc_OOS"], _ = colcorr(ym[oos], Pr.loc[oos, [c for c in cols if c in Pr.columns]])
        # ters yön: hisse_{t-1} -> x_t (yalnız BIST dışı anlamlı)
        Ysh = y.shift(1)
        rv = {}
        for c in cols:
            df = pd.concat([P[c], Ysh], axis=1).dropna()
            rv[c] = df.iloc[:, 0].corr(df.iloc[:, 1]) if len(df) > 250 else np.nan
        res["reverse"] = pd.Series(rv)
        df = pd.DataFrame(res); df["n_sync"] = n1; df["n_lag"] = n3
        df["stock"] = st; df["sym"] = df.index
        rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["group"] = A["sym"].map(cat["group"]); A["name"] = A["sym"].map(cat["name"])
    fam = {"sync_pc": "n_sync", "gap_l1": "n_lag", "intra_l1": "n_lag", "xintra_l1": "n_lag", "reverse": "n_sync"}
    ntests = 0
    for f, nn in fam.items():
        t = A[f] * np.sqrt(A[nn] - 2) / np.sqrt(1 - A[f] ** 2)
        p = 2 * (1 - stats.norm.cdf(t.abs()))
        rej, padj = ll.fdr(np.asarray(p, float))
        A[f + "_t"] = t; A[f + "_q"] = padj; A[f + "_fdr"] = rej; ntests += int(np.isfinite(np.asarray(p, float)).sum())
    A.to_csv(RES + "/a2_scan.csv", index=False)
    with open(RES + "/a2_top.txt", "w") as fh:
        fh.write(f"Toplam test sayısı: {ntests} (5 aile x 3 hisse x ~{len(cols)} sembol)\n")
        for f in fam:
            fh.write(f"\n===== {f}: FDR geçen = {A[f + '_fdr'].sum()} =====\n")
            for st in STOCKS:
                x = A[(A.stock == st)].sort_values(f, key=lambda s: -s.abs()).head(25)
                fh.write(f"--- {st}\n" + x[["sym", "group", "name", f, f + "_t", f + "_q", "intra_l1_IS", "intra_l1_OOS", "sync_pc_IS", "sync_pc_OOS"]].round(3).to_string(index=False) + "\n")
    print(open(RES + "/a2_top.txt").read()[:200])
