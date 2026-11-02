"""5 dk (son ~60 gün): gap'in geri dönüşü ne kadar hızlı? Saf müzayede gürültüsü ilk dakikalarda düzelir; aşırı tepki/likidite primi yavaş."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_K1_b")
from kb import *
P = pd.read_parquet(OUT + "/panel_b.parquet"); P = P[P.date >= "2026-07-01"]
fr = []
for s in VIOP:
    m = m5(s)
    if m is None: continue
    piv = m.pivot_table(index="day", columns="hm", values="c", aggfunc="last")
    opn = m[m.hm == 655].set_index("day").o
    df = pd.DataFrame({"auc": opn})
    for hm, lab in [(700, "p1005"), (710, "p1015"), (725, "p1030"), (825, "p1130")]:
        df[lab] = piv.get(hm)
    df["sym"] = s; fr.append(df.reset_index().rename(columns={"day": "date"}))
M = pd.concat(fr).merge(P[["date", "sym", "gap", "intra", "o", "c", "liqT"]], on=["date", "sym"], how="inner")
M = M[(M.auc / M.o - 1).abs() < 0.002]
print("m5 örneklem:", M.date.min().date(), M.date.max().date(), len(M), "hisse-gün; açılış==m5 06:55:", round(((M.auc / M.o - 1).abs() < 1e-6).mean(), 3))
segs = {"auc->10:05": np.log(M.p1005 / M.o), "10:05->10:15": np.log(M.p1015 / M.p1005), "10:15->10:30": np.log(M.p1030 / M.p1015),
        "10:30->11:30": np.log(M.p1130 / M.p1030), "11:30->kapanış": np.log(M.c / M.p1130), "auc->kapanış": M.intra}
rows = []
for grp in ["hepsi", "dusuk", "orta", "yuksek"]:
    sub = M if grp == "hepsi" else M[M.liqT == grp]
    for k, v in segs.items():
        v = v.loc[sub.index]
        # günlük kümelenmiş: her gün kesit eğimi -> Fama-MacBeth
        dd = pd.DataFrame({"y": v, "x": sub.gap, "d": sub.date}).dropna()
        sl = dd.groupby("d").apply(lambda z: np.polyfit(z.x, z.y, 1)[0] if len(z) > 5 and z.x.std() > 0 else np.nan).dropna()
        b, t, n = ols_nw(dd.sort_values("d").y.values, [dd.sort_values("d").x.values])
        sel = dd[dd.x.abs() > 0.01]; fadeg = (-np.sign(sel.x) * sel.y * 1e4)
        rows.append(dict(grp=grp, seg=k, b_pool=round(b[1], 4), t_pool=round(t[1], 2), fm_slope=round(sl.mean(), 4), fm_t=round(sl.mean() / sl.std() * np.sqrt(len(sl)), 2),
                         fade_gross_bps=round(fadeg.mean(), 1), n_fade=len(fadeg)))
R = pd.DataFrame(rows); print(R.to_string()); R.to_csv(OUT + "/res_b7_m5.csv", index=False)
