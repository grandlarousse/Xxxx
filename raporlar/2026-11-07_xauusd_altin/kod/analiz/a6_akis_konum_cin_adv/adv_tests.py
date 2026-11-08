"""Hakem testleri: alt dönem, komşu parametreler, drift, bacaklar, maliyet, dairesel kaydırma permütasyonu, erken dönem, çoklu test."""
import sys, warnings
warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
sys.path.insert(0, f"{S}/code"); sys.path.insert(0, f"{S}/out/a6_akis_konum_cin_adv")
from lib_altin import load_viop, load_spot, fwd, nw_ols, ic, split_stats, backtest, IS_END, bh_fdr
from adv_cn import composite, resid, STK
D = load_viop(); SP = load_spot(); R = D["v_ret"]
F = pd.read_csv(f"{S}/out/a6_akis_konum_cin_adv/adv_cn_features.csv", index_col=0, parse_dates=True).reindex(D.index)
FS = pd.read_csv(f"{S}/out/a6_akis_konum_cin_adv/adv_cn_features_spot.csv", index_col=0, parse_dates=True).reindex(SP.index)
PER = {"2017-19": ("2017-01-01", "2019-12-31"), "2020-21": ("2020-01-01", "2021-12-31"), "2022-23": ("2022-01-01", "2023-12-31"), "2024-26": ("2024-01-01", "2026-12-31")}
EXT = ((D.index >= "2020-03-01") & (D.index <= "2020-04-30")) | ((D.index >= "2026-01-01") & (D.index <= "2026-02-28"))
ROLL = (D.v_code != D.v_code.shift(1)); ROLLN = (ROLL | ROLL.shift(1, fill_value=False) | ROLL.shift(-1, fill_value=False)).values

def icp(x, y, h, m=None):
    if m is not None: x = x[m]; y = y[m]
    r = ic(x, y, max(h, 5)); return r["ic"], r["t"], r["n"]

def sub_ic(x, h, y=None):
    y = D[f"fwd{h}"] if y is None else y
    out = {}
    for k, (a, b) in PER.items():
        m = (D.index >= a) & (D.index <= b); c, t, n = icp(x, y, h, m); out[k] = f"{c:+.3f}({t:+.2f})"
    return out

def sharpe_sub(pos, h, cost=5, demean=False):
    out = {}
    for k, (a, b) in list(PER.items()) + [("IS", ("2017-01-01", "2021-12-31")), ("OOS", ("2022-01-01", "2026-12-31")), ("full", ("2010", "2027"))]:
        m = (R.index >= a) & (R.index <= b)
        bt = backtest(pos[m], R[m], h, cost, demean=demean)
        out[k] = round(bt["sharpe"], 2) if bt else np.nan
    return out

def block(title): print("\n" + "=" * 8, title, "=" * 8)

x = F["comp"]
block("1) Bileşik: IC ufuk taraması (VİOP fwd)")
for h in (1, 2, 3, 4, 5, 6, 7, 8, 10):
    y = fwd(R, h); st = split_stats(x, y, h)
    print(f"h={h:2d} ic={st['ic']:+.3f} t={st['t']:+.2f} IS t={st['t_is']:+.2f} OOS t={st['t_oos']:+.2f} yrs {st['yrs_same_sign']}/{st['yrs']}", sub_ic(x, h, y))

block("2) Tek hisseler ve 2899 hariç bileşik h=3/5")
for nm, s in [("600547", F["600547.SS"]), ("1818", F["1818.HK"]), ("2899", F["2899.HK"]), ("ex2899", F[["600547.SS", "1818.HK"]].mean(axis=1).where(F[["600547.SS", "1818.HK"]].notna().sum(axis=1) >= 1)),
              ("HK2", F[["1818.HK", "2899.HK"]].mean(axis=1))]:
    for h in (3, 5):
        st = split_stats(s, D[f"fwd{h}"], h)
        print(f"{nm:7s} h={h} ic={st['ic']:+.3f} t={st['t']:+.2f} IS={st['t_is']:+.2f} OOS={st['t_oos']:+.2f}", sub_ic(s, h))

