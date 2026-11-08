"""Hakem: madenci artığı ailesi (C2j, C2, C1) bağımsız yeniden kurulum + gecikme yapısı + bileşen ayrıştırma + alt dönem."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e2_etf_leadlag")
from e2_common import *
ADV = f"{S}/out/e2_etf_leadlag_adv"
d = load()
R = {t: ret_of(d, t) for t in ["GLD", "GDX", "GDXJ", "SPY"]}
SIG1 = pd.read_pickle(f"{OUT}/s1_signals.pkl")

def resid2(y, win=250, minp=60):
    X = pd.concat([R["GLD"], R["SPY"]], axis=1); X.columns = ["GLD", "SPY"]
    # bağımsız uygulama: pandas rolling cov matrisi yerine numpy lstsq (aynı fikir) ama beta yalnız t-1'e kadar
    B = roll_beta2(R[y], X, win, minp).shift(1)
    e = R[y] - B["GLD"] * R["GLD"] - B["SPY"] * R["SPY"]
    return e, B

e_j, Bj = resid2("GDXJ"); e_x, Bx = resid2("GDX")
# 1) yeniden üretim
for nm, e, k, T, h in [("C2j", e_j, 1, "GDXJ", 3), ("C2", e_x, 3, "GDX", 3), ("C1", e_x, 10, "GLD", 5)]:
    x = e.rolling(k, min_periods=k).sum().shift(1)
    key = ("GDXJ~GLD+SPY" if nm == "C2j" else "GDX~GLD+SPY", k)
    diff = (x - SIG1[key]).abs().max()
    st = split_stats(x, fwd(R[T], h), h)
    print(f"[repro] {nm}: max|x-analist|={diff:.2e} ic={st['ic']:.3f} t={st['t']:.2f} t_is={st['t_is']:.2f} t_oos={st['t_oos']:.2f} yrs={st['yrs_same_sign']}/{st['yrs']}")

# 2) gecikme yapısı: e_s ile tek günlük R_{s+j} (j=1 => sinyal anından hemen sonraki gün)
print("\n[gecikme] IC(e_s, R_{s+j}) NW t (tam / IS / OOS)")
for nm, e in [("GDXJres", e_j), ("GDXres", e_x)]:
    for T in ["GDXJ", "GDX", "GLD"]:
        out = []
        for j in range(1, 7):
            x = e.shift(j)
            a = ic(x, R[T], 5); ai = ic(x[x.index <= IS_END], R[T][R[T].index <= IS_END], 5); ao = ic(x[x.index > IS_END], R[T][R[T].index > IS_END], 5)
            out.append(f"j{j}:{a['ic']:+.3f}({a['t']:+.1f}|{ai['t']:+.1f}|{ao['t']:+.1f})")
        print(nm, "->", T, " ".join(out))

# 3) bileşen ayrıştırma (C2j): x = r_J - bG r_G - bS r_S (t-1). Her bileşen ayrı, ve çoklu rank-NW
from scipy.stats import norm
def rgz(s):
    r = s.rank(pct=True); n = s.notna().sum(); return pd.Series(norm.ppf((r * n - 0.5) / n), index=s.index)
print("\n[bilesen] C2j hedef GDXJ h3 / GLD h3")
for T in ["GDXJ", "GLD"]:
    y = fwd(R[T], 3)
    comps = {"r_GDXJ": R["GDXJ"].shift(1), "-bG*r_GLD": -(Bj["GLD"] * R["GLD"]).shift(1), "-bS*r_SPY": -(Bj["SPY"] * R["SPY"]).shift(1),
             "r_GLD": R["GLD"].shift(1), "r_SPY": R["SPY"].shift(1), "x_C2j": e_j.shift(1)}
    for cn, x in comps.items():
        st = split_stats(x, y, 3)
        print(f"  {T} <- {cn:10s} ic={st['ic']:+.3f} t={st['t']:+.2f} is={st['t_is']:+.2f} oos={st['t_oos']:+.2f}")
    X = pd.concat([rgz(comps["r_GDXJ"]).rename("J"), rgz(comps["r_GLD"]).rename("G"), rgz(comps["r_SPY"]).rename("S")], axis=1)
    yy = rgz(y)
    for nm, msk in [("full", X.index > "1900"), ("is", X.index <= IS_END), ("oos", X.index > IS_END), ("22+", X.index >= "2022-01-01")]:
        r = nw_ols(yy.reindex(X[msk].index), X[msk], lags=5); m = r["model"]
        print(f"  {T} multi {nm}: tJ={m.tvalues['J']:+.2f} tG={m.tvalues['G']:+.2f} tS={m.tvalues['S']:+.2f}")

# 4) alt dönem IC (görevdeki dört dönem) — C1/C2/C2j
print("\n[alt donem] IC (NW t)")
P4 = [("2008-01-01", "2012-12-31"), ("2013-01-01", "2017-12-31"), ("2018-01-01", "2021-12-31"), ("2022-01-01", "2026-12-31")]
for nm, e, k, T, h in [("C2j", e_j, 1, "GDXJ", 3), ("C2", e_x, 3, "GDX", 3), ("C1", e_x, 10, "GLD", 5), ("C2j->GLD", e_j, 1, "GLD", 3)]:
    x = e.rolling(k, min_periods=k).sum().shift(1); y = fwd(R[T], h)
    s = []
    for a, b in P4:
        r = sub_ic(x, y, h, a, b); s.append(f"{a[:4]}-{b[2:4]}: {r['ic']:+.3f} ({r['t']:+.2f}) n={r['n']}")
    print(nm, " | ".join(s))

# 5) GDXJ yıl yıl IC ve işaret
x = e_j.shift(1); y = fwd(R["GDXJ"], 3)
dd = pd.concat([x.rename("x"), y.rename("y")], axis=1).dropna()
print("\n[C2j yillik IC]", dd.groupby(dd.index.year).apply(lambda g: round(g.x.corr(g.y, method="spearman"), 3)).to_dict())
pd.to_pickle(dict(e_j=e_j, e_x=e_x, Bj=Bj, Bx=Bx), f"{ADV}/resid.pkl")
