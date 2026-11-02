"""Toplu (vektörize) OLS + Newey-West: y_t = a + b*x_{i,t} + c'C_t + e  — her aday i için ayrı tam-örneklem maskesi.
nw_batch(y, X, C, L=5) -> dict(b, t, t_ols, pc, n) (her biri N uzunluğunda).
Bartlett ağırlıklı HAC, maxlags=L, küçük örneklem düzeltmesi yok (statsmodels HAC ile ≈ aynı; doğrulama: python3 hreg.py).
"""
import numpy as np, pandas as pd

def nw_batch(y, X, C=None, L=5, min_n=250):
    """Hızlı sürüm: A = Σ M z z' matris çarpımlarıyla; NW varyansı yalnız b için (a1' S a1) h_it = e_it (a1·z_it) üzerinden."""
    y = np.asarray(y, float); X = np.asarray(X, float)
    T, N = X.shape
    C = np.empty((T, 0)) if C is None else np.asarray(C, float).reshape(T, -1)
    m = C.shape[1]; p = m + 2
    okc = np.isfinite(y) & np.isfinite(C).all(1)
    M = (okc[:, None] & np.isfinite(X)).T.astype(float)  # (N,T)
    y0 = np.where(okc, y, 0.0); C0 = np.where(np.isfinite(C), C, 0.0); X0T = np.where(np.isfinite(X), X, 0.0).T
    W = np.concatenate([np.ones((T, 1)), C0], 1)  # (T, m+1)
    k = m + 1
    WW = (W[:, :, None] * W[:, None, :]).reshape(T, k * k)
    MX = M * X0T
    A = np.empty((N, p, p))
    AWW = (M @ WW).reshape(N, k, k)
    AxW = MX @ W
    Axx = (MX * X0T).sum(1)
    idxW = [0] + list(range(2, p))
    A[:, 0:1, 0:1] = AWW[:, 0:1, 0:1]
    A[np.ix_(range(N), idxW, idxW)] = AWW
    A[:, 1, idxW] = AxW; A[:, idxW, 1] = AxW; A[:, 1, 1] = Axx
    Ay = np.empty((N, p)); AyW = M @ (W * y0[:, None]); Ay[:, idxW] = AyW; Ay[:, 1] = MX @ y0
    n = M.sum(1)
    good = n >= max(min_n, p + 5)
    out = {kk: np.full(N, np.nan) for kk in ["b", "t", "t_ols", "pc", "se"]}; out["n"] = n
    if not good.any(): return out
    A = A[good]; Ay = Ay[good]; Mg = M[good]; Xg = X0T[good]
    A += np.eye(p)[None] * 1e-13 * np.trace(A, axis1=1, axis2=2)[:, None, None]
    Ainv = np.linalg.inv(A)
    beta = np.einsum("npq,nq->np", Ainv, Ay)
    fit = beta[:, idxW] @ W.T + beta[:, 1:2] * Xg
    e = (y0[None, :] - fit) * Mg
    a1 = Ainv[:, 1, :]
    q = a1[:, idxW] @ W.T + a1[:, 1:2] * Xg
    h = e * q
    V = (h * h).sum(1)
    for l in range(1, L + 1):
        V += 2 * (1.0 - l / (L + 1.0)) * (h[:, l:] * h[:, :-l]).sum(1)
    b = beta[:, 1]; se = np.sqrt(np.maximum(V, 0)); ng = n[good]
    s2 = (e ** 2).sum(1) / (ng - p)
    t_ols = b / np.sqrt(s2 * Ainv[:, 1, 1])
    out["b"][good] = b; out["se"][good] = se; out["t"][good] = b / se
    out["t_ols"][good] = t_ols; out["pc"][good] = t_ols / np.sqrt(t_ols ** 2 + ng - p)
    return out

if __name__ == "__main__":
    import sys, time, statsmodels.api as sm
    sys.path.insert(0, __file__.rsplit("/", 1)[0]); import hdata
    D = hdata.load(); cc = D["cc"]; intra = D["intra"]
    y = intra["PGSUS"]; X = cc.shift(1); C = pd.concat([cc["PGSUS"].shift(1), cc["XU100"].shift(1)], axis=1)
    t0 = time.time(); r = nw_batch(y.values, X.values, C.values); print("süre", time.time() - t0, X.shape)
    i = list(X.columns).index("THYAO")
    df = pd.concat([y.rename("y"), X["THYAO"].rename("x"), C], axis=1).dropna()
    mm = sm.OLS(df["y"], sm.add_constant(df.drop(columns="y"))).fit(cov_type="HAC", cov_kwds={"maxlags": 5, "use_correction": False})
    print("batch b,t:", r["b"][i], r["t"][i], r["n"][i], " statsmodels:", mm.params["x"], mm.tvalues["x"], len(df))
    mo = sm.OLS(df["y"], sm.add_constant(df.drop(columns="y"))).fit(); print("ols t", r["t_ols"][i], mo.tvalues["x"])
