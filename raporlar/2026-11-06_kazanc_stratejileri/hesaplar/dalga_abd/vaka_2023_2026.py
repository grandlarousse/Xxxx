"""6) Vaka calismasi 2023-2026: French 49 sektor gunluk VW (son veri 2026-09-30).
Tema vekili sektorler: Chips (AI yari iletken), Hardw (AI donanim/depolama + Apple), ElcEq (elektrik ekipmani/guc),
Util (kamu hizmetleri/guc talebi), Mach (makine; turbin/sogutma kismen), Aero+Guns (savunma/uzay), Drugs (GLP-1),
Gold+Mines (altin/metal), Softw, BusSv, Fin/Banks, Steel, Oil, Coal.
Cikti: donem getirisi, piyasaya gore, en buyuk dusus, haftalik RS kirilim kurali islemleri (N52 + RS trailing %10), yil yil RS.
"""
import os
import numpy as np
import pandas as pd
from ff_load import load_daily49, load_ff_daily
from dalga_tanim import OUT
from swing_haftalik import run

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 40)
pd.set_option("display.max_rows", 300)

d = load_daily49()["vw"] / 100
ff = load_ff_daily() / 100
rm = (ff["Mkt-RF"] + ff["RF"]).reindex(d.index)
inds = ["Chips", "Hardw", "ElcEq", "Util", "Mach", "Aero", "Guns", "Drugs", "Gold", "Mines", "Softw", "BusSv", "Fin", "Banks", "Steel", "Oil", "Coal", "Cnstr", "Telcm", "Rtail"]
sub = d.loc["2022-10-01":, inds]
P = (1 + sub).cumprod()
M = (1 + rm.loc[sub.index]).cumprod()
RS = P.div(M, axis=0)

rows = []
for ind in inds:
    p = P[ind]; rs = RS[ind]
    a = p.loc["2022-12-30":]
    a = a / a.iloc[0]
    dd = (a / a.cummax() - 1)
    rsa = rs.loc["2022-12-30":] / rs.loc["2022-12-30":].iloc[0]
    row = dict(ind=ind, ret_2023_26=a.iloc[-1] - 1, rs_2023_26=rsa.iloc[-1] - 1, maxdd=dd.min(), maxdd_date=dd.idxmin().date(),
               rs_peak_date=rsa.idxmax().date(), rs_from_peak=rsa.iloc[-1] / rsa.max() - 1)
    for y in (2023, 2024, 2025):
        s = p.loc[str(y)]; s0 = p.loc[:f"{y-1}-12-31"].iloc[-1]
        m0 = M.loc[:f"{y-1}-12-31"].iloc[-1]
        row[f"r{y}"] = s.iloc[-1] / s0 - 1
        row[f"x{y}"] = (s.iloc[-1] / s0) / (M.loc[str(y)].iloc[-1] / m0) - 1
    s0 = p.loc[:"2025-12-31"].iloc[-1]; m0 = M.loc[:"2025-12-31"].iloc[-1]
    row["r2026ytd"] = p.iloc[-1] / s0 - 1
    row["x2026ytd"] = (p.iloc[-1] / s0) / (M.iloc[-1] / m0) - 1
    # 2026 icindeki en buyuk dusus
    b = p.loc["2025-12-31":]; row["dd2026"] = (b / b.cummax() - 1).min()
    rows.append(row)
T = pd.DataFrame(rows).set_index("ind")
mk = M.loc["2022-12-30":] / M.loc["2022-12-30":].iloc[0]
print("Piyasa 2023-01..2026-09:", round(mk.iloc[-1] - 1, 3), "maxDD", round((mk / mk.cummax() - 1).min(), 3))
print((T.select_dtypes("number") * 100).round(1).join(T[["maxdd_date", "rs_peak_date"]]).to_string())

# Haftalik RS kirilim kurali islemleri (N52, RS trailing 10%) 2023+ girisler
tr = run(N=52, exit_kind="rstrail", X=0.10)
tr = tr[(tr.entry >= "2022-10-01") & (tr.ind.isin(inds))].copy()
tr["abs"] = np.expm1(tr.labs); tr["rel"] = np.expm1(tr.lrel)
print("\nN52 + RS trailing %10 islemleri (2022-10 sonrasi giris):")
print(tr[["ind", "entry", "exit", "days", "abs", "rel"]].assign(abs=lambda x: (x["abs"] * 100).round(1), rel=lambda x: (x.rel * 100).round(1)).to_string())
tr2 = run(N=26, exit_kind="pxtrail", X=0.12)
tr2 = tr2[(tr2.entry >= "2022-10-01") & (tr2.ind.isin(inds))].copy()
tr2["abs"] = np.expm1(tr2.labs); tr2["rel"] = np.expm1(tr2.lrel)
print("\nN26 + fiyat trailing %12 islemleri (2022-10 sonrasi giris):")
print(tr2[["ind", "entry", "exit", "days", "abs", "rel"]].assign(abs=lambda x: (x["abs"] * 100).round(1), rel=lambda x: (x.rel * 100).round(1)).to_string())
summ = pd.concat([tr.groupby("ind").agg(n1=("abs", "size"), abs1=("abs", lambda x: np.prod(1 + x) - 1), rel1=("rel", lambda x: np.prod(1 + x) - 1)),
                  tr2.groupby("ind").agg(n2=("abs", "size"), abs2=("abs", lambda x: np.prod(1 + x) - 1), rel2=("rel", lambda x: np.prod(1 + x) - 1))], axis=1)
print("\nKural ozeti (bilesik, islemler toplami):")
print(summ.round(3).to_string())
T.to_pickle(os.path.join(OUT, "vaka_T.pkl"))
# Chips icin 2023-2026 tum >=15% dususler
for ind in ["Chips", "Hardw", "ElcEq", "Util", "Gold", "Aero"]:
    p = P[ind].loc["2022-12-30":]
    pk = p.cummax(); dd = p / pk - 1
    # dusus bolumleri
    eps = []
    inn = False
    for t, v in dd.items():
        if not inn and v <= -0.15:
            inn = True; start = pk.loc[:t].idxmax() if False else p.loc[:t][p.loc[:t] == pk.loc[t]].index[-1]; mn = v; mnd = t
        elif inn:
            if v < mn:
                mn, mnd = v, t
            if v == 0:
                eps.append((start.date(), mnd.date(), round(mn, 3), t.date())); inn = False
    if inn:
        eps.append((start.date(), mnd.date(), round(mn, 3), None))
    print(ind, ">=15% dususler (tepe, dip, derinlik, toparlanma):", eps)
