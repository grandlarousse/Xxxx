"""v_duyarlilik ek testler:
(a) SASA çiftleri hisse-ajanı tarzında (ll.decomp cc, BIST takvimi, 2014+): v3 vs v4, ajan değerleriyle karşılaştırma
(b) SASA varyans payları (XU100; küresel-8 t ve t-1) 1y/3y/2024-26: v3 vs v4 (ag ajanının 'en yerli hisse SASA' iddiası)
(c) Madde 3 sağlamlık: Spearman medyanları
(d) Gap fade h1 dönemi (2023-12+) girişler: E0 açılış / E2 ilk saat barı (h+l+c)/3 / E3 07:30 UTC (10:30 TSİ) — v3 vs v4
(e) EREGL–ISDMR ve TRALT–GC=F sağlamlık: Spearman ve %1 winsorize kısmi korelasyon
(f) Gap fade IS v3->v4 farkının kaynağı: v4'ün eklediği işlemler ve cc-filtresinin sonuca koşullanması
"""
import vers, numpy as np, pandas as pd, statsmodels.api as sm
L = vers.L; STK = vers.VIOP; V = ["v3", "v4"]
OUT = []
def rec(item, stock, driver, metric, period, vals, note=""):
    OUT.append(dict(item=item, stock=stock, driver=driver, metric=metric, period=period, v3=vals.get("v3"), v4=vals.get("v4"), note=note))
def pc(a, b, m):
    df = pd.concat([a.rename("a"), b.rename("b"), m.rename("m")], axis=1).dropna()
    if len(df) < 30: return np.nan, len(df)
    C = np.column_stack([np.ones(len(df)), df["m"].values])
    ra = df["a"].values - C @ np.linalg.lstsq(C, df["a"].values, rcond=None)[0]; rb = df["b"].values - C @ np.linalg.lstsq(C, df["b"].values, rcond=None)[0]
    return float(np.corrcoef(ra, rb)[0, 1]), len(df)
def nw_mean(x, lags=5):
    x = pd.Series(x).dropna()
    if len(x) < 20: return np.nan, np.nan, len(x)
    m = sm.OLS(x.values, np.ones(len(x))).fit(cov_type="HAC", cov_kwds={"maxlags": lags}); return float(m.params[0]), float(m.tvalues[0]), len(x)
D = {v: {s: L[v].decomp(s + ".IS") for s in STK + ["XU100", "XU030", "HEKTS", "KMPUR", "SMRTG", "ISDMR", "EREGL"]} for v in V}
CAL = L["v4"].bist_cal(); CAL = CAL[CAL >= "2014-01-01"]; LAST = CAL[-1]
# ---------------- (a) hisse ajanı tarzı SASA çiftleri
AG = {"HEKTS": (0.474, 0.643, 0.547, 0.301, 0.541), "KMPUR": (0.396, 0.397, 0.403, 0.170, 0.386), "SMRTG": (0.350, 0.356, 0.204, 0.169, 0.416)}
for drv in ["HEKTS", "KMPUR", "SMRTG", "XU100"]:
    res = {}
    for v in V:
        cc = pd.DataFrame({k: D[v][k]["cc"].reindex(CAL) for k in ["SASA", drv, "XU100"]})
        o = {}
        for lab, st in [("full", CAL[0]), ("3y", LAST - pd.DateOffset(years=3)), ("1y", LAST - pd.DateOffset(years=1))]:
            d = cc[cc.index >= st][["SASA", drv]].dropna(); o[f"corr_{lab}"] = d["SASA"].corr(d[drv]); o[f"n_{lab}"] = len(d)
        if drv != "XU100": o["pc_full"], _ = pc(cc["SASA"], cc[drv], cc["XU100"])
        d = cc[["SASA", drv]].dropna(); o["beta_full"] = float(np.cov(d["SASA"], d[drv])[0, 1] / np.var(d[drv], ddof=1))
        d1 = cc[cc.index >= LAST - pd.DateOffset(years=1)][["SASA", drv]].dropna(); o["beta_1y"] = float(np.cov(d1["SASA"], d1[drv])[0, 1] / np.var(d1[drv], ddof=1))
        res[v] = o
    for k in res["v4"]:
        note = ""
        if drv in AG:
            mp = {"corr_full": 0, "corr_3y": 1, "corr_1y": 2, "pc_full": 3, "beta_full": 4}
            if k in mp: note = f"ajan (f_y_hisse) değeri {AG[drv][mp[k]]}"
        rec("5a_sasa_decompcc", "SASA.IS", drv + ".IS", k.rsplit("_", 1)[0], k.rsplit("_", 1)[1], {v: res[v][k] for v in V}, note)
# ---------------- (b) SASA varyans payı: XU100 ve küresel-8 (t, t-1), ret tabanlı ve decomp-cc tabanlı
G8 = ["ES=F", "EEM", "^STOXX50E", "^VIX", "DX-Y.NYB", "BZ=F", "GC=F", "^TNX"]
for v in V:
    pass
