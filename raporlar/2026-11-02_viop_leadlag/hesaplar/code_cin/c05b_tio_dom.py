"""cin - TIO=F (COMEX:TIO1!) ön ay = aylık ORTALAMA fiyatlı kontrat testi: ay içi volatilite çöküşü ve DCE demir cevheri ile
korelasyonun ay içi güne göre değişimi. Çıktı: code_cin/tio_dom.csv"""
import cin_lib as C, numpy as np, pandas as pd
t = C.price_local("TIO=F"); i = C.price_local("FUT:I"); f = C.price_local("FMG.AX")
P = pd.concat([t.rename("tio"), i.rename("dce"), f.rename("fmg")], axis=1, join="inner").dropna(); R = np.log(P).diff().dropna()
R = R[R.index >= "2019-01-01"]; b = pd.cut(R.index.day, [0, 7, 14, 21, 31], labels=["1-7", "8-14", "15-21", "22-31"])
rows = []
for k, g in R.groupby(b):
    rows.append({"gun": k, "n": len(g), "tio_absret_pct": 100 * g.tio.abs().mean(), "dce_absret_pct": 100 * g.dce.abs().mean(),
                 "corr_tio_dce": g.tio.corr(g.dce), "corr_fmg_dce": g.fmg.corr(g.dce)})
pd.DataFrame(rows).round(3).to_csv("tio_dom.csv", index=False); print(pd.DataFrame(rows).round(3).to_string(index=False))
