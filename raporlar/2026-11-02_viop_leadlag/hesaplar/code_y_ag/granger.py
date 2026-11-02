"""3) Granger nedensellik ağı (öngörü GÜCÜ testi — öngörü/strateji değil).
y_t = c + Σ_k a_k y_{t-k} + Σ_k m_k XU100_{t-k} + Σ_k g_k x_{t-k} + e ;  H0: g=0 (HC1-dayanıklı Wald, χ²_p), p ∈ {1,2}.
Hedef türleri: cc (kapanış-kapanış), gap (önceki kapanış->açılış), intra (açılış->kapanış; işlenebilir kısım).
Kaynaklar: 47 hisse + XU100 + 10 sürücü (A: ham hizalama; B: ABD/FX kapanışlı sürücüler +1 gün kaydırılmış).
Dönemler: tam 2014–2026, IS 2014–2020, OOS 2021–2026. BH-FDR aile içinde (dönem×p×hedef×hizalama).
Ayrıca: ters yön (hisse -> sürücü), kaydırılmış-kaynak null, likidite (bayat fiyat) kontrolü.
"""
import numpy as np, pandas as pd, time
from common import *
import ll
from scipy import stats
from common import *
from dy import DRV, SHORT

def wald_hc1(y, X, Z):
    """FWL: y ve X'i Z'ye göre artıkla, sonra X katsayıları için HC1 Wald. Dönüş (W, p, b1, t1, pc1, n)."""
    n = len(y)
    Zt = np.linalg.lstsq(Z, np.column_stack([y, X]), rcond=None)[0]
    R = np.column_stack([y, X]) - Z @ Zt
    ry, RX = R[:, 0], R[:, 1:]
    XtX = RX.T @ RX; b = np.linalg.solve(XtX, RX.T @ ry); e = ry - RX @ b
    k = Z.shape[1] + X.shape[1]
    inv = np.linalg.inv(XtX); meat = (RX * e[:, None] ** 2).T @ RX
    V = inv @ meat @ inv * n / (n - k)
    W = float(b @ np.linalg.solve(V, b)); p = float(stats.chi2.sf(W, X.shape[1]))
    t1 = b[0] / np.sqrt(V[0, 0]); pc1 = np.corrcoef(ry, RX[:, 0])[0, 1]
    return W, p, b[0], t1, pc1, n

def lagmat(s, p): return np.column_stack([s.shift(k).values for k in range(1, p + 1)])

def sources(align):
    P = panel(); S = {s: P[s + ".IS"] for s in STOCKS}; S["XU100"] = P["XU100.IS"]
    for d in DRV:
        x = P[d]; S[SHORT[d]] = x.shift(1) if (align == "B" and d in US_CLOSE) else x
    return pd.DataFrame(S)

def targets():
    P = panel(); D = pd.read_parquet(os.path.join(SCR, "data", "panel_decomp_bist.parquet"))
    T = {}
    for s in STOCKS:
        T[(s, "cc")] = P[s + ".IS"]
        T[(s, "gap")] = D[(s, "gap")].reindex(P.index); T[(s, "intra")] = D[(s, "intra")].reindex(P.index)
    return T

PER = {"tam": ("2014-01-01", "2026-10-30"), "IS": ("2014-01-01", "2020-12-31"), "OOS": ("2021-01-01", "2026-10-30")}

