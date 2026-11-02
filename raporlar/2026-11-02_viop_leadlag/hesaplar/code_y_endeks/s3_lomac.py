"""GÖREV 2b: Büyük -> küçük öncülüğü (Lo–MacKinlay çapraz otokorelasyonu), likit/illikit ayrımı.
1) 176 BIST hissesi (veri setindeki tümü) -> aylık likidite (önceki 60 gün medyan TL hacim) beşlileri, eşit ağırlıklı portföy (cc/gap/intra).
   corr(Q_i,t , Q_j,t-1) matrisi + regresyon Q1_t = a + b Q5_{t-1} + c Q1_{t-1} (+XU100_{t-1}) ve ters yön.
2) Endeks düzeyi: XU030 -> XYUZO / XTUMY / XKOBI / XU100-dışı; ters yön.
3) VİOP hisselerinde XU030-ex_{t-1} öncülük katsayısı ~ likidite (kesit).
4) Yıllara ve rejimlere göre.
"""
from ye_common import *
cat = pd.read_csv(SCR + "/data/catalog.csv"); B = cat[cat.group.isin(["VIOP", "BIST_other"])].sym
STK = [s.replace(".IS", "") for s in B if not s.startswith("X")]
R = {}; G = {}; I_ = {}; TV = {}; Z = {}
for s in STK:
    y = s + ".IS"; d = stk_dec(y); R[s] = stk_ret(y); G[s] = d["gap"]; I_[s] = d["intra"]
    TV[s] = turnover(y)
R = pd.DataFrame(R); G = pd.DataFrame(G).reindex(R.index); I_ = pd.DataFrame(I_).reindex(R.index); TV = pd.DataFrame(TV).reindex(R.index)
R = R[R.index >= "2012-01-01"]; G = G.reindex(R.index); I_ = I_.reindex(R.index); TV = TV.reindex(R.index)
liq = TV.rolling(60, min_periods=40).median().shift(1)
# sıfır getiri oranı (bayat fiyat göstergesi), önceki 60 gün
zf = (R == 0).astype(float).where(R.notna()).rolling(60, min_periods=40).mean().shift(1)
me = liq.resample("MS").first()  # ay başı sıralama (önceki günlere dayalı)
grp = pd.DataFrame(index=R.index, columns=R.columns, dtype=float)
for mdt in me.index:
    row = me.loc[mdt].dropna()
    if len(row) < 30: continue
    q = pd.qcut(row.rank(method="first"), 5, labels=False) + 1
    msk = (R.index >= mdt) & (R.index < mdt + pd.DateOffset(months=1))
    grp.loc[msk, q.index] = np.tile(q.values, (msk.sum(), 1))
P = {}
for lab, X in [("cc", R), ("gap", G), ("intra", I_)]:
    for q in range(1, 6):
        P[(lab, q)] = X.where(grp == q).mean(axis=1)
P = pd.DataFrame(P)
nst = grp.notna().sum(axis=1)
zfq = {q: zf.where(grp == q).mean(axis=1).mean() for q in range(1, 6)}
liqq = {q: (liq.where(grp == q).median(axis=1)).median() / 1e6 for q in range(1, 6)}
print("hisse sayısı medyan:", nst[nst > 0].median(), "sıfır getiri oranı:", {k: round(v, 3) for k, v in zfq.items()}, "medyan hacim mn TL:", {k: round(v, 1) for k, v in liqq.items()})
P = P[P.index >= START]
m = idx_ret("XU100"); x30 = idx_ret("XU030")
PER = {"full": (START, END), "IS": (START, SPLIT - pd.Timedelta(days=1)), "OOS": (SPLIT, END)}
def reg(y, x, ctr, per="full"):
    df = pd.concat([y.rename("y"), x.rename("x")] + [c.rename(f"c{i}") for i, c in enumerate(ctr)], axis=1)
    a, b = PER[per] if isinstance(per, str) else per; df = df[(df.index >= a) & (df.index <= b)].dropna()
    if len(df) < 40: return np.nan, np.nan, len(df)
    Zd = (df - df.mean()) / df.std(); bb, tt, n, _ = ols_nw(Zd["y"].values, Zd.drop(columns="y").values); return bb[1], tt[1], n
rows = []
# 1) çapraz otokorelasyon matrisi (cc)
cm = pd.DataFrame(index=range(1, 6), columns=range(1, 6), dtype=float)
for i in range(1, 6):
    for j in range(1, 6):
        cm.loc[i, j] = P[("cc", i)].corr(P[("cc", j)].shift(1))
