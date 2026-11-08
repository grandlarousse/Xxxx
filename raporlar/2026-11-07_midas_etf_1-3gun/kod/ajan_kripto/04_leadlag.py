"""4) Lead-lag: leadlag_sweep.csv aile özeti + ek testler. Çalıştır: python3 -I kod/ajan_kripto/04_leadlag.py
 (a) sweep: aile hedefleri için eşzamanlı sürücüler (corr_1y/beta_1y) ve gecikmeli öncü adayları (FDR, IS/OOS, bp/sd)
 (b) ek: BTC 16:00 ET getirisi (t) -> hedef (t+1, t+1..t+3); hedefin kendi gecikmesi kontrollü (Newey-West),
     'yetişme' u_t = beta60*r_BTC,t - r_T,t'nin öncü katkısı: r_T(t+1) = a + b*u_t + c*r_T,t  (kendi getirisini ayrıca kontrol)
 (c) yetişme kuralının maliyetli backtesti (TH06 benzeri): u_t >= +2 sd(60) -> hedefte C0 long, çıkış C_t+1 (ve C1/O1)
 (d) gerçek zamanlı: BTC 16:00->09:30 ET hareketi -> IBIT açılış boşluğu (R²) ve aynı günün IBIT gün içi getirisi (kural testi)
Çıktı: sonuclar/aile_kripto/leadlag_aile.csv, leadlag_ek_testler.csv, leadlag_kural_testleri.csv"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import kr, lib

pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40); pd.set_option("display.max_rows", 300)
L = pd.read_csv(os.path.join(kr.ROOT, "sonuclar", "leadlag_sweep.csv"))
x = L[L.target.isin(kr.FAM)].copy()
n_sweep = len(x) * 4
x["fdr_any"] = x[["fdr10_lag_t_h1", "fdr10_lag_t_h3", "fdr10_catch_t_h1", "fdr10_catch_t_h3"]].any(axis=1)
# aile içi yeniden BH (aile alt kümesinde)
for c in ["lag_t_h1", "lag_t_h3", "catch_t_h1", "catch_t_h3"]:
    x["fdr_aile_" + c] = lib.bh_fdr(x["p_" + c].values, 0.10)
x.to_csv(os.path.join(kr.OUT, "leadlag_aile.csv"), index=False)
print("Sweep aile satırı:", len(x), " test (4 tür):", n_sweep, " global FDR geçen:", int(x.fdr_any.sum()),
      " aile içi FDR geçen:", {c: int(x["fdr_aile_" + c].sum()) for c in ["lag_t_h1", "lag_t_h3", "catch_t_h1", "catch_t_h3"]})
# IS ve OOS'ta aynı işaret + |t|>=2 olan gecikmeli satırlar (yalnız IS'i olan hedefler: BLOK)
cand = x[((x.lag_t_h1_is * x.lag_t_h1_oos > 0) & (x.lag_t_h1.abs() >= 2)) | ((x.lag_t_h3_is * x.lag_t_h3_oos > 0) & (x.lag_t_h3.abs() >= 2))]
print("IS/OOS aynı işaret ve |t|>=2 gecikmeli satırlar:")
print(cand[["target", "leader", "n", "lag_t_h1", "lag_t_h1_is", "lag_t_h1_oos", "lag_bp_per_sd_h1", "lag_t_h3", "lag_t_h3_is", "lag_t_h3_oos", "lag_bp_per_sd_h3"]].round(2).to_string(index=False))

# ----------------------------------------------------------------------------------------------
BTC = kr.crypto_et_proxy("BTC-USD"); ETH = kr.crypto_et_proxy("ETH-USD")
rb = np.log(BTC["c"]).diff(); re_ = np.log(ETH["c"]).diff()
TGT = {s: lib.load(s) for s in ["IBIT", "ETHA", "BITX", "ETHU", "MSTU", "CONL", "BLOK", "BITO"]}
TGT["MSTR"] = kr.stock("MSTR"); TGT["COIN"] = kr.stock("COIN")
ek = []
def fwd(r, h): return r[::-1].rolling(h).sum()[::-1].shift(-1)
for T, df in TGT.items():
    for Lname, rl in (("BTC_16ET", rb), ("ETH_16ET", re_)):
        if T in ("IBIT", "BITX", "BITO") and Lname == "BTC_16ET": continue   # aynı dayanak (corr~1): anlamsız
        if T in ("ETHA", "ETHU") and Lname == "ETH_16ET": continue
        ry = np.log(df["c"]).diff()
        d = pd.DataFrame({"y": ry, "x": rl.reindex(ry.index)}).dropna()
        d = d[d.index >= "2023-06-01"]
        beta60 = d.y.rolling(60).cov(d.x) / d.x.rolling(60).var()
        d["u"] = beta60 * d.x - d.y
        for h in (1, 3):
            d["fy"] = fwd(ry, h).reindex(d.index)
            dd = d.dropna()
            if len(dd) < 200: continue
            X1 = np.column_stack([np.ones(len(dd)), dd.y.values, dd.x.values])
            b1, t1 = kr.nw_t(dd.fy.values, X1, h)
            X2 = np.column_stack([np.ones(len(dd)), dd.u.values])
            b2, t2 = kr.nw_t(dd.fy.values, X2, h)
            X3 = np.column_stack([np.ones(len(dd)), dd.u.values, dd.y.values])
            b3, t3 = kr.nw_t(dd.fy.values, X3, h)
            half = len(dd) // 2
            sub = []
            for part in (dd.iloc[:half], dd.iloc[half:]):
                bb, tt = kr.nw_t(part.fy.values, np.column_stack([np.ones(len(part)), part.u.values, part.y.values]), h)
                sub.append(tt[1])
            ek.append({"hedef": T, "oncu": Lname, "h": h, "n": len(dd), "basla": str(dd.index[0].date()),
                       "corr_ayni_gun": dd.y.corr(dd.x), "lag_t_kendi_kontrollu": t1[2], "lag_bp_per_sd": b1[2] * dd.x.std() * 1e4,
                       "kendi_gecikme_t": t1[1],
                       "yetisme_t_ham": t2[1], "yetisme_bp_per_sd": b2[1] * dd.u.std() * 1e4,
                       "yetisme_t_kendi_kontrollu": t3[1], "yetisme_bp_per_sd_kontrollu": b3[1] * dd.u.std() * 1e4,
                       "kendi_t_yetisme_modelinde": t3[2], "yetisme_t_1yari": sub[0], "yetisme_t_2yari": sub[1]})
EK = pd.DataFrame(ek)
from scipy import stats as st
for c in ["lag_t_kendi_kontrollu", "yetisme_t_kendi_kontrollu"]:
    EK["p_" + c] = 2 * st.norm.sf(EK[c].abs())
EK.to_csv(os.path.join(kr.OUT, "leadlag_ek_testler.csv"), index=False)
print("\n=== Ek lead-lag (2023-06+, BTC/ETH 16:00 ET) ===")
print(EK.round(2).to_string(index=False))

# ----------------------------------------------------------------------------------------------
# (c) yetişme kuralı backtest: u_t >= 2*sd60(u) -> hedef long; u_t <= -2 sd -> (long-only) sinyal yok
kural = []
for T in ["MSTU", "CONL", "BLOK", "ETHA", "ETHU"]:
    df = TGT[T]; ry = np.log(df["c"]).diff()
    for Lname, rl in (("BTC_16ET", rb),) if T != "ETHA" and T != "ETHU" else (("BTC_16ET", rb),):
        d = pd.DataFrame({"y": ry, "x": rl.reindex(ry.index)}).dropna()
        beta60 = d.y.rolling(60).cov(d.x) / d.x.rolling(60).var()
        u = beta60 * d.x - d.y
        z = u / u.rolling(60).std()
        for side, sig in (("u>=+2sd", z >= 2), ("u<=-2sd", z <= -2)):
            for mode in ("C0", "O1", "C1"):
                s, tr = kr.full_eval(df, sig.reindex(df.index).fillna(False), 1, mode, kr.spread_bp(T), label=f"{T}<-{Lname} {side}")
                s.update({"hedef": T, "oncu": Lname, "kural": side})
                kural.append(s)
# (d) gerçek zamanlı: BTC gece hareketi -> IBIT gün içi (O1, h=1): sinyal açılışta bilinir (BTC 16:00->09:30)
I = TGT["IBIT"]
night = np.log(BTC["o"] / BTC["c"].shift(1))
zn = night / night.rolling(60).std()
for side, sig in (("BTC_gece_z>=+1", zn >= 1), ("BTC_gece_z<=-1", zn <= -1)):
    # O1 modunda sinyal t'de olmalı: açılış t+1'deki bilgi -> sinyali bir gün geri kaydır (t+1 gecesi t'nin sinyali gibi)
    sg = sig.shift(-1).reindex(I.index).fillna(False)
    for etf in ("IBIT", "SBIT", "BITI", "BITX"):
        df = lib.load(etf)
        s, tr = kr.full_eval(df, sg.reindex(df.index).fillna(False), 1, "O1", kr.spread_bp(etf), label=f"{etf} {side} (açılışta bilinen)")
        s.update({"hedef": etf, "oncu": "BTC_16ET->0930ET", "kural": side})
        kural.append(s)
# (e) BLOK <- reel faiz kanalı (sweep'te IS ve OOS aynı işaret, FDR yok): TIP günlük getiri z>=+1 / DFII10 değişim z<=-1 -> BLOK long h=3
B = TGT["BLOK"]
tip = lib.load("TIP")["c"].pct_change(); ztip = tip / tip.rolling(60).std()
dfii = lib.fred("DFII10").reindex(B.index).ffill().diff(); zdf = dfii / dfii.rolling(60).std()
for side, sig in (("TIP_z>=+1", ztip >= 1), ("DFII10_dz<=-1", zdf <= -1)):
    for mode in ("C0", "O1", "C1"):
        s, tr = kr.full_eval(B, sig.reindex(B.index).fillna(False), 3, mode, kr.spread_bp("BLOK"), label=f"BLOK {side} h3")
        s.update({"hedef": "BLOK", "oncu": side, "kural": side})
        kural.append(s)
K = pd.DataFrame(kural)
K.to_csv(os.path.join(kr.OUT, "leadlag_kural_testleri.csv"), index=False)
print("\n=== Lead-lag kural testleri (maliyetli, 2.500$) ===")
print(K[["label", "mode", "n", "mean_gross_bp", "mean_net_bp", "t", "is_net_bp", "oos_net_bp", "win", "pf", "years_pos_frac", "h1_net_bp", "h2_net_bp", "net_10000"]].round(2).to_string(index=False))
print("\nEk test sayısı: ek regresyon", len(EK) * 2, "+ kural", len(K))
