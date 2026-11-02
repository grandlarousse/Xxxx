"""Gece hareketi (15:00 UTC t-1 -> 06:00 UTC t; BIST açılışından ÖNCE bilinir) -> hisse gap_t (fiyatlanma) ve gün-içi_t (işlenebilir).
Ayrıca gündüz hareketi (06:00->15:00 UTC t) senkron. Değişkenler: n_usd, n_eur, n_bsk, n_xau, n_gc (saatlik; 2024-01 / 2024-06+).
Kontroller: hisse cc_{t-1}, XU100 cc_{t-1}; 'X' sürümü: XU100 gap_t / gün-içi_t senkron kontrol (hisseye özgü).
Çıktı: res/night.csv"""
import numpy as np, pandas as pd
import mlib as M, ll
mac = pd.read_parquet(M.RES + "/macro_daily.parquet")
xu = mac["xu100"]; xg = M.dec("XU100", "gap"); xi = M.dec("XU100", "intra")
half = pd.Timestamp("2025-06-01")
rows = []
for v in ["n_usd", "n_eur", "n_bsk", "n_xau", "n_gc"]:
    x = mac[v]; sd = x.std(); x = x.clip(-5 * sd, 5 * sd)
    for s in M.STOCKS + ["XU100", "XU030", "XBANK", "XUSIN"]:
        r = M.cc(s); g = M.dec(s, "gap"); it = M.dec(s, "intra")
        C = pd.DataFrame({"x": x, "own": r.shift(1), "m": xu.shift(1)})
        o = {"var": v, "stock": s}
        for nm, y in [("gap", g), ("intra", it), ("cc", r)]:
            q = M.ols(y, C)
            if q: o[f"{nm}_b"], o[f"{nm}_t"], o["n"] = q[0]["x"], q[1]["x"], q[2]
            q1 = M.ols(y[y.index < half], C); q2 = M.ols(y[y.index >= half], C)
            o[f"{nm}_t_h1"] = q1[1]["x"] if q1 else np.nan; o[f"{nm}_t_h2"] = q2[1]["x"] if q2 else np.nan
            o[f"{nm}_corr"] = pd.concat([y, x], axis=1).dropna().corr().iloc[0, 1]
        if s not in ("XU100",):
            q = M.ols(g, pd.DataFrame({"x": x, "mg": xg, "own": r.shift(1)})); o["gapX_t"] = q[1]["x"] if q else np.nan
            q = M.ols(it, pd.DataFrame({"x": x, "mi": xi, "own": r.shift(1)})); o["intraX_t"] = q[1]["x"] if q else np.nan
            o["intraX_b"] = q[0]["x"] if q else np.nan
        rows.append(o)
N = pd.DataFrame(rows); N.to_csv(M.RES + "/night.csv", index=False)
pd.set_option("display.width", 250)
for v in ["n_usd", "n_xau"]:
    print(v); print(N[N["var"] == v][["stock", "n", "gap_corr", "gap_t", "intra_corr", "intra_t", "intra_t_h1", "intra_t_h2", "gapX_t", "intraX_t", "cc_t"]].round(2).to_string(index=False))
