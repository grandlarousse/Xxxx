"""A8b: hacim koşullu momentum backtesti (bireysel yatırımcı ilgisi vekili). Sinyal: sign(r_{t-1}) yalnız anormal TL hacmi_{t-1}
(log(v_{t-1}/ort20_{t-2..t-21})) kendi geçmiş 250g dağılımının üst %33'ündeyse (look-ahead yok: eşik geçmiş pencereden).
Hedef: cc_t (t-1 kapanış seansında gir ~ yaklaşık) ve intra_t (t açılışında gir). Maliyet 0/10/15 bps. IS 2014-2020 / OOS 2021-2026."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kc import *
HERE = os.path.dirname(os.path.abspath(__file__)); rows = []
for s in STOCKS:
    d = ll.raw(ll.T(s)).copy(); d.index = pd.DatetimeIndex(d["ldate"].values); d = d[~d.index.duplicated(keep="last")]
    v = (d["v"] * d["c"]).replace(0, np.nan); av = np.log(v / v.rolling(20).mean().shift(1))
    thr = av.rolling(250, min_periods=120).quantile(2 / 3).shift(1)
    hi = (av > thr).astype(float)
    r = R(s); dd = DEC(s)
    sig = (np.sign(r) * hi.reindex(r.index)).shift(1)  # t-1 kapanışında bilinir
    for tname, tgt in [("cc", r), ("intra", dd["intra"])]:
        for cost in [0, 10, 15]:
            res, pnl, pos = run_bt(sig, tgt, cost)
            yb = res["by_year_bps"]
            rows.append({"stock": s, "target": tname, "cost": cost, **{f"{k}_{p}": res[p].get(k, np.nan) for p in ["IS", "OOS"] for k in ["n", "mean_bps", "t", "sharpe"]},
                         "pos_years": sum(1 for x in yb.values() if x > 0), "years": len(yb)})
X = pd.DataFrame(rows); X.to_csv(os.path.join(HERE, "res_extra_volmom_bt.csv"), index=False)
print(X[X.cost.isin([0, 10])].round(2).to_string(index=False))