block("3) Kural: sign(bileşik), h=5 — alt dönem Sharpe (net 5 / 10 bps, demeaned), bacaklar")
pos = np.sign(x).fillna(0)
for h in (3, 5):
    print(f"h={h} net5 ", sharpe_sub(pos, h, 5)); print(f"h={h} net10", sharpe_sub(pos, h, 10)); print(f"h={h} dm5  ", sharpe_sub(pos, h, 5, True))
    print(f"h={h} long ", sharpe_sub(pos.clip(lower=0), h, 5), "\n    long dm", sharpe_sub(pos.clip(lower=0), h, 5, True))
    print(f"h={h} short", sharpe_sub(pos.clip(upper=0), h, 5), "\n    shortdm", sharpe_sub(pos.clip(upper=0), h, 5, True))
bh = pd.Series(1.0, index=R.index)
print("buy&hold", sharpe_sub(bh, 1, 0))
print("pozisyon uzun oranı (aktif):", round((pos > 0).sum() / (pos != 0).sum(), 3), " OOS:", round((pos[D.index > IS_END] > 0).sum() / (pos[D.index > IS_END] != 0).sum(), 3))

block("4) Komşu parametreler: beta penceresi, min hisse, eşik")
for win in (60, 120, 250, 500, 750):
    c, _ = composite(D.index, win=win, minobs=int(min(150, win * 0.6)))
    st = split_stats(c, D["fwd5"], 5); st3 = split_stats(c, D["fwd3"], 3)
    pb = backtest(np.sign(c).fillna(0)[D.index > IS_END], R[D.index > IS_END], 5)
    pbi = backtest(np.sign(c).fillna(0)[D.index <= IS_END], R[D.index <= IS_END], 5)
    print(f"win={win:3d} h5 t={st['t']:+.2f} IS={st['t_is']:+.2f} OOS={st['t_oos']:+.2f} | h3 t={st3['t']:+.2f} | rule h5 Sharpe IS={pbi['sharpe']:+.2f} OOS={pb['sharpe']:+.2f}")
for mn in (1, 2, 3):
    c, _ = composite(D.index, minn=mn); st = split_stats(c, D["fwd5"], 5); print(f"min hisse={mn} h5 t={st['t']:+.2f} IS={st['t_is']:+.2f} OOS={st['t_oos']:+.2f} n={st['n']}")
c, _ = composite(D.index, use_mkt=False); st = split_stats(c, D["fwd5"], 5); print(f"yalnız altın betası h5 t={st['t']:+.2f} IS={st['t_is']:+.2f} OOS={st['t_oos']:+.2f}")
# ham getiri ortalaması (artık değil)
sd = x.rolling(250, min_periods=120).std().shift(1)
for k in (0.0, 0.25, 0.5, 1.0, 1.5):
    p = pd.Series(np.where(x > k * sd, 1, np.where(x < -k * sd, -1, 0)), index=D.index).where(x.notna(), 0)
    print(f"eşik |x|>{k}σ: Sharpe h5", sharpe_sub(p, 5), "aktif oran", round((p != 0).mean(), 2))

block("5) Uç dönem / roll / 2026 hariç; uç değer kırpma")
y5 = D["fwd5"]
for lab, m in [("tam", np.ones(len(D), bool)), ("uç hariç", ~EXT), ("roll±1 hariç", ~ROLLN), ("ikisi hariç", ~EXT & ~ROLLN), ("2026 hariç", D.index < "2026-01-01"),
               ("2025-26 hariç", D.index < "2025-01-01")]:
    c_, t_, n_ = icp(x, y5, 5, m); ci, ti, _ = icp(x, y5, 5, m & (D.index <= IS_END)); co, to, _ = icp(x, y5, 5, m & (D.index > IS_END))
    print(f"{lab:14s} h5 ic={c_:+.3f} t={t_:+.2f} | IS t={ti:+.2f} | OOS ic={co:+.3f} t={to:+.2f}")
