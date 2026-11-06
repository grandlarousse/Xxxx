"""3) Grid medyanlari, on yil tablolari, dalga istatistikleri, onay-sonrasi devam olasiliklari."""
import os
import numpy as np
import pandas as pd
from dalga_tanim import base_data, OUT
from kurallar import perf, rs_breakout, false_starts, wave_capture

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 40)
pd.set_option("display.max_rows", 500)

R, RM, RF, m = base_data()
res = pd.read_pickle(os.path.join(OUT, "kurallar_grid.pkl"))
rot = pd.read_pickle(os.path.join(OUT, "rot_series.pkl"))
rsb = pd.read_pickle(os.path.join(OUT, "rsb_series.pkl"))
waves = pd.read_pickle(os.path.join(OUT, "waves_40_20.pkl"))

bm = {p: perf(RM.loc[p:], RF)["cagr"] for p in ("1930", "2000", "2015")}
ew = R.mean(axis=1)
bew = {p: perf(ew.loc[p:], RF)["cagr"] for p in ("1930", "2000", "2015")}
print("Piyasa CAGR", bm, "EW49", bew)

# ---- Grid medyanlari aile bazinda
cols = ["cagr", "sharpe", "maxdd", "cagr00", "sharpe00", "cagr15", "maxdd15", "hit", "capture_med", "lag_med"]
g = res.copy()
g["fam2"] = g.rule.str.extract(r"^(\w)_")[0] + g.rule.str.extract(r"_(plain|abs|mkt|buf|trail15)$")[0].fillna("")
# k=1 haric ayrica
print("\n== Aile medyanlari (tum grid) ==")
print(g.groupby("fam2")[cols].median().round(3).to_string())
gk = g[~g.rule.str.contains("_k1_")]
print("\n== Aile medyanlari (k>=3) ==")
print(gk.groupby("fam2")[cols].median().round(3).to_string())
# lookback bazinda (B plain)
B = g[g.fam2 == "Bplain"].copy()
B["L"] = B.rule.str.extract(r"_L(\d+)s")[0].astype(int)
B["skip"] = B.rule.str.extract(r"s(\d)_k")[0].astype(int)
B["k"] = B.rule.str.extract(r"_k(\d+)_")[0].astype(int)
print("\n== B plain: L x k CAGR (1930+) ==")
print(B.pivot_table(index=["L", "skip"], columns="k", values="cagr").round(3).to_string())
print("\n== B plain: L x k CAGR (2000+) ==")
print(B.pivot_table(index=["L", "skip"], columns="k", values="cagr00").round(3).to_string())
print("\n== B plain: L x k CAGR (2015+) ==")
print(B.pivot_table(index=["L", "skip"], columns="k", values="cagr15").round(3).to_string())
print("\n== B plain: L x k MaxDD (1930+) ==")
print(B.pivot_table(index=["L", "skip"], columns="k", values="maxdd").round(3).to_string())

# ---- On yil tablosu: secili kurallar, yillik bilesik getiri farki (kural - piyasa)
sel = ["B_L12s0_k3_plain", "C_L12s0_k3_abs", "B_L6s0_k5_plain", "C_L6s0_k5_abs", "B_L3s0_k5_plain", "D_L6s1_k10_buf", "C_L12s0_k5_mkt"]
ser = {k: rot[k][0] for k in sel}
for k in ["A_N12_trail15_none", "A_N6_time12_none", "A_N12_time12_none", "A_N12_ma10_none"]:
    ser[k] = rsb[k][1]
