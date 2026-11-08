import sys, numpy as np, pandas as pd
S="/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
sys.path.insert(0,f"{S}/code")
from lib_altin import load_spot, load_viop, hourly, split_stats, IS_END
sp=load_spot(); vp=load_viop()
sig=pd.read_parquet(f"{S}/out/a5_esz_artik/signals_spot.parquet")
# 1) duka file vs panel consistency at 15:00 (panel built before duka update)
for sym in ["DOLLARIDXUSD","USTBONDTRUSD","USA500IDXUSD","XAGUSD","XAUUSD"]:
    h=hourly(sym); h.index=h.index.tz_convert(None); print(sym, h.index.min(), h.index.max(), h.index.tz, len(h))
    c=h["c"]; s=c[c.index.hour==14]; s.index=s.index.normalize()
    col = "xau_p15" if sym=="XAUUSD" else f"dk_{sym}_p15"
    a=sp[col]; b=s.reindex(sp.index)
    m=a.notna()&b.notna()
    print("  panel vs current file 14:00 close: n",m.sum()," exact eq",(np.isclose(a[m],b[m],rtol=1e-9)).mean().round(4), " max rel diff",(np.abs(a[m]/b[m]-1)).max(), " panel-only",(a.notna()&b.isna()).sum()," file-only",(a.isna()&b.notna()).sum())
    # 12:00
    if sym=="XAUUSD":
        s12=c[c.index.hour==11]; s12.index=s12.index.normalize(); b12=s12.reindex(sp.index); m=sp.xau_p12.notna()&b12.notna()
        print("  xau_p12 vs 11:00 close eq", np.isclose(sp.xau_p12[m], b12[m]).mean(), "panel-only", (sp.xau_p12.notna()&b12.isna()).sum())
