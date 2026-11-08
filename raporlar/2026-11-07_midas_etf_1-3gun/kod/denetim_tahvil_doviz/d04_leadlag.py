"""DENETİM tahvil_doviz — gecikmeli öncü iddialarının bağımsız kontrolü.
Model: r_T(t+1..t+h) = a + b*r_L(t) + c*r_T(t) + e  (kendi gecikmesi kontrollü), Newey-West (h+1 gecikme) t.
Ekonomik büyüklük: b * sd(r_L) (bp / 1 sd) ; maliyet: tarama.csv cost_rt_bp. IS (..2021) / OOS (2022..) ayrı t.
Ayrıca UUP<-SPY'yi gece (C->O) ve gün içi (O->C) parçalarına ayırır (bayat fiyat kontrolü).
Çalıştır: python3 -I kod/denetim_tahvil_doviz/d04_leadlag.py
"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np, pandas as pd
import lib
from d01_s1_yeniden import IDX, ROOT, OUT

sys.path.insert(0, os.path.join(os.path.dirname(HERE), "ajan_tahvil_doviz"))
import td  # yalnız dağıtım düzeltmeli fiyat için (td.load); istatistik burada bağımsız

tar = pd.read_csv(os.path.join(ROOT, "sonuclar", "tarama.csv")).set_index("sym")

def nw_ols(y, X, L):
    m = np.isfinite(y) & np.all(np.isfinite(X), axis=1); y = y[m]; X = X[m]
    n, k = X.shape; XtX = np.linalg.inv(X.T @ X); b = XtX @ X.T @ y; u = y - X @ b
    S = (X * u[:, None]).T @ (X * u[:, None])
    for l in range(1, L + 1):
        w = 1 - l / (L + 1); G = (X[l:] * u[l:, None]).T @ (X[:-l] * u[:-l, None]); S += w * (G + G.T)
    V = XtX @ S @ XtX
    return b, b / np.sqrt(np.diag(V)), n

def lr(sym):
    return np.log(td.load(sym)["c"]).diff().reindex(IDX)

def leader(name):
    if name.startswith("DGS"):
        return lib.fred(name).reindex(IDX).diff()   # yüzde puan değişimi (~15:30 ET, t kapanışında bilinir)
    return lr(name)

rows = []
pairs = [("TLT", "IEF"), ("TLT", "DGS10"), ("TLT", "DGS30"), ("TLT", "SPY"), ("TLT", "TIP"), ("TLT", "HYG"),
         ("TMV", "IEF"), ("TMV", "TIP"), ("TBT", "IEF"), ("TBT", "DGS30"), ("TMF", "IEF"), ("TMF", "TIP"),
         ("UUP", "SPY"), ("UUP", "HYG"), ("UUP", "LQD")]
for T, Ln in pairs:
    rT = lr(T); rL = leader(Ln)
    for h in (1, 3):
        fwd = sum(rT.shift(-k) for k in range(1, h + 1))
        X = np.column_stack([np.ones(len(IDX)), rL.values, rT.values]); y = fwd.values
        b, t, n = nw_ols(y, X, h + 1)
        isx = IDX <= pd.Timestamp("2021-12-31")
        _, tis, _ = nw_ols(y[isx], X[isx], h + 1); _, toos, _ = nw_ols(y[~isx], X[~isx], h + 1)
        bp_sd = b[1] * np.nanstd(rL.values) * 1e4
        rows.append((T, Ln, h, n, t[1], tis[1], toos[1], bp_sd, t[2], float(tar.loc[T, "cost_rt_bp"])))
R = pd.DataFrame(rows, columns=["hedef", "oncu", "h", "n", "t_oncu_kontrollu", "t_is", "t_oos", "bp_per_sd", "t_kendi", "maliyet_bp"])
R["p"] = 2 * (1 - __import__("scipy").stats.norm.cdf(R.t_oncu_kontrollu.abs()))
R["fdr10"] = lib.bh_fdr(R.p.values, 0.10)
R["ekonomik"] = R.bp_per_sd.abs() * 2 > R.maliyet_bp   # 2 sd'lik sinyal bile maliyeti karşılıyor mu
print(R.round(3).to_string(index=False))
R.to_csv(os.path.join(OUT, "d04_leadlag.csv"), index=False)

# UUP <- SPY gece / gün içi ayrıştırması
u = td.load("UUP").reindex(IDX); s = lr("SPY")
night = np.log(u["o"] / u["c"].shift(1)).shift(-1)   # t kapanışı -> t+1 açılışı
intra = np.log(u["c"] / u["o"]).shift(-1)            # t+1 açılış -> t+1 kapanış
own = lr("UUP")
for nm, y in (("gece C_t->O_t+1", night), ("gün içi O_t+1->C_t+1", intra)):
    X = np.column_stack([np.ones(len(IDX)), s.values, own.values])
    b, t, n = nw_ols(y.values, X, 2)
    print(f"UUP<-SPY {nm}: t={t[1]:.2f}, bp/sd={b[1]*np.nanstd(s.values)*1e4:.2f}")