def run(align="A", shift_null=0, kinds=("cc", "gap", "intra"), lags=(1, 2), pers=("tam", "IS", "OOS")):
    P = panel(); S = sources(align); T = targets(); xu = P["XU100.IS"]; rows = []
    if shift_null: S = S.shift(shift_null)  # kaynak serisini zaman içinde kaydır (null)
    for p in lags:
        XU = lagmat(xu, p)
        SL = {c: lagmat(S[c], p) for c in S.columns}
        for tgt in STOCKS:
            own = lagmat(P[tgt + ".IS"], p)
            for kind in kinds:
                y = T[(tgt, kind)].values
                for pn in pers:
                    a, b = PER[pn]; tmask = (P.index >= a) & (P.index <= b)
                    base_ok = tmask & ~np.isnan(y) & ~np.isnan(own).any(1) & ~np.isnan(XU).any(1)
                    for src in S.columns:
                        if src == tgt: continue
                        X = SL[src]; ok = base_ok & ~np.isnan(X).any(1)
                        if ok.sum() < 150: continue
                        Z = np.column_stack([np.ones(ok.sum()), own[ok], XU[ok]]) if src != "XU100" else np.column_stack([np.ones(ok.sum()), own[ok]])
                        try: W, pv, b1, t1, pc1, n = wald_hc1(y[ok], X[ok], Z)
                        except Exception: continue
                        rows.append((align, shift_null, p, pn, kind, src, tgt, W, pv, b1, t1, pc1, n))
        print("p", p, "done", flush=True)
    R = pd.DataFrame(rows, columns=["align", "shift", "p", "period", "kind", "src", "tgt", "W", "pval", "b1", "t1", "pc1", "n"])
    R["q"] = np.nan; R["sig"] = False
    for key, g in R.groupby(["align", "shift", "p", "period", "kind"]):
        rej, q = ll.fdr(g["pval"].values, 0.05); R.loc[g.index, "q"] = q; R.loc[g.index, "sig"] = rej
    return R

def reverse(align="A", lags=(1,), pers=("tam", "IS", "OOS")):
    """hisse/XU100_{t-k} -> sürücü_t (sürücünün kendi lag'i + XU100 lag kontrollü)."""
    P = panel(); S = sources(align); xu = P["XU100.IS"]; rows = []
    for p in lags:
        XU = lagmat(xu, p)
        for d in DRV:
            dn = SHORT[d]; y = S[dn].values; own = lagmat(S[dn], p)
            for pn in pers:
                a, b = PER[pn]; tmask = (P.index >= a) & (P.index <= b)
                base_ok = tmask & ~np.isnan(y) & ~np.isnan(own).any(1) & ~np.isnan(XU).any(1)
                for src in STOCKS + ["XU100"]:
                    X = lagmat(S[src], p); ok = base_ok & ~np.isnan(X).any(1)
                    if ok.sum() < 150: continue
                    Z = np.column_stack([np.ones(ok.sum()), own[ok], XU[ok]]) if src != "XU100" else np.column_stack([np.ones(ok.sum()), own[ok]])
                    W, pv, b1, t1, pc1, n = wald_hc1(y[ok], X[ok], Z)
                    rows.append((align, p, pn, src, dn, W, pv, b1, t1, pc1, n))
    R = pd.DataFrame(rows, columns=["align", "p", "period", "src", "tgt", "W", "pval", "b1", "t1", "pc1", "n"])
    R["q"] = np.nan; R["sig"] = False
    for key, g in R.groupby(["align", "p", "period"]):
        rej, q = ll.fdr(g["pval"].values, 0.05); R.loc[g.index, "q"] = q; R.loc[g.index, "sig"] = rej
    return R

def liquidity():
    rows = []
    for s in STOCKS:
        d = ll.raw(s + ".IS"); d = d[(d["ldate"] >= "2021-01-01")]
        tl = (d["v"] * d["c"]).replace(0, np.nan)
        r = ll.ret(s); r = r[r.index >= "2021-01-01"]
        rows.append({"stock": s, "med_tl_vol_mn": float(tl.median() / 1e6), "zero_ret_frac": float((r == 0).mean()),
                     "ac1": float(r.autocorr(1))})
    return pd.DataFrame(rows)

if __name__ == "__main__":
    t0 = time.time()
    RA = run("A"); print("A", round(time.time() - t0)); RB = run("B", kinds=("cc", "intra"), lags=(1,)); print("B", round(time.time() - t0))
    nulls = [run("A", shift_null=k, kinds=("cc", "intra"), lags=(1,), pers=("tam",)) for k in (157, 409, 733)]
    pd.concat([RA, RB] + nulls).to_csv(os.path.join(CACHE, "granger_all.csv.gz"), index=False)
    RV = pd.concat([reverse("A"), reverse("B")]); RV.to_csv(os.path.join(CACHE, "granger_reverse.csv"), index=False)
    liquidity().to_csv(os.path.join(CACHE, "liquidity.csv"), index=False)
    print("done", round(time.time() - t0))
