"""GÖREV 1 + 2 (5 dk): lider (5 endeks + 11 likit hisse) -> 47 VİOP hissesi, gecikme 1..6 bar (5..30 dk).
Kestirim (öngörü, P): y_t = a + Σ_{k=1..6} b_k L_{t-k} + Σ c_k y_{t-k} + Σ d_k XU030_{t-k} + e   (L=XU030 ise XU030 kontrolü yok)
  gün-içi gecikmeler; gün başından önceki gecikmeler 0. Hedef slotlar 07:05..14:55 (07:00 barı sadece gecikme olarak).
  Getiriler slot bazında standartlaştırılır (her 5 dk dilimi eşit ağırlık; 'std'); dayanıklılık: ham ('raw'), açılış hariç (07:30 sonrası, 'x30').
  SE: gün kümelenmiş. Ortak test: Wald(b1..b6)=0, Σb t.
Gecikme ölçüsü (D): y_t ~ L_{t..t-6} + y_{t-1..t-6}: gecikmeli pay DS = Σ_{k≥1} b_k / Σ_{k≥0} b_k; tepki süresi = kümülatif tepkinin %90'ına ulaşılan lag x 5 dk.
Hou–Moskowitz D1 (XU030'a göre) = 1 - R²(lag0) / R²(lag0..6).
BAYAT FİYAT (Görev 2) varyantları: hedef = bar içi log(C_t/O_t) ('oc', ilk işlemden itibaren -> bayat son fiyat sıçramasını dışlar),
  hedef = bar arası sıçrama log(O_t/C_{t-1}) ('jump'); alt örneklem: hedef r_{t-1}≠0 / =0 ; hedef hacim_{t-1} ≥ / < slot medyanı.
TERS YÖN: hedef -> lider aynı modelle.
Çıktı: res/a1_m5_pairs.csv, res/a1_m5_delay.csv
"""
import numpy as np, pandas as pd, c_common as c
K = 6
TG = c.VIOP; LD = c.LEADERS
ALL = sorted(set(TG) | set(LD))
R = {s: c.m5_ret(s, "cc") for s in ALL}
ROC = {s: c.m5_ret(s, "oc") for s in TG + [x for x in LD if x not in TG]}
RJ = {s: c.m5_ret(s, "jump") for s in TG}
VOL = {s: c.m5_panel(s)["V"][:, 1:] for s in TG}
nd, nb = R["XU030"].shape
day_id = np.repeat(np.arange(nd), nb).reshape(nd, nb)
slot = np.tile(np.arange(nb), (nd, 1))

def stdz(X):
    sd = np.nanstd(X, axis=0, keepdims=True); sd[sd == 0] = np.nan
    return X / sd
RS = {s: stdz(R[s]) for s in ALL}
ROCS = {s: stdz(ROC[s]) for s in ROC}; RJS = {s: stdz(RJ[s]) for s in RJ}

def lags(X, ks):
    Z = np.nan_to_num(X, nan=0.0)
    return [c.lagmat(Z, k) for k in ks]

def fit(y, Xlist, mask, ntest):
    """y gün x bar; Xlist: liste (gün x bar); ilk ntest regresör test edilen. mask: kullanılacak satırlar."""
    Y = y[mask]; X = np.column_stack([x[mask] for x in Xlist]); g = day_id[mask]
    ok = ~np.isnan(Y) & ~np.isnan(X).any(axis=1)
    if ok.sum() < 500: return None
    b, se, cov, r2, n = c.ols_cl(Y[ok], X[ok], g[ok])
    idx = list(range(1, 1 + ntest))
    w, p = c.wald(b, cov, idx); s, ts = c.tsum(b, cov, idx)
    return dict(b=b[1:1 + ntest], t=b[1:1 + ntest] / se[1:1 + ntest], sum=s, tsum=ts, wald_p=p, r2=r2, n=int(ok.sum()))

base_mask = (slot >= 1)
x30_mask = (slot >= 6)
half1 = day_id < nd // 2; half2 = ~half1

