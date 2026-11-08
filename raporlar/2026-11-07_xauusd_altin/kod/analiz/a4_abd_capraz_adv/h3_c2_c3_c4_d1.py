"""h3: C2 (eğri Δ5), C3 (DXY sapması C), C4 (reel+dolar model artığı), D1 (dolar emilim) çürütme denemesi."""
import sys, json; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a4_abd_capraz_adv")
from adv_common import *
pd.set_option("display.width", 250)
d = load_viop(); sp = load_spot(); idx = d.index; ISM = idx <= IS_END; OOSM = ~ISM

def hourly_px(sym):
    h = hourly(sym).copy(); i = pd.to_datetime(h.index)
    if i.tz is not None: i = i.tz_convert("UTC").tz_localize(None)
    return pd.Series(h["c"].values, index=i + pd.Timedelta(hours=1))
XAU = hourly_px("XAUUSD"); DXY = hourly_px("DOLLARIDXUSD")
prev = pd.Series(idx, index=idx).shift(1)
def win(px, d0, h0, d1, h1):
    return pd.Series(np.log(px.reindex(pd.DatetimeIndex(d1) + pd.Timedelta(hours=h1)).values / px.reindex(pd.DatetimeIndex(d0) + pd.Timedelta(hours=h0)).values), index=idx)

def sub_table(x, y, pos, h, ret=None, label=""):
    ret = d.v_ret if ret is None else ret
    rows = []
    for nm, a, b in SUBP + [("IS", "2017-01-01", "2021-12-31"), ("OOS", "2022-01-01", "2026-12-31"), ("full", "2010-01-01", "2026-12-31"),
                            ("2025-26 hariç", None, None), ("2020,2025,2026 hariç", None, None)]:
        if a is None:
            m = ~idx.year.isin([2025, 2026]) if nm.startswith("2025") else ~idx.year.isin([2020, 2025, 2026])
        else:
            m = per_mask(idx, a, b)
        s = ic(x[m], y[m], max(h, 5)); p = ic(x[m], y[m], max(h, 5), "pearson")
        rows.append(dict(donem=nm, n=s["n"], ic=round(s["ic"], 3), t=round(s["t"], 2), pear_t=round(p["t"], 2), sh5=bt_stats(pos[m], ret[m], h)["sh"], t5=bt_stats(pos[m], ret[m], h)["t"],
                         sh10=bt_stats(pos[m], ret[m], h, 10)["sh"], sh_dm=bt_stats(pos[m], ret[m], h, demean=True)["sh"],
                         long=bt_stats(pos[m].clip(lower=0), ret[m], h)["sh"], short=bt_stats(pos[m].clip(upper=0), ret[m], h)["sh"]))
    T = pd.DataFrame(rows); print(label, "\n", T.to_string(index=False)); return T

R = {}
# ================= C2
curve = d.ust_nom10 - d.ust_nom2
z2 = zscale(curve.diff(5)); p2 = (z2 / 2).clip(-1, 1).fillna(0.0)
R["C2_alt"] = sub_table(z2, d.fwd1, p2, 1, label="C2 alt dönem").to_dict("records")
# komşu parametreler: Δk k=1..20, eğri tanımı, h
rows = []
for nm, c in (("10-2", d.ust_nom10 - d.ust_nom2), ("10-3m", d.ust_nom10 - d.ust_nom3m), ("30-5", d.ust_nom30 - d.ust_nom5), ("5-2", d.ust_nom5 - d.ust_nom2), ("30-2", d.ust_nom30 - d.ust_nom2), ("2y(-)", -d.ust_nom2), ("10y", d.ust_nom10)):
    for k in (1, 2, 3, 5, 10, 20):
        zz = zscale(c.diff(k))
        for h in (1, 3, 5):
            s = split_stats(zz, d[f"fwd{h}"], h)
            rows.append(dict(egri=nm, k=k, h=h, ic=round(s["ic"], 3), t=round(s["t"], 2), t_is=round(s["t_is"], 2), t_oos=round(s["t_oos"], 2)))
G = pd.DataFrame(rows)
print("C2 komşu (h=1) t\n", G[G.h == 1].pivot(index="egri", columns="k", values="t").to_string())
print("C2 komşu (h=1) t_is\n", G[G.h == 1].pivot(index="egri", columns="k", values="t_is").to_string())
print("C2 10-2 tüm h\n", G[G.egri == "10-2"].pivot(index="k", columns="h", values="t").to_string())
G.to_csv(f"{OUT}/h3_c2_komsu.csv", index=False)
# erken spot
zs = zscale((sp.ust_nom10 - sp.ust_nom2).diff(5)); ps = (zs / 2).clip(-1, 1).fillna(0.0)
for nm, a, b in [("2010-12", "2010-01-01", "2012-12-31"), ("2013-16", "2013-01-01", "2016-12-31"), ("2010-16", "2010-01-01", "2016-12-31"), ("2017-26", "2017-03-01", "2026-12-31")]:
    m = per_mask(sp.index, a, b); s = ic(zs[m], sp.sfwd1[m], 5)
    print("C2 spot", nm, round(s["ic"], 3), round(s["t"], 2), bt_stats(ps[m], sp.s_ret[m], 1))