print("corr(Q_i,t , Q_j,t-1)  (satır i=takipçi, sütun j=lider; 1=en illikit, 5=en likit)\n", cm.round(3))
cm.to_csv(RES + "/lomac_crossauto.csv")
for tgt in ["cc", "gap", "intra"]:
    for per in list(PER) + list(REGIMES):
        pp = PER.get(per, REGIMES.get(per))
        for (yq, xq) in [(1, 5), (2, 5), (3, 5), (5, 1)]:
            y = P[(tgt, yq)]; x = P[("cc", xq)].shift(1)
            b, t, n = reg(y, x, [P[("cc", yq)].shift(1)], pp); b2, t2, n2 = reg(y, x, [P[("cc", yq)].shift(1), m.shift(1)], pp) if xq != 5 else (np.nan, np.nan, 0)
            rows.append(dict(test=f"Q{xq}_lag1->Q{yq}", target=tgt, per=per, b=b, t=t, n=n, b_ctrlXU100=b2, t_ctrlXU100=t2))
        for lead, fol in [("XU030", "XYUZO"), ("XU030", "XTUMY"), ("XU030", "XKOBI"), ("XU100", "XTUMY"), ("XYUZO", "XU030"), ("XTUMY", "XU030"), ("XU030", "Q1"), ("XU030", "Q3")]:
            if tgt != "cc" and fol.startswith("X"): continue
            y = P[(tgt, int(fol[1]))] if fol.startswith("Q") else idx_ret(fol)
            own = P[("cc", int(fol[1]))].shift(1) if fol.startswith("Q") else idx_ret(fol).shift(1)
            b, t, n = reg(y, idx_ret(lead).shift(1), [own], pp)
            rows.append(dict(test=f"{lead}_lag1->{fol}", target=tgt, per=per, b=b, t=t, n=n))
L = pd.DataFrame(rows); L.to_csv(RES + "/lomac_tests.csv", index=False)
pd.set_option("display.width", 220)
print(L[L.per.isin(["full", "IS", "OOS"])].pivot_table(index=["test", "target"], columns="per", values=["b", "t"]).round(3).to_string())
print(L[~L.per.isin(["full", "IS", "OOS"]) & (L.target == "cc")].pivot_table(index="test", columns="per", values="b").round(3).to_string())
# yıllara göre: XU030_{t-1} -> Q1_t (cc) ve XTUMY
yr = []
for y_ in range(2014, 2027):
    a, b_ = pd.Timestamp(f"{y_}-01-01"), pd.Timestamp(f"{y_}-12-31")
    r1 = reg(P[("cc", 1)], x30.shift(1), [P[("cc", 1)].shift(1)], (a, b_)); r2 = reg(idx_ret("XTUMY"), x30.shift(1), [idx_ret("XTUMY").shift(1)], (a, b_))
    r3 = reg(P[("intra", 1)], x30.shift(1), [P[("cc", 1)].shift(1)], (a, b_))
    yr.append(dict(year=y_, b_Q1cc=r1[0], t_Q1cc=r1[1], b_Q1intra=r3[0], t_Q1intra=r3[1], b_XTUMY=r2[0], t_XTUMY=r2[1]))
Y = pd.DataFrame(yr); Y.to_csv(RES + "/lomac_years.csv", index=False); print(Y.round(3).to_string())
P.to_parquet(RES + "/liq_portfolios.parquet")
# 3) VİOP kesit: likidite ve bayatlık
A = pd.read_csv(RES + "/lead_idx_to_stock.csv") if os.path.exists(RES + "/lead_idx_to_stock.csv") else None
if A is not None:
    lv = pd.Series({s: np.log(TV[s][TV.index >= "2021-01-01"].median()) for s in VIOP}); z0 = pd.Series({s: (R[s][R.index >= "2021-01-01"] == 0).mean() for s in VIOP})
    out = []
    for tgt in ["cc", "gap", "intra"]:
        a = A[(A.idx == "XU030") & (A.target == tgt)]
        a = a[a["var"] == "ex"].set_index("stock").reindex(VIOP).combine_first(a[a["var"] == "raw"].set_index("stock"))
        bb = a["b_OOS"]
        out.append(dict(target=tgt, corr_b_logliq=bb.corr(lv), corr_b_zero=bb.corr(z0), spearman_b_logliq=bb.corr(lv, method="spearman"), mean_b=bb.mean(),
                        mean_b_illiq=bb[lv < lv.median()].mean(), mean_b_liq=bb[lv >= lv.median()].mean()))
    print(pd.DataFrame(out).round(3))
    pd.DataFrame(out).to_csv(RES + "/lomac_viop_cross.csv", index=False)
    pd.DataFrame({"log_turnover_2021": lv, "zero_ret_frac_2021": z0}).to_csv(RES + "/viop_liquidity.csv")