df = pd.DataFrame(ser)
df["MKT"] = RM
df["EW49"] = ew
df = df.loc["1930":]
dec = (df.index.year // 10) * 10
def ann(x):
    return (1 + x).prod() ** (12 / len(x)) - 1
T = df.groupby(dec).agg(ann)
for p, lab in (("2000", "2000-26"), ("2015", "2015-26"), ("2020", "2020-26")):
    T.loc[lab] = df.loc[p:].apply(ann)
ex = T.sub(T["MKT"], axis=0).drop(columns=["MKT"])
print("\n== On yillik yillik bilesik getiri (mutlak) ==")
print((T * 100).round(1).to_string())
print("\n== Piyasaya gore fark (yillik puan) ==")
print((ex * 100).round(1).to_string())
# yillik kazanma orani 1930-2025 (takvim yili)
yr = df.groupby(df.index.year).agg(lambda x: (1 + x).prod() - 1)
yr = yr.loc[:2025]
print("\nTakvim yili piyasayi gecme orani (1930-2025):")
print((yr.drop(columns="MKT").gt(yr["MKT"], axis=0)).mean().round(2).to_string())
print("2000-2025:")
print((yr.loc[2000:].drop(columns="MKT").gt(yr.loc[2000:, "MKT"], axis=0)).mean().round(2).to_string())
print("\nSon yillar (takvim yili getirisi %):")
print((yr.loc[2018:] * 100).round(1).to_string())
ytd = df.loc["2026"].apply(lambda x: (1 + x).prod() - 1)
print("2026 Oca-Eyl:", (ytd * 100).round(1).to_string())
# drawdown listesi
for k in ["B_L12s0_k3_plain", "C_L12s0_k3_abs", "A_N12_trail15_none"]:
    w = (1 + df[k]).cumprod()
    dd = w / w.cummax() - 1
    print(k, "en kotu DD 2000+:", round(dd.loc["2000":].min(), 3), dd.loc["2000":].idxmin(), " 2015+:", round((w.loc["2015":] / w.loc["2015":].cummax() - 1).min(), 3))

# ---- Dalga istatistikleri
waves["dec"] = (waves.start.apply(lambda p: p.year) // 10) * 10
nind = R.notna().groupby((R.index.year // 10) * 10).sum().sum(axis=1) / 12  # sektor-yil
wd = waves.groupby("dec").agg(n=("ind", "size"), rs_med=("rs_gain", "median"), abs_med=("abs_gain", "median"),
                               mo_med=("months", "median"), post12_rs=("rs_post12", "median"),
                               post24_rs=("rs_post24", "median"), gb24=("giveback24", "median"))
wd["per100_ind_yr"] = wd["n"] / nind.reindex(wd.index) * 100
print("\n== Dalga istatistikleri (RS>=+40%/<=12ay, zigzag 20%) ==")
print(wd.round(3).to_string())
print("Tum:", len(waves), "medyan RS", waves.rs_gain.median(), "medyan ay", waves.months.median(),
      "medyan abs", waves.abs_gain.median(), "post12 RS medyan", waves.rs_post12.median(),
      "post12 RS<0 orani", (waves.rs_post12 < 0).mean(), "giveback24>50% orani", (waves.giveback24 > 0.5).mean())
w50 = pd.read_pickle(os.path.join(OUT, "waves_50_20.pkl"))
print("Esik 50%:", len(w50), "medyan RS", w50.rs_gain.median(), "medyan ay", w50.months.median())

# ---- Onay sonrasi devam: RS 6 ayda >= +X (ilk gecis), ileri RS getirileri
lrel = np.log1p(R).sub(np.log1p(RM), axis=0)
X = lrel.cumsum()
rows = []
for thr in (0.15, 0.25, 0.40):
    for lb in (3, 6, 12):
        s = X - X.shift(lb)
        hit = s >= np.log(1 + thr)
        first = hit & ~hit.shift(1, fill_value=False)
        for h in (1, 3, 6, 12):
            fwd = X.shift(-h) - X
            v = fwd.where(first).stack().dropna()
            v = v[v.index.get_level_values(0) >= pd.Period("1930-01", "M")]
            v00 = v[v.index.get_level_values(0) >= pd.Period("2000-01", "M")]
            rows.append(dict(thr=thr, lb=lb, h=h, n=len(v), mean=np.expm1(v).mean(), med=np.expm1(v).median(),
                             pos=(v > 0).mean(), n00=len(v00), mean00=np.expm1(v00).mean(), pos00=(v00 > 0).mean()))
cont = pd.DataFrame(rows)
print("\n== Onay sonrasi ileri RS (piyasaya gore) getirisi ==")
print(cont.round(3).to_string())
# karsilastirma: kosulsuz
for h in (1, 3, 6, 12):
    fwd = (X.shift(-h) - X).loc["1930":].stack().dropna()
    print("kosulsuz h=", h, "ort", round(np.expm1(fwd).mean(), 4), "pos", round((fwd > 0).mean(), 3))

# ---- A ailesi islem istatistikleri donem bazinda (temsilci kurallar)
for k in ["A_N12_trail15_none", "A_N6_time12_none", "A_N12_ma10_none", "A_N6_trail10_none"]:
    tr = rsb[k][0].copy()
    tr["per"] = pd.cut(tr.entry.apply(lambda p: p.year), [1900, 1969, 1999, 2014, 2030], labels=["-1969", "1970-99", "2000-14", "2015-26"])
    fs = false_starts(tr, waves, R)
    tr["fs"] = fs
    print("\n", k)
    print(tr.groupby("per", observed=True).agg(n=("ind", "size"), ay=("months", "mean"), kazanc_orani=("rel_net", lambda x: (x > 0).mean()),
                                ort_rel=("rel_net", "mean"), med_rel=("rel_net", "median"), ort_abs=("abs_net", "mean"),
                                yanlis_bas=("fs", "mean")).round(3).to_string())
    # en iyi %10 islemin toplam kazanca katkisi
    lr = np.log1p(tr.rel_net)
    srt = lr.sort_values(ascending=False)
    print("  en iyi %10 islem toplam log-rel katkisi:", round(srt.iloc[:len(srt) // 10].sum() / lr.sum(), 2), "toplam log", round(lr.sum(), 2))
