"""GÖREV 4 (Asya) + GÖREV 6 (hafta sonu BTC) — kısa sürüm.
Asya: HSI 07:30->kapanış(~08:10) (BIST açılışından SONRAKİ kısım; h1 06:30 barı kapanışı -> 07:30 barı kapanışı), HSI/N225/KS11/Şanghay gün getirisi,
CNH=X 07:00->08:30 -> BIST 08:30->kapanış ('rest'). Ayrıca N225/KS11 gün getirisi -> BIST gap (lag0 zaten önde).
Hafta sonu: BTC Cuma 15:00 -> Pazartesi 07:00 (h1, 2024-11+) ve günlük uzun örneklem (Cuma 24:00 -> Pazar 24:00 UTC, 2015+) -> Pazartesi gap / gün-içi."""
import numpy as np, pandas as pd, g_common as g
BI = pd.read_pickle(g.RES + "/t1_BI.pkl"); X = pd.read_parquet(g.RES + "/t1_X_night.parquet")
days = X.index; D = g.bist_days().reindex(days)
prevday = pd.DatetimeIndex(D["prev"].values)
def lr(a, b): return pd.Series(np.log(b / a), index=days)
S = pd.DataFrame(index=days)
S["HSI_late"] = lr(g.snap_at("^HSI", g.utc(days, "07:30"), max_age_h=0.6).values, g.snap_at("^HSI", g.utc(days, "08:30"), max_age_h=0.6).values)
S["HSI_day"] = lr(g.snap_at("^HSI", g.utc(prevday, "08:30"), max_age_h=80).values, g.snap_at("^HSI", g.utc(days, "08:30"), max_age_h=0.6).values)
S["HSI_to0730"] = lr(g.snap_at("^HSI", g.utc(prevday, "08:30"), max_age_h=80).values, g.snap_at("^HSI", g.utc(days, "07:30"), max_age_h=0.6).values)
for s, t in [("^N225", "06:35"), ("^KS11", "06:35"), ("000001.SS", "07:05")]:
    S[s + "_day"] = lr(g.snap_at(s, g.utc(prevday, t), max_age_h=80).values, g.snap_at(s, g.utc(days, t), max_age_h=1.2).values)
S["CNH_0700_0830"] = lr(g.snap_at("CNH=X", g.utc(days, "07:00"), max_age_h=1.5).values, g.snap_at("CNH=X", g.utc(days, "08:30"), max_age_h=1.5).values)
S["ES_0700_0830"] = lr(g.snap_at("ES=F", g.utc(days, "07:00"), max_age_h=1.5).values, g.snap_at("ES=F", g.utc(days, "08:30"), max_age_h=1.5).values)
for c in S: S.loc[S[c].abs() > 8 * S[c].std(), c] = np.nan
SPLIT = pd.Timestamp("2025-07-01"); rows = []
tests = [("HSI_late", "rest"), ("HSI_late", "r1"), ("HSI_day", "rest"), ("HSI_to0730", "rest"), ("^N225_day", "gap"), ("^N225_day", "intra"),
         ("^KS11_day", "gap"), ("^KS11_day", "intra"), ("000001.SS_day", "gap"), ("000001.SS_day", "intra"), ("CNH_0700_0830", "rest"), ("ES_0700_0830", "rest"), ("ES_0700_0830", "r1")]
for st, B in BI.items():
    for sig, tgt in tests:
        c, t, n = g.corr_t(B[tgt], S[sig])
        pc, _ = g.ll.partial_corr(B[tgt], S[sig], [S["ES_0700_0830"]]) if tgt == "rest" and sig != "ES_0700_0830" else (np.nan, 0)
        df = pd.concat([np.sign(S[sig]).rename("p"), B[tgt].rename("y")], axis=1).dropna(); pnl = df.p * df.y
        o = pnl[df.index >= SPLIT]; i_ = pnl[df.index < SPLIT]
        rows.append(dict(stock=st, signal=sig, target=tgt, corr=c, t=t, n=n, pc_given_ES0830=pc, bt_IS_bps=1e4 * i_.mean(), bt_OOS_bps=1e4 * o.mean(),
                         bt_OOS_t=g.ll.nw_t(o)[1], c_IS=pd.concat([B[tgt], S[sig]], axis=1).dropna().loc[:SPLIT].corr().iloc[0, 1],
                         c_OOS=pd.concat([B[tgt], S[sig]], axis=1).dropna().loc[SPLIT:].corr().iloc[0, 1]))
