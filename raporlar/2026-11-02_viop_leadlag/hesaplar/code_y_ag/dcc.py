"""4) Zamanla değişen korelasyon: GARCH(1,1) (varyans hedeflemeli Gauss QMLE) + iki değişkenli DCC(1,1); ayrıca EWMA(λ=0,94).
Çiftler: 47 hisse ↔ XU100_t, ↔ ES_{t-1} (BIST_t açılış gap'ini besleyen ABD kapanışı), ↔ USDTRY_t (FX_FIX'li UTC günü t).
Bulaşma (contagion): kriz penceresi vs önceki 250 işlem günü (kriz başlangıcından 20 gün önce biten) — ham ve
Forbes–Rigobon (kaynak değişken varyans artışına göre) düzeltilmiş korelasyon, Fisher-z testi; DCC ortalama farkı.
"""
import numpy as np, pandas as pd, time
from scipy.signal import lfilter
from scipy.optimize import minimize
from common import *

def garch_fit(e):
    e = e - e.mean(); v0 = e.var(); e2 = e ** 2
    def sig2(par):
        a, b = par; w = (1 - a - b) * v0
        x = w + a * np.r_[v0, e2[:-1]]
        s, _ = lfilter([1.0], [1.0, -b], x, zi=[b * v0]); return s
    def nll(par):
        a, b = par
        if a < 0 or b < 0 or a + b >= 0.999: return 1e10
        s = sig2(par); return 0.5 * np.sum(np.log(s) + e2 / s)
    best = None
    for x0 in [(0.05, 0.9), (0.1, 0.85), (0.03, 0.95)]:
        r = minimize(nll, x0, method="Nelder-Mead", options={"xatol": 1e-5, "fatol": 1e-4, "maxiter": 400})
        if best is None or r.fun < best.fun: best = r
    s = sig2(best.x); return e / np.sqrt(s), best.x, np.sqrt(s)

def dcc_fit(z1, z2):
    Q11b, Q22b, Q12b = np.mean(z1 * z1), np.mean(z2 * z2), np.mean(z1 * z2)
    def path(par):
        a, b = par; c = 1 - a - b
        def rec(x, qb):
            u = c * qb + a * np.r_[qb, x[:-1]]
            q, _ = lfilter([1.0], [1.0, -b], u, zi=[b * qb]); return q
        q11 = rec(z1 * z1, Q11b); q22 = rec(z2 * z2, Q22b); q12 = rec(z1 * z2, Q12b)
        return np.clip(q12 / np.sqrt(q11 * q22), -0.999, 0.999)
    def nll(par):
        a, b = par
        if a < 0 or b < 0 or a + b >= 0.999: return 1e10
        r = path(par); return 0.5 * np.sum(np.log(1 - r ** 2) + (z1 ** 2 + z2 ** 2 - 2 * r * z1 * z2) / (1 - r ** 2))
    best = None
    for x0 in [(0.02, 0.95), (0.05, 0.9), (0.01, 0.98)]:
        r = minimize(nll, x0, method="Nelder-Mead", options={"xatol": 1e-5, "fatol": 1e-4, "maxiter": 400})
        if best is None or r.fun < best.fun: best = r
    return path(best.x), best.x

def ewma_corr(x, y, lam=0.94):
    def rec(v, init):
        u = (1 - lam) * np.r_[init, v[:-1]]
        q, _ = lfilter([1.0], [1.0, -lam], u, zi=[lam * init]); return q
    n0 = min(60, len(x))
    sxx = rec(x * x, np.mean(x[:n0] ** 2)); syy = rec(y * y, np.mean(y[:n0] ** 2)); sxy = rec(x * y, np.mean(x[:n0] * y[:n0]))
    return sxy / np.sqrt(sxx * syy)

