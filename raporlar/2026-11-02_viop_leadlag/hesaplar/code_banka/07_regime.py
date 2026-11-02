"""USDTRY rejimleri + 2026 küresel faktör kayması + Brent sağlamlık."""
import bk, numpy as np, pandas as pd, statsmodels.api as sm
X = bk.R("XBANK"); M = bk.xu(); T = bk.R("TRY=X")
out = []
# rejim: TRY 60g realize vol, geçmiş 2y medyanına göre (sadece geçmiş bilgi)
v = T.rolling(60).std(); vm = v.rolling(500, min_periods=250).median().shift(1)
reg = pd.Series(np.where(v > 1.5 * vm, "şok(yüksek vol)", "sakin/carry"), index=T.index); reg[vm.isna()] = np.nan
periods = {"2014-2017": ("2014", "2018"), "2018-08 kriz y.": ("2018-05", "2019-01"), "2019-2020": ("2019", "2021"), "2021 Q4 şok": ("2021-09", "2022-01"),
           "2022-2023H1 (KKM/heterodoks)": ("2022-01", "2023-06"), "2023-06..2025-03 carry": ("2023-06-22", "2025-03-19"), "2025-03..2026-10": ("2025-03-19", "2026-11")}
for k, (a, b) in periods.items():
    df = pd.concat([X.rename("x"), T.rename("t"), M.rename("m")], axis=1).dropna(); df = df[(df.index >= a) & (df.index < b)]
    m = sm.OLS(df.x, sm.add_constant(df[["m", "t"]])).fit(cov_type="HC0")
    out.append((k, len(df), df.x.corr(df.t), bk.pc(df.x, df.t, df.m), m.params["t"], m.tvalues["t"], 1e4 * df.t.std()))
for k in ["şok(yüksek vol)", "sakin/carry"]:
    df = pd.concat([X.rename("x"), T.rename("t"), M.rename("m"), reg.rename("r")], axis=1).dropna(); df = df[(df.r == k) & (df.index >= "2010")]
    m = sm.OLS(df.x.astype(float), sm.add_constant(df[["m", "t"]].astype(float))).fit(cov_type="HC0")
    out.append(("REJİM:" + k, len(df), df.x.astype(float).corr(df.t.astype(float)), bk.pc(df.x.astype(float), df.t.astype(float), df.m.astype(float)), m.params["t"], m.tvalues["t"], 1e4 * df.t.astype(float).std()))
R = pd.DataFrame(out, columns=["period", "n", "corr", "pc_xu100", "beta_TRY|XU", "t", "TRY_sd_bps"]).round(3)
R.to_csv(bk.RES + "/try_regimes.csv", index=False); print(R.to_string(index=False))
# asimetri: TL değer kaybı vs kazancı
df = pd.concat([X.rename("x"), T.rename("t"), M.rename("m")], axis=1).dropna(); df = df[df.index >= "2010"]
df["tp"] = df.t.clip(lower=0); df["tn"] = df.t.clip(upper=0)
m = sm.OLS(df.x, sm.add_constant(df[["m", "tp", "tn"]])).fit(cov_type="HC0")
print("Asimetri (XBANK~XU100+TRY+ +TRY-): b+ %.3f (t %.2f)  b- %.3f (t %.2f)" % (m.params.tp, m.tvalues.tp, m.params.tn, m.tvalues.tn))
# 2026 kayması: son 1y kısmi korelasyonlar
rows = []
for d in ["BZ=F", "CL=F", "^TNX", "BBVA.MC", "SAN.MC", "EUFN", "EMB", "EEM", "TUR", "^VIX", "GC=F", "TRY=X", "ES=F", "^STOXX50E", "DX-Y.NYB", "TPEIR.AT", "OTP.BD", "PKO.WA"]:
    r = bk.R(d)
    for lab, a, b in [("2025-11..2026-10", "2025-10-31", "2026-11"), ("2024-11..2025-10", "2024-10-31", "2025-10-31"), ("2021-2024", "2021", "2024-11")]:
        df = pd.concat([X.rename("x"), r.rename("d"), M.rename("m")], axis=1).dropna(); df = df[(df.index > a) & (df.index < b)]
        if len(df) < 60: continue
        w = df.clip(df.quantile(0.02), df.quantile(0.98), axis=1)  # winsorize sağlamlık
        rows.append((d, lab, len(df), df.x.corr(df.d), bk.pc(df.x, df.d, df.m), bk.pc(w.x, w.d, w.m), bk.pc(df.x, df.d, [df.m, T.reindex(df.index).fillna(0)])))
Q = pd.DataFrame(rows, columns=["driver", "period", "n", "corr", "pc_xu", "pc_xu_wins", "pc_xu_try"]).round(3)
Q.to_csv(bk.RES + "/shift_2026.csv", index=False)
print(Q.pivot(index="driver", columns="period", values="pc_xu").to_string())
print("winsorize 2025-11..2026-10:\n", Q[Q.period == "2025-11..2026-10"][["driver", "pc_xu", "pc_xu_wins", "pc_xu_try"]].to_string(index=False))
# Brent 2026: en büyük günleri çıkar
df = pd.concat([X.rename("x"), bk.R("BZ=F").rename("d"), M.rename("m")], axis=1).dropna(); df = df[df.index > "2025-10-31"]
top = df.d.abs().sort_values(ascending=False).index[:10]
print("Brent 2026 pc, en büyük 10 Brent günü hariç:", round(bk.pc(df.drop(top).x, df.drop(top).d, df.drop(top).m), 3), " | bu 10 gün:", [str(t.date()) for t in sorted(top)])