# C2 hazine verisi zaman kontrolü: panel ust_nom10 gün t değeri = ham Hazine gün t-1?
print("C2: ust değişimi gün t vs xau 15→15 aynı gün korelasyonu (bilgi zamanı makul mü):",
      round(pd.concat([d.ust_real10.diff(), np.log(d.xau_p15).diff()], axis=1).corr().iloc[0, 1], 3),
      " bir gün önceki altın:", round(pd.concat([d.ust_real10.diff(), np.log(d.xau_p15).diff().shift(1)], axis=1).corr().iloc[0, 1], 3),
      " t-1 20:00 altın [t-2 20 → t-1 20]:", round(pd.concat([d.ust_real10.diff(), win(XAU, prev.shift(1).values, 20, prev.values, 20)], axis=1).corr().iloc[0, 1], 3))

# ================= C3
x_dxy = win(DXY, prev.values, 20, idx, 15); g_C = win(XAU, prev.values, 20, idx, 15)
b = beta(g_C, x_dxy, 250, 150); b = (x_dxy.rolling(250, min_periods=150).cov(g_C) / x_dxy.rolling(250, min_periods=150).var()).shift(1)
z3 = zscale(b * x_dxy - g_C); p3 = -(z3 / 2).clip(-1, 1).fillna(0.0)
R["C3_alt"] = sub_table(-z3, d.fwd1, p3, 1, label="C3 alt dönem (işaret çevrilmiş: -gap)").to_dict("records")
zg = zscale(g_C)
print("C3: altının kendi C getirisi (z) → fwd1:", {k: round(v, 3) for k, v in split_stats(zg, d.fwd1, 1).items() if k not in ("by_year",)})
pg = (zg / 2).clip(-1, 1).fillna(0.0)
print("C3: altın öz-momentum kuralı backtest IS/OOS:", bt_stats(pg[ISM], d.v_ret[ISM], 1), bt_stats(pg[OOSM], d.v_ret[OOSM], 1))
# kısmi: -gap | altın C
X = pd.concat([(-z3).rename("x"), zg.rename("g"), d.fwd1.rename("y")], axis=1).dropna()
for nm, m in (("full", slice(None)), ("IS", X.index <= IS_END), ("OOS", X.index > IS_END)):
    XX = X[m] if not isinstance(m, slice) else X; Z = XX.rank(); Z = (Z - Z.mean()) / Z.std()
    print("C3 sıra-kısmi", nm, round(nw_ols(Z.y, Z[["x", "g"]], lags=5)["t"], 2), "| DXY C getirisi tek başına:", round(ic(zscale(x_dxy)[XX.index], XX.y, 5)["t"], 2))

# ================= C4
r4 = pd.read_parquet(f"{S}/out/a4_abd_capraz/s2_model_artik_p15_W120.parquet")["rz"].reindex(idx)
p4 = (r4 / 2).clip(-1, 1).fillna(0.0)
R["C4_alt"] = sub_table(r4, d.fwd1, p4, 1, label="C4 alt dönem").to_dict("records")
g1 = zscale(np.log(d.xau_p15).diff()); g5 = zscale(np.log(d.xau_p15).diff(5)); g20 = zscale(np.log(d.xau_p15).diff(20))
X = pd.concat([r4.rename("x"), g1.rename("g1"), g5.rename("g5"), g20.rename("g20"), d.fwd1.rename("y")], axis=1).dropna()
Z = X.rank(); Z = (Z - Z.mean()) / Z.std()
print("C4 sıra-kısmi (g1,g5,g20 kontrol) t:", round(nw_ols(Z.y, Z[["x", "g1", "g5", "g20"]], lags=5)["t"], 2))
print("C4 artığın altın seviye/momentum ile korelasyonu: corr(r4, g20)=", round(X[["x", "g20"]].corr().iloc[0, 1], 2), " corr(r4,g5)=", round(X[["x", "g5"]].corr().iloc[0, 1], 2))

# ================= D1
dx = zscale(np.log(d["y_DX_Y_NYB"]).diff())
rC = win(XAU, prev.values, 20, idx, 15)
gUS = win(XAU, prev.shift(1).values, 20, prev.values, 20)  # altının DXY değişimiyle eş-zamanlı ABD-günü getirisi [t-2 20 → t-1 20]
gl = zscale(np.log(d["y_GLD"]).diff())
print("D1 ana:", {k: round(v, 3) for k, v in split_stats(dx, rC, 1).items() if k != "by_year"})
print("D1 Pearson:", {k: round(v, 3) for k, v in split_stats(dx, rC, 1, method="pearson").items() if k != "by_year"})
for nm, cc in (("altın eş-zamanlı [t-2 20→t-1 20]", gUS), ("GLD Δ1", gl)):
    X = pd.concat([dx.rename("x"), zscale(cc).rename("c"), rC.rename("y")], axis=1).dropna()
    for pn, m in (("full", slice(None)), ("IS", X.index <= IS_END), ("OOS", X.index > IS_END)):
        XX = X if isinstance(m, slice) else X[m]; Z = XX.rank(); Z = (Z - Z.mean()) / Z.std()
        r = nw_ols(Z.y, Z[["x", "c"]], lags=5); r2 = nw_ols(Z.y, Z[["c", "x"]], lags=5)
        print(f"D1 sıra-kısmi | {nm} [{pn}]: DXY t={r['t']:.2f}  kontrol t={r2['t']:.2f}")
print("D1: altının kendi ABD-günü getirisi → C penceresi (öz-tersine dönüş):", {k: round(v, 3) for k, v in split_stats(zscale(gUS), rC, 1).items() if k != "by_year"})
print("D1 → fwd1, fwd3:", round(split_stats(dx, d.fwd1, 1)["t"], 2), round(split_stats(dx, d.fwd3, 3)["t"], 2))
json.dump(R, open(f"{OUT}/h3.json", "w"), indent=1, default=float)
