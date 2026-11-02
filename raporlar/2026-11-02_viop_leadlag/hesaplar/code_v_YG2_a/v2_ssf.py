"""v_YG2_a / 2: VİOP pay vadelisi (SSF) ile işlenebilirlik.
Zamanlama (BIST): spot kapanış seansı 18:00-18:05 (fiyat 18:05'te belirlenir), kapanış fiyatından işlemler 18:08-18:10.
SSF normal seansı 23.09.2022'den beri 09:30-18:15 (öncesi 18:10). Günlük uzlaşma = seansın son 10 dk'sındaki (18:05-18:15)
işlemlerin miktar ağırlıklı ortalaması (10 işlemden azsa son 10 işlem). => uzlaşma fiyatı, C BİLİNDİKTEN SONRA oluşan, SSF'de
ulaşılabilir bir VWAP vekili.
Testler:
 (1) Uzlaşma fiyatı C'yi mi izliyor, 'adil' fiyatı mı?  dbasis_t = log(F_t/C_t) - log(F_{t-1}/C_{t-1}) (aynı sözleşme) ~ CA_t
     F adil fiyatı izliyorsa eğim ≈ -(geçici pay) ≈ -0,35; C'yi izliyorsa ≈ 0.
 (2) SSF stratejisi: giriş F_settle_t, çıkış t+1 07:30 vekili  F̂ = P0730_{t+1} * exp(basis_{t+1}),  basis = log(settle/C)
     => pnl_SSF = pnl_spot(C->07:30) - sign(CA)*(basis_{t+1}-basis_t)  [ -sign(CA) pozisyon ]
     ve SSF kapanıştan kapanışa: -sign(CA)*log(F_{t+1}/F_t) (taşıma düzeltmeli).
Vade sonu günü dolan sözleşme C'de uzlaşır -> bir sonraki vade kullanılır (expiry > t+1).
"""
import numpy as np, pandas as pd, vcommon as v
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
P = v.load()
V47 = [s for s in P.stock.unique() if s not in ("XU030", "XU100")]
S = P[P.stock.isin(V47)].copy()
days = np.sort(P.date.unique()); half = days[len(days) // 2]
F = pd.read_parquet(v.SCR + "/data/viop_panel.parquet", columns=["date", "code", "root", "segment", "expiry", "settle", "close", "vwap", "trades", "value_tl"])
F = F[(F.segment == "SSF") & (F.date >= "2023-11-01") & F.root.isin(V47)].copy()
F["date"] = pd.to_datetime(F["date"]).dt.normalize(); F["expiry"] = pd.to_datetime(F["expiry"]).dt.normalize()
# her gün için: expiry > sonraki işlem günü olan en yakın vade (t ve t+1'de aynı sözleşme)
dser = pd.Series(days); nxt = dict(zip(days[:-1], days[1:]))
F["nextday"] = F["date"].map(nxt)
G = F[F.expiry > F.nextday].sort_values(["root", "date", "expiry"]).groupby(["root", "date"]).head(1)
G = G[["root", "date", "code", "expiry", "settle", "close", "vwap", "trades", "value_tl"]].rename(columns={"root": "stock"})
# aynı sözleşmenin t+1 değerleri
F2 = F[["code", "date", "settle", "close", "trades"]].rename(columns={"date": "nextday", "settle": "settle1", "close": "close1", "trades": "trades1"})
G = G.merge(F[["code", "date", "nextday"]], on=["code", "date"]).merge(F2, on=["code", "nextday"], how="left")
# t-1 değerleri (aynı sözleşme)
prv = dict(zip(days[1:], days[:-1]))
G["prevday"] = G["date"].map(prv)
F0 = F[["code", "date", "settle"]].rename(columns={"date": "prevday", "settle": "settle0"})
G = G.merge(F0, on=["code", "prevday"], how="left")
S = S.merge(G, on=["stock", "date"], how="left")
# t+1 ve t-1 spot kapanışları
g = S.groupby("stock")
S["C1"] = g["C"].shift(-1); S["C0"] = g["C"].shift(1); S["P7_1"] = g["P0730"].shift(-1)
S["tau"] = (S["expiry"] - S["date"]).dt.days
S["basis"] = np.log(S["settle"] / S["C"]); S["basis1"] = np.log(S["settle1"] / S["C1"]); S["basis0"] = np.log(S["settle0"] / S["C0"])
for c in ["basis", "basis1", "basis0"]:
    S.loc[S[c].abs() > 0.15, c] = np.nan
S["dbasis"] = S["basis"] - S["basis0"]
S["dbasis1"] = S["basis1"] - S["basis"]
S["settle_vs_P1500"] = np.log(S["settle"] / S["P1500"])
S["liq_ok"] = S["trades"] >= 200  # gün içi 200+ işlem: son 10 dk'da >=10 işlem olması olası
print("SSF eşleşen yaz gözlemi:", S[S.CA.notna() & S.settle.notna()].shape[0], " basis medyan (bps):", round(1e4 * S.basis.median(), 1), " tau medyan:", S.tau.median())
rows = []
# (1) uzlaşma fiyatı neyi izliyor?
for lab, m in [("ALL", S.CA.notna()), ("trades>=200", S.CA.notna() & S.liq_ok), ("trades<200", S.CA.notna() & ~S.liq_ok)]:
    d = S[m][["dbasis", "CA", "L30", "date"]].dropna()
    b, se, n, Gd = v.ols_cl(d["dbasis"].values, d[["CA", "L30"]].values, d["date"].values)
    rows.append(dict(test="dbasis~CA", sub=lab, n=n, b_CA=b[1], t_CA=b[1] / se[1], b_L30=b[2], t_L30=b[2] / se[2]))
    # basis değişimi t->t+1 (ertesi gün 'düzelme')
    d = S[m][["dbasis1", "CA", "date"]].dropna()
    b, se, n, Gd = v.ols_cl(d["dbasis1"].values, d[["CA"]].values, d["date"].values)
    rows.append(dict(test="dbasis(t->t+1)~CA", sub=lab, n=n, b_CA=b[1], t_CA=b[1] / se[1]))
R1 = pd.DataFrame(rows); print(R1.round(3).to_string())

# (2) SSF stratejisi
S["y_ssf730"] = S["y_c730"] + S["basis1"] - S["basis"]          # F_settle_t -> F̂_{t+1,07:30}
S["theta"] = S["basis"] / S["tau"].clip(lower=1) * (S["nextday"] - S["date"]).dt.days  # 1 günlük taşıma erimesi
S["y_ssfcc"] = np.log(S["settle1"] / S["settle"]) + S["theta"]    # F_settle_t -> F_settle_{t+1}, taşıma düzeltmeli
S["y_spot_cc_same"] = S["y_cc"]
rows = []
base = S.CA.notna() & S.basis.notna() & S.basis1.notna() & S.y_c730.notna()
for thr in [0.0025, 0.005]:
    for lab, m in [("ALL", base), ("H1", base & (S.date < half)), ("H2", base & (S.date >= half)), ("trades>=200", base & S.liq_ok), ("trades<200", base & ~S.liq_ok)]:
        for y in ["y_c730", "y_ssf730", "y_cc", "y_ssfcc"]:
            dd, ntr, pnl = v.port(S, "CA", y, thr, m.values)
            mm, tt, nd = v.nw_t(dd)
            rows.append(dict(thr_bps=thr * 1e4, sub=lab, y=y, n_days=nd, n_tr=ntr, mean_bps=mm, t=tt, per_trade=pnl.mean()))
R2 = pd.DataFrame(rows); print(R2.round(2).to_string())
R1.to_csv(v.RES + "/v2_ssf_track.csv", index=False); R2.to_csv(v.RES + "/v2_ssf_bt.csv", index=False)
S[["stock", "date", "CA", "basis", "basis1", "dbasis", "trades", "y_c730", "y_ssf730", "y_ssfcc", "tau"]].to_parquet(v.RES + "/v2_ssf_panel.parquet")
