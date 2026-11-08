"""Denetim: volatilite ailesi gecikmeli öncü iddialarının bağımsız yeniden hesabı (kendi HAC kodu).
Çalıştırma: python3 -I kod/denetim_volatilite/denetim_leadlag.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, pandas as pd
import dlib, lib
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)

def hac(y, X, L):
    XtXi = np.linalg.pinv(X.T @ X); b = XtXi @ X.T @ y; e = y - X @ b
    u = X * e[:, None]; S = u.T @ u
    for l in range(1, L + 1):
        w = 1 - l / (L + 1); G = u[l:].T @ u[:-l]; S += w * (G + G.T)
    V = XtXi @ S @ XtXi
    return b, b / np.sqrt(np.diag(V))

def test(T, xname, x, h, al):
    df = lib.load(T); c = df.c; o = df.o
    own = np.log(c).diff()
    y = np.log(c.shift(-h) / c) if al == "C0" else np.log(c.shift(-h) / o.shift(-1))
    D = pd.DataFrame({"y": y, "x": x.reindex(df.index), "own": own}).replace([np.inf, -np.inf], np.nan).dropna()
    out = {"hedef": T, "oncu": xname, "h": h, "hiz": al, "n": len(D)}
    for per, m in (("tum", np.ones(len(D), bool)), ("is", D.index <= dlib.IS_END), ("oos", D.index > dlib.IS_END)):
        d = D[m]
        if len(d) < 150: out[f"t_{per}"] = np.nan; continue
        z = (d.x - d.x.mean()) / d.x.std()
        b, t = hac(d.y.values, np.c_[np.ones(len(d)), z, d.own], max(h, 5))
        b0, t0 = hac(d.y.values, np.c_[np.ones(len(d)), d.own], max(h, 5))
        out[f"bp_sd_{per}"] = b[1] * 1e4; out[f"t_{per}"] = t[1]
        if per == "tum": out["t_own_yalniz"] = t0[1]; out["t_own_ile"] = t[2]
    # quintile ekonomik: en üst %20 x günlerinde ortalama ileri getiri - genel ort (bp)
    q = D.x.rank(pct=True)
    out["ust20_minus_ort_bp"] = (D.y[q > 0.8].mean() - D.y.mean()) * 1e4
    out["alt20_minus_ort_bp"] = (D.y[q < 0.2].mean() - D.y.mean()) * 1e4
    return out

rows = []
vix = lib.vol_index("VIX"); vvix = lib.vol_index("VVIX")
for T in ["VXX", "SVXY", "SVIX"]:
    idx = lib.load(T).index
    ratio = (vvix / vix).reindex(idx)
    q = np.log(lib.load("QQQ").c).diff().reindex(idx)
    for h in (1, 3):
        for al in ("C0", "O1"):
            rows.append(test(T, "VVIX/VIX", ratio, h, al))
            rows.append(test(T, "QQQ_r", q, h, al))
R = pd.DataFrame(rows); print(R.round(2).to_string())
R.to_csv(os.path.join(dlib.OUT, "leadlag_denetim.csv"), index=False)

# VVIX/VIX -> VXX O1 h1 işlem olarak: oran en üst %20'de (yalnız IS'te belirlenen eşik) VXX O1 h1 long
vx = lib.load("VXX"); r = (vvix / vix).reindex(vx.index)
thr = r[r.index <= dlib.IS_END].quantile(0.8)
s = (r > thr).fillna(False)
for mode in ("C0", "O1", "C1"):
    for h in (1, 2):
        x = dlib.summ(dlib.sim(vx, s, h, mode, dlib.cost("VXX")), f"VXX VVIX/VIX>IS_p80({thr:.2f}) {mode} h{h}")
        print(f"  {x['tag']}: n={x['n']} brüt={x['brut_bp']:.1f} net={x['net_bp']:.1f} t={x['t']:.2f} IS={x['is_net_bp']:.1f} OOS={x['oos_net_bp']:.1f}")

# leadlag_sweep'ten aile hedefleri, FDR bayrakları
sw = pd.read_csv(os.path.join(lib.ROOT, "sonuclar", "leadlag_sweep.csv"))
fam = sw[sw.target.isin(["SVXY", "SVIX", "VXX", "VIXY", "UVXY", "UVIX", "VIXM"])]
fl = [c for c in fam.columns if c.startswith("fdr10_")]
print("\nsweep aile satırı:", len(fam), "FDR bayrağı olan:", int(fam[fl].any(axis=1).sum()))
fam = fam.assign(m=fam.lag_t_h1.abs().combine(fam.lag_t_h3.abs(), max))
print(fam.sort_values("m", ascending=False).head(10)[["target", "leader", "corr_1y", "lag_t_h1", "lag_t_h3", "lag_t_h1_is", "lag_t_h1_oos", "catch_t_h1"] + fl].round(2).to_string())
