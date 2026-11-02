"""GÖREV 4: Rejimler (2018, Ara 2021, Haz 2023, Mar 2025, Eyl–Eki 2026 fon krizi) — senkron yapı, büyük/küçük ayrışması, öncülük değişimi."""
from ye_common import *
P = pd.read_parquet(RES + "/liq_portfolios.parquet"); P.columns = [f"{a}_{b}" for a, b in P.columns]
x30, x100, xtumy, xyuzo, xbank, xusin, xkobi = (idx_ret(k) for k in ["XU030", "XU100", "XTUMY", "XYUZO", "XBANK", "XUSIN", "XKOBI"])
V = pd.DataFrame({s: stk_ret(s) for s in VIOP})
cat = pd.read_csv(SCR + "/data/catalog.csv"); B = cat[cat.group.isin(["VIOP", "BIST_other"])].sym
ALL = pd.DataFrame({s.replace(".IS", ""): stk_ret(s) for s in B if not s.startswith("X")})
TVv = pd.DataFrame({s.replace(".IS", ""): turnover(s) for s in B if not s.startswith("X")}).reindex(ALL.index)
WIN = dict(REGIMES); WIN["2026_fon_krizi_cekirdek_16Eyl+"] = ("2026-09-16", "2026-10-30"); WIN["2026_Oca-Agu_oncesi"] = ("2026-01-01", "2026-08-31")
WIN["2024"] = ("2024-01-01", "2024-12-31"); WIN["2025_Haz-Ara"] = ("2025-06-01", "2025-12-31"); WIN["tum_2014-2026"] = ("2014-01-01", "2026-10-30")
def regz(y, x, own, a, b):
    df = pd.concat([y.rename("y"), x.rename("x"), own.rename("o")], axis=1); df = df[(df.index >= a) & (df.index <= b)].dropna()
    if len(df) < 25: return np.nan, np.nan, len(df)
    Z = (df - df.mean()) / df.std(); bb, tt, n, _ = ols_nw(Z["y"].values, Z[["x", "o"]].values, lags=3); return bb[1], tt[1], n
rows = []
for nm, (a, b) in WIN.items():
    a, b = pd.Timestamp(a), pd.Timestamp(b); sel = lambda s: s[(s.index >= a) & (s.index <= b)]
    r = {"regime": nm, "start": a.date(), "end": b.date(), "n_days": len(sel(x30).dropna())}
    r["cum_XU030_%"] = 100 * (np.exp(sel(x30).sum()) - 1); r["cum_XYUZO_%"] = 100 * (np.exp(sel(xyuzo).sum()) - 1); r["cum_XTUMY_%"] = 100 * (np.exp(sel(xtumy).sum()) - 1)
    r["cum_Q1illik_%"] = 100 * (np.exp(sel(P["cc_1"]).sum()) - 1); r["cum_Q5likit_%"] = 100 * (np.exp(sel(P["cc_5"]).sum()) - 1)
    r["rel_XTUMY-XU030_%"] = r["cum_XTUMY_%"] - r["cum_XU030_%"]; r["rel_XYUZO-XU030_%"] = r["cum_XYUZO_%"] - r["cum_XU030_%"]
    r["vol_XU030_ann%"] = 100 * sel(x30).std() * np.sqrt(252); r["vol_XTUMY_ann%"] = 100 * sel(xtumy).std() * np.sqrt(252)
    d = pd.concat([sel(x30), sel(xtumy), sel(xyuzo), sel(xbank), sel(xusin)], axis=1).dropna(); d.columns = ["x30", "tumy", "yuzo", "bank", "usin"]
    r["corr_XU030_XTUMY"] = d.x30.corr(d.tumy); r["corr_XU030_XYUZO"] = d.x30.corr(d.yuzo); r["corr_XBANK_XUSIN"] = d.bank.corr(d.usin)
    r["beta_XTUMY_on_XU030"] = np.polyfit(d.x30, d.tumy, 1)[0] if len(d) > 10 else np.nan
    v = sel(V).dropna(axis=1, thresh=10); cm = v.corr().values; r["avg_pair_corr_VIOP"] = np.nanmean(cm[np.triu_indices_from(cm, 1)])
    r["xsec_disp_bps"] = 1e4 * sel(ALL).std(axis=1).mean()
    for nmL, y_, x_, o_ in [("lead_XU030->XTUMY", xtumy, x30.shift(1), xtumy.shift(1)), ("lead_XU030->XYUZO", xyuzo, x30.shift(1), xyuzo.shift(1)),
                             ("lead_XU030->Q1_cc", P["cc_1"], x30.shift(1), P["cc_1"].shift(1)), ("lead_XU030->Q1_intra", P["intra_1"], x30.shift(1), P["cc_1"].shift(1)),
                             ("lead_XTUMY->XU030", x30, xtumy.shift(1), x30.shift(1)), ("lead_XBANK->XUSIN", xusin, xbank.shift(1), xusin.shift(1)), ("lead_XUSIN->XBANK", xbank, xusin.shift(1), xbank.shift(1)),
                             ("autocorr_XTUMY", xtumy, xtumy.shift(1), x30.shift(1)), ("autocorr_Q1", P["cc_1"], P["cc_1"].shift(1), x30.shift(1))]:
        bb, tt, n = regz(y_, x_, o_, a, b); r[f"{nmL}_b"] = bb; r[f"{nmL}_t"] = tt
    # likidite: Q1 vs Q5 medyan TL hacmi (dönem / önceki 120 gün)
    tvs = TVv[(TVv.index >= a) & (TVv.index <= b)].median(); tvp = TVv[(TVv.index < a)].tail(120).median()
    r["turnover_ratio_vs_prev120_median"] = (tvs / tvp).median()
    r["zero_ret_frac"] = (sel(ALL) == 0).sum().sum() / sel(ALL).notna().sum().sum()
    rows.append(r)
R = pd.DataFrame(rows); R.to_csv(RES + "/regimes.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 80)
print(R.set_index("regime").T.round(3).to_string())
# Fon krizi günlük tablo
fc = pd.DataFrame({"XU030": x30, "XU100": x100, "XYUZO": xyuzo, "XTUMY": xtumy, "XKOBI": xkobi, "Q1": P["cc_1"], "Q3": P["cc_3"], "Q5": P["cc_5"]})
fc = fc[(fc.index >= "2026-08-15") & (fc.index <= END)]
cum = 100 * (np.exp(fc.cumsum()) - 1)
print((100 * fc).round(2).assign(**{"cum_XTUMY-XU030": (cum.XTUMY - cum.XU030).round(2)}).to_string())
cum.to_csv(RES + "/fon_krizi_cum.csv")
