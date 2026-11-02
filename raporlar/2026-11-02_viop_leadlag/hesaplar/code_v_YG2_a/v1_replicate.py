"""v_YG2_a / 1: iddianın bağımsız yeniden üretimi.
(a) havuz regresyonu: y_{t+1} ~ CA_t + L30_t + DAY_t, gün kümelenmiş SE (47 hisse, yaz günleri)
(b) portföy BT5: pos=-sign(CA) |CA|>eşik, giriş C_t, çıkış O_{t+1} / 07:30_{t+1} / ...; günlük eşit ağırlık; NW(5) t
(c) yarılar (orijinal tanım: h1 gün ızgarasının ortanca günü), yıllar, likit/illikit, XU030
"""
import numpy as np, pandas as pd, vcommon as v
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
P = v.load()
V47 = [s for s in P.stock.unique() if s not in ("XU030", "XU100")]
S = P[P.stock.isin(V47)].copy()
days = np.sort(P.date.unique()); half = days[len(days) // 2]
print("yarı sınırı:", pd.Timestamp(half).date())
out = []

# (a) havuz regresyonu
print("\n(a) Havuz regresyonu (yaz, 47 hisse), gün kümelenmiş")
for y in ["y_gap", "y_o730", "y_c730", "y_730c", "y_cc", "y_c830", "y_cvw", "y_cc2"]:
    d = S[[y, "CA", "L30", "DAY", "date"]].dropna()
    b, se, n, G = v.ols_cl(d[y].values, d[["CA", "L30", "DAY"]].values, d["date"].values)
    r = dict(test="pooled", y=y, n=n, days=G, b_CA=b[1], t_CA=b[1] / se[1], b_L30=b[2], t_L30=b[2] / se[2], b_DAY=b[3], t_DAY=b[3] / se[3])
    out.append(r); print({k: (round(x, 3) if isinstance(x, float) else x) for k, x in r.items()})

# yalnız CA (tek değişken)
for y in ["y_gap", "y_o730", "y_c730"]:
    d = S[[y, "CA", "date"]].dropna()
    b, se, n, G = v.ols_cl(d[y].values, d[["CA"]].values, d["date"].values)
    print("tek CA", y, round(b[1], 3), round(b[1] / se[1], 2), n)

# (b) portföy
LQ = v.liquidity(S); rank = LQ.rank(ascending=False)
liq = list(rank[rank <= 23].index); ill = list(rank[rank > 23].index)
print("\nlikit23:", liq); print("illikit24:", ill)
X = P[P.stock == "XU030"]
print("\n(b) BT5 portföy (bps/gün-portföy, NW t)")
rows = []
for thr in [0.0, 0.001, 0.0025, 0.005]:
    for y in ["y_gap", "y_c730", "y_cvw", "y_c830", "y_cc"]:
        for lab, m in [("ALL", S.date >= days[0]), ("H1", S.date < half), ("H2", S.date >= half), ("2024", S.year == 2024), ("2025", S.year == 2025), ("2026", S.year == 2026),
                       ("likit23", S.stock.isin(liq)), ("illikit24", S.stock.isin(ill))]:
            dd, ntr, pnl = v.port(S, "CA", y, thr, m.values)
            mm, tt, nd = v.nw_t(dd)
            rows.append(dict(thr_bps=thr * 1e4, y=y, sub=lab, n_days=nd, n_tr=ntr, mean_bps=mm, t=tt, per_trade_bps=pnl.mean(), hit=(dd > 0).mean()))
        dd, ntr, pnl = v.port(X, "CA", y, thr)
        mm, tt, nd = v.nw_t(dd)
        rows.append(dict(thr_bps=thr * 1e4, y=y, sub="XU030", n_days=nd, n_tr=ntr, mean_bps=mm, t=tt, per_trade_bps=pnl.mean(), hit=(dd > 0).mean()))
B = pd.DataFrame(rows)
B.to_csv(v.RES + "/v1_bt5.csv", index=False)
print(B[B.thr_bps == 25].round(2).to_string())
print(B[(B.y == "y_c730") & (B["sub"].isin(["ALL", "H1", "H2", "XU030"]))].round(2).to_string())

# XU030 regresyonu
d = X[["y_gap", "y_c730", "CA", "L30", "DAY", "date"]].dropna()
for y in ["y_gap", "y_c730"]:
    b, se, n, G = v.ols_cl(d[y].values, d[["CA", "L30", "DAY"]].values, np.arange(len(d)))
    print("XU030", y, "b_CA", round(b[1], 3), "t", round(b[1] / se[1], 2), n)
pd.DataFrame(out).to_csv(v.RES + "/v1_pooled.csv", index=False)
