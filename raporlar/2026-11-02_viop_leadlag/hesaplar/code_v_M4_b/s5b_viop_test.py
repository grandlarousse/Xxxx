"""s5b: GERCEK VIOP pay vadelisi uzerinde dogrudan test (2017-03..2026-10).
fut_intra = log(KAPANIS/ACILIS) en yuksek hacimli kontrat; ayrica log(UZLASMA/ACILIS). Likidite + tik maliyeti."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vb, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
A = pd.read_parquet(os.path.join(vb.OUT, "viop_rows.parquet"))
A = A[(A.open > 0) & (A.close > 0) & (A.value > 0)]
A = A.sort_values("value").groupby(["und", "date"]).tail(1).set_index(["und", "date"]).sort_index()
cA, _ = vb.comp(vb.JP_AU)
rows, liq, cmp_rows = [], [], []
for u in ["EREGL", "KRDMD", "BRSAN", "XU030"]:
    F = A.loc[u].copy()
    F["fi"] = np.log(F.close / F.open); F["fs"] = np.log(F.settle / F.open)
    F.loc[F.fi.abs() > 0.105, ["fi", "fs"]] = np.nan
    F["tick_bps"] = (0.01 if u != "XU030" else 0.025) / F.open * 1e4
    spot = vb.bist(u + ".IS")
    F["spot_intra"] = spot.intra.reindex(F.index)
    for y, g in F.groupby(F.index.year):
        liq.append(dict(und=u, year=y, days=len(g), med_value_mTL=g.value.median() / 1e6, med_trades=g.ntr.median(), med_tick_bps=g.tick_bps.median(),
                        corr_fut_spot_intra=g[["fi", "spot_intra"]].corr().iloc[0, 1], fut_minus_spot_intra_bps=1e4 * (g.fi - g.spot_intra).mean()))
    for minntr in (0, 50, 200):
        G = F[F.ntr >= minntr]
        for tgt in ("fi", "fs", "spot_intra"):
            y_ = G[tgt]
            for per, a, e in [("ALL", "2017-01-01", "2027-01-01"), ("2017-20", "2017-01-01", "2021-01-01"), ("2021-23", "2021-01-01", "2024-01-01"), ("2024-26", "2024-01-01", "2027-01-01")]:
                m = (y_.index >= a) & (y_.index < e)
                r, t, n = vb.corr_t(cA, y_[m])
                # backtest: re-z gecmis pencere TUM BIST gunlerinde (hedef bagimsiz) -> sonra hedef gunlerine
                c2 = cA.dropna(); z = vb.zpast(c2).reindex(y_[m].index)
                pos = np.sign(z).where(z.abs() > 1, 0).fillna(0)
                gross = pos * y_[m]
                act = pos != 0
                tick = G.tick_bps[m]
                out = dict(und=u, min_trades=minntr, target=tgt, period=per, corr=r, corr_t=t, n=n, n_tr=int(act.sum()),
                           gross_bps=1e4 * gross[act].mean(), net15_bps=1e4 * gross[act].mean() - 15, t15=vb.nwt(gross[act] - 15e-4),
                           net_tick_bps=(1e4 * gross[act] - (tick[act] + 4)).mean(), t_tick=vb.nwt(gross[act] - (tick[act] + 4) / 1e4),
                           med_tick=tick[act].median())
                rows.append(out)
R = pd.DataFrame(rows); L = pd.DataFrame(liq)
R.to_csv(os.path.join(vb.OUT, "res_s5_viop_bt.csv"), index=False); L.to_csv(os.path.join(vb.OUT, "res_s5_viop_liq.csv"), index=False)
pd.set_option("display.width", 250)
print(L.round(2).to_string())
print(R[R.min_trades == 50].round(2).to_string())
print(R[(R.min_trades != 50) & (R.period == "ALL")].round(2).to_string())
