"""Hedefli analizler -> res/*.csv ; ekrana sadece özet."""
import bk, ll, numpy as np, pandas as pd
pd.set_option("display.width", 220)
X = bk.R("XBANK"); M = bk.xu(); TRY = bk.R("TRY=X")
out = {}
# (a) yıllık korelasyon + kısmi korelasyon (XBANK)
drv = ["TUR", "TRY=X", "BBVA.MC", "BZ=F", "^TNX", "GC=F", "^VIX", "EMB", "EEM", "^STOXX50E", "SAN.MC", "ES=F"]
yr = {}; yp = {}
for d in drv:
    r = bk.R(d)
    df = pd.concat([X.rename("x"), r.rename("d"), M.rename("m")], axis=1).dropna(); df = df[df.index >= "2010-01-01"]
    yr[d] = df.groupby(df.index.year).apply(lambda g: g["x"].corr(g["d"]))
    yp[d] = df.groupby(df.index.year).apply(lambda g: bk.pc(g["x"], g["d"], g["m"]))
yr = pd.DataFrame(yr).round(2); yp = pd.DataFrame(yp).round(2)
yr.to_csv(bk.RES + "/xbank_yearly_corr.csv"); yp.to_csv(bk.RES + "/xbank_yearly_pcorr.csv")
print("XBANK yıllık corr:\n", yr[["TUR", "TRY=X", "BBVA.MC", "BZ=F", "^TNX", "GC=F", "EMB"]].to_string())
print("XBANK yıllık KISMİ corr (|XU100):\n", yp[["TUR", "TRY=X", "BBVA.MC", "BZ=F", "^TNX", "GC=F", "EMB"]].to_string())

# (b) XBANK'ın XU100'e göre fazla getirisi (banka faktörü) ile sürücüler
ex = X - (pd.concat([X, M], axis=1).dropna().cov().iloc[0, 1] / M.var()) * M
rows = []
for d in drv + ["TRY=X", "^MOVE", "HYG", "EMLC", "CEW", "2YY=F", "^IRX"]:
    r = bk.R(d); c, t, n = bk.hc_t(ex[ex.index >= "2010"], r)
    c3, t3, _ = bk.hc_t(ex[ex.index >= "2023-10-30"], r)
    rows.append((d, c, t, c3, t3, n))
bf = pd.DataFrame(rows, columns=["driver", "corr_exbank", "t", "corr_3y", "t_3y", "n"]).round(3)
bf.to_csv(bk.RES + "/bankfactor_drivers.csv"); print("\nBanka faktörü (XBANK - beta*XU100):\n", bf.to_string(index=False))

# (c) GARAN <-> BBVA
eub = pd.concat([bk.R(s) for s in ["SAN.MC", "BNP.PA", "ISP.MI", "UCG.MI", "DBK.DE"]], axis=1).mean(axis=1)  # Avrupa banka faktörü (aynı kapanış saati)
G = bk.R("GARAN"); Gu = G - TRY; B = bk.R("BBVA.MC"); BA = bk.R("BBVA")
res = {}
for lab, st in [("full", "2010"), ("IS", "2014"), ("OOS", "2021"), ("3y", "2023-10-30"), ("1y", "2025-10-30")]:
    en = "2021" if lab == "IS" else "2100"
    sl = lambda s: s[(s.index >= st) & (s.index < en)]
    df = pd.concat([sl(B).rename("b"), G.rename("g"), Gu.rename("gu"), eub.rename("e"), M.rename("m"), X.rename("x")], axis=1).dropna()
    import statsmodels.api as sm
    mdl = sm.OLS(df["b"], sm.add_constant(df[["e", "gu"]])).fit(cov_type="HC0")
    res[lab] = {"corr_B_G": df.b.corr(df.g), "pc_B_G|EUbank": bk.pc(df.b, df.g, df.e), "pc_B_Gusd|EUbank": bk.pc(df.b, df.gu, df.e),
                "beta_B_on_Gusd": mdl.params["gu"], "t": mdl.tvalues["gu"], "pc_G_B|XU100": bk.pc(df.g, df.b, df.m),
                "pc_G_B|XBANK": bk.pc(df.g, df.b, df.x), "pc_B_X|EU": bk.pc(df.b, df.x - TRY.reindex(df.index), df.e), "n": len(df)}
gb = pd.DataFrame(res).T.round(3); gb.to_csv(bk.RES + "/garan_bbva.csv"); print("\nGARAN<->BBVA.MC:\n", gb.to_string())
# Türkiye şok günleri: |XU100|>4% (veya TRY şoku) BBVA tepki
df = pd.concat([B.rename("b"), eub.rename("e"), Gu.rename("gu"), M.rename("m")], axis=1).dropna()
sh = df[df.m.abs() > 0.04]
print("Şok günü n=", len(sh), " BBVA-EUbank ort (XU100<-4%):", round(1e4 * (sh.b - sh.e)[sh.m < 0].mean(), 1), "bps;  (XU100>4%):", round(1e4 * (sh.b - sh.e)[sh.m > 0].mean(), 1), "bps")
for dd in ["2018-08-10", "2018-08-13", "2021-11-15", "2021-11-16", "2021-12-20", "2021-12-21", "2023-05-29", "2023-06-22", "2025-03-19", "2025-03-20", "2025-03-21"]:
    t = pd.Timestamp(dd)
    if t in df.index: print(dd, "GARAN(TL)", round(100 * G.get(t, np.nan), 2), "GARAN$", round(100 * df.loc[t, "gu"], 2), "BBVA.MC", round(100 * df.loc[t, "b"], 2), "EUbank", round(100 * df.loc[t, "e"], 2))