# Pearson (uç değerlere duyarlı) vs Spearman
print("Pearson h5:", round(ic(x, y5, 5, method="pearson")["t"], 2), " Spearman:", round(ic(x, y5, 5)["t"], 2))
# 2022-2023 / 2024-2025 ayrı
for a, b in [("2022", "2022"), ("2023", "2023"), ("2024", "2024"), ("2025", "2025"), ("2026", "2026")]:
    m = (D.index >= f"{a}-01-01") & (D.index <= f"{b}-12-31"); c_, t_, n_ = icp(x, y5, 5, m); print(f"  {a}: ic={c_:+.3f} t={t_:+.2f} n={n_}")

block("6) Dairesel kaydırma permütasyonu (otokorelasyonu korur): tam ve OOS t dağılımı")
rng = np.random.default_rng(7)
def t_of(xx, yy):
    d = pd.concat([xx.rename("x"), yy.rename("y")], axis=1).dropna().rank()
    return np.corrcoef(d.x, d.y)[0, 1] * np.sqrt(len(d))
xv = x.copy(); obs = t_of(xv, y5); oo = t_of(xv[D.index > IS_END], y5[D.index > IS_END])
xs = x.values; n = len(xs); null = []; nullo = []
oosm = D.index > IS_END
for _ in range(2000):
    k = rng.integers(60, n - 60)
    xr = pd.Series(np.roll(xs, k), index=D.index)
    null.append(t_of(xr, y5)); nullo.append(t_of(xr[oosm], y5[oosm]))
null = np.array(null); nullo = np.array(nullo)
print(f"tam: gözlenen z~{obs:.2f}, perm p(|z|>=obs)={np.mean(np.abs(null) >= abs(obs)):.4f}; OOS: z~{oo:.2f}, p={np.mean(np.abs(nullo) >= abs(oo)):.4f}")

block("7) Spot panel: erken dönem 2010-2016 ve tam 2010-2026 (sıfır hacim günleri NaN vs tutulmuş)")
for col in ("comp", "comp_keep0", "600547.SS", "600547.SS_keep0", "1818.HK", "2899.HK"):
    for h in (3, 5):
        y = SP[f"sfwd{h}"]
        for lab, (a, b) in [("2010-13", ("2010", "2013-12-31")), ("2014-16", ("2014", "2016-12-31")), ("2010-16", ("2010", "2016-12-31")), ("2017-21", ("2017", "2021-12-31")), ("2022-26", ("2022", "2026-12-31")), ("2010-26", ("2010", "2026-12-31"))]:
            m = (SP.index >= a) & (SP.index <= b); c_, t_, n_ = icp(FS[col], y, h, m)
            print(f"{col:16s} h={h} {lab}: ic={c_:+.3f} t={t_:+.2f} n={n_}", end=" | ")
        print()

block("8) Kontroller: spot r1, r5, 07->15, VİOP r_{t-1}, 07->07 altın; ayrıca GDX (ABD altın madencileri t-1) ")
s_r1 = np.log(D.xau_p15 / D.xau_p15_prev); s_r5 = np.log(D.xau_p15 / D.xau_p15.shift(5)); s_715 = np.log(D.xau_p15 / D.xau_p07)
g77 = np.log(D.xau_p07 / D.xau_p07.shift(1)); gdx = np.log(D["y_GDX"]).diff() if "y_GDX" in D else None
C = pd.concat([s_r1.rename("r1"), s_r5.rename("r5"), s_715.rename("r715"), R.shift(1).rename("v1"), g77.rename("g77")] + ([gdx.rename("gdx")] if gdx is not None else []), axis=1)
xz = (x - x.mean()) / x.std()
for h in (3, 5):
    y = D[f"fwd{h}"]
    for lab, m in [("tam", slice(None)), ("IS", D.index <= IS_END), ("OOS", D.index > IS_END)]:
        Xd = pd.concat([xz.rename("x"), C], axis=1)
        r_ = nw_ols(y[m], Xd[m], lags=max(h, 5)); print(f"h={h} {lab}: b={r_['b']*1e4:.1f}bps/σ t={r_['t']:+.2f} n={r_['n']}")
print("corr(bileşik, 07->15 aynı gün):", round(x.corr(s_715), 3), " corr(bileşik, g77):", round(x.corr(g77), 3), " corr(bileşik, gdx t-1 kapanış):", round(x.corr(gdx), 3) if gdx is not None else "")
