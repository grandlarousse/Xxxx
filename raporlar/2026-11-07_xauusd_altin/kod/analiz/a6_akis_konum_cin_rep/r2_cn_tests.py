import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a6_akis_konum_cin_rep")
from r0_base import *
T = viop_target(); F = pd.read_parquet(f"{OUT}/r1_features_viop.parquet")
r = T.ret
CL = [("comp", 5, "a6_cn_gold_res_comp_h5"), ("res_600547.SS", 5, "a6_res600547_h5"), ("r_HSI", 3, "a6_hsi_h3"), ("comp_sum5", 1, "a6_cn_res_sum5_h1"),
      ("comp", 3, "comp_h3"), ("comp_sum5", 3, "sum5_h3"), ("res_1818.HK", 5, "res1818_h5"), ("res_2899.HK", 5, "res2899_h5"), ("r_HSI", 1, "hsi_h1")]
rows = []
for col, h, cid in CL:
    x = F[col]; y = T[f"fwd{h}"]
    st = split(x, y, h)
    sgn = np.sign(split(x[x.index <= IS_END], y[y.index <= IS_END], h)["ic"])
    pos = (sgn * np.sign(x)).fillna(0.0)
    o5 = periods(pos, r, h, 5.0); o10 = periods(pos, r, h, 10.0); o5nn = periods(pos, r, h, 5.0, netted=False)
    chg = float((pos.diff().abs() > 0).sum() / len(pos) * 252)
    flips = float(((np.sign(x).diff().abs() > 0) & x.notna() & x.shift(1).notna()).sum() / x.notna().sum() * 252)
    # IS tercile kuralı
    q1, q2 = x[x.index <= IS_END].quantile([1/3, 2/3])
    pt = pd.Series(np.where(x > q2, sgn, np.where(x < q1, -sgn, 0.0)), index=x.index).where(x.notna(), 0.0)
    ot = periods(pt, r, h, 5.0)
    rows.append(dict(id=cid, x=col, h=h, ic=st["ic"], t=st["t"], n=st["n"], t_is=st["t_is"], t_oos=st["t_oos"], ic_is=st["ic_is"], ic_oos=st["ic_oos"], yrs=st["yrs"], is_sign=sgn,
                     sh_full=o5["full"]["LS"], sh_is=o5["is"]["LS"], sh_oos=o5["oos"]["LS"], sh_oos_dm=o5["oos"]["LS_dm"], sh_oos_10=o10["oos"]["LS"], sh_oos_nonnet=o5nn["oos"]["LS"],
                     long_oos=o5["oos"]["long"], long_oos_dm=o5["oos"]["long_dm"], short_oos=o5["oos"]["short"], short_oos_dm=o5["oos"]["short_dm"], bh_oos=o5["oos"]["bh"], bh_is=o5["is"]["bh"],
                     terc_oos=ot["oos"]["LS"], terc_is=ot["is"]["LS"], chg_per_yr=chg, flips_per_yr_valid=flips, by_year=st["by_year"]))
df = pd.DataFrame(rows)
pd.set_option("display.width", 300); pd.set_option("display.max_columns", 40)
print(df.drop(columns=["by_year"]).round(3).to_string(index=False))
for _, rw in df.iterrows(): print(rw.id, rw.by_year)
df.to_csv(f"{OUT}/r2_cn_tests.csv", index=False)