# (d) Kamu vs özel
pub = pd.concat([bk.R(s) for s in bk.STATE], axis=1).mean(axis=1); pri = pd.concat([bk.R(s) for s in bk.PRIVATE], axis=1).mean(axis=1)
spr = pub - pri; spr.rename("state_minus_private").to_frame().to_parquet(bk.RES + "/state_spread.parquet")
rows = []
for d in ["XU100", "TRY=X", "TUR", "GC=F", "BZ=F", "^VIX", "EMB", "^TNX", "BBVA.MC", "EEM", "DX-Y.NYB"]:
    r = bk.R(d); c, t, n = bk.hc_t(spr[spr.index >= "2010"], r); co, to, _ = bk.hc_t(spr[spr.index >= "2021"], r)
    ci, ti, _ = bk.hc_t(spr[(spr.index >= "2014") & (spr.index < "2021")], r)
    pcm = bk.pc(spr[spr.index >= "2010"], r, M) if d != "XU100" else np.nan
    rows.append((d, c, t, pcm, ci, ti, co, to, n))
sp = pd.DataFrame(rows, columns=["driver", "corr", "t", "pc_xu100", "is_corr", "is_t", "oos_corr", "oos_t", "n"]).round(3)
sp.to_csv(bk.RES + "/state_spread_drivers.csv"); print("\nKamu-Özel spread sürücüleri:\n", sp.to_string(index=False))
# banka bazında betalar (çoklu regresyon: XU100, TRY, GC, BZ, VIX) 2021+
import statsmodels.api as sm
rows = []
for s in bk.ALL:
    for per, st, en in [("IS", "2014", "2021"), ("OOS", "2021", "2100")]:
        df = pd.concat([bk.R(s).rename("y"), M.rename("XU100"), TRY.rename("TRY"), bk.R("GC=F").rename("GC"), bk.R("BZ=F").rename("BZ"), bk.R("^VIX").rename("VIX"), bk.R("EMB").rename("EMB")], axis=1).dropna()
        df = df[(df.index >= st) & (df.index < en)]
        m = sm.OLS(df["y"], sm.add_constant(df.drop(columns="y"))).fit(cov_type="HC0")
        rows.append({"stock": s, "per": per, **{f"b_{k}": m.params[k] for k in m.params.index if k != "const"}, **{f"t_{k}": m.tvalues[k] for k in m.params.index if k != "const"}, "r2": m.rsquared})
bb = pd.DataFrame(rows).round(3); bb.to_csv(bk.RES + "/bank_multibeta.csv")
print("\nÇoklu beta (OOS 2021+):\n", bb[bb.per == "OOS"][["stock", "b_XU100", "b_TRY", "t_TRY", "b_GC", "t_GC", "b_BZ", "t_BZ", "b_EMB", "t_EMB", "r2"]].to_string(index=False))
print(bb[bb.per == "IS"][["stock", "b_XU100", "b_TRY", "t_TRY", "b_GC", "t_GC", "b_BZ", "t_BZ", "r2"]].to_string(index=False))

# (e) Altın: USD ve TL bazlı
gtl = bk.R("GC=F") + TRY
rows = []
for s in bk.ALL:
    a = bk.R(s)
    rows.append((s, bk.pc(a, bk.R("GC=F"), M), bk.pc(a, gtl, M), bk.pc(a, bk.R("GC=F"), [M, TRY]), bk.pc(a[a.index >= "2021"], bk.R("GC=F"), M), bk.pc(a[a.index >= "2023-10-30"], bk.R("GC=F"), M)))
gd = pd.DataFrame(rows, columns=["stock", "pc_GCusd|XU", "pc_GCtl|XU", "pc_GC|XU,TRY", "pc_GC|XU_2021+", "pc_GC|XU_3y"]).round(3)
gd.to_csv(bk.RES + "/gold.csv"); print("\nAltın:\n", gd.to_string(index=False))

# (f) ^MOVE zaman damgası kontrolü
mv = bk.R("^MOVE"); vx = bk.R("^VIX"); tn = bk.R("^TNX")
print("\nMOVE hizalama: corr(MOVE_t, VIX_t)=%.3f corr(MOVE_t,VIX_{t-1})=%.3f corr(MOVE_t,VIX_{t+1})=%.3f | |dTNX|: lag0 %.3f lag-1 %.3f lag+1 %.3f" % (
    mv.corr(vx), mv.corr(vx.shift(1)), mv.corr(vx.shift(-1)), mv.corr(tn.abs()), mv.corr(tn.abs().shift(1)), mv.corr(tn.abs().shift(-1))))
