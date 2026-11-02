"""s5d: VIOP vadeli o->c: yillik, long/short, XU030 vadelisiyle hedge (gecmis 250g beta), Tokyo 06:30 donemi ayrimi."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vb, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
A = pd.read_parquet(os.path.join(vb.OUT, "viop_rows.parquet"))
A = A[(A.open > 0) & (A.close > 0) & (A.value > 0)]
A = A.sort_values("value").groupby(["und", "date"]).tail(1).set_index(["und", "date"]).sort_index()
cA, _ = vb.comp(vb.JP_AU); z = vb.zpast(cA.dropna())
X = A.loc["XU030"]; xi = np.log(X.close / X.open)
rows = []
for u in ["EREGL", "KRDMD"]:
    F = A.loc[u].copy(); fi = np.log(F.close / F.open); fi[fi.abs() > 0.105] = np.nan
    tick = 0.01 / F.open * 1e4
    df = pd.DataFrame({"fi": fi, "xi": xi.reindex(fi.index), "z": z.reindex(fi.index), "tick": tick}).dropna(subset=["fi", "z"])
    cov = (df.fi * df.xi).rolling(250, min_periods=60).mean() - df.fi.rolling(250, min_periods=60).mean() * df.xi.rolling(250, min_periods=60).mean()
    beta = (cov / df.xi.rolling(250, min_periods=60).var()).shift(1)
    df["hed"] = df.fi - beta * df.xi
    df["pos"] = np.sign(df.z).where(df.z.abs() > 1, 0)
    a = df[df.pos != 0].copy()
    a["net15"] = a.pos * a.fi - 15e-4; a["nettick"] = a.pos * a.fi - (a.tick + 4) / 1e4
    a["hed15"] = a.pos * a.hed - 17e-4  # hedge bacagi ~2 bps ek
    grp = list(a.groupby(a.index.year)) + [("2024-01..2024-11-04", a[(a.index >= "2024-01-01") & (a.index < "2024-11-05")]), ("2024-11-05+ (Tokyo 06:30)", a[a.index >= "2024-11-05"]), ("2017-2026", a)]
    for y, g in grp:
        rows.append(dict(und=u, year=y, n=len(g), gross=1e4 * (g.pos * g.fi).mean(), net15=1e4 * g.net15.mean(), t15=vb.nwt(g.net15), net_tick=1e4 * g.nettick.mean(),
                         med_tick=g.tick.median(), hedged15=1e4 * g.hed15.mean(), t_hed=vb.nwt(g.hed15.dropna()),
                         long15=1e4 * g[g.pos > 0].net15.mean(), short15=1e4 * g[g.pos < 0].net15.mean(), hit=(g.net15 > 0).mean()))
R = pd.DataFrame(rows); R.to_csv(os.path.join(vb.OUT, "res_s5d_fut_yearly.csv"), index=False)
pd.set_option("display.width", 250); print(R.round(2).to_string())
