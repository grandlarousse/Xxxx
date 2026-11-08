"""Rapor için markdown tabloları üretir (CSV çıktılarından) -> tables.md"""
from a2_common import *
def md(df, idx=True):
    d = df.reset_index() if idx else df
    cols = [str(c) for c in d.columns]
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, r in d.iterrows():
        out.append("| " + " | ".join("" if (isinstance(x, float) and np.isnan(x)) else str(x) for x in r.values) + " |")
    return "\n".join(out)
T = []
A = pd.read_csv(f"{OUT}/a_segments_ic.csv")
T.append("### A: segment IC tablosu\n" + md(A[["predictor", "h", "n", "ic", "t", "t_is", "t_oos", "yrs", "ic_1016", "t_1016", "yrs_1016"]], False))
T.append("### B1: segment ort. yıl yıl (bps/gün)\n" + md(pd.read_csv(f"{OUT}/b_segment_mean_by_year_bps.csv").set_index("date"), True))
T.append("### B2: segment testleri\n" + md(pd.read_csv(f"{OUT}/b_segment_tests.csv"), False))
T.append("### B3: saatlik\n" + md(pd.read_csv(f"{OUT}/b_hourly_mean_bps.csv", index_col=0), True))
alt = pd.read_csv(f"{OUT}/b_alt_entry.csv")
T.append("### B4: alternatif giriş Sharpe\n" + md(alt.pivot_table(index=["strat", "cost"], columns="per", values="sharpe"), True))
T.append("### B5: alt yıl yıl\n" + md(pd.read_csv(f"{OUT}/b_alt_by_year_net5.csv").set_index("date"), True))
T.append("### C: baz\n" + md(pd.read_csv(f"{OUT}/c_basis_ic.csv")[["predictor", "h", "n", "ic", "t", "t_is", "t_oos", "yrs"]], False))
T.append("### C2: rv\n" + md(pd.read_csv(f"{OUT}/c_relative_value_bt.csv"), False))
T.append("### D\n" + md(pd.read_csv(f"{OUT}/d_fix_ic.csv")[["predictor", "h", "n", "ic", "t", "t_is", "t_oos", "yrs"]], False))
T.append("### D2\n" + md(pd.read_csv(f"{OUT}/d_fix_hour_means_by_year_bps.csv").set_index("date"), True))
T.append("### E\n" + md(pd.read_csv(f"{OUT}/e_weekend_ic.csv")[["predictor", "h", "n", "ic", "t", "t_is", "t_oos", "yrs"]], False))
T.append("### E2\n" + md(pd.read_csv(f"{OUT}/e_dow.csv"), False))
T.append("### F\n" + md(pd.read_csv(f"{OUT}/f_micro_ic.csv")[["predictor", "h", "n", "ic", "t", "t_is", "t_oos", "yrs"]], False))
T.append("### F2\n" + md(pd.read_csv(f"{OUT}/f_viop_native_night_day.csv").set_index("date"), True))
r = pd.read_csv(f"{REG_DIR}/{AGENT}.csv"); r["q_bh"] = bh_fdr(r.p.fillna(1).values)
r.to_csv(f"{OUT}/registry_with_q.csv", index=False)
T.append("### R: kayıt (p<0.05)\n" + md(r[r.p < 0.05].sort_values("p")[["family", "test_id", "h", "ic", "t", "t_is", "t_oos", "yrs_same_sign", "yrs", "p", "q_bh"]].round(4), False))
open(f"{OUT}/tables.md", "w").write("\n\n".join(T))
print("ok", len(r))
