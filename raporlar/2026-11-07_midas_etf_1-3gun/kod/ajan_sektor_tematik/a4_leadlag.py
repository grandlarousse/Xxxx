"""Görev 4: lead-lag ek testleri (sektor_tematik).
(A) Genişletilmiş öncü regresyonu: r_T(t+1..t+h) = a + b*r_T(t) + c*r_L(t)  (Newey-West, h=1,3), IS/OOS.
    Öncüler: süpürmedeki ETF'lere ek olarak NVDA, TSM, AVGO (hisse), EWT, EWY, SOXX, QQQ.
(B) Süpürmede FDR'den geçen negatif gecikmelerin (QQQ->IGV/SKYY/WCLD/CIBR, EEM->KWEB) işlem kuralına çevrilmesi
    (maliyetli, C0/O1/C1) ve öncünün katkısının kendi gecikmesine karşı ayrıştırılması.
(C) İzleme ETF'leri için eşzamanlı sürücüler (corr_1y, beta_1y; öncü DEĞİL).
Çıktılar: sonuclar/aile_sektor_tematik/leadlag_ek.csv, leadlag_kural.csv, suruculer.csv"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from havuz import *

sys.path.insert(0, KOD)
from leadlag_sweep import nw_t, fwd


def lr(s):
    return np.log(D(s)["c"]).diff()


IDX = D("SPY").index
# ---------------- (A) ----------------
TARGETS = ["SMH", "SOXX", "XLK", "IGV", "XBI", "KRE", "XLE", "KWEB", "ARKK", "COPX", "URA"]
LEAD_EXTRA = {"SMH": ["NVDA", "TSM", "AVGO", "EWT", "EWY", "QQQ", "SOXX"],
              "SOXX": ["NVDA", "TSM", "AVGO", "EWT", "EWY", "QQQ"],
              "XLK": ["NVDA", "AAPL", "MSFT", "AVGO", "QQQ", "SMH"],
              "IGV": ["MSFT", "QQQ", "XLK", "SPY", "SMH"],
              "XBI": ["IBB", "IWM", "QQQ", "SPY"], "KRE": ["XLF", "IWM", "TLT", "SPY"],
              "XLE": ["USO", "BNO", "XOP", "SPY"], "KWEB": ["FXI", "EEM", "QQQ", "SPY"],
              "ARKK": ["QQQ", "IWM", "TSLA", "COIN"], "COPX": ["CPER", "XME", "EEM", "FXI"], "URA": ["NLR", "SPY", "XLE"]}
rows = []
for T in TARGETS:
    y0 = lr(T).reindex(IDX)
    for L in LEAD_EXTRA[T]:
        x = lr(L).reindex(IDX)
        df = pd.DataFrame({"y": y0, "x": x}).dropna()
        rec = {"target": T, "leader": L, "n": len(df)}
        last = df.tail(252); rec["corr_1y"] = last.y.corr(last.x)
        rec["beta_1y"] = np.cov(last.y, last.x)[0, 1] / np.var(last.x, ddof=1)
        for h in (1, 3):
            fy = fwd(y0, h).reindex(df.index)
            d2 = pd.DataFrame({"fy": fy, "x": df.x, "own": df.y}).dropna()
            X = np.column_stack([np.ones(len(d2)), d2.own, d2.x])
            b, t = nw_t(d2.fy.values, X, h)
            rec[f"own_b_h{h}"] = b[1]; rec[f"own_t_h{h}"] = t[1]; rec[f"lag_b_h{h}"] = b[2]; rec[f"lag_t_h{h}"] = t[2]
            rec[f"lag_bp_per_sd_h{h}"] = b[2] * d2.x.std() * 1e4
            # öncü tek başına (kendi gecikmesi olmadan) -> fark kendi gecikmesinin payını gösterir
            b0, t0 = nw_t(d2.fy.values, np.column_stack([np.ones(len(d2)), d2.x]), h)
            rec[f"lag_only_t_h{h}"] = t0[1]
            for nm, m in (("is", d2.index <= lib.IS_END), ("oos", d2.index > lib.IS_END)):
                dd = d2[m]
                bb, tt = nw_t(dd.fy.values, np.column_stack([np.ones(len(dd)), dd.own, dd.x]), h)
                rec[f"lag_t_h{h}_{nm}"] = tt[2]
        rec["p_h1"] = lib.t_to_p(rec["lag_t_h1"], rec["n"]); rec["p_h3"] = lib.t_to_p(rec["lag_t_h3"], rec["n"])
        rows.append(rec)
A = pd.DataFrame(rows)
A["fdr10_h1"] = lib.bh_fdr(A.p_h1.values, 0.10); A["fdr10_h3"] = lib.bh_fdr(A.p_h3.values, 0.10)
A.to_csv(os.path.join(OUT, "leadlag_ek.csv"), index=False)
pd.set_option("display.width", 260); pd.set_option("display.max_rows", 200)
print("(A) ek öncü testleri:", len(A) * 2, "test")
print(A[["target", "leader", "corr_1y", "own_t_h1", "lag_t_h1", "lag_t_h1_is", "lag_t_h1_oos", "lag_only_t_h1", "lag_bp_per_sd_h1",
         "lag_t_h3", "lag_t_h3_is", "lag_t_h3_oos", "lag_bp_per_sd_h3", "fdr10_h1", "fdr10_h3"]].round(2).to_string())

# ---------------- (B) kural ----------------
def z1(s, n=60):
    r = lr(s); return r / r.rolling(n).std().shift(1)

K = []
CASES = [("QQQ", "IGV"), ("QQQ", "SKYY"), ("QQQ", "WCLD"), ("QQQ", "CIBR"), ("EEM", "KWEB")]
for L, T in CASES:
    zl = z1(L).reindex(D(T).index); zt = z1(T)
    resid = lr(T) - lr(L).reindex(D(T).index)  # basit fark
    defs = {f"{L}_z<-1 -> al {T}": zl < -1,
            f"{L}_z>+1 -> al {T} (beklenen negatif)": zl > 1,
            f"{L}_z<-1 & {T} kendi z>-1 -> al {T}": (zl < -1) & (zt > -1),
            f"kontrol: {T} kendi z<-1 -> al {T}": zt < -1,
            f"kontrol: {L}_z<-1 -> al {L}": None}
    for nm, sig in defs.items():
        for mode in ("C0", "O1", "C1"):
            for h in (1, 2, 3):
                if sig is None:
                    tr = run_sym(L, z1(L) < -1, h, mode)
                else:
                    tr = run_sym(T, sig, h, mode)
                s = summarize(tr, nm, per_sym=False); s.update({"leader": L, "target": T, "mode": mode, "h": h})
                s["p"] = lib.t_to_p(s.get("t_naive", np.nan), s.get("n", 0))
                K.append(s)
K = pd.DataFrame(K); K.to_csv(os.path.join(OUT, "leadlag_kural.csv"), index=False)
print("\n(B) kural testleri:", len(K))
print(K[(K.h == 1)][["label", "mode", "h", "n", "mean_gross_bp", "mean_net_bp", "t_naive", "is_net_bp", "oos_net_bp", "years_pos_frac", "win"]].round(2).to_string())

# ---------------- (C) sürücüler ----------------
WATCH = ["SMH", "SOXX", "SOXL", "XLK", "TECL", "IGV", "XBI", "KRE", "XLE", "XOP", "KWEB", "COPX", "ARKK", "URA", "XLF", "LABU"]
DRV = ["SPY", "QQQ", "IWM", "SMH", "XLK", "NVDA", "TSM", "AVGO", "MSFT", "XLF", "KRE", "TLT", "USO", "BNO", "XLE", "CPER", "GLD",
       "EEM", "FXI", "IBB", "XBI", "IBIT", "UUP"]
COPY = {s: set(v) for v in CLUSTERS.values() for s in v}
C = []
vix = np.log(lib.vol_index("VIX").reindex(IDX)).diff()
d10 = lib.fred("DGS10").reindex(IDX).diff()
for T in WATCH:
    y = lr(T).reindex(IDX)
    cand = {L: lr(L).reindex(IDX) for L in DRV if L not in COPY.get(T, {T}) and L != T and L not in (UNDER.get(T),)}
    cand["VIX_dlog"] = vix; cand["DGS10_d"] = d10
    for L, x in cand.items():
        d = pd.DataFrame({"y": y, "x": x}).dropna().tail(252)
        if len(d) < 120: continue
        C.append({"target": T, "driver": L, "corr_1y": d.y.corr(d.x), "beta_1y": np.cov(d.y, d.x)[0, 1] / np.var(d.x, ddof=1)})
C = pd.DataFrame(C); C["abs"] = C.corr_1y.abs()
C = C.sort_values(["target", "abs"], ascending=[True, False]); C.to_csv(os.path.join(OUT, "suruculer.csv"), index=False)
print("\n(C) sürücüler (ilk 4)")
print(C.groupby("target").head(4).round(2).to_string())