GR = {g: L["v4"].ret(g) for g in G8}  # BIST dışı: sürümden bağımsız
for base in ["ret", "decomp_cc"]:
    for per, st, en in [("1y", LAST - pd.DateOffset(years=1), LAST), ("2024-26", pd.Timestamp("2024-01-01"), LAST), ("3y", LAST - pd.DateOffset(years=3), LAST), ("2014-20", pd.Timestamp("2014-01-01"), pd.Timestamp("2020-12-31"))]:
        r2x, r2g, nn = {}, {}, {}
        for v in V:
            y = L[v].ret("SASA.IS") if base == "ret" else D[v]["SASA"]["cc"].reindex(CAL)
            x = L[v].ret("XU100.IS")
            X = pd.DataFrame({**{g: GR[g] for g in G8}, **{g + "_1": GR[g].shift(1) for g in G8}})
            df = pd.concat([y.rename("y"), x.rename("x"), X], axis=1).dropna(); df = df[(df.index >= st) & (df.index <= en)]
            r2x[v] = df["y"].corr(df["x"]) ** 2
            r2g[v] = sm.OLS(df["y"], sm.add_constant(df[list(X.columns)])).fit().rsquared_adj; nn[v] = len(df)
        rec("5b_sasa_varshare", "SASA.IS", "XU100", f"R2_{base}", per, r2x); rec("5b_sasa_varshare", "SASA.IS", "KÜRESEL-8 (t,t-1)", f"adjR2_{base}", per, r2g)
        rec("5b_sasa_varshare", "SASA.IS", "-", f"n_{base}", per, nn)
# ---------------- (c) madde 3 Spearman
es1 = L["v4"].ret("ES=F").shift(1)
for col in ["gap", "intra"]:
    for per, st, en in [("IS", "2014-01-01", "2020-12-31"), ("OOS", "2021-01-01", "2026-12-31")]:
        med = {}
        for v in V:
            cs = []
            for s in STK:
                df = pd.concat([D[v][s][col].rename("y"), es1.rename("e")], axis=1).dropna(); df = df[(df.index >= st) & (df.index <= en)]
                cs.append(df["y"].corr(df["e"], method="spearman"))
            med[v] = float(np.nanmedian(cs))
        rec("3_es_lag1_spearman", "47 medyan", "ES=F(t-1)", f"spearman_{col}", per, med)
# ---------------- (d) gap fade h1 dönemi giriş varyantları
def h1_entry(s):
    h = vers.L["v4"].raw(s + ".IS", "h1"); h = h[~h.index.duplicated(keep="last")]
    fb = h[(h.index.hour == 6) & (h.index.minute == 30)].copy(); fb.index = pd.DatetimeIndex(fb.index.tz_convert(None).normalize())
    return ((fb["h"] + fb["l"] + fb["c"]) / 3), fb["c"]
TP = {}; P730 = {}
for s in STK: TP[s], P730[s] = h1_entry(s)
H1START = pd.Timestamp("2023-12-01")
for v in V:
    rows = {}
    for en in ["E0_open", "E2_tp_ilkbar", "E3_0730UTC"]:
        G = {}
        for s in STK:
            d = D[v][s]; d = d[d.index >= H1START]
            raw = vers._raw(s + ".IS").reindex(d.index)
            c730 = P730[s].reindex(d.index)
            # h1 veri hatası filtresi (ör. HEKTS 2024-09 h1 fiyatları bölünmeye göre düzeltilmemiş): |O->07:30| ve |07:30->C| <= %12
            ok = d["intra"].notna() & TP[s].reindex(d.index).notna() & (np.log(c730 / raw["o"]).abs() <= 0.12) & (np.log(raw["c"] / c730).abs() <= 0.12)
            px = raw["o"] if en == "E0_open" else (TP[s].reindex(d.index) if en == "E2_tp_ilkbar" else P730[s].reindex(d.index))
            y = np.log(raw["c"] / px).where(ok)
            pos = -np.sign(d["gap"]).where(d["gap"].abs() > 0.01, 0.0)
            G[s] = (pos * y).where((pos != 0) & y.notna())
        G = pd.DataFrame(G); pp = G.mean(axis=1); m, t, n = nw_mean(pp)
        rows[en] = (1e4 * m, t, int(G.notna().sum().sum()))
        ms, ts, ns = nw_mean(G["SASA"])
        rec("4b_gapfade_h1", "SASA.IS", "own |gap|>%1", f"{en}_mean_bps", "2023-12+", {v: 1e4 * ms}) if False else None
        OUT.append(dict(item="4b_gapfade_h1", stock="portföy 47", driver="own |gap|>%1", metric=f"{en}_mean_bps", period="2023-12..2026-10", **{v: 1e4 * m}, note=f"{v}: t={t:.2f}, işlem={int(G.notna().sum().sum())}"))
        OUT.append(dict(item="4b_gapfade_h1", stock="SASA.IS", driver="own |gap|>%1", metric=f"{en}_mean_bps", period="2023-12..2026-10", **{v: 1e4 * ms}, note=f"{v}: t={ts:.2f}, işlem={ns}"))
