"""GPR z250 iddiası. Ham dosya data/misc/gpr_daily.xls (DAY=YYYYMMDD, GPRD). Gün t'de kullanılabilir son D: D <= t - lag takvim günü.
Analist: lag=2 (D+1 23:00 UTC varsayımı). Sağlamlık: lag 7, 10 (haftalık güncelleme olasılığı)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a6_akis_konum_cin_rep")
from r0_base import *
T = viop_target(); days = T.index; r = T.ret
g = pd.read_excel(f"{S}/data/misc/gpr_daily.xls")
g = g[pd.to_numeric(g.DAY, errors="coerce").notna()]
g["d"] = pd.to_datetime(g.DAY.astype(int).astype(str), format="%Y%m%d"); g = g.set_index("d").sort_index()
gp = g["GPRD"].astype(float)
print("GPR son tarih:", gp.index.max().date(), "son değer", round(gp.iloc[-1], 6), "| panel sabiti 97.667847 = son değer mi?", np.isclose(gp.iloc[-1], 97.667847))
Dp = pd.read_parquet(f"{P}/panel_viop.parquet"); print("panel gpr_GPRD benzersiz değer sayısı:", Dp.gpr_GPRD.nunique())

def asof(days_, lag):
    i = gp.index.searchsorted(days_ - pd.Timedelta(days=lag), side="right") - 1
    return pd.Series(np.where(i >= 0, gp.values[np.clip(i, 0, None)], np.nan), index=days_)

def z250(s, w=250, minp=200):
    m = s.rolling(w, min_periods=minp).mean(); sd = s.rolling(w, min_periods=minp).std()
    return (s - m) / sd

out = []
for lag in (2, 7, 10):
    lg = np.log(asof(days, lag).clip(lower=1)); z = z250(lg)
    for h in (3, 5):
        st = split(z, T[f"fwd{h}"], h)
        sgn = np.sign(split(z[z.index <= IS_END], T[f"fwd{h}"][T.index <= IS_END], h)["ic"])
        pos = (sgn * np.sign(z)).fillna(0.0); o = periods(pos, r, h, 5.0); o10 = periods(pos, r, h, 10.0)
        chg = (pos.diff().abs() > 0).sum() / len(pos) * 252
        out.append(dict(lag=lag, h=h, ic=st["ic"], t=st["t"], t_is=st["t_is"], t_oos=st["t_oos"], yrs=st["yrs"], n=st["n"], is_sign=sgn, sh_is=o["is"]["LS"], sh_oos=o["oos"]["LS"], sh_oos_dm=o["oos"]["LS_dm"],
                        sh_oos10=o10["oos"]["LS"], long_oos=o["oos"]["long"], long_oos_dm=o["oos"]["long_dm"], short_oos=o["oos"]["short"], short_oos_dm=o["oos"]["short_dm"], bh_oos=o["oos"]["bh"], chg=chg,
                        by_year=st["by_year"]))
    if lag == 2:
        zz = z
# kontrollü: spot r1, r5, 07-15, VİOP r_{t-1}
G15 = pd.Series(gold_at(days + pd.Timedelta(hours=15)), index=days); G07 = pd.Series(gold_at(days + pd.Timedelta(hours=7)), index=days)
C = pd.DataFrame({"s_r1": np.log(G15 / G15.shift(1)), "s_r5": np.log(G15 / G15.shift(5)), "s_0715": np.log(G15 / G07), "v_r1": r.shift(1)})
xz = (zz - zz.mean()) / zz.std(); d = pd.concat([T.fwd5.rename("y"), xz.rename("x"), C], axis=1).dropna()
b, t, n = nw_t(d.y.values, np.column_stack([np.ones(len(d)), d.drop(columns="y").values]), 5); print("GPR z250 h5 kontrollü t:", round(t[1], 2))
# 2010-2016 erken: spot takvim
bd = pd.bdate_range("2008-06-01", "2017-01-31"); p15 = pd.Series(gold_at(bd + pd.Timedelta(hours=15), 1.0), index=bd).dropna(); sr = np.log(p15).diff()
ze = z250(np.log(asof(p15.index, 2).clip(lower=1))); y5 = sum(sr.shift(-j) for j in range(1, 6))
m = (p15.index >= "2010-01-01") & (p15.index <= "2016-12-31"); e = ic_t(ze[m], y5[m], 5); print("erken 2010-2016 GPR z250 h5: IC", round(e["ic"], 3), "t", round(e["t"], 2))
df = pd.DataFrame(out); pd.set_option("display.width", 300); print(df.drop(columns="by_year").round(3).to_string(index=False))
print(df[(df.lag == 2) & (df.h == 5)].by_year.iloc[0])
df.to_csv(f"{OUT}/r7_gpr.csv", index=False)
