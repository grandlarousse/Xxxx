"""Saatlik (İş h1, 2017+) XU030(ex) -> hisse gecikmeli tepki (Σβ1..3) yıllara göre + XU030 -> XTUMY/XYUZO yıllık."""
import sys; sys.argv = ["x", "isy", "h1"]
import s4_intraday as S4
from ye_common import *
x = S4.bar_ret(S4.px("XU030")); rows = []
for s in VIOP:
    p = S4.px(s)
    if p is None: continue
    S_ = S4.bar_ret(p)
    df = pd.concat([x["r"].rename("i"), S_["r"].rename("s"), x["date"]], axis=1, join="inner")
    w = weight_series("XU030", s, pd.DatetimeIndex(df["date"].unique())).reindex(df["date"]).values
    XE = pd.DataFrame({"r": np.log1p((np.expm1(df["i"]) - w * np.expm1(df["s"]).fillna(0)) / (1 - w)).values, "date": df["date"].values}, index=df.index)
    for y in range(2017, 2027):
        o = S4.leadlag(S_, XE, (pd.Timestamp(f"{y}-01-01"), pd.Timestamp(f"{y}-12-31")))
        rows.append({"stock": s, "year": y, "b0": o["b0"], "b1": o["b1"], "sum_lag": o["sum_lag"], "t_sum": o["t_sum_lag"], "lag_share": o["lag_share"], "n": o["n"]})
    print(s, flush=True)
Y = pd.DataFrame(rows); Y.to_csv(RES + "/intraday_h1_years.csv", index=False)
pd.set_option("display.width", 250)
print(Y.pivot_table(index="year", values=["b0", "b1", "sum_lag", "lag_share", "t_sum"], aggfunc="median").round(3))
print(Y.groupby("stock").apply(lambda g: pd.Series({"frac_yrs_pos": (g.sum_lag > 0).mean(), "med_share": g.lag_share.median()})).sort_values("med_share").round(2).T.to_string())
rr = []
for a, b in [("XU030", "XTUMY"), ("XU030", "XYUZO"), ("XBANK", "XUSIN"), ("XUSIN", "XBANK"), ("XU030", "XHOLD")]:
    for y in range(2017, 2027):
        o = S4.leadlag(S4.bar_ret(S4.px(b)), S4.bar_ret(S4.px(a)), (pd.Timestamp(f"{y}-01-01"), pd.Timestamp(f"{y}-12-31")))
        rr.append({"pair": f"{a}->{b}", "year": y, "b0": o["b0"], "b1": o["b1"], "t1": o["t1"], "sum_lag": o["sum_lag"], "t_sum": o["t_sum_lag"], "lag_share": o["lag_share"]})
RR = pd.DataFrame(rr); RR.to_csv(RES + "/intraday_h1_idx_years.csv", index=False)
print(RR.pivot_table(index="year", columns="pair", values="lag_share").round(3).to_string()); print(RR.pivot_table(index="year", columns="pair", values="t_sum").round(2).to_string())
