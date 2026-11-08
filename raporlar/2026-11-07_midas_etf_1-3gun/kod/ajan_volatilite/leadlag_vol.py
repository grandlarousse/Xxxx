"""Volatilite ailesi lead-lag ek testleri (SVXY, SVIX, VXX).
(1) sonuclar/leadlag_sweep.csv'den eşzamanlı sürücüler (corr_1y, beta_1y) ve gecikmeli t'ler (FDR bayraklarıyla).
(2) Ek: t'de bilinen DURUM değişkenleri ve öncü getirileri -> ileri getiri, kendi gecikmesi kontrollü, Newey-West t, IS/OOS:
      y = r_T(giriş -> giriş+h) ;  x = öncü_t ;  kontrol = r_T(t)
    İki hizalama: 'C0' (t kapanışından; VIX 16:15 -> 15 dk ileri bakış içerir) ve 'O1' (t+1 açılışından, temiz).
    Ekonomik büyüklük: 1 sd'lik x değişiminin ileri getiriye etkisi (bp) ve maliyet (cost_rt_bp) ile oran.
(3) BH-FDR (q=0.10) bu dosyadaki tüm (hedef x öncü x h x hizalama) testleri üzerinde.
Çalıştırma: python3 -I kod/ajan_volatilite/leadlag_vol.py
Çıktı: sonuclar/aile_volatilite/leadlag_ek.csv, leadlag_esz.csv"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np, pandas as pd
import vlib, lib
from scipy import stats as st

def nw(y, X, lags):
    n, k = X.shape
    XtX = np.linalg.inv(X.T @ X); b = XtX @ X.T @ y; e = y - X @ b
    u = X * e[:, None]; S = u.T @ u
    for l in range(1, lags + 1):
        w = 1 - l / (lags + 1); G = u[l:].T @ u[:-l]; S += w * (G + G.T)
    V = XtX @ S @ XtX
    return b, b / np.sqrt(np.diag(V))

def leaders(idx):
    x = vlib.ctx(idx)
    spy = lib.load("SPY"); qqq = lib.load("QQQ")
    L = pd.DataFrame(index=idx)
    L["VIX_dlog"] = np.log(x["VIX"]).diff()
    L["VVIX_dlog"] = np.log(x["VVIX"]).diff()
    L["R3M_seviye"] = x["R3M"]
    L["R3M_degisim"] = x["R3M"].diff()
    L["R9D_seviye"] = x["R9D"]
    L["VIX_gerilme_log"] = np.log(x["VIX"] / x["VIX_SMA10"])
    L["VVIX_VIX_oran"] = x["VVIX"] / x["VIX"]
    L["SPY_r"] = np.log(spy["c"]).diff().reindex(idx)
    L["QQQ_r"] = np.log(qqq["c"]).diff().reindex(idx)
    L["SPY_r5"] = np.log(spy["c"]).diff(5).reindex(idx)
    try:
        b = lib.btc_at_us_close("BTC-USD").reindex(idx); L["BTC_16ET_r"] = np.log(b).diff()
    except Exception:
        pass
    for f in ["DGS10"]:
        s = lib.fred(f)
        if s is not None: L[f + "_d"] = s.reindex(idx).diff()
    return L

def run(verbose=True):
    sw = pd.read_csv(os.path.join(lib.ROOT, "sonuclar", "leadlag_sweep.csv"))
    tarama = pd.read_csv(os.path.join(lib.ROOT, "sonuclar", "tarama.csv")).set_index("sym")
    targets = ["SVXY", "SVIX", "VXX"]
    esz = sw[sw.target.isin(targets)][["target", "leader", "n", "corr_full", "corr_1y", "beta_1y", "lag_t_h1", "lag_t_h3",
                                        "lag_t_h1_is", "lag_t_h1_oos", "fdr10_lag_t_h1", "fdr10_lag_t_h3", "catch_t_h1", "fdr10_catch_t_h1"]]
    esz = esz.reindex(esz["corr_1y"].abs().sort_values(ascending=False).index)
    esz.to_csv(os.path.join(vlib.OUT, "leadlag_esz.csv"), index=False)
    rows = []
    for T in targets:
        df = lib.load(T); idx = df.index
        L = leaders(idx)
        c = df["c"]; o = df["o"]
        own = np.log(c).diff()
        cost = float(tarama.loc[T, "cost_rt_bp"])
        for h in (1, 3):
            y_c0 = np.log(c.shift(-h) / c)                 # t kapanışı -> t+h kapanışı
            y_o1 = np.log(c.shift(-h) / o.shift(-1))       # t+1 açılışı -> t+h kapanışı (h=1: gün içi)
            for al, y in (("C0", y_c0), ("O1", y_o1)):
                for nm in L.columns:
                    D = pd.DataFrame({"y": y, "x": L[nm], "own": own}).replace([np.inf, -np.inf], np.nan).dropna()
                    if len(D) < 250: continue
                    res = {"hedef": T, "oncu": nm, "h": h, "hizalama": al, "n": len(D)}
                    for per, m in (("tum", np.ones(len(D), bool)), ("is", D.index <= lib.IS_END), ("oos", D.index > lib.IS_END)):
                        d = D[m]
                        if len(d) < 150:
                            res[f"t_{per}"] = np.nan; res[f"b_{per}"] = np.nan; continue
                        X = np.c_[np.ones(len(d)), (d["x"] - d["x"].mean()) / d["x"].std(), d["own"]]
                        b, t = nw(d["y"].values, X, max(h, 5))
                        res[f"b_{per}"] = b[1] * 1e4; res[f"t_{per}"] = t[1]
                    res["bp_per_sd"] = res["b_tum"]
                    res["bp_per_sd_bolu_maliyet"] = abs(res["b_tum"]) / cost
                    res["p"] = float(2 * st.norm.sf(abs(res["t_tum"]))) if np.isfinite(res["t_tum"]) else np.nan
                    rows.append(res)
    R = pd.DataFrame(rows)
    R["fdr10"] = lib.bh_fdr(R["p"].values, 0.10)
    R["is_oos_ayni_isaret"] = np.sign(R["t_is"]) == np.sign(R["t_oos"])
    R["gecerli_oncu"] = R["fdr10"] & R["is_oos_ayni_isaret"] & (R["bp_per_sd_bolu_maliyet"] > 1.0)
    R.to_csv(os.path.join(vlib.OUT, "leadlag_ek.csv"), index=False)
    if verbose:
        pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40); pd.set_option("display.max_rows", 300)
        print("=== Eşzamanlı (sweep): en yüksek |corr_1y| ilk 8, hedef başına ===")
        for T in targets:
            print(esz[esz.target == T].head(8).round(3).to_string())
        print("\nSweep'te aile hedefleri için FDR geçen gecikmeli öncü sayısı:",
              int(sw[sw.target.isin(vlib.FAM)][["fdr10_lag_t_h1", "fdr10_lag_t_h3", "fdr10_catch_t_h1", "fdr10_catch_t_h3"]].any(axis=1).sum()))
        print(f"\n=== Ek testler: {len(R)} test, FDR geçen {int(R['fdr10'].sum())}, geçerli öncü (FDR+IS/OOS aynı işaret+|etki|>maliyet) {int(R['gecerli_oncu'].sum())} ===")
        R["m"] = R["t_tum"].abs()
        print(R.sort_values("m", ascending=False).head(30)[["hedef", "oncu", "h", "hizalama", "n", "b_tum", "t_tum", "t_is", "t_oos",
              "bp_per_sd_bolu_maliyet", "fdr10", "is_oos_ayni_isaret", "gecerli_oncu"]].round(2).to_string())
    return R, esz

if __name__ == "__main__":
    run()
