"""Adim 5: yillara gore kirilim + maliyet duyarliligi + karistirma (permutasyon) null'u, tum adaylar icin."""
import sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_C4C5_a")
import vlib as V, numpy as np, pandas as pd
from s02_hk_timing import signals, C, TR
pd.set_option("display.width", 250)
OUT = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_C4C5_a/"
KR = V.bist_daily("KRDMD.IS")
def shfe_cum(code):
    m = V.shfe_main(code); lp = m["r_cc"].fillna(0).cumsum(); lv, _ = V.on_cal(lp, C); r = lv.diff()
    r[r.index.isin(m.index[m["r_cc"].isna()])] = np.nan; return r
S1 = signals("1787.HK"); S2 = signals("2899.HK"); S3 = signals("600547.SS"); S4 = signals("601899.SS")
HC = V.shfe_main("HC"); HC = HC[HC.index.isin(C)]
cands = {
 "1787.HK CLOSE -> TRALT [orijinal, ileriye bakma]": (S1["CLOSE"], TR["intra"], "2018-10-01"),
 "1787.HK OPEN(01:30UTC) -> TRALT": (S1["OPEN"], TR["intra"], "2018-10-01"),
 "1787.HK CLOSE_{t-1} -> TRALT": (S1["CLOSE"].shift(1), TR["intra"], "2018-10-01"),
 "2899.HK CLOSE -> TRALT [ileriye bakma]": (S2["CLOSE"], TR["intra"], "2014-01-01"),
 "600547.SS CLOSE(07:00UTC) -> TRALT": (S3["CLOSE"], TR["intra"], "2014-01-01"),
 "600547.SS OPEN(01:30UTC) -> TRALT": (S3["OPEN"], TR["intra"], "2014-01-01"),
 "601899.SS CLOSE(07:00UTC) -> TRALT": (S4["CLOSE"], TR["intra"], "2014-01-01"),
 "SHFE HC kumulatif [orijinal] -> KRDMD": (shfe_cum("HC"), KR["intra"], "2018-11-28"),
 "SHFE HC taze (yalniz t) -> KRDMD": (HC["r_cc"], KR["intra"], "2018-11-28"),
 "SHFE HC GAPD(07->13UTC t-1) -> KRDMD": (HC["r_gap"], KR["intra"], "2018-11-28"),
 "SHFE HC OCD(13UTC t-1->07UTC t) -> KRDMD": (HC["r_oc"], KR["intra"], "2018-11-28"),
}
rng = np.random.default_rng(7)
rows, yrs = [], {}
for lab, (s, y, st) in cands.items():
    df = pd.concat([s.rename("s"), y.rename("y")], axis=1).dropna(); df = df[df.index >= st]
    c, t, n = V.zt(df.y, df.s)
    rr = {"aday": lab, "n": n, "corr": c, "t": t}
    for cost in [0, 4, 8, 10, 15]:
        r, _ = V.bt(df.s, df.y, cost)
        rr[f"net{cost}_ALL"] = r["ALL"].get("mean_bps"); rr[f"sh{cost}_IS"] = r["IS"].get("sharpe"); rr[f"sh{cost}_OOS"] = r["OOS"].get("sharpe")
        if cost == 10: yrs[lab] = r["yr"]; rr["net10_IS"] = r["IS"].get("mean_bps"); rr["net10_OOS"] = r["OOS"].get("mean_bps"); rr["bt_t_ALL"] = r["ALL"].get("t")
    # yillik korelasyon isaret istikrari
    yc = df.groupby(df.index.year).apply(lambda g: g.y.corr(g.s) if len(g) > 60 else np.nan).dropna()
    rr["yil_pozitif"] = f"{int((yc > 0).sum())}/{len(yc)}"
    # blok permutasyon null'u (20 gunluk bloklar karistirilir): brut ortalama getiri
    pos = np.sign(df.s.values); y_ = df.y.values; g0 = np.mean(pos * y_)
    B = 20; nb = len(df) // B; null = []
    for _ in range(1000):
        idx = np.concatenate([np.arange(b * B, b * B + B) for b in rng.permutation(nb)])
        null.append(np.mean(pos[:nb * B] * y_[idx]))
    rr["perm_p_brut"] = float((np.array(null) >= g0).mean())
    rows.append(rr)
R = pd.DataFrame(rows); R.round(3).to_csv(OUT + "s05_years_costs.csv", index=False)
print(R.round(2).to_string())
Y = pd.DataFrame(yrs).T; Y.to_csv(OUT + "s05_by_year_net10.csv"); print("\nYillara gore net (10 bps) ortalama bps/islem:"); print(Y.round(1).to_string())
