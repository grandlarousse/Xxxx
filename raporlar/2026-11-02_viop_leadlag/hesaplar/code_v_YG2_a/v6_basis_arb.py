"""v_YG2_a / 6: ALTERNATİF GİRİŞ — spot-SSF baz yakınsaması (h1 dönemi, yaz günleri, CA gerekli).
Gözlem (v2): SSF uzlaşması (18:05-18:15 VWAP) müzayede hareketinin yalnız ~%41'ini izliyor; ertesi gün baz normale dönüyor (+0,56·CA).
İşlem: CA<0 -> spot C_t'den AL (kapanış fiyatından işlemler 18:08-18:10) + SSF uzlaşma civarı SAT;  CA>0 -> tersi (spot açığa satış gerekir).
Çıkış: (i) t+1 kapanış: spot C_{t+1} (kapanış müzayedesi) + SSF uzlaşma_{t+1} -> tamamen GÖZLENEN fiyatlar
        (ii) t+1 07:30: spot P0730 + SSF vekili P0730·exp(basis_{t+1})
Taşıma: baz her gün θ = basis/τ·Δgün kadar erir; uzun spot/kısa SSF bu θ'yı kazanır ama spotun finansmanını öder -> θ çıkarılır.
"""
import numpy as np, pandas as pd, vcommon as v
pd.set_option("display.width", 250)
Z = pd.read_parquet(v.RES + "/v2_ssf_panel.parquet")
P = v.load(); P = P[~P.stock.isin(["XU030", "XU100"])]
Z = Z.merge(P[["stock", "date", "y_cc", "C"]], on=["stock", "date"], how="left")
Z["dbasis1"] = Z.basis1 - Z.basis
days = np.sort(P.date.unique()); nxt = dict(zip(days[:-1], days[1:]))
Z["dd"] = (Z.date.map(nxt) - Z.date).dt.days
Z["theta"] = Z.basis / Z.tau.clip(lower=1) * Z.dd
half = days[len(days) // 2]
rows = []
for thr in [0.0025, 0.005]:
    for lab, m in [("ALL", Z.date >= days[0]), ("H1", Z.date < half), ("H2", Z.date >= half), ("uzun-spot ayağı (CA<0)", Z.CA < 0), ("kısa-spot ayağı (CA>0)", Z.CA > 0)]:
        d = Z[m & Z.CA.notna() & Z.dbasis1.notna() & (Z.CA.abs() > thr)].copy()
        s = -np.sign(d.CA)  # spot pozisyon yönü; SSF ters
        # kapanış->kapanış: spot log(C1/C) - SSF log(F1/F) = -(dbasis1);  pozisyon s: s*(-dbasis1); taşıma düzeltmesi: uzun spot (s=+1) θ öder
        pnl_cc = 1e4 * (s * (-d.dbasis1) - s * d.theta)
        pnl_730 = 1e4 * (s * (d.y_c730 - d.y_ssf730) - s * d.theta)
        for nm, pnl in [("C->C_{t+1} (gözlenen)", pnl_cc), ("C->07:30 (vekil)", pnl_730)]:
            daily = pnl.groupby(d.date).mean(); mm, tt, nd = v.nw_t(daily)
            r = dict(thr_bps=thr * 1e4, sub=lab, exit=nm, n_tr=len(d), n_days=nd, gross_bps=mm, t=tt)
            # maliyet: spot (komisyon 2x2 bps + çıkış yarım spread ~ yarım tik) + SSF gidiş-dönüş 8/15 + SSF tik
            tk = 1e4 * 0.01 / d.C; tsp = 1e4 * v.tick_spot(d.C) / d.C
            for c in [8, 15]:
                net = (pnl - 4 - 0.5 * tsp - c - tk).groupby(d.date).mean(); r[f"net_SSF{c}"] = net.mean(); r[f"t_net{c}"] = v.nw_t(net)[1]
            rows.append(r)
R = pd.DataFrame(rows); R.to_csv(v.RES + "/v6_basis_arb.csv", index=False); print(R.round(2).to_string())
print("ortalama θ (bps/gün):", round(1e4 * Z.theta.median(), 2), " baz medyanı (bps):", round(1e4 * Z.basis.median(), 1))
