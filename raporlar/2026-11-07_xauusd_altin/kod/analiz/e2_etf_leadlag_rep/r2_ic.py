"""r2: alti iddianin IC / NW t (lag=max(h,5)) / IS<=2017 / OOS 2018+ / 2022+ / yil isareti, alt donemler, placebo, uc donem haric, kismi (rank-gauss) testler."""
import sys, json
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e2_etf_leadlag_rep")
from rep_lib import *
from scipy.stats import norm
Z = pd.read_pickle(f"{OUT}/r1_signals.pkl"); SIG, R, LP, cal = Z["SIG"], Z["R"], Z["LP"], Z["cal"]

def Y(und, h): return fwd_ret(LP[und], h)

# PL=F 2008-2009 bayat (ceyreklik) veri: bayat gunleri NaN yapan surum
pl = yahoo("PL_F"); ipos = pl.index.searchsorted(cal, side="left") - 1
pl_gap = pd.Series((cal - pl.index[ipos]).days, index=cal)
stale = pl_gap.rolling(6, min_periods=1).max() > 5
PL_clean = SIG["PL_d5"].where(~stale)

CLAIMS = {
    "E2-C2j": dict(x=SIG[("GDXJres", 1, 60)], und="GDXJ", h=3, sign=+1),
    "E2-C2": dict(x=SIG[("GDXres", 3, 60)], und="GDX", h=3, sign=+1),
    "E2-C1": dict(x=SIG[("GDXres", 10, 60)], und="GLD", h=5, sign=+1),
    "E2-C5": dict(x=SIG["asia1"], und="GLD", h=3, sign=+1),
    "E2-C4": dict(x=SIG["PL_d5"], und="GDX", h=3, sign=-1),
    "E2-C3": dict(x=SIG["gi"], und="GDX", h=1, sign=-1),
}
VARIANTS = {
    "E2-C2j_minp250": dict(x=SIG[("GDXJres", 1, 250)], und="GDXJ", h=3),
    "E2-C2_minp250": dict(x=SIG[("GDXres", 3, 250)], und="GDX", h=3),
    "E2-C1_minp250": dict(x=SIG[("GDXres", 10, 250)], und="GLD", h=5),
    "E2-C5_onGDX": dict(x=SIG["asia1"], und="GDX", h=3),
    "E2-C4_PL_bayat_haric": dict(x=PL_clean, und="GDX", h=3),
    "E2-C4_2010+": dict(x=SIG["PL_d5"][SIG["PL_d5"].index >= "2010-01-01"], und="GDX", h=3),
    "E2-C2j_onGLD": dict(x=SIG[("GDXJres", 1, 60)], und="GLD", h=3),
}
EXT = [("2008-09-01", "2008-12-31"), ("2013-04-01", "2013-06-30"), ("2020-02-20", "2020-04-30"), ("2026-01-01", "2026-02-28")]
rows = []; byyear = {}
for cid, c in {**CLAIMS, **VARIANTS}.items():
    y = Y(c["und"], c["h"]); x = c["x"]
    st = stats_block(x, y, c["h"])
    ex = pd.Series(False, index=x.index)
    for a, b in EXT: ex |= (x.index >= a) & (x.index <= b)
    _, t_ex, _ = ic_t(x.where(~ex), y, max(c["h"], 5))
    sub = {}
    for a, b in [("2008-01-01", "2012-12-31"), ("2013-01-01", "2017-12-31"), ("2018-01-01", "2021-12-31"), ("2022-01-01", "2024-12-31"), ("2025-01-01", "2026-12-31"), ("2018-01-01", "2024-12-31")]:
        i_, t_, n_ = sub_ic(x, y, c["h"], a, b); sub[f"ic_{a[:4]}_{b[:4]}"] = (round(i_, 3) if np.isfinite(i_) else None, round(t_, 2) if np.isfinite(t_) else None)
    plac = {s: round(ic_t(x.shift(s), y, max(c["h"], 5))[0], 3) for s in (-2, -1, 0, 1, 2, 3)}
    byyear[cid] = st.pop("by_year").round(3)
    rows.append(dict(id=cid, und=c["und"], h=c["h"], **{k: (round(v, 3) if isinstance(v, float) else v) for k, v in st.items()}, t_ex_extremes=round(t_ex, 2), **sub, placebo=plac))
T = pd.DataFrame(rows)
T.to_csv(f"{OUT}/r2_ic.csv", index=False)
pd.DataFrame(byyear).to_csv(f"{OUT}/r2_ic_yillik.csv")
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
print(T[["id", "und", "h", "ic", "t", "t_is", "t_oos", "t_22", "yrs_same", "yrs", "n", "n_is", "n_oos", "t_ex_extremes"]].to_string())
print(T[["id"] + [c for c in T.columns if c.startswith("ic_20")]].to_string())
for r in rows: print(r["id"], r["placebo"])
print(pd.DataFrame(byyear).to_string())

# ---------- kismi testler (rank-gauss, NW OLS) ----------
def rg(s):
    s = s.copy(); r = s.rank(pct=True); n = s.notna().sum(); return pd.Series(norm.ppf((r * n - 0.5) / n), index=s.index)
