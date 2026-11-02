"""BIST fiyat marjı rejimini veriden doğrula: yıl/yarıyıl bazında |günlük değişim| kümelenmesi (limit-tavan/taban yığılmaları).
Tüm BIST hisseleri (data/daily/*.IS, X* endeksler hariç), ham 'c' (Yahoo kapanışı) ile log(c_t/c_{t-1})."""
import glob, os, numpy as np, pandas as pd, vers
fs = [f for f in glob.glob(vers.DATA + "/daily/*.IS.parquet") if not os.path.basename(f).startswith("X")]
R = []
for f in fs:
    d = pd.read_parquet(f); d.index = pd.DatetimeIndex(d["ldate"].values); d = d[~d.index.duplicated(keep="last")].sort_index()
    d = d[d["v"].fillna(0) > 0]
    r = np.log(d["c"] / d["c"].shift(1)).dropna(); R.append(r)
R = pd.concat(R); R = R[R.index >= "2008-01-01"]
p = np.exp(R) - 1
per = R.index.year.astype(str) + np.where(R.index.month <= 6, "H1", "H2")
# 2020'yi 03-13 civarında böl
per = np.where((R.index >= "2020-01-01") & (R.index < "2020-03-13"), "2020a(<03-13)", per)
per = np.where((R.index >= "2020-03-13") & (R.index < "2020-07-01"), "2020b(>=03-13)", per)
T = pd.DataFrame({"per": per, "p": p.values})
def bands(x):
    a = x.abs()
    return pd.Series({"n": len(x), "9.5-10.5%": int(((a > 0.095) & (a <= 0.105)).sum()), "10.5-19.5%": int(((a > 0.105) & (a <= 0.195)).sum()),
                      "19.5-20.5%": int(((a > 0.195) & (a <= 0.205)).sum()), ">20.5%": int((a > 0.205).sum()),
                      "up 10.5-19.5": int(((x > 0.105) & (x <= 0.195)).sum()), "max_up_p99.9": float(x.quantile(0.999))})
out = T.groupby("per")["p"].apply(bands).unstack()
out.to_csv(vers.RES + "/d3_limit_regime.csv")
pd.set_option("display.width", 200); print(out.to_string())