# satırları v3/v4 olarak birleştir
X = pd.DataFrame(OUT)
X = X.groupby(["item", "stock", "driver", "metric", "period"], sort=False).agg({"v3": "first", "v4": "first", "note": lambda z: " | ".join(sorted(set([str(q) for q in z if isinstance(q, str) and q])))}).reset_index()
OUT = X.to_dict("records")
# ---------------- (e) sağlamlık: Spearman ve winsorize kısmi korelasyon
def wins(x, q=0.01):
    lo, hi = x.quantile(q), x.quantile(1 - q); return x.clip(lo, hi)
for a, b in [("EREGL.IS", "ISDMR.IS"), ("TRALT.IS", "GC=F"), ("THYAO.IS", "LHA.DE"), ("AEFES.IS", "CCOLA.IS")]:
    for per, st, en in [("full", "2010-01-01", "2026-12-31"), ("IS", "2014-01-01", "2020-12-31")]:
        o = {}; ow = {}; os_ = {}
        for v in V:
            ra, rb, rm = L[v].ret(a), L[v].ret(b), L[v].ret("XU100.IS")
            df = pd.concat([ra.rename("a"), rb.rename("b"), rm.rename("m")], axis=1).dropna(); df = df[(df.index >= st) & (df.index <= en)]
            o[v], _ = pc(df["a"], df["b"], df["m"])
            ow[v], _ = pc(wins(df["a"]), wins(df["b"]), wins(df["m"]))
            rk = df.rank(); os_[v], _ = pc(rk["a"], rk["b"], rk["m"])
        rec("1c_pair_robust", a, b, "pc_pearson", per, o); rec("1c_pair_robust", a, b, "pc_winsor1%", per, ow); rec("1c_pair_robust", a, b, "pc_spearman", per, os_)
# ---------------- (f) gap fade IS farkının kaynağı
add_rows = []
for s in STK:
    g3, g4 = D["v3"][s], D["v4"][s]
    for d_, tag in [(g3, "v3"), (g4, "v4")]:
        pass
    i = g4.index[(g4.index >= "2014-01-01") & (g4.index < "2021-01-01")]
    a3 = g3.reindex(i); a4 = g4.reindex(i)
    tr3 = a3["gap"].abs() > 0.01; tr4 = a4["gap"].abs() > 0.01
    new = tr4 & ~tr3 & a4["intra"].notna()
    pnl = (-np.sign(a4["gap"]) * a4["intra"])[new]
    for t_, p_ in pnl.items(): add_rows.append(dict(stock=s, date=t_.date(), gap=a4.loc[t_, "gap"], intra=a4.loc[t_, "intra"], cc=a4.loc[t_, "cc"], pnl_bps=1e4 * p_))
A = pd.DataFrame(add_rows); A.to_csv(vers.RES + "/d2_fade_added_trades.csv", index=False)
OUT.append(dict(item="4c_fade_IS_kaynak", stock="47", driver="v4'ün eklediği IS işlemleri", metric="n", period="IS", v3=0, v4=len(A), note=""))
OUT.append(dict(item="4c_fade_IS_kaynak", stock="47", driver="v4'ün eklediği IS işlemleri", metric="mean_pnl_bps", period="IS", v3=np.nan, v4=A["pnl_bps"].mean(), note=f"medyan {A['pnl_bps'].median():.0f}; >0 payı {(A['pnl_bps']>0).mean():.2f}; |cc|>%10,5 olanlar {int((A['cc'].abs()>np.log(1.105)).sum())}"))
# cc-koşullanması: 2014-20, |gap|>%1 günlerinde, |cc| bant içi olan vs olmayan fade pnl (v4 verisi)
ALL = []
for s in STK:
    a4 = D["v4"][s]; a4 = a4[(a4.index >= "2014-01-01") & (a4.index < "2021-01-01")]
    m = (a4["gap"].abs() > 0.01) & a4["intra"].notna()
    x = a4[m].copy(); x["pnl"] = -np.sign(x["gap"]) * x["intra"]; x["band"] = x["cc"].abs() > np.log(1.105); ALL.append(x)
ALL = pd.concat(ALL)
for b_, lab in [(True, "|cc|>%10,5 (v3'te silinen)"), (False, "|cc|<=%10,5")]:
    z = ALL[ALL.band == b_]["pnl"]
    OUT.append(dict(item="4c_fade_IS_kaynak", stock="47 havuz", driver=lab, metric="mean_pnl_bps", period="IS", v3=np.nan, v4=1e4 * z.mean(), note=f"n={len(z)}; >0 payı {(z>0).mean():.2f}"))
R = pd.DataFrame(OUT); R.to_csv(vers.RES + "/d2_extra.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 500); pd.set_option("display.max_colwidth", 80)
print(R.round(4).to_string())
