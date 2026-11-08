"""s7: (i) Asya altın madencileri artığı (gün t yerel kapanış, cutoff'tan önce) -> GLD/GDX: 'madenciler öncü' bulgusunun bağımsız piyasada tekrarı.
   Zijin 2899.HK & Zhaojin 1818.HK (HK kapanışı 16:10 HKT = 08:10 UTC), Shandong 600547.SS (15:00 CST = 07:00 UTC).
   Pencere: önceki yerel kapanış -> gün t yerel kapanış. Altın: xau_07utc (aynı pencere, ≈1 saat fark HK için), endeks: HSI / SSE (aynı borsa, senkron).
   e_t = r_miner - b_g * r_xau07 - b_m * r_index (250 gün yuvarlanan, beta_{t-1}). Yalnız yerel borsanın gün t'de işlem gördüğü günler.
(ii) Son 730 gün: C1 sinyali (t-1'de biten 10 gün GDX artığı) + gün t içi artık (t-1 16:00 -> t 14:30 ET) birleşimi -> GLD fwd.
"""
from e2_common import *
d = load()
R = {t: ret_of(d, t) for t in ["GLD", "GDX", "GDXJ", "SPY"]}
rows = []
x07 = np.log(d["xau_07utc"])
def local_ret(col):
    s = np.log(d[col].astype(float)); a = d[col + "_avail"]
    fresh = a.ne(a.shift(1))        # gün t'de yeni yerel kapanış var mı
    r = s.diff(); r[~fresh] = np.nan
    return r, fresh
res_list = []
for mc, ic_ in [("y_2899_HK", "y__HSI"), ("y_1818_HK", "y__HSI"), ("y_600547_SS", "y_000001_SS")]:
    rm, fr = local_ret(mc); ri, _ = local_ret(ic_)
    # altın: son taze yerel kapanıştan bu yana xau 07 UTC değişimi (tatil sonrası birikimli)
    last = x07.where(fr).ffill().shift(1)
    rg = (x07 - last).where(fr)
    X = pd.concat([rg.rename("g"), ri.rename("m")], axis=1)
    B = roll_beta2(rm, X, 250, 120).shift(1)
    e = rm - B["g"] * rg - B["m"] * ri
    res_list.append(e.rename(mc))
E = pd.concat(res_list, axis=1)
comp = E.mean(axis=1, skipna=True)          # eşit ağırlık (mevcut olanlar)
SIGA = {}
for k in (1, 5, 10):
    x = comp.fillna(0).rolling(k, min_periods=1).sum().where(comp.notna() | (k > 1))   # k=1: yalnız taze günler
    SIGA[k] = x
    for T in ["GLD", "GDX"]:
        for h in HS:
            rows.append(test("a_madenci_artik", f"a5_asya_madenci_artik_k{k}_{T}_h{h}", x, R[T], h, f"Asya madenci artığı (gün t 07-08 UTC) k={k} -> {T}"))
# kontrol: C1 (ABD madenci artığı) ile kısmi
SIG1 = pd.read_pickle(f"{OUT}/s1_signals.pkl")
from scipy.stats import norm
def rgz(s):
    r = s.rank(pct=True); n = s.notna().sum(); return pd.Series(norm.ppf((r * n - 0.5) / n), index=s.index)
for k in (5, 10):
    for h in (3, 5):
        y = rgz(fwd(R["GLD"], h)); X = pd.concat([rgz(SIGA[k]).rename("asya"), rgz(SIG1[("GDX~GLD+SPY", k)]).rename("abd")], axis=1)
        o = {}
        for nm, msk in [("full", slice(None)), ("is", X.index <= IS_END), ("oos", X.index > IS_END)]:
            Xm = X[msk] if not isinstance(msk, slice) else X
            r = nw_ols(y.reindex(Xm.index), Xm, lags=max(h, 5)); o[nm] = (round(r["t"], 2), round(float(r["model"].tvalues["abd"]), 2))
        register(AGENT, "a_kismi_rank", f"A_asya{k}_vs_abd{k}_GLD_h{h}", "Asya madenci artığı | ABD madenci artığı", h, dict(t=o["full"][0], t_is=o["is"][0], t_oos=o["oos"][0], n=None))
        print(f"kısmi GLD h{h} k{k}: (asya t, abd t) full {o['full']} is {o['is']} oos {o['oos']}")
# (ii) son 730 gün birleşim
SIG2 = pd.read_pickle(f"{OUT}/s2_signals.pkl")
intr = SIG2[("b2", "GDX~GLD+SPY")]
c1 = SIG1[("GDX~GLD+SPY", 10)]
lib_altin.IS_END = pd.Timestamp("2025-05-31")
for nm, x in [("C1_yalniz", c1.where(intr.notna())), ("gunici_yalniz", intr), ("C1+gunici", c1 + intr)]:
    for h in (3, 5):
        st = test("b_gunici_rv", f"b3_{nm}_GLD_h{h}", x, R["GLD"], h, f"son 730 gün {nm} -> GLD", note="hourly 730d")
        print(nm, h, {kk: round(st[kk], 3) for kk in ["ic", "t", "t_is", "t_oos", "n"]})
lib_altin.IS_END = pd.Timestamp("2017-12-31")
pd.to_pickle(SIGA, f"{OUT}/s7_signals.pkl")
res = pd.DataFrame(rows); cols = ["test_id", "h", "ic", "t", "t_is", "t_oos", "ic_oos", "t_22", "yrs_same_sign", "yrs", "n"]
res[cols].to_csv(f"{OUT}/s7_asya_madenci.csv", index=False)
pd.set_option("display.width", 250); print(res[cols].round(3).to_string())
print("Asya artık kapsama:", E.notna().sum().to_dict(), E.index[E.notna().any(axis=1)].min())