def nw_multi(y, Xdf, L):
    d = pd.concat([y.rename("y"), Xdf], axis=1).dropna()
    yv = d["y"].values; Xv = np.column_stack([np.ones(len(d)), d.iloc[:, 1:].values])
    b = np.linalg.lstsq(Xv, yv, rcond=None)[0]; u = yv - Xv @ b
    g = Xv * u[:, None]; Sm = g.T @ g
    for l in range(1, L + 1):
        w = 1 - l / (L + 1); G = g[l:].T @ g[:-l]; Sm += w * (G + G.T)
    XtXi = np.linalg.inv(Xv.T @ Xv); V = XtXi @ Sm @ XtXi
    return dict(zip(d.columns[1:], (b / np.sqrt(np.diag(V)))[1:])), len(d)
def kret(tk, k): return R[tk].rolling(k, min_periods=k).sum().shift(1)
def partial(name, main, ctrls, und, h):
    y = rg(Y(und, h)); X = pd.concat([rg(main).rename("main")] + [rg(c).rename(f"c{i}") for i, c in enumerate(ctrls)], axis=1)
    o = {}
    for nm, m in [("full", slice(None)), ("is", X.index <= IS_END), ("oos", X.index > IS_END), ("22", X.index >= "2022-01-01")]:
        Xm = X if isinstance(m, slice) else X[m]
        tt, n = nw_multi(y.reindex(Xm.index), Xm, max(h, 5)); o[nm] = round(tt["main"], 2)
        if nm == "full": o["others"] = {k: round(v, 2) for k, v in tt.items() if k != "main"}
    print(f"{name:45s} h={h}", o); return o
PT = {}
gi = SIG["gi"]
PT["C1 resid10->GLD5 | GLD10, gi"] = partial("C1 resid10->GLD5 | GLD10, gi", SIG[("GDXres", 10, 60)], [kret("GLD", 10), gi], "GLD", 5)
PT["C1 GLD10 own -> GLD5"] = partial("C1 GLD10 own -> GLD5", kret("GLD", 10), [], "GLD", 5)
PT["C1 GLD5 own -> GLD5"] = partial("C1 GLD5 own -> GLD5", kret("GLD", 5), [], "GLD", 5)
PT["C5 asia5 | US resid5 -> GLD3"] = partial("C5 asia5 | US resid5 -> GLD3", SIG["asia5"], [SIG[("GDXres", 5, 60)]], "GLD", 3)
PT["C5 US resid5 | asia5 -> GLD3"] = partial("C5 US resid5 | asia5 -> GLD3", SIG[("GDXres", 5, 60)], [SIG["asia5"]], "GLD", 3)
PT["C4 PL5 | GLD5,GDX5,SPY5,gi"] = partial("C4 PL5 | GLD5,GDX5,SPY5,gi", SIG["PL_d5"], [kret("GLD", 5), kret("GDX", 5), kret("SPY", 5), gi], "GDX", 3)
PT["C4 PL5 | resid5,GLD5"] = partial("C4 PL5 | resid5,GLD5", SIG["PL_d5"], [SIG[("GDXres", 5, 60)], kret("GLD", 5)], "GDX", 3)
PT["C4clean PL5 | GLD5,GDX5,SPY5,gi"] = partial("C4clean PL5 | GLD5,GDX5,SPY5,gi", PL_clean, [kret("GLD", 5), kret("GDX", 5), kret("SPY", 5), gi], "GDX", 3)
PT["C3 gi | GLD1,GDX1 -> GDX1"] = partial("C3 gi | GLD1,GDX1 -> GDX1", gi, [kret("GLD", 1), kret("GDX", 1)], "GDX", 1)
PT["C2j residJ1 | GDXJ1, gi"] = partial("C2j residJ1 | GDXJ1, gi", SIG[("GDXJres", 1, 60)], [kret("GDXJ", 1), gi], "GDXJ", 3)

# ---------- ayristirma: GDXJ ileri artigi vs ileri GLD ----------
X2 = pd.concat([R["GLD"], R["SPY"]], axis=1); X2.columns = ["GLD", "SPY"]
dec = {}
for und, key in (("GDXJ", ("GDXJres", 1, 60)), ("GDX", ("GDXres", 3, 60))):
    B = roll_ols(R[und], X2, 250, 120)       # t dahil (t kapanisinda bilinir)
    fres = Y(und, 3) - B["GLD"] * Y("GLD", 3) - B["SPY"] * Y("SPY", 3)
    s1 = stats_block(SIG[key], fres, 3); s2 = stats_block(SIG[key], Y("GLD", 3), 3)
    dec[und] = dict(fwd_resid=dict(ic=round(s1["ic"], 3), t=round(s1["t"], 2), t_is=round(s1["t_is"], 2), t_oos=round(s1["t_oos"], 2), t_22=round(s1["t_22"], 2)),
                    fwd_GLD=dict(ic=round(s2["ic"], 3), t=round(s2["t"], 2), t_is=round(s2["t_is"], 2), t_oos=round(s2["t_oos"], 2), t_22=round(s2["t_22"], 2)))
print(json.dumps(dec, indent=1))
json.dump(dict(partial=PT, decomposition=dec), open(f"{OUT}/r2_kismi_ayristirma.json", "w"), indent=1, default=str)
