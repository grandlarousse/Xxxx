"""5) Lead-lag denetimi: (i) leadlag_sweep'te aile hedeflerinde FDR bayrakları; (ii) en güçlü FDR'siz adayları bağımsız
yeniden tahmin (kendi gecikmesi kontrollü, Newey-West, IS/OOS); (iii) etki büyüklüğü vs maliyet; (iv) IWM<-SPY ters işaretinin
kontrolü; (v) bayat fiyat kontrolü (düşük hacimli aile ETF'lerinde hedefin önceki gün getirisi ile öncü çakışması)."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import dt, lib
from scipy import stats as st
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
L = pd.read_csv(os.path.join(lib.ROOT, "sonuclar", "leadlag_sweep.csv"))
FAM = ("SPY VOO IVV QQQ QQQM DIA IWM MDY RSP VTI TQQQ SQQQ UPRO SPXU SPXL SPXS SSO SDS QLD QID UDOW SDOW TNA TZA SH PSQ URTY SRTY MTUM QUAL USMV VLUE IWF IWD IWO IWN SCHD JEPI JEPQ VUG VTV SPLV SPHB VIG DGRO DVY NOBL QYLD XYLD SPYD COWZ AVUV SCHG MGK VYM").split()
x = L[L.target.isin(FAM)]
print("aile satırı:", len(x), "| fdr10_lag_t_h1:", int(x.fdr10_lag_t_h1.sum()), "| fdr10_lag_t_h3:", int(x.fdr10_lag_t_h3.sum()),
      "| fdr10_catch h1/h3:", int(x.fdr10_catch_t_h1.sum()), int(x.fdr10_catch_t_h3.sum()))
print("lag FDR (global) geçen aile satırları:")
print(x[x.fdr10_lag_t_h1 | x.fdr10_lag_t_h3][["target", "leader", "lag_t_h1", "lag_t_h3", "lag_t_h1_is", "lag_t_h1_oos", "lag_t_h3_is", "lag_t_h3_oos"]].to_string(index=False))

def nw(y, X, lags):
    xtx = np.linalg.inv(X.T @ X); b = xtx @ X.T @ y; e = y - X @ b; u = X * e[:, None]; S = u.T @ u
    for l in range(1, lags + 1):
        w = 1 - l / (lags + 1); G = u[l:].T @ u[:-l]; S += w * (G + G.T)
    V = xtx @ S @ xtx
    return b, b / np.sqrt(np.diag(V))

spy = lib.load("SPY"); idx = spy.index
def lr(s): return np.log(lib.load(s)["c"]).diff().reindex(idx)
def fwd(r, h): return pd.Series(r[::-1].rolling(h).sum()[::-1].values, index=r.index).shift(-1)
LEAD = {"TIP": lr("TIP"), "SPY": lr("SPY"), "LQD": lr("LQD"), "DFII10_d": lib.fred("DFII10").reindex(idx).diff(),
        "DGS10_d": lib.fred("DGS10").reindex(idx).diff(), "VIX_dlog": np.log(lib.vol_index("VIX").reindex(idx)).diff()}
ROWS = []
for T in ("SPY", "QQQ", "IWM", "RSP", "DIA", "MDY"):
    y0 = lr(T)
    for Ln, xl in LEAD.items():
        if Ln == T: continue
        for h in (1, 3):
            d = pd.DataFrame({"fy": fwd(y0, h), "own": y0, "x": xl}).dropna()
            # DFII10/DGS10 (Hazine eğrisi ~15:30 ET kotasyonları, akşam yayımlanır) -> t'de C0 için bilinmez; O1/C1 için bilinir.
            X = np.column_stack([np.ones(len(d)), d["own"], d["x"]])
            b, t = nw(d["fy"].values, X, h)
            rec = {"target": T, "leader": Ln, "h": h, "t": t[2], "bp_per_sd": b[2] * d["x"].std() * 1e4}
            for nm, m in (("is", d.index <= dt.IS_END), ("oos", d.index > dt.IS_END)):
                dd = d[m]; Xs = np.column_stack([np.ones(len(dd)), dd["own"], dd["x"]])
                bb, tt = nw(dd["fy"].values, Xs, h); rec[f"t_{nm}"] = tt[2]; rec[f"bp_per_sd_{nm}"] = bb[2] * dd["x"].std() * 1e4
            # sadece kendi gecikmesi olmadan
            b0, t0 = nw(d["fy"].values, np.column_stack([np.ones(len(d)), d["x"]]), h); rec["t_kontrolsuz"] = t0[1]
            ROWS.append(rec)
R = pd.DataFrame(ROWS)
R["p"] = 2 * st.norm.sf(R.t.abs()); R["fdr10_bu_kume"] = lib.bh_fdr(R.p.values, 0.10)
R["ayni_isaret"] = np.sign(R.t_is) == np.sign(R.t_oos)
R.to_csv(os.path.join(dt.OUT, "leadlag_yeniden.csv"), index=False)
print(R.round(2).sort_values("t", key=abs, ascending=False).head(20).to_string(index=False))
print("Bu küçük kümede (", len(R), "test) BH-FDR geçen:", int(R.fdr10_bu_kume.sum()))
# ekonomik büyüklük: 1 sd'lik öncü hareketi için 3 günlük beklenen getiri ~ 20-30 bp; z>1 günlerinde ortalama |z|~1.5 -> ~30-40 bp brüt,
# maliyet 13 bp (2.500$) / 31 bp (1.000$).
# (iv) IWM<-SPY ters işaret: kendi gecikmesi + SPY'ın kendi gecikmesi kontrolüyle (SPY'ın günlük ortalamaya dönüşü IWM'e mi taşınıyor?)
y = lr("IWM"); xs = lr("SPY")
for h in (1, 3):
    d = pd.DataFrame({"fy": fwd(y, h), "own": y, "spy": xs, "spyf": fwd(xs, h)}).dropna()
    b, t = nw(d.fy.values, np.column_stack([np.ones(len(d)), d.own, d.spy]), h)
    b2, t2 = nw((d.fy - d.spyf).values, np.column_stack([np.ones(len(d)), d.own, d.spy]), h)
    print(f"IWM<-SPY h{h}: IWM ileri getiri t(SPY)={t[2]:.2f}; (IWM-SPY) ileri getiri t(SPY)={t2[2]:.2f} -> göreli etki")
# (v) bayat fiyat: düşük hacimli aile ETF'lerinde (XYLD, SPYD, DVY, NOBL, SPHB, URTY, SRTY) r_T(t) ile r_SPY(t+1) korelasyonu
print("Bayat fiyat kontrolü: corr(r_SPY(t), r_T(t+1)) ve corr(r_T(t), r_T(t+1))")
for T in ("XYLD", "SPYD", "DVY", "NOBL", "SPHB", "URTY", "SRTY", "QYLD", "SPY", "IWM"):
    rt = lr(T); rs = lr("SPY")
    print(f"  {T}: corr(SPY_t, T_t+1)={rs.corr(rt.shift(-1)):.3f}  otokor(T)={rt.corr(rt.shift(1)):.3f}")

# (vi) T10YIE 'yetişme' (kontrollü) 2020 dahil/hariç: gap = beta60*dT10YIE - r_T ; fy(h3) ~ own + gap
t10 = lib.fred("T10YIE").reindex(idx).diff()
for T in ("SPY", "QQQ", "IWM"):
    y0 = lr(T); df = pd.DataFrame({"y": y0, "x": t10}).dropna()
    beta60 = df.y.rolling(60).cov(df.x) / df.x.rolling(60).var(); gap = beta60 * df.x - df.y
    d2 = pd.DataFrame({"fy": fwd(y0, 3).reindex(df.index), "own": df.y, "gap": gap}).dropna()
    for lab, m in (("tum", np.ones(len(d2), bool)), ("2020_haric", d2.index.year != 2020), ("OOS", d2.index > dt.IS_END)):
        dd = d2[m]; b, t = nw(dd.fy.values, np.column_stack([np.ones(len(dd)), dd.own, dd.gap]), 3)
        print(f"T10YIE yetişme {T} h3 {lab}: t(gap)={t[2]:.2f}")
