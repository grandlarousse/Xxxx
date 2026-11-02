"""GÖREV 5: GÜN-İÇİ MOMENTUM (Gao, Han, Li, Zhou 2018, JFE): ilk yarım saat getirisi -> son yarım saat getirisi.
BIST uyarlaması (h1, 2023-12..2026-10, ~720 gün):
  r_first = log(P0730 / C_{t-1}) (önceki kapanış -> 10:30 TSİ; gece gap'i dahil, Gao tanımı) = gap + r1 (O->07:30)
  r_12    = log(P1430 / P1330) (sondan ikinci saat)
  r_last  = log(C / P1430) = son 30 dk sürekli + kapanış müzayedesi (yıl boyu)
  r_last_c= log(P1500 / P1430) yalnız sürekli işlem (yaz günleri), CA = kapanış müzayedesi (yaz).
Regresyon: r_last = a + b1 r_first (+ b2 r_12), HAC(5). IS = ilk yarı, OOS = ikinci yarı. Hisse başına + havuzlanmış (gün kümelenmiş).
Koşullu: |r_first| tercilleri (yüksek oynaklık günleri; Gao: etki yüksek oynaklıkta güçlü).
Backtest: 14:30'da sign(r_first) pozisyonu, kapanışta (veya 15:00'te, yaz) çık; maliyet 0/2/4/8/15 bps.
Çıktı: res/a5_stock.csv, res/a5_pooled.csv, res/a5_bt.csv
"""
import numpy as np, pandas as pd, c_common as c
ll = c.ll; TG = c.VIOP
D = c.h1_days(); days = D.index; half = days[len(days) // 2]
rows = []; pool = []; bt = []
for s in ["XU030", "XU100", "XBANK", "XUSIN"] + TG:
    H = c.h1_panel(s); dd = ll.decomp(s).reindex(days)
    X = pd.DataFrame(index=days)
    X["gap"] = dd["gap"]; X["r1"] = H["r1"]; X["r_first"] = X["gap"] + X["r1"]
    X["r_mid"] = np.log(H["P1330"] / H["P0730"]); X["r_12"] = np.log(H["P1430"] / H["P1330"])
    X["r_last"] = H["r9"]; X["r_last_c"] = H["r9a"]; X["CA"] = H["ca"]
    X["stock"] = s; X["date"] = X.index
    if s in TG: pool.append(X)
    for y in ["r_last", "r_last_c", "CA"]:
        for xs in [["r_first"], ["gap", "r1"], ["r_first", "r_12"]]:
            for per, m in [("all", X.index >= days[0]), ("is", X.index < half), ("oos", X.index >= half)]:
                df = X[m][[y] + xs].dropna()
                if len(df) < 80: continue
                import statsmodels.api as sm
                mod = sm.OLS(df[y].values, sm.add_constant(df[xs].values)).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
                o = dict(stock=s, y=y, spec="+".join(xs), period=per, n=len(df), r2=mod.rsquared)
                for i, x in enumerate(xs): o[f"b_{x}"] = mod.params[1 + i]; o[f"t_{x}"] = mod.tvalues[1 + i]
                rows.append(o)
    # backtest
    for exit_, y in [("close", X["r_last"]), ("1500", X["r_last_c"])]:
        for sig in ["r_first", "r1", "r_first&r_12"]:
            if sig == "r_first&r_12":
                sg = np.sign(X["r_first"]).where(np.sign(X["r_first"]) == np.sign(X["r_12"]), 0.0)
            else: sg = np.sign(X[sig])
            pos = sg.where(y.notna()).dropna(); yy = y.reindex(pos.index)
            for per, m in [("all", pos.index >= days[0]), ("is", pos.index < half), ("oos", pos.index >= half)]:
                p = pos[m]; g = (p * yy[m])[p != 0]
                if len(g) < 30: continue
                mm, t, _ = ll.nw_t(g.reset_index(drop=True), None, 5)
                o = dict(stock=s, exit=exit_, signal=sig, period=per, n=len(g), gross_bps=1e4 * mm, t=t, hit=float((g > 0).mean()))
                for cst in [2, 4, 8, 15]: o[f"net{cst}"] = 1e4 * mm - cst
                bt.append(o)
ST = pd.DataFrame(rows)
for (y, sp, per), g in ST.groupby(["y", "spec", "period"]):
    k = "t_" + sp.split("+")[0]
    m = g["stock"].isin(TG)
    rej, padj = ll.fdr(ll.t_to_p(g.loc[m, k].values)); ST.loc[g.index[m.values], "fdr"] = rej
ST.to_csv(c.RES + "/a5_stock.csv", index=False)
pd.DataFrame(bt).to_csv(c.RES + "/a5_bt.csv", index=False)
PO = pd.concat(pool)
# kesitsel göreli: gün ortalamasından arındırılmış
for v in ["r_first", "r_last", "r_12", "gap", "r1", "r_last_c"]:
    PO[v + "_x"] = PO[v] - PO.groupby("date")[v].transform("mean")
rows = []
for y, xs in [("r_last", ["r_first"]), ("r_last", ["gap", "r1"]), ("r_last", ["r_first", "r_12"]), ("r_last_c", ["r_first"]), ("r_last_x", ["r_first_x"]), ("r_last_x", ["gap_x", "r1_x"]), ("r_last_c_x", ["r_first_x"])]:
    for per, m in [("all", PO.index >= days[0]), ("is", PO.index < half), ("oos", PO.index >= half)]:
        df = PO[m][[y, "date"] + xs].dropna()
        b, se, cov, r2, n = c.ols_cl(df[y].values, df[xs].values, df["date"].values)
        o = dict(y=y, spec="+".join(xs), period=per, n=n, r2=r2)
        for i, x in enumerate(xs): o[f"b_{x}"] = b[1 + i]; o[f"t_{x}"] = b[1 + i] / se[1 + i]
        rows.append(o)
# koşullu (XU030): |r_first| tercilleri
X = c.h1_panel("XU030"); dd = ll.decomp("XU030").reindex(days)
rf = (dd["gap"] + X["r1"]); rl = X["r9"]
q = rf.abs().rank(pct=True)
for lab, m in [("low", q <= 1 / 3), ("mid", (q > 1 / 3) & (q <= 2 / 3)), ("high", q > 2 / 3)]:
    df = pd.concat([rl.rename("y"), rf.rename("x")], axis=1)[m].dropna()
    b, t, n = ll.nw_t(df["y"], df["x"])
    rows.append(dict(y="XU030 r_last", spec=f"r_first tercile {lab}", period="all", n=n, b_r_first=b, t_r_first=t))
pd.DataFrame(rows).to_csv(c.RES + "/a5_pooled.csv", index=False)
print(pd.DataFrame(rows).round(4).to_string())
print(ST[(ST.stock.isin(["XU030", "XU100", "XBANK", "XUSIN"]))].round(4).to_string())
