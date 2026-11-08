import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e2_etf_leadlag")
from e2_common import *
d = load(); R = {t: ret_of(d, t) for t in ["GLD", "GDX", "GDXJ"]}
SIG1 = pd.read_pickle(f"{OUT}/s1_signals.pkl")
for nm, x, T, h in [("C2j", SIG1[("GDXJ~GLD+SPY", 1)], "GDXJ", 3), ("C2j->GLD", SIG1[("GDXJ~GLD+SPY", 1)], "GLD", 3), ("C2", SIG1[("GDX~GLD+SPY", 3)], "GDX", 3), ("C2_k1", SIG1[("GDX~GLD+SPY", 1)], "GDX", 3), ("C1", SIG1[("GDX~GLD+SPY", 10)], "GLD", 5)]:
    z = pd.concat([x.rename("x"), fwd(R[T], h).rename("y")], axis=1).dropna()
    out = {}
    for lab, m in [("IS", z.index <= IS_END), ("OOS", z.index > IS_END)]:
        g = z[m]; out[lab] = {["Pzt", "Sal", "Car", "Per", "Cum"][k]: round(gg.x.corr(gg.y, method="spearman"), 3) for k, gg in g.groupby(g.index.dayofweek)}
    # Çarşamba hariç tam dönem IC ve NW t
    zz = z[z.index.dayofweek != 2]; r = ic(zz.x, zz.y, max(h, 5))
    print(nm, out, f"| Carsamba haric: ic {r['ic']:+.3f} t {r['t']:+.2f}")
# C2j yalnız-uzun OOS Sharpe Çarşamba sinyalleri hariç
x = SIG1[("GDXJ~GLD+SPY", 1)]; r = R["GDXJ"][R["GDXJ"].index >= "2018-01-01"].dropna()
pos = pos_from_signal(x, 1, 0.7).clip(lower=0); p2 = pos.copy(); p2[p2.index.dayofweek == 2] = 0
print("C2j OOS L tum:", round(backtest(pos, r, 3, 10)["sharpe"], 2), " Carsamba sinyalleri kapali:", round(backtest(p2, r, 3, 10)["sharpe"], 2), " Ldm:", round(backtest(p2, r, 3, 10, demean=True)["sharpe"], 2))
