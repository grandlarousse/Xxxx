"""4) Lead-lag: leadlag_sweep.csv'nin aile alt kümesi + ek testler (dağıtım-düzeltmeli veriyle).
Çalıştır: python3 -I kod/ajan_tahvil_doviz/04_leadlag.py
(a) Aile özeti: sweep'te FDR geçen satırlar, ekonomik büyüklük / maliyet oranı.
(b) Döviz ETF'leri <- SPY: gecikmeli etkinin gece (C_t->O_t+1) / gün içi (O_t+1->C_t+1) ayrıştırması; likit (UUP/FXE/FXY) vs
    likiditesiz (FXF/FXB/FXA/FXC) karşılaştırması (bayat kapanış artefaktı kontrolü); maliyetli işlem kuralı (C0/O1/C1).
(c) HYG/JNK/USHY <- SPY (kendi gecikmesi kontrollü, IS/OOS).
(d) 'Yetişme' (catch-up) satırları: öncünün katkısı kendi gecikmesine karşı (fy = a + b*own + k*gap), ekonomik büyüklük;
    BIL/SGOV'un dağıtım düzeltmesi öncesi/sonrası.
(e) TLT/TMF/TMV/TBT/EDV/UUP için aday öncüler (faiz, enflasyon başabaşı, reel faiz, SPY, VIX, HYG, bakır/altın): kendi gecikmesi
    kontrollü Newey-West t, IS/OOS, bp/sd; BH-FDR (q=0.10) bu set içinde.
Çıktılar: leadlag_aile_fdr.csv, leadlag_fx_spy.csv, leadlag_fx_kural.csv, leadlag_hy_spy.csv, leadlag_catch_kontrollu.csv,
          leadlag_izleme_oncu.csv, leadlag_suruculer.csv"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import td, lib
from scipy import stats as st

pd.set_option("display.width", 250); pd.set_option("display.max_rows", 300); pd.set_option("display.max_columns", 40)
SW = pd.read_csv(os.path.join(td.ROOT, "sonuclar", "leadlag_sweep.csv"))
x = SW[SW.target.isin(td.FAM)].copy()
scr = pd.read_csv(os.path.join(td.ROOT, "sonuclar", "tarama.csv")).set_index("sym")
x["cost_rt_bp"] = x.target.map(scr.cost_rt_bp)
for h in (1, 3):
    x[f"lag_bp_sd_over_cost_h{h}"] = x[f"lag_bp_per_sd_h{h}"].abs() / x.cost_rt_bp
    x[f"catch_bp_sd_over_cost_h{h}"] = x[f"catch_bp_per_sd_h{h}"].abs() / x.cost_rt_bp
f = x[x.fdr10_lag_t_h1 | x.fdr10_lag_t_h3 | x.fdr10_catch_t_h1 | x.fdr10_catch_t_h3]
f.to_csv(os.path.join(td.OUT, "leadlag_aile_fdr.csv"), index=False)
print("(a) Aile hedef x öncü satırı:", len(x), " FDR (lag h1/h3, catch h1/h3):",
      [int(x["fdr10_" + c].sum()) for c in ("lag_t_h1", "lag_t_h3", "catch_t_h1", "catch_t_h3")])
print("FDR geçen gecikmeli (lag) satırların hedefleri:", f[f.fdr10_lag_t_h1 | f.fdr10_lag_t_h3].target.value_counts().to_dict())
print("FDR geçen gecikmeli satırlarda |bp/sd| / maliyet en yüksek:",
      f[f.fdr10_lag_t_h1].lag_bp_sd_over_cost_h1.max().round(3))
print("FDR geçen yetişme satırlarının hedefleri:", f[f.fdr10_catch_t_h1 | f.fdr10_catch_t_h3].target.value_counts().to_dict())
print("  bunlarda catch bp/sd (h3) medyan:", f[f.fdr10_catch_t_h3].groupby("target").catch_bp_per_sd_h3.median().round(2).to_dict())

def nw(y, X, lags):
    n, k = X.shape
    xtx = np.linalg.inv(X.T @ X); b = xtx @ X.T @ y; e = y - X @ b
    u = X * e[:, None]; S = u.T @ u
    for l in range(1, lags + 1):
        w = 1 - l / (lags + 1); G = u[l:].T @ u[:-l]; S += w * (G + G.T)
    V = xtx @ S @ xtx
    return b, b / np.sqrt(np.diag(V))

def fwd(r, h):
    return r[::-1].rolling(h).sum()[::-1].shift(-1)

R = td.rets()
IDX = R.index

def lagreg(T, Lser, h=1, ystar=None, label=""):
    y0 = R[T] if ystar is None else ystar
    fy = fwd(R[T], h) if ystar is None else ystar
    d = pd.DataFrame({"fy": fy, "own": R[T], "x": Lser}).dropna()
    out = {"target": T, "leader": label, "h": h, "n": len(d)}
    if len(d) < 300: return out
    b, t = nw(d.fy.values, np.column_stack([np.ones(len(d)), d.own.values, d.x.values]), max(1, h))
    out.update({"b": b[2], "t": t[2], "bp_per_sd": b[2] * d.x.std() * 1e4})
    for nm, m in (("is", d.index <= lib.IS_END), ("oos", d.index > lib.IS_END)):
        dd = d[m]
        if len(dd) > 150:
            b2, t2 = nw(dd.fy.values, np.column_stack([np.ones(len(dd)), dd.own.values, dd.x.values]), max(1, h))
            out[f"t_{nm}"] = t2[2]
    return out

# ---------------- (b) döviz <- SPY ----------------
print("\n(b) Döviz ETF'leri <- SPY(t): ertesi gün getirisinin gece/gün içi ayrıştırması (kendi gecikmesi kontrollü)")
rows = []
spy = R["SPY"]
for T in ["UUP", "FXE", "FXY", "FXF", "FXB", "FXA", "FXC", "UDN"]:
    d = td.load(T).reindex(IDX)
    on = np.log(d["o"] / d["c"].shift(1)).shift(-1)       # C_t -> O_t+1
    idy = np.log(d["c"] / d["o"]).shift(-1)               # O_t+1 -> C_t+1
    full = R[T].shift(-1)
    for part, y in (("tam_C->C", full), ("gece_C->O", on), ("gun_ici_O->C", idy)):
        rr = lagreg(T, spy, 1, ystar=y, label="SPY")
        rr["parca"] = part; rr["med_dv_mn"] = scr.loc[T, "med_dollar_vol_m"]; rr["cost_rt_bp"] = scr.loc[T, "cost_rt_bp"]
        rows.append(rr)
fx = pd.DataFrame(rows)
fx.to_csv(os.path.join(td.OUT, "leadlag_fx_spy.csv"), index=False)
print(fx[["target", "parca", "n", "t", "t_is", "t_oos", "bp_per_sd", "med_dv_mn", "cost_rt_bp"]].round(2).to_string(index=False))

print("\n(b2) İşlem kuralı: SPY z1>=+1 (60g oynaklığa göre) -> FXE/FXF/FXY/FXB long; SPY z1<=-1 -> UUP long; h=1")
zs = lib.zret(lib.load("SPY")["c"], 1)
kr = []
for T, cond, lab in [("FXE", zs >= 1, "SPYz>=1"), ("FXF", zs >= 1, "SPYz>=1"), ("FXY", zs >= 1, "SPYz>=1"), ("FXB", zs >= 1, "SPYz>=1"),
                     ("UUP", zs <= -1, "SPYz<=-1"), ("FXE", zs >= 2, "SPYz>=2"), ("UUP", zs <= -2, "SPYz<=-2"), ("FXY", zs >= 2, "SPYz>=2")]:
    df = td.load(T)
    for m in ("C0", "O1", "C1"):
        s, _ = td.full_eval(df, cond, 1, m, label=lab, sym=T, warm=60)
        kr.append(td.row(s, {"kural": lab}))
kr = pd.DataFrame(kr)
kr.to_csv(os.path.join(td.OUT, "leadlag_fx_kural.csv"), index=False)
print(kr[["kural", "sym", "mode", "n", "mean_gross_bp", "t_gross", "mean_net_bp", "net_bp_10000", "t", "is_net_bp", "oos_net_bp"]].round(2).to_string(index=False))

# ---------------- (c) HY <- SPY ----------------
print("\n(c) HYG/JNK/USHY <- SPY (kendi gecikmesi kontrollü)")
hy = []
for T in ["HYG", "JNK", "USHY", "BKLN", "EMB"]:
    for L in ["SPY", "QQQ"]:
        for h in (1, 3):
            hy.append(lagreg(T, R[L], h, label=L))
hy = pd.DataFrame(hy)
hy.to_csv(os.path.join(td.OUT, "leadlag_hy_spy.csv"), index=False)
print(hy.round(2).to_string(index=False))

# ---------------- (d) yetişme: öncü katkısı kendi gecikmesine karşı ----------------
print("\n(d) Yetişme (catch-up): fy = a + b*own + k*gap; gap = beta60*r_L - r_T (dağıtım düzeltmeli veri)")
X = {}
for L in ["SPY", "QQQ", "IEF", "SHY", "TLT", "XLF", "XLK"]:
    X[L] = R[L] if L in R else np.log(lib.load(L)["c"]).diff().reindex(IDX)
vix = lib.vol_index("VIX").reindex(IDX); X["VIX_dlog"] = np.log(vix).diff()
X["DGS2_d"] = td.yld("DGS2").ffill().diff()
cc = []
for T, L in [("BIL", "VIX_dlog"), ("BIL", "XLF"), ("SGOV", "VIX_dlog"), ("SGOV", "QQQ"), ("GOVT", "IEF"), ("GOVT", "SHY"), ("GOVT", "DGS2_d"),
             ("TBT", "IEF"), ("TIP", "IEF"), ("SCHP", "IEF"), ("STIP", "SHY")]:
    xs = X[L]
    for ver in ("duzeltilmis", "eski_lib"):
        yT = R[T] if ver == "duzeltilmis" else np.log(lib.load(T)["c"]).diff().reindex(IDX)
        d = pd.DataFrame({"y": yT, "x": xs}).dropna()
        beta = d.y.rolling(60).cov(d.x) / d.x.rolling(60).var()
        gap = beta * d.x - d.y
        for h in (1, 3):
            fy = fwd(yT, h).reindex(d.index)
            dd = pd.DataFrame({"fy": fy, "own": d.y, "gap": gap}).dropna()
            b0, t0 = nw(dd.fy.values, np.column_stack([np.ones(len(dd)), dd.gap.values]), h)
            b1, t1 = nw(dd.fy.values, np.column_stack([np.ones(len(dd)), dd.own.values, dd.gap.values]), h)
            bo, to = nw(dd.fy.values, np.column_stack([np.ones(len(dd)), dd.own.values]), h)
            cc.append({"target": T, "leader": L, "veri": ver, "h": h, "n": len(dd), "t_catch_yalniz": t0[1], "t_catch_kontrollu": t1[2],
                       "t_kendi_gecikme": to[1], "catch_bp_per_sd_kontrollu": b1[2] * dd.gap.std() * 1e4,
                       "cost_rt_bp": scr.loc[T, "cost_rt_bp"]})
cc = pd.DataFrame(cc)
cc.to_csv(os.path.join(td.OUT, "leadlag_catch_kontrollu.csv"), index=False)
print(cc.round(2).to_string(index=False))

# ---------------- (e) izleme ETF'leri için aday öncüler ----------------
print("\n(e) İzleme ETF'leri: aday öncüler (kendi gecikmesi kontrollü)")
cand = {}
for nm in ["DGS10", "DGS2", "DGS30", "DFII10", "T10YIE"]:
    cand[nm + "_d"] = td.yld(nm).ffill().diff()
cand["T10Y2Y_d"] = (td.yld("DGS10") - td.yld("DGS2")).ffill().diff()
cand["SPY"] = R["SPY"]; cand["QQQ"] = R["QQQ"]; cand["HYG"] = R["HYG"]; cand["LQD"] = R["LQD"]; cand["UUP"] = R["UUP"]; cand["FXY"] = R["FXY"]
cand["VIX_dlog"] = X["VIX_dlog"]; cand["GLD"] = R["GLD"]; cand["USO"] = R["USO"]
cand["CPER/GLD_d"] = np.log(lib.load("CPER")["c"].reindex(IDX) / lib.load("GLD")["c"].reindex(IDX)).diff()
cand["TLT"] = R["TLT"]; cand["IEF"] = R["IEF"]; cand["TIP"] = R["TIP"]
ld = []
for T in ["TLT", "TMF", "TMV", "TBT", "EDV", "UUP"]:
    for L, s in cand.items():
        if L == T: continue
        for h in (1, 3):
            rr = lagreg(T, s, h, label=L); ld.append(rr)
ld = pd.DataFrame(ld).dropna(subset=["t"])
ld["p"] = 2 * st.norm.sf(ld.t.abs())
ld["fdr10"] = lib.bh_fdr(ld.p.values, 0.10)
ld["isoos_ayni"] = np.sign(ld.t_is) == np.sign(ld.t_oos)
ld["cost_rt_bp"] = ld.target.map(scr.cost_rt_bp)
ld["ekonomik"] = ld.bp_per_sd.abs() > ld.cost_rt_bp
ld["gecerli_oncu"] = ld.fdr10 & ld.isoos_ayni & ld.ekonomik
ld.to_csv(os.path.join(td.OUT, "leadlag_izleme_oncu.csv"), index=False)
print("Test:", len(ld), " FDR:", int(ld.fdr10.sum()), " FDR+IS/OOS aynı işaret:", int((ld.fdr10 & ld.isoos_ayni).sum()),
      " + ekonomik (>maliyet):", int(ld.gecerli_oncu.sum()))
print(ld.sort_values("p").head(25)[["target", "leader", "h", "n", "t", "t_is", "t_oos", "bp_per_sd", "cost_rt_bp", "fdr10", "gecerli_oncu"]]
      .round(2).to_string(index=False))

# eşzamanlı sürücüler (son 252 gün korelasyon/beta) — öncü DEĞİL
sv = []
last = IDX[-252:]
for T in ["TLT", "TMF", "TMV", "TBT", "EDV", "UUP"]:
    for L, s in cand.items():
        if L == T: continue
        d = pd.DataFrame({"y": R[T], "x": s}).loc[last].dropna()
        if len(d) < 100: continue
        sv.append({"target": T, "driver": L, "corr_1y": d.y.corr(d.x), "beta_1y": d.y.cov(d.x) / d.x.var()})
sv = pd.DataFrame(sv)
sv["abs"] = sv.corr_1y.abs()
sv = sv.sort_values(["target", "abs"], ascending=[True, False])
sv.to_csv(os.path.join(td.OUT, "leadlag_suruculer.csv"), index=False)
print("\nEşzamanlı sürücüler (son 1 yıl, ilk 6):")
print(sv.groupby("target").head(6).round(3).to_string(index=False))
