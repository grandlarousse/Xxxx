"""Hedge'li (TUPRS vadeli - XU030 vadeli) asimetrik maliyet: pay vadelisi 8/15 bps + endeks vadelisi 3 bps gidiş-dönüş."""
import numpy as np, pandas as pd
import vlib as V
X = pd.read_parquet(V.RES + "/panel_E3.parquet")
out = []
for c_stk in (0, 8, 15):
    for lab, tgt, c_idx in [("tek bacak TUPRS", X.y, 0), ("TUPRS-XU030", X.y_h30, 3)]:
        df, pos = V.positions(X.US, tgt)
        pnl = pos * df.y - (c_stk + (c_idx if c_stk > 0 else 0)) / 1e4 * pos.abs()
        for per, m in [("IS", df.index < "2021"), ("OOS", df.index >= "2021")]:
            s = V.bt_stats(pnl[m], pos[m]); out.append({"strateji": lab, "maliyet": f"{c_stk}+{c_idx if c_stk>0 else 0}", "dönem": per, **{k: s[k] for k in ["n", "mean_bps", "t", "sharpe", "maxdd_pct"]}})
T = pd.DataFrame(out); print(T.round(2).to_string(index=False)); T.to_csv(V.RES + "/hedge_cost.csv", index=False)
# net yıllık (8 bps tek bacak)
df, pos = V.positions(X.US, X.y); pnl = pos * df.y - 8e-4 * pos.abs(); a = pos != 0
yr = (1e4 * pnl[a]).groupby(pnl[a].index.year).agg(["mean", "size"]).round(1)
pnl15 = pos * df.y - 15e-4 * pos.abs(); yr["net15"] = (1e4 * pnl15[a]).groupby(pnl15[a].index.year).mean().round(1)
yr.columns = ["net8_bps", "n", "net15_bps"]; print(yr.T.to_string())
print("net8 pozitif yıl:", int((yr.net8_bps > 0).sum()), "/", len(yr), "| net15 pozitif yıl:", int((yr.net15_bps > 0).sum()))
yr.to_csv(V.RES + "/by_year_net.csv")
