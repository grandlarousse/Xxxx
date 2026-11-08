"""Görev 4: Lead-lag (tek hisse kaldıraçlı aile).
(1) leadlag_sweep.csv'den aile hedefleri: eşzamanlı sürücüler (corr_1y, beta_1y) ve gecikmeli öncü/yetişme istatistikleri (FDR bayrakları).
(2) Ek test (dayanakta 2016+, IS/OOS): r_hisse(t+1..t+h) = a + b*x_t + c*r_hisse(t), x = öncü getirisi ya da yetişme boşluğu
    (beta60*r_L - r_hisse); Newey-West. Öncüler: QQQ, SPY, SMH, XLK (+ NVDA için SOX vekili SMH); MSTR/COIN için BTC@16:00 ET (2023-06+).
    Ekonomik büyüklük: 1 sd'lik x'in 2x ETF'te beklenen etkisi (2*b*sd) maliyetle karşılaştırılır.
(3) Gerçek zamanlı izleme: BTC gece hareketi -> MSTR/COIN açılış boşluğu (t4'te hesaplandı, btc_gece_acilis.csv).
Çalıştırma: python3 -I kod/ajan_tek_hisse_kaldiracli/t5_leadlag.py
Çıktılar: leadlag_aile_sweep.csv, leadlag_suruculer.csv, leadlag_ek_regresyon.csv"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import thk, lib

pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40); pd.set_option("display.max_rows", 300)
L = pd.read_csv(os.path.join(thk.ROOT, "sonuclar", "leadlag_sweep.csv"))
F = L[L.target.isin(thk.FAM)].copy()
F.to_csv(os.path.join(thk.OUT, "leadlag_aile_sweep.csv"), index=False)
fl = ["fdr10_lag_t_h1", "fdr10_lag_t_h3", "fdr10_catch_t_h1", "fdr10_catch_t_h3"]
print("Sweep: aile hedef x öncü satırı:", len(F), " FDR bayraklı satır:", int(F[fl].any(axis=1).sum()))
# en güçlü (geçmeyen) gecikmeli adaylar
F["max_abs_t"] = F[["lag_t_h1", "lag_t_h3", "catch_t_h1", "catch_t_h3"]].abs().max(axis=1)
print(F.sort_values("max_abs_t", ascending=False).head(12)[["target", "leader", "n", "lag_t_h1", "lag_t_h3", "catch_t_h1", "catch_t_h3", "lag_bp_per_sd_h1", "catch_bp_per_sd_h1"]].round(2).to_string())

# eşzamanlı sürücüler: sweep corr_1y + dayanak hissenin kendisi
TVL = {"SPY": "AMEX:SPY", "QQQ": "NASDAQ:QQQ", "IWM": "AMEX:IWM", "DIA": "AMEX:DIA", "SMH": "NASDAQ:SMH", "XLK": "AMEX:XLK",
       "IBIT": "NASDAQ:IBIT", "ETHA": "NASDAQ:ETHA", "BITO": "AMEX:BITO", "BTC_16ET": "COINBASE:BTCUSD", "ETH_16ET": "COINBASE:ETHUSD",
       "VIX_dlog": "CBOE:VIX", "XLF": "AMEX:XLF", "KWEB": "AMEX:KWEB", "EEM": "AMEX:EEM", "XLE": "AMEX:XLE", "KRE": "AMEX:KRE", "XBI": "AMEX:XBI"}
tv_etf = pd.read_csv(os.path.join(thk.ROOT, "sonuclar", "tv_etf.csv")).drop_duplicates("sym").set_index("sym")["tv"].to_dict()
for k in list(TVL):
    if k in tv_etf: TVL[k] = tv_etf[k]
drv = []
for e in thk.FAM:
    d = lib.load(e); st = thk.UNDER[e]; s = thk.load_stock(st).reindex(d.index)
    re = np.log(d["c"]).diff(); rs = np.log(s["c"]).diff()
    z = pd.DataFrame({"re": re, "rs": rs}).dropna().tail(252)
    drv.append({"etf": e, "surucu": st, "tv": thk.TV_STOCK[st], "corr_1y": z.re.corr(z.rs), "beta_1y": np.cov(z.re, z.rs)[0, 1] / z.rs.var(), "kaynak": "dayanak"})
    sub = F[F.target == e].copy()
    sub = sub[~sub.leader.isin(["UNL", "USL", "BNO", "SHY"])]
    sub = sub.reindex(sub.corr_1y.abs().sort_values(ascending=False).index).head(5)
    for _, r in sub.iterrows():
        drv.append({"etf": e, "surucu": r.leader, "tv": TVL.get(r.leader, tv_etf.get(r.leader, "")), "corr_1y": r.corr_1y, "beta_1y": r.beta_1y, "kaynak": "sweep"})
DRV = pd.DataFrame(drv); DRV.to_csv(os.path.join(thk.OUT, "leadlag_suruculer.csv"), index=False)
print(DRV.round(3).to_string())

# ---------- ek regresyonlar (dayanak, 2016+) ----------
def nw(y, X, lags):
    X = np.column_stack([np.ones(len(y)), X]); xtx = np.linalg.inv(X.T @ X); b = xtx @ X.T @ y; e = y - X @ b
    u = X * e[:, None]; Sm = u.T @ u
    for l in range(1, lags + 1):
        w = 1 - l / (lags + 1); G = u[l:].T @ u[:-l]; Sm += w * (G + G.T)
    V = xtx @ Sm @ xtx
    return b, b / np.sqrt(np.diag(V))

LEAD = {"QQQ": np.log(lib.load("QQQ")["c"]).diff(), "SPY": np.log(lib.load("SPY")["c"]).diff(),
        "SMH": np.log(lib.load("SMH")["c"]).diff(), "XLK": np.log(lib.load("XLK")["c"]).diff()}
btc = np.log(lib.btc_at_us_close("BTC-USD")).diff()
rows = []
for st in thk.STOCKS:
    sdf = thk.load_stock(st); rs = np.log(sdf["c"]).diff()
    leaders = dict(LEAD)
    if st in ("MSTR", "COIN"): leaders["BTC_16ET"] = btc.reindex(sdf.index)
    for ln, rl in leaders.items():
        rl = rl.reindex(sdf.index)
        beta = rs.rolling(60).cov(rl) / rl.rolling(60).var()
        gap = beta * rl - rs
        for xn, x in (("lag", rl), ("yetisme", gap)):
            for h in (1, 3):
                y = sum(rs.shift(-i) for i in range(1, h + 1))
                for per, sl in (("tum", slice(None)), ("IS", slice(None, "2021-12-31")), ("OOS", slice("2022-01-01", None))):
                    z = pd.DataFrame({"y": y, "x": x, "own": rs}).dropna().loc[sl]
                    if len(z) < 250: continue
                    b, t = nw(z.y.values, z[["x", "own"]].values, 5 if h == 1 else 8)
                    # yetişme için kendi gecikmesi olmadan (ham) t de raporlanır
                    b0, t0 = nw(z.y.values, z[["x"]].values, 5 if h == 1 else 8)
                    rows.append({"hisse": st, "oncu": ln, "tip": xn, "h": h, "donem": per, "n": len(z), "b": b[1], "t": t[1], "t_ham": t0[1],
                                 "b_own": b[2], "t_own": t[2], "etki_2x_bp_per_sd": 2 * b[1] * z.x.std() * 1e4,
                                 "maliyet_rt_bp": thk.cost_for(thk.PRIMARY[st])})
R = pd.DataFrame(rows)
full = R[R.donem == "tum"].copy()
full["p"] = [lib.t_to_p(t, n) for t, n in zip(full.t, full.n)]
full["fdr"] = lib.bh_fdr(full.p.values, 0.10)
W = full.merge(R[R.donem == "IS"][["hisse", "oncu", "tip", "h", "t"]].rename(columns={"t": "t_IS"}), on=["hisse", "oncu", "tip", "h"], how="left") \
        .merge(R[R.donem == "OOS"][["hisse", "oncu", "tip", "h", "t"]].rename(columns={"t": "t_OOS"}), on=["hisse", "oncu", "tip", "h"], how="left")
W["ayni_isaret"] = np.sign(W.t_IS) == np.sign(W.t_OOS)
W["ekonomik"] = W.etki_2x_bp_per_sd.abs() > W.maliyet_rt_bp
W["gecerli_oncu"] = W.fdr & W.ayni_isaret & W.ekonomik
W.to_csv(os.path.join(thk.OUT, "leadlag_ek_regresyon.csv"), index=False)
print("\nEk regresyon testleri (tam dönem):", len(W), " FDR geçen:", int(W.fdr.sum()), " geçerli öncü (FDR+IS/OOS aynı işaret+ekonomik):", int(W.gecerli_oncu.sum()))
print(W.sort_values("t", key=lambda s: -s.abs()).head(20)[["hisse", "oncu", "tip", "h", "n", "b", "t", "t_ham", "t_own", "t_IS", "t_OOS", "etki_2x_bp_per_sd", "maliyet_rt_bp", "fdr", "gecerli_oncu"]].round(2).to_string())
