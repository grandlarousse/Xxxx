"""GÖREV 1 (60 dk, 2023-12..2026-10): lider -> 47 hisse, gecikme 1..6 bar.
Parçalar (yıl boyu tutarlı ızgara): r1 = O->07:30 (30 dk), r2..r8 = 07:30->08:30 ... 13:30->14:30, r9 = 14:30->kapanış (son 30 dk + kapanış müzayedesi).
Model: y_t = a + Σ_{k=1..6} b_k L_{t-k} + Σ c_k y_{t-k} + Σ d_k XU030_{t-k}, gün-içi (gün öncesi gecikmeler 0), parça bazında standartlaştırılmış.
Hedef parçalar r2..r9. SE gün kümelenmiş. IS = ilk yarı (< 2025-05-15), OOS = ikinci yarı.
Ayrıca dağıtılmış gecikme (lag0..6) ile gecikmeli pay ve D1 (XU030).
Çıktı: res/a1b_h1_pairs.csv, res/a1b_h1_delay.csv
"""
import numpy as np, pandas as pd, c_common as c
K = 6; TG = c.VIOP; LD = c.LEADERS; ALL = sorted(set(TG) | set(LD))
H = {s: c.h1_panel(s) for s in ALL}
days = H["XU030"].index
R = {s: H[s][c.H1_PIECES].values for s in ALL}
def stdz(X):
    sd = np.nanstd(X, axis=0, keepdims=True); sd[sd == 0] = np.nan; return X / sd
RS = {s: stdz(R[s]) for s in ALL}
nd, nb = R["XU030"].shape
day_id = np.repeat(np.arange(nd), nb).reshape(nd, nb); slot = np.tile(np.arange(nb), (nd, 1))
SPLIT = pd.Timestamp("2025-05-15"); is_ = (days < SPLIT)[:, None] & np.ones((1, nb), bool)
def lags(X, ks):
    Z = np.nan_to_num(X, nan=0.0); return [c.lagmat(Z, k) for k in ks]
# satır geçerliliği: hedef ve gecikmelerin kaynak barları gerçek veri olmalı (NaN -> 0 yapılmadan önce)
def fit(y, Xlist, mask, ntest, valid=None):
    m = mask & ~np.isnan(y)
    if valid is not None: m &= valid
    Y = y[m]; X = np.column_stack([x[m] for x in Xlist]); g = day_id[m]
    if len(Y) < 300: return None
    b, se, cov, r2, n = c.ols_cl(Y, X, g)
    idx = list(range(1, 1 + ntest)); w, p = c.wald(b, cov, idx); s, ts = c.tsum(b, cov, idx)
    return dict(b=b[1:1 + ntest], t=b[1:1 + ntest] / se[1:1 + ntest], sum=s, tsum=ts, p=p, r2=r2, n=len(Y))
base = slot >= 1
rows = []
for L in LD:
    for Y in TG:
        if L == Y: continue
        for d, (LL, YY) in {"fwd": (L, Y), "rev": (Y, L)}.items():
            valid = ~np.isnan(R[LL]).all(axis=1)[:, None] & ~np.isnan(R[YY]).all(axis=1)[:, None]
            yl = lags(RS[YY], range(1, K + 1)); ml = lags(RS["XU030"], range(1, K + 1)) if "XU030" not in (LL, YY) else []
            Xs = lags(RS[LL], range(1, K + 1)) + yl + ml
            out = dict(leader=L, target=Y, dir=d)
            a = RS[YY][base]; bb = RS[LL][base]; ok = ~np.isnan(a) & ~np.isnan(bb); out["corr0"] = np.corrcoef(a[ok], bb[ok])[0, 1]
            for nm, msk in [("all", base), ("is", base & is_), ("oos", base & ~is_)]:
                f = fit(RS[YY], Xs, msk, K, valid)
                if f is None: continue
                for k in range(3): out[f"{nm}_b{k+1}"] = f["b"][k]; out[f"{nm}_t{k+1}"] = f["t"][k]
                out[f"{nm}_sum"] = f["sum"]; out[f"{nm}_tsum"] = f["tsum"]; out[f"{nm}_p"] = f["p"]; out[f"{nm}_n"] = f["n"]
            f = fit(RS[YY], lags(RS[LL], range(0, K + 1)) + yl, base, K + 1, valid)
            if f is not None:
                b_ = f["b"]; tot = b_.sum(); out["dl_b0"] = b_[0]; out["delay_share"] = (tot - b_[0]) / tot if tot else np.nan
            rows.append(out)
    print(L, flush=True)
PR = pd.DataFrame(rows)
for nm in ["all", "is", "oos"]:
    for d in ["fwd", "rev"]:
        m = PR["dir"] == d; rej, padj = c.ll.fdr(PR.loc[m, f"{nm}_p"].values); PR.loc[m, f"{nm}_fdr"] = rej; PR.loc[m, f"{nm}_padj"] = padj
PR.to_csv(c.RES + "/a1b_h1_pairs.csv", index=False)
rows = []
for Y in TG:
    valid = ~np.isnan(R[Y]).all(axis=1)[:, None]
    f0 = fit(RS[Y], lags(RS["XU030"], [0]), base, 1, valid); f1 = fit(RS[Y], lags(RS["XU030"], range(0, K + 1)), base, K + 1, valid)
    f2 = fit(RS[Y], lags(RS["XU030"], range(1, K + 1)) + lags(RS["XU030"], [0]), base, K, valid)
    rows.append(dict(stock=Y, r2_0=f0["r2"], r2_all=f1["r2"], D1=1 - f0["r2"] / f1["r2"], b0=f1["b"][0], sum_b1_6=f1["b"][1:].sum(), t_sum_b1_6=f2["tsum"], t_b1=f1["t"][1]))
pd.DataFrame(rows).to_csv(c.RES + "/a1b_h1_delay.csv", index=False)
print("bitti")