A = pd.DataFrame(rows); A.to_csv(g.RES + "/t4_asia.csv", index=False)
# ---- hafta sonu BTC ----
RET = ["ASTOR", "SASA", "HEKTS", "ODAS", "TRALT", "PETKM"]
mon = D.index[D["monday_after_fri"].fillna(False).astype(bool)]
rows = []
bd = g.ll.raw("BTC-USD"); bts = pd.Series(bd["c"].values, index=pd.DatetimeIndex(bd["ldate"].values)); bts = bts[~bts.index.duplicated(keep="last")]
for st in g.IDX + g.VIOP:
    if st not in BI: continue
    B = BI[st]
    # h1 kısa örneklem
    wk = pd.concat([X["BTC-USD"].rename("x"), B[["gap", "intra", "rest"]]], axis=1).loc[mon].dropna()
    wd = pd.concat([X["BTC-USD"].rename("x"), B[["gap", "intra"]]], axis=1).drop(index=mon, errors="ignore").dropna()
    # günlük uzun örneklem: Pazartesi gap vs BTC (Cuma kapanış 24:00 -> Pazar 24:00)
    dd = g.ll.decomp(st); dd = dd[dd.index >= "2015-01-01"]
    mons = dd.index[dd.index.dayofweek == 0]
    fri = mons - pd.Timedelta(days=3); sun = mons - pd.Timedelta(days=1)
    xb = pd.Series(np.log(bts.reindex(sun).values / bts.reindex(fri).values), index=mons)
    L = pd.concat([xb.rename("x"), dd.loc[mons, ["gap", "intra"]]], axis=1).dropna()
    Lr = L[L.index >= "2021-01-01"]
    def cc(df, a): return df["x"].corr(df[a]) if len(df) > 30 else np.nan
    rows.append(dict(stock=st, retail=st in RET, n_h1_wkend=len(wk), c_gap_wkend_h1=cc(wk, "gap"), c_intra_wkend_h1=cc(wk, "intra"), c_gap_weekday_h1=cc(wd, "gap"),
                     t_gap_wkend_h1=g.corr_t(wk["gap"], wk["x"])[1] if len(wk) > 40 else np.nan,
                     n_long=len(L), c_gap_long=cc(L, "gap"), t_gap_long=g.corr_t(L["gap"], L["x"])[1], c_intra_long=cc(L, "intra"), t_intra_long=g.corr_t(L["intra"], L["x"])[1],
                     c_gap_2021p=cc(Lr, "gap"), c_gap_pre2021=cc(L[L.index < "2021-01-01"], "gap"),
                     bt_intra_long_bps=1e4 * (np.sign(L["x"]) * L["intra"]).mean(), beta_gap_long=np.polyfit(L["x"], L["gap"], 1)[0] if len(L) > 30 else np.nan))
H = pd.DataFrame(rows); H.to_csv(g.RES + "/t6_weekend.csv", index=False)
pd.set_option("display.width", 250)
a = A[A.stock.isin(["XU030", "XBANK"])][["stock", "signal", "target", "corr", "t", "n", "pc_given_ES0830", "c_IS", "c_OOS", "bt_OOS_bps", "bt_OOS_t"]].round(3)
print(a.to_string(index=False))
s = A[A.stock.isin(g.VIOP)]; print(s.groupby(["signal", "target"])[["corr", "t", "c_IS", "c_OOS", "bt_OOS_bps"]].median().round(3).to_string())
print(s.assign(sig=s.t.abs() > 2).groupby(["signal", "target"])["sig"].mean().round(2).to_dict())
print(H[H.retail | H.stock.isin(["XU030", "XU100"])].round(3).to_string(index=False))
print("all47 median", H[H.stock.isin(g.VIOP)][["c_gap_wkend_h1", "c_gap_weekday_h1", "c_gap_long", "c_intra_long", "c_gap_2021p", "c_gap_pre2021"]].median().round(3).to_dict())
