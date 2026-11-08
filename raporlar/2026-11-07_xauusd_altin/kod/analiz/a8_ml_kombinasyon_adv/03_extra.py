"""Hakem ek kontroller: (a) gün-gün gecikme IC'si (hangi gün taşıyor), (b) demeaned uzun/kısa bacaklar, (c) tepe günler,
(d) nom2/curve sinyalinin altının kendi momentumu ile örtüşmesi (kısmi regresyon), (e) çoklu test (Bonferroni/BH; ajan ve global kayıt),
(f) spot panel 2010-16 seg_last1h alt pencereler."""
import sys, glob, numpy as np, pandas as pd
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/code")
from lib_altin import load_viop, load_spot, ic, backtest, fwd, nw_ols, bh_fdr
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
OUT = f"{S}/out/a8_ml_kombinasyon_adv"
d = load_viop(); s = load_spot(); ret = d.v_ret


def asof(x):
    return x.reindex(x.index.union(d.index)).ffill(limit=2).reindex(d.index)


sig = {
    "-nom2_d5 h1": (asof(-s.ust_nom2.diff(5)), 1),
    "+curve_d5 h1": (asof((s.ust_nom10 - s.ust_nom2).diff(5)), 1),
    "+seg_last1h h5": (asof(np.log(s.xau_p15 / s.xau_p14)), 5),
}
# (a) gün-gün: x_t ile r_{t+k}
print("== gecikme IC t (x_t vs v_ret_{t+k}), 2017-03.. / OOS")
for nm, (x, h) in sig.items():
    out = {}
    for k in range(1, 8):
        y = ret.shift(-k)
        out[k] = (round(ic(x, y, 5)["t"], 2), round(ic(x.loc["2022":], y.loc["2022":], 5)["t"], 2))
    print(nm, out)
# (b) demeaned bacaklar (tam 2017-03.. ve OOS)
print("== demeaned uzun / kısa Sharpe")
for nm, (x, h) in sig.items():
    pos = np.sign(x)
    for pn, a in (("FULL", "2017-03"), ("OOS", "2022")):
        r = ret.loc[a:].dropna(); rd = r - r.mean()
        L = backtest(pos.clip(lower=0).reindex(r.index).fillna(0), rd, h); Sx = backtest(pos.clip(upper=0).reindex(r.index).fillna(0), rd, h)
        print(nm, pn, "uzun_dm", round(L["sharpe"], 2), "kısa_dm", round(Sx["sharpe"], 2), "uzun oranı", round(float((pos.loc[a:] > 0).mean()), 2))
# (c) tepe günler: en büyük 10/20 |pnl| günü atılınca OOS Sharpe
print("== tepe gün duyarlılığı (OOS, 5 bps)")
for nm, (x, h) in sig.items():
    r = ret.loc["2022":].dropna(); b = backtest(np.sign(x).reindex(r.index).fillna(0), r, h); p = b["pnl"]
    res = {}
    for k in (5, 10, 20):
        top = p.sort_values(ascending=False).index[:k]; q = p.drop(top); res[f"-top{k}"] = round(q.mean() / q.std() * np.sqrt(252), 2)
    print(nm, "OOS Sharpe", round(b["sharpe"], 2), res, "yıllık", p.groupby(p.index.year).apply(lambda v: round(v.mean() / v.std() * np.sqrt(252), 2)).to_dict())
# (d) altın momentumu ile kısmi regresyon: fwd_h ~ sinyal + px_r5 + px_r20 (spot 15:00)
lp = np.log(asof(s.xau_p15))
ctrl = pd.concat([(lp - lp.shift(5)).rename("r5"), (lp - lp.shift(20)).rename("r20"), (lp - lp.shift(1)).rename("r1")], axis=1)
print("== kısmi regresyon (z-skorlu; NW lag max(h,5)), 2017-03..")
for nm, (x, h) in sig.items():
    y = fwd(ret, h).loc["2017-03":]
    X = pd.concat([((x - x.mean()) / x.std()).rename("sig"), ctrl], axis=1).loc["2017-03":]
    r0 = nw_ols(y, X[["sig"]], lags=max(h, 5)); r1 = nw_ols(y, X, lags=max(h, 5))
    print(nm, "t yalnız", round(r0["t"], 2), "t kontrollü", round(r1["t"], 2), "corr(sig,r5)", round(X.sig.corr(X.r5), 2), "corr(sig,r20)", round(X.sig.corr(X.r20), 2))
# (e) çoklu test
reg = pd.read_csv(f"{S}/out/registry/a8_ml_kombinasyon.csv")
allr = pd.concat([pd.read_csv(f) for f in glob.glob(f"{S}/out/registry/*.csv")], ignore_index=True)
for nm, R in (("a8", reg), ("global", allr)):
    R = R[np.isfinite(R.t)].copy()
    R["p2"] = 2 * (1 - __import__("scipy").stats.norm.cdf(R.t.abs()))
    R["q"] = bh_fdr(R.p2.values)
    n = len(R)
    print(f"== {nm}: n={n}, Bonferroni |t| eşiği (α=0.05) ≈ {__import__('scipy').stats.norm.ppf(1 - 0.025 / n):.2f}; min q={R.q.min():.3f}; q<0.10 sayısı={int((R.q < 0.10).sum())}")
    for tid in ("uni_rt_nom2_d5_h1", "uni_seg_last1h_h5", "uni_rt_curve_2s10s_d5_h1"):
        m = R[R.test_id == tid] if "test_id" in R else R.iloc[0:0]
        if len(m): print("   ", tid, "t", round(m.t.iloc[0], 2), "p", round(m.p2.iloc[0], 4), "q", round(m.q.iloc[0], 3), "Bonf p", min(1, round(m.p2.iloc[0] * n, 3)))
    print("    |t|>=2:", int((R.t.abs() >= 2).sum()), "beklenen", round(0.0455 * n, 1), " |t|>=3:", int((R.t.abs() >= 3).sum()), "beklenen", round(0.0027 * n, 1))
# global kayıtta benzer öngörücüler (diğer ajanlar)
mask = allr.predictor.astype(str).str.contains("nom2|2s10s|curve|last1h|14_15|p14|son saat", case=False, regex=True)
print(allr.loc[mask & (allr.agent != "a8_ml_kombinasyon"), ["agent", "test_id", "predictor", "h", "ic", "t", "t_is", "t_oos"]].round(3).to_string(index=False)[:6000])
# (f) spot seg_last1h alt pencereler (sfwd5)
x = np.log(s.xau_p15 / s.xau_p14)
for a, b in (("2010", "2011"), ("2012", "2013"), ("2014", "2015"), ("2016", "2016"), ("2017", "2019"), ("2020", "2021"), ("2022", "2023"), ("2024", "2026")):
    st = ic(x.loc[a:b], s.sfwd5.loc[a:b], 5); print("spot seg_last1h h5", a, b, "IC", round(st["ic"], 3), "t", round(st["t"], 2))
