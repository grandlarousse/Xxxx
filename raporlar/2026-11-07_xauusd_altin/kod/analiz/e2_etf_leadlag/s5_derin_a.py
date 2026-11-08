"""s5: aile a ve c adaylarında derin inceleme (kayda geçer): yıllık IC, kısmi regresyon (kontroller), beta penceresi, uç dönem dışlama, placebo.
Kontroller (hepsi gün t'de bilinen): GLD/GDX'in kendi k-günlük geçmiş getirisi (t-1'de biter), SPY k-gün, gün-içi altın [t-1 16:00 -> t 15:00 ET].
"""
from e2_common import *
d = load()
R = {t: ret_of(d, t) for t in ["GLD", "GDX", "GDXJ", "SLV", "SIL", "SPY"]}
SIG1 = pd.read_pickle(f"{OUT}/s1_signals.pkl"); FEAT3 = pd.read_pickle(f"{OUT}/s3_signals.pkl")
def kret(t, k): return R[t].rolling(k, min_periods=k).sum().shift(1)
gi = np.log(d["xau_cut"]) - np.log(d["xau_close"].shift(1))
pd.set_option("display.width", 250)
out = []
# --- (1) yıllık IC
for key, T, h in [(("GDX~GLD+SPY", 10), "GLD", 5), (("GDX~GLD+SPY", 5), "GLD", 5), (("GDX~GLD+SPY", 10), "GLD", 3), (("GDXJ~GLD+SPY", 10), "GLD", 5), (("GDXJ~GLD+SPY", 1), "GDXJ", 3), (("GDX~GLD+SPY", 3), "GDX", 3), (("GDX~GLD", 10), "GLD", 5)]:
    x = SIG1[key]; st = split_stats(x, fwd(R[T], h), h)
    print(key, T, h, "t", round(st["t"], 2), "yıllık:", {k: round(v, 3) for k, v in st["by_year"].items()})
for nm, T, h in [(("PLATIN", "d5"), "GDX", 3), (("PLATIN", "d5"), "GDX", 5)]:
    st = split_stats(FEAT3[nm], fwd(R[T], h), h); print(nm, T, h, {k: round(v, 3) for k, v in st["by_year"].items()})
st = split_stats(gi, fwd(R["GDX"], 1), 1); print("gi->GDX h1", {k: round(v, 3) for k, v in st["by_year"].items()})
# --- (2) kısmi regresyon (z-ölçekli, NW lag=max(h,5)); kayda: her kontrol setinde ana değişkenin t'si
def z(s): return (s - s.mean()) / s.std()
def partial(name, main, ctrls, T, h):
    y = fwd(R[T], h); X = pd.concat([z(main).rename("main")] + [z(c).rename(f"c{i}") for i, c in enumerate(ctrls)], axis=1)
    o = {}
    for nm, msk in [("full", slice(None)), ("is", X.index <= IS_END), ("oos", X.index > IS_END)]:
        Xm = X[msk] if not isinstance(msk, slice) else X
        r = nw_ols(y.reindex(Xm.index) * 100, Xm, lags=max(h, 5)); o[nm] = r["t"]
        if nm == "full":
            m = r["model"]; o["coefs_t"] = {k: round(float(v), 2) for k, v in m.tvalues.items()}
    row = register(AGENT, "a_kismi", name, f"partial {name}", h, dict(t=o["full"], t_is=o["is"], t_oos=o["oos"], n=None), note="NW kısmi t, kontroller: " + ",".join(str(i) for i in range(len(ctrls))))
    print(f"{name:55s} h={h} t_full={o['full']:.2f} t_is={o['is']:.2f} t_oos={o['oos']:.2f}  {o['coefs_t']}")
    return o
