import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e2_etf_leadlag")
from e2_common import *
d = load()
print(d.shape, d.index.min(), d.index.max())
for t in ["GLD","GDX","GDXJ","SPY","GLL","DUST","JDST","SLV"]:
    c = d[f"c_{t}"]; r = ret_of(d, t)
    first = c.first_valid_index()
    cc = c[c.index >= first]
    nmiss = cc.isna().sum(); zero = (r == 0).sum()
    big = r[r.abs() > 0.15]
    print(f"{t}: first {first.date()} missing_after_first {nmiss} zero_ret {zero} |r|>15%: {len(big)}", big.round(3).to_dict() if len(big) < 12 else len(big))
# close vs adjclose: ex-dividend jumps sanity for GDXJ
import pandas as pd
y = pd.read_parquet(f"{P}/yahoo/GDXJ.parquet")
f = (y.adjclose / y.close); jumps = f[f.pct_change().abs() > 0.002]
print("GDXJ adj factor changes (dividends):", jumps.index.strftime('%Y-%m-%d').tolist()[-12:])
# same-day dates where GDXJ missing but GLD present
for t in ["GDX","GDXJ","SPY"]:
    m = d["c_GLD"].notna() & d[f"c_{t}"].isna() & (d.index >= d[f"c_{t}"].first_valid_index())
    print(t, "missing while GLD present:", m.sum(), d.index[m][:10].tolist())
# compare Yahoo GLD close to SSGA NAV-implied? check stale closes: identical consecutive closes
for t in ["GLD","GDX","GDXJ"]:
    c = d[f"c_{t}"]; print(t, "identical consecutive closes:", int((c.diff() == 0).sum()))
