"""Senkron + öncülük (değişken_{t-1} -> hisse cc/gap/intra) + ters yön (hisse_{t-1} -> değişken_t) taraması.
47 VİOP hissesi + 5 endeks x makro değişkenler. Kontroller: hisse_{t-1}, XU100_{t-1} (öncülükte), XU100_t (senkron kısmi).
Çıktı: res/scan_<tag>.csv . Kullanım: python3 04_sync_lead.py <tag> var1,var2,...  [start]"""
import sys, numpy as np, pandas as pd
import mlib as M, ll
tag = sys.argv[1]; VARS = sys.argv[2].split(","); START = pd.Timestamp(sys.argv[3] if len(sys.argv) > 3 else "2014-01-01")
mac = pd.read_parquet(M.RES + "/macro_daily.parquet")
TGT = M.STOCKS + ["XU100", "XU030", "XBANK", "XUSIN"]  # XHOLD: Yahoo günlük verisi yok (1 satır)
xu = mac["xu100"]; xu_i = M.dec("XU100", "intra"); xu_g = M.dec("XU100", "gap")
last = mac.index.max(); d3 = last - pd.DateOffset(years=3); d1 = last - pd.DateOffset(years=1)
rows = []
for v in VARS:
    x = mac[v].copy(); x = x[x.index >= START]
    # winsorize 5 sd (aşırı uç değerler: 2018/2021 kriz günleri tutulur ama kırpılır)
    sd = x.std(); x = x.clip(-5 * sd, 5 * sd)
    for s in TGT:
        r = M.cc(s); r = r[r.index >= START]
        g = M.dec(s, "gap"); it = M.dec(s, "intra")
        o = {"var": v, "stock": s}
        o["corr_full"], o["n"] = M.corr(r, x); o["corr_3y"], _ = M.corr(r, x, d3); o["corr_1y"], _ = M.corr(r, x, d1)
        if s != "XU100":
            o["pc"], _ = M.pcorr(r, x, [xu]); o["pc_is"], _ = M.pcorr(r[r.index < M.SPLIT], x, [xu]); o["pc_oos"], _ = M.pcorr(r[r.index >= M.SPLIT], x, [xu])
            o["pc_3y"], _ = M.pcorr(r[r.index >= d3], x, [xu]); o["pc_1y"], _ = M.pcorr(r[r.index >= d1], x, [xu])
            df = pd.concat([r.rename("r"), x.rename("x"), xu.rename("m")], axis=1).dropna()
            yc = df.groupby(df.index.year).apply(lambda z: M.pcorr(z["r"], z["x"], [z["m"]])[0] if len(z) > 60 else np.nan).dropna()
            ref = np.sign(o["pc"]); o["yr_same_pc"] = float((np.sign(yc) == ref).mean()) if len(yc) else np.nan; o["n_years"] = len(yc)
            q = M.ols(r, pd.DataFrame({"x": x, "m": xu})); o["beta_x"], o["t_beta_x"] = (q[0]["x"], q[1]["x"]) if q else (np.nan, np.nan)
        else:
            df = pd.concat([r.rename("r"), x.rename("x")], axis=1).dropna()
            yc = df.groupby(df.index.year).apply(lambda z: z["r"].corr(z["x"]) if len(z) > 60 else np.nan).dropna()
            o["yr_same_pc"] = float((np.sign(yc) == np.sign(o["corr_full"])).mean()); o["n_years"] = len(yc)
        q = M.ols(r, pd.DataFrame({"x": x})); o["beta"], o["t_beta"] = (q[0]["x"], q[1]["x"]) if q else (np.nan, np.nan)
        o["corr_is"], _ = M.corr(r, x, None, M.SPLIT); o["corr_oos"], _ = M.corr(r, x, M.SPLIT)
        # öncülük: değişken_{t-1}
        xl = x.shift(1); C = pd.DataFrame({"x": xl, "own": r.shift(1), "m": xu.shift(1)})
        for nm, y in [("cc", r), ("gap", g), ("intra", it)]:
            q = M.ols(y, C)
            if q:
                o[f"L_{nm}_b"], o[f"L_{nm}_t"], o[f"L_{nm}_n"] = q[0]["x"], q[1]["x"], q[2]
                qi = M.ols(y[y.index < M.SPLIT], C); qo = M.ols(y[y.index >= M.SPLIT], C)
                o[f"L_{nm}_t_is"] = qi[1]["x"] if qi else np.nan; o[f"L_{nm}_t_oos"] = qo[1]["x"] if qo else np.nan
                o[f"L_{nm}_corr"] = pd.concat([y, xl], axis=1).dropna().corr().iloc[0, 1]
        if s not in ("XU100",):  # hisseye özgü gün-içi (XU100 gün-içi senkron kontrol)
            q = M.ols(it, pd.DataFrame({"x": xl, "mi": xu_i, "own": r.shift(1)}))
            if q: o["L_intraX_b"], o["L_intraX_t"] = q[0]["x"], q[1]["x"]
            q = M.ols(g, pd.DataFrame({"x": xl, "mg": xu_g, "own": r.shift(1)}))
            if q: o["L_gapX_b"], o["L_gapX_t"] = q[0]["x"], q[1]["x"]
        # çok günlük sürüklenme: değişken_{t-1} -> cc(t+1..t+4) (t gününü atla: gap etkisini dışla)
        fwd = sum(r.shift(-k) for k in range(1, 5))
        q = M.ols(fwd, C, lags=8)
        if q: o["L_md_b"], o["L_md_t"] = q[0]["x"], q[1]["x"]
        # ters yön: hisse_{t-1} -> değişken_t (değişken_{t-1}, XU100_{t-1} kontrollü)
        if s != "XU100":
            q = M.ols(x, pd.DataFrame({"s": r.shift(1), "xl": x.shift(1), "m": xu.shift(1)}))
        else:
            q = M.ols(x, pd.DataFrame({"s": r.shift(1), "xl": x.shift(1)}))
        if q:
            o["R_b"], o["R_t"] = q[0]["s"], q[1]["s"]
            sub = lambda a, b_: M.ols(x[(x.index >= a) & (x.index < b_)], pd.DataFrame({"s": r.shift(1), "xl": x.shift(1)} | ({"m": xu.shift(1)} if s != "XU100" else {})))
            qi = sub(START, M.SPLIT); qo = sub(M.SPLIT, last + pd.Timedelta(days=1))
            o["R_t_is"] = qi[1]["s"] if qi else np.nan; o["R_t_oos"] = qo[1]["s"] if qo else np.nan
        rows.append(o)
    print(v, "ok", flush=True)
out = pd.DataFrame(rows); out.to_csv(M.RES + f"/scan_{tag}.csv", index=False); print(out.shape)