mr10 = SIG1[("GDX~GLD+SPY", 10)]; mr5 = SIG1[("GDX~GLD+SPY", 5)]; mrj1 = SIG1[("GDXJ~GLD+SPY", 1)]; mr3 = SIG1[("GDX~GLD+SPY", 3)]
for h in (3, 5):
    partial(f"P1 mresid10->GLD | GLD10,GDX10,SPY10,gi h{h}", mr10, [kret("GLD", 10), kret("GDX", 10), kret("SPY", 10), gi], "GLD", h)
    partial(f"P2 mresid5->GLD | GLD5,GDX5,SPY5,gi h{h}", mr5, [kret("GLD", 5), kret("GDX", 5), kret("SPY", 5), gi], "GLD", h)
    partial(f"P3 mresid3->GDX | GDX3,GLD3,SPY3,gi h{h}", mr3, [kret("GDX", 3), kret("GLD", 3), kret("SPY", 3), gi], "GDX", h)
    partial(f"P4 PLATIN_d5->GDX | GLD5,GDX5,SPY5,mresid5,gi h{h}", FEAT3[("PLATIN", "d5")], [kret("GLD", 5), kret("GDX", 5), kret("SPY", 5), mr5, gi], "GDX", h)
    partial(f"P5 GLD5->GDX | GDX5,SPY5,mresid5,gi h{h}", kret("GLD", 5), [kret("GDX", 5), kret("SPY", 5), mr5, gi], "GDX", h)
    partial(f"P6 JPETF_d5->GDX | GLD5,GDX5,SPY5,gi h{h}", FEAT3[("JP_GOLD_ETF_1328", "d5")], [kret("GLD", 5), kret("GDX", 5), kret("SPY", 5), gi], "GDX", h)
partial("P7 gi->GDX | GLD1,GDX1,mresid1 h1", gi, [kret("GLD", 1), kret("GDX", 1), SIG1[("GDX~GLD+SPY", 1)]], "GDX", 1)
partial("P8 GDX5 own->GDX | GLD5,SPY5 h5", kret("GDX", 5), [kret("GLD", 5), kret("SPY", 5)], "GDX", 5)
partial("P9 GLD5 own->GLD | GDX5,SPY5 h5", kret("GLD", 5), [kret("GDX", 5), kret("SPY", 5)], "GLD", 5)
# --- (3) beta penceresi duyarlılığı (kayda)
def resid2(y, xs, win):
    X = pd.concat([R[x] for x in xs], axis=1); X.columns = xs
    B = roll_beta2(R[y], X, win, min(60, win // 2)).shift(1)
    return R[y] - sum(B[x] * R[x] for x in xs)
for win in (60, 500):
    e = resid2("GDX", ["GLD", "SPY"], win)
    for k in (5, 10):
        x = e.rolling(k).sum().shift(1)
        for h in (3, 5):
            st = test("a_madenci_artik", f"a3_GDX~GLD+SPY_W{win}_k{k}_GLD_h{h}", x, R["GLD"], h, f"resid GDX~GLD+SPY W={win} k={k} -> GLD", note="beta penceresi duyarlılığı")
            print("W", win, "k", k, "h", h, {kk: round(st[kk], 2) for kk in ["ic", "t", "t_is", "t_oos", "t_22"]}, st["yrs_same_sign"], "/", st["yrs"])
# --- (4) uç dönem dışlama
for key, T, h in [(("GDX~GLD+SPY", 10), "GLD", 5), (("GDX~GLD+SPY", 5), "GLD", 5), (("GDXJ~GLD+SPY", 1), "GDXJ", 3)]:
    x = SIG1[key].copy(); y = fwd(R[T], h)
    ex = pd.Series(False, index=x.index)
    for a, b in EXTREMES.values(): ex |= (x.index >= a) & (x.index <= b)
    st = test("a_madenci_artik", f"a4_{key[0]}_k{key[1]}_{T}_h{h}_uc_haric", x.where(~ex), R[T], h, f"{key} uç dönemler hariç", note="robust")
    print("uç hariç", key, T, h, {kk: round(st[kk], 2) for kk in ["ic", "t", "t_is", "t_oos", "t_22"]})
    print("placebo", key, T, h, placebo_lead(x, R[T], h))
print("placebo gi->GDX h1", placebo_lead(gi, R["GDX"], 1))
print("placebo PLATIN d5->GDX h3", placebo_lead(FEAT3[("PLATIN", "d5")], R["GDX"], 3))