def fr_test(x, y, crisis, calm):
    """Forbes–Rigobon: x = kaynak (piyasa/ES/USDTRY), y = hisse."""
    xc, yc = x[crisis], y[crisis]; xt, yt = x[calm], y[calm]
    ok_c = ~(np.isnan(xc) | np.isnan(yc)); ok_t = ~(np.isnan(xt) | np.isnan(yt))
    xc, yc, xt, yt = xc[ok_c], yc[ok_c], xt[ok_t], yt[ok_t]
    nc, nt = len(xc), len(xt)
    if nc < 10 or nt < 60: return {}
    rc = np.corrcoef(xc, yc)[0, 1]; rt = np.corrcoef(xt, yt)[0, 1]
    delta = xc.var() / xt.var() - 1; radj = rc / np.sqrt(1 + delta * (1 - rc ** 2))
    se = np.sqrt(1 / (nc - 3) + 1 / (nt - 3))
    return {"n_crisis": nc, "rho_calm": rt, "rho_crisis": rc, "rho_crisis_FR": radj, "vol_ratio_src": np.sqrt(xc.var() / xt.var()),
            "z_raw": (np.arctanh(rc) - np.arctanh(rt)) / se, "z_FR": (np.arctanh(radj) - np.arctanh(rt)) / se}

if __name__ == "__main__":
    t0 = time.time(); P = panel(); P = P[P.index >= START]
    src = {"XU100": P["XU100.IS"], "ES_l1": P["ES=F"].shift(1), "USDTRY": P["TRY=X"]}
    zsrc = {}; info = []
    for k, s in src.items():
        e = s.fillna(0).values; z, par, sd = garch_fit(e); zsrc[k] = pd.Series(z, index=s.index); info.append({"series": k, "alpha": par[0], "beta": par[1]})
    D = {}; E = {}; pars = []
    for st in STOCKS:
        r = P[st + ".IS"]; fv = r.first_valid_index(); r = r[r.index >= fv]
        z, par, sd = garch_fit(r.fillna(0).values); info.append({"series": st, "alpha": par[0], "beta": par[1]})
        zs = pd.Series(z, index=r.index)
        for k in src:
            zz = zsrc[k].reindex(r.index).values
            rho, dp = dcc_fit(zs.values, zz); D[(st, k)] = pd.Series(rho, index=r.index)
            E[(st, k)] = pd.Series(ewma_corr(r.fillna(0).values, src[k].reindex(r.index).fillna(0).values), index=r.index)
            pars.append({"stock": st, "src": k, "dcc_a": dp[0], "dcc_b": dp[1]})
        print(st, round(time.time() - t0), flush=True)
    DD = pd.DataFrame(D); DD.columns = pd.MultiIndex.from_tuples(DD.columns); DD.to_parquet(os.path.join(CACHE, "dcc_paths.parquet"))
    EE = pd.DataFrame(E); EE.columns = pd.MultiIndex.from_tuples(EE.columns); EE.to_parquet(os.path.join(CACHE, "ewma_paths.parquet"))
    pd.DataFrame(pars).to_csv(os.path.join(CACHE, "dcc_params.csv"), index=False); pd.DataFrame(info).to_csv(os.path.join(CACHE, "garch_params.csv"), index=False)
    # bulaşma testleri
    idx = P.index; rows = []
    for cn, (a, b, typ) in CRISES.items():
        crisis = (idx >= a) & (idx <= b); i0 = np.argmax(idx >= pd.Timestamp(a))
        calm = np.zeros(len(idx), bool); calm[max(0, i0 - 270):max(0, i0 - 20)] = True
        for st in STOCKS:
            y = P[st + ".IS"].values
            for k, s in src.items():
                res = fr_test(s.values, y, crisis, calm)
                if not res: continue
                dser = DD[(st, k)].reindex(idx).values
                res.update({"crisis": cn, "type": typ, "stock": st, "src": k, "dcc_calm": np.nanmean(dser[calm]), "dcc_crisis": np.nanmean(dser[crisis]),
                            "dcc_peak": np.nanmax(dser[crisis]) if np.isfinite(dser[crisis]).any() else np.nan})
                rows.append(res)
    C = pd.DataFrame(rows); C.to_csv(os.path.join(CACHE, "contagion_tests.csv"), index=False)
    print("done", round(time.time() - t0))
