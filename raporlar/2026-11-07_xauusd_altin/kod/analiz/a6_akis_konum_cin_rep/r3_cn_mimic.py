"""Fark teşhisi: analistin inşasını (VİOP takviminde 'bilinen kapanış' farkı, VİOP günlerinde kayan OLS) kendi kodumla taklit et."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a6_akis_konum_cin_rep")
from r0_base import *
from r1_cn import yh, rolling_resid, STK, GOLD_SNAP
T = viop_target(); days = T.index; r = T.ret

def asof_close(tk):
    y = yh(tk); i = y.index.searchsorted(days, side="right") - 1
    c = pd.Series(np.where(i >= 0, y.adjclose.values[np.clip(i, 0, None)], np.nan), index=days)
    dt = pd.Series(np.where(i >= 0, y.index.values[np.clip(i, 0, None)], np.datetime64("NaT")), index=days)
    return c, dt

def mimic_resid(tk, win=250, minn=150):
    c, dt = asof_close(tk); cm, dtm = asof_close(STK[tk])
    rs = np.log(c).diff(); rs[dt == dt.shift(1)] = np.nan
    rm = np.log(cm).diff(); rm[dtm == dtm.shift(1)] = np.nan
    hh, mm = GOLD_SNAP[tk]
    g = pd.Series(gold_at(pd.DatetimeIndex(dt) + pd.Timedelta(hours=hh, minutes=mm), max_stale_h=3), index=days)
    rg = np.log(g / g.shift(1)); rg[dt == dt.shift(1)] = np.nan
    d = pd.concat([rs.rename("y"), rg.rename("g"), rm.rename("m")], axis=1).dropna()
    X = np.column_stack([np.ones(len(d)), d.g.values, d.m.values])
    return pd.Series(rolling_resid(d.y.values, X, win, minn), index=d.index).reindex(days)

M = pd.DataFrame({f"res_{tk}": mimic_resid(tk) for tk in STK})
M["comp"] = M.mean(axis=1).where(M.notna().sum(axis=1) >= 2)
M["comp_sum5"] = M["comp"].rolling(5, min_periods=3).sum()
M.to_parquet(f"{OUT}/r3_mimic_features.parquet")
F = pd.read_parquet(f"{OUT}/r1_features_viop.parquet")
A = pd.read_csv(f"{S}/out/a6_akis_konum_cin/c_asia_features.csv", index_col=0, parse_dates=True)   # yalnız karşılaştırma için okunur
amap = {"comp": "cn_gold_res_comp", "res_600547.SS": "res600547_SS", "res_1818.HK": "res1818_HK", "res_2899.HK": "res2899_HK"}
for k, a in amap.items():
    print(k, "ilk geçerli: mine", F[k].first_valid_index().date(), "mimic", M[k].first_valid_index().date(), "analist", A[a].first_valid_index().date(),
          "| corr mine~analist", round(F[k].corr(A[a].reindex(days)), 3), "mimic~analist", round(M[k].corr(A[a].reindex(days)), 4))
pd.set_option("display.width", 250)
rows = []
for k, h in [("comp", 5), ("res_600547.SS", 5), ("comp_sum5", 1), ("comp", 3)]:
    for lab, x in [("mine", F[k]), ("mine_from_2017-10", F[k].where(F.index >= M[k].first_valid_index())), ("mimic", M[k])]:
        st = split(x, T[f"fwd{h}"], h)
        pos = np.sign(x).fillna(0.0); o = periods(pos, r, h, 5.0); o10 = periods(pos, r, h, 10.0)
        rows.append(dict(x=k, h=h, ver=lab, ic=st["ic"], t=st["t"], t_is=st["t_is"], t_oos=st["t_oos"], yrs=st["yrs"], n=st["n"], sh_is=o["is"]["LS"], sh_oos=o["oos"]["LS"], sh_oos_dm=o["oos"]["LS_dm"],
                         sh_oos10=o10["oos"]["LS"], long_oos=o["oos"]["long"], short_oos=o["oos"]["short"], chg=(pos.diff().abs() > 0).sum() / len(pos) * 252))
df = pd.DataFrame(rows); print(df.round(3).to_string(index=False)); df.to_csv(f"{OUT}/r3_mimic_compare.csv", index=False)
