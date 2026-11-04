"""Dolum varsayımına duyarlılık: uzlaşma yerine son işlem fiyatı (close) ve VWAP (gün) ile aynı kontrat getirisi."""
import numpy as np, pandas as pd, cl, ev, c1sig
p = cl.panel().sort_values(["code", "date"])
def alt_ret(und, field):
    f = cl.front(und); x = p[p["und"] == und][["date", "code", field]].copy()
    x["prev"] = x.groupby("code")[field].shift(1); x = x.set_index(["date", "code"])
    key = list(zip(f.index, f["code"]))
    v = x.reindex(key); r = np.log(v[field].values / v["prev"].values)
    s = pd.Series(r, index=f.index).reindex(cl.cal()); s[~np.isfinite(s)] = np.nan
    base = cl.fut_ret(und, und + ".IS" if und not in ("XU030",) else None); s[base.isna()] = np.nan
    s[(s - base).abs() > 0.05] = np.nan
    return s
u = ev.R("USDTRY"); g = ev.R("XAUUSD")
C = [("REF->TUPRS", c1sig.z_ref(), "TUPRS", 2, "raw", "2017-03-06"), ("ASX->EREGL", c1sig.z_asx(), "EREGL", 3, "hedged", "2017-03-06"),
     ("GOLD->TRALT", cl.zscale(g, 250, 100), "TRALT", 2, "hedged", "2018-12-17"), ("USD5->THYAO", cl.zscale(sum(u.shift(i) for i in range(5)), 250, 100), "THYAO", 3, "raw", "2017-03-06")]
for lab, z, und, h, lg, st in C:
    for fld in ("settle", "close", "vwap"):
        r = ev.R(und) if fld == "settle" else alt_ret(und, fld)
        m = ev.R("XU030") if fld == "settle" else alt_ret("XU030", fld)
        y = cl.fwd(r - cl.roll_beta(r, m, 250, 100) * m if lg == "hedged" else r, h); y = y[y.index >= st]
        tr = cl.trades(z, y, h, 1.0); s = cl.summ(tr, 8 + (3 if lg == "hedged" else 0))
        print(lab, fld, "n", s["n"], "net", round(s["net"], 1), "t", round(s["t"], 2), "2024-26", cl.periods(tr, 8)["2024-26"])
