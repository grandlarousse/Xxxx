"""03: İddianın birebir yeniden üretimi (kendi kodum) + yıllık kırılım + maliyet duyarlılığı."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_S2_a")
from vs import *
pd.set_option("display.width", 250)
df = pd.read_parquet(OUT + "/02_daily.parquet")
q = df[(df.index >= "2014-01-01")].copy()
q = q[q.D.abs() < 0.15]
q["U"] = q.D - q.gap1
PER = [("ALL", "2014-01-01", "2026-12-31"), ("IS", "2014-01-01", "2020-12-31"), ("OOS", "2021-01-01", "2026-12-31")]
print("=== Regresyonlar (NW t, 5 gecikme) ===")
rows = []
for lab, s, e in PER:
    z = q[(q.index >= s) & (q.index <= e)]
    for spec, xs in [("intra1~D", ["D"]), ("intra1~D+gap1", ["D", "gap1"]), ("gap1~D", ["D"]), ("cc1~D", ["D"]), ("intra1~U", ["U"])]:
        y = spec.split("~")[0]
        m, n = nw(z[y], z[xs])
        rows.append(dict(per=lab, spec=spec, b=round(m.params[xs[0]], 3), t=round(m.tvalues[xs[0]], 2),
                         b2=round(m.params[xs[1]], 3) if len(xs) > 1 else np.nan, t2=round(m.tvalues[xs[1]], 2) if len(xs) > 1 else np.nan, n=n))
A = pd.DataFrame(rows); print(A.to_string(index=False)); A.to_csv(OUT + "/03_reg.csv", index=False)
print("\n=== Backtest (kendi motorum), maliyet 8 bps ===")
rows = []
for nm, sig in [("D", q.D), ("U=D-gap1", q.U)]:
    for thr in [0, 0.0025, 0.005, 0.0075, 0.01, 0.015]:
        for lab, s, e in PER:
            r = bt(sig, q.intra1, 8, thr, s, e); rows.append(dict(sig=nm, thr_bps=thr * 1e4, per=lab, **r))
B = pd.DataFrame(rows)
print(B[["sig", "thr_bps", "per", "n", "mean_bps", "t", "hit", "sharpe", "long_frac"]].round(2).to_string(index=False))
B.to_csv(OUT + "/03_bt.csv", index=False)
print("\n=== |U|>50 bps ve |D|>50: yıllara göre net bps/işlem (8 bps) ve n ===")
for nm, sig in [("U", q.U), ("D", q.D)]:
    yy = []
    for y in range(2014, 2027):
        r = bt(sig, q.intra1, 8, 0.005, f"{y}-01-01", f"{y}-12-31"); yy.append((y, r.get("n"), round(r.get("mean_bps", np.nan), 1), round(r.get("t", np.nan), 2)))
    print(nm, yy)
print("\n=== Maliyet duyarlılığı |U|>50 bps (OOS / IS) ===")
for c in [0, 2, 4, 8, 10, 12, 15, 20]:
    ro = bt(q.U, q.intra1, c, 0.005, "2021-01-01"); ri = bt(q.U, q.intra1, c, 0.005, "2014-01-01", "2020-12-31")
    rd = bt(q.D, q.intra1, c, 0.005, "2021-01-01")
    print(f"maliyet {c:>2} bps: U OOS {ro['mean_bps']:6.1f} bps Sharpe {ro['sharpe']:5.2f} | U IS {ri['mean_bps']:6.1f} Sh {ri['sharpe']:5.2f} | D OOS {rd['mean_bps']:6.1f} Sh {rd['sharpe']:5.2f}")
