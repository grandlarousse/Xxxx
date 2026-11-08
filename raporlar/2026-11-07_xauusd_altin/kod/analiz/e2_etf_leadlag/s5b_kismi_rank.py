"""s5b: kısmi regresyonlar sıra-normal (rank-gauss) dönüşümüyle (uç değerlere dayanıklı). Kontroller artığın bileşenleriyle doğrusal bağımlı OLMAYACAK şekilde seçildi:
  - Madenci artığı -> GLD: kontrol = GLD'nin kendi k-gün getirisi (altının kendi dönüşü) + gün içi altın. Artık GDX bilgisini taşıyor mu?
  - GDX'in eşdeğer ayrışımı: GLD fwd ~ GDX_k + GLD_k + SPY_k (ortak anlamlılık / her bileşen).
"""
from e2_common import *
from scipy.stats import norm
d = load()
R = {t: ret_of(d, t) for t in ["GLD", "GDX", "GDXJ", "SPY"]}
SIG1 = pd.read_pickle(f"{OUT}/s1_signals.pkl"); FEAT3 = pd.read_pickle(f"{OUT}/s3_signals.pkl")
def kret(t, k): return R[t].rolling(k, min_periods=k).sum().shift(1)
gi = np.log(d["xau_cut"]) - np.log(d["xau_close"].shift(1))
def rg(s):
    r = s.rank(pct=True); n = s.notna().sum(); return pd.Series(norm.ppf((r * n - 0.5) / n), index=s.index)
def partial(name, main, ctrls, T, h):
    y = rg(fwd(R[T], h)); X = pd.concat([rg(main).rename("main")] + [rg(c).rename(f"c{i}") for i, c in enumerate(ctrls)], axis=1)
    o = {}
    for nm, msk in [("full", slice(None)), ("is", X.index <= IS_END), ("oos", X.index > IS_END), ("22", X.index >= "2022-01-01")]:
        Xm = X[msk] if not isinstance(msk, slice) else X
        r = nw_ols(y.reindex(Xm.index), Xm, lags=max(h, 5)); o[nm] = r["t"]
        if nm == "full": o["coefs_t"] = {k: round(float(v), 2) for k, v in r["model"].tvalues.items() if k != "const"}
    register(AGENT, "a_kismi_rank", name, f"rank-partial {name}", h, dict(t=o["full"], t_is=o["is"], t_oos=o["oos"], n=None), note="rank-gauss kısmi NW t")
    print(f"{name:52s} h={h} main t_full={o['full']:.2f} is={o['is']:.2f} oos={o['oos']:.2f} 22+={o['22']:.2f} | {o['coefs_t']}")
for k in (5, 10):
    for h in (3, 5):
        m = SIG1[("GDX~GLD+SPY", k)]
        partial(f"R1 resid{k}->GLD | GLD{k}, gi", m, [kret("GLD", k), gi], "GLD", h)
        partial(f"R2 GDX{k}->GLD | GLD{k}, SPY{k}, gi", kret("GDX", k), [kret("GLD", k), kret("SPY", k), gi], "GLD", h)
        partial(f"R3 GLD{k}->GLD | GDX{k}, SPY{k}, gi", kret("GLD", k), [kret("GDX", k), kret("SPY", k), gi], "GLD", h)
        partial(f"R4 GLD{k} own->GLD (tek)", kret("GLD", k), [], "GLD", h)
for k in (1, 3):
    partial(f"R5 residJ{k}->GDXJ | GDXJ{k}, gi", SIG1[("GDXJ~GLD+SPY", k)], [kret("GDXJ", k), gi], "GDXJ", 3)
    partial(f"R6 resid{k}->GDX | GDX{k}, gi", SIG1[("GDX~GLD+SPY", k)], [kret("GDX", k), gi], "GDX", 3)
partial("R7 gi->GDX | GLD1,GDX1", gi, [kret("GLD", 1), kret("GDX", 1)], "GDX", 1)
partial("R8 gi->GLD | GLD1", gi, [kret("GLD", 1)], "GLD", 1)
for h in (3, 5):
    partial(f"R9 PLATIN_d5->GDX | GLD5,GDX5,SPY5,gi", FEAT3[("PLATIN", "d5")], [kret("GLD", 5), kret("GDX", 5), kret("SPY", 5), gi], "GDX", h)
    partial(f"R10 PLATIN_d5->GDX | resid5, GLD5", FEAT3[("PLATIN", "d5")], [SIG1[("GDX~GLD+SPY", 5)], kret("GLD", 5)], "GDX", h)
