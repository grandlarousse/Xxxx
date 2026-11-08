"""h5: C3 kısmi t tutarsızlığı (analist Pearson −0,72; sıra-tabanlı?), D1 kayıt q değeri, C1 Pearson kısmi kontrol ayrıştırması."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a4_abd_capraz_adv")
from adv_common import *
d = load_viop(); idx = d.index
def hourly_px(sym):
    h = hourly(sym).copy(); i = pd.to_datetime(h.index)
    if i.tz is not None: i = i.tz_convert("UTC").tz_localize(None)
    return pd.Series(h["c"].values, index=i + pd.Timedelta(hours=1))
XAU = hourly_px("XAUUSD"); DXY = hourly_px("DOLLARIDXUSD")
prev = pd.Series(idx, index=idx).shift(1)
def win(px, d0, h0, d1, h1):
    return pd.Series(np.log(px.reindex(pd.DatetimeIndex(d1) + pd.Timedelta(hours=h1)).values / px.reindex(pd.DatetimeIndex(d0) + pd.Timedelta(hours=h0)).values), index=idx)
x_dxy = win(DXY, prev.values, 20, idx, 15); g_C = win(XAU, prev.values, 20, idx, 15)
b = (x_dxy.rolling(250, min_periods=150).cov(g_C) / x_dxy.rolling(250, min_periods=150).var()).shift(1)
z3 = zscale(b * x_dxy - g_C)
C = pd.DataFrame({"g1": np.log(d.xau_p15).diff(), "g5": np.log(d.xau_p15).diff(5), "spx": zscale(np.log(d.y__GSPC).diff()), "vix": zscale(np.log(d.y__VIX).diff()), "gC": zscale(g_C)}, index=idx)
y = d.fwd1
def part(x, ctrl, rank, m=None):
    D = pd.concat([x.rename("x"), C[ctrl], y.rename("y")], axis=1)
    if m is not None: D = D[m]
    D = D.dropna()
    if rank: D = D.rank()
    Z = (D - D.mean()) / D.std()
    return round(nw_ols(Z.y, Z[["x"] + ctrl], lags=5)["t"], 2)
for ctrl in (["gC"], ["g1", "g5", "spx", "vix", "gC"], ["g1", "g5"]):
    for rank in (False, True):
        print("C3 kısmi", ctrl, "sıra" if rank else "Pearson", "full", part(z3, ctrl, rank), "IS", part(z3, ctrl, rank, idx <= IS_END), "OOS", part(z3, ctrl, rank, idx > IS_END))
print("corr(z3, gC):", round(pd.concat([z3, C.gC], axis=1).corr().iloc[0, 1], 3), " sıra:", round(pd.concat([z3, C.gC], axis=1).corr("spearman").iloc[0, 1], 3))
# DXY bileşeni: z(b*x_dxy) tek başına ve gC kontrollü
zd = zscale(b * x_dxy)
print("DXY bileşeni b*x tek başına → fwd1:", {k: round(v, 3) for k, v in split_stats(zd, y, 1).items() if k != "by_year"})
r = pd.read_csv(f"{S}/out/a4_abd_capraz/kayit_fdr_birincil.csv")
print(r[r.test_id.str.contains("emilim")].sort_values("p").head(6)[["test_id", "t", "t_is", "t_oos", "q_birincil"]].to_string())
r2 = pd.read_csv(f"{S}/out/registry/a4_abd_capraz.csv")
e = r2[r2.family.str.contains("emilim")]; print("emilim testleri:", len(e), "|t|>=2:", (e.t.abs() >= 2).sum(), "beklenen ~", round(len(e) * 0.0455, 1))
print(e.loc[e.t.abs() >= 2, ["test_id", "t", "t_is", "t_oos"]].to_string())
# C1: Pearson kısmi, tek tek kontroller (analist s5 tekrar) ve IS'te 2017 hariç
x = miner_resid(d, "y_GDXJ"); y3 = d.fwd3
for nm, m in (("IS", idx <= IS_END), ("IS 2018-21", (idx >= "2018-01-01") & (idx <= IS_END)), ("OOS", idx > IS_END)):
    D = pd.concat([x.rename("x"), C[["g1", "g5", "spx", "vix", "gC"]], y3.rename("y")], axis=1)[m].dropna()
    for rank in (False, True):
        Z = D.rank() if rank else D; Z = (Z - Z.mean()) / Z.std()
        print("C1 kısmi (g1,g5,spx,vix,gC)", nm, "sıra" if rank else "Pearson", round(nw_ols(Z.y, Z[["x", "g1", "g5", "spx", "vix", "gC"]], lags=5)["t"], 2))
