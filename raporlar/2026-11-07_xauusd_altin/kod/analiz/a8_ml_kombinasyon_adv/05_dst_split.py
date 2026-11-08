"""Hakem: seg_last1h mekanizma testi — ABD yaz saati (14-15 UTC = 10-11 ET) ve kış saati (9-10 ET) ayrı; VİOP ve spot."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/code")
from lib_altin import load_viop, load_spot, ic, backtest, fwd
d = load_viop(); s = load_spot()
def us_dst(idx):
    t = pd.DatetimeIndex(idx).tz_localize("UTC") + pd.Timedelta(hours=14)
    return pd.Series(t.tz_convert("America/New_York").map(lambda z: z.dst() != pd.Timedelta(0)), index=idx).astype(bool)
for nm, df, r, a in (("VİOP 2017+", d, d.v_ret, "2017-03"), ("spot 2010-16", s.loc[:"2016"], s.s_ret.loc[:"2016"], "2010"), ("spot 2017+", s.loc["2017":], s.s_ret.loc["2017":], "2017")):
    x = np.log(df.xau_p15 / df.xau_p14); dst = us_dst(df.index)
    for h in (1, 3, 5):
        y = fwd(r, h)
        print(nm, "h", h, "yaz(DST) t", round(ic(x[dst], y[dst], max(h, 5))["t"], 2), "n", int(dst.sum()), "| kış t", round(ic(x[~dst], y[~dst], max(h, 5))["t"], 2), "n", int((~dst).sum()))
