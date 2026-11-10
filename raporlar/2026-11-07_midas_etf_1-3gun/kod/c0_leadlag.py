"""Kullanıcının düzeni: sinyal t kapanışında görülür, AYNI KAPANIŞTA (C0) alınır, 1-3 gün sonra kapanışta satılır.
Bu betik eşik tabanlı lead-lag kurallarını C0 girişiyle sistematik olarak backtest eder (yalnız long; Midas'ta açığa satış yok).
Öncü L, hedef T (likit ETF'ler). Sinyaller (t'de bilinen; oynaklık ve beta t-1'e kadarki 60 günle):
  L_UP   : z_L(t) = r_L(t)/sd60_L >= +2           -> T al
  L_DN   : z_L(t) <= -2                            -> T al
  GERIDE : kalıntı = r_T(t) - beta60*r_L(t); z <= -2 (T, öncünün ima ettiğinin gerisinde kaldı) -> T al (yetişme)
  ONDE   : kalıntı z >= +2 (T öncüden güçlü)        -> T al (göreli momentum)
Kontrol: hedefin kendi sinyali OWN_DN (z_T <= -2) ve OWN_UP (z_T >= +2) — öncünün katkısını ayırmak için.
Tutuş h=1,2,3; maliyet 2.500 $ (komisyon 12 bp + makas). Çıktı: sonuclar/c0_leadlag.csv
Kullanım: python3 -I kod/c0_leadlag.py"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from multiprocessing import Pool
import lib
from leadlag_sweep import build_panel

PANEL = None

def init(p):
    global PANEL
    PANEL = p

def z_of(x):
    return x / x.rolling(60).std().shift(1)

def one(T):
    R, X = PANEL
    df = lib.load(T)
    cost = lib.cost_bp(df)
    rT = np.log(df["c"]).diff()
    out = []
    def run(sig, leader, kind):
        sig = sig.reindex(df.index).fillna(False).astype(bool)
        sig.iloc[:80] = False
        if sig.sum() < 30: return
        for h in (1, 2, 3):
            tr = lib.trades(df, sig, h, "C0", None, cost)
            if len(tr) < 30: continue
            s = lib.stats(tr, df, h, "C0")
            x = tr["net"].values
            out.append({"target": T, "leader": leader, "kind": kind, "h": h, "n": s["n"], "net_bp": s["mean_net_bp"], "gross_bp": s["mean_gross_bp"],
                        "edge_bp": s.get("edge_bp"), "t": s["t"], "is_net_bp": s["is_net_bp"], "oos_net_bp": s["oos_net_bp"], "is_t": s["is_t"], "oos_t": s["oos_t"],
                        "years_pos": s["years_pos_frac"], "win": s["win"], "worst_bp": s["worst_bp"], "maxdd": s["maxdd"], "cost_bp": cost,
                        "t_top5_out": (np.sort(x)[:-5].mean() / (np.sort(x)[:-5].std(ddof=1) / math.sqrt(len(x) - 5))) if len(x) > 10 else np.nan})
    zT = z_of(rT)
    run(zT <= -2, T, "OWN_DN"); run(zT >= 2, T, "OWN_UP")
    for L in X.columns:
        if L == T: continue
        rL = X[L].reindex(df.index)
        if rL.notna().sum() < 400: continue
        zL = z_of(rL)
        cov = rT.rolling(60).cov(rL).shift(1); var = rL.rolling(60).var().shift(1)
        beta = cov / var
        res = rT - beta * rL
        zr = res / res.rolling(60).std().shift(1)
        run(zL >= 2, L, "L_UP"); run(zL <= -2, L, "L_DN")
        run(zr <= -2, L, "GERIDE"); run(zr >= 2, L, "ONDE")
    return out

if __name__ == "__main__":
    R, X = build_panel()
    scr = pd.read_csv(os.path.join(lib.ROOT, "sonuclar", "tarama.csv"))
    targets = scr[(scr["n"] >= 750) & (scr["med_dollar_vol_m"] >= 20)]["sym"].tolist()
    print("hedef", len(targets), "öncü", X.shape[1], flush=True)
    with Pool(3, initializer=init, initargs=((R, X),)) as p:
        rows = []
        for o in p.imap_unordered(one, targets, chunksize=1):
            rows += o
    res = pd.DataFrame(rows)
    from scipy import stats as st
    res["p1"] = st.t.sf(res["t"], res["n"] - 1)          # tek yönlü: net > 0
    res["fdr10"] = lib.bh_fdr(res["p1"].values, 0.10)
    res["fdr05"] = lib.bh_fdr(res["p1"].values, 0.05)
    res.to_csv(os.path.join(lib.ROOT, "sonuclar", "c0_leadlag.csv"), index=False)
    print(res.shape, "fdr10", int(res.fdr10.sum()), "fdr05", int(res.fdr05.sum()))
