"""Ek kontroller: (1) kontrolsüz lag-1 korelasyonlar (kontrollerin etkisi), (2) THYAO/XULAS_{t-1} -> piyasa (B testinde öne çıkan küme), (3) backtest."""
from ye_common import *
x30 = idx_ret("XU030"); x100 = idx_ret("XU100")
y = ll.raw("XU030.IS"); y.index = pd.DatetimeIndex(y["ldate"]); y = y[~y.index.duplicated(keep="last")]
o = y["o"].reindex(x30.index); c_ = idx_px("XU030"); intra30 = np.log(c_ / o); bad = (o <= 0) | (np.abs(np.log(o / c_.shift(1))) < 1e-7); intra30[bad] = np.nan; gap30 = x30 - intra30
rows = []
for s in VIOP:
    d = stk_dec(s); cc = stk_ret(s)
    df = frame({"cc": cc, "gap": d["gap"], "intra": d["intra"], "x": x30.shift(1), "own": cc.shift(1)}).dropna()
    rows.append({"stock": s, "corr_cc_XU030lag1": df.cc.corr(df.x), "corr_gap_XU030lag1": df.gap.corr(df.x), "corr_intra_XU030lag1": df.intra.corr(df.x),
                 "own_ac1": df.cc.corr(df.own), "corr_intra_ownlag1": df.intra.corr(df.own), "corr_gap_ownlag1": df.gap.corr(df.own)})
U = pd.DataFrame(rows).set_index("stock"); U.to_csv(RES + "/uncontrolled_lag1.csv"); print(U.describe().round(3).to_string())
# THYAO -> piyasa
PER = {"full": (START, END), "IS": (START, SPLIT - pd.Timedelta(days=1)), "OOS": (SPLIT, END)}
def reg(yv, xv, ctr, a, b):
    df = pd.concat([yv.rename("y"), xv.rename("x")] + [c.rename(f"c{i}") for i, c in enumerate(ctr)], axis=1); df = df[(df.index >= a) & (df.index <= b)].dropna()
    if len(df) < 60: return np.nan, np.nan, len(df)
    Z = (df - df.mean()) / df.std(); bb, tt, n, _ = ols_nw(Z["y"].values, Z.drop(columns="y").values); return bb[1], tt[1], n
out = []
for lead in ["THYAO", "PGSUS", "XULAS", "GARAN", "AKBNK", "ASELS", "TUPRS", "KCHOL", "BIMAS"]:
    xl = (idx_ret(lead) if lead.startswith("X") else stk_ret(lead)).shift(1)
    for tn, tg in [("XU030_cc", x30), ("XU030_gap", gap30), ("XU030_intra", intra30), ("XU100_cc", x100)]:
        r = {"leader": lead, "target": tn}
        for pn, (a, b) in PER.items():
            bb, tt, n = reg(tg, xl, [x30.shift(1)], a, b); r[f"b_{pn}"] = bb; r[f"t_{pn}"] = tt; r[f"n_{pn}"] = n
        yrs = [reg(tg, xl, [x30.shift(1)], pd.Timestamp(f"{yy}-01-01"), pd.Timestamp(f"{yy}-12-31"))[0] for yy in range(2014, 2027)]
        r["frac_years_pos"] = np.mean([v > 0 for v in yrs if np.isfinite(v)]); r["by_year"] = str(np.round(yrs, 2).tolist())
        out.append(r)
O = pd.DataFrame(out); O.to_csv(RES + "/leader_stocks.csv", index=False); pd.set_option("display.width", 250); print(O.drop(columns="by_year").round(3).to_string())
print(O[O.leader == "THYAO"][["target", "by_year"]].to_string())
# backtest: rölatif THYAO_{t-1} - XU030_{t-1} -> XU030 gün-içi_t (XU030 vadelisi ile işlenebilir)
sig = (stk_ret("THYAO") - x30).shift(1); sig = sig[sig.index >= START]  # 2014 öncesi Yahoo açılış verisi güvenilmez
bts = []
for c in [0, 8, 15, 4]:
    for tn, tg in [("XU030_intra", intra30), ("XU030_cc", x30)]:
        res, _ = ll.backtest(sig, tg, cost_bps=c, mode="z", thr=1.0, split=str(SPLIT.date()))
        bts.append({"bt": f"BT4_THYAO-XU030_t-1->{tn}", "cost": c, **{f"{k}_{f}": res[k].get(f) for k in ["IS", "OOS"] for f in ["n", "mean_bps", "t", "sharpe", "hit"]}, "by_year": str(res["by_year_bps"])})
B = pd.DataFrame(bts); B.to_csv(RES + "/bt_thyao_lead.csv", index=False); print(B.round(2).to_string())
