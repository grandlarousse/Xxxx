import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_E3_b")
"""02: Ortak faktör kontrolleri. Tüm kontroller BIST t açılışından ÖNCE bilinir (gap_t açılışta bilinir), aksi belirtilmedikçe."""
import vb, numpy as np, pandas as pd
F = pd.read_parquet(vb.RES + "/F.parquet"); G = F[F.index >= "2014-01-01"].copy()
K = {
 "K0 yok": [],
 "K1 ES+BZ": ["A_ES=F", "A_BZ=F"],
 "K2 +EEM,USDTRY,TUR,VIX": ["A_ES=F", "A_BZ=F", "A_EEM", "FX_TRY", "A_TUR", "A_^VIX"],
 "K3 +XLE": ["A_ES=F", "A_BZ=F", "A_EEM", "FX_TRY", "A_TUR", "A_^VIX", "A_XLE"],
 "K4 +CL,HO,RB,NG": ["A_ES=F", "A_BZ=F", "A_EEM", "FX_TRY", "A_TUR", "A_^VIX", "A_XLE", "A_CL=F", "A_HO=F", "A_RB=F", "A_NG=F"],
 "K5 +BIST gecikmeleri+gap_t": ["A_ES=F", "A_BZ=F", "A_EEM", "FX_TRY", "A_TUR", "A_^VIX", "A_XLE", "A_CL=F", "A_HO=F", "A_RB=F", "A_NG=F",
                                 "tu_cc_l1", "xu_cc_l1", "xkmya_cc_l1", "xusin_cc_l1", "aygaz_cc_l1", "petkm_cc_l1", "tu_gap", "xu_gap", "tu_intra_l1", "y_h_l1"],
 "K6 K5+XOM,CVX,COP,SHEL": ["A_ES=F", "A_BZ=F", "A_EEM", "FX_TRY", "A_TUR", "A_^VIX", "A_XLE", "A_CL=F", "A_HO=F", "A_RB=F", "A_NG=F",
                                 "tu_cc_l1", "xu_cc_l1", "xkmya_cc_l1", "xusin_cc_l1", "aygaz_cc_l1", "petkm_cc_l1", "tu_gap", "xu_gap", "tu_intra_l1", "y_h_l1", "A_XOM", "A_CVX", "A_COP", "A_SHEL"],
}
rows = []
for y in ["y_h", "y_raw", "xu_intra", "xusin_intra"]:
    for sg in ["A_USREF", "A_OUT"]:
        for kn, ks in K.items():
            for pk, m in [("ALL", G.index >= "1900"), ("IS", G.index < vb.SPLIT), ("OOS", G.index >= vb.SPLIT), ("14-17", (G.index >= "2014") & (G.index < "2018")), ("18-20", (G.index >= "2018") & (G.index < "2021")), ("21-23", (G.index >= "2021") & (G.index < "2024")), ("24-26", G.index >= "2024")]:
                g = G[m]; X = g[[sg] + ks]
                if y == "y_raw" and kn != "K0 yok": X = pd.concat([X, g[["xu_intra"]]], axis=1) if kn.startswith("K5") or kn.startswith("K6") else X
                p, t, n = vb.nw(g[y], X)
                rows.append(dict(y=y, sig=sg, ctrl=kn, per=pk, b_bps_per_1pct=100 * p[sg], t=t[sg], n=n))
R = pd.DataFrame(rows); R.to_csv(vb.RES + "/02_controls.csv", index=False)
pd.set_option("display.width", 250)
for y in ["y_h", "y_raw", "xu_intra", "xusin_intra"]:
    print("\n=== hedef", y, "(t değerleri; y_raw K5/K6'da XU100 gün-içi eşzamanlı kontrol eklendi)")
    print(R[R.y == y].pivot_table(index=["sig", "ctrl"], columns="per", values="t").round(2)[["ALL", "IS", "OOS", "14-17", "18-20", "21-23", "24-26"]].to_string())
print("\nbeta (bps TUPRS-XU100 gün-içi / %1 sepet) y_h A_USREF:")
print(R[(R.y == "y_h") & (R.sig == "A_USREF")].pivot_table(index="ctrl", columns="per", values="b_bps_per_1pct").round(1)[["ALL", "IS", "OOS"]].to_string())
# korelasyonlar
print("\ncorr(A_USREF, kontroller):"); print(G[["A_USREF", "A_XLE", "A_BZ=F", "A_ES=F", "A_HO=F", "A_CRAK", "A_OUT", "tu_gap", "tu_cc_l1"]].corr()["A_USREF"].round(2).to_string())
