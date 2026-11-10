"""Kardeş ve negatif kontrol: aynı kural başka 'öncü'lerle (madenciler, gümüş, enerji, EM...)."""
import numpy as np, pandas as pd
from adv_lib import *
pv = viop(); r = pv.v_ret; bh = (np.exp(r) - 1).iloc[1:]
rows = []
for tk, kind in [("GDX", "madenci ETF (kural)"), ("GDXJ", "küçük madenci ETF"), ("RING", "madenci ETF"), ("SGDM", "madenci ETF"), ("NEM", "madenci hisse"), ("AEM", "madenci hisse"), ("B", "madenci hisse (Barrick)"), ("KGC", "madenci hisse"), ("FNV", "royalty"), ("WPM", "royalty"),
                 ("SIL", "gümüş madenci"), ("SLV", "gümüş"), ("PPLT", "platin"), ("COPX", "bakır madenci"), ("XLE", "enerji hisse"), ("EEM", "gelişen piyasa"), ("TLT", "uzun tahvil"), ("HYG", "yüksek getirili tahvil")]:
    try:
        R = us_returns((tk, "GLD", "SPY"))
    except Exception as ex:
        print(tk, "yok", ex); continue
    if R.index[0] > pd.Timestamp("2015-01-01"): print(tk, "geç başlıyor", R.index[0].date())
    e, _ = rolling_resid(R, y=tk); E = e.rolling(10).sum(); pre = E[:"2017-12-31"].dropna()
    if len(pre) < 500: print(tk, "2018 öncesi veri az:", len(pre)); continue
    th = pre.quantile(.8); x, _ = map_us_to_viop(E, pv.index); s = (x > th).astype(float)
    p = pnl(position(s, 3), r, 5); al = alpha(p, bh)
    row = dict(oncu=tk, tur=kind, esik=round(th * 100, 2), n=int(s.sum()))
    for per, a, b in [("tam", None, None), ("18-26", "2018", None), ("18-24", "2018", "2024"), ("25-26", "2025", None)]:
        row[f"h3t_{per}"] = round(nw_diff(fwd(r, 3)[a:b], s[a:b], 10)["t"], 2); row[f"h5t_{per}"] = round(nw_diff(fwd(r, 5)[a:b], s[a:b], 10)["t"], 2)
    row["Sharpe"] = round(sharpe(p), 2); row["alfa_t"] = round(al[1], 2)
    rows.append(row)
pd.set_option("display.width", 250); print(pd.DataFrame(rows).set_index("oncu").to_string())
