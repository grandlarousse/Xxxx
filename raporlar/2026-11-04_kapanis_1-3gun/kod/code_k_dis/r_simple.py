"""Pratik (basit) kural sürümleri: beta=1 artık, tek üye; son dönem (2025-26) performansı. VİOP vadeli (2017+), maliyet 8/15 (+3 hedge)."""
import numpy as np, pandas as pd, klib as K, ll
F = K.fut_panel(); R = F; mk = F["XU030"]
betaS = K.roll_beta(R[K.STOCKS], mk, 250, 60)
def sig_simple(members, region, lag):
    r = pd.concat([ll.ret(m) for m in members], axis=1).mean(axis=1) - (ll.ret(region) if region else 0)
    return r.shift(lag)
S = {
 "REF_US basit (VLO,MPC,PSX,PBF - SPX, t-1)": (sig_simple(["VLO", "MPC", "PSX", "PBF"], "^GSPC", 1), "TUPRS"),
 "REF_US yalnız VLO - SPX (t-1)": (sig_simple(["VLO"], "^GSPC", 1), "TUPRS"),
 "FMG.AX - ASX200 (t)": (sig_simple(["FMG.AX"], "^AXJO", 0), "EREGL"),
 "FMG.AX+BHP.AX - ASX200 (t)": (sig_simple(["FMG.AX", "BHP.AX"], "^AXJO", 0), "EREGL"),
 "FMG.AX - ASX200 (t) -> KRDMD": (sig_simple(["FMG.AX"], "^AXJO", 0), "KRDMD"),
 "VİOP XAUUSD (t) -> TRALT": (F["XAUUSD"], "TRALT"),
 "VİOP XAUUSD (t) -> TRMET": (F["XAUUSD"], "TRMET"),
 "VİOP USDTRY 5g (t) -> THYAO": (K.cum(F["USDTRY"], 5, 0), "THYAO"),
}
rows = []
for nm, (x, s) in S.items():
    z = K.sdscale(x.reindex(R.index), 250, 60)
    for h in (1, 2, 3):
        for tg in ("raw", "hedged"):
            y = K.fwd(R[s], h) if tg == "raw" else K.fwd(R[s], h) - betaS[s] * K.fwd(mk, h)
            y = y[y.index >= "2017-03-06"]
            tr = K.trades_nonoverlap(z, y, h, 1.0); ex = 3 if tg == "hedged" else 0
            a = K.trade_stats(tr, 8 + ex, "2022-01-01"); b = K.trade_stats(tr, 15 + ex, "2022-01-01")
            rec = tr[tr.index >= "2025-01-01"]["gross"] * 1e4 - 8 - ex
            rows.append(dict(kural=nm, hisse=s, h=h, tgt=tg, n=a["n"], yil=round(a["per_yr"], 1), brut=a["gross"], net8=a["net"], t8=a["t_net"], net15=b["net"], t15=b["t_net"],
                             IS=a["IS_net"], IS_t=a["IS_t"], OOS=a["OOS_net"], OOS_t=a["OOS_t"], son_2025_26=rec.mean(), son_n=len(rec), yillar=a["yrs_pos"], hit=a["hit"]))
O = pd.DataFrame(rows); O.to_csv(K.RES + "/r_simple.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 45); print(O.round(1).to_string())
