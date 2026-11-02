import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_E3_b")
"""08: Son dönem (2026) ve rejim kırılımı; enerji sinyalleri yarışı (alt dönemler)."""
import vb, numpy as np, pandas as pd
F = pd.read_parquet(vb.RES + "/F.parquet"); s = F["A_USREF"]
for tgt in ["y_raw", "y_h"]:
    pnl, pos = vb.bt(s, F[tgt], 1.0); a = pos != 0
    p = pnl[a & (pnl.index >= "2025-07-01")]
    q = p.groupby(p.index.to_period("Q")).agg(["mean", "count"]); q["mean"] *= 1e4
    print(tgt, "çeyreklik |z|>1 brüt bps (2025-07+):", q.round(1).T.to_string())
    for a0, b0, lab in [("2025-03-19", "2025-04-30", "Mart 2025 şoku"), ("2026-08-01", "2026-11-01", "Ağu-Eki 2026 (fon krizi)"), ("2018-08-01", "2018-10-31", "2018 kur krizi"), ("2021-12-01", "2022-01-31", "Ara 2021"), ("2023-06-01", "2023-07-31", "Haz 2023")]:
        pp = pnl[a & (pnl.index >= a0) & (pnl.index < b0)]
        print(f"   {lab}: n {len(pp)}, brüt {1e4*pp.mean():.1f} bps")
    # rolling 250 işlem günlük ortalama
# Yarış: hangi enerji sinyali? alt dönemlerde tek değişkenli NW t, y_h
cands = ["A_USREF", "A_OUT", "A_VLO", "A_CRAK", "A_XLE", "A_XOP", "A_XOM", "A_CVX", "A_COP", "A_SHEL", "A_BZ=F", "A_CL=F", "A_HO=F", "A_RB=F", "A_ES=F", "A_SPY", "A_EEM", "A_TUR", "FX_TRY"]
PER = [("ALL", "2014", "2027"), ("IS", "2014", "2021"), ("OOS", "2021", "2027"), ("14-17", "2014", "2018"), ("18-20", "2018", "2021"), ("21-23", "2021", "2024"), ("24-26", "2024", "2027")]
rows = []
for c in cands:
    r = {"sig": c}
    for pk, a0, b0 in PER:
        m = (F.index >= a0) & (F.index < b0)
        _, t, _ = vb.nw(F.y_h[m], F[c][m].rename("x")); r[pk] = t["x"]
    rows.append(r)
print("\nTek değişkenli NW t, hedef y_h (TUPRS-XU100 gün-içi):"); print(pd.DataFrame(rows).set_index("sig").round(2).to_string())
# Rafineri-özgü kısım: USREF'in XLE'ye göre artığı
m = F.index >= "2014"
G = F[m].copy(); b = np.polyfit(G[["A_XLE", "A_USREF"]].dropna().A_XLE, G[["A_XLE", "A_USREF"]].dropna().A_USREF, 1)
G["ref_x"] = G.A_USREF - (b[0] * G.A_XLE + b[1])
rows = []
for pk, a0, b0 in PER:
    mm = (G.index >= a0) & (G.index < b0)
    p, t, n = vb.nw(G.y_h[mm], G[["ref_x", "A_XLE"]][mm]); rows.append(dict(per=pk, t_ref_minus_xle=t["ref_x"], t_xle=t["A_XLE"]))
print("\nUSREF'in XLE'den arındırılmış kısmı + XLE birlikte (y_h):"); print(pd.DataFrame(rows).set_index("per").round(2).T.to_string())
