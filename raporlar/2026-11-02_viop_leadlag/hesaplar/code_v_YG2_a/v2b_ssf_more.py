"""v_YG2_a / 2b: SSF 'close' (son işlem) ile aynı test; hisse bazında eğim; SSF ciro tercillerine göre; spot uzun-yalnız ayağı."""
import numpy as np, pandas as pd, vcommon as v
pd.set_option("display.width", 250)
S = pd.read_parquet(v.RES + "/v2_ssf_panel.parquet")
P = v.load(); P = P[~P.stock.isin(["XU030", "XU100"])]
F = pd.read_parquet(v.SCR + "/data/viop_panel.parquet", columns=["date", "code", "root", "segment", "expiry", "close", "settle", "trades"])
F = F[(F.segment == "SSF") & (F.date >= "2023-11-01")].copy(); F["date"] = pd.to_datetime(F.date).dt.normalize()
# aynı front sözleşme kodu için close
S2 = pd.read_parquet(v.RES + "/v2_ssf_panel.parquet")
G = pd.read_parquet(v.RES + "/panel.parquet")[["stock", "date", "C", "P1500"]]
# front sözleşme kodunu yeniden kur (v2 ile aynı kural)
days = np.sort(G.date.unique()); nxt = dict(zip(days[:-1], days[1:])); prv = dict(zip(days[1:], days[:-1]))
F["nextday"] = F.date.map(nxt); F["expiry"] = pd.to_datetime(F.expiry)
fr = F[F.expiry > F.nextday].sort_values(["root", "date", "expiry"]).groupby(["root", "date"]).head(1)[["root", "date", "code", "close", "settle", "trades"]]
fr["prevday"] = fr.date.map(prv)
f0 = F[["code", "date", "close", "settle"]].rename(columns={"date": "prevday", "close": "close0", "settle": "settle0"})
fr = fr.merge(f0, on=["code", "prevday"], how="left").rename(columns={"root": "stock"})
X = P[["stock", "date", "CA", "L30", "C", "y_c730"]].merge(fr, on=["stock", "date"], how="left")
X["C0"] = X.groupby("stock")["C"].shift(1)
X["db_close"] = np.log(X.close / X.C) - np.log(X.close0 / X.C0)
X["db_settle"] = np.log(X.settle / X.C) - np.log(X.settle0 / X.C0)
for c in ["db_close", "db_settle"]: X.loc[X[c].abs() > 0.1, c] = np.nan
out = []
for c in ["db_close", "db_settle"]:
    d = X[["CA", c, "date"]].dropna()
    b, se, n, g = v.ols_cl(d[c].values, d[["CA"]].values, d["date"].values)
    out.append(dict(y=c, stock="POOLED", b=b[1], t=b[1] / se[1], n=n))
    for s, ds in X.groupby("stock"):
        d = ds[["CA", c]].dropna()
        if len(d) < 100: continue
        b, se, n, g = v.ols_cl(d[c].values, d[["CA"]].values, np.arange(len(d)))
        out.append(dict(y=c, stock=s, b=b[1], t=b[1] / se[1], n=n, ssf_trades_med=ds.trades.median()))
O = pd.DataFrame(out)
print(O[O.stock == "POOLED"].round(3))
W = O[O.y == "db_settle"].set_index("stock")
print("hisse bazında db_settle~CA eğimi: medyan", round(W.b.median(), 3), " min", round(W.b.min(), 3), " max", round(W.b.max(), 3), " eğim>-0,2 olan:", list(W[W.b > -0.2].index))
W2 = W.drop("POOLED").sort_values("ssf_trades_med")
W2["tercile"] = pd.qcut(W2.ssf_trades_med.rank(), 3, labels=["dusuk", "orta", "yuksek"])
print(W2.groupby("tercile")[["b", "ssf_trades_med"]].median().round(3))
print(W2.sort_values("b").round(3).to_string())
O.to_csv(v.RES + "/v2b_ssf_slopes.csv", index=False)
