"""Hakem: C5 bağımsızlığı (Asya artığı ABD artığını mı aktarıyor), hisse bazında C5, C1 kaplama null'u, C4 kümesi/kısmi, C2j'nin C4/SPY ile örtüşmesi."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e2_etf_leadlag")
from e2_common import *
from scipy.stats import norm
d = load()
R = {t: ret_of(d, t) for t in ["GLD", "GDX", "GDXJ", "SPY"]}
SIG1 = pd.read_pickle(f"{OUT}/s1_signals.pkl"); SIGA = pd.read_pickle(f"{OUT}/s7_signals.pkl"); F3 = pd.read_pickle(f"{OUT}/s3_signals.pkl")
def rgz(s):
    r = s.rank(pct=True); n = s.notna().sum(); return pd.Series(norm.ppf((r * n - 0.5) / n), index=s.index)
def part(y, cols, h, lab):
    X = pd.concat([rgz(c).rename(n) for n, c in cols.items()], axis=1); yy = rgz(y)
    out = []
    for nm, msk in [("full", X.index > "1900"), ("is", X.index <= IS_END), ("oos", X.index > IS_END), ("22+", X.index >= "2022-01-01")]:
        m = nw_ols(yy.reindex(X[msk].index), X[msk], lags=max(h, 5))["model"]
        out.append(f"{nm}: " + " ".join(f"{k}={m.tvalues[k]:+.2f}" for k in cols))
    print(f"  {lab}: " + " | ".join(out))
# --- C5: Asya artığı (gün t) ile ABD artığı (t-1) korelasyonu
a1 = SIGA[1]; us = SIG1[("GDX~GLD+SPY", 1)]; usj = SIG1[("GDXJ~GLD+SPY", 1)]
dd = pd.concat([a1, us, usj], axis=1, keys=["asya", "abd_GDX_e(t-1)", "abd_GDXJ_e(t-1)"]).dropna()
print("[C5] Spearman korelasyon:", dd.corr("spearman").round(3).iloc[0].to_dict(), "n", len(dd))
for nm, msk in [("IS", dd.index <= IS_END), ("OOS", dd.index > IS_END)]:
    print("   ", nm, dd[msk].corr("spearman").round(3).iloc[0].to_dict())
part(fwd(R["GLD"], 3), {"asya": a1, "usGDX": us, "usGDXJ": usj}, 3, "GLD h3 ~ asya1 + ABD e(t-1)")
part(fwd(R["GLD"], 3), {"asya": a1, "usGDX3": SIG1[("GDX~GLD+SPY", 3)]}, 3, "GLD h3 ~ asya1 + ABD GDX k3")
# hisse bazında C5 (s7'yi yeniden kur)
x07 = np.log(d["xau_07utc"])
def local_ret(col):
    s = np.log(d[col].astype(float)); a = d[col + "_avail"]; fresh = a.ne(a.shift(1)); r = s.diff(); r[~fresh] = np.nan; return r, fresh
for mc, ic_ in [("y_2899_HK", "y__HSI"), ("y_1818_HK", "y__HSI"), ("y_600547_SS", "y_000001_SS")]:
    rm, fr = local_ret(mc); ri, _ = local_ret(ic_)
    last = x07.where(fr).ffill().shift(1); rg = (x07 - last).where(fr)
    X = pd.concat([rg.rename("g"), ri.rename("m")], axis=1); B = roll_beta2(rm, X, 250, 120).shift(1)
    e = rm - B["g"] * rg - B["m"] * ri
    for T in ["GLD", "GDX"]:
        st = split_stats(e, fwd(R[T], 3), 3); s22 = sub_ic(e, fwd(R[T], 3), 3, start="2022-01-01")
        print(f"[C5 hisse] {mc} -> {T} h3: ic {st['ic']:+.3f} t {st['t']:+.2f} is {st['t_is']:+.2f} oos {st['t_oos']:+.2f} 22+ {s22['t']:+.2f} yrs {st['yrs_same_sign']}/{st['yrs']}")
# copper exposure of Zijin residual: corr with copper d1 (t-1 US close) 
cu = np.log(d["y_HG_F"]).diff()
print("[C5] Zijin artığı ile bakır (t-1 kapanış, d1) korelasyonu:")
rm, fr = local_ret("y_2899_HK")
# --- C1 kaplama: null ve maliyet
x = SIG1[("GDX~GLD+SPY", 10)]; p = pos_from_signal(x, +1, 0.8); ov = pd.Series(1.0, index=p.index); ov[p < 0] = 0.0
rng = np.random.default_rng(3)
for a_, b_ in [("2018-01-01", None), ("2022-01-01", None), ("2018-01-01", "2021-12-31"), ("2008-01-01", "2017-12-31")]:
    r = R["GLD"][(R["GLD"].index >= a_) & ((R["GLD"].index <= b_) if b_ else True)].dropna()
    o = ov.reindex(r.index).fillna(1)
    act = {c: backtest(o, r, 5, c)["sharpe"] for c in (10, 20)}
    bh = backtest(pd.Series(1.0, index=r.index), r, 1, 0)["sharpe"]
    nul = np.array([backtest(pd.Series(np.roll(o.values, s), index=o.index), r, 5, 10)["sharpe"] for s in rng.integers(120, len(o) - 120, 300)])
    print(f"[C1 kaplama] {a_[:4]}-{(b_ or '2026')[:4]}: Sharpe 10bp {act[10]:.2f} 20bp {act[20]:.2f} | B&H {bh:.2f} | null med {np.median(nul):.2f} 95% {np.quantile(nul,.95):.2f} p={np.mean(nul>=act[10]):.3f}")
# --- C4: GDXJ hedefi, PPLT ETF ile, d3/d10 pencereleri, ve C2j ile örtüşme
pl = np.log(d["y_PL_F"].astype(float)); pp = np.log(d["y_PPLT"].astype(float)) if "y_PPLT" in d else None
for nm, xx in [("PL_F d3", pl.diff(3)), ("PL_F d5", pl.diff(5)), ("PL_F d10", pl.diff(10)), ("PPLT d5", pp.diff(5) if pp is not None else None)]:
    if xx is None: continue
    for T in ["GDX", "GDXJ", "GLD"]:
        st = split_stats(xx, fwd(R[T], 3), 3)
        print(f"[C4] {nm} -> {T} h3: ic {st['ic']:+.3f} t {st['t']:+.2f} is {st['t_is']:+.2f} oos {st['t_oos']:+.2f} yrs {st['yrs_same_sign']}/{st['yrs']}")
c4 = -F3[("PLATIN", "d5")]
dd = pd.concat([c4, SIG1[("GDX~GLD+SPY", 3)], SIG1[("GDXJ~GLD+SPY", 1)], -F3[("SPY", "d5")], -np.log(d["y_GLD"]).diff(5)], axis=1, keys=["-PL5", "C2", "C2j", "-SPY5", "-GLD5"]).dropna()
print("[C4] korelasyon:", dd.corr("spearman").round(2).to_dict())
part(fwd(R["GDXJ"], 3), {"C2j": SIG1[("GDXJ~GLD+SPY", 1)], "negPL5": c4, "negSPY5": -F3[("SPY", "d5")]}, 3, "GDXJ h3 ~ C2j + -PL5 + -SPY5")
part(fwd(R["GDX"], 3), {"C2": SIG1[("GDX~GLD+SPY", 3)], "negPL5": c4}, 3, "GDX h3 ~ C2 + -PL5")
# C4 yıllık IC
xx = pl.diff(5); y = fwd(R["GDX"], 3); z = pd.concat([xx.rename("x"), y.rename("y")], axis=1).dropna()
print("[C4 yillik IC]", z.groupby(z.index.year).apply(lambda g: round(g.x.corr(g.y, method='spearman'), 3)).to_dict())
# Platin veri: Yahoo vadeli roll sıçramaları — |d1|>6% günler
d1 = pl.diff(); print("[C4] PL=F |d1|>6% gün sayısı:", int((d1.abs() > 0.06).sum()), d1[d1.abs() > 0.06].round(3).to_dict())
