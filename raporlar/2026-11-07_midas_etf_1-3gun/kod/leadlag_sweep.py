"""Sistematik öncü-ardıl (lead-lag) taraması. Tüm seriler t kapanışında (16:00 ET) bilinir şekilde hizalanır.
Her hedef ETF T ve öncü L için:
  eşzamanlı: corr (tam örnek, son 252g), beta (son 252g)
  gecikmeli (öncülük): r_T(t+1..t+h) = a + b*r_L(t) + c*r_T(t)   (h=1,3; HAC t)
  yetişme (catch-up): gap_t = beta60_t * r_L(t) - r_T(t);  r_T(t+1..t+h) = a + k*gap_t   (k>0: T, L'yi geriden izler)
  IS (<=2021) / OOS (2022+) katsayı işaretleri.
Çıktı: sonuclar/leadlag_sweep.csv"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from multiprocessing import Pool
import lib, universe

LEADERS_ETF = ["SPY","QQQ","IWM","DIA","TLT","IEF","SHY","UUP","FXY","FXE","GLD","SLV","CPER","USO","BNO","UNG","UNL","USL",
               "HYG","LQD","EEM","FXI","KWEB","EWJ","SMH","XLE","XLF","KRE","XLK","GDX","XBI","IBIT","ETHA","BITO","DBA","TIP"]
PANEL = None

def build_panel():
    syms = lib.available()
    R = {}
    for s in syms:
        try:
            d = lib.load(s)
        except Exception:
            continue
        R[s] = np.log(d["c"]).diff()
    R = pd.DataFrame(R)
    spy_idx = lib.load("SPY").index
    R = R.reindex(spy_idx)
    X = {}
    for L in LEADERS_ETF:
        if L in R: X[L] = R[L]
    vix = lib.vol_index("VIX").reindex(spy_idx); v3 = lib.vol_index("VIX3M").reindex(spy_idx)
    X["VIX_dlog"] = np.log(vix).diff()
    X["VIXTS_d"] = (vix / v3).diff()
    for nm in ["OVX", "GVZ", "VVIX"]:
        try: X[nm + "_dlog"] = np.log(lib.vol_index(nm).reindex(spy_idx)).diff()
        except Exception: pass
    try:
        b = lib.btc_at_us_close("BTC-USD").reindex(spy_idx)
        X["BTC_16ET"] = np.log(b).diff()
        e = lib.btc_at_us_close("ETH-USD").reindex(spy_idx)
        X["ETH_16ET"] = np.log(e).diff()
    except Exception as ex:
        print("btc", ex)
    for f in ["DGS10", "DGS2", "DGS30", "DFII10", "T10YIE"]:
        s = lib.fred(f)
        if s is not None:
            X[f + "_d"] = s.reindex(spy_idx).diff()
    for f in ["BAMLH0A0HYM2"]:
        s = lib.fred(f)
        if s is not None:
            X["HYOAS_d"] = s.reindex(spy_idx).diff()
    X = pd.DataFrame(X)
    return R, X

def nw_t(y, x, lags):
    """OLS + Newey-West t (son sütun hariç sabit içerir). x: (n,k) sabit dahil."""
    n, k = x.shape
    xtx = np.linalg.inv(x.T @ x); b = xtx @ x.T @ y; e = y - x @ b
    u = x * e[:, None]
    S = u.T @ u
    for l in range(1, lags + 1):
        w = 1 - l / (lags + 1); G = u[l:].T @ u[:-l]; S += w * (G + G.T)
    V = xtx @ S @ xtx
    return b, b / np.sqrt(np.diag(V))

def fwd(r, h):
    return r[::-1].rolling(h).sum()[::-1].shift(-1)  # r(t+1)+...+r(t+h)

def one(T):
    R, X = PANEL
    out = []
    y0 = R[T]
    if y0.notna().sum() < 500: return out
    for L in X.columns:
        if L == T: continue
        x = X[L]
        df = pd.DataFrame({"y": y0, "x": x}).dropna()
        if len(df) < 400: continue
        rec = {"target": T, "leader": L, "n": len(df), "start": str(df.index[0].date())}
        rec["corr_full"] = df["y"].corr(df["x"]); last = df.tail(252)
        rec["corr_1y"] = last["y"].corr(last["x"])
        rec["beta_1y"] = np.cov(last["y"], last["x"])[0, 1] / np.var(last["x"], ddof=1) if np.var(last["x"]) > 0 else np.nan
        # rolling beta 60 (t'ye kadar)
        cov = df["y"].rolling(60).cov(df["x"]); var = df["x"].rolling(60).var()
        beta60 = cov / var
        gap = beta60 * df["x"] - df["y"]
        for h in (1, 3):
            fy = fwd(y0, h).reindex(df.index)
            d2 = pd.DataFrame({"fy": fy, "x": df["x"], "own": df["y"], "gap": gap}).dropna()
            if len(d2) < 300: continue
            Y = d2["fy"].values
            Xm = np.column_stack([np.ones(len(d2)), d2["own"].values, d2["x"].values])
            b, t = nw_t(Y, Xm, max(1, h))
            rec[f"lag_b_h{h}"] = b[2]; rec[f"lag_t_h{h}"] = t[2]
            Xg = np.column_stack([np.ones(len(d2)), d2["gap"].values])
            bg, tg = nw_t(Y, Xg, max(1, h))
            rec[f"catch_k_h{h}"] = bg[1]; rec[f"catch_t_h{h}"] = tg[1]
            for nm, m in (("is", d2.index <= lib.IS_END), ("oos", d2.index > lib.IS_END)):
                dd = d2[m]
                if len(dd) > 150:
                    b2, t2 = nw_t(dd["fy"].values, np.column_stack([np.ones(len(dd)), dd["own"].values, dd["x"].values]), max(1, h))
                    bg2, tg2 = nw_t(dd["fy"].values, np.column_stack([np.ones(len(dd)), dd["gap"].values]), max(1, h))
                    rec[f"lag_t_h{h}_{nm}"] = t2[2]; rec[f"catch_t_h{h}_{nm}"] = tg2[1]
            # ekonomik büyüklük: x 1 sd hareketinde beklenen h-günlük getiri (bp)
            rec[f"lag_bp_per_sd_h{h}"] = b[2] * d2["x"].std() * 1e4
            rec[f"catch_bp_per_sd_h{h}"] = bg[1] * d2["gap"].std() * 1e4
        out.append(rec)
    return out

def init(p):
    global PANEL
    PANEL = p

if __name__ == "__main__":
    R, X = build_panel()
    scr = pd.read_csv(os.path.join(lib.ROOT, "sonuclar", "tarama.csv"))
    targets = scr[(scr["n"] >= 500) & (scr["med_dollar_vol_m"] >= 2)]["sym"].tolist()
    with Pool(max(2, os.cpu_count() - 1), initializer=init, initargs=((R, X),)) as p:
        rows = []
        for o in p.imap_unordered(one, targets, chunksize=2):
            rows += o
    res = pd.DataFrame(rows)
    from scipy import stats as st
    for c in ["lag_t_h1", "lag_t_h3", "catch_t_h1", "catch_t_h3"]:
        p = 2 * st.norm.sf(res[c].abs())
        res["p_" + c] = p
        res["fdr10_" + c] = lib.bh_fdr(p.values, 0.10)
    res.to_csv(os.path.join(lib.ROOT, "sonuclar", "leadlag_sweep.csv"), index=False)
    X.describe().T.to_csv(os.path.join(lib.ROOT, "sonuclar", "leadlag_leaders_desc.csv"))
    print(res.shape, {c: int(res["fdr10_" + c].sum()) for c in ["lag_t_h1", "lag_t_h3", "catch_t_h1", "catch_t_h3"]})