rows = []
def run_pair(L, Y, tag):
    RR = RS
    yl = lags(RR[Y], range(1, K + 1)); ml = lags(RR["XU030"], range(1, K + 1)) if L != "XU030" and Y != "XU030" else []
    Ll = lags(RR[L], range(1, K + 1))
    Xs = Ll + yl + ml
    out = dict(leader=L, target=Y, dir=tag)
    a = RR[Y][base_mask]; b0 = RR[L][base_mask]; ok = ~np.isnan(a) & ~np.isnan(b0)
    out["corr0"] = np.corrcoef(a[ok], b0[ok])[0, 1]
    for nm, msk, yy in [("std", base_mask, RR[Y]), ("x30", x30_mask, RR[Y]), ("h1", base_mask & half1, RR[Y]), ("h2", base_mask & half2, RR[Y])]:
        f = fit(yy, Xs, msk, K)
        if f is None: continue
        for k in range(K): out[f"{nm}_b{k+1}"] = f["b"][k]; out[f"{nm}_t{k+1}"] = f["t"][k]
        out[f"{nm}_sum"] = f["sum"]; out[f"{nm}_tsum"] = f["tsum"]; out[f"{nm}_p"] = f["wald_p"]; out[f"{nm}_n"] = f["n"]
    # ham getiri (bps cinsinden etki)
    yl_r = lags(R[Y], range(1, K + 1)); ml_r = lags(R["XU030"], range(1, K + 1)) if L != "XU030" and Y != "XU030" else []
    f = fit(R[Y], lags(R[L], range(1, K + 1)) + yl_r + ml_r, base_mask, K)
    if f is not None:
        out["raw_b1"] = f["b"][0]; out["raw_t1"] = f["t"][0]; out["raw_sum"] = f["sum"]; out["raw_tsum"] = f["tsum"]; out["raw_p"] = f["wald_p"]
    if tag == "fwd" and Y in RJ:
        # bayat fiyat varyantları
        for nm, yy in [("oc", ROCS[Y]), ("jump", RJS[Y])]:
            f = fit(yy, Xs, base_mask, K)
            if f is not None:
                out[f"{nm}_b1"] = f["b"][0]; out[f"{nm}_t1"] = f["t"][0]; out[f"{nm}_sum"] = f["sum"]; out[f"{nm}_tsum"] = f["tsum"]; out[f"{nm}_p"] = f["wald_p"]
        prevzero = c.lagmat(np.nan_to_num(R[Y], nan=0.0), 1) == 0
        V = VOL[Y]; vmed = np.nanmedian(V, axis=0, keepdims=True); prevact = c.lagmat(V, 1) >= vmed
        for nm, msk in [("pz", base_mask & prevzero), ("pnz", base_mask & ~prevzero), ("va", base_mask & prevact), ("vl", base_mask & ~prevact)]:
            f = fit(RR[Y], Xs, msk, K)
            if f is not None:
                out[f"{nm}_b1"] = f["b"][0]; out[f"{nm}_t1"] = f["t"][0]; out[f"{nm}_sum"] = f["sum"]; out[f"{nm}_tsum"] = f["tsum"]; out[f"{nm}_n"] = f["n"]
    # dağıtılmış gecikme (gecikme ölçüsü)
    f = fit(RR[Y], lags(RR[L], range(0, K + 1)) + yl, base_mask, K + 1)
    if f is not None:
        bb = f["b"]; tot = bb.sum(); out["dl_b0"] = bb[0]; out["dl_tot"] = tot
        out["delay_share"] = (tot - bb[0]) / tot if tot != 0 else np.nan
        cr = np.cumsum(bb) / tot if tot > 0 else np.full(K + 1, np.nan)
        out["adj_min90"] = 5 * int(np.argmax(cr >= 0.9)) if tot > 0 and (cr >= 0.9).any() else np.nan
    rows.append(out)

import time; t0 = time.time()
for L in LD:
    for Y in TG:
        if L == Y: continue
        run_pair(L, Y, "fwd")
        run_pair(Y, L, "rev")
    print(L, round(time.time() - t0, 1), flush=True)
PR = pd.DataFrame(rows)
from scipy import stats
for nm in ["std", "x30", "raw"]:
    p = PR[f"{nm}_p"].values
    for d in ["fwd", "rev"]:
        m = PR["dir"] == d
        rej, padj = c.ll.fdr(p[m.values]); PR.loc[m, f"{nm}_fdr"] = rej; PR.loc[m, f"{nm}_padj"] = padj
PR.to_csv(c.RES + "/a1_m5_pairs.csv", index=False)

# Hou–Moskowitz D1 ve dağıtılmış gecikme vs XU030 her hisse için (std, ham)
rows = []
for Y in TG:
    for RR, lab in [(RS, "std"), (R, "raw")]:
        y = RR[Y]; M0 = lags(RR["XU030"], [0]); Mall = lags(RR["XU030"], range(0, K + 1))
        f0 = fit(y, M0, base_mask, 1); f1 = fit(y, Mall, base_mask, K + 1)
        bb = f1["b"]; tot = bb.sum()
        f2 = fit(y, lags(RR["XU030"], range(1, K + 1)) + M0, base_mask, K)
        rows.append(dict(stock=Y, spec=lab, r2_0=f0["r2"], r2_all=f1["r2"], D1=1 - f0["r2"] / f1["r2"], b0=bb[0], sum_b1_6=tot - bb[0],
                         t_sum_b1_6=f2["tsum"], t_b1=f1["t"][1], delay_share=(tot - bb[0]) / tot))
DL = pd.DataFrame(rows); DL.to_csv(c.RES + "/a1_m5_delay.csv", index=False)
print("bitti", round(time.time() - t0, 1))
